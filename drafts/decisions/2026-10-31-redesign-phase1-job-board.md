# Redesign phase 1: job board first screen (KT, 31 Oct 2026)

Trigger: a coworker's feedback (what does "6 hours re-checked" mean; the packages come first; filters take too much room; the example label confuses; the Executive section looks awkward) plus KT's own observations and a long master prompt generated elsewhere. KT said Claude's judgement on the intricate design decisions outranks the prompt. The prompt was used as input, not a specification.

## What was measured (live, before the change)
| Desktop 1280x800 | Position of |
|---|---|
| Hero | 0 to 557 px |
| Packages block | 669 to 1,209 px |
| Toolbar | 1,241 to 2,136 px (Fields 308 px and More filters 393 px forced OPEN on screens 720 px and wider) |
| **First job card** | **2,199 px** (fold at 800) |
Phone 390x844: first card at 1,680 px. Cause on desktop: `window.innerWidth >= 720` opened both filter panels. Dark-mode visitors also got a near-black page because the CSS followed the operating system's dark setting.

## Competitor observations (direct, 31 Oct, first screen only)
Remote OK: no hero, a single row of dropdowns, jobs immediately. Remotive: headline, big search, pill filters, count, jobs inside the first screen. Working Nomads: short hero plus a sidebar, jobs visible. We Work Remotely: large hero, stats, jobs below the fold (it is the category leader, so brand carries it; we cannot). Himalayas blocked automated access; FlexJobs timed out (not inspected). Services: TopResume leads with one action (free resume review, no prices in the hero); ResumeWriters leads with a bold claim, a risk-reversal banner and a real phone number. No conversion rates were available for any of them and none are claimed here.

## Decisions
1. **Hero**: compact, light, one line of value: "Remote jobs that show who can apply", a sentence on fresh listings from employers' own feeds, and one facts line ("1,033 remote jobs, 163 companies, Updated every 6 hours"). The "Every 6 hrs / Re-checked" tile (added 29 Oct) confused a first-time reader and is gone. Removed the "Browse the jobs" button: the search box is now on the first screen.
2. **Filters collapsed on every screen size.** Search and Experience stay visible; Fields and More filters are one tap away. All existing filters, the guided finder, active-filter chips and URL state are untouched.
3. **Packages moved below the job list and the free email signup**, so nothing paid sits between a visitor and the jobs. Result: first card at 692 px on desktop (inside the first screen, was 2,199) and 903 px on a phone (was 1,680).
4. **One light theme for every visitor** (removed the OS dark-mode styling on the public pages; `color-scheme: light`). Reason: KT does not want the navy/dark look, and a different first impression per device is worse than one consistent one. Trade-off: people who rely on dark mode lose it; a proper theme switch can be added later if wanted.

## Not taken from the prompt, and why
- "Scraped" as a selling point: the board reads employers' public job-feed endpoints, not scraped pages, and the word would hurt trust. Wording used: "from employers' own job feeds".
- "Verified" means: the listing came from the employer's own feed, the link is kept only while it stays in that feed, and the eligibility is shown as the employer states it. It does NOT mean we confirmed the role is still open or that the applicant's country is accepted. Copy must not claim more.
- Showing a founder photo: KT's own rule of 24 Oct says no personal name, face or photo on the brand. KT now suggests a photo for the services page. That needs KT's explicit yes (and a genuine photo); not built yet.
- Removing the "illustrative example" label: the before/after examples are fictional. Deleting the disclosure would make them read as client results. Plan: keep the disclosure, make it shorter and clearer.

## Phase 2 (services page), done 31 Oct 2026
- **Light hero** and light closing band (navy removed on the services page too); secondary buttons now outline-on-light.
- **Executive** is no longer a collapsible at the bottom (it sat at 4,460 px, three dense text columns and a dark box). It is now an open section directly after the packages (about 1,940 px), each card leading with a benefit line and three short bullets, and the timeline as three clear steps. All service terms are unchanged (2 / 3 working days, 30 days, 12 posts, the connection aim and its caveat, approval before publishing, Growth $99 optional). The `/services#executive` link used by emails still works.
- **"Best for" line** on each package card (the intended customer), without claiming suitability for any background.
- **Example label** kept (the examples are fictional) but shortened and restyled: "Sample for illustration: a fictional person and fictional figures. Not a client result." No more italics.
- **Not done:** the human-credibility/photo block. KT's 24 Oct rule forbids a personal name or photo on the brand; it needs KT's explicit yes and a genuine photo. The page has room for it (after "How we work") once approved.

## Addendum: "verified" is now defined on the site (31 Oct 2026)
The ChatGPT analysis KT shared flagged that "verified" needs a defined meaning. The pipeline does test every link on each refresh (`check_links` in `scripts/fetch_jobs.py`) and drops failures, so the claim is accurate, but it was never spelled out. `/verify` now opens with "What 'verified' means here": what is checked every 6 hours, and what is not (employer identity is not audited; a role can be filled before the employer removes it; acceptance of an applicant's country is the employer's decision; no promise of interviews). The home hero links to it ("What 'verified' means"). Guarded by `tests/test_hero_jobs.py`.
