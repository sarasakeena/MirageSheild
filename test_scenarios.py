"""
MIRAGE-SHIELD Automated Scenario Verification Suite
Runs Scenarios 1, 2, and 3 five times in a row to verify zero flakes and strict gate compliance:
- Gate: All 3 scenarios must pass 5 times consecutively.
"""

import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from shared.schemas import VerdictAction, DoorStatus
from shared.fixtures import (
    SCENARIO_1_CALL_RISK,
    SCENARIO_1_DOOR_EVIDENCE,
    SCENARIO_2_CALL_RISK,
    SCENARIO_2_DOOR_EVIDENCE,
    SCENARIO_3_CALL_RISK,
    SCENARIO_3_DOOR_EVIDENCE,
)
from agent.brain import MirageShieldAgent
from agent.payment_guard import PaymentGuard
from agent.aws_audit import AwsAuditLedger


def run_tests():
    print("=" * 70)
    print("🧪 MIRAGE-SHIELD INTEGRATION VERIFICATION SUITE")
    print("   Running Scenarios 1, 2, and 3 (5 consecutive iterations each)")
    print("=" * 70)

    agent = MirageShieldAgent()
    guard = PaymentGuard()
    ledger = AwsAuditLedger()

    total_runs = 0
    passed_runs = 0

    # -----------------------------------------------------------------
    # SCENARIO 1: Digital Arrest Scam (5 Iterations)
    # -----------------------------------------------------------------
    print("\n▶ Testing SCENARIO 1: Digital Arrest Extortion (Scam Caught)...")
    for i in range(1, 6):
        total_runs += 1
        verdict = agent.evaluate(SCENARIO_1_CALL_RISK, SCENARIO_1_DOOR_EVIDENCE)
        
        # Verify Contradiction
        assert verdict.contradiction_detected is True, f"Iteration {i}: Expected contradiction_detected=True"
        assert verdict.action == VerdictAction.INTERVENE, f"Iteration {i}: Expected action=INTERVENE, got {verdict.action}"
        assert verdict.interventions.tv_takeover_triggered is True, f"Iteration {i}: Expected TV takeover"
        assert verdict.interventions.payment_locked is True, f"Iteration {i}: Expected payment lock"
        assert verdict.signed_audit_record_id is not None, f"Iteration {i}: Expected signed audit record"

        # Verify Payment Guard behavior
        guard.lock_transfers("Scenario 1 active")
        attempt = guard.process_payment_attempt(450000.0, "998822114433", "RBI Escrow")
        assert attempt["blocked"] is True, f"Iteration {i}: Transfer should be blocked"

        # Verify Family Co-Sign
        guard.unlock_transfers("Rohan (Son)")
        attempt_after = guard.process_payment_attempt(450000.0, "998822114433", "RBI Escrow")
        assert attempt_after["blocked"] is False, f"Iteration {i}: Transfer should pass after co-sign"

        passed_runs += 1
        print(f"   ✔ Iteration {i}/5 PASSED (Contradiction Caught, TV Takeover Triggered, Payment Locked & Released via Co-Sign)")

    # -----------------------------------------------------------------
    # SCENARIO 2: Genuine Family Call (5 Iterations)
    # -----------------------------------------------------------------
    print("\n▶ Testing SCENARIO 2: Genuine Family Video Call (Zero False Alarms)...")
    for i in range(1, 6):
        total_runs += 1
        verdict = agent.evaluate(SCENARIO_2_CALL_RISK, SCENARIO_2_DOOR_EVIDENCE)

        assert verdict.contradiction_detected is False, f"Iteration {i}: False contradiction raised"
        assert verdict.action == VerdictAction.SAFE, f"Iteration {i}: Expected action=SAFE, got {verdict.action}"
        assert verdict.interventions.tv_takeover_triggered is False, f"Iteration {i}: TV should stay quiet"
        assert verdict.interventions.payment_locked is False, f"Iteration {i}: Payments should remain free"

        passed_runs += 1
        print(f"   ✔ Iteration {i}/5 PASSED (Stays Quiet, Zero False Alarms, TV Ambient)")

    # -----------------------------------------------------------------
    # SCENARIO 3: Real Amazon Courier Delivery (5 Iterations)
    # -----------------------------------------------------------------
    print("\n▶ Testing SCENARIO 3: Real Amazon Courier Delivery (Verified Delivery)...")
    for i in range(1, 6):
        total_runs += 1
        verdict = agent.evaluate(SCENARIO_3_CALL_RISK, SCENARIO_3_DOOR_EVIDENCE)

        assert verdict.contradiction_detected is False, f"Iteration {i}: Genuine package should not trigger contradiction"
        assert verdict.action == VerdictAction.SAFE, f"Iteration {i}: Expected action=SAFE"
        assert verdict.door_evidence.door_status == DoorStatus.PACKAGE_DELIVERED, f"Iteration {i}: Expected PACKAGE_DELIVERED"
        assert verdict.interventions.tv_takeover_triggered is False, f"Iteration {i}: TV should not intervene on real package"

        passed_runs += 1
        print(f"   ✔ Iteration {i}/5 PASSED (Package Verified, Human Verified, Zero False Alarms)")

    # -----------------------------------------------------------------
    # KMS Cryptographic Signature Check
    # -----------------------------------------------------------------
    print("\n▶ Testing AWS KMS Cryptographic Signature Ledger...")
    sig, digest = ledger.sign_verdict(verdict)
    assert len(sig) > 20, "Signature should be non-empty"
    assert len(digest) == 64, "Digest must be 64-char SHA256 hex"
    print(f"   ✔ Cryptographic Sign PASSED (Signature: {sig[:24]}... Digest: {digest[:16]}...)")

    print("\n" + "=" * 70)
    print(f"🎉 ALL INTEGRATION TESTS PASSED: {passed_runs}/{total_runs} runs successful (100% PASS RATE)")
    print("   Gate to Day 4 PASSED: All three scenarios passed 5 times in a row!")
    print("=" * 70)


if __name__ == "__main__":
    run_tests()
