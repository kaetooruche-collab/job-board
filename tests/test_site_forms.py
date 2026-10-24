"""The website's forms must go through /api/subscribe (consent evidence, blocklist protection) and nowhere else."""
import os, re, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read(n):
    return open(os.path.join(ROOT, n), encoding="utf-8").read()


class Forms(unittest.TestCase):
    def test_no_page_posts_straight_to_brevo(self):
        for n in ["index.html", "services.html", "free-check.html", "order.html", "subscribed.html", "site-config.js", "site-forms.js"]:
            self.assertNotIn("sibforms.com", read(n), n)

    def test_forms_use_the_shared_handler_and_have_a_honeypot(self):
        for n, kind in [("index.html", "signup"), ("free-check.html", "check"), ("order.html", "order")]:
            t = read(n)
            self.assertIn(f"submitSiteForm(event, '{kind}')", t, n)
            self.assertIn('name="website"', t, n)
            self.assertIn("site-forms.js", t, n)

    def test_tips_box_is_never_pre_ticked(self):
        for n in ["index.html", "free-check.html", "order.html"]:
            for m in re.finditer(r'<input[^>]*name="tips"[^>]*>', read(n)):
                self.assertNotIn("checked", m.group(0), n)

    def test_consent_wording_is_the_approved_text_on_all_three_forms(self):
        text = "Also send me occasional CV and LinkedIn tips, and Yireh Careers service offers. Roughly twice a month at most. You can unsubscribe in any email. This is separate from"
        for n in ["index.html", "free-check.html", "order.html"]:
            self.assertIn(text, read(n), n)

    def test_order_and_confirmation_pages_are_noindex(self):
        for n in ["order.html", "subscribed.html"]:
            self.assertIn('content="noindex, nofollow"', read(n), n)

    def test_privacy_page_describes_the_new_purposes(self):
        t = read("privacy.html")
        for needle in ["CV and LinkedIn tips and offers", "Order details form", "do-not-email list", "jobs only"]:
            self.assertIn(needle, t)

    def test_free_check_promise_has_real_numbers(self):
        for n in ["free-check.html", "services.html"]:
            t = read(n)
            self.assertIn("about 10 a week", t, n)
            self.assertIn("within 2 working days", t, n)
            self.assertNotIn("limited number", t, n)

    def test_no_secret_in_client_files(self):
        for n in ["index.html", "free-check.html", "order.html", "site-forms.js", "site-config.js"]:
            self.assertNotIn("xkeysib", read(n), n)


if __name__ == "__main__":
    unittest.main()
