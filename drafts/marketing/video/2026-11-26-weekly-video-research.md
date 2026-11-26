# Weekly jobs video: research, catalog, checklist, scripts (26 Nov 2026)

Status: **PROPOSED, waiting for KT** (script choice, Yireh pronunciation, voice). Nothing has been spent since the first attempt.
Process KT asked for (25 Nov): think, gather, catalog, pick what is relevant, checklist, then execute.
Evidence labels: **[Established]** checked by us or from a primary source; **[Reported]** from a secondary or vendor source we could not check; **[Hypothesis]** our reasoning, untested.

## 1. Why the first attempt failed (diagnosis from the files, not a guess)

| KT's note | What actually happened | Fix |
|---|---|---|
| "The script is off" | It opened on a quote from the fine print (abstract, no person in it), then read out four job titles as a list, then stacked three disclaimers ("free", "no fee", "check each employer's rules") at the end. No moment, no feeling, no turn. | Open on a moment the viewer has lived (KT's "halfway through an application" hook). One pain, one turn, one proof, one step. Job titles go on screen, not in the voice. |
| "The voice is off" | The voice was chosen from catalog voices described as "Tech Explainer" and "calm, patient" (`voices.json`). That suits tutorials, not a social hook. | Audition voices described as energetic and conversational; also offer KT's own voice. |
| "Cadence is off; no base for inflection or excitement" | Delivery was preset `warmer`, style `0`, stability `0.5` (`narration.json`): the flattest settings. The script had long sentences and almost no pauses, so the voice had nothing to rise or fall on. | Preset `energetic`, style about 0.35, stability about 0.35, speed about 1.05; short sentences; ellipses and full stops placed where the voice should pause or land. ElevenLabs says punctuation shapes rhythm and an ellipsis gives a natural pause [Established, ElevenLabs docs]; lower stability gives more varied delivery [Reported, Runware guide]. |
| "Pronunciation of Yireh is off" | "Yireh" was written as plain text, so the voice guessed. | Write it in the narration as a phonetic respelling once KT confirms the sound (section 6). The Hebrew word (yir'eh) is said "yir-EH", stress on the second syllable [Established, Strong's H3070 lexicons]; KT's own pronunciation decides. |

Spent on the first attempt: about 47 narration credits plus the presenter image. No video was rendered.

## 2. What we know (catalog)

### 2a. The audience's pains, in their words (from `drafts/marketing/audience-research-and-icp.md`, 31 Oct, verbatim quotes there)
1. **"Remote" that isn't open to me** [Established that it is voiced, on three continents]: "Most of the ones I've applied to have ended up being fake or actually hybrid"; "can u recommend pages to find remote jobs in usa or eu... I'm desperate". A Reddit story reported in the press: four interviews for a "Remote US" role, rejected over location [Reported].
2. **Paying to look or to apply** [Established]: the biggest paid remote board charges a subscription (trial, then billed every 4 weeks, per its pricing page); its unhappy reviewers say listings were "easily duplicated on LinkedIn". Scam fear: "Legitimate companies cover recruitment costs, not candidates." The US regulator (FTC) counted job-scam losses of over $500 million in 2024, and reports rose 19% in the first half of 2025 [Reported via press; FTC figure].
3. **Silence after 100+ applications** [Established that it is voiced]: "100+ applications with ZERO interviews".
4. **Jobs scattered across many sites** [Reported]: one survey of 10,000 job seekers says they use 4.5 job sites on average (no clear date). Weak evidence; use as feeling ("ten tabs open"), not as a number.
5. **Ghost and fake jobs** [Reported]: 18-22% of postings on one hiring platform looked like ghost jobs; 86% of surveyed US adults say they have met one.
Their words: legit, real, scam, fake, US only, hybrid (but they said remote), desperate, tired, 100+ applications. Ours ("verified", "eligibility") are weaker.

### 2b. Our facts, measured on the live board (26 Nov 2026, `yirehcareers.vercel.app/jobs.json`)
- 1,765 remote jobs from 363 companies; 612 posted in the last 7 days.
- 683 (39%) are open only to people in the United States. 19 are open worldwide. 252 (14%) do not say where applicants may live.
- Pick a country and the board shows only jobs open to that country (unspecified ones stay hidden unless you ask to see them). This is true by construction (`index.html`).
- Every job opens its original posting; the board is free, needs no account, and we never charge to apply (trust rule 1).
- Pay is shown on 1,068 jobs (61%), only where the posting states it.
- What we must NOT say: "all remote jobs" (we list 363 companies, not all), "every job shows who can apply" (14% do not say), "guaranteed", "the only board", any hiring-system name, "straight to the employer".

### 2c. What converts in short video (strength of evidence is low; vendor-heavy)
- TikTok's own guidance: put the content proposition in the first 3 seconds [Established, TikTok]. Most recall impact happens in the first 6 seconds of an ad [Reported, TikTok internal analysis via press].
- Common structure for 30-second ads: hook (0-3 s), problem/agitate (3-8 s), solution and proof (about 10 s), call to action (about 2 s) [Reported, several ad-tool vendors; heuristics, not tests].
- Problem-agitate-solve fits viewers who already feel the problem [Reported]. Our viewers do (2a).
- Pace: one audio-ad study found about 180 words a minute worked best, and a shorter script at that pace beat a longer one read fast [Reported; 51 people, audio only]. For us: 70-85 words for 30 seconds, leaving room for pauses.
- Write three openings for one body and test them [Reported, common advice]. This is how we learn which pain sells.
- Text on screen and motion in the first two seconds help hold viewers [Reported, vendor data].

### 2d. AI presenter and voice: trust and rules
- Research is mixed: one study found disclosing an AI avatar lowered trust and purchase intent; another found the opposite; a human presenter raised trust in two experiments (n=656 and 769) [Reported, academic]. Clumsy or "lacking human presence" AI hurts trust; "AI-assisted with human supervision" is preferred [Reported].
- TikTok: realistic AI-generated people or voices must carry the AI-generated label; voice clones count [Established for the label, TikTok support page]. Ads with realistic AI content need disclosure too [Reported].
- Reading for us [Hypothesis]: our audience's top fear is being scammed. A realistic AI face selling jobs may look like the scam they fear. KT's real voice over screen recordings of the board (no AI face) may earn more trust than an AI presenter. Worth testing.

### 2e. Voice options
- Catalog voices: auditions are free. Pick by description: energetic, conversational, young adult, social media, not "explainer" or "customer care".
- KT's own voice: BHuman can use a reference recording (`provider_mode: reference_audio`) or a voice cloned in the BHuman app. ElevenLabs advice for an instant clone: 1-2 minutes of clean, dry audio (no music, echo or second voice), one steady delivery style; more than 2-3 minutes adds little [Established, ElevenLabs docs]. Recording in the energetic style KT wants is what makes the clone energetic.
- Or KT records the voiceover directly on a phone (free, the most human option); we supply the script with pause and stress marks.

## 3. What is relevant and what we act on
1. Lead with the location pain: it is the loudest in the research, and our country filter is the clearest proof we have.
2. Paying-to-look and scam fear: the second hook to test. "Free, and we never charge you to apply" answers both.
3. "All in one place": use the honest version ("1,765 remote jobs, 363 companies, one place"), never "all".
4. Silence after 100 applications: leave it for a CV-service video later. It would mix two offers into one video.
5. Ghost-job statistics: do not use. The numbers conflict, and our 30-day age limit is not proof that a job is real.

## 4. Checklist (each line has a test)
| # | Step | Done when |
|---|---|---|
| 1 | KT picks a script (A, B or C) or asks for changes | KT's yes in chat |
| 2 | KT says how "Yireh" is said | KT gives one respelling or a 3-second voice note |
| 3 | Copy check on the chosen script | No forbidden claim (2b list); every number matches the live board on the day; one legal point, said once |
| 4 | Voice: KT listens to free auditions (including voice 3) or chooses own voice | KT's pick |
| 5 | One short test narration of the hook only (about 5 s, about 5 credits) with the respelling | KT hears "Yireh" said right and the hook lands |
| 6 | Full narration (about 30 credits for 30 s) | Length 28-34 s; KT approves the audio |
| 7 | Visual plan: screen recording of the board (country picker in action) with text on screen; AI presenter only if KT wants it | KT approves |
| 8 | Render plan shown with its credit cost; start only on KT's explicit yes | KT confirms the charge |
| 9 | Post with the AI-generated label if the face or voice is AI; caption with the link | Label on; link works |
| 10 | Measure after 7 days: views, 2-second holds, average watch time, profile and link clicks (GoatCounter `utm_source=tiktok`) | Numbers recorded in `drafts/analytics/` |

## 5. Three scripts (same body, three openings, so the hook can be tested)
Read at about 165 words a minute. `...` marks a pause, *italics* the stressed word. [Screen] lines are on-screen text, not spoken. `YIREH` is replaced with KT's respelling.

### A. "Halfway" (KT's hook; location pain) — 66 spoken words, about 27 s with pauses
> You're halfway through a remote job application... and then you see it.
> [Screen: "Must be located in the US"]
> *US residents only.*
> All that time... gone.
> So we built YIREH Careers.
> Pick your country... and you only see remote jobs that are *actually* open to you.
> [Screen: country picker → list filters]
> This week: six hundred new ones.
> Every job opens the original posting. It's *free*... and we never charge you to apply.
> Link in bio. Pick your country.

### B. "Pay to look" (paywall and scam fear) — 63 spoken words, about 26 s with pauses
> Stop paying to look at remote jobs.
> Some sites charge you every month just to search... and a real employer will *never* ask you to pay to apply.
> YIREH Careers is free. No account. No fee.
> Seventeen hundred remote jobs, from three hundred and sixty companies... in one place.
> [Screen: 1,765 remote jobs · 363 companies]
> Pick your country, and see only the ones open to you.
> Link in bio.

### C. "Four in ten" (our own number; location pain) — 61 spoken words, about 25 s with pauses
> Almost four in ten "remote" jobs... are only open to people in the US.
> [Screen: 683 of 1,765 · US only]
> We counted.
> If you live anywhere else, that's a lot of applications going nowhere.
> YIREH Careers lets you pick your country... and shows you only the remote jobs open to *you*.
> Six hundred new this week. Free. And we never charge you to apply.
> Link in bio.

Recommendation [Hypothesis]: post **A first** (a moment people have lived, in their words, and KT's own idea), then B and C in the next two weeks with the same visuals, so we can see which pain gets watched and clicked. All numbers are refreshed from the live board on the day of recording.

Copy check done on all three: no "all remote jobs", no "guaranteed" or "only", no hiring-system name, no country other than the US (which is in the posting text the viewer sees), "free" and "never charge you to apply" are trust rule 1, numbers measured 26 Nov.

## 6. Yireh pronunciation
**Decided by KT, 26 Nov 2026:** "Yi" as in "why", "reh" as in "ray" (YYE-ray, /ˈjaɪ.reɪ/). In narration text spell it "Yai-ray"; on screen and in captions it stays "Yireh". Voice: Olivia (ElevenLabs `pPoztmvzd5p26S3MsNrV`), delivery preset energetic, stability 0.35, style 0.35. Script: KT's version as edited in chat on 26 Nov (see `2026-11-26-chatgpt-sop-review.md`); presenter for opening and ending only, board footage in the middle.

Earlier candidates (superseded):
The narration must spell the name the way it sounds. Candidates (KT picks, or sends a voice note):
1. "Yeer-eh" (Hebrew-like; stress on the second syllable: yeer-EH)
2. "Yee-ray" (like the end of "Jehovah Jireh" in many worship songs, with a Y)
3. "Yeer-ay" (stress on the first syllable: YEER-ay)
Once chosen, it goes into the narration text only; the on-screen text and captions keep "Yireh".

## Sources (read 25-26 Nov 2026)
- TikTok AI-generated content: https://support.tiktok.com/en/using-tiktok/creating-videos/ai-generated-content
- TikTok first-3-seconds guidance and hook-rate benchmarks (vendor): https://billo.app/blog/hook-rate-to-hold-rate ; https://www.marketingbrew.com/stories/2023/12/18/pay-attention-to-me-report-shares-brand-tips-for-catching-users-interest-on-tiktok
- Ad script structures (vendor): https://motionapp.com/blog/how-to-write-ugc-ad-scripts ; https://www.gotolstoy.com/blog/how-to-structure-ugc-ads
- Speaking rate study: https://yougov.com/articles/28144-audio-ads-180-words-minute-commercial-optimal-timi
- AI presenter trust: https://www.mdpi.com/2076-328x/16/2/240 ; https://www.news.vcu.edu/article/2025/07/in-creating-an-ad-using-ai-for-scenes--but-not-people--may-retain-consumer-trust ; https://marketingdive.com/news/ai-disclosure-labels-dont-hurt-ad-performance-heres-what-the-numbers-say/822711/
- ElevenLabs delivery and pronunciation: https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices ; https://elevenlabs.io/blog/pronunciation-dictionary-guide ; https://runware.ai/docs/models/elevenlabs-v3/guides/directing-with-audio-tags
- ElevenLabs voice cloning: https://elevenlabs.io/docs/product-guides/voices/voice-cloning/instant-voice-cloning
- Yireh: https://biblehub.com/hebrew/3070.htm ; https://www.blueletterbible.org/lexicon/h3070
- Paid boards: https://www.flexjobs.com/pricing.aspx ; https://www.trustpilot.com/review/www.flexjobs.com?page=8
- Job scams: https://fortune.com/2025/11/17/ftc-data-confirms-job-offer-text-scams-more-common-now/
- US-only remote frustration: https://hackernoon.com/us-only-vs-work-from-anywhere-remote-jobs-problem ; https://weworkremotely.com/how-to-overcome-the-hardest-parts-of-landing-a-remote-job
- Ghost jobs: https://fortune.com/2025/01/16/job-market-rife-fake-listing-ghosting-hiring-managers/ ; https://www.resumebuilder.com/ghost-jobs/
- Job sites used: https://grabjobs.co/resources/career-resources/job-search/survey/
- Firecrawl was out of credits for this research (resets 26 Nov 05:29 UTC); WebSearch was used instead, so creator videos themselves were not watched. That is a gap: KT, or a later Firecrawl pass, can add 5-10 real remote-job videos with their view counts.
