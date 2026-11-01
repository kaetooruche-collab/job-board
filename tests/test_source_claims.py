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
ATS_HOSTS = ("greenhouse.io", "lever.co", "ashbyhq.com")


class SourceClaims(unittest.TestCase):
    def test_no_live_surface_says_links_go_to_the_employers_own_page(self):
        for f in LIVE:
            text = (ROOT / f).read_text(encoding="utf-8")
            m = OVERSTATES.search(text)
            self.assertIsNone(m, f"{f}: {m.group(0) if m else ''}")

    def test_the_hiring_systems_are_named_where_sources_are_disclosed_not_in_the_hero(self):
        for f in ("index.html", "verify.html"):
            t = (ROOT / f).read_text(encoding="utf-8")
            for name in ("Greenhouse", "Lever", "Ashby"):
                self.assertIn(name, t, f)
        self.assertIn("original posting", (ROOT / "index.html").read_text(encoding="utf-8"))
        self.assertIn("id=\"where-from\"", (ROOT / "verify.html").read_text(encoding="utf-8"))

    @unittest.skipIf(os.environ.get("GITHUB_WORKFLOW") == "Refresh job listings",
                     "data-dependent: must never block a refresh; it is a tripwire for people changing sources")
    def test_the_sourcing_claim_matches_the_data(self):
        """If this fails, a source other than the three hiring systems was added: update the wording before shipping."""
        rows = json.loads((ROOT / "jobs.json").read_text(encoding="utf-8"))
        off = [r["sourceUrl"] for r in rows if not any(h in urllib.parse.urlparse(r["sourceUrl"]).netloc for h in ATS_HOSTS)]
        self.assertEqual(off, [], f"{len(off)} listings link somewhere other than Greenhouse, Lever or Ashby, e.g. {off[:2]}")
        self.assertLessEqual({r["sourceName"] for r in rows}, {"Greenhouse", "Lever", "Ashby"})


if __name__ == "__main__":
    unittest.main()
