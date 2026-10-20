"""
Physical Claim Extractor
Extracts claims made by the caller about physical-world events
(e.g., officers at front door, raid underway, seized parcels)
so the Agent Brain can verify them against Ring evidence.
"""

import re
import logging
from typing import List
from shared.schemas import PhysicalClaims

logger = logging.getLogger("claim_extractor")


class PhysicalClaimExtractor:
    """
    Extracts structured physical assertions from call transcripts.
    These claims are passed to the Agent to corroborate with the Ring Evidence Oracle.
    """

    def extract_claims(self, transcript: str) -> PhysicalClaims:
        if not transcript:
            return PhysicalClaims()

        text = transcript.lower()

        officers_at_door = bool(
            re.search(r"(?:officers?|police|team)\s+(?:standing|waiting|present)?\s*(?:outside|at)\s+(?:your\s+)?(?:front\s+)?door", text) or
            re.search(r"standing outside your front door right now", text) or
            re.search(r"police.*outside your door", text)
        )

        raid_underway = bool(
            re.search(r"break\s+(?:the\s+)?door", text) or
            re.search(r"raid\s+(?:your\s+)?(?:house|premises|home)", text) or
            re.search(r"physical\s+arrest", text)
        )

        parcel_seized = bool(
            re.search(r"(?:parcel|package|shipment|consignment)\s+(?:seized|intercepted|confiscated)", text) or
            re.search(r"(?:fedex|dhl|customs)\s+parcel", text)
        )

        raw_claims = []
        if officers_at_door:
            raw_claims.append("Caller claimed law enforcement officers are standing outside your front door.")
        if raid_underway:
            raw_claims.append("Caller claimed officers will break down door or execute immediate raid.")
        if parcel_seized:
            raw_claims.append("Caller claimed a contraband parcel under your name was seized at transit hub.")

        officer_names = []
        name_match = re.findall(r"(?:acp|dcp|inspector|officer|constable)\s+([a-z\s]+?)(?:,|\.|\bfrom|\bwith)", text)
        for n in name_match:
            clean_n = n.strip().title()
            if len(clean_n) > 2 and clean_n not in officer_names:
                officer_names.append(clean_n)

        return PhysicalClaims(
            claimed_officers_at_door=officers_at_door,
            claimed_raid_underway=raid_underway,
            claimed_parcel_seized=parcel_seized,
            claimed_parcel_origin="Transit Hub / Customs" if parcel_seized else None,
            claimed_officer_names=officer_names,
            raw_claims=raw_claims
        )
