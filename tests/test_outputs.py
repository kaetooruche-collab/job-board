import sys
import unittest
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import make_outputs  # noqa: E402

NOW = datetime(2026, 10, 17, 12, 0, tzinfo=timezone.utc)


def row(i, company, hours_ago, arrangement="fully_remote", level="mid", category="Support"):
    return {"id": f"j{i}", "title": f"Role {i}", "company": company, "category": category, "level": level,
            "jobType": "Full-time", "workArrangement": arrangement, "salaryText": None,
            "postedAt": (NOW - timedelta(hours=hours_ago)).isoformat(), "sourceName": "Test",
            "sourceUrl": f"https://example.com/{i}", "eligibility": {"label": "Worldwide"}}


class WhatsAppPost(unittest.TestCase):
    def test_one_per_company_and_no_unclear(self):
        rows = [row(1, "A", 1), row(2, "A", 2), row(3, "B", 3, "remote_unclear"), row(4, "C", 4, category="Sales"),
                row(5, "D", 5, category="Design"), row(6, "E", 6, category="Ops")]
        items = make_outputs.pick(rows, NOW)
        companies = [r["company"] for r in items]
        self.assertEqual(len(companies), len(set(companies)))
        self.assertNotIn("B", companies)

    def test_old_listings_excluded(self):
        rows = [row(1, "A", 100), row(2, "B", 2)]
        self.assertEqual([r["id"] for r in make_outputs.pick(rows, NOW)], ["j2"])

    def test_early_career_listing_included_when_available(self):
        rows = [row(i, f"C{i}", i, category=f"Cat{i}") for i in range(1, 8)] + [row(9, "Junior Co", 60, level="junior", category="Cat9")]
        ids = [r["id"] for r in make_outputs.pick(rows, NOW)]
        self.assertIn("j9", ids)

    def test_render_has_direct_link_time_and_pay_rule(self):
        items = make_outputs.pick([row(1, "A", 1), row(2, "B", 2, category="X"), row(3, "C", 3, category="Y")], NOW)
        text = make_outputs.render(items, NOW)
        self.assertIn("https://example.com/1", text)
        self.assertIn("Posted 17 Oct on Test", text)
        self.assertIn("Pay: not stated", text)
        self.assertIn("utm_campaign=weekly", text)
        self.assertNotIn("UTC", text)

    def test_weekly_window_is_seven_days(self):
        rows = [row(1, "A", 100), row(2, "B", 2), row(3, "C", 200)]
        ids = [r["id"] for r in make_outputs.pick(rows, NOW, max_age_hours=make_outputs.WEEKLY_AGE_HOURS)]
        self.assertEqual(sorted(ids), ["j1", "j2"])

    def test_open_to_all_listings_come_first(self):
        restricted = row(1, "A", 1, category="X")
        restricted["eligibility"] = {"type": "countries", "label": "US only"}
        rows = [restricted] + [row(i, f"C{i}", i + 1, category=f"Cat{i}") for i in range(2, 8)]
        ids = [r["id"] for r in make_outputs.pick(rows, NOW)]
        self.assertNotIn("j1", ids)


if __name__ == "__main__":
    unittest.main()
