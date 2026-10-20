"""
Coercion Script Classifier
Analyzes call transcripts for digital arrest and courier extortion coercion patterns.
Flags isolation demands, fake warrants, contraband seizures, and urgent money demands.
"""

import re
import logging
from typing import Dict, Any, List, Tuple
from shared.schemas import CoercionFlag

logger = logging.getLogger("coercion_classifier")

# Pattern libraries based on Indian Cybercrime Coordination Centre (I4C) advisories
PATTERNS = {
    CoercionFlag.ISOLATION_DEMAND: [
        r"\b(?:do not|don'?t)\s+(?:disconnect|cut|hang up|end)\b",
        r"\b(?:do not|don'?t)\s+(?:tell|inform|speak to)\s+(?:anyone|family|police|lawyer|relatives)\b",
        r"\b(?:stay|lock yourself|remain)\s+(?:in\s+the\s+room|alone|isolated)\b",
        r"\b(?:keep|maintain)\s+(?:camera|video)\s+(?:on|active)\s+at\s+all\s+times\b",
        r"\bdigital\s+surveillance\b",
        r"\bunder\s+(?:24/7\s+)?surveillance\b"
    ],
    CoercionFlag.FAKE_WARRANT_THREAT: [
        r"\barrest\s+(?:memo|warrant|order)\b",
        r"\b(?:ndps|narcotics)\s+act\b",
        r"\bsection\s+(?:67|420|120b)\b",
        r"\bmoney\s+laundering\b",
        r"\bnon-?bailable\s+warrant\b",
        r"\bhigh\s+court\s+order\b",
        r"\bcourt\s+summons\b"
    ],
    CoercionFlag.SEIZED_CONTRABAND_CLAIM: [
        r"\b(?:parcel|package|shipment|courier)\s+(?:seized|intercepted|confiscated|stopped)\b",
        r"\b(?:fedex|dhl|customs|postal)\s+(?:parcel|consignment)\b",
        r"\b(?:passports|mdma|drugs|contraband|narcotics|sim\s+cards|weapons)\b",
        r"\bmumbai\s+(?:airport|customs|hub)\b",
        r"\btaiwan|cambodia|dubai\b"
    ],
    CoercionFlag.OFFICERS_DISPATCHED_CLAIM: [
        r"\b(?:officers?|team|police|personnel)\s+(?:dispatched|arriving|outside|waiting)\b",
        r"\boutside\s+your\s+(?:front\s+)?door\b",
        r"\bat\s+your\s+door\b",
        r"\bbreak\s+(?:the\s+)?door\b",
        r"\braid\s+(?:your\s+house|premises|home)\b",
        r"\bphysical\s+arrest\b"
    ],
    CoercionFlag.URGENT_FUND_TRANSFER_DEMAND: [
        r"\b(?:transfer|send|deposit|pay)\s+(?:money|funds|amount|rupees|inr|lakh|crore)\b",
        r"\brbi\b",
        r"\b(?:verification|clearance|security|escrow)\s+account\b",
        r"\b(?:immediate|urgent|within\s+\d+\s+minutes)\b",
        r"\bclear\s+your\s+name\b",
        r"\brefunded\s+after\s+verification\b"
    ],
    CoercionFlag.SECRECY_OATH_DEMAND: [
        r"\boath\s+of\s+secrecy\b",
        r"\bconfidential\s+investigation\b",
        r"\bnational\s+security\b",
        r"\bdo\s+not\s+disclose\b"
    ],
    CoercionFlag.ARREST_MEMO_THREAT: [
        r"\bpolice\s+custody\b",
        r"\bhandcuffed\b",
        r"\bjail\b",
        r"\bprison\b",
        r"\bcriminal\s+record\b"
    ]
}


class CoercionClassifier:
    """
    Evaluates transcript against coercive psychological manipulation patterns.
    Outputs a 0.0 - 1.0 coercion score and list of triggered flags.
    """

    def analyze_transcript(self, transcript: str) -> Tuple[float, List[CoercionFlag], List[str]]:
        if not transcript or len(transcript.strip()) < 10:
            return 0.0, [], []

        text = transcript.lower()
        matched_flags: List[CoercionFlag] = []
        snippets: List[str] = []

        total_weights = 0.0

        weight_map = {
            CoercionFlag.ISOLATION_DEMAND: 0.35,
            CoercionFlag.FAKE_WARRANT_THREAT: 0.25,
            CoercionFlag.SEIZED_CONTRABAND_CLAIM: 0.25,
            CoercionFlag.OFFICERS_DISPATCHED_CLAIM: 0.30,
            CoercionFlag.URGENT_FUND_TRANSFER_DEMAND: 0.40,
            CoercionFlag.SECRECY_OATH_DEMAND: 0.15,
            CoercionFlag.ARREST_MEMO_THREAT: 0.20,
        }

        for flag, regex_list in PATTERNS.items():
            flag_matched = False
            for pattern in regex_list:
                match = re.search(pattern, text)
                if match:
                    if not flag_matched:
                        matched_flags.append(flag)
                        total_weights += weight_map.get(flag, 0.2)
                        flag_matched = True
                    snippets.append(match.group(0))

        # Normalize score between 0.0 and 1.0
        final_score = min(1.0, round(total_weights, 2))
        logger.info(f"Coercion score: {final_score} | Matched flags: {[f.value for f in matched_flags]}")
        return final_score, matched_flags, snippets
