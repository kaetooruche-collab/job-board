---
name: classify-job-listing
description: Decide whether a job listing is genuinely remote, hybrid or on-site, who is eligible to apply, and what experience level it needs. Use when reviewing listings in data/review_queue.json, when a listing looks mislabelled on the job board, or when changing scripts/classify.py.
---

# Classify a job listing

The automated classifier is `scripts/classify.py` (run `python3 -I -m unittest discover -s tests`). This skill is for judging the borderline cases it flags, and for improving it.

## 1. Read the whole listing
Title, location field, any structured work-arrangement field, the full description, duties, hours, residency rules, office attendance, application requirements. Never decide from one keyword.

## 2. Work arrangement (pick one)
- **Fully remote**: no routine office attendance. May still limit countries or time zones.
- **Remote, geographic restrictions**: remote, but applicants must live in or be authorised to work in named places ("Remote, United States" is remote, not on-site).
- **Remote, unclear**: marketed as remote or credible signs of remote, but the listing does not settle full-remote vs hybrid. Publish with a visible "not confirmed" label; say what is unresolved.
- **Hybrid**: required recurring office attendance ("three days a week", "every Monday").
- **On-site**: mainly at a physical workplace, even if "flexible" or "occasional remote" is mentioned.

Context rules that the code encodes (keep them when editing):
- "Remote opportunities available" or "some roles may be remote" in a company intro does not prove this vacancy is remote.
- "Occasional" / quarterly / annual / retreat / ad-hoc meetups is not hybrid; record it as occasional and flag "confirm how often".
- "Remote after training": ask whether training is on-site and for how long; treat as unclear.
- "Must live within N miles of the office": remote claim needs interpretation; treat as unclear.
- Negations flip meaning ("never required to come to the office", "not hybrid").
- "Hybrid" in tech phrases (hybrid cloud, hybrid analyzers) or "in person" in communication-skill lists is not a work arrangement.
- On-site with customers (sales calls, client visits) is travel, not office attendance.
- A structured field that says hybrid beats company-level "we are a distributed company" wording.
- When evidence conflicts (title says remote, description says hybrid), flag it for review. Do not silently pick one.

## 3. Geographic eligibility
Worldwide / named country / named countries / region / time zone / unclear. Remote does not mean worldwide. Keep the employer's wording. Note work-authorisation and contractor-versus-employee limits. A city in the location field without "remote" is not proof of where remote applicants may live.

## 4. Experience level
Internship, entry, junior, mid, senior, leadership. Decide from the years and skills the description requires; "assistant" does not mean entry-level if it asks for five years. Note when equivalent experience is accepted. Manager titles that do not manage people are individual contributors.

## 5. Never
Invent pay, eligibility, employer details or requirements. Publish a listing as fully remote on insufficient evidence.

## 6. Improve the classifier
Add a failing test in `tests/test_classify.py` that reproduces the real wording, then change `scripts/classify.py`, then run all tests and re-check a sample of real listings (fetch from a few employer boards and read the evidence it prints).
