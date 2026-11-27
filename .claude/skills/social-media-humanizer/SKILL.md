---
name: social-media-humanizer
description: Mandatory for ANY words Yireh Careers' social accounts will show or say - video scripts, presenter lines, hooks, captions, headlines, carousel and static slides, Story text, on-screen text, CTAs, comments and replies, hashtags and descriptions. Makes copy sound like a thoughtful person talking to another person, chooses the right emotional tone, and runs the first-impression and read-aloud tests before anything is approved. Use whenever social copy for Yireh Careers is written, edited, reviewed or replied with.
---

# Social media humanizer (Yireh Careers)

Someone is going to meet this while scrolling, tired, on a phone, maybe reading in their second language. They are not waiting for an advert. Give them a reason to stop: recognise something, feel something, learn something, or get curious about something. Then keep the promise the opening made.

This skill shapes *how* things are said. *What* may be claimed is set by `CLAUDE.md` (copy rules, no guarantees, no hiring-system names, no country named in posts) and `social/BRAND_GUIDELINES.md`. If they conflict, the rules win and the wording finds another way.

## 1. Before writing a single line: picture the reader
Write the answers down in the post's brief (one line each). If you can't answer, you're not ready to write.
1. **Who is this for, specifically?** Not "job seekers". For example: a customer-support agent with four years' experience who keeps finding "remote" roles that turn out to be US only; or a graduate applying for their first role; or a senior engineer sizing up whether remote is realistic from where they live. Don't assume unemployed, young, inexperienced or desperate.
2. **What are they thinking right now?** In their words, not ours. Use `social/AUDIENCE_RESEARCH.md` (verbatim quotes). "Remote but not for me." "100+ applications, zero interviews." "Is this legit?"
3. **What would make them stop?** A situation they recognise, a fact they didn't know, a mistake they might be making, something they can do in the next minute.
4. **What would make them trust it?** Specifics they can check: a real posting, a dated number, a screen recording of the actual board. Not adjectives.
5. **What is the one next step?** Exactly one. And only if it's natural (see section 9).

## 2. Choose the emotional tone on purpose
Pick **one primary tone** (and at most one secondary) per piece, from this table, and write it in the brief. Tone decides word choice, sentence length, humour, punctuation and, for video, the delivery settings in `bhuman-presenter-director`.

| # | Tone | Use it for | Sounds like | Never when | Delivery hint |
|---|---|---|---|---|---|
| 1 | Happy | Genuinely good news: a feature that helps, a useful find | Light, warm, a smile you can hear | The subject is rejection, scams or money worries | `warmer`, style 0.3-0.4 |
| 2 | Jolly | Relatable job-hunt absurdities, light myth-busting | Playful, self-aware, one joke not five | Anything about someone's loss, money or safety | `energetic`, speed 1.05 |
| 3 | Curious | Surprising patterns, "have you noticed…" | Questions that are real, not rhetorical filler | You already know the answer is obvious | `natural`, slight lift at ends |
| 4 | Surprised | Data reveals, unexpected rules | A beat of disbelief, then the fact plainly | The "surprise" is manufactured | pause before the reveal |
| 5 | Frustrated | Naming a real job-search annoyance (US-only "remote", ghosting) | Mild, recognising, shared; "you know the feeling" | Ranting, blaming employers wholesale, exaggerating | `natural`, slightly slower on the sting |
| 6 | Sad / empathetic | Rejection, long searches, discouragement | Quiet, honest, no silver linings forced in | Exploiting it to sell; "don't give up!!" | `deliberate`, speed 0.92-0.95 |
| 7 | Serious | Scams, money, eligibility rules | Composed, exact, no jokes | You're tempted to dramatise | `deliberate`, stability 0.6 |
| 8 | Professional | CV, ATS, LinkedIn, interview advice | Knowledgeable colleague, clear steps | It turns into jargon or a lecture | `natural`, stability 0.55 |
| 9 | Reassuring | How-to and "here's what you can do" | Calm, steady, "here's how" | The facts don't support reassurance | `warmer`, speed 0.95 |
| 10 | Excited | A genuinely new, useful feature | Energy from the specifics, not exclamation marks | It's routine; you'd be faking it | `energetic`, style 0.4 |
| 11 | Reflective | Career development, bigger-picture thoughts | Measured, a thought worth sitting with | The viewer needs a quick answer | `deliberate`, longer pauses |
| 12 | Assertive | Correcting a myth, a clear rule | Direct, short, confident | Talking down to people | `natural`, falling endings |

Matching examples:
- Discovering a "remote" job is US only → **frustrated (mild) + curious**, then reassuring.
- Showing how to filter by where you live → **reassuring + professional**.
- A useful new board feature → **excited** (only if it's really new and useful).
- CV rejection → **empathetic + serious**, never jolly.
- "Pay to see jobs" scams → **serious + assertive**.

Vary the tone across a week. Two posts in a row with the same tone and the same structure is a warning sign.

## 3. The first-impression test (every piece, before anything else)
Look only at the first thing a person meets: the first spoken sentence, the first frame and its text, the first slide, the first line of the caption, the headline of a graphic.
- **Is there a reason to continue?** A recognisable situation, a specific fact, a useful promise, a real question.
- **Does it start with the subject?** Delete anything before the subject.
- **Could a stranger understand it in one second without context?** No jargon ("eligibility", "ATS-optimised", "classifier", "verified listings").
- **On screen and on covers: six words or fewer** for the headline (long text costs clicks; Lingnan 2024, tier 3 in `social/research/2026-11-27-question-bank-and-sources.md`).

Never open with: "Hello everyone", "Hey guys", "Welcome back", "Today we're going to talk about", "In this video", "Did you know that…" as a reflex, a logo sting, the brand name, or a generic line about how hard the job market is.

## 4. Hooks that earn attention, and keep their promise
Use the approach the subject deserves. Each hook must be **fulfilled** by what follows; if the body can't deliver, change the hook.
- **A situation they recognise:** "You find the perfect remote job. Then you scroll to the bottom."
- **A specific, checkable fact:** "Out of 1,987 remote postings on our board today, 27 are open to anyone, anywhere." (measured that day, dated on screen)
- **A misconception and its correction:** "'Remote' tells you where you'll work. It doesn't tell you where you can live."
- **A demonstration:** start on the screen doing the thing.
- **A before/after contrast:** the same search before and after one filter.
- **An open loop**, closed within the piece: "There's one line in every posting that saves you an hour. It's not the title."
- **A real question**, only if people genuinely wonder it: "How do people outside the US actually find remote work?"

Don't: invent suspense the content can't pay off; use "you won't believe"; promise jobs, interviews or outcomes; make a number sound bigger than it is; ask three rhetorical questions in a row.

## 5. Sound like a person
**Do:**
- Contractions (you're, it's, don't, we've).
- Specific, recognisable situations ("the 'apply from' line at the bottom", "the fourth round of interviews").
- Everyday words: "check" not "verify", "jobs you can apply for" not "eligible opportunities", "posting" not "listing" when talking about the employer's page.
- Short and long sentences mixed. A fragment now and then. Then a fuller sentence that explains.
- One idea per sentence. For second-language readers, prefer common words over idioms that don't travel ("hit the ground running", "a slam dunk").
- Natural transitions: "So", "Here's the thing", "Which means", "And yes,", or none at all.
- Occasional, light humour where the tone allows (see section 2). One joke, not a routine.

**Don't (the checker warns on the phrases):**
- Corporate or AI filler: "unlock your potential", "in today's competitive landscape", "your dream job awaits", "take your career to the next level", "game-changer", "elevate", "seamless", "leverage", "navigate the job market", "empower", "embark on a journey", "look no further", "whether you're X or Y", "it's no secret that", "the ultimate guide", "delve", "in the world of", "let's dive in", "buckle up".
- Forced enthusiasm: stacked adjectives, "amazing!", more than one exclamation mark in a piece.
- Repetitive structures: every line the same length; every caption "Hook. Three bullets. CTA."; the rule of three in every paragraph; every video ending "Link in bio!".
- Explaining what the viewer just saw.
- Empty motivation ("keep going, your time will come!").
- Every caption sounding like an advert. Most captions should read like a note from a knowledgeable friend.

**Rewrite examples (from our own drafts):**
- "Verified remote opportunities for every stage of your career." → "See which remote jobs hire where you live."
- "Our platform empowers job seekers to discover eligible roles seamlessly." → "Tell the board where you live. It shows the jobs open to you."
- "Unlock remote jobs worldwide today!" → (claim isn't true; most aren't worldwide) "Most remote jobs name a country. These three don't."
- "Remote roles you can apply for across whole regions." → "Open beyond one country." (shorter, and doesn't promise eligibility)

## 6. Rhythm and variety
Across a week, vary: the opening type (section 4), sentence length, how the post ends (a question, a fact, a next step, nothing), the tone, the presenter, the visual treatment. A viewer should not be able to predict the next line just because it's another Yireh Careers post. `check_post.py` blocks a hook used in the last 60 days; you are responsible for repeated *shapes*, which no script can catch.

## 7. The read-aloud test (every spoken line, every caption)
Say it out loud as if talking to one person across a table. Then ask:
1. Would a person actually say this? Would *you*?
2. Does it sound rehearsed or like an advert?
3. Any sentence you ran out of breath on, or tripped over? Split it.
4. Awkward transitions? Words that sound the same back to back?
5. Does the emotion fit the subject (section 2)?
6. Does the ending land naturally, or does it trail off into a slogan?
7. Any phrase from the "don't" list?
8. For narration: numbers written the way they should be said ("twenty-seven", "nearly two thousand"), brand name in its narration spelling ("Yai-ray Careers"), no symbols the voice will misread (%, /, &, $ in the script).
If any answer is wrong, rewrite and test again. For narration, also run `social/tools/voice_qc.py` on the generated audio (the presenter-director skill covers this).

## 8. Formats
- **Spoken script:** written for the ear. Shorter sentences than captions. Write it separately from on-screen text and captions; the three do different jobs.
- **On-screen text:** the few words that carry the point if the sound is off. Not a transcript (captions do that). Six words or fewer per frame.
- **Captions (post text):** first line earns the tap on "more" (under ~125 characters; feeds cut the rest). Don't repeat the video. Add context, a detail, a question people would want to answer, or the next step. Two to five short lines is plenty.
- **Carousel:** slide 1 is the reason to swipe; each slide adds one thing; a logical order (problem → explanation → steps → what to do); the last slide concludes or gives the step. Never more than ~20 words on a slide.
- **Static post:** one message understood in a glance; clear hierarchy; no paragraphs in the graphic.
- **Story:** one frame, one sentence, the link sticker; never "swipe".
- **Comments and replies:** like a helpful person: specific, short, warm. Answer the actual question. Don't push the service in every reply. Never ask someone to DM a CV or personal details (the scam script our audience fears). If you don't know, say so and point to the posting.
- **Hashtags and descriptions:** 3-5 relevant tags (`social/PLATFORM_GUIDELINES.md`); descriptions written for search, in plain words people type ("remote jobs open worldwide").

## 9. CTAs: one, natural, earned
One primary action per piece, and only after giving value. Choose the one that fits:
see the board · filter by where you live · look at a category · save this · send it to someone who's job hunting · answer a question in the comments · get the free CV check · read about a service.
Don't force a CTA where it would feel tacked on; a useful tip can just end. Never: "DM me", "comment JOBS and I'll send the list", fake urgency ("only today!"), fake scarcity ("spots filling fast").

## 10. Think like the marketer, not the operator (KT, 27 Nov 2026)
The agency built and runs the board, but on social it is the **marketer**. The operator's habit of hedging every sentence ("jobs that *say* they're open to you", "listings we *believe*…") makes the product sound unsure of itself and costs attention and trust. KT: "as a marketer, your goal is to frame information such that it influences people to perceive it positively."
- **Frame true facts positively** (attribute framing: "75% lean" beat "25% fat" for the same beef; Levin & Gaeth 1988; consistent across studies in Levin, Schneider & Gaeth 1998). Say what the product does in confident, plain words: "See the jobs open to you." "Every job shows where it hires from." "Free to apply."
- **Lead with the gain, not the gap:** "27 roles open to anyone, anywhere: here they are", not "only 27"; "1,500+ jobs name where they hire, so you know before you apply", not "most jobs aren't open to you".
- **Caveats live in one place, once**, in the caption's closing line or on the board itself (the board's cards and /verify already explain the detail). Never in the hook, the cover or the CTA.
- **The line not to cross is truth, not tone:** positive framing of true facts, yes; claims that aren't true, never (no "guaranteed", no "worldwide" for a role that isn't, no invented numbers or outcomes). Those are CLAUDE.md rules and legal lines (FTC net impression).
- Small wording is the agency's call; don't ask KT about it (`state.json` copy_authority).

## 11. Truth comes first (non-negotiable)
Humanising never bends a fact. No invented jobs, numbers, testimonials, outcomes or customer stories. "Free" said once. Eligibility in the employer's words; never imply all remote jobs are worldwide; numbers measured on the post day and dated. When a vivid line and a true line compete, the true line wins and you find a vivid way to say it.

## 12. Final check (write the answers in the brief or the week's calendar notes)
**Humanisation:** human-sounding? natural aloud? right emotion? varied sentences? no AI phrasing?
**Attention:** is the first thing interesting to *this* reader? reason to keep going? interest held?
**Truth:** every claim supported? eligibility accurate? prices and service details current (`site-config.js`, services page)? any misleading impression (FTC net impression)?
**Action:** one clear, natural next step, after value?
If an important answer is no, revise before approval. **Framing:** is every true fact framed as a gain? Any hedge that makes us sound unsure (cut it, or move the one caveat to the caption's last line)?
Then run `python3 social/tools/check_post.py <posts file>`.
