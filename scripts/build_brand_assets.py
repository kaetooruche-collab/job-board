"""Builds the site's brand files from the one YC mark: favicon (svg, png, ico), apple-touch-icon,
the email logo and og-image.png.  Run: python3 scripts/build_brand_assets.py
(needs Node + Playwright and Pillow; the mark is the same one used for the WhatsApp picture,
see drafts/whatsapp-profile/build_profile_pictures.py)."""
import io
import os
import subprocess
import textwrap

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRAD = ("<defs><linearGradient id='t' x1='0' y1='0' x2='1' y2='1'><stop offset='0' stop-color='#3b82f6'/>"
        "<stop offset='1' stop-color='#1d4ed8'/></linearGradient></defs>")


def glyph(stroke):
    return (f"<g fill='none' stroke-width='{stroke}' stroke-linecap='round' stroke-linejoin='round'>"
            "<path d='M25 31 L48 56' stroke='#fff'/><path d='M48 56 L48 82' stroke='#fff'/>"
            "<path d='M48 56 L83 17' stroke='#bfdbfe'/></g>")


def tile(rx, stroke):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'>{GRAD}"
            f"<rect width='100' height='100' rx='{rx}' fill='url(#t)'/>{glyph(stroke)}</svg>")


FAVICON_SVG = tile(22, 12)          # rounded tile, heavier strokes so it holds at 16px
SQUARE_SVG = tile(0, 10.5)          # full-bleed square for apple-touch-icon (iOS rounds it itself)
EMAIL_SVG = tile(22, 10.5)
open(os.path.join(ROOT, "favicon.svg"), "w").write(FAVICON_SVG)

OG_HTML = f"""
<style>@font-face{{font-family:Inter;src:url(file://{ROOT}/fonts/inter-latin.woff2);font-weight:100 900}}
body{{margin:0;width:1200px;height:630px;font-family:Inter,sans-serif;color:#fff;
background:radial-gradient(circle at 82% 22%,#2a4a7f 0,#14223f 38%,#0b1220 75%)}}
.logo{{position:absolute;left:84px;top:104px;display:flex;align-items:center;gap:28px;font-size:104px;font-weight:800;letter-spacing:-3px}}
.logo svg{{width:96px;height:96px}} .logo b{{color:#60a5fa;font-weight:800}}
h1{{position:absolute;left:84px;top:262px;width:860px;margin:0;font-size:58px;line-height:1.18;font-weight:700;letter-spacing:-1px}}
.pills{{position:absolute;left:84px;top:484px;display:flex;gap:16px}}
.pills span{{border:2px solid #3a4a6b;border-radius:30px;padding:14px 26px;font-size:26px;font-weight:600;color:#c7d6f5;background:rgba(255,255,255,.04)}}
</style>
<div class="logo">{EMAIL_SVG}<div>Yireh <b>Careers</b></div></div>
<h1>Verified remote jobs. Every link goes to the employer’s own posting.</h1>
<div class="pills"><span>Updated every 6 hours</span><span>CV &amp; LinkedIn help</span></div>
"""

js = textwrap.dedent(f"""
const {{ chromium }} = require('playwright');
const fs = require('fs');
(async () => {{
  const b = await chromium.launch();
  async function shot(html, w, h, out, transparent) {{
    const p = await b.newPage({{ viewport: {{ width: w, height: h }} }});
    await p.setContent(html);
    await p.evaluate(() => document.fonts.ready);
    await p.screenshot({{ path: out, omitBackground: !!transparent }});
    await p.close();
  }}
  const wrap = (svg, s) => `<style>body{{margin:0;background:transparent}}svg{{display:block;width:${{s}}px;height:${{s}}px}}</style>` + svg;
  await shot(wrap({FAVICON_SVG!r}, 256), 256, 256, '{ROOT}/_icon256.png', true);
  await shot(wrap({SQUARE_SVG!r}, 180), 180, 180, '{ROOT}/apple-touch-icon.png', false);
  await shot(wrap({EMAIL_SVG!r}, 144), 144, 144, '{ROOT}/yc-logo.png', true);
  await shot({OG_HTML!r}, 1200, 630, '{ROOT}/og-image.png', false);
  await b.close();
}})();
""")
open("/tmp/_brand.js", "w").write(js)
subprocess.run(["node", "/tmp/_brand.js"], check=True, cwd=ROOT)

big = Image.open(os.path.join(ROOT, "_icon256.png")).convert("RGBA")
big.resize((32, 32), Image.LANCZOS).save(os.path.join(ROOT, "favicon-32.png"))
big.save(os.path.join(ROOT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
os.remove(os.path.join(ROOT, "_icon256.png"))
print("built: favicon.svg favicon-32.png favicon.ico apple-touch-icon.png yc-logo.png og-image.png")
