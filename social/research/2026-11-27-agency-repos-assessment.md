# Assessment: GitHub "AI social media agency" repositories, and what Yireh should take from them (27 Nov 2026)

**Why:** KT shared a ChatGPT recommendation (27 Nov) to build the agency from five community repositories, with seven specialist "departments", brand discovery from scratch and a full metrics system. Its own step 7 asked for a repository-level check before building anything. This is that check. Each repository page was read on 27 Nov 2026 (Firecrawl). Key instruction files were opened where they exist. Nothing was installed or run.
**Labels:** [Established] = read in the repository or tool on 27 Nov; [Hypothesis] = our reading.

## 1. What the repositories actually are [Established]
| Repository | Stars | Commits | Last commit | Licence | What is really there | Verdict |
|---|---|---|---|---|---|---|
| filnik/social-media-manager-AI | 12 | 7 | 25 Feb 2026 | MIT | 5 Claude Code skills (LinkedIn post, video script, carousel, ideas, `/create-brand`), "60 expert profiles", 14 templates. No analytics or learning. | Small; LinkedIn-first. Brand creation is for brands without an identity. |
| 3echo-dev/social-campaign | 1 | 283 | 27 Oct 2026 | MIT | A full plugin with a server, database migrations and a job board. The skills (`write-hook`, `policy-check`…) are 10-line adapters into its own pipeline, so the method can't be lifted out. It has 9 approval gates and reads results from ad accounts or Metricool. | The most built, but heavy machinery tied to its own system. Borrow the approval-gate idea, not the code. |
| safrin96/agentic-content-system | 7 | 5 | 10 May 2026 | MIT | 19 skills with real instructions. Read in full: `content-deduplicator` (hook/angle/data fingerprints, a 60-day hook window, formula used 3+ times in 30 days) and `content-reviewer` (GO/NO-GO gate). Its README calls itself "a template" with "5 placeholder pillars". LinkedIn and Instagram only. | **The best ideas per line.** Borrow the repetition check and the GO/NO-GO discipline. |
| aiimpactagency/social-media-team | 5 | 2 | 12 Jun 2026 | **none stated** | 15 skills listed (per-platform writers, hook generator, comment-reply drafter, performance review via Blotato). | 2 commits. **No licence, so its text must not be copied.** |
| mrsahilbeniwal/social-campaigns | 9 | 8 | 10 Apr 2026 | MIT | One `SKILL.md` plus references. Reads a codebase (CSS, Tailwind, landing copy) to extract colours, fonts and voice. Phase 5 "performance-informed refinements" with no stated data source. | We already did this extraction from the site (`social/BRAND_GUIDELINES.md`). |

None of the five has more than 12 stars, and none publishes results showing it grew an account. They are frameworks, not tested systems. ChatGPT's own caution says the same.

## 2. Where the recommendation holds, and what we already have
| Recommendation | Evidence or status | Action |
|---|---|---|
| The objective is visits to the board and service enquiries, not likes | Agreed; matches `drafts/social/agency-plan.md` (GoatCounter by `utm_source`). But posts have no stated funnel stage. | **Add:** every post declares `funnel` (awareness / consideration / conversion) and `goal_metric`; the checker requires them. |
| Don't repeat hooks and topics | safrin96's deduplicator is a concrete method; we had nothing. | **Add:** a repetition check across all calendars. Block a near-identical hook in 60 days. Recurring slots marked with a `series` name are only flagged. |
| Track every post's results | Planned (`performance.md`) but no structure yet. | **Add:** `social/post-log.csv`, one row per post per platform, with the source of each number. |
| Approval gates before money and publishing | We already have them: KT approves the week (Phase 1), the BHuman cost first, nothing published without the checker. | Keep. |
| Posting times are a hypothesis, tested on our data | Already the rule (`research/2026-11-26-posting-times.md`). | Keep. |
| UTM tags | Already used. Limit: one bio link per platform, so clicks can be told apart by platform but not by post. | Keep; say so in reports. |
| Adversarial review passes (Skeptic, Scroller, Competitor, Editor) | safrin96's six-pass protocol; our checker covers rules but not quality. | **Add** as a written pass in the weekly checklist (in the skill), not as separate agents. |

## 3. Where the evidence disagrees with the recommendation
1. **"Build the brand identity from scratch; don't pick colours because they look attractive."**
   - Yireh already has an identity, decided by KT and in use:
     - the name (24 Oct 2026);
     - the YC mark and logo files (24 Oct 2026);
     - the site's navy, blue and Inter;
     - the voice guide (24 Oct 2026).
   - The brand guide was taken from the live site, which is the method `mrsahilbeniwal` automates.
   - Starting again would reopen KT's decisions and make the social accounts look unlike the board people land on.
   - Recognition comes from consistency between the posts and the site.
2. **"Seven departments as specialist agents."**
   - The repositories built that way have 2 to 8 commits.
   - At 6 posts a week, separate agents add cost and hand-offs. Each one starts with no context (our own tool rules say the same).
   - The roles become passes inside one workflow: research, plan, write, review, measure. Our skill already runs that cycle.
3. **"Candidate success stories" as a content type.**
   - We have none: 0 orders, 0 sign-ups (job-board review, 16 Nov).
   - Inventing or implying one breaks CLAUDE.md's verification rule and the FTC endorsement guides.
   - This content type is parked until a real person agrees in writing to be featured.
4. **"Track 3-second views, watch time and completion rate."**
   - Buffer's API (checked 27 Nov) returns reactions, comments and impressions or reach where the network supplies them. Figures refresh daily and go 31 days back on the free plan.
   - It does not give 3-second views, average watch time or completion.
   - Those live in TikTok Studio and Instagram Insights, which we have no access to. KT can read them weekly (2 minutes); otherwise the log marks them "not available".
5. **"Claude needs historical social analytics."**
   - Correct, but there is almost none: Video 1 had 84 TikTok views on 26 Nov.
   - Until there is data, every "what works" claim stays a hypothesis. The first four weeks are for building a baseline, not for proving winners.

## 4. Decision for the agency (Phase 0 addendum)
- Install no repository. Borrow three methods, rewritten for our rules and tools:
  - the repetition check (safrin96);
  - the GO/NO-GO review passes (safrin96);
  - the funnel-stage discipline and approval gates (3echo).
- Credit: safrin96/agentic-content-system (MIT) for the deduplicator and reviewer ideas; no text copied.
- Keep the existing brand. The work that grows traffic is consistent posting, real roles and honest measurement, not a new identity.
