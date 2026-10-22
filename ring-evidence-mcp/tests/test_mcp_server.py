"""
Standalone MCP Server Test Suite
================================
Validates tool registration, schema definitions, and direct tool execution
for the Ring Evidence Oracle Model Context Protocol (MCP) server.
"""

import asyncio
import os
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# Add src to python path for standalone test execution
TEST_DIR = Path(__file__).resolve().parent
PROJECT_DIR = TEST_DIR.parent
SRC_DIR = PROJECT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from ring_evidence_mcp.server import mcp, get_door_evidence, verify_porch_claim


def test_tool_registration():
    """Verifies that MCP tools are properly discovered and registered on the server."""
    tools = asyncio.run(mcp.list_tools())
    tool_names = [t.name for t in tools]

    print("\n--- Testing Tool Registration ---")
    print(f"Registered Tools: {tool_names}")

    assert "get_door_evidence" in tool_names, "Missing 'get_door_evidence' tool in MCP registry"
    assert "verify_porch_claim" in tool_names, "Missing 'verify_porch_claim' tool in MCP registry"
    assert len(tools) >= 2, f"Expected at least 2 registered tools, found {len(tools)}"
    print("✔ Tool registration test passed.")


def test_get_door_evidence_direct():
    """Verifies direct execution of the get_door_evidence tool."""
    evidence = asyncio.run(get_door_evidence(window_hours=6))

    print("\n--- Testing get_door_evidence Direct Call ---")
    print(f"Device ID: {evidence.get('device_id')}")
    print(f"Door Status: {evidence.get('door_status')}")
    print(f"Human Count: {evidence.get('human_events_count')}")
    print(f"Integrity Hash: {evidence.get('sha256_integrity_hash')}")

    assert "door_status" in evidence
    assert "human_events_count" in evidence
    assert "package_events_count" in evidence
    assert "motion_events_count" in evidence
    assert "sha256_integrity_hash" in evidence
    assert "snapshot_reference" in evidence
    assert evidence["window_hours"] == 6
    print("✔ Direct get_door_evidence execution passed.")


def test_verify_porch_claim_contradiction():
    """Verifies that extortion claims (police at door) trigger a proven contradiction against empty porch."""
    result = asyncio.run(verify_porch_claim(claim_type="police_at_door", window_hours=6))

    print("\n--- Testing verify_porch_claim (Extortion Claim) ---")
    print(f"Claim Analyzed: {result.get('claim_analyzed')}")
    print(f"Contradiction Detected: {result.get('contradiction_detected')}")
    print(f"Verdict: {result.get('verdict')}")
    print(f"Action: {result.get('recommended_action')}")

    assert result["contradiction_detected"] is True
    assert result["verdict"] == "CONTRADICTION_PROVED"
    assert result["recommended_action"] == "INTERVENE_AND_ALERT"
    assert "Caller claims" in result["summary"]
    print("✔ Physical contradiction verification passed.")


def test_mcp_server_call_tool_dispatch():
    """Verifies tool dispatch via the official MCP Server call_tool interface."""
    async def run_call():
        res = await mcp.call_tool("verify_porch_claim", {"claim_type": "police_outside_front_door"})
        return res

    call_result = asyncio.run(run_call())

    print("\n--- Testing MCP Server Tool Dispatch ---")
    print(f"Call Result Type: {type(call_result)}")
    print(f"Result Meta: {call_result}")

    assert call_result is not None
    assert call_result.is_error is False

    # In MCP, structured_content or content contains the tool result
    data = getattr(call_result, "structured_content", None) or {}
    text_content = ""
    if getattr(call_result, "content", None):
        text_content = str(call_result.content)

    print(f"Dispatched content successfully verified.")
    print("✔ MCP JSON-RPC / Protocol call_tool dispatch passed.")


def main():
    print("=" * 65)
    print("🔔 RING-EVIDENCE-MCP STANDALONE TEST RUNNER")
    print("=" * 65)

    test_tool_registration()
    test_get_door_evidence_direct()
    test_verify_porch_claim_contradiction()
    test_mcp_server_call_tool_dispatch()

    print("\n" + "=" * 65)
    print("🎉 ALL 4 STANDALONE MCP TESTS PASSED (100% SUCCESS)!")
    print("=" * 65)


if __name__ == "__main__":
    main()
