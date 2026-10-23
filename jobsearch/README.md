# Pharmacy job search system (KT's personal search; not part of the public job board)

This folder is private: it is excluded from the website (`.vercelignore`). It does not use the job board's classifier. It finds jobs by reading them.

## The goal
50 real, open jobs posted within the last 7 days, for a 2024 MPharm graduate (not a licensed pharmacist), in pharmacy and pharmacy-adjacent work: pharmacy roles, healthcare operations, clinical strategy, implementation, medical information, drug safety (pharmacovigilance), regulatory affairs, clinical operations, product and customer success. A job is only listed if its posting says it is open, its date is inside the last 7 days, and its description has been read.

## The files
| File | What it is |
|---|---|
| `pharmacy-jobs.xlsx` | The working list: one row per job, with requirements, eligibility quotes, what your MPharm maps to, gaps, link, contact email (only if published) and check-off columns. Sheets: Active list, Ruled out (and why), Dropped at recheck, How to use. |
| `pharmacy-jobs.md` / `.csv` | The same list in plain formats. |
| `raw/*.json` | The researched records, one file per role family (the source of truth). |
| `AGENT_BRIEF.md` | The research rules every search follows. |
| `find_jobs.py`, `discover_boards.py` | Pull openings from the public job-board feeds of health and pharma employers. |
| `verify_and_build.py` | Merges the records, re-checks each link, removes anything older than 7 days or closed, rebuilds the list. |
| `templates/` | CV, cover letter and application-email templates and the tailoring rules. |
| `private/` | Your master CV and the documents made for each job (kept in the private repo, never deployed). |

## The steps for every job (the check-off columns)
1. **Read the posting** in full (not the title). Note what it asks the person to do.
2. **Eligibility**: residency, work authorisation, language, licence. If it says you must live in a country you do not, mark No and move on.
3. **Map it**: list the 5 to 8 requirements, and for each one name the real evidence from your CV (a placement, a project, a module, a dissertation, a tool). No evidence means a gap, written down honestly.
4. **CV tailored**: same truthful CV, re-ordered and re-worded to echo the posting's own words where they are true (`templates/cv-tailoring-rules.md`).
5. **Cover letter** if the posting asks for one or the role is competitive (`templates/cover-letter-template.md`).
6. **Contact**: use the email the posting or the company's careers page publishes. If none, apply through the portal. We never guess or scrape personal emails.
7. **Apply**, record the date, **follow up** after 7 to 10 days if there is a contact, and note the result.

## Keeping it going
- Weekly refresh: `python3 jobsearch/find_jobs.py` for the employer feeds, new web searches by role family (same rules as `AGENT_BRIEF.md`), then `python3 jobsearch/verify_and_build.py`. Expired jobs drop out, new ones are added.
- A recurring scheduled Claude task could do this every week. It needs KT's approval (it uses search and writes to this repo).

## Rules
- Never invent experience, results or qualifications in any document. Every claim must come from your own CV or answers.
- Do not scrape LinkedIn, Indeed, Glassdoor or similar sites (their terms forbid it). You search those by hand and paste links in; we then read and check them the same way.
- Some employers (for example large pharma on Workday) block automatic checks; those links are marked as verified by opening the page, not by script.
