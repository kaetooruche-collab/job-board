# UX audit log

Newest first. Each entry: evidence (measured, with viewport and date) · likely cause · severity ·
business impact · what changed · how to tell if it worked. Nothing here is a guess presented as a
measurement; hypotheses are labelled **[H]**.

---

## 2026-10-28 · A-1 — The hero had no route to the jobs

**Evidence** (live site, measured on the deployed build):

| Element | 1440×900 desktop | 360×740 phone |
|---|---|---|
| Services block top | 591px (above fold) | 688px (above fold) |
| Search box top | **1,182px — 282px below fold** | **1,222px — 482px below fold** |
| First job card top | **2,081px — 1,181px below fold** | **1,685px — 945px below fold** |
| Hero contents | h1, tagline, paragraph, 3 stats — **zero links or buttons** | same |

A visitor who lands and does not scroll sees marketing and a services pitch, and no jobs, no search
and no way to reach them except scrolling about 1.3 screens.

**Likely cause:** the Phase-0 decision to move the services block above the listings (done to make
paid services discoverable) stacked hero → disclaimer → services → toolbar, and the hero itself was
never given a CTA because it had never needed one.

**Severity:** medium-high for a job board. **Business impact:** the free utility is the reason
anyone arrives and the thing that earns the trust the paid services sell on; putting it 1.3 screens
down risks a bounce before the product appears, and it costs the conversion path nothing to fix —
the services block stays exactly where Phase 0 put it. **[H]** on the bounce effect: unmeasured,
because there has been almost no traffic.

**What changed:** one anchor in the hero — "Browse the jobs ↓" → `#jobs` (the search toolbar),
styled with the existing accent, contrast-corrected for dark mode (white on `#60a5fa` is ~2:1, so
dark text is used on both dark-mode paths), `scroll-margin-top` so the fixed header does not cover
the search box, and a new GoatCounter event `jobs-hero-jump` so the click is counted. Synced with
URL state: `syncURL()` already preserves `location.hash`, so the anchor never fights filters.

**Verification:** 184 tests pass (5 new in `tests/test_hero_jobs.py`); browser pass at 1440 and
360 — button visible within the first screen on both, click lands with the search box at 167px/163px
from the top, `#jobs` in the URL, zero console errors.

**How to tell if it worked:** `jobs-hero-jump` events in GoatCounter (counts phone vs desktop via
the existing pattern) over the next two weeks; guardrail is that `services-click-home-*` must not
fall — if the jump steals attention from the services block, the two are in tension and KT decides
the order.

---

## 2026-10-28 · A-0 — Deployed-build baseline (clean pass)

Live site audited at 1440×900 and 360×740 after the 28 Oct deploy: **0px horizontal overflow** on
`/`, `/services` and `/verify`; **zero console errors or page errors** on any page; search ranks
correctly (query "software engineer" → top result "Software Engineer (Contract)"); nav is
`Yireh Careers · How We Verify · Get Job-Ready` (Platforms no longer in the nav); services H1 and
verify H1 render as written. This is the reference state future audits compare against.