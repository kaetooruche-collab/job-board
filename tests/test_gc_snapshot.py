"""The weekly GoatCounter snapshot renders a dated markdown report with deltas, without touching the network."""
import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import gc_snapshot as gc

DATA = {
    "All time": {
        "views": 144,
        "events": 12,
        "pages": [{"path": "/", "count": 121}, {"path": "/services", "count": 8}],
        "event_rows": [
            {"path": "apply-click", "count": 1, "title": "j89a48738c3"},
            {"path": "conversion-check", "count": 2, "title": "Form submitted: check"},
        ],
    },
    "Last 7 days": {"views": 9, "events": 2, "pages": [], "event_rows": []},
}


class Render(unittest.TestCase):
    def test_report_has_headings_tables_and_machine_readable_totals(self):
        md = gc.render("2026-10-27", DATA, None)
        self.assertIn("# GoatCounter snapshot — 2026-10-27", md)
        self.assertIn("| Last 7 days | 9 | 2 |", md)
        self.assertIn("| 121 | `/` |", md)
        self.assertIn("`apply-click`", md)
        self.assertIn("Form submissions (conversion-*): **2**", md)
        self.assertIn("<!-- totals: views=144 events=12 date=2026-10-27 -->", md)

    def test_delta_against_a_previous_snapshot(self):
        prev = {"views": 144, "events": 10, "file": "GC-2026-10-20.md"}
        self.assertEqual(gc.delta(150, prev, "views"), "+6 since GC-2026-10-20.md")
        self.assertEqual(gc.delta(144, prev, "views"), "no change")
        self.assertEqual(gc.delta(100, prev, "views"), "-44 since GC-2026-10-20.md")

    def test_previous_totals_reads_the_newest_snapshot(self):
        original = gc.OUT_DIR
        with tempfile.TemporaryDirectory() as d:
            gc.OUT_DIR = pathlib.Path(d)
            try:
                (gc.OUT_DIR / "GC-2026-10-20.md").write_text(
                    "text\n<!-- totals: views=144 events=12 date=2026-10-20 -->\n",
                    encoding="utf-8",
                )
                found = gc.previous_totals()
                self.assertEqual((found["views"], found["events"]), (144, 12))
            finally:
                gc.OUT_DIR = original

    def test_previous_totals_is_none_when_no_snapshot_exists(self):
        original = gc.OUT_DIR
        with tempfile.TemporaryDirectory() as d:
            gc.OUT_DIR = pathlib.Path(d)
            try:
                self.assertIsNone(gc.previous_totals())
            finally:
                gc.OUT_DIR = original

    def test_the_api_key_never_appears_in_a_report(self):
        key = gc.load_key() or "absent-key-sentinel"
        md = gc.render("2026-10-27", DATA, None)
        self.assertNotIn(key, md)



class Referrers(unittest.TestCase):
    def test_referrer_section_renders_and_missing_data_is_harmless(self):
        d = {k: dict(v) for k, v in DATA.items()}
        d["All time"]["refs"] = [{"name": "facebook", "count": 7}]
        d["Last 7 days"]["refs"] = None
        md = gc.render("2026-11-03", d, None)
        self.assertIn("Where visitors came from (all time)", md)
        self.assertIn("| 7 | facebook |", md)
        self.assertIn("Referrer data could not be fetched", md)

class Funnel(unittest.TestCase):
    def test_funnel_groups_events_and_never_double_counts(self):
        w = {"views": 0, "events": 0,
             "pages": [{"path": "/", "count": 200}, {"path": "/services", "count": 30}],
             "event_rows": [
                 {"path": "apply-click", "count": 5}, {"path": "conversion-signup", "count": 4},
                 {"path": "cv-click-job-cv-button", "count": 3}, {"path": "cv-click-home-free-check", "count": 1},
                 {"path": "conversion-check", "count": 2}, {"path": "free-check-open-email", "count": 2},
                 {"path": "services-click-pay-professional", "count": 2}, {"path": "services-click-pricing-essential", "count": 1},
                 {"path": "services-click-home-packages", "count": 9},   # not a price or pay click
                 {"path": "conversion-order", "count": 1}, {"path": "filter-level", "count": 40}]}
        got = dict(gc.funnel_counts(w))
        self.assertEqual(got["Looked at jobs (home page views)"], 200)
        self.assertEqual(got["Clicked Apply on a job"], 5)
        self.assertEqual(got["Opened WhatsApp about a CV or free check"], 4)
        self.assertEqual(got["Looked at prices or pay buttons"], 3)
        self.assertEqual(got["Sent an order form"], 1)
        self.assertEqual(sum(got.values()), 200 + 5 + 4 + 4 + 2 + 2 + 3 + 1)

    def test_report_shows_funnel_rates_and_what_is_not_measured(self):
        d = {k: dict(v) for k, v in DATA.items()}
        md = gc.render("2026-11-03", d, None)
        self.assertIn("## Funnel", md)
        self.assertIn("| Joined the weekly email (form sent) | 0 | 0 |", md)
        self.assertIn("clicks and form submits, not people", md)
        self.assertIn("not in GoatCounter", md)

    def test_empty_windows_do_not_crash(self):
        self.assertEqual(sum(n for _, n in gc.funnel_counts({})), 0)
        self.assertEqual(sum(n for _, n in gc.funnel_counts(None)), 0)


if __name__ == "__main__":
    unittest.main()
