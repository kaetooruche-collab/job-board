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


class Dates(unittest.TestCase):
    def test_recruitee_and_iso_dates(self):
        self.assertEqual(F.parse_dt("2026-11-24 10:10:44 UTC"), datetime(2026, 11, 24, 10, 10, 44, tzinfo=timezone.utc))
        self.assertEqual(F.parse_dt("2026-11-24T10:10:44Z"), datetime(2026, 11, 24, 10, 10, 44, tzinfo=timezone.utc))
        self.assertIsNone(F.parse_dt("Posted 3 Days Ago"))
