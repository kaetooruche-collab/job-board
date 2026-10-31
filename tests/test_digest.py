import os, sys, unittest, json, datetime as D

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
import make_digest as md


def job(i, company, level="mid", arr="fully_remote", elig="countries", age=1, label="United States only"):
    now = D.datetime(2026, 10, 24, tzinfo=D.timezone.utc)
    return {"id": f"j{i}", "title": f"Role {i}", "company": company, "level": level, "workArrangement": arr,
            "eligibility": {"type": elig, "label": label}, "salaryText": None, "sourceUrl": f"https://example.com/{i}",
            "postedAt": (now - D.timedelta(days=age)).isoformat()}


class Digest(unittest.TestCase):
    now = D.datetime(2026, 10, 24, tzinfo=D.timezone.utc)

    def rows(self):
        r = []
        for i, lv in enumerate(["junior", "junior", "junior", "mid", "mid", "senior", "senior", "leadership"]):
            r.append(job(i, f"Co{i}", level=lv, age=i % 5))
        r.append(job(20, "Co0", level="mid"))                       # same company as Co0: must not repeat
        r.append(job(21, "Old", age=12))                            # too old
        r.append(job(22, "Unsure", arr="remote_unclear"))           # remote not confirmed
        r.append(job(23, "NoElig", elig="unclear", label="Eligibility unclear"))
        r.append(job(24, "Open", level="junior", elig="worldwide", label="Worldwide"))
        return r

    def test_rules(self):
        sections, total = md.pick(self.rows(), self.now)
        shown = [r for _, items in sections for r in items]
        self.assertLessEqual(len(shown), md.TOTAL)
        self.assertEqual(len({r["company"].lower() for r in shown}), len(shown))
        for r in shown:
            self.assertIn(r["workArrangement"], ("fully_remote", "remote_geo_restricted"))
            self.assertNotEqual(r["eligibility"]["type"], "unclear")
            self.assertLessEqual((self.now - D.datetime.fromisoformat(r["postedAt"])).days, 7)
        self.assertIn("Open", [r["company"] for r in shown])         # worldwide is preferred

    def test_html_is_clean(self):
        doc, subject, preview, sections, total, now = md.build(self.rows(), self.now)
        low = (doc + subject + preview).lower()
        for banned in ["guarantee", "no work permit", "only job board", "perfect for"]:
            self.assertNotIn(banned, low)
        self.assertIn("{{ unsubscribe }}", doc)
        self.assertIn("https://example.com/", doc)

    def test_rename_note_is_optional_and_in_place(self):
        plain = md.build(self.rows(), self.now)[0]
        noted = md.build(self.rows(), self.now, rename_note=True)[0]
        self.assertNotIn("RemoteNC", plain)
        self.assertIn("RemoteNC is now Yireh Careers", noted)
        self.assertIn("{{ unsubscribe }}", noted)


    LEX = {"countries": [{"name": "Nigeria"}, {"name": "Germany"}, {"name": "Canada"}],
           "regions": {"Africa": {"members": ["Nigeria"]}, "EMEA": {"members": ["Nigeria", "Germany"]}}}

    def test_open_to_is_strict(self):
        ww = job(1, "A", elig="worldwide", label="Worldwide")
        ca = job(2, "B", elig="countries")
        ca["eligibility"]["countries"] = ["Canada"]
        reg = job(3, "C", elig="region")
        reg["eligibility"]["regions"] = ["Africa"]
        unknown_region = job(4, "D", elig="region")
        unknown_region["eligibility"]["regions"] = ["Nowhere"]
        unclear = job(5, "E", elig="unclear")
        tz = job(6, "F", elig="timezone")
        self.assertTrue(md.open_to(ww, "Nigeria", self.LEX))
        self.assertFalse(md.open_to(ca, "Nigeria", self.LEX))
        self.assertTrue(md.open_to(ca, "Canada", self.LEX))
        self.assertTrue(md.open_to(reg, "Nigeria", self.LEX))
        self.assertFalse(md.open_to(reg, "Germany", self.LEX))
        self.assertFalse(md.open_to(unknown_region, "Nigeria", self.LEX))   # the site is lenient here; an email must not be
        self.assertFalse(md.open_to(unclear, "Nigeria", self.LEX))
        self.assertFalse(md.open_to(tz, "Nigeria", self.LEX))

    def test_coverage_counts_only_recent_remote_roles(self):
        rows = self.rows()
        counts, total = md.coverage(rows, self.now, self.LEX)
        self.assertEqual(counts["Nigeria"], 1)           # only the worldwide one
        self.assertGreaterEqual(counts["Canada"], 1)
        self.assertEqual(list(counts.values()), sorted(counts.values(), reverse=True))

    def test_country_edition_only_has_open_roles_and_says_why(self):
        rows = []
        for i in range(5):
            rows.append(job(i, f"Ww{i}", level=["junior", "mid", "senior", "mid", "junior"][i], elig="worldwide", label="Worldwide"))
        for i in range(5, 9):
            r = job(i, f"Us{i}", level="mid")
            r["eligibility"]["countries"] = ["United States"]
            rows.append(r)
        import unittest.mock as mock
        with mock.patch.object(md, "load_lexicon", return_value=self.LEX):
            doc, subject, preview, sections, total, now = md.build(rows, self.now, country="Nigeria")
        shown = [r for _, items in sections for r in items]
        self.assertTrue(shown)
        self.assertTrue(all(r["company"].startswith("Ww") for r in shown))
        self.assertEqual(total, 5)
        self.assertIn("You told us you can work from Nigeria", doc)
        self.assertIn("Check each employer", doc)
        self.assertIn("{{ unsubscribe }}", doc)
        self.assertEqual(subject, "5 new remote jobs this week")


if __name__ == "__main__":
    unittest.main()
