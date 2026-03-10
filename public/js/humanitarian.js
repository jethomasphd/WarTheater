/* ═══════════════════════════════════════════════════════════════
   THE WAR THEATER — Humanitarian Panel
   ═══════════════════════════════════════════════════════════════ */

WarTheater.Humanitarian = {
  charts: {},

  init() {
    this.renderCasualtiesChart();
    this.renderInfrastructureGrid();
    this.renderHistoricalComparison();
  },

  // Animate all counter elements
  animateCounters() {
    const counters = document.querySelectorAll('.counter');
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const el = entry.target;
          const target = parseInt(el.dataset.target, 10);
          if (target && !el.dataset.animated) {
            el.dataset.animated = 'true';
            WarTheater.Utils.animateCounter(el, target, 2500);
          }
        }
      });
    }, { threshold: 0.3 });

    counters.forEach(c => observer.observe(c));
  },

  renderCasualtiesChart() {
    const ctx = document.getElementById('chart-casualties');
    if (!ctx) return;

    const labels = ['Feb 28', 'Mar 1', 'Mar 2', 'Mar 3', 'Mar 4', 'Mar 5', 'Mar 6', 'Mar 7', 'Mar 8', 'Mar 9', 'Mar 10'];
    const defaults = WarTheater.Utils.chartDefaults();

    this.charts.casualties = new Chart(ctx, {
      type: 'bar',
      data: {
        labels,
        datasets: [
          {
            label: 'Iranian (Military)',
            data: [80, 120, 150, 130, 110, 100, 90, 140, 120, 80, 80],
            backgroundColor: 'rgba(184, 28, 28, 0.6)',
            borderColor: '#b81c1c',
            borderWidth: 1,
            stack: 'casualties'
          },
          {
            label: 'Iranian (Civilian)',
            data: [5, 10, 15, 12, 35, 20, 15, 25, 18, 10, 8],
            backgroundColor: 'rgba(255, 255, 255, 0.4)',
            borderColor: '#ffffff',
            borderWidth: 1,
            stack: 'casualties'
          },
          {
            label: 'US Military',
            data: [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            backgroundColor: 'rgba(74, 158, 255, 0.6)',
            borderColor: '#4a9eff',
            borderWidth: 1,
            stack: 'casualties'
          },
          {
            label: 'Lebanese',
            data: [0, 0, 40, 55, 60, 65, 58, 72, 55, 45, 36],
            backgroundColor: 'rgba(123, 63, 160, 0.6)',
            borderColor: '#7b3fa0',
            borderWidth: 1,
            stack: 'casualties'
          }
        ]
      },
      options: {
        ...defaults,
        scales: {
          ...defaults.scales,
          x: { ...defaults.scales.x, stacked: true },
          y: {
            ...defaults.scales.y,
            stacked: true,
            ticks: {
              ...defaults.scales.y.ticks,
              callback: (v) => v + ' est.'
            }
          }
        }
      }
    });
  },

  renderInfrastructureGrid() {
    const grid = document.getElementById('infrastructure-grid');
    if (!grid) return;

    const items = [
      { icon: '🏥', label: 'Hospitals Damaged', count: '3+', note: 'Southern Lebanon' },
      { icon: '🏫', label: 'Schools Destroyed', count: '1', note: 'Minab girls\' school' },
      { icon: '⚡', label: 'Power Plants Hit', count: '4+', note: 'Iran grid disruption' },
      { icon: '🛢️', label: 'Oil Facilities Hit', count: '3', note: 'Kharg, Abadan + more' },
      { icon: '✈️', label: 'Airports Damaged', count: '5+', note: 'Iran + region' },
      { icon: '🌉', label: 'Bridges Destroyed', count: '8+', note: 'Western Iran' }
    ];

    grid.innerHTML = items.map(item => `
      <div style="text-align: center; padding: var(--space-md);">
        <div style="font-size: 2rem; margin-bottom: var(--space-sm);" aria-hidden="true">${item.icon}</div>
        <div class="font-data" style="font-size: var(--text-xl); color: var(--humanitarian);">${item.count}</div>
        <div style="font-family: 'Barlow Condensed', sans-serif; font-size: var(--text-xs); text-transform: uppercase; letter-spacing: 0.06em; color: var(--text-secondary); margin-top: 4px;">${item.label}</div>
        <div style="font-size: 10px; color: var(--text-dim); margin-top: 2px;">${item.note}</div>
      </div>
    `).join('');
  },

  renderHistoricalComparison() {
    const ctx = document.getElementById('chart-historical');
    if (!ctx) return;

    const defaults = WarTheater.Utils.chartDefaults();

    this.charts.historical = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['Iran 2026\n(Day 11)', 'Iraq 2003\n(Day 11)', 'Libya 2011\n(Day 11)', 'Gulf War 1991\n(Day 11)'],
        datasets: [
          {
            label: 'Total Strikes',
            data: [3000, 12000, 400, 18000],
            backgroundColor: 'rgba(212, 120, 42, 0.5)',
            borderColor: '#d4782a',
            borderWidth: 1
          },
          {
            label: 'US KIA',
            data: [6, 65, 0, 15],
            backgroundColor: 'rgba(74, 158, 255, 0.5)',
            borderColor: '#4a9eff',
            borderWidth: 1
          },
          {
            label: 'Est. Daily Cost ($M)',
            data: [500, 720, 120, 600],
            backgroundColor: 'rgba(239, 68, 68, 0.5)',
            borderColor: '#ef4444',
            borderWidth: 1
          }
        ]
      },
      options: {
        ...defaults,
        indexAxis: 'y',
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
