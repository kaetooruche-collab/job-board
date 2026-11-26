// Screenshot every NN.html in the given folders to NN.jpg (JPEG, quality 92) at 1080x1350 (used by render_posts.py).
// Fonts: Inter from the system (installed here) — no network needed.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const dirs = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  for (const dir of dirs) {
    const files = fs.readdirSync(dir).filter(f => /^\d+\.html$/.test(f)).sort();
    for (const f of files) {
      await page.goto('file://' + path.resolve(dir, f));
      await page.evaluate(() => document.fonts.ready);
      // Fail loudly if text overflows the slide (a cut-off title is worse than no post).
      const over = await page.evaluate(() => {
        const out = [];
        document.querySelectorAll('h1,.title,.sub,.card').forEach(el => {
          const r = el.getBoundingClientRect();
          if (r.bottom > 1350 - 120) out.push(el.className || el.tagName);
        });
        return out;
      });
      if (over.length) console.error(`WARNING ${dir}/${f}: text reaches the footer (${over.join(', ')})`);
      await page.screenshot({ path: path.resolve(dir, f.replace('.html', '.jpg')), type: 'jpeg', quality: 92 });
    }
  }
  await browser.close();
})();
