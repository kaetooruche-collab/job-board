# How to fire Fable on Yireh Careers (operating manual)

Written 16 Nov 2026. Read this once, tick the checklist, then fire.

## What the shot is
One long run of Claude Fable 5.2 that reads everything, researches the web, and writes a diagnosis and a plan: `drafts/fable/output/00-memo.md` to `09-open-questions.md`. It changes nothing on the live site. The brief is `brief.md`; your answers go in `kt-inputs.md`.

Why a plan and not the whole revamp in one go: Fable's judgment is the valuable part. Typing code is not. A revamp built in one run is one giant change nobody can review, and one wrong assumption spoils all of it. So: Fable plans, a cheaper model builds each ticket in a small reviewed change, and (optionally) Fable checks the result afterwards.

## What it costs (an estimate, not a quote)
List prices in the model reference I read on 16 Nov: Fable 5.2 is $8 per million input tokens and $40 per million output tokens (thinking counts as output). The context pack is about 111,000 tokens, so reading it once is under $1. A long research run might write 150,000 to 400,000 tokens including thinking, which is about $6 to $16, plus the web pages it reads. Expect roughly $5 to $40 in total. It is unlikely to exceed $100 unless it loops. If you run it inside a subscription, usage limits apply instead of per-token billing; I do not know your plan. Check the price table again before you fire; prices change.

## Settings
- Model: Claude Fable 5.2. Effort: `high`. Do not use `max` (it is for measuring the model's ceiling). Thinking is always on and cannot be turned off.
- Do not add lines such as "think less" or "answer quickly": they do not work on this model.
- Let it run. Single turns on hard tasks can take many minutes.

## Before you fire (tick all)
- [ ] You answered `kt-inputs.md` sections 1 to 6 (or accepted the defaults on purpose).
- [ ] Regenerate the context pack today: `python3 scripts/build_fable_context.py` (numbers go stale within days).
- [ ] The repository is on `main`, up to date, and the tests pass (`python3 -m unittest discover -s tests`).
- [ ] You decided where to run it (default: Claude Code on the web, in this repository, with Fable selected).
- [ ] High value, optional: 5 to 10 real comments from your Facebook groups, your order and free-check counts, and the results of five quick "what is this site?" conversations (three questions: what does it do, who is it for, how is it different from LinkedIn or Indeed). Without them, Fable has to label the audience as an assumption.

## How to fire
In a new Claude Code session on this repository, choose Fable and send exactly this:

> Read `drafts/fable/brief.md` and follow it. The inputs are in `drafts/fable/kt-inputs.md` and `drafts/fable/inputs/`. Write only under `drafts/fable/output/`.

Leave permissions so it can read everything and write only in `drafts/fable/output/`. Do not give it permission to commit, push, send or change accounts; the brief says it must not, and the permissions should agree.

## When it finishes: how to check it (20 minutes)
1. Run `git status`. Only files under `drafts/fable/output/` should be new. Anything else changed is a problem: stop and tell Claude.
2. Read `00-memo.md` first. If you cannot say what the five bets are after reading it, the memo failed; ask for a rewrite.
3. Pick 10 claims at random from `01-findings.md` marked Established. Open the source of each. Report how many were right (for example "9 of 10"). Fewer than 9 means do not act on the plan yet.
4. Read `09-open-questions.md`. Answer what only you can answer.
5. Ask Claude to turn `08-tickets.md` into pull requests one at a time, with tests, using an everyday model.

## If it goes wrong
- It stopped early or gave only a summary: reply "Finish every deliverable the brief lists." Do not restart; the work is saved in the output folder.
- Numbers you cannot trace to a source: reject those findings.
- It recommends something the project rules forbid (scraping a site whose terms forbid it, a listing paywall): that is a finding for you to decide, not an instruction to follow.
- It touched files outside the output folder: stop and tell Claude before doing anything else.
