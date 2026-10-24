"""Builds the WhatsApp profile pictures: SVG masters + 1024px PNGs + a circle preview.
Run: python3 drafts/whatsapp-profile/build_profile_pictures.py   (needs Node + Playwright, already in the cloud image)
Design: a "Y" whose right arm is a check mark: Y for Yireh, check for verified. Palette from the site (navy hero, blue accent)."""
import os, subprocess, textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
BG = ("<defs><radialGradient id='g' cx='72%' cy='28%' r='80%'><stop offset='0' stop-color='#1f3f73'/><stop offset='.55' stop-color='#12213f'/>"
      "<stop offset='1' stop-color='#0b1220'/></radialGradient><linearGradient id='t' x1='0' y1='0' x2='1' y2='1'><stop offset='0' stop-color='#3b82f6'/>"
      "<stop offset='1' stop-color='#1d4ed8'/></linearGradient><filter id='s' x='-20%' y='-20%' width='140%' height='150%'>"
      "<feDropShadow dx='0' dy='10' stdDeviation='14' flood-color='#000' flood-opacity='.35'/></filter></defs>"
      "<rect width='1024' height='1024' fill='url(#g)'/>")
# 560px tile centred (corner distance 396px, inside the 512px circle WhatsApp crops to)
TILE = "<rect x='232' y='232' width='560' height='560' rx='128' fill='url(#t)' filter='url(#s)'/>"
# the mark, drawn on a 100-unit grid and scaled into the tile
MARK = ("<g transform='translate(232 232) scale(5.6)' fill='none' stroke-width='10.5' stroke-linecap='round' stroke-linejoin='round'>"
        "<path d='M25 31 L48 56' stroke='#fff'/><path d='M48 56 L48 82' stroke='#fff'/><path d='M48 56 L83 17' stroke='#bfdbfe'/></g>")
MARK_SMALL = MARK.replace("translate(232 232) scale(5.6)", "translate(302 122) scale(4.2)")  # for the name variant (tile 420)
VARIANTS = {
    "yc-mark": f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1024 1024'>{BG}{TILE}{MARK}</svg>",
    "yc-monogram": (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1024 1024'>{BG}{TILE}"
                    "<text x='512' y='640' text-anchor='middle' font-family='Inter' font-weight='800' font-size='300' letter-spacing='-10'>"
                    "<tspan fill='#fff'>Y</tspan><tspan fill='#bfdbfe'>C</tspan></text></svg>"),
    "yc-mark-with-name": (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1024 1024'>{BG}"
                          "<rect x='302' y='170' width='420' height='420' rx='96' fill='url(#t)' filter='url(#s)'/>"
                          "<g transform='translate(302 170) scale(4.2)' fill='none' stroke-width='10.5' stroke-linecap='round' stroke-linejoin='round'>"
                          "<path d='M25 31 L48 56' stroke='#fff'/><path d='M48 56 L48 82' stroke='#fff'/><path d='M48 56 L83 17' stroke='#bfdbfe'/></g>"
                          "<text x='512' y='760' text-anchor='middle' font-family='Inter' font-weight='800' font-size='104' letter-spacing='-2'>"
                          "<tspan fill='#fff'>Yireh </tspan><tspan fill='#60a5fa'>Careers</tspan></text></svg>"),
}
for n, svg in VARIANTS.items():
    open(os.path.join(HERE, n + ".svg"), "w").write(svg)

js = textwrap.dedent(f"""
const {{ chromium }} = require('playwright');
const fs = require('fs');
(async () => {{
  const b = await chromium.launch();
  const font = "file://{ROOT}/fonts/inter-latin.woff2";
  for (const n of {list(VARIANTS)!r}) {{
    const svg = fs.readFileSync('{HERE}/' + n + '.svg', 'utf8');
    const p = await b.newPage({{ viewport: {{ width: 1024, height: 1024 }} }});
    await p.setContent(`<style>@font-face{{font-family:Inter;src:url(${{font}});font-weight:100 900}}body{{margin:0}}svg{{display:block;width:1024px;height:1024px}}</style>` + svg);
    await p.evaluate(() => document.fonts.ready);
    await p.screenshot({{ path: '{HERE}/' + n + '.png' }});
    await p.close();
  }}
  // circle preview at real sizes on a light and a dark chat list
  const p = await b.newPage({{ viewport: {{ width: 900, height: 330 }}, deviceScaleFactor: 2 }});
  const row = (bg, fg) => `<div style="background:${{bg}};color:${{fg}};padding:18px 22px;border-radius:12px;margin-bottom:14px;font:14px Inter,sans-serif">` +
    {list(VARIANTS)!r}.map(n => `<span style="display:inline-block;text-align:center;margin-right:34px"><img src="data:image/png;base64,${{fs.readFileSync('{HERE}/' + n + '.png').toString('base64')}}" style="border-radius:50%;width:96px;height:96px;display:block"><img src="data:image/png;base64,${{fs.readFileSync('{HERE}/' + n + '.png').toString('base64')}}" style="border-radius:50%;width:40px;height:40px;margin-top:10px"><br><small>${{n}}</small></span>`).join('') + '</div>';
  await p.setContent(`<style>@font-face{{font-family:Inter;src:url(${{font}});font-weight:100 900}}body{{margin:0;padding:10px;background:#888}}</style>` + row('#ffffff', '#111') + row('#111b21', '#e9edef'));
  await p.screenshot({{ path: '{HERE}/preview-circles.png', fullPage: true }});
  await b.close();
}})();
""")
open("/tmp/_profile.js", "w").write(js)
subprocess.run(["node", "/tmp/_profile.js"], check=True, cwd=ROOT)
print("built:", ", ".join(VARIANTS), "+ preview-circles.png")
