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

  // Arc layer toggle integration
  function initArcToggle() {
    const arcCheckbox = document.querySelector('[data-layer="arcs"]');
    if (arcCheckbox) {
      arcCheckbox.addEventListener('change', (e) => {
        WarTheater.Arcs.toggle(e.target.checked);
      });
    }
  }

  // ─── BOOT ───────────────────────────────────────────────
  try {
    // Navigation
    initNavigation();
    updateTimestamp();
    setInterval(updateTimestamp, 60000);

    // Initialize map
    WarTheater.Map.init();

    // Load all data
    const data = await WarTheater.Data.loadAll();

    // Populate map
    await WarTheater.Map.populate(data);

    // Initialize arcs
    WarTheater.Arcs.init(WarTheater.Map.map);
    WarTheater.Arcs.toggle(false); // Off by default
    initArcToggle();

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
