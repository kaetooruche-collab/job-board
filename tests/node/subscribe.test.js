'use strict';
const test = require('node:test');
const assert = require('node:assert');
const { createHandler, loadKey } = require('../../api/subscribe.js');

const KEY = 'xkeysib-' + 'a'.repeat(30);
const ORIGIN = 'https://yirehcareers.vercel.app';

function harness(contact, opts) {
  opts = opts || {};
  const calls = [];
  const fetchImpl = async (url, init) => {
    const path = url.replace('https://api.brevo.com/v3', '');
    const body = init.body ? JSON.parse(init.body) : undefined;
    calls.push({ method: init.method, path, body, headers: init.headers });
    let status = 200, data = {};
    if (init.method === 'GET') { if (contact) data = contact; else status = 404; }
    else if (path === '/contacts' && init.method === 'POST') { status = opts.dup ? 400 : 201; data = opts.dup ? { code: 'duplicate_parameter' } : { id: 9 }; }
    else if (init.method === 'PUT') { opts.putCalls = (opts.putCalls || 0) + 1; status = (opts.putFailFirst && opts.putCalls === 1) ? 400 : 204; }
    else if (path === '/smtp/email') status = opts.mailFails ? 500 : 201;
    if (opts.writeFails && init.method !== 'GET' && path !== '/smtp/email') status = 500;
    return { status, json: async () => data };
  };
  const logs = [];
  const orig = console.log; console.log = (...a) => logs.push(a.join(' '));
  const handler = createHandler({ sleep: async () => {}, fetchImpl, env: { BREVO_API_KEY: KEY }, now: () => new Date('2026-10-24T10:00:00Z'), limiter: opts.limiter });
  async function post(payload, o) {
    o = o || {};
    const res = { headers: {}, setHeader(k, v) { this.headers[k] = v; }, end(b) { this.body = JSON.parse(b); } };
    await handler({ method: o.method || 'POST', headers: { origin: o.origin === undefined ? ORIGIN : o.origin, 'x-forwarded-for': o.ip || '1.2.3.4' }, body: payload }, res);
    return res;
  }
  return { post, calls, logs, restore: () => { console.log = orig; } };
}

test('rejects wrong method and wrong origin without calling Brevo', async () => {
  const h = harness(null);
  assert.strictEqual((await h.post({}, { method: 'GET' })).statusCode, 405);
  assert.strictEqual((await h.post({ form: 'signup', email: 'a@b.co' }, { origin: 'https://evil.example' })).statusCode, 403);
  assert.strictEqual((await h.post({ form: 'signup', email: 'a@b.co' }, { origin: '' })).statusCode, 403);
  h.restore(); assert.strictEqual(h.calls.length, 0);
});

test('honeypot gets a quiet success and no Brevo call', async () => {
  const h = harness(null);
  const r = await h.post({ form: 'signup', email: 'bot@x.com', website: 'http://spam' });
  h.restore(); assert.strictEqual(r.statusCode, 200); assert.strictEqual(h.calls.length, 0);
});

test('new signup: creates contact on Job alerts with consent evidence, no tips', async () => {
  const h = harness(null);
  const r = await h.post({ form: 'signup', email: 'New@Example.com', firstName: 'Amara', level: 'early' });
  h.restore();
  assert.strictEqual(r.statusCode, 200); assert.strictEqual(r.body.ok, true);
  const w = h.calls.find(c => c.method === 'POST' && c.path === '/contacts');
  assert.strictEqual(w.body.email, 'new@example.com');
  assert.deepStrictEqual(w.body.listIds, [11]);
  assert.strictEqual(w.body.attributes.CONSENT_JOBS_AT, '2026-10-24');
  assert.strictEqual(w.body.attributes.CONSENT_JOBS_SRC, 'signup-v1');
  assert.strictEqual(w.body.attributes.LEVEL_INTEREST, 'early');
  assert.strictEqual(w.body.attributes.CONSENT_TIPS_AT, undefined);
  assert.strictEqual(w.body.updateEnabled, false);
});

test('signup with the tips box adds Career tips and records tips consent', async () => {
  const h = harness(null);
  await h.post({ form: 'signup', email: 'a@b.co', tips: true });
  h.restore();
  const w = h.calls.find(c => c.path === '/contacts' && c.method === 'POST');
  assert.deepStrictEqual(w.body.listIds, [11, 18]);
  assert.strictEqual(w.body.attributes.CONSENT_TIPS_AT, '2026-10-24');
  assert.strictEqual(w.body.attributes.CONSENT_TIPS_SRC, 'signup-v1');
});

test('existing contact keeps its original consent evidence', async () => {
  const h = harness({ emailBlacklisted: false, attributes: { CONSENT_JOBS_AT: '2026-09-01', CONSENT_JOBS_SRC: 'legacy', FIRSTNAME: 'Old', STAGE: 'subscriber', LEAD_SOURCE: 'x' } });
  await h.post({ form: 'signup', email: 'a@b.co', firstName: 'New', tips: true });
  h.restore();
  const w = h.calls.find(c => c.method === 'PUT');
  assert.strictEqual(w.body.attributes.CONSENT_JOBS_AT, undefined);
  assert.strictEqual(w.body.attributes.CONSENT_JOBS_SRC, undefined);
  assert.strictEqual(w.body.attributes.FIRSTNAME, undefined);
  assert.strictEqual(w.body.attributes.CONSENT_TIPS_AT, '2026-10-24');
});

test('a blocklisted contact is never written to, and the signup is told plainly', async () => {
  const h = harness({ emailBlacklisted: true, attributes: {} });
  const r = await h.post({ form: 'signup', email: 'a@b.co', tips: true });
  h.restore();
  assert.strictEqual(r.statusCode, 200); assert.strictEqual(r.body.ok, false); assert.strictEqual(r.body.blocked, true);
  assert.deepStrictEqual(h.calls.map(c => c.method), ['GET']);
});

test('free check for a blocklisted address: no contact change, KT still notified', async () => {
  const h = harness({ emailBlacklisted: true, attributes: {} });
  const r = await h.post({ form: 'check', email: 'a@b.co', firstName: 'Amara', tips: true });
  h.restore();
  assert.strictEqual(r.body.ok, true);
  assert.deepStrictEqual(h.calls.map(c => c.method + ' ' + c.path), ['GET /contacts/a%40b.co', 'POST /smtp/email']);
  assert.match(h.calls[1].body.textContent, /blocklisted/);
});

test('free check: contact without lists, stage set, KT notified from the Yireh sender', async () => {
  const h = harness(null);
  const r = await h.post({ form: 'check', email: 'a@b.co', firstName: 'Amara', role: 'Customer support', tips: false });
  h.restore();
  assert.strictEqual(r.body.ok, true);
  const w = h.calls.find(c => c.path === '/contacts' && c.method === 'POST');
  assert.strictEqual(w.body.listIds, undefined);
  assert.strictEqual(w.body.attributes.STAGE, 'check_requested');
  const m = h.calls.find(c => c.path === '/smtp/email');
  assert.deepStrictEqual(m.body.to, [{ email: 'yirehcareers@gmail.com' }]);
  assert.strictEqual(m.body.sender.id, 4);
  assert.match(m.body.textContent, /Customer support/);
  assert.match(m.body.textContent, /Tips and offers consent: no/);
});

test('order intake needs a package and records it', async () => {
  const h = harness(null);
  assert.strictEqual((await h.post({ form: 'order', email: 'a@b.co', firstName: 'A' })).statusCode, 400);
  const r = await h.post({ form: 'order', email: 'a@b.co', firstName: 'A', package: 'Professional', role: 'PM' });
  h.restore();
  assert.strictEqual(r.body.ok, true);
  const w = h.calls.find(c => c.path === '/contacts' && c.method === 'POST');
  assert.strictEqual(w.body.attributes.LAST_PACKAGE, 'professional');
  assert.strictEqual(w.body.attributes.STAGE, 'order_intake');
});

test('validation: bad email, unknown form, oversize body', async () => {
  const h = harness(null);
  assert.strictEqual((await h.post({ form: 'signup', email: 'nope' })).statusCode, 400);
  assert.strictEqual((await h.post({ form: 'other', email: 'a@b.co' })).statusCode, 400);
  assert.strictEqual((await h.post({ form: 'signup', email: 'a@b.co', firstName: 'x'.repeat(9000) })).statusCode, 400);
  h.restore(); assert.strictEqual(h.calls.length, 0);
});

test('rate limit: the 9th submission from one address in an hour is refused', async () => {
  const h = harness(null);
  let last;
  for (let i = 0; i < 9; i++) last = await h.post({ form: 'signup', email: `u${i}@b.co` }, { ip: '9.9.9.9' });
  h.restore(); assert.strictEqual(last.statusCode, 429);
});

test('parallel duplicate create falls back to an update', async () => {
  const h = harness(null, { dup: true });
  const r = await h.post({ form: 'signup', email: 'a@b.co' });
  h.restore();
  assert.strictEqual(r.body.ok, true);
  assert.deepStrictEqual(h.calls.filter(c => c.method !== 'GET').map(c => c.method), ['POST', 'PUT']);
});

test('Brevo failures give a clean 502 and the log holds no personal data', async () => {
  const h = harness(null, { writeFails: true });
  const r = await h.post({ form: 'signup', email: 'secret.person@example.com', firstName: 'Secret' });
  h.restore();
  assert.strictEqual(r.statusCode, 502); assert.strictEqual(r.body.ok, false);
  assert.ok(h.logs.length > 0);
  for (const l of h.logs) { assert.ok(!/secret/i.test(l)); assert.ok(!l.includes('@')); }
  const h2 = harness(null, { mailFails: true });
  assert.strictEqual((await h2.post({ form: 'check', email: 'a@b.co', firstName: 'A' })).statusCode, 502); h2.restore();
});

test('key loader accepts the plain key and the base64 text, rejects junk', () => {
  assert.strictEqual(loadKey({ BREVO_API_KEY: KEY }), KEY);
  const wrapped = Buffer.from(JSON.stringify({ api_key: KEY })).toString('base64');
  assert.strictEqual(loadKey({ BREVO_API_KEY: wrapped }), KEY);
  assert.strictEqual(loadKey({ BREVO_API_KEY: 'junk' }), '');
  assert.strictEqual(loadKey({}), '');
});

test('the API key is sent only to Brevo, in a header', async () => {
  const h = harness(null);
  await h.post({ form: 'signup', email: 'a@b.co' });
  h.restore();
  for (const c of h.calls) { assert.strictEqual(c.headers['api-key'], KEY); assert.ok(!JSON.stringify(c.body || {}).includes(KEY)); }
});

test('duplicate create retries the update if the parallel request has not finished writing', async () => {
  const opts = { dup: true, putFailFirst: true };
  const h = harness(null, opts);
  const r = await h.post({ form: 'signup', email: 'a@b.co' });
  h.restore();
  assert.strictEqual(r.body.ok, true);
  assert.deepStrictEqual(h.calls.filter(c => c.method !== 'GET').map(c => c.method), ['POST', 'PUT', 'PUT']);
});
