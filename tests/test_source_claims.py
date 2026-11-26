"""Where listings come from, stated accurately (KT, 1 Nov 2026).

Facts (measured 1 Nov): all 1,001 apply links open the posting on a Greenhouse, Lever or Ashby hosted page; none are on an employer's own
domain. So "links to the employer's own posting / page" and "direct link to the employer" overstate it: a reader can take them to mean the
employer's own website. The accurate claim is: postings are read from companies' own public hiring pages (Greenhouse, Lever, Ashby), and each
link opens the original posting there. Why it matters: advertising law judges the overall impression, not only literal words (FTC net
impression; EU Unfair Commercial Practices Directive art. 6 and 7). See drafts/decisions/2026-11-01-source-and-link-wording.md."""
import json, os, pathlib, re, unittest, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
LIVE = ["index.html", "services.html", "verify.html", "privacy.html", "thanks.html", "subscribed.html", "free-check.html", "order.html",
        "kit.html", "site-config.js", "scripts/email_data.py", "scripts/make_outputs.py", "scripts/build_brand_assets.py", "data/whatsapp_post.txt"]
OVERSTATES = re.compile(r"employer.{0,8}s own (?:posting|page|site)|direct(?:ly)? (?:link )?to the employer|straight to the employer|"
                        r"links? straight to the employer|employer.{0,8}s own link", re.I)
ATS_HOSTS = ("greenhouse.io", "lever.co", "ashbyhq.com", "jobs.personio.de", "jobs.personio.com")


class SourceClaims(unittest.TestCase):
    def test_no_live_surface_says_links_go_to_the_employers_own_page(self):
        for f in LIVE:
            text = (ROOT / f).read_text(encoding="utf-8")
            m = OVERSTATES.search(text)
            self.assertIsNone(m, f"{f}: {m.group(0) if m else ''}")

    def test_no_public_surface_promises_a_6_hourly_update(self):
        """Measured 18-25 Nov 2026: GitHub runs the "6-hourly" refresh every 10-16 hours. The site says "daily"."""
        for f in LIVE:
            text = (ROOT / f).read_text(encoding="utf-8")
            self.assertNotRegex(text, r"(?i)every 6 hours|every six hours", f)

    def test_no_public_page_uses_the_retired_eligibility_label(self):
        """KT, 25 Nov 2026: "Eligibility unclear can't keep appearing." Cards say "Location not specified"; a UX audit on 26 Nov
        found the old label still on /verify. The data may keep it (card-text.js turns it into plain words); pages may not."""
        for f in [x for x in LIVE if x.endswith(".html")]:
            text = (ROOT / f).read_text(encoding="utf-8")
            for retired in ("Eligibility unclear", "Remote: not confirmed", "Why this label"):
                self.assertNotIn(retired, text, f"{f}: {retired}")

    def test_no_public_surface_names_a_hiring_system(self):
        """KT, 25 Nov 2026: "don't mention greenhouse, lever, ashby, recruitee or personio. there is no reason to mention
        any of them or include any of them." Cards say "Source: the company's hiring page" instead."""
        names = re.compile(r"\b(?:Greenhouse|Lever|Ashby|Recruitee|Personio|Workable)\b")
        for f in LIVE:
            text = (ROOT / f).read_text(encoding="utf-8")
            if f.endswith(".py"):  # scripts: only the strings they write for readers count
                text = "\n".join(re.findall(r"f?\"[^\"\n]*\"|f?'[^'\n]*'", text))
            m = names.search(text)
            self.assertIsNone(m, f"{f}: names {m.group(0) if m else ''}")
        self.assertIn("original posting", (ROOT / "index.html").read_text(encoding="utf-8"))
        self.assertIn("id=\"where-from\"", (ROOT / "verify.html").read_text(encoding="utf-8"))
        self.assertIn("Source: the company\\u2019s hiring page", (ROOT / "index.html").read_text(encoding="utf-8"))

    @unittest.skipIf(os.environ.get("YC_SKIP_LIVE_DATA") == "1",
                     "data-dependent: must never block a refresh; it is a tripwire for people changing sources")
    def test_the_sourcing_claim_matches_the_data(self):
        """If this fails, a source other than the three hiring systems was added: update the wording before shipping."""
        rows = json.loads((ROOT / "jobs.json").read_text(encoding="utf-8"))
        # Recruitee careers pages may sit on the company's own domain, so only the other systems are checked by host
        off = [r["sourceUrl"] for r in rows if r["sourceName"] != "Recruitee"
               and not any(h in urllib.parse.urlparse(r["sourceUrl"]).netloc for h in ATS_HOSTS)]
        self.assertEqual(off, [], f"{len(off)} listings link somewhere other than a hiring-system page, e.g. {off[:2]}")
        self.assertLessEqual({r["sourceName"] for r in rows}, {"Greenhouse", "Lever", "Ashby", "Recruitee", "Personio"})


if __name__ == "__main__":
    unittest.main()
