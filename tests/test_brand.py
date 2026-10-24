"""The public pages must carry the current brand and none of the retired names, and share previews must work."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ["index.html", "services.html", "verify.html", "privacy.html", "thanks.html", "subscribed.html", "free-check.html", "order.html"]
RETIRED = ["kaeto", "kayz global ltd", "kt-photo.webp", "founder, "]
DOMAIN = "https://yirehcareers.vercel.app"


def page(name):
    return (ROOT / name).read_text(encoding="utf-8")


def visible(text):
    # strip the analytics subdomain (an account id, not visible wording)
    return text.replace("kayzglobal.goatcounter.com", "").replace("kayzglobal", "")


class Brand(unittest.TestCase):
    def test_retired_names_are_gone_from_public_pages(self):
        for n in PAGES + ["kit.html"]:
            low = visible(page(n)).lower()
            for w in RETIRED:
                self.assertNotIn(w, low, f"{n} still mentions {w!r}")
            self.assertNotIn("true<span>remote", low, n)

    def test_every_page_shows_the_new_logo(self):
        for n in PAGES:
            self.assertIn("Yireh <span>Careers</span>", page(n), n)

    def test_founder_photo_and_section_are_removed(self):
        self.assertFalse((ROOT / "kt-photo.webp").exists())
        self.assertNotIn("Who&rsquo;s behind this", page("services.html"))
        self.assertIn("How we work", page("services.html"))

    def test_privacy_page_does_not_claim_a_company(self):
        p = page("privacy.html")
        self.assertNotIn("Ltd", p)
        self.assertIn("not a registered company", p)

    def test_share_preview_tags_with_absolute_urls(self):
        for n, path in [("index.html", "/"), ("services.html", "/services"), ("verify.html", "/verify"), ("privacy.html", "/privacy")]:
            t = page(n)
            for prop in ("og:title", "og:description", "og:image", "og:url"):
                self.assertIn(f'property="{prop}"', t, f"{n} {prop}")
            self.assertIn(f'content="{DOMAIN}{path}"', t, n)
            self.assertIn(f'content="{DOMAIN}/og-image.png"', t, n)
            self.assertIn('name="twitter:card"', t, n)
        img = (ROOT / "og-image.png").read_bytes()
        self.assertEqual(img[:8], b"\x89PNG\r\n\x1a\n")
        w, h = int.from_bytes(img[16:20], "big"), int.from_bytes(img[20:24], "big")
        self.assertEqual((w, h), (1200, 630))

    def test_kit_is_unlisted_and_tags_its_links(self):
        k = page("kit.html")
        self.assertIn('name="robots" content="noindex, nofollow"', k)
        for src in ("whatsapp", "facebook", "tiktok", "snapchat"):
            self.assertIn(f"tag('{src}'", k)
        self.assertIn("utm_source=", k)
        script = k.split("<script>", 1)[1].lower()  # the text the posts are built from, not the rules box that tells KT what not to write
        for bad in ("guaranteed", "no work permit needed", "you will get", "get you noticed"):
            self.assertNotIn(bad, script)
        self.assertNotIn("gc.zgo.at", k)  # the analytics script must not be on the kit: opening it must not count as a visit

    def test_old_address_redirects_to_the_new_one(self):
        import json
        v = json.loads((ROOT / "vercel.json").read_text())
        red = v["redirects"][0]
        self.assertEqual(red["has"][0]["value"], "northcyprusremotejobboard.vercel.app")
        self.assertTrue(red["destination"].startswith(DOMAIN))
        self.assertFalse(red["permanent"])

    def test_no_country_or_city_in_the_public_address_or_name(self):
        self.assertNotIn("cyprus", DOMAIN)

    def test_jobicy_is_off(self):
        s = (ROOT / "scripts" / "fetch_jobs.py").read_text()
        self.assertIn("USE_JOBICY = False", s)


if __name__ == "__main__":
    unittest.main()
