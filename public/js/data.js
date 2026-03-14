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

  // Strike data (filter out _metadata entry)
  async getStrikesIran() {
    const raw = await this.loadLocal('data/strikes-iran.json');
    if (Array.isArray(raw)) return raw.filter(s => s.id !== '_metadata');
    return raw;
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
      brent: { price: 103.86, change_pct: 46.3, baseline: 71.00 },
      wti: { price: 99.50, change_pct: 49.6, baseline: 66.50 },
      gas: { price: 3.95, change_pct: 32.6, baseline: 2.98 },
      sp500: { value: 6632.19, change_pct: -3.6, baseline: 6878.88 },
      daily_cost: 590000000,
      total_cost: 7600000000
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
