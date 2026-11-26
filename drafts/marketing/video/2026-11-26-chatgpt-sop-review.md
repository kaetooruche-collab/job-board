# Review of ChatGPT's "Research-Driven AI Video Advertising SOP" (26 Nov 2026)

Source: KT's shared conversation (https://chatgpt.com/share/6b07d551-a71c-83ed-80d4-bd8196bb5c90), read in full. It has two parts:
1. The UX audit, already handled in `drafts/reviews/2026-11-26-ux-audit-ledger.md`.
2. The video SOP: research, presenter, delivery and direction, audience, three concepts, production SOP, testing, and three scripts.

Each claim that matters was checked on 26 Nov. Labels:
- **[Verified]**: checked against the source.
- **[Unverified]**: not checked.
- **[Conflict]**: clashes with our rules or our tools.

## 1. What holds up, and we keep
| Point | Check |
|---|---|
| Lead with the "remote doesn't mean anywhere" problem; eligibility is the central message | Matches our own research (pain 1) and data. Their Video 1 is the same idea as our script A. |
| Alion index: 0.4% of remote postings are open worldwide, 46.4% are US-only, 17.6% are open to at least one Global South country | **[Verified]** at alion.io (Oct 2026): 148,845 postings from 22,175 employers, CC BY 4.0. Our own board agrees: 19 of 1,765 open worldwide (1.1%), 683 US-only (38.7%). |
| AI presenters are less effective than human ones; human-like cues shrink the gap | **[Verified]** Yim, Liska, Mu, Thakkar (2026), *Journal of Research in Interactive Marketing* 20(1):108-122, three experiments. This is the strongest argument for a real voice and a screen-led video. |
| Combine the presenter with real screen recordings of the board; captions always; 9:16; safe zones | Sound, and doable: I can record the real board at phone size and assemble it with ffmpeg here. KT doesn't have to edit. |
| One message per video; test hooks while keeping everything else the same; don't judge by likes | Sound, and matches our plan (three openings, one body). |
| Conversational, not corporate and not influencer-style; spoken language, not written | Sound, and matches KT's voice guide. |
| No invented testimonials, no fake listings, the site must deliver what the ad promises | Matches our rules. |

## 2. What has to change before use
1. **Wording that breaks our tested copy rules [Conflict].** The scripts say:
   - "from employers' own career pages"
   - "jobs link directly to the original employer posting"
   - "apply directly"
   - "Check your eligibility"

   `tests/test_source_claims.py` bans the first three because they overstate where the links go. We also can't confirm anyone's eligibility; we show what the employer states. Replacements:
   - "the company's hiring page"
   - "opens the original posting"
   - "see where you can apply from"
2. **The performance tags can't be carried out in BHuman [Verified against BHuman's tool list].** Tags such as [SMILE], [GESTURE: open palm], "raise eyebrows" and [PAUSE 0.8s] have no control behind them. BHuman takes:
   - the voice settings (delivery preset, speed, stability, style, and a plain-text note);
   - one free-text instruction for the video render;
   - only the "continuous" video style.

   Worse, a tag left inside the script text gets **read aloud**. Pacing therefore comes from punctuation, sentence length and the voice settings; expression goes in the render instruction as a request, not a guarantee. ChatGPT itself flagged that this needed checking.
3. **The testing plan assumes paid ads [Conflict with our situation].** CTR, cost per landing-page view, 9 variants and "sufficient impressions" all need ad spend. We post organically and get about 50 home-page views a week, so nine variants cannot reach a meaningful sample. Instead:
   - one video a week, changing only the opening;
   - judge on TikTok's own 2-second hold, average watch time and link clicks, tracked through our tagged links (`utm_source=tiktok`) in GoatCounter.

   Paid testing would need KT's decision on money.
4. **Scripts are longer and more pitch-like than KT's voice guide allows.** For example: "That's why there's Yireh Careers. We bring remote opportunities from employers' own career pages into one place, with information about where you can apply from." Shorter, warmer versions are below.
5. **Speaking pace of 140–155 words a minute** is their opinion, not a cited study. The one study we found favours about 180 for ads. The difference is small; we'll set it by ear in the test clip.
6. **A presenter aged 28–38, a woman for Video 1, a man for Video 2.** Reasonable, but untested. Given the AI-spokesperson study and our audience's fear of scams, the presenter should be on screen only briefly (hook and ending), with the board itself carrying the middle. An AI face also needs TikTok's AI-generated label.
7. **The images and links in the SOP are irrelevant.** Stock photos, plus links to a meme site, a French newspaper and a US law blog: decoration with no evidence value. Ignore them.
8. **"Job-detail views"** as a metric: there are no job pages, so we measure apply clicks and searches instead (both already tracked).

## 3. Merged Video 1 (KT's hook + ChatGPT's concept 1 + our rules)
Voice: Olivia (warm British female). "Yireh" is said like "Jireh" with a Y (YYE-ruh). It is spelled phonetically in the narration only; the exact spelling is tested in a 5-second clip first. 83 spoken words, about 30 s at 165 words a minute.

| Time | Spoken | On screen |
|---|---|---|
| 0–4 s | You're halfway through a remote job application... and then you see it. *US residents only.* | Presenter close-up; text "US residents only" |
| 4–10 s | Remote doesn't always mean *anywhere*. On our board, almost four in ten remote jobs are open only to people in the US. | Board: US-only pills; "683 of 1,765 · US only · 26 Nov" |
| 10–20 s | That's why we built Yireh Careers. Tell it where you live... and it shows you the remote jobs that say they're open to *you*. | Screen recording: typing a country, the list filtering |
| 20–26 s | Every job opens the original posting, with its real date. | A card: posted date, Apply button |
| 26–31 s | It's *free*, and we never charge you to apply. Link in bio. | Presenter or logo; yirehcareers.vercel.app |

Copy check:
- No "directly", no "employer's own" and no "check your eligibility".
- "That say they're open to you" is accurate: it is the employer's statement.
- Numbers are measured from our board and dated.
- One legal point (free, no fee), said once.

Openings to test later, with the same body:
- B: "Remote doesn't mean you can work from anywhere."
- C: "Before you apply for another remote job, check one thing."

## 4. Decisions for KT
1. **Presenter:** AI presenter for the opening and ending only, with the board in the middle (recommended), or voice-only over the board with no face at all (most trust, cheapest), or the presenter throughout.
2. **Approve the merged Video 1 wording** above (public copy rule).
3. **Paid testing:** no (organic, one variable a week) or yes with a budget.

## 5. Progress (26 Nov 2026)
- KT chose: presenter for opening and ending only, board footage in the middle; KT's script with Claude's three edits; "Yireh" = YYE-ray; voice Olivia.
- Spent so far today: two name tests (7.4 s and 6.1 s) and the full voiceover (26.3 s, approved by KT), about 41 credits.
- Board footage recorded from the live site (14 s, 1080x1920, free). Voice timings: hook 0–5.0 s, "Remote doesn't always mean anywhere" 6.0–7.6 s, Yireh and the country line 7.9–13.3 s, original posting 14.1–18.4 s, free and CTA 18.9–25.8 s.
- Next: a woman presenter (KT picks the look; generation costs credits), the render plan with its cost, then assembly with captions and the on-screen statistic.
- KT, 26 Nov: **no country named in videos** (a named country whose viewers then find few jobs works against us); long term, keep growing the number of jobs open outside the US. The board footage blurs the typed country and the filter tag.
- KT chose the **warm, at-home presenter** (BHuman presenter 53bb213d; the attached copy is visually identical). Render estimate: standard 480p = 27 Speakeasy seconds; HD 720p = 54. Waiting for KT's confirmation before any render.
