/* ═══════════════════════════════════════════════════════════════
   THE WAR THEATER — Data Layer
   Fetches from local JSON files + API proxy when available.
   ALL dashboard data lives in public/data/ JSON files.
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

  // ─── Data accessors ─────────────────────────────────────

  async getHeroStats() {
    return this.loadLocal('data/hero-stats.json');
  },

  async getStrikesIran() {
    const raw = await this.loadLocal('data/strikes-iran.json');
    if (Array.isArray(raw)) return raw.filter(s => s.id !== '_metadata');
    return raw;
  },

  async getStrikesRetaliation() {
    return this.loadLocal('data/strikes-retaliation.json');
  },

  async getCarriers() {
    return this.loadLocal('data/carriers.json');
  },

  async getHormuz() {
    return this.loadLocal('data/hormuz.json');
  },

  async getTimeline() {
    return this.fetchWithFallback('/timeline', 'data/timeline-events.json');
  },

  async getBaselines() {
    return this.loadLocal('data/baselines.json');
  },

  async getOilPrices() {
    return this.loadLocal('data/oil-prices.json');
  },

  async getMarkets() {
    return this.loadLocal('data/markets.json');
  },

  async getWarCosts() {
    return this.loadLocal('data/war-costs.json');
  },

  async getCasualties() {
    return this.loadLocal('data/casualties.json');
  },

  async getInfrastructure() {
    return this.loadLocal('data/infrastructure.json');
  },

  async getHistoricalComparison() {
    return this.loadLocal('data/historical-comparison.json');
  },

  async getGlobalBases() {
    return this.loadLocal('data/global-bases.json');
  },

  async getCalculator() {
    return this.loadLocal('data/calculator.json');
  },

  // AI Briefing
  async getBriefing() {
    return this.fetchWithFallback('/briefing', null);
  },

  // Load all initial data
  async loadAll() {
    const [
      heroStats, strikes, retaliation, carriers, hormuz,
      timeline, baselines, oilPrices, markets, warCosts,
      casualties, infrastructure, historicalComparison,
      globalBases, calculator
    ] = await Promise.all([
      this.getHeroStats(),
      this.getStrikesIran(),
      this.getStrikesRetaliation(),
      this.getCarriers(),
      this.getHormuz(),
      this.getTimeline(),
      this.getBaselines(),
      this.getOilPrices(),
      this.getMarkets(),
      this.getWarCosts(),
      this.getCasualties(),
      this.getInfrastructure(),
      this.getHistoricalComparison(),
      this.getGlobalBases(),
      this.getCalculator()
    ]);

    return {
      heroStats, strikes, retaliation, carriers, hormuz,
      timeline, baselines, oilPrices, markets, warCosts,
      casualties, infrastructure, historicalComparison,
      globalBases, calculator
    };
  }
};
