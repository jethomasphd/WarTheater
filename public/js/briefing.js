/* ═══════════════════════════════════════════════════════════════
   THE WAR THEATER — Briefing Panel
   Fetches AI-generated daily briefing from API or uses embedded
   ═══════════════════════════════════════════════════════════════ */

WarTheater.Briefing = {
  init() {
    this.loadBriefing();
  },

  async loadBriefing() {
    // Try to fetch live briefing from API
    const data = await WarTheater.Data.getBriefing();
    if (data && data.html) {
      const container = document.getElementById('briefing-content');
      if (container) {
        container.innerHTML = data.html;
      }
    }
    // Otherwise, the embedded HTML briefing in index.html serves as default
  }
};
