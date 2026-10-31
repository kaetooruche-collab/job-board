"""Builds the weekly jobs email from jobs.json: data/weekly_digest.html and data/weekly_digest.txt.
Run: python3 scripts/make_digest.py [--rename-note]
     python3 scripts/make_digest.py --country "Nigeria"   (an edition with only roles open to applicants in that country or worldwide)
     python3 scripts/make_digest.py --coverage            (how many of this week's roles are open to each country)
Copy and design now live in scripts/email_data.py (JA-D) and scripts/email_render.py (see drafts/email-system/).
Rules (CLAUDE.md copy rules + drafts/voice-and-copy-guide.md): only roles that read as remote and were posted in the last 7 days;
one per company; clear eligibility first; a spread of levels; no promotion inside the digest; every link goes to the employer's own posting.
KT sends the campaign by hand in Brevo to the list "Job alerts" (Brevo skips blocklisted contacts automatically)."""
import json, os, sys, html, datetime as D

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://yirehcareers.vercel.app"
WA = "905338225854"
ADDR = "Yireh Careers · Yenice Sokak, 99300 Kyrenia, Cyprus"
EARLY = ("internship", "entry", "junior")
LEVEL = {"internship": "Internship", "entry": "Entry level", "junior": "Junior", "mid": "Mid level",
         "senior": "Senior", "leadership": "Leadership", "unspecified": "Level not stated"}
TOTAL = 6
MIN_SHOWN = 3   # fewer than this: skip the week (email JA-D failure rule)


def load():
    return json.load(open(os.path.join(ROOT, "jobs.json"), encoding="utf-8"))


def age_days(r, now):
    return (now - D.datetime.fromisoformat(r["postedAt"].replace("Z", "+00:00"))).total_seconds() / 86400


def load_lexicon():
    return json.load(open(os.path.join(ROOT, "data", "geo_lexicon.json"), encoding="utf-8"))


def open_to(r, country, lexicon=None):
    """True only when the employer's own wording makes the role open to someone in `country`.
    Stricter than the site filter on purpose: an email must not promise what the posting does not say,
    so 'unclear', 'timezone' and an unknown region count as NOT open."""
    el = r.get("eligibility") or {}
    t = el.get("type")
    if t == "worldwide":
        return True
    if t == "countries":
        return country in (el.get("countries") or [])
    if t == "region":
        if country in (el.get("countries") or []):
            return True
        regions = (lexicon or {}).get("regions", {})
        return any(country in (regions.get(name) or {}).get("members", []) for name in (el.get("regions") or []))
    return False


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


def coverage(rows, now, lexicon):
    """{country: roles from the last 7 days that read as remote and are open to that country}, most first."""
    recent = [r for r in rows if r["workArrangement"] in ("fully_remote", "remote_geo_restricted") and 0 <= age_days(r, now) <= 7]
    counts = {c["name"]: sum(1 for r in recent if open_to(r, c["name"], lexicon)) for c in lexicon["countries"]}
    return dict(sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))), len(recent)


def build(rows=None, now=None, rename_note=False, country=None):
    """Returns (html, subject, preview, sections, new_total, now). Copy and design: scripts/email_data.py (JA-D) and scripts/email_render.py."""
    import email_data as ed
    import email_render as er
    rows = rows or load()
    now = now or D.datetime.now(D.timezone.utc)
    if country:
        lex = load_lexicon()
        rows = [r for r in rows if open_to(r, country, lex)]
    sections, new_total = pick(rows, now)
    cards, new_total, shown = er.render_digest_cards(sections, new_total, now, sys.modules[__name__])
    email = dict(next(e for e in ed.EMAILS if e["id"] == "JA-D"))
    if rename_note:   # one-off line for the first send after the rename from RemoteNC
        email["body"] = [email["body"][0], ("p", "A quick note: RemoteNC is now Yireh Careers. It's the same weekly job email, with the same one-tap unsubscribe.")] + list(email["body"][1:])
    if country:   # one plain sentence, placed right after the greeting line pair
        email["body"] = [email["body"][0], email["body"][1], ("p", f"You told us you can work from {country}, so these are roles whose posting names {country}, its region, or worldwide. Check each employer's rules before you apply.")] + list(email["body"][2:])
    doc = er.render_html(email, preview_mode=False, digest_cards=cards, n_total=new_total, shown=shown)
    subject = email["subject"].replace("{N}", str(new_total))
    preview = email["preview"]
    return doc, subject, preview, sections, new_total, now


def slug(country):
    return "".join(ch.lower() if ch.isalnum() else "-" for ch in country).strip("-")


def main():
    if "--coverage" in sys.argv:
        counts, total = coverage(load(), D.datetime.now(D.timezone.utc), load_lexicon())
        print(f"{total} remote roles posted in the last 7 days. Roles open to each country (top 40):")
        for c, n in list(counts.items())[:40]:
            print(f"  {n:4d}  {c}{'' if n >= MIN_SHOWN else '  (too few for an edition)'}")
        return
    country = None
    if "--country" in sys.argv:
        country = sys.argv[sys.argv.index("--country") + 1]
        if country not in [c["name"] for c in load_lexicon()["countries"]]:
            sys.exit(f"Unknown country {country!r}: use a name exactly as it appears in data/geo_lexicon.json")
    doc, subject, preview, sections, new_total, now = build(rename_note="--rename-note" in sys.argv, country=country)
    if sum(len(i) for _, i in sections) < MIN_SHOWN:
        print(f"Only {sum(len(i) for _, i in sections)} qualifying roles: skip this week, do not send an empty digest.")
        return
    out = os.path.join(ROOT, "data")
    suffix = ""
    if country:
        out = os.path.join(out, "country_digests")
        os.makedirs(out, exist_ok=True)
        suffix = "_" + slug(country)
    open(os.path.join(out, f"weekly_digest{suffix}.html"), "w", encoding="utf-8").write(doc)
    name = "Weekly jobs " + now.strftime("%Y-%m-%d") + (f" ({country})" if country else "")
    open(os.path.join(out, f"weekly_digest{suffix}.txt"), "w", encoding="utf-8").write(
        f"Campaign name: {name}\nSubject: {subject}\nPreview text: {preview}\nList: " + (f"Job alerts, contacts whose WORK_COUNTRY is {country} only. " if country else "Job alerts. ") + "Class S (consent: job alerts); no promotion inside.\n"
        "Suggested send: Tuesday morning, then compare with another day (no evidence yet for the best day).\n\n" +
        "\n".join(f"[{n}] {r['title']} at {r['company']} ({r['level']}, {(r.get('eligibility') or {}).get('label')}) {r['sourceUrl']}" for n, i in sections for r in i) + "\n")
    print(name, "|", subject, "|", sum(len(i) for _, i in sections), "jobs shown of", new_total, "new this week")


if __name__ == "__main__":
    main()
