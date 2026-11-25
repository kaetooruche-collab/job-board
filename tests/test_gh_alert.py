"""The failure-alert logic: one issue per workflow, updated not duplicated, closed on recovery."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
import gh_alert as A  # noqa: E402


class Alerts(unittest.TestCase):
    NOW = "2026-11-25T10:00:00Z"

    def test_first_failure_opens_one_labelled_issue(self):
        ops = A.decide("fail", None, "Refresh job listings", "tests failed", self.NOW)
        self.assertEqual(len(ops), 1)
        method, path, payload = ops[0]
        self.assertEqual((method, path), ("POST", "/issues"))
        self.assertEqual(payload["labels"], ["autopilot"])
        self.assertIn("Refresh job listings", payload["title"])
        self.assertEqual(A.parse_state(payload["body"])["count"], 1)

    def test_repeat_failure_updates_the_same_issue_and_counts(self):
        body = A.body_for("Refresh job listings", "x", 4, "2026-11-24T00:00:00Z", "2026-11-24T18:00:00Z")
        existing = {"number": 7, "body": body}
        ops = A.decide("fail", existing, "Refresh job listings", "x", self.NOW, last_comment_at="2026-11-25T08:00:00Z")
        self.assertEqual([o[0] for o in ops], ["PATCH"], "no comment within a day of the last one")
        st = A.parse_state(ops[0][2]["body"])
        self.assertEqual(st, {"count": 5, "first_seen": "2026-11-24T00:00:00Z"})

    def test_a_daily_reminder_comment_after_24_hours(self):
        existing = {"number": 7, "body": A.body_for("W", "x", 2, "2026-11-23T00:00:00Z", "2026-11-23T06:00:00Z")}
        ops = A.decide("fail", existing, "W", "x", self.NOW, last_comment_at="2026-11-24T09:00:00Z")
        self.assertEqual([o[0] for o in ops], ["PATCH", "POST"])

    def test_recovery_closes_the_issue_and_a_green_run_without_one_does_nothing(self):
        ops = A.decide("ok", {"number": 9, "body": ""}, "W", "", self.NOW)
        self.assertEqual([o[0] for o in ops], ["POST", "PATCH"])
        self.assertEqual(ops[1][2]["state"], "closed")
        self.assertEqual(A.decide("ok", None, "W", "", self.NOW), [])

    def test_without_a_token_it_only_prints(self):
        env = {k: os.environ.pop(k) for k in ("GH_TOKEN", "GITHUB_TOKEN") if k in os.environ}
        try:
            self.assertEqual(A.main(["gh_alert.py", "fail", "W", "why"]), 0)
        finally:
            os.environ.update(env)


if __name__ == "__main__":
    unittest.main()
