"""Builds mail.html: the private "Reply templates" page for the order and service emails sent from Gmail.

Run: python3 scripts/build_mail_page.py
The copy comes from scripts/email_data.py (class O emails). Each template is rendered in a paste-safe version of the
Yireh Careers letter design (inline styles only, no dark-mode CSS, no tables for layout) so it survives a paste into
a Gmail compose window. The page lets KT fill in the first name and package, edit anything else in place, and copy the
result as formatted text. The page holds no customer data: everything stays in the browser.
"""
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import email_data as ed  # noqa: E402

TX, MUT, BRAND, ACC = "#1c2733", "#5b6877", "#0f2a4d", "#1d4ed8"
GROUPS = [
    ("Free CV check", ["OP-1", "OP-13", "OP-15", "OP-2"]),
    ("Orders", ["OP-3", "OP-16", "OP-4", "OP-5", "OP-6", "OP-7"]),
    ("Executive and LinkedIn Growth", ["OP-8", "OP-9", "OP-10", "OP-11"]),
    ("Privacy and stop requests", ["OP-12", "OP-14"]),
]
P = f'margin:0 0 16px;font-size:16px;line-height:1.6;color:{TX};'


def top_level_groups(s):
    """Split s into ('text', str) and ('gap', str) parts; a gap is a whole top-level [...] group, nested ones included."""
    out, depth, start, last = [], 0, 0, 0
    for i, ch in enumerate(s):
        if ch == "[":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "]" and depth:
            depth -= 1
            if depth == 0:
                if start > last:
                    out.append(("text", s[last:start]))
                out.append(("gap", s[start:i + 1]))
                last = i + 1
    if last < len(s):
        out.append(("text", s[last:]))
    return out


def inline(text):
    t = html.escape(text, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", lambda m: f'<a href="{m.group(2)}" style="color:{ACC};">{m.group(1)}</a>', t)
    t = t.replace("{FIRST}", "[First name]")
    parts = []
    for kind, s in top_level_groups(t):
        if kind == "text":
            parts.append(s)
        elif s == "[First name]":
            parts.append(f'<mark class="gap" data-f="first">{s}</mark>')
        elif s == "[Package]":
            parts.append(f'<mark class="gap" data-f="package">{s}</mark>')
        else:
            parts.append(f'<mark class="gap">{s}</mark>')
    return "".join(parts)


def body_html(email):
    out = []
    for kind, val in email["body"]:
        if kind == "p":
            out.append(f'<p style="{P}">{inline(val)}</p>')
        elif kind == "ul":
            lis = "".join(f'<li style="margin:0 0 8px;">{inline(i)}</li>' for i in val)
            out.append(f'<ul style="margin:0 0 16px;padding:0 0 0 22px;font-size:16px;line-height:1.6;color:{TX};">{lis}</ul>')
        elif kind == "kv":
            rows = "".join(f'<p style="margin:0 0 4px;font-size:16px;line-height:1.5;color:{TX};"><span style="color:{MUT};">{html.escape(k)}:</span> '
                           f'<strong>{inline(v)}</strong></p>' for k, v in val)
            out.append(f'<div style="margin:0 0 16px;">{rows}</div>')
    return "\n".join(out)


def build():
    by_id = {e["id"]: e for e in ed.EMAILS if e["cls"] == "O"}
    listed = [i for _, ids in GROUPS for i in ids]
    assert sorted(listed) == sorted(by_id), (set(by_id) ^ set(listed))
    data = []
    for g, ids in GROUPS:
        for i in ids:
            e = by_id[i]
            text = json.dumps(e["body"])
            data.append({
                "id": i, "group": g, "name": e["name"], "subject": e["subject"], "when": f'{e["trigger"]} ({e["timing"][0].lower() + e["timing"][1:]})',
                "attach": "attached" in text.lower(), "html": body_html(e),
            })
    cfg = {"logo": f"{ed.SITE}/yc-logo.png", "sign": ed.SIGN, "address": ed.ADDRESS, "tx": TX, "mut": MUT, "brand": BRAND, "acc": ACC}
    page = TEMPLATE.replace("/*DATA*/", json.dumps(data, ensure_ascii=False).replace("</", "<\\/")) \
                   .replace("/*CFG*/", json.dumps(cfg, ensure_ascii=False))
    return page


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Reply templates — Yireh Careers</title>
  <meta name="robots" content="noindex, nofollow">
  <meta name="referrer" content="no-referrer">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="preload" href="/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/fonts/inter.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    :root {
      --bg: #f8f9fb; --surface: #ffffff; --text: #1a1a2e; --text-secondary: #5f6368; --accent: #2563eb;
      --accent-hover: #1d4ed8; --border: #e2e5e9; --green: #0d9488; --warn-bg: #fef3c7; --warn-text: #78350f; --radius: 10px;
    }
    @media (prefers-color-scheme: dark) {
      :root:not([data-theme="light"]) {
        --bg: #0c0c18; --surface: #161625; --text: #e8e8f0; --text-secondary: #9ca3af; --accent: #60a5fa;
        --accent-hover: #93bbfd; --border: #262640; --green: #2dd4bf; --warn-bg: #3a2e12; --warn-text: #f5d58a; color-scheme: dark;
      }
    }
    body { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; background: var(--bg); color: var(--text); line-height: 1.55; -webkit-font-smoothing: antialiased; }
    .wrap { max-width: 860px; margin: 0 auto; padding: 1.5rem 1rem 4rem; }
    h1 { font-size: clamp(1.4rem, 4vw, 1.9rem); font-weight: 800; letter-spacing: -0.5px; margin-bottom: 0.4rem; }
    .lead { color: var(--text-secondary); font-size: 0.95rem; margin-bottom: 1.25rem; max-width: 64ch; }
    .controls { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 1rem; display: grid; gap: 0.9rem; margin-bottom: 1rem; }
    .row { display: flex; gap: 1rem; flex-wrap: wrap; align-items: flex-end; }
    label { font-size: 0.8rem; font-weight: 700; display: grid; gap: 0.3rem; color: var(--text-secondary); min-width: 0; }
    label.inline { display: flex; align-items: center; gap: 0.45rem; font-weight: 600; }
    select, input[type=text] { font: inherit; font-size: 0.95rem; background: var(--surface); color: var(--text); border: 1px solid var(--border); border-radius: 6px; padding: 0.45rem 0.55rem; min-width: 12rem; max-width: 100%; }
    .grow { flex: 1 1 18rem; } .grow input, .grow select { width: 100%; }
    button { font: inherit; }
    .btn { background: var(--accent); color: #fff; border: none; border-radius: 8px; padding: 0.6rem 1.1rem; font-weight: 700; font-size: 0.9rem; cursor: pointer; }
    .btn:hover { background: var(--accent-hover); }
    .btn.secondary { background: transparent; color: var(--accent); border: 1px solid var(--accent); }
    .btn:focus-visible, select:focus-visible, input:focus-visible, #editor:focus-visible { outline: 3px solid var(--accent); outline-offset: 2px; }
    .hint { font-size: 0.85rem; color: var(--text-secondary); }
    .hint strong { color: var(--text); }
    .paper { background: #ffffff; color: #1c2733; border: 1px solid var(--border); border-radius: var(--radius); padding: 1.4rem 1.2rem; margin-bottom: 0.8rem; overflow-x: auto; }
    #editor { max-width: 600px; margin: 0 auto; }
    mark.gap { background: #fff3a3; color: #1c2733; border-radius: 3px; padding: 0 2px; }
    mark.gap.filled { background: transparent; padding: 0; }
    .actions { display: flex; gap: 0.6rem; flex-wrap: wrap; align-items: center; margin-bottom: 0.6rem; }
    #status { font-size: 0.85rem; font-weight: 700; }
    #status.ok { color: var(--green); } #status.warn { color: var(--warn-text); background: var(--warn-bg); padding: 0.25rem 0.6rem; border-radius: 6px; }
    .steps { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 1rem 1.2rem; margin-top: 1.4rem; font-size: 0.88rem; }
    .steps h2 { font-size: 1rem; font-weight: 800; margin-bottom: 0.4rem; }
    .steps ol, .steps ul { padding-left: 1.2rem; display: grid; gap: 0.3rem; margin: 0.4rem 0; }
    .rules { background: var(--warn-bg); color: var(--warn-text); border-radius: var(--radius); padding: 0.9rem 1rem; font-size: 0.85rem; margin-top: 1rem; }
  </style>
</head>
<body>
<div class="wrap">
  <h1>Reply templates</h1>
  <p class="lead">The order and service emails, in the same look as our Brevo emails, ready to paste into Gmail. Pick one, type the name and package, change anything else right in the preview, then copy. This page is unlisted and not indexed, and it keeps nothing you type.</p>

  <div class="controls">
    <div class="row">
      <label class="grow">Template
        <select id="tpl"></select>
      </label>
    </div>
    <div class="row">
      <label>First name <input type="text" id="first" placeholder="e.g. Amara" autocomplete="off"></label>
      <label>Package
        <select id="pkg">
          <option value="">(choose)</option>
          <option>Essential package</option><option>Professional package</option><option>Executive package</option>
        </select>
      </label>
      <label class="inline"><input type="checkbox" id="logo" checked> Include the logo</label>
    </div>
    <div class="row">
      <label class="grow">Subject line <input type="text" id="subject" autocomplete="off"></label>
    </div>
    <p class="hint" id="when"></p>
  </div>

  <div class="paper"><div id="editor" contenteditable="true" spellcheck="true"></div></div>
  <div class="actions">
    <button class="btn" id="copy">Copy email</button>
    <button class="btn secondary" id="copySubject">Copy subject</button>
    <span id="status" role="status"></span>
  </div>
  <p class="hint">Yellow means "still to fill in". Click into the preview and type over it, or delete a paragraph you don't need. The yellow never reaches Gmail.</p>

  <div class="steps">
    <h2>In Gmail, every time</h2>
    <ol>
      <li>In yirehcareers@gmail.com, open the client's email thread and click <strong>Reply</strong> (or <strong>Compose</strong> for a new email).</li>
      <li>Here: choose the template, fill in the name and package, edit the rest, tap <strong>Copy email</strong>.</li>
      <li>In Gmail, click in the message body and paste (Ctrl+V, or Cmd+V on a Mac). Then tap <strong>Copy subject</strong> here and paste it into the subject (leave the subject alone when replying in a thread).</li>
      <li>Attach any files. Read it once, then send.</li>
    </ol>
    <p class="hint">If a template is also in your Gmail "Templates", ignore that copy: this page is the up-to-date one.</p>
  </div>

  <div class="rules">
    <strong>Check before the first real send:</strong>
    <ul>
      <li>Send yourself one first (from this page to kaetooruche@gmail.com) and open it on your phone. Pasted logos and layout can look different in each mail app. If the logo doesn't show, untick "Include the logo".</li>
      <li>Service emails carry no offers, prices or promotion. Don't add any (the only prices are the ones already in the templates).</li>
      <li>Never paste a CV or bank details into this page. It doesn't need them.</li>
    </ul>
  </div>
</div>

<script>
(function () {
  var DATA = /*DATA*/;
  var CFG = /*CFG*/;
  var sel = document.getElementById('tpl'), editor = document.getElementById('editor'), subj = document.getElementById('subject');
  var first = document.getElementById('first'), pkg = document.getElementById('pkg'), logo = document.getElementById('logo');
  var statusEl = document.getElementById('status'), whenEl = document.getElementById('when');
  var armed = false, armTimer = null;

  var g = '';
  DATA.forEach(function (d, i) {
    if (d.group !== g) { g = d.group; var og = document.createElement('optgroup'); og.label = g; sel.appendChild(og); }
    var o = document.createElement('option'); o.value = i; o.textContent = d.name; sel.lastChild.appendChild(o);
  });

  function header() {
    return '<table role="presentation" cellpadding="0" cellspacing="0" style="margin:0 0 6px;"><tr>' +
      '<td style="padding:0 10px 0 0;vertical-align:middle;"><img src="' + CFG.logo + '" width="32" height="32" alt="" style="display:block;border:0;border-radius:7px;width:32px;height:32px;"></td>' +
      '<td style="font-size:18px;font-weight:800;color:' + CFG.brand + ';vertical-align:middle;">Yireh Careers</td></tr></table>' +
      '<div style="width:34px;border-top:3px solid ' + CFG.acc + ';margin:0 0 22px;"></div>';
  }
  function load() {
    var d = DATA[sel.value];
    editor.innerHTML = '<div style="font-family:Arial,Helvetica,sans-serif;color:' + CFG.tx + ';max-width:560px;">' + header() + d.html +
      '<p style="margin:0 0 22px;font-size:16px;line-height:1.5;color:' + CFG.tx + ';">Best,<br><strong>' + CFG.sign + '</strong></p>' +
      '<p style="margin:0;font-size:12px;line-height:1.5;color:' + CFG.mut + ';">Yireh Careers &middot; ' + CFG.address.replace('Yireh Careers, ', '') + '</p></div>';
    subj.value = d.subject;
    whenEl.innerHTML = '<strong>When to send:</strong> ' + d.when + (d.attach ? ' <strong>Remember to attach the file.</strong>' : '');
    applyField('first'); applyField('package'); logoToggle(); disarm(); status('', '');
  }
  function applyField(kind) {
    var v = (kind === 'first' ? first.value : pkg.value).trim(), token = kind === 'first' ? '[First name]' : '[Package]';
    editor.querySelectorAll('mark[data-f="' + kind + '"]').forEach(function (m) {
      m.textContent = v || token; m.classList.toggle('filled', !!v);
    });
  }
  function logoToggle() {
    var img = editor.querySelector('img'); if (img) img.style.display = logo.checked ? 'block' : 'none';
  }
  function gaps() {
    var n = 0;
    editor.querySelectorAll('mark').forEach(function (m) { if (/[\[\]]/.test(m.textContent)) n++; });
    if (/[\[\]]/.test(subj.value)) n++;
    return n;
  }
  function status(t, cls) { statusEl.textContent = t; statusEl.className = cls || ''; }
  function disarm() { armed = false; clearTimeout(armTimer); }

  function clean() {
    var c = editor.cloneNode(true); c.removeAttribute('contenteditable'); c.removeAttribute('id'); c.removeAttribute('spellcheck');
    c.querySelectorAll('mark').forEach(function (m) { m.replaceWith.apply(m, Array.prototype.slice.call(m.childNodes)); });
    if (!logo.checked) { var img = c.querySelector('img'); if (img && img.closest('td')) img.closest('td').remove(); }
    else { var im = c.querySelector('img'); if (im) im.style.display = 'block'; }
    return c;
  }
  function copyRich() {
    var box = document.createElement('div');
    box.style.cssText = 'position:fixed;left:-9999px;top:0;width:600px;background:#fff;';
    box.appendChild(clean()); document.body.appendChild(box);
    var htmlStr = box.innerHTML, text = box.innerText;
    function fallback() {
      var r = document.createRange(); r.selectNodeContents(box);
      var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
      var ok = false; try { ok = document.execCommand('copy'); } catch (e) {}
      s.removeAllRanges(); document.body.removeChild(box); return ok;
    }
    if (navigator.clipboard && window.ClipboardItem) {
      navigator.clipboard.write([new ClipboardItem({ 'text/html': new Blob([htmlStr], { type: 'text/html' }), 'text/plain': new Blob([text], { type: 'text/plain' }) })])
        .then(function () { document.body.removeChild(box); done(true); }, function () { done(fallback()); });
    } else { done(fallback()); }
  }
  function done(ok) { status(ok ? 'Copied. Paste it into Gmail.' : 'Copy was blocked. Select the preview and copy it by hand.', ok ? 'ok' : 'warn'); }

  document.getElementById('copy').addEventListener('click', function () {
    var n = gaps();
    if (n && !armed) {
      armed = true; armTimer = setTimeout(disarm, 10000);
      status(n + ' gap' + (n === 1 ? '' : 's') + ' still in [brackets]. Fill them in, or tap Copy again to copy anyway.', 'warn'); return;
    }
    disarm(); copyRich();
  });
  document.getElementById('copySubject').addEventListener('click', function () {
    var t = subj.value;
    function ok() { status('Subject copied.', 'ok'); }
    if (navigator.clipboard) navigator.clipboard.writeText(t).then(ok, function () { subj.select(); document.execCommand('copy'); ok(); });
    else { subj.select(); document.execCommand('copy'); ok(); }
  });
  sel.addEventListener('change', load);
  first.addEventListener('input', function () { applyField('first'); disarm(); });
  pkg.addEventListener('change', function () { applyField('package'); disarm(); });
  logo.addEventListener('change', logoToggle);
  editor.addEventListener('input', disarm);
  load();
})();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    out = os.path.join(ROOT, "mail.html")
    open(out, "w", encoding="utf-8").write(build())
    print("wrote mail.html with", sum(len(ids) for _, ids in GROUPS), "templates")
