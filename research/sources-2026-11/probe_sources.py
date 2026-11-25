#!/usr/bin/env python3
"""Phase 1c (25 Nov 2026): live probe of candidate job sources beyond Greenhouse, Lever and Ashby.

For every candidate with a machine-readable endpoint: is it reachable without a key, how many postings, does
each posting carry an original posting date, a location or remote flag, a direct link, and how many titles
look entry-level or junior. Raw responses are stored truncated in probes/<id>.txt, measurements in
probe_results.json. Candidates that need a key or have no feed are recorded too, with the reason.
Terms of use are NOT judged here: that is step 1d, done by reading each shortlisted source's terms.

    python3 research/sources-2026-11/probe_sources.py
"""
import json
import re
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
PROBES = HERE / "probes"
PROBES.mkdir(exist_ok=True)
JUNIOR = re.compile(r"\b(intern(ship)?s?|junior|jr\.?|entry[- ]level|graduate|new grad|trainee|apprentice(ship)?|associate|assistant|early career|working student|werkstudent)\b", re.I)
SENIOR = re.compile(r"\b(senior|sr\.?|staff|principal|lead|head|director|vp|vice president|chief|manager)\b", re.I)
REMOTE = re.compile(r"\b(remote|anywhere|work from home|wfh|home[- ]based|telecommut\w*|distributed)\b", re.I)
UA = {"User-Agent": "Mozilla/5.0 (compatible; YirehCareersResearch/1.0; +https://yirehcareers.vercel.app/verify)"}

# id, category, name, method, url, how to find the list of postings in the JSON, title key, extra keys to check
# category: ats (one employer per call), board (remote job board), aggregator, public-service, nonprofit, junior
C = [
    # ---- employer hiring systems beyond the three (sample tenants from the public endpoint reference) ----
    ("recruitee", "ats", "Recruitee", "GET", "https://bunq.recruitee.com/api/offers/", "offers", "title", ["published_at", "remote", "location", "careers_url"]),
    ("workable", "ats", "Workable", "GET", "https://apply.workable.com/api/v1/widget/accounts/huzzle?details=true", "jobs", "title", ["published_on", "created_at", "telecommuting", "url", "country"]),
    ("workable-all", "aggregator", "Workable public job search (all employers)", "GET", "https://jobs.workable.com/api/v1/jobs?location=remote&limit=100", "jobs", "title", ["created", "workplace", "url"]),
    ("rippling", "ats", "Rippling", "GET", "https://api.rippling.com/platform/api/ats/v1/board/rippling/jobs", None, "name", ["url", "workLocation"]),
    ("personio", "ats", "Personio (XML)", "XML", "https://thermondo.jobs.personio.de/xml", "position", "name", ["createdAt", "office"]),
    ("breezy", "ats", "Breezy HR", "GET", "https://thirdchannel-inc.breezy.hr/json", None, "name", ["published_date", "location", "url"]),
    ("teamtailor", "ats", "Teamtailor (JSON feed)", "GET", "https://polestar.teamtailor.com/jobs.json", "items", "title", ["date_published", "url"]),
    ("bamboohr", "ats", "BambooHR", "GET", "https://401auto.bamboohr.com/careers/list", "result", "jobOpeningName", ["location", "isRemote"]),
    ("smartrecruiters", "ats", "SmartRecruiters (posting API)", "GET", "https://api.smartrecruiters.com/v1/companies/smartrecruiters/postings", "content", "name", ["releasedDate", "location", "ref"]),
    ("pinpoint", "ats", "Pinpoint", "GET", "https://pinpoint.pinpointhq.com/postings.json", "data", "title", ["created_at", "workplace_type", "url"]),
    ("homerun", "ats", "Homerun", "GET", "https://api.homerun.co/v1/jobs", None, "title", []),
    ("comeet", "ats", "Comeet (needs company token)", "NOTE", "https://developers.comeet.com/reference/careers-api-overview", None, None, []),
    ("join", "ats", "JOIN (join.com)", "NOTE", "https://join.com/companies/<company>", None, None, []),
    ("workday", "ats", "Workday (cxs, NVIDIA sample)", "POST", "https://nvidia.wd5.myworkdayjobs.com/wday/cxs/nvidia/NVIDIAExternalCareerSite/jobs", "jobPostings", "title", ["postedOn", "locationsText", "externalPath"]),
    ("jobvite", "ats", "Jobvite (no public JSON)", "NOTE", "https://jobs.jobvite.com/<company>", None, None, []),
    ("icims", "ats", "iCIMS (no public JSON)", "NOTE", "https://careers-<company>.icims.com", None, None, []),
    ("dover", "ats", "Dover", "NOTE", "https://app.dover.com/jobs/<company>", None, None, []),
    # ---- remote job boards ----
    ("remoteok", "board", "Remote OK", "GET", "https://remoteok.com/api", None, "position", ["date", "location", "url", "tags"]),
    ("wwr", "board", "We Work Remotely (RSS, all)", "RSS", "https://weworkremotely.com/remote-jobs.rss", "item", "title", ["pubDate", "region", "link"]),
    ("himalayas", "board", "Himalayas", "GET", "https://himalayas.app/jobs/api?limit=20", "jobs", "title", ["pubDate", "locationRestrictions", "seniority", "applicationLink"]),
    ("workingnomads", "board", "Working Nomads", "GET", "https://www.workingnomads.com/api/exposed_jobs/", None, "title", ["pub_date", "location", "url"]),
    ("arbeitnow", "board", "Arbeitnow", "GET", "https://www.arbeitnow.com/api/job-board-api", "data", "title", ["created_at", "remote", "location", "url"]),
    ("remotive", "board", "Remotive (EXCLUDED by project rule)", "SKIP", "https://remotive.com/api/remote-jobs", None, None, []),
    ("jobicy", "board", "Jobicy (EXCLUDED: dates not original)", "SKIP", "https://jobicy.com/api/v2/remote-jobs", None, None, []),
    ("nodesk", "board", "NoDesk entry-level", "HTML", "https://nodesk.co/remote-jobs/entry-level/", None, None, []),
    ("jobspresso", "board", "Jobspresso (RSS)", "RSS", "https://jobspresso.co/feed/?post_type=job_listing", "item", "title", ["pubDate", "link"]),
    ("remoteco", "board", "Remote.co (RSS)", "RSS", "https://remote.co/feed/", "item", "title", ["pubDate"]),
    ("dynamite", "board", "Dynamite Jobs", "HTML", "https://dynamitejobs.com/remote-jobs", None, None, []),
    ("4dayweek", "board", "4 Day Week", "HTML", "https://4dayweek.io/remote-jobs", None, None, []),
    ("hn", "board", "Hacker News Who is Hiring (Algolia)", "GET", "https://hn.algolia.com/api/v1/search_by_date?tags=comment,story_46108941&hitsPerPage=50", "hits", "comment_text", ["created_at"]),
    ("hn-thread", "board", "HN Who is Hiring thread lookup", "GET", "https://hn.algolia.com/api/v1/search?query=%22Ask%20HN%3A%20Who%20is%20hiring%3F%22&tags=story,author_whoishiring&hitsPerPage=3", "hits", "title", ["created_at", "objectID"]),
    ("yc", "board", "Y Combinator Work at a Startup", "HTML", "https://www.workatastartup.com/jobs", None, None, []),
    ("wellfound", "board", "Wellfound", "HTML", "https://wellfound.com/remote", None, None, []),
    ("jobgether", "board", "Jobgether", "HTML", "https://jobgether.com/", None, None, []),
    ("remoterocketship", "board", "Remote Rocketship", "HTML", "https://www.remoterocketship.com/", None, None, []),
    ("arc", "board", "Arc.dev junior", "HTML", "https://arc.dev/remote-jr-jobs", None, None, []),
    ("euremote", "board", "EU Remote Jobs (RSS)", "RSS", "https://euremotejobs.com/feed/?post_type=job_listing", "item", "title", ["pubDate", "link"]),
    ("landingjobs", "board", "Landing.jobs API", "GET", "https://landing.jobs/api/v1/jobs?limit=50", None, "title", ["published_at", "remote", "url"]),
    ("findwork", "aggregator", "Findwork.dev API (key)", "KEY", "https://findwork.dev/api/jobs/", None, None, []),
    # ---- aggregators with APIs ----
    ("themuse", "junior", "The Muse API (level filter)", "GET", "https://www.themuse.com/api/public/jobs?page=1&level=Entry%20Level&location=Flexible%20%2F%20Remote", "results", "name", ["publication_date", "locations", "levels", "refs"]),
    ("themuse-intern", "junior", "The Muse API internships remote", "GET", "https://www.themuse.com/api/public/jobs?page=1&level=Internship&location=Flexible%20%2F%20Remote", "results", "name", ["publication_date", "locations", "levels"]),
    ("adzuna", "aggregator", "Adzuna API (free key)", "KEY", "https://developer.adzuna.com/", None, None, []),
    ("jooble", "aggregator", "Jooble API (free key)", "KEY", "https://jooble.org/api/about", None, None, []),
    ("careerjet", "aggregator", "Careerjet API (affiliate id)", "KEY", "https://www.careerjet.com/partners/api/", None, None, []),
    ("reed", "aggregator", "Reed.co.uk API (free key)", "KEY", "https://www.reed.co.uk/developers", None, None, []),
    ("usajobs", "public-service", "USAJobs API (free key)", "KEY", "https://developer.usajobs.gov/", None, None, []),
    ("jsearch", "aggregator", "JSearch / Google for Jobs resellers (paid)", "PAID", "https://www.openwebninja.com/api/jsearch", None, None, []),
    ("theirstack", "aggregator", "TheirStack (paid)", "PAID", "https://theirstack.com/en/job-posting-api", None, None, []),
    ("techmap", "aggregator", "Techmap jobdatafeeds (paid)", "PAID", "https://jobdatafeeds.com/job-api", None, None, []),
    ("jobdataapi", "aggregator", "jobdataapi.com (paid)", "PAID", "https://jobdataapi.com/", None, None, []),
    ("coresignal", "aggregator", "Coresignal (paid)", "PAID", "https://coresignal.com/solutions/jobs-data-api/", None, None, []),
    # ---- public employment services and open data ----
    ("se-jobsearch", "public-service", "Sweden Arbetsformedlingen JobSearch (open)", "GET", "https://jobsearch.api.jobtechdev.se/search?q=remote&limit=50", "hits", "headline", ["publication_date", "workplace_address", "webpage_url", "application_details"]),
    ("de-ba", "public-service", "Germany Bundesagentur Jobsuche (public client id)", "GETH", "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v4/jobs?angebotsart=1&arbeitszeit=ho&size=50", "stellenangebote", "titel", ["aktuelleVeroeffentlichungsdatum", "arbeitsort", "refnr"]),
    ("ch-jobroom", "public-service", "Switzerland job-room", "NOTE", "https://www.job-room.ch/", None, None, []),
    ("no-nav", "public-service", "Norway NAV pam-stilling-feed (free token)", "KEY", "https://navikt.github.io/pam-stilling-feed/", None, None, []),
    ("fr-francetravail", "public-service", "France Travail Offres d'emploi (free key)", "KEY", "https://francetravail.io/data/api/offres-emploi", None, None, []),
    ("ca-jobbank", "public-service", "Canada Job Bank open data", "NOTE", "https://open.canada.ca/data/en/dataset/ea639e28-c0fc-48bf-b5dd-b8899bd43072", None, None, []),
    ("eures", "public-service", "EURES (no public API)", "NOTE", "https://eures.europa.eu/", None, None, []),
    ("nlx", "public-service", "US National Labor Exchange (partner)", "NOTE", "https://www.careeronestop.org/Developers/WebAPI/jobs-api-updates.aspx", None, None, []),
    ("nyc", "public-service", "NYC Jobs open data", "GET", "https://data.cityofnewyork.us/resource/kpav-sd4t.json?$limit=50", None, "business_title", ["posting_date", "work_location"]),
    # ---- nonprofit, international, impact ----
    ("reliefweb", "nonprofit", "ReliefWeb Jobs API (UN OCHA)", "GET", "https://api.reliefweb.int/v1/jobs?appname=yirehcareers-research&limit=100&profile=full&preset=latest", "data", "fields.title", ["fields.date.created", "fields.country", "fields.career_categories", "fields.experience", "fields.url"]),
    ("unjobs", "nonprofit", "UN Careers / UNjobs", "NOTE", "https://careers.un.org/", None, None, []),
    ("idealist", "nonprofit", "Idealist", "HTML", "https://www.idealist.org/en/jobs?locationType=REMOTE", None, None, []),
    ("80k", "nonprofit", "80,000 Hours job board", "HTML", "https://jobs.80000hours.org/", None, None, []),
    ("climatebase", "nonprofit", "Climatebase", "HTML", "https://climatebase.org/jobs?l=Remote", None, None, []),
    ("techjobsforgood", "nonprofit", "Tech Jobs for Good", "HTML", "https://techjobsforgood.com/jobs/?remote=true", None, None, []),
    # ---- junior and early-career lists (employer discovery seeds) ----
    ("simplify-newgrad", "junior", "SimplifyJobs New-Grad-Positions (GitHub list)", "GET", "https://raw.githubusercontent.com/SimplifyJobs/New-Grad-Positions/dev/.github/scripts/listings.json", None, "title", ["date_posted", "locations", "url", "company_name", "active"]),
    ("simplify-intern", "junior", "SimplifyJobs Summer Internships (GitHub list)", "GET", "https://raw.githubusercontent.com/SimplifyJobs/Summer2026-Internships/dev/.github/scripts/listings.json", None, "title", ["date_posted", "locations", "url", "company_name", "active"]),
    ("newgrad-jobs", "junior", "newgrad-jobs.com", "HTML", "https://www.newgrad-jobs.com/", None, None, []),
    ("entrylevelremote", "junior", "entrylevelremotejob.com", "HTML", "https://entrylevelremotejob.com/", None, None, []),
    ("wayup", "junior", "WayUp", "HTML", "https://www.wayup.com/", None, None, []),
    ("handshake", "junior", "Handshake (closed, student accounts)", "NOTE", "https://joinhandshake.com/", None, None, []),
    ("internshala", "junior", "Internshala (work from home internships)", "HTML", "https://internshala.com/internships/work-from-home-internships/", None, None, []),
    ("prosple", "junior", "Prosple / GradConnection", "HTML", "https://prosple.com/", None, None, []),
]


def dig(obj, path):
    for p in path.split("."):
        obj = obj.get(p) if isinstance(obj, dict) else None
    return obj


def probe(c):
    cid, cat, name, method, url, list_key, title_key, keys = c
    rec = {"id": cid, "category": cat, "name": name, "method": method, "url": url}
    if method in ("NOTE", "KEY", "PAID", "SKIP"):
        rec["result"] = {"NOTE": "no public feed found or needs a company-specific token", "KEY": "needs a free API key or partner id",
                         "PAID": "paid data vendor", "SKIP": "excluded by an earlier project decision"}[method]
        return rec
    t0 = time.time()
    try:
        if method == "POST":
            r = requests.post(url, json={"limit": 20, "offset": 0, "searchText": "remote"}, headers=UA, timeout=25)
        elif method == "GETH":
            r = requests.get(url, headers={**UA, "X-API-Key": "jobboerse-jobsuche"}, timeout=25)
        else:
            r = requests.get(url, headers=UA, timeout=25)
    except Exception as e:
        rec["result"] = f"unreachable: {type(e).__name__}"
        return rec
    rec["status"], rec["ms"], rec["bytes"] = r.status_code, int((time.time() - t0) * 1000), len(r.content)
    (PROBES / f"{cid}.txt").write_text(r.text[:20000], encoding="utf-8", errors="replace")
    if r.status_code != 200:
        rec["result"] = f"HTTP {r.status_code}"
        return rec
    titles, present = [], {k: 0 for k in keys}
    if method in ("RSS", "XML", "HTML"):
        tag = list_key or "item"
        items = re.findall(rf"<{tag}\b.*?</{tag}>", r.text, re.S | re.I) if method != "HTML" else []
        for it in items:
            m = re.search(rf"<{title_key}>(.*?)</{title_key}>", it, re.S | re.I)
            titles.append(re.sub(r"<!\[CDATA\[|\]\]>", "", m.group(1)).strip() if m else "")
            for k in keys:
                present[k] += 1 if re.search(rf"<{k}\b", it, re.I) else 0
        if method == "HTML":
            rec["result"] = "HTML page only (no feed); usable only by scraping, terms decide"
            rec["has_jobposting_jsonld"] = '"JobPosting"' in r.text
            rec["remote_mentions"] = len(REMOTE.findall(r.text))
            return rec
    else:
        try:
            data = r.json()
        except ValueError:
            rec["result"] = "not JSON"
            return rec
        items = data if isinstance(data, list) else (dig(data, list_key) if list_key else data)
        if isinstance(items, dict):
            items = list(items.values())
        items = [i for i in (items or []) if isinstance(i, dict)]
        if cid == "remoteok":
            items = [i for i in items if i.get("position")]
        for it in items:
            t = dig(it, title_key) if title_key else ""
            titles.append(re.sub(r"<[^>]+>", " ", str(t or ""))[:200])
            for k in keys:
                present[k] += 1 if dig(it, k) not in (None, "", [], {}) else 0
        rec["total_reported"] = (data.get("total") or data.get("totalFound") or data.get("totalCount") or data.get("page_count")
                                 or dig(data, "totalCount") or data.get("maxCount")) if isinstance(data, dict) else None
        rec["sample_item_keys"] = sorted(items[0].keys())[:40] if items else []
    n = len(titles)
    rec.update({"items": n, "fields_present": present,
                "junior_titles": sum(1 for t in titles if JUNIOR.search(t) and not SENIOR.search(t)),
                "senior_titles": sum(1 for t in titles if SENIOR.search(t)),
                "remote_in_title": sum(1 for t in titles if REMOTE.search(t)),
                "sample_titles": titles[:8], "result": "ok" if n else "reachable, no items parsed"})
    return rec


if __name__ == "__main__":
    with ThreadPoolExecutor(10) as ex:
        res = list(ex.map(probe, C))
    (HERE / "probe_results.json").write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    for r in res:
        extra = f"items={r.get('items')} junior={r.get('junior_titles')} senior={r.get('senior_titles')} fields={r.get('fields_present')}" if r.get("items") else ""
        print(f"{r['id']:18} {r['category']:14} {r.get('status', ''):>4} {r['result'][:60]:60} {extra}")
