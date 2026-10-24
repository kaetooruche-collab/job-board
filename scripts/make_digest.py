"""Builds the weekly jobs email from jobs.json: data/weekly_digest.html and data/weekly_digest.txt.
Run: python3 scripts/make_digest.py
Rules (CLAUDE.md copy rules + drafts/voice-and-copy-guide.md): only roles that read as remote and were posted in the last 7 days;
one per company; clear eligibility first; a spread of levels; no promotion inside the digest; every link goes to the employer's own posting.
KT sends the campaign by hand in Brevo (list: Job alert subscribers; exclude: Do not send)."""
import json, os, html, datetime as D

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://yirehcareers.vercel.app"
WA = "905338225854"
ADDR = "Yireh Careers · Yenice Sokak, 99300 Kyrenia, Cyprus"
EARLY = ("internship", "entry", "junior")
LEVEL = {"internship": "Internship", "entry": "Entry level", "junior": "Junior", "mid": "Mid level",
         "senior": "Senior", "leadership": "Leadership", "unspecified": "Level not stated"}
TOTAL = 6


def load():
    return json.load(open(os.path.join(ROOT, "jobs.json"), encoding="utf-8"))


def age_days(r, now):
    return (now - D.datetime.fromisoformat(r["postedAt"].replace("Z", "+00:00"))).total_seconds() / 86400


def openness(r):
    t = (r.get("eligibility") or {}).get("type")
    return {"worldwide": 3, "region": 2, "countries": 1}.get(t, 0)


def pick(rows, now):
    pool = [r for r in rows if r["workArrangement"] in ("fully_remote", "remote_geo_restricted")
            and 0 <= age_days(r, now) <= 7 and (r.get("eligibility") or {}).get("type") not in ("unclear", "timezone")]
    pool.sort(key=lambda r: r["postedAt"], reverse=True)
    pool.sort(key=lambda r: -openness(r))
    bands = [("Starting out", lambda r: r["level"] in EARLY, 2), ("Mid-level", lambda r: r["level"] == "mid", 2),
             ("Senior and leadership", lambda r: r["level"] in ("senior", "leadership"), 2)]
    chosen, companies = [], set()

    def take(r):
        c = r["company"].strip().lower()
        if c in companies:
            return False
        companies.add(c); chosen.append(r); return True

    sections = []
    for name, test, n in bands:
        items = []
        for r in pool:
            if len(items) >= n:
                break
            if test(r) and take(r):
                items.append(r)
        sections.append((name, items))
    # top up to TOTAL from the rest, newest first, keeping one per company
    for r in sorted(pool, key=lambda r: r["postedAt"], reverse=True):
        if sum(len(i) for _, i in sections) >= TOTAL:
            break
        if take(r):
            name = "Starting out" if r["level"] in EARLY else "Mid-level" if r["level"] == "mid" else "Senior and leadership"
            dict(sections)[name].append(r)
    return [(n, i) for n, i in sections if i], len([r for r in rows if r["workArrangement"] in ("fully_remote", "remote_geo_restricted") and 0 <= age_days(r, now) <= 7])


def ago(r, now):
    d = int(age_days(r, now))
    return "today" if d == 0 else "1 day ago" if d == 1 else f"{d} days ago"


def build(rows=None, now=None):
    rows = rows or load()
    now = now or D.datetime.now(D.timezone.utc)
    sections, new_total = pick(rows, now)
    shown = sum(len(i) for _, i in sections)
    e = lambda s: html.escape(s or "", quote=True)
    body = []
    body.append('<p style="margin:0 0 14px;">Hi {{ contact.FIRSTNAME | default:"there" }},</p>')
    body.append(f'<p style="margin:0 0 18px;">{new_total} new remote jobs went up this week. Here are {shown} to start with. Each one links to the employer\'s own posting.</p>')
    for name, items in sections:
        body.append(f'<p style="margin:18px 0 8px;font:700 13px Arial,Helvetica,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:#1d4f91;">{e(name)}</p>')
        for r in items:
            pay = f' · {e(r["salaryText"])}' if r.get("salaryText") else ""
            label = (r.get("eligibility") or {}).get("label") or "Eligibility unclear"
            body.append(
                '<div style="margin:0 0 14px;padding:0 0 14px;border-bottom:1px solid #e3e9f3;">'
                f'<a href="{e(r["sourceUrl"])}" style="font-weight:700;font-size:17px;color:#1d4f91;text-decoration:none;">{e(r["title"].strip())}</a>'
                f'<div style="font-size:14px;color:#55627a;margin-top:2px;">{e(r["company"])} · {e(LEVEL.get(r["level"], ""))} · Who can apply: {e(label)}{pay} · Posted {ago(r, now)}</div></div>')
    body.append('<p style="margin:6px 0 14px;font-size:14px;color:#55627a;">Employers decide who they can hire, so check their rules for your country before you apply.</p>')
    cta = f"{SITE}/?utm_source=brevo&utm_medium=email&utm_campaign=weekly-digest"
    subject = f"This week's remote jobs: {shown} to start with"
    preview = f"{new_total} new listings, each linked to the employer's own posting."
    doc = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light dark"><meta name="supported-color-schemes" content="light dark">
<title>Yireh Careers</title>
<style>
@media (prefers-color-scheme: dark){{ .bg{{background:#0b1220!important}} .card{{background:#131c2e!important}} .tx{{color:#e6ebf5!important}} }}
@media only screen and (max-width:620px){{ .wrap{{width:100%!important}} .pad{{padding:22px 18px!important}} }}
</style></head>
<body class="bg" style="margin:0;padding:0;background:#eef2f8;">
<div style="display:none;max-height:0;overflow:hidden;opacity:0;">{html.escape(preview, quote=False)}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" class="bg" style="background:#eef2f8;"><tr><td align="center" style="padding:24px 12px;">
<table role="presentation" class="wrap" width="600" cellpadding="0" cellspacing="0" style="width:600px;max-width:100%;">
<tr><td style="background:#0f2a4d;padding:18px 28px;border-radius:12px 12px 0 0;font:700 20px Arial,Helvetica,sans-serif;color:#ffffff;">Yireh Careers</td></tr>
<tr><td class="card pad" style="background:#ffffff;padding:28px;font:16px/1.65 Arial,Helvetica,sans-serif;color:#1b2536;">
<div class="tx">{''.join(body)}
<p style="margin:22px 0 22px;"><a href="{cta}" style="display:inline-block;background:#1d4f91;color:#ffffff;text-decoration:none;font-weight:700;padding:13px 24px;border-radius:8px;">See all {new_total} new jobs</a></p>
<p style="margin:0;">Thanks,<br><strong>The Yireh Careers team</strong></p></div></td></tr>
<tr><td style="background:#0f2a4d;padding:18px 28px;border-radius:0 0 12px 12px;font:12.5px/1.6 Arial,Helvetica,sans-serif;color:#b9cdea;">
<p style="margin:0;">Reply to this email any time, or message us on WhatsApp: <a href="https://wa.me/{WA}" style="color:#9db4d6;">+90 533 822 5854</a></p>
<p style="margin:6px 0 0;">{ADDR}</p>
<p style="margin:6px 0 0;">You're getting this because you signed up with Yireh Careers. <a href="{{{{ unsubscribe }}}}" style="color:#9db4d6;">Unsubscribe</a></p></td></tr>
</table></td></tr></table></body></html>"""
    return doc, subject, preview, sections, new_total, now


def main():
    doc, subject, preview, sections, new_total, now = build()
    out = os.path.join(ROOT, "data")
    open(os.path.join(out, "weekly_digest.html"), "w", encoding="utf-8").write(doc)
    name = "Weekly jobs " + now.strftime("%Y-%m-%d")
    open(os.path.join(out, "weekly_digest.txt"), "w", encoding="utf-8").write(
        f"Campaign name: {name}\nSubject: {subject}\nPreview text: {preview}\nList: Job alert subscribers. Exclude: Do not send.\n"
        "Suggested send: Tuesday morning, then compare with another day (no evidence yet for the best day).\n\n" +
        "\n".join(f"[{n}] {r['title']} at {r['company']} ({r['level']}, {(r.get('eligibility') or {}).get('label')}) {r['sourceUrl']}" for n, i in sections for r in i) + "\n")
    print(name, "|", subject, "|", sum(len(i) for _, i in sections), "jobs shown of", new_total, "new this week")


if __name__ == "__main__":
    main()
