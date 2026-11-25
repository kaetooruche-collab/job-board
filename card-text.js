/* What a job card says about location and caveats, in plain words for job seekers.
 *
 * KT, 25 Nov 2026: "You can't talk to users like this ... Eligibility unclear can't keep appearing." The data keeps the
 * classifier's own notes (written for checking, not for reading); this file turns them into the few facts a reader
 * needs, and drops the rest. Kept separate from index.html so tests/node/card-text.test.js can check every phrase.
 * Decision and wording options: drafts/decisions/2026-11-25-card-wording-for-readers.md.
 */
(function (root, factory) {
  var api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  if (root) root.YCCard = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';

  /* Where you can apply from: one short phrase, or null when the employer does not say. */
  function applyFrom(job) {
    var el = job.eligibility || {};
    if (el.type === 'worldwide') return 'Worldwide';
    if (el.type === 'unclear' || !el.label) return null;
    return el.label.replace(/ only$/, '');
  }

  function listOf(note) {
    var m = /cannot hire in:\s*(.+?)\.?$/i.exec(note);
    return m ? m[1].replace(/ and others$/i, ' and some others') : null;
  }

  /* The caveats worth a reader's attention, each in one short line; everything else stays out of sight. */
  function heads(job) {
    var src = (job.unresolvedQuestions || []).concat((job.eligibility || {}).notes || []);
    var out = [];
    function add(s) { if (s && out.indexOf(s) === -1) out.push(s); }
    src.forEach(function (n) {
      if (/occasional office or in-person attendance/i.test(n)) add('May need occasional office visits');
      else if (/in-person onboarding or training/i.test(n)) add('Starts with in-person onboarding or training');
      else if (/cannot hire in:/i.test(n)) add('Not open to applicants in: ' + listOf(n));
      else if (/existing work authori[sz]ation/i.test(n)) add('You’ll need the right to work there already');
    });
    if ((job.eligibility || {}).authorizationRequired) add('You’ll need the right to work there already');
    return out.slice(0, 2);
  }

  /* Quotes from the posting that explain the labels; the classifier's own working notes are left out. */
  function quotes(job) {
    var keep = [];
    var stated = String(job.regionAsStated || '').trim().toLowerCase();
    (job.evidence || []).forEach(function (e) {
      if (!e || !e.text) return;
      if (/company-level|not counted|explicitly no office|mixed office/i.test(e.signal || '')) return;
      if (/^field says /i.test(e.text)) return;                 /* "field says remote (Remote)" is our shorthand */
      if (e.effect && !/remote|restricted|worldwide/i.test(e.effect)) return;
      if (e.text.trim().toLowerCase() === stated || e.text.trim().length < 12) return;   /* repeats the location line */
      if (keep.indexOf(e.text) === -1) keep.push(e.text);
    });
    return keep.slice(0, 2);
  }

  return { applyFrom: applyFrom, heads: heads, quotes: quotes };
});
