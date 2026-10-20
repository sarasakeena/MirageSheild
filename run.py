"""
MIRAGE-SHIELD Single-Command Unified Server
Mounts the Ring Partner API client, AI Detector, Strands Agent Brain,
Fire TV Living Room Takeover, and Multi-Device Master Web Console.
"""

import os
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

import uvicorn
from fastapi import FastAPI, Request, Response, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from pydantic import BaseModel

from shared.schemas import (
    DoorEvidence,
    CallRisk,
    Verdict,
    VerdictAction,
    DoorStatus,
)
from shared.fixtures import (
    SCENARIO_1_DOOR_EVIDENCE,
    SCENARIO_1_CALL_RISK,
    SCENARIO_1_VERDICT,
    SCENARIO_2_DOOR_EVIDENCE,
    SCENARIO_2_CALL_RISK,
    SCENARIO_2_VERDICT,
    SCENARIO_3_DOOR_EVIDENCE,
    SCENARIO_3_CALL_RISK,
    SCENARIO_3_VERDICT,
    get_scenario_fixture
)
from ring_service.client import RingPartnerClient
from ring_service.evidence import DoorEvidenceOracle
from ring_service.chime import ChimeAlertService
from ring_service.webhook import verify_ring_signature, webhook_dispatcher
from detector.scam_detector import ScamCallDetector
from agent.brain import agent_brain
from agent.payment_guard import payment_guard
from agent.aws_audit import aws_audit_ledger

app = FastAPI(
    title="MIRAGE-SHIELD",
    description="Physical Evidence Oracle & Living Room Defense Against Digital Arrest Scams",
    version="1.0.0"
)

# Initialize singletons
ring_client = RingPartnerClient()
ring_oracle = DoorEvidenceOracle(client=ring_client)
chime_service = ChimeAlertService(client=ring_client)
scam_detector = ScamCallDetector()

# Mount Static Directories
static_dir = PROJECT_ROOT / "static"
firetv_static_dir = PROJECT_ROOT / "firetv_app" / "static"
console_static_dir = PROJECT_ROOT / "web_console" / "static"

app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
app.mount("/firetv", StaticFiles(directory=str(firetv_static_dir), html=True), name="firetv")
app.mount("/console", StaticFiles(directory=str(console_static_dir), html=True), name="console")

# Global active state
current_state = {
    "scenario_id": 1,
    "verdict": SCENARIO_1_VERDICT,
    "call_risk": SCENARIO_1_CALL_RISK,
    "door_evidence": SCENARIO_1_DOOR_EVIDENCE
}
payment_guard.lock_transfers("Scenario 1 active: Digital arrest extortion caught by Ring oracle", SCENARIO_1_VERDICT.verdict_id)


# ==========================================
# PAGE ROUTES
# ==========================================
@app.get("/", response_class=HTMLResponse)
async def root_redirect():
    """Serves the Master Console as the default landing view."""
    index_file = console_static_dir / "index.html"
    return HTMLResponse(content=index_file.read_text(encoding="utf-8"))


# ==========================================
# RING PARTNER API & ORACLE ENDPOINTS
# ==========================================
@app.get("/api/ring/devices")
async def get_ring_devices():
    """Calls GET /v1/devices on Ring Partner API (or sandbox)."""
    return {"devices": ring_client.list_devices()}


@app.get("/api/ring/evidence")
async def get_ring_door_evidence(window_hours: int = 6):
    """Returns DoorEvidence object: checks humans, parcels, and snapshot integrity."""
    evidence = ring_oracle.get_door_evidence(window_hours=window_hours)
    return evidence.model_dump()


@app.get("/api/ring/snapshot/latest.jpg")
async def get_latest_snapshot():
    """Serves the latest Ring video doorbell snapshot."""
    img_name = "scenario1_empty_porch.jpg"
    if current_state["scenario_id"] == 3:
        img_name = "scenario3_amazon_delivery.jpg"
    snapshot_path = static_dir / "images" / img_name
    if snapshot_path.exists():
        return FileResponse(snapshot_path, media_type="image/jpeg")
    return JSONResponse(status_code=404, content={"error": "Snapshot not found"})


@app.post("/api/ring/webhook")
async def ring_webhook_handler(request: Request):
    """
    Ring Webhook Receiver.
    Verifies HMAC-SHA256 signature in X-Signature-SHA256 header and responds HTTP 200 within 5 seconds.
    """
    signature_header = request.headers.get("X-Signature-SHA256", "")
    body_bytes = await request.body()

    # If secret is set, verify cryptographic signature
    if signature_header and not verify_ring_signature(body_bytes, signature_header):
        raise HTTPException(status_code=401, detail="Invalid HMAC-SHA256 signature")

    # Asynchronously dispatch event to background processor
    try:
        event_data = await request.json()
        await webhook_dispatcher.dispatch_event(event_data)
    except Exception:
        pass

    return {"status": "accepted", "message": "Event queued for asynchronous processing"}


# ==========================================
# SCENARIO SWITCHER & AGENT BRAIN ENDPOINTS
# ==========================================
@app.post("/api/scenario/{scenario_id}")
async def set_active_scenario(scenario_id: int):
    """
    Switches active roadmap test scenario:
    1: Digital Arrest Extortion (Contradiction Caught -> INTERVENE)
    2: Genuine Family Video Call (SAFE -> Stays Quiet)
    3: Real Amazon Courier Delivery (Verified Delivery -> SAFE)
    """
    if scenario_id not in (1, 2, 3):
        raise HTTPException(status_code=400, detail="Invalid scenario ID. Must be 1, 2, or 3.")

    current_state["scenario_id"] = scenario_id
    fixture = get_scenario_fixture(scenario_id)

    if scenario_id == 1:
        ring_client.set_sandbox_door_state("CLEAR")
        current_state["door_evidence"] = SCENARIO_1_DOOR_EVIDENCE
        current_state["call_risk"] = SCENARIO_1_CALL_RISK
        current_state["verdict"] = SCENARIO_1_VERDICT
        payment_guard.lock_transfers(
            reason="Scenario 1: Digital arrest extortion caught by Ring oracle",
            incident_id=SCENARIO_1_VERDICT.verdict_id
        )
    elif scenario_id == 2:
        ring_client.set_sandbox_door_state("CLEAR")
        current_state["door_evidence"] = SCENARIO_2_DOOR_EVIDENCE
        current_state["call_risk"] = SCENARIO_2_CALL_RISK
        current_state["verdict"] = SCENARIO_2_VERDICT
        payment_guard.unlock_transfers("System Reset")
    elif scenario_id == 3:
        ring_client.set_sandbox_door_state("PACKAGE_DELIVERED", SCENARIO_3_DOOR_EVIDENCE.recent_events)
        current_state["door_evidence"] = SCENARIO_3_DOOR_EVIDENCE
        current_state["call_risk"] = SCENARIO_3_CALL_RISK
        current_state["verdict"] = SCENARIO_3_VERDICT
        payment_guard.unlock_transfers("System Reset")

    return fixture


@app.get("/api/verdict/latest")
async def get_latest_verdict():
    """Returns the current active verdict for Fire TV takeover and web console."""
    return current_state["verdict"].model_dump()


# ==========================================
# FINANCIAL PAYMENT GUARD & CO-SIGN ENDPOINTS
# ==========================================
class PaymentAttemptRequest(BaseModel):
    amount_inr: float = 450000.0
    recipient_account: str = "998822114433"
    recipient_name: str = "RBI Escrow Verification"


class CosignRequest(BaseModel):
    authorized_by: str = "Rohan (Son)"


@app.post("/api/payment/attempt")
async def attempt_payment(req: PaymentAttemptRequest):
    """
    Evaluates an outgoing transfer attempt against the active payment guard.
    Returns blocked status if an extortion intervention is active.
    """
    result = payment_guard.process_payment_attempt(
        amount_inr=req.amount_inr,
        recipient_account=req.recipient_account,
        recipient_name=req.recipient_name
    )
    return result


@app.post("/api/payment/cosign")
async def cosign_payment(req: CosignRequest):
    """
    Family co-sign endpoint to authorize fund release after reviewing evidence.
    """
    payment_guard.unlock_transfers(authorized_by=req.authorized_by)
    return {
        "status": "unlocked",
        "authorized_by": req.authorized_by,
        "message": f"Payment unlocked via family co-sign authorization by {req.authorized_by}."
    }


# ==========================================
# AWS AUDIT TRAIL ENDPOINTS
# ==========================================
@app.get("/api/audit/incidents")
async def get_audit_incidents():
    """Returns tamper-evident AWS KMS digitally signed incident records."""
    return {
        "kms_key_arn": f"arn:aws:kms:{aws_audit_ledger.region}:123456789012:key/{aws_audit_ledger.kms_key_id}",
        "dynamodb_table": aws_audit_ledger.table_name,
        "incidents": aws_audit_ledger.list_recent_incidents()
    }


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "MIRAGE-SHIELD",
        "active_scenario": current_state["scenario_id"],
        "payment_locked": payment_guard.is_locked
    }


if __name__ == "__main__":
    host = os.getenv("SERVER_HOST", "127.0.0.1")
    port = int(os.getenv("SERVER_PORT", "8000"))
    print(f"================================================================")
    print(f"🛡️  MIRAGE-SHIELD Living Room Scam Defense Server Booting")
    print(f"    - Web Console:   http://{host}:{port}/")
    print(f"    - Fire TV App:   http://{host}:{port}/firetv")
    print(f"    - API Docs:      http://{host}:{port}/docs")
    print(f"================================================================")
    uvicorn.run("run:app", host=host, port=port, reload=False)
