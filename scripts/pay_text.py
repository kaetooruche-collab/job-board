"""Copy a pay range out of a posting's own text, exactly as the employer wrote it. Never estimate, never convert.

Only a sentence that is clearly about pay and contains a range like "$147,800 - $226,700" counts.
"""
import re

import classify as C

RANGE_RE = re.compile(r"((?:[$€£]|USD|EUR|GBP|CAD|AUD)\s?\d{2,3}(?:,\d{3})+(?:\.\d+)?)\s*(?:-|–|—|to)\s*((?:[$€£]|USD|EUR|GBP|CAD|AUD)?\s?\d{2,3}(?:,\d{3})+(?:\.\d+)?)", re.I)
PAY_WORDS_RE = re.compile(r"\b(?:salary|base pay|base salary|pay range|pay ranges|compensation|starting (?:salary|pay)|on-target earnings|OTE|total target|annual (?:base|pay|salary))\b", re.I)
NOT_PAY_RE = re.compile(r"\b(?:revenue|funding|raised|valuation|budget|ARR|stipend|bonus of up to|signing bonus|relocation|contract value|deal size|quota)\b", re.I)


def _num(s):
    return float(re.sub(r"[^\d.]", "", s))


def pay_from_text(description):
    text = C.clean_text(description or "")
    found = []
    for m in RANGE_RE.finditer(text):
        ctx = text[max(0, m.start() - 160): m.end() + 80]
        near = text[max(0, m.start() - 50): m.end() + 30]  # words about something else must be right next to the number
        if not PAY_WORDS_RE.search(ctx) or NOT_PAY_RE.search(near):
            continue
        lo, hi = m.group(1).strip(), m.group(2).strip()
        if _num(lo) <= _num(hi) <= 5 * _num(lo):  # reject nonsense spans
            found.append((_num(lo), _num(hi), lo, hi))
    if not found:
        return None
    if len({(f[0], f[1]) for f in found}) == 1:
        _, _, lo, hi = found[0]
        return f"{lo} - {hi}"
    lo = min(found, key=lambda f: f[0]); hi = max(found, key=lambda f: f[1])
    return f"{lo[2]} - {hi[3]} (varies by location)"
