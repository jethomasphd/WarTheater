/* ═══════════════════════════════════════════════════════════════
   THE WAR THEATER — Financial Panel (Chart.js)
   ═══════════════════════════════════════════════════════════════ */

WarTheater.Financial = {
  charts: {},

  init(data) {
    this.renderOilChart();
    this.renderMarketsChart();
    this.renderHormuzChart();
    this.renderDailyCostChart();
  },

  renderOilChart() {
    const ctx = document.getElementById('chart-oil');
    if (!ctx) return;

    // Simulated daily oil price data Jan-Mar 2026
    const labels = [
      'Jan 1', 'Jan 8', 'Jan 15', 'Jan 22', 'Jan 29',
      'Feb 5', 'Feb 12', 'Feb 19', 'Feb 27',
      'Feb 28', 'Mar 1', 'Mar 2', 'Mar 3', 'Mar 4', 'Mar 5',
      'Mar 6', 'Mar 7', 'Mar 8', 'Mar 9', 'Mar 10'
    ];

    const brent = [
      74.2, 73.8, 72.1, 71.5, 72.8,
      73.1, 71.9, 72.6, 72.38,
      85.4, 88.7, 90.2, 91.8, 93.5, 94.1,
      96.3, 101.2, 100.8, 101.1, 101.5
    ];

    const wti = [
      71.8, 71.2, 69.8, 69.1, 70.5,
      70.9, 69.5, 70.3, 70.82,
      82.1, 85.9, 87.3, 88.7, 90.1, 91.5,
      93.8, 97.8, 97.2, 97.8, 98.2
    ];

    const defaults = WarTheater.Utils.chartDefaults();

    this.charts.oil = new Chart(ctx, {
      type: 'line',
      data: {
        labels,
        datasets: [
          {
            label: 'Brent Crude',
            data: brent,
            borderColor: '#d4782a',
            backgroundColor: 'rgba(212, 120, 42, 0.1)',
            borderWidth: 2,
            fill: true,
            tension: 0.3,
            pointRadius: 0,
            pointHitRadius: 8
          },
          {
            label: 'WTI Crude',
            data: wti,
            borderColor: '#8a8a8a',
            backgroundColor: 'rgba(138, 138, 138, 0.05)',
            borderWidth: 1.5,
            fill: true,
            tension: 0.3,
            pointRadius: 0,
            pointHitRadius: 8
          }
        ]
      },
      options: {
        ...defaults,
        plugins: {
          ...defaults.plugins,
          annotation: {
            annotations: {
              warStart: {
                type: 'line',
                xMin: 8,
                xMax: 8,
                borderColor: 'rgba(212, 120, 42, 0.5)',
                borderWidth: 1,
                borderDash: [4, 4]
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
              callback: (v) => '$' + v
            }
          }
        }
      }
    });
  },

  renderMarketsChart() {
    const ctx = document.getElementById('chart-markets');
    if (!ctx) return;

    const labels = ['Feb 27', 'Feb 28', 'Mar 1', 'Mar 2', 'Mar 3', 'Mar 4', 'Mar 5', 'Mar 6', 'Mar 7', 'Mar 8', 'Mar 9', 'Mar 10'];
    const defaults = WarTheater.Utils.chartDefaults();

    this.charts.markets = new Chart(ctx, {
      type: 'line',
      data: {
        labels,
        datasets: [
          {
            label: 'S&P 500',
            data: [100, 95.2, 93.8, 93.1, 92.5, 91.8, 91.7, 92.0, 91.2, 91.5, 91.6, 91.7],
            borderColor: '#ef4444',
            borderWidth: 2,
            tension: 0.3,
            pointRadius: 0
          },
          {
            label: 'Defense (RTX, LMT avg)',
            data: [100, 105.2, 107.8, 109.1, 110.5, 111.2, 112.0, 112.4, 113.1, 113.5, 113.8, 112.4],
            borderColor: '#22c55e',
            borderWidth: 1.5,
            tension: 0.3,
            pointRadius: 0
          },
          {
            label: 'Oil Majors (XOM, CVX avg)',
            data: [100, 108.1, 112.5, 114.2, 116.8, 118.1, 119.5, 121.2, 125.8, 124.9, 125.3, 124.7],
            borderColor: '#d4a020',
            borderWidth: 1.5,
            tension: 0.3,
            pointRadius: 0
          },
          {
            label: 'Airlines (DAL, UAL avg)',
            data: [100, 91.2, 87.5, 85.1, 83.2, 81.5, 79.8, 78.2, 76.5, 77.1, 77.8, 78.2],
            borderColor: '#7b3fa0',
            borderWidth: 1.5,
            tension: 0.3,
            pointRadius: 0
          }
        ]
      },
      options: {
        ...defaults,
        scales: {
          ...defaults.scales,
          y: {
            ...defaults.scales.y,
            min: 70,
            max: 130,
            ticks: {
              ...defaults.scales.y.ticks,
              callback: (v) => v
            }
          }
        }
      }
    });
  },

  renderHormuzChart() {
    const ctx = document.getElementById('chart-hormuz');
    if (!ctx) return;

    const labels = ['Feb 25', 'Feb 26', 'Feb 27', 'Feb 28', 'Mar 1', 'Mar 2', 'Mar 3', 'Mar 4', 'Mar 5', 'Mar 6', 'Mar 7', 'Mar 8', 'Mar 9', 'Mar 10'];
    const defaults = WarTheater.Utils.chartDefaults();

    this.charts.hormuz = new Chart(ctx, {
      type: 'bar',
      data: {
        labels,
        datasets: [{
          label: 'Daily Tanker Transits',
          data: [85, 84, 85, 42, 5, 3, 2, 2, 2, 3, 2, 2, 3, 2],
          backgroundColor: labels.map((_, i) => i < 3 ? 'rgba(212, 160, 32, 0.6)' : 'rgba(239, 68, 68, 0.6)'),
          borderColor: labels.map((_, i) => i < 3 ? '#d4a020' : '#ef4444'),
          borderWidth: 1
        }]
      },
      options: {
        ...defaults,
        plugins: {
          ...defaults.plugins,
          legend: { display: false }
        },
        scales: {
          ...defaults.scales,
          y: {
            ...defaults.scales.y,
            min: 0,
            max: 100,
            ticks: {
              ...defaults.scales.y.ticks,
              callback: (v) => v + ' ships'
            }
          }
        }
      }
    });
  },

  renderDailyCostChart() {
    const ctx = document.getElementById('chart-daily-cost');
    if (!ctx) return;

    const labels = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7', 'Day 8', 'Day 9', 'Day 10', 'Day 11'];
    // Estimated daily cost ramp-up (millions)
    const costs = [380, 420, 480, 500, 510, 490, 500, 520, 510, 505, 500];
    const cumulative = [];
    let sum = 0;
    costs.forEach(c => { sum += c; cumulative.push(sum); });

    const defaults = WarTheater.Utils.chartDefaults();

    this.charts.dailyCost = new Chart(ctx, {
      type: 'bar',
      data: {
        labels,
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
            label: 'Cumulative ($M)',
            data: cumulative,
            type: 'line',
            borderColor: '#ef4444',
            borderWidth: 2,
            tension: 0.3,
            pointRadius: 0,
            yAxisID: 'y1'
          }
        ]
      },
      options: {
        ...defaults,
        scales: {
          ...defaults.scales,
          y: {
            ...defaults.scales.y,
            position: 'left',
            ticks: {
              ...defaults.scales.y.ticks,
              callback: (v) => '$' + v + 'M'
            }
          },
          y1: {
            ...defaults.scales.y,
            position: 'right',
            grid: { drawOnChartArea: false },
            ticks: {
              ...defaults.scales.y.ticks,
              callback: (v) => '$' + (v / 1000).toFixed(1) + 'B'
            }
          }
        }
      }
    });
  }
};
