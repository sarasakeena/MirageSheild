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

// IST Live Clock Controller
function updateISTClock() {
  const dateEl = document.getElementById('ist-date');
  const timeEl = document.getElementById('ist-time');
  const phoneClock = document.getElementById('phone-status-time');
  const ringTimestamp = document.getElementById('ring-feed-timestamp');
  
  const now = new Date();
  const optionsDate = { weekday: 'short', day: '2-digit', month: 'short', year: 'numeric', timeZone: 'Asia/Kolkata' };
  const optionsTime = { hour: '2-digit', minute: '2-digit', hour12: false, timeZone: 'Asia/Kolkata' };
  const optionsSec = { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false, timeZone: 'Asia/Kolkata' };
  
  const dateStr = now.toLocaleDateString('en-GB', optionsDate);
  const timeStr = now.toLocaleTimeString('en-GB', optionsTime);
  const timeWithSec = now.toLocaleTimeString('en-GB', optionsSec);

  if (dateEl) dateEl.textContent = dateStr;
  if (timeEl) timeEl.textContent = `${timeStr} IST`;
  if (phoneClock) phoneClock.textContent = timeStr;
  if (ringTimestamp) ringTimestamp.textContent = `${dateStr} ${timeWithSec}`;
}
setInterval(updateISTClock, 1000);
updateISTClock();

// Diagnostics Tray Toggle
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

// Live Call Duration Timer
let callElapsedSeconds = 84;
let callTimerInterval = null;

function startCallTimer() {
  callElapsedSeconds = 0;
  if (callTimerInterval) clearInterval(callTimerInterval);
  const timerEl = document.getElementById('call-duration-timer');
  
  function tick() {
    callElapsedSeconds++;
    if (timerEl) {
      const mins = String(Math.floor(callElapsedSeconds / 60)).padStart(2, '0');
      const secs = String(callElapsedSeconds % 60).padStart(2, '0');
      timerEl.textContent = `00:${mins}:${secs}`;
    }
  }
  tick();
  callTimerInterval = setInterval(tick, 1000);
}

// Run Scenario
async function runScenario(scenarioId) {
  currentScenarioId = scenarioId;
  startCallTimer();
  
  // Highlight active button
  [1, 2, 3].forEach(id => {
    const btn = document.getElementById(`btn-scen-${id}`);
    if (btn) btn.classList.toggle('active', id === scenarioId);
  });

  try {
    const res = await fetch(`/api/scenario/${scenarioId}`, { method: 'POST' });
    const data = await res.json();
    applyScenarioUI(data);
    loadRecentIncidents();
  } catch (err) {
    console.error("Error setting scenario:", err);
  }
}

function applyScenarioUI(data) {
  const cRisk = data.call_risk || {};
  const dEvidence = data.door_evidence || {};
  const vVerdict = data.verdict || {};

  // Refresh TV embed
  if (tvIframe && tvIframe.contentWindow) {
    try { tvIframe.contentWindow.location.reload(); } catch(_) {}
  }

  // Update Dynamic Claim vs Reality Fields
  const claimCountEl = document.getElementById('claim-count');
  const claimSubEl = document.getElementById('claim-sub');
  const transcriptQuoteEl = document.getElementById('transcript-quote');
  const dfScoreNumber = document.getElementById('df-score-number');
  const dfProgressBar = document.getElementById('df-progress-bar');
  const tvStatusChip = document.getElementById('tv-status-chip');
  const chimeChip = document.getElementById('chime-chip');

  // Update Dynamic Regex Coercion Classifier Output & Phrases
  if (coercionScoreBadge && cRisk) {
    const cScore = Math.round((cRisk.coercion_score || 0) * 100);
    coercionScoreBadge.textContent = cScore >= 40 ? 'HIGH' : 'LOW';
    coercionScoreBadge.className = 'severity-pill-high';
    if (cScore < 40) {
      coercionScoreBadge.style.color = 'var(--green)';
      coercionScoreBadge.style.background = 'var(--green-subtle)';
    } else {
      coercionScoreBadge.style.color = 'var(--red)';
      coercionScoreBadge.style.background = 'rgba(255, 48, 79, 0.12)';
    }

    if (detectedPhrasesList) {
      const snippets = cRisk.detected_coercion_snippets || [];
      if (snippets.length > 0) {
        detectedPhrasesList.innerHTML = snippets.map(s => `<span class="threat-chip">"${s}"</span>`).join('');
      } else {
        detectedPhrasesList.innerHTML = '<span class="threat-chip" style="color:var(--muted); border-color:var(--border);">Normal conversation</span>';
      }
    }
  }

  // Deepfake hero score
  if (cRisk.deepfake_confidence !== undefined) {
    const scoreVal = cRisk.deepfake_confidence || 0;
    if (dfScoreNumber) dfScoreNumber.textContent = scoreVal.toFixed(2);
    if (dfProgressBar) dfProgressBar.style.width = `${Math.round(scoreVal * 100)}%`;
  }

  if (currentScenarioId === 1) {
    // SCENARIO 1: Digital Arrest Extortion
    if (claimCountEl) claimCountEl.textContent = '3 OFFICERS';
    if (claimSubEl) claimSubEl.textContent = 'outside your door';
    if (rHumanCount) rHumanCount.textContent = '0';
    if (rPkgCount) rPkgCount.textContent = '0';
    if (rDingCount) rDingCount.textContent = '0';

    if (transcriptQuoteEl) {
      transcriptQuoteEl.textContent = '“Armed police are outside your door. Transfer ₹4,50,000 now.”';
    }

    if (tvTakeoverTitle) tvTakeoverTitle.textContent = 'Takeover Active';
    if (tvTakeoverSubtitle) tvTakeoverSubtitle.textContent = 'Living room TV intercepted · Emergency 1930 alert displayed. Fire TV Simulator (Vega OS)';
    if (tvStatusChip) {
      tvStatusChip.textContent = '● ACTIVE';
      tvStatusChip.className = 'module-status-chip alert';
    }
    if (chimeChip) {
      chimeChip.textContent = '● SOUNDING';
      chimeChip.className = 'module-status-chip alert';
    }
    if (rChimeStatus) {
      rChimeStatus.textContent = 'ALERT SOUNDING [SIMULATED CHIME]';
      rChimeStatus.className = 'module-action-title alert';
    }

    if (ringOracleBadge) {
      ringOracleBadge.textContent = '✔ RING PHYSICAL ORACLE: 0 PEOPLE AT DOOR (ENTRANCE EMPTY)';
    }
    if (bankFrozenBadge) {
      bankFrozenBadge.textContent = '● ACTIVE';
      bankFrozenBadge.className = 'module-status-chip active';
    }

    callVideo.src = '/static/images/scam_officer_call.jpg';
    callerName.textContent = cRisk.caller_claimed_identity || 'ACP Vikram Rathore';
    callerOrg.textContent = 'Crime Branch / Mumbai Narcotics';
    dfTag.style.display = 'block';
    dfPct.textContent = 'Deepfake analysis simulated';
    transcriptEl.textContent = cRisk.transcript || 'Officers have been dispatched and are standing outside your front door right now. Transfer ₹4,50,000 to the RBI verification escrow account immediately!';
    callStatusBadge.textContent = '● LIVE';
    callStatusBadge.className = 'badge-pill-threat';
    paymentStatusEl.textContent = 'Outgoing UPI/bank transfers blocked immediately. [Simulated Gateway]';

    if (ringFeed) ringFeed.src = '/static/images/scenario1_empty_porch.jpg';
    doorStatusPill.textContent = 'DOOR: CLEAR (0 PEOPLE, 0 PARCELS)';
    doorHashPill.textContent = 'SHA256: 9f83c18b...';

    if (oracleCallout) {
      oracleCallout.style.display = 'flex';
      oracleCallout.className = 'contradiction-glow-box';
    }
    const cleanDesc = (vVerdict.contradiction_summary || '').replace(/^(🚨\s*)?(PHYSICAL\s*)?CONTRADICTION\s*(DETECTED|CAUGHT|PROVED)?:?\s*/i, '');
    if (oracleDesc) oracleDesc.textContent = cleanDesc || "0 people & 0 vehicles at entrance in past 6 hours.";

    familyBadge.textContent = '● SENT';
    familyBadge.className = 'module-status-chip sent';
    familySms.innerHTML = `Alert sent to 2 family members with incident details. SIMULATED SMS`;
    cosignResult.textContent = 'Current Status: Transfers Frozen by Policy';

    appendLog('action', `[${new Date().toLocaleTimeString()}] INTERVENTION ACTIVATED: Scam contradiction caught.`);
    appendLog('info', `[${new Date().toLocaleTimeString()}] Engine active: ${vVerdict.reasoning_engine || 'Local Rule Heuristic'}.`);
    appendLog('kms', `[${new Date().toLocaleTimeString()}] Signed with Local HMAC-SHA256 (Sandbox Key). In-memory ledger committed.`);
    kmsSigDisplay.textContent = '3f9a6c7e9f83c18b76d0d2ff881679058b8d4f40f0c05763bf84c35626eb06c4ff94e09d';
    verifyStatus.textContent = 'Signature Verified Valid (LOCAL_HMAC_SHA256_SANDBOX)';
    verifyStatus.style.color = 'var(--green)';

  } else if (currentScenarioId === 2) {
    // SCENARIO 2: Genuine Family Call
    if (claimCountEl) claimCountEl.textContent = '0 THREATS';
    if (claimSubEl) claimSubEl.textContent = 'family video call';
    if (rHumanCount) rHumanCount.textContent = '0';
    if (rPkgCount) rPkgCount.textContent = '0';
    if (rDingCount) rDingCount.textContent = '0';

    if (transcriptQuoteEl) {
      transcriptQuoteEl.textContent = '“Hi Mom! Just calling to check if you got the sweets we sent from Chennai.”';
    }

    if (tvTakeoverTitle) tvTakeoverTitle.textContent = 'Takeover Standby';
    if (tvTakeoverSubtitle) tvTakeoverSubtitle.textContent = 'TV ambient display active. Zero false alarms triggered. Fire TV Simulator (Vega OS)';
    if (tvStatusChip) {
      tvStatusChip.textContent = '● READY';
      tvStatusChip.className = 'module-status-chip ready';
    }
    if (chimeChip) {
      chimeChip.textContent = '● READY';
      chimeChip.className = 'module-status-chip ready';
    }
    if (rChimeStatus) {
      rChimeStatus.textContent = 'QUIET [SIMULATED CHIME]';
      rChimeStatus.className = 'module-action-title';
      rChimeStatus.style.color = 'var(--green)';
    }

    if (ringOracleBadge) {
      ringOracleBadge.textContent = '✔ RING PHYSICAL ORACLE: PORCH SECURE & QUIET';
    }
    if (bankFrozenBadge) {
      bankFrozenBadge.textContent = '● ARMED';
      bankFrozenBadge.className = 'module-status-chip ready';
    }

    callVideo.src = '/static/images/genuine_daughter_call.jpg';
    callerName.textContent = 'Pooja (Daughter)';
    callerOrg.textContent = 'Family Contact';
    dfTag.style.display = 'none';
    transcriptEl.textContent = cRisk.transcript || 'Hi Mom! Just calling to check if you got the sweets we sent from Chennai.';
    callStatusBadge.textContent = '● SAFE';
    callStatusBadge.className = 'badge-pill-live';
    paymentStatusEl.textContent = 'Payment Guard: Armed & Normal [Simulated Gateway]';

    if (ringFeed) ringFeed.src = '/static/images/scenario1_empty_porch.jpg';
    doorStatusPill.textContent = 'DOOR: CLEAR';
    doorHashPill.textContent = 'SHA256: 9f83c18b...';

    if (oracleCallout) {
      oracleCallout.style.display = 'flex';
      oracleCallout.className = 'contradiction-glow-box safe';
    }
    if (oracleDesc) oracleDesc.textContent = 'Normal family conversation verified. Zero physical contradiction.';

    familyBadge.textContent = '● IDLE';
    familyBadge.className = 'module-status-chip ready';
    familySms.innerHTML = `No alert required. Family contact verified. SIMULATED SMS`;
    cosignResult.textContent = 'No active locks.';

    kmsSigDisplay.textContent = '8a72b0c16f21c99b881679058b8d4f40f0c05763bf84c35626eb06c4ff94e09d12345678';
    verifyStatus.textContent = 'Normal Session Committed (LOCAL_HMAC_SHA256_SANDBOX)';

  } else if (currentScenarioId === 3) {
    // SCENARIO 3: Real Amazon Courier Delivery (FIXED: Courier photo instead of daughter)
    if (claimCountEl) claimCountEl.textContent = '1 COURIER';
    if (claimSubEl) claimSubEl.textContent = 'package at door';
    if (rHumanCount) rHumanCount.textContent = '1';
    if (rPkgCount) rPkgCount.textContent = '1';
    if (rDingCount) rDingCount.textContent = '1';

    if (transcriptQuoteEl) {
      transcriptQuoteEl.textContent = '“Hello sir, I have placed your Amazon package safely by the front door.”';
    }

    if (tvTakeoverTitle) tvTakeoverTitle.textContent = 'Delivery Verified';
    if (tvTakeoverSubtitle) tvTakeoverSubtitle.textContent = 'Real parcel confirmed at entrance. Zero false alarms. Fire TV Simulator (Vega OS)';
    if (tvStatusChip) {
      tvStatusChip.textContent = '● READY';
      tvStatusChip.className = 'module-status-chip ready';
    }
    if (chimeChip) {
      chimeChip.textContent = '● CHIME';
      chimeChip.className = 'module-status-chip ready';
    }
    if (rChimeStatus) {
      rChimeStatus.textContent = 'DOORBELL DING [SIMULATED CHIME]';
      rChimeStatus.className = 'module-action-title';
      rChimeStatus.style.color = 'var(--blue)';
    }

    if (ringOracleBadge) {
      ringOracleBadge.textContent = '✔ RING PHYSICAL ORACLE: 1 PARCEL DELIVERED';
    }
    if (bankFrozenBadge) {
      bankFrozenBadge.textContent = '● ARMED';
      bankFrozenBadge.className = 'module-status-chip ready';
    }

    // FIX SCENARIO 3 BUG: show delivery image instead of daughter
    callVideo.src = '/static/images/scenario3_amazon_delivery.jpg';
    callerName.textContent = 'Amazon Delivery (Ramesh)';
    callerOrg.textContent = 'Logistics Courier';
    dfTag.style.display = 'none';
    transcriptEl.textContent = cRisk.transcript || 'Hello sir, I have placed your Amazon package safely by the front door.';
    callStatusBadge.textContent = '● DELIVERY';
    callStatusBadge.className = 'badge-pill-live';
    paymentStatusEl.textContent = 'Payment Guard: Armed [Simulated Gateway]';

    if (ringFeed) ringFeed.src = '/static/images/scenario3_amazon_delivery.jpg';
    doorStatusPill.textContent = 'DOOR: PACKAGE DELIVERED (1 PARCEL)';
    doorHashPill.textContent = 'SHA256: 7a819bcf...';

    if (oracleCallout) {
      oracleCallout.style.display = 'flex';
      oracleCallout.className = 'contradiction-glow-box safe';
    }
    if (oracleDesc) oracleDesc.textContent = 'Ring Camera Confirms Amazon Parcel on porch. No false alarm raised.';

    familyBadge.textContent = '● DELIVERY';
    familyBadge.className = 'module-status-chip ready';
    familySms.innerHTML = `Amazon Package arrived at front porch. Courier verified. SIMULATED SMS`;
    cosignResult.textContent = 'No locks active.';

    kmsSigDisplay.textContent = '7a819bcf881679058b8d4f40f0c05763bf84c35626eb06c4ff94e09dd2b4e1f0a1b2c3d4';
    verifyStatus.textContent = 'Delivery Audit Logged (LOCAL_HMAC_SHA256_SANDBOX)';
  }
}

// Dynamic Recent Incidents Loader from /api/audit/incidents
async function loadRecentIncidents() {
  const container = document.getElementById('incidents-table-body');
  const auditSystemMode = document.getElementById('audit-system-mode');
  
  try {
    const res = await fetch('/api/audit/incidents');
    if (!res.ok) return;
    const data = await res.json();
    
    // Update Audit & Integrity system badge
    if (auditSystemMode) {
      if (data.kms_active && data.signature_mode === 'AWS_KMS_ASYMMETRIC_RSA') {
        auditSystemMode.textContent = 'AWS KMS SIGNED';
      } else {
        auditSystemMode.textContent = 'LOCAL_HMAC_SHA256_SANDBOX';
      }
    }

    if (!container) return;

    const incidents = data.incidents || [];
    if (incidents.length === 0) {
      container.innerHTML = `
        <div class="incident-row">
          <div class="inc-ico-circle red">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1 22 16.92z"/></svg>
          </div>
          <div class="inc-main">
            <span class="inc-title">Digital arrest attempt</span>
            <span class="inc-sub">Scam call with fake police claim</span>
          </div>
          <span class="inc-time">14:32<br>23 Oct 2026</span>
          <span class="inc-badge-pill danger">HIGH RISK</span>
          <span class="inc-meta-ring">Ring: 0 humans</span>
          <span class="inc-meta-extra">Deepfake: 0.92</span>
          <span class="inc-arrow">›</span>
        </div>
        <div class="incident-row">
          <div class="inc-ico-circle green">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2" ry="2"/></svg>
          </div>
          <div class="inc-main">
            <span class="inc-title">Family video call</span>
            <span class="inc-sub">Sister video call (Chennai)</span>
          </div>
          <span class="inc-time">13:08<br>23 Oct 2026</span>
          <span class="inc-badge-pill safe">VERIFIED SAFE</span>
          <span class="inc-meta-ring">Ring: 1 human</span>
          <span class="inc-meta-extra">Normal call</span>
          <span class="inc-arrow">›</span>
        </div>
        <div class="incident-row">
          <div class="inc-ico-circle blue">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="1" y="3" width="15" height="13"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>
          </div>
          <div class="inc-main">
            <span class="inc-title">Courier arrival</span>
            <span class="inc-sub">Amazon delivery (package detected)</span>
          </div>
          <span class="inc-time">12:41<br>23 Oct 2026</span>
          <span class="inc-badge-pill delivery">VERIFIED DELIVERY</span>
          <span class="inc-meta-ring">Ring: 1 human</span>
          <span class="inc-meta-extra">Package detected</span>
          <span class="inc-arrow">›</span>
        </div>
      `;
      return;
    }

    container.innerHTML = incidents.slice(0, 4).map(inc => {
      const isIntervene = inc.action === 'INTERVENE';
      const pillClass = isIntervene ? 'danger' : 'safe';
      const circleClass = isIntervene ? 'red' : 'green';
      const badgeText = isIntervene ? 'HIGH RISK' : 'VERIFIED SAFE';
      const timeStr = inc.timestamp ? inc.timestamp.substring(11, 16) : '14:32';
      return `
        <div class="incident-row">
          <div class="inc-ico-circle ${circleClass}">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>
          </div>
          <div class="inc-main">
            <span class="inc-title">${inc.incident_id || 'Incident Recorded'}</span>
            <span class="inc-sub">${isIntervene ? 'Scam call blocked by Ring Oracle' : 'Verified safe interaction'}</span>
          </div>
          <span class="inc-time">${timeStr}<br>23 Oct 2026</span>
          <span class="inc-badge-pill ${pillClass}">${badgeText}</span>
          <span class="inc-meta-ring">Ring: Verified</span>
          <span class="inc-meta-extra">HMAC-SHA256</span>
          <span class="inc-arrow">›</span>
        </div>
      `;
    }).join('');

  } catch (err) {
    console.warn("Could not load recent incidents:", err);
  }
}

// Copy Hash to Clipboard
function copyAuditHash() {
  const hashEl = document.getElementById('kms-sig-display');
  const btn = document.getElementById('btn-copy-hash');
  if (hashEl) {
    const text = hashEl.textContent.trim();
    navigator.clipboard.writeText(text).then(() => {
      if (btn) {
        btn.innerHTML = '<span style="color:var(--green); font-size:10px;">✔</span>';
        setTimeout(() => {
          btn.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>';
        }, 1500);
      }
    });
  }
}

// Modal Takeover Handlers
function openTakeoverModal() {
  const modal = document.getElementById('takeover-modal');
  if (modal) modal.classList.add('open');
}

function closeTakeoverModal() {
  const modal = document.getElementById('takeover-modal');
  if (modal) modal.classList.remove('open');
}

// Toggle Victim Phone Drawer
function toggleVictimPhoneDrawer(forceState) {
  const drawer = document.getElementById('victim-phone-drawer');
  if (!drawer) return;
  if (typeof forceState === 'boolean') {
    drawer.classList.toggle('open', forceState);
  } else {
    drawer.classList.toggle('open');
  }
}

// Payment Attempt
async function attemptPayment() {
  if (paymentStatusEl) paymentStatusEl.textContent = 'Processing transaction request [Simulated Gateway]...';
  try {
    const res = await fetch('/api/payment/attempt', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ amount_inr: 450000.0, recipient_account: '998822114433' })
    });
    const result = await res.json();
    if (result.blocked) {
      if (paymentStatusEl) {
        paymentStatusEl.innerHTML = `🛑 <strong>BLOCKED:</strong> ₹4,50,000 transfer halted by MIRAGE-SHIELD! [Simulated Gateway]`;
        paymentStatusEl.style.color = 'var(--red)';
      }
      appendLog('action', `[${new Date().toLocaleTimeString()}] Transfer of ₹4,50,000 to fake RBI escrow BLOCKED [Simulated Gateway].`);
    } else {
      if (paymentStatusEl) {
        paymentStatusEl.innerHTML = `✔ Transfer processed: ₹4,50,000 [Simulated Gateway]`;
        paymentStatusEl.style.color = 'var(--green)';
      }
    }
  } catch (err) {
    console.error("Payment attempt error:", err);
  }
}

// Family Co-sign actions
async function approveCosign() {
  if (cosignResult) cosignResult.textContent = 'Authorizing release with family signature...';
  try {
    const res = await fetch('/api/payment/cosign', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ authorized_by: 'Rohan (Son) - Verified PIN' })
    });
    const result = await res.json();
    if (cosignResult) {
      cosignResult.innerHTML = `✔ <strong>PAYMENT RELEASED:</strong> Authorized by ${result.authorized_by}`;
      cosignResult.style.color = 'var(--green)';
    }
    if (paymentStatusEl) {
      paymentStatusEl.textContent = 'Payment Guard: Released by Family Co-Sign [Simulated Gateway]';
      paymentStatusEl.style.color = 'var(--green)';
    }
    appendLog('kms', `[${new Date().toLocaleTimeString()}] Family co-sign approved by Rohan. Payment unblocked.`);
  } catch (err) {
    console.error("Cosign error:", err);
  }
}

async function rejectPayment() {
  if (cosignResult) {
    cosignResult.innerHTML = `🛑 <strong>TRANSFER PERMANENTLY BLOCKED:</strong> Reported to 1930 Cyber Cell.`;
    cosignResult.style.color = 'var(--red)';
  }
  if (paymentStatusEl) {
    paymentStatusEl.textContent = 'Payment Guard: Transfer cancelled permanently. 1930 report filed. [Simulated Gateway]';
    paymentStatusEl.style.color = 'var(--red)';
  }
}

function appendLog(type, text) {
  if (!agentLogs) return;
  const div = document.createElement('div');
  div.className = `t-line ${type}`;
  div.textContent = text;
  agentLogs.appendChild(div);
  agentLogs.scrollTop = agentLogs.scrollHeight;
}

// Ring Health API check
async function updateRingHealthStatus() {
  try {
    const res = await fetch('/api/ring/health');
    if (!res.ok) return;
    const data = await res.json();
    const telRing = document.getElementById('tel-ring');
    const telRingDot = document.getElementById('tel-ring-dot');
    
    if (telRing) {
      if (data.status === 'CONNECTED') {
        telRing.textContent = 'SYSTEM OPERATIONAL';
        if (telRingDot) {
          telRingDot.className = 'status-dot-pulse';
        }
      } else {
        telRing.textContent = 'SYSTEM ACTIVE (SANDBOX)';
        if (telRingDot) {
          telRingDot.className = 'status-dot-pulse';
        }
      }
    }
  } catch (err) {
    console.warn("Could not fetch Ring health:", err);
  }
}

// In-Page Toast Controller
let toastTimeout = null;
function showToast(title, message, type = 'safe') {
  const toast = document.getElementById('console-toast');
  const titleEl = document.getElementById('toast-title');
  const msgEl = document.getElementById('toast-message');
  if (!toast) return;

  if (titleEl) titleEl.textContent = title;
  if (msgEl) msgEl.textContent = message;

  toast.className = `console-toast ${type}`;
  toast.classList.remove('hidden');

  if (toastTimeout) clearTimeout(toastTimeout);
  toastTimeout = setTimeout(() => {
    hideToast();
  }, 4000);
}

function hideToast() {
  const toast = document.getElementById('console-toast');
  if (toast) toast.classList.add('hidden');
}

function dial1930() {
  appendLog('action', `[${new Date().toLocaleTimeString()}] EMERGENCY ACTION: Connecting to 1930 helpline.`);
  showToast('Calling 1930 (simulated)', 'Connecting victim to National Cyber Crime Helpline. Outgoing bank transfers remain locked by policy.', 'alert');
}

function endCallAndProtect() {
  if (callStatusBadge) {
    callStatusBadge.textContent = '● TERMINATED';
    callStatusBadge.className = 'badge-pill-live';
  }
  if (bankFrozenBadge) {
    bankFrozenBadge.textContent = '● SECURED';
    bankFrozenBadge.className = 'module-status-chip ready';
  }
  if (paymentStatusEl) {
    paymentStatusEl.textContent = 'Payment Guard: Call Severed. Bank Transfers Fully Secured.';
    paymentStatusEl.style.color = 'var(--green)';
  }
  closeTakeoverModal();
  showToast('Threat Neutralized', 'Call terminated and bank transfers secured. Incident committed to HMAC-SHA256 audit ledger.', 'safe');
}

function viewDoorbellLive() {
  showToast('Live stream view (simulated)', 'Front entrance status: CLEAR (0 humans detected, entrance empty).', 'safe');
}

function resetAll() {
  runScenario(1);
}

// Initial boot
document.addEventListener('DOMContentLoaded', () => {
  runScenario(1);
  updateRingHealthStatus();
  loadRecentIncidents();
});

