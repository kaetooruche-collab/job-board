"""Shared renderer for the Yireh Careers emails (single column letter design, light and dark mode).

Used by scripts/make_digest.py (the weekly digest) and drafts/email-system/build_library.py (previews and copy files).
Copy and metadata live in scripts/email_data.py. Brevo merge tags are kept in the HTML:
{{ contact.FIRSTNAME | default:"there" }} and {{ unsubscribe }}; preview mode swaps in a sample name and a dummy link.
"""
import html
import re
from urllib.parse import quote

import email_data as ed

BREVO_FIRST = '{{ contact.FIRSTNAME | default:"there" }}'
SAMPLE_FIRST = "Amara"

# Light tokens first, then the dark overrides used inside the <style> block (see render_html).
C = dict(bg="#f3f0e8", card="#ffffff", tx="#1c2733", mut="#5b6877", brand="#0f2a4d", acc="#1d4ed8", rule="#e6e1d6",
         chip="#d9dee6")


def words(text):
    return len(re.findall(r"[A-Za-z0-9$%'’][A-Za-z0-9$%'’.,-]*", text))


def body_text(email, with_first=True):
    """Plain text of the body blocks, used for word counts, lint and the text version."""
    out = []
    for kind, val in email["body"]:
        if kind == "p":
            out.append(val)
        elif kind == "ul":
            out.extend("- " + i for i in val)
        elif kind == "kv":
            out.extend(f"{k}: {v}" for k, v in val)
    t = "\n\n".join(out)
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", t)
    t = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r"\1 (\2)", t)
    return t.replace("{FIRST}", "[First name]" if with_first else SAMPLE_FIRST)


def cta_url(email):
    cta = email.get("cta")
    if not cta:
        return None
    label, key = cta
    if key.startswith("wa:"):
        code, text = key[3:].split("|", 1)
        return f"{ed.WA}?text={quote(text + ' (' + code + ')')}"
    base = ed.LINKS[key]
    frag = ""
    if "#" in base:
        base, frag = base.split("#", 1)
        frag = "#" + frag
    sep = "&" if "?" in base else "?"
    return (f"{base}{sep}utm_source=brevo&utm_medium=email&utm_campaign={email['id'].lower()}"
            f"&utm_content={email.get('utm') or 'cta'}{frag}")


def inline(text):
    t = html.escape(text, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", lambda m: f'<a class="lnk" href="{m.group(2)}" style="color:{C["acc"]};">{m.group(1)}</a>', t)
    return t


def blocks_html(email, first):
    out = []
    p_style = f'margin:0 0 18px;font-size:17px;line-height:1.65;color:{C["tx"]};'
    for kind, val in email["body"]:
        if kind == "p":
            out.append(f'<p class="tx" style="{p_style}">{inline(val).replace("{FIRST}", first)}</p>')
        elif kind == "ul":
            lis = "".join(f'<li class="tx" style="margin:0 0 8px;">{inline(i)}</li>' for i in val)
            out.append(f'<ul class="tx" style="margin:0 0 18px;padding:0 0 0 22px;font-size:17px;line-height:1.6;color:{C["tx"]};">{lis}</ul>')
        elif kind == "kv":
            rows = "".join(
                f'<tr><td class="mut" style="padding:6px 16px 6px 0;font-size:15px;color:{C["mut"]};white-space:nowrap;vertical-align:top;">{html.escape(k)}</td>'
                f'<td class="tx" style="padding:6px 0;font-size:16px;color:{C["tx"]};">{html.escape(v)}</td></tr>' for k, v in val)
            out.append(f'<table role="presentation" cellpadding="0" cellspacing="0" style="margin:0 0 18px;">{rows}</table>')
    return "\n".join(out)


def button_html(label, url):
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" class="btn" style="margin:6px 0 26px;"><tr>'
            f'<td style="border-radius:8px;background:{C["acc"]};" bgcolor="{C["acc"]}">'
            f'<a href="{html.escape(url, quote=True)}" style="display:inline-block;padding:14px 26px;font-size:16px;font-weight:700;'
            f'line-height:1.2;color:#ffffff;text-decoration:none;border-radius:8px;">{html.escape(label)}</a></td></tr></table>')


FOOT = {
    "S": "You're getting this because you signed up for the weekly job email at yirehcareers.vercel.app.",
    "P": "This is a promotional email. You're getting it because you asked for CV and LinkedIn tips and offers from Yireh Careers.",
}

CSS = f"""
body,table,td,a{{-webkit-text-size-adjust:100%;}}
body{{margin:0;padding:0;}}
@media (prefers-color-scheme: dark){{
 .bg{{background:#0e131a!important}} .card{{background:#172029!important}} .tx{{color:#e7edf4!important}}
 .mut{{color:#9aa8b8!important}} .brand{{color:#a9c4ff!important}} .rule{{border-color:#263340!important}}
 .bar{{background:#6ea0ff!important}} .btn td{{background:#6ea0ff!important}} .btn a{{color:#0b1220!important}}
 .chip{{border-color:#33414f!important;color:#c9d4e0!important}} .chip-open{{background:#12301f!important;border-color:#1f5c3a!important;color:#9fe3b9!important}}
 a,.lnk{{color:#8db6ff!important}}
}}
@media only screen and (max-width:620px){{
 .wrap{{width:100%!important}} .pad{{padding:26px 20px!important}} .btn,.btn td,.btn a{{width:100%!important;box-sizing:border-box}}
 .btn a{{display:block!important;text-align:center!important}} h1{{font-size:23px!important}}
}}
"""


def shell(subject, preview, inner, footer_html, title=None):
    pre = html.escape(preview or "", quote=False)
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light dark"><meta name="supported-color-schemes" content="light dark">
<title>{html.escape(title or subject, quote=False)}</title>
<style>{CSS}</style></head>
<body class="bg" style="margin:0;padding:0;background:{C['bg']};font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;">
<div style="display:none;max-height:0;overflow:hidden;opacity:0;color:transparent;">{pre}&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" class="bg" style="background:{C['bg']};"><tr><td align="center" style="padding:28px 12px 36px;">
<table role="presentation" class="wrap" width="600" cellpadding="0" cellspacing="0" style="width:600px;max-width:100%;">
<tr><td class="card pad" style="background:{C['card']};border-radius:14px;padding:34px 40px 30px;">
<table role="presentation" cellpadding="0" cellspacing="0" style="margin:0 0 26px;"><tr><td class="brand" style="font-size:18px;font-weight:800;letter-spacing:-.01em;color:{C['brand']};padding:0 0 8px;white-space:nowrap;">Yireh Careers</td></tr>
<tr><td class="bar" style="height:3px;width:34px;background:{C['acc']};line-height:3px;font-size:3px;border-radius:2px;">&nbsp;</td></tr></table>
{inner}
</td></tr>
<tr><td class="mut" style="padding:20px 8px 0;font-size:13px;line-height:1.65;color:{C['mut']};">
{footer_html}
</td></tr></table></td></tr></table></body></html>"""


def render_html(email, preview_mode=True, digest_cards=None, n_total=None, shown=None):
    first = SAMPLE_FIRST if preview_mode else BREVO_FIRST
    subject = email["subject"].replace("{N}", str(n_total or 6)).replace("{SHOWN}", str(shown or 6))
    head = f'<h1 class="brand" style="margin:0 0 20px;font-size:26px;line-height:1.25;font-weight:800;letter-spacing:-.015em;color:{C["brand"]};">{html.escape(subject, quote=False)}</h1>'
    body = blocks_html(email, first).replace("{N}", str(n_total or 6)).replace("{SHOWN}", str(shown or 6))
    if digest_cards is not None:
        body = body.replace("[Job cards, generated by scripts/make_digest.py: title, company, level, who can apply, pay if stated, how long ago]", "§CARDS§")
        body = re.sub(r'<p[^>]*>§CARDS§</p>', digest_cards + '<div style="height:14px;line-height:14px;font-size:14px;">&nbsp;</div>', body)
    url = cta_url(email)
    btn = button_html(email["cta"][0].replace("{N}", str(n_total or 6)), url) if url else ""
    sign = f'<p class="tx" style="margin:0;font-size:17px;line-height:1.5;color:{C["tx"]};">Best,<br><strong>{ed.SIGN}</strong></p>'
    unsub = "#unsubscribe-link-goes-here" if preview_mode else "{{ unsubscribe }}"
    foot = (f'<p style="margin:0 0 8px;">{FOOT[email["cls"]]}</p>'
            f'<p style="margin:0 0 8px;">{html.escape(ed.ADDRESS)}</p>'
            f'<p style="margin:0;">Replies come to a real inbox. <a href="{unsub}" style="color:{C["mut"]};text-decoration:underline;">Unsubscribe</a> '
            f'(one tap) &middot; <a href="{ed.SITE}/privacy" style="color:{C["mut"]};text-decoration:underline;">Privacy</a></p>')
    return shell(subject, email["preview"], head + "\n" + body + "\n" + btn + "\n" + sign, foot)


def render_digest_cards(sections, total, now, md):
    """sections: output of make_digest.pick; md: the make_digest module (level labels and relative dates)."""
    out = []
    shown = 0
    for name, items in sections:
        out.append(f'<p class="mut" style="margin:24px 0 10px;font-size:12.5px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:{C["mut"]};">{html.escape(name)}</p>')
        for r in items:
            shown += 1
            elig = (r.get("eligibility") or {})
            label = elig.get("label") or "Eligibility unclear"
            open_ww = elig.get("type") == "worldwide"
            chip_cls = "chip chip-open" if open_ww else "chip"
            chip_style = ("background:#e6f4ea;border:1px solid #b6dfc3;color:#14532d;" if open_ww
                          else f'border:1px solid {C["chip"]};color:{C["tx"]};')
            pay = f' &middot; {html.escape(r["salaryText"])}' if r.get("salaryText") else ""
            out.append(
                f'<div class="rule" style="margin:0 0 4px;padding:0 0 16px;border-bottom:1px solid {C["rule"]};">'
                f'<a class="lnk" href="{html.escape(r["sourceUrl"], quote=True)}" style="font-size:18px;font-weight:700;line-height:1.35;color:{C["acc"]};text-decoration:none;">{html.escape(r["title"].strip(), quote=False)}</a>'
                f'<div class="mut" style="margin:4px 0 8px;font-size:15px;color:{C["mut"]};">{html.escape(r["company"], quote=False)} &middot; {html.escape(md.LEVEL.get(r["level"], ""))}{pay} &middot; {md.ago(r, now)}</div>'
                f'<span class="{chip_cls}" style="display:inline-block;padding:3px 10px;border-radius:999px;font-size:13px;font-weight:600;{chip_style}">Who can apply: {html.escape(label, quote=False)}</span></div>')
    return "\n".join(out), total, shown


