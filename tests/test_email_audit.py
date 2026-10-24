import base64, json, os, sys, unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
import email_audit as ea

GOOD_HTML = "<p>x</p>{{ unsubscribe }} Yenice Sokak"


def fake(contacts, html=GOOD_HTML, lists=None, company="KAYZ Global Ltd"):
    lists = lists if lists is not None else [{"id": 11, "name": "Job alerts"}, {"id": 18, "name": "Career tips"},
                                             {"id": 19, "name": "Check result sent"}, {"id": 20, "name": "Order completed"}]
    def call(path):
        if path == "/account": return 200, {"companyName": company}
        if path.startswith("/contacts/lists"): return 200, {"lists": lists}
        if path == "/contacts/attributes": return 200, {"attributes": [{"name": a} for a in ea.ATTRIBUTES]}
        if path.startswith("/smtp/templates?"): return 200, {"templates": [{"id": 74, "name": "YC2 | JA-1", "isActive": True}]}
        if path.startswith("/smtp/templates/"): return 200, {"htmlContent": html}
        if path.startswith("/contacts?"): return 200, {"contacts": contacts}
        return 404, {}
    return call


class Audit(unittest.TestCase):
    def test_clean_account_passes_with_notes(self):
        hard, notes = ea.audit(fake([{"email": "a@x.com", "listIds": [11], "attributes": {}}]))
        self.assertEqual(hard, [])
        self.assertTrue(any("no CONSENT_JOBS_AT" in n for n in notes))
        self.assertFalse(any("a@x.com" in n for n in notes))      # addresses are masked

    def test_tips_without_consent_is_hard_failure(self):
        hard, _ = ea.audit(fake([{"email": "b@x.com", "listIds": [18], "attributes": {}}]))
        self.assertTrue(any("Career tips" in h for h in hard))

    def test_tips_with_consent_passes(self):
        hard, _ = ea.audit(fake([{"email": "b@x.com", "listIds": [18], "attributes": {"CONSENT_TIPS_AT": "2026-10-24"}}]))
        self.assertEqual(hard, [])

    def test_template_without_unsubscribe_or_address_fails(self):
        hard, _ = ea.audit(fake([], html="<p>hi</p>"))
        self.assertEqual(len([h for h in hard if "template" in h]), 2)

    def test_wrong_account_stops(self):
        hard, _ = ea.audit(fake([], company="Someone Else"))
        self.assertTrue(hard and "account check failed" in hard[0])

    def test_missing_list_fails(self):
        hard, _ = ea.audit(fake([], lists=[{"id": 11, "name": "Job alerts"}]))
        self.assertEqual(len([h for h in hard if h.startswith("list missing")]), 3)

    def test_key_formats(self):
        plain = "xkeysib-" + "a" * 20
        self.assertEqual(ea.load_key({"BREVO_API_KEY": plain}), plain)
        wrapped = base64.b64encode(json.dumps({"api_key": plain}).encode()).decode()
        self.assertEqual(ea.load_key({"BREVO_API_KEY": wrapped}), plain)
        with self.assertRaises(SystemExit):
            ea.load_key({"BREVO_API_KEY": "nonsense"})


if __name__ == "__main__":
    unittest.main()
