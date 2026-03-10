/* KV Cache Helpers */

export async function getCached(env, key, ttlSeconds) {
  if (!env.THEATER_CACHE) return null;

  try {
    const raw = await env.THEATER_CACHE.get(key);
    if (!raw) return null;

    const data = JSON.parse(raw);
    const age = (Date.now() - data._cached_at) / 1000;

    if (age > ttlSeconds) return null; // Stale
    return data;
  } catch {
    return null;
  }
}

export async function setCache(env, key, data) {
  if (!env.THEATER_CACHE) return;

  try {
    const payload = { ...data, _cached_at: Date.now() };
    await env.THEATER_CACHE.put(key, JSON.stringify(payload));
  } catch (e) {
    console.error('Cache write failed:', e.message);
  }
}

// TTL constants (seconds)
export const TTL = {
  OIL: 15 * 60,          // 15 minutes
  CONFLICT: 60 * 60,     // 1 hour
  DISPLACEMENT: 6 * 60 * 60, // 6 hours
  MARKETS: 15 * 60,      // 15 minutes
  BRIEFING: 12 * 60 * 60, // 12 hours
  GAS: 60 * 60,          // 1 hour
  TIMELINE: 60 * 60      // 1 hour
};
