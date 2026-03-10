/* Anthropic API Client for Cloudflare Workers */

export async function generateBriefing(env, contextData) {
  const apiKey = env.ANTHROPIC_API_KEY;
  if (!apiKey) {
    throw new Error('ANTHROPIC_API_KEY not configured');
  }

  const today = new Date().toISOString().split('T')[0];

  const prompt = `You are an intelligence analyst preparing a daily briefing on the 2026 Iran War for public consumption. You are precise, factual, and unflinching. You do not editorialize. You present the data and its implications.

Today is ${today}. Here is the latest data:

CONFLICT DATA:
${JSON.stringify(contextData.conflict || {}, null, 2)}

FINANCIAL DATA:
- Brent crude: $${contextData.brent || '—'} (${contextData.brentChange || '—'}% since Feb 27)
- WTI crude: $${contextData.wti || '—'} (${contextData.wtiChange || '—'}% since Feb 27)
- US gas avg: $${contextData.gas || '—'}/gal (${contextData.gasChange || '—'}% since Feb 27)
- S&P 500: ${contextData.sp500 || '—'} (${contextData.sp500Change || '—'}% since Feb 27)

LATEST DEVELOPMENTS:
${contextData.headlines || 'No headlines available.'}

Generate a structured intelligence briefing with these sections:
1. SITUATION SUMMARY (3 paragraphs, plain language)
2. KEY DEVELOPMENTS (5-7 bullet points)
3. FINANCIAL OUTLOOK (2 paragraphs)
4. HUMANITARIAN UPDATE (2 paragraphs)
5. WHAT TO WATCH (3-5 forward-looking items)

Be direct. Be precise. Let the data speak.

Return the briefing as HTML using these CSS classes: briefing-section for each section wrapper, h3 for section titles, p for paragraphs, ul/li for bullet lists.`;

  const response = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': apiKey,
      'anthropic-version': '2023-06-01'
    },
    body: JSON.stringify({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 4096,
      messages: [{
        role: 'user',
        content: prompt
      }]
    })
  });

  if (!response.ok) {
    const err = await response.text();
    throw new Error(`Anthropic API error: ${response.status} — ${err}`);
  }

  const result = await response.json();
  const text = result.content[0].text;

  return {
    html: text,
    generated_at: new Date().toISOString(),
    model: 'claude-sonnet-4-20250514'
  };
}
