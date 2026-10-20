# MIRAGE-SHIELD Devpost Submission Package

> **Living-Room Defense Against "Digital Arrest" & Courier-Extortion Scams**
> *Amazon Build Hackathon 2026*

---

## 1. Project Overview & Inspiration
Digital arrest and courier extortion scams have reached epidemic proportions, causing hundreds of crores in losses and targeting vulnerable citizens—particularly senior citizens living alone. Scammers succeed by manufacturing extreme psychological isolation: they impersonate law enforcement over video calls, threaten non-existent arrest warrants, demand that victims lock their doors, and claim police officers are waiting outside.

**Core Claim**: Scammers win by lying about the physical world while keeping the victim isolated on a small phone screen. **MIRAGE-SHIELD catches the lie with physical sensors and breaks the isolation on the biggest screen in the house (the living-room Fire TV).**

---

## 2. What It Does (The 3 Signals & 4 Shields)
1. **Ring as the Evidence Oracle**:
   When the scammer claims *"Police officers are outside your front door right now"*, MIRAGE-SHIELD queries Ring Doorbell event history (`get_door_evidence`). If Ring verifies 0 people and 0 vehicles at the entrance, the physical contradiction is immediately exposed.
2. **Deepfake & Coercion Detection**:
   Our computer vision model flags facial boundary warping and synthetic uniform insignia (92% likelihood); our NLP classifier flags isolation scripts, fake Section 67 NDPS warrants, and extortion demands (96% coercion score).
3. **Fire TV Takeover (Vega OS)**:
   In under 3 seconds from the scam claim being spoken, the living-room TV takes over with irrefutable proof: Ring camera snapshot of the empty porch, a bold alert that *"Police never arrest over video call"*, and direct access to the 1930 National Cyber Crime helpline.
4. **Payment Guard & Family Co-Sign**:
   All outgoing bank/UPI transfers are automatically frozen. Victims cannot transfer extortion funds without authenticated family co-sign authorization.

---

## 3. Demo Video Script (2:55 Timing)

| Time | On Screen | Voice-Over / Narrative |
|:---|:---|:---|
| **0:00 – 0:15** | Black screen with verified statistic: *Over ₹120 Crore lost to Digital Arrest scams in India in recent months.* Phone begins ringing. | "Digital arrest scams are draining innocent citizens. Scammers win through one weapon: lying about the physical world." |
| **0:15 – 0:55** | Split screen: Fake ACP officer on victim's smartphone, living-room Fire TV in ambient mode, Ring Doorbell live feed. Officer threatens an arrest memo and claims police are outside the door. Deepfake risk climbs to 92%. | "The fake officer claims a seized narcotics parcel and says police are standing outside her front door right now. The victim is terrified and isolated." |
| **0:55 – 1:25** | **The Scam-Caught Moment:** Agent checks Ring Oracle: 0 people, 0 parcels. Physical contradiction confirmed! Fire TV immediately takes over the screen. Ring chime sounds alarm. Victim attempts ₹4,50,000 transfer—it gets instantly BLOCKED. | "Ring proves the claim is an absolute lie. The living-room TV takes over, shattering the scammer's isolation. Outgoing bank transfers are locked down." |
| **1:25 – 1:45** | Family Guardian phone receives instant push alert with evidence. Family member reviews the contradiction and approves emergency protection. | "Family is immediately pulled back in. Money stays locked until family co-signs." |
| **1:45 – 2:10** | Rapid walkthrough of Scenarios 2 & 3: Genuine family call stays quiet; legitimate Amazon courier delivery is verified by Ring without false alarms. | "It doesn't cry wolf: real family calls pass silently, and real courier deliveries are verified." |
| **2:10 – 2:35** | Architecture & AWS telemetry: Bedrock reasoning trace, AWS KMS digital signature verification, and Amazon DynamoDB tamper-evident incident ledger. | "Under the hood: Amazon Bedrock reasoning, AWS KMS cryptographic signing, and Ring Partner API." |
| **2:35 – 2:55** | Open-source `ring-evidence-mcp` package announcement and closing. | "Scammers lie about the front door. Ring tells the truth. Introducing MIRAGE-SHIELD." |

---

## 4. Honest Scoping (What is Real, Simulated, and Test-Mode)
- **Real Ring API Calls**: Official Ring Partner API client (`api.amazonvision.com`) implemented in `ring_service/client.py` for `/v1/devices`, `/v1/devices/{id}/events`, snapshot hashes, and chime playback. Built-in sandbox mode uses captured API fixtures for offline resiliency.
- **Real Cryptographic Ledger**: AWS KMS digital signing (`RSASSA_PKCS1_V1_5_SHA_256`) and DynamoDB audit ledger.
- **Staged Scam Video Clips**: Video calls filmed with staged impersonation clips to comply with hackathon rules (no third-party copyrighted footage).
- **Test-Mode Payments**: Mock UPI / bank transfer gateway demonstrating instantaneous payment freeze and family co-sign authorization.

---

## 5. Track Selections & Submissions
- **Primary Track**: Ring Primary Track
- **Mini-Challenge 1**: AWS Builder Track (Bedrock, KMS, DynamoDB, Transcribe, Lambda)
- **Mini-Challenge 2**: Open Source Track (`ring-evidence-mcp` on PyPI / GitHub)
