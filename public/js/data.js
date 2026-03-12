/* ═══════════════════════════════════════════════════════════════
   THE WAR THEATER — Data Layer
   Fetches from local JSON files + API proxy when available
   ═══════════════════════════════════════════════════════════════ */

WarTheater.Data = {
  cache: {},
  API_BASE: '/api',

  // Load local JSON data file
  async loadLocal(path) {
    if (this.cache[path]) return this.cache[path];
    try {
      const resp = await fetch(path);
      if (!resp.ok) throw new Error(`Failed to load ${path}: ${resp.status}`);
      const data = await resp.json();
      this.cache[path] = data;
      return data;
    } catch (e) {
      console.warn(`[Data] Failed to load ${path}:`, e.message);
      return null;
    }
  },

  // Attempt API call, fall back to local data
  async fetchWithFallback(apiPath, localPath) {
    try {
      const resp = await fetch(this.API_BASE + apiPath, {
        signal: AbortSignal.timeout(5000)
      });
      if (resp.ok) {
        const data = await resp.json();
        this.cache[apiPath] = data;
        return data;
      }
    } catch (e) {
      // API not available — fall back to local
    }
    if (localPath) return this.loadLocal(localPath);
    return null;
  },

  // Strike data
  async getStrikesIran() {
    return this.loadLocal('data/strikes-iran.json');
  },

  async getStrikesRetaliation() {
    return this.loadLocal('data/strikes-retaliation.json');
  },

  // Carrier data
  async getCarriers() {
    return this.loadLocal('data/carriers.json');
  },

  // Hormuz data
  async getHormuz() {
    return this.loadLocal('data/hormuz.json');
  },

  // Missile ranges
  async getMissileRanges() {
    return this.loadLocal('data/missile-ranges.json');
  },

  // Timeline events
  async getTimeline() {
    return this.fetchWithFallback('/timeline', 'data/timeline-events.json');
  },

  // Baselines
  async getBaselines() {
    return this.loadLocal('data/baselines.json');
  },

  // Financial data (from API or curated)
  async getFinancial() {
    const apiData = await this.fetchWithFallback('/oil', null);
    if (apiData) return apiData;

    // Return curated current snapshot
    return {
      timestamp: new Date().toISOString(),
      brent: { price: 100.11, change_pct: 38.3, baseline: 72.38 },
      wti: { price: 95.28, change_pct: 34.5, baseline: 70.82 },
      gas: { price: 3.72, change_pct: 22.0, baseline: 3.05 },
      sp500: { value: 6694, change_pct: -2.5, baseline: 6867 },
      daily_cost: 500000000,
      total_cost: 5000000000
    };
  },

  // AI Briefing
  async getBriefing() {
    return this.fetchWithFallback('/briefing', null);
  },

  // Load all initial data
  async loadAll() {
    const [strikes, retaliation, carriers, hormuz, timeline, baselines, financial] = await Promise.all([
      this.getStrikesIran(),
      this.getStrikesRetaliation(),
      this.getCarriers(),
      this.getHormuz(),
      this.getTimeline(),
      this.getBaselines(),
      this.getFinancial()
    ]);

    return { strikes, retaliation, carriers, hormuz, timeline, baselines, financial };
  }
};
