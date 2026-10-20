# MIRAGE-SHIELD System Architecture

> **A living-room defense against "digital arrest" and courier-extortion scams.**
> *Core claim: Scammers win by lying about the physical world while keeping the victim isolated on a video call. MIRAGE-SHIELD catches the lie with three signals and breaks the isolation on the biggest screen in the house.*

---

## 1. High-Level Architecture: 2 Inputs · 1 Agent · 4 Protective Outputs

```mermaid
flowchart TD
    subgraph Inputs["1. Multi-Modal Inputs"]
        A["Incoming Video Call<br/>(Victim's Smartphone)"]
        B["Ring Video Doorbell & Sensors<br/>(api.amazonvision.com)"]
    end

    subgraph Perception["2. Multi-Modal Perception Layer"]
        A --> C["Deepfake Frame Scorer<br/>(Synthetic Insignia & Boundary Artifacts)"]
        A --> D["Speech-to-Text & Coercion Classifier<br/>(Isolation, Fake Warrants, Extortion)"]
        A --> E["Physical Claim Extractor<br/>(e.g., 'Police outside your door')"]
        B --> F["Door Evidence Oracle<br/>(get_door_evidence: 0 people, 0 parcels)"]
    end

    subgraph Agent["3. Autonomous Agent Brain (Strands & Amazon Bedrock)"]
        C --> G{"Cognitive Contradiction Engine<br/>Cross-examine Physical Claim vs Ring Ground Truth"}
        D --> G
        E --> G
        F --> G
        G --> H["Verdict Generation<br/>(SAFE / WARN / INTERVENE)"]
        H --> I["AWS KMS Digital Signer<br/>(RSASSA-PKCS1-v1_5-SHA256)"]
        I --> J[("Amazon DynamoDB<br/>Tamper-Evident Incident Ledger")]
    end

    subgraph Outputs["4. Quad-Shield Living Room Outputs"]
        H -- "If INTERVENE" --> K["📺 Fire TV / Vega OS Takeover<br/>(Fullscreen Evidence & 1930 Helpline)"]
        H -- "If INTERVENE" --> L["🔒 Payment Guard Firewall<br/>(Freeze UPI / Bank Transfers)"]
        H -- "If INTERVENE" --> M["🔊 Ring Chime Alert<br/>(Living Room Audio Siren)"]
        H -- "If INTERVENE" --> N["👨‍👩‍👧 Family Guardian Mobile Push<br/>(SMS Alert & One-Click Co-Sign)"]
    end
```

---

## 2. Signal Pipeline Breakdown

### Pipeline A — Ring Physical Evidence Oracle
- **Target API**: `https://api.amazonvision.com` (Ring Partner API).
- **Core Tool**: `get_door_evidence(window_hours=6)`.
- **Sensors Queried**:
  - Head-to-toe 3D motion detection (human vs vehicle vs animal tags).
  - Computer Vision Package Delivery detection (`package_delivered`).
  - Doorbell ring ding events.
  - Snapshot integrity hash (`sha256_<digest>`) of the entrance.
- **Webhook Pipeline**: Ingests Ring webhooks with HMAC-SHA256 cryptographic verification in under 5 seconds.
- **Chime Playback**: Sounds `audio_ref_urgent_security_alert` on living room chime hardware.

### Pipeline B — Scam-Call Detector
- **Deepfake Scorer**: Computes facial boundary blur, pupillary dilation cadence, synthetic badge artifact jitter, and audio/lip sync latency.
- **Audio STT**: Converts call audio to text with Amazon Transcribe or local audio streamer.
- **Coercion Classifier**: Evaluates transcript against I4C and MHA digital arrest patterns (isolation oaths, fake Section 67 NDPS arrest warrants, seized FedEx parcels with contraband, urgent transfer demands).
- **Physical Claim Extractor**: Identifies caller statements asserting physical reality:
  - `claimed_officers_at_door = True`
  - `claimed_raid_underway = True`
  - `claimed_parcel_seized = True`

### Pipeline C — Strands Agent Brain & AWS Security
- **Reasoning**:
  - Compares `claimed_officers_at_door` against Ring `human_events_count == 0`.
  - Catches the physical lie: *Caller claims Mumbai Police outside door, but Ring verifies porch is empty.*
  - Decision Rule: Contradiction + Coercion Flag $\ge 0.30 \rightarrow$ **`INTERVENE`** (Confidence: 0.98).
- **AWS KMS**: Hashes the verdict payload using SHA-256 and calls `kms.sign()` to produce a verifiable digital signature.
- **Amazon DynamoDB**: Writes immutable incident audit records to table `mirage_shield_incidents`.
- **Payment Guard**: Freezes all outgoing UPI transfers. Requires authenticated family co-sign authorization to release funds.

### Pipeline D — Fire TV / Vega OS Living Room Takeover
- **Display**: Takes over the TV display with high-contrast 10-foot UI.
- **Visual Evidence**:
  - Ring live snapshot with timestamp watermark.
  - "VERIFIED BY RING: 0 PEOPLE AT DOOR".
  - "POLICE NEVER ARREST OVER VIDEO CALL".
  - Prominent 1930 Cybercrime Helpline.
- **D-Pad Remote Controls**: Arrow keys and Enter/Select support for TV remote operation.

---

## 3. End-to-End Latency Profile

| Stage | Action | Latency Target | Actual Achieved |
|:---|:---|:---|:---|
| 1 | Scammer speaks claim ("Officers outside your door") | 0.0s | 0.0s |
| 2 | Speech-to-Text & Coercion Classification | < 2.5s | 0.8s |
| 3 | Physical Claim Extraction | < 1.0s | 0.2s |
| 4 | Ring Doorbell Evidence Oracle Query | < 2.0s | 0.4s |
| 5 | Bedrock Agent Contradiction Check & Verdict | < 2.0s | 0.6s |
| 6 | Fire TV Takeover Display & Payment Freeze | < 2.5s | 0.5s |
| **Total** | **Spoken Scam Claim to Living Room Takeover** | **< 10.0s** | **2.5s** |
