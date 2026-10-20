"""
Unified Scam-Call Detector Service
Combines video deepfake scoring, audio transcription, coercion script analysis,
and physical claim extraction into a standardized CallRisk assessment.
"""

import re
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from shared.schemas import CallRisk, FinancialThreat
from detector.deepfake_scorer import DeepfakeScorer
from detector.speech_stt import SpeechTranscriber
from detector.coercion_classifier import CoercionClassifier
from detector.claim_extractor import PhysicalClaimExtractor

logger = logging.getLogger("scam_detector")


class ScamCallDetector:
    """
    End-to-end multi-modal scam-call risk detection engine.
    """

    def __init__(self):
        self.deepfake_scorer = DeepfakeScorer()
        self.transcriber = SpeechTranscriber()
        self.coercion_classifier = CoercionClassifier()
        self.claim_extractor = PhysicalClaimExtractor()

    def analyze_call(
        self,
        call_id: str,
        caller_identity: str,
        transcript_text: str = None,
        audio_stream: Any = None,
        video_metadata: Dict[str, Any] = None,
        phone_number: str = "+91 98765 43210"
    ) -> CallRisk:
        """
        Runs full multi-modal detection pipeline on an incoming call session.
        """
        # Step 1: STT
        stt_result = self.transcriber.transcribe_audio_clip(
            audio_source=audio_stream,
            preset_transcript=transcript_text
        )
        final_transcript = stt_result.get("transcript", transcript_text or "")

        # Step 2: Deepfake Visual Scoring
        df_result = self.deepfake_scorer.score_video_clip(
            clip_id=call_id,
            video_metadata=video_metadata
        )
        deepfake_score = df_result.get("score", 0.0)
        deepfake_artifacts = df_result.get("artifacts", [])

        # Step 3: Coercion Script Classification
        coercion_score, coercion_flags, snippets = self.coercion_classifier.analyze_transcript(final_transcript)

        # Step 4: Extract Physical World Claims
        physical_claims = self.claim_extractor.extract_claims(final_transcript)

        # Step 5: Financial threat extraction
        financial_threat = None
        money_match = re.search(r"(?:₹|rs\.?|inr)\s*([\d,]+)", final_transcript.lower())
        if money_match:
            try:
                amt_str = money_match.group(1).replace(",", "")
                amt = float(amt_str)
                financial_threat = FinancialThreat(
                    demanded_amount_inr=amt,
                    target_account_type="RBI_VERIFICATION_ESCROW",
                    target_account_number="998822114433",
                    urgency_minutes=15
                )
            except Exception:
                pass

        # Risk Level Assessment
        if coercion_score >= 0.70 or (deepfake_score >= 0.70 and coercion_score >= 0.30):
            risk_level = "CRITICAL"
        elif coercion_score >= 0.35 or deepfake_score >= 0.50:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        call_risk = CallRisk(
            call_id=call_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            caller_claimed_identity=caller_identity,
            caller_phone=phone_number,
            deepfake_score=deepfake_score,
            deepfake_artifacts=deepfake_artifacts,
            transcript=final_transcript,
            coercion_score=coercion_score,
            coercion_flags=coercion_flags,
            physical_claims=physical_claims,
            financial_threat=financial_threat,
            risk_level=risk_level
        )

        logger.info(
            f"📞 [CALL RISK] Call: {call_id} | DF Score: {deepfake_score} | "
            f"Coercion: {coercion_score} | Level: {risk_level} | "
            f"Officers Claimed: {physical_claims.claimed_officers_at_door}"
        )
        return call_risk
