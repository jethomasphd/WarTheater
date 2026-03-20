/* ═══════════════════════════════════════════════════════════════
   THE WAR THEATER — Financial Panel (Chart.js)
   Every chart tells the story of what this war costs.
   All data loaded from JSON files in public/data/.
   ═══════════════════════════════════════════════════════════════ */

WarTheater.Financial = {
  charts: {},

  init(data) {
    this.renderOilChart(data.oilPrices);
    this.renderMarketsChart(data.markets);
    this.renderHormuzChart(data.warCosts);
    this.renderDailyCostChart(data.warCosts);
  },

  // ─── OIL PRICE TIMELINE ──────────────────────────────────
  renderOilChart(oilData) {
    const ctx = document.getElementById('chart-oil');
    if (!ctx || !oilData) return;

    const labels = oilData.labels;
    const brent = oilData.brent;
    const wti = oilData.wti;
    const preWarIdx = oilData.pre_war_index;
    const dayMap = oilData.day_map;
    const baselines = oilData.baselines;

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
            pointRadius: labels.map(function(_, i) { return i === preWarIdx || i === labels.length - 1 ? 4 : (i === preWarIdx + 6 ? 3 : 0); }),
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
            pointRadius: labels.map(function(_, i) { return i === preWarIdx || i === labels.length - 1 ? 3 : 0; }),
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
                if (idx === preWarIdx) return label + ' — PRE-WAR CLOSE';
                if (idx > preWarIdx) {
                  var day = dayMap[idx - preWarIdx - 1] || (idx - preWarIdx);
                  return label + ' — Day ' + day + ' of conflict';
                }
                return label;
              },
              label: function(item) {
                var val = item.raw;
                var baseline = item.datasetIndex === 0 ? baselines.brent : baselines.wti;
                var name = item.datasetIndex === 0 ? 'Brent' : 'WTI';
                if (item.dataIndex <= preWarIdx) {
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
            max: 120,
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
  renderMarketsChart(marketsData) {
    var ctx = document.getElementById('chart-markets');
    if (!ctx || !marketsData) return;

    var labels = marketsData.labels;
    var contexts = marketsData.contexts;
    var ds = marketsData.datasets;
    var defaults = WarTheater.Utils.chartDefaults();

    function makeDataset(d, width) {
      return {
        label: d.label,
        data: d.data,
        borderColor: d.color,
        borderWidth: width,
        tension: 0.3,
        pointRadius: d.data.map(function(_, i) { return i === 0 || i === d.data.length - 1 ? 3 : 0; }),
        pointBackgroundColor: d.color
      };
    }

    this.charts.markets = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [
          makeDataset(ds.sp500, 2),
          makeDataset(ds.defense, 1.5),
          makeDataset(ds.oil_majors, 1.5),
          makeDataset(ds.airlines, 1.5)
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
  renderHormuzChart(warCostsData) {
    var ctx = document.getElementById('chart-hormuz');
    if (!ctx || !warCostsData) return;

    var t = warCostsData.tanker_transits;
    var labels = t.labels;
    var data = t.data;
    var prewar = t.prewar_daily;
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
                var pctDown = ((prewar - v) / prewar * 100).toFixed(0);
                return v + ' tankers/day (' + pctDown + '% below normal)';
              },
              afterLabel: function(item) {
                var v = item.raw;
                if (v <= 10) {
                  var lostBbl = ((prewar - v) / prewar * 20.5).toFixed(1);
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
  renderDailyCostChart(warCostsData) {
    var ctx = document.getElementById('chart-daily-cost');
    if (!ctx || !warCostsData) return;

    var labels = warCostsData.labels;
    var costs = warCostsData.daily_cost_millions;
    var dayNotes = warCostsData.day_notes;
    var homePrice = warCostsData.median_home_price_millions;

    var cumulative = [];
    var sum = 0;
    costs.forEach(function(c) { sum += c; cumulative.push(sum); });

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
                var homes = Math.round(costs[idx] / homePrice);
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
