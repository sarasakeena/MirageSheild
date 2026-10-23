# 🛡️ MIRAGE-SHIELD: Comprehensive Frontend Architecture & Design Audit

> **Amazon Build Hackathon 2026** — *Ring Primary Track + AWS Builder + Open Source Challenge*  
> **Submission Deadline**: October 23, 18:00 IST  
> **Backend Status**: **FROZEN & VERIFIED** (`verify_all.py` 2/2 required gates passed; `test_scenarios.py` 15/15 passed)  
> **Audit Focus**: Frontend authenticity, visual polish, demo recording impact, and zero-risk refinement roadmap.

---

## 1. Frontend Inventory & Architecture

### 1.1 Complete Frontend File Tree

```text
MirageSheild/
├── web_console/
│   └── static/
│       ├── index.html       # Master Console HTML shell (Top Nav, Scenario Bar, 2-Col Theater Grid, Diagnostics Drawer)
│       ├── style.css        # Master Console design system, dark theme tokens, layout grid, component styling (1,257 lines)
│       └── app.js           # Console Controller: scenario switching, Ring health polling, payment & co-sign state (473 lines)
├── firetv_app/
│   └── static/
│       ├── index.html       # Standalone 10-foot Fire TV interface (Ambient Screensaver & Fullscreen Scam Takeover) (176 lines)
│       ├── tv.css           # 10-foot TV styles: viewport units (vw), overscan margins, D-Pad focus halo rings (587 lines)
│       └── tv.js            # TV Controller: D-Pad remote key handling, 1500ms verdict polling, clock ticker (141 lines)
└── static/
    └── images/
        ├── scam_officer_call.jpg         # Staged video call feed: Fake police officer in uniform (Scenario 1) (729 KB)
        ├── genuine_daughter_call.jpg     # Genuine family video call feed: Daughter portrait (Scenario 2) (743 KB)
        ├── scenario1_empty_porch.jpg     # Ring doorbell camera snapshot: Porch clear, 0 humans (Scenarios 1 & 2) (985 KB)
        └── scenario3_amazon_delivery.jpg # Ring doorbell camera snapshot: Real Amazon delivery courier with parcel (Scenario 3) (1.0 MB)
```

### 1.2 Technology Stack & Dependencies

| Layer | Implementation | Notes / Constraints |
|:---|:---|:---|
| **Core Framework** | Vanilla HTML5 + ES6 JavaScript | Zero npm, zero bundler, zero build step; served directly by FastAPI |
| **Styling** | Vanilla CSS3 with Custom Properties | CSS Grid & Flexbox; scoped variables in `:root` |
| **Typography** | Google Fonts CDN | `Outfit` (Headings/Display), `Inter` (Body/UI), `JetBrains Mono` (Telemetry/Code) |
| **Iconography** | Native System Emoji | 🛡️, ⚙️, 📱, 📺, 👤, 📦, 🔔, 📞, ⏹, 🔒, 🛑, ✔, ✖, 🚨 (No SVG icon sprite library) |
| **External CDN Assets** | Ring Hardware CDN | `https://app-content.ring.com/.../DoorbellPro/rvdp_3x.png` (Ring Doorbell Pro hardware thumb) |
| **Web Server Mount** | FastAPI `StaticFiles` in `run.py` | Mounted at `/`, `/console`, `/firetv`, and `/static` |

### 1.3 Serving Routes in `run.py`

- `GET /`: Serves `web_console/static/index.html` as the default landing view.
- `GET /console`: Static mount of `web_console/static/` (with HTML directory serving).
- `GET /firetv`: Static mount of `firetv_app/static/` (serves 10-foot Fire TV simulator).
- `GET /static/...`: Serves static image assets (`/static/images/...`).
- `GET /api/ring/snapshot/latest.jpg`: Returns latest Ring doorbell snapshot dynamically based on `current_state["scenario_id"]`.

---

## 2. Screen-by-Screen Breakdown

### 2.1 Master Console (`web_console/static/index.html`)

| Property | Details |
|:---|:---|
| **Responsible Files** | [index.html](file:///c:/Users/Dell/OneDrive/Desktop/Tabu/MirageSheild/web_console/static/index.html), [style.css](file:///c:/Users/Dell/OneDrive/Desktop/Tabu/MirageSheild/web_console/static/style.css), [app.js](file:///c:/Users/Dell/OneDrive/Desktop/Tabu/MirageSheild/web_console/static/app.js) |
| **Layout Structure** | Fixed Top Nav (`.top-nav`), Scenario Switcher Bar (`.scenario-bar`), 2-Column Incident Theater (`35%` Phone Col, `65%` TV Col), Collapsible Bottom Drawer (`.bottom-drawer-container`), Footer (`.console-footer`). |
| **Data Sources** | Live API: `GET /api/ring/health`, `POST /api/scenario/{id}`, `POST /api/payment/attempt`, `POST /api/payment/cosign`. |
| **State Transitions** | Clicking Scenarios 1, 2, or 3 calls `runScenario(id)`: dynamically updates text content, images, badge classes, and posts live verdicts. |

### 2.2 Victim's Smartphone Panel (Phone View)

| Property | Details |
|:---|:---|
| **Responsible Files** | [index.html:L68-126](file:///c:/Users/Dell/OneDrive/Desktop/Tabu/MirageSheild/web_console/static/index.html#L68-L126), [style.css:L362-608](file:///c:/Users/Dell/OneDrive/Desktop/Tabu/MirageSheild/web_console/static/style.css#L362-L608), [app.js:L138-290](file:///c:/Users/Dell/OneDrive/Desktop/Tabu/MirageSheild/web_console/static/app.js#L138-L290) |
| **Components** | Device frame (`.phone-frame`), video feed box (`.video-container`), caller overlay (`.caller-id-overlay`), deepfake alert pill (`.deepfake-live-tag`), CSS audio waveform (`.audio-waveform-bar`), live transcript box (`.transcript-box`), regex coercion tags (`.phrase-tags`), bank frozen pill (`.bank-frozen-pill`), payment test action (`.payment-action-box`). |
| **Current Visual Style** | Dark rounded bezel (`border: 3px solid #232c3f; border-radius: 24px`), glowing red badges during Scenario 1, emerald during Scenario 2. |
| **Data Origin** | Dynamic from backend detector + fixtures via `POST /api/scenario/{id}`. Staged JPG video feed. Waveform is purely CSS keyframe simulation. |
| **Issues** | **Bug in Scenario 3**: Reuses `genuine_daughter_call.jpg` for the Amazon courier Ramesh! Phone chrome lacks realistic OS status bar (clock, cellular, battery, dynamic island). |

### 2.3 Fire TV Living Room Takeover Panel

| Property | Details |
|:---|:---|
| **Responsible Files** | **Console Embedded**: [index.html:L128-226](file:///c:/Users/Dell/OneDrive/Desktop/Tabu/MirageSheild/web_console/static/index.html#L128-L226)<br>**Standalone 10-Foot App**: [firetv_app/static/index.html](file:///c:/Users/Dell/OneDrive/Desktop/Tabu/MirageSheild/firetv_app/static/index.html), [tv.css](file:///c:/Users/Dell/OneDrive/Desktop/Tabu/MirageSheild/firetv_app/static/tv.css), [tv.js](file:///c:/Users/Dell/OneDrive/Desktop/Tabu/MirageSheild/firetv_app/static/tv.js) |
| **Components** | Emergency flasher badge, high-contrast headline banner, Ring camera feed snapshot with oracle badge, Physical Contradiction Callout box, 3 metric pills (Humans, Packages, Dings), Door/Chime status strip, Remote action buttons (1930 Helpline, End Call, View Doorbell). |
| **Current Visual Style** | High-contrast emergency red gradient with radial pulsing glow (`alarm-throb`), bright cyan Ring accents (`#00d2ff`), emerald verification badges (`#00e676`). |
| **Data Origin** | Backend `Verdict` object (`/api/verdict/latest`). Ring door evidence is real sensor data schema. |
| **Issues** | Text discrepancies between console embed and standalone `/firetv` page (e.g., headline copy differs). Action buttons display bracketed text like `[SELECT]` and `[▲ UP]` instead of authentic Fire TV remote button badges. |

### 2.4 Ring Doorbell Camera Panel

| Property | Details |
|:---|:---|
| **Responsible Files** | [index.html:L151-208](file:///c:/Users/Dell/OneDrive/Desktop/Tabu/MirageSheild/web_console/static/index.html#L151-L208), [style.css:L665-840](file:///c:/Users/Dell/OneDrive/Desktop/Tabu/MirageSheild/web_console/static/style.css#L665-L840) |
| **Components** | 16:9 doorbell camera snapshot (`.snapshot-display-wrap`), Ring Physical Oracle overlay badge, physical contradiction explanation banner, metric chips row, chime status indicator, SHA256 integrity hash chip. |
| **Current Visual Style** | Camera snapshot framed in 2px cyan border with a bottom-left green pill overlay. |
| **Data Origin** | Ring snapshot served via `/api/ring/snapshot/...`. Event counts (0 humans, 0 packages) from `DoorEvidenceOracle` and sanitized Ring sandbox fixtures. |
| **Issues** | Lacks authentic Ring app OSD overlays (Ring logo watermark in top-left corner, live timestamp in top-right, recording red dot indicator, WHEP 1080p stream badge). |

### 2.5 Family Guardian SMS & Co-Sign View

| Property | Details |
|:---|:---|
| **Responsible Files** | [index.html:L305-327](file:///c:/Users/Dell/OneDrive/Desktop/Tabu/MirageSheild/web_console/static/index.html#L305-L327), [style.css:L1140-1207](file:///c:/Users/Dell/OneDrive/Desktop/Tabu/MirageSheild/web_console/static/style.css#L1140-L1207), [app.js:L316-339](file:///c:/Users/Dell/OneDrive/Desktop/Tabu/MirageSheild/web_console/static/app.js#L316-L339) |
| **Components** | SMS bubble (`.alert-sms-bubble`), sender tag "SIMULATED SMS · 12:48 PM", message body, Co-sign control box with "✖ Block & File 1930" and "✔ Family Co-Sign" buttons, result status message. |
| **Current Visual Style** | Embedded inside Diagnostics Drawer Card 3. Red-tinted card with plain buttons. |
| **Data Origin** | Generated by `app.js` using scenario data. Button triggers real `POST /api/payment/cosign`. |
| **Issues** | **Hidden by default** inside the collapsed bottom drawer! During a video recording, the judge will not see the Family Guardian SMS or co-sign workflow unless the drawer is clicked. Visual presentation looks like a desktop card rather than a realistic mobile notification banner. |

### 2.6 AWS Audit Ledger & Cryptographic Verification View

| Property | Details |
|:---|:---|
| **Responsible Files** | [index.html:L274-303](file:///c:/Users/Dell/OneDrive/Desktop/Tabu/MirageSheild/web_console/static/index.html#L274-L303), [style.css:L1075-1139](file:///c:/Users/Dell/OneDrive/Desktop/Tabu/MirageSheild/web_console/static/style.css#L1075-L1139), [app.js:L341-356](file:///c:/Users/Dell/OneDrive/Desktop/Tabu/MirageSheild/web_console/static/app.js#L341-L356) |
| **Components** | Engine indicator (`#tel-agent`), scrolling terminal log box (`#agent-logs`), cryptographic signature box (`#kms-sig-display`), "✔ Verify Signature" button (`.audit-btn`), verification status text. |
| **Current Visual Style** | Purple accent theme (`rgba(168, 85, 247, 0.25)`), monospace code display. |
| **Data Origin** | Ingested via `/api/audit/incidents` or scenario verdict `signed_audit_record_id`. |
| **Issues** | Long raw hash string (`hmac_sha256_...`) wraps clumsily in small containers; verification button uses a simple 400ms setTimeout. |

---

## 3. Data & Integration Map

### 3.1 Backend Endpoints Called by Frontend

```
Frontend (app.js / tv.js)
  │
  ├── GET  /api/ring/health       ──> Checks Bearer JWT expiry, reports CONNECTED / TOKEN_EXPIRED
  ├── GET  /api/ring/devices      ──> Ingests official Ring JSON:API devices array & image_url
  ├── POST /api/scenario/{1|2|3}  ──> Triggers AI detector & agent brain; updates global state
  ├── GET  /api/verdict/latest    ──> Polled by Fire TV app (/firetv) every 1500ms
  ├── POST /api/payment/attempt   ──> Tests transfer against PaymentGuard (returns blocked: true/false)
  ├── POST /api/payment/cosign    ──> Authorizes fund unlock with "Rohan (Son)" family signature
  └── GET  /api/audit/incidents   ──> Retrieves signed incidents & KMS key ARN
```

### 3.2 Endpoint Payloads & Contracts

| Endpoint | Method | Request Body Shape | Response Payload Shape |
|:---|:---|:---|:---|
| `/api/scenario/{id}` | `POST` | Empty | `{ scenario_name, scenario_id, door_evidence: {...}, call_risk: {...}, verdict: {...} }` |
| `/api/verdict/latest` | `GET` | Empty | `{ verdict_id, action, contradiction_detected, contradiction_summary, door_evidence, call_risk, interventions, ... }` |
| `/api/payment/attempt` | `POST` | `{"amount_inr": 450000.0, "recipient_account": "998822114433"}` | `{"blocked": bool, "amount_inr": float, "reason": str, "lock_id": str}` |
| `/api/payment/cosign` | `POST` | `{"authorized_by": "Rohan (Son)"}` | `{"status": "unlocked", "authorized_by": str, "message": str}` |
| `/api/ring/health` | `GET` | `?refresh=false` | `{"status": str, "authenticated": bool, "mode": str, "is_playground": bool, "device_name": str}` |

### 3.3 Hardcoded, Mocked & Placeholder Inventory

1. **Static Waveform**: In `index.html:L89-93`, 9 `<span>` tags with CSS keyframe `wave` animation.
2. **Scenario 3 Courier Photo Reuse**: In `app.js:L255`, `callVideo.src = '/static/images/genuine_daughter_call.jpg';` is assigned for "Amazon Delivery (Ramesh)".
3. **Deepfake Badge**: Hardcoded string `"Deepfake analysis simulated"` in `app.js:L155` and `index.html:L84`.
4. **Fire TV Clock in `tv.js`**: `now.toUTCString()` prints UTC day/date which conflicts with the Indian Standard Time (IST) incident narrative.
5. **Static Device ID**: `ringDeviceIdChip.textContent = 'ava1.ring.device...'` placeholder.

---

## 4. Design System as It Exists Today

### 4.1 Token Palette

```css
:root {
  /* Surfaces */
  --bg-main: #07090e;
  --bg-card: rgba(13, 18, 30, 0.92);
  --bg-card-hover: rgba(20, 27, 44, 0.98);
  --border-subtle: rgba(255, 255, 255, 0.08);

  /* Accents */
  --cyan-ring: #00d2ff;       /* Ring & Living Room Brand */
  --red-alert: #ff2b43;       /* Scam Emergency */
  --emerald-safe: #00e676;    /* Safe / Porch Clear */
  --amber-warn: #ffb020;      /* Coercion Warning */
  --purple-aws: #a855f7;      /* AWS KMS & Cloud */

  /* Typography */
  --font-heading: 'Outfit', sans-serif;
  --font-text: 'Inter', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}
```

### 4.2 Inconsistencies & Fragmentations

- **Headline Copy Discrepancy**:
  - Console embed ([index.html:L143](file:///c:/Users/Dell/OneDrive/Desktop/Tabu/MirageSheild/web_console/static/index.html#L143)): `"🚨 DIGITAL ARREST SCAM DETECTED: HANG UP IMMEDIATELY"`
  - Standalone Fire TV ([firetv_app/index.html:L47](file:///c:/Users/Dell/OneDrive/Desktop/Tabu/MirageSheild/firetv_app/static/index.html#L47)): `"POLICE NEVER ARREST OVER VIDEO CALL"`
- **Button Border Radii**: Varies between `4px` (drawer), `6px` (pay-btn), `8px` (scenario), `10px` (theater actions), `12px` (TV D-Pad). Needs unified 8px/12px scale.
- **Glassmorphism Inconsistency**: Some cards use `backdrop-filter: blur(16px)`, others use flat `#0a0d16`.

### 4.3 Fire TV 10-Foot Compliance Check

| Guideline | Standard Requirement | Current Implementation | Verdict |
|:---|:---|:---|:---|
| **Overscan Margins** | Minimum 4% to 5% safe padding | `.tv-body` has padding `2.2vw 3.5vw 2.6vw 3.5vw` (~3.5% to 5%) | **PASS** |
| **Typography Scale** | Headlines ≥ 48px; Body ≥ 24px | Headlines at `3.4vw` (~65px on 1080p); body at `1.15vw` (~22px) | **MARGINAL** (Body slightly small) |
| **Color Contrast** | Minimum 4.5:1 ratio | White/Yellow text on dark red/navy (`#0d0e14` / `#2b060d`) > 9:1 | **PASS** |
| **D-Pad Focus States**| High-visibility focus ring | Border `#38bdf8`, glow `rgba(56, 189, 248, 0.95)`, scale `1.04` | **PASS** |
| **Remote Navigation** | Arrow keys + Enter key | Complete keydown dispatcher in [tv.js:L56-69](file:///c:/Users/Dell/OneDrive/Desktop/Tabu/MirageSheild/firetv_app/static/tv.js#L56-L69) | **PASS** |

---

## 5. "Feels Inauthentic / Unpolished" Diagnosis

### 5.1 What Looks "Prototype-y" or AI-Generated

1. **System Emojis as UI Icons**:
   - `📱 1. VICTIM'S SMARTPHONE`, `📺 2. LIVING ROOM FIRE TV TAKEOVER`, `👤 0 Humans`, `📦 0 Packages`, `🔔 0 Dings`, `📞 1930`.
   - On Windows 11, system emojis render as flat 2D cartoon icons with black outlines, immediately signaling an amateur prototype.
2. **Unrealistic Smartphone Chrome**:
   - The phone view is a simple rectangular box. Real phone screens in product demos have an authentic iOS/Android status bar (Carrier "Jio 5G", Signal bars, Wi-Fi, 12:48 PM, Battery 84%), a front-camera dynamic island/notch, and authentic floating call controls (red circular hangup button, mic mute, speaker toggle).
3. **Hidden Climax Features**:
   - The **Family Guardian SMS** and **Payment Co-Sign** are hidden inside the collapsed bottom drawer by default. If the presenter doesn't remember to toggle the drawer, the co-sign mechanism is never shown!
4. **Courier Video Feed Confusion (Scenario 3)**:
   - When switching to Scenario 3 (Amazon Delivery Ramesh), the phone feed continues displaying the photo of Pooja (Daughter). This is a glaring continuity error for judges.
5. **Raw D-Pad Button Labels**:
   - Buttons currently read `[SELECT] End Call & Protect Account`, `[▲ UP] View Doorbell Live`, `[▼ DOWN] Call 1930 Helpline`. Real Fire TV interfaces use sleek pill badges or remote button icons instead of bracketed text.
6. **No Ring Camera OSD**:
   - The doorbell feed snapshot lacks standard Ring telemetry: no `Ring` logo in the top-left, no live timestamp (`OCT 23 2026 12:48:12 IST`), no red recording dot, and no `1080p HD` indicator.

### 5.2 Evaluation Across Demo Video Moments

| Video Timestamp | Narrative Moment | Screen Evaluated | Current Appearance vs Real Product Feel |
|:---|:---|:---|:---|
| **0:15** | Fake Police Extortion Call | Victim Phone Col | **Moderate**. Shows transcript and coercion tag, but lacks believable phone UI chrome and live call duration timer (`00:14`). |
| **0:55** | **The Climax**: Ring CLEAR → TV Takeover → Chime → Payment Lock | Entire Screen (Theater Grid) | **High Impact, but jarring**. The contradiction is clear, but the split between "Scammer's False Claim" and "Ring Sensor Ground Truth" should be visually highlighted with an authentic side-by-side contrast badge. |
| **1:25** | Family Guardian SMS + Co-Sign Release | Bottom Drawer Card 3 | **Low Visibility / Risky**. Hidden in collapsed drawer. Needs to appear as a prominent mobile push notification with an authentic two-tap authorization button. |
| **1:45** | Genuine Call & Courier Scenarios | All Screens | **Confusing in Scenario 3**. Ramesh the delivery driver shows daughter Pooja's photo. Scenario 2 is clean and quiet. |

---

## 6. Prioritized Refinement Plan

### 6.1 Ranking Table: Impact vs. Effort

| Priority | Polish Item | Visual Impact | Effort (Mins) | Safety / Risk | Files to Touch |
|:---:|:---|:---:|:---:|:---:|:---|
| **#1** | **Authentic Smartphone Call UI & Chrome**<br>Add iOS/Android status bar (Jio 5G, clock, battery), camera notch, floating call action buttons (mute, keypad, end call), call duration counter (`02:14`). | **High** | 25m | Safe (CSS/HTML only) | `web_console/static/index.html`, `style.css` |
| **#2** | **Fix Scenario 3 Courier Identity & Avatar**<br>Create clean delivery courier avatar/badge for Ramesh in Scenario 3 so it doesn't display daughter Pooja's portrait. | **High** | 10m | Safe (app.js UI switch) | `web_console/static/app.js` |
| **#3** | **Authentic Ring Camera On-Screen Display (OSD)**<br>Add official Ring logo watermark, live timestamp (`OCT 23 2026 12:48:12 IST`), green `● LIVE` badge, and `1080p HD` chip over the snapshot. | **High** | 15m | Safe (HTML/CSS only) | `web_console/static/index.html`, `style.css` |
| **#4** | **Prominent Family Guardian SMS Push Banner**<br>Bring the Family Guardian SMS alert and Co-sign authorization into prominent view (or give it an animated pop-in notification card) so it is impossible to miss during recording. | **High** | 25m | Safe (CSS/HTML layout) | `web_console/static/index.html`, `style.css` |
| **#5** | **Replace System Emojis with Clean Inline SVG Icons**<br>Replace cartoonish system emojis (`📱`, `📺`, `👤`, `📦`, `🔔`, `📞`, `⚙️`, `🔒`) with crisp, professional SVG icons (Lucide/Feather style). | **High** | 20m | Safe (Markup/CSS only) | `web_console/static/index.html`, `style.css` |
| **#6** | **Harmonize Fire TV Headline & Remote Badges**<br>Align headline copy between console and `/firetv`; style `[SELECT]`, `[UP]`, `[DOWN]` as polished Fire TV remote keycaps. | **Med** | 15m | Safe (HTML/CSS) | `web_console/static/index.html`, `style.css`, `firetv_app/static/index.html`, `tv.css` |
| **#7** | **Physical Contradiction Split-Card Accent**<br>Emphasize the scammer claim vs. Ring truth with a sleek split badge: `CLAIM: Armed Police at Door` (Red) vs `RING TRUTH: 0 People / Clear` (Cyan/Green). | **Med** | 15m | Safe (CSS/HTML) | `web_console/static/index.html`, `style.css` |
| **#8** | **AWS KMS Cryptographic Seal Badge**<br>Upgrade the raw HMAC hash block into an official-looking AWS KMS cryptographic tamper-evident certificate stamp. | **Med** | 15m | Safe (HTML/CSS) | `web_console/static/index.html`, `style.css` |

### 6.2 Recommended Strategy

- **2-Hour Minimum-Viable Polish Pass** (Items #1 to #5):
  - Focus on what the camera sees in 1080p: Smartphone chrome, Ring camera OSD watermark, courier photo fix, prominent Family SMS push banner, and clean SVG icons.
- **Stretch Pass (+45 mins)** (Items #6 to #8):
  - Remote keycap badges, Physical Contradiction split-card, and AWS KMS cryptographic certificate seal.

---

## 7. Don't-Break List (Strict Zero-Regressions Guarantee)

The following element IDs, classes, and honest scoping labels are actively referenced by `app.js`, `tv.js`, or the backend contracts and **MUST NOT** be renamed or removed:

### 7.1 DOM IDs Required by `web_console/static/app.js`

- `call-video-feed`, `caller-name-display`, `caller-org-display`, `call-status-badge`
- `deepfake-tag`, `df-percentage`, `transcript-content`, `coercion-score-badge`, `detected-phrases-list`
- `bank-frozen-badge`, `btn-attempt-payment`, `payment-status-display`
- `tv-takeover-title`, `tv-takeover-subtitle`, `ring-oracle-badge`
- `ring-camera-feed`, `door-status-pill`, `door-hash-pill`
- `r-human-count`, `r-pkg-count`, `r-ding-count`, `r-chime-status`
- `oracle-verdict-callout`, `oracle-contradiction-desc`, `.callout-badge`
- `family-sms-body`, `family-status-badge`, `cosign-result-text`
- `agent-logs`, `kms-sig-display`, `verify-status-text`, `tel-agent`, `tel-agent-dot`
- `tel-ring`, `tel-ring-dot`, `ring-oracle-status-badge`, `ring-device-name`, `ring-device-id-chip`, `ring-device-thumb`, `ring-activity-log`
- `diagnostics-drawer`, `tray-toggle-btn`, `drawer-toggle-btn`, `tray-chevron`, `drawer-chevron`
- `btn-scen-1`, `btn-scen-2`, `btn-scen-3`

### 7.2 DOM IDs Required by `firetv_app/static/tv.js`

- `tv-ambient-screen`, `tv-intervention-screen`, `tv-clock`, `takeover-timestamp`
- `tv-snapshot-img`, `tv-contradiction-text`, `tv-human-count`, `tv-pkg-count`, `tv-ding-count`
- `tv-df-bar`, `tv-df-val`, `tv-coercion-bar`, `tv-coercion-val`
- `btn-hangup`, `btn-doorbell`, `btn-helpline`

### 7.3 Mandatory Honest Scoping Labels (Must Remain Visible)

Judges evaluate transparency. The following disclosure tags must be preserved:
- `[Simulated Gateway]` (on payment test buttons and transfer status)
- `Deepfake analysis simulated` (on deepfake signal tags)
- `[SIMULATED CHIME]` (on chime audio status)
- `SIMULATED SMS` / `[Simulated Response]` (on family alert and cybercrime forwarding)
- `VEGA OS 10-FOOT INTERVENTION UI` / `Fire TV Simulator (Vega OS)`
- `Local Rule Heuristic` / `LOCAL_HMAC_SHA256_SANDBOX` (when AWS credentials are not live)

---

## 8. Screenshot & Screen Recording Readiness

### 8.1 Ideal Viewport Dimensions for 1080p Recording

1. **Master Console (2-Column Theater)**:
   - **Resolution**: `1920 × 1080` (16:9 Full HD).
   - **Browser**: Chrome / Edge in fullscreen (`F11`), browser zoom at `100%` (or `90%` if taskbar is visible).
   - Ensure the scenario switcher bar and both columns (phone + TV card) fit fully within the fold without vertical page scrolling.
2. **Standalone Fire TV (`/firetv`)**:
   - **Resolution**: Exactly `1920 × 1080` in fullscreen mode.
   - Ideal for B-roll footage showing living room TV perspective.
3. **Smartphone Crop**:
   - If recording an inset picture-in-picture of the phone: `420 × 860` aspect ratio.

### 8.2 Clean-Up Checklist for Video Recording

- [ ] Hide any localhost URL banners or browser address bars (record via window capture or fullscreen F11).
- [ ] Ensure custom scrollbars are styled sleekly (`width: 4px; background: transparent;`) so thick grey default scrollbars don't appear.
- [ ] Pre-check that Ring Partner API token is active, or confirm the green "Doorbell Pro • 🟢 Connected (Playground API)" or fallback badge is cleanly rendered.

---

## Recommended First 5 Changes

When you give the go-ahead, we can implement these 5 safe, non-breaking refinements in under 45 minutes:

1. **Authentic Phone Frame Chrome**: Add an authentic mobile status bar (`Jio 5G`, `12:48 PM`, Wi-Fi, battery icons) and floating call control bar (`Mute`, `Keypad`, `End Call`).
2. **Ring Camera OSD Overlay**: Add the crisp `Ring` watermark, `● LIVE`, and timestamp stamp on the camera feed.
3. **Scenario 3 Courier Fix**: Swap out Pooja's portrait during Scenario 3 with an authentic delivery courier avatar/badge.
4. **Elevated Family SMS Alert**: Make the Family Guardian SMS notification and co-sign button visible and prominent without needing to expand the bottom drawer.
5. **Clean SVG Iconography**: Replace clunky Windows emoji with lightweight, sharp inline SVGs for security shield, phone, TV, package, bell, and locks.
