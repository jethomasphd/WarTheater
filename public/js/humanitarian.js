/* ═══════════════════════════════════════════════════════════════
   THE WAR THEATER — Humanitarian Panel
   Every number was a person. The counter preserves that.
   All data loaded from JSON files in public/data/.
   ═══════════════════════════════════════════════════════════════ */

WarTheater.Humanitarian = {
  charts: {},

  init(data) {
    this.renderCasualtiesChart(data.casualties);
    this.renderInfrastructureGrid(data.infrastructure);
    this.renderHistoricalComparison(data.historicalComparison);
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
  renderCasualtiesChart(casualtyData) {
    var ctx = document.getElementById('chart-casualties');
    if (!ctx || !casualtyData) return;

    var labels = casualtyData.labels;
    var dayContexts = casualtyData.day_contexts;
    var ds = casualtyData.datasets;
    var defaults = WarTheater.Utils.chartDefaults();

    function makeDataset(d) {
      return {
        label: d.label,
        data: d.data,
        backgroundColor: d.color === '#ffffff' ? 'rgba(255, 255, 255, 0.35)' : d.color.replace(')', ', 0.6)').replace('rgb', 'rgba').replace('#', ''),
        borderColor: d.color,
        borderWidth: 1,
        stack: 'casualties'
      };
    }

    // Build datasets with proper alpha for stacked bars
    var colorAlpha = {
      '#b81c1c': 'rgba(184, 28, 28, 0.6)',
      '#ffffff': 'rgba(255, 255, 255, 0.35)',
      '#4a9eff': 'rgba(74, 158, 255, 0.6)',
      '#7b3fa0': 'rgba(123, 63, 160, 0.6)',
      '#ffc832': 'rgba(255, 200, 50, 0.6)'
    };

    var datasets = Object.values(ds).map(function(d) {
      return {
        label: d.label,
        data: d.data,
        backgroundColor: colorAlpha[d.color] || 'rgba(138, 138, 138, 0.6)',
        borderColor: d.color,
        borderWidth: 1,
        stack: 'casualties'
      };
    });

    this.charts.casualties = new Chart(ctx, {
      type: 'bar',
      data: { labels: labels, datasets: datasets },
      options: {
        ...defaults,
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
                var total = 0;
                items.forEach(function(item) { total += item.raw; });
                var lines = ['', 'Total this day: ~' + total + ' estimated casualties'];
                if (idx === 0) lines.push('Includes 165+ killed at Minab girls\' school');
                if (dayContexts[idx]) {
                  var U = WarTheater.Utils, w = window.innerWidth < 600 ? 42 : 70;
                  lines = lines.concat([''], U.wrap(U.latest(dayContexts[idx], 420), w));
                }
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
  renderInfrastructureGrid(infraData) {
    var grid = document.getElementById('infrastructure-grid');
    if (!grid || !infraData) return;

    var U = WarTheater.Utils;
    grid.innerHTML = infraData.map(function(item) {
      var latestNote = U.latest(item.note);
      var shortNote = U.latest(item.note, 220);
      var detail = U.latest(item.detail);
      return '<div class="card infra-card" style="text-align: center; padding: var(--space-lg);">' +
        '<div class="font-data" style="font-size: var(--text-2xl); color: var(--humanitarian); line-height: 1;">' + item.count + '</div>' +
        '<div style="font-family: \'Barlow Condensed\', sans-serif; font-size: var(--text-sm); text-transform: uppercase; letter-spacing: 0.06em; color: var(--text-primary); margin-top: 8px;">' + item.label + '</div>' +
        '<div style="font-size: 10px; color: var(--text-dim); margin-top: 4px; text-align: left; line-height: 1.5;">' + shortNote + '</div>' +
        '<details class="infra-more"><summary>Latest update &amp; background</summary>' +
        (latestNote.length > shortNote.length ? '<p>' + latestNote + '</p>' : '') +
        '<p>' + detail + '</p></details>' +
        '<div style="font-size: 9px; color: var(--text-dim); margin-top: 6px; font-family: \'JetBrains Mono\', monospace;">Source: ' + item.source + '</div>' +
        '</div>';
    }).join('');
  },

  // ─── HISTORICAL COMPARISON ────────────────────────────────
  renderHistoricalComparison(histData) {
    var ctx = document.getElementById('chart-historical');
    if (!ctx || !histData) return;

    var defaults = WarTheater.Utils.chartDefaults();
    var conflicts = histData.conflicts;

    var conflictNotes = {};
    conflicts.forEach(function(c, i) { conflictNotes[i] = c.note; });

    this.charts.historical = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: conflicts.map(function(c) { return c.label; }),
        datasets: [
          {
            label: 'Targets Struck',
            data: conflicts.map(function(c) { return c.targets_struck; }),
            backgroundColor: 'rgba(212, 120, 42, 0.5)',
            borderColor: '#d4782a',
            borderWidth: 1
          },
          {
            label: 'US KIA',
            data: conflicts.map(function(c) { return c.us_kia; }),
            backgroundColor: 'rgba(74, 158, 255, 0.5)',
            borderColor: '#4a9eff',
            borderWidth: 1
          },
          {
            label: 'Est. Daily Cost ($M, 2026 dollars)',
            data: conflicts.map(function(c) { return c.daily_cost_millions; }),
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
                if (!conflictNotes[idx]) return [];
                var U = WarTheater.Utils, w = window.innerWidth < 600 ? 42 : 70;
                return [''].concat(U.wrap(conflictNotes[idx], w));
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
