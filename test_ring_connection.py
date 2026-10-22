"""
Official Ring Partner API Connection Tester
Allows testing live credentials against api.amazonvision.com safely without leaking secrets.
Reads RING_ACCESS_TOKEN from environment or .env, parses official JSON:API data array,
and reports actual HTTP status codes, error details, and device listings.

Includes JWT pre-flight expiry detection and retry with backoff for transient network errors.
"""

import os
import sys
import json
import base64
import time
from pathlib import Path
from datetime import datetime, timezone, timedelta

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

import requests

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Lightweight zero-dependency .env loader
def _load_project_env(override: bool = False):
    candidates = [
        PROJECT_ROOT / ".env",
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


def _get_active_token(cli_token: str = None) -> str:
    if cli_token:
        return cli_token.strip()
    _load_project_env(override=True)
    token = os.getenv("RING_ACCESS_TOKEN", "").strip()
    if not token:
        token = os.getenv("RING_API_TOKEN", "").strip()
    if token in ("mock_developer_playground_token", "your_ring_playground_or_oauth_token_here"):
        return ""
    return token


def _check_jwt_expiry(token: str):
    """Pre-flight JWT expiry check. Returns (is_expired, exp_datetime_or_None)."""
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return False, None
        payload = parts[1]
        payload += "=" * (4 - len(payload) % 4)
        decoded = json.loads(base64.urlsafe_b64decode(payload))
        exp_ts = decoded.get("exp")
        if exp_ts:
            exp_dt = datetime.fromtimestamp(exp_ts, tz=timezone.utc)
            now = datetime.now(timezone.utc)
            return now >= exp_dt, exp_dt
    except Exception:
        pass
    return False, None


def _save_token_to_env(saved_token: str):
    """Safely updates or adds RING_ACCESS_TOKEN in .env."""
    env_file = PROJECT_ROOT / ".env"
    lines = []
    found = False
    if env_file.is_file():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("RING_ACCESS_TOKEN="):
                lines.append(f"RING_ACCESS_TOKEN={saved_token.strip()}")
                found = True
            else:
                lines.append(line)
    if not found:
        lines.append(f"RING_ACCESS_TOKEN={saved_token.strip()}")
    env_file.write_text("\n".join(lines) + "\n", encoding="utf-8")


def test_connection(token: str = None, base_url: str = None):
    token = _get_active_token(token)
    base_url = (base_url or RING_API_BASE_URL).rstrip("/")

    print("=" * 65)
    print("🔔 RING PARTNER API VERIFICATION TEST")
    print(f"   Target URL: {base_url}/v1/devices")
    print("=" * 65)

    if not token:
        print("\n⚠️  No valid live token found in environment.")
        print("   RING_ACCESS_TOKEN is not set in environment or .env.")
        print("   Status: RUNNING IN LOCAL SANDBOX FIXTURES MODE.")
        print("\n   To test with a live token from the Ring Developer Playground:")
        print("   1. Open .env and set: RING_ACCESS_TOKEN=<your_30_min_playground_token>")
        print("   2. Run: python test_ring_connection.py <optional_token>")
        return False

    # Mask token for safe printing
    masked_token = token[:6] + "..." + token[-4:] if len(token) > 12 else "***"
    print(f"   Using Token: {masked_token}")

    # Pre-flight JWT expiry check — avoid wasted network round-trip
    expired, exp_dt = _check_jwt_expiry(token)
    if expired and exp_dt:
        now = datetime.now(timezone.utc)
        ago_secs = (now - exp_dt).total_seconds()
        if ago_secs < 3600:
            ago_str = f"{ago_secs:.0f}s ago"
        else:
            ago_str = f"{ago_secs/3600:.1f}h ago"
        print(f"\n   ⏰ TOKEN EXPIRED (pre-flight JWT check)")
        print(f"      Expired at: {exp_dt.strftime('%Y-%m-%d %H:%M:%S UTC')} ({ago_str})")
        print(f"      Ring Playground tokens are valid for only 30 minutes.")
        print(f"      → Generate a fresh token at the Ring Developer Portal Playground.")
        print(f"      → Update .env: RING_ACCESS_TOKEN=<new_token>")
        return False

    if exp_dt:
        ttl = (exp_dt - datetime.now(timezone.utc)).total_seconds()
        print(f"   Token TTL: {ttl:.0f}s remaining (expires {exp_dt.strftime('%H:%M:%S UTC')})")

    print("   Sending GET /v1/devices request (timeout: 10s connect, 30s read)...")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": "MIRAGE-SHIELD-Verification/1.0",
        "Accept": "application/json"
    }

    max_retries = 1
    for attempt in range(max_retries + 1):
        try:
            start = time.time()
            resp = requests.get(f"{base_url}/v1/devices", headers=headers, timeout=(10, 30))
            elapsed = time.time() - start
            print(f"\n   HTTP Status Code: {resp.status_code} ({resp.reason}) [{elapsed:.1f}s]")

            if resp.status_code == 200:
                body = resp.json()
                devices = body.get("data", [])
                print(f"   ✔ SUCCESS! Retrieved {len(devices)} device(s) from official Ring API.")
                for d in devices:
                    attrs = d.get("attributes", {})
                    name = attrs.get("name", "Unnamed Device")
                    kind = attrs.get("kind", "Unknown Kind")
                    print(f"      - Device ID: {d.get('id')} | Name: '{name}' | Kind: {kind}")
                    if "Playground" in name:
                        print("        [Ring Developers Playground Virtual Device Verified]")
                
                # Auto-save verified token to .env if passed from CLI
                if token and token != os.getenv("RING_ACCESS_TOKEN", ""):
                    try:
                        _save_token_to_env(token)
                        print("\n   💾 Automatically saved verified token to .env for MIRAGE-SHIELD!")
                    except Exception as e:
                        print(f"   (Could not auto-save to .env: {e})")
                return True
            elif resp.status_code == 401:
                print("   ❌ FAILED: 401 Unauthorized.")
                print("      The Ring Developer Playground token has expired or is invalid.")
                print("      (Note: Developer Playground tokens expire every 30 minutes).")
                return False
            elif resp.status_code == 403:
                print("   ❌ FAILED: 403 Forbidden.")
                print("      The token does not have permission to query /v1/devices.")
                return False
            else:
                print(f"   ❌ FAILED: Response from Ring API: {resp.text[:200]}")
                return False
        except requests.exceptions.RequestException as e:
            if attempt < max_retries:
                wait = 2 ** attempt
                print(f"\n   ⚠️ Network error ({type(e).__name__}), retrying in {wait}s... [{attempt+1}/{max_retries+1}]")
                time.sleep(wait)
                continue
            print(f"\n   ❌ NETWORK / CONNECTION ERROR (after {max_retries+1} attempts): {e}")
            return False

    return False


if __name__ == "__main__":
    cli_token = sys.argv[1] if len(sys.argv) > 1 else None
    test_connection(token=cli_token)
