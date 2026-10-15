#!/usr/bin/env python3
"""Fetch 100+ verified, worldwide, entry-level remote job listings from
multiple sources: Jobicy, Greenhouse, Lever, Ashby.
Every link verified before inclusion."""

import json
import os
import re
import time
import unicodedata
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from email.utils import parsedate_to_datetime
from pathlib import Path

import requests

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
OUTPUT_FILE = REPO_ROOT / "jobs.json"
REMOVED_LOG = REPO_ROOT / "data" / "removed.log"

S = requests.Session()
S.headers.update({"User-Agent": "JobBoard/1.0 (educational project)"})

# Use custom CA bundle only if present (cloud dev environment)
CA_BUNDLE = os.environ.get("CA_BUNDLE_PATH", "/root/.ccr/ca-bundle.crt")
if os.path.exists(CA_BUNDLE):
    S.verify = CA_BUNDLE

THIRTY_DAYS_AGO = datetime.now(timezone.utc) - timedelta(days=30)
NOW = datetime.now(timezone.utc)

SENIOR_RE = re.compile(
    r'\b(senior|sr\.?\s|staff|principal|lead\b|head of|director|vp\b|'
    r'vice president|chief|c-level|architect|distinguished|fellow|'
    r'engineering manager|team lead)\b', re.I
)

ENTRY_RE = re.compile(
    r'\b(junior|jr\.?\b|entry[- ]level|associate|coordinator|specialist|'
    r'representative|assistant|intern|trainee|analyst|support|'
    r'customer (success|service|experience|care)|community|moderator|'
    r'data entry|virtual assistant|administrative|clerk|researcher|'
    r'writer|copywriter|social media|recruiter|tutor|teacher|'
    r'translator|interpreter|transcri|annotator|labeler|'
    r'early career|new grad|graduate|apprentice|fresher)\b', re.I
)

LOCATION_RESTRICTED = re.compile(
    r'(\bus\b|united states|usa\b|u\.s\.|americas|canada\b|\buk\b|united kingdom|'
    r'europe\b|emea\b|apac\b|dach\b|latam\b|\beu\b|'
    r'north america|south america|asia.?pacific|middle east|africa\b|'
    r'\bsea\b|southeast asia|'
    r'germany|france|spain|italy|netherlands|ireland|australia|new zealand|'
    r'japan\b|korea|singapore|india\b|brazil|mexico|argentina|colombia|'
    r'nigeria|kenya|south africa|israel|poland|czech|romania|hungary|austria|'
    r'switzerland|belgium|denmark|sweden|norway|finland|portugal|greece|turkey|'
    r'egypt|philippines|vietnam|thailand|indonesia|malaysia|taiwan|hong kong|china|'
    r'bulgaria|belarus|ukraine|russia|croatia|serbia|slovenia|'
    r'lithuania|latvia|estonia|slovakia|'
    r'saudi|uae|qatar|bahrain|oman|kuwait|'
    r'pakistan|bangladesh|sri lanka|nepal|myanmar|cambodia|'
    r'morocco|tunisia|algeria|ghana|ethiopia|tanzania|uganda|rwanda|'
    r'peru|chile|ecuador|venezuela|uruguay|paraguay|bolivia|'
    r'san francisco|new york|\bnyc\b|\bsf\b|\bla\b|london|berlin|paris|amsterdam|toronto|sydney|melbourne|'
    r'bangalore|bengaluru|mumbai|delhi|hyderabad|pune|chennai|'
    r'seattle|boston|chicago|los angeles|denver|austin|portland|atlanta|'
    r'dublin|warsaw|prague|budapest|bucharest|lisbon|madrid|barcelona|'
    r'munich|hamburg|zurich|vienna|stockholm|oslo|copenhagen|helsinki|'
    r'istanbul|ankara|'
    r'beijing|shanghai|shenzhen|tokyo|osaka|seoul|'
    r'sao paulo|s[aã]o paulo|buenos aires|bogota|bogot[aá]|lima|santiago|cairo|lagos|'
    r'manila|jakarta|bangkok|kuala lumpur|taipei|'
    r'riyadh|dubai|doha|abu dhabi|sofia|belgrade|zagreb|'
    r'kyiv|minsk|tallinn|riga|vilnius|bratislava|'
    r'nairobi|accra|cape town|johannesburg|casablanca|'
    r'\bcdmx\b|ciudad de m[eé]xico|costa rica|\bcri\b|puerto rico|'
    r'neuruppin|'
    r'bay area|silicon valley|'
    r'alabama|alaska|arizona|arkansas|california|colorado|connecticut|delaware|'
    r'florida|hawaii|idaho|illinois|indiana|iowa|kansas|kentucky|louisiana|'
    r'maine|maryland|massachusetts|michigan|minnesota|mississippi|missouri|'
    r'montana|nebraska|nevada|new hampshire|new jersey|new mexico|new york|'
    r'north carolina|north dakota|ohio|oklahoma|oregon|pennsylvania|'
    r'rhode island|south carolina|south dakota|tennessee|texas|utah|vermont|'
    r'virginia|washington\b|west virginia|wisconsin|wyoming|'
    r'ontario|british columbia|quebec|alberta|'
    r'iceland|reykjavik|'
    r'cincinnati|detroit|miami|philadelphia|san diego|san antonio|dallas|houston|'
    r'phoenix|indianapolis|columbus|charlotte|nashville|'
    r'in.?office|on.?site|hybrid)', re.I
)
US_STATES = {'AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN',
             'IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV',
             'NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN',
             'TX','UT','VT','VA','WA','WV','WI','WY','DC'}
US_STATE_PAT = re.compile(r',\s*(' + '|'.join(US_STATES) + r')\b')

TITLE_LOCATION_RE = re.compile(
    r'\b(united states|canada|united kingdom|germany|france|spain|italy|'
    r'netherlands|ireland|australia|new zealand|japan\b|korea|singapore|india\b|'
    r'brazil|mexico|argentina|colombia|nigeria|kenya|south africa|israel|'
    r'poland|czech|romania|hungary|austria|switzerland|belgium|denmark|'
    r'sweden|norway|finland|portugal|greece|turkey|egypt|philippines|'
    r'vietnam|thailand|indonesia|malaysia|taiwan|hong kong|china\b|'
    r'costa rica|puerto rico|kazakhstan|albania|georgia\b|'
    r'bulgaria|belarus|ukraine|russia|croatia|serbia|slovenia|'
    r'lithuania|latvia|estonia|slovakia|'
    r'saudi|uae|qatar|bahrain|oman|kuwait|'
    r'pakistan|bangladesh|sri lanka|nepal|myanmar|cambodia|laos|'
    r'morocco|tunisia|algeria|ghana|ethiopia|tanzania|uganda|rwanda|'
    r'peru|chile|ecuador|venezuela|uruguay|paraguay|bolivia|'
    r'ohio|california|texas|florida|new york|illinois|'
    r'san francisco|london|berlin|paris|amsterdam|toronto|sydney|'
    r'melbourne|bangalore|mumbai|delhi|seattle|boston|chicago|los angeles|'
    r'denver|austin|portland|atlanta|dublin|warsaw|prague|munich|'
    r'istanbul|ankara|tokyo|osaka|seoul|cairo|lagos|manila|jakarta|bangkok|'
    r'riyadh|dubai|doha|abu dhabi|sofia|bucharest|belgrade|zagreb|'
    r'kyiv|minsk|tallinn|riga|vilnius|bratislava|'
    r'nairobi|accra|addis ababa|cape town|johannesburg|casablanca|'
    r'lima|santiago|bogota|buenos aires|sao paulo|'
    r'north america|south america|latin america|eastern canada|western canada|'
    r'middle east|africa\b|asia\b|europe\b|emea\b|apac\b|latam\b|dach\b|saarc\b)\b', re.I
)

TITLE_REGION_RE = re.compile(
    r'[-–,]\s*(east|west|north|south|central|pacific|atlantic)\s*$|'
    r'[-–,]\s*(east|west|north|south)\s+region|'
    r'\bin the (us|uk|eu)\b|'
    r'\b(us|uk) only\b|'
    r'\banywhere in the (us|uk)\b', re.I
)

NON_ENGLISH_RE = re.compile(
    r'\(m/[fwd]/[dw]\)|'
    r'\b(und|für|oder|bei|mit|über)\b|'
    r'\b(y|del|los|las|para|como|desde|hacia|entre|sobre|según|'
    r'diagnóstico|mecánico|presupuesto|automotriz)\b', re.I
)

SEARCH_URL_RE = re.compile(r'/jobs/search\b|/search\?|/careers\?.*q=', re.I)

CATEGORY_MAP = {
    'customer support': re.compile(r'(customer.*(support|service|success|experience|care)|help\s*desk|cx\b|technical support|support (engineer|specialist|representative|agent|associate))', re.I),
    'operations': re.compile(r'(operations|ops\b|project.*(coordinator|specialist)|program|logistics|supply|implementation|onboarding)', re.I),
    'data & analytics': re.compile(r'(data.*(analyst|entry|engineer|science|specialist|annotator)|analytics|business intelligence|bi\b|reporting|labeler|annotator)', re.I),
    'writing & content': re.compile(r'(writ|content|copy|editor|blog|documentation|technical writ|transcri)', re.I),
    'marketing': re.compile(r'(marketing|growth|seo|social media|brand|communications|pr\b|public relation|demand gen|email market)', re.I),
    'design': re.compile(r'(design|ux|ui|graphic|visual|creative|illustrat)', re.I),
    'engineering': re.compile(r'(engineer(?!.*support)|developer|software|frontend|backend|fullstack|full.stack|devops|sre|platform)', re.I),
    'sales': re.compile(r'(sales|account.*(executive|develop|represent)|business development|bdr\b|sdr\b|revenue|inside sales)', re.I),
    'human resources': re.compile(r'(human resources|hr\b|recruiting|recruiter|talent|people ops)', re.I),
    'finance & accounting': re.compile(r'(financ|account(?!.*(executive|develop|represent|manag))|bookkeep|payroll|billing|treasury|audit|tax)', re.I),
    'admin & virtual assistant': re.compile(r'(admin|virtual assistant|executive assistant|office|receptionist|clerk)', re.I),
    'community & moderation': re.compile(r'(community|moderator|moderation|trust.safety)', re.I),
    'teaching & tutoring': re.compile(r'(teacher|tutor|instructor|educator|coach|mentor|teaching)', re.I),
    'translation': re.compile(r'(translat|interpret|linguist|localiz)', re.I),
    'research': re.compile(r'(research|researcher|insight)', re.I),
}

def categorize(title):
    for cat, pat in CATEGORY_MAP.items():
        if pat.search(title):
            return cat
    return 'other'

def is_senior(title):
    return bool(SENIOR_RE.search(title))

def normalize(s):
    return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()

def is_location_ok(loc_str):
    loc = normalize((loc_str or "").strip())
    if not loc:
        return True
    if re.search(r'\b(worldwide|anywhere|global|all countries)\b', loc, re.I):
        return True
    if LOCATION_RESTRICTED.search(loc):
        return False
    if US_STATE_PAT.search(loc):
        return False
    if re.match(r'^remote\s*[-–/(]', loc, re.I):
        return False
    if re.search(r'\bhq\b|headquarters', loc, re.I):
        return False
    if re.match(r'^(remote|fully remote|remoto|distributed|work from anywhere)$', loc, re.I):
        return True
    if ',' in loc or ';' in loc:
        return False
    return True


def title_has_location(title):
    t = normalize(title)
    if TITLE_LOCATION_RE.search(t):
        return True
    if TITLE_REGION_RE.search(t):
        return True
    return False


def is_non_english(title):
    if NON_ENGLISH_RE.search(title):
        return True
    try:
        title.encode('ascii')
    except UnicodeEncodeError:
        non_ascii = sum(1 for c in title if ord(c) > 127)
        if non_ascii > 2:
            return True
    return False


def is_search_url(url):
    return bool(SEARCH_URL_RE.search(url))

def verify_link(url, timeout=12):
    try:
        headers = {}
        resp = S.head(url, timeout=timeout, allow_redirects=True, headers=headers)
        if resp.status_code == 405:
            resp = S.get(url, timeout=timeout, allow_redirects=True, stream=True, headers=headers)
            resp.close()
        return resp.status_code < 400
    except:
        return False

def strip_html(s):
    if not s:
        return ""
    t = re.sub(r'<[^>]+>', ' ', s)
    t = re.sub(r'\s+', ' ', t).strip()
    return t[:300]


# ── Source 2: Jobicy ──────────────────────────────────────────────────
def fetch_jobicy():
    jobs = []
    for tag in ["", "customer-service", "writing", "data", "marketing", "sales",
                "teaching", "virtual-assistant", "admin"]:
        params = {"count": 50, "geo": "anywhere"}
        if tag:
            params["tag"] = tag
        try:
            resp = S.get("https://jobicy.com/api/v2/remote-jobs", params=params, timeout=20)
            if resp.status_code != 200:
                continue
            data = resp.json()
            for j in data.get("jobs", []):
                title = j.get("jobTitle", "")
                level = (j.get("jobLevel") or "").lower()
                if is_senior(title) or level in ("director", "executive", "c-suite"):
                    continue
                pub = j.get("pubDate", "")
                try:
                    dt = datetime.fromisoformat(pub.replace("Z", "+00:00"))
                    if dt < THIRTY_DAYS_AGO:
                        continue
                except:
                    dt = None

                geo = j.get("jobGeo", "")
                if geo and not re.search(r'(anywhere|worldwide|global)', geo, re.I):
                    continue

                salary = None
                smin = j.get("salaryMin")
                smax = j.get("salaryMax")
                scur = j.get("salaryCurrency", "")
                if smin and smax:
                    salary = f"{scur} {smin:,}–{smax:,}/yr"
                elif smin:
                    salary = f"{scur} {smin:,}+/yr"

                jobs.append({
                    "title": title,
                    "company": j.get("companyName", ""),
                    "url": j.get("url", ""),
                    "location": geo or "Anywhere",
                    "salary": salary,
                    "posted": dt,
                    "source": "Jobicy",
                    "description": strip_html(j.get("jobDescription", "")),
                    "jobType": ", ".join(j.get("jobType", [])) or "Full-time",
                    "is_entry": bool(ENTRY_RE.search(title)) or level in ("entry", "any", "junior", "trainee", ""),
                })
            time.sleep(0.5)
        except Exception as e:
            print(f"  Jobicy ({tag}) error: {e}")
    return jobs


# ── Source 4: Greenhouse ATS ──────────────────────────────────────────
GH_BOARDS = [
    'gitlab', 'zapier', 'buffer', 'cloudflare', 'hashicorp',
    'datadog', 'twilio', 'hubspot', 'canva', 'deel',
    'oysterhr', 'doist', 'toggl', 'hotjar', 'miro',
    'airtable', 'gorgias', 'posthog', 'supabase',
    'sourcegraph', 'grafana', 'elastic', 'wikimediafoundation', 'mozilla',
    'coinbase', 'discord', 'loom', 'remotecom',
    'webflow', 'netlify', 'vercel', 'retool', 'temporal',
    'circleci', 'buildkite', 'contentful', 'ghost',
    'launchdarkly', 'amplitude', 'mixpanel', 'pendo',
    'teleport', 'replit', 'automattic', 'shopify', 'stripe',
    'gusto', 'rippling', 'plaid', 'brex',
    'figma', 'calendly', 'asana', 'monday', 'clickup',
    'freshworks', 'zendesk', 'intercom', 'helpscout', 'frontapp',
    'customerio', 'auth0', 'okta', 'jumpcloud',
    'sentry', 'newrelic', 'pagerduty',
    'wise', 'revolut', 'kraken',
    'chainalysis', 'neon', 'airbyte', 'fivetran',
    'algolia', 'sanity', 'strapi', 'fullstory',
    'jetbrains', 'affirm', 'klarna',
    'remote', 'oyster', 'omnipresent', 'multiplier',
    'safetywing', 'letsdeel', 'velocity-global', 'papayaglobal',
    'aircall', 'groove', 'olark',
    'basecamp', 'whereby', 'krisp',
    'lemlist', 'clay', 'apollo',
    'beehiiv', 'convertkit', 'substack',
    'digitalocean', 'kinsta', 'cloudways', 'hostinger',
    'toptal', 'turing', 'andela', 'crossoverforwork',
    'testgorilla', 'close', 'balsamiq',
    'upwork', 'n26', 'binance', 'gemini',
    'opensea', 'alchemy',
    'render', 'railway', 'planetscale',
]
GH_BOARDS = list(dict.fromkeys(GH_BOARDS))

def fetch_one_gh(board):
    jobs = []
    try:
        resp = S.get(f"https://boards-api.greenhouse.io/v1/boards/{board}/jobs",
                     timeout=15, params={"content": "true"})
        if resp.status_code != 200:
            return jobs
        for j in resp.json().get("jobs", []):
            title = j.get("title", "")
            if is_senior(title):
                continue
            loc = j.get("location", {})
            loc_str = loc.get("name", "") if isinstance(loc, dict) else str(loc)
            if not is_location_ok(loc_str):
                continue
            updated = j.get("updated_at", "")
            try:
                dt = datetime.fromisoformat(updated.replace("Z", "+00:00"))
                if dt < THIRTY_DAYS_AGO:
                    continue
            except:
                dt = None
            jobs.append({
                "title": title,
                "company": board,
                "url": j.get("absolute_url", ""),
                "location": loc_str or "Remote",
                "salary": None,
                "posted": dt,
                "source": "Greenhouse",
                "description": strip_html(j.get("content", "")),
                "jobType": "Full-time",
                "is_entry": bool(ENTRY_RE.search(title)),
            })
    except:
        pass
    return jobs

def fetch_greenhouse():
    all_jobs = []
    with ThreadPoolExecutor(max_workers=12) as ex:
        futs = {ex.submit(fetch_one_gh, b): b for b in GH_BOARDS}
        for f in as_completed(futs):
            result = f.result()
            if result:
                print(f"  [gh] {futs[f]}: {len(result)}", flush=True)
                all_jobs.extend(result)
    return all_jobs


# ── Source 5: Lever ATS ───────────────────────────────────────────────
LEVER_BOARDS = [
    'spotify', 'anthropic', 'openai', 'databricks',
    'snowflakecomputing', 'confluent', 'pinecone', 'cohere',
    'huggingface', 'replicate', 'elevenlabs', 'assemblyai',
    'deepgram', 'khanacademy', 'duolingo', 'coursera',
    'toptal', 'crossoverforwork', 'n8n',
    'fly', 'render', 'railway',
    'neon', 'turso', 'clerk',
    'inngest', 'highlight', 'axiom',
    'warp', 'raycast',
    'twitch', 'lyft', 'robinhood',
    'affirm', 'klarna', 'anyscale',
    'toggl', 'doist', 'krisp',
    'beehiiv', 'convertkit',
    'close', 'apollo', 'clay', 'lemlist',
    'airtable', 'coda', 'notion',
    'webflow', 'framer', 'bubble',
    'retool', 'appsmith',
    'supabase', 'cal',
    'temporal', 'circleci',
    'sentry', 'PostHog', 'amplitude', 'heap',
    'LaunchDarkly', 'auth0', 'stytch',
    'gitpod', 'coder',
    'miro', 'figma', 'canva',
    'remote', 'deel', 'oyster',
]
LEVER_BOARDS = list(dict.fromkeys(LEVER_BOARDS))

def fetch_one_lever(company):
    jobs = []
    try:
        resp = S.get(f"https://api.lever.co/v0/postings/{company}",
                     timeout=15, params={"mode": "json"})
        if resp.status_code != 200:
            return jobs
        data = resp.json()
        if not isinstance(data, list):
            return jobs
        for j in data:
            title = j.get("text", "")
            if is_senior(title):
                continue
            loc = j.get("categories", {}).get("location", "")
            if not is_location_ok(loc):
                continue
            ms = j.get("createdAt", 0)
            try:
                dt = datetime.fromtimestamp(ms / 1000, tz=timezone.utc) if ms else None
                if dt and dt < THIRTY_DAYS_AGO:
                    continue
            except:
                dt = None
            jobs.append({
                "title": title,
                "company": company,
                "url": j.get("hostedUrl", ""),
                "location": loc or "Remote",
                "salary": None,
                "posted": dt,
                "source": "Lever",
                "description": strip_html(j.get("descriptionPlain", ""))[:300],
                "jobType": j.get("categories", {}).get("commitment", "Full-time") or "Full-time",
                "is_entry": bool(ENTRY_RE.search(title)),
            })
    except:
        pass
    return jobs

def fetch_lever():
    all_jobs = []
    with ThreadPoolExecutor(max_workers=12) as ex:
        futs = {ex.submit(fetch_one_lever, b): b for b in LEVER_BOARDS}
        for f in as_completed(futs):
            result = f.result()
            if result:
                print(f"  [lv] {futs[f]}: {len(result)}", flush=True)
                all_jobs.extend(result)
    return all_jobs


# ── Source 6: Ashby ATS ───────────────────────────────────────────────
ASHBY_BOARDS = [
    'ramp', 'linear', 'notion', 'vercel', 'cal',
    'resend', 'dub', 'tinybird', 'axiom',
    'planetscale', 'railway', 'render',
    'clerk', 'stytch', 'inngest', 'highlight',
    'neon', 'turso', 'warp', 'raycast',
    'passage', 'fig',
]

def fetch_one_ashby(board):
    jobs = []
    try:
        resp = S.get(f"https://api.ashbyhq.com/posting-api/job-board/{board}", timeout=15)
        if resp.status_code != 200:
            return jobs
        for j in resp.json().get("jobs", []):
            title = j.get("title", "")
            if j.get("isListed") is False:
                continue
            if is_senior(title):
                continue
            loc = j.get("location", "")
            if not isinstance(loc, str):
                loc = str(loc)
            if not is_location_ok(loc):
                continue
            pub = j.get("publishedAt", "")
            try:
                dt = datetime.fromisoformat(pub.replace("Z", "+00:00")) if pub else None
                if dt and dt < THIRTY_DAYS_AGO:
                    continue
            except:
                dt = None
            if not dt:
                continue
            jobs.append({
                "title": title,
                "company": board,
                "url": j.get("jobUrl", ""),
                "location": loc or "Remote",
                "salary": None,
                "posted": dt,
                "source": "Ashby",
                "description": "",
                "jobType": j.get("employmentType", "Full-time") or "Full-time",
                "is_entry": bool(ENTRY_RE.search(title)),
            })
    except:
        pass
    return jobs

def fetch_ashby():
    all_jobs = []
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(fetch_one_ashby, b): b for b in ASHBY_BOARDS}
        for f in as_completed(futs):
            result = f.result()
            if result:
                print(f"  [ab] {futs[f]}: {len(result)}", flush=True)
                all_jobs.extend(result)
    return all_jobs


# ── Company name cleanup ──────────────────────────────────────────────
COMPANY_FIX = {
    'gitlab': 'GitLab', 'cloudflare': 'Cloudflare', 'stripe': 'Stripe',
    'elastic': 'Elastic', 'datadog': 'Datadog', 'okta': 'Okta',
    'coinbase': 'Coinbase', 'figma': 'Figma', 'intercom': 'Intercom',
    'asana': 'Asana', 'mozilla': 'Mozilla', 'discord': 'Discord',
    'twilio': 'Twilio', 'netlify': 'Netlify', 'vercel': 'Vercel',
    'circleci': 'CircleCI', 'wise': 'Wise', 'n26': 'N26',
    'jetbrains': 'JetBrains', 'fivetran': 'Fivetran', 'mixpanel': 'Mixpanel',
    'pagerduty': 'PagerDuty', 'newrelic': 'New Relic', 'affirm': 'Affirm',
    'customerio': 'Customer.io', 'upwork': 'Upwork', 'gemini': 'Gemini',
    'turing': 'Turing', 'planetscale': 'PlanetScale', 'algolia': 'Algolia',
    'gusto': 'Gusto', 'brex': 'Brex', 'buildkite': 'Buildkite',
    'toptal': 'Toptal', 'testgorilla': 'TestGorilla', 'doist': 'Doist',
    'toggl': 'Toggl', 'hotjar': 'Hotjar', 'buffer': 'Buffer',
    'zapier': 'Zapier', 'automattic': 'Automattic', 'remote': 'Remote.com',
    'remotecom': 'Remote.com', 'spotify': 'Spotify', 'neon': 'Neon',
    'fly': 'Fly.io', 'anyscale': 'Anyscale', 'linear': 'Linear',
    'ramp': 'Ramp', 'notion': 'Notion', 'render': 'Render',
    'clerk': 'Clerk', 'railway': 'Railway', 'resend': 'Resend',
    'axiom': 'Axiom', 'inngest': 'Inngest', 'warp': 'Warp',
    'hubspot': 'HubSpot', 'canva': 'Canva', 'deel': 'Deel',
    'oysterhr': 'Oyster', 'miro': 'Miro', 'posthog': 'PostHog',
    'supabase': 'Supabase', 'grafana': 'Grafana', 'shopify': 'Shopify',
    'rippling': 'Rippling', 'plaid': 'Plaid', 'monday': 'Monday.com',
    'clickup': 'ClickUp', 'freshworks': 'Freshworks', 'zendesk': 'Zendesk',
    'helpscout': 'Help Scout', 'frontapp': 'Front', 'safetywing': 'SafetyWing',
    'digitalocean': 'DigitalOcean', 'anthropic': 'Anthropic',
    'openai': 'OpenAI', 'hashicorp': 'HashiCorp',
}

def fix_company(name):
    key = name.strip().lower().replace(' ', '').replace('-', '').replace('_', '')
    for k, v in COMPANY_FIX.items():
        if k.replace('-', '').replace('_', '') == key:
            return v
    return name.strip() or "Unknown"


# ── Main ──────────────────────────────────────────────────────────────
def main():
    all_jobs = []
    removed = []

    print("\n=== Fetching from Jobicy ===")
    jobicy = fetch_jobicy()
    print(f"  Jobicy: {len(jobicy)} jobs")
    all_jobs.extend(jobicy)

    print("\n=== Fetching from Greenhouse ATS ===")
    gh = fetch_greenhouse()
    print(f"  Greenhouse total: {len(gh)} jobs")
    all_jobs.extend(gh)

    print("\n=== Fetching from Lever ATS ===")
    lv = fetch_lever()
    print(f"  Lever total: {len(lv)} jobs")
    all_jobs.extend(lv)

    print("\n=== Fetching from Ashby ATS ===")
    ab = fetch_ashby()
    print(f"  Ashby total: {len(ab)} jobs")
    all_jobs.extend(ab)

    print(f"\n=== Total raw candidates: {len(all_jobs)} ===")

    seen_urls = set()
    seen_title_co = set()
    deduped = []
    title_loc_dropped = 0
    search_url_dropped = 0
    non_english_dropped = 0
    for j in all_jobs:
        url = j["url"].strip().rstrip("/")
        if not url or url in seen_urls:
            continue
        if is_search_url(url):
            search_url_dropped += 1
            removed.append(f"search-url | {j['title']} | {j['company']} | {url}")
            continue
        if title_has_location(j["title"]):
            title_loc_dropped += 1
            removed.append(f"title-location | {j['title']} | {j['company']} | {url}")
            continue
        if is_non_english(j["title"]):
            non_english_dropped += 1
            removed.append(f"non-english | {j['title']} | {j['company']} | {url}")
            continue
        title_co_key = (j["title"].lower().strip(), j["company"].lower().strip())
        if title_co_key in seen_title_co:
            continue
        seen_title_co.add(title_co_key)
        seen_urls.add(url)
        deduped.append(j)
    print(f"After dedup: {len(deduped)} (dropped {title_loc_dropped} title-loc, {search_url_dropped} search-URL, {non_english_dropped} non-English)")

    deduped.sort(key=lambda x: (
        -int(x.get("is_entry", False)),
        -(x["posted"].timestamp() if x.get("posted") else 0),
    ))

    MAX_PER = 8
    company_counts = {}
    capped = []
    for j in deduped:
        c = fix_company(j["company"])
        j["company"] = c
        n = company_counts.get(c, 0)
        if n < MAX_PER:
            company_counts[c] = n + 1
            capped.append(j)
        else:
            removed.append(f"company-cap | {j['title']} | {c} | {j['url']}")
    print(f"After company cap ({MAX_PER}/co): {len(capped)}")

    candidates = capped[:250]
    print(f"\nVerifying {len(candidates)} links...")

    verified = []
    with ThreadPoolExecutor(max_workers=20) as ex:
        fmap = {ex.submit(verify_link, j["url"]): j for j in candidates}
        done = 0
        for f in as_completed(fmap):
            done += 1
            j = fmap[f]
            try:
                if f.result():
                    verified.append(j)
                else:
                    removed.append(f"link-dead | {j['title']} | {j['company']} | {j['url']}")
            except:
                removed.append(f"link-error | {j['title']} | {j['company']} | {j['url']}")
            if done % 50 == 0:
                print(f"  Verified {done}/{len(candidates)}, {len(verified)} passed", flush=True)

    print(f"\nVerified: {len(verified)}")

    verified.sort(key=lambda x: (
        -int(x.get("is_entry", False)),
        -(x["posted"].timestamp() if x.get("posted") else 0),
    ))
    final = verified[:100]
    print(f"Final count: {len(final)}")

    final = [j for j in final if j.get("posted")]
    output = []
    for i, j in enumerate(final):
        output.append({
            "id": f"job-{i+1}",
            "title": j["title"],
            "company": j["company"],
            "category": categorize(j["title"]),
            "jobType": j.get("jobType", "Full-time"),
            "regionAsStated": j.get("location", "Remote"),
            "salaryText": j.get("salary"),
            "postedAt": j["posted"].isoformat() if j.get("posted") else None,
            "applyBefore": None,
            "sourceName": j["source"],
            "sourceUrl": j["url"],
            "firstSeenAt": NOW.isoformat(),
            "lastVerifiedAt": NOW.isoformat(),
            "flags": [],
            "description": j.get("description") or f"{j['title']} at {j['company']}",
        })

    output.sort(key=lambda x: x.get("postedAt") or "1970-01-01", reverse=True)

    cats = {}
    for j in output:
        cats[j["category"]] = cats.get(j["category"], 0) + 1
    print("\nCategory breakdown:")
    for c, n in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"  {c}: {n}")

    sources = {}
    for j in output:
        sources[j["sourceName"]] = sources.get(j["sourceName"], 0) + 1
    print("\nSource breakdown:")
    for s, n in sorted(sources.items(), key=lambda x: -x[1]):
        print(f"  {s}: {n}")

    companies = {}
    for j in output:
        companies[j["company"]] = companies.get(j["company"], 0) + 1
    print(f"\nUnique companies: {len(companies)}")
    print("Top companies:")
    for c, n in sorted(companies.items(), key=lambda x: -x[1])[:20]:
        print(f"  {c}: {n}")

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\nWrote {len(output)} jobs to {OUTPUT_FILE}")

    REMOVED_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(REMOVED_LOG, "w") as f:
        f.write(f"# Removed listings — {NOW.isoformat()}\n")
        for line in removed:
            f.write(line + "\n")
    print(f"Wrote {len(removed)} removed entries to {REMOVED_LOG}")


if __name__ == "__main__":
    main()
