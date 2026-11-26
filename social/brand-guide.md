# Yireh Careers on social: brand guide (26 Nov 2026)

Status: **PROPOSED** (Phase 0). Binding rules come from `CLAUDE.md` and `drafts/voice-and-copy-guide.md`; this guide applies them to TikTok, Instagram and Facebook. Where they differ, CLAUDE.md wins. Every post is checked by `social/tools/check_post.py` before it is scheduled.

## 1. Who we are talking to
**People outside the US, wherever they live** (KT, 26 Nov 2026; `drafts/decisions/2026-11-26-who-to-target.md`): Canada, the UK and Europe, Latin America, South Asia, South-East Asia and Africa. US viewers are welcome but not chased. Often on a phone, often reading in a second language, tired of applying to "remote" jobs that turn out to be closed to them, and wary of scams. Their words: legit, real, scam, fake, "remote but not for me", tired, 100+ applications. Ours ("verified", "eligibility", "classifier") are weaker; use theirs. (Evidence: `drafts/marketing/audience-research-and-icp.md`, `research/2026-11-26-niche.md`, `research/2026-11-26-niche-outside-us.md`.)

**Supply differs a lot by country** (26 Nov, after the refresh with PRs 81-83: Canada 369, UK 294, Germany 171, India 159, Brazil 153, Mexico 133, Philippines 90, Nigeria 74, South Africa 73, Kenya 68, Ghana 67, Indonesia 47; worldwide 36). So never imply plenty for everyone: no board-wide totals as a promise; prefer numbers true for every viewer (open worldwide, open beyond one country). See `research/2026-11-26-scope-outside-us.md`.

## 2. Voice
- **A kind, capable person across a table.** Short sentences, plain words, contractions, "you" and "we". Calm, a little warm. At most one exclamation mark in a post.
- **Bottom line first.** The first line is the hook; it names a moment or a fact, not the brand.
- **One post, one job, one next step.** The next step is always the link in bio.
- **Specific beats vague.** A real role, a dated number, a quote from a posting. Never hype.
- **Signed as the team.** No founder name or face anywhere except the services page (KT, 31 Oct).
- **The presenter** (AI, warm at-home woman, Olivia's voice) opens and closes videos only; the board carries the middle. "Yireh" is said YYE-ray (written "Yai-ray" in narration only; "Yireh" on screen).

## 3. Content pillars (6 posts a week to start)
| Pillar | Share | What | Why |
|---|---|---|---|
| **Jobs**: real roles | 3 a week | Role cards and carousels from the live feed: open worldwide or across a whole region beyond the US, newest first, posting opened that day | The proof. Saves and shares. |
| **Proof**: the weekly video | 1 a week (Tuesday) | Presenter hook and close, live-board footage in the middle, one dated number | Reach; explains what the board does |
| **Tips**: check before you apply | 2 a week | Eligibility wording, scam signs, reading a posting | Trust and saves; useful without us |
| **Service**: CV help | at most 1 in 6 posts, never inside a jobs post | The free CV check first; paid packages only with KT's yes on the wording | Revenue, after trust |

## 4. What we never say or do (blocked by `check_post.py`)
- "guaranteed", "the only …", "no work permit needed", "all remote jobs", "every job shows who can apply".
- Any hiring-system name (Greenhouse, Lever, Ashby, Recruitee, Personio, Workable, Workday, …). Cards say "Source: the company's hiring page".
- "direct/straight to the employer", "apply directly", "the employer's own posting/page". Say "opens the original posting".
- That a role suits a background ("perfect for graduates", "for students"). Say "entry-level and junior".
- **"DM me", "comment JOBS", "send us your CV"**: the scam script our audience fears. The CTA is the link in bio. CVs go by email through the site, never by DM.
- **No country named** in videos or posts (KT, 26 Nov 2026): no typed country in footage, no country on a featured card. Regions (Africa, Asia, EMEA, APAC, worldwide) are fine. Exceptions only with KT's recorded yes (`allow_countries` + `allow_reason`).
- "Free / we never charge you to apply" said **once** per post (once spoken plus once on screen at most).
- The CV service inside a jobs post.

## 5. Numbers, dates and featured roles
- Every number comes from the live feed (`social/tools/feed.py stats`) **on the post day**, and is dated on screen: "From our live board, 1 Dec 2026".
- Every featured role is re-opened on the post day (`social/tools/verify-open.js`): the posting loads, the title matches, no closed-role wording, and no single-country wording on a "Worldwide" or region card. Roles that fail go in `social/data/exclude_jobs.json` and `social/board-issues.md`.
- Pay is shown only as the posting states it; otherwise "Not stated".

## 6. Visual identity (matches the site)
| Token | Value | Use |
|---|---|---|
| Hero navy | gradient `#131c35` → `#0f2a4d` → `#17407a` (135°) | Slide and video backgrounds |
| Brand blue | `#2563eb` (hover `#1d4ed8`) | Buttons, tip numbers, links |
| Light blue | `#7cb3ff` (kickers), `#a9ccff` (footers), `#dbe7ff` (body on navy) | Text on navy |
| Card | `#ffffff`, text `#1a1a2e`, secondary `#5f6368`, rule `#e2e5e9`, radius 28 px | Role cards |
| Pills | Worldwide `#f0fdfa`/`#0d9488`; region `#eff6ff`/`#2563eb`; neutral `#f1f3f5`/`#5f6368` | Where you can apply from, Remote, job type |
| Type | **Inter**: 800 headlines (tight, -0.03em), 700 brand and buttons, 600 labels, 500 body | Everything |
| Mark | The YC mark: white Y whose right arm is a light-blue tick, on a blue tile (`favicon.svg`; 1024 px versions in `drafts/whatsapp-profile/`; wordmarks in `drafts/brand/`) | Top-left of every slide; profile pictures |

**Templates** (all built by `social/tools/render_posts.py`, 1080x1350):
1. **Cover**: kicker (caps, light blue) → headline (Inter 800, ~104 px) → one-line sub. Content centred vertically.
2. **Role card**: white card on navy: pills (where you can apply from · Remote · job type) → title → company → Posted / Pay / Source rows → "Apply on the original posting" button.
3. **Tip**: blue number tile → headline → two-line explanation.
4. **Closing**: "Your next step" → headline → `yirehcareers.vercel.app` in a white pill.
Every slide: the mark and "Yireh Careers" top-left, "n / total" top-right on carousels, the date line bottom-left, "Link in bio" bottom-right.

**Video** (1080x1920): presenter 0–4 s and the last 5–6 s; live-board footage in the middle (`social/tools/record-board-footage.js`, worldwide demo, no country shown); burned-in captions in Inter ExtraBold with the styles in `drafts/marketing/video/video1/captions.ass`; numbers in a blue box with their date; "AI-generated presenter" in the corner while the presenter is on screen. Text stays inside y 270–1250 (safe zones: `research/2026-11-26-platform-specs.md`).

## 7. Captions
1. **Line 1 is the hook** (under ~125 characters; feeds cut the rest). Their words, a specific pain or fact.
2. Two or three short lines of substance.
3. **"Link in bio."** (on the role posts: "Check each employer's rules for your country before you apply.", once).
4. **3–5 hashtags** at the end (Instagram's hard limit is 5). No #fyp, #viral, #reels or #explore.
5. Spell-checked (`check_post.py`; the 26 Nov thumbnail said "DOSEN'T").
6. Bio link per platform: `https://yirehcareers.vercel.app/?utm_source=<tiktok|instagram|facebook>&utm_campaign=bio`.

## 8. Hashtag sets (pick one set; never more than 5 tags)
| Post type | Set |
|---|---|
| Weekly video | `#remotejobs #remotework #jobsearch #workfromhome` |
| Role cards | `#remotejobs #remotework #jobsearch #hiring` |
| Eligibility tips | `#remotejobs #jobsearch #jobtips #remotework` |
| Scam and safety tips | `#jobscams #remotejobs #jobsearch #careertips` |
| CV service | `#cvtips #jobsearch #remotejobs` |
Region tags and Spanish or Portuguese captions are later tests (Latin America's remote-job niche runs in Spanish and Portuguese), not defaults; other languages need KT's yes. Hashtags are a weak lever (Instagram's own Dec 2025 guidance); the hook and the content matter more.

## 9. AI label
Any post with the AI presenter or the AI voice: platform AI label ON (TikTok "AI-generated content"; Meta "AI info") and "AI-generated presenter" on screen. Screen recordings, role cards and text slides need no label.

## 10. Timing
All posts at **15:00 UTC** for the first two weeks (morning to midday in the Americas, afternoon in Europe and Africa, evening in South Asia; late in South-East Asia); no Sunday posts; the weekly video on Tuesday. Changed from 12:00 UTC on 26 Nov after KT widened the audience. Evidence and the planned time test: `research/2026-11-26-posting-times.md`.
