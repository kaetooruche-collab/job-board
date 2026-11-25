# Job cards in the reader's words; only confirmed-remote jobs (25 Nov 2026)

KT, 25 Nov 2026, after reading the live board with "Early career" and "Cyprus" chosen: "You can't talk to users like this ... Eligibility unclear can't keep appearing, or we will delete it altogether ... 'Remote: not confirmed' ... that's not what people want."

## 1. What was measured (live board, 1,197 listings)
- 293 cards (24%) said "Eligibility unclear" and 125 said "Remote: not confirmed".
- 24 different machine-written notes reached readers, for example "The location field names a place but does not say the role is remote there; confirm whether applicants elsewhere are accepted." (73 cards) and "Occasional office or in-person attendance is mentioned; confirm how often." (206).
- The country filter showed every job that does not say where it hires under every country (`matchesCountry` ended in `return true`), so "Cyprus" listed jobs based in India and Portugal. That broke the headline promise.
- Four labelling bugs sat behind many of those cards, found by reading them (section 3).

## 2. How a leading board words it (read 25 Nov 2026)
We Work Remotely's customer-support category: every card states a place in plain words: "Anywhere in the World" (58), "🇺🇸 United States of America" (8), "Asia Only" (8), "North America Only" (2), "🇨🇦 Canada", "🇮🇳 India". No card carries a negative label. (Himalayas could not be read: its cards load with JavaScript and the research tool's credits ran out.)

## 3. Accuracy first: the bugs behind the cards (fixed, with regression fixtures)
- "including but not limited to office location" was read as "no office" (Accenture Federal Services: 129 on-site postings shown as remote).
- "50% Telecommuting permitted" and "hybrid ... up to 50%" were not read as hybrid (Stripe, Compeer).
- A company line ("we hire globally", "no borders or HQ") overruled the job's own location field and produced "unclear" (Certa, Oyster, GitLab, Lyra, Natera and others). Now the location field wins unless the worldwide line talks about the role, candidates or "you".
- "Analyst II", "Engineer 2", "SDE-2", "Senior Sales Associate", "Lead Tax Associate" were labelled junior or entry (10 now mid-level).
Old versus new on the 13,007 postings of the last 30 days in all feeds: 148 publish decisions change (all to excluded, each checked: on-site, hybrid, in-person internships), 134 "unclear" labels become a real answer, 10 levels move to mid. 0 errors.

## 4. Options considered for jobs that do not say where you can apply from
- (a) Keep "Eligibility unclear". Rejected: negative, vague, and on a quarter of cards.
- (b) Hide them entirely. Rejected: the jobs are real and remote; hiding them hides real options, and the headline says we say when it is not clear.
- (c) **Chosen:** a quiet grey pill "Location not specified", shown only when no country is chosen. With a country chosen, only jobs open to that country (named, its region, or worldwide) are shown, with a link "Show N more that don't say where you can apply from". Accurate (it states a fact about the posting, not a judgement), and the reader decides.

## 5. What changed for the reader
- Only jobs whose posting confirms they are remote are published (`PUBLISH_REMOTE_UNCLEAR = False` in `scripts/fetch_jobs.py`; held jobs are logged in `data/removed.log`). The "Remote: not confirmed" pill and the "Confirmed remote only" box are gone.
- Under the pills, at most two plain facts: "May need occasional office visits", "Starts with in-person onboarding or training", "Not open to applicants in: ...", "You'll need the right to work there already". Nothing else from the classifier's notes is shown.
- "Why this label?" became "Where this comes from": the employer's location as written, and up to two quotes from the posting.
- The post kit and WhatsApp post say "not specified, check the posting" instead of "Eligibility unclear".
- Wording lives in `card-text.js`; `tests/node/card-text.test.js` fails if a card line uses machine words ("location field", "the listing", "unclear", "not confirmed" and others).
