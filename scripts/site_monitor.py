"""Checks the LIVE site every few hours and fails loudly (GitHub emails the repo owner) when something is wrong.

It tests what a visitor sees, not what the pipeline intended: pages load, the job data is fresh and
sane, tracking is present, forbidden wording has not crept in, prices and contact details are the
approved ones, and a random sample of apply links still opens.
"""
import json
import os
import random
import re
import sys

import requests

SITE = os.environ.get("SITE_URL", "https://northcyprusremotejobboard.vercel.app").rstrip("/")
PAGES = ["/", "/services", "/verify", "/privacy"]
APPROVED_EMAIL = "trueremote.jobs@gmail.com"
WHATSAPP_NUMBER = "905338225854"
FORBIDDEN = ["no work permit needed", "the only job board", "premium pay", "payhip", "guaranteed job", "guaranteed interview", "continues until you do", "until the target is reached", "until you reach 500"]
PRICES = ["$29", "$49", "$149", "$99"]
UA = {"User-Agent": "Mozilla/5.0 (compatible; site-monitor)"}
SAMPLE = 12

fails, warns = [], []


def get(path, **kw):
    return requests.get(SITE + path if path.startswith("/") else path, headers=UA, timeout=30, **kw)


def main():
    html = {}
    for p in PAGES:
        try:
            r = get(p)
        except requests.RequestException as e:
            fails.append(f"{p}: could not load ({e})"); continue
        if r.status_code != 200:
            fails.append(f"{p}: HTTP {r.status_code}"); continue
        html[p] = r.text

    for p, t in html.items():
        low = t.lower()
        if "kayzglobal.goatcounter.com/count" not in t:
            fails.append(f"{p}: GoatCounter script missing")
        for w in FORBIDDEN:
            if w in low:
                fails.append(f"{p}: forbidden wording found: '{w}'")
        for addr in set(re.findall(r"mailto:([^\"'?<>\s]+)", t)):
            if addr.lower() != APPROVED_EMAIL:
                fails.append(f"{p}: unexpected email address {addr}")
        for num in set(re.findall(r"wa\.me/(\d+)", t)):
            if num != WHATSAPP_NUMBER:
                fails.append(f"{p}: unexpected WhatsApp number {num}")
        if re.search(r"<script[^>]+src=[\"']https?://(?!gc\.zgo\.at)", t):
            warns.append(f"{p}: loads a script from another site; check it is intended")
    if "/services" in html:
        for pr in PRICES:
            if pr not in html["/services"]:
                fails.append(f"/services: approved price {pr} not shown")
        if "payhip" in html["/services"].lower() or "checkout" in html["/services"].lower().replace("no online checkout", ""):
            fails.append("/services: mentions a checkout; there must be no on-site payment")

    # job data
    rows = []
    try:
        r = get("/jobs.json")
        rows = r.json()
    except Exception as e:  # noqa: BLE001
        fails.append(f"/jobs.json: could not read ({e})")
    if rows:
        from datetime import datetime, timezone
        newest = max(x["postedAt"] for x in rows)
        age_h = (datetime.now(timezone.utc) - datetime.fromisoformat(newest.replace("Z", "+00:00"))).total_seconds() / 3600
        if len(rows) < 150:
            fails.append(f"jobs.json: only {len(rows)} listings")
        if age_h > 48:
            fails.append(f"jobs.json: newest listing is {age_h:.0f} hours old; the refresh may be stuck")
        ids = [x["id"] for x in rows]
        if len(ids) != len(set(ids)):
            fails.append("jobs.json: duplicate listing ids")
        sample = random.sample(rows, min(SAMPLE, len(rows)))
        dead, inconclusive = [], 0
        for x in sample:
            try:
                rr = requests.get(x["sourceUrl"], headers=UA, timeout=20, allow_redirects=True)
                final = rr.url.lower()
                if rr.status_code in (404, 410) or "error=true" in final:
                    dead.append(f"{x['title']} at {x['company']} -> HTTP {rr.status_code}")
                elif rr.status_code in (401, 403, 429):
                    inconclusive += 1
            except requests.RequestException:
                inconclusive += 1
        if len(dead) > max(2, SAMPLE // 4):
            fails.append(f"{len(dead)} of {len(sample)} sampled apply links are dead: " + "; ".join(dead[:4]))
        elif dead:
            warns.append(f"{len(dead)} of {len(sample)} sampled apply links are dead (listings close; the next refresh removes them): " + "; ".join(dead[:3]))
        print(f"checked {len(html)} pages, {len(rows)} listings, newest {age_h:.1f}h old, sampled {len(sample)} links ({inconclusive} inconclusive)")
    for w in warns:
        print("WARN:", w)
    for f in fails:
        print("FAIL:", f)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
