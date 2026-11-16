# Should Yireh Careers exist? An evidence review (16 Nov 2026)

Written for KT. One file, as asked. It answers your questions and the ones you did not ask, using measured data from our own systems and sources read today.

**Evidence labels.** *Established*: I measured it or read the source first-hand today (source given). *Reported*: a source says so; I did not verify it. *Inference*: my reasoning from the evidence. *Assumption*: nothing supports it yet.

**Limits.** Traffic is so small that every rate below is unstable. I could not read your Facebook groups, your WhatsApp chats or Google Search Console. I do not know your orders, your income needs or your hours. Section 7 lists what only you know.

---

## 1. The answer in one paragraph

**Do not abandon it, and do not keep building it.** In its current form Yireh Careers is not a working business: 410 page views, 17 apply clicks, 0 sign-ups, 0 free-check forms and 0 recorded orders in about five weeks (*Established*). The feature we believed was unique is offered free, at over 100 times our size, by Himalayas and by Remote Rocketship (*Established*, section 3, Q7). The plan to earn money from $29 to $149 CV services has weak evidence behind it and poor pay per hour (Q10 to Q12). But the problem is real and documented, the site costs almost nothing to keep alive, and demand for your service can be tested in 30 days without writing more code. So: **freeze development, put the board in maintenance mode, and run one cheap demand test with a stop rule (section 5).** If the test fails, stop and move your time elsewhere without regret.

## 2. The facts today (*Established*, 16 Nov 2026)

| What | Number | Source |
|---|---|---|
| Page views, all time / last 7 days | 410 / 101 | GoatCounter snapshot 10 Nov |
| Home page views, all time / last 7 days | 211 / 30 | same |
| Apply clicks, all time | 17 | same |
| WhatsApp clicks about a CV or free check | 7 | same |
| Email sign-ups, free-check forms, order forms | 0, 0, 0 | same |
| Email subscribers | 3, all your own contacts | Brevo |
| Digests sent since the rebrand | 1 (30 Oct): 3 delivered, 0 clicks | Brevo |
| Weekly email routine | Failed 10 Nov ("access denied"); nothing sent 3 or 10 Nov | scheduled-task record |
| Listings / companies | 1,006 / 161 | `jobs.json` |
| Open worldwide / name countries / unclear | 12 / 724 / 249 | `jobs.json` |
| Apply links blocked on a given refresh | 4% to 22% | `data/metrics.json` history |
| Work shipped | 62 merged changes since 12 Oct, 214 automated tests, 26 decision records | repository |

## 3. Your questions, answered

### Q1. Why does the Yireh Careers job board exist?
By its own brief it exists for two reasons. First, to fix what you lived through: applying to over 200 remote jobs and finding the rules for who can apply buried in the posting. Second, as the brief states, "Revenue comes from KT's paid CV and LinkedIn services… The board earns trust and traffic" (`CLAUDE.md`). So the honest description is: **a free tool that is also the marketing channel for a paid service.**

### Q2. What is its main job?
One sentence: *tell me which remote jobs I can apply to from where I live, and that they are real.* The problem is real. Job Badger read 993 remote listings (16 Sept 2026): 92% named a place, 38% were US-only, and a person in Nigeria could apply to 11% (*Established*, read 1 Nov). WorkinVirtual found 11.6% of 112 listings worldwide (*Established*). People describe it in their own words: "Most of the ones I've applied to have ended up being fake or actually hybrid" (`drafts/marketing/audience-research-and-icp.md`).

### Q3. Does it do that job well today?
Partly. I tested it today by pulling 20 random listings and comparing each card with the employer's own posting data.

- Posting date correct: **20 of 20.**
- Fully correct card: **15 of 20.**
- **Wrong on the core claim, 2 of 20:** two Brex roles are shown as remote, but the posting says "This role will be based in our San Francisco office… We currently require a minimum of three coordinated days in the office per week." Our classifier was fooled by the line "up to four weeks per year of fully remote work". **All 15 Brex listings on the board carry this error.** It is not fixed yet.
- Eligibility understated, 2 of 20: Mercury and Lyra Health cards say "Eligibility unclear" although the location field says United States (and Canada).
- Debatable, 1 of 20: a ZipRecruiter role whose posting opens "We offer a hybrid work environment" is shown as "Remote: not confirmed".

With 2 errors in 20, the true error rate is somewhere between about 3% and 30%; the sample is too small to say more (*Inference*). A board whose promise is "these are remote" cannot show hybrid jobs as remote. This is the first thing to fix (section 4).

### Q4. Does it work perfectly, and will it ever?
No, and no. No job board is ever perfect: employers write vague postings (249 of ours do not say who can apply), fill roles before removing them, and block automated checks (4% to 22% of our link checks). The right goal is not perfection. It is **"never wrong on remote, and honest when unsure"**, which the board mostly does and competitors rarely state.

### Q5. What does it need to get as close as possible?
1. Fix the hybrid-as-remote error, add those postings to the regression tests, and add a rule that blocks "N days in the office" (*the project's own quality rule*).
2. Run the 15-listing spot check every week and publish the score.
3. Reduce the link-check blocking (it is throttling from GitHub's servers; a slower checker or a different checking route).
4. A custom domain and one page per job or per country, so search engines can find anything (Q9).
None of these is worth doing until the demand test in section 5 passes, except item 1, which is a truth problem on a live site.

### Q6. Why would people tell their friends about it?
People pass on things that make them useful to a friend. Nielsen's 2021 survey (40,000 people, 56 countries) found 88% trust recommendations from people they know, more than any other channel (*Reported by Nielsen*). The shareable moment for us would be: "this shows the remote jobs you can apply to **from our country**." Today there is nothing to share except the home page: no country page, no job page, no saved search. And there is no sign of sharing yet: 5 visits from WhatsApp all time (*Established*). **So far, they don't.**

### Q7. Is our main feature actually unique?
**No. This is the most important finding in this file.** Read today (*Established*):
- **Himalayas** lists 120,415 remote jobs, free. Every listing carries a label such as "United States only", "Nigeria only" or "AL, AD + 74 more". It has a page per country ("Remote jobs in Nigeria": 2,190 jobs), a "work from anywhere" page, a time-zone filter, and says over 1,000,000 remote workers use it.
- **Remote Rocketship**: "Pulled straight from company career pages", "You can filter by country and time zone so you only see roles you can actually be hired for", "Loved by 10,000+ remote workers". It charges job seekers a subscription (*Reported*, petecodes.io: $18 a month).
- Job Badger, WorkinVirtual and Peepuu (Nigeria) also sell the same idea.

Our earlier strategy paper called eligibility "the one thing no competitor does as a primary feature". That was wrong, or is no longer true. What we still do differently is narrower: we quote the employer's wording, say "unclear" openly, and exclude hybrid roles. Those are quality points, not a reason for a stranger to switch from a board with 120 times more jobs.

### Q8. Who is the customer, and can they pay?
The people hurt most by location limits live outside the US and UK. They are also the people for whom our prices are heaviest. World Bank income per person, 2024 (*Established*, World Bank API, read today):

| Country | Income per person per month (US$) | Essential ($29) as a share of a month |
|---|---|---|
| Nigeria | 143 | 20% |
| Pakistan | 119 | 24% |
| Kenya | 173 | 17% |
| India | 213 | 14% |
| Philippines | 373 | 8% |
| Türkiye | 1,119 | 2.6% |
| United Kingdom | 4,110 | 0.7% |
| United States | 6,909 | 0.4% |

Averages hide a professional class that earns far more, so this does not prove nobody can pay (*Inference*). But the group with the pain and the group with the money overlap least. US and UK readers can pay easily, yet they need the eligibility feature least, and a US survey found only 3.7% of adults used a professional résumé writer (Novoresume 2026, *Reported*, a vendor).

### Q9. Can anyone find the site?
Barely. A web search for `site:yirehcareers.vercel.app` returned no results today (*Established* for that search index; Google Search Console would confirm it, and only you can open it). Three structural reasons (*Inference*): the whole board is one page that loads its jobs with a script, so there are no job or country pages to index; it sits on a free shared `vercel.app` address, which users report Google treats with caution (*Reported*, forum posts); and the three communities we planned to post in forbid self-promotion (r/RemoteJobs, r/jobsearch, r/remotework; *Established* 31 Oct). Your only working channel is Facebook groups, where you told me most posts are not approved.

### Q10. Does Yireh Careers exist to sell CV and LinkedIn services?
Yes. That is the business model in the brief. The board itself earns nothing and is not designed to.

### Q11. Is that a good business model?
The evidence says it is weak as designed.
- **Boards that earn money are paid by employers or by subscriptions, not by CV writing.** Remote OK charges employers from $299 a post and reports about $25,000 a month; We Work Remotely charges $299; Remote Rocketship charges seekers a subscription and reports about $6,500 a month; OnlineJobs.ph charges employers $69 to $99 a month (*Reported*, gaps.com and petecodes.io). I found no board funded mainly by CV services.
- **CV writing is crowded and cheap at the low end.** Fiverr's own guide lists writers "From $15", "From $20", "From $30" (*Established*, fiverr.com, read today). A market summary says barriers to entry are "near zero" and AI is "eroding the entry-level segment" (*Reported*, ideacrystal.com).
- **Your pay per hour is low.** If a CV takes about 4 hours (*Reported* industry figure; your real time is unknown), Essential pays about $7 an hour. US independent writers charge $100 to $400 per résumé (*Reported*).
- **The arithmetic.** To earn $1,000 a month at an average order of $45 you need about 22 orders a month. We see 3.3 WhatsApp clicks per 100 home views. If one chat in ten buys (*Assumption*), you need about 6,700 home views a month. You have about 130. That is a 50-fold gap, and then about 88 hours of writing.

### Q12. Why would this work?
- The problem is real and measured (Q2).
- Visitors behave as if they want it: 18 uses of the country filter, 17 apply clicks and 7 CV-related WhatsApp clicks from 211 home views (*Established*). Small, but not nothing.
- It costs almost nothing to run: every tool is on a free plan and the refresh is automatic.
- You can do the service yourself, and you told me earlier that one free check turned into a customer (a single case).
- The trust work is done: tests, a checker, honest labels, a real founder story.

### Q13. Why would this fail?
CB Insights studied 101 startup post-mortems: 42% failed because there was "no market need", 29% ran out of cash, 17% lacked a business model (*Established*, CB Insights report PDF). Our risks map onto those:
1. **No distribution.** 30 home views a week and no working channel (Q9).
2. **No real difference** from much larger free boards (Q7).
3. **The payer problem** (Q8) and thin margins (Q11).
4. **One person.** Every order is your hours; the Tuesday email has already silently failed for two weeks.
5. **Accuracy.** One classifier error put 15 hybrid jobs on a "remote" board (Q3).
6. **Building instead of selling.** 62 changes shipped; one person outside your contacts has yet to give us an email address.

### Q14. Was it worth the energy and resources put in so far?
Judged by results, not yet: five weeks of work, 62 shipped changes, this session's computing alone is metered at about $295 (*Established*, session record; it may be covered by your plan), and no customer from the site. Judged by what you now hold, partly: a working pipeline, a classifier, an email system and a clear picture of the market. But **the past spend should not decide anything.** Arkes and Blumer (1985) showed that people keep investing because of what they have already spent, and that this leads to worse decisions (*Reported*, the standard reference on sunk cost). The only question that counts is the next 30 days of your time.

### Q15. Why not abandon it and spend the resources on a different project?
That is a legitimate option, and here is the fair case for each side.
- **For leaving it:** the model is unproven, the gap is 50-fold, and your account also runs a daily search for freelance email-marketing work with payment inside 7 to 30 days, which suggests near-term income matters to you (*Inference* from your own scheduled task). Freelance work pays sooner than an audience can be built.
- **For keeping it alive:** it costs nothing to leave running, and one cheap test can settle the question. Quitting before that test means never knowing.
- **My recommendation:** do neither extreme. Cap this at about 5 hours a week for 30 days, all of it on the test in section 5, and put the rest of your time where income is nearer. Let the stop rule decide.

### Q16. Should the CV service be tested without the board?
Yes. This is the cheapest strong test available. The service does not need the board to be sold. Offer it directly to people you can already reach. If strangers will not pay you $29 to $49 when asked plainly, a bigger board will not change that. If they will, you have a business whether or not the board grows.

### Q17. Why did 211 home visits produce zero sign-ups?
Unknown. Candidate reasons (*Inference*): the visitors were few and partly ourselves; the weekly email offers nothing a visitor cannot get by returning; the sign-up sits below the listings. The fix is not another redesign. Ask five real visitors three questions: what does this site do, who is it for, would you come back and why?

### Q18. Is scraping 100+ job sites the answer?
No. It adds listings, and listings are not what is missing; visitors and buyers are. It also multiplies the accuracy and blocking problems above, and many of the sites forbid it.

### Q19. Is there a better way to earn from the same assets?
Possibly, each *Inference* and each needing its own test: charge for higher-value work (a full application package for one specific job at $99 or more, for people with US or UK incomes); sell to a narrow group you understand well (for example pharmacists or healthcare professionals moving to remote work, where you have real knowledge); or use the pipeline as a portfolio piece to win paid marketing and automation work. Employer-paid listings and seeker subscriptions need traffic we do not have.

### Q20. What would make this worth scaling later?
Evidence, in this order: strangers pay; they come from a channel we can repeat; they come back or refer someone. Only then do a domain, country pages and more sources make sense.

## 4. What stays, what goes

**Stays (cheap, true, or needed for the test):** the live site in maintenance mode; the 6-hourly refresh and the site monitor; the honest labels and the verify page; the services page and the free CV check; WhatsApp as the sales channel; the weekly spot check. **Fix now:** the Brex hybrid error, and re-authorise the Tuesday email routine or pause it.

**Goes, or is frozen until the test passes:** the 100-site scraping idea; the full "revamp"; more redesigns and copy passes; country editions of the email; card checkout; new sources; the Executive ($149) and LinkedIn Growth ($99 a month) offers as lead offers, since nobody has asked for them (keep them on the page, stop working on them); any further automation.

## 5. The 30-day test and the stop rule

Until 16 Dec 2026, spend your Yireh hours only on these.
1. **Sell the service directly** (Q16). Offer the free CV check and the $29 to $49 packages to at least 30 real people: your network, the groups that accept you, people who message you. Log every reply.
2. **Talk to 10 job seekers** (5 minutes each): what did they last pay for CV help, and what would make them pay?
3. **Post the weekly roles** in the groups that allow it, with tagged links.

**Stop rule (my judgment, adjust it now, not later):**
- **Continue** if by 16 Dec at least 3 strangers have paid, or at least 10 people asked for a free check.
- **Stop building** if neither happens. Leave the site running untouched, or take it down, and move your time to nearer income.
- **Rethink the offer** (Q19) if people want help but will not pay these prices for it.

## 6. What this means for the planned Fable run

You switched this session to Fable 5.2, so this review is that model's work. The brief in `drafts/fable/` asks for a full revamp plan. On this evidence a revamp is premature: it would improve a product whose demand is unproven. Hold that brief until the 30-day test passes.

## 7. What only you know (and it changes the answer)

1. Have you had any paid order, and from where?
2. How many free CV checks or WhatsApp enquiries so far, and what did people ask?
3. How long does one CV really take you?
4. How much income do you need, and by when?
5. Which Facebook groups accept your posts, and how big are they?
6. What does Google Search Console show for the site?

## 8. Sources

Own data: `jobs.json`, `data/metrics.json`, `data/link_state.json`, `drafts/analytics/GC-2026-11-10.md`, Brevo account (campaign 105, list 11), scheduled-task record, 20-listing check against the Greenhouse, Ashby and Lever public feeds (16 Nov).
Read today: himalayas.app/jobs and himalayas.app/jobs/countries/nigeria; remoterocketship.com; fiverr.com/resources/guides/writing-and-copywriting/resume-service-cost; World Bank indicator NY.GNP.PCAP.CD (2024); CB Insights, "The Top 20 Reasons Startups Fail" (101 post-mortems); gaps.com/job-boards and petecodes.io/job-boards-guide (reported revenues); ideacrystal.com (résumé-service economics); Nielsen, Trust in Advertising 2021; Arkes and Blumer (1985), "The psychology of sunk cost".
Read earlier and still relied on: job-badger.com/guides/remote-jobs-report; workinvirtual.com/research/remote-job-eligibility-index-2026; subreddit rules (31 Oct); `drafts/decisions/` in this repository.
