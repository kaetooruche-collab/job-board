"""Delivery times and priority wording must agree everywhere on the services page (KT, 25 Oct 2026)."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
S = (ROOT / "services.html").read_text(encoding="utf-8")


class DeliveryTimes(unittest.TestCase):
    def test_package_cards(self):
        self.assertIn("Delivered within 2 working days of completing onboarding", S)
        self.assertIn("Delivered within 3 working days of completing onboarding", S)

    def test_comparison_table(self):
        self.assertIn("<td>2 working days</td><td>3 working days</td>", S)

    def test_priority_is_one_working_day_and_old_wording_is_gone(self):
        self.assertIn("Priority delivery<small>Your documents within 1 working day", S)
        self.assertIn("priority delivery, within 1 working day ($15)", S)
        for old in ("48-hour priority", "Delivered in 5 working days", "instead of 5"):
            self.assertNotIn(old, S, old)

    def test_faq_matches(self):
        self.assertIn("Essential is delivered in 2 working days and Professional in 3", S)
        self.assertNotIn("<td>5 working days</td>", S)
        self.assertNotIn("Professional are delivered in 5", S)

    def test_executive_timing_untouched(self):
        self.assertIn("CV and cover letter within 2 working days, LinkedIn profile setup within 5", S)


if __name__ == "__main__":
    unittest.main()
