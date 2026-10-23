// MIRAGE-SHIELD Fire TV Remote & Takeover Controller
// Supports D-Pad Arrow navigation, Enter key, and real-time backend synchronization

document.addEventListener('DOMContentLoaded', () => {
  const ambientScreen = document.getElementById('tv-ambient-screen');
  const takeoverScreen = document.getElementById('tv-intervention-screen');
  const clockEl = document.getElementById('tv-clock');
  const timestampEl = document.getElementById('takeover-timestamp');

  // Evidence elements
  const snapshotImg = document.getElementById('tv-snapshot-img');
  const contradictionText = document.getElementById('tv-contradiction-text');
  const humanCount = document.getElementById('tv-human-count');
  const pkgCount = document.getElementById('tv-pkg-count');
  const dingCount = document.getElementById('tv-ding-count');

  // AI signals
  const dfBar = document.getElementById('tv-df-bar');
  const dfVal = document.getElementById('tv-df-val');
  const coercionBar = document.getElementById('tv-coercion-bar');
  const coercionVal = document.getElementById('tv-coercion-val');

  // Buttons
  const buttons = [
    document.getElementById('btn-hangup'),
    document.getElementById('btn-doorbell'),
    document.getElementById('btn-helpline')
  ];
  let currentFocusIndex = 0;

  // Clock ticker
  function updateClock() {
    const now = new Date();
    const timeStr = now.toLocaleTimeString('en-IN', { timeZone: 'Asia/Kolkata', hour: '2-digit', minute: '2-digit' });
    if (clockEl) clockEl.textContent = timeStr;
    if (timestampEl) {
      const dateStr = now.toLocaleDateString('en-IN', { timeZone: 'Asia/Kolkata', month: 'short', day: 'numeric', year: 'numeric' }).toUpperCase();
      const secStr = now.toLocaleTimeString('en-IN', { timeZone: 'Asia/Kolkata', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false });
      timestampEl.textContent = `${dateStr} · ${secStr} IST`;
    }
  }
  setInterval(updateClock, 1000);
  updateClock();

  // D-Pad Remote Navigation
  function setFocus(index) {
    if (index < 0) index = 0;
    if (index >= buttons.length) index = buttons.length - 1;
    currentFocusIndex = index;
    buttons.forEach((btn, idx) => {
      if (idx === index) {
        btn.classList.add('focused');
        btn.focus();
      } else {
        btn.classList.remove('focused');
      }
    });
  }

  window.addEventListener('keydown', (e) => {
    if (takeoverScreen.classList.contains('hidden')) return;

    if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
      setFocus(currentFocusIndex + 1);
      e.preventDefault();
    } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
      setFocus(currentFocusIndex - 1);
      e.preventDefault();
    } else if (e.key === 'Enter') {
      buttons[currentFocusIndex].click();
      e.preventDefault();
    }
  });

  // Button actions
  buttons[0].addEventListener('click', () => {
    // Hangup / Dismiss
    takeoverScreen.classList.add('hidden');
    ambientScreen.classList.remove('hidden');
  });

  buttons[1].addEventListener('click', () => {
    // Open full doorbell feed modal or view
    alert("Displaying Fullscreen 1080p WHEP Live Stream from Front Porch Ring Doorbell...");
  });

  buttons[2].addEventListener('click', () => {
    // 1930 Helpline action
    alert("Connecting living room speaker to National Cybercrime Helpline: 1930");
  });

  // State sync from backend API
  let lastVerdictId = null;

  async function checkVerdict() {
    try {
      const res = await fetch('/api/verdict/latest');
      if (!res.ok) return;
      const data = await res.json();
      if (!data || !data.action) return;

      if (data.action === 'INTERVENE') {
        ambientScreen.classList.add('hidden');
        takeoverScreen.classList.remove('hidden');

        // Update evidence
        if (data.door_evidence) {
          humanCount.textContent = data.door_evidence.human_events_count || 0;
          pkgCount.textContent = data.door_evidence.package_events_count || 0;
          dingCount.textContent = data.door_evidence.ding_events_count || 0;
          if (data.door_evidence.latest_snapshot_url) {
            snapshotImg.src = data.door_evidence.latest_snapshot_url;
          }
        }

        if (data.contradiction_summary) {
          const cleanSummary = data.contradiction_summary.replace(/^(🚨\s*)?(PHYSICAL\s*)?CONTRADICTION\s*(DETECTED|CAUGHT|PROVED)?:?\s*/i, '');
          contradictionText.innerHTML = cleanSummary;
        }

        if (data.call_risk) {
          const dfPct = Math.round((data.call_risk.deepfake_score || 0) * 100);
          dfBar.style.width = `${dfPct}%`;
          dfVal.textContent = data.call_risk.deepfake_simulated ? "Deepfake analysis simulated" : `${dfPct}% (Model Detected)`;

          const cPct = Math.round((data.call_risk.coercion_score || 0) * 100);
          coercionBar.style.width = `${cPct}%`;
          coercionVal.textContent = `${cPct}% (Extortion & Isolation Script)`;
        }

        setFocus(0);
      } else {
        // Safe or Warn
        takeoverScreen.classList.add('hidden');
        ambientScreen.classList.remove('hidden');
      }
    } catch (err) {
      console.warn("Polling verdict error:", err);
    }
  }

  setInterval(checkVerdict, 1500);
  checkVerdict();
});
