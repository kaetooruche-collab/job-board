"""Crawl basics (31 Oct 2026): every public page has a canonical URL that matches the sitemap; private pages stay out of it."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = "https://yirehcareers.vercel.app"
PUBLIC = {"index.html": "/", "services.html": "/services", "verify.html": "/verify", "privacy.html": "/privacy", "free-check.html": "/free-check"}
PRIVATE = ("order", "subscribed", "thanks", "kit", "mail", "api")


class Crawl(unittest.TestCase):
    def test_robots_points_at_the_sitemap_and_blocks_only_the_api(self):
        r = (ROOT / "robots.txt").read_text(encoding="utf-8")
        self.assertIn(f"Sitemap: {DOMAIN}/sitemap.xml", r)
        self.assertIn("Disallow: /api/", r)
        for p in PRIVATE[:-1]:  # private pages rely on noindex; listing them in robots.txt would advertise them
            self.assertNotIn(f"/{p}", r)

    def test_sitemap_lists_exactly_the_public_pages(self):
        locs = re.findall(r"<loc>([^<]+)</loc>", (ROOT / "sitemap.xml").read_text(encoding="utf-8"))
        self.assertEqual(sorted(locs), sorted(DOMAIN + p for p in PUBLIC.values()))

    def test_each_public_page_has_the_matching_canonical(self):
        for f, path in PUBLIC.items():
            self.assertIn(f'<link rel="canonical" href="{DOMAIN}{path}">', (ROOT / f).read_text(encoding="utf-8"), f)


class Nav(unittest.TestCase):
    def test_header_cta_is_the_free_cv_check_and_services_stays_reachable(self):
        for f in ("index.html", "services.html", "verify.html", "privacy.html", "thanks.html"):
            t = (ROOT / f).read_text(encoding="utf-8")
            self.assertIn('class="nav-cta"', t, f)
            self.assertIn('href="/free-check"', t, f)
            self.assertNotIn("Get Job-Ready", t, f)
            self.assertIn(">Career services</a>", t, f)


if __name__ == "__main__":
    unittest.main()
