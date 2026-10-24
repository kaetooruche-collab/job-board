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


if __name__ == "__main__":
    unittest.main()
