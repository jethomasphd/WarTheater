/* ═══════════════════════════════════════════════════════════════
   THE WAR THEATER — Utilities
   ═══════════════════════════════════════════════════════════════ */

const WarTheater = window.WarTheater || {};

WarTheater.Utils = {
  // Format numbers with commas
  formatNumber(n) {
    if (n == null) return '—';
    return n.toLocaleString('en-US');
  },

  // Format currency
  formatCurrency(n, decimals = 2) {
    if (n == null) return '—';
    return '$' + n.toFixed(decimals).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  },

  // Format large currency (billions/millions)
  formatLargeCurrency(n) {
    if (n >= 1e12) return '$' + (n / 1e12).toFixed(1) + 'T';
    if (n >= 1e9) return '$' + (n / 1e9).toFixed(1) + 'B';
    if (n >= 1e6) return '$' + (n / 1e6).toFixed(0) + 'M';
    return WarTheater.Utils.formatCurrency(n, 0);
  },

  // Format percentage change
  formatChange(pct, prefix) {
    if (pct == null) return '—';
    const sign = pct >= 0 ? '+' : '';
    const label = prefix ? prefix + ' ' : '';
    return label + sign + pct.toFixed(1) + '% since Feb 27';
  },

  // Animated counter
  animateCounter(element, target, duration = 2000) {
    const start = 0;
    const startTime = performance.now();

    function update(currentTime) {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      // Ease out cubic
      const eased = 1 - Math.pow(1 - progress, 3);
      const current = Math.floor(start + (target - start) * eased);
      element.textContent = WarTheater.Utils.formatNumber(current);
      if (progress < 1) {
        requestAnimationFrame(update);
      }
    }
    requestAnimationFrame(update);
  },

  // Day number since war start
  getWarDay(dateStr) {
    const warStart = new Date('2026-02-28');
    const date = dateStr ? new Date(dateStr) : new Date();
    const diff = Math.floor((date - warStart) / (1000 * 60 * 60 * 24));
    return diff + 1; // Day 1 = Feb 28
  },

  // Format date for display
  formatDate(dateStr) {
    const d = new Date(dateStr);
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    return months[d.getMonth()] + ' ' + d.getDate();
  },

  // Format full date
  formatDateFull(dateStr) {
    const d = new Date(dateStr);
    return d.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });
  },

  // Generate date range array
  dateRange(startStr, endStr) {
    const dates = [];
    const current = new Date(startStr);
    const end = new Date(endStr);
    while (current <= end) {
      dates.push(current.toISOString().split('T')[0]);
      current.setDate(current.getDate() + 1);
    }
    return dates;
  },

  // Debounce
  debounce(fn, delay) {
    let timer;
    return function (...args) {
      clearTimeout(timer);
      timer = setTimeout(() => fn.apply(this, args), delay);
    };
  },

  // Chart.js default dark theme options
  chartDefaults() {
    return {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          labels: {
            color: '#8a8a8a',
            font: { family: "'Barlow Condensed', sans-serif", size: 11 },
            boxWidth: 12,
            padding: 12
          }
        },
        tooltip: {
          backgroundColor: 'rgba(10,10,10,0.95)',
          borderColor: '#1a1a1a',
          borderWidth: 1,
          titleFont: { family: "'Barlow Condensed', sans-serif", size: 13, weight: '600' },
          bodyFont: { family: "'JetBrains Mono', monospace", size: 11 },
          titleColor: '#e0e0e0',
          bodyColor: '#8a8a8a',
          padding: 12,
          cornerRadius: 0
        }
      },
      scales: {
        x: {
          grid: { color: 'rgba(26,26,26,0.8)', lineWidth: 0.5 },
          ticks: {
            color: '#555555',
            font: { family: "'JetBrains Mono', monospace", size: 10 }
          },
          border: { color: '#1a1a1a' }
        },
        y: {
          grid: { color: 'rgba(26,26,26,0.8)', lineWidth: 0.5 },
          ticks: {
            color: '#555555',
            font: { family: "'JetBrains Mono', monospace", size: 10 }
          },
          border: { color: '#1a1a1a' }
        }
      }
    };
  },

  // Create vertical line annotation for war start
  warStartAnnotation() {
    return {
      type: 'line',
      xMin: 'Feb 28',
      xMax: 'Feb 28',
      borderColor: 'rgba(212, 120, 42, 0.5)',
      borderWidth: 1,
      borderDash: [4, 4],
      label: {
        display: true,
        content: 'WAR BEGINS',
        color: '#d4782a',
        font: { family: "'Barlow Condensed', sans-serif", size: 9, weight: '600' },
        position: 'start'
      }
    };
  }
};

window.WarTheater = WarTheater;
