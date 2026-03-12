/* ═══════════════════════════════════════════════════════════════
   THE WAR THEATER — Briefing Panel
   Supports historical briefing navigation via archived HTML files
   ═══════════════════════════════════════════════════════════════ */

WarTheater.Briefing = {
  index: [],
  currentIdx: -1,
  cache: {},

  async init() {
    await this.loadIndex();
    this.bindNav();
  },

  async loadIndex() {
    try {
      var resp = await fetch('data/briefings/index.json');
      if (resp.ok) {
        this.index = await resp.json();
        // Start on the latest briefing
        this.currentIdx = this.index.length - 1;
        // Cache the current embedded briefing so we don't re-fetch it
        var container = document.getElementById('briefing-content');
        if (container && this.index.length > 0) {
          var latestEntry = this.index[this.index.length - 1];
          this.cache[latestEntry.file] = container.innerHTML;
        }
        this.updateNav();
      }
    } catch (e) {
      console.warn('[Briefing] Could not load briefing index:', e.message);
    }
  },

  bindNav() {
    var self = this;
    var prevBtn = document.getElementById('briefing-prev');
    var nextBtn = document.getElementById('briefing-next');

    if (prevBtn) {
      prevBtn.addEventListener('click', function() {
        if (self.currentIdx > 0) {
          self.currentIdx--;
          self.loadBriefing(self.currentIdx);
        }
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener('click', function() {
        if (self.currentIdx < self.index.length - 1) {
          self.currentIdx++;
          self.loadBriefing(self.currentIdx);
        }
      });
    }
  },

  async loadBriefing(idx) {
    var entry = this.index[idx];
    if (!entry) return;

    var container = document.getElementById('briefing-content');
    if (!container) return;

    // Check cache first
    if (this.cache[entry.file]) {
      container.innerHTML = this.cache[entry.file];
      this.updateNav();
      return;
    }

    try {
      var resp = await fetch(entry.file);
      if (resp.ok) {
        var html = await resp.text();
        this.cache[entry.file] = html;
        container.innerHTML = html;
      }
    } catch (e) {
      console.warn('[Briefing] Failed to load', entry.file, e.message);
    }

    this.updateNav();
  },

  updateNav() {
    var prevBtn = document.getElementById('briefing-prev');
    var nextBtn = document.getElementById('briefing-next');
    var indicator = document.getElementById('briefing-nav-indicator');

    if (prevBtn) {
      prevBtn.disabled = this.currentIdx <= 0;
      if (this.currentIdx > 0) {
        prevBtn.title = this.index[this.currentIdx - 1].label;
      } else {
        prevBtn.title = '';
      }
    }

    if (nextBtn) {
      var isLatest = this.currentIdx >= this.index.length - 1;
      nextBtn.disabled = isLatest;
      if (!isLatest) {
        nextBtn.title = this.index[this.currentIdx + 1].label;
      } else {
        nextBtn.title = '';
      }
    }

    if (indicator && this.index.length > 0) {
      var entry = this.index[this.currentIdx];
      var isLatest = this.currentIdx >= this.index.length - 1;
      indicator.textContent = isLatest ? entry.label + '  (LATEST)' : entry.label + '  (ARCHIVED)';
      indicator.style.color = isLatest ? 'var(--text-secondary)' : 'var(--text-dim)';
    }
  }
};
