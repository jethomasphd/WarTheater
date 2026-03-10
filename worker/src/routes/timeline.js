import { getCached, setCache, TTL } from '../lib/cache.js';

export async function handleTimeline(request, env, ctx) {
  const cached = await getCached(env, 'timeline:events', TTL.TIMELINE);
  if (cached) {
    return new Response(JSON.stringify(cached), {
      headers: { 'Content-Type': 'application/json' }
    });
  }

  // Timeline is primarily served from static data/timeline-events.json
  // This route exists to merge curated + ACLED-enriched events
  // For now, return signal to use local data
  return new Response(JSON.stringify({ use_local: true }), {
    status: 204,
    headers: { 'Content-Type': 'application/json' }
  });
}
