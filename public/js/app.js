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

  // ─── POPULATE HERO STATS FROM JSON ───────────────────────
  function populateHeroStats(heroStats) {
    if (!heroStats) return;

    // Timestamp
    var ts = document.getElementById('last-updated');
    if (ts) ts.textContent = heroStats.timestamp_label;

    // Cost panel
    var cost = heroStats.cost;
    if (cost) {
      setHero('brent-price', '$' + cost.brent.price, cost.brent.change, cost.brent.tooltip);
      setHero('wti-price', '$' + cost.wti.price, cost.wti.change, cost.wti.tooltip);
      setHero('gas-price', '$' + cost.gas.price, cost.gas.change, cost.gas.tooltip);
      setHero('sp500-value', WarTheater.Utils.formatNumber(cost.sp500.value), cost.sp500.change, cost.sp500.tooltip);
      // S&P 500: green when at/above pre-war baseline, red when below
      var sp500Baseline = (heroStats.history && heroStats.history[0] && heroStats.history[0].sp500) || 6878.88;
      var sp500Up = cost.sp500.value >= sp500Baseline;
      var sp500ValueEl = document.getElementById('sp500-value');
      if (sp500ValueEl) sp500ValueEl.style.color = sp500Up ? 'var(--financial-down)' : 'var(--financial-up)';
      var sp500ChangeEl = document.getElementById('sp500-change');
      if (sp500ChangeEl) {
        sp500ChangeEl.classList.remove('up', 'down');
        sp500ChangeEl.classList.add(sp500Up ? 'down' : 'up');
      }
      setHero('daily-cost', '~$' + cost.daily_cost.value + cost.daily_cost.unit, null, cost.daily_cost.tooltip);
      var dcNote = document.getElementById('daily-cost-note');
      if (dcNote) dcNote.textContent = cost.daily_cost.note;
      setHero('total-cost', '~$' + cost.total_cost.value + cost.total_cost.unit, null, cost.total_cost.tooltip);
      var tcNote = document.getElementById('total-cost-note');
      if (tcNote) tcNote.textContent = cost.total_cost.note;

      // Update labels
      setLabel('brent-price', cost.brent.label);
      setLabel('wti-price', cost.wti.label);
      setLabel('gas-price', cost.gas.label);
      setLabel('sp500-value', cost.sp500.label);
      setLabel('daily-cost', cost.daily_cost.label);
      setLabel('total-cost', cost.total_cost.label + ' (' + heroStats.war_day + ' Days)');
    }

    // Toll panel — set counter targets and notes
    var toll = heroStats.toll;
    if (toll) {
      var tollKeys = ['targets_struck', 'us_kia', 'us_wia', 'iranian_killed', 'lebanese_killed', 'displaced', 'flights_cancelled', 'children_killed'];
      tollKeys.forEach(function(key) {
        var metric = toll[key];
        if (!metric) return;
        var container = document.querySelector('[data-hero="' + key + '"]');
        if (!container) return;

        var counter = container.querySelector('.counter');
        if (counter) counter.dataset.target = metric.value;

        var note = container.querySelector('.change');
        if (note) note.textContent = metric.note;

        container.setAttribute('title', metric.tooltip);

        var label = container.querySelector('.label');
        if (label) label.textContent = metric.label;
      });
    }
  }

  function setHero(id, value, change, tooltip) {
    var el = document.getElementById(id);
    if (el) el.textContent = value;
    if (change) {
      var changeEl = document.getElementById(id.replace('-price', '-change').replace('-value', '-change'));
      if (changeEl) changeEl.textContent = change;
    }
    if (tooltip && el) {
      var parent = el.closest('.hero-metric');
      if (parent) parent.setAttribute('title', tooltip);
    }
  }

  function setLabel(id, label) {
    var el = document.getElementById(id);
    if (el) {
      var labelEl = el.parentElement.querySelector('.label');
      if (labelEl) labelEl.textContent = label;
    }
  }

  // Cinematic intro — staggered fade reveal
  function initIntro() {
    var intro = document.getElementById('cinematic-intro');
    if (!intro) return;

    if (sessionStorage.getItem('wt-intro-seen')) {
      intro.remove();
      showDisclaimer();
      return;
    }

    function dismiss() {
      intro.classList.add('fade-out');
      sessionStorage.setItem('wt-intro-seen', '1');
      setTimeout(function() {
        intro.remove();
        showDisclaimer();
      }, 1000);
    }

    document.getElementById('intro-enter').addEventListener('click', dismiss);
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && intro.parentNode) dismiss();
    });
  }

  // Disclaimer gate — must acknowledge before viewing dashboard
  function showDisclaimer() {
    var overlay = document.getElementById('disclaimer-overlay');
    if (!overlay) return;

    if (sessionStorage.getItem('wt-disclaimer-ack')) {
      overlay.remove();
      return;
    }

    overlay.style.display = 'flex';

    var checkbox = document.getElementById('disclaimer-agree');
    var enterBtn = document.getElementById('disclaimer-enter');

    checkbox.addEventListener('change', function() {
      enterBtn.disabled = !checkbox.checked;
    });

    enterBtn.addEventListener('click', function() {
      overlay.classList.add('fade-out');
      sessionStorage.setItem('wt-disclaimer-ack', '1');
      setTimeout(function() { overlay.remove(); }, 1000);
    });
  }

  // ─── BOOT ───────────────────────────────────────────────
  try {
    initIntro();
    // If intro was absent, ensure disclaimer still fires
    if (!document.getElementById('cinematic-intro')) {
      showDisclaimer();
    }

    // Navigation
    initNavigation();
    // Theater panel is active on load — hide footer
    document.body.classList.add('theater-active');

    // Initialize map
    WarTheater.Map.init();

    // Load all data
    const data = await WarTheater.Data.loadAll();

    // Populate hero stats from JSON
    populateHeroStats(data.heroStats);

    // Populate map
    await WarTheater.Map.populate(data);

    // Financial charts
    WarTheater.Financial.init(data);

    // Humanitarian
    WarTheater.Humanitarian.init(data);

    // Calculator
    WarTheater.Calculator.init(data.calculator);

    // Timeline
    await WarTheater.Timeline.init();

    // Briefing
    await WarTheater.Briefing.init();

    console.log('[War Theater] Dashboard initialized. Day ' + WarTheater.Utils.getWarDay() + ' of Operation Epic Fury.');
  } catch (e) {
    console.error('[War Theater] Initialization failed:', e);
  }
})();
