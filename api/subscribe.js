'use strict';
/*
 * POST /api/subscribe: the one server-side door from the website to Brevo.
 * Decision record: drafts/decisions/2026-10-24-signup-function.md. Design and consent rules: drafts/email-system/07-data-consent-event-model.md.
 *
 * Forms (JSON body): { form: 'signup' | 'check' | 'order', email, firstName?, level?, package?, role?, tips?: boolean, website?: '' (honeypot) }
 * What it does, in order: checks origin, size, honeypot and rate limit; validates; reads the Brevo contact; NEVER writes to a blocklisted
 * contact (a form can no longer reverse an unsubscribe); records consent evidence once (date and wording version, never overwritten);
 * adds the contact to the right lists; for the free check and order forms it emails KT a notice so no request is missed.
 * The Brevo key is read from the BREVO_API_KEY environment variable (plain `xkeysib-...` or the base64 text Brevo displays).
 * No personal data is logged. No dependencies.
 */

const BREVO = 'https://api.brevo.com/v3';
const NOTIFY_TO = 'yirehcareers@gmail.com';
const SENDER_ID = 4;                                  // Brevo sender "Yireh Careers"
const LIST_JOBS = 11;                                 // "Job alerts"
const LIST_TIPS = 18;                                 // "Career tips"
const ORIGINS = ['https://yirehcareers.vercel.app'];
const VERSION = { signup: 'signup-v1', check: 'check-v1', order: 'order-v1' };
const LEVELS = { early: 'early', mid: 'mid', senior_plus: 'senior_plus' };
const PACKAGES = ['essential', 'professional', 'executive'];
const MAX_BODY = 4096;
const RATE_LIMIT = 8;                                 // submissions per IP per hour (best effort: per server instance)
const MESSAGES = {
  signup: "Thanks, you're on the list. Your weekly job email will arrive in your inbox.",
  check: "Thanks. Now email your CV to yirehcareers@gmail.com and we'll reply with three things to fix first.",
  order: "Thanks, we've got your details. Reply to our email with your CV and we'll confirm your dates.",
  blocked: "This address unsubscribed earlier, so we can't add it here. Email us at yirehcareers@gmail.com and we'll sort it out.",
  invalid: 'Please check the email address and try again.',
  limited: 'Too many attempts. Please try again later, or email us at yirehcareers@gmail.com.',
  failed: "Something went wrong on our side. Please try again, or email us at yirehcareers@gmail.com."
};

function loadKey(env) {
  let k = String((env || {}).BREVO_API_KEY || '').trim();
  if (k.startsWith('eyJ')) {
    try { k = JSON.parse(Buffer.from(k, 'base64').toString('utf8')).api_key; } catch (e) { return ''; }
  }
  return k.startsWith('xkeysib-') ? k : '';
}

function clean(s, max) {
  return String(s == null ? '' : s).replace(/[\u0000-\u001f\u007f<>]/g, ' ').replace(/\s+/g, ' ').trim().slice(0, max);
}

function makeLimiter() {
  const hits = new Map();
  return function allow(ip, nowMs) {
    const recent = (hits.get(ip) || []).filter(t => nowMs - t < 3600000);
    if (recent.length >= RATE_LIMIT) { hits.set(ip, recent); return false; }
    recent.push(nowMs); hits.set(ip, recent);
    if (hits.size > 5000) hits.clear();
    return true;
  };
}

function createHandler(deps) {
  deps = deps || {};
  const fetchImpl = deps.fetchImpl || fetch;
  const env = deps.env || process.env;
  const now = deps.now || (() => new Date());
  const allow = deps.limiter || makeLimiter();
  const sleep = deps.sleep || (ms => new Promise(r => setTimeout(r, ms)));
  const origins = ORIGINS.concat(env.EXTRA_ALLOWED_ORIGIN ? [env.EXTRA_ALLOWED_ORIGIN] : []);

  async function brevo(key, method, path, body) {
    const res = await fetchImpl(BREVO + path, {
      method,
      headers: { 'api-key': key, accept: 'application/json', 'content-type': 'application/json', 'user-agent': 'YirehCareersSite/1.0' },
      body: body === undefined ? undefined : JSON.stringify(body)
    });
    let data = {};
    try { data = await res.json(); } catch (e) { /* empty body */ }
    return { status: res.status, data };
  }

  return async function handler(req, res) {
    function send(status, ok, message, extra) {
      res.statusCode = status;
      res.setHeader('Content-Type', 'application/json; charset=utf-8');
      res.setHeader('Cache-Control', 'no-store');
      res.setHeader('X-Content-Type-Options', 'nosniff');
      res.end(JSON.stringify(Object.assign({ ok, message }, extra || {})));
    }
    function log(outcome, form) { try { console.log(JSON.stringify({ at: 'subscribe', form: form || null, outcome })); } catch (e) { /* ignore */ } }

    if (req.method !== 'POST') { res.setHeader('Allow', 'POST'); return send(405, false, 'Method not allowed'); }
    const origin = String((req.headers || {}).origin || '');
    if (!origins.includes(origin)) { log('bad_origin'); return send(403, false, 'Not allowed'); }

    let body = req.body;
    if (typeof body === 'string') { try { body = JSON.parse(body); } catch (e) { body = null; } }
    if (!body || typeof body !== 'object' || JSON.stringify(body).length > MAX_BODY) { log('bad_body'); return send(400, false, MESSAGES.invalid); }

    const form = String(body.form || '');
    if (!VERSION[form]) { log('bad_form'); return send(400, false, MESSAGES.invalid); }
    if (clean(body.website, 50)) { log('honeypot', form); return send(200, true, MESSAGES[form]); }   // bots get a quiet "success"

    const fwd = String((req.headers || {})['x-forwarded-for'] || '').split(',')[0].trim() || 'unknown';
    if (!allow(fwd, now().getTime())) { log('rate_limited', form); return send(429, false, MESSAGES.limited); }

    const email = clean(body.email, 254).toLowerCase();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email) || email.length > 254) { log('bad_email', form); return send(400, false, MESSAGES.invalid); }
    const firstName = clean(body.firstName, 60);
    const level = LEVELS[String(body.level || '')] || '';
    const pkg = PACKAGES.includes(String(body.package || '').toLowerCase()) ? String(body.package).toLowerCase() : '';
    const role = clean(body.role, 200);
    const wantsTips = body.tips === true || body.tips === 'true' || body.tips === 'on';
    if (form === 'order' && !pkg) { log('bad_package', form); return send(400, false, MESSAGES.invalid); }
    if (form === 'check' && !firstName) { log('bad_name', form); return send(400, false, MESSAGES.invalid); }

    const key = loadKey(env);
    if (!key) { log('no_key', form); return send(500, false, MESSAGES.failed); }

    try {
      const today = now().toISOString().slice(0, 10);
      const path = '/contacts/' + encodeURIComponent(email);
      const found = await brevo(key, 'GET', path);
      if (found.status !== 200 && found.status !== 404) { log('lookup_failed', form); return send(502, false, MESSAGES.failed); }
      const existing = found.status === 200 ? found.data : null;
      const attrs0 = (existing && existing.attributes) || {};

      if (existing && existing.emailBlacklisted) {
        // Never touch a blocklisted contact. A service request is still a service request: tell KT.
        if (form === 'signup') { log('blocked', form); return send(200, false, MESSAGES.blocked, { blocked: true }); }
        const n = await notify(key, form, { email, firstName, pkg, role, wantsTips: false, blocked: true });
        if (!n) { log('notify_failed', form); return send(502, false, MESSAGES.failed); }
        log('blocked_service_only', form);
        return send(200, true, MESSAGES[form]);
      }

      const attrs = {};
      const lists = [];
      if (firstName && !attrs0.FIRSTNAME) attrs.FIRSTNAME = firstName;
      if (!attrs0.LEAD_SOURCE) attrs.LEAD_SOURCE = 'site-' + form;
      if (form === 'signup') {
        lists.push(LIST_JOBS);
        if (!attrs0.CONSENT_JOBS_AT) { attrs.CONSENT_JOBS_AT = today; attrs.CONSENT_JOBS_SRC = VERSION.signup; }
        if (level) attrs.LEVEL_INTEREST = level;
        if (!attrs0.STAGE) attrs.STAGE = 'subscriber';
      } else if (form === 'check') {
        if (attrs0.STAGE !== 'customer') attrs.STAGE = 'check_requested';
      } else if (form === 'order') {
        if (attrs0.STAGE !== 'customer') attrs.STAGE = 'order_intake';
        attrs.LAST_PACKAGE = pkg;
      }
      if (wantsTips) {
        lists.push(LIST_TIPS);
        if (!attrs0.CONSENT_TIPS_AT) { attrs.CONSENT_TIPS_AT = today; attrs.CONSENT_TIPS_SRC = VERSION[form]; }
      }

      let w;
      if (existing) {
        const upd = { attributes: attrs };
        if (lists.length) upd.listIds = lists;
        w = await brevo(key, 'PUT', path, upd);
      } else {
        const create = { email, attributes: attrs, updateEnabled: false };
        if (lists.length) create.listIds = lists;
        w = await brevo(key, 'POST', '/contacts', create);
        if (w.status === 400 && w.data && w.data.code === 'duplicate_parameter') {   // created a moment ago by a parallel request
          const upd = { attributes: attrs };
          if (lists.length) upd.listIds = lists;
          for (let i = 0; i < 3; i++) {                                                // the other request may not have finished writing yet
            await sleep(i === 0 ? 250 : 600);
            w = await brevo(key, 'PUT', path, upd);
            if ([200, 201, 204].includes(w.status)) break;
          }
        }
      }
      if (![200, 201, 204].includes(w.status)) { log('write_failed_' + w.status, form); return send(502, false, MESSAGES.failed); }

      if (form !== 'signup') {
        const n = await notify(key, form, { email, firstName, pkg, role, wantsTips, blocked: false });
        if (!n) { log('notify_failed', form); return send(502, false, MESSAGES.failed); }
      }
      log('ok' + (wantsTips ? '_tips' : ''), form);
      return send(200, true, MESSAGES[form]);
    } catch (e) {
      log('error', form);
      return send(502, false, MESSAGES.failed);
    }
  };

  async function notify(key, form, d) {
    const lines = form === 'check'
      ? ['New FREE CV CHECK request', '', 'Name: ' + d.firstName, 'Email: ' + d.email, 'Aiming for: ' + (d.role || '(not given)'),
         'Tips and offers consent: ' + (d.wantsTips ? 'YES (ticked)' : 'no'),
         '', 'Next: reply from yirehcareers@gmail.com with template "OP-1 Free check: request received" (or OP-13 if this week is full). The CV should arrive by email.']
      : ['New ORDER INTAKE', '', 'Package: ' + d.pkg, 'Name: ' + (d.firstName || '(not given)'), 'Email: ' + d.email, 'Roles aiming for: ' + (d.role || '(not given)'),
         'Tips and offers consent: ' + (d.wantsTips ? 'YES (ticked)' : 'no'),
         '', 'Next: confirm the payment yourself, record it in the register, then send template "OP-3 Order: payment received, what we need".'];
    if (d.blocked) lines.push('', 'Note: this address is blocklisted in Brevo for marketing. Service emails from Gmail are fine; nothing was changed in Brevo.');
    const r = await brevo(key, 'POST', '/smtp/email', {
      sender: { id: SENDER_ID },
      to: [{ email: NOTIFY_TO }],
      replyTo: { email: d.email },
      subject: (form === 'check' ? 'Free CV check request: ' : 'Order intake (' + d.pkg + '): ') + (d.firstName || d.email),
      textContent: lines.join('\n')
    });
    return [200, 201, 202].includes(r.status);
  }
}

module.exports = createHandler();
module.exports.createHandler = createHandler;
module.exports.loadKey = loadKey;
