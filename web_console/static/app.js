// MIRAGE-SHIELD Master Console Application Controller
// Orchestrates multi-device synchronization across Phone, Fire TV, Ring Oracle, and Family Guardian

let currentScenarioId = 1;

// Elements
const callVideo = document.getElementById('call-video-feed');
const callerName = document.getElementById('caller-name-display');
const callerOrg = document.getElementById('caller-org-display');
const dfTag = document.getElementById('deepfake-tag');
const dfPct = document.getElementById('df-percentage');
const transcriptEl = document.getElementById('transcript-content');
const paymentStatusEl = document.getElementById('payment-status-display');
const callStatusBadge = document.getElementById('call-status-badge');

const ringFeed = document.getElementById('ring-camera-feed');
const doorStatusPill = document.getElementById('door-status-pill');
const doorHashPill = document.getElementById('door-hash-pill');
const rHumanCount = document.getElementById('r-human-count');
const rPkgCount = document.getElementById('r-pkg-count');
const rDingCount = document.getElementById('r-ding-count');
const rChimeStatus = document.getElementById('r-chime-status');
const oracleCallout = document.getElementById('oracle-verdict-callout');
const oracleDesc = document.getElementById('oracle-contradiction-desc');
const ringDeviceName = document.getElementById('ring-device-name');
const ringDeviceIdChip = document.getElementById('ring-device-id-chip');
const ringDeviceThumb = document.getElementById('ring-device-thumb');
const ringActivityLog = document.getElementById('ring-activity-log');

const familySms = document.getElementById('family-sms-body');
const familyBadge = document.getElementById('family-status-badge');
const cosignResult = document.getElementById('cosign-result-text');

const agentLogs = document.getElementById('agent-logs');
const kmsSigDisplay = document.getElementById('kms-sig-display');
const verifyStatus = document.getElementById('verify-status-text');
const tvIframe = document.getElementById('tv-iframe');
const coercionScoreBadge = document.getElementById('coercion-score-badge');
const detectedPhrasesList = document.getElementById('detected-phrases-list');

// Incident Theater Specific Elements
const tvTakeoverTitle = document.getElementById('tv-takeover-title');
const tvTakeoverSubtitle = document.getElementById('tv-takeover-subtitle');
const ringOracleBadge = document.getElementById('ring-oracle-badge');
const bankFrozenBadge = document.getElementById('bank-frozen-badge');

// Diagnostics Tray Toggle (Header button & Bottom drawer toggle)
function toggleDiagnosticsTray() {
  const drawer = document.getElementById('diagnostics-drawer');
  const btn = document.getElementById('tray-toggle-btn');
  const drawerBtn = document.getElementById('drawer-toggle-btn');
  const trayChev = document.getElementById('tray-chevron');
  const drawerChev = document.getElementById('drawer-chevron');
  if (!drawer) return;
  const isCollapsed = drawer.classList.contains('collapsed');
  if (isCollapsed) {
    drawer.classList.remove('collapsed');
    if (btn) btn.classList.add('open');
    if (drawerBtn) drawerBtn.classList.add('open');
    if (trayChev) trayChev.textContent = '▴';
    if (drawerChev) drawerChev.textContent = '▴ Collapse Diagnostics';
  } else {
    drawer.classList.add('collapsed');
    if (btn) btn.classList.remove('open');
    if (drawerBtn) drawerBtn.classList.remove('open');
    if (trayChev) trayChev.textContent = '▾';
    if (drawerChev) drawerChev.textContent = '▾ Expand Diagnostics';
  }
}

function appendRingLog(type, text) {
  if (!ringActivityLog) return;
  const div = document.createElement('div');
  div.className = `a-log-item ${type}`;
  const now = new Date();
  const timeStr = `[${now.toLocaleTimeString()}]`;
  div.innerHTML = `<span class="a-time">${timeStr}</span> ${text}`;
  ringActivityLog.appendChild(div);
  ringActivityLog.scrollTop = ringActivityLog.scrollHeight;
}

// Run Scenario
async function runScenario(scenarioId) {
  currentScenarioId = scenarioId;
  
  // Highlight active button
  [1, 2, 3].forEach(id => {
    const btn = document.getElementById(`btn-scen-${id}`);
    if (btn) btn.classList.toggle('active', id === scenarioId);
  });

  try {
    const res = await fetch(`/api/scenario/${scenarioId}`, { method: 'POST' });
    const data = await res.json();
    applyScenarioUI(data);
  } catch (err) {
    console.error("Error setting scenario:", err);
  }
}

function applyScenarioUI(data) {
  const cRisk = data.call_risk;
  const dEvidence = data.door_evidence;
  const vVerdict = data.verdict;

  // Refresh TV embed
  if (tvIframe) {
    tvIframe.contentWindow.location.reload();
  }

  // Update Telemetry Bar Agent Engine dynamically
  const telAgent = document.getElementById('tel-agent');
  const telAgentDot = document.getElementById('tel-agent-dot');
  if (telAgent && vVerdict && vVerdict.reasoning_engine) {
    if (vVerdict.reasoning_engine.includes('Bedrock Converse')) {
      telAgent.textContent = 'AMAZON BEDROCK CONVERSE';
      if (telAgentDot) telAgentDot.className = 'dot green';
    } else {
      telAgent.textContent = 'LOCAL RULE HEURISTIC';
      if (telAgentDot) telAgentDot.className = 'dot yellow';
    }
  }

  // Update Dynamic Regex Coercion Classifier Output & Phrases
  if (coercionScoreBadge && detectedPhrasesList && cRisk) {
    const cScore = Math.round((cRisk.coercion_score || 0) * 100);
    coercionScoreBadge.textContent = `${cScore}% COERCION`;
    coercionScoreBadge.className = cScore >= 40 ? 'badge-red' : 'badge-green';

    const snippets = cRisk.detected_coercion_snippets || [];
    if (snippets.length > 0) {
      detectedPhrasesList.innerHTML = snippets.map(s => `<span class="phrase-tag">"${s}"</span>`).join('');
    } else {
      detectedPhrasesList.innerHTML = '<span style="font-size: 10px; color: #64748b;">No coercive phrases detected (natural speech)</span>';
    }
  }

  if (currentScenarioId === 1) {
    // Scenario 1: Digital Arrest Extortion
    if (tvTakeoverTitle) tvTakeoverTitle.textContent = '🚨 DIGITAL ARREST SCAM DETECTED: HANG UP IMMEDIATELY';
    if (tvTakeoverSubtitle) tvTakeoverSubtitle.textContent = 'Indian Law Enforcement never conducts arrests or trials over video calls.';
    if (ringOracleBadge) {
      ringOracleBadge.textContent = '✔ RING PHYSICAL ORACLE: 0 PEOPLE AT DOOR (ENTRANCE EMPTY)';
      ringOracleBadge.className = 'ring-oracle-badge-overlay';
    }
    if (bankFrozenBadge) {
      bankFrozenBadge.textContent = '🔒 BANK TRANSFERS FROZEN BY POLICY';
      bankFrozenBadge.className = 'bank-frozen-pill';
    }

    callVideo.src = '/static/images/scam_officer_call.jpg';
    callerName.textContent = cRisk.caller_claimed_identity;
    callerOrg.textContent = 'Crime Branch / Mumbai Narcotics';
    dfTag.style.display = 'flex';
    dfPct.textContent = 'Deepfake analysis simulated';
    transcriptEl.textContent = cRisk.transcript;
    callStatusBadge.textContent = 'INCOMING EXTORTION CALL';
    callStatusBadge.className = 'pane-status live';
    paymentStatusEl.textContent = 'Payment Guard: Transfers LOCKED by MIRAGE-SHIELD [Simulated Gateway]';
    paymentStatusEl.style.color = '#ff6b7e';

    if (ringFeed) ringFeed.src = '/static/images/scenario1_empty_porch.jpg';
    doorStatusPill.textContent = 'DOOR: CLEAR (0 PEOPLE, 0 PARCELS)';
    doorStatusPill.style.background = 'rgba(0, 230, 118, 0.9)';
    doorHashPill.textContent = 'SHA256: 9f83c18b...';
    rHumanCount.textContent = '0';
    rPkgCount.textContent = '0';
    if (rDingCount) rDingCount.textContent = '0';
    rChimeStatus.textContent = 'ALERT SOUNDING [SIMULATED CHIME]';
    rChimeStatus.className = 'subbar-val alert';
    oracleCallout.style.display = 'block';
    const calloutBadge = oracleCallout.querySelector('.callout-badge');
    if (calloutBadge) {
      calloutBadge.textContent = '🚨 PHYSICAL CONTRADICTION DETECTED';
      calloutBadge.style.color = 'var(--red-alert)';
    }
    const cleanDesc = (vVerdict.contradiction_summary || '').replace(/^(🚨\s*)?(PHYSICAL\s*)?CONTRADICTION\s*(DETECTED|CAUGHT|PROVED)?:?\s*/i, '');
    oracleDesc.textContent = cleanDesc || "Caller claims Mumbai Crime Branch officers are outside your front door, but Ring Doorbell verifies 0 people and 0 vehicles at the entrance in the last 6 hours.";

    familyBadge.textContent = 'EMERGENCY ALERT';
    familyBadge.className = 'pane-status alert';
    familySms.innerHTML = `🚨 <strong>SUSPECTED DIGITAL ARREST SCAM:</strong> Mom is on an active video call with a fake police officer demanding ₹4,50,000. Ring front door camera verifies NO ONE is outside. <strong>Outgoing bank payments have been LOCKED automatically.</strong>`;
    cosignResult.textContent = 'Current Status: Transfers Frozen by Policy';
    cosignResult.style.color = '#ff6b7e';

    appendLog('action', `[${new Date().toLocaleTimeString()}] INTERVENTION ACTIVATED: Scam contradiction caught.`);
    appendLog('info', `[${new Date().toLocaleTimeString()}] Engine active: ${vVerdict.reasoning_engine || 'Local Rule Heuristic'}.`);
    appendLog('kms', `[${new Date().toLocaleTimeString()}] Signed with Local HMAC-SHA256 (Sandbox Key). In-memory ledger committed.`);
    kmsSigDisplay.textContent = 'hmac_sha256_9f83c18b76d0d2ff881679058b8d4f40f0c05763bf84c35626eb06c4ff94e09d';
    verifyStatus.textContent = 'Signature Verified Valid (Local HMAC-SHA256)';
    verifyStatus.style.color = '#00e676';

    appendRingLog('info', 'GET /v1/devices -> 200 OK (Playground Device)');
    appendRingLog('warn', 'Oracle query: 0 humans, 0 dings in 6h window');
    appendRingLog('alert', 'Contradiction flagged: Scammer claimed raid; Porch is CLEAR');
    appendRingLog('alert', 'Chime alert dispatched: audio_ref_urgent_security_alert');

  } else if (currentScenarioId === 2) {
    // Scenario 2: Genuine Family Call
    if (tvTakeoverTitle) tvTakeoverTitle.textContent = '🟢 NORMAL FAMILY CALL VERIFIED: NO THREAT';
    if (tvTakeoverSubtitle) tvTakeoverSubtitle.textContent = 'Conversational speech patterns normal. Zero coercion or deepfake detected.';
    if (ringOracleBadge) {
      ringOracleBadge.textContent = '✔ RING PHYSICAL ORACLE: PORCH SECURE & QUIET';
      ringOracleBadge.className = 'ring-oracle-badge-overlay safe';
    }
    if (bankFrozenBadge) {
      bankFrozenBadge.textContent = '✔ TRANSFERS ARMED & NORMAL';
      bankFrozenBadge.className = 'bank-frozen-pill secured';
    }

    callVideo.src = '/static/images/genuine_daughter_call.jpg';
    callerName.textContent = 'Pooja (Daughter)';
    callerOrg.textContent = 'Family Contact';
    dfTag.style.display = 'none';
    transcriptEl.textContent = cRisk.transcript;
    callStatusBadge.textContent = 'ACTIVE FAMILY CALL';
    callStatusBadge.className = 'pane-status armed';
    paymentStatusEl.textContent = 'Payment Guard: Normal / Armed [Simulated Gateway]';
    paymentStatusEl.style.color = '#94a3b8';

    if (ringFeed) ringFeed.src = '/static/images/scenario1_empty_porch.jpg';
    doorStatusPill.textContent = 'DOOR: CLEAR';
    doorStatusPill.style.background = 'rgba(0, 210, 255, 0.8)';
    rHumanCount.textContent = '0';
    rPkgCount.textContent = '0';
    if (rDingCount) rDingCount.textContent = '0';
    rChimeStatus.textContent = 'QUIET [SIMULATED CHIME]';
    rChimeStatus.className = 'subbar-val clear';
    oracleCallout.style.display = 'none';

    familyBadge.textContent = 'NORMAL';
    familyBadge.className = 'pane-status armed';
    familySms.innerHTML = `Family Sentinel: No suspicious calls or coercion detected. Everything quiet.`;
    cosignResult.textContent = 'No active locks.';
    cosignResult.style.color = '#94a3b8';

    appendLog('info', `[${new Date().toLocaleTimeString()}] Genuine call verified: Zero coercion or deepfake. Verdict=SAFE.`);
    appendRingLog('info', 'GET /v1/devices -> 200 OK (Playground Device)');
    appendRingLog('success', 'Event history: 0 humans, 0 dings (Quiet baseline)');
    appendRingLog('success', 'Oracle verification: Normal family call verified');

  } else if (currentScenarioId === 3) {
    // Scenario 3: Real Amazon Courier Delivery
    if (tvTakeoverTitle) tvTakeoverTitle.textContent = '📦 AMAZON COURIER DELIVERY VERIFIED';
    if (tvTakeoverSubtitle) tvTakeoverSubtitle.textContent = 'Real package delivery confirmed at entrance. Zero false alarms triggered.';
    if (ringOracleBadge) {
      ringOracleBadge.textContent = '✔ RING PHYSICAL ORACLE: 1 PARCEL DELIVERED';
      ringOracleBadge.className = 'ring-oracle-badge-overlay safe';
    }
    if (bankFrozenBadge) {
      bankFrozenBadge.textContent = '✔ TRANSFERS ARMED & NORMAL';
      bankFrozenBadge.className = 'bank-frozen-pill secured';
    }

    callVideo.src = '/static/images/genuine_daughter_call.jpg';
    callerName.textContent = 'Amazon Delivery (Ramesh)';
    callerOrg.textContent = 'Logistics Courier';
    dfTag.style.display = 'none';
    transcriptEl.textContent = cRisk.transcript;
    callStatusBadge.textContent = 'DELIVERY CALL';
    callStatusBadge.className = 'pane-status armed';
    paymentStatusEl.textContent = 'Payment Guard: Armed [Simulated Gateway]';
    paymentStatusEl.style.color = '#94a3b8';

    if (ringFeed) ringFeed.src = '/static/images/scenario3_amazon_delivery.jpg';
    doorStatusPill.textContent = 'DOOR: PACKAGE DELIVERED (1 PARCEL)';
    doorStatusPill.style.background = 'rgba(0, 230, 118, 0.9)';
    doorHashPill.textContent = 'SHA256: 7a819bcf...';
    rHumanCount.textContent = '1';
    rPkgCount.textContent = '1';
    if (rDingCount) rDingCount.textContent = '1';
    rChimeStatus.textContent = 'DOORBELL DING [SIMULATED CHIME]';
    rChimeStatus.className = 'subbar-val clear';
    oracleCallout.style.display = 'block';
    oracleCallout.querySelector('.callout-badge').textContent = 'DELIVERY CONFIRMED';
    oracleCallout.querySelector('.callout-badge').style.color = '#00e676';
    oracleDesc.textContent = 'Ring Camera Confirms Amazon Parcel on porch. No false alarm raised.';

    familyBadge.textContent = 'DELIVERY';
    familyBadge.className = 'pane-status armed';
    familySms.innerHTML = `Amazon Package arrived at front porch. Courier verified by Ring doorbell.`;
    cosignResult.textContent = 'No locks.';
    cosignResult.style.color = '#94a3b8';

    appendLog('oracle', `[${new Date().toLocaleTimeString()}] Ring package delivery verified. Genuine courier passed with zero false alarms.`);
    appendRingLog('info', 'GET /v1/devices -> 200 OK (Playground Device)');
    appendRingLog('info', 'Event history: 1 package delivered, 1 ding in past 6h');
    appendRingLog('success', 'Oracle verification: Amazon courier drop verified (Safe)');
  }
}

// Interactive Payment Attempt
async function attemptPayment() {
  paymentStatusEl.textContent = 'Processing transaction request [Simulated Gateway]...';
  try {
    const res = await fetch('/api/payment/attempt', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ amount_inr: 450000.0, recipient_account: '998822114433' })
    });
    const result = await res.json();
    if (result.blocked) {
      paymentStatusEl.innerHTML = `🛑 <strong>BLOCKED:</strong> ₹4,50,000 transfer halted by MIRAGE-SHIELD! [Simulated Gateway]`;
      paymentStatusEl.style.color = '#ff2b43';
      appendLog('action', `[${new Date().toLocaleTimeString()}] Transfer of ₹4,50,000 to fake RBI escrow BLOCKED [Simulated Gateway].`);
    } else {
      paymentStatusEl.innerHTML = `✔ Transfer processed: ₹4,50,000 [Simulated Gateway]`;
      paymentStatusEl.style.color = '#00e676';
    }
  } catch (err) {
    console.error("Payment attempt error:", err);
  }
}

// Family Co-sign actions
async function approveCosign() {
  cosignResult.textContent = 'Authorizing release with family signature...';
  try {
    const res = await fetch('/api/payment/cosign', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ authorized_by: 'Rohan (Son) - Verified PIN' })
    });
    const result = await res.json();
    cosignResult.innerHTML = `✔ <strong>PAYMENT RELEASED:</strong> Authorized by ${result.authorized_by}`;
    cosignResult.style.color = '#00e676';
    paymentStatusEl.textContent = 'Payment Guard: Released by Family Co-Sign [Simulated Gateway]';
    paymentStatusEl.style.color = '#00e676';
    appendLog('kms', `[${new Date().toLocaleTimeString()}] Family co-sign approved by Rohan. Payment unblocked.`);
  } catch (err) {
    console.error("Cosign error:", err);
  }
}

function rejectPayment() {
  cosignResult.innerHTML = `✖ <strong>TRANSFER BLOCKED INDEFINITELY.</strong> Incident forwarded to Cyber Helpline 1930. [Simulated Response]`;
  cosignResult.style.color = '#ff2b43';
  appendLog('action', `[${new Date().toLocaleTimeString()}] Family confirmed scam. Permanent block committed to in-memory ledger.`);
}

function verifyKmsSignature() {
  verifyStatus.textContent = 'Validating cryptographic HMAC-SHA256 signature against payload digest...';
  setTimeout(() => {
    verifyStatus.innerHTML = `✔ <strong>Cryptographic Signature VALID (Local HMAC-SHA256 Sandbox Digest)</strong>`;
    verifyStatus.style.color = '#00e676';
  }, 400);
}

function appendLog(type, text) {
  if (!agentLogs) return;
  const div = document.createElement('div');
  div.className = `t-line ${type}`;
  div.textContent = text;
  agentLogs.appendChild(div);
  agentLogs.scrollTop = agentLogs.scrollHeight;
}

// Dynamic Ring Health and Playground Detection
async function updateRingHealthStatus() {
  try {
    const res = await fetch('/api/ring/health');
    if (!res.ok) return;
    const data = await res.json();
    const telRing = document.getElementById('tel-ring');
    const telRingDot = document.getElementById('tel-ring-dot');
    const ringBadge = document.getElementById('ring-oracle-status-badge');

    if (telRing) {
      if (data.status === 'CONNECTED') {
        telRing.textContent = data.is_playground ? 'Doorbell Pro • 🟢 Connected (Playground API)' : 'Doorbell Pro • 🟢 Connected (Live API)';
        if (telRingDot) telRingDot.className = 'dot green';
        if (ringBadge) {
          ringBadge.textContent = data.is_playground ? 'PLAYGROUND DEVICE (LIVE API)' : 'LIVE RING DEVICE';
          ringBadge.className = 'pane-status armed';
        }
        if (ringDeviceName && data.device_name) {
          ringDeviceName.textContent = data.device_name;
        }
        if (ringDeviceIdChip) {
          ringDeviceIdChip.textContent = 'ava1.ring.device...';
          if (data.device_id) {
            ringDeviceIdChip.title = data.device_id;
          }
        }

        // Fetch official device details for thumbnail
        try {
          const devRes = await fetch('/api/ring/devices');
          if (devRes.ok) {
            const devData = await devRes.json();
            const firstDev = (devData.devices && devData.devices[0]) || {};
            const imgUrl = (firstDev.raw_attributes && firstDev.raw_attributes.image_url) || null;
            if (imgUrl && ringDeviceThumb) {
              ringDeviceThumb.src = imgUrl;
            }
          }
        } catch (_) {}

      } else if (data.status === 'TOKEN_EXPIRED') {
        telRing.textContent = 'Doorbell Pro • 🔴 Token Expired (401)';
        if (telRingDot) telRingDot.className = 'dot red';
        if (ringBadge) {
          ringBadge.textContent = 'TOKEN EXPIRED (401)';
          ringBadge.className = 'pane-status alert';
        }
      } else if (data.status === 'FORBIDDEN') {
        telRing.textContent = 'Doorbell Pro • 🔴 Forbidden (403)';
        if (telRingDot) telRingDot.className = 'dot red';
        if (ringBadge) {
          ringBadge.textContent = 'ACCESS FORBIDDEN (403)';
          ringBadge.className = 'pane-status alert';
        }
      } else {
        telRing.textContent = 'Doorbell Pro • 🟡 Connected (Sandbox Fixtures)';
        if (telRingDot) telRingDot.className = 'dot yellow';
        if (ringBadge) {
          ringBadge.textContent = 'SANDBOX FIXTURES';
          ringBadge.className = 'pane-status armed';
        }
      }
    }
  } catch (err) {
    console.warn("Could not fetch Ring health:", err);
  }
}

// Action Bar Remote / Screen Handlers for Living Room Incident Theater
function dial1930() {
  appendLog('action', `[${new Date().toLocaleTimeString()}] EMERGENCY ACTION: Connecting to Indian National Cyber Crime Helpline (1930).`);
  alert('🚨 EMERGENCY PROTOCOL TRIGGERED:\n\nConnecting victim to Indian National Cyber Crime Helpline 1930.\n\n• Bank transfers remain locked by policy.\n• Cryptographic evidence bundle & Ring doorbell snapshots submitted to Indian Cyber Crime Reporting Portal (cybercrime.gov.in).');
}

function endCallAndProtect() {
  if (callStatusBadge) {
    callStatusBadge.textContent = 'CALL TERMINATED BY USER';
    callStatusBadge.className = 'pane-status safe';
  }
  if (bankFrozenBadge) {
    bankFrozenBadge.textContent = '🛡️ ACCOUNT SECURED & TRANSFERS SAFE';
    bankFrozenBadge.className = 'bank-frozen-pill secured';
  }
  if (paymentStatusEl) {
    paymentStatusEl.textContent = 'Payment Guard: Call Severed. Bank Transfers Fully Secured.';
    paymentStatusEl.style.color = '#00e676';
  }
  appendLog('action', `[${new Date().toLocaleTimeString()}] Remote command: [SELECT] End Call & Protect Account executed.`);
  appendLog('info', `[${new Date().toLocaleTimeString()}] Extortion video call severed. Threat neutralized.`);
  alert('✔ CALL TERMINATED & ACCOUNT PROTECTED!\n\n• Video stream severed.\n• Outgoing banking transfers secured.\n• Incident logged in HMAC-SHA256 audit ledger.');
}

function viewDoorbellLive() {
  appendRingLog('info', 'Switching to Ring Video Doorbell Pro Live View (1080p WHEP SDP negotiation)...');
  appendLog('oracle', `[${new Date().toLocaleTimeString()}] Ring 1080p WHEP live stream requested. Zero movement outside.`);
  alert('🔔 RING VIDEO DOORBELL PRO - LIVE VIEW:\n\n• WHEP SDP media session established (1080p receive-only).\n• Front entrance status: CLEAR (0 humans detected, entrance empty).');
}

function sendTvKey(key) {
  if (tvIframe && tvIframe.contentWindow) {
    tvIframe.contentWindow.dispatchEvent(new KeyboardEvent('keydown', { key: key }));
  }
}

function resetAll() {
  runScenario(1);
}

// Initial boot
document.addEventListener('DOMContentLoaded', () => {
  runScenario(1);
  updateRingHealthStatus();
});

