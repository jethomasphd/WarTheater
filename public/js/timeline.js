/* ═══════════════════════════════════════════════════════════════
   THE WAR THEATER — Timeline Panel (The Record)
   Every event is sourced. Every date is a day of the war.
   ═══════════════════════════════════════════════════════════════ */

WarTheater.Timeline = {
  events: [],
  currentFilter: 'all',

  async init() {
    this.events = await WarTheater.Data.getTimeline() || [];
    // Handle API wrapper
    if (this.events.use_local) {
      this.events = await WarTheater.Data.loadLocal('data/timeline-events.json') || [];
    }
    this.render();
    this.bindFilters();
  },

  bindFilters() {
    var self = this;
    document.querySelectorAll('#timeline-filters .filter-btn').forEach(function(btn) {
      btn.addEventListener('click', function(e) {
        document.querySelectorAll('#timeline-filters .filter-btn').forEach(function(b) { b.classList.remove('active'); });
        e.target.classList.add('active');
        self.currentFilter = e.target.dataset.filter;
        self.render();
      });
    });
  },

  // Category descriptions for cognitive handholds
  getCategoryLabel(cat) {
    var labels = {
      military: 'MILITARY OPERATION',
      financial: 'FINANCIAL IMPACT',
      humanitarian: 'HUMANITARIAN',
      diplomatic: 'DIPLOMATIC',
      domestic: 'DOMESTIC / CIVIL'
    };
    return labels[cat] || cat.toUpperCase();
  },

  // Category colors
  getCategoryColor(cat) {
    var colors = {
      military: '#d4782a',
      financial: '#ef4444',
      humanitarian: '#f59e0b',
      diplomatic: '#4a9eff',
      domestic: '#7b3fa0'
    };
    return colors[cat] || '#8a8a8a';
  },

  render() {
    var container = document.getElementById('timeline-events');
    if (!container) return;
    var self = this;

    var filtered = this.currentFilter === 'all'
      ? this.events
      : this.events.filter(function(e) { return e.category === self.currentFilter; });

    if (filtered.length === 0) {
      container.innerHTML = '<div style="text-align: center; padding: var(--space-xl); color: var(--text-dim); font-style: italic;">No events in this category.</div>';
      return;
    }

    // Group by date for section headers
    var currentDate = null;

    container.innerHTML = filtered.map(function(event) {
      var dayNum = WarTheater.Utils.getWarDay(event.date);
      var catColor = self.getCategoryColor(event.category);
      var catLabel = self.getCategoryLabel(event.category);
      var dateHeader = '';

      // Add date separator when date changes
      if (event.date !== currentDate) {
        currentDate = event.date;
        dateHeader = '<div style="' +
          'padding: var(--space-lg) 0 var(--space-sm);' +
          'margin-top: var(--space-md);' +
          'border-top: 1px solid var(--border);' +
          'display: flex;' +
          'align-items: baseline;' +
          'gap: var(--space-md);' +
          '">' +
          '<span style="font-family: \'Barlow Condensed\', sans-serif; font-size: var(--text-lg); text-transform: uppercase; letter-spacing: 0.06em; color: var(--text-primary);">' +
          WarTheater.Utils.formatDateFull(event.date) +
          '</span>' +
          '<span style="font-family: \'JetBrains Mono\', monospace; font-size: var(--text-xs); color: var(--text-accent); letter-spacing: 0.08em;">DAY ' + dayNum + ' OF OPERATION EPIC FURY</span>' +
          '</div>';
      }

      return dateHeader +
        '<div class="timeline-event" data-category="' + event.category + '" data-date="' + event.date + '">' +

          // Date column
          '<div class="event-date">' +
            '<div>' + WarTheater.Utils.formatDate(event.date) + '</div>' +
            '<div style="color: var(--text-accent); font-size: 9px; font-weight: 600;">DAY ' + dayNum + '</div>' +
            (event.time ? '<div style="font-size: 9px; margin-top: 2px;">' + event.time + ' UTC</div>' : '') +
          '</div>' +

          // Marker
          '<div class="event-marker marker-' + event.category + '" style="position: relative;">' +
            '<div style="position: absolute; top: -3px; left: -3px; width: 16px; height: 16px; border-radius: 50%; background: ' + catColor + '; opacity: 0.15;"></div>' +
          '</div>' +

          // Content
          '<div class="event-content">' +

            // Category tag
            '<div style="margin-bottom: 6px;">' +
              '<span class="event-tag ' + event.category + '">' + catLabel + '</span>' +
            '</div>' +

            // Title
            '<div class="event-title" style="color: ' + catColor + ';">' + event.title + '</div>' +

            // Description
            '<div class="event-desc">' + event.description + '</div>' +

            // Data point callout (if present)
            (event.data_point ?
              '<div style="' +
                'background: rgba(26,26,26,0.8);' +
                'border-left: 2px solid ' + catColor + ';' +
                'padding: 6px 10px;' +
                'margin: 8px 0;' +
                'font-family: \'JetBrains Mono\', monospace;' +
                'font-size: var(--text-xs);' +
                'color: ' + catColor + ';' +
                '">' + event.data_point + '</div>'
              : '') +

            // Meta: source
            '<div class="event-meta" style="margin-top: 8px;">' +
              (event.source ?
                '<span style="font-family: \'JetBrains Mono\', monospace; font-size: 10px; color: var(--text-dim);">Source: ' + event.source + '</span>'
                : '') +
            '</div>' +

          '</div>' +
        '</div>';
    }).join('');
  }
};
