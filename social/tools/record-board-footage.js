// Record phone-sized footage of the LIVE board for videos (free; no account, no spend).
// Based on drafts/marketing/video/video1/record-board-footage.js, changed for KT's rule of 26 Nov 2026:
// NO country is typed or shown. The default demo types "Worldwide roles only" into "Where do you live?".
//
//   node social/tools/record-board-footage.js --out social/output/footage/2026-12-01 [--seconds 14]
// Cards are hidden until the worldwide filter is applied; the final view is scanned for country names (exit 1 if any).
// Then: ffmpeg -framerate <fps from meta.json> -i <out>/frames/f%05d.jpg -vf "scale=1080:1920,format=yuv420p" -c:v libx264 <out>/board.mp4
// Hidden while recording (QA 27 Nov): undated counts (.hero-facts, #job-count), the paid "Get a CV" link (.cv-btn) and the
// hero's "Free. No fee to apply." (a post says free at most once). Nothing else on the live page is changed.
// Writes <out>/frames/*.jpg (1080x1920), <out>/meta.json (frame times, scene marks, the job shown at the end,
// today's job count as the page shows it). The job in the last shot must still be checked against its posting.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > -1 ? process.argv[i + 1] : d; };
const OUT = path.resolve(arg('out', `social/output/footage/${new Date().toISOString().slice(0, 10)}`));
const SCENE = 'worldwide';   // the only scene that cannot show a country (KT, 26 Nov 2026)
const SECONDS = Number(arg('seconds', 14));
const sleep = ms => new Promise(r => setTimeout(r, ms));

(async () => {
  const frames = path.join(OUT, 'frames');
  fs.rmSync(frames, { recursive: true, force: true });
  fs.mkdirSync(frames, { recursive: true });
  const browser = await chromium.launch();
  // 432x768 CSS pixels at 2.5x = 1080x1920 frames
  const ctx = await browser.newContext({ viewport: { width: 432, height: 768 }, deviceScaleFactor: 2.5, isMobile: true, hasTouch: true });
  await ctx.route(/goatcounter|gc\.zgo\.at/, r => r.abort());   // never count our own recording as a visit
  const p = await ctx.newPage();
  await p.goto('https://yirehcareers.vercel.app/?utm_source=video', { waitUntil: 'networkidle' });
  // Cards stay hidden until the worldwide filter is on, so no card's country label is ever filmed.
  await p.addStyleTag({ content: '.inline-signup{display:none!important} html{scroll-behavior:smooth} body.yc-rec .job-card{visibility:hidden} .hero-facts,#job-count,.cv-btn{visibility:hidden!important} #level-row,#level-group-label{display:none!important} .hero-sub{font-size:0!important} .hero-sub::after{content:"Every job shows where it hires from.";font-size:16px}' });
  await p.evaluate(() => document.body.classList.add('yc-rec'));

  let done = false, n = 0;
  const times = [];
  const t0 = Date.now();
  const marks = {};
  const capture = (async () => {
    while (!done) {
      const buf = await p.screenshot({ type: 'jpeg', quality: 88 });
      fs.writeFileSync(path.join(frames, `f${String(n).padStart(5, '0')}.jpg`), buf);
      times.push(Date.now() - t0); n++;
    }
  })();
  const mark = k => { marks[k] = Date.now() - t0; };

  mark('A_top'); await sleep(2200);
  // B: the search box
  await p.evaluate(() => window.scrollTo({ top: document.querySelector('.toolbar').getBoundingClientRect().top + scrollY - 70 }));
  await sleep(700); mark('B_toolbar');
  await p.click('#f-country-input'); await sleep(800);
  await p.keyboard.type('Worldwide roles only', { delay: 110 });
  await p.locator('#f-country-input').dispatchEvent('change');
  await p.locator('#f-country-input').blur();
  await sleep(900);
  await p.evaluate(() => document.body.classList.remove('yc-rec'));
  await sleep(1300); mark('C_filtered');
  // D: the first card in the list (whatever today's feed shows); scroll it into view and hold
  const card = p.locator('.job-card').first();
  const bb = await card.boundingBox();
  if (bb) await p.evaluate(y => window.scrollBy({ top: y - 90 }), bb.y);
  mark('D_card');
  const remaining = Math.max(2000, SECONDS * 1000 - (Date.now() - t0));
  await sleep(remaining);
  const shown = {
    title: await card.locator('.job-title').innerText().catch(() => null),
    company: await card.locator('.job-company').innerText().catch(() => null),
    link: await card.locator('a[href^="http"]').first().getAttribute('href').catch(() => null),
  };
  const countText = (await p.innerText('#job-count').catch(() => '')).slice(0, 80);
  // Country scan of everything filmed in the final view (KT's rule): lexicon names and aliases.
  const lex = JSON.parse(fs.readFileSync(path.join(__dirname, '..', '..', 'data', 'geo_lexicon.json'), 'utf8'));
  const visible = await p.evaluate(() => [...document.querySelectorAll('body *')].filter(e => {
    const r = e.getBoundingClientRect(); return e.children.length === 0 && r.bottom > 0 && r.top < innerHeight && r.width > 0;
  }).map(e => e.innerText).join(' '));
  const countries = [];
  for (const c of lex.countries) for (const nm of [c.name, ...c.aliases.filter(a => a.length > 3 && a !== 'america')])
    if (new RegExp('\\b' + nm.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '\\b', 'i').test(visible)) countries.push(c.name);
  done = true; await capture;
  const secs = times[times.length - 1] / 1000;
  const meta = { recorded_at: new Date().toISOString(), scene: SCENE, frames: n, seconds: secs,
    fps: +(n / secs).toFixed(2), frame_ms: times, marks, last_card: shown, job_count_text: countText,
    countries_visible_at_end: [...new Set(countries)],
    reminder: 'Open last_card.link and confirm the role is open before using this footage (skill guardrail 6).' };
  fs.writeFileSync(path.join(OUT, 'meta.json'), JSON.stringify(meta, null, 2));
  console.log(JSON.stringify({ out: OUT, frames: n, fps: meta.fps, marks, last_card: shown, countText, countries_visible_at_end: meta.countries_visible_at_end }, null, 1));
  if (meta.countries_visible_at_end.length) { console.error('A country is on screen: do not use this footage.'); process.exitCode = 1; }
  await browser.close();
})();
