"""Guards for the Whop card-checkout buttons: config shape, page markup, thanks page and the monitor rule."""
import json
import re
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import site_monitor  # noqa: E402

CONFIG = (ROOT / "site-config.js").read_text()
SERVICES = (ROOT / "services.html").read_text()
THANKS = (ROOT / "thanks.html").read_text()
PLAN_PATH = r"/checkout/(plan|ch)_[A-Za-z0-9]+/?$"


def config_values():
    mode = re.search(r"checkout:\s*\{[^}]*?mode:\s*'(\w+)'", CONFIG, re.S).group(1)
    urls = dict(re.findall(r"(essential|professional):\s*'(https?://[^']*)'", CONFIG))
    return mode, urls


def run_check(config_js, services_html="<p>Pay by card</p>"):
    site_monitor.fails.clear()
    site_monitor.warns.clear()
    with mock.patch.object(site_monitor, "get", lambda path, **kw: SimpleNamespace(text=config_js)):
        site_monitor.check_checkout(services_html)
    return list(site_monitor.fails), list(site_monitor.warns)


def cfg(mode, a, b):
    return f"const SITE={{checkout:{{mode:'{mode}',essential:'{a}',professional:'{b}'}}}};"


class CheckoutFiles(unittest.TestCase):
    def test_config_mode_and_urls_are_well_formed(self):
        mode, urls = config_values()
        self.assertIn(mode, {"off", "sandbox", "live"})
        self.assertEqual(set(urls), {"essential", "professional"})
        self.assertNotEqual(mode, "sandbox", "sandbox mode must never be on the public site")
        host = {"live": "whop.com", "sandbox": "sandbox.whop.com"}.get(mode)
        for plan, url in urls.items():
            if host:
                self.assertRegex(url, rf"^https://{re.escape(host)}{PLAN_PATH}", plan)
        self.assertNotEqual(urls["essential"], urls["professional"])

    def test_no_secret_in_client_files(self):
        for text in (CONFIG, SERVICES, THANKS):
            self.assertIsNone(re.search(r"(apik_|sk_live|sk_test|Bearer\s+[A-Za-z0-9_\-]{20,})", text))

    def test_pay_buttons_are_hidden_until_script_validates_them(self):
        for plan in ("essential", "professional"):
            tag = re.search(rf'<a [^>]*data-pay="{plan}"[^>]*>', SERVICES).group(0)
            self.assertIn(" hidden", tag)
            self.assertIn('href="#"', tag)
            self.assertIn(f'data-wa-order="{plan}"', SERVICES)  # WhatsApp ordering stays as the fallback

    def test_only_essential_and_professional_get_pay_buttons(self):
        self.assertEqual(set(re.findall(r'data-pay="(\w+)"', SERVICES)), {"essential", "professional"})

    def test_services_no_longer_says_no_checkout_and_keeps_prices(self):
        self.assertNotIn("no online checkout", SERVICES.lower())
        for price in ("$29", "$49", "$149", "$99"):
            self.assertIn(price, SERVICES)

    def test_card_payment_copy_is_hidden_unless_the_buttons_are_live(self):
        # whatever says "pay by card" in sentences must sit inside data-card-copy (hidden by default), with a WhatsApp-only twin
        self.assertIn("data-wa-only", SERVICES)
        for m in re.finditer(r"<[^>]*data-card-copy[^>]*>", SERVICES):
            self.assertIn("hidden", m.group(0))
        for phrase in ("can be paid by card on a secure checkout page", "Pay by card on the secure checkout page"):
            i = SERVICES.index(phrase)
            self.assertIn("data-card-copy", SERVICES[max(0, i - 200):i])

    def test_copy_does_not_promise_usd_only_card_checkout(self):
        # Whop adaptive pricing shows buyers their local currency at card checkout (KT decision, 23 Oct).
        self.assertNotIn("all prices are in usd", SERVICES.lower())
        self.assertIn("your own currency", SERVICES)

    def test_thanks_page_is_noindex_and_claims_nothing_verified(self):
        self.assertRegex(THANKS, r'<meta name="robots" content="[^"]*noindex')
        low = THANKS.lower()
        for phrase in ("payment received", "payment confirmed", "order confirmed", "you have paid", "guaranteed"):
            self.assertNotIn(phrase, low)
        self.assertIn("yirehcareers@gmail.com", THANKS)
        self.assertIn("Reached this page without paying", THANKS)

    def test_vercel_sends_noindex_header_for_thanks(self):
        rules = [h for h in json.loads((ROOT / "vercel.json").read_text())["headers"] if h["source"] == "/thanks"]
        self.assertTrue(rules and any(x["key"] == "X-Robots-Tag" and "noindex" in x["value"] for x in rules[0]["headers"]))


class MonitorCheckoutRule(unittest.TestCase):
    def test_accepts_live_whop_urls(self):
        fails, _ = run_check(cfg("live", "https://whop.com/checkout/plan_AAA111", "https://whop.com/checkout/plan_BBB222/"))
        self.assertEqual(fails, [])

    def test_rejects_sandbox_mode_on_live_site(self):
        fails, _ = run_check(cfg("sandbox", "https://sandbox.whop.com/checkout/plan_AAA", "https://sandbox.whop.com/checkout/plan_BBB"))
        self.assertTrue(any("sandbox" in f for f in fails))

    def test_rejects_live_mode_with_bad_or_foreign_urls(self):
        for bad in ("https://sandbox.whop.com/checkout/plan_AAA", "https://evil.example/checkout/plan_AAA", "https://whop.com/", "http://whop.com/checkout/plan_AAA"):
            fails, _ = run_check(cfg("live", bad, "https://whop.com/checkout/plan_BBB"))
            self.assertTrue(fails, bad)

    def test_off_mode_is_accepted_with_no_warnings(self):
        fails, warns = run_check(cfg("off", "", ""))
        self.assertEqual((fails, warns), ([], []))


if __name__ == "__main__":
    unittest.main()
