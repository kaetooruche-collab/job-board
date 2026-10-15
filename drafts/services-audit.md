# Kaeto Career Services: landing page audit and decisions needed

Reviewed on 2026-10-15. Pages inspected: the rebuilt services page (`drafts/services-rebuild.html`, the one you saw on the preview link) and the older page that is live on the main site (381 lines, no prices).

Nothing described here has been changed on the live site. The live services page still shows only the older version, with your new contact email.

---

## 1. What is already working

- A clear sequence: problem, what we do, examples, packages, how it works, about you, questions, final call to action.
- One-tap WhatsApp button on every screen, and a "Questions? Chat first" link under each package.
- The before/after CV example is the most persuasive part of the page.
- Packages list what is NOT included, which helps people choose.
- Readable on a phone, works in dark mode, FAQ is keyboard-friendly.
- Payhip wiring is in place: each "Get started" button falls back to WhatsApp until a Payhip product key is added.

## 2. What needs improvement (most important first)

1. **The page sells a different offer from the one you now want.** It shows four products ($79, $149, $199, and a separate $199 LinkedIn Growth Package). Your offer is three: Essential $29, Professional $49, Executive $99 (Executive = Professional + personal branding + 30-day LinkedIn growth).
2. **Invented comparison prices.** "$227 if bought separately, save $78" and "$335 if bought separately, save $136" refer to separate prices that do not exist. This is the kind of misleading comparison you ruled out. Remove.
3. **Outcome promises.** "Get callbacks, not silence", "land a remote role", "Ready to stop getting ignored?", and, in the Growth card under "What you get at the end", "500+ quality connections in your industry" and "a visible posting history that shows recruiters you're serious". These present hoped-for results as things the customer will receive.
4. **Claims nobody can verify from the page.** "Written by a real person who reviews applications for a living", "No AI-generated filler", "Most Popular" badge (no sales data behind it), and the before/after examples, which show invented figures (340% engagement growth, 12,000+ subscribers, 3,200 monthly views) without saying they are fictional. The sample LinkedIn profile ("Jane Doe, 500+ connections") has the same problem.
5. **Deliverables on the page that are not in your brief.** LinkedIn: "engagement activity to increase your visibility", "end-of-month progress report", "custom banner and profile picture guidance", "endorsements and recommendations guidance". Complete package: "personal statement", "interview preparation guide", "15-minute consultation call", "unlimited revisions", "30 days of revision support". "Personal Statement" also appears as a service tile, but it is in none of your three packages.
6. **Personal branding is never explained.** The only mention is "content strategy tailored to your target industry". Your brief is right that this is the main differentiator.
7. **Revision rules are vague.** The FAQ says "every package includes revision rounds" without numbers, and nothing says what counts as one round or how feedback on ongoing LinkedIn work differs.
8. **Timelines contradict each other.** Package cards say 5 and 7 working days; the FAQ says 3 to 5 and 5 to 7. The 30-day Executive period is not visible before purchase.
9. **Hard to choose.** Pricing starts about 1,100 lines down the page, after the $199 Growth card. There is no side-by-side comparison.
10. **Checkout wording does not match reality yet.** The FAQ and "How it works" say people go to a secure checkout and can pay by card or PayPal. Until Payhip product keys are filled in, the buttons open WhatsApp.
11. **Silent on refunds, cancellation and privacy.** Customers send a CV, which is personal data, and nothing says how it is handled.
12. **Brand naming.** The page says "TrueRemote" and "Career Services, TrueRemote". Your brief names the business Kaeto Career Services, associated with True Remote.

## 3. What I will implement without asking (after you answer, so I only edit the page once)

Wording and meaning-preserving fixes: grammar and clarity; label the examples "Illustrative example: fictional person and figures"; remove the invented "bought separately" prices; consistent heading style, spacing and mobile layout; move pricing and a three-column comparison table up, directly under the hero; make "Executive includes everything in Professional" visible by layout; make checkout wording match what actually happens; accessibility fixes; brand name "Kaeto Career Services" in the title, about line and footer.

## 4. The two operational problems you flagged are real, and one is bigger than a wording issue

### 4a. "Manual, targeted LinkedIn connection building" conflicts with LinkedIn's rules unless the client sends the requests

LinkedIn only lets a member send connection requests from their own account. There is no "delegate" access for a personal profile. So "manual" building by you means one of three things:

- **A. Done with the client (compliant).** You identify the right people each week and write the personalised notes; the client sends the requests from their own account.
- **B. You log in to the client's account (not recommended).** This looks like account sharing, and it puts the client's account at risk.
- **C. Requests sent from your own account.** Safe, but it grows your network, not theirs.

What LinkedIn's agreement says (wording from a published copy of the User Agreement; I could not open LinkedIn's live page automatically, so please read the current text before finalising): members agree to "protect against wrongful access to your account (e.g., use a strong password and keep it confidential)" and "not share or transfer your account or any part of it"; an earlier version lists as prohibited "use or attempt to use another's account" and "use bots or other automated methods to access the Services, add or download contacts, send or redirect messages". Your own brief also rules out credential-sharing, so option B contradicts it.

### 4b. The 500+ number

- It is ambiguous: is the target 500+ **total** connections or 500+ **new** ones? A client starting with 84 connections would need about 416 new ones in 30 days.
- Reaching it depends on the starting network, how many invitations LinkedIn lets the account send (limits vary and are tighter for new accounts), and how many people accept. I did not verify specific limits or acceptance rates, so the page should not quote any.
- So it must be worded as a target, not a result, and it needs conditions.

### 4c. Publishing 12 posts "on the client's behalf"

Same issue: a personal profile cannot be delegated. Compliant ways are the client approving a scheduling tool through LinkedIn's official sign-in (no password shared), or the client posting from your ready-written calendar. I have not verified LinkedIn's current API terms for scheduling tools, so check them before choosing.

There is also no approval process defined yet (see Q6 to Q8).

### 4d. A note on arithmetic

"3 posts per week" and "12 posts in 30 days" fit together only as 4 weeks of 3 posts, with about 2 spare days.

## 5. Decisions I need from you (answer by number; silence is not approval)

**Packages and wording**

- **Q1. Merge of Complete and Growth into Executive.** The old Complete ($199: personal statement, interview prep guide, 15-minute call, unlimited revisions, 30 days of revision support) and the separate Growth Package ($199) disappear, replaced by Executive at $99. Confirm that those extras are removed, and decide what happens to the Personal Statement tile (remove it, or keep it as a paid add-on, which would be a new service and fee). *Recommendation: remove the extras and the tile.*
- **Q2. Document delivery times.** Keep the existing "5 working days" for Essential and Professional? For Executive, keep 5 working days for the CV, cover letter and profile, with the 30-day service running alongside? *Recommendation: yes to both.*
- **Q3. Extra CV details on the current cards** (Word + PDF delivery, ATS-friendly formatting, tailored to your industry, section-by-section LinkedIn copy). Keep them as descriptions of how the work is done? *Recommendation: keep.*
- **Q4. Headline.** "Get callbacks, not silence" promises an outcome. Options: (a) "Professional CVs, cover letters and LinkedIn profiles, written for you." (b) "A CV and LinkedIn presence that show what you can do." (c) your own. Also "Ready to stop getting ignored?" becomes "Ready to get started?".
- **Q5. Claims.** Can you stand behind "written by a real person who reviews applications for a living" and "no AI-generated filler"? *Recommendation: remove both unless true and provable; keep your own introduction.*
- **Q6. "Most Popular" badge.** No data supports it. *Recommendation: remove, or replace with "Most complete application package" on Professional.*

**Revisions and feedback**

- **Q7. What is a revision round?** Nothing defines it today. *Proposed definition for approval:* one consolidated set of change requests, sent in a single message after you deliver the documents. Do you want a time limit to request revisions (for example 14 days after delivery)? Is starting again from scratch, or changing the target role entirely, outside the allowance?
- **Q8. How feedback works in the 30-day Executive service.** Branding strategy and LinkedIn posts are not part of the 3 document revision rounds. *Proposed for approval:* clients receive the branding strategy first and can ask questions or request changes before posting begins; each batch of posts is shown for approval before publishing; a post the client does not approve is not published. How many changes per post or per batch? I will not invent a number.

**Executive operations**

- **Q9. Connection building method** (4a above): A, B or C? *Recommendation: A (done with the client).*
- **Q10. The 500+ target.** Options: (1) "Target of 500+ total connections; not guaranteed; depends on starting network, acceptance and LinkedIn limits"; (2) an effort commitment instead, such as "a weekly list of N targeted people with personalised notes" (N is your choice); (3) a target scaled to starting network size. Also: total or new? *Recommendation: (1) plus (2), stated as "total connections".*
- **Q11. Publishing method** (4c): client-approved scheduling tool, or client posts from your calendar? *Recommendation: scheduling tool using LinkedIn's official sign-in, only after you have checked the tool's terms; otherwise client posts.*
- **Q12. Approval timing and what if the client goes quiet.** For example: batches of drafts delivered at agreed points; client replies within X hours or the post waits; does the 30-day clock pause or keep running? You said the 30 days start at purchase. If the client takes 5 days to send their details, they lose 5 days. Do you keep that, or start the clock when the onboarding form is complete? *The page must say which one.*
- **Q13. Branding strategy deliverable.** What does the client actually receive (a written document? a call?), and who approves it?

**Terms and trust**

- **Q14. Refunds, cancellation and privacy.** None on the page. Payhip lets you set a refund policy. What do you want to offer? What do you want to say about how CVs are stored and deleted?
- **Q15. Founder introduction.** Proposed, changing only the opening and role line: *"Hi, I'm Kaeto. I've reviewed hundreds of applications and know exactly what makes a recruiter stop scrolling. Every CV, cover letter and profile I write is built to get you noticed, because I've seen what gets ignored, and I won't let that happen to yours."* Role line: "Founder, Kaeto Career Services". Please confirm that Kaeto is the name to use, that the "hundreds of applications" claim is true, and keep or soften "I won't let that happen to yours" (it reads close to a promise).

**For your information (not a page decision)**

- Money: Payhip's free plan takes 5% plus Stripe's card fee (about 2.9% + $0.30 per sale). That leaves roughly $26 from $29, $45 from $49 and $91 from $99. Executive includes a 30-day programme of manual work plus 12 written posts, so check the hours against $99.
- Until you create the three Payhip products and send me the keys, "Get started" opens WhatsApp. The Payhip products need to be created at $29, $49 and $99.

---

## 6. Draft copy for the new sections (for your approval; items marked [Q#] depend on your answers)

**Package line (Executive)**
"Executive: $99. Everything in Professional, plus personal branding and 30 days of LinkedIn growth support."

**Executive timeline**
"The Executive service runs for 30 days from the date of purchase. Your CV, cover letter and LinkedIn profile work come first [Q2]. The branding strategy, connection building and 12 posts run across the 30 days. Posts are published through the month, not on day one."

**What personal branding means here**
"Personal branding is not a headline and a nicer photo. We work out how you should be positioned for the roles you want, then decide who you should be visible to: recruiters and talent acquisition professionals, hiring managers, experienced people in your target field, peers in relevant communities, and industry specialists. The people are chosen deliberately, so your network is relevant rather than random. We do not promise that any connection leads to a reply, interview or job offer."

**Connection building** [Q9, Q10]
"We identify relevant people based on your target industry, desired roles, experience, expertise and goals [and prepare personalised invitations for you to send from your own account (option A)]. Our target is 500+ [total] connections [Q10]. This is a target, not a guarantee: it depends on the size of your starting network, how many people accept, and LinkedIn's own limits on invitations. We do not use bots or automation, and we never ask for your password."

**Content** [Q8, Q11, Q12]
"We write and publish 12 LinkedIn posts for you across the 30 days (about 3 per week), tailored to your background, target industry and branding strategy. They draw on your real experience; we do not invent achievements or opinions. You see each batch before it goes out [Q8]. This is an active service, not advice about what to post. We do not guarantee impressions, followers, recruiter replies, interviews or employment."

**Revisions**
"Essential: 2 rounds. Professional: 3 rounds. Executive: 3 rounds for the CV, cover letter and LinkedIn profile work. Branding strategy and LinkedIn posts are part of the 30-day service and follow their own approval step [Q8]; they do not use up your document revision rounds. A round means [Q7]."

**What we do not promise**
"No guaranteed interviews, job offers, recruiter replies, impressions or follower numbers. No bots, no automated engagement, no fake accounts, and no sharing of passwords."

## 7. Proposed page order

Hero (with a plain statement of what you get) → three packages with the comparison table and revision limits → what Executive adds (personal branding, connection building, content, timeline) → how it works → examples (CV and LinkedIn, labelled illustrative) → about Kaeto → what we do not promise → FAQ → final call to action.

## 8. After you answer

I will rebuild the page from `drafts/services-rebuild.html`, update the Payhip settings to three products, run the checks from your brief (prices, deliverables, revision limits, Executive timeline, 12-post wording, 500+ wording, links, mobile and dark mode), and publish through a pull request for your approval.
