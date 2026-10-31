# The person behind the service: what comparable providers do (31 Oct 2026)

KT confirmed the supplied photograph is genuine and asked whether to show a name and what to say, based on what successful providers in this niche actually do. This overrides the 24 Oct "no photo, no name" rule for the services page only (KT's instruction, 31 Oct).

## Evidence (labelled)
**Research / usability guidance**
- Stanford Web Credibility Project, 10 guidelines from three years of research with 4,500+ people (credibility.stanford.edu/guidelines). Guideline 4: "Show that honest and trustworthy people stand behind your site": first show there are real people behind it, then convey their trustworthiness through images or text (bios with a personal touch). Guideline 3: give the credentials of the people providing the service. Guideline 2: show a real organisation (a physical address). Guideline 5: make contact easy.
- Research report supplied by KT (31 Oct): real photo, real name, role and truthful background; never stock or AI faces.

**Observed on live pages, 31 Oct (not conversion data; nobody publishes theirs)**
| Provider | What they show | Pattern |
|---|---|---|
| Cultivated Culture (Austin Belcak, large audience) | Name in the page title; first person; own struggle story (300+ applications, no results), then the system he built, then results | Relatable origin story, then proof |
| AvidCareerist (Donna Svei, executive resumes) | Name in the page title; "I work with you"; 25+ years recruiting, 400+ placements, former CPA | Specific credentials with numbers; first person |
| ResumeWriters.com (Brian McCullough) | "Meet the founder": name, role, photos including a personal one; promises a refund and a referral if they cannot match a writer | Named founder, a human touch, honest fallback |
| JobJenny | The brand is a named person | Personal brand |

Common to all four: a **name**, a **face**, **first person**, and **one or two specific, true facts** about why they are qualified. None used stock photos or hid the person.

## Decision
Show a name (first name at minimum), the photo, three short first-person sentences. Every sentence must be true and already supportable.

## Facts already published and safe to reuse
Run by an individual business owner based in Kyrenia (privacy page); clients message on WhatsApp; documents go by email; work starts from the client's own CV and target roles; AI tools help with wording and everything is checked before delivery.

## Still needed from KT (nothing is invented)
1. The name to display. 2. One or two true facts about why KT does this or is qualified (own job-search story, relevant background, a real number only if true). 3. Optionally one human detail.

## Draft for KT to edit
"Hi, I'm [Name]. I run Yireh Careers from Kyrenia, and I'm the person you message on WhatsApp. Every order starts from your own CV and the roles you're aiming for, and I check everything before it reaches you. [One true sentence on why you do this.]"

Assets prepared: `images/about-480.webp`, `images/about-960.webp` (square crop of the supplied photo).

## Also fixed in this change
The public site was serving CLAUDE.md (the internal brief), `scripts/`, `tests/`, `.github/` and several `data/` reports. No secrets were in them, but they are internal. `.vercelignore` now hides them; the files the site loads (`jobs.json`, `data/geo_lexicon.json`, `api/`, `fonts/`, `images/`) are unaffected and guarded by `tests/test_public_surface.py`.
