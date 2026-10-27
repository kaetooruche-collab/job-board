"""The "Platforms you can sign up to" section is a fallback resource, not a destination:
it stays off the primary navigation, sits after our own signup and trust sections, is
labelled by kind, and is measured. Decision: drafts/decisions/2026-10-27-platforms-section.md."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = (ROOT / "index.html").read_text(encoding="utf-8")


class Platforms(unittest.TestCase):
    def test_it_is_not_in_the_primary_navigation_or_mobile_menu(self):
        nav = INDEX[INDEX.find("<nav>"):INDEX.find("</nav>")]
        self.assertNotIn("#platforms", nav, "the section must not be a top-level destination")
        start = INDEX.find('<div class="mobile-menu"')
        menu = INDEX[start:INDEX.find("</div>", start)]
        self.assertNotIn("#platforms", menu, "the section must not be in the mobile menu either")

    def test_it_is_reachable_from_the_footer(self):
        footer = INDEX[INDEX.find("<footer>"):]
        self.assertIn('href="#platforms"', footer)

    def test_it_sits_after_the_signup_and_trust_sections(self):
        subscribe = INDEX.find('id="subscribe"')
        verify = INDEX.find('id="how-we-verify"')
        platforms = INDEX.find('id="platforms"')
        self.assertGreater(platforms, -1)
        self.assertLess(subscribe, platforms, "email signup must come before the outbound links")
        self.assertLess(verify, platforms, "trust section must come before the outbound links")

    def test_outbound_clicks_and_section_views_are_measured(self):
        for needle in ["platform-click", "platform-view", 'data-platform="']:
            self.assertIn(needle, INDEX, needle)

    def test_boards_and_talent_marketplaces_are_labelled_apart(self):
        for p in json.loads((ROOT / "platforms.json").read_text(encoding="utf-8")):
            self.assertIn(p.get("type"), ("board", "marketplace"), p.get("name"))
            self.assertTrue(p["url"].startswith("https://"), p["name"])
            self.assertTrue(p.get("description"), p["name"])
        self.assertIn("Talent marketplaces", INDEX)
        self.assertIn("Job boards", INDEX)

    def test_the_section_does_not_claim_to_verify_external_listings(self):
        body = INDEX[INDEX.find('id="platforms"'):INDEX.find("<!-- REPORT -->")]
        self.assertNotIn("We verified each signup page", body)
        self.assertIn("we don&rsquo;t check their listings", body)


class FilteredUrls(unittest.TestCase):
    """Filter state round-trips through the URL without fanning out pageviews."""

    def test_canonical_is_declared(self):
        self.assertIn('rel="canonical" href="https://yirehcareers.vercel.app/"', INDEX)

    def test_filter_state_reads_from_and_writes_to_the_url(self):
        self.assertIn("function readURL()", INDEX)
        self.assertIn("function syncURL()", INDEX)
        self.assertIn("history.replaceState", INDEX)

    def test_level_deep_link_still_works(self):
        # the kit posts link with ?level=early; the accepted values must stay in readURL
        for lvl in ["early", "mid", "senior_plus"]:
            self.assertIn(f"'{lvl}'", INDEX[INDEX.find("function readURL()"):INDEX.find("function syncURL()")])


if __name__ == "__main__":
    unittest.main()