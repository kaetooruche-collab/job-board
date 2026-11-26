// Guardrail 6: a job shown in a post is still open and its card matches the posting.
// Opens each job's posting in a real browser, checks the title is on the page and no closed-role wording is.
//   node social/tools/verify-open.js social/output/2026-12-01/w49-p2/manifest.json [more manifests]
// Writes "check" into each manifest job: {checked_open_on, ok, title_found, closed_wording, final_url}.
// Exit 1 if any job fails, so it can gate scheduling.
const { chromium } = require('playwright');
const fs = require('fs');

const CLOSED = /no longer (?:accepting|available|open)|position (?:has been )?filled|job (?:is )?closed|this job has expired|posting has (?:expired|closed)|not accepting applications|job not found|page not found|this position is closed/i;

// A posting that limits applicants to one country contradicts a "Worldwide" or region card.
const lex = JSON.parse(fs.readFileSync(require('path').join(__dirname, '..', '..', 'data', 'geo_lexicon.json'), 'utf8'));
const COUNTRY = lex.countries.map(c => c.name).concat(['US', 'U.S.', 'USA', 'UK'])
  .map(n => n.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|');
const LIMIT = new RegExp('(?:anywhere|based|located|reside|residing|live|living|resident|residents|eligible to work) (?:with)?in (?:the )?(?:contiguous |continental |lower 48 )?(?:' + COUNTRY + ')\\b|(?:' + COUNTRY + ')[- ](?:only|based only)\\b', 'i');

const words = t => t.toLowerCase().replace(/[^a-z0-9 ]+/g, ' ').split(/\s+/).filter(w => w.length > 2);

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36' });
  let bad = 0;
  const today = new Date().toISOString().slice(0, 10);
  for (const file of process.argv.slice(2)) {
    const m = JSON.parse(fs.readFileSync(file, 'utf8'));
    for (const j of m.jobs) {
      const page = await ctx.newPage();
      let check = { checked_open_on: today, ok: false };
      try {
        const resp = await page.goto(j.sourceUrl, { waitUntil: 'networkidle', timeout: 45000 });
        await page.waitForTimeout(1500);
        const text = (await page.innerText('body')).replace(/\s+/g, ' ');
        const need = words(j.title);
        const have = new Set(words(text));
        const found = need.filter(w => have.has(w)).length;
        const closed = (text.match(CLOSED) || [null])[0];
        const wideCard = j.apply_from === 'Worldwide' || !/\b(?:only)\b/.test(j.apply_from || '') && !lex.countries.some(c => (j.apply_from || '').includes(c.name));
        const limit = wideCard ? (text.match(LIMIT) || [null])[0] : null;
        check = { ...check, http: resp && resp.status(), final_url: page.url(),
          title_found: `${found}/${need.length} title words`, closed_wording: closed, contradiction: limit,
          ok: !!resp && resp.status() < 400 && found >= Math.ceil(need.length * 0.75) && !closed && !limit };
      } catch (e) {
        check.error = String(e).slice(0, 200);
      }
      j.check = check;
      if (!check.ok) bad++;
      console.log(`${check.ok ? 'OPEN ' : 'CHECK'} ${j.id} ${j.title} | ${j.company} | ${check.title_found || check.error} ${check.closed_wording || ''} ${check.contradiction ? 'CONTRADICTS CARD: ' + check.contradiction : ''}`);
      await page.close();
    }
    fs.writeFileSync(file, JSON.stringify(m, null, 2));
  }
  await browser.close();
  process.exit(bad ? 1 : 0);
})();
