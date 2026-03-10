/* ═══════════════════════════════════════════════════════════════
   THE WAR THEATER — Cloudflare Worker
   API proxy, data aggregation, AI briefing engine
   ═══════════════════════════════════════════════════════════════ */

import { handleOil } from './routes/oil.js';
import { handleConflict } from './routes/conflict.js';
import { handleDisplacement } from './routes/displacement.js';
import { handleMarkets } from './routes/markets.js';
import { handleBriefing } from './routes/briefing.js';
import { handleGas } from './routes/gas.js';
import { handleTimeline } from './routes/timeline.js';
import { corsHeaders, handleCORS } from './lib/cors.js';

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;

    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
      return handleCORS(request, env);
    }

    // Route matching
    try {
      let response;

      if (path === '/api/oil') {
        response = await handleOil(request, env, ctx);
      } else if (path === '/api/conflict') {
        response = await handleConflict(request, env, ctx);
      } else if (path === '/api/displacement') {
        response = await handleDisplacement(request, env, ctx);
      } else if (path === '/api/markets') {
        response = await handleMarkets(request, env, ctx);
      } else if (path === '/api/briefing') {
        response = await handleBriefing(request, env, ctx);
      } else if (path === '/api/gas-prices') {
        response = await handleGas(request, env, ctx);
      } else if (path === '/api/timeline') {
        response = await handleTimeline(request, env, ctx);
      } else {
        response = new Response(JSON.stringify({ error: 'Not found' }), {
          status: 404,
          headers: { 'Content-Type': 'application/json' }
        });
      }

      // Add CORS headers
      const headers = new Headers(response.headers);
      Object.entries(corsHeaders(env)).forEach(([k, v]) => headers.set(k, v));

      return new Response(response.body, {
        status: response.status,
        headers
      });
    } catch (err) {
      return new Response(JSON.stringify({ error: 'Internal server error', message: err.message }), {
        status: 500,
        headers: {
          'Content-Type': 'application/json',
          ...corsHeaders(env)
        }
      });
    }
  }
};
