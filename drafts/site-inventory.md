# Site inventory: Yireh Careers (job board and career services)

**Inspected 29 Oct 2026** on the live site https://yirehcareers.vercel.app, in a real browser at desktop (1280 px) and phone (390 px) width, plus the repository at commit `main` after PR #36. This file goes stale when either tool redesigns something: re-inspect after any big change and update the date. Read this before changing the site; it is the shared picture for Claude Code and the other coding tool.

**Result of the inspection:** all 10 pages return 200; no JavaScript errors; no failed requests; no horizontal overflow at either width; the 6-hourly refresh and 3-hourly monitor are running; 1,047 listings from 161 companies; the monitor sampled 12 apply links (2 inconclusive, a bot-blocking effect, not a failure).

## 1. Pages

| Path | Public? | Purpose | Height desktop / phone |
|---|---|---|---|
| `/` | public, indexed | Job board: hero, search, filters, guided finder, listings, signup, how we verify, platforms | 16,747 / 23,392 px |
| `/services` | public | CV, cover letter and LinkedIn packages, add-ons, proof, FAQ, terms | 6,356 / 9,115 |
| `/verify` | public | The six trust rules and how listings are checked | 2,577 / 3,202 |
| `/privacy` | public | Privacy policy (legal text; do not edit lightly) | 5,492 / 8,400 |
| `/free-check` | public | Free CV check request form (posts to `/api/subscribe`) | 1,034 / 1,199 |
| `/order` | private (noindex) | Order details form after a package is agreed (`?package=` prefill) | 956 / 1,074 |
| `/subscribed` | noindex | Confirmation landing page | 800 / 844 |
| `/thanks` | noindex | After card payment (information only; checkout is OFF) | 961 / 1,141 |
| `/kit` | private (noindex, no analytics) | Post kit: ready-to-copy posts from the live feed | 3,967 / 4,947 |
| `/mail` | private (noindex, no analytics) | Reply templates for order and service emails, copy into Gmail | 1,550 / 2,121 |

Other public files: `jobs.json` (the feed), `platforms.json`, `og-image.png`, favicons, `yc-logo.png` (used by emails), `/fonts`.

## 2. Home page, top to bottom (desktop offsets)
1. **Nav** (How We Verify, Get Job-Ready; hamburger on phone). Platforms was removed from the nav on 27 Oct.
2. **Hero** (0 to ~560): H1 "Verified remote jobs for every stage of your career", sub-line, three live stats (1,047 verified listings, 161 companies, "100% link-checked"), "Browse the jobs" jump button.
3. **Listings notice** and a quiet services offer ("Need help with your application?", y 788) above the job list.
4. **Guided finder** ("Let's narrow it down"), search box (ranked, substring-safe), experience row, field, country, job type, posted-within, pay filter, "confirmed remote only", clear filters; filters are remembered for returning visitors.
5. **Job list** (~y 1,200 to 14,400): 40 cards per page with "Show more". Each card: title, company, level, type, who can apply, pay if stated, posted date, source, "Why this label?", Apply, "Get a CV for this role" (opens WhatsApp).
6. **Email signup** (y 14,437): email, optional first name, level, unticked tips checkbox, honeypot.
7. **How we verify** (y 14,910): the six trust rules.
8. **Platforms you can sign up to** (y 15,305, the last section; 9 outside boards), then footer.

## 3. Services page, top to bottom
Hero (pain-led headline, free CV check + See packages, three trust points) -> pricing: Essential $29 (2 working days), Professional $49 (3), Executive $149 (30-day service) -> comparison table -> add-ons and LinkedIn Growth $99 a month -> before/after examples (fictional, labelled) -> free-check strip with 3 steps -> How we work -> What we promise and don't -> three-step process -> Executive deep dive and timeline -> refunds/privacy details (collapsed) -> 19 FAQ items -> final CTA. A sticky green "Free CV check" button follows the visitor on phone.

## 4. Forms and the API
`/api/subscribe` (Vercel function, key in env, origin allowlist, honeypot, rate limit): signup, free check, order, health. Never writes to a blocklisted Brevo contact; records consent date and wording version. Successful submissions fire GoatCounter events `conversion-signup` and `conversion-check`.

## 5. Measurement (GoatCounter, kayzglobal.goatcounter.com)
Home: `jobs-hero-jump`, `guide-finder`, `filter-level/-field/-country`, `service-nudge` (+ dismiss), `services-click-home-packages`, `platform-view`, `platform-click`, `apply-click`, `cv-click-*`. Services: hero, pricing (per package + question links), add-ons, growth, mid and final free-check, WhatsApp and email buttons, sticky button. Forms: conversion events above. The weekly numbers script (`scripts/gc_snapshot.py`, workflow `weekly-snapshot.yml`, Tuesdays 05:00 UTC) needs the repo secret `GOATCOUNTER_API_KEY` (KT to-do).

## 6. Automation and integrations
- **Feed:** GitHub Action every 6 h (`fetch-jobs.yml`): fetch, classify, QA rules, write `jobs.json` and reports.
- **Monitor:** every 3 h (`site-monitor.yml`): pages, freshness, approved prices/wording, icon files, sampled links.
- **Brevo (KAYZ Global Ltd):** lists Job alerts (11), Career tips (18), markers 19 and 20; templates 74-85; four automations; weekly digest campaign. **Weekly email routine:** Tuesdays 08:20 Istanbul, with Gmail and Brevo attached (see `drafts/kt-todo.md`).
- **Payments:** card checkout built but OFF (`mode: 'off'`). Orders go through WhatsApp.
- **Vercel:** static site plus one function; `cleanUrls`; noindex headers on `/thanks /kit /subscribed /order /mail`.

## 7. Claims on the page that must stay true
Prices $29 / $49 / $149 / $99 a month; delivery 2 / 3 working days (Executive 2 + 5); priority 1 working day $15; revision limits 2 / 3 / 3; free check about 10 a week, reply within 2 working days; "we never charge you to apply"; every listing links to the employer's own posting; pay only when stated; no "guaranteed", no outcome promises. See `drafts/decisions/2026-10-25-*.md`.

## 8. Findings from this inspection (nothing was changed in this pass)
1. **"100% link-checked" (hero stat) overstates.** The strategy review recorded 8 employer sites (31 listings) that did not visibly show the posting when opened and 6 bot-blocked links nobody could verify. The monitor samples 12 links; it does not check all. Suggest "Links checked every 6 hours" or a percentage taken from the real check results. Trust is the brand, so this one matters most.
2. **Home is very long on phone (23,392 px).** The email signup is at 85% of the page and platforms at 90%. Most visitors never reach either. A signup nearer the top (or after the first few cards) is the likeliest conversion win on the board.
3. **The Platforms section** lists 9 outside job boards. It is the last thing on the page, and a decision record exists (`2026-10-27-platforms-section.md`, kept but demoted). Two entries conflict with our own rules: **Jobicy** (we excluded it as a source because its dates are wrong) and **Toptal** (blocks automated checks, so unverified). See KT's question and my recommendation in the session notes; if removed from the home page, `/platforms` as a separate footer-linked page is the middle option.
4. **Hero audience wording**: "for students, graduates and career-changers" says who the board is for; keep it from drifting into "roles suit graduates" (copy rule).
5. **Executive LinkedIn setup is 5 working days but Professional (which includes LinkedIn setup) is 3.** Open decision for KT.
6. **GoatCounter key secret** is not yet added, so the weekly numbers report fails loudly each Tuesday until KT adds it.
7. **Whop sandbox descriptions** may still say 5 working days (cannot check from here); matters only when card checkout goes live.
8. **The older 25 Oct tone and conversion work** is intact (checked: delivery times, hero, `/mail`, logo, conversion events).
