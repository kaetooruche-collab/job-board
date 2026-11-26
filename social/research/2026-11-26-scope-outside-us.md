# Addendum: if the audience is "everyone outside the US" (26 Nov 2026)

**Status:** KT is weighing two scopes: "everyone" or "people outside the US" (message from the job-board session, 26 Nov). Phase 0 was briefed on Africa, South Asia and South-East Asia. Until KT decides, the calendar keeps that brief; this note says what changes under the wider scope. Labels as in the other research notes.

## 1. Where our supply is (measured on the live feed, 26 Nov 2026, the site's own "open to" rule) [Established]
| Region | Jobs open to (example countries) |
|---|---|
| North America outside the US | Canada 193 |
| UK and Ireland | United Kingdom 146, Ireland 75 |
| EU | Germany 84, Spain 71, Poland 69, Netherlands 68, France 67 |
| South Asia | India 78, Pakistan 28, Bangladesh 26 |
| Latin America | Mexico 68, Brazil 60, Argentina 57, Colombia 55 |
| Africa | South Africa 38, Egypt 34, Nigeria 33, Kenya 33, Ghana 33 |
| South-East Asia | Philippines 38, Vietnam 27, Indonesia 26, Malaysia 26 |
| Worldwide (open to all of the above) | 19 |
| United States, for comparison | 1,122 of 1,759 |

Supply is strongest for Canada and the UK, then the EU, India and Latin America (about 55-85 each), and weakest for Africa and South-East Asia (about 26-38). The job-board session's figures agree within feed refreshes. Country names appear here only as working notes, never in posts.

## 2. Posts that could mislead a low-supply viewer [Hypothesis; net-impression test per CLAUDE.md]
| Post | Risk | Proposed fix (needs KT's yes, copy rule) |
|---|---|---|
| `w49-p1` video "Pay to look": "Over seventeen hundred remote jobs ... Tell it where you live and see the ones that say they're open to you." | **High.** The big number implies plenty for everyone; a viewer in Ghana or Indonesia finds about 30. | Drop the total from the voice and screen, or say the honest spread: "Tell it where you live, and see only the ones open to you. For some places that's a few dozen, not thousands." Prefer a number the viewer can rely on: "19 open worldwide this week". |
| `w50-p2` cover "{n} of {total} remote jobs are open beyond one country" | Low. It states scarcity honestly. | None. |
| `w50-p1` video "three in four ... open to just one country" | Low. It names the problem, then "only the jobs open to you" sets the right expectation. | None. |
| Role carousels: "open worldwide, or across a region that includes Africa or Asia" | Accurate under the current brief; too narrow under "outside the US". | Under the wider scope: "open worldwide, or across a whole region". The role picker already switches (`YC_SOCIAL_SCOPE=outside_us`: 52 roles qualify today against 28). |
| Tips (all) | None; country-neutral and useful anywhere. | None. |

## 3. Posting time under the wider scope [Established arithmetic; Hypothesis on fit]
| UTC | Mexico City | Toronto | São Paulo | London | Berlin | Lagos | Nairobi | Delhi | Manila |
|---|---|---|---|---|---|---|---|---|---|
| 12:00 (current) | 06:00 | 07:00 | 09:00 | 12:00 | 13:00 | 13:00 | 15:00 | 17:30 | 20:00 |
| **15:00** | 09:00 | 10:00 | 12:00 | 15:00 | 16:00 | 16:00 | 18:00 | 20:30 | 23:00 |
| 18:00 | 12:00 | 13:00 | 15:00 | 18:00 | 19:00 | 19:00 | 21:00 | 23:30 | 02:00 |

12:00 UTC is too early for the Americas. **15:00 UTC** is the best single compromise for "outside the US": afternoon in Europe and Africa, morning to midday in the Americas, evening in South Asia; it loses South-East Asia (23:00). If the scope widens, move the default to 15:00 UTC and make "12:00 vs 15:00" the week-3 test.

## 4. Niche accounts beyond Africa and Asia
Not researched yet. The 26 Nov sample (`2026-11-26-niche.md`) already shows the large US-facing list accounts; a pass on Europe, UK, Canada and Latin America (including Spanish and Portuguese-language accounts) costs about 6-10 Firecrawl credits and is worth doing once KT picks the scope.
