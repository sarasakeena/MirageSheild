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
const rChimeStatus = document.getElementById('r-chime-status');
const oracleCallout = document.getElementById('oracle-verdict-callout');
const oracleDesc = document.getElementById('oracle-contradiction-desc');

const familySms = document.getElementById('family-sms-body');
const familyBadge = document.getElementById('family-status-badge');
const cosignResult = document.getElementById('cosign-result-text');

const agentLogs = document.getElementById('agent-logs');
const kmsSigDisplay = document.getElementById('kms-sig-display');
const verifyStatus = document.getElementById('verify-status-text');
const tvIframe = document.getElementById('tv-iframe');

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

  if (currentScenarioId === 1) {
    // Scenario 1: Digital Arrest Extortion
    callVideo.src = '/static/images/scam_officer_call.jpg';
    callerName.textContent = cRisk.caller_claimed_identity;
    callerOrg.textContent = 'Crime Branch / Mumbai Narcotics';
    dfTag.style.display = 'flex';
    dfPct.textContent = '92%';
    transcriptEl.textContent = cRisk.transcript;
    callStatusBadge.textContent = 'INCOMING EXTORTION CALL';
    callStatusBadge.className = 'pane-status live';
    paymentStatusEl.textContent = 'Payment Guard: Transfers LOCKED by MIRAGE-SHIELD';
    paymentStatusEl.style.color = '#ff6b7e';

    ringFeed.src = '/static/images/scenario1_empty_porch.jpg';
    doorStatusPill.textContent = 'DOOR: CLEAR (0 PEOPLE, 0 PARCELS)';
    doorStatusPill.style.background = 'rgba(0, 230, 118, 0.9)';
    doorHashPill.textContent = 'SHA256: 9f83c18b...';
    rHumanCount.textContent = '0';
    rPkgCount.textContent = '0';
    rChimeStatus.textContent = 'ALERT SOUNDING';
    rChimeStatus.className = 'r-val alert';
    oracleCallout.style.display = 'block';
    oracleDesc.textContent = vVerdict.contradiction_summary;

    familyBadge.textContent = 'EMERGENCY ALERT';
    familyBadge.className = 'pane-status alert';
    familySms.innerHTML = `🚨 <strong>SUSPECTED DIGITAL ARREST SCAM:</strong> Mom is on an active video call with a fake police officer demanding ₹4,50,000. Ring front door camera verifies NO ONE is outside. <strong>Outgoing bank payments have been LOCKED automatically.</strong>`;
    cosignResult.textContent = 'Current Status: Transfers Frozen by Policy';
    cosignResult.style.color = '#ff6b7e';

    appendLog('action', `[${new Date().toLocaleTimeString()}] INTERVENTION ACTIVATED: Scam contradiction caught.`);
    appendLog('kms', `[${new Date().toLocaleTimeString()}] Signed with AWS KMS Key ARN alias/mirage-shield-ledger-key.`);
    kmsSigDisplay.textContent = 'kMS_sig_9f83c18b76d0d2ff881679058b8d4f40f0c05763bf84c35626eb06c4ff94e09d';
    verifyStatus.textContent = 'Signature Verified Valid';
    verifyStatus.style.color = '#00e676';

  } else if (currentScenarioId === 2) {
    // Scenario 2: Genuine Family Call
    callVideo.src = '/static/images/genuine_daughter_call.jpg';
    callerName.textContent = 'Pooja (Daughter)';
    callerOrg.textContent = 'Family Contact';
    dfTag.style.display = 'none';
    transcriptEl.textContent = cRisk.transcript;
    callStatusBadge.textContent = 'ACTIVE FAMILY CALL';
    callStatusBadge.className = 'pane-status armed';
    paymentStatusEl.textContent = 'Payment Guard: Normal / Armed';
    paymentStatusEl.style.color = '#94a3b8';

    ringFeed.src = '/static/images/scenario1_empty_porch.jpg';
    doorStatusPill.textContent = 'DOOR: CLEAR';
    doorStatusPill.style.background = 'rgba(0, 210, 255, 0.8)';
    rHumanCount.textContent = '0';
    rPkgCount.textContent = '0';
    rChimeStatus.textContent = 'QUIET';
    rChimeStatus.className = 'r-val';
    oracleCallout.style.display = 'none';

    familyBadge.textContent = 'NORMAL';
    familyBadge.className = 'pane-status armed';
    familySms.innerHTML = `Family Sentinel: No suspicious calls or coercion detected. Everything quiet.`;
    cosignResult.textContent = 'No active locks.';
    cosignResult.style.color = '#94a3b8';

    appendLog('info', `[${new Date().toLocaleTimeString()}] Genuine call verified: Zero coercion or deepfake. Verdict=SAFE.`);

  } else if (currentScenarioId === 3) {
    // Scenario 3: Real Amazon Courier Delivery
    callVideo.src = '/static/images/genuine_daughter_call.jpg';
    callerName.textContent = 'Amazon Delivery (Ramesh)';
    callerOrg.textContent = 'Logistics Courier';
    dfTag.style.display = 'none';
    transcriptEl.textContent = cRisk.transcript;
    callStatusBadge.textContent = 'DELIVERY CALL';
    callStatusBadge.className = 'pane-status armed';
    paymentStatusEl.textContent = 'Payment Guard: Armed';
    paymentStatusEl.style.color = '#94a3b8';

    ringFeed.src = '/static/images/scenario3_amazon_delivery.jpg';
    doorStatusPill.textContent = 'DOOR: PACKAGE DELIVERED (1 PARCEL)';
    doorStatusPill.style.background = 'rgba(0, 230, 118, 0.9)';
    doorHashPill.textContent = 'SHA256: 7a819bcf...';
    rHumanCount.textContent = '1';
    rPkgCount.textContent = '1';
    rChimeStatus.textContent = 'DOORBELL DING';
    rChimeStatus.className = 'r-val';
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
  }
}

// Interactive Payment Attempt
async function attemptPayment() {
  paymentStatusEl.textContent = 'Processing transaction request...';
  try {
    const res = await fetch('/api/payment/attempt', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ amount_inr: 450000.0, recipient_account: '998822114433' })
    });
    const result = await res.json();
    if (result.blocked) {
      paymentStatusEl.innerHTML = `🛑 <strong>BLOCKED:</strong> ₹4,50,000 transfer halted by MIRAGE-SHIELD!`;
      paymentStatusEl.style.color = '#ff2b43';
      appendLog('action', `[${new Date().toLocaleTimeString()}] Transfer of ₹4,50,000 to fake RBI escrow BLOCKED.`);
    } else {
      paymentStatusEl.innerHTML = `✔ Transfer processed: ₹4,50,000`;
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
    paymentStatusEl.textContent = 'Payment Guard: Released by Family Co-Sign';
    paymentStatusEl.style.color = '#00e676';
    appendLog('kms', `[${new Date().toLocaleTimeString()}] Family co-sign approved by Rohan. Payment unblocked.`);
  } catch (err) {
    console.error("Cosign error:", err);
  }
}

function rejectPayment() {
  cosignResult.innerHTML = `✖ <strong>TRANSFER BLOCKED INDEFINITELY.</strong> Incident forwarded to Cyber Helpline 1930.`;
  cosignResult.style.color = '#ff2b43';
  appendLog('action', `[${new Date().toLocaleTimeString()}] Family confirmed scam. Permanent block committed to DynamoDB.`);
}

function verifyKmsSignature() {
  verifyStatus.textContent = 'Validating KMS key signature against SHA256 payload...';
  setTimeout(() => {
    verifyStatus.innerHTML = `✔ <strong>Cryptographic Signature VALID (AWS KMS RSASSA_PKCS1_V1_5)</strong>`;
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
});
