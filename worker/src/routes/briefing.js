import { getCached, setCache, TTL } from '../lib/cache.js';
import { generateBriefing } from '../lib/claude.js';

export async function handleBriefing(request, env, ctx) {
  const today = new Date().toISOString().split('T')[0];
  const cacheKey = `briefing:${today}`;

  // Check cache
  const cached = await getCached(env, cacheKey, TTL.BRIEFING);
  if (cached) {
    return new Response(JSON.stringify(cached), {
      headers: { 'Content-Type': 'application/json' }
    });
  }

  // Generate new briefing
  try {
    const contextData = {
      brent: '100.11',
      brentChange: '+38.3',
      wti: '95.28',
      wtiChange: '+34.5',
      gas: '3.72',
      gasChange: '+22.0',
      sp500: '6,694',
      sp500Change: '-2.5',
      headlines: [
        'Mojtaba Khamenei named Supreme Leader, vows resistance',
        'US strikes on Kharg Island oil terminal continue',
        'Hezbollah rocket attacks intensify on northern Israel',
        'SPR release authorized: 30M barrels over 60 days',
        'Gas prices at $3.48/gal, up 14.1% from pre-war'
      ].join('\n'),
      conflict: {
        total_strikes: 3000,
        us_kia: 6,
        us_wia: 10,
        iranian_casualties_est: 1200,
        lebanese_casualties: 486,
        displaced_lebanon: 450000
      }
    };

    const briefing = await generateBriefing(env, contextData);
    await setCache(env, cacheKey, briefing);

    return new Response(JSON.stringify(briefing), {
      headers: { 'Content-Type': 'application/json' }
    });
  } catch (e) {
    // Return error but don't crash
    return new Response(JSON.stringify({
      error: 'Briefing generation failed',
      message: e.message,
      fallback: true
    }), {
      status: 503,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}
