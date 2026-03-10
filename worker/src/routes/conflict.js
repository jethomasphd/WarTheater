import { getCached, setCache, TTL } from '../lib/cache.js';

export async function handleConflict(request, env, ctx) {
  const cached = await getCached(env, 'conflict:latest', TTL.CONFLICT);
  if (cached) {
    return new Response(JSON.stringify(cached), {
      headers: { 'Content-Type': 'application/json' }
    });
  }

  // Try ACLED API
  try {
    if (env.ACLED_API_KEY) {
      const params = new URLSearchParams({
        key: env.ACLED_API_KEY,
        country: 'Iran',
        event_date: '2026-02-28|2026-12-31',
        event_date_where: 'BETWEEN',
        limit: 500
      });

      const resp = await fetch(`https://api.acleddata.com/acled/read?${params}`);
      if (resp.ok) {
        const data = await resp.json();
        await setCache(env, 'conflict:latest', data);
        return new Response(JSON.stringify(data), {
          headers: { 'Content-Type': 'application/json' }
        });
      }
    }
  } catch (e) {
    // Fall through
  }

  // Fallback summary
  const fallback = {
    timestamp: new Date().toISOString(),
    total_events: 3000,
    fatalities_reported: 1200,
    countries: ['Iran', 'Lebanon', 'Kuwait', 'Israel', 'Iraq'],
    source: 'curated',
    note: 'ACLED API not available — using curated estimates'
  };

  return new Response(JSON.stringify(fallback), {
    headers: { 'Content-Type': 'application/json' }
  });
}
