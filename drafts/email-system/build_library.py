"""Builds the reviewable email library from email_data.py.

Run: python3 drafts/email-system/build_library.py
Writes: drafts/email-system/11-email-inventory.md, copy/0*.md (one per stage), preview/*.html and preview/index.html.
Nothing is sent and nothing in Brevo is touched. Brevo merge tags are kept in the HTML: {{ contact.FIRSTNAME | default:"there" }}
and {{ unsubscribe }}; the preview files substitute a sample name and a dummy link so they open in any browser.
"""
import html
import os
import re
import sys
import json
import datetime as D
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import email_data as ed  # noqa: E402

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


def render_digest_cards(rows, now):
    import make_digest as md
    sections, total = md.pick(rows, now)
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


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(text)


def email_md(e):
    b = body_text(e)
    url = cta_url(e)
    lines = [f"### {e['id']} · {e['name']}", "",
             "| Field | Value |", "|---|---|",
             f"| Class | **{e['cls']}** ({'subscribed content' if e['cls']=='S' else 'promotional or relationship' if e['cls']=='P' else 'operational'}) · channel: {e['channel']} |",
             f"| Journey | {e['journey']} |",
             f"| Audience | {e['audience']} |",
             f"| Purpose | {e['purpose']} |",
             f"| Trigger | {e['trigger']} |",
             f"| Entry conditions | {e['entry']} |",
             f"| Permission | {e['consent']} |",
             f"| Timing | {e['timing']} |",
             f"| Frequency | {e['freq']} |",
             f"| Exit and suppression | {e['exit']} (a blocklisted contact never receives any Brevo email) |",
             f"| Failure handling | {e['failure']} |",
             f"| Primary metric / guardrail | {e['metric']} / {e['guardrail']} |",
             f"| Evidence and confidence | {e['evidence']} Confidence: **{e['confidence']}** |",
             f"| Body length | {words(b)} words |", "", f"**Subject:** {e['subject']}  "]
    if e["preview"]:
        lines.append(f"**Preview text:** {e['preview']}  ")
    if url:
        lines.append(f"**Button:** {e['cta'][0]}  ")
        lines.append(f"**Link:** `{url}`  ")
    lines += ["", "```", b.replace("[First name]", "[First name]"), "```", ""]
    if e["cls"] != "O":
        lines.append(f"Rendered preview: `preview/{e['id']}.html`\n")
    return "\n".join(lines)


def main():
    now = D.datetime.now(D.timezone.utc)
    rows = json.load(open(os.path.join(ROOT, "jobs.json"), encoding="utf-8"))
    cards, total, shown = render_digest_cards(rows, now)
    by_stage = {}
    for e in ed.EMAILS:
        by_stage.setdefault(e["stage"], []).append(e)
        if e["cls"] in ("S", "P"):
            if e["id"] == "JA-D":
                doc = render_html(e, True, cards, total, shown)
            else:
                doc = render_html(e, True)
            write(os.path.join(HERE, "preview", f"{e['id']}.html"), doc)
    for stage, items in sorted(by_stage.items()):
        intro = {
            "05-operational": "These are plain-text emails sent by hand from yirehcareers@gmail.com as Gmail templates (Settings, Advanced, Templates). They replace `drafts/gmail-customer-emails.md`. They carry no promotion. Square brackets are filled in by KT. Signature: **The Yireh Careers team**, then one line with the WhatsApp number.\n",
        }.get(stage, "Brevo emails: designed as a calm single-column letter (see `copy/00-design-and-voice.md`). Merge tags: first name uses `{{ contact.FIRSTNAME | default:\"there\" }}`; unsubscribe uses `{{ unsubscribe }}`.\n")
        write(os.path.join(HERE, "copy", f"{stage}.md"),
              f"# {ed.STAGE_TITLES[stage]}\n\nGenerated by `build_library.py` from `email_data.py`. Edit the data file, not this file. Status: PROPOSED, not approved.\n\n{intro}\n" +
              "\n---\n\n".join(email_md(e) for e in items))
    # inventory
    inv = ["# 11 · Email inventory and copy library index", "",
           "Status: PROPOSED (Phase 9 deliverable). Generated by `build_library.py`. **29 emails.** Full copy, fields and links are in `copy/` (one file per stage); rendered previews of the 13 Brevo emails are in `preview/index.html`.", "",
           "Classes: **S** subscribed content (Brevo, consent: job alerts) · **P** promotional or relationship (Brevo, consent: tips and offers) · **O** operational (Gmail, by hand, no promotion).", "",
           "| ID | Name | Class | Channel | Trigger | Permission | Timing | Subject | Words | Confidence |", "|---|---|---|---|---|---|---|---|---|---|"]
    for e in ed.EMAILS:
        inv.append(f"| {e['id']} | {e['name']} | {e['cls']} | {e['channel']} | {e['trigger']} | {e['consent']} | {e['timing']} | {e['subject']} | {words(body_text(e))} | {e['confidence']} |")
    inv += ["", "## Single email or sequence?", "",
            "| Flow | Decision | Why |", "|---|---|---|",
            "| Job-alert welcome | One email | Nothing more to add; the digest is the follow-up |",
            "| Tips | Three-email intro, then monthly | Each adds new information (check, AI checklist, facts and price); stop at three |",
            "| Free-check follow-up | One email | A second would repeat the same offer |",
            "| After the order | Two emails, days 21 and 60, by package | Different jobs: what comes next, then a check-in |",
            "| Service stages | One per stage | Each stage has its own job |",
            "| Dormant check | One email, quarterly | One question deserves one email |", "",
            "## Frequency and caps", "",
            "- Promotional (P): at most 2 per rolling 14 days per person; one or two a month after the intro.",
            "- Subscribed content (S): the weekly digest, one per week.",
            "- Operational (O): as the order needs; no promotion inside.",
            "- No P email within 14 days of a completed order except as scheduled in the table above.", ""]
    write(os.path.join(HERE, "11-email-inventory.md"), "\n".join(inv))
    # preview index
    idx = ["<!DOCTYPE html><html lang='en'><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Email previews</title>",
           "<style>body{font-family:system-ui,sans-serif;max-width:860px;margin:32px auto;padding:0 16px;color:#1c2733}li{margin:6px 0}small{color:#5b6877}</style>",
           "<h1>Yireh Careers: email previews</h1><p>Proposed designs, not sent. Sample name \"Amara\". The digest uses real jobs from jobs.json.</p><ul>"]
    for e in ed.EMAILS:
        if e["cls"] in ("S", "P"):
            idx.append(f"<li><a href='{e['id']}.html'><strong>{e['id']}</strong> {html.escape(e['name'])}</a> <small>({e['cls']}) &middot; subject: {html.escape(e['subject'])}</small></li>")
    idx.append("</ul>")
    write(os.path.join(HERE, "preview", "index.html"), "\n".join(idx))
    print("emails:", len(ed.EMAILS), "| brevo previews:", sum(1 for e in ed.EMAILS if e['cls'] in ('S', 'P')))


if __name__ == "__main__":
    main()
