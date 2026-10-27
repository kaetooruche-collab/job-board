/* Board search: does this listing match the query, and how well?
 *
 * Kept in its own file so the logic can be unit-tested (tests/node/search.test.js) and so the
 * page and the relevance harness measure exactly the same code.
 *
 * Rules:
 *  - The query is normalised: lower-cased, punctuation and hyphens become spaces, so
 *    "customer-support", "customer support" and "Customer  support" are the same query.
 *  - Every query term must match (AND), as the search always did — no listing appears that
 *    could not before, except where punctuation or plurals previously hid it.
 *  - A term matches a word when one is a prefix of the other, or when their roots agree.
 *    The root strips a small set of English endings (plurals, -ing, -er/-or) in both
 *    directions, so "nurses" finds "Nurse", "developers" finds "Developer" and "project
 *    manager" finds "Project Management" — while short terms stay precise: "hr" no longer
 *    matches "their" or "through", which it did as a raw substring.
 *  - Results are ranked: title beats company beats category beats location beats
 *    description. Equal scores keep the feed order (newest first), so ranking never
 *    disturbs recency within a relevance tier.
 */
(function (root, factory) {
  var api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  if (root) root.YCSearch = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';

  function normalise(text) {
    return String(text == null ? '' : text)
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();
  }

  function words(text) {
    var w = normalise(text);
    return w ? w.split(' ') : [];
  }

  /* Light, symmetric stemming, applied to the term and to the word alike:
       1. one plural "s",
       2. one real ending (-ies, -es, -ing, -er/-or),
       3. a trailing silent "e" only when nothing heavy was stripped.
     "developers" and "developer" meet at "develop"; "nurse", "nurses" and "nursing" meet at
     "nurs"; "accountant" stays away from "account" and "bookkeeping" stays away from "booking",
     because neither pair shares a suffix. Nothing matches that both sides do not agree on. */
  function root(word) {
    var w = word;
    if (w.length > 3 && /s$/.test(w) && !/ss$/.test(w)) w = w.slice(0, -1);   // developers → developer
    var heavy = false;
    if (w.length > 4 && /ies$/.test(w)) { w = w.slice(0, -3) + 'y'; heavy = true; }
    else if (w.length > 3 && /(sses|shes|ches|xes|zes|[^s]es)$/.test(w)) { w = w.slice(0, -2); heavy = true; }
    else if (w.length > 5 && /ing$/.test(w)) { w = w.slice(0, -3); heavy = true; }
    else if (w.length > 4 && /(er|or)$/.test(w)) { w = w.slice(0, -2); heavy = true; }
    if (!heavy && w.length > 4 && /e$/.test(w)) w = w.slice(0, -1);            // nurse → nurs
    return w;
  }

  var rootCache = {};
  function cachedRoot(word) {
    if (!(word in rootCache)) rootCache[word] = root(word);
    return rootCache[word];
  }

  /* How strongly a word answers a term.
     A word may be the term itself at the start (market → marketing), share its root exactly
     (nurse/nurses/nursing → nurs), or be a longer form of it (manager → management, worth only
     half). Never the other way round: letting a short stem satisfy a longer query is what made
     "accountant" match every "account" and "bookkeeper" match "booking".
     A real hit scores 1 (the word starts with the term, or the two roots agree); a word that is
     merely a longer form of it scores 0.5. The half-weight matters: for "developers" a title
     reading "Software Developer" must beat "Business Development", which shares the stem but is
     not the job the person asked for. */
  function matchWeight(term, word) {
    if (word.indexOf(term) === 0) return 1;
    var rt = cachedRoot(term), rw = cachedRoot(word);
    if (rt === rw) return 1;
    if (rw.indexOf(rt) === 0 && rt.length >= 3) return 0.5;
    return 0;
  }

  function bestWeight(term, wordList) {
    var best = 0;
    for (var k = 0; k < wordList.length; k++) {
      var w = matchWeight(term, wordList[k]);
      if (w === 1) return 1;
      if (w > best) best = w;
    }
    return best;
  }

  function haystack(job) {
    var cats = job.categories && job.categories.length ? job.categories : [job.category];
    var el = job.eligibility || {};
    return {
      title: words(job.title),
      company: words(job.company),
      categories: words((cats || []).join(' ')),
      region: words((job.regionAsStated || '') + ' ' + (el.label || '')),
      description: words(job.description || '')
    };
  }

  /* Field weights: a term in the title counts for far more than the same term buried in the
     description, which is what puts real matches on the first page. */
  var WEIGHTS = { title: 8, company: 4, categories: 3, region: 2, description: 1 };

  function termsOf(query) {
    return normalise(query).split(' ').filter(Boolean);
  }

  /* Every term must match somewhere in the listing — the original AND rule, spread across
     the whole listing rather than confined to one field, so "project manager remote" still
     finds a title with "Project Manager" and a description with "remote". */
  function matches(job, query) {
    var termList = termsOf(query);
    if (!termList.length) return true;
    var fields = haystack(job);
    for (var t = 0; t < termList.length; t++) {
      var found = false;
      for (var key in WEIGHTS) {
        if (bestWeight(termList[t], fields[key]) > 0) { found = true; break; }
      }
      if (!found) return false;
    }
    return true;
  }

  /* Per-term, per-field score. A listing mentioning every term in its title beats one that
     mentions all of them only in its description; an exact hit beats a merely related word. */
  function score(job, query) {
    var termList = termsOf(query);
    if (!termList.length) return 0;
    var fields = haystack(job), total = 0;
    for (var key in WEIGHTS) {
      var hits = fieldHits(termList, fields[key]);
      if (hits) total += WEIGHTS[key] * hits;
    }
    return total;
  }

  function fieldHits(termList, wordList) {
    var hits = 0;
    for (var i = 0; i < termList.length; i++) hits += bestWeight(termList[i], wordList);
    return hits;
  }

  /* Stable rank: higher score first, feed order (newest first) preserved on ties. */
  function rank(list, query) {
    if (!termsOf(query).length) return list.slice();
    var keyed = list.map(function (job, i) {
      return { job: job, i: i, s: score(job, query) };
    });
    keyed.sort(function (a, b) { return b.s - a.s || a.i - b.i; });
    return keyed.map(function (k) { return k.job; });
  }

  return {
    normalise: normalise,
    root: root,
    termsOf: termsOf,
    matches: matches,
    score: score,
    rank: rank
  };
});