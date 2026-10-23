import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import qa_checks as Q  # noqa: E402

NOW = datetime(2026, 10, 17, 12, 0, tzinfo=timezone.utc)


def rec(**kw):
    base = {"id": "j1", "title": "Customer Support Agent", "company": "Acme", "level": "mid", "workArrangement": "fully_remote",
            "regionAsStated": "Remote - United States", "salaryText": None, "flags": [], "sourceName": "Test",
            "sourceUrl": "https://boards.example.com/acme/jobs/123", "postedAt": (NOW - timedelta(days=2)).isoformat(),
            "eligibility": {"type": "countries", "label": "United States only", "countries": ["United States"], "regions": [], "notes": []}}
    base.update(kw)
    return base


def rules(issues, severity=None):
    return {i["rule"] for i in issues if severity is None or i["severity"] == severity}


class JobicyDates(unittest.TestCase):
    def test_jobicy_listings_are_blocked_because_their_date_is_not_original(self):
        r = rec(sourceName="Jobicy", sourceUrl="https://jobicy.com/jobs/156488-director-people-operations", postedAt="2026-10-16T06:19:36+00:00")
        self.assertIn("source-date-not-original", rules(Q.check_listing(r, None, NOW), Q.BLOCK))

    def test_employer_board_sources_are_not_blocked_by_that_rule(self):
        for src in ("Greenhouse", "Lever", "Ashby"):
            self.assertNotIn("source-date-not-original", rules(Q.check_listing(rec(sourceName=src), None, NOW)), src)

    def test_the_real_evidence_is_in_the_fixture(self):
        import json
        fx = json.loads((Path(__file__).resolve().parent / "fixtures" / "jobicy_dates.json").read_text())
        self.assertGreater(fx["pair"]["jobicy"]["postedAt"], fx["pair"]["employer_greenhouse"]["postedAt"])
        self.assertEqual(fx["batches"]["2026-10-23T07:09"], 20)


class ListingChecks(unittest.TestCase):
    def test_clean_record_passes(self):
        self.assertEqual(Q.check_listing(rec(), {"description": "Fully remote role.", "result": {}}, NOW), [])

    def test_senior_title_cannot_be_junior(self):
        self.assertIn("level-title-conflict", rules(Q.check_listing(rec(title="Senior Marketing Operations Specialist", level="junior"), None, NOW), Q.BLOCK))

    def test_junior_markers_and_lead_generation_are_fine(self):
        for t in ("Associate Product Manager", "Junior Data Analyst", "Lead Generation Specialist", "Assistant Manager Trainee"):
            self.assertNotIn("level-title-conflict", rules(Q.check_listing(rec(title=t, level="junior"), None, NOW)), t)

    def test_label_contradicts_exclusion_note(self):
        e = {"type": "countries", "label": "United States only", "countries": ["United States"], "regions": [],
             "notes": ["The posting says it cannot hire in: United States."]}
        self.assertIn("eligibility-contradicts-exclusion", rules(Q.check_listing(rec(eligibility=e), None, NOW), Q.BLOCK))

    def test_label_with_no_support_in_evidence_is_held(self):
        # the old "hear back from us" bug: the label says United States but nothing names it
        raw = {"description": "Fully remote.", "result": {"evidence": [{"text": "you will hear back from us"}], "eligibility": {"evidence": []}}}
        r = rec(regionAsStated="Remote")
        self.assertIn("eligibility-label-unsupported", rules(Q.check_listing(r, raw, NOW), Q.BLOCK))

    def test_plain_statement_that_role_is_not_remote(self):
        raw = {"description": "This role is hybrid, three days per week in the office.", "result": {}}
        self.assertIn("says-not-remote-but-published-as-remote", rules(Q.check_listing(rec(), raw, NOW), Q.BLOCK))

    def test_hybrid_in_the_location_line(self):
        raw = {"description": "\U0001F4CDLondon (Hybrid) | \U0001F4B0\u00a375,000 - \u00a395,000", "result": {}}
        self.assertIn("says-not-remote-but-published-as-remote", rules(Q.check_listing(rec(), raw, NOW), Q.BLOCK))

    def test_remote_friendly_wording_is_not_flagged(self):
        raw = {"description": "We are a remote-first company with an optional office in Austin for team meetups.", "result": {}}
        self.assertNotIn("says-not-remote-but-published-as-remote", rules(Q.check_listing(rec(), raw, NOW)))

    def test_estimated_pay_is_held(self):
        self.assertIn("salary-looks-estimated", rules(Q.check_listing(rec(salaryText="approx. USD 50,000"), None, NOW), Q.BLOCK))

    def test_homepage_url_is_held(self):
        self.assertIn("not-a-specific-posting-url", rules(Q.check_listing(rec(sourceUrl="https://example.com/"), None, NOW), Q.BLOCK))

    def test_old_and_future_postings_are_held(self):
        old = (NOW - timedelta(days=45)).isoformat()
        fut = (NOW + timedelta(days=5)).isoformat()
        self.assertIn("older-than-30-days", rules(Q.check_listing(rec(postedAt=old), None, NOW), Q.BLOCK))
        self.assertIn("posted-in-future", rules(Q.check_listing(rec(postedAt=fut), None, NOW), Q.BLOCK))

    def test_html_in_title_is_held(self):
        self.assertIn("html-in-title-or-company", rules(Q.check_listing(rec(title="Support &amp; Success"), None, NOW), Q.BLOCK))

    def test_trust_flags_never_published(self):
        self.assertIn("trust-flag-published", rules(Q.check_listing(rec(flags=["applicant_fee"]), None, NOW), Q.BLOCK))


class RunChecks(unittest.TestCase):
    def test_big_drop_stops_the_run(self):
        abort, _ = Q.drift({"count": 300, "bySource": {}}, {"count": 1000, "bySource": {}})
        self.assertTrue(abort)

    def test_normal_change_does_not_stop(self):
        abort, warn = Q.drift({"count": 950, "bySource": {"A": 100}, "pctEligibilityUnclear": 20, "pctRemoteUnclear": 5, "pctWorldwide": 30, "pctEarlyCareer": 11},
                              {"count": 1000, "bySource": {"A": 105}, "pctEligibilityUnclear": 19, "pctRemoteUnclear": 5, "pctWorldwide": 29, "pctEarlyCareer": 11})
        self.assertEqual((abort, warn), ([], []))

    def test_shift_in_shape_warns(self):
        _, warn = Q.drift({"count": 1000, "bySource": {}, "pctEligibilityUnclear": 60, "pctRemoteUnclear": 5, "pctWorldwide": 30, "pctEarlyCareer": 11},
                          {"count": 1000, "bySource": {}, "pctEligibilityUnclear": 20, "pctRemoteUnclear": 5, "pctWorldwide": 29, "pctEarlyCareer": 11})
        self.assertTrue(any("unclear eligibility" in w for w in warn))

    def test_source_outage_warns(self):
        _, warn = Q.drift({"count": 900, "bySource": {"Ashby": 5}, "pctEligibilityUnclear": 0, "pctRemoteUnclear": 0, "pctWorldwide": 0, "pctEarlyCareer": 0},
                          {"count": 1000, "bySource": {"Ashby": 200}, "pctEligibilityUnclear": 0, "pctRemoteUnclear": 0, "pctWorldwide": 0, "pctEarlyCareer": 0})
        self.assertTrue(any("Ashby" in w for w in warn))


if __name__ == "__main__":
    unittest.main()
