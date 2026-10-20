MIRAGE-SHIELD Development Roadmap

Oct 19, 2026 · @prajit

Mission and deadline

We ship MIRAGE-SHIELD, a living-room defence against "digital arrest" and courier-extortion scams, by Oct 24, 00:30 IST (Oct 23, 12:00 PM PDT). Confirm this on the Devpost page today; plan to submit by Oct 23, 18:00 IST to keep a 6-hour buffer.

Core claim: Scammers win by lying about the physical world ("officers are outside your door", "a parcel in your name was seized") while keeping the victim isolated on a video call. MIRAGE-SHIELD catches the lie with three signals and breaks the isolation on the biggest screen in the house.

Ring as the evidence oracle. Ring event history, live status and snapshots prove whether anyone or any parcel actually came to the door.

Deepfake and coercion detection. Our deepfake model checks the scam video call; a classifier flags coercion scripts in the transcript.

Fire TV intervention. A Vega OS app takes over the TV with the evidence, the law, the 1930 helpline and a family alert, while payments stay locked.

Entries: Ring primary track (fallback: Fire TV if the gallery looks thinner there on Oct 23), AWS Builder mini challenge, Open Source mini challenge.

Working mode: one team, one roadmap. Everyone works the same phase together; nobody starts the next phase until the current gate passes.

System architecture

MIRAGE-SHIELD architecture · 2 inputs, 1 agent, 4 outputs

The agent intervenes only when the call looks manipulated or coercive and Ring contradicts what the caller claims about the door.

Stack: Python (FastAPI) for the Ring service and detector; Strands Agents SDK on Bedrock, deployed to AgentCore Runtime or Lambda; AWS KMS and DynamoDB for signed incident records; Vega OS React Native app (fallback: Fire OS) for the TV; a small web console for the phone and family views; ring-api-helloworld, ringpartner and ring-sandbox for Ring access and testing.

Compliance checklist

Every item below is a disqualification or scoring risk, so we design against it from the first commit.

Rule

What it means for us

Ring tech must be called in code

Real calls to api.amazonvision.com (devices, event history, snapshots, webhooks, chime playback) in the main code path, not only in the README

Demo via simulator or device

Ring Developer Playground token or emulator is fine; show it working on screen

Video under 3 minutes, public, English

YouTube or Vimeo; best material in the first 30 seconds

No third-party footage or music

Film our own scam-call clips; use royalty-free or no music

Repo has all source and run instructions

One-command setup in README; .env.example, no secrets committed

Public repo with OSI license, or private and shared

Default: public with MIT license on submission day (avoids expiring collaborator invites)

Product feedback for every tool used

Ring API, Vega SDK, Bedrock/AgentCore, Kiro: what worked, what didn't, onboarding, would we reuse

AWS Builder fields

Document each AWS service and how it is used

Open Source fields

Contribution URL, repo URL, GitHub username, what/how/why

Friction log (optional, up to 10% bonus)

Task, steps, expected vs actual, severity, workaround, suggestion; target 6 to 8 entries

Honest scoping

State plainly: simulator footage, test-mode payments, staged scam call

Rule for the whole build: the moment anyone hits friction with a tool, they add a friction-log row in the shared sheet before fixing it.

Day 1 (Oct 19, evening to Oct 20, morning): foundations

Goal: every external dependency answers a hello-world call before anyone writes product code.

Block 1 — Decisions and repo (2 hours)

☐ Confirm the deadline and rules on the Devpost page; register the team

☐ Answer two blocking questions: does anyone own a Ring doorbell? Is anyone on macOS or Ubuntu for the Vega tools?

☐ Create the monorepo: /ring-service, /detector, /agent, /firetv-app, /web-console, /docs

☐ If using Kiro, open the repo in Kiro and commit the /.kiro folder from commit 1

☐ Add MIT license, README skeleton, .env.example, .gitignore

☐ Create the friction-log sheet and the product-feedback notes file

Block 2 — Ring access (3 hours)

☐ Clone AmazonAppDev/ring-api-helloworld and run it

☐ Get a Developer Playground token (30-minute expiry) and call GET /v1/devices

☐ Call event history, a snapshot, and device configurations; save the raw responses as fixtures

☐ Check whether a chime device exists in the playground and list its audio_ref slots

☐ Install the ring-sandbox emulator so work never blocks on token expiry

Block 3 — Fire TV and AWS access (3 hours)

☐ Install Vega Developer Tools and boot the Vega Virtual Device; run vega-video-sample

☐ If Vega tools fail on our machines, fall back to a Fire OS app (React Native or Kotlin) on the Android TV emulator

☐ Enable Bedrock model access in our AWS account; make one test call from Python

☐ Install the Strands Agents SDK and run its hello-world agent

Block 4 — Interface contracts (1 hour)

☐ Write the JSON schema for the three messages the system passes: DoorEvidence, CallRisk, Verdict

☐ Commit sample JSON for each so every component can be built against fakes

Gate to Day 2: a Ring device list, a Vega app on screen, a Bedrock reply, and the three schemas are all in the repo.

Day 2 (Oct 20): core pipelines

Goal: each of the four pipelines works on its own against fake inputs from the Day 1 schemas.

Pipeline A — Ring evidence service

☐ Webhook endpoint with HMAC-SHA256 verification; respond 200 within 5 seconds and process asynchronously

☐ get_door_evidence(window) tool: queries event history for human, vehicle, package and ding events in the last N hours

☐ Fetch the latest snapshot for the window and store its hash

☐ Return a DoorEvidence object: "0 people, 0 parcels in 6 hours" plus snapshot link

☐ Chime alert: play one pre-loaded audio_ref when a scam is confirmed (skip if no chime in playground)

Pipeline B — Scam-call detector

☐ Record our own staged scam calls (fake "officer", fake police backdrop) and genuine calls as test clips

☐ Adapt our existing deepfake model to score video frames from a call clip; output a 0–1 manipulation score

☐ Speech-to-text on the call audio (Amazon Transcribe or Whisper)

☐ Coercion-script classifier on the transcript: flags isolation demands, fake warrants, seized-parcel claims, payment demands

☐ Extract physical-world claims ("officers at your door", "parcel seized") as structured items for the agent to check

☐ Return a CallRisk object

Pipeline C — Agent brain

☐ Strands agent with tools: get_door_evidence, score_call, lock_payments, notify_family, trigger_tv_alert

☐ Decision logic: deepfake score + coercion flags + Ring contradicting a claim → Verdict (safe / warn / intervene)

☐ Payment lock: a test-mode transfer stays blocked while an intervention is active; family co-sign releases it

☐ Sign each verdict with AWS KMS and store it in DynamoDB as an incident record

☐ Deploy to AgentCore Runtime if time allows; otherwise Lambda, and note it

Pipeline D — Fire TV app

☐ Home screen and a full-screen intervention screen with D-pad focus

☐ Intervention screen shows: Ring snapshot and "no one at your door" evidence, the deepfake score, the line "police never arrest over video call", 1930 helpline, family notified

☐ Poll or subscribe to the backend for new verdicts

Gate to Day 3: each pipeline returns correct output for one scam clip and one genuine clip, using fakes for its neighbours.

Day 3 (Oct 21): end-to-end integration

Goal: one staged scam call flows through the whole system and ends on the Fire TV screen with no manual steps.

Morning — wire the loop

☐ Replace every fake with the real component: call clip → detector → agent → Ring evidence → verdict → Fire TV + chime + family alert

☐ Web console (the "victim's phone" view): plays the scam call, shows live risk score, tries a payment that gets blocked

☐ Family view: receives the alert and can co-sign to release a payment

☐ Measure time from the scam claim being spoken to the TV takeover; target under 10 seconds

Afternoon — the three demo scenarios

☐ Scenario 1, scam caught: fake officer claims a seized parcel and officers outside; Ring shows nobody → intervene

☐ Scenario 2, genuine call: a real relative calls, no coercion, no deepfake → stays quiet (proves low false alarms)

☐ Scenario 3, real courier: Ring shows a genuine package event; the agent confirms it and does not raise a false alarm

☐ Run each scenario 5 times; log failures and fix the top two

Evening — open source and hardening

☐ Extract the Ring evidence tool into a standalone MIT-licensed package (e.g. ring-evidence-mcp) or open a PR on ring-sandbox adding the scam-scenario scripts

☐ Write its README: what it does, how it works, why it matters

☐ Handle the 30-minute token expiry, webhook retries and empty event history gracefully

☐ Optional, only with a physical Ring doorbell: passive screen-replay check on the door snapshot

Gate to Day 4: all three scenarios pass 5 times in a row on a clean clone using the README steps.

Day 4 (Oct 22 to Oct 23): freeze, film, submit

Goal: a submitted entry by Oct 23, 18:00 IST, six and a half hours before the hard deadline.

Oct 22, morning — polish

☐ Fix only demo-path bugs; no new features after 12:00 IST

☐ Make the Fire TV intervention screen look finished: large type, high contrast, clear evidence panel

☐ Clean-clone test: someone who did not write the code follows the README on a fresh machine

Oct 22, afternoon — feature freeze at 16:00 IST, then film

☐ Record each demo scenario screen-by-screen at 1080p; record a backup take of everything

☐ Record the voice-over separately for clean audio

☐ Edit to under 2:55; check no third-party music or footage is in it

☐ Upload to YouTube as public; watch it once on a phone

Oct 22, evening — write-ups

☐ Devpost description: problem, how it works, architecture image, what's real vs simulated

☐ Product feedback for Ring API, Vega SDK, Bedrock/AgentCore/Strands, Kiro

☐ AWS Builder section: each service and its role

☐ Open Source section: contribution URL, repo URL, GitHub username, description

☐ Friction log: clean up to 6 to 8 strong entries

☐ Optional feature requests with urgency labels

Oct 23 — submit

☐ Make the repo public with the MIT license (or private + add the six reviewers today)

☐ Final read of every submission field by two people

☐ Submit by 18:00 IST; screenshot the confirmation

☐ After submitting: check the Devpost gallery and decide Ring vs Fire TV primary track only if editing is still allowed

Demo video script (2:55)

The scam-caught moment lands inside the first 60 seconds, because judges may stop watching at any point.

Time

On screen

Voice-over (gist)

0:00–0:15

Black screen, one verified statistic, then a phone ringing

Digital arrest scams are draining Indian seniors; the scam starts with a lie about the physical world

0:15–0:55

Split screen: fake "officer" video call on the phone, the living-room TV, the Ring feed

The officer claims a seized parcel and police at the door; the deepfake score climbs

0:55–1:25

Agent checks Ring: zero people, zero parcels; TV takes over with the evidence; chime sounds; payment attempt blocked

Ring proves the claim is false; the TV breaks the isolation the scammer depends on

1:25–1:45

Family phone gets the alert; co-sign view

Family is pulled back in; money stays locked until they co-sign

1:45–2:10

Scenario 2 and 3 quickly: genuine call stays quiet; real courier is confirmed

It doesn't cry wolf: real people and real parcels pass

2:10–2:35

Architecture image; Ring API calls highlighted; signed incident record

How it works: Ring evidence, deepfake model, Bedrock agent, Fire TV app

2:35–2:55

Team, open-source package, one-line close

Scammers lie about the front door. Ring tells the truth.

Risks, fallbacks and cut order

The Ring evidence check and the Fire TV takeover are the product; everything else can be cut.

Risk

Fallback

Vega tools won't install on our machines

Fire OS app on the Android TV emulator; same screens

Playground token expires mid-demo

Record against ring-sandbox fixtures captured from the real API; say so in the write-up

No chime device in the playground

Drop the chime; the TV takeover carries the alert

Deepfake model weak on call video

Lean on coercion-script detection plus the Ring contradiction; show the deepfake score as one signal

Bedrock model access delayed

Strands with any already-enabled model; keep AWS for KMS, DynamoDB and Lambda

AgentCore deployment fails

Run the Strands agent on Lambda and note it in the AWS section

Integration slips past Day 3

Hard-wire the scenario order for the demo; keep the Ring calls real

Cut order if we fall behind:

Chime alert

Family co-sign screen (keep the notification)

AgentCore (use Lambda)

Scenario 3, real courier

Deepfake video score (keep transcript coercion detection)

Never cut: real Ring API calls, the Fire TV intervention screen, Scenario 1.

Facts to verify and final checklist

Nothing from the Gemini report goes into the pitch until it is checked against a primary source.

Verify before use

☐ Digital arrest loss figures: use MHA or I4C sources directly; the 2025 figure in the report may be total cyber fraud, not digital arrest alone

☐ Competitor projects named in the report (ATLAS Steward, VoiceGuard MCP, Hold On): confirm in the Devpost gallery

☐ AgentCore, Strands and model version names: take them from the docs at install time

☐ Vega Developer Tools OS support

☐ Whether the Ring playground exposes a chime and which event types it simulates

Already verified in Ring's official docs

Live video over WHEP is receive-only video, with no audio

Chime playback plays a pre-set audio_ref slot; it cannot speak arbitrary text

All Ring media carries a visible watermark

The simulator offers package, vehicle and motion live-view events

Final submission checklist

☐ Text description

☐ Repo link: public with MIT license, or private with all six reviewers added

☐ Demo video link, public, under 3 minutes, English

☐ Product feedback for every tool

☐ Track and mini challenges selected

☐ AWS Builder fields

☐ Open Source fields

☐ Friction log entries

☐ Statement of what is real, simulated and test-mode

Sources: Ring Partner API documentation · Ring live video streaming · Ring release notes · ring-api-helloworld · ringpartner Python SDK · Devpost hackathon page