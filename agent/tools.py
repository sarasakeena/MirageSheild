"""
Agent Tool Registry
Defines callable tools for the Strands / Bedrock Agent:
- get_door_evidence: Ring physical oracle
- score_call: Multi-modal scam detection
- lock_payments: Financial firewall
- notify_family: Family emergency notification
- trigger_tv_alert: Fire TV / Vega OS intervention takeover
"""

import logging
from typing import Dict, Any, Tuple
from shared.schemas import DoorEvidence, CallRisk, PhysicalClaims, DoorStatus
from ring_service.evidence import DoorEvidenceOracle
from ring_service.chime import ChimeAlertService

logger = logging.getLogger("agent_tools")


class AgentTools:
    def __init__(self, ring_oracle: DoorEvidenceOracle = None, chime_service: ChimeAlertService = None):
        self.ring_oracle = ring_oracle or DoorEvidenceOracle()
        self.chime_service = chime_service or ChimeAlertService()

    def get_door_evidence(self, window_hours: int = 6) -> DoorEvidence:
        """Queries the Ring door oracle for physical evidence."""
        return self.ring_oracle.get_door_evidence(window_hours=window_hours)

    def check_physical_contradiction(
        self,
        claims: PhysicalClaims,
        evidence: DoorEvidence
    ) -> Tuple[bool, str]:
        """
        Cross-examines caller's physical world claims against Ring door evidence.
        Catches the scammer in a direct lie.
        """
        # Claim 1: Officers/police at door
        if claims.claimed_officers_at_door:
            if evidence.human_events_count == 0:
                summary = (
                    f"Caller claims police/officers are standing outside "
                    f"your front door, but Ring Doorbell verifies 0 people at the entrance in the last {evidence.window_hours} hours."
                )
                return True, summary

        # Claim 2: Immediate raid / door break
        if claims.claimed_raid_underway:
            if evidence.door_status == DoorStatus.CLEAR:
                summary = (
                    f"Caller threatens an immediate police raid at your premises, "
                    f"yet Ring Doorbell confirms front entrance is completely clear and undisturbed."
                )
                return True, summary

        # Claim 3: Parcel seized vs delivered
        if claims.claimed_parcel_seized and evidence.package_events_count == 0 and evidence.human_events_count == 0:
            # Caller claims contraband parcel intercepted elsewhere to extort money
            pass

        return False, "No physical contradictions detected."

    def trigger_chime_alert(self, audio_ref: str = "audio_ref_urgent_security_alert") -> Dict[str, Any]:
        """Sounds the Ring Chime in the living room."""
        return self.chime_service.alert_living_room(audio_ref=audio_ref)
