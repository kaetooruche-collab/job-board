# Tone of voice: how to market a free remote job board (27 Nov 2026)

KT's question: should the copy be neutral and professional, over-enthusiastic, in the middle, or a mix? **Answer: confident and warm, "moderately enthusiastic", with the energy coming from specific benefits, not from hype. The level moves with the topic.**

## The evidence
| Finding | Source | Strength |
|---|---|---|
| "Casual, conversational, and moderately enthusiastic tones performed best" on friendliness, trustworthiness and desirability; four dimensions: funny–serious, formal–casual, respectful–irreverent, enthusiastic–matter-of-fact | Nielsen Norman Group, "The Impact of Tone of Voice on Users' Brand Perception" (50 US adults rating paired samples, plus qualitative sessions) | Tier 3: controlled but small, US only |
| Consumers rank **authenticity and relatability** as the top brand content traits; originality makes favourite brands stand out; trend-chasing is "embarrassing" to a third | Sprout Social Index 2025 | Tier 4: large survey, vendor |
| Scam job ads have about **4x the emphasised text** of real ones (40.5% vs 9.8% of descriptions) and use "work from home", "be your own boss", "income", "easy money"; real ads say "business", "opportunity"; scam ads are short and vague and skip requirements and benefits | Vidros et al. 2017, *Future Internet* (17,880 real job ads, EMSCAD dataset) | Tier 3: peer-reviewed, large real dataset |
| The same fact framed as a gain is rated better ("75% lean" vs "25% fat"); consistent across studies | Levin & Gaeth 1988; Levin, Schneider & Gaeth 1998 | Tier 3: classic, replicated |
| Our audience already fears scams and "helpers" who collect CVs | `AUDIENCE_RESEARCH.md` (verbatim Reddit, Nairaland, Trustpilot) | Tier 1: our own research |
| A leading free board (Himalayas) speaks confidently with social proof: "the best remote job board", "Join over 1,000,000+ job seekers" | himalayas.app, read 27 Nov | Observation |
| Conversion copy is built from the customer's own words (voice-of-customer "message mining") | Copyhackers / Joanna Wiebe | Tier 5: practitioner method, widely used |

## What that means for Yireh Careers
1. **Confident, never hedging.** We built something useful; say it plainly. "See the remote jobs open to you." "Every job shows where it hires from." Caveats appear once, in a caption's last line or on the board. (KT, 27 Nov: think like the marketer, not the operator.)
2. **Moderately enthusiastic.** Energy comes from verbs, specifics and outcomes ("27 roles open to anyone, anywhere, all checked this morning"). It never comes from capitals, "!!!", emoji strings or hype words, because in this niche hype *looks like a scam* (Vidros 2017).
3. **Casual and conversational, professionally accurate.** Contractions, short sentences, "you" and "we"; a knowledgeable friend, not a recruiter or a hype account.
4. **Specific beats superlative.** We can't honestly claim "the best"; we can show "1,987 jobs from 338 companies, every one linked to the original posting". Real numbers, dated, are our social proof.
5. **Positive framing of true facts.** Lead with the gain ("1,500+ jobs tell you exactly where they hire, so you know before you apply"), never the gap ("most jobs aren't open to you").
6. **Words to avoid** (scam vocabulary in this niche): easy money, be your own boss, earn from home, guaranteed income, unlimited earning, no experience needed (unless the posting says it), DM me, act now.

## The dial by content type (humanizer tones)
| Content | Where on the dial | Example opening |
|---|---|---|
| Roles open beyond one country | upbeat, confident | "27 remote roles open to anyone, anywhere. Here are three." |
| Board demos and features | light excitement | "Type where you live. Watch the board change." |
| Numbers and discoveries | curious, a little surprised | "We sorted 1,987 remote jobs by who can apply." |
| Eligibility and how-to tips | reassuring, professional | "One line in a posting saves you an hour." |
| Scams and safety | serious, assertive, calm | "Three messages a real employer won't send you." |
| CV, rejection, long searches | empathetic, steady | "Silence after 100 applications isn't always about you." |
| Free CV check and services | warm, plain, low-pressure | "Not sure if it's your CV or the jobs? We'll tell you the three things we'd fix first." |

## How it's enforced
- The conversion copywriter agent writes to this file and the humanizer skill.
- The QA agent scores every piece on tone fit, using the dial above.
- `check_post.py` warns on filler phrases and more than one exclamation mark, and blocks the copy rules in CLAUDE.md.
