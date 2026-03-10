/* ═══════════════════════════════════════════════════════════════
   THE WAR THEATER — Main Application Controller
   ═══════════════════════════════════════════════════════════════ */

(async function () {
  'use strict';

  // Panel navigation
  function initNavigation() {
    const buttons = document.querySelectorAll('.panel-nav button');
    const panels = document.querySelectorAll('.panel');

    buttons.forEach(btn => {
      btn.addEventListener('click', () => {
        const target = btn.dataset.panel;

        // Update tabs
        buttons.forEach(b => {
          b.classList.remove('active');
          b.setAttribute('aria-selected', 'false');
        });
        btn.classList.add('active');
        btn.setAttribute('aria-selected', 'true');

        // Update panels
        panels.forEach(p => p.classList.remove('active'));
        const panel = document.getElementById('panel-' + target);
        if (panel) {
          panel.classList.add('active');

          // Toggle footer visibility — hide on full-viewport map panel
          if (target === 'theater') {
            document.body.classList.add('theater-active');
          } else {
            document.body.classList.remove('theater-active');
          }

          // Trigger chart resize on panel switch
          if (target === 'cost' && WarTheater.Financial.charts) {
            Object.values(WarTheater.Financial.charts).forEach(c => c && c.resize());
          }
          if (target === 'toll' && WarTheater.Humanitarian.charts) {
            Object.values(WarTheater.Humanitarian.charts).forEach(c => c && c.resize());
            WarTheater.Humanitarian.animateCounters();
          }

          // Invalidate map size if switching to theater
          if (target === 'theater' && WarTheater.Map.map) {
            setTimeout(() => WarTheater.Map.map.invalidateSize(), 100);
          }
        }
      });
    });
  }

  // Update timestamp
  function updateTimestamp() {
    const el = document.getElementById('last-updated');
    if (el) {
      const now = new Date();
      el.textContent = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false });
    }
  }

  // Cinematic intro — staggered fade reveal
  function initIntro() {
    var intro = document.getElementById('cinematic-intro');
    if (!intro) return;

    if (sessionStorage.getItem('wt-intro-seen')) {
      intro.remove();
      return;
    }

    function dismiss() {
      intro.classList.add('fade-out');
      sessionStorage.setItem('wt-intro-seen', '1');
      setTimeout(function() { intro.remove(); }, 1000);
    }

    document.getElementById('intro-enter').addEventListener('click', dismiss);
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && intro.parentNode) dismiss();
    });
  }

  // ─── BOOT ───────────────────────────────────────────────
  try {
    initIntro();

    // Navigation
    initNavigation();
    updateTimestamp();
    // Theater panel is active on load — hide footer
    document.body.classList.add('theater-active');
    setInterval(updateTimestamp, 60000);

    // Initialize map
    WarTheater.Map.init();

    // Load all data
    const data = await WarTheater.Data.loadAll();

    // Populate map
    await WarTheater.Map.populate(data);

    // Financial charts
    WarTheater.Financial.init(data);

    // Humanitarian
    WarTheater.Humanitarian.init();

    // Calculator
    WarTheater.Calculator.init();

    // Timeline
    await WarTheater.Timeline.init();

    // Briefing
    WarTheater.Briefing.init();

    console.log('[War Theater] Dashboard initialized. Day ' + WarTheater.Utils.getWarDay() + ' of Operation Epic Fury.');
  } catch (e) {
    console.error('[War Theater] Initialization failed:', e);
  }
})();
