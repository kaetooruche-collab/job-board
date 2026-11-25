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
