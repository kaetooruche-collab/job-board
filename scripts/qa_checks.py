"""Independent quality checks for the job feed.

Why this exists: the classifier marks its own homework. Every bug found so far
(a pronoun read as a country, equal-opportunity text read as a hiring ban, a
"Senior" title shown as junior) was one the classifier could not see itself.
These checks do NOT reuse the classifier's reasoning. They look at the finished
record and at the raw posting text and ask "does this contradict itself or the
source?". A listing that fails a BLOCK rule is held back from the site and logged
for review. WARN rules are counted in data/qa_report.md so a person can look.

Two levels:
  check_listing(record, raw)  one listing at a time, before it is published
  audit_run(records, history) the whole run, compared with earlier runs (drift)

Every time a new kind of bug is found: add the real text to
tests/fixtures/regressions.json and, if it is a CLASS of bug, a rule here.
"""
import re
from collections import Counter
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse

import classify as C

BLOCK, WARN = "block", "warn"
EARLY_LEVELS = {"internship", "entry", "junior"}
MAX_AGE_DAYS = 30

# A title that says senior/lead/manager cannot be an early-career role unless it also says junior/associate/etc.
SENIOR_TITLE_RE = re.compile(
    r"\b(senior|sr\.?|staff|principal|lead(?!\s+(?:gen\w*|nurtur\w*|qualif\w*|research\w*|sourc\w*|scor\w*|captur\w*))|head of|director|vp|vice president|chief|architect|manager|president)\b", re.I)
EARLY_TITLE_RE = re.compile(r"\b(junior|jr\.?|associate|intern(?:ship)?|trainee|apprentice|graduate|entry[- ]level|new grad|early career|assistant)\b", re.I)

# Plain statements that the role is NOT remote. The classifier weighs context; this is a blunt second opinion.
NOT_REMOTE_RE = [
    re.compile(r"\(\s*(?:hybrid|on-?site|in-?office)\s*\)|(?:\U0001F4CD|\blocation\s*:)\s*[^|\n.]{0,40}\bhybrid\b", re.I),
    re.compile(r"\b(?:this|the)\s+(?:role|position|job|opportunity)\s+(?:is|will be)\s+(?:an?\s+)?(?:on-?site|in-?office|in-?person|hybrid)\b", re.I),
    re.compile(r"\bnot\s+(?:a\s+)?(?:fully\s+)?remote\s+(?:role|position|job|opportunity)\b", re.I),
    re.compile(r"\b(?:one|two|three|four|five|[1-5])\s+days?\s+(?:per|a|each|every)\s+week\s+(?:in|at)\s+(?:the|our)\s+(?:office|hq|headquarters)\b", re.I),
    re.compile(r"#\s*LI\s*[-_]?\s*hybrid\b", re.I),
    re.compile(r"\b(?:required|expected|must)\b[^.]{0,30}\bwork(?:ing)? (?:from|at|in) (?:a |an |our |the )?(?:[\w-]+\s){0,3}?(?:office|hq|headquarters)\b[^.]{0,40}\b(?:\d|one|two|three|four|five)\s*days?\s*(?:a|per|each|every)\s*(?:week|month)", re.I),
    re.compile(r"\bmust\s+(?:be\s+able\s+to\s+)?(?:work|be)\s+(?:on-?site|in\s+the\s+office)\b", re.I),
]
PAY_RANGE_RE = re.compile(r"(?:[$\u20ac\u00a3]\s?\d{2,3}(?:,\d{3})+(?:\.\d+)?|\b\d{2,3}(?:,\d{3})+\s*(?:USD|EUR|GBP))\s*(?:-|\u2013|\u2014|to)\s*(?:[$\u20ac\u00a3]\s?)?\d{2,3}(?:,\d{3})+", re.I)
ESTIMATE_RE = re.compile(r"\b(?:estimat\w+|approx\w*|about|around|roughly)\b|~", re.I)
EXCL_NOTE_RE = re.compile(r"cannot hire in:\s*(.+?)(?: and others)?\.?$", re.I)
HTML_JUNK_RE = re.compile(r"<[a-z/][^>]*>|&(?:amp|lt|gt|quot|#\d+);", re.I)


def _issue(rule, severity, detail):
    return {"rule": rule, "severity": severity, "detail": detail}


def _parse(ts):
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def check_listing(rec, raw=None, now=None):
    """Return a list of issues for one finished record. `raw` is the pipeline's raw listing (full text, classifier result)."""
    now = now or datetime.now(timezone.utc)
    issues = []
    title, company, url = rec.get("title") or "", rec.get("company") or "", rec.get("sourceUrl") or ""
    elig = rec.get("eligibility") or {}
    level = rec.get("level")

    # ---- data integrity -------------------------------------------------
    if not title.strip() or not company.strip():
        issues.append(_issue("missing-title-or-company", BLOCK, f"title={title!r} company={company!r}"))
    if HTML_JUNK_RE.search(title) or HTML_JUNK_RE.search(company):
        issues.append(_issue("html-in-title-or-company", BLOCK, f"{title!r} / {company!r}"))
    u = urlparse(url)
    if u.scheme != "https" or not u.netloc or u.path in ("", "/"):
        issues.append(_issue("not-a-specific-posting-url", BLOCK, url))
    try:
        posted = _parse(rec["postedAt"])
        if posted > now + timedelta(days=1):
            issues.append(_issue("posted-in-future", BLOCK, rec["postedAt"]))
        elif posted < now - timedelta(days=MAX_AGE_DAYS + 1):
            issues.append(_issue("older-than-30-days", BLOCK, rec["postedAt"]))
    except (KeyError, ValueError, AttributeError):
        issues.append(_issue("missing-or-bad-posted-date", BLOCK, str(rec.get("postedAt"))))
    sal = rec.get("salaryText")
    if sal:
        if ESTIMATE_RE.search(sal):
            issues.append(_issue("salary-looks-estimated", BLOCK, sal))
        elif not re.search(r"\d", sal):
            issues.append(_issue("salary-without-figures", WARN, sal))
    bad_flags = [f for f in (rec.get("flags") or []) if f in ("commission_only_or_unpaid", "applicant_fee", "suspicious_contact")]
    if bad_flags:
        issues.append(_issue("trust-flag-published", BLOCK, ", ".join(bad_flags)))

    # ---- experience level versus title ---------------------------------
    if level in EARLY_LEVELS and SENIOR_TITLE_RE.search(title) and not EARLY_TITLE_RE.search(title):
        issues.append(_issue("level-title-conflict", BLOCK, f"level={level} title={title!r}"))
    if re.search(r"\bintern(ship)?\b", title, re.I) and level != "internship":
        issues.append(_issue("intern-title-not-internship", WARN, f"level={level} title={title!r}"))

    # ---- eligibility versus its own evidence ---------------------------
    notes = elig.get("notes") or []
    label_countries = set(elig.get("countries") or [])
    for n in notes:
        m = EXCL_NOTE_RE.search(n)
        if m:
            banned = {x.strip() for x in m.group(1).split(",")}
            clash = banned & label_countries
            if clash:
                issues.append(_issue("eligibility-contradicts-exclusion", BLOCK, f"label lists {sorted(clash)} but note says cannot hire there: {n}"))
    if elig.get("type") in ("countries", "region") and (label_countries or elig.get("regions")):
        g = C.geo()
        texts = [rec.get("regionAsStated") or ""]
        res = (raw or {}).get("result") or {}
        for e in (res.get("eligibility", {}).get("evidence") or []) + (res.get("evidence") or []):
            texts.append(e.get("text") or "")
        places = g.find_places(" ".join(texts), allow_state_abbr=True)
        countries, regions = g.expand(places)
        supported = set(countries)
        if elig.get("type") == "countries" and label_countries:
            missing = sorted(label_countries - supported)
            if missing and len(missing) == len(label_countries):
                issues.append(_issue("eligibility-label-unsupported", BLOCK, f"label={sorted(label_countries)} but nothing in the location or evidence names them"))
            elif missing and len(missing) <= 6:  # a long list is a region written out in full, not a mistake
                issues.append(_issue("eligibility-label-partly-unsupported", WARN, f"not found in evidence: {missing}"))
    if elig.get("type") == "worldwide":
        g = C.geo()
        stated = rec.get("regionAsStated") or ""
        if not re.search(r"\b(anywhere|worldwide|global|remote)\b", stated, re.I) and [p for p in g.find_places(stated) if p["kind"] in ("country",)]:
            issues.append(_issue("worldwide-label-but-location-names-a-country", WARN, f"regionAsStated={stated!r}"))

    if raw is not None and not sal and PAY_RANGE_RE.search(C.clean_text(raw.get("description", ""))):
        issues.append(_issue("pay-in-posting-but-card-says-not-stated", WARN, PAY_RANGE_RE.search(C.clean_text(raw.get("description", ""))).group(0)))

    # ---- remote status: blunt second opinion on the full text ----------
    if raw is not None and rec.get("workArrangement") in (C.FULLY_REMOTE, C.REMOTE_RESTRICTED):
        text = C.clean_text(raw.get("description", ""))
        for rx in NOT_REMOTE_RE:
            m = rx.search(text)
            if m:
                issues.append(_issue("says-not-remote-but-published-as-remote", BLOCK, text[max(0, m.start() - 60): m.end() + 60].replace("\n", " ")))
                break
    return issues


def summarise(records):
    n = len(records) or 1
    cnt = lambda pred: sum(1 for r in records if pred(r))
    return {
        "count": len(records),
        "bySource": dict(Counter(r["sourceName"] for r in records)),
        "pctEligibilityUnclear": round(100 * cnt(lambda r: r["eligibility"]["type"] == "unclear") / n, 1),
        "pctRemoteUnclear": round(100 * cnt(lambda r: r["workArrangement"] == C.REMOTE_UNCLEAR) / n, 1),
        "pctWorldwide": round(100 * cnt(lambda r: r["eligibility"]["type"] == "worldwide") / n, 1),
        "pctEarlyCareer": round(100 * cnt(lambda r: r["level"] in EARLY_LEVELS) / n, 1),
        "pctSeniorPlus": round(100 * cnt(lambda r: r["level"] in ("senior", "leadership")) / n, 1),
    }


def drift(current, previous):
    """Compare this run with the previous one. Returns (abort_reasons, warnings)."""
    abort, warn = [], []
    if not previous:
        return abort, warn
    if previous["count"] >= 100 and current["count"] < 0.6 * previous["count"]:
        abort.append(f"listings fell from {previous['count']} to {current['count']} (more than 40%); keeping the previous data")
    if current["count"] == 0:
        abort.append("no listings at all; keeping the previous data")
    for src, was in previous.get("bySource", {}).items():
        now = current["bySource"].get(src, 0)
        if was >= 20 and now < 0.3 * was:
            warn.append(f"source {src}: {was} -> {now} listings (source may be down or changed)")
    for key, limit, label in [("pctEligibilityUnclear", 15, "listings with unclear eligibility"),
                              ("pctRemoteUnclear", 15, "listings with unclear remote status"),
                              ("pctWorldwide", 20, "worldwide-eligible listings"),
                              ("pctEarlyCareer", 10, "early-career listings")]:
        if key not in current or key not in previous:
            continue
        d = current[key] - previous[key]
        if abs(d) > limit:
            warn.append(f"{label}: {previous[key]}% -> {current[key]}% (moved {d:+.1f} points)")
    return abort, warn


def duplicates(records):
    """Same company, title AND stated location more than once: a true repeat."""
    c = Counter((r["company"].strip().lower(), r["title"].strip().lower(), r["regionAsStated"].strip().lower()) for r in records)
    return [f"{k[1]} at {k[0]} ({k[2]}) appears {v} times" for k, v in c.items() if v > 1]


def report(now, published, held, warnings, summary, drift_warn, drift_abort, dup):
    lines = [f"# Quality report, {now.isoformat(timespec='minutes')}", ""]
    lines += [f"- Published: **{published}**", f"- Held back by a quality rule (not published): **{len(held)}**",
              f"- Warnings (published, but look): **{sum(len(v) for v in warnings.values())}**", ""]
    if drift_abort:
        lines += ["## RUN STOPPED", *[f"- {x}" for x in drift_abort], ""]
    if held:
        lines += ["## Held back", ""]
        by = {}
        for h in held:
            by.setdefault(h["rule"], []).append(h)
        for rule, items in sorted(by.items(), key=lambda kv: -len(kv[1])):
            lines.append(f"### {rule} ({len(items)})")
            for h in items[:5]:
                lines.append(f"- {h['title']} at {h['company']}: {h['detail']}")
            lines.append("")
    if warnings:
        lines += ["## Warnings", ""]
        for rule, items in sorted(warnings.items(), key=lambda kv: -len(kv[1])):
            lines.append(f"### {rule} ({len(items)})")
            for h in items[:5]:
                lines.append(f"- {h['title']} at {h['company']}: {h['detail']}")
            lines.append("")
    if drift_warn or dup:
        lines += ["## Changes since the previous run", *[f"- {x}" for x in drift_warn + dup[:10]], ""]
    lines += ["## Shape of the feed", "", "```", *[f"{k}: {v}" for k, v in summary.items()], "```", ""]
    return "\n".join(lines)
