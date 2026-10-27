"""Copy a pay range out of a posting's own text, exactly as the employer wrote it. Never estimate, never convert.

Only a sentence that is clearly about pay and contains a range like "$147,800 - $226,700" counts.
"""
import re

import classify as C

RANGE_RE = re.compile(r"((?:[$€£]|USD|EUR|GBP|CAD|AUD)\s?\d{2,3}(?:,\d{3})+(?:\.\d+)?)\s*(?:-|–|—|to)\s*((?:[$€£]|USD|EUR|GBP|CAD|AUD)?\s?\d{2,3}(?:,\d{3})+(?:\.\d+)?)", re.I)
PAY_WORDS_RE = re.compile(r"\U0001F4B0|\b(?:salary|base pay|base salary|pay range|pay ranges|compensation|starting (?:salary|pay)|on-target earnings|OTE|total target|annual (?:base|pay|salary))\b", re.I)
NOT_PAY_RE = re.compile(r"\b(?:revenue|funding|raised|valuation|budget|ARR|stipend|bonus of up to|signing bonus|relocation|contract value|deal size|quota)\b", re.I)
# The label must sit directly in front of the figures ("New hire equity: $16,000"). A word further
# back — "Annual base salary range (excluding equity and bonus): $135,320" — is about something
# else and must not cost the listing its pay line.
LABEL_NOT_PAY_RE = re.compile(r"\b(?:equity|stocks?|options?|RSUs?|signing|retention|grants?|refresh|commissions?|stipends?|allowances?|severance|deferred|bonus|awards?)\s*[:\-–—=]?\s*$", re.I)
CODE_RE = re.compile(r"\b(USD|EUR|GBP|CAD|AUD|CHF)\b", re.I)


def _num(s):
    return float(re.sub(r"[^\d.]", "", s))


# How far back a pay word ("salary", "compensation", 💰…) may sit and still vouch for a range.
# Employers often put the heading first and the figures in a list underneath ("Zone A: $112,000 -
# $135,000"), so the word can be several lines above the number. Widen with care: a longer window
# is a looser claim that the numbers are pay.
PAY_LOOKBACK = 400
PAY_LOOKAHEAD = 80


def _currency_code(text, start, end, lookback=None):
    """The currency named for this range: the nearest code written *before* it, else the nearest one after.

    Employers name the currency once for a block ("figures cited below are in USD") and then list the
    zones, so the code sits above the number — and a later block renames it for its own figures.
    Looking backwards first is what keeps a Canadian section from relabelling the American one above it.
    """
    lookback = PAY_LOOKBACK if lookback is None else lookback
    base = max(0, start - lookback)
    before, after = [], []
    for m in CODE_RE.finditer(text[base:end + 40]):
        a, b = base + m.start(), base + m.end()
        code = m.group(1).upper()
        if b <= start:
            before.append((start - b, code))
        elif a >= end:
            after.append((a - end, code))
        else:
            before.append((0, code))          # the code is part of the range itself, e.g. "CAD 120,000"
    for pool in (before, after):
        if not pool:
            continue
        pool.sort()
        if len(pool) > 1 and pool[0][0] == pool[1][0] and pool[0][1] != pool[1][1]:
            return None                        # two currencies equally close: refuse to guess
        return pool[0][1]
    return None


def pay_from_text(description, lookback=None):
    lookback = PAY_LOOKBACK if lookback is None else lookback
    text = C.clean_text(description or "")
    found = []
    for m in RANGE_RE.finditer(text):
        ctx = text[max(0, m.start() - lookback): m.end() + PAY_LOOKAHEAD]
        near = text[max(0, m.start() - 50): m.end() + 30]  # words about something else must be right next to the number
        label = text[max(0, m.start() - 60):m.start()]
        if not PAY_WORDS_RE.search(ctx) or NOT_PAY_RE.search(near) or LABEL_NOT_PAY_RE.search(label):
            continue
        lo, hi = m.group(1).strip(), m.group(2).strip()
        if _num(lo) <= _num(hi) <= 5 * _num(lo):  # reject nonsense spans
            found.append((_num(lo), _num(hi), lo, hi, _currency_code(text, m.start(), m.end(), lookback)))
    if not found:
        return None

    # Never mix currencies into one span: a posting that lists USD zones and a Canadian range would
    # otherwise produce a figure that is true of neither. Keep the largest single-currency group.
    buckets = {}
    for f in found:
        buckets.setdefault(f[4], []).append(f)
    code = sorted(buckets, key=lambda k: (-len(buckets[k]), k is None))[0]
    rows = buckets[code]

    if len({(r[0], r[1]) for r in rows}) == 1:
        body, varies = f"{rows[0][2]} - {rows[0][3]}", ""
    else:
        lo = min(rows, key=lambda r: r[0])
        hi = max(rows, key=lambda r: r[1])
        body, varies = f"{lo[2]} - {hi[3]}", " (varies by location)"
    return body + (f" {code}" if code else "") + varies   # the employer named it; show it