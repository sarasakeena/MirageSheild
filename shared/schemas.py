"""
MIRAGE-SHIELD Shared Data Contracts and JSON Schemas
Defines DoorEvidence, CallRisk, PhysicalClaim, Verdict, and IncidentRecord contracts.
"""

from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime, timezone


class DoorStatus(str, Enum):
    CLEAR = "CLEAR"
    HUMAN_PRESENT = "HUMAN_PRESENT"
    PACKAGE_DELIVERED = "PACKAGE_DELIVERED"
    MOTION_DETECTED = "MOTION_DETECTED"
    RING_DING = "RING_DING"


class VerdictAction(str, Enum):
    SAFE = "SAFE"
    WARN = "WARN"
    INTERVENE = "INTERVENE"


class CoercionFlag(str, Enum):
    ISOLATION_DEMAND = "ISOLATION_DEMAND"
    FAKE_WARRANT_THREAT = "FAKE_WARRANT_THREAT"
    SEIZED_CONTRABAND_CLAIM = "SEIZED_CONTRABAND_CLAIM"
    OFFICERS_DISPATCHED_CLAIM = "OFFICERS_DISPATCHED_CLAIM"
    URGENT_FUND_TRANSFER_DEMAND = "URGENT_FUND_TRANSFER_DEMAND"
    SECRECY_OATH_DEMAND = "SECRECY_OATH_DEMAND"
    ARREST_MEMO_THREAT = "ARREST_MEMO_THREAT"


class PhysicalClaims(BaseModel):
    claimed_officers_at_door: bool = False
    claimed_raid_underway: bool = False
    claimed_parcel_seized: bool = False
    claimed_parcel_origin: Optional[str] = None
    claimed_officer_names: List[str] = Field(default_factory=list)
    raw_claims: List[str] = Field(default_factory=list)


class FinancialThreat(BaseModel):
    demanded_amount_inr: float = 0.0
    target_account_type: str = "RBI_SECURITY_ESCROW"
    target_account_number: Optional[str] = None
    urgency_minutes: int = 15


class CallRisk(BaseModel):
    call_id: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    caller_claimed_identity: str
    caller_phone: str = "+91 98765 43210"
    deepfake_score: float = Field(ge=0.0, le=1.0, description="0.0 to 1.0 deepfake likelihood")
    deepfake_artifacts: List[str] = Field(default_factory=list)
    deepfake_simulated: bool = True
    deepfake_analysis_note: str = "Deepfake analysis simulated"
    transcript: str
    coercion_score: float = Field(ge=0.0, le=1.0, description="0.0 to 1.0 coercion index")
    coercion_flags: List[CoercionFlag] = Field(default_factory=list)
    detected_coercion_snippets: List[str] = Field(default_factory=list)
    physical_claims: PhysicalClaims = Field(default_factory=PhysicalClaims)
    financial_threat: Optional[FinancialThreat] = None
    risk_level: str = "LOW"  # LOW, MEDIUM, CRITICAL


class DoorEvidence(BaseModel):
    device_id: str
    device_name: str = "Front Door Ring Video Doorbell Pro 2"
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    window_hours: int = 6
    human_events_count: int = 0
    vehicle_events_count: int = 0
    package_events_count: int = 0
    ding_events_count: int = 0
    latest_snapshot_url: str = "/api/ring/snapshot/latest.jpg"
    latest_snapshot_hash: str = "sha256_e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    door_status: DoorStatus = DoorStatus.CLEAR
    summary: str = "0 people, 0 parcels in 6 hours"
    recent_events: List[Dict[str, Any]] = Field(default_factory=list)


class InterventionDetails(BaseModel):
    tv_takeover_triggered: bool = False
    tv_headline: str = "POLICE NEVER ARREST OVER VIDEO CALL"
    tv_guidance: str = "Hang up immediately. No legitimate law enforcement or courier operates via Skype, WhatsApp, or video calls."
    payment_locked: bool = True
    payment_lock_id: Optional[str] = None
    family_notified: bool = True
    family_contacts_alerted: List[str] = Field(default_factory=lambda: ["Rohan (Son) - +91 98200 11223"])
    chime_alert_played: bool = False
    chime_audio_ref: str = "audio_ref_urgent_security_alert"
    helpline_displayed: str = "1930 (National Cyber Crime Reporting Portal)"


class Verdict(BaseModel):
    verdict_id: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    action: VerdictAction
    confidence: float = Field(ge=0.0, le=1.0)
    contradiction_detected: bool = False
    contradiction_summary: str = ""
    reasons: List[str] = Field(default_factory=list)
    reasoning_engine: str = "Local Rule-Based Heuristic (Bedrock Inactive)"
    door_evidence: DoorEvidence
    call_risk: CallRisk
    interventions: InterventionDetails
    signed_audit_record_id: Optional[str] = None


class IncidentRecord(BaseModel):
    incident_id: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    verdict_id: str
    action: VerdictAction
    deepfake_score: float
    coercion_score: float
    contradiction_detected: bool
    contradiction_summary: str
    ring_evidence_hash: str
    snapshot_hash: str
    payment_lock_active: bool = False
    family_cosign_status: str = "PENDING"  # PENDING, APPROVED, REJECTED
    kms_key_arn: str
    kms_signature: str
    signature_type: str = "LOCAL_HMAC_SHA256"
    storage_type: str = "IN_MEMORY"
    dynamodb_status: str = "COMMITTED"
