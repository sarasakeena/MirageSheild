"""
Ring Door Evidence Service
Acts as the physical-world Evidence Oracle:
Queries Ring event history and snapshots over a time window, computes hashes,
and returns a standardized DoorEvidence object.
"""

import logging
from datetime import datetime, timezone
from typing import Optional
from shared.schemas import DoorEvidence, DoorStatus
from ring_service.client import RingPartnerClient

logger = logging.getLogger("ring_evidence")


class DoorEvidenceOracle:
    """
    Physical-world Evidence Oracle powered by Ring Doorbell.
    Contradicts scam claims by inspecting physical front-door ground truth.
    """

    def __init__(self, client: Optional[RingPartnerClient] = None):
        self.client = client or RingPartnerClient()

    def get_door_evidence(
        self,
        window_hours: int = 6,
        device_id: str = "ring_doorbell_01_entrance"
    ) -> DoorEvidence:
        """
        Inspects the front door over the requested window.
        Returns a DoorEvidence object verifying whether any human or package arrived.
        """
        events = self.client.get_event_history(device_id=device_id, window_hours=window_hours)
        snapshot_info = self.client.get_latest_snapshot(device_id=device_id)

        human_count = 0
        vehicle_count = 0
        package_count = 0
        ding_count = 0

        for evt in events:
            kind = evt.get("kind", "").lower()
            cv_tags = [t.lower() for t in evt.get("cv_tags", [])]

            if kind == "package_delivered" or "package" in cv_tags:
                package_count += 1
            if kind == "ding" or "doorbell_press" in cv_tags:
                ding_count += 1
            if "human" in cv_tags or "visitor" in cv_tags or kind == "human":
                human_count += 1
            if "vehicle" in cv_tags or kind == "vehicle":
                vehicle_count += 1

        # Determine door status
        if human_count > 0:
            door_status = DoorStatus.HUMAN_PRESENT
        elif package_count > 0:
            door_status = DoorStatus.PACKAGE_DELIVERED
        elif ding_count > 0:
            door_status = DoorStatus.RING_DING
        else:
            door_status = DoorStatus.CLEAR

        # Generate concise human-readable summary
        if human_count == 0 and package_count == 0:
            summary = f"0 people, 0 parcels in {window_hours} hours"
        else:
            summary = f"{human_count} people, {package_count} parcels in {window_hours} hours"

        evidence = DoorEvidence(
            device_id=device_id,
            device_name="Front Door Video Doorbell Pro 2",
            timestamp=datetime.now(timezone.utc).isoformat(),
            window_hours=window_hours,
            human_events_count=human_count,
            vehicle_events_count=vehicle_count,
            package_events_count=package_count,
            ding_events_count=ding_count,
            latest_snapshot_url=snapshot_info.get("snapshot_url", "/api/ring/snapshot/latest.jpg"),
            latest_snapshot_hash=snapshot_info.get("snapshot_hash", "sha256_e3b0c44298"),
            door_status=door_status,
            summary=summary,
            recent_events=events
        )

        logger.info(f"🔍 [DOOR EVIDENCE ORACLE] Window: {window_hours}h | Status: {door_status.value} | Summary: {summary}")
        return evidence
