import { getCached, setCache, TTL } from '../lib/cache.js';

export async function handleMarkets(request, env, ctx) {
  const cached = await getCached(env, 'markets:snapshot', TTL.MARKETS);
  if (cached) {
    return new Response(JSON.stringify(cached), {
      headers: { 'Content-Type': 'application/json' }
    });
  }

  // Curated snapshot (would be replaced by live financial API)
  const snapshot = {
    timestamp: new Date().toISOString(),
    sp500: { value: 6694, change_pct: -2.5, baseline: 6867 },
    defense_stocks: {
      RTX: { price: 146.4, change_pct: 14.2 },
      LMT: { price: 542.4, change_pct: 11.8 },
      NOC: { price: 577.0, change_pct: 10.8 },
      GD: { price: 330.4, change_pct: 10.7 },
      BA: { price: 190.2, change_pct: 6.3 }
    },
    oil_stocks: {
      XOM: { price: 135.2, change_pct: 24.8 },
      CVX: { price: 189.0, change_pct: 23.9 },
      COP: { price: 140.3, change_pct: 24.8 }
    },
    airlines: {
      DAL: { price: 51.0, change_pct: -18.4 },
      UAL: { price: 76.6, change_pct: -22.0 },
      AAL: { price: 13.7, change_pct: -23.0 }
    },
    source: 'curated'
  };

  await setCache(env, 'markets:snapshot', snapshot);

  return new Response(JSON.stringify(snapshot), {
    headers: { 'Content-Type': 'application/json' }
  });
}
