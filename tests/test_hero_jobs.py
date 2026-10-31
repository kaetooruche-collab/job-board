"""The first screen must serve job discovery (KT, 31 Oct 2026, after a coworker's feedback).

Measured before the change (live, 1280x800): hero 557px, the packages block 669-1209px, the toolbar
(with Fields and More filters forced open on wide screens) 1241-2136px, first job card at 2,199px.
Competitors that convert (Remote OK, Remotive, Working Nomads) show jobs in the first screen.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = (ROOT / "index.html").read_text(encoding="utf-8")


class FirstScreen(unittest.TestCase):
    def test_hero_is_compact_and_states_the_unique_value(self):
        self.assertIn("Remote jobs that show <em>who can apply</em>", INDEX)
        self.assertIn('class="hero-facts"', INDEX)
        self.assertIn('id="total-jobs"', INDEX)
        self.assertNotIn("Every 6 hrs", INDEX)  # confused a first-time reader

    def test_services_block_comes_after_the_job_list_and_signup(self):
        self.assertGreater(INDEX.index('<section class="services"'), INDEX.index('id="job-list"'))
        self.assertGreater(INDEX.index('<section class="services"'), INDEX.index('id="subscribe"'))

    def test_filters_start_collapsed_on_every_screen_size(self):
        self.assertIn("document.getElementById('more-filters').open = false;", INDEX)
        self.assertIn("document.getElementById('fields-group').open = false;", INDEX)
        self.assertNotIn("window.innerWidth >= 720;\n      document.getElementById('more-filters')", INDEX)

    def test_the_search_toolbar_is_the_anchor_target_and_clears_the_header(self):
        self.assertIn('<div class="toolbar" id="jobs">', INDEX)
        self.assertIn(".toolbar { scroll-margin-top:", INDEX)

    def test_syncurl_keeps_the_hash_so_the_anchor_never_fights_filter_state(self):
        i = INDEX.find("function syncURL()")
        self.assertIn("location.hash", INDEX[i:i + 1200])

    def test_one_light_theme_for_every_visitor(self):
        for name in ("index.html", "services.html", "verify.html", "privacy.html", "thanks.html", "form-page.css"):
            self.assertNotIn("prefers-color-scheme", (ROOT / name).read_text(encoding="utf-8"), name)
        self.assertIn('<meta name="color-scheme" content="light">', INDEX)


if __name__ == "__main__":
    unittest.main()
