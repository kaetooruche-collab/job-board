"""Every element the page script looks up by id must exist in the page.

Regression (26 Nov 2026, found while checking a UX audit): "Clear filters" still set a checkbox ("f-confirmed") that was
removed on 25 Nov, so the click threw "Cannot set properties of null" and the list never reset."""
import pathlib, re, unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ["index.html", "services.html", "verify.html", "free-check.html", "order.html", "kit.html", "privacy.html"]


class PageIds(unittest.TestCase):
    def test_every_looked_up_id_exists(self):
        for name in PAGES:
            f = ROOT / name
            if not f.exists():
                continue
            text = f.read_text(encoding="utf-8")
            used = set(re.findall(r"getElementById\(\s*['\"]([^'\"]+)['\"]\s*\)", text))
            # ids written in HTML, including ids inside HTML that the script builds as strings
            present = set(re.findall(r"\bid=\\?[\"']([^\"'\\]+)", text))
            self.assertEqual(sorted(used - present), [], f"{name}: script looks up ids that are not on the page")


if __name__ == "__main__":
    unittest.main()
