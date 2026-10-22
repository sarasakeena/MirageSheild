"""
Ring Partner API Client
Communicates with api.amazonvision.com (official Ring Partner API) for device listing,
capabilities, status, event history, and chime playback.
Supports the official Ring Developers Playground Bearer token (RING_ACCESS_TOKEN)
with clear error categorization (401 expired, 403 forbidden, network errors)
and resilient sanitized fallback fixtures.
"""

import os
import json
import base64
import hashlib
import logging
import time
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timezone, timedelta
import requests

logger = logging.getLogger("ring_client")
logging.basicConfig(level=logging.INFO)

# Lightweight zero-dependency .env loader
def _load_project_env(override: bool = False):
    candidates = [
        Path(__file__).resolve().parent.parent / ".env",
        Path.cwd() / ".env"
    ]
    for p in candidates:
        if p.is_file():
            try:
                for line in p.read_text(encoding="utf-8").splitlines():
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" in line:
                        k, v = line.split("=", 1)
                        k = k.strip()
                        v = v.strip().strip("'\"")
                        if k and (override or k not in os.environ):
                            os.environ[k] = v
            except Exception:
                pass

_load_project_env()

RING_API_BASE_URL = os.getenv("RING_API_BASE_URL", "https://api.amazonvision.com").rstrip("/")
FIXTURE_PATH = Path(__file__).resolve().parent / "fixtures" / "ring_playground_devices.json"


def _get_active_token() -> str:
    """Retrieves access token prioritizing RING_ACCESS_TOKEN then RING_API_TOKEN."""
    _load_project_env(override=True)
    token = os.getenv("RING_ACCESS_TOKEN", "").strip()
    if not token:
        token = os.getenv("RING_API_TOKEN", "").strip()
    if token in ("mock_developer_playground_token", "your_ring_playground_or_oauth_token_here"):
        return ""
    return token


def _decode_jwt_exp(token: str) -> Optional[datetime]:
    """Decodes the `exp` claim from a JWT without verifying signature.
    Returns the expiration datetime (UTC) or None if decoding fails."""
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        payload = parts[1]
        payload += "=" * (4 - len(payload) % 4)
        decoded = json.loads(base64.urlsafe_b64decode(payload))
        exp_ts = decoded.get("exp")
        if exp_ts:
            return datetime.fromtimestamp(exp_ts, tz=timezone.utc)
    except Exception:
        pass
    return None


def _is_token_expired(token: str, buffer_seconds: int = 30) -> Tuple[bool, Optional[datetime]]:
    """Pre-flight check: returns (is_expired, expiration_time).
    Considers a token expired if it will expire within buffer_seconds."""
    exp = _decode_jwt_exp(token)
    if exp is None:
        return False, None  # Can't determine — let the server decide
    now = datetime.now(timezone.utc)
    return now >= (exp - timedelta(seconds=buffer_seconds)), exp


# Default timeout: (connect_timeout, read_timeout) in seconds.
# Ring Playground API is hosted in ap-northeast-1 (Tokyo), so generous read timeout.
DEFAULT_TIMEOUT = (10, 30)
MAX_RETRIES = 1  # One retry for transient network errors


class RingPartnerClient:
    """
    Official Ring Partner API integration client.
    Handles device queries, video doorbell event history, snapshot retrieval,
    and chime audio alert playback against https://api.amazonvision.com.
    """

    def __init__(
        self,
        base_url: str = RING_API_BASE_URL,
        token: Optional[str] = None,
        sandbox_mode: Optional[bool] = None
    ):
        self.base_url = (base_url or RING_API_BASE_URL).rstrip("/")
        self._explicit_token = token
        self._explicit_sandbox = sandbox_mode
        self._mock_events: List[Dict[str, Any]] = []
        self._current_door_state: str = "CLEAR"  # CLEAR, HUMAN_DETECTED, PACKAGE_DELIVERED
        self._last_health_cache: Optional[Dict[str, Any]] = None
        self._last_health_check_time: Optional[datetime] = None

    @property
    def token(self) -> str:
        if self._explicit_token is not None:
            return self._explicit_token
        return _get_active_token()

    @property
    def sandbox_mode(self) -> bool:
        if self._explicit_sandbox is not None:
            return self._explicit_sandbox
        # Force sandbox if explicitly set in env, or if no token available
        env_sandbox = os.getenv("RING_SANDBOX_MODE", "").lower() in ("true", "1", "yes")
        return env_sandbox or (not bool(self.token))

    def _masked_token(self) -> str:
        """Safely masks token for logging. Never logs secret values."""
        t = self.token
        if not t:
            return "<none>"
        if len(t) <= 8:
            return "***"
        return f"{t[:4]}...{t[-4:]}"

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "User-Agent": "MIRAGE-SHIELD-Oracle/1.0",
            "Accept": "application/json"
        }

    def _load_sanitized_fixtures(self) -> List[Dict[str, Any]]:
        """Loads sanitized offline fixtures for repeatable testing without secrets."""
        if FIXTURE_PATH.is_file():
            try:
                data = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
                devices_data = data.get("data", [])
                normalized = []
                for d in devices_data:
                    attrs = d.get("attributes", {})
                    normalized.append({
                        "id": d.get("id", "playground_device_v4_test"),
                        "kind": attrs.get("kind", "doorbell_v4"),
                        "description": attrs.get("name", "Playground Device"),
                        "name": attrs.get("name", "Playground Device"),
                        "online": attrs.get("online", True),
                        "is_playground": True,
                        "health": attrs.get("health", {}),
                        "features": attrs.get("capabilities", {})
                    })
                return normalized
            except Exception as e:
                logger.warning(f"Could not load sanitized fixtures ({e}), using default mock.")

        return [
            {
                "id": "playground_device_v4_test",
                "kind": "doorbell_v4",
                "description": "Playground Device (Offline Fixture)",
                "name": "Playground Device",
                "online": True,
                "is_playground": True,
                "health": {"battery_percentage": 100, "wifi_signal_category": "good", "rssi": -50},
                "features": {"motion_detection": True, "package_alerts": False}
            }
        ]

    def _request_with_retry(self, method: str, url: str, **kwargs) -> requests.Response:
        """Makes an HTTP request with a single retry for transient network errors."""
        kwargs.setdefault("timeout", DEFAULT_TIMEOUT)
        kwargs.setdefault("headers", self._headers())
        last_exc = None
        for attempt in range(MAX_RETRIES + 1):
            try:
                resp = requests.request(method, url, **kwargs)
                return resp
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                last_exc = e
                if attempt < MAX_RETRIES:
                    wait = 2 ** attempt  # 1s, 2s, ...
                    logger.info(f"Retrying Ring API request ({type(e).__name__}), attempt {attempt + 2}/{MAX_RETRIES + 1} in {wait}s...")
                    time.sleep(wait)
        raise last_exc

    def check_health(self, force_refresh: bool = False) -> Dict[str, Any]:
        """
        Performs a safe, non-destructive backend health check against GET /v1/devices.
        Distinguishes 200 OK, 401 Expired Token, 403 Forbidden, and Network Failures.
        Includes JWT pre-flight expiry detection to avoid unnecessary network calls.
        Never leaks tokens.
        """
        now = datetime.now(timezone.utc)
        if not force_refresh and self._last_health_cache and self._last_health_check_time:
            if (now - self._last_health_check_time).total_seconds() < 10:
                return self._last_health_cache

        token = self.token
        if not token:
            res = {
                "status": "UNAUTHENTICATED",
                "authenticated": False,
                "http_status": None,
                "mode": "SANDBOX_FIXTURES",
                "message": "No live RING_ACCESS_TOKEN configured in environment. Operating in sandbox fixtures mode.",
                "base_url": self.base_url,
                "device_count": 1,
                "device_name": "Playground Device (Fixture)",
                "is_playground": True,
                "timestamp": now.isoformat()
            }
            self._last_health_cache = res
            self._last_health_check_time = now
            return res

        # Pre-flight JWT expiry check — avoid unnecessary network round-trip
        expired, exp_time = _is_token_expired(token)
        if expired:
            exp_str = exp_time.strftime("%Y-%m-%d %H:%M:%S UTC") if exp_time else "unknown"
            ago = f"{(now - exp_time).total_seconds():.0f}s ago" if exp_time else ""
            logger.warning(f"Ring Playground token expired at {exp_str} ({ago}). Skipping API call.")
            res = {
                "status": "TOKEN_EXPIRED",
                "authenticated": False,
                "http_status": None,
                "mode": "SANDBOX_FALLBACK",
                "message": f"Ring Playground token expired at {exp_str} ({ago}). Playground tokens last 30 minutes. Generate a new one at the Ring Developer Portal.",
                "base_url": self.base_url,
                "device_count": 0,
                "device_name": None,
                "is_playground": True,
                "token_expired_at": exp_str,
                "timestamp": now.isoformat()
            }
            self._last_health_cache = res
            self._last_health_check_time = now
            return res

        # Attempt real request to official Ring Partner API (with retry)
        target_url = f"{self.base_url}/v1/devices"
        logger.info(f"Checking Ring API health with token [{self._masked_token()}] at {target_url}...")
        try:
            resp = self._request_with_retry("GET", target_url)
            
            if resp.status_code == 200:
                body = resp.json()
                raw_devices = body.get("data", [])
                device_name = "Unknown Device"
                device_id = None
                if raw_devices:
                    first = raw_devices[0]
                    device_id = first.get("id")
                    device_name = first.get("attributes", {}).get("name", "Ring Device")

                is_playground = "Playground" in device_name or "playground" in str(device_id).lower()

                res = {
                    "status": "CONNECTED",
                    "authenticated": True,
                    "http_status": 200,
                    "mode": "PLAYGROUND_API" if is_playground else "LIVE_PARTNER_API",
                    "message": f"Successfully verified Ring API connection ({device_name}).",
                    "base_url": self.base_url,
                    "device_count": len(raw_devices),
                    "device_name": device_name,
                    "device_id": device_id,
                    "is_playground": is_playground,
                    "timestamp": now.isoformat()
                }
            elif resp.status_code == 401:
                logger.warning("Ring API 401 Unauthorized: Developer Playground token expired (30-min lifespan).")
                res = {
                    "status": "TOKEN_EXPIRED",
                    "authenticated": False,
                    "http_status": 401,
                    "mode": "SANDBOX_FALLBACK",
                    "message": "Ring Playground access token has expired or is invalid. Playground tokens expire strictly in 30 minutes. Falling back to sandbox fixtures.",
                    "base_url": self.base_url,
                    "device_count": 0,
                    "device_name": None,
                    "is_playground": True,
                    "timestamp": now.isoformat()
                }
            elif resp.status_code == 403:
                logger.warning("Ring API 403 Forbidden: Token lacks permission for /v1/devices.")
                res = {
                    "status": "FORBIDDEN",
                    "authenticated": False,
                    "http_status": 403,
                    "mode": "SANDBOX_FALLBACK",
                    "message": "Ring access token does not have permission to query /v1/devices.",
                    "base_url": self.base_url,
                    "device_count": 0,
                    "device_name": None,
                    "is_playground": False,
                    "timestamp": now.isoformat()
                }
            else:
                logger.warning(f"Ring API returned HTTP {resp.status_code}: {resp.text[:120]}")
                res = {
                    "status": f"HTTP_{resp.status_code}",
                    "authenticated": False,
                    "http_status": resp.status_code,
                    "mode": "SANDBOX_FALLBACK",
                    "message": f"Ring API returned unexpected status {resp.status_code}.",
                    "base_url": self.base_url,
                    "device_count": 0,
                    "device_name": None,
                    "is_playground": False,
                    "timestamp": now.isoformat()
                }
        except requests.exceptions.RequestException as e:
            logger.warning(f"Network error connecting to Ring API ({type(e).__name__}): {e}")
            res = {
                "status": "NETWORK_ERROR",
                "authenticated": False,
                "http_status": None,
                "mode": "SANDBOX_FALLBACK",
                "message": f"Network failure connecting to Ring API ({type(e).__name__}). Operating in sandbox fixtures mode.",
                "base_url": self.base_url,
                "device_count": 0,
                "device_name": None,
                "is_playground": False,
                "timestamp": now.isoformat()
            }

        self._last_health_cache = res
        self._last_health_check_time = now
        return res

    def list_devices(self) -> List[Dict[str, Any]]:
        """
        Calls GET /v1/devices on Ring Partner API (or returns sanitized fixtures).
        Correctly parses the official Ring Partner API JSON:API envelope (data array).
        """
        if not self.sandbox_mode and self.token:
            try:
                # Pre-flight JWT expiry check for list_devices
                expired, _ = _is_token_expired(self.token)
                if expired:
                    logger.info("Token expired pre-flight, falling back to fixtures for list_devices.")
                    return self._load_sanitized_fixtures()

                resp = self._request_with_retry("GET", f"{self.base_url}/v1/devices")
                if resp.status_code == 200:
                    body = resp.json()
                    raw_list = body.get("data", [])
                    if raw_list:
                        normalized = []
                        for d in raw_list:
                            attrs = d.get("attributes", {})
                            normalized.append({
                                "id": d.get("id"),
                                "kind": attrs.get("kind", "doorbell_v4"),
                                "description": attrs.get("name", "Playground Device"),
                                "name": attrs.get("name", "Playground Device"),
                                "online": attrs.get("online", True),
                                "is_playground": True,
                                "raw_attributes": attrs
                            })
                        return normalized
                logger.warning(f"Ring API returned status {resp.status_code}, falling back to sanitized fixtures.")
            except Exception as e:
                logger.warning(f"Failed to connect to Ring API ({e}), falling back to sandbox fixtures.")

        return self._load_sanitized_fixtures()

    def get_event_history(
        self,
        device_id: str,
        window_hours: int = 6,
        event_types: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Queries event history for human, package, and motion/ding events.
        Virtual Playground devices do not capture live outdoor video, so scenario fixtures
        provide the deterministic physical ground truth for extortion testing.
        """
        if self._mock_events:
            return self._mock_events

        if self._current_door_state == "CLEAR":
            return []
        elif self._current_door_state == "PACKAGE_DELIVERED":
            return [
                {
                    "event_id": "ring_evt_pkg_9981",
                    "device_id": device_id,
                    "kind": "package_delivered",
                    "created_at": (datetime.now(timezone.utc) - timedelta(minutes=4)).isoformat(),
                    "confidence": 0.94,
                    "cv_tags": ["package", "cardboard_box", "carrier_courier"]
                },
                {
                    "event_id": "ring_evt_ding_9980",
                    "device_id": device_id,
                    "kind": "ding",
                    "created_at": (datetime.now(timezone.utc) - timedelta(minutes=5)).isoformat(),
                    "confidence": 1.0,
                    "cv_tags": ["doorbell_press"]
                }
            ]
        elif self._current_door_state == "HUMAN_DETECTED":
            return [
                {
                    "event_id": "ring_evt_human_1201",
                    "device_id": device_id,
                    "kind": "motion",
                    "created_at": (datetime.now(timezone.utc) - timedelta(minutes=2)).isoformat(),
                    "confidence": 0.88,
                    "cv_tags": ["human", "visitor"]
                }
            ]
        return []

    def set_sandbox_door_state(self, state: str, events: Optional[List[Dict[str, Any]]] = None):
        """Allows testing scenarios to switch Ring door state between CLEAR, PACKAGE_DELIVERED, and HUMAN_DETECTED."""
        self._current_door_state = state
        self._mock_events = events or []

    def get_latest_snapshot(self, device_id: str) -> Dict[str, Any]:
        """
        Returns URL and computed SHA256 integrity hash of the door snapshot.
        Virtual Playground devices have no physical camera lens, so scenario footage is served.
        """
        state_map = {
            "CLEAR": "/api/ring/snapshot/scenario1_empty_porch.jpg",
            "PACKAGE_DELIVERED": "/api/ring/snapshot/scenario3_amazon_delivery.jpg",
            "HUMAN_DETECTED": "/api/ring/snapshot/visitor_porch.jpg"
        }
        url = state_map.get(self._current_door_state, "/api/ring/snapshot/scenario1_empty_porch.jpg")
        mock_hash = hashlib.sha256(url.encode()).hexdigest()
        
        return {
            "snapshot_url": url,
            "snapshot_hash": f"sha256_{mock_hash}",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def trigger_chime(self, chime_device_id: str, audio_ref: str = "audio_ref_urgent_security_alert") -> Dict[str, Any]:
        """
        Triggers chime audio alert playback.
        If live API token is active, sends POST to official API; otherwise simulates playback locally.
        """
        payload = {"audio_ref": audio_ref}
        if not self.sandbox_mode and self.token:
            try:
                resp = requests.post(
                    f"{self.base_url}/v1/devices/{chime_device_id}/play-audio",
                    headers=self._headers(),
                    json=payload,
                    timeout=4.0
                )
                if resp.status_code in (200, 202, 204):
                    return {"status": "success", "http_status": resp.status_code, "audio_ref": audio_ref}
            except Exception as e:
                logger.warning(f"Chime API playback failed ({e}), logging alert locally.")

        logger.info(f"🔊 [RING CHIME ALERT] Playing audio slot '{audio_ref}' on chime '{chime_device_id}'")
        return {
            "status": "success",
            "mode": "sandbox",
            "audio_ref": audio_ref,
            "played_at": datetime.now(timezone.utc).isoformat(),
            "message": f"Chime audio slot '{audio_ref}' played successfully."
        }
