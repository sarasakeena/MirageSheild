# `ring-evidence-mcp`

> **Model Context Protocol (MCP) server exposing Amazon Ring video doorbells as a physical-world Evidence Oracle for AI agents.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![MCP Compliant](https://img.shields.io/badge/MCP-2024--11--05-green.svg)](https://modelcontextprotocol.io)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

---

## Why It Matters

In modern social engineering attacks—most notably **"digital arrest" and courier extortion scams**—scammers succeed by **lying about the physical world**:
- *"Police officers are standing outside your door right now."*
- *"A seized narcotics package in your name was confiscated."*
- *"You cannot disconnect or open your door; you are under surveillance."*

AI agents monitoring calls or protecting vulnerable seniors cannot debunk these lies through language models alone. **`ring-evidence-mcp` bridges this gap.** It connects an agent to the physical reality of the front door, providing immutable sensor-backed proof of what actually happened.

---

## Features

- 🔍 **`get_door_evidence(window_hours, device_id)`**:
  Queries Ring event history for human, vehicle, and package events over a rolling window. Computes an integrity hash of the latest camera snapshot.
- ⚖️ **`verify_physical_claim(claim_type, window_hours)`**:
  Directly cross-checks physical assertions (e.g. `officers_at_door`, `package_delivered`) against Ring sensor ground truth.
- 🔊 **`trigger_chime_alert(audio_ref)`**:
  Plays an urgent audio slot on the living room Ring Chime device to break the victim's trance.
- 🛡️ **Resilient Token Expiry Handling**:
  Gracefully refreshes Ring OAuth tokens, retries transient API errors, and seamlessly operates against `ring-sandbox` fixtures when offline.

---

## Installation

```bash
pip install ring-evidence-mcp
```

Or run directly from source:

```bash
python -m open_source.ring_evidence_mcp.server
```

---

## MCP Configuration

Add this server to your Claude Desktop, Bedrock Strands, or Antigravity configuration file (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "ring-evidence": {
      "command": "python",
      "args": ["-m", "open_source.ring_evidence_mcp.server"],
      "env": {
        "RING_API_TOKEN": "your_ring_partner_api_token",
        "RING_API_BASE_URL": "https://api.amazonvision.com",
        "RING_SANDBOX_MODE": "false"
      }
    }
  }
}
```

---

## Example Tool Output

```json
{
  "device_id": "ring_doorbell_01_entrance",
  "device_name": "Front Door Video Doorbell Pro 2",
  "window_hours": 6,
  "human_events_count": 0,
  "vehicle_events_count": 0,
  "package_events_count": 0,
  "ding_events_count": 0,
  "latest_snapshot_hash": "sha256_9f83c18b76d0d2ff881679058b8d4f40f0c05763bf84c35626eb06c4ff94e09d",
  "door_status": "CLEAR",
  "summary": "0 people, 0 parcels in 6 hours"
}
```

---

## License

MIT License. Copyright (c) 2026 MIRAGE-SHIELD Team.
