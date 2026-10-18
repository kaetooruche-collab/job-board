# Audit of audit_sample.json (10 records), run 18 Oct 2026

Method: every posting was fetched from its public source on 18 Oct 2026. The 4 SmartRecruiters postings were read from the public API (`api.smartrecruiters.com/v1/companies/{co}/postings/{id}`) and the live page. The 5 Workday postings were read from the tenant's public `/wday/cxs/.../job/...` JSON, and the Ashby posting from the public posting API (`includeCompensation=true`). The Ergomed Berlin page was re-read with Firecrawl (maxAge 0), and the page headers for Belgrade and Zagreb were checked the same way. No LinkedIn, Indeed, Glassdoor or ZipRecruiter pages were opened.

Scope of the "fully correct" count: items 1, 2, 3, 4 and 7. Items 5 (eligibility) and 6 (fit) are reported separately.

## Totals

- Fully correct (items 1-4 and 7 all match): 9 of 10.
- At least one mismatch in items 1-4 and 7: 1 of 10 (clinops-10, a minor unsupported location detail).
- Fit rating disagreements: 4 of 10 (medinfo-4, regulatory-7, clinops-11 and healthtech_ops-5, all B should be C). The other 6 ratings I agree with.
- Eligibility (item 5) problems: 1 record states a conclusion the posting does not state (medinfo-5, "no"), and 1 more is a softer version of the same issue (clinops-11). Details are in the mismatch list.
- All 10 postings are open, and all 10 posted dates match the source and are on or after 2026-10-11.

## Per-record results

### 1. clinops-10: Ergomed, Trial Master File Specialist (TMFS) II (SmartRecruiters 744000155752099)
1. Open: MATCH. API `active: true`, the page has an "I'm interested" button, and there is no closed wording.
2. Posted date: MATCH. `releasedDate` 2026-10-15T12:49Z, `datePosted` is the same, and it is after 10-11.
3. Location and work mode: MISMATCH (minor).
   - The page header says "Belgrade, Serbia / Employees can work remotely". The structured data adds Sarajevo (addressLocality), and the "Country/Region" custom field says Bosnia and Herzegovina.
   - The record's claim "also for Novi Sad, Serbia" appears nowhere in the API, the page text or the page metadata. It is unsupported.
   - Remote is a SmartRecruiters flag (`remote: true, hybrid: false`). The body text never says remote.
4. Experience, education and licence: MATCH.
   - Quote: "TMF maintenance and quality check experience", "Administrative work experience, preferably in an international Clinical Research setting". No years are given, and no education or licence is stated.
   - SmartRecruiters tags it "Entry Level", but the title says "experience required".
5. Eligibility: no work-authorisation text, and "Very good English oral and written" is present. The record is right, and "unclear" is correct.
6. Fit: agree B. The clear gap is hands-on TMF/QC experience, which is required, and no years are stated.
7. Salary: MATCH (none stated).

### 2. medinfo-6: Novartis, Medical Information Associate, Seoul (REQ-10087203)
1. Open: MATCH. `canApply: true`, `posted: true`. The record missed that the JSON has `endDate: 2026-10-31`, so the role closes in 13 days. The record has no field for this, so it is an omission and not a mismatch.
2. Posted date: MATCH. `startDate` 2026-10-13 and "Posted 5 Days Ago".
3. Location and work mode: MATCH. Seoul, South Korea. The posting says nothing on remote or hybrid, so "unclear" is right.
4. Experience, education and licence: MATCH.
   - "At least one year of experience in a healthcare setting".
   - "Bachelor's degree in Life Sciences or a relevant healthcare discipline, such as pharmacy, nursing or medicine".
   - No licence is stated.
5. Eligibility: no residency or work-authorisation text, and Korean is not mentioned. The posting is for the Novartis Korea Limited entity and works "in line with local regulations". Whether Korean is needed in practice cannot be checked from the text.
6. Fit: agree B. The gap is 1 year in a healthcare setting. The role is also tied to Seoul, so it is not realistic for a non-resident.
7. Salary: MATCH (none stated).

### 3. clinops-1: Thermo Fisher, Assistant CRA, Johannesburg (R-01368231)
1. Open: MATCH. `canApply: true`, and no closed wording.
2. Posted date: MATCH. `startDate` 2026-10-12 and "Posted 6 Days Ago".
3. Location and work mode: MATCH, with a caveat.
   - `remoteType: Fully Remote`, location "South Africa - Johannesburg - Woodlands Drive".
   - The body says "perform remote activities", "Work is performed most of the time in an office or home office environment", and lists "Standard Office Hours" with environmental condition "Office".
   - So "remote" rests on the structured flag. The text is only "office or home office".
4. Experience, education and licence: MATCH.
   - "comparable to 0 to 2 years", with equivalency considered.
   - "Bachelor's degree in a life science discipline or related field or a Registered Nursing certification or equivalent".
   - No licence is required.
5. Eligibility: no residency or work-authorisation sentence. The role is tied to the South African entity, and "Excellent English language and grammar skills" is stated. "Unclear" is correct.
6. Fit: agree A on the stated minimum (0-2 years, a degree). This is conditional on being able to work in South Africa.
7. Salary: MATCH (none stated).

### 4. medinfo-5: Fortrea, Medical Contact Center Associate I, Manila (266007)
1. Open: MATCH. `canApply: true`.
2. Posted date: MATCH. `startDate` 2026-10-16 and "Posted 2 Days Ago".
3. Location and work mode: MATCH, with a caveat. `remoteType: Hybrid`, location Manila, Philippines. The body contradicts itself: "Physical Demands/Work Environment: Office Environment or remote."
4. Experience, education and licence: MATCH.
   - "Bachelor's or Master's in Pharmacy or Life Science or Medical Science or related area + 1 to 2 years of safety experience".
   - The posting also gives alternative routes, including "Fortrea may consider relevant and equivalent experience in lieu of educational requirements".
   - No licence is required.
5. Eligibility: the record says `open_to_non_residents: "no"`. The posting contains no residency or work-authorisation wording, so "no" is an inference from the Manila location and is not stated. It should read "unclear" (or "inferred no"). It is also inconsistent with the other location-bound records, which say "unclear".
6. Fit: agree B. The gap is 1-2 years of safety (AE/SAE) experience. The role is hybrid in Manila.
7. Salary: MATCH (none stated).

### 5. medinfo-4: Ergomed/PrimeVigilance, Medical Writer III (PV), Zagreb (744000155975969)
1. Open: MATCH. `active: true`, and the page has an apply button.
2. Posted date: MATCH. 2026-10-16T11:43Z.
3. Location and work mode: MATCH. The page header says "Zagreb, Croatia / Employees can work remotely". The API says `remote: true, hybrid: false`.
4. Experience, education and licence: MATCH.
   - "Minimum 2 years' experience in Medical Writing and associated fields (case processing, signal detection or risk management) ideally within a CRO environment".
   - "MD, pharmacy or Life Science degree (Masters or PhD is desirable)".
   - No licence is required.
5. Eligibility: no work-authorisation text. "Fluency in English" is required. "Unclear" is correct.
6. Fit: DISAGREE. The record says B and it should be C.
   - The role is "Level III" (SmartRecruiters: Mid-Senior Level), looking for "an experienced pharmacovigilance medical writer".
   - It has a 2-year minimum in a specialised field, plus "Ability to effectively train and mentor Associate Medical Writers" and a client-facing lead role.
   - That is more than one gap for a graduate with little or no experience.
7. Salary: MATCH (none stated).

### 6. regulatory-7: Ergomed/PrimeVigilance, Local Contact Person for PV and RA (Contractor) - Germany (744000155310319)
1. Open: MATCH. `active: true`. Page: "Berlin, Germany / Employees can work remotely".
2. Posted date: MATCH. 2026-10-13T16:06Z.
3. Location and work mode: MATCH. Berlin, `remote: true, hybrid: false`.
   - The record correctly noted that the body names Australia ("compliance with national pharmacovigilance and regulatory requirements in Australia"). I confirmed this.
   - The role is a Contractor, tagged in the custom field "Permanent/Contractor: Contractor". The record has this only in the title.
4. Experience, education and licence: MATCH.
   - "At least 3 years of pharmacovigilance or safety-related experience in pharmaceutical, CRO, or regulatory environment".
   - "Bachelor's Degree in Life Sciences or Chemistry, Nursing or equivalent professional experience".
   - "Prior experience in Regulatory Affairs is preferred but not mandatory".
   - No licence is stated.
5. Eligibility: no work-authorisation text. The posting is internally inconsistent (Germany vs Australia), so the target country is not reliable.
6. Fit: DISAGREE. The record says B and it should be C. The minimum is 3 years of PV experience, the role is a Local Country Person Responsible for PV/RA, and it is a contractor position. That is not one gap.
7. Salary: MATCH (none stated).

### 7. clinops-11: PSI CRO, Site Contract Specialist I, Mexico (744000155843309)
1. Open: MATCH. `active: true`, and the page has an apply button.
2. Posted date: MATCH. 2026-10-15T19:50Z.
3. Location and work mode: MATCH. Mexico City, `remote: true`. The body says "Home-based position in Mexico."
4. Experience, education and licence: MATCH.
   - "Previous experience working with study startup operations is required".
   - "College/University degree or an equivalent combination of education, training & experience".
   - No licence is required.
5. Eligibility: "Home-based position in Mexico. Only CVs in English will be considered." and "Fluency in Spanish and English, oral and written." The record's "no" for non-residents is a reasonable inference from "in Mexico". The posting does not literally say non-residents are excluded.
6. Fit: DISAGREE. The record says B and it should be C.
   - There are two required gaps: previous study start-up operations experience (required) and fluency in Spanish (required, if the candidate lacks it).
   - It is also a home-based position in Mexico only.
7. Salary: MATCH (none stated).

### 8. healthtech_ops-5: Montu UK (Leafio), Quality Assurance Officer, Winnersh (Ashby d3f2d04d-1b78-45cf-8886-1525a0d92c62)
1. Open: MATCH. `isListed: true`, an `applyUrl` exists, and there is no closed wording.
2. Posted date: MATCH. `publishedAt` 2026-10-14T16:10Z.
3. Location and work mode: MATCH. The location string is "Hybrid Winnersh". `workplaceType` and `isRemote` are null. The posting lists "Work-from-home options" under benefits.
4. Experience, education and licence: MATCH.
   - "Proven experience working within a GMDP regulated pharmaceutical environment ... with more than 2 years experience".
   - No education is stated, and no licence is stated.
   - It also requires proven QMS experience and proven experience with unlicensed products (Regulation 167).
5. Eligibility: no visa wording. The role is UK-based (MHRA, Reg 167, GDP). Correct.
6. Fit: DISAGREE. The record says B and it should be C.
   - There are three separate "proven experience" requirements: GMDP over 2 years, QMS, and Reg 167.
   - It is a hybrid on-site UK role.
   - That is more than one gap.
7. Salary: MATCH. Ashby compensation is "£50K – £55K" (GBP, salary, per year). The posting also lists "Offers Equity", which the record omitted. This is minor.

### 9. pharmacovigilance-4: Thermo Fisher, Drug Safety Reporting Coordinator, Remote Philippines (R-01364421)
1. Open: MATCH. `canApply: true`.
2. Posted date: MATCH. `startDate` 2026-10-17 and "Posted Yesterday".
3. Location and work mode: MATCH, with a caveat.
   - `remoteType: Fully Remote`, location "Remote, Philippines". The requisition descriptor is "Philippines - Taguig City - Seven NEO Bldg., 5th Avenue - Remote".
   - The body says "Work is performed in an office environment with exposure to electrical office equipment" and "Potential drives to site locations and/or travel required on rare occasion". So remote rests on the structured flag and the "Remote" label.
4. Experience, education and licence: MATCH.
   - "Previous experience ... (comparable to at least 2 years)", with equivalency allowed.
   - "High / Secondary school diploma or equivalent and relevant formal academic / vocational qualification".
   - No licence is stated.
5. Eligibility: no residency or work-authorisation wording, though the location is Philippines-specific. "Unclear" is correct.
6. Fit: agree B. The gap is about 2 years of comparable experience (equivalency considered). The role is administrative, with a low qualification bar.
7. Salary: MATCH (none stated).

### 10. clinops-4: Thermo Fisher, FSP Clinical Trial Coordinator, Remote Sweden (R-01369781)
1. Open: MATCH. `canApply: true`.
2. Posted date: MATCH. `startDate` 2026-10-16 and "Posted 2 Days Ago".
3. Location and work mode: MATCH, with a caveat. `remoteType: Fully Remote`, location "Remote, Sweden". The body adds "Hybrid work if located in Copenhagen or Stockholm (where we have Thermo Fisher offices). If other location, it will be a remote work setting." So "remote" is conditional. The record quotes this in `eligibility_stated`, but `work_mode: remote` on its own over-simplifies it.
4. Experience, education and licence: MATCH.
   - "comparable to 0 to 1 year".
   - "High / Secondary school diploma or equivalent and relevant formal academic / vocational qualification. Bachelor's degree preferred."
   - No licence is stated.
5. Eligibility: "Good English language and grammar skills and proficient local language skills (Swedish or Danish)". The record has this. There is no work-authorisation text.
6. Fit: agree B. The one clear gap is Swedish or Danish.
7. Salary: MATCH (none stated).

## Every mismatch and disagreement

Mismatches in items 1-4 and 7:
1. clinops-10, item 3 (minor): "also for Novi Sad, Serbia" is not on the posting, API or metadata. Only Belgrade (page header) and Sarajevo/Bosnia and Herzegovina (structured data and custom field) are supported.

Eligibility issues (item 5, not in the tally):
2. medinfo-5: `open_to_non_residents: "no"` is an inference. The posting states no residency or work-authorisation rule. It is inconsistent with other location-bound records marked "unclear".
3. clinops-11: "no" is a strong inference from "Home-based position in Mexico", not an explicit statement.

Fit disagreements (item 6), all B to C:
4. medinfo-4: Level III, 2-year minimum, and mentoring duties.
5. regulatory-7: 3-year PV minimum, local responsible person role, contractor.
6. clinops-11: required start-up operations experience plus required Spanish, in Mexico only.
7. healthtech_ops-5: three separate "proven experience" requirements, and hybrid UK on-site.

Omissions and caveats (not counted as mismatches):
8. medinfo-6: the record missed the posting's `endDate` of 2026-10-31.
9. healthtech_ops-5: the record omitted "Offers Equity" in the compensation.
10. clinops-1, pharmacovigilance-4, clinops-4 and medinfo-5: the record's `work_mode` follows the Workday flag, while the body text is softer or contradicts it. Respectively: "office or home office"; "office environment"; hybrid in Stockholm or Copenhagen; "Office Environment or remote" (the flag says Hybrid).
11. clinops-10: remote is stated only by a flag and a page label ("Employees can work remotely"), not in the description.

## Limits of this audit
- Workday pages were verified through the tenant JSON. For Workday I cannot tell whether `startDate` is the original post date or a repost date. The "Posted N days ago" text agrees with it in every case.
- Whether any posting needs a specific local language or residency beyond what the text says cannot be checked from the postings. Where a text was silent, I did not guess.
- I did not test the apply flows beyond confirming that an apply button or `canApply`/`applyUrl` exists.
