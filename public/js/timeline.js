/* ═══════════════════════════════════════════════════════════════
   THE WAR THEATER — Timeline Panel
   ═══════════════════════════════════════════════════════════════ */

WarTheater.Timeline = {
  events: [],
  currentFilter: 'all',

  async init() {
    this.events = await WarTheater.Data.getTimeline() || [];
    this.render();
    this.bindFilters();
  },

  bindFilters() {
    document.querySelectorAll('#timeline-filters .filter-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        document.querySelectorAll('#timeline-filters .filter-btn').forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');
        this.currentFilter = e.target.dataset.filter;
        this.render();
      });
    });
  },

  render() {
    const container = document.getElementById('timeline-events');
    if (!container) return;

    const filtered = this.currentFilter === 'all'
      ? this.events
      : this.events.filter(e => e.category === this.currentFilter);

    container.innerHTML = filtered.map(event => {
      const dayNum = WarTheater.Utils.getWarDay(event.date);
      return `
        <div class="timeline-event" data-category="${event.category}">
          <div class="event-date">
            <div>${WarTheater.Utils.formatDate(event.date)}</div>
            <div style="color: var(--text-accent); font-size: 9px;">DAY ${dayNum}</div>
            ${event.time ? `<div style="font-size: 9px;">${event.time}</div>` : ''}
          </div>
          <div class="event-marker marker-${event.category}"></div>
          <div class="event-content">
            <div class="event-title">${event.title}</div>
            <div class="event-desc">${event.description}</div>
            <div class="event-meta">
              <span class="event-tag ${event.category}">${event.category}</span>
              ${event.data_point ? `<span style="color: var(--text-accent);">${event.data_point}</span>` : ''}
              ${event.source ? `<span>Source: ${event.source}</span>` : ''}
            </div>
          </div>
        </div>
      `;
    }).join('');
  }
};
