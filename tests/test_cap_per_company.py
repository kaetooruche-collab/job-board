"""The 15-per-employer limit keeps early-career roles first (25 Nov 2026), then the newest."""
import os
import sys
import unittest
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
import fetch_jobs as F  # noqa: E402

NOW = datetime(2026, 11, 25, tzinfo=timezone.utc)


def job(i, level, company="Acme"):
    return {"company": company, "posted": NOW - timedelta(days=i), "title": f"{level} {i}",
            "result": {"experience": {"level": level}}}


class Cap(unittest.TestCase):
    def test_an_old_junior_role_survives_many_newer_senior_roles(self):
        items = [job(i, "senior") for i in range(20)] + [job(25, "junior"), job(26, "internship")]
        out = F.cap_per_company(items, [])
        self.assertEqual(len(out), F.MAX_PER_COMPANY)
        self.assertIn("junior 25", [j["title"] for j in out])
        self.assertIn("internship 26", [j["title"] for j in out])
        # the rest of the places go to the newest senior roles
        self.assertIn("senior 0", [j["title"] for j in out])
        self.assertNotIn("senior 19", [j["title"] for j in out])

    def test_small_employers_are_untouched_and_companies_are_separate(self):
        items = [job(i, "mid", "A") for i in range(5)] + [job(i, "senior", "B") for i in range(3)]
        self.assertEqual(len(F.cap_per_company(items, [])), 8)


if __name__ == "__main__":
    unittest.main()


class TotalCap(unittest.TestCase):
    def test_under_the_limit_nothing_is_cut(self):
        items = [job(i, "senior", f"C{i}") for i in range(10)]
        self.assertEqual(len(F.cap_total(items, limit=20)), 10)

    def test_over_the_limit_old_early_career_roles_survive_and_the_oldest_others_go(self):
        # 25 Nov 2026: a 1,200 cap cut 594 checked jobs by age, 21 of them early-career roles still open
        items = [job(i, "senior", f"S{i}") for i in range(10)] + [job(20 + i, "junior", f"J{i}") for i in range(3)]
        out = F.cap_total(items, limit=8)
        titles = [j["title"] for j in out]
        self.assertEqual(len(out), 8)
        self.assertTrue(all(f"junior {20 + i}" in titles for i in range(3)))
        self.assertIn("senior 0", titles)
        self.assertNotIn("senior 9", titles)
        self.assertEqual([j["posted"] for j in out], sorted((j["posted"] for j in out), reverse=True), "newest first")

    def test_the_two_limits_agree(self):
        import discover_boards as D
        self.assertEqual(F.MAX_LISTINGS, D.MAX_LIVE_LISTINGS)


class Dates(unittest.TestCase):
    def test_recruitee_and_iso_dates(self):
        self.assertEqual(F.parse_dt("2026-11-24 10:10:44 UTC"), datetime(2026, 11, 24, 10, 10, 44, tzinfo=timezone.utc))
        self.assertEqual(F.parse_dt("2026-11-24T10:10:44Z"), datetime(2026, 11, 24, 10, 10, 44, tzinfo=timezone.utc))
        self.assertIsNone(F.parse_dt("Posted 3 Days Ago"))


def job_where(i, level, company, countries):
    j = job(i, level, company)
    j["result"]["eligibility"] = {"type": "countries", "countries": countries}
    return j


class OutsideUsFirst(unittest.TestCase):
    """KT, 26 Nov 2026: the board is for people outside the US, so US-only roles are the first to go."""
    def test_total_cap_cuts_us_only_roles_before_roles_open_outside_the_us(self):
        items = ([job_where(i, "senior", f"U{i}", ["United States"]) for i in range(6)]
                 + [job_where(10 + i, "senior", f"G{i}", ["Germany", "India"]) for i in range(4)])
        titles = [j["title"] for j in F.cap_total(items, limit=5)]
        self.assertTrue(all(f"senior {10 + i}" in titles for i in range(4)), "every role open outside the US stays")
        self.assertIn("senior 0", titles)            # the newest US-only role fills the last place
        self.assertNotIn("senior 1", titles)

    def test_per_company_limit_is_wider_for_roles_open_outside_the_us(self):
        items = ([job_where(i, "senior", "Elastic", ["United States"]) for i in range(30)]
                 + [job_where(40 + i, "senior", "Elastic", ["Spain", "Brazil"]) for i in range(50)])
        out = F.cap_per_company(items, [])
        us = [j for j in out if F.us_only(j)]
        self.assertEqual(len(us), F.MAX_PER_COMPANY)
        self.assertEqual(len(out) - len(us), F.MAX_PER_COMPANY_OUTSIDE_US)

    def test_roles_that_do_not_say_keep_the_strict_limit_and_sit_between(self):
        self.assertFalse(F.open_outside_us(job(0, "mid")))
        self.assertTrue(F.open_outside_us(job_where(0, "mid", "A", ["United States", "Canada"])))
        items = ([job_where(i, "mid", f"U{i}", ["United States"]) for i in range(3)] + [job(10 + i, "mid", f"N{i}") for i in range(3)]
                 + [job_where(20 + i, "mid", f"G{i}", ["Brazil"]) for i in range(3)])
        titles = [j["title"] for j in F.cap_total(items, limit=5)]
        self.assertTrue(all(f"mid {20 + i}" in titles for i in range(3)))   # outside the US: all kept
        self.assertIn("mid 10", titles); self.assertIn("mid 11", titles)    # then roles that do not say
        self.assertFalse(any(f"mid {i}" in titles for i in range(3)))        # US-only go first

    def test_us_only_means_only_the_united_states(self):
        self.assertTrue(F.us_only(job_where(0, "mid", "A", ["United States"])))
        self.assertFalse(F.us_only(job_where(0, "mid", "A", ["United States", "Canada"])))
        self.assertFalse(F.us_only(job(0, "mid")))  # not stated: not counted as US-only
