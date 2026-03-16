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
      'Mar 2', 'Mar 3', 'Mar 4', 'Mar 5',
      'Mar 6', 'Mar 9', 'Mar 10', 'Mar 11', 'Mar 12', 'Mar 13', 'Mar 16'
    ];

    // Source: Financials.md source of truth (CNBC/FRED/EIA confirmed settlements)
    // Pre-war weekly prices, then trading-day-only post-war data
    // Mar 16: Brent +3% on Fujairah/Dubai attacks (CNBC/Bloomberg)
    const brent = [
      74.2, 73.8, 72.1, 71.5, 72.8,
      73.1, 71.9, 72.6, 71.00,
      77.74, 81.40, 82.50, 82.73,
      92.66, 98.96, 87.80, 91.98, 100.46, 103.14, 106.18
    ];

    const wti = [
      71.8, 71.2, 69.8, 69.1, 70.5,
      70.9, 69.5, 70.3, 66.50,
      71.23, 74.56, 77.50, 80.97,
      90.86, 94.77, 83.45, 87.25, 95.73, 98.71, 100.66
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
            pointRadius: labels.map(function(_, i) { return i === 8 || i === labels.length - 1 ? 4 : (i === 14 ? 3 : 0); }),
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
                if (idx >= 9) {
                  // Trading-day-only labels: Mar 2=Day 3, Mar 3=Day 4, Mar 4=Day 5, Mar 5=Day 6,
                  // Mar 6=Day 7, Mar 9=Day 10, Mar 10=Day 11, Mar 11=Day 12, Mar 12=Day 13, Mar 13=Day 14
                  var dayMap = [3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 17];
                  var day = dayMap[idx - 9] || (idx - 8);
                  return label + ' — Day ' + day + ' of conflict';
                }
                return label;
              },
              label: function(item) {
                var val = item.raw;
                var baseline = item.datasetIndex === 0 ? 71.00 : 66.50;
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

    // Markets chart uses trading days only (Feb 28 and Mar 1 were weekend — no trading)
    var labels = ['Feb 27', 'Mar 2', 'Mar 3', 'Mar 4', 'Mar 5', 'Mar 6', 'Mar 9', 'Mar 10', 'Mar 11', 'Mar 12', 'Mar 13', 'Mar 16'];
    var defaults = WarTheater.Utils.chartDefaults();

    var contexts = [
      'Pre-war close — baseline',
      'Day 3 — First trading session; S&P recovers from -1.2% intraday to flat',
      'Day 4 — S&P -0.94%; Brent +4.71%; Hormuz closure formal',
      'Day 5 — S&P bounces +0.78%; oil prices steady',
      'Day 6 — Pentagon: $11.3B cumulative cost; S&P -0.56%',
      'Day 7 — S&P -1.33%; WTI best week since 1983; worst S&P week in 5 months',
      'Day 10 — Brent intraday $119.50; Trump says war "very complete"',
      'Day 11 — Brent crashes 11.3% on false Hormuz escort report',
      'Day 12 — IEA 400M bbl reserve release; CSIS: $16.5B cumulative',
      'Day 13 — Brent closes above $100; S&P -1.52% (worst since Feb)',
      'Day 14 — S&P hits 2026 low at 6,632; Brent $103.14; AUMF debate',
      'Day 17 — Brent $106.18 on Fujairah/Dubai attacks; S&P futures +0.5%'
    ];

    this.charts.markets = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [
          {
            // S&P 500 indexed: baseline 6878.88 = 100
            // Confirmed closes: 6881.62, 6816.63, 6869.50, 6830.71, 6740.02, 6795.99, 6781.48, 6775.80, 6672.62, 6632.19
            // Mar 16: futures +0.5% from 6632.19 ≈ 6664 = 96.9 indexed (intraday, not close)
            label: 'S&P 500',
            data: [100, 100.0, 99.1, 99.9, 99.3, 98.0, 98.8, 98.6, 98.5, 97.0, 96.4, 96.9],
            borderColor: '#ef4444',
            borderWidth: 2,
            tension: 0.3,
            pointRadius: [3, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 3],
            pointBackgroundColor: '#ef4444'
          },
          {
            label: 'Defense (RTX + LMT)',
            data: [100, 103.5, 106.0, 108.0, 109.5, 110.5, 112.5, 113.0, 113.5, 115.8, 116.5, 117.0],
            borderColor: '#22c55e',
            borderWidth: 1.5,
            tension: 0.3,
            pointRadius: [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
            pointBackgroundColor: '#22c55e'
          },
          {
            label: 'Oil Majors (XOM + CVX)',
            data: [100, 106.0, 110.0, 112.0, 114.0, 119.0, 124.0, 117.0, 121.0, 128.0, 130.0, 133.0],
            borderColor: '#d4a020',
            borderWidth: 1.5,
            tension: 0.3,
            pointRadius: [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
            pointBackgroundColor: '#d4a020'
          },
          {
            label: 'Airlines (DAL + UAL)',
            data: [100, 92.0, 88.0, 85.0, 83.0, 81.0, 78.0, 78.5, 78.0, 76.0, 75.5, 74.0],
            borderColor: '#7b3fa0',
            borderWidth: 1.5,
            tension: 0.3,
            pointRadius: [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
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
                if (contexts[idx]) return items[0].label + ' — ' + contexts[idx];
                return items[0].label;
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

    var labels = ['Feb 25', 'Feb 26', 'Feb 27', 'Feb 28', 'Mar 1', 'Mar 2', 'Mar 3', 'Mar 4', 'Mar 5', 'Mar 6', 'Mar 7', 'Mar 8', 'Mar 9', 'Mar 10', 'Mar 11', 'Mar 12', 'Mar 13', 'Mar 14', 'Mar 15', 'Mar 16'];
    // Source: USNI/Lloyd's List AIS data. Pre-war ~50/day. Traffic down 97% by Day 11.
    // Shadow fleet/Chinese-flagged vessels account for remaining transits.
    var data = [50, 50, 50, 25, 5, 0, 2, 2, 2, 3, 2, 2, 3, 2, 3, 3, 3, 3, 3, 3];
    var defaults = WarTheater.Utils.chartDefaults();

    this.charts.hormuz = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: 'Daily Tanker Transits',
          data: data,
          backgroundColor: data.map(function(v) { return v > 30 ? 'rgba(212, 160, 32, 0.6)' : 'rgba(239, 68, 68, 0.6)'; }),
          borderColor: data.map(function(v) { return v > 30 ? '#d4a020' : '#ef4444'; }),
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
                if (v >= 30) return v + ' tankers/day (normal traffic)';
                var pctDown = ((50 - v) / 50 * 100).toFixed(0);
                return v + ' tankers/day (' + pctDown + '% below normal)';
              },
              afterLabel: function(item) {
                var v = item.raw;
                if (v <= 10) {
                  var lostBbl = ((50 - v) / 50 * 20.5).toFixed(1);
                  return 'Approx. ' + lostBbl + 'M barrels/day blocked\nInsurance premiums up 400%';
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

    // Source: Financials.md — Pentagon $11.3B Day 6, CSIS $16.5B Day 12, Penn Wharton daily estimates
    // Values in $M. Front-loaded: ~$3B/day opening then declining to ~$850M/day steady state
    var labels = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7', 'Day 8', 'Day 9', 'Day 10', 'Day 11', 'Day 12', 'Day 13', 'Day 14', 'Day 15', 'Day 16', 'Day 17'];
    var costs = [3000, 2600, 2000, 1500, 1100, 1100, 1000, 900, 800, 800, 850, 850, 900, 900, 850, 850, 850];
    var cumulative = [];
    var sum = 0;
    costs.forEach(function(c) { sum += c; cumulative.push(sum); });

    var dayNotes = [
      'First strikes — $5.6B munitions in 48 hrs (WaPo)',
      'Sustained air campaign — 900 targets in first 12 hours',
      'First trading day — 3 carrier groups fully engaged',
      'Hormuz formally closed — insurance-driven shutdown',
      'Minab school — global scrutiny; Pentagon: $11.3B cumulative',
      'Pentagon reports $11.3B to Senate — confirmed anchor point',
      'One week — WTI best week since 1983',
      'Oil infrastructure strikes begin — Kharg, Abadan',
      'Brent intraday $119.50 — SPR release announced',
      'New Supreme Leader — 16 minelayers destroyed',
      'IEA 400M bbl reserve release — CSIS: $16.5B cumulative',
      'Brent closes above $100 — 5 vessels hit in Hormuz',
      'KC-135 crash kills 6 — IDF ground war in Lebanon',
      'Kharg Island struck — 15,000+ targets — AUMF debate',
      'Weekend — France/Italy open talks with Iran',
      'Weekend — gas at $3.69 — war cost at ~$20B',
      'Day 17 — Dubai airport struck; Brent $106.18; 56% oppose war'
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
                  'Running total: $' + (total / 1000).toFixed(1) + 'B'
                ];
                if (dayNotes[idx]) lines.push(dayNotes[idx]);
                // Opportunity cost context — median US home ~$420K
                var homes = Math.round(costs[idx] / 0.42);
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
