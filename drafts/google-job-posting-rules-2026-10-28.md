# Google JobPosting rules for listings we do not own — checked 28 Oct 2026

Answers the open item in `drafts/kt-todo.md` §5 and the Phase-1 note in `CLAUDE.md`
("check Google's CURRENT job-posting rules before adding markup, and tell KT what you find").
Sources were opened and read in October 2026; URLs are at the bottom. Evidence labels:
**[Doc]** = stated in Google's own documentation · **[Inference]** = our reading of it ·
**[Unclear]** = Google does not say.

## 1. Can a third-party board mark up jobs it does not own?

**[Doc]** Yes in principle. Google's Job Posting feature explicitly covers "employers, ATS providers
and job boards", and the markup may sit on a page you own. The hard requirement is structural, not
ownership: **the markup must be on the same page as the job description and describe one specific
job** — a list or search page does not qualify.

**[Unclear]** Google does not settle the case closest to us: a detail page that reproduces an
employer's posting but sends the applicant to the employer's own Greenhouse/Lever/Ashby page. The
docs require "a way to apply" without saying the apply flow must be on your own domain, and they do
not confirm it either. Separately, Google's structured-data policy treats posting "on behalf of" an
organisation **without authorisation** as a violation — there is no page saying aggregation itself is
authorised.

## 2. Our actual blocker: we have no job pages

**[Inference, high confidence]** The board renders ~1,000 listings as cards on **one URL**
(`yirehcareers.vercel.app/`). JobPosting markup on that page would describe a list, not a job, so it
would not be eligible — and mismatched or ineligible markup risks a manual action that removes rich
results sitewide. **Per-job detail pages are a prerequisite for any job markup.** That matches the
strategy review, which already defers per-job pages (`2026-10-24-board-strategy...md`, §6 point 6).

## 3. What the rules require when we do build them

| Requirement | Google's rule | Our position |
|---|---|---|
| One job per page, markup on that page | **[Doc]** required | Not built yet — prerequisite |
| `datePosted` | **[Doc]** required; must be the employer's original posting date | We already store exactly that (Jobicy was dropped for violating it) |
| `title`, `description`, `hiringOrganization` | **[Doc]** required | All present in `jobs.json` |
| `jobLocation` with `addressCountry` | **[Doc]** required | Present via the eligibility data |
| `validThrough` | **[Doc]** required only if the posting has an expiry; omit if unknown | We rarely get one (ATS feeds almost never send it) → omit rather than invent |
| `jobLocationType: TELECOMMUTE` | **[Doc]** required for fully remote jobs | Maps to our `fully_remote` class only — not to "remote unclear" |
| `applicantLocationRequirements` | **[Doc]** required for geo-restricted remote jobs | Maps to our countries/region eligibility; the `unclear` class has nothing to state |
| `baseSalary` | **[Doc]** recommended, and stated as **for employers only** | **[Unclear]** our pay text is copied verbatim from the employer's posting; safest first build is to omit `baseSalary` |
| Expired jobs | **[Doc]** remove the page, remove the markup, or pass `validThrough`; slow removal may draw a manual action | Our 30-day refresh drops stale rows already |
| `noindex` pages | **[Doc]** ineligible for job results | Our per-job pages would need to be indexable |

## 4. Recommendation

**Do not add JobPosting markup now.** Two independent reasons:

1. **Technical:** there is nothing to mark up — a card list cannot carry valid JobPosting data.
2. **Policy [Unclear]:** Google never says an aggregator linking out to the employer's ATS is
   eligible, and treats unauthorised posting on behalf of a company as a violation. Shipping markup
   we cannot be sure is authorised risks a manual action on the whole domain for a feature we cannot
   yet measure the value of.

**Sequencing:** build per-job pages only after the strategy review's own gate (two weeks of click
data deciding whether organic job search is worth the route). When that happens: markup exactly the
visible content, omit `baseSalary` and `validThrough` unless the employer states them, mark only
`fully_remote` jobs as `TELECOMMUTE`, keep `unclear` listings out of remote-specific properties, and
re-check these rules right before shipping (they change).

**Decision for KT:** (a) defer per-job pages and markup until traffic data says organic job search
matters — *recommended*; or (b) build per-job pages now without markup, to start earning organic
search, accepting the build cost.

## Sources (opened 28 Oct 2026)

- Job Posting structured data reference: https://developers.google.com/search/docs/appearance/structured-data/job-posting
- Structured data general policies (visible content, manual actions): https://developers.google.com/search/docs/appearance/structured-data/sd-policies
- JavaScript SEO basics (rendering, crawlable URLs): https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics

Earlier related note: `research/job-sources-100.md` item 92 already recommended "default to no
markup unless an employer agrees; KT decides" — this check reaches the same place by a different
route (page structure first, authorisation second).