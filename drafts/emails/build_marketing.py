"""Builds the Yireh Careers lifecycle (marketing) emails into drafts/emails/marketing/ and a review sheet.
Run: python3 drafts/emails/build_marketing.py
Voice: drafts/voice-and-copy-guide.md. Punchy, brief, warm; one call to action; honest (no fake urgency, no outcome promises).
Merge variable: {{ contact.FIRSTNAME | default:"there" }} (marketing automations use contact attributes, not params)."""
import os, html, json, urllib.parse
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "marketing")
os.makedirs(OUT, exist_ok=True)
SITE = "https://yirehcareers.vercel.app"
WA = "905338225854"
ADDR = "Yireh Careers · Yenice Sokak, 99300 Kyrenia, Cyprus"

def utm(path, camp):
    return f"{SITE}{path}{'&' if '?' in path else '?'}utm_source=brevo&utm_medium=email&utm_campaign={camp}"

def wa(text, camp=None):
    return f"https://wa.me/{WA}?text=" + urllib.parse.quote(text)

HI = 'Hi {{ contact.FIRSTNAME | default:"there" }},'

def wrap(preheader, body_html, cta_label, cta_url):
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light dark"><meta name="supported-color-schemes" content="light dark">
<title>Yireh Careers</title>
<style>
@media (prefers-color-scheme: dark){{ .bg{{background:#0b1220!important}} .card{{background:#131c2e!important}} .tx{{color:#e6ebf5!important}} }}
@media only screen and (max-width:620px){{ .wrap{{width:100%!important}} .pad{{padding:22px 18px!important}} }}
</style></head>
<body class="bg" style="margin:0;padding:0;background:#eef2f8;">
<div style="display:none;max-height:0;overflow:hidden;opacity:0;">{html.escape(preheader, quote=False)}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" class="bg" style="background:#eef2f8;"><tr><td align="center" style="padding:24px 12px;">
<table role="presentation" class="wrap" width="600" cellpadding="0" cellspacing="0" style="width:600px;max-width:100%;">
<tr><td style="background:#0f2a4d;padding:18px 28px;border-radius:12px 12px 0 0;font:700 20px Arial,Helvetica,sans-serif;color:#ffffff;">Yireh Careers</td></tr>
<tr><td class="card pad" style="background:#ffffff;padding:28px;font:16px/1.65 Arial,Helvetica,sans-serif;color:#1b2536;">
<div class="tx">{body_html}
<p style="margin:22px 0 22px;"><a href="{cta_url}" style="display:inline-block;background:#1d4f91;color:#ffffff;text-decoration:none;font-weight:700;padding:13px 24px;border-radius:8px;">{cta_label}</a></p>
<p style="margin:0;">Thanks,<br><strong>The Yireh Careers team</strong></p></div></td></tr>
<tr><td style="background:#0f2a4d;padding:18px 28px;border-radius:0 0 12px 12px;font:12.5px/1.6 Arial,Helvetica,sans-serif;color:#b9cdea;">
<p style="margin:0;">Reply to this email any time, or message us on WhatsApp: <a href="https://wa.me/{WA}" style="color:#9db4d6;">+90 533 822 5854</a></p>
<p style="margin:6px 0 0;">{ADDR}</p>
<p style="margin:6px 0 0;">You're getting this because you signed up with Yireh Careers. <a href="{{{{ unsubscribe }}}}" style="color:#9db4d6;">Unsubscribe</a></p></td></tr>
</table></td></tr></table></body></html>"""

def P(t): return f'<p style="margin:0 0 14px;">{t}</p>'
def UL(items): return '<ul style="margin:0 0 14px;padding-left:20px;">' + ''.join(f'<li style="margin:0 0 6px;">{i}</li>' for i in items) + '</ul>'

CHECK_MSG = "Hello, I found you through your email and would like a free quick CV check."
E = []  # (id, flow, when, subject, preheader, body_html, cta_label, cta_url, notes)

E.append(("W1", "Welcome", "Day 0, right after sign-up (add to list: Job alert subscribers)",
  "You're in. Here's your first move", "Every job links to the employer's own posting.",
  P(HI) + P("Job hunting can feel like shouting into the void. We built Yireh Careers to make it a little less confusing.") +
  P("Every job here links straight to the employer's own posting, shows when it went up, and says who can apply. Each week we'll send you the newest ones.") +
  P("<strong>Your first move:</strong> open the board and pick your level."),
  "Browse remote jobs", utm("/", "welcome-1"), "Replaces template 40."))

E.append(("W2", "Welcome", "Day 3",
  "The 30-second check that saves hours", "Before you spend an evening on an application.",
  P(HI) + P("Nothing stings like a long application for a job you can't take. Before you apply, check three things:") +
  UL(["<strong>Who can apply.</strong> Each card says. If it says unclear, ask the employer.",
      "<strong>When it was posted.</strong> Newer postings are more likely to still be open.",
      "<strong>Whether it's really remote.</strong> We mark each job as confirmed or not."]) +
  P("Thirty seconds now can save you an evening."),
  "Open the board", utm("/", "welcome-2"), "No promotion: pure value."))

E.append(("W3", "Welcome", "Day 7 (skip if they are already in any Customers list)",
  "Applying and hearing nothing?", "A free CV check. Three fixes, no strings.",
  P(HI) + P("Sending applications and hearing nothing is exhausting. Sometimes it's the CV.") +
  P("Email us yours and we'll send back the three things we'd fix first. It's free, once per person, and we delete your CV after 30 days if you don't order.") +
  P("No pressure. Your job alerts keep coming either way."),
  "Get my free CV check", wa(CHECK_MSG), "First soft offer. One legal fact (30-day deletion), once."))

E.append(("F1", "Free CV check follow-up", "Day 3 after the check was sent (add to list: Free CV check requested, on the day you send the result)",
  "Did the three fixes help?", "Quick check-in from us.",
  P(HI) + P("A quick check-in. Did our three fixes make sense?") +
  P("If you'd rather we just did it for you, <strong>Essential ($29)</strong> is a full CV, and <strong>Professional ($49)</strong> adds a cover letter and LinkedIn setup.") +
  P("Questions? Just reply."),
  "See what's included", utm("/services", "checkfollow-1"), ""))

E.append(("F2", "Free CV check follow-up", "Day 8 (skip if they ordered)",
  "Still thinking it over?", "No rush. Two honest answers.",
  P(HI) + P("No rush at all. Two honest answers to the usual worries:") +
  UL(["<strong>Cost?</strong> Essential is $29, and your free check is yours to keep either way.",
      "<strong>Time?</strong> We do the writing. You send your CV and the roles you want."]) +
  P("If it's something else, tell us. We'd rather know."),
  "Chat with us", wa("Hello, I had a free CV check and have a question about the packages."), "Last email in the flow. Exit after this."))

E.append(("P1", "After an order (Essential / Professional / Executive)", "Day 1 after 'order complete'",
  "How's the new CV feeling?", "Tell us if anything needs a tweak.",
  P(HI) + P("Now it's in your hands. How does it read to you?") +
  P("If anything feels off, just reply and tell us. Changes within your revision rounds are on us.") +
  P("Good luck out there."),
  "Reply with your thoughts", "mailto:yirehcareers@gmail.com?subject=My%20documents", "Support first, no selling."))

E.append(("P2", "After an order", "Day 10",
  "Could you spare 30 seconds?", "One sentence from you helps the next person.",
  P(HI) + P("If our work helped, one or two sentences from you would mean a lot. It also helps the next person decide.") +
  P("Just reply with a line. And tell us if we may share it (first name only, never your surname)."),
  "Write a line", "mailto:yirehcareers@gmail.com?subject=My%20feedback", "Testimonial ask. Only share with explicit permission."))

E.append(("P3-ES", "After an order: Essential", "Day 21",
  "Want a cover letter and LinkedIn to match?", "Your CV is sorted. Here's the next step.",
  P(HI) + P("Your CV is sorted. A matching <strong>cover letter ($15)</strong> and <strong>LinkedIn profile setup ($25)</strong> can make the rest of your application feel as sharp.") +
  P("Add either one, or both, when you're ready."),
  "See the add-ons", utm("/services", "essential-upsell"), "Upsell by behaviour/stage, not a countdown."))

E.append(("P3-PRO", "After an order: Professional", "Day 21",
  "Keep your LinkedIn working while you search", "12 posts and weekly connections, month to month.",
  P(HI) + P("Your CV, cover letter and profile are set. The next question is visibility.") +
  P("<strong>LinkedIn Growth ($99 a month)</strong> gives you 12 posts and weekly targeted connection requests, month to month. You pay on WhatsApp, nothing is automatic, and you can stop before any month starts."),
  "Tell me more", wa("Hello, I'd like to hear more about LinkedIn Growth."), ""))

E.append(("P3-EXEC", "After an order: Executive", "Day 30 (when the 30-day service ends)",
  "Want to keep the momentum going?", "Your 30 days are up.",
  P(HI) + P("Your 30-day LinkedIn service has wrapped up. If you'd like to keep going, <strong>LinkedIn Growth</strong> carries on the same work for $99 a month: 12 posts and weekly targeted connection requests.") +
  P("Month to month, paid on WhatsApp, no automatic charges."),
  "Keep it going", wa("Hello, I'd like to continue with LinkedIn Growth."), "Mirrors the WhatsApp progress message."))

E.append(("P4", "After an order", "Day 60",
  "How's the search going?", "Two months on.",
  P(HI) + P("Two months on. If you've landed something, congratulations. We'd love to hear about it.") +
  P("Still searching? Here are the newest remote jobs. And if a friend needs a hand with their CV, feel free to forward this email."),
  "See the newest jobs", utm("/", "customer-60"), "Referral by forwarding; no incentives promised."))

E.append(("S1", "Sunset (inactive subscribers)", "After about 60 days with no clicks (subscribers only)",
  "Still want these job emails?", "No hard feelings either way.",
  P(HI) + P("We haven't seen a click from you in a while, and that's okay.") +
  P("Want to keep getting weekly jobs? Tap below. If we don't hear from you, we'll pause your emails so your inbox stays clean."),
  "Yes, keep them coming", utm("/", "sunset-keep"), "Rule: no click within 14 days -> add to 'Do not send'."))

E.append(("T1", "Monthly tip", "Once a month, to subscribers",
  "One CV fix you can make tonight", "It takes five minutes.",
  P(HI) + P("Open your CV. Look at the top third of the first page.") +
  P("Does it say who you are, what you do, and what you're aiming for? If a stranger can't tell at a glance, reword the top line.") +
  P("It's one of the three things we check first."),
  "Get my free CV check", wa(CHECK_MSG), "One tip, one soft offer. Keep promotions out of the weekly digest."))

meta = {}
review = ["# Lifecycle email copy: for review\n", "Generated by `drafts/emails/build_marketing.py`. Subject, preview text, body and button for every lifecycle email. Edit the script, not this file.\n"]
for (id_, flow, when, subj, pre, body, label, url, note) in E:
    fn = f"{id_.lower()}.html"
    open(os.path.join(OUT, fn), "w", encoding="utf-8").write(wrap(pre, body, label, url))
    meta[id_] = {"flow": flow, "when": when, "subject": subj, "preheader": pre, "file": fn, "button": label}
    import re
    txt = re.sub(r"<[^>]+>", "", body.replace("</p>", "\n\n").replace("</li>", "\n").replace("<li", "- <li"))
    txt = html.unescape(txt).replace('{{ contact.FIRSTNAME | default:"there" }}', "[First name]")
    review.append(f"## {id_}: {subj}\n")
    review.append(f"Flow: {flow}. When: {when}.  \nPreview text: {pre}  \nButton: **{label}**" + (f"  \nNote: {note}" if note else "") + "\n")
    review.append("```\n" + re.sub(r"\n{3,}", "\n\n", txt).strip() + "\n```\n")
open(os.path.join(OUT, "meta.json"), "w").write(json.dumps(meta, indent=1))
open(os.path.join(OUT, "..", "..", "email-copy-review.md"), "w", encoding="utf-8").write("\n".join(review))
print(len(E), "emails written;", "words per body:", {k: len(re.sub(r"<[^>]+>", " ", v[5]).split()) for k, v in zip([e[0] for e in E], E)})
