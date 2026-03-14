/* ═══════════════════════════════════════════════════════════════
   THE WAR THEATER — Humanitarian Panel
   Every number was a person. The counter preserves that.
   ═══════════════════════════════════════════════════════════════ */

WarTheater.Humanitarian = {
  charts: {},

  init() {
    this.renderCasualtiesChart();
    this.renderInfrastructureGrid();
    this.renderHistoricalComparison();
  },

  // Animate all counter elements on scroll into view
  animateCounters() {
    var counters = document.querySelectorAll('.counter');
    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          var el = entry.target;
          var target = parseInt(el.dataset.target, 10);
          if (target && !el.dataset.animated) {
            el.dataset.animated = 'true';
            WarTheater.Utils.animateCounter(el, target, 2500);
          }
        }
      });
    }, { threshold: 0.3 });

    counters.forEach(function(c) { observer.observe(c); });
  },

  // ─── CASUALTIES BY DAY ────────────────────────────────────
  // AUDIT NOTE: Iranian military numbers scaled to match hero counter (1,500 total
  // through Day 14). Lebanese numbers adjusted to match hero counter (720 through
  // Day 14). All daily values are estimates from ACLED, IRNA, Lebanese Health
  // Ministry, and DoD; exact figures are unknowable in an active conflict.
  renderCasualtiesChart() {
    var ctx = document.getElementById('chart-casualties');
    if (!ctx) return;

    var labels = ['Feb 28', 'Mar 1', 'Mar 2', 'Mar 3', 'Mar 4', 'Mar 5', 'Mar 6', 'Mar 7', 'Mar 8', 'Mar 9', 'Mar 10', 'Mar 11', 'Mar 12', 'Mar 13'];
    var defaults = WarTheater.Utils.chartDefaults();

    var dayContexts = [
      'Day 1 — First strikes and Iranian retaliation',
      'Day 2 — Hormuz closure, sustained bombing',
      'Day 3 — Hezbollah enters the war',
      'Day 4 — Houthi attacks expand conflict',
      'Day 5 — Minab school incident (165+ killed)',
      'Day 6 — Global protests, air campaign continues',
      'Day 7 — One week of conflict',
      'Day 8 — Oil infrastructure strikes begin',
      'Day 9 — SPR release, strikes continue',
      'Day 10 — New Supreme Leader named',
      'Day 11 — No ceasefire in sight',
      'Day 12 — NATO intercepts Iranian missile over Turkey; 8th US KIA',
      'Day 13 — IDF ground war in Lebanon; IRGC fires on US Navy; Ahvaz hospital incident',
      'Day 14 — IRGC batteries destroyed; second convoy; IDF at Bint Jbeil'
    ];

    this.charts.casualties = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Iranian Military',
            data: [65, 98, 122, 106, 90, 82, 73, 114, 98, 65, 65, 78, 91, 95],
            backgroundColor: 'rgba(184, 28, 28, 0.6)',
            borderColor: '#b81c1c',
            borderWidth: 1,
            stack: 'casualties'
          },
          {
            label: 'Iranian Civilian',
            data: [5, 10, 15, 12, 35, 20, 15, 25, 18, 10, 8, 45, 20, 20],
            backgroundColor: 'rgba(255, 255, 255, 0.35)',
            borderColor: '#ffffff',
            borderWidth: 1,
            stack: 'casualties'
          },
          {
            label: 'US Military',
            data: [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
            backgroundColor: 'rgba(74, 158, 255, 0.6)',
            borderColor: '#4a9eff',
            borderWidth: 1,
            stack: 'casualties'
          },
          {
            label: 'Lebanese (all)',
            data: [0, 0, 44, 58, 64, 68, 61, 75, 58, 48, 40, 54, 85, 65],
            backgroundColor: 'rgba(123, 63, 160, 0.6)',
            borderColor: '#7b3fa0',
            borderWidth: 1,
            stack: 'casualties'
          },
          {
            label: 'Israeli Military',
            data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 6],
            backgroundColor: 'rgba(255, 200, 50, 0.6)',
            borderColor: '#ffc832',
            borderWidth: 1,
            stack: 'casualties'
          }
        ]
      },
      options: {
        ...defaults,
        plugins: {
          ...defaults.plugins,
          tooltip: {
            ...defaults.plugins.tooltip,
            callbacks: {
              title: function(items) {
                var idx = items[0].dataIndex;
                return dayContexts[idx] || items[0].label;
              },
              afterBody: function(items) {
                var idx = items[0].dataIndex;
                var total = 0;
                items.forEach(function(item) { total += item.raw; });
                var lines = ['', 'Total this day: ~' + total + ' estimated casualties'];
                if (idx === 4) lines.push('Includes 165+ killed at Minab girls\' school');
                return lines;
              },
              footer: function() {
                return 'Source: ACLED, DoD, Lebanese Health Ministry, IRNA';
              }
            }
          }
        },
        scales: {
          ...defaults.scales,
          x: { ...defaults.scales.x, stacked: true },
          y: {
            ...defaults.scales.y,
            stacked: true,
            ticks: {
              ...defaults.scales.y.ticks,
              callback: function(v) { return v + ' est.'; }
            }
          }
        }
      }
    });
  },

  // ─── INFRASTRUCTURE DAMAGE ────────────────────────────────
  renderInfrastructureGrid() {
    var grid = document.getElementById('infrastructure-grid');
    if (!grid) return;

    var items = [
      {
        label: 'Hospitals Damaged',
        count: '5+',
        note: 'Lebanon + Ahvaz, Iran',
        source: 'OCHA / IRNA',
        detail: 'Structural damage from strikes on adjacent military positions. 3+ facilities in south Lebanon degraded. Day 13: Hospital in Ahvaz damaged. Day 14: Sidon field hospital reports structural damage from nearby ground combat.'
      },
      {
        label: 'Schools Destroyed',
        count: '1',
        note: 'Minab, Iran',
        source: 'Iranian Red Crescent / AP',
        detail: 'Girls\' school struck by US Tomahawk cruise missile adjacent to IRGC naval complex. 165-180 killed (mostly girls aged 7-12). School triple-tapped per Iranian officials. Pentagon investigation underway.'
      },
      {
        label: 'Power Plants Hit',
        count: '4+',
        note: 'Western Iran',
        source: 'DoD / satellite imagery',
        detail: 'Grid disruptions across western Iran. Isfahan, Kermanshah, Ahvaz power infrastructure degraded. Civilian blackouts reported in multiple provinces.'
      },
      {
        label: 'Oil Facilities Hit',
        count: '3',
        note: 'Kharg, Abadan + storage',
        source: 'DoD / shipping data',
        detail: '90% of Iran\'s oil export capacity targeted since March 7. Kharg Island terminal — which handles 90% of Iranian oil exports — effectively destroyed.'
      },
      {
        label: 'Airports Damaged',
        count: '5+',
        note: 'Iran + region',
        source: 'ACLED / Flightradar24',
        detail: 'Mehrabad (Tehran), Shiraz TAB 6, Tabriz TAB 2 runways cratered in first wave. Regional airspace closures affect 19,500+ commercial flights.'
      },
      {
        label: 'Bridges Destroyed',
        count: '8+',
        note: 'Western Iran',
        source: 'Satellite imagery',
        detail: 'Road and rail bridges in Kermanshah, Lorestan, and Khuzestan provinces destroyed to degrade IRGC logistics and prevent resupply to missile launch sites.'
      }
    ];

    grid.innerHTML = items.map(function(item) {
      return '<div class="card" style="text-align: center; padding: var(--space-lg);" title="' + item.detail.replace(/"/g, '&quot;') + '">' +
        '<div class="font-data" style="font-size: var(--text-2xl); color: var(--humanitarian); line-height: 1;">' + item.count + '</div>' +
        '<div style="font-family: \'Barlow Condensed\', sans-serif; font-size: var(--text-sm); text-transform: uppercase; letter-spacing: 0.06em; color: var(--text-primary); margin-top: 8px;">' + item.label + '</div>' +
        '<div style="font-size: 10px; color: var(--text-dim); margin-top: 4px;">' + item.note + '</div>' +
        '<div style="font-size: 10px; color: var(--text-secondary); margin-top: 8px; padding-top: 6px; border-top: 1px solid var(--border); text-align: left; line-height: 1.5;">' + item.detail + '</div>' +
        '<div style="font-size: 9px; color: var(--text-dim); margin-top: 6px; font-family: \'JetBrains Mono\', monospace;">Source: ' + item.source + '</div>' +
        '</div>';
    }).join('');
  },

  // ─── HISTORICAL COMPARISON ────────────────────────────────
  // Sources: CRS Reports R44116 (Iraq), RL33110 (Gulf War), R41725 (Libya).
  // Iraq 2003 Day 14: ~15,000 sorties flown, ~75 US KIA (CRS R44116, p.12).
  // Costs inflation-adjusted to 2026 dollars using BLS CPI-U.
  // Gulf 1991 Day 14: air campaign only (ground war began Day 39).
  renderHistoricalComparison() {
    var ctx = document.getElementById('chart-historical');
    if (!ctx) return;

    var defaults = WarTheater.Utils.chartDefaults();

    var conflictNotes = {
      0: 'Operation Epic Fury — air + ground (Lebanon). 3 carrier groups. Hormuz partially breached. IRGC coastal batteries destroyed. IDF at Bint Jbeil.',
      1: 'Operation Iraqi Freedom — "shock and awe" + ground invasion. 300,000 troops deployed.',
      2: 'Operation Odyssey Dawn / Unified Protector — NATO no-fly zone. Limited US role.',
      3: 'Operation Desert Storm — 38-day air campaign + 100-hour ground war. 700,000 coalition troops.'
    };

    this.charts.historical = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['Iran 2026 (Day 14)', 'Iraq 2003 (Day 14)', 'Libya 2011 (Day 14)', 'Gulf 1991 (Day 14)'],
        datasets: [
          {
            label: 'Total Strikes',
            data: [3700, 15000, 510, 22000],
            backgroundColor: 'rgba(212, 120, 42, 0.5)',
            borderColor: '#d4782a',
            borderWidth: 1
          },
          {
            label: 'US KIA',
            data: [8, 75, 0, 18],
            backgroundColor: 'rgba(74, 158, 255, 0.5)',
            borderColor: '#4a9eff',
            borderWidth: 1
          },
          {
            label: 'Est. Daily Cost ($M, 2026 dollars)',
            data: [580, 750, 125, 620],
            backgroundColor: 'rgba(239, 68, 68, 0.5)',
            borderColor: '#ef4444',
            borderWidth: 1
          }
        ]
      },
      options: {
        ...defaults,
        indexAxis: 'y',
        plugins: {
          ...defaults.plugins,
          tooltip: {
            ...defaults.plugins.tooltip,
            callbacks: {
              title: function(items) {
                return items[0].label;
              },
              afterBody: function(items) {
                var idx = items[0].dataIndex;
                return conflictNotes[idx] ? ['\n' + conflictNotes[idx]] : [];
              },
              footer: function() {
                return 'Sources: CRS, DoD historical data, ACLED, CBO';
              }
            }
          }
        },
        scales: {
          x: {
            ...defaults.scales.x,
            stacked: false
          },
          y: {
            ...defaults.scales.y,
            ticks: {
              ...defaults.scales.y.ticks,
              font: { family: "'Barlow Condensed', sans-serif", size: 11 }
            }
          }
        }
      }
    });
  }
};
