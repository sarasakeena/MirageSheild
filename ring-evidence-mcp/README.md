# 🔔 ring-evidence-mcp

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![MCP: >=0.1.0](https://img.shields.io/badge/MCP-Protocol-purple.svg)](https://modelcontextprotocol.io/)

**Model Context Protocol (MCP) server exposing Ring Doorbell & Camera physical entrance telemetry to LLM reasoning agents.**

`ring-evidence-mcp` is an open-source tool developed as part of the **MIRAGE-SHIELD** project (Amazon Developer Hackathon 2026). It bridges the gap between conversational AI agents (Claude, Amazon Bedrock, GPT-4) and real-world IoT sensor feeds—giving agents the physical ground truth necessary to expose "Digital Arrest" extortion scams and video deepfake impersonations in real time.

---

## 🌟 Why This Matters: Physical Contradiction Defense

In a **Digital Arrest extortion scam**, criminals impersonate law enforcement (CBI, Mumbai Crime Branch, Customs) over video calls, claiming:
> *"Armed officers are standing outside your front door right now. Transfer ₹4,50,000 immediately or we will break the door!"*

Conversational LLMs analyzing only audio/text transcripts often struggle to disprove this threat with certainty. `ring-evidence-mcp` solves this by giving the agent direct access to the **Ring Doorbell Physical Oracle**:
- The agent queries `verify_porch_claim("police_at_door")`.
- Ring reveals **0 humans** and **0 vehicles** at the front door.
- **Physical Contradiction Caught**: The agent confirms with 99% certainty that the caller is lying, halts outgoing bank transfers, and triggers emergency alerts.

---

## 🚀 Key Features

- **Standard MCP Protocol**: Compatible with Claude Desktop, Cursor, Amazon Bedrock Agent, and any standard MCP client.
- **Dual API / Sandbox Architecture**:
  - Live queries against the official **Ring Partner API** (`https://api.amazonvision.com/v1/devices`).
  - Seamless, zero-config fallback to sanitized offline fixtures when offline or during automated testing.
- **Cryptographic Evidence Integrity**: Every door evidence payload is signed with a deterministic **SHA256 integrity digest**.
- **Ready-to-Use Cross-Examination Tool**: High-level `verify_porch_claim` tool cross-checks common extortion claims (police at door, raid underway, seized contraband, genuine parcel deliveries).

---

## 📦 Installation

### From Source
```bash
cd ring-evidence-mcp
pip install -e .
```

### Direct Pip Install
```bash
pip install mcp httpx pydantic
```

---

## 🛠️ MCP Tools Exposed

### 1. `get_door_evidence`
Retrieves ground-truth entrance telemetry for a given lookback window.

**Arguments:**
| Parameter | Type | Default | Description |
|---|---|---|---|
| `window_hours` | `int` | `6` | Number of hours to inspect for events (1 to 72). |

**Response Schema:**
```json
{
  "timestamp": "2026-10-21T09:48:37Z",
  "window_hours": 6,
  "door_status": "CLEAR",
  "human_events_count": 0,
  "package_events_count": 0,
  "motion_events_count": 0,
  "ding_events_count": 0,
  "device_id": "ava1.ring.device.sandbox_sanitized_demo",
  "device_name": "Playground Device",
  "device_kind": "doorbell_pro",
  "snapshot_reference": "https://app-content.ring.com/shared/images/devices/square_device_images/DoorbellPro/rvdp_3x.png",
  "verified_by": "Live Ring Partner API (https://api.amazonvision.com)",
  "is_fallback": false,
  "sha256_integrity_hash": "a2b0d17ea4797d556a4cc7e0e93c0e045d0777b1309a1ca0976a2c5788c6b2da"
}
```

---

### 2. `verify_porch_claim`
Cross-examines an external assertion against verified Ring physical evidence to flag extortion lies.

**Arguments:**
| Parameter | Type | Default | Description |
|---|---|---|---|
| `claim_type` | `str` | *required* | Assertion or transcript phrase (e.g. `"police_at_door"`, `"raid_underway"`, `"parcel_seized"`, or natural dialogue). |
| `window_hours` | `int` | `6` | Time window to check against. |

**Example Response (Extortion Contradiction Proved):**
```json
{
  "claim_analyzed": "police_at_door",
  "contradiction_detected": true,
  "verdict": "CONTRADICTION_PROVED",
  "confidence": 0.99,
  "summary": "Caller claims law enforcement / police officers are outside your front door right now, but Ring Doorbell verifies 0 people and 0 vehicles at the entrance in the last 6 hours.",
  "recommended_action": "INTERVENE_AND_ALERT",
  "door_evidence": { ... }
}
```

---

## ⚙️ Configuration & Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `RING_ACCESS_TOKEN` | Optional | `None` | Bearer token from Ring Partner API / Developers Playground. If absent, uses sanitized fixtures. |
| `RING_API_BASE_URL` | Optional | `https://api.amazonvision.com` | Ring Partner REST API endpoint. |
| `RING_DEVICE_ID` | Optional | Auto-discovered | Target Ring Doorbell device ID. |

---

## 🔌 Connecting to MCP Clients

### 1. Claude Desktop Configuration
Add the following snippet to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "ring-evidence": {
      "command": "python",
      "args": [
        "-m",
        "ring_evidence_mcp.server"
      ],
      "env": {
        "RING_ACCESS_TOKEN": "eyJhbGciOi...",
        "RING_API_BASE_URL": "https://api.amazonvision.com"
      }
    }
  }
}
```

### 2. Direct Programmatic Usage in Python
```python
import asyncio
from ring_evidence_mcp.server import mcp, verify_porch_claim

async def main():
    # Direct function execution
    verdict = await verify_porch_claim("Officers outside door")
    print("Contradiction:", verdict["contradiction_detected"])
    print("Summary:", verdict["summary"])

    # Or via MCP protocol call_tool
    res = await mcp.call_tool("get_door_evidence", {"window_hours": 6})
    print("Evidence:", res)

asyncio.run(main())
```

---

## 🧪 Testing & Verification

Run the standalone verification suite:
```bash
python tests/test_mcp_server.py
```

Expected output:
```text
=================================================================
🔔 RING-EVIDENCE-MCP STANDALONE TEST RUNNER
=================================================================

--- Testing Tool Registration ---
Registered Tools: ['get_door_evidence', 'verify_porch_claim']
✔ Tool registration test passed.

--- Testing get_door_evidence Direct Call ---
Device ID: ava1.ring.device.sandbox_sanitized_demo
Door Status: CLEAR
Human Count: 0
Integrity Hash: 19ce70fe13793778d07baaf24716d728adb5ff5dea25886259a8ff64ffaa117a
✔ Direct get_door_evidence execution passed.

--- Testing verify_porch_claim (Extortion Claim) ---
Claim Analyzed: police_at_door
Contradiction Detected: True
Verdict: CONTRADICTION_PROVED
Action: INTERVENE_AND_ALERT
✔ Physical contradiction verification passed.

--- Testing MCP Server Tool Dispatch ---
✔ MCP JSON-RPC / Protocol call_tool dispatch passed.

=================================================================
🎉 ALL 4 STANDALONE MCP TESTS PASSED (100% SUCCESS)!
=================================================================
```

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.
Part of the open-source **MIRAGE-SHIELD** scam defense ecosystem.
