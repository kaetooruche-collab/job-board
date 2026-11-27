#!/usr/bin/env python3
"""Compare a featured role's card with the employer's own structured data (the hiring system's public feed).

Why (reviewer, 27 Nov 2026): verify-open.js confirmed postings were open and titles matched, but three cards were
still wrong: a "Worldwide" role whose location list was Argentina/Brazil/Chile (Recruitee locations[]), an "EMEA" role
whose locations were two UK cities (Ashby), and "Pay: Not stated" on a posting that states $105k-$122k (Greenhouse).

    python3 social/tools/verify_source.py social/output/2026-12-02/w49-p2/manifest.json [more]   # exit 1 on any failure
    python3 -c "import verify_source; ..."  # check_job(job) for picking roles

Rules (a card may only be featured when all hold; unknown or unreachable source = not featured):
- Worldwide card: no structured location names a country, US state, province or city.
- Region card: the structured locations must not all be specific places in one country.
- Pay: a card saying "Not stated" fails if the posting text states a figure with a currency.
Writes "source_check" into each manifest job. Not a hiring-system name ever reaches a post: this is internal.
"""
from __future__ import annotations

import datetime as dt
import html
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEX = json.loads((ROOT / "data" / "geo_lexicon.json").read_text(encoding="utf-8"))
WIDE_WORDS = re.compile(r"\b(remote|anywhere|worldwide|global|globally|international|distributed|emea|apac|latam|"
                        r"americas|europe|asia|africa|middle east|world)\b", re.I)
_AMT = r"(?:[$€£]|(?:USD|EUR|GBP|CAD|AUD)\s?)\s?\d[\d,.]*(?:\s?[kK])?(?![\d,.]*\s?(?:[mMbB]\b|million|billion|bn))"
# A salary statement: a currency range ("$105k–$122k", "USD 90,000 - 120,000"), or one amount next to a pay word.
PAY = re.compile(rf"{_AMT}\s?(?:-|–|—|to)\s?(?:[$€£]|USD|EUR|GBP|CAD|AUD)?\s?\d[\d,.]*(?:\s?[kK])?(?![\d,.]*\s?(?:[mMbB]\b|million|billion))"
                 rf"|(?:salary|compensation|base pay|pay range|OTE|annual pay)[^.\n]{{0,60}}?{_AMT}", re.I)


def _places() -> dict[str, str]:
    """lower-case place name -> country."""
    out = {}
    for c in LEX["countries"]:
        for n in [c["name"], *c.get("aliases", [])]:
            if len(n) > 3 or n.isupper():
                out[n.lower()] = c["name"]
    for s in LEX.get("usStates", []):
        out[s.split(" (")[0].lower()] = "United States"
    for p, c in (LEX.get("provinces") or {}).items():
        out[p.lower()] = c
    cities = LEX.get("cities") or {}
    for city, c in (cities.items() if isinstance(cities, dict) else []):
        out[city.lower()] = c if isinstance(c, str) else (c.get("country") if isinstance(c, dict) else "")
    for k in ("us", "america", "american"):
        out.pop(k, None)
    out.update({"uk": "United Kingdom", "usa": "United States", "brasil": "Brazil"})
    return out


PLACES = _places()


def countries_in(text: str) -> set[str]:
    t = (text or "").lower()
    return {c for p, c in PLACES.items() if re.search(rf"(?<![a-z]){re.escape(p)}(?![a-z])", t)}


def _get(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; YirehCareersCheck/1.0)"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.loads(r.read().decode())


def fetch(source_url: str) -> dict:
    """{'locations': [str], 'text': str} from the hiring system's public feed, or raise."""
    u = source_url
    m = re.search(r"greenhouse\.io/([^/]+)/jobs/(\d+)", u)
    if m:
        d = _get(f"https://boards-api.greenhouse.io/v1/boards/{m[1]}/jobs/{m[2]}")
        return {"locations": [(d.get("location") or {}).get("name", "")], "text": html.unescape(d.get("content", ""))}
    m = re.search(r"jobs\.ashbyhq\.com/([^/]+)/([0-9a-f-]{36})", u)
    if m:
        d = _get(f"https://api.ashbyhq.com/posting-api/job-board/{m[1]}?includeCompensation=true")
        j = next(x for x in d["jobs"] if x["id"] == m[2])
        locs = [j.get("location") or ""] + [s.get("location", "") for s in j.get("secondaryLocations") or []]
        comp = json.dumps(j.get("compensation") or {})
        return {"locations": locs, "text": (j.get("descriptionPlain") or "") + " " + comp}
    m = re.search(r"jobs\.lever\.co/([^/]+)/([0-9a-f-]{36})", u)
    if m:
        j = _get(f"https://api.lever.co/v0/postings/{m[1]}/{m[2]}")
        locs = (j.get("categories") or {}).get("allLocations") or [(j.get("categories") or {}).get("location", "")]
        return {"locations": locs, "text": (j.get("descriptionPlain") or "") + " " + (j.get("additionalPlain") or "")
                + " " + json.dumps(j.get("salaryRange") or {})}
    m = re.search(r"https://([^/]+)/o/([^/?#]+)", u)
    if m:
        d = _get(f"https://{m[1]}/api/offers/")
        o = next(x for x in d["offers"] if x["slug"] == m[2])
        locs = [f"{l.get('name', '')} {l.get('country', '')}".strip() for l in o.get("locations") or []] or [o.get("location", "")]
        return {"locations": locs, "text": html.unescape(re.sub("<[^>]+>", " ", o.get("description", "") + " " + o.get("requirements", "")))}
    raise LookupError("source not supported for structured checks")


def check_job(job: dict) -> dict:
    elig = job.get("eligibility") or {}
    label = elig.get("label") or job.get("apply_from") or ""
    kind = elig.get("type") or ("worldwide" if "worldwide" in label.lower() else "region")
    res = {"checked_on": dt.date.today().isoformat(), "ok": False, "label": label}
    try:
        src = fetch(job["sourceUrl"])
    except Exception as e:  # unknown or unreachable: never featured
        res["reason"] = f"could not read the employer's structured data ({type(e).__name__}: {str(e)[:80]})"
        return res
    locs = [l for l in src["locations"] if l]
    res["locations"] = locs
    named = set().union(*[countries_in(l) for l in locs]) if locs else set()
    if kind == "worldwide" and named:
        res["reason"] = f"card says Worldwide but the posting's locations name {sorted(named)}"
        return res
    if kind == "region" and locs and named and len(named) == 1 and not any(WIDE_WORDS.search(l) for l in locs):
        res["reason"] = f"card says {label} but the posting's locations are places in {next(iter(named))} only"
        return res
    if not job.get("salaryText") and PAY.search(src["text"] or ""):
        res["reason"] = f"card says pay not stated but the posting states '{PAY.search(src['text'])[0]}'"
        return res
    res["ok"] = True
    return res


_CACHE: dict[str, dict] = {}


def ok(job: dict) -> bool:
    if job["id"] not in _CACHE:
        _CACHE[job["id"]] = check_job(job)
    return _CACHE[job["id"]]["ok"]


def verified_stats(jobs: list[dict], st: dict) -> dict:
    """Numbers we say on screen must survive the same check: 'open worldwide' counts only roles whose employer data
    agrees (reviewer, 27 Nov: the raw count included LATAM-only roles)."""
    st = dict(st)
    ww = [j for j in jobs if (j.get("eligibility") or {}).get("type") == "worldwide"]
    st["worldwide_on_board"] = len(ww)
    st["worldwide"] = sum(1 for j in ww if ok(j))
    st["worldwide_note"] = "counted only roles whose employer data confirms no country limit (verify_source.py)"
    # everything not in the four shown groups (time-zone-only rules, worldwide labels not confirmed) so a split adds up
    st["other_eligibility"] = st.get("jobs", len(jobs)) - st["worldwide"] - st.get("region_wide", 0) - st.get("named_countries", 0) - st.get("location_not_specified", 0)
    return st


def main(argv=None) -> int:
    bad = 0
    for mf in argv or sys.argv[1:]:
        p = Path(mf)
        m = json.loads(p.read_text(encoding="utf-8"))
        for j in m.get("jobs", []):
            j["source_check"] = check_job(j)
            print(("OK  " if j["source_check"]["ok"] else "FAIL"), j["id"], j["company"], "|", j["source_check"].get("reason", j["source_check"].get("locations")))
            bad += not j["source_check"]["ok"]
        p.write_text(json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
