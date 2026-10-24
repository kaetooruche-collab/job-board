"""Read-only audit of the Brevo account against the email-system design (drafts/email-system/06-brevo-architecture.md).

Run: BREVO_API_KEY=... python3 scripts/email_audit.py
Never writes. Never prints the key or full email addresses. Exit code 1 if a HARD rule is broken, 0 otherwise.
HARD rules: the account is the expected one; the four lists exist; nobody on 'Career tips' lacks CONSENT_TIPS_AT; every Brevo
email template has the unsubscribe tag and the postal address. Everything else is reported as a note.
The key may be the plain `xkeysib-...` key or the base64 text Brevo displays (`eyJ...`); both work.
Brevo's /senders endpoints reject the default Python User-Agent, so a normal one is sent.
"""
import base64
import json
import os
import sys
import urllib.error
import urllib.request

BASE = "https://api.brevo.com/v3"
EXPECTED_COMPANY = "KAYZ Global Ltd"
LISTS = ["Job alerts", "Career tips", "Check result sent", "Order completed"]
RETIRED_LISTS = ["Free CV check requested", "Customers: Essential", "Customers: Professional", "Customers: Executive",
                 "LinkedIn Growth: active", "Do not send", "Job alert subscribers"]
ATTRIBUTES = ["CONSENT_JOBS_AT", "CONSENT_JOBS_SRC", "CONSENT_TIPS_AT", "CONSENT_TIPS_SRC", "LEVEL_INTEREST", "STAGE", "LAST_PACKAGE", "COMPLETED_ON"]
TEMPLATE_PREFIX = "YC2 | "
ADDRESS_FRAGMENT = "Yenice Sokak"


def load_key(env=None):
    k = (env or os.environ).get("BREVO_API_KEY", "").strip()
    if k.startswith("eyJ"):
        try:
            k = json.loads(base64.b64decode(k + "=" * (-len(k) % 4)))["api_key"]
        except Exception:
            raise SystemExit("BREVO_API_KEY looks like the base64 text but could not be decoded")
    if not k.startswith("xkeysib-"):
        raise SystemExit("BREVO_API_KEY is missing or not a Brevo key (expected xkeysib-...)")
    return k


def make_call(key):
    def call(path):
        req = urllib.request.Request(BASE + path, headers={"api-key": key, "accept": "application/json", "user-agent": "curl/8.5.0"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.status, json.loads(r.read().decode() or "{}")
        except urllib.error.HTTPError as e:
            try:
                return e.code, json.loads(e.read().decode())
            except Exception:
                return e.code, {}
    return call


def mask(email):
    return (email[:1] + "***@" + email.split("@")[-1]) if "@" in email else "***"


def all_contacts(call, page=500):
    out, offset = [], 0
    while True:
        s, b = call(f"/contacts?limit={page}&offset={offset}")
        if s != 200:
            raise RuntimeError(f"contacts read failed: {s}")
        rows = b.get("contacts", [])
        out += rows
        if len(rows) < page:
            return out
        offset += page


def audit(call):
    """Returns (hard_failures, notes). `call(path)` returns (status, json)."""
    hard, notes = [], []
    s, acc = call("/account")
    if s != 200 or acc.get("companyName") != EXPECTED_COMPANY:
        return [f"account check failed (status {s}, company {acc.get('companyName')!r})"], notes
    s, b = call("/contacts/lists?limit=50")
    lists = {l["name"]: l for l in b.get("lists", [])}
    for n in LISTS:
        if n not in lists:
            hard.append(f"list missing: {n}")
    for n in RETIRED_LISTS:
        if n in lists:
            notes.append(f"retired list still present: {n}")
    s, b = call("/contacts/attributes")
    have = {a["name"] for a in b.get("attributes", [])}
    for a in ATTRIBUTES:
        if a not in have:
            hard.append(f"attribute missing: {a}")
    # templates: unsubscribe tag and address
    s, b = call("/smtp/templates?limit=100")
    tpl = [t for t in b.get("templates", []) if t["name"].startswith(TEMPLATE_PREFIX)]
    if not tpl:
        notes.append("no YC2 templates found")
    for t in tpl:
        s, full = call(f"/smtp/templates/{t['id']}")
        html = full.get("htmlContent", "")
        if "{{ unsubscribe }}" not in html and "{{unsubscribe}}" not in html:
            hard.append(f"template {t['id']} ({t['name']}) has no unsubscribe tag")
        if ADDRESS_FRAGMENT not in html:
            hard.append(f"template {t['id']} ({t['name']}) has no postal address")
        if not t.get("isActive"):
            notes.append(f"template {t['id']} is inactive")
    # contacts and consent
    contacts = all_contacts(call)
    tips_id = lists.get("Career tips", {}).get("id")
    jobs_id = lists.get("Job alerts", {}).get("id")
    for c in contacts:
        ids = c.get("listIds", [])
        attrs = c.get("attributes", {})
        who = mask(c.get("email", ""))
        if tips_id in ids and not attrs.get("CONSENT_TIPS_AT"):
            hard.append(f"contact {who} is on Career tips with no CONSENT_TIPS_AT")
        if jobs_id in ids and not attrs.get("CONSENT_JOBS_AT"):
            notes.append(f"contact {who} is on Job alerts with no CONSENT_JOBS_AT (consent source unverified: no digest or promotion until confirmed)")
        if c.get("emailBlacklisted") and ids:
            notes.append(f"contact {who} is blocklisted but still on {len(ids)} list(s) (Brevo will not send; check it is intended)")
    notes.append(f"{len(contacts)} contact(s) in total")
    return hard, notes


def main():
    call = make_call(load_key())
    hard, notes = audit(call)
    for n in notes:
        print("note:", n)
    for h in hard:
        print("HARD:", h)
    print("RESULT:", "FAIL" if hard else "pass", f"({len(hard)} hard, {len(notes)} notes)")
    sys.exit(1 if hard else 0)


if __name__ == "__main__":
    main()
