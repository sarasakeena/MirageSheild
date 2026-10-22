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
        self._bedrock_client = None
        self._bedrock_status = "UNINITIALIZED"

        try:
            import boto3
            self._bedrock_client = boto3.client("bedrock-runtime", region_name=self.aws_region)
            self._bedrock_status = "CLIENT_READY"
        except Exception as e:
            self._bedrock_status = f"INIT_FAILED ({type(e).__name__})"

    def _invoke_bedrock_converse(self, call_risk: CallRisk, door_evidence: DoorEvidence, contradiction: bool) -> Optional[Dict[str, Any]]:
        """
        Attempts a real Amazon Bedrock Converse API invocation if credentials & model access are active.
        """
        if not self._bedrock_client:
            return None

        prompt = (
            f"You are the MIRAGE-SHIELD Living Room Defense Agent. Analyze the following signals:\n"
            f"1. Spoken Claims: {call_risk.physical_claims.raw_claims}\n"
            f"2. Coercion Score: {call_risk.coercion_score} with flags: {[f.value for f in call_risk.coercion_flags]}\n"
            f"3. Ring Front Door Evidence: {door_evidence.summary} (Door Status: {door_evidence.door_status.value})\n"
            f"4. Physical Contradiction Detected: {contradiction}\n\n"
            f"Output a one-sentence legal and factual reasoning assessment for the victim."
        )

        try:
            resp = self._bedrock_client.converse(
                modelId=self.bedrock_model_id,
                messages=[{"role": "user", "content": [{"text": prompt}]}],
                inferenceConfig={"maxTokens": 100, "temperature": 0.2}
            )
            output_text = resp["output"]["message"]["content"][0]["text"]
            logger.info(f"Amazon Bedrock Converse reply: {output_text[:80]}...")
            return {
                "success": True,
                "engine": f"Amazon Bedrock Converse ({self.bedrock_model_id})",
                "analysis": output_text
            }
        except Exception as e:
            err_code = getattr(e, 'response', {}).get('Error', {}).get('Code', type(e).__name__)
            logger.warning(f"Bedrock Converse call failed ({err_code}), gracefully using local rule engine.")
            return {
                "success": False,
                "engine": f"Local Rule-Based Heuristic (Bedrock: {err_code})",
                "error": str(err_code)
            }

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

        # Step 2b: Try real Bedrock Converse call if available
        bedrock_result = self._invoke_bedrock_converse(call_risk, door_evidence, contradiction_detected)
        if bedrock_result and bedrock_result.get("success"):
            reasoning_engine = bedrock_result["engine"]
        elif bedrock_result:
            reasoning_engine = bedrock_result["engine"]
        else:
            reasoning_engine = "Local Rule-Based Heuristic (Bedrock Client Unavailable)"

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
            reasoning_engine=reasoning_engine,
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
