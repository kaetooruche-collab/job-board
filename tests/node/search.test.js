/* Search relevance tests for search.js (node:test). Uses the real jobs.json where it matters,
 * so the assertions are about the board's actual listings, not fixtures I invented. */
const test = require('node:test');
const assert = require('node:assert');
const fs = require('node:fs');
const path = require('node:path');

const S = require('../../search.js');
const jobs = JSON.parse(fs.readFileSync(path.join(__dirname, '..', '..', 'jobs.json'), 'utf8'));

const j = (o) => Object.assign({ categories: [], eligibility: {} }, o);

test('query normalisation turns punctuation and case into one query', () => {
  assert.strictEqual(S.normalise('Customer-Support'), 'customer support');
  assert.strictEqual(S.normalise('  project   manager!! '), 'project manager');
  assert.deepStrictEqual(S.termsOf('customer-support'), ['customer', 'support']);
});

test('hyphenated and multi-space queries match plain listings', () => {
  const job = j({ title: 'Customer Support Representative' });
  assert.ok(S.matches(job, 'customer support'));
  assert.ok(S.matches(job, 'customer-support'));
  assert.ok(S.matches(job, 'Customer  Support'));
});

test('plurals and -ing match in both directions', () => {
  const dev = j({ title: 'Software Developer' });
  assert.ok(S.matches(dev, 'developers'), 'query plural finds singular title');
  assert.ok(S.matches(dev, 'developer'), 'singular query finds singular title');

  const nurse = j({ title: 'Registered Nurse' });
  assert.ok(S.matches(nurse, 'nurses'), 'plural query finds singular title');
  assert.ok(S.matches(j({ title: 'Nursing Assistant' }), 'nurse'), 'singular query finds -ing title');
  assert.ok(S.matches(j({ title: 'Project Management' }), 'project manager'), '-er query finds -ment title');
  assert.ok(S.matches(j({ title: 'Design Systems Lead' }), 'designer'), 'query -er finds stem title');
});

test('short terms stay precise: "hr" must not match words that merely contain it', () => {
  const job = j({ title: 'Operations Coordinator', description: 'You will work through their checks and charts.' });
  assert.ok(!S.matches(job, 'hr'), '"hr" must not match "through"/"their"/"charts"');
  assert.ok(S.matches(j({ title: 'HR Business Partner' }), 'hr'), 'but a real HR title still matches');
  assert.ok(S.matches(j({ title: 'HRIS Specialist' }), 'hr'));
});

test('every term must still match somewhere (the original AND rule)', () => {
  const job = j({ title: 'Project Manager', description: 'Fully remote team.' });
  assert.ok(S.matches(job, 'project manager remote'), 'terms may live in different fields');
  assert.ok(!S.matches(job, 'project manager accountant'));
});

test('a title match scores above a description-only match', () => {
  const inTitle = j({ title: 'Account Executive', description: 'Sell the product.' });
  const inDesc = j({ title: 'Warehouse Associate', description: 'Prior account executive experience helps.' });
  assert.ok(S.score(inTitle, 'account executive') > S.score(inDesc, 'account executive'));
  const ranked = S.rank([inDesc, inTitle], 'account executive');
  assert.strictEqual(ranked[0], inTitle, 'title match is ranked first');
});

test('ranking is stable: equal scores keep the feed order', () => {
  const a = j({ title: 'Alpha Analyst' }), b = j({ title: 'Beta Analyst' }), c = j({ title: 'Gamma Analyst' });
  const ranked = S.rank([a, b, c], 'analyst');
  assert.deepStrictEqual(ranked, [a, b, c]);
});

test('an empty query returns everything, unchanged', () => {
  const list = [j({ title: 'One' }), j({ title: 'Two' })];
  assert.ok(S.matches(list[0], ''));
  assert.deepStrictEqual(S.rank(list, '   '), list);
});

test('no listing that matched at a word start before is lost now (recall guard, real data)', () => {
  const queries = ['customer support', 'customer service', 'no experience', 'project manager',
    'software engineer', 'accountant', 'recruiter', 'sales', 'analyst', 'marketing manager', 'hr'];
  const oldMatch = (job, q) => {
    const cats = job.categories && job.categories.length ? job.categories : [job.category];
    const hay = [job.title, job.company, job.description, (cats || []).join(' '),
      job.regionAsStated, (job.eligibility || {}).label].join(' ').toLowerCase();
    return q.split(/\s+/).filter(Boolean).every((t) => {
      let i = hay.indexOf(t);
      while (i !== -1) {
        const before = i === 0 || !/[a-z0-9]/.test(hay[i - 1]);   // old match at a word start
        if (before) return true;
        i = hay.indexOf(t, i + 1);
      }
      return false;
    });
  };
  for (const q of queries) {
    const oldHits = jobs.filter((x) => oldMatch(x, q));
    const lost = oldHits.filter((x) => !S.matches(x, q));
    assert.strictEqual(lost.length, 0, `"${q}" lost ${lost.length} listings, e.g. ${lost[0] && lost[0].title}`);
  }
});

test('every title match outranks every description-only match (real data)', () => {
  const queries = ['software engineer', 'recruiter', 'account executive', 'customer support',
    'marketing manager', 'sales', 'analyst', 'project manager'];
  /* "the title alone satisfies the query" — the same shipped matcher, pointed at the title only */
  const inTitle = (x, q) => S.matches({ title: x.title, categories: [], eligibility: {} }, q);
  for (const q of queries) {
    const ranked = S.rank(jobs, q);
    const named = ranked.map((x) => inTitle(x, q));
    const firstMiss = named.indexOf(false);
    const lastHit = named.lastIndexOf(true);
    assert.ok(firstMiss === -1 || lastHit < firstMiss,
      `"${q}": a title match appears after a weaker result at position ${lastHit}`);
    // the page a reader actually loads must be the best of what exists
    const titleHits = named.filter(Boolean).length;
    const pageSize = Math.min(40, titleHits);
    assert.strictEqual(named.slice(0, pageSize).filter(Boolean).length, pageSize,
      `"${q}": page 1 is not filled with the listings that name the role`);
    if (ranked.length > 40 && titleHits >= 40) {
      const share = named.slice(0, 40).filter(Boolean).length / 40;
      assert.ok(share === 1, `"${q}": only ${(share * 100).toFixed(0)}% of page 1 names the role`);
    }
  }
});

test('a query with no real roles never shows a listing that claims that role', () => {
  // Stemming may surface listings whose *description* uses the verb ("translating customer needs
  // into products"), which is honest — but a card may only claim a role in its title when the word
  // is really there. This guards against stemming inventing a claim, and it stays true as the feed
  // changes: the board gained a genuine "Writer/Translator" listing on 28 Oct, which is a real
  // match, not a fabricated one.
  const inTitle = (x, q) => S.matches({ title: x.title, categories: [], eligibility: {} }, q);
  // a real inflection of the same word is an honest match too ("Nurse" for "nursing")
  const FORMS = { nursing: 'nurs(?:e|es|ing)' };
  const literal = (x, q) => new RegExp('\\b' + (FORMS[q] || q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + 's?') + '\\b', 'i').test(x.title);
  for (const q of ['translator', 'nursing', 'bookkeeper']) {
    const hits = jobs.filter((x) => S.matches(x, q));
    const claimed = hits.filter((x) => inTitle(x, q));
    const fabricated = claimed.filter((x) => !literal(x, q));
    assert.strictEqual(fabricated.length, 0, `"${q}": ${fabricated.length} title(s) claim a role the word is not in`);
    assert.ok(hits.length < 25, `"${q}": ${hits.length} results is noise, not a match`);
  }
});

test('a stray initial in a listing cannot satisfy a long query', () => {
  // regression: the reverse-prefix rule once let the single word "t" match "translator",
  // which returned 104 listings on a board with no translation work on it at all.
  const job = j({ title: 'Care Navigator', description: 'Team of three. T tickets handled daily.' });
  assert.ok(!S.matches(job, 'translator'));
  assert.ok(!S.matches(job, 'recruiter'), 'and "r" does not match "recruiter" either');
});