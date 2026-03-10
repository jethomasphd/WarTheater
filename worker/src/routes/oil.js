import { getCached, setCache, TTL } from '../lib/cache.js';

export async function handleOil(request, env, ctx) {
  // Check cache
  const cached = await getCached(env, 'oil:latest', TTL.OIL);
  if (cached) {
    return new Response(JSON.stringify(cached), {
      headers: { 'Content-Type': 'application/json' }
    });
  }

  // Try external API
  try {
    if (env.OIL_API_KEY) {
      const resp = await fetch(`https://api.oilpriceapi.com/v1/prices/latest`, {
        headers: { 'Authorization': `Token ${env.OIL_API_KEY}` }
      });
      if (resp.ok) {
        const data = await resp.json();
        await setCache(env, 'oil:latest', data);
        return new Response(JSON.stringify(data), {
          headers: { 'Content-Type': 'application/json' }
        });
      }
    }
  } catch (e) {
    // Fall through to static data
  }

  // Fallback: curated current data
  const fallback = {
    timestamp: new Date().toISOString(),
    brent: { price: 101.50, change_pct: 40.2, baseline: 72.38 },
    wti: { price: 98.20, change_pct: 38.7, baseline: 70.82 },
    source: 'curated'
  };

  return new Response(JSON.stringify(fallback), {
    headers: { 'Content-Type': 'application/json' }
  });
}
