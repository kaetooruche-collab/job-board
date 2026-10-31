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

## Next (phase 2, services page)
Light hero, balanced package cards with the benefit first, the Executive section laid out openly instead of an awkward collapsible, clearer example label, a human-credibility block built so a real photo can be dropped in once KT approves.
