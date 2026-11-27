# Yireh Careers on social: brand guidelines (26 Nov 2026; extended 27 Nov 2026)

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

**Series colours** (27 Nov 2026, all from the site's own palette; renderer themes; evidence in `research/2026-11-27-formats-and-colour.md`):
| Series | Theme | Background | Text |
|---|---|---|---|
| Roles (carousels, single role) | navy | hero navy gradient | white |
| Tips (eligibility, reading a posting) | light | `#eef2f8` | `#1a1a2e`, blue kickers |
| Safety and scams | amber accent | `#eef2f8` with an amber top bar and number tiles | `#1a1a2e`, dark amber kickers |
| Numbers and the weekly video's cover | blue | `#2563eb` → `#1d4ed8` | white; mark ringed in white |
| CV service | teal accent | `#eef2f8` with a teal top bar and tiles | `#1a1a2e`, teal kickers |
Blue and white dominate every post; amber and teal are accents only, never full backgrounds (distinctive-asset evidence: `research/2026-11-27-question-bank-and-sources.md`, section 3). The mark, Inter, the card and the footer never change.

**Templates** (all built by `social/tools/render_posts.py`, 1080x1350):
1. **Cover**: kicker (caps, light blue) → headline (Inter 800, ~104 px) → one-line sub. Content centred vertically.
2. **Role card**: white card on navy: pills (where you can apply from · Remote · job type) → title → company → Posted / Pay / Source rows → "Apply on the original posting" button.
3. **Tip**: blue number tile → headline → two-line explanation.
4. **Closing**: "Your next step" → headline → `yirehcareers.vercel.app` in a white pill.
Every slide: the mark and "Yireh Careers" top-left, "n / total" top-right on carousels, the date line bottom-left, "Link in bio" bottom-right.

**Video** (1080x1920): presenter 0–4 s and the last 5–6 s; live-board footage in the middle (`social/tools/record-board-footage.js`, worldwide demo, no country shown); burned-in captions from the spoken words (`social/tools/compose_video.py`: Inter ExtraBold 74 px, white on a navy box, up to 4 words a line, key words in brand blue, lower-middle of the frame); numbers in a blue box with their date. **No visible "AI presenter" badge, watermark or tag** (KT, 27 Nov 2026): disclosure is each platform's own AI label. Text stays inside the safe zone: top 270 px, bottom 420 px and right 150 px clear (`research/2026-11-26-platform-specs.md`).

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

## 9. AI label (changed 27 Nov 2026, KT)
Any post with the AI presenter or the AI voice: the **platform's own AI label ON** (TikTok "AI-generated content" and Instagram via Buffer `isAiGenerated`; Facebook "AI info" ticked by KT, or the screen-only cut goes there). **No visible AI badge, watermark or tag in the video, design or caption by default.** Never switch a required platform label off. Screen recordings, role cards and text slides need no label. `check_post.py` blocks a presenter video without `ai_label` and warns on a visible badge.

## 10. Formats per platform (proposed 27 Nov 2026, waiting for KT's yes)
TikTok gets video and photo carousels; Instagram gets Reels, carousels and Stories with a link sticker, and no single-image posts; Facebook gets Reels and carousels with a per-post link. Full table and evidence: `research/2026-11-27-formats-and-colour.md`, section 3.

## 11. Timing
All posts at **15:00 UTC** for the first two weeks (morning to midday in the Americas, afternoon in Europe and Africa, evening in South Asia; late in South-East Asia); no Sunday posts; the weekly video on Tuesday. Changed from 12:00 UTC on 26 Nov after KT widened the audience. Evidence and the planned time test: `research/2026-11-26-posting-times.md`.

## 12. Logo use
- The YC mark (white Y whose right arm is a light-blue tick, on a blue tile; `favicon.svg`, 1024 px files in `drafts/whatsapp-profile/`) sits top-left on slides at 56 px, with "Yireh Careers" in Inter 700 beside it. Clear space around it of at least half the tile's width.
- On blue backgrounds the tile gets a 3 px white ring so it doesn't disappear. Never recolour, stretch, rotate, outline or add a shadow to the mark. Never put it on a busy photo without the navy or white panel behind it.
- In videos the mark appears only on the closing frame (with the board URL), never as an opening sting. Profile pictures use the mark alone.

## 13. Typography hierarchy (Inter throughout)
| Level | Slides (1080x1350) | Video (1080x1920) | Weight | Notes |
|---|---|---|---|---|
| Headline | 88-104 px, tracking -0.03em | hook text 86 px | 800 | six words or fewer; `text-wrap: balance`; no stranded last word |
| Kicker | 30 px caps, tracking +0.08em | — | 700 | light blue on navy, brand blue on light |
| Body | 40-44 px | — | 500 | at most two lines on a slide |
| Captions (subtitles) | — | 74 px | 800 | white on a navy box (`&H004D2A0F`), key words `#2563EB` |
| Labels and pills | 26-30 px | — | 600 | "Worldwide", "Apply from", job type |
| Footer | 24 px | — | 500 | date line left, "Link in bio" right |
Line height 1.05 for headlines, 1.35 for body. Left-aligned text on slides; centred only on covers and closing slides.

## 14. Spacing and layout
- An 80 px outer margin on slides; a 32 px gap between elements; a 28 px card radius; 8 px grid.
- One message per slide; at least 30% empty space. Never more than ~20 words on a slide.
- **Variety without losing recognition:** recognition comes from the mark, Inter, the palette, the card style and the footer, not from one layout. Rotate treatments by subject:
  - full-bleed headline on navy;
  - a light slide with a number tile;
  - a real board screenshot with a callout;
  - a "posting excerpt" quote card (the employer's own words, with the link);
  - split before/after;
  - a question card for community posts.
  Two posts in a row should not share a treatment.

## 15. Graphic elements and icons
Pills (as on the site), number tiles, a thin brand-blue underline for emphasis, a callout arrow (2 px, rounded) to point at a part of a real screenshot. Icons: simple line icons (2 px stroke, rounded) in the brand blue or navy, only where they carry meaning (location pin for "where you can apply from", calendar for "posted", shield for "never pay"). No emoji in graphics; at most one in a caption when it adds meaning. No stock photos of laptops on beaches.

## 16. Templates in use (built by `social/tools/render_posts.py`, `free_video.py`, `compose_video.py`)
Cover, role card, tip with number tile, closing slide (section 6); Story frame (slide 1 on a 1080x1920 navy canvas plus link sticker); video cover (a frame with the hook in the Hook caption style); static post (one headline, one supporting line, optional screenshot); free screen-only video (text slides, board footage, closing slide).
