"""Real postings that once broke the classifier. Add an entry every time a new kind of bug is found."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from classify import classify_listing, feed_decision  # noqa: E402

CASES = json.loads((ROOT / "tests" / "fixtures" / "regressions.json").read_text(encoding="utf-8"))


class Regressions(unittest.TestCase):
    def test_every_fixture(self):
        for c in CASES:
            with self.subTest(c["name"]):
                r = classify_listing(c["title"], c.get("location", ""), c["description"], hint=c.get("hint"), remote_feed=c.get("remote_feed", False))
                e, notes, ex = r["eligibility"], " | ".join(r["eligibility"]["notes"]), c["expect"]
                if ex.get("not_published"):
                    self.assertNotEqual(feed_decision(r)[0], "publish")
                if "level" in ex:
                    self.assertEqual(r["experience"]["level"], ex["level"])
                if "label" in ex:
                    self.assertEqual(e["label"], ex["label"])
                for s in ex.get("note_absent", []):
                    self.assertNotIn(s, notes)
                for s in ex.get("note_present", []):
                    self.assertIn(s, notes)
                for country in ex.get("countries_exclude", []):
                    self.assertNotIn(country, e["countries"])


if __name__ == "__main__":
    unittest.main()
