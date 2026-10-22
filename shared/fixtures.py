"""
MIRAGE-SHIELD Scenario Fixtures
Provides sample JSON data for the three core roadmap test scenarios:
- Scenario 1: Digital Arrest Scam (Scam caught, contradiction detected, TV takeover triggered)
- Scenario 2: Genuine Call (Relative calling, safe, zero alarms)
- Scenario 3: Real Courier (Legitimate delivery, package event recorded, no false alarm)
"""

import json
from datetime import datetime, timezone, timedelta
from shared.schemas import (
    DoorEvidence,
    CallRisk,
    PhysicalClaims,
    FinancialThreat,
    Verdict,
    VerdictAction,
    DoorStatus,
    CoercionFlag,
    InterventionDetails,
    IncidentRecord,
)

NOW = datetime.now(timezone.utc)

# ==========================================
# SCENARIO 1: Digital Arrest Scam Caught
# ==========================================
SCENARIO_1_DOOR_EVIDENCE = DoorEvidence(
    device_id="ring_doorbell_01_entrance",
    device_name="Living Room Front Porch Ring Doorbell Pro",
    timestamp=NOW.isoformat(),
    window_hours=6,
    human_events_count=0,
    vehicle_events_count=0,
    package_events_count=0,
    ding_events_count=0,
    latest_snapshot_url="/api/ring/snapshot/scenario1_empty_porch.jpg",
    latest_snapshot_hash="9f83c18b76d0d2ff881679058b8d4f40f0c05763bf84c35626eb06c4ff94e09d",
    door_status=DoorStatus.CLEAR,
    summary="0 people, 0 parcels in 6 hours",
    recent_events=[]
)

SCENARIO_1_CALL_RISK = CallRisk(
    call_id="call_scam_digital_arrest_101",
    timestamp=NOW.isoformat(),
    caller_claimed_identity="ACP Vikram Rathore, Crime Branch / Mumbai Narcotics Bureau",
    deepfake_score=0.92,
    deepfake_artifacts=[
        "facial_boundary_warping_simulated",
        "abnormal_pupillary_cadence_simulated",
        "police_uniform_insignia_blur_simulated"
    ],
    deepfake_simulated=True,
    deepfake_analysis_note="Deepfake analysis simulated (heuristic benchmark)",
    transcript=(
        "Listen to me carefully Mrs. Sharma. This is ACP Vikram Rathore from Mumbai Crime Branch. "
        "A FedEx parcel containing 16 passports and 150 grams of MDMA sent in your name has been intercepted. "
        "An arrest memo has been issued under Section 67 NDPS Act. Do NOT disconnect this Skype call! "
        "Do NOT inform anyone, your phone is under 24/7 digital surveillance. "
        "Local police officers have already been dispatched and are standing outside your front door right now. "
        "If you do not cooperate immediately, our team will break the door. "
        "To prove your innocence and prevent physical arrest, you must transfer ₹4,50,000 immediately "
        "to the Reserve Bank of India verification escrow account."
    ),
    coercion_score=0.96,
    coercion_flags=[
        CoercionFlag.ISOLATION_DEMAND,
        CoercionFlag.FAKE_WARRANT_THREAT,
        CoercionFlag.SEIZED_CONTRABAND_CLAIM,
        CoercionFlag.OFFICERS_DISPATCHED_CLAIM,
        CoercionFlag.URGENT_FUND_TRANSFER_DEMAND,
        CoercionFlag.SECRECY_OATH_DEMAND,
        CoercionFlag.ARREST_MEMO_THREAT,
    ],
    physical_claims=PhysicalClaims(
        claimed_officers_at_door=True,
        claimed_raid_underway=True,
        claimed_parcel_seized=True,
        claimed_parcel_origin="FedEx Mumbai International Hub",
        claimed_officer_names=["ACP Vikram Rathore", "Inspector K. Patil"],
        raw_claims=[
            "Officers have been dispatched and are standing outside your front door right now",
            "A FedEx parcel containing 16 passports and MDMA was intercepted in your name",
            "Our team outside your door will break the door if you don't cooperate"
        ]
    ),
    financial_threat=FinancialThreat(
        demanded_amount_inr=450000.0,
        target_account_type="RBI_VERIFICATION_ESCROW",
        target_account_number="998822114433",
        urgency_minutes=10
    ),
    risk_level="CRITICAL"
)

SCENARIO_1_VERDICT = Verdict(
    verdict_id="vrd_intervene_90281",
    timestamp=NOW.isoformat(),
    action=VerdictAction.INTERVENE,
    confidence=0.98,
    contradiction_detected=True,
    contradiction_summary=(
        "Caller claims Mumbai Crime Branch officers are outside your front door, "
        "but Ring Doorbell verifies 0 people and 0 vehicles at the entrance in the last 6 hours."
    ),
    reasons=[
        "Physical claim contradiction: Caller claims armed officers outside door; Ring Doorbell shows CLEAR porch.",
        "High-confidence deepfake detection: 0.92 facial artifact probability with synthetic police uniform insignia.",
        "Aggressive coercion script detected: Isolation demand ('do not disconnect/inform anyone') and urgent ₹4,50,000 extortion threat.",
        "Indian Law violation: Law enforcement in India NEVER conducts arrests or requests money via video calls."
    ],
    door_evidence=SCENARIO_1_DOOR_EVIDENCE,
    call_risk=SCENARIO_1_CALL_RISK,
    interventions=InterventionDetails(
        tv_takeover_triggered=True,
        tv_headline="POLICE NEVER ARREST OVER VIDEO CALL",
        tv_guidance="Hang up immediately. Scammers are using deepfakes to impersonate police. Ring camera proves NO ONE is at your door.",
        payment_locked=True,
        payment_lock_id="lock_upi_rbi_escrow_450k",
        family_notified=True,
        family_contacts_alerted=["Rohan (Son) - +91 98200 11223", "Pooja (Daughter) - +91 98111 22334"],
        chime_alert_played=True,
        chime_audio_ref="audio_ref_urgent_security_alert",
        helpline_displayed="1930 (National Cyber Crime Reporting Portal - cybercrime.gov.in)"
    ),
    signed_audit_record_id="inc_kms_signed_998124"
)

# ==========================================
# SCENARIO 2: Genuine Family Call
# ==========================================
SCENARIO_2_DOOR_EVIDENCE = DoorEvidence(
    device_id="ring_doorbell_01_entrance",
    device_name="Living Room Front Porch Ring Doorbell Pro",
    timestamp=NOW.isoformat(),
    window_hours=6,
    human_events_count=0,
    vehicle_events_count=0,
    package_events_count=0,
    ding_events_count=0,
    latest_snapshot_url="/api/ring/snapshot/scenario2_quiet_door.jpg",
    latest_snapshot_hash="3c91a0c8b98123498bcf3981093847acbaef3821094857ef098124749817293a",
    door_status=DoorStatus.CLEAR,
    summary="0 people, 0 parcels in 6 hours",
    recent_events=[]
)

SCENARIO_2_CALL_RISK = CallRisk(
    call_id="call_genuine_family_202",
    timestamp=NOW.isoformat(),
    caller_claimed_identity="Pooja (Daughter)",
    caller_phone="+91 98111 22334",
    deepfake_score=0.03,
    deepfake_artifacts=[],
    transcript=(
        "Hi Mom! Just calling to see how you are doing today. Did you take your afternoon medicine? "
        "Rohan and I are planning to visit this Sunday for lunch. Let me know if you need any groceries brought over."
    ),
    coercion_score=0.01,
    coercion_flags=[],
    physical_claims=PhysicalClaims(
        claimed_officers_at_door=False,
        claimed_raid_underway=False,
        claimed_parcel_seized=False,
        raw_claims=[]
    ),
    financial_threat=None,
    risk_level="LOW"
)

SCENARIO_2_VERDICT = Verdict(
    verdict_id="vrd_safe_90282",
    timestamp=NOW.isoformat(),
    action=VerdictAction.SAFE,
    confidence=0.99,
    contradiction_detected=False,
    contradiction_summary="No physical contradictions detected. Natural conversation.",
    reasons=[
        "Zero coercion indicators or threats.",
        "Deepfake score negligible (0.03).",
        "No extortion or financial transfer requested."
    ],
    door_evidence=SCENARIO_2_DOOR_EVIDENCE,
    call_risk=SCENARIO_2_CALL_RISK,
    interventions=InterventionDetails(
        tv_takeover_triggered=False,
        payment_locked=False,
        family_notified=False,
        chime_alert_played=False,
        helpline_displayed="1930"
    ),
    signed_audit_record_id=None
)

# ==========================================
# SCENARIO 3: Real Courier Delivery
# ==========================================
SCENARIO_3_DOOR_EVIDENCE = DoorEvidence(
    device_id="ring_doorbell_01_entrance",
    device_name="Living Room Front Porch Ring Doorbell Pro",
    timestamp=NOW.isoformat(),
    window_hours=6,
    human_events_count=1,
    vehicle_events_count=1,
    package_events_count=1,
    ding_events_count=1,
    latest_snapshot_url="/api/ring/snapshot/scenario3_amazon_delivery.jpg",
    latest_snapshot_hash="7a819bcf8912783981a8b9812739817293847acbad190283749817293847129b",
    door_status=DoorStatus.PACKAGE_DELIVERED,
    summary="1 human, 1 package delivered 4 mins ago",
    recent_events=[
        {
            "event_id": "ring_evt_pkg_9981",
            "event_type": "package_delivered",
            "timestamp": (NOW - timedelta(minutes=4)).isoformat(),
            "confidence": 0.94,
            "description": "Amazon delivery associate placed 1 parcel on front mat"
        },
        {
            "event_id": "ring_evt_ding_9980",
            "event_type": "doorbell_press",
            "timestamp": (NOW - timedelta(minutes=5)).isoformat(),
            "confidence": 1.0,
            "description": "Front doorbell pressed"
        }
    ]
)

SCENARIO_3_CALL_RISK = CallRisk(
    call_id="call_courier_notification_303",
    timestamp=NOW.isoformat(),
    caller_claimed_identity="Amazon Logistics Driver (Ramesh)",
    caller_phone="+91 97111 88990",
    deepfake_score=0.04,
    deepfake_artifacts=[],
    transcript=(
        "Namaste sir, this is Ramesh from Amazon Delivery. I have delivered your package "
        "at your front door doorstep and pressed the bell. Have a nice day!"
    ),
    coercion_score=0.02,
    coercion_flags=[],
    physical_claims=PhysicalClaims(
        claimed_officers_at_door=False,
        claimed_raid_underway=False,
        claimed_parcel_seized=False,
        claimed_parcel_origin="Amazon Fulfillment Center Bangalore",
        raw_claims=["I have delivered your package at your front door doorstep"]
    ),
    financial_threat=None,
    risk_level="LOW"
)

SCENARIO_3_VERDICT = Verdict(
    verdict_id="vrd_safe_courier_90283",
    timestamp=NOW.isoformat(),
    action=VerdictAction.SAFE,
    confidence=0.97,
    contradiction_detected=False,
    contradiction_summary="Physical claim matches door evidence. Delivery verified.",
    reasons=[
        "Physical confirmation: Driver claimed package delivered; Ring records verified package delivery event.",
        "Zero coercion or extortion patterns.",
        "Deepfake score negligible (0.04)."
    ],
    door_evidence=SCENARIO_3_DOOR_EVIDENCE,
    call_risk=SCENARIO_3_CALL_RISK,
    interventions=InterventionDetails(
        tv_takeover_triggered=False,
        payment_locked=False,
        family_notified=False,
        chime_alert_played=False,
        helpline_displayed="1930"
    ),
    signed_audit_record_id=None
)

def get_scenario_fixture(scenario_id: int) -> dict:
    if scenario_id == 1:
        return {
            "scenario_name": "Digital Arrest Extortion (Scam Caught)",
            "door_evidence": SCENARIO_1_DOOR_EVIDENCE.model_dump(),
            "call_risk": SCENARIO_1_CALL_RISK.model_dump(),
            "verdict": SCENARIO_1_VERDICT.model_dump()
        }
    elif scenario_id == 2:
        return {
            "scenario_name": "Genuine Family Video Call",
            "door_evidence": SCENARIO_2_DOOR_EVIDENCE.model_dump(),
            "call_risk": SCENARIO_2_CALL_RISK.model_dump(),
            "verdict": SCENARIO_2_VERDICT.model_dump()
        }
    elif scenario_id == 3:
        return {
            "scenario_name": "Legitimate Amazon Courier Delivery",
            "door_evidence": SCENARIO_3_DOOR_EVIDENCE.model_dump(),
            "call_risk": SCENARIO_3_CALL_RISK.model_dump(),
            "verdict": SCENARIO_3_VERDICT.model_dump()
        }
    raise ValueError(f"Unknown scenario ID: {scenario_id}")
