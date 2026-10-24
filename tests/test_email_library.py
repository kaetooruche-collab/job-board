"""Copy rules for the proposed email library (drafts/email-system). These tests check the rules in
drafts/voice-and-copy-guide.md and drafts/email-system/07-data-consent-event-model.md; they do not prove the copy is good."""
import os, re, sys, json, unittest, datetime as D

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "drafts", "email-system"))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import email_data as ed
import build_library as bl

BANNED = ["guarantee", "no work permit", "only job board", "perfect for", "hurry", "last chance", "limited time", "act now",
          "don't miss", "dont miss", "urgent", "expires", "countdown", "asap", "100%", "get you hired", "land you a job",
          "more interviews", "for students", "for graduates"]
PRICE_OK = {"OP-3", "OP-6", "OP-10"}          # service emails that may state a price: contract terms only
OFFER_WORDS = ["offer", "discount", "add-on", "upgrade", "special price", "% off"]
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿]")


class Library(unittest.TestCase):
    def test_ids_unique_and_classes_valid(self):
        ids = [e["id"] for e in ed.EMAILS]
        self.assertEqual(len(ids), len(set(ids)))
        for e in ed.EMAILS:
            self.assertIn(e["cls"], "SPO")

    def test_every_email_has_required_fields(self):
        need = ["id", "name", "cls", "channel", "journey", "audience", "purpose", "trigger", "entry", "consent", "timing",
                "subject", "preview", "body", "exit", "freq", "failure", "metric", "guardrail", "evidence", "confidence"]
        for e in ed.EMAILS:
            for k in need:
                self.assertIn(k, e, f"{e['id']} missing {k}")
            if e["cls"] != "O":
                self.assertTrue(e["preview"], f"{e['id']} needs preview text")

    def test_banned_phrases_and_tone(self):
        for e in ed.EMAILS:
            t = (e["subject"] + " " + e["preview"] + " " + bl.body_text(e)).lower()
            for b in BANNED:
                self.assertNotIn(b, t, f"{e['id']} contains '{b}'")
            self.assertLessEqual(t.count("!"), 1, e["id"])
            self.assertIsNone(EMOJI.search(t), e["id"])
            self.assertLessEqual(len(e["subject"]), 55, e["id"])

    def test_lengths(self):
        for e in ed.EMAILS:
            n = bl.words(bl.body_text(e))
            if e["cls"] in "SP":
                self.assertTrue(40 <= n <= 115, f"{e['id']} has {n} words")
            else:
                self.assertLessEqual(n, 130, f"{e['id']} has {n} words")

    def test_consent_matches_class(self):
        for e in ed.EMAILS:
            if e["cls"] == "P":
                self.assertTrue(e["consent"].startswith("Tips and offers"), e["id"])
            if e["cls"] == "S":
                self.assertTrue(e["consent"].startswith("Job alerts"), e["id"])
            if e["cls"] == "O":
                self.assertIn("None needed", e["consent"], e["id"])
                self.assertIn("Gmail", e["channel"], e["id"])

    def test_service_emails_carry_no_promotion(self):
        for e in ed.EMAILS:
            if e["cls"] != "O":
                continue
            self.assertIsNone(e.get("cta"), e["id"])
            t = bl.body_text(e).lower()
            self.assertNotIn("utm_", t)
            for w in OFFER_WORDS:
                self.assertNotIn(w, t, f"{e['id']} contains '{w}'")
            if e["id"] not in PRICE_OK:
                self.assertNotIn("$", t, f"{e['id']} states a price")

    def test_marketing_emails_have_one_cta_unsubscribe_and_address(self):
        for e in ed.EMAILS:
            if e["cls"] == "O":
                continue
            self.assertIsNotNone(e["cta"], e["id"])
            url = bl.cta_url(e)
            if url.startswith(ed.SITE):
                self.assertIn("utm_source=brevo", url)
                self.assertIn(f"utm_campaign={e['id'].lower()}", url)
                # the query string must come before any #fragment
                self.assertTrue(url.index("?") < (url.index("#") if "#" in url else 10 ** 9), url)
            doc = bl.render_html(e, preview_mode=False, digest_cards="", n_total=6, shown=6) if e["id"] == "JA-D" else bl.render_html(e, preview_mode=False)
            self.assertIn("{{ unsubscribe }}", doc, e["id"])
            self.assertIn("Kyrenia", doc, e["id"])
            self.assertIn('{{ contact.FIRSTNAME | default:"there" }}', doc, e["id"])
            self.assertEqual(doc.count('class="btn"'), 1, e["id"])
            self.assertIn("prefers-color-scheme: dark", doc)

    def test_no_founder_or_personal_name(self):
        for e in ed.EMAILS:
            t = bl.body_text(e)
            for name in ["KT", "Kaeto", "Oruche"]:
                self.assertNotIn(name, t, e["id"])

    def test_promotional_cap_design(self):
        # tips series timing: CT-1 day 1, CT-2 day 8, CT-3 day 17 after joining -> any 14-day window holds at most 2 emails
        days = [1, 8, 17]
        for start in range(0, 20):
            self.assertLessEqual(sum(1 for d in days if start <= d < start + 14), 2)


if __name__ == "__main__":
    unittest.main()
