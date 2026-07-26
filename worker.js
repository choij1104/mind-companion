/**
 * Mind Companion — API relay (Cloudflare Worker)
 * ------------------------------------------------------------------
 * Keeps the Anthropic API key on the server so it never appears in the
 * published web app. The app calls this Worker; the Worker calls Anthropic.
 *
 * Setup (see README):
 *   1. Create a Worker at dash.cloudflare.com
 *   2. Paste this file in
 *   3. Settings -> Variables -> add a SECRET named ANTHROPIC_API_KEY
 *   4. Optional: add a plain variable ALLOWED_ORIGIN with your site address,
 *      e.g. https://choij1104.github.io
 *   5. Deploy, then paste the Worker address into the app's Settings screen
 */

const MODEL = 'claude-sonnet-4-6';
const MAX_TOKENS = 400;
const MAX_BODY_BYTES = 24000;   // refuse oversized payloads
const MAX_MESSAGES = 14;        // refuse runaway histories

export default {
  async fetch(request, env) {
    const origin = request.headers.get('Origin') || '';
    const allowed = env.ALLOWED_ORIGIN || '*';
    const cors = {
      'Access-Control-Allow-Origin': allowed === '*' ? '*' : allowed,
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Max-Age': '86400',
      'Vary': 'Origin'
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: cors });
    }

    // health check so the app can verify the address
    if (request.method === 'GET') {
      return json({ ok: true, service: 'mind-companion-relay' }, 200, cors);
    }

    if (request.method !== 'POST') {
      return json({ error: 'method_not_allowed' }, 405, cors);
    }

    if (allowed !== '*' && origin && origin !== allowed) {
      return json({ error: 'origin_not_allowed' }, 403, cors);
    }

    if (!env.ANTHROPIC_API_KEY) {
      return json({ error: 'missing_api_key' }, 500, cors);
    }

    let body;
    try {
      const raw = await request.text();
      if (raw.length > MAX_BODY_BYTES) {
        return json({ error: 'payload_too_large' }, 413, cors);
      }
      body = JSON.parse(raw);
    } catch {
      return json({ error: 'bad_request' }, 400, cors);
    }

    const messages = Array.isArray(body.messages) ? body.messages : null;
    if (!messages || !messages.length || messages.length > MAX_MESSAGES) {
      return json({ error: 'bad_messages' }, 400, cors);
    }

    // only the fields we allow through — the client cannot pick the model
    const payload = {
      model: MODEL,
      max_tokens: MAX_TOKENS,
      system: typeof body.system === 'string' ? body.system.slice(0, 6000) : undefined,
      messages: messages.map(m => ({
        role: m.role === 'assistant' ? 'assistant' : 'user',
        content: String(m.content || '').slice(0, 4000)
      }))
    };

    try {
      const res = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': env.ANTHROPIC_API_KEY,
          'anthropic-version': '2023-06-01'
        },
        body: JSON.stringify(payload)
      });

      const data = await res.json();

      if (!res.ok) {
        return json({ error: 'upstream_error', status: res.status }, 502, cors);
      }

      const text = (data.content || [])
        .filter(b => b.type === 'text')
        .map(b => b.text)
        .join('\n')
        .trim();

      return json({ text }, 200, cors);
    } catch {
      return json({ error: 'network_error' }, 502, cors);
    }
  }
};

function json(obj, status, cors) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { 'Content-Type': 'application/json', ...cors }
  });
}
