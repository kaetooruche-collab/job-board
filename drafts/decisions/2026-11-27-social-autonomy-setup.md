# Social agency: autonomy switches, format plan, BHuman budget, presenter cast (27 Nov 2026)

Status: DECIDED by KT, 27 Nov 2026 (answers 1-5 in the social agency session), except where marked.

## 1. Scheduled sessions and reminders: YES
- Monday plan, posting-day publish and Friday review run as scheduled tasks that fire into the social agency session (map: `social/OPERATING-SYSTEM.md`).
- Google Calendar reminders for KT (kaetooruche@gmail.com) for the first two weeks: approve each week, check the first posts, read each review.

## 2. Mode: approve-week (AGREED)
`social/state.json` mode `approve-week`. Week of 1 Dec approved (KT: "5. yes"). Each later week needs KT's "yes week <date>". Autopilot only after 2-3 clean weeks and KT's word.

## 3. Format plan: YES, because the evidence supports it (KT: "if support - yes")
| Part of the plan | Evidence | Strength |
|---|---|---|
| No single-image posts on Instagram; carousels instead | Mosseri, 23 Oct 2026: "carousels do better than single photos" | Reported quote of the platform head (tier 2) |
| Video for reach on all three | Buffer, 4M+ posts: Reels 36% more reach than carousels; TikTok ranks by watch behaviour | Vendor (tier 4) plus platform guidance |
| Carousels for depth | Buffer: carousels 12% more engagement; Socialinsider leads on carousels | Vendor (tier 4); Dash Social conflicts on views, but the plan uses both formats, so the conflict doesn't change it |
| Facebook: a tagged board link in the caption | Buffer's API: a link card can't be combined with images, so the link goes in the text; Facebook captions make links clickable | Established (API schema) |
| Instagram Stories with a link sticker on roles days | Buffer API supports `link` on stories; Stories reach followers, not new people | Established mechanics; low value while followers are few, near-zero cost |
Weakest part: Stories (few followers). Kept because they cost nothing and give the only clickable Instagram link besides the bio.

## 4. BHuman: Ultimate plan, budget 200 credits a month for social
- Plan (KT's screenshots, 27 Nov): Ultimate, $150 a month, 500 shared credits; 497.75 left. Pricing page: 1 Speakeasy minute = 15 credits.
- Cost per weekly video: a 30-second render was estimated at 30 Speakeasy seconds = 7.5 credits (plan_render, 27 Nov); narration at 1 credit per second per the tool docs (unit to be confirmed on the next render). Allow about 20-25 credits per video including one retake and voice auditions; a new presenter's first video about 40.
- Allocation: up to 200 a month for social (4-5 weekly videos, new presenters, one test), 300 left for KT's other uses (AI Studio, outreach). Each render still needs KT's yes on its estimate (BHuman's own rule), given in the weekly approval.
- Open: Video 1 carried a watermark (`output_watermarked.mp4`). Check the next render on Ultimate for one.

## 5. Week 1 wording and the free CV-check post: YES

## 6. Presenter, voice and background (KT: "you can't use the same presenter or background or voice every time")
- **Agreed in part.**
  - For: TikTok lists repetitive and unoriginal content as ineligible for the For You feed (as quoted in a 2026 guide; TikTok's page was not readable by our scraper). Advertising wear-out is well documented.
  - Against a new face each time: research on recurring brand characters (Garretson & Niedrich 2004; Callcott & Lee 1995) and Ehrenberg-Bass on distinctive assets says a recurring character builds recognition and trust.
- **Decision:** a small cast of 2-3 presenters (`social/data/cast.json`), each always with its own voice. The setting, outfit and framing change every video; no presenter and setting pair repeats within 8 weeks. Scripts are written for the presenter's persona and setting. The planner picks the presenter and setting.
- Label: hypothesis. Test it with Instagram Trial Reels once there are numbers.

## 7. Silence counts as yes (KT, 27 Nov, later the same day; overrides the 'needs KT's yes' parts above)
KT: "my yes should not hold up things ... set up a backup that if you don't get my yes, it goes out as is and as scheduled based on your researched data. The goal is autonomy."
- A week with no answer is approved automatically at 23:00 Istanbul on the Monday before its Tuesday (`state.json` `auto_approve_after_deadline`). KT's "no" or `hold` still stops it.
- BHuman renders without an answer: allowed when `plan_render` estimates 30 credits or fewer and the month stays within the 200-credit budget (KT's standing confirmation, recorded in `state.json`). Otherwise the free screen-only video goes out on time.
- What still protects quality without KT: the copy checker in schedule mode, same-day role checks, the `social-reviewer` agent every week (a BLOCK it can't fix drops the post), and the publishing gate.
- Residual risk: a post that passes every check but reads badly goes out unseen. Accepted by KT for autonomy. The Friday review looks for it.

## 8. Reversed: KT's yes is required again, with a backup (KT, 27 Nov, after section 7)
KT: "your risk is valid and very true, you were right to leave things as before, I need to check and approve before it goes out and if I can't check, a good back-up solution should exist." Section 7 is withdrawn.
- **Approval required.** Nothing new goes out without KT's yes.
- **Escalation.** A review reminder the day after planning, then a last call at 20:00 on the deadline Monday (pop-up and email).
- **Backup when KT can't check** (`social/tools/backup.py`; the gate enforces it): past the deadline with no answer, a post goes out only if its hook and caption (numbers masked) come from a week KT approved. It must have no AI presenter or voice and must not be a service post. Other posts are swapped for an approved post of the same series (an unapproved video becomes an approved roles post), or held until KT is back.
  - Roles, numbers and dates are still refreshed and re-checked on the day: that is data, not new wording.
- **No BHuman render without KT's yes.**
- **Why this backup** (alternatives considered):
  - (a) Publish anyway: rejected; the unseen-awkward-post risk.
  - (b) Skip the week: safe, but it breaks posting consistency, which the platforms reward and an audience-building account needs.
  - (c) Approved material only: no unseen wording reaches the public, and the account keeps posting.
  - Its cost: repeats. The Friday review watches for fatigue.
