"""
Payment Guard & Family Co-Sign Engine
Prevents extortion money transfers during scam calls.
Maintains lock states and manages the family co-signing release flow.
"""

import uuid
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timezone

logger = logging.getLogger("payment_guard")


class PaymentGuard:
    """
    Financial firewall that halts unauthorized transfers during active scam events.
    Requires secondary authorization (family co-sign) before releasing locked payments.
    """

    def __init__(self):
        self._is_locked: bool = False
        self._active_lock_id: Optional[str] = None
        self._lock_reason: Optional[str] = None
        self._blocked_attempts: list = []
        self._cosign_status: str = "NONE"  # NONE, PENDING, APPROVED, REJECTED
        self._family_approver: Optional[str] = None

    @property
    def is_locked(self) -> bool:
        return self._is_locked

    def lock_transfers(self, reason: str, incident_id: str = None) -> str:
        """Locks all outgoing transactions immediately."""
        self._is_locked = True
        self._active_lock_id = f"lock_{uuid.uuid4().hex[:10]}"
        self._lock_reason = reason
        self._cosign_status = "PENDING"
        logger.warning(f"🔒 [PAYMENT LOCKED] Lock ID: {self._active_lock_id} | Reason: {reason}")
        return self._active_lock_id

    def unlock_transfers(self, authorized_by: str) -> bool:
        """Unlocks transactions after authorized family co-sign."""
        self._is_locked = False
        self._cosign_status = "APPROVED"
        self._family_approver = authorized_by
        logger.info(f"🔓 [PAYMENT UNLOCKED] Co-signed and released by: {authorized_by}")
        return True

    def process_payment_attempt(
        self,
        amount_inr: float,
        recipient_account: str,
        recipient_name: str = "RBI Escrow Verification"
    ) -> Dict[str, Any]:
        """
        Evaluates an outgoing transfer attempt against the active payment guard.
        """
        now = datetime.now(timezone.utc).isoformat()
        if self._is_locked:
            attempt_record = {
                "timestamp": now,
                "amount_inr": amount_inr,
                "recipient_account": recipient_account,
                "recipient_name": recipient_name,
                "status": "BLOCKED",
                "lock_id": self._active_lock_id,
                "reason": self._lock_reason or "Digital arrest scam intervention active"
            }
            self._blocked_attempts.append(attempt_record)
            logger.warning(f"🛑 [TRANSFER BLOCKED] Attempt of ₹{amount_inr:,.2f} to {recipient_account} was REJECTED.")
            return {
                "success": False,
                "blocked": True,
                "message": (
                    f"TRANSACTION BLOCKED BY MIRAGE-SHIELD: Outgoing payment of ₹{amount_inr:,.2f} "
                    f"to '{recipient_name}' is locked. Suspected digital arrest extortion."
                ),
                "record": attempt_record,
                "cosign_required": True
            }

        return {
            "success": True,
            "blocked": False,
            "message": f"Payment of ₹{amount_inr:,.2f} processed successfully.",
            "cosign_required": False
        }

    def get_status(self) -> Dict[str, Any]:
        return {
            "is_locked": self._is_locked,
            "active_lock_id": self._active_lock_id,
            "lock_reason": self._lock_reason,
            "cosign_status": self._cosign_status,
            "family_approver": self._family_approver,
            "blocked_count": len(self._blocked_attempts),
            "recent_blocked_attempts": self._blocked_attempts[-5:]
        }


payment_guard = PaymentGuard()
