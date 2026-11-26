# A region named beside a country no longer widens who can apply (26 Nov 2026)

Status: **live** (PR #79 merged on KT's yes, 26 Nov 2026; refresh run 45801361058). Checked on the live site: Concentric "Australia, Singapore", CircleCI "Japan only", Sprout Social "Philippines only"; jobs open to India 81 -> 78.

**Bug:** postings limited to one country were labelled with the whole region and shown to ~40 countries:
- Concentric "open to those based in Australia" was labelled APAC.
- CircleCI "Remote - Japan" was labelled APAC.
- Sprout Social "must be based in the Philippines … another location within APAC, we aren't able to hire" was labelled APAC.

Found while choosing India footage for video 1 (3 of the 81 jobs shown for India).

**Fix:** a region that only comes from the description is dropped when the posting names a country inside it. Two kinds of region are kept:
1. A region the employer lists as a location option.
2. A region the posting widens to on purpose:
   - "anywhere in …"
   - "remote across …"
   - "ideally" or "with a preference for"
   - "will consider applicants from …"
   - "you can be based in …"
   - "another … country"

   A widening phrase doesn't count when the sentence refuses to hire.

**How the rule was found:** by the old-versus-new comparison on 12,887 postings.
- **Version 1** (drop any region beside a member country): 100 changes. It wrongly narrowed real region-wide openings (Ashby "Remote - European Union", Alpaca "Remote Americas", Deepgram "EU - Remote").
- **Version 2** (description-only regions): 64 changes. Still wrong for "anywhere in Europe" (ElevenLabs), "any other location in Europe" (Azul) and "remote across the European Union" (Wrike).
- **Final:** 41 changes (29 published), each read against its wording. 0 changes to which jobs are published.

**Follow-ups (separate bugs, not fixed here):**
- Doximity "San Francisco, CA or Remote (U.S.)" is labelled "South America, United States, Canada".
- Andela "Strategic Partnership Manager" (London) is labelled Africa and Latin America from a sentence about Andela's talent network.
- ClickHouse "We're small, senior and remote across North America and EMEA" is a team statement read as eligibility.

The new QA warning (`region-label-wider-than-location`) surfaces cases like these in `data/qa_report.md`.
