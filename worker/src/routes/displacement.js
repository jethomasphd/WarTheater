import { getCached, setCache, TTL } from '../lib/cache.js';

export async function handleDisplacement(request, env, ctx) {
  const cached = await getCached(env, 'displacement:latest', TTL.DISPLACEMENT);
  if (cached) {
    return new Response(JSON.stringify(cached), {
      headers: { 'Content-Type': 'application/json' }
    });
  }

  // UNHCR API attempt
  try {
    const resp = await fetch('https://data.unhcr.org/api/population/?country_of_origin=LBN&year=2026');
    if (resp.ok) {
      const data = await resp.json();
      await setCache(env, 'displacement:latest', data);
      return new Response(JSON.stringify(data), {
        headers: { 'Content-Type': 'application/json' }
      });
    }
  } catch (e) {
    // Fall through
  }

  const fallback = {
    timestamp: new Date().toISOString(),
    lebanon_displaced: 450000,
    iran_internal_displaced: null,
    sources: ['UNHCR', 'OCHA'],
    source: 'curated'
  };

  return new Response(JSON.stringify(fallback), {
    headers: { 'Content-Type': 'application/json' }
  });
}
