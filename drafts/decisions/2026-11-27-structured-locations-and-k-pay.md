# Job location lists, conflicts and "$105k" pay (27 Nov 2026)

Status: built on branch `claude/lucid-lovelace-3ribsh`, tests pass, **not merged**: needs KT's yes.
Reported by the social agency (`social/board-issues.md`, branch `claude/social-agency`), confirmed against the employers' public feeds on 27 Nov 2026.

## What was wrong (established, checked in the live feeds)
1. **Recruitee:** every remote offer on all 6 boards has location text "Remote job"; the places are only in `locations[]`. Trafilea's Argentina/Brazil/Chile roles showed **Worldwide**.
2. **Body text beat the job's own location list.** Airwallex listed "UK - Manchester; UK - Birmingham", the body said "This role is remote in the EMEA region", the card said **EMEA**. When the system flagged a job remote, company wording was added to the list (Ajax Systems UK sales roles labelled "..., Ukraine, Turkey, Vietnam" from "factories ... located in Ukraine").
3. **Pay written as "$105k–$122k"** was not read (the pattern only knew "105,000"). Customer.io cards said "Not stated".

## What changed
- `scripts/fetch_jobs.py`: Recruitee location built from `locations[]` (a region name such as "LATAM" or "Worldwide" kept as written; otherwise the country). Every source now keeps its raw location list for the QA check.
- `scripts/classify.py`: when the location list names specific places and its own text does not say remote, and the body names places outside the list, the card shows no eligibility claim ("Location not specified", with the employer's location shown) and both quotes are kept. Not a conflict: a body that stays inside the list, or one that deliberately widens it and so explains it ("anywhere in Europe", "with a preference for Prague"). A title saying "Worldwide" against a country list is also a conflict (Tether).
- `scripts/pay_text.py`: reads "$105k" figures (2–3 digits before k, so "$1.5k" stipends never count).
- `scripts/qa_checks.py`: **BLOCK** a Worldwide card whose location list names places; **WARN** a label wider than a one-country, non-remote list (WARN because most hits on the live feed were correct widenings); the pay WARN now sees the k form.
- 9 regression fixtures with the real posting text (`tests/fixtures/regressions.json`); unit tests for the QA rules and the Recruitee reader.

## Old versus new, same live data (27 Nov 2026, 42,698 postings, 2,000 published each run)
- 57 cards change their location label; 16 cards gain stated pay (all were "Not stated"; each figure checked to be a salary line).
- Recruitee (36): 4 Trafilea Worldwide → Argentina / Argentina, Brazil / LATAM ...; 32 "not specified" → the employer's listed countries or region.
- Other systems (21) now show no eligibility claim. By reading each posting: **16 had a wrong label** (Airwallex, Ajax ×4, Glitch ×2, Fullstory ×2, RWS, Assembled, Mutt Data, Andela, ClickHouse Singapore, Echodyne, Fastly*); **5 had a correct label that is now hidden** (Veeva ×3 "Europe", Spotify "Americas", Atomic Invest "LATAM"). The rule chooses saying less over saying something wrong.
- Worldwide cards: 36 → 32. QA blocks on the new run: no new ones.

\*Fastly is the weak case: the location is one office tag (San Francisco) while the body says "open to candidates residing in ... North America" and Fastly's own metadata says Region NAMER. The consistent rule calls it a conflict. Option: treat a single Greenhouse office as an office. Not done without KT.

## Open (hypothesis, not checked)
- **Tether** posts one role per country (one location each). Titles that say "Worldwide" are now unclear; titles that don't now read "<country> only". Whether Tether really restricts those is not verified.
- Label tidying: "South America, Latin America, Brazil, Chile" is accurate but wordy.
- The "Location not specified" pill text ("the employer doesn't say") is not exactly right for a conflict; the copy rule applies before changing it.
