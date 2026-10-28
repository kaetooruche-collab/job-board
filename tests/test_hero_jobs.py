"""The hero must offer an above-the-fold route to the listings.

Evidence (28 Oct 2026, live site, 1440x900): the services block starts at 591px, the search box
at 1,182px and the first job card at 2,081px - 1,181px below the fold - while the hero contained
no link to any of it. On a 360x740 phone the first card was 945px below the fold. A job board
whose hero cannot reach the jobs in one tap inverts its own value exchange.
"""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = (ROOT / "index.html").read_text(encoding="utf-8")


class HeroRoutesToJobs(unittest.TestCase):
    def test_hero_has_a_link_to_the_listings(self):
        self.assertIn('class="hero-jobs-cta" href="#jobs"', INDEX)

    def test_the_anchor_target_exists_and_is_the_search_toolbar(self):
        self.assertIn('<div class="toolbar" id="jobs">', INDEX)

    def test_the_jump_is_measured(self):
        self.assertIn("trackEvent('jobs-hero-jump'", INDEX)

    def test_the_scroll_target_clears_the_fixed_header(self):
        self.assertIn(".toolbar { scroll-margin-top:", INDEX)

    def test_syncurl_keeps_the_hash_so_the_anchor_never_fights_filter_state(self):
        # filters live in the query string; clicking #jobs must not drop or reset them
        self.assertIn("location.hash", INDEX[INDEX.find("function syncURL()"):INDEX.find("function syncURL()") + 1200])


if __name__ == "__main__":
    unittest.main()
