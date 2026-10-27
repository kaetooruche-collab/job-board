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


if __name__ == "__main__":
    unittest.main()