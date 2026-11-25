"""The health check's rules, with no network."""
import os
import sys
import unittest
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
import health_check as H  # noqa: E402

NOW = datetime(2026, 11, 25, 12, 0, tzinfo=timezone.utc)


class Health(unittest.TestCase):
    def test_the_18_to_25_november_outage_reads_red(self):
        s, why = H.check_freshness({"generatedAt": "2026-11-18T20:26:00+00:00", "activeListings": 1019}, NOW)
        self.assertEqual(s, H.RED)
        self.assertIn("hours ago", why)
        s, _ = H.check_workflow("refresh", 14, "active", {"created_at": "2026-11-25T10:00:00Z", "conclusion": "failure"}, NOW)
        self.assertEqual(s, H.RED)

    def test_a_normal_day_is_green(self):
        self.assertEqual(H.check_freshness({"generatedAt": "2026-11-25T08:00:00+00:00"}, NOW)[0], H.GREEN)
        self.assertEqual(H.check_volume([1000, 1010, 990, 1020, 1005], 1036)[0], H.GREEN)
        self.assertEqual(H.check_workflow("x", 14, "active", {"created_at": "2026-11-25T09:00:00Z", "conclusion": "success"}, NOW)[0], H.GREEN)

    def test_a_disabled_or_overdue_workflow_is_red(self):
        self.assertIn("disabled_inactivity", H.check_workflow("x", 14, "disabled_inactivity", None, NOW)[1])
        self.assertEqual(H.check_workflow("x", 14, "active", {"created_at": "2026-11-24T00:00:00Z", "conclusion": "success"}, NOW)[0], H.RED)

    def test_volume_drop_and_repo_inactivity(self):
        self.assertEqual(H.check_volume([1000] * 10, 650)[0], H.RED)
        self.assertEqual(H.check_volume([1000] * 10, 800)[0], H.AMBER)
        self.assertEqual(H.check_repo_activity("2026-10-20T00:00:00Z", NOW)[0], H.AMBER)
        self.assertEqual(H.check_repo_activity("2026-09-01T00:00:00Z", NOW)[0], H.RED)

    def test_overall_is_the_worst_check(self):
        self.assertEqual(H.overall([("a", H.GREEN, ""), ("b", H.AMBER, ""), ("c", H.RED, "")]), H.RED)
        self.assertEqual(H.overall([]), H.GREEN)


if __name__ == "__main__":
    unittest.main()
