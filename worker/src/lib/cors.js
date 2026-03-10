/* CORS Middleware */

export function corsHeaders(env) {
  const allowed = env.ALLOWED_ORIGINS || 'https://wartheater.org,http://localhost:8788';
  return {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '86400'
  };
}

export function handleCORS(request, env) {
  return new Response(null, {
    status: 204,
    headers: corsHeaders(env)
  });
}
