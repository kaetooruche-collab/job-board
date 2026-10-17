import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from pay_text import pay_from_text  # noqa: E402


class PayFromText(unittest.TestCase):
    def test_copies_the_range_as_written(self):
        t = "The base pay ranges for this role are $147,800 - $226,700 per year, depending on location."
        self.assertEqual(pay_from_text(t), "$147,800 - $226,700")

    def test_several_ranges_become_one_span_marked_by_location(self):
        t = "Salary range for New York: $136,000 - $170,000. Salary range for the Bay Area: $151,120 - $189,000."
        self.assertEqual(pay_from_text(t), "$136,000 - $189,000 (varies by location)")

    def test_ignores_numbers_that_are_not_pay(self):
        for t in ("We raised $100,000 - $500,000 in funding rounds.", "Our customers spend $50,000 - $80,000 on contract value.",
                  "Sales quota is $500,000 - $900,000 per year.", "A $2,000 - $3,000 learning stipend."):
            self.assertIsNone(pay_from_text(t), t)

    def test_no_pay_no_result(self):
        self.assertIsNone(pay_from_text("Great benefits and a friendly team."))


if __name__ == "__main__":
    unittest.main()
