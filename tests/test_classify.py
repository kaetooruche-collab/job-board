import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from classify import (  # noqa: E402
    classify_listing, feed_decision,
    FULLY_REMOTE, REMOTE_RESTRICTED, REMOTE_UNCLEAR, HYBRID, ON_SITE,
)


def run(title, location="", description="", hint=None, remote_feed=False):
    r = classify_listing(title, location, description, hint=hint, remote_feed=remote_feed)
    return r, feed_decision(r)[0]


class WorkArrangement(unittest.TestCase):
    def test_fully_remote_stated(self):
        r, d = run("Customer Support Specialist", "Remote",
                   "This is a fully remote position. You will answer customer emails and chats.")
        self.assertIn(r["workArrangement"], (FULLY_REMOTE, REMOTE_RESTRICTED))
        self.assertEqual(d, "publish")
        self.assertEqual(r["confidence"], "high")

    def test_remote_united_states_is_restricted_not_onsite(self):
        r, d = run("Bookkeeper", "Remote - United States",
                   "We are hiring a bookkeeper to work from home. You must be located in the United States.")
        self.assertEqual(r["workArrangement"], REMOTE_RESTRICTED)
        self.assertEqual(r["eligibility"]["label"], "United States only")
        self.assertEqual(d, "publish")

    def test_hybrid_three_days(self):
        r, d = run("Marketing Coordinator", "London", "Hybrid, three days in the office each week.")
        self.assertEqual(r["workArrangement"], HYBRID)
        self.assertEqual(d, "exclude")

    def test_work_from_home_but_office_every_monday(self):
        r, d = run("Office Administrator", "Remote",
                   "Work from home, but must attend the office every Monday for team planning.")
        self.assertNotEqual(r["workArrangement"], FULLY_REMOTE)
        self.assertIn(d, ("review", "exclude"))

    def test_occasional_office_visits_still_remote(self):
        r, d = run("Content Writer", "Remote",
                   "This is a remote role with occasional office visits a few times a year for team meetups.")
        self.assertIn(r["workArrangement"], (FULLY_REMOTE, REMOTE_RESTRICTED))
        self.assertEqual(r["officeAttendance"], "occasional")
        self.assertEqual(d, "publish")
        self.assertTrue(any("how often" in q for q in r["unresolvedQuestions"]))

    def test_negated_office_requirement(self):
        r, d = run("Data Entry Clerk", "Remote",
                   "You will never be required to come to the office. This is a work from home job.")
        self.assertEqual(d, "publish")
        self.assertEqual(r["officeAttendance"], "explicitly_none")

    def test_company_level_remote_wording_not_enough(self):
        r, d = run("Accountant", "Chicago, IL",
                   "Remote opportunities are available for some roles at our company. Join our busy finance team in our downtown office.")
        self.assertNotEqual(r["workArrangement"], FULLY_REMOTE)
        self.assertNotEqual(d, "publish")

    def test_remote_after_training_is_unclear(self):
        r, d = run("Customer Service Representative", "Remote",
                   "Remote after 3 months of on-site training at our call centre.")
        self.assertEqual(r["workArrangement"], REMOTE_UNCLEAR)
        self.assertEqual(r["confidence"], "low")
        self.assertTrue(r["unresolvedQuestions"])

    def test_live_near_office_is_unclear(self):
        r, d = run("Support Agent", "Remote",
                   "This is a remote position, but candidates must live within 30 miles of our office.")
        self.assertEqual(r["workArrangement"], REMOTE_UNCLEAR)

    def test_title_says_remote_description_says_hybrid_is_conflict(self):
        r, d = run("Remote Marketing Manager", "Remote",
                   "Hybrid working: three days per week in the office. Office-based team.")
        self.assertTrue(r["conflict"])
        self.assertEqual(d, "review")

    def test_marketed_remote_but_unclear_is_kept_and_labelled(self):
        r, d = run("Virtual Assistant", "Remote", "Assist the founder with scheduling and inbox management.")
        self.assertIn(d, ("publish",))
        self.assertIn(r["workArrangement"], (FULLY_REMOTE, REMOTE_UNCLEAR, REMOTE_RESTRICTED))

    def test_remote_feed_without_evidence_is_unclear(self):
        r, d = run("Social Media Manager", "", "Grow our social channels.", remote_feed=True)
        self.assertEqual(r["workArrangement"], REMOTE_UNCLEAR)
        self.assertEqual(r["confidence"], "low")
        self.assertEqual(d, "publish")

    def test_city_only_no_remote_evidence_is_onsite(self):
        r, d = run("Nurse", "Dallas, TX", "Provide patient care at our clinic. In-person shifts.")
        self.assertEqual(r["workArrangement"], ON_SITE)
        self.assertEqual(d, "exclude")

    def test_structured_hint_alone_is_remote_medium(self):
        r, d = run("Recruiter", "", "Source and screen candidates.", hint="remote")
        self.assertIn(d, ("publish",))
        self.assertNotEqual(r["workArrangement"], ON_SITE)

    def test_not_remote_statement(self):
        r, d = run("Analyst", "Remote", "This role is not remote. Candidates work on-site five days a week.")
        self.assertNotEqual(d, "publish")

    def test_work_from_home_some_days_is_hybrid(self):
        r, d = run("Integration Engineer", "Vancouver, BC",
                   "This role is based in our office with an office-centric hybrid schedule. The standard in-office days are Monday, Tuesday and Thursday. Most of us work from home on Wednesdays.")
        self.assertEqual(r["workArrangement"], HYBRID)
        self.assertEqual(d, "exclude")
        self.assertFalse(r["conflict"])

    def test_balanced_policy_sentence_is_not_remote_proof(self):
        r, d = run("Account Executive", "London, England",
                   "Our team has a hybrid working policy. We believe working in person helps us stay connected while still providing flexibility to work remotely.")
        self.assertEqual(d, "exclude")

    def test_remote_first_but_not_remote_only_company(self):
        r, d = run("Market Operations Specialist", "Remote - USA",
                   "We are a remote-first, but not remote-only company. Expect to get together quarterly for in-person working sessions.")
        self.assertEqual(d, "publish")
        self.assertEqual(r["officeAttendance"], "occasional")


class Eligibility(unittest.TestCase):
    def test_worldwide(self):
        r, _ = run("Support Agent", "Anywhere", "We hire team members from anywhere in the world. Fully remote.")
        self.assertEqual(r["eligibility"]["type"], "worldwide")
        self.assertEqual(r["eligibility"]["label"], "Worldwide")

    def test_us_pronoun_is_not_a_country(self):
        r, _ = run("Support Agent", "Remote", "Join us as we build great support. You will work with us daily from home.")
        self.assertEqual(r["eligibility"]["type"], "unclear")

    def test_region_europe(self):
        r, _ = run("Translator", "Remote - Europe", "Fully remote position for translators.")
        self.assertEqual(r["eligibility"]["type"], "region")
        self.assertIn("Germany", r["eligibility"]["countries"])
        self.assertEqual(r["workArrangement"], REMOTE_RESTRICTED)

    def test_multiple_countries(self):
        r, _ = run("Support Agent", "Remote - Canada; Remote - United States", "Fully remote.")
        self.assertEqual(sorted(r["eligibility"]["countries"]), ["Canada", "United States"])

    def test_location_vs_description_conflict(self):
        r, _ = run("Support Agent", "Remote - United States",
                   "Fully remote. We hire candidates from anywhere in the world.")
        self.assertTrue(r["eligibility"]["conflict"])
        self.assertEqual(r["eligibility"]["label"], "Eligibility unclear")

    def test_description_restriction_with_generic_location(self):
        r, _ = run("Paralegal", "Remote",
                   "Fully remote. Applicants must be legally authorised to work in Canada.")
        self.assertEqual(r["eligibility"]["countries"], ["Canada"])
        self.assertTrue(r["eligibility"]["authorizationRequired"])

    def test_mentions_of_customers_abroad_do_not_restrict(self):
        r, _ = run("Support Agent", "Remote",
                   "Fully remote role. We serve customers in Germany, France and Spain.")
        self.assertEqual(r["eligibility"]["type"], "unclear")

    def test_city_location_without_remote_is_flagged(self):
        r, _ = run("Support Agent", "Austin, TX", "We are a remote-first company. Fully remote role.")
        self.assertEqual(r["eligibility"]["type"], "unclear")

    def test_timezone_requirement(self):
        r, _ = run("Support Agent", "Remote", "Fully remote. Must overlap with EST working hours.")
        self.assertEqual(r["eligibility"]["type"], "timezone")

    def test_bare_country_location_with_remote_hint(self):
        r, d = run("Support Agent", "Bahrain", "Help customers by chat and email.", hint="remote")
        self.assertEqual(r["eligibility"]["label"], "Bahrain only")
        self.assertEqual(d, "publish")

    def test_region_list_location_with_remote_hint(self):
        r, _ = run("Client Advisor", "Canada, Central America, South America", "Advise clients.", hint="remote")
        self.assertIn("Canada", r["eligibility"]["countries"])
        self.assertIn("Peru", r["eligibility"]["countries"])

    def test_hybrid_field_beats_company_distributed_wording(self):
        r, d = run("IT Director", "London", "We are a globally distributed company with great people.", hint="hybrid")
        self.assertEqual(r["workArrangement"], HYBRID)
        self.assertEqual(d, "exclude")

    def test_hybrid_in_technical_phrase_is_not_arrangement(self):
        r, d = run("Platform Engineer", "Remote", "Fully remote. You will run hybrid-cloud infrastructure and hybrid analyzers.")
        self.assertEqual(d, "publish")

    def test_in_person_in_communication_skills_is_not_office(self):
        r, d = run("Support Agent", "Remote", "Fully remote. You must communicate well in person, online and in writing.")
        self.assertEqual(d, "publish")

    def test_onsite_with_customers_is_not_office_attendance(self):
        r, d = run("Sales Engineer", "Remote", "Fully remote role. You will run demos both onsite and remotely with customers.")
        self.assertEqual(d, "publish")

    def test_depending_on_location_is_not_on_location(self):
        r, d = run("Support Agent", "Remote", "Fully remote. Benefits vary depending on location.")
        self.assertEqual(d, "publish")

    def test_company_level_worldwide_wording_does_not_override_location(self):
        r, _ = run("Security Engineer", "Remote - US",
                   "We are a fully remote company. While many roles may function from anywhere in the world, US based team members must be available in Eastern hours.", hint=None)
        self.assertEqual(r["eligibility"]["label"], "United States only")
        self.assertFalse(r["eligibility"]["conflict"])

    def test_office_in_location_field_is_onsite_evidence(self):
        r, d = run("Product Designer", "Paris office", "You can work remote if that is your profile, or from the office.")
        self.assertNotEqual(d, "publish")

    def test_location_line_in_description_is_role_level_remote(self):
        r, d = run("Customer Success Manager", "USA", "Location: Remote-first (United States). You will manage accounts.")
        self.assertEqual(d, "publish")
        self.assertIn(r["workArrangement"], (FULLY_REMOTE, REMOTE_RESTRICTED))

    def test_company_boilerplate_only_is_low_confidence(self):
        r, d = run("Customer Success Associate", "Philippines",
                   "We have an internationally distributed workforce of about 10,000 employees spanning many countries. Support our clients.")
        self.assertEqual(r["confidence"], "low")
        self.assertNotEqual(r["eligibility"]["label"], "Philippines only")

    def test_feed_geography_is_trusted(self):
        r, _ = run("Product Manager", "LATAM, Canada, USA",
                   "Fully remote. We hire talent from anywhere in the world.", remote_feed=True)
        self.assertIn("Canada", r["eligibility"]["countries"])


class ExperienceAndCategories(unittest.TestCase):
    def test_assistant_with_years_not_entry(self):
        r, _ = run("Executive Assistant", "Remote", "Fully remote. 8+ years of experience supporting executives required.")
        self.assertEqual(r["experience"]["level"], "senior")

    def test_internship(self):
        r, _ = run("Marketing Intern", "Remote", "Fully remote internship for students.")
        self.assertEqual(r["experience"]["level"], "internship")

    def test_no_experience_required(self):
        r, _ = run("Customer Support Agent", "Remote", "Fully remote. No experience required; full training provided.")
        self.assertEqual(r["experience"]["level"], "entry")

    def test_equivalent_experience(self):
        r, _ = run("Accountant", "Remote", "Fully remote. 3 years of experience or equivalent practical experience. Bachelor's degree preferred.")
        self.assertTrue(r["experience"]["equivalentExperienceAccepted"])
        self.assertEqual(r["experience"]["level"], "mid")

    def test_leadership(self):
        r, _ = run("Director of Finance", "Remote", "Fully remote.")
        self.assertEqual(r["experience"]["level"], "leadership")

    def test_ic_manager_is_not_leadership(self):
        r, _ = run("Customer Success Manager", "Remote", "Fully remote. 3 years of experience in SaaS.")
        self.assertNotEqual(r["experience"]["level"], "leadership")

    def test_categories_cover_non_tech(self):
        cases = {
            "Virtual Assistant": "Administration & Operations",
            "Customer Support Representative": "Customer Service & Support",
            "Medical Billing and Coding Specialist": "Healthcare & Life Sciences",
            "Accounts Payable Specialist": "Finance & Accounting",
            "Online English Tutor": "Education & Language",
            "Paralegal": "Legal & Compliance",
            "Technical Writer": "Writing & Editing",
            "Recruiter": "Human Resources & Recruiting",
            "Software Engineer": "Software & Engineering",
            "Content Moderator": "Trust, Safety & Moderation",
        }
        for title, expected in cases.items():
            with self.subTest(title=title):
                r, _ = run(title, "Remote", "Fully remote.")
                self.assertEqual(r["primaryCategory"], expected)


class Quality(unittest.TestCase):
    def test_commission_only_excluded(self):
        r, d = run("Sales Agent", "Remote", "Fully remote. This is a commission-only role.")
        self.assertEqual(d, "exclude")

    def test_applicant_fee_excluded(self):
        r, d = run("Data Entry", "Remote", "Work from home. A registration fee of $50 is required before training.")
        self.assertEqual(d, "exclude")

    def test_clean_listing_publishes(self):
        r, d = run("Data Analyst", "Remote", "Fully remote. 2 years of experience with SQL.")
        self.assertEqual(d, "publish")


if __name__ == "__main__":
    unittest.main(verbosity=2)
