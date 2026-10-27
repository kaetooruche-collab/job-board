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

    # --- regressions from real listings (27 Oct 2026) -------------------------------------
    # The QA rule "pay-in-posting-but-card-says-not-stated" flagged 11 published cards whose
    # posting did state pay. Cause: the figures sit in a bullet list under a heading, further
    # than the old 160-character window from any word about pay.

    ZONE_LIST = (
        "About you\nWe are looking for someone with experience, knowledge, qualifications, "
        "and skills in financial modelling, forecasting and partner reporting for a fast-moving "
        "international team where you will own the numbers end to end and work with leaders.",
        "\nCompensation\nFor candidates hired into this role, the annual base salary range is based "
        "on a number of factors including job-related skills, qualifications, experience, education, "
        "and other business and operational needs at the time of hire.",
        "\n - United States (all figures cited below are in USD and pertain to workers in the United States)"
        "\n - Zone A: $112,000 - $135,000"
        "\n - Zone B: $105,000 - $126,000"
        "\n - Zone C: $98,300 - $118,000",
    )

    def test_zone_list_under_a_heading_is_now_found(self):
        t = "".join(self.ZONE_LIST)
        self.assertIsNone(pay_from_text(t, lookback=160), "the old window missed this")
        self.assertEqual(pay_from_text(t), "$98,300 - $135,000 USD (varies by location)")

    def test_a_named_currency_is_shown_not_assumed(self):
        t = "Total compensation for this vacancy: IC4: $140,000-$190,000 CAD, paid annually."
        self.assertEqual(pay_from_text(t), "$140,000 - $190,000 CAD")
        # a dollar figure with no currency named stays exactly as written — no invented suffix
        t2 = "Base pay range for the role is $140,000 - $190,000 per year."
        self.assertEqual(pay_from_text(t2), "$140,000 - $190,000")

    def test_two_currencies_are_never_merged_into_one_span(self):
        t = ("Compensation: United States (figures in USD): $195,000 - $230,000; "
             "$180,000 - $205,000. Canada (figures in CAD): CAD 120,000 - 140,000.")
        out = pay_from_text(t)
        self.assertEqual(out, "$180,000 - $230,000 USD (varies by location)")
        self.assertNotIn("CAD", out.replace("USD", ""))

    def test_equity_directly_in_front_of_the_figures_is_not_pay(self):
        # real shape from an Affirm posting: the label names the figures, so no pay word further
        # back may vouch for them
        self.assertIsNone(pay_from_text(
            "Compensation and benefits for this role. Equity Grade - 2. "
            "New hire equity: $16,000-$24,000. Annual Refresh: $5,000."))
        self.assertIsNone(pay_from_text("Compensation. Commission: $5,000 - $10,000 per quarter."))

    def test_saying_excluding_equity_does_not_cost_the_listing_its_pay(self):
        # the first draft of the label rule rejected these 12 real listings; the words about
        # equity are not the label for the figures
        for t, want in (
            ("Compensation. Annual base salary range (excluding equity and bonus):  $135,320 - $159,200 USD",
             "$135,320 - $159,200 USD"),
            ("Compensation. Base Salary  $248,000 - $310,000 USD   Why us?", "$248,000 - $310,000 USD"),
            ("Compensation. The base salary range is $110,000-$150,000 USD.", "$110,000 - $150,000 USD"),
        ):
            self.assertEqual(pay_from_text(t), want, t)


if __name__ == "__main__":
    unittest.main()
