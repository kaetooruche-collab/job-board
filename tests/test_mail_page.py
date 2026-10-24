"""mail.html (the private reply-templates page) must stay in step with the copy and stay private."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import build_mail_page  # noqa: E402
import email_data as ed  # noqa: E402


class MailPage(unittest.TestCase):
    def test_page_is_up_to_date_with_the_copy(self):
        self.assertEqual((ROOT / "mail.html").read_text(encoding="utf-8"), build_mail_page.build(),
                         "run: python3 scripts/build_mail_page.py")

    def test_every_service_email_is_on_the_page(self):
        page = (ROOT / "mail.html").read_text(encoding="utf-8")
        for e in ed.EMAILS:
            if e["cls"] == "O":
                self.assertIn(f'"id": "{e["id"]}"', page, e["id"])

    def test_page_is_private_and_has_no_tracking(self):
        page = (ROOT / "mail.html").read_text(encoding="utf-8")
        self.assertIn('name="robots" content="noindex, nofollow"', page)
        self.assertNotIn("goatcounter", page.lower())
        self.assertNotIn("fetch(", page)
        self.assertNotIn("XMLHttpRequest", page)
        self.assertIn('"source": "/mail"', (ROOT / "vercel.json").read_text(encoding="utf-8").replace('": "', '": "'))

    def test_package_token_reads_naturally(self):
        # the package field inserts "Essential package", so the copy must not say "your payment for Essential package"
        self.assertNotIn("payment for [Package]", (ROOT / "scripts" / "email_data.py").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
