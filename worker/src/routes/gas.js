import { getCached, setCache, TTL } from '../lib/cache.js';

export async function handleGas(request, env, ctx) {
  const cached = await getCached(env, 'gas:national', TTL.GAS);
  if (cached) {
    return new Response(JSON.stringify(cached), {
      headers: { 'Content-Type': 'application/json' }
    });
  }

  // Try FRED API for gas prices
  try {
    if (env.FRED_API_KEY) {
      const resp = await fetch(
        `https://api.stlouisfed.org/fred/series/observations?series_id=GASREGW&api_key=${env.FRED_API_KEY}&file_type=json&sort_order=desc&limit=30`
      );
      if (resp.ok) {
        const data = await resp.json();
        await setCache(env, 'gas:national', data);
        return new Response(JSON.stringify(data), {
          headers: { 'Content-Type': 'application/json' }
        });
      }
    }
  } catch (e) {
    // Fall through
  }

  const fallback = {
    timestamp: new Date().toISOString(),
    national_avg: 3.48,
    change_pct: 14.1,
    baseline: 3.05,
    unit: 'USD/gallon',
    source: 'curated'
  };

  return new Response(JSON.stringify(fallback), {
    headers: { 'Content-Type': 'application/json' }
  });
}
