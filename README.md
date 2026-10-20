# 🛡️ MIRAGE-SHIELD

> **Living-Room Defense Against "Digital Arrest" & Courier-Extortion Scams**
> *Ring Primary Track · AWS Builder Mini-Challenge · Open Source Mini-Challenge*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Ring Partner API](https://img.shields.io/badge/Ring%20API-api.amazonvision.com-00d2ff.svg)](https://developer.amazon.com/ring)
[![AWS Bedrock](https://img.shields.io/badge/AWS-Bedrock%20%7C%20KMS%20%7C%20DynamoDB-orange.svg)](https://aws.amazon.com/bedrock/)
[![Test Suite](https://img.shields.io/badge/Tests-15%2F15%20Passing-brightgreen.svg)](test_scenarios.py)

---

## The Problem: The "Digital Arrest" Epidemic

Scammers in India and across the globe are impersonating police, CBI officers, and customs officials on video calls. They manipulate victims with:
1. **Isolation demands**: *"Do not disconnect. Close your door. You are under digital arrest."*
2. **Fake contraband claims**: *"A seized FedEx parcel in your name contained narcotics and fake passports."*
3. **Physical-world lies**: *"Police officers are outside your front door right now. If you don't transfer money to the RBI verification escrow account, they will break the door."*

Victims panic because they are trapped on a 6-inch phone screen in a psychological state of fear.

---

## The Solution: 2 Inputs · 1 Agent · 4 Living-Room Shields

**Core Claim**: Scammers win by lying about the physical world. **MIRAGE-SHIELD catches the lie using Ring physical sensors and shatters the isolation on the biggest screen in the house (the living-room Fire TV).**

```
┌─────────────────────────────────┐       ┌───────────────────────────────────┐
│     Incoming Video Call         │       │    Ring Video Doorbell Sensors    │
│  - Deepfake Frame Analysis      │       │  - 3D Motion & Human Detection    │
│  - Transcript Coercion NLP      │       │  - Package Delivery Verification  │
│  - Physical Claim Extraction    │       │  - Snapshot Cryptographic Hash    │
└────────────────┬────────────────┘       └─────────────────┬─────────────────┘
                 │                                          │
                 └────────────────────┬─────────────────────┘
                                      ▼
                    ┌───────────────────────────────────┐
                    │    Strands / Bedrock AI Brain     │
                    │   Cross-examines claim vs Ring:   │
                    │   Caller claims police at door?   │
                    │   Ring proves 0 people outside!   │
                    │    ==> PHYSICAL CONTRADICTION     │
                    └─────────────────┬─────────────────┘
                                      │
         ┌────────────────────────────┼────────────────────────────┐
         ▼                            ▼                            ▼
┌──────────────────┐        ┌──────────────────┐        ┌──────────────────┐
│ 📺 Fire TV Alert │        │ 🔒 Payment Guard │        │ 👨‍👩‍👧 Family Co-Sign│
│ Living room TV   │        │ Outgoing bank &  │        │ Instant SMS alert│
│ takeover with    │        │ UPI transfers    │        │ & secondary key  │
│ Ring evidence!   │        │ frozen instantly!│        │ release workflow │
└──────────────────┘        └──────────────────┘        └──────────────────┘
```

---

## ⚡ Quickstart: One-Command Setup

### 1. Clone & Install Dependencies

```bash
git clone https://github.com/your-team/MIRAGESHEILD.git
cd MIRAGESHEILD

# Install requirements
pip install -r requirements.txt
```

### 2. Configure Environment (Optional)

```bash
cp .env.example .env
# Edit .env with your Ring or AWS credentials, or run directly in resilient sandbox mode!
```

### 3. Launch the Complete System

```bash
python run.py
```

Once booted, open your browser:
- 🎛️ **Master Console**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/) *(Multi-device ecosystem: Phone, TV, Ring, Family, and AWS audit)*
- 📺 **Fire TV Takeover**: [http://127.0.0.1:8000/firetv](http://127.0.0.1:8000/firetv) *(10-foot living room screen)*
- 📖 **Interactive API Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧪 Run Automated Integration Suite (15/15 Tests)

To verify all roadmap gates (running Scenarios 1, 2, and 3 five consecutive times):

```bash
python test_scenarios.py
```

Output:
```
======================================================================
🧪 MIRAGE-SHIELD INTEGRATION VERIFICATION SUITE
   Running Scenarios 1, 2, and 3 (5 consecutive iterations each)
======================================================================
▶ Testing SCENARIO 1: Digital Arrest Extortion (Scam Caught)...
   ✔ Iteration 1/5 PASSED (Contradiction Caught, TV Takeover Triggered, Payment Locked)
   ✔ Iteration 2/5 PASSED ... [5/5 PASSED]
▶ Testing SCENARIO 2: Genuine Family Video Call (Zero False Alarms)...
   ✔ Iteration 1/5 PASSED ... [5/5 PASSED]
▶ Testing SCENARIO 3: Real Amazon Courier Delivery (Verified Delivery)...
   ✔ Iteration 1/5 PASSED ... [5/5 PASSED]
▶ Testing AWS KMS Cryptographic Signature Ledger...
   ✔ Cryptographic Sign PASSED
🎉 ALL INTEGRATION TESTS PASSED: 15/15 runs successful (100% PASS RATE)
```

---

## 📁 Monorepo Directory Structure

```
MIRAGESHEILD/
├── ring_service/          # Official Ring Partner API client, Webhooks (HMAC-SHA256), Door Oracle
├── detector/              # Deepfake visual frame scorer, STT, and Coercion Script Classifier
├── agent/                 # Strands / Bedrock AI reasoning engine, Payment Guard, and AWS KMS Ledger
├── firetv_app/            # Fire TV & Vega OS 10-foot living room takeover application (D-pad support)
├── web_console/           # Interactive Master Console (Phone, TV, Ring Doorbell, Family Guardian)
├── shared/                # Pydantic schemas (DoorEvidence, CallRisk, Verdict) & scenario fixtures
├── open_source/           # ring-evidence-mcp: Standalone Model Context Protocol (MCP) server
├── docs/                  # ARCHITECTURE.md, FRICTION_LOG.md, PRODUCT_FEEDBACK.md, AWS_BUILDER.md
├── static/                # High-definition visual assets (Ring doorbell snapshots & video calls)
├── test_scenarios.py      # Automated 15-run verification test suite
├── run.py                 # Single-command unified server launcher
├── requirements.txt       # Unified Python dependencies
├── .env.example           # Environment configuration template
└── LICENSE                # MIT Open Source License
```

---

## 🏆 Hackathon Tracks & Challenges

| Track | Implementation | Deliverable |
|:---|:---|:---|
| **Ring Primary Track** | Real calls to `api.amazonvision.com` (devices, event history, snapshots, HMAC webhooks, chime playback) | [`ring_service/`](ring_service/) |
| **AWS Builder Track** | Amazon Bedrock (Strands Agents), AWS KMS cryptographic signing, Amazon DynamoDB incident ledger, Transcribe | [`docs/AWS_BUILDER.md`](docs/AWS_BUILDER.md) |
| **Open Source Track** | Reusable `ring-evidence-mcp` (Model Context Protocol server for AI agents) on PyPI | [`open_source/ring_evidence_mcp/`](open_source/ring_evidence_mcp/) |

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
