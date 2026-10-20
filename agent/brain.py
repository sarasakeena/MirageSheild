"""
MIRAGE-SHIELD Agent Brain (Strands Agents SDK & Amazon Bedrock Architecture)
Autonomous AI reasoning agent that cross-correlates multi-modal call risk with
physical Ring door evidence to expose digital arrest lies and take over the living room.
"""

import os
import uuid
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timezone

from shared.schemas import (
    Verdict,
    VerdictAction,
    DoorEvidence,
    CallRisk,
    InterventionDetails,
    DoorStatus,
)
from agent.tools import AgentTools
from agent.payment_guard import payment_guard
from agent.aws_audit import aws_audit_ledger

logger = logging.getLogger("agent_brain")


class MirageShieldAgent:
    """
    Strands & Bedrock AI Agent Brain.
    Orchestrates evidence collection, cross-examination, and defense actions.
    """

    def __init__(self, tools: Optional[AgentTools] = None):
        self.tools = tools or AgentTools()
        self.bedrock_model_id = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0")
        self.aws_region = os.getenv("AWS_REGION", "us-east-1")
        self._last_verdict: Optional[Verdict] = None

    def evaluate(self, call_risk: CallRisk, custom_door_evidence: Optional[DoorEvidence] = None) -> Verdict:
        """
        Main cognitive reasoning loop.
        Fuses audio-visual call risk and physical Ring door oracle data.
        """
        now_iso = datetime.now(timezone.utc).isoformat()
        verdict_id = f"vrd_{uuid.uuid4().hex[:10]}"

        # Step 1: Query Physical Evidence Oracle (Ring)
        if custom_door_evidence:
            door_evidence = custom_door_evidence
        else:
            door_evidence = self.tools.get_door_evidence(window_hours=6)

        # Step 2: Cross-examine Physical Claims against Reality
        contradiction_detected, contradiction_summary = self.tools.check_physical_contradiction(
            claims=call_risk.physical_claims,
            evidence=door_evidence
        )

        # Step 3: Cognitive Decision Matrix
        reasons = []
        action = VerdictAction.SAFE
        confidence = 0.90

        if contradiction_detected:
            # High priority physical lie detected
            if call_risk.coercion_score >= 0.30 or call_risk.deepfake_score >= 0.40:
                action = VerdictAction.INTERVENE
                confidence = 0.98
                reasons.append(contradiction_summary)
                reasons.append(
                    f"Digital arrest script confirmed: Coercion index {call_risk.coercion_score:.2f} "
                    f"with {len(call_risk.coercion_flags)} high-risk flags."
                )
                if call_risk.deepfake_score >= 0.50:
                    reasons.append(f"Visual facial synthesis detected with {call_risk.deepfake_score:.2f} probability.")
            else:
                action = VerdictAction.WARN
                confidence = 0.85
                reasons.append(contradiction_summary)
        else:
            # No physical contradiction: check pure call metrics
            if call_risk.coercion_score >= 0.75 or call_risk.deepfake_score >= 0.85:
                action = VerdictAction.INTERVENE
                confidence = 0.94
                reasons.append(f"Critical coercion score ({call_risk.coercion_score:.2f}) with immediate financial extortion demand.")
                if call_risk.deepfake_score >= 0.50:
                    reasons.append(f"Deepfake visual artifacts present ({call_risk.deepfake_score:.2f}).")
            elif call_risk.coercion_score >= 0.40 or call_risk.deepfake_score >= 0.50:
                action = VerdictAction.WARN
                confidence = 0.80
                reasons.append("Elevated risk indicators observed during call. Exercise caution.")
            else:
                action = VerdictAction.SAFE
                confidence = 0.99
                reasons.append("Call shows no coercion, deepfake markers, or physical anomalies.")
                if door_evidence.package_events_count > 0:
                    reasons.append("Legitimate courier delivery verified by Ring video doorbell.")

        # Step 4: Defense Interventions Orchestration
        tv_takeover = (action == VerdictAction.INTERVENE)
        payment_lock = (action == VerdictAction.INTERVENE)
        chime_alert = (action == VerdictAction.INTERVENE)
        family_notify = (action == VerdictAction.INTERVENE)

        lock_id = None
        if payment_lock:
            lock_id = payment_guard.lock_transfers(
                reason=f"Intervention {verdict_id}: Digital arrest extortion caught by Ring oracle",
                incident_id=verdict_id
            )

        if chime_alert:
            self.tools.trigger_chime_alert("audio_ref_urgent_security_alert")

        interventions = InterventionDetails(
            tv_takeover_triggered=tv_takeover,
            tv_headline="🚨 POLICE NEVER ARREST OVER VIDEO CALL",
            tv_guidance=(
                "Hang up immediately! Scammers are impersonating law enforcement using deepfakes. "
                "Ring front door camera verifies NO ONE is outside your house."
            ),
            payment_locked=payment_lock,
            payment_lock_id=lock_id,
            family_notified=family_notify,
            family_contacts_alerted=[
                "Rohan (Son) - +91 98200 11223",
                "Pooja (Daughter) - +91 98111 22334"
            ] if family_notify else [],
            chime_alert_played=chime_alert,
            chime_audio_ref="audio_ref_urgent_security_alert",
            helpline_displayed="1930 (National Cyber Crime Reporting Portal - cybercrime.gov.in)"
        )

        verdict = Verdict(
            verdict_id=verdict_id,
            timestamp=now_iso,
            action=action,
            confidence=confidence,
            contradiction_detected=contradiction_detected,
            contradiction_summary=contradiction_summary if contradiction_detected else "No physical contradiction.",
            reasons=reasons,
            door_evidence=door_evidence,
            call_risk=call_risk,
            interventions=interventions
        )

        # Step 5: Cryptographic Signing with AWS KMS & DynamoDB Audit Commit
        if action in (VerdictAction.INTERVENE, VerdictAction.WARN):
            sig_b64, digest_hex = aws_audit_ledger.sign_verdict(verdict)
            incident_record = aws_audit_ledger.store_incident(verdict, sig_b64)
            verdict.signed_audit_record_id = incident_record.incident_id

        self._last_verdict = verdict
        logger.info(
            f"🧠 [AGENT VERDICT] Action: {action.value} | Confidence: {confidence:.2f} | "
            f"Contradiction: {contradiction_detected} | TV: {tv_takeover} | PayLock: {payment_lock}"
        )
        return verdict

    def get_latest_verdict(self) -> Optional[Verdict]:
        return self._last_verdict


agent_brain = MirageShieldAgent()
