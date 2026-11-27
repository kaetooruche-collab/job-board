# The questions this agency must answer, and where trustworthy answers come from (27 Nov 2026)

KT, 27 Nov: "what we need is what has been proven and researched to work… is there a repo that gives verified researched insights into brand colouring, copy, content creation, hooks, covers, thumbnails, hashtags? Compile a thorough list of the questions we need solid answers to, then find sources we can trust."

## 1. Is there a repo? No.
- Searched 27 Nov: GitHub and the web for curated, evidence-based marketing or creative research collections.
- Found: Google's marketing-solutions repos (ad tooling, not research), small "ad optimisation" student projects, and the five agency frameworks assessed in `2026-11-27-agency-repos-assessment.md`.
- No repository collects peer-reviewed or platform-verified findings on colour, hooks, covers or hashtags. The repos are methods: someone's way of working, not evidence that it works.
- **What we do instead:** build our own evidence library (this file and `research/`), with every answer graded by the tiers below.

## 2. Which sources to trust, in order
| Tier | Source type | Trust | Examples we use |
|---|---|---|---|
| **1** | **Our own tests and numbers** | Highest for *our* audience; small samples at first | Buffer metrics, GoatCounter by `utm_source`, Instagram Trial Reels (shown to non-followers first), YouTube Test & Compare if we ever post there |
| **2** | **The platform itself** | High for how ranking works and the rules; it doesn't tell us what our audience likes | Instagram's head Adam Mosseri and @creators; creators.instagram.com; TikTok Creative Center and Creator Academy; YouTube Help and its Creator Liaison; Meta Business Help |
| **3** | **Peer-reviewed research and research institutes** | High for general human behaviour; check sample, date and context | Ehrenberg-Bass Institute (distinctive brand assets); Elliot & Maier, *Annual Review of Psychology* 2014 (colour); Labrecque & Milne, *JAMS* 2012 (colour and brand personality); Kanuri et al., *IJRM* 2024 (colour complexity); Bakhshi et al., CHI 2014 (faces on Instagram); Lingnan University, *J. Business Research* 2024 (16,215 YouTube thumbnails) |
| **4** | **Large vendor studies** | Medium: big samples, their own customers and definitions, commercial motive | Buffer (millions of posts), Sprout Social, Socialinsider, Dash Social, 1of10 (300,000 YouTube videos) |
| **5** | **Blogs, gurus, AI answers, GitHub repos** | Ideas to test, never evidence | Most "X% more clicks" claims |

**Watch for laundered numbers.** Example (MarkStudios' source audit, Sept 2026): "faces get 38% more clicks" is quoted everywhere for YouTube. It actually comes from a 2014 study of *likes on Instagram photos* (Georgia Tech and Yahoo Labs, 1.1 million photos). Every number we use is traced to its original source.

## 3. Your question first: a yellow post leading to a blue-and-white board
- **Your instinct has support** (Tier 3). The Ehrenberg-Bass Institute's research on distinctive brand assets says colour, font and logo help people recognise a brand in clutter only when used consistently. Romaniuk: "Inconsistencies in colours, fonts, logos and the like are the enemy of distinctive asset building" and "Consistency is crucial."
- **Practitioner advice agrees** (Tier 5). "Message match" from conversion practice (Unbounce and others) says the ad and the page it opens should look and promise the same. We found no peer-reviewed test of ad-to-page colour match specifically.
- **Colour meaning depends on context** (Tier 3). The strongest review (Elliot & Maier, 2014) finds colour effects real but dependent on context. It rejects universal rules like "blue means trust".
  - Labrecque & Milne (2012) found what predicts preference is the colour *fitting the brand's personality*.
  - Blue suits "competent and reliable", which is what a job board that verifies postings wants to be.
- **Variety still helps attention** (Tier 3). Kanuri et al. (2024) found more colour variety *inside* an image draws attention and engagement.
- **How to reconcile them (our reading, to test):**
  - Keep **blue and white as the dominant brand colours on every post**: the mark, the blue, Inter, the white card.
  - Get variety from **inside** the image: real board screenshots, coloured pills and labels, one accent colour per series (amber for warnings, teal for the service) used as a highlight, not as the whole background.
  - Full-bleed yellow or teal posts are the weakest choice by this evidence. I'm changing the renderer to match (section 5).

## 4. The question bank
Status: **A** = answered well enough to act on (source given) · **P** = partly answered; act on it and test · **O** = open; only our own data can answer it.

### A. Audience
| # | Question | Best source | Status |
|---|---|---|---|
| A1 | Where do our viewers and visitors actually live? | T1: GoatCounter locations (PR #80), TikTok and Instagram audience tabs | O |
| A2 | What languages do they read comfortably? | T1 + T3 | O (Latin America is Spanish/Portuguese-first: niche research 26 Nov, T4) |
| A3 | When are our followers online? | T1: TikTok Studio, Instagram Insights | O (starting rule: 15:00 UTC) |
| A4 | What do they fear and want, in their words? | Comments, Reddit, Nairaland (audience research 31 Oct) | P |
| A5 | What do they search for on TikTok and Instagram? | T2: TikTok Creative Center keyword insights; T1 search terms | O |

### B. Message and positioning
| # | Question | Best source | Status |
|---|---|---|---|
| B1 | What is our one promise, and what proves it? | Our product + decision 26 Nov ("people outside the US") | A |
| B2 | How are we different from the big free boards with a country filter? | T1 competitor check (16 Nov review: Himalayas, Remote Rocketship) | P |
| B3 | Which claims can we make legally and honestly? | CLAUDE.md copy rules; FTC and EU unfair-practices guidance | A |

### C. Brand identity and colour
| # | Question | Best source | Status |
|---|---|---|---|
| C1 | Should every post use the brand colours, or vary? | T3 Ehrenberg-Bass; Elliot & Maier; Kanuri | A (section 3) |
| C2 | Which brand elements must never change? | T3 Ehrenberg-Bass (mark, colour, font) | A: YC mark, blue, Inter, card |
| C3 | Do colours mean different things to our audience's cultures? | T3 cross-cultural colour research (Aslam 2006, in the reviews) | P: meanings are culture-dependent; we use colour for recognition, not symbolism |
| C4 | Is our text readable on phones, in sunlight, for low vision? | WCAG contrast standard | A: check every theme (AA) |
| C5 | Does a post that looks like the site convert better than one that doesn't? | T1 test | O |

### D. Formats per platform
| # | Question | Best source | Status |
|---|---|---|---|
| D1 | Which formats reach new people on each platform? | T2 Mosseri; T4 Buffer, Socialinsider | A (`2026-11-27-formats-and-colour.md`) |
| D2 | Carousel or single image? | T2 Mosseri, 23 Oct 2026: carousels do better | A |
| D3 | How long should our videos be? | T4 Buffer, 2.7 million Reels; T2 TikTok; T1 our watch time | P |
| D4 | How many slides per carousel? | T4 | O |
| D5 | Are Stories worth it with few followers? | T2 (Stories reach followers) | P: cheap; test once there are followers |
| D6 | Does the same file posted to all three hurt reach (watermarks, crops)? | T2 platform guidance on originality and watermarks | P: post clean, original files only |

### E. Hooks and copy
| # | Question | Best source | Status |
|---|---|---|---|
| E1 | What must happen in the first 1–3 seconds? | T2 TikTok and Instagram creator guidance | A: the point and motion up front |
| E2 | Number vs question vs statement hooks | T3 Lingnan 2024 (question titles went with fewer views, observational); T1 tests | P |
| E3 | How long should captions be? | T4 | O |
| E4 | Which call to action gets clicks without looking like a scam? | Audience research (Fear 2) + T1 | P: link in bio, never "DM me" |
| E5 | Does negative framing ("stop wasting…") help or hurt? | T3 Kanuri 2024 (negative text weakened the colour effect); T1 | P |
| E6 | Plain English level for second-language readers | Plain-language standards (UK/Australian style manuals) | A: short, plain, one idea per line |

### F. Covers, thumbnails and visuals
| # | Question | Best source | Status |
|---|---|---|---|
| F1 | What makes a cover or thumbnail get tapped? | T2 YouTube: tests are judged on watch time, not clicks, to avoid clickbait; T3 Lingnan 2024 (faces and text went with more views; long text with fewer clicks) | P |
| F2 | Faces or no faces? | T3 Bakhshi 2014 (Instagram likes +38%); T4 1of10 (300,000 YouTube videos: no overall difference, depends on niche) | P: test |
| F3 | Text on the cover: how much? | T3 Lingnan 2024 (long text worse) | P: about 6 words or fewer |
| F4 | AI presenter, human voice, or screen only? | T3 (AI presenter trust studies, 26 Nov research) | P: test; AI label always |
| F5 | Real screenshots vs designed slides | T3 Kanuri (colour complexity); T1 | P |

### G. Distribution
| # | Question | Best source | Status |
|---|---|---|---|
| G1 | Best days and times | T4 studies conflict; T1 | O (starting 15:00 UTC) |
| G2 | How often to post | T4 vendor studies (not yet read for this); T1 | O |
| G3 | Do hashtags help, and how many? | T2 Instagram: 5 maximum since Dec 2025, "generic tags don't help"; T3 Martínez-Borda 2026 on TikTok: relevance and combination matter more than count | A: 3–5 relevant tags |
| G4 | Keywords in captions and on screen for TikTok and Instagram search | T2 TikTok Creative Center | P |
| G5 | Trending audio: does it help, and is it licensed for business accounts? | T2 (business accounts are limited to commercial music) | P |

### H. Trust and compliance
| # | Question | Best source | Status |
|---|---|---|---|
| H1 | When must we label AI? | T2 TikTok and Meta rules | A |
| H2 | What makes a job post look like a scam to our audience? | Audience research; T2 platform scam guidance | A |
| H3 | Can we show real candidates or results? | FTC endorsement guides; CLAUDE.md | A: only real, consented, typical |

### I. Measurement and testing
| # | Question | Best source | Status |
|---|---|---|---|
| I1 | Which number judges each kind of post? | T2 Mosseri: sends per reach, likes per reach, watch time | A (funnel field on every post) |
| I2 | How many posts before we can call a winner? | Statistics; T2 YouTube's own test waits for a "meaningful difference" | P: our working rule (not a cited standard) is no calls under about 1,000 views per variant |
| I3 | How to test fairly with a small account | T2 Instagram Trial Reels (same audience type) | A: use Trial Reels for hook tests |
| I4 | Which visits and enquiries came from social? | T1 UTM + GoatCounter; Facebook per-post links | P |

### J. Conversion
| # | Question | Best source | Status |
|---|---|---|---|
| J1 | Does the bio and profile tell people what to do next? | T2 platform profile guidance; T1 | O |
| J2 | Where should the link land: home, a filtered view, or a social landing page? | Practitioner message match (T5) + T1 test | O |
| J3 | What turns a board visitor into a free-check request? | T1 (site analytics, job-board session) | O |

## 5. What changes now
1. **Colours.** Blue and white dominate every post. Amber and teal become accents (labels, number tiles, highlight bars) on the light background, not full backgrounds. Evidence in section 3. The navy, light and bright-blue themes stay.
2. **Hook tests run as Instagram Trial Reels** when there are videos (shown to non-followers first; Instagram's own feature).
3. **Every new "fact" about what works** gets its tier, source and date in `research/`; Tier 5 claims are never used as reasons on their own.
