#!/usr/bin/env python3
"""Guardrail checker for Yireh Careers social posts (the skill's checklist, made automatic).

Usage:
    python3 social/tools/check_post.py social/calendar/2026-12-01.posts.json            # draft mode
    python3 social/tools/check_post.py social/calendar/2026-12-01.posts.json --mode schedule
    python3 social/tools/check_post.py --text "Some caption" --platform instagram

A posts file is a JSON list (or {"posts": [...]}) of post specs:
    id, date (YYYY-MM-DD), platforms [tiktok|instagram|facebook], pillar (jobs|tips|proof|service|brand),
    format (video|image|carousel|text), on_screen [str], script str, caption str,
    ai_presenter bool, ai_voice bool, ai_label bool, measured_on (YYYY-MM-DD, the day the numbers were measured),
    allow_countries [str]  (only with KT's recorded approval; say where in `allow_reason`).

BLOCK findings fail the run (exit 1). WARN findings are printed and need a human look.
Rules come from CLAUDE.md, drafts/voice-and-copy-guide.md and .claude/skills/social-agency/SKILL.md.
Nothing here edits a post: it only reports.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GEO = ROOT / "data" / "geo_lexicon.json"

BLOCK, WARN = "BLOCK", "WARN"


@dataclass
class Finding:
    level: str
    rule: str
    detail: str

    def __str__(self) -> str:
        return f"{self.level:5} {self.rule}: {self.detail}"


# ---------------------------------------------------------------- forbidden wording (CLAUDE.md + skill)
# Each entry: rule id, regex (case-insensitive), what to say instead.
FORBIDDEN = [
    ("guarantee", r"\bguarantee[sd]?\b|\bguaranteeing\b", "never promise an outcome"),
    ("the-only", r"\bthe only\b|\bonly (?:legit|real|genuine|verified) (?:job )?(?:board|site)\b", "no 'the only' claims"),
    ("direct-to-employer",
     r"\b(?:direct(?:ly)?|straight) (?:link )?(?:to|from) the (?:employer|company)\b"
     r"|\bapply directly\b|\bdirect link to the employer\b",
     "say 'opens the original posting'"),
    ("employer-own-page", r"\bemployers?['’]s? own (?:posting|page|career|careers|site|website|job)", "say 'the company's hiring page'"),
    ("suits-background",
     r"\b(?:perfect|ideal|great|suitable|made) for (?:students?|graduates?|grads|freshers|beginners|nurses|pharmacists|moms|mums)\b"
     r"|\bsuits? (?:your|a|any) (?:degree|background)\b|\bfor (?:students|graduates)\b",
     "never claim a role suits a background; say 'entry-level and junior'"),
    ("scam-cta",
     r"\bdm (?:me|us)\b|\bsend (?:me|us) a dm\b|\binbox (?:me|us)\b|\bmessage (?:me|us) for\b"
     r"|\bcomment [\"'“‘]?[a-z]+[\"'”’]? (?:for|to get|and (?:i|we)(?:'|’)ll)\b|\bcomment (?:for|to get) the (?:list|link)\b"
     r"|\bsend (?:me|us) your cv\b",
     "the CTA is the link in bio; never DM or comment-for-the-list (the scam script)"),
    ("work-permit", r"\bno (?:work permit|visa|work authori[sz]ation) (?:needed|required)\b", "never say no permit needed"),
    ("all-remote-jobs", r"\ball (?:the )?remote jobs\b|\bevery remote job\b", "we list hundreds of companies, not all"),
    ("every-job-shows", r"\bevery (?:job|listing) shows who can apply\b", "about 1 in 7 jobs do not say"),
]

# No public post names a hiring system (KT, 25 Nov 2026). Proper nouns that are also English words are
# matched case-sensitively (Lever, Workday); the rest case-insensitively.
HIRING_SYSTEMS_CI = ["greenhouse", "ashby", "recruitee", "personio", "workable", "smartrecruiters", "bamboohr",
                     "icims", "teamtailor", "jobvite", "breezy hr", "jazzhr", "taleo", "successfactors"]
HIRING_SYSTEMS_CS = ["Lever", "Workday"]

# "Free / never charge you to apply" is said once, never stacked (skill, rule 7).
FREE_PATTERNS = [r"\bnever charge\w*\b", r"\bno fees?\b", r"\b(?:it(?:'|’)s|completely|always|100%) free\b",
                 r"\bfree to (?:use|apply|search)\b", r"^free[.!]?$"]

# Common misspellings seen in this niche, checked even without a dictionary.
KNOWN_TYPOS = {"dosen't": "doesn't", "dosent": "doesn't", "doesnt": "doesn't", "recieve": "receive",
               "oppurtunity": "opportunity", "oppotunity": "opportunity", "remotly": "remotely",
               "aplly": "apply", "applicaton": "application", "seperate": "separate", "untill": "until",
               "wont": "won't", "cant": "can't", "youre": "you're", "theyre": "they're", "its'": "it's"}

# Words the dictionary does not know but we use on purpose.
BRAND_WORDS = {"yireh", "yai-ray", "yirehcareers", "vercel", "app", "utm", "tiktok", "instagram", "facebook",
               "linkedin", "whatsapp", "cv", "cvs", "emea", "apac", "anz", "latam", "reels", "reel", "dm", "dms",
               "fyp", "wfh", "ai", "ok", "postiz", "goatcounter", "online", "onboarding", "carousel", "screenshot",
               "remotejobs", "remotework", "jobsearch", "workfromhome", "worldwide", "eu", "hr", "fp&a", "saas",
               "devops", "postgres", "supabase", "it's", "you're", "we're", "we've", "don't", "doesn't", "isn't",
               "can't", "won't", "that's", "here's", "there's", "they're", "you've", "you'll", "we'll", "what's",
               "let's", "i'm", "i've", "hasn't", "aren't", "wasn't", "didn't", "jobseekers", "remotejob",
               "jobhunting", "careertips", "cvtips", "jobtips", "remoteworklife", "hiringnow", "nov", "dec",
               "mon", "tue", "wed", "thu", "fri", "sat", "sun", "utc", "fully-remote", "region-wide",
               "entry-level", "mid-level", "e.g", "etc", "vs", "pm", "am", "bio", "yai", "asia", "africa", "europe", "americas", "telegram", "jobscams"}

PLATFORM_CAPTION_LIMITS = {"instagram": 2200, "tiktok": 2200, "facebook": 63206}  # TikTok video: 2,200 (photo: 4,000)
PLATFORM_HASHTAG_LIMITS = {"instagram": 5, "tiktok": 5, "facebook": 5}            # IG hard cap 5 (Dec 2025); skill: 3 to 5
HIRING_SYSTEM_NOTE = "no public post names a hiring system (KT, 25 Nov 2026)"


def _load_geo():
    """Countries and their aliases (blocked) and demonyms (warned; they double as language names)."""
    try:
        data = json.loads(GEO.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return [], []
    names, demonyms = [], []
    for c in data.get("countries", []):
        names.append(c["name"])
        for a in c.get("aliases", []):
            if a == "america":      # "North America" and "the Americas" are regions
                continue
            # Short aliases ("us", "uk", "uae") only count in capitals, so the pronoun "us" never trips it.
            names.append(a.upper() if len(a.replace(".", "")) <= 3 else a)
        demonyms.extend(c.get("demonyms", []))
    # Short upper-case forms are matched case-sensitively so "us" the pronoun never trips it.
    # ("America" is left out on purpose: "North America" and "the Americas" are regions, not countries.)
    names.extend(["US", "U.S.", "USA", "U.S.A.", "UK", "UAE", "KSA"])
    return names, demonyms


GEO_NAMES, GEO_DEMONYMS = _load_geo()


def _country_hits(text: str, allow: set[str]) -> tuple[list[str], list[str]]:
    hits, soft = [], []
    for name in GEO_NAMES:
        if name.lower() in allow or name in allow:
            continue
        short = len(name.replace(".", "")) <= 3
        if short:
            pat = r"(?<![A-Za-z])" + re.escape(name) + r"(?![A-Za-z])"
            if re.search(pat, text):  # case-sensitive
                hits.append(name)
        elif re.search(r"\b" + re.escape(name) + r"\b", text, re.I):
            # "Georgia" and "Jordan" are also names; still block: the rule is about what the reader sees.
            hits.append(name)
    for d in GEO_DEMONYMS:
        if d.lower() in allow:
            continue
        if re.search(r"\b" + re.escape(d) + r"\b", text, re.I):
            soft.append(d)
    # "South Africa" also matches "Africa"? No: Africa is a region, not in the country list.
    return sorted(set(hits)), sorted(set(soft))


def _strip_for_spelling(text: str) -> str:
    text = re.sub(r"https?://\S+|\b\S+\.(?:app|com|io|co|org)\S*", " ", text)  # URLs
    text = re.sub(r"[#@][\w.]+", " ", text)                                       # hashtags, handles
    return text


def _words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z][A-Za-z'’&-]*[A-Za-z]|[A-Za-z]", text)


_SPELL = None


def _spell():
    global _SPELL
    if _SPELL is None:
        try:
            from spellchecker import SpellChecker  # pyspellchecker, MIT; social/tools/requirements.txt
            _SPELL = SpellChecker()
        except ImportError:
            _SPELL = False
    return _SPELL


def check_spelling(text: str, extra_ok: set[str]) -> list[Finding]:
    out = []
    clean = _strip_for_spelling(text)
    words = [w.replace("’", "'") for w in _words(clean)]
    for w in words:
        lw = w.lower()
        if lw in KNOWN_TYPOS:
            out.append(Finding(BLOCK, "spelling", f"'{w}' should be '{KNOWN_TYPOS[lw]}'"))
    sp = _spell()
    if sp is False:
        out.append(Finding(WARN, "spelling", "pyspellchecker not installed; only the known-typo list was checked"))
        return out
    ok = BRAND_WORDS | {e.lower() for e in extra_ok}
    candidates = set()
    for w in words:
        lw = w.lower()
        if lw in ok or lw in KNOWN_TYPOS or len(lw) < 3 or w.isupper():
            continue
        for part in re.split(r"[-&]", lw):
            part = part.strip("'")
            if part.endswith("'s"):
                part = part[:-2]
            if len(part) >= 3 and part not in ok:
                candidates.add(part)
    for w in sorted(sp.unknown(candidates)):
        if w in ok:
            continue
        guess = sp.correction(w)
        out.append(Finding(BLOCK, "spelling", f"'{w}' is not in the dictionary" + (f" (did you mean '{guess}'?)" if guess and guess != w else "")
                           + "; if it is a real name, add it to the post's spelling_ok list"))
    return out


def _all_text(post: dict) -> dict[str, str]:
    parts = {
        "on_screen": "\n".join(post.get("on_screen") or []),
        "script": post.get("script") or "",
        "caption": post.get("caption") or "",
    }
    for i, slide in enumerate(post.get("slides") or (post.get("render") or {}).get("slides") or []):
        # "t" (slide type) and "n" (the tip's number) are layout, not claims
        parts[f"slide {i + 1}"] = "\n".join(str(v) for k, v in slide.items() if isinstance(v, str) and k not in ("t", "n", "id"))
    return parts


def check_post(post: dict, mode: str = "draft") -> list[Finding]:
    f: list[Finding] = []
    parts = _all_text(post)
    full = "\n".join(parts.values())
    allow = {a for a in (post.get("allow_countries") or [])}
    allow_l = {a.lower() for a in allow} | allow

    # 1. Forbidden wording
    for rule, pat, fix in FORBIDDEN:
        for where, txt in parts.items():
            m = re.search(pat, txt, re.I | re.M)
            if m:
                f.append(Finding(BLOCK, rule, f"'{m.group(0)}' in {where}: {fix}"))
    for name in HIRING_SYSTEMS_CI:
        if re.search(r"\b" + re.escape(name) + r"\b", full, re.I):
            f.append(Finding(BLOCK, "hiring-system", f"'{name}': {HIRING_SYSTEM_NOTE}"))
    for name in HIRING_SYSTEMS_CS:
        if re.search(r"\b" + re.escape(name) + r"\b", full):
            f.append(Finding(BLOCK, "hiring-system", f"'{name}': {HIRING_SYSTEM_NOTE}"))

    # 2. Countries (KT, 26 Nov 2026: no country named in videos; the plan extends it to role posts)
    hits, soft = _country_hits(full, allow_l)
    for h in hits:
        f.append(Finding(BLOCK, "country", f"'{h}' is named; no country in posts (KT, 26 Nov 2026)"))
    for d in soft:
        f.append(Finding(WARN, "country-word", f"'{d}' may read as a country (or is a language); check it"))
    if allow and not post.get("allow_reason"):
        f.append(Finding(BLOCK, "country", "allow_countries is set without allow_reason (where KT approved it)"))

    # 3. Numbers must be measured on the live board, on the post day when scheduling
    numbers = re.findall(r"(?<![\w/.:#-])\d[\d,]*(?:\.\d+)?%?(?![\w:])", _strip_for_spelling(parts["on_screen"] + "\n" + parts["script"] + "\n" + parts["caption"] + "\n" + "\n".join(v for k, v in parts.items() if k.startswith("slide"))))
    numbers = [n for n in numbers if not re.fullmatch(r"20\d\d", n)]  # years
    if numbers:
        mo = post.get("measured_on")
        if not mo:
            f.append(Finding(BLOCK, "numbers", f"numbers {numbers[:5]} have no measured_on date"))
        elif mode == "schedule" and mo != post.get("date"):
            f.append(Finding(BLOCK, "numbers", f"numbers measured {mo}, post goes out {post.get('date')}: re-measure on the day"))
        elif mode == "draft" and mo != post.get("date"):
            f.append(Finding(WARN, "numbers", f"numbers measured {mo}; re-measure on {post.get('date')} before scheduling"))
        # Numbers that are our own service terms (read from a page) need no "live board" date line.
        if post.get("format") in ("video", "image", "carousel") and not post.get("number_dated_on_screen", False) \
                and not post.get("numbers_source"):
            f.append(Finding(BLOCK, "numbers", "a number is shown but the on-screen date line is missing (set number_dated_on_screen when the date is on the media)"))

    # 4. Spelling
    f.extend(check_spelling(full, set(post.get("spelling_ok") or [])))

    # 5. AI label
    if (post.get("ai_presenter") or post.get("ai_voice")) and not post.get("ai_label"):
        f.append(Finding(BLOCK, "ai-label", "AI presenter or cloned/AI voice without ai_label: true"))

    # 6. Featured jobs must be re-opened before scheduling
    if post.get("featured_jobs"):
        for j in post["featured_jobs"]:
            if mode == "schedule" and not j.get("checked_open_on") == post.get("date"):
                f.append(Finding(BLOCK, "featured-open", f"{j.get('id')}: posting not re-opened on the post day"))
            elif not j.get("checked_open_on"):
                f.append(Finding(WARN, "featured-open", f"{j.get('id')}: posting not opened yet"))

    # 7. Free claim said once
    free_hits = sum(len(re.findall(p, txt, re.I | re.M)) for p in FREE_PATTERNS for txt in (parts["script"], parts["caption"], parts["on_screen"]))
    if free_hits > 2:
        f.append(Finding(BLOCK, "free-stacked", f"'free / never charge / no fee' appears {free_hits} times; say it once"))
    elif free_hits == 2:
        f.append(Finding(WARN, "free-stacked", "'free / never charge' appears twice (fine only if once spoken, once on screen)"))

    # 8. The CV service never inside a jobs post
    if post.get("pillar") == "jobs" and re.search(r"\bcv (?:service|check|writing|rewrite)\b|\$\s?\d|\bpackage\b", full, re.I):
        f.append(Finding(BLOCK, "service-in-jobs-post", "the CV service is never promoted inside a jobs post"))

    # 9. Platform limits, hashtags, links
    cap = parts["caption"]
    tags = re.findall(r"(?<!\w)#\w+", cap)
    for p in post.get("platforms") or []:
        lim = PLATFORM_CAPTION_LIMITS.get(p)
        if lim and len(cap) > lim:
            f.append(Finding(BLOCK, "caption-length", f"{p}: {len(cap)} characters, limit {lim}"))
        hl = PLATFORM_HASHTAG_LIMITS.get(p)
        if hl is not None and len(tags) > hl:
            f.append(Finding(BLOCK if p == "instagram" else WARN, "hashtags", f"{p}: {len(tags)} hashtags, ours max {hl}"))
    for url in re.findall(r"https?://\S*yirehcareers\S*", full):
        if "utm_source=" not in url:
            f.append(Finding(WARN, "utm", f"{url} has no utm_source"))
    if cap and len(cap.split("\n", 1)[0]) > 125:
        f.append(Finding(WARN, "hook-length", "first caption line is over 125 characters; feeds cut it"))
    if full.count("!") > 1:
        f.append(Finding(WARN, "tone", "more than one exclamation mark (voice guide: at most one)"))
    if post.get("format") == "video" and not post.get("captions_burned_in", True):
        f.append(Finding(WARN, "captions", "video without burned-in captions"))

    # 10. Every post states its job in the funnel and the number that judges it (assessment, 27 Nov 2026)
    if "id" in post and post.get("id") != "text":
        if post.get("funnel") not in FUNNEL:
            f.append(Finding(BLOCK, "funnel", f"funnel must be one of {sorted(FUNNEL)}"))
        if not post.get("goal_metric"):
            f.append(Finding(BLOCK, "funnel", "goal_metric missing (the one number that says whether this post worked)"))
    return f


FUNNEL = {"awareness", "consideration", "conversion"}


def _norm_hook(post: dict) -> str:
    h = post.get("hook") or (post.get("caption") or "").split("\n", 1)[0]
    return re.sub(r"[^a-z0-9 ]+", "", re.sub(r"\d[\d,]*", "#", h.lower())).strip()


def check_repetition(posts: list[dict], window_days: int = 60) -> dict[str, list[Finding]]:
    """Hook repetition across posts (idea from safrin96/agentic-content-system's content-deduplicator, MIT).
    Near-identical hooks within the window block, unless both posts share a `series` (a recurring slot), which is
    only flagged. Numbers are masked so "19 jobs" and "36 jobs" count as the same hook."""
    import datetime as _dt
    from difflib import SequenceMatcher
    out: dict[str, list[Finding]] = {}
    ordered = sorted(posts, key=lambda p: (p.get("date", ""), p.get("id", "")))
    for i, p in enumerate(ordered):
        hp = _norm_hook(p)
        if not hp:
            continue
        for q in ordered[:i]:
            try:
                gap = (_dt.date.fromisoformat(p["date"]) - _dt.date.fromisoformat(q["date"])).days
            except (KeyError, ValueError):
                gap = 0
            if gap > window_days:
                continue
            ratio = SequenceMatcher(None, hp, _norm_hook(q)).ratio()
            if ratio >= 0.8:
                same_series = p.get("series") and p.get("series") == q.get("series")
                out.setdefault(p["id"], []).append(Finding(
                    WARN if same_series else BLOCK, "repeat-hook",
                    f"hook is {ratio:.0%} like {q['id']} ({q.get('date')})" + (" (same series)" if same_series else "; rewrite or mark both as one series")))
    return out


def load_posts(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data["posts"] if isinstance(data, dict) else data


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("posts", nargs="?", help="posts JSON file")
    ap.add_argument("--mode", choices=["draft", "schedule"], default="draft")
    ap.add_argument("--text", help="check a single piece of text as a caption")
    ap.add_argument("--platform", default="instagram")
    a = ap.parse_args(argv)
    if a.text is not None:
        posts = [{"id": "text", "caption": a.text, "platforms": [a.platform]}]
    elif a.posts:
        posts = load_posts(Path(a.posts))
    else:
        ap.error("give a posts file or --text")
    history = []
    if a.posts:
        for other in sorted(Path(a.posts).resolve().parent.glob("*.posts.json")):
            if other.resolve() != Path(a.posts).resolve():
                history += load_posts(other)
    reps = check_repetition(history + posts)
    blocked = 0
    for p in posts:
        fs = check_post(p, a.mode) + reps.get(p.get("id"), [])
        b = [x for x in fs if x.level == BLOCK]
        blocked += bool(b)
        status = "FAIL" if b else ("CHECK" if fs else "PASS")
        print(f"[{status}] {p.get('id')}")
        for x in fs:
            print("   ", x)
    print(f"\n{len(posts)} posts, {blocked} blocked ({a.mode} mode)")
    return 1 if blocked else 0


if __name__ == "__main__":
    sys.exit(main())
