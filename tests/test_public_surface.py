"""Internal files must not be served by the public site; the files the site really loads must stay served (KT, 31 Oct 2026)."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IGNORED = (ROOT / ".vercelignore").read_text(encoding="utf-8").split()


class PublicSurface(unittest.TestCase):
    def test_internal_material_is_not_deployed(self):
        for item in ("drafts", "jobsearch", "research", "CLAUDE.md", "scripts", "tests", ".github", "data/qa_report.md", "data/removed.log"):
            self.assertIn(item, IGNORED, item)

    def test_everything_the_site_loads_is_still_deployed(self):
        for needed in ("jobs.json", "data/geo_lexicon.json", "api", "fonts", "images", "index.html", "services.html", "search.js", "site-forms.js", "site-config.js", "yc-logo.png"):
            self.assertNotIn(needed, IGNORED, needed)
            self.assertFalse(any(needed.startswith(i + "/") for i in IGNORED), needed)


if __name__ == "__main__":
    unittest.main()
