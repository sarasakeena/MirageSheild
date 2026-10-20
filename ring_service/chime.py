"""
Ring Chime Trigger
Plays pre-recorded high-priority chime alerts when extortion or digital arrest is detected.
"""

import logging
from typing import Dict, Any
from ring_service.client import RingPartnerClient

logger = logging.getLogger("ring_chime")


class ChimeAlertService:
    def __init__(self, client: RingPartnerClient = None):
        self.client = client or RingPartnerClient()

    def alert_living_room(
        self,
        chime_device_id: str = "ring_chime_01_livingroom",
        audio_ref: str = "audio_ref_urgent_security_alert"
    ) -> Dict[str, Any]:
        """
        Triggers Ring Chime audio slot playback.
        """
        logger.info(f"Triggering chime alert on device: {chime_device_id} with slot {audio_ref}")
        return self.client.trigger_chime(chime_device_id, audio_ref)
