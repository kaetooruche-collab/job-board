# Research brief for one role family (read fully before starting)

## Who the list is for
KT is a pharmacy graduate: MPharm, graduated 2024. NOT a registered/licensed pharmacist anywhere (so roles that legally require a pharmacist licence are out unless the posting says an unlicensed graduate can apply). Early career. KT wants jobs that can be done remotely or that accept applicants outside the employer's country, and also pharmacy-adjacent roles beyond traditional pharmacy: healthcare operations, clinical strategy, implementation, medical information, drug safety (pharmacovigilance), regulatory affairs, product, customer success, clinical operations, and similar.
Do not rule a job out because the TITLE is unfamiliar. Open the posting and read what it asks the person to do and what it requires.

## What to produce
A JSON file at the path given in your task: a list of job records (schema below). Aim for 12-18 records that are real, open and posted within the last 7 days (today is 18 Oct 2026, so posted on or after 11 Oct 2026). Quality over quantity: every record must be verified by opening the posting page.

## Hard rules
1. Open every posting page yourself (firecrawl_scrape with maxAge 0, or for Greenhouse/Lever/Ashby use the public JSON API with curl/requests). Never fill a field from a search snippet alone.
2. Posted date must come from the posting page or the employer's ATS data, not from guesswork. Quote the evidence in date_evidence. If a page shows only "3 days ago", compute the date from today and say so. If you cannot establish a date within the last 7 days, do not include the job.
3. The page must still be open: an Apply button or form, and none of: "no longer accepting", "expired", "position filled", "closed". Set verified_open accordingly; do not include jobs that are closed.
4. Prefer the employer's own careers/ATS page as `url`. Aggregator pages (Himalayas, DailyRemote, RemoteRocketship, Ladders and similar) are fine for discovery, but find the employer's own posting and use that. If you can only find an aggregator copy, set url_kind to "aggregator".
5. Do NOT open or scrape LinkedIn, Indeed, Glassdoor, ZipRecruiter or similar sites (their terms forbid it). KT searches those by hand.
6. Never invent anything. Pay only if the posting states it. Requirements and keywords must come from the posting text. Contact emails only if they are published on the posting or on the company's own careers/contact page; give the page URL in contact_email_source. Never guess an email address. If there is none, use null and say "apply via the portal".
7. Read the WHOLE description. Record work authorisation, residency, language and licence rules exactly as the posting words them (short quotes). Several postings say "remote" but only for residents of one country; say so.
8. Rate fit honestly for an unlicensed 2024 MPharm graduate with little or no industry experience: A = meets the stated minimum (or the posting says a pharmacy/life-science degree with 0-2 years is enough); B = stretch, one clear gap (for example 2-3 years asked, or a language, or a country restriction that may or may not apply); C = not realistic (licence required, 5+ years, PhD/MD, senior or director level). Include A and B in the main list. Put C records in the same file with fit "C" and a one-line reason (a handful at most), so KT sees what was ruled out and why.
9. Do not use the job board's classifier or any scripts in /home/user/job-board/scripts. Use your own reading.
10. If the same job is posted in several countries, make one record per distinct posting URL only if the location differs in a way that matters for KT; otherwise one record.
11. Keep requests gentle: no more than about 2 requests per second; do not hammer any site.

## Record schema (one JSON object per job)
{
 "id": "<family-slug>-<n>",
 "role_family": "",
 "title": "", "company": "",
 "url": "employer or ATS page", "url_kind": "employer|ats|aggregator",
 "found_via": "how you found it",
 "posted_date": "YYYY-MM-DD", "date_evidence": "quote or field name",
 "location": "as stated", "work_mode": "remote|home-based|hybrid|on-site|unclear",
 "eligibility_stated": "short quotes on residency, work authorisation, languages, licence",
 "open_to_non_residents": "yes|no|unclear",
 "employment_type": "", "salary_stated": null,
 "min_education": "", "min_experience": "", "licence_required": "none|<which licence>", "languages": "",
 "key_requirements": ["up to 8, paraphrased from the posting"],
 "key_duties": ["up to 5"],
 "keywords_for_cv": ["8-12 exact phrases from the posting that a CV should echo, only where KT can honestly claim them"],
 "fit": "A|B|C", "fit_reason": "1-2 sentences",
 "mpharm_overlap": "which parts of an MPharm map onto this role",
 "gaps": "what is missing",
 "how_to_apply": "portal|email|other", "apply_url": "",
 "docs_required": "CV, cover letter, other, as stated",
 "contact_email": null, "contact_email_source": null,
 "verified_open": true
}
Return a short summary at the end: how many records, how many A/B/C, which searches you used, and anything you could not verify.
