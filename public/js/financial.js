/* ═══════════════════════════════════════════════════════════════
   THE WAR THEATER — Financial Panel (Chart.js)
   Every chart tells the story of what this war costs.
   ═══════════════════════════════════════════════════════════════ */

WarTheater.Financial = {
  charts: {},

  init(data) {
    this.renderOilChart();
    this.renderMarketsChart();
    this.renderHormuzChart();
    this.renderDailyCostChart();
  },

  // ─── OIL PRICE TIMELINE ──────────────────────────────────
  renderOilChart() {
    const ctx = document.getElementById('chart-oil');
    if (!ctx) return;

    const labels = [
      'Jan 2', 'Jan 8', 'Jan 15', 'Jan 22', 'Jan 29',
      'Feb 5', 'Feb 12', 'Feb 19', 'Feb 27',
      'Feb 28', 'Mar 1', 'Mar 2', 'Mar 3', 'Mar 4', 'Mar 5',
      'Mar 6', 'Mar 7', 'Mar 8', 'Mar 9', 'Mar 10', 'Mar 11', 'Mar 12', 'Mar 13'
    ];

    const brent = [
      74.2, 73.8, 72.1, 71.5, 72.8,
      73.1, 71.9, 72.6, 72.38,
      85.4, 88.7, 90.2, 91.8, 93.5, 94.1,
      96.3, 101.5, 100.8, 101.1, 101.5, 88.3, 100.11, 98.82
    ];

    const wti = [
      71.8, 71.2, 69.8, 69.1, 70.5,
      70.9, 69.5, 70.3, 70.82,
      82.1, 85.9, 87.3, 88.7, 90.1, 91.5,
      93.8, 97.8, 97.2, 97.8, 98.2, 85.1, 95.28, 95.28
    ];

    const defaults = WarTheater.Utils.chartDefaults();

    this.charts.oil = new Chart(ctx, {
      type: 'line',
      data: {
        labels,
        datasets: [
          {
            label: 'Brent Crude ($/bbl)',
            data: brent,
            borderColor: '#d4782a',
            backgroundColor: 'rgba(212, 120, 42, 0.08)',
            borderWidth: 2,
            fill: true,
            tension: 0.3,
            pointRadius: labels.map(function(_, i) { return i === 8 || i === labels.length - 1 ? 4 : 0; }),
            pointBackgroundColor: '#d4782a',
            pointHitRadius: 10
          },
          {
            label: 'WTI Crude ($/bbl)',
            data: wti,
            borderColor: '#8a8a8a',
            backgroundColor: 'rgba(138, 138, 138, 0.04)',
            borderWidth: 1.5,
            fill: true,
            tension: 0.3,
            pointRadius: labels.map(function(_, i) { return i === 8 || i === labels.length - 1 ? 3 : 0; }),
            pointBackgroundColor: '#8a8a8a',
            pointHitRadius: 10
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
                var label = items[0].label;
                if (idx === 8) return label + ' — PRE-WAR CLOSE';
                if (idx >= 9) return label + ' — Day ' + (idx - 8) + ' of conflict';
                return label;
              },
              label: function(item) {
                var val = item.raw;
                var baseline = item.datasetIndex === 0 ? 72.38 : 70.82;
                var name = item.datasetIndex === 0 ? 'Brent' : 'WTI';
                if (item.dataIndex <= 8) {
                  return name + ': $' + val.toFixed(2) + '/bbl';
                }
                var change = ((val - baseline) / baseline * 100).toFixed(1);
                return name + ': $' + val.toFixed(2) + '/bbl  (+' + change + '% since pre-war)';
              }
            }
          }
        },
        scales: {
          ...defaults.scales,
          y: {
            ...defaults.scales.y,
            min: 65,
            max: 110,
            ticks: {
              ...defaults.scales.y.ticks,
              callback: function(v) { return '$' + v; }
            }
          }
        }
      }
    });
  },

  // ─── MARKET IMPACT ────────────────────────────────────────
  // NOTE: S&P indexed values reflect the composite effect of surging defense/oil
  // sectors (+15-22%) offsetting broader market declines. The S&P dropped to 91.7
  // (6,297) at its worst on Day 5, then recovered as sector rotation stabilized
  // the index. Hero metric 6,672.62 on Day 14 = 97.2 indexed.
  renderMarketsChart() {
    var ctx = document.getElementById('chart-markets');
    if (!ctx) return;

    var labels = ['Feb 27', 'Feb 28', 'Mar 1', 'Mar 2', 'Mar 3', 'Mar 4', 'Mar 5', 'Mar 6', 'Mar 7', 'Mar 8', 'Mar 9', 'Mar 10', 'Mar 11', 'Mar 12', 'Mar 13'];
    var defaults = WarTheater.Utils.chartDefaults();

    var contexts = [
      'Pre-war close — baseline',
      'War begins — markets crash on open',
      'Hormuz closure — oil stocks surge',
      'Hezbollah enters — second front opens',
      'Houthi attacks on Saudi oil',
      'Minab school incident — S&P hits war low (6,297)',
      'Markets stabilize — defense/oil surge offsets broader decline',
      'Sector rotation continues — defense +10.5%',
      'US strikes Iranian oil — Brent tops $100',
      'SPR release announced — modest recovery',
      'New Supreme Leader — no ceasefire',
      'Day 11 — no end in sight',
      'Day 12 — Oil crashes on false Hormuz claim; markets rally on hope',
      'Day 13 — Defense surge on ground war; S&P recovers to 6,694',
      'Day 14 — AUMF debate; oil eases; S&P dips to 6,673'
    ];

    this.charts.markets = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'S&P 500',
            data: [100, 96.5, 95.0, 94.0, 93.0, 91.7, 92.0, 92.5, 92.0, 92.5, 93.0, 93.5, 95.0, 97.5, 97.2],
            borderColor: '#ef4444',
            borderWidth: 2,
            tension: 0.3,
            pointRadius: [3, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 3],
            pointBackgroundColor: '#ef4444'
          },
          {
            label: 'Defense (RTX + LMT)',
            data: [100, 103.5, 105.0, 106.5, 108.0, 109.5, 110.0, 110.5, 112.0, 112.5, 112.8, 113.0, 111.5, 115.8, 116.5],
            borderColor: '#22c55e',
            borderWidth: 1.5,
            tension: 0.3,
            pointRadius: [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
            pointBackgroundColor: '#22c55e'
          },
          {
            label: 'Oil Majors (XOM + CVX)',
            data: [100, 106.0, 110.0, 112.0, 114.0, 116.0, 117.0, 119.0, 124.0, 123.5, 124.0, 123.5, 117.0, 122.0, 121.0],
            borderColor: '#d4a020',
            borderWidth: 1.5,
            tension: 0.3,
            pointRadius: [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
            pointBackgroundColor: '#d4a020'
          },
          {
            label: 'Airlines (DAL + UAL)',
            data: [100, 92.0, 88.0, 85.0, 83.0, 81.0, 79.5, 78.5, 77.0, 77.5, 78.0, 78.5, 80.0, 76.0, 75.5],
            borderColor: '#7b3fa0',
            borderWidth: 1.5,
            tension: 0.3,
            pointRadius: [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
            pointBackgroundColor: '#7b3fa0'
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
                if (idx === 0) return items[0].label + ' — BASELINE (pre-war close)';
                return items[0].label + ' — Day ' + idx;
              },
              label: function(item) {
                var val = item.raw;
                var change = (val - 100).toFixed(1);
                var sign = val >= 100 ? '+' : '';
                return item.dataset.label + ': ' + val.toFixed(1) + ' (' + sign + change + '%)';
              },
              afterBody: function(items) {
                var idx = items[0].dataIndex;
                return contexts[idx] ? ['\n' + contexts[idx]] : [];
              }
            }
          }
        },
        scales: {
          ...defaults.scales,
          y: {
            ...defaults.scales.y,
            min: 70,
            max: 130,
            ticks: {
              ...defaults.scales.y.ticks,
              callback: function(v) {
                if (v === 100) return '100 (baseline)';
                return v;
              }
            }
          }
        }
      }
    });
  },

  // ─── HORMUZ TANKER CHART ──────────────────────────────────
  renderHormuzChart() {
    var ctx = document.getElementById('chart-hormuz');
    if (!ctx) return;

    var labels = ['Feb 25', 'Feb 26', 'Feb 27', 'Feb 28', 'Mar 1', 'Mar 2', 'Mar 3', 'Mar 4', 'Mar 5', 'Mar 6', 'Mar 7', 'Mar 8', 'Mar 9', 'Mar 10', 'Mar 11', 'Mar 12', 'Mar 13'];
    var data = [85, 84, 85, 42, 5, 3, 2, 2, 2, 3, 2, 2, 3, 2, 3, 6, 8];
    var defaults = WarTheater.Utils.chartDefaults();

    this.charts.hormuz = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: 'Daily Tanker Transits',
          data: data,
          backgroundColor: data.map(function(v) { return v > 40 ? 'rgba(212, 160, 32, 0.6)' : 'rgba(239, 68, 68, 0.6)'; }),
          borderColor: data.map(function(v) { return v > 40 ? '#d4a020' : '#ef4444'; }),
          borderWidth: 1
        }]
      },
      options: {
        ...defaults,
        plugins: {
          ...defaults.plugins,
          legend: { display: false },
          tooltip: {
            ...defaults.plugins.tooltip,
            callbacks: {
              title: function(items) {
                var idx = items[0].dataIndex;
                if (idx < 3) return items[0].label + ' — Pre-war normal';
                if (idx === 3) return items[0].label + ' — WAR BEGINS';
                return items[0].label + ' — Day ' + (idx - 2) + ' of closure';
              },
              label: function(item) {
                var v = item.raw;
                if (v >= 40) return v + ' tankers/day (normal traffic)';
                var pctDown = ((85 - v) / 85 * 100).toFixed(0);
                return v + ' tankers/day (' + pctDown + '% below normal)';
              },
              afterLabel: function(item) {
                var v = item.raw;
                if (v <= 10) {
                  var lostBbl = ((85 - v) / 85 * 20.5).toFixed(1);
                  return 'Approx. ' + lostBbl + 'M barrels/day blocked\nInsurance premiums up 1100%';
                }
                return '';
              }
            }
          }
        },
        scales: {
          ...defaults.scales,
          y: {
            ...defaults.scales.y,
            min: 0,
            max: 100,
            ticks: {
              ...defaults.scales.y.ticks,
              callback: function(v) { return v + ' ships'; }
            }
          }
        }
      }
    });
  },

  // ─── DAILY COST CHART ─────────────────────────────────────
  renderDailyCostChart() {
    var ctx = document.getElementById('chart-daily-cost');
    if (!ctx) return;

    var labels = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7', 'Day 8', 'Day 9', 'Day 10', 'Day 11', 'Day 12', 'Day 13', 'Day 14'];
    var costs = [380, 420, 480, 500, 510, 490, 500, 520, 510, 505, 500, 515, 560, 580];
    var cumulative = [];
    var sum = 0;
    costs.forEach(function(c) { sum += c; cumulative.push(sum); });

    var dayNotes = [
      'First strikes — Tomahawks + B-2s + F-35s',
      'Sustained air campaign — 1,000+ sorties',
      'Escalation — 3 carrier groups fully engaged',
      'Full tempo operations',
      'Minab incident — global scrutiny intensifies',
      'Continued operations — week 1 ends',
      'One week mark — $3.3B spent',
      'Oil infrastructure strikes begin',
      'Brent crosses $100/barrel',
      'SPR release — costs continue mounting',
      'Day 11 — no ceasefire in sight',
      'Day 12 — Oil crashes; 3 ships hit in Hormuz',
      'Day 13 — Hormuz convoy ops; IRGC engages US Navy; IDF ground war in Lebanon',
      'Day 14 — Retaliatory strikes on IRGC batteries; second convoy; Bint Jbeil'
    ];

    var defaults = WarTheater.Utils.chartDefaults();

    this.charts.dailyCost = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Daily Cost ($M)',
            data: costs,
            backgroundColor: 'rgba(212, 120, 42, 0.5)',
            borderColor: '#d4782a',
            borderWidth: 1,
            yAxisID: 'y'
          },
          {
            label: 'Cumulative Total ($M)',
            data: cumulative,
            type: 'line',
            borderColor: '#ef4444',
            borderWidth: 2,
            tension: 0.3,
            pointRadius: labels.map(function(_, i) { return i === labels.length - 1 ? 5 : 0; }),
            pointBackgroundColor: '#ef4444',
            yAxisID: 'y1'
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
                return items[0].label + ' of Operation Epic Fury';
              },
              afterBody: function(items) {
                var idx = items[0].dataIndex;
                var total = cumulative[idx];
                var lines = [
                  'Running total: $' + (total / 1000).toFixed(2) + 'B'
                ];
                if (dayNotes[idx]) lines.push(dayNotes[idx]);
                // Opportunity cost context
                var homes = Math.round(costs[idx] / 0.2);
                lines.push('This day alone = ' + WarTheater.Utils.formatNumber(homes) + ' median US homes');
                return lines;
              }
            }
          }
        },
        scales: {
          ...defaults.scales,
          y: {
            ...defaults.scales.y,
            position: 'left',
            ticks: {
              ...defaults.scales.y.ticks,
              callback: function(v) { return '$' + v + 'M'; }
            }
          },
          y1: {
            ...defaults.scales.y,
            position: 'right',
            grid: { drawOnChartArea: false },
            ticks: {
              ...defaults.scales.y.ticks,
              callback: function(v) { return '$' + (v / 1000).toFixed(1) + 'B'; }
            }
          }
        }
      }
    });
  }
};
