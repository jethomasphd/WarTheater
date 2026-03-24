/* ═══════════════════════════════════════════════════════════════
   THE WAR THEATER — Briefing Panel
   Dynamically loads the latest briefing from data/briefings/
   ═══════════════════════════════════════════════════════════════ */

WarTheater.Briefing = {
  async init() {
    var container = document.getElementById('briefing-content');
    if (!container) {
      console.warn('[Briefing] No #briefing-content container found');
      return;
    }

    try {
      var resp = await fetch('data/briefings/index.json');
      if (!resp.ok) throw new Error('HTTP ' + resp.status);
      var index = await resp.json();

      // Find the latest briefing (highest day number)
      index.sort(function(a, b) { return b.day - a.day; });
      var latest = index[0];
      if (!latest) throw new Error('Empty briefing index');

      // Fetch the briefing HTML fragment
      var htmlResp = await fetch(latest.file);
      if (!htmlResp.ok) throw new Error('HTTP ' + htmlResp.status + ' loading ' + latest.file);
      var html = await htmlResp.text();

      // Inject the briefing content, preserving the archive CTA
      container.innerHTML = html +
        '<div class="briefing-archive-cta">' +
          '<div class="briefing-archive-cta-rule"></div>' +
          '<p class="briefing-archive-cta-label">Previous briefings are preserved in the archive</p>' +
          '<a href="archive.html" class="briefing-archive-btn">Enter The Archive &#9654;</a>' +
        '</div>';

      console.log('[Briefing] Loaded Day ' + latest.day + ' briefing');
    } catch (err) {
      console.error('[Briefing] Failed to load latest briefing:', err);
      // Leave whatever static content exists as fallback
    }
  }
};
