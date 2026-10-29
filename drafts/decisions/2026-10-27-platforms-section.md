# Decision review: should the "Platforms you can sign up to" section exist, and where?

**Status: implemented 27 Oct 2026 on branch `freebuff/eef7defc2f751b126b46605f`.** Priority 0 of the
optimization brief. Prompted by KT: *"why are we advertising our competitors?"*

## 1. What was verified against the project (not assumed)

| Claim from the earlier assessment | Verified? | Evidence |
|---|---|---|
| The brief requires two labelled sections (open listings + platforms) | Yes | `CLAUDE.md`, Phase 1 |
| Only 17 of ~1,026 listings are open worldwide | Yes, current data | `jobs.json`: `worldwide` = 17 of 1,002; `countries` = 708, `unclear` = 250 |
| Section sits before the email signup | Yes | measured offsets: services 591 → **subscribe 14,675 → verify 15,199 → platforms 15,627** (before the change) |
| `Platforms` was in the primary nav *and* the mobile menu | Yes | `index.html`, two anchor links |
| No click measurement existed | Yes | `loadPlatforms()` rendered plain anchors; no event, no impression |
| Nothing in tests/scripts depends on the section | Yes | grep over `tests/`, `scripts/`, workflows: no matches |
| Platform destinations reachable | 8 of 9 | HTTP 200 from this machine. **Toptal returns 403 to any automated client here, including a real Chromium** (Cloudflare bot blocking) — unverified from this environment, left in place. |

## 2. Research (evidence strength labelled)

- **SEO — no competitor-link penalty.** Google's outbound-link documentation creates no special rule
  for competing destinations, and Google's own linking-out guidance says useful links are fine.
  [Qualify your outbound links](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links) ·
  [Linking out (Google Search Central, 2008)](https://developers.google.com/search/blog/2008/10/linking-out-often-its-just-applying).
  *Strong for "Google says no such rule"; no controlled ranking study exists either way.* SEO was
  assessed separately from attention, as instructed.
- **Trust from linking out — indirect only.** NN/g finds users judge credibility partly by a site's
  connections and transparency, but does not test competitor links.
  [NN/g, Trustworthiness in Web Design](https://www.nngroup.com/articles/trustworthy-design/).
  Google's 2008 post *speculates* relevant links may bring repeat visitors — practitioner opinion,
  not measurement. **No direct evidence found that recommending alternatives raises or lowers
  conversion or return visits.**
- **Navigation — primary nav is for core destinations; footers for secondary ones.**
  [NN/g Menu-Design Checklist](https://www.nngroup.com/articles/menu-design/) ·
  [NN/g Footers 101](https://www.nngroup.com/articles/footers/) ·
  [Baymard on footer links](https://baymard.com/research-articles/footer-links-ecommerce).
  *Indirect but consistent.*
- **Signup-before-resources ordering: no comparative evidence found** — treated as a hypothesis
  (see §5, how to evaluate).
- **Competitor inspection (direct observation).** Of seven sites inspected: Himalayas and Rezi do
  name alternative boards, but only in **editorial articles** that lead with their own product;
  NoDesk keeps a "Remote Job Boards" directory; We Work Remotely, Remote OK, Working Nomads and
  Teal show no competitor directory on their main pages; FlexJobs unverified (timeouts). **Nobody
  puts a competitor directory in the primary navigation of their homepage.**
- **GoatCounter capabilities (official docs).** Events carry path/title/referrer, no page-path field
  alongside an event ([events](https://goatcounter.com/help/events), [js API](https://goatcounter.com/help/js));
  sessions are IP+UA in memory for 8 hours, **no persistent identity → return-after-outbound-click
  cannot be measured** ([sessions](https://goatcounter.com/help/sessions)); a canonical URL changes
  the path GoatCounter reports ([path](https://goatcounter.com/help/path)).

## 3. Decision

**Retain the section; demote it (option 2).** The default hypothesis held, with these resolutions:

1. **Kept** — it addresses a real gap (17 worldwide-open listings out of 1,002; 250 whose eligibility
   the employer does not state), and no credible evidence shows outbound alternatives cause net harm.
   Removing it purely because it links out was rejected; keeping it purely because the brief says so
   was also rejected — the brief's *requirement* is two labelled sections, not nav prominence.
2. **`Platforms` removed from the primary nav and the mobile menu**; now linked from the **footer**
   (secondary destination → secondary navigation, per NN/g; matches the competitor norm).
3. **Moved after the email signup and the trust section** (subscribe → verify → platforms), so our
   two conversion asks come before the exits.
4. **Kinds are now distinguished** — `platforms.json` gained a `type` field (5 `board`, 4
   `marketplace`) rendered as a badge, and the intro copy says plainly that we check each page opens
   but **do not check their listings**, and therefore show no posting dates for them.
5. **Measured** — `platform-view` (IntersectionObserver, once, only when on screen) and
   `platform-click` (name + phone/desktop in the title, no personal data).
6. **Jobicy inconsistency resolved as "consistent"**: it is excluded from our *feed* because of its
   dates; as a *platform* entry the section shows no dates by design, so no date claim is made.

Also shipped alongside (same brief): `services-click-*` events for the home services block, the
nudge block and the `/free-check`, `/order` → `/services` bridges (previously unmeasured); an honest
load-error state (a failed `jobs.json` fetch now says "We could not load the listings" instead of the
false "No verified listings right now", and the hero counters show "—"); and filter state in the URL
(`?field=`, `?country=`, `?q=`, `?minsal=` … plus the existing `?level=`), with a canonical link so
filtered URLs don't fan out pageviews while campaign parameters stay in the URL.

## 4. What changed in code

`index.html` (nav, footer, section move + copy, canonical, load-error state, `readURL`/`syncURL`,
platform events, services-click events), `platforms.json` (9 × `type`), `site-forms.js`
(`trackEvt` helper), `free-check.html` and `order.html` (one tracked link each),
`tests/test_platforms.py` (9 new tests).

## 5. Verification and how to evaluate this with real behaviour

- `python3 -I -m unittest discover -s tests` → **168 tests, OK** (159 before + 9 new).
- Headless Chromium at 1440×900 and 360×740: nav and mobile menu free of `#platforms`, footer link
  present, section order measured (14,675 → 15,199 → 15,627), 9 cards with correct kind badges,
  `platform-view` and `platform-click` fired with mocked GoatCounter, `services-click-home-packages`
  fired, deep links `?level=early` (94 listings) and `?field=Sales&level=mid&minsal=60000&cur=USD&utm_source=kit`
  (27 listings, chips correct, `utm_source` preserved after changing a filter), `?q=nurse&country=Germany`
  (1 listing), forced 500 on `jobs.json` → "We could not load the listings" + "—", no app console
  errors, no horizontal overflow at 360px. Screenshots: `artifacts/ui-platforms.png`,
  `artifacts/ui-bottom-stack.png`.
- **Not verified:** Toptal's destination (bot-blocked from this machine); Safari/Firefox;
  whether anyone actually clicks these links (needs live traffic).

**Evaluation plan:** after ~2 weeks of traffic read `platform-view` vs `platform-click` (clicks per
impression), then `services-click-home-packages` / `-nudge-*` vs `conversion-check`. A near-zero
click rate on `platform-view` means the section is decoration — shrink it to one line or drop it; a
high rate with weak `conversion-check` means it is leaking intent — that argues for reordering, not
for dishonesty. Return-after-visit **cannot** be measured on GoatCounter (no persistent identity);
if that question ever matters, it needs a tool that can do it and a privacy review first.

## Addendum, 29 Oct 2026: REMOVED (KT's decision, Claude's recommendation)
KT asked again whether the section hurts us. There is still no direct evidence either way, but the case for removal is stronger than for keeping: it sat at about 90% of a very long page (23,392 px on a phone), so few people saw it; it conflicts with the "verified" promise (Jobicy was excluded as a source for bad dates and Toptal cannot be machine-checked); and the board's own "Worldwide roles only" filter already answers the real need. **The section, its footer link, its tracking events (`platform-view`, `platform-click`), `platforms.json` and `tests/test_platforms.py` were deleted.** To bring it back, KT must ask for it.
