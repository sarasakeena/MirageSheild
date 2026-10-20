"""
Ring Webhook Handler with HMAC-SHA256 Signature Verification
Handles incoming Ring event notifications (motion, ding, package_delivered, live_view)
verifies cryptographic authenticity, responds HTTP 200 immediately, and dispatches asynchronously.
"""

import hmac
import hashlib
import os
import logging
from typing import Dict, Any, Tuple
import asyncio

logger = logging.getLogger("ring_webhook")
RING_WEBHOOK_SECRET = os.getenv("RING_WEBHOOK_SECRET", "mirage_shield_hmac_secret_2026")


def verify_ring_signature(payload_bytes: bytes, signature_header: str, secret: str = RING_WEBHOOK_SECRET) -> bool:
    """
    Verifies Ring webhook HMAC-SHA256 signature header.
    Format is typically: 'sha256=<hex_digest>' or raw hex string.
    """
    if not signature_header:
        return False
        
    expected_prefix = "sha256="
    if signature_header.startswith(expected_prefix):
        provided_sig = signature_header[len(expected_prefix):]
    else:
        provided_sig = signature_header

    mac = hmac.new(secret.encode("utf-8"), payload_bytes, hashlib.sha256)
    computed_sig = mac.hexdigest()
    
    # Constant-time comparison to prevent timing attacks
    return hmac.compare_digest(computed_sig, provided_sig)


class RingWebhookDispatcher:
    """
    Asynchronous event dispatcher for Ring webhooks.
    """

    def __init__(self):
        self._listeners = []

    def register_listener(self, callback):
        self._listeners.append(callback)

    async def dispatch_event(self, event_data: Dict[str, Any]):
        """Runs registered listeners asynchronously so webhook returns HTTP 200 instantly."""
        for listener in self._listeners:
            try:
                if asyncio.iscoroutinefunction(listener):
                    asyncio.create_task(listener(event_data))
                else:
                    listener(event_data)
            except Exception as e:
                logger.error(f"Error executing webhook listener: {e}")


webhook_dispatcher = RingWebhookDispatcher()
