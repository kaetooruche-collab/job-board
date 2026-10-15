"""Context-aware classifier for job listings.

Reads the title, location field, structured hints and the full description and
returns, for every listing: work arrangement, geographic eligibility, office
attendance, experience level, categories, quality flags, the evidence behind
each decision, a confidence, and any unresolved questions.

No single keyword decides the outcome. Evidence is gathered per sentence,
negations and company-level wording are recognised, and contradictions are
flagged for review rather than silently resolved.
"""

import html
import json
import re
import unicodedata
from pathlib import Path

LEXICON_PATH = Path(__file__).resolve().parent.parent / "data" / "geo_lexicon.json"

FULLY_REMOTE = "fully_remote"
REMOTE_RESTRICTED = "remote_geo_restricted"
REMOTE_UNCLEAR = "remote_unclear"
HYBRID = "hybrid"
ON_SITE = "on_site"

# ── Text helpers ──────────────────────────────────────────────────────

def clean_text(text):
    if not text:
        return ""
    t = html.unescape(text) if "&lt;" in text or "&amp;" in text else text
    t = re.sub(r"<\s*(br|/p|/li|/div|/h\d|/ul)\s*/?>", "\n", t, flags=re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    t = unicodedata.normalize("NFKC", t)
    t = t.replace("’", "'").replace("‘", "'").replace("–", "-").replace("—", "-")
    t = re.sub(r"[ \t\r\f\v]+", " ", t)
    t = re.sub(r"\n\s*\n+", "\n", t)
    return t.strip()[:30000]


def split_sentences(text):
    parts = re.split(r"(?<=[.!?])\s+|\n+|•|\s-\s|;\s", text)
    return [p.strip()[:420] for p in parts if p and len(p.strip()) > 2]


def _snip(s, n=170):
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= n else s[: n - 1] + "…"


NEG_BEFORE = re.compile(r"\b(no|not|non|never|without|isn't|aren't|don't|doesn't|neither|nor|zero|cannot|can't)\b", re.I)
NEG_AFTER = re.compile(
    r"^\W{0,3}(?:is|are|will be|would be)?\s*(?:not|never)\s+(?:required|needed|expected|necessary|available|possible|permitted)"
    r"|^\W{0,3}(?:not required|not needed|is optional|isn't required|aren't required)", re.I)


def _negated(sentence, m):
    before = sentence[max(0, m.start() - 45): m.start()]
    after = sentence[m.end(): m.end() + 45]
    return bool(NEG_BEFORE.search(before)) or bool(NEG_AFTER.search(after))


# ── Geography ─────────────────────────────────────────────────────────

class _Geo:
    def __init__(self, path=LEXICON_PATH):
        lex = json.loads(Path(path).read_text(encoding="utf-8"))
        self.country_names = [c["name"] for c in lex["countries"]]
        self.regions = lex["regions"]
        self.us_states = lex["usStates"]
        self.us_abbr = set(lex["usStateAbbreviations"])
        self.cities = lex["cities"]
        self.provinces = lex["provinces"]
        self.timezones = lex["timezones"]
        ci, cs, self.map = [], [], {}
        for c in lex["countries"]:
            name = c["name"]
            if name in ("Georgia", "Jordan", "Chad"):
                continue
            ci.append(name)
            self.map[name.lower()] = ("country", name)
            for a in c["aliases"] + c["demonyms"]:
                if a.isupper() or len(a) <= 3 or "." in a:
                    cs.append(a)
                else:
                    ci.append(a)
                self.map[a.lower()] = ("country", name)
        self.map["us"] = ("country", "United States")
        self.map["uk"] = ("country", "United Kingdom")
        self.map["uae"] = ("country", "United Arab Emirates")
        self.region_alias = {}
        for rname, r in self.regions.items():
            for a in r["aliases"]:
                self.region_alias[a.lower()] = rname
        reg_ci = [a for a in self.region_alias if len(a) > 3]
        reg_cs = ["EU", "EEA", "UK", "US", "UAE", "EMEA", "APAC", "DACH", "LATAM", "MENA", "GCC", "ANZ", "SEA"]
        for a in reg_cs:
            if a.lower() in self.region_alias:
                self.map.setdefault(a.lower(), ("region", self.region_alias[a.lower()]))
        for a in reg_ci:
            self.map[a] = ("region", self.region_alias[a])
        for s in self.us_states:
            nm = s.replace(" (US)", "")
            ci.append(nm)
            self.map[nm.lower()] = ("state", "United States")
        for p, c in self.provinces.items():
            ci.append(p)
            self.map[p.lower()] = ("state", c)
        for city, c in self.cities.items():
            ci.append(city)
            self.map[city.lower()] = ("city", c)
        ci += reg_ci
        ci = sorted(set(ci), key=len, reverse=True)
        self.re_ci = re.compile(r"(?<![A-Za-z])(" + "|".join(re.escape(x) for x in ci) + r")(?![A-Za-z])", re.I)
        cs_all = sorted(set(cs + ["US", "U.S.", "USA", "U.S.A.", "UK", "U.K.", "UAE", "EU", "EEA", "EMEA", "APAC", "DACH", "LATAM", "MENA", "GCC", "ANZ"]), key=len, reverse=True)
        self.re_cs = re.compile(r"(?<![A-Za-z])(" + "|".join(re.escape(x) for x in cs_all) + r")(?![A-Za-z])")
        self.re_state_abbr = re.compile(r",\s*([A-Z]{2})(?![A-Za-z])")

    def find_places(self, text, allow_state_abbr=False):
        """Return list of dicts {kind, name, raw} for places found in text."""
        found, seen = [], set()
        spans = []
        for m in self.re_ci.finditer(text):
            spans.append((m.start(), m.end(), m.group(1)))
        for m in self.re_cs.finditer(text):
            spans.append((m.start(), m.end(), m.group(1)))
        spans.sort()
        last_end = -1
        for s, e, raw in spans:
            if s < last_end:
                continue
            key = raw.lower().replace(".", "")
            hit = self.map.get(raw.lower()) or self.map.get(key)
            if not hit:
                continue
            kind, name = hit
            if raw.lower() in ("washington",) and "dc" not in text.lower():
                pass
            last_end = e
            k = (kind, name, raw.lower())
            if k not in seen:
                seen.add(k)
                found.append({"kind": kind, "name": name, "raw": raw})
        if allow_state_abbr:
            for m in self.re_state_abbr.finditer(text):
                if m.group(1) in self.us_abbr:
                    k = ("state", "United States", m.group(1))
                    if k not in seen:
                        seen.add(k)
                        found.append({"kind": "state", "name": "United States", "raw": m.group(1)})
        return found

    def expand(self, places):
        """Return (countries, regions) lists for a list of places."""
        countries, regions = [], []
        for p in places:
            if p["kind"] == "region":
                if p["name"] not in regions:
                    regions.append(p["name"])
                for c in self.regions[p["name"]]["members"]:
                    if c not in countries:
                        countries.append(c)
            else:
                if p["name"] not in countries:
                    countries.append(p["name"])
        return countries, regions


_GEO = None


def geo():
    global _GEO
    if _GEO is None:
        _GEO = _Geo()
    return _GEO


# ── Work arrangement ──────────────────────────────────────────────────

LOC_REMOTE = re.compile(r"\b(remote|anywhere|worldwide|work from home|wfh|home[- ]based|distributed|telecommut\w*|virtual|global)\b", re.I)
LOC_HYBRID = re.compile(r"\bhybrid\b", re.I)
LOC_ONSITE = re.compile(r"\b(on[- ]?site|in[- ]office|in[- ]person|office[- ]based)\b", re.I)

STRONG_REMOTE = [
    (r"\b(fully|100%|completely|entirely|totally|100 percent)[ -]remote\b", 3.0),
    (r"\bwork(?:ing)? (?:from|at) home\b", 3.0),
    (r"\bwork(?:ing)? from anywhere\b", 3.0),
    (r"\bwork remotely\b", 3.0),
    (r"\blocation[- ]independent\b", 3.0),
    (r"\btelecommut\w+", 3.0),
    (r"\bhome[- ]based\b", 3.0),
    (r"\bvirtual (?:position|role|job|opportunity|assistant position)\b", 3.0),
    (r"\bremote (?:position|role|job|opportunity|work)\b", 3.0),
    (r"\b(?:this|the) (?:position|role|job) is (?:fully |100% )?remote\b", 3.0),
    (r"\bremote,? (?:work|working) (?:environment|arrangement)\b", 3.0),
    (r"\b(?:work )?location\s*:?\s*[-]?\s*(?:fully\s+)?remote\b", 3.0),
    (r"\bremote[- ]first\b", 2.0),
    (r"\bfully[- ]distributed\b|\b(?:globally |geographically )?distributed (?:team|company|workforce|organi[sz]ation)\b", 1.5),
]
STRONG_REMOTE_RE = [(re.compile(p, re.I), w) for p, w in STRONG_REMOTE]
BARE_REMOTE_RE = re.compile(r"\bremote(?:ly)?\b", re.I)
WEAK_REMOTE_RE = re.compile(r"\bremote[- ]friendly\b|\bflexible (?:work )?(?:location|arrangement)s?\b|\bwork flexibility\b", re.I)

COMPANY_LEVEL_RE = re.compile(
    r"\b(?:some|certain|select|various|many|other|several|a number of|eligible|most)\s+(?:roles|positions|jobs|opportunities|teams)\b"
    r"|opportunities (?:are )?available|remote (?:and|or|/) ?(?:hybrid|on-?site|in-?office) (?:options|roles|positions|opportunities|working)"
    r"|(?:options|flexibility|ability|opportunity|opportunities) (?:for|to) work(?:ing)? remotely"
    r"|we (?:also )?offer (?:flexible|remote|hybrid)|remote work (?:options|policy|perks?|benefits?)"
    r"|depending on (?:the )?(?:role|position|team|location)|role[- ]dependent|varies (?:by|depending)|where (?:the )?(?:role|position) allows"
    r"|(?:we|our) (?:employees|team members|people)", re.I)

HYBRID_PATTERNS = [
    (re.compile(r"\bhybrid\b", re.I), 3.0, "hybrid wording"),
    (re.compile(r"\b(?:partially|partly) remote\b", re.I), 3.0, "partially remote"),
    (re.compile(r"\b(?:\d|one|two|three|four|1-2|2-3|3-4)\s*(?:days?)\s*(?:a|per|each|/)\s*week\s*(?:in|at|on)[- ]?(?:the\s*)?(?:office|site)", re.I), 3.0, "set office days"),
    (re.compile(r"\b(?:in|at) the office\s+(?:\d|one|two|three|four)\b|\b(?:\d|one|two|three|four)\s*days?\s*(?:in|at) the office", re.I), 3.0, "set office days"),
    (re.compile(r"\b(?:every|each)\s+(?:monday|tuesday|wednesday|thursday|friday|week|other week)\b[^.]{0,50}\b(?:office|on-?site|in person)", re.I), 3.0, "recurring office day"),
    (re.compile(r"\b(?:office|on-?site|in person)\b[^.]{0,40}\b(?:every|each)\s+(?:monday|tuesday|wednesday|thursday|friday|week)\b", re.I), 3.0, "recurring office day"),
    (re.compile(r"\bmust (?:attend|come|be present|report|be (?:in|at|on))[^.]{0,40}\b(?:office|on-?site|in person|headquarters|hq)\b", re.I), 2.5, "must attend office"),
    (re.compile(r"\bflexible hybrid\b|\bhybrid (?:work|schedule|model|arrangement)\b", re.I), 3.0, "hybrid wording"),
    (re.compile(r"\bwork(?:ing)? from home\s+(?:on\s+)?(?:\d|one|two|three|four|(?:mon|tues|wednes|thurs|fri)days?)\b|\b(?:\d|one|two|three|four)\s*days?\s*(?:a|per|each)\s*week\s*(?:from home|remote(?:ly)?|working remotely)\b", re.I), 3.0, "partial home working"),
]
ONSITE_PATTERNS = [
    (re.compile(r"\bon[- ]?site\b", re.I), 2.0, "on-site wording"),
    (re.compile(r"\bin[- ]?office\b|\boffice[- ]based\b", re.I), 2.0, "office-based wording"),
    (re.compile(r"\bin[- ]person\b", re.I), 1.5, "in-person wording"),
    (re.compile(r"\bwork(?:ing)? (?:from|at|in) (?:our|the) (?:\w+\s){0,2}?(?:office|headquarters|hq|clinic|hospital|store|branch|warehouse|facility|campus|site|premises|restaurant|lab)\b", re.I), 2.5, "works at a physical workplace"),
    (re.compile(r"\brelocat\w+", re.I), 1.5, "relocation mentioned"),
    (re.compile(r"\bcommut\w+", re.I), 1.0, "commute mentioned"),
    (re.compile(r"\bphysical presence\b|\bat our office\b", re.I), 2.0, "physical presence"),
]
NOT_REMOTE_RE = re.compile(r"\b(?:not|isn't|no)\s+(?:a\s+|an\s+)?(?:fully\s+)?remote\b(?![- ]only|[- ]first)|\bremote (?:work )?(?:is )?not (?:available|possible|permitted|offered|an option)\b|\bno remote\b|\bnot eligible for remote\b", re.I)
OCCASIONAL_RE = re.compile(
    r"\boccasional(?:ly)?\b|\b(?:quarterly|annual(?:ly)?|bi-?annual(?:ly)?|twice a year|once a year|a few times (?:a|per) year|periodic(?:ally)?|from time to time|infrequent(?:ly)?)\b"
    r"|\b(?:company|team)[- ](?:retreat|offsite|off-site|meetup|summit|get-together|gathering)s?\b|\b(?:retreat|offsite|off-site|meetup)s?\b|\bas needed\b|\bwhen needed\b|\bad[- ]?hoc\b|\bon occasion\b|\brarely\b|\b(?:team )?gatherings?\b|\bmay be (?:asked|required|invited|expected) to (?:report|attend|travel|come|meet)", re.I)
OFFICE_WORD_RE = re.compile(r"\b(?:office|on-?site|in[- ]person|headquarters|hq|retreat|offsite|off-site|meetups?)\b", re.I)
NO_OFFICE_RE = re.compile(
    r"\b(?:no|not|never|without|zero)\b[^.]{0,45}\b(?:office|on-?site|commut\w*|in[- ]person|headquarters)\b"
    r"|\b(?:office|on-?site|commut\w*|in[- ]person)\b[^.]{0,35}\b(?:not|never)\s+(?:required|needed|necessary|expected)\b", re.I)
RESIDENCY_NEAR_RE = re.compile(r"\b(?:live|reside|located|be based|residing|living)\s+(?:within|near|in commuting distance|close to|no more than)\b[^.]{0,40}\b(?:\d+\s*(?:miles|mi|km|kilometers|kilometres|minutes|hours)|commut\w+|the office|our office|an office)", re.I)
REMOTE_AFTER_RE = re.compile(r"\bremote\s+(?:after|following|upon|once)\b[^.]{0,50}\b(?:training|onboarding|probation|ramp|period|months?|weeks?)\b|\b(?:training|onboarding)\b[^.]{0,40}\b(?:is|will be|are)?\s*(?:held\s+)?(?:on-?site|in[- ]person|at (?:our|the) office)\b", re.I)
VIRTUAL_TRAINING_RE = re.compile(r"\b(?:virtual|online|remote)\s+(?:training|onboarding)\b", re.I)


MIXED_RE = re.compile(r"\b(?:office|in[- ]person|on-?site|in-?office|hybrid)\b", re.I)
ARR_CTX_RE = re.compile(r"\b(?:office|on-?site|remote(?:ly)?|days?|week|working|work (?:from|arrangement|model|schedule|policy)|schedule|commut\w*|in[- ]person|location|attend|presence)\b", re.I)
TECH_HYBRID_RE = re.compile(r"^hybrid[- ]?(?:cloud|multi-?cloud|analy\w+|go-to-market|gtm|search|deploy\w*|infra\w*|app\w*|vehicle|encrypt\w*|integration|sales|motion|approach|architecture|solutions?|environments?|talent|delivery|experiences?|formats?|engineering|events?|models? (?:of|for) (?:delivery|talent|consulting))", re.I)
COMPANY_HYBRID_RE = re.compile(
    r"\b(?:is|are) a (?:hybrid|remote|distributed) (?:organi[sz]ation|company|team|workplace)\b"
    r"|\bremote (?:or|and|/) ?hybrid\b|\bhybrid (?:or|and|/) ?remote\b|\bhybrid (?:expectations|requirements)\b[^.]{0,60}\b(?:will be|communicated|discussed)\b"
    r"|\b(?:any|if any)\b[^.]{0,50}\bhybrid\b", re.I)
COMM_MODE_RE = re.compile(r"\b(?:online|virtual(?:ly)?|writing|written|oral|verbal|phone|telephone|email|video|remotely|digital|chat)\b", re.I)
CUSTOMER_CTX_RE = re.compile(r"\b(?:customers?|clients?|prospects?|partners?|sales calls?|demos?|presentations?|events?|conferences?|trade ?shows?|users?)\b", re.I)
IN_PERSON_ONBOARDING_RE = re.compile(r"\bin[- ]person\s+(?:onboarding|training|orientation)\b|\b(?:onboarding|training|orientation)\b[^.]{0,25}\bin[- ]person\b", re.I)


def _hint_value(hint):
    if not hint:
        return None
    h = str(hint).strip().lower().replace("-", "").replace(" ", "").replace("_", "")
    if h in ("remote", "true", "fullyremote"):
        return "remote"
    if h == "hybrid":
        return "hybrid"
    if h in ("onsite", "inoffice", "false_onsite"):
        return "onsite"
    return None


def assess_work_arrangement(title, location, description, hint=None, remote_feed=False):
    ev = []              # list of dicts: signal, text, effect
    remote = 0.0
    office = 0.0
    unresolved = []
    attendance = "none_stated"
    flags = set()

    def add(signal, text, effect):
        ev.append({"signal": signal, "text": _snip(text), "effect": effect})

    # structured hint
    h = _hint_value(hint)
    if h == "remote":
        remote += 3.0; add("structured work-arrangement field", f"field says remote ({hint})", "remote")
    elif h == "hybrid":
        office += 3.0; add("structured work-arrangement field", f"field says hybrid ({hint})", "hybrid")
    elif h == "onsite":
        office += 3.0; add("structured work-arrangement field", f"field says on-site ({hint})", "on_site")

    # location field
    loc = location or ""
    if LOC_HYBRID.search(loc):
        office += 3.0; add("location field", loc, "hybrid")
    elif LOC_ONSITE.search(loc) or (re.search(r"\boffice\b", loc, re.I) and not LOC_REMOTE.search(loc)):
        office += 3.0; add("location field", loc, "on_site")
    if LOC_REMOTE.search(loc):
        remote += 3.0; add("location field", loc, "remote")

    # title
    ttl = title or ""
    if re.search(r"\bhybrid\b", ttl, re.I):
        office += 2.0; add("title", ttl, "hybrid")
    if re.search(r"\b(on[- ]?site|in[- ]office|office[- ]based)\b", ttl, re.I):
        office += 2.0; add("title", ttl, "on_site")
    if re.search(r"\b(remote|work from home|wfh|virtual|telecommut\w*|home[- ]based)\b", ttl, re.I):
        remote += 2.0; add("title", ttl, "remote")

    text = clean_text(description)
    sents = split_sentences(text)
    strong_hits = bare_hits = 0
    occasional_seen = False
    company_level_seen = False
    recurring_seen = False
    full_remote_explicit = False
    role_remote = h == "remote" or bool(LOC_REMOTE.search(loc)) or bool(re.search(r"\b(remote|work from home|wfh|virtual|telecommut\w*|home[- ]based)\b", ttl, re.I))
    virtual_training = bool(VIRTUAL_TRAINING_RE.search(text))

    for s in sents:
        company_level = bool(COMPANY_LEVEL_RE.search(s)) and bool(BARE_REMOTE_RE.search(s))
        if NOT_REMOTE_RE.search(s):
            office += 3.0; add("description", s, "on_site"); continue
        occasional_here = bool(OCCASIONAL_RE.search(s)) and bool(OFFICE_WORD_RE.search(s))
        company_hybrid = bool(COMPANY_HYBRID_RE.search(s))
        hy_hit = False
        for rx, w, label in HYBRID_PATTERNS:
            m = rx.search(s)
            if not m or _negated(s, m):
                continue
            if label in ("hybrid wording", "partially remote"):
                if TECH_HYBRID_RE.search(s[m.start(): m.start() + 40]) or re.search(r"(?:cloud|multi|self-?hosted|and)\s*$", s[max(0, m.start() - 14): m.start()], re.I):
                    continue
                if not ARR_CTX_RE.search(s):
                    continue
            if occasional_here and label == "must attend office":
                break
            if company_hybrid:
                office += 0.8; add("description (company-level wording)", s, "unclear")
                unresolved.append("The listing mentions hybrid arrangements in general terms; confirm what applies to this role.")
            else:
                office += w; add("description", s, "hybrid"); recurring_seen = True
            hy_hit = True
            break
        if hy_hit:
            continue
        mixed = bool(MIXED_RE.search(s))
        # remote evidence
        matched_strong = False
        for rx, wt in STRONG_REMOTE_RE:
            m = rx.search(s)
            if m and not _negated(s, m):
                matched_strong = True
                if company_level:
                    company_level_seen = True
                    add("description (company-level wording, not counted)", s, "unclear")
                elif strong_hits < 2:
                    strong_hits += 1
                    if wt >= 3.0 and not mixed:
                        role_remote = True
                    remote += 0.5 if mixed else wt
                    add("description (mixed office and remote wording)" if mixed else "description", s, "remote (weak)" if mixed else "remote")
                    if not mixed and re.search(r"(fully|100%|completely|entirely|totally)[ -]remote|remote[- ]first|work from anywhere|location[- ]independent", s, re.I):
                        full_remote_explicit = True
                break
        if not matched_strong:
            if company_level:
                company_level_seen = True
                add("description (company-level wording, not counted)", s, "unclear")
            elif WEAK_REMOTE_RE.search(s):
                remote += 0.8; add("description", s, "remote (weak)")
            elif BARE_REMOTE_RE.search(s) and bare_hits < 3:
                m = BARE_REMOTE_RE.search(s)
                if not _negated(s, m):
                    bare_hits += 1
                    remote += 0.5
                    if bare_hits == 1:
                        add("description", s, "remote (weak)")

        # office evidence (on-site wording, attendance)
        if NO_OFFICE_RE.search(s) and not occasional_here:
            remote += 1.0; add("description (explicitly no office)", s, "remote"); attendance = "explicitly_none"
            continue
        if occasional_here:
            occasional_seen = True
            add("description (occasional attendance)", s, "occasional")
            continue
        if IN_PERSON_ONBOARDING_RE.search(s) and not virtual_training:
            office += 1.0; flags.add("in_person_onboarding")
            unresolved.append("Mentions in-person onboarding or training; confirm how long and whether the ongoing role is remote.")
            add("description", s, "unclear")
            continue
        for rx, w, label in ONSITE_PATTERNS:
            m = rx.search(s)
            if not m:
                continue
            if _negated(s, m):
                remote += 1.0; add("description (explicitly no office)", s, "remote"); attendance = "explicitly_none"
                break
            if label in ("in-person wording", "on-site wording", "office-based wording") and (COMM_MODE_RE.search(s) or CUSTOMER_CTX_RE.search(s)):
                break
            if label == "works at a physical workplace" and CUSTOMER_CTX_RE.search(s) and re.search(r"\b(?:visit|meet|travel)", s, re.I):
                break
            office += w; add("description", s, "on_site")
            break

        if RESIDENCY_NEAR_RE.search(s):
            unresolved.append("Applicants must live near an office; confirm whether office attendance is expected.")
            flags.add("residency_near_office"); add("description", s, "unclear")
            office += 1.0
        if REMOTE_AFTER_RE.search(s) and not virtual_training:
            unresolved.append("Remote only after training or onboarding; confirm whether that period is on-site and how long it lasts.")
            flags.add("remote_after_training"); add("description", s, "unclear")

    # decision
    conflict = False
    arrangement = None
    confidence = "medium"
    r, o = remote, office

    if r >= 2 and o >= 2 and o >= 2 * r and o - r >= 3:
        arrangement = HYBRID if any(e["effect"] == "hybrid" for e in ev) else ON_SITE
        confidence = "medium"
    elif r >= 2 and o >= 2:
        conflict = True
        arrangement = HYBRID if o >= r else REMOTE_UNCLEAR
        confidence = "low"
        unresolved.append("The listing contradicts itself about remote versus office work; needs review.")
    elif o >= 3 and r < 2:
        arrangement = HYBRID if any(e["effect"] == "hybrid" for e in ev) else ON_SITE
        confidence = "high" if o >= 5 else "medium"
    elif r >= 3 and o < 2 and not role_remote:
        arrangement = REMOTE_UNCLEAR
        confidence = "low"
        unresolved.append("Remote is mentioned only in general terms about the company; the listing does not state this role is remote.")
    elif r >= 3 and o < 2:
        arrangement = FULLY_REMOTE
        confidence = "high" if (full_remote_explicit or r >= 5) and not flags else "medium"
        if o >= 1 and "residency_near_office" in flags:
            arrangement = REMOTE_UNCLEAR; confidence = "low"
    elif r >= 1 and o < 2:
        arrangement = REMOTE_UNCLEAR
        confidence = "low" if (r < 2 or not role_remote) else "medium"
    elif remote_feed and o < 2:
        arrangement = REMOTE_UNCLEAR
        confidence = "low"
        add("source", "listed on a remote-job feed; the listing itself does not say", "unclear")
    else:
        arrangement = ON_SITE
        confidence = "low"
        flags.add("no_remote_evidence")
        unresolved.append("No evidence in the listing that the role is remote.")

    if arrangement in (FULLY_REMOTE, REMOTE_UNCLEAR) and flags & {"remote_after_training", "residency_near_office"}:
        arrangement = REMOTE_UNCLEAR
        confidence = "low"
    if arrangement == FULLY_REMOTE and company_level_seen and not (h == "remote" or LOC_REMOTE.search(loc) or full_remote_explicit):
        arrangement = REMOTE_UNCLEAR; confidence = "low"
    if arrangement == REMOTE_UNCLEAR and company_level_seen:
        unresolved.append("The listing only mentions remote work in general company terms; it does not confirm this role.")

    if arrangement == HYBRID or (arrangement == ON_SITE and "no_remote_evidence" not in flags):
        attendance = "recurring" if arrangement == HYBRID else "required"
    elif occasional_seen:
        attendance = "occasional"
        unresolved.append("Occasional office or in-person attendance is mentioned; confirm how often.")
        if arrangement == FULLY_REMOTE:
            confidence = "medium"
    elif attendance == "none_stated" and arrangement in (FULLY_REMOTE, REMOTE_UNCLEAR):
        attendance = "none_stated"
    if recurring_seen and arrangement in (FULLY_REMOTE, REMOTE_UNCLEAR) and conflict:
        attendance = "recurring"

    return {
        "arrangement": arrangement,
        "attendance": attendance,
        "confidence": confidence,
        "conflict": conflict,
        "unresolved": list(dict.fromkeys(unresolved)),
        "evidence": ev,
        "flags": sorted(flags),
        "scores": {"remote": round(r, 1), "office": round(o, 1)},
    }


# ── Geographic eligibility ────────────────────────────────────────────

WW_COMPANY_LEVEL_RE = re.compile(r"\b(?:many|some|most|certain|select|several|various|other)\s+(?:of our\s+)?(?:roles|positions|jobs|teams|opportunities)\b|see (?:the )?individual (?:job )?listings?|depending on (?:the )?(?:role|position|team)", re.I)
WORLDWIDE_LOC = re.compile(r"\b(anywhere|worldwide|world[- ]wide|global(?:ly)?|all countries|any country|work from anywhere)\b", re.I)
WORLDWIDE_DESC = re.compile(
    r"\b(?:anywhere in the world|from anywhere in the world|any (?:country|location)|all countries|worldwide|world[- ]wide|globally|work from anywhere|"
    r"from anywhere|any time ?zone|all time ?zones|no location restrictions?|location[- ]independent|open to (?:candidates|applicants|talent) (?:from )?(?:anywhere|all|any|around the world|across the world))\b", re.I)
APPLICANT_CONTEXT = re.compile(r"\b(candidates?|applicants?|hir(?:e|ing)|apply|work from|located|based|open to|eligible|team members?|you can|join us|talent|employees?|contractors?)\b", re.I)
RESTRICTION_CUES = [
    re.compile(r"\b(?:must|need to|have to|required to|should)\s+(?:be\s+)?(?:legally\s+)?(?:located|based|resid\w+|living|live)\s+(?:in|within)\b", re.I),
    re.compile(r"\b(?:candidates|applicants|you|we)\s+(?:must|should|need to|can only|are only able to|are unable to)\s+(?:be\s+)?(?:legally\s+)?(?:authori[sz]ed|eligible|entitled|permitted|able|hire|accept|consider)", re.I),
    re.compile(r"\b(?:authori[sz]ed|eligible|legally entitled|right) to work (?:in|within|from)\b", re.I),
    re.compile(r"\bonly\s+(?:accepting|considering|hiring|open to|available to|available in|hire)\b", re.I),
    re.compile(r"\b(?:open|available)\s+(?:only\s+)?to\s+(?:candidates|applicants|residents)\s+(?:in|from|located)\b", re.I),
    re.compile(r"\bresidents? of\b", re.I),
    re.compile(r"\b(?:based|located|living|resident|residing)\s+in\s+(?:the\s+)?[A-Z]", re.I),
    re.compile(r"[A-Za-z.]+[- ]based\s+(?:candidates|applicants|employees|only|position|role)", re.I),
    re.compile(r"\bwe (?:currently )?(?:hire|employ|have (?:entities|employees))\b[^.]{0,40}\b(?:in|from)\s+the following\b", re.I),
    re.compile(r"\b(?:hiring|recruiting) (?:in|from)\b", re.I),
]
TIMEZONE_RE = re.compile(
    r"\b(?:overlap(?:ping)? (?:with|of)|within|in the|aligned with|working hours (?:in|of)?|available during)\b[^.]{0,40}\b(?:time ?zones?|UTC|GMT|EST|PST|CST|MST|EDT|PDT|CET|IST)\b"
    r"|\b(?:UTC|GMT)\s*[+-]\s*\d{1,2}\b|\b(?:EST|PST|CST|CET|EET)\s+(?:hours|time ?zone)\b", re.I)
AUTH_RE = re.compile(r"\b(?:existing|current|valid|legal)\s+(?:right|authori[sz]ation|work (?:permit|authori[sz]ation))|(?:will not|do not|does not|unable to)\s+(?:provide )?(?:sponsor|visa)|no (?:visa )?sponsorship|must (?:already )?have the right to work|authori[sz]ed to work", re.I)
CONTRACTOR_RE = re.compile(r"\b(?:international |overseas |global )?(?:independent )?contractors?\b[^.]{0,60}\b(?:worldwide|any country|anywhere|around the world|globally|international)\b|\b(?:hire|engage)s? (?:contractors?|freelancers?)[^.]{0,30}\b(?:worldwide|anywhere|globally|in (?:many|most|any|over \d+) countries)\b", re.I)


def _label_for(places_countries, regions, worldwide, tz):
    if worldwide:
        return "Worldwide"
    parts = []
    for r in regions:
        parts.append(r)
    explicit_countries = places_countries
    if explicit_countries:
        if len(explicit_countries) <= 3:
            parts.extend(explicit_countries)
        else:
            parts.append(f"{len(explicit_countries)} countries")
    if parts:
        if len(parts) == 1 and not regions:
            return f"{parts[0]} only"
        return ", ".join(parts) + (" only" if len(parts) == 1 else "")
    if tz:
        return "Time zone requirement"
    return "Eligibility unclear"


def assess_eligibility(title, location, description, remote_evidence=False, remote_feed=False):
    g = geo()
    loc = location or ""
    text = clean_text(description)
    sents = split_sentences(text)
    ev = []
    conflict = False
    notes = []

    loc_ww = bool(WORLDWIDE_LOC.search(loc)) and not re.search(r"\b(?:global|anywhere)\b[^,;]*\b(?:in|within|across)\s+(?:the\s+)?[A-Z]", loc)
    loc_places = g.find_places(loc, allow_state_abbr=True)
    loc_has_remote = bool(LOC_REMOTE.search(loc))
    if not loc_has_remote and remote_evidence and loc_places and all(p["kind"] in ("country", "region") for p in loc_places):
        loc_has_remote = True

    # title suffixes like "- Canada" or "(UK)"
    title_places = []
    m = re.search(r"[-,(]\s*([A-Za-z .&/]+?)\s*\)?\s*$", title or "")
    if m:
        title_places = [p for p in g.find_places(m.group(1)) if p["kind"] in ("country", "region")]

    desc_ww, desc_places, tz_hit = [], [], None
    for s in sents:
        if WORLDWIDE_DESC.search(s) and APPLICANT_CONTEXT.search(s):
            m = WORLDWIDE_DESC.search(s)
            if not _negated(s, m) and not WW_COMPANY_LEVEL_RE.search(s) and not re.search(r"\b(?:customers?|users?|clients?|offices?|products?|brands?|companies|markets?|colleagues)\b[^.]{0,30}(?:worldwide|around the world|globally)|(?:worldwide|around the world|globally)\b[^.]{0,30}\b(?:customers?|users?|clients?)", s, re.I):
                desc_ww.append(s)
        if any(rx.search(s) for rx in RESTRICTION_CUES):
            places = [p for p in g.find_places(s) if p["kind"] in ("country", "region", "state", "city")]
            if places:
                desc_places.append((s, places))
        if tz_hit is None and TIMEZONE_RE.search(s):
            tz_hit = s

    restricted_places = []
    restricted_from = []
    if loc_places and (loc_has_remote or not loc_ww):
        restricted_places.extend(loc_places)
        restricted_from.append(("location field", loc))
    for s, places in desc_places:
        restricted_places.extend(places)
        restricted_from.append(("description", s))
    if not restricted_places and title_places:
        restricted_places.extend(title_places)
        restricted_from.append(("title", title))

    worldwide_from = []
    if loc_ww and not loc_places:
        worldwide_from.append(("location field", loc))
    elif loc_ww and loc_places and re.search(r"\b(anywhere|worldwide|global)\b", loc, re.I):
        worldwide_from.append(("location field", loc))
    for s in desc_ww[:2]:
        worldwide_from.append(("description", s))

    countries, regions = g.expand(restricted_places)
    explicit = []
    for p in restricted_places:
        if p["kind"] != "region" and p["name"] not in explicit:
            explicit.append(p["name"])

    etype = "unclear"
    confidence = "low"
    if worldwide_from and restricted_places and remote_feed and loc_places:
        etype = "region" if (regions and not explicit) else "countries"
        confidence = "medium"
        notes.append("The listing text mentions worldwide wording, but the job feed's location field limits applicants; the feed's field is shown.")
        for src, t in restricted_from[:2]:
            ev.append({"signal": src, "text": _snip(t), "effect": "restricted"})
    elif worldwide_from and restricted_places:
        conflict = True
        etype = "unclear"
        notes.append("The location field and the description disagree about where applicants can be; check the employer's wording.")
        for src, t in restricted_from[:2]:
            ev.append({"signal": src, "text": _snip(t), "effect": "restricted"})
        for src, t in worldwide_from[:2]:
            ev.append({"signal": src, "text": _snip(t), "effect": "worldwide"})
    elif worldwide_from:
        etype = "worldwide"
        confidence = "high" if any(src == "description" for src, _ in worldwide_from) and loc_ww else "medium"
        for src, t in worldwide_from[:2]:
            ev.append({"signal": src, "text": _snip(t), "effect": "worldwide"})
    elif restricted_places:
        etype = "region" if (regions and not explicit) else "countries"
        in_loc = any(src == "location field" for src, _ in restricted_from)
        in_desc = any(src == "description" for src, _ in restricted_from)
        confidence = "high" if (in_loc and in_desc) else ("medium" if (in_loc and loc_has_remote) or in_desc else "low")
        if in_loc and not loc_has_remote and not in_desc:
            confidence = "low"
            notes.append("The location field names a place but does not say the role is remote there; confirm whether applicants elsewhere are accepted.")
            etype = "unclear"
        for src, t in restricted_from[:3]:
            ev.append({"signal": src, "text": _snip(t), "effect": "restricted"})
    elif tz_hit:
        etype = "timezone"; confidence = "low"
        ev.append({"signal": "description", "text": _snip(tz_hit), "effect": "time zone"})

    if etype == "unclear" and not conflict and not notes:
        notes.append("The listing does not state where applicants must live or be authorised to work.")

    authorization = bool(AUTH_RE.search(text))
    contractor = None
    m = CONTRACTOR_RE.search(text)
    if m:
        contractor = _snip(m.group(0), 160)
    if authorization:
        notes.append("Applicants may need existing work authorisation; check the posting.")

    label = _label_for(explicit, regions, etype == "worldwide", tz_hit if etype == "timezone" else None) if etype not in ("unclear",) else "Eligibility unclear"
    if etype == "region" and regions:
        label = ", ".join(regions)

    return {
        "type": etype,
        "label": label,
        "countries": countries if etype in ("countries", "region") else [],
        "regions": regions if etype in ("countries", "region") else [],
        "statedLocation": _snip(loc, 120) if loc else None,
        "authorizationRequired": authorization,
        "contractorNote": contractor,
        "confidence": confidence,
        "conflict": conflict,
        "notes": notes,
        "evidence": ev,
    }


# ── Experience level ──────────────────────────────────────────────────

LEADERSHIP_TITLE = re.compile(r"\b(head of|director|vp\b|vice president|chief|c[teo]o\b|president|general manager|managing)\b", re.I)
MANAGER_TITLE = re.compile(r"\b(manager|lead|supervisor|team lead)\b", re.I)
PEOPLE_MGMT = re.compile(r"\b(direct reports?|manage (?:a )?team|lead (?:a )?team|people manager|line manage\w*|managing (?:a )?team|supervis\w+ (?:a )?team|manage and mentor|build and lead)\b", re.I)
SENIOR_TITLE = re.compile(r"\b(senior|sr\.?|staff|principal|distinguished|expert|architect|fellow)\b", re.I)
JUNIOR_TITLE = re.compile(r"\b(junior|jr\.?|associate)\b", re.I)
ENTRY_TITLE = re.compile(r"\b(entry[- ]level|trainee|apprentice|graduate|new grad|early career|fresher|graduate (?:program|scheme))\b", re.I)
INTERN_TITLE = re.compile(r"\b(intern(?:ship)?|working student|werkstudent|co-?op|student (?:assistant|worker|position)|placement year|summer (?:analyst|associate))\b", re.I)
NO_EXP_RE = re.compile(r"\bno (?:prior |previous |formal )?(?:work )?experience (?:is )?(?:required|needed|necessary)\b|\bwill (?:train|provide training)\b|\bentry[- ]level\b|\bfull training (?:is )?provided\b|\bno experience\b", re.I)
YEARS_RE = re.compile(r"(\d{1,2})\s*(?:\+|plus)?\s*(?:-|to|–)?\s*(\d{1,2})?\s*\+?\s*(?:years?|yrs?)\b", re.I)
EQUIV_RE = re.compile(r"\b(?:or )?equivalent (?:practical |relevant |work |professional )?experience\b|\bor equivalent\b|\bin lieu of\b|\bequivalent combination\b", re.I)
DEGREE_RE = re.compile(r"\b(bachelor'?s?|master'?s?|phd|doctorate|associate'?s? degree|degree|diploma|certification|licen[sc]e[ds]?|registered nurse|\bRN\b|CPA|CFA|ACCA|\bCA\b|bar (?:admission|exam))\b", re.I)


def assess_experience(title, description):
    t = title or ""
    text = clean_text(description)
    sents = split_sentences(text)
    years = None
    for s in sents:
        if "experience" in s.lower() or re.search(r"\byears?\b", s, re.I):
            if re.search(r"\b(preferred|nice to have|bonus|a plus|ideally|desirable)\b", s, re.I) and years is not None:
                continue
            m = YEARS_RE.search(s)
            if m:
                y = int(m.group(1))
                if y <= 25 and re.search(r"experience|exp\b|background|working|work", s, re.I):
                    years = y if years is None else years
    no_exp = bool(NO_EXP_RE.search(text)) or bool(NO_EXP_RE.search(t))
    people_mgmt = bool(PEOPLE_MGMT.search(text))
    notes = []
    level = "unspecified"
    basis = None
    if INTERN_TITLE.search(t):
        level, basis = "internship", "title"
    elif LEADERSHIP_TITLE.search(t) and not re.search(r"\b(?:sales|customer success|account|community|product|project|program|content|social media|marketing|office|case|payroll|finance|operations|support) manager\b", t, re.I):
        level, basis = "leadership", "title"
    elif MANAGER_TITLE.search(t) and people_mgmt:
        level, basis = "leadership", "title and description"
    elif ENTRY_TITLE.search(t):
        level, basis = "entry", "title"
    elif years is not None:
        level = "entry" if years == 0 else "junior" if years <= 2 else "mid" if years <= 5 else "senior"
        basis = f"{years}+ years stated"
    elif no_exp:
        level, basis = "entry", "description"
    elif SENIOR_TITLE.search(t):
        level, basis = "senior", "title"
    elif JUNIOR_TITLE.search(t):
        level, basis = "junior", "title"
    elif MANAGER_TITLE.search(t):
        level, basis = "mid", "title (individual-contributor manager)"
    if years is not None and level in ("entry", "junior") and ENTRY_TITLE.search(t) is None and JUNIOR_TITLE.search(t) and years >= 3:
        level = "mid"; basis = f"{years}+ years stated"; notes.append("Title says junior or associate but the description asks for more experience.")
    if years is not None and SENIOR_TITLE.search(t) and level in ("junior", "entry"):
        notes.append("Title says senior but the description asks for little experience.")
    if no_exp and years not in (None, 0) and level != "entry":
        notes.append("The description mentions both 'no experience' and a years requirement.")
    degrees = sorted({d.group(1).lower() for d in DEGREE_RE.finditer(text)})[:4]
    return {
        "level": level,
        "basis": basis,
        "yearsMin": years if years is not None else (0 if no_exp else None),
        "equivalentExperienceAccepted": bool(EQUIV_RE.search(text)),
        "qualificationsMentioned": degrees,
        "notes": notes,
    }


# ── Employment type ───────────────────────────────────────────────────

def assess_employment_type(title, declared, description):
    blob = " ".join([title or "", declared or "", clean_text(description)[:1500]]).lower()
    out = []
    if re.search(r"\bintern(ship)?\b", blob):
        out.append("Internship")
    if re.search(r"\bfreelance|\bfreelancer\b", blob):
        out.append("Freelance")
    if re.search(r"\bcontract(or)?\b|\bfixed[- ]term\b", blob):
        out.append("Contract")
    if re.search(r"\bpart[- ]time\b", blob):
        out.append("Part-time")
    if re.search(r"\btemporary\b|\bseasonal\b", blob):
        out.append("Temporary")
    if re.search(r"\bfull[- ]time\b", blob) or not out:
        out.insert(0, "Full-time")
    return list(dict.fromkeys(out))


# ── Category taxonomy (multi-label) ───────────────────────────────────

TAXONOMY = {
    "Administration & Operations": r"virtual assistant|administrative|admin\b|executive assistant|personal assistant|office (manager|coordinator|assistant)|data entry|clerk|receptionist|operations (coordinator|associate|analyst|specialist|manager)|project coordinator|scheduling|appointment|dispatcher|coordinator|back office|secretar",
    "Customer Service & Support": r"customer (service|support|success|care|experience|happiness|advocate)|support (specialist|agent|representative|associate|engineer|analyst)|call cent|contact cent|help ?desk|live chat|client (success|service|support)|technical support|service desk|care (advisor|agent)|customer representative|\bcsr\b|\bcx\b",
    "Sales": r"\bsales\b|business development|account (executive|manager)|\bsdr\b|\bbdr\b|appointment setter|lead generation|inside sales|revenue|account development|partnerships? (manager|associate)",
    "Marketing & Communications": r"marketing|\bseo\b|social media|email market|brand|communications|public relations|\bpr\b|growth|demand gen|campaign|community manager|influencer|content strateg",
    "Writing & Editing": r"writer|copywrit|editor|proofread|content (writer|creator|editor)|technical writ|journalist|blog|transcri|ghostwrit|documentation",
    "Design & Creative": r"design|\bux\b|\bui\b|graphic|illustrat|video edit|animator|motion|creative|photograph|videograph",
    "Finance & Accounting": r"account(ant|ing| payable| receivable)|bookkeep|financ|payroll|billing|treasury|audit|\btax\b|\bfp&a\b|controller|accounts (payable|receivable)|credit (analyst|control)|collections|invoice|revenue (accountant|accounting)",
    "Business & Analysis": r"business analyst|management consult|strategy|business operations|operations analyst|process (analyst|improvement)|project manager|program manager|product owner|chief of staff",
    "Data & Analytics": r"data (analyst|scientist|engineer|annotator|labeler|labeller|specialist|quality)|analytics|business intelligence|\bbi\b|machine learning|\bml\b|\bai (trainer|tutor|specialist|data)|annotat|statistic",
    "Software & Engineering": r"software|developer|engineer(?!.*support)|frontend|front-end|backend|back-end|full[- ]?stack|devops|\bsre\b|\bqa\b|quality assurance|test (engineer|automation)|mobile (developer|engineer)|programmer|platform engineer|web developer",
    "IT & Security": r"\bit (support|technician|administrator|specialist|analyst)|help desk|systems? administrator|sysadmin|network|cyber|security (analyst|engineer|specialist)|infosec|cloud|infrastructure|soc analyst",
    "Product & Project": r"product (manager|owner|analyst|designer)|project manager|program manager|scrum|delivery manager|agile",
    "Healthcare & Life Sciences": r"health|medical|clinical|nurse|nursing|therap|physician|doctor|pharma|biotech|patient|telehealth|coding specialist|billing and coding|care coordinator|dental|psycholog|counsel|laborator|\brn\b|\bnp\b|\bpa-c\b",
    "Education & Language": r"teacher|tutor|instructor|educator|teaching|curriculum|instructional design|academic|e-?learning|lecturer|professor|language (teacher|coach|instructor)|\besl\b|\btefl\b|training (specialist|coordinator)|learning (designer|experience)",
    "Human Resources & Recruiting": r"recruit|talent (acquisition|sourc|partner)|\bhr\b|human resources|people (ops|operations|partner|team)|onboarding specialist|hris|compensation|benefits (specialist|admin)|sourcer",
    "Legal & Compliance": r"legal|paralegal|attorney|lawyer|counsel\b|compliance|\baml\b|\bkyc\b|regulatory|contracts? (manager|specialist|administrator)|privacy|risk (analyst|manager)|fraud",
    "Translation & Interpretation": r"translat|interpret|linguist|localiz|subtitl|language specialist|bilingual",
    "Research": r"research(er)?\b|insight|user research|market research|policy analyst|scientist",
    "Supply Chain & Procurement": r"procurement|purchasing|supply chain|logistics|sourcing (specialist|manager)|buyer|vendor management|inventory|fulfil",
    "Trust, Safety & Moderation": r"moderat|trust (&|and) safety|content review|community (safety|support)|policy enforcement|abuse|investigations? analyst",
}
_TAX_RE = {k: re.compile(v, re.I) for k, v in TAXONOMY.items()}
_TAX_ORDER = list(TAXONOMY)


def assess_categories(title, description):
    t = title or ""
    desc = clean_text(description)[:900]
    scores = {}
    for cat, rx in _TAX_RE.items():
        s = 0
        s += 4 * len(rx.findall(t))
        s += min(2, len(rx.findall(desc))) * 0.6
        if s:
            scores[cat] = s
    if not scores:
        return "Other", ["Other"]
    ranked = sorted(scores.items(), key=lambda kv: (-kv[1], _TAX_ORDER.index(kv[0])))
    primary = ranked[0][0]
    cats = [c for c, s in ranked if s >= 3.0 or c == primary][:3]
    return primary, cats


# ── Quality / safety flags ────────────────────────────────────────────

COMMISSION_ONLY_RE = re.compile(r"\b(?:commission|performance)[- ]only\b|\b100% commission\b|\bstraight commission\b|\bno (?:base|fixed|guaranteed) (?:salary|pay|wage)\b|\bunpaid (?:trial|training|test)\b", re.I)
APPLICANT_FEE_RE = re.compile(
    r"\b(?:registration|application|processing|training|starter kit|onboarding|background check|equipment|admin)\s+fee\b"
    r"|\byou (?:will )?(?:need|have|must) to (?:pay|purchase|buy|invest|deposit)\b|\bpurchase (?:your own )?(?:equipment|kit|laptop|software)\b"
    r"|\bdeposit (?:is )?required\b|\b(?:send|wire|transfer) (?:us )?(?:money|funds)\b|\bcashier'?s? check\b|\bcheck to deposit\b|\bpay (?:a |an )?(?:small )?(?:fee|deposit)\b", re.I)
SCAM_CONTACT_RE = re.compile(r"\b(?:interview|apply|contact|hiring manager)\b[^.]{0,50}\b(?:telegram|whatsapp|signal|hangouts)\b|\b(?:telegram|whatsapp)\b[^.]{0,50}\b(?:interview|hiring|apply)\b|\b@(?:gmail|yahoo|outlook|hotmail)\.com\b", re.I)
UNREALISTIC_PAY_RE = re.compile(r"\bearn (?:up to )?\$?\d{3,}\s*(?:/|per|a)\s*(?:day|hour)\b.{0,40}\bno experience\b|\bget paid (?:daily|instantly)\b", re.I)


def assess_quality(title, description):
    text = clean_text(description) + " " + (title or "")
    flags, reason, exclude = [], None, False
    if COMMISSION_ONLY_RE.search(text):
        flags.append("commission_only_or_unpaid"); exclude = True; reason = "commission-only or unpaid work"
    if APPLICANT_FEE_RE.search(text):
        flags.append("applicant_fee"); exclude = True; reason = "asks applicants to pay or send money"
    if SCAM_CONTACT_RE.search(text):
        flags.append("suspicious_contact")
    if UNREALISTIC_PAY_RE.search(text):
        flags.append("unrealistic_pay_claim")
    return {"flags": flags, "exclude": exclude, "reason": reason, "review": bool(flags) and not exclude}


# ── Public API ────────────────────────────────────────────────────────

def classify_listing(title, location="", description="", hint=None, declared_type=None, remote_feed=False):
    work = assess_work_arrangement(title, location, description, hint=hint, remote_feed=remote_feed)
    elig = assess_eligibility(title, location, description,
                              remote_evidence=work["arrangement"] in (FULLY_REMOTE, REMOTE_UNCLEAR),
                              remote_feed=remote_feed)
    if (work["arrangement"] == REMOTE_UNCLEAR and not remote_feed and elig["type"] in ("countries", "region")
            and elig["evidence"] and all(e["signal"] in ("location field", "title") for e in elig["evidence"])):
        elig["notes"].append(f"The location field lists {elig['statedLocation']}, but the listing does not confirm the role is remote there.")
        elig.update({"type": "unclear", "label": "Eligibility unclear", "countries": [], "regions": [], "confidence": "low"})
    exp = assess_experience(title, description)
    primary, cats = assess_categories(title, description)
    quality = assess_quality(title, description)
    etypes = assess_employment_type(title, declared_type, description)

    arrangement = work["arrangement"]
    if arrangement in (FULLY_REMOTE,) and elig["type"] in ("countries", "region", "timezone"):
        arrangement = REMOTE_RESTRICTED
    elif arrangement == REMOTE_UNCLEAR and elig["type"] in ("countries", "region") and work["confidence"] != "low":
        arrangement = REMOTE_UNCLEAR

    confidence = work["confidence"]
    unresolved = list(work["unresolved"]) + list(elig["notes"] if elig["type"] == "unclear" else [])
    if elig["conflict"]:
        unresolved.append("Eligibility wording conflicts inside the listing.")

    return {
        "workArrangement": arrangement,
        "officeAttendance": work["attendance"],
        "eligibility": elig,
        "evidence": work["evidence"][:6],
        "confidence": confidence,
        "unresolvedQuestions": list(dict.fromkeys(unresolved)),
        "conflict": work["conflict"],
        "flags": work["flags"],
        "experience": exp,
        "primaryCategory": primary,
        "categories": cats,
        "employmentTypes": etypes,
        "quality": quality,
        "scores": work["scores"],
    }


def feed_decision(result):
    """Return (decision, reason): decision is 'publish', 'review' or 'exclude'."""
    q = result["quality"]
    if q["exclude"]:
        return "exclude", q["reason"]
    arr = result["workArrangement"]
    if result["conflict"]:
        return "review", "contradictory remote/office information"
    if arr == HYBRID:
        return "exclude", "hybrid: office attendance required"
    if arr == ON_SITE:
        return "exclude", "on-site or no evidence of remote work"
    if q["review"]:
        return "review", "suspicious wording: " + ", ".join(q["flags"])
    return "publish", arr
