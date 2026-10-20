"""
Scam Detector Module
"""
from detector.deepfake_scorer import DeepfakeScorer
from detector.speech_stt import SpeechTranscriber
from detector.coercion_classifier import CoercionClassifier
from detector.claim_extractor import PhysicalClaimExtractor
from detector.scam_detector import ScamCallDetector

__all__ = [
    "DeepfakeScorer",
    "SpeechTranscriber",
    "CoercionClassifier",
    "PhysicalClaimExtractor",
    "ScamCallDetector"
]
