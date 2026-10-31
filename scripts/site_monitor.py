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

SITE = os.environ.get("SITE_URL", "https://yirehcareers.vercel.app").rstrip("/")
PAGES = ["/", "/services", "/verify", "/privacy", "/thanks", "/free-check"]
APPROVED_EMAIL = "yirehcareers@gmail.com"
WHATSAPP_NUMBER = "905338225854"
FORBIDDEN = ["no work permit needed", "the only job board", "premium pay", "payhip", "guaranteed job", "guaranteed interview", "continues until you do", "until the target is reached", "until you reach 500", "kaeto career", "kayz global ltd", "kt-photo.webp", "founder, "]
PRICES = ["$29", "$49", "$149", "$99"]
UA = {"User-Agent": "Mozilla/5.0 (compatible; site-monitor)"}
SAMPLE = 12

fails, warns = [], []


LIVE_CHECKOUT = re.compile(r"^https://whop\.com/checkout/(plan|ch)_[A-Za-z0-9]+/?$")


def check_checkout(services_html):
    """The card buttons must point at the live Whop checkout, never a sandbox, and the copy must match the config."""
    try:
        cfg = get("/site-config.js").text
    except requests.RequestException as e:
        fails.append(f"/site-config.js: could not load ({e})"); return
    mode = re.search(r"checkout:\s*\{[^}]*?mode:\s*'(\w+)'", cfg, re.S)
    mode = mode.group(1) if mode else None
    urls = re.findall(r"(?:essential|professional):\s*'(https?://[^']*)'", cfg)
    if mode == "live":
        if len(urls) != 2 or not all(LIVE_CHECKOUT.match(u) for u in urls):
            fails.append(f"site-config.js: live checkout URLs are not https://whop.com/checkout/ch_... ({urls})")
    elif mode == "sandbox":
        fails.append("site-config.js: checkout mode is 'sandbox' on the live site; set 'live' with real URLs or 'off'")
    elif mode != "off":
        fails.append(f"site-config.js: checkout mode not recognised ({mode})")
    # mode "off": card buttons and card-payment copy stay hidden (services.html shows WhatsApp-only copy), nothing to check

def get(path, **kw):
    return requests.get(SITE + path if path.startswith("/") else path, headers=UA, timeout=30, **kw)


def check_api():
    """The form endpoint must be deployed and must refuse strangers. Neither call writes anything."""
    try:
        r = get("/api/subscribe")
        if r.status_code != 405:
            fails.append(f"/api/subscribe: GET should answer 405, got {r.status_code} (function missing or broken)")
        r = requests.post(SITE + "/api/subscribe", json={"form": "signup", "email": "monitor@example.com"}, timeout=20)
        if r.status_code != 403:
            fails.append(f"/api/subscribe: a post without our origin should be refused (403), got {r.status_code}")
        # Proves the Brevo key stored in Vercel still works (it can expire or be revoked). Writes nothing.
        r = requests.post(SITE + "/api/subscribe", json={"form": "health"}, headers={"Origin": SITE}, timeout=30)
        if r.status_code != 200:
            fails.append(f"/api/subscribe health check failed (HTTP {r.status_code}: {r.text[:120]}): the website forms are probably broken; the Brevo key in Vercel may have expired")
    except requests.RequestException as e:
        fails.append(f"/api/subscribe: could not check ({e})")


def main():
    html = {}
    check_api()
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
        if p in ("/", "/services", "/verify") and 'property="og:image"' not in t:
            fails.append(f"{p}: share preview tags (og:image) missing; links pasted into WhatsApp or Facebook would show no picture")
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
        if "payhip" in html["/services"].lower():
            fails.append("/services: mentions payhip; the approved card provider is Whop")
        check_checkout(html["/services"])
    if "/thanks" in html:
        low = html["/thanks"].lower()
        if 'name="robots"' not in low or "noindex" not in low:
            fails.append("/thanks: missing noindex meta tag")
        try:
            if "noindex" not in get("/thanks").headers.get("X-Robots-Tag", "").lower():
                fails.append("/thanks: X-Robots-Tag noindex header missing")
        except requests.RequestException as e:
            fails.append(f"/thanks: header check failed ({e})")
        for w in ("payment received", "payment confirmed", "order confirmed", "you have paid"):
            if w in low:
                fails.append(f"/thanks: claims a verified payment ('{w}'); the page cannot know that")

    # share image, tab icons and the email logo must open (the weekly emails load /yc-logo.png from here)
    for img in ("/og-image.png", "/favicon.svg", "/favicon-32.png", "/favicon.ico", "/apple-touch-icon.png", "/yc-logo.png"):
        try:
            ri = get(img)
            ctype = ri.headers.get("content-type", "")
            if ri.status_code != 200 or not (ctype.startswith("image/") or ctype.startswith("application/octet")):
                fails.append(f"{img}: HTTP {ri.status_code}, type {ctype}")
        except requests.RequestException as e:
            fails.append(f"{img}: could not load ({e})")

    # crawl basics: robots.txt must point at the sitemap, the sitemap must list the public pages
    try:
        rb = get("/robots.txt"); sm = get("/sitemap.xml")
        if rb.status_code != 200 or "Sitemap:" not in rb.text:
            fails.append("/robots.txt: missing or no Sitemap line")
        if sm.status_code != 200 or "<urlset" not in sm.text or f"{SITE}/services" not in sm.text:
            fails.append("/sitemap.xml: missing or does not list the public pages")
    except requests.RequestException as e:
        fails.append(f"crawl files: could not load ({e})")

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
