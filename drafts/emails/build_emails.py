"""Builds the Brevo email templates (HTML) into this folder. Run: python3 build_emails.py
Copy rules live in drafts/voice-and-copy-guide.md (short, warm, one next step, legal points said once)."""
import os, html, json
OUT = os.path.dirname(os.path.abspath(__file__))
WA = "https://wa.me/905338225854"
MAIL = "yirehcareers@gmail.com"
ADDR = "Yireh Careers · Kyrenia, Northern Cyprus"
ADDR_NEWSLETTER = "Yireh Careers · Yenice Sokak, 99300 Kyrenia, Cyprus"  # KT confirmed 24 Oct 2026

def wrap(preheader, title, body, newsletter=False):
    reason = ("You're getting this because you signed up for job alerts. "
              '<a href="{{ unsubscribe }}" style="color:#9db4d6;">Unsubscribe</a>') if newsletter else \
             "You're getting this because you contacted or bought from Yireh Careers."
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light dark"><meta name="supported-color-schemes" content="light dark">
<title>{html.escape(title, quote=False)}</title>
<style>
@media (prefers-color-scheme: dark){{
 .bg{{background:#0b1220!important}} .card{{background:#131c2e!important}}
 .tx{{color:#e6ebf5!important}} .mu{{color:#a9b4c7!important}} .box{{background:#1a2740!important;border-color:#2c3f63!important}}
}}
@media only screen and (max-width:620px){{ .wrap{{width:100%!important}} .pad{{padding:22px 18px!important}} }}
</style></head>
<body class="bg" style="margin:0;padding:0;background:#eef2f8;">
<div style="display:none;max-height:0;overflow:hidden;opacity:0;">{html.escape(preheader, quote=False)}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" class="bg" style="background:#eef2f8;"><tr><td align="center" style="padding:24px 12px;">
<table role="presentation" class="wrap" width="600" cellpadding="0" cellspacing="0" style="width:600px;max-width:100%;">
<tr><td style="background:#0f2a4d;background-image:linear-gradient(135deg,#0f2a4d,#1d4f91);padding:26px 28px;border-radius:12px 12px 0 0;">
<div style="font:700 22px Arial,Helvetica,sans-serif;color:#ffffff;letter-spacing:.2px;">Yireh Careers</div>
<div style="font:13px Arial,Helvetica,sans-serif;color:#b9cdea;margin-top:4px;">CVs, cover letters and LinkedIn profiles</div></td></tr>
<tr><td class="card pad" style="background:#ffffff;padding:30px 28px;font:16px/1.6 Arial,Helvetica,sans-serif;color:#1b2536;">
<div class="tx">{body}
<p style="margin:24px 0 0;">Thanks,<br><strong>The Yireh Careers team</strong></p></div></td></tr>
<tr><td style="background:#0f2a4d;padding:20px 28px;border-radius:0 0 12px 12px;font:12.5px/1.6 Arial,Helvetica,sans-serif;color:#b9cdea;">
<p style="margin:0;">Questions? Reply to this email, or message us on WhatsApp: <a href="{WA}" style="color:#9db4d6;">+90 533 822 5854</a></p>
<p style="margin:6px 0 0;">{ADDR_NEWSLETTER if newsletter else ADDR}</p><p style="margin:6px 0 0;">{reason}</p></td></tr>
</table></td></tr></table></body></html>"""

def p(t): return f'<p style="margin:0 0 14px;">{t}</p>'
def h(t): return f'<h1 style="margin:0 0 16px;font:700 22px/1.3 Arial,Helvetica,sans-serif;">{t}</h1>'
def box(t): return f'<div class="box" style="background:#f2f6fc;border:1px solid #d5e0f0;border-radius:8px;padding:14px 16px;margin:0 0 16px;">{t}</div>'
def ul(items): return '<ul style="margin:0 0 14px;padding-left:20px;">' + ''.join(f'<li style="margin:0 0 6px;">{i}</li>' for i in items) + '</ul>'
def btn(t, url): return f'<p style="margin:0 0 14px;"><a href="{url}" style="display:inline-block;background:#1d4f91;color:#ffffff;text-decoration:none;font-weight:700;padding:12px 22px;border-radius:8px;">{t}</a></p>'
HI = p('Hi {{ params.FIRSTNAME | default:"there" }},')

T = {}
T["TR-01 Order received and onboarding"] = ("Thanks, here's how we get started", "One quick step and we can begin.",
 h("Thanks for your order") + HI +
 p("We've got your <strong>{{ params.PACKAGE }}</strong> order. To get going, just reply to this email with:") +
 ul(["your current CV (Word, PDF or plain text), and your LinkedIn link if you have one",
     "the kind of roles you're going for, and the countries you can work in",
     "any job postings you like (optional)"]) +
 p("That's it. You don't need to send ID or bank details. Email works best for documents, so they stay private and in one place. WhatsApp is perfect for questions.") +
 p("Your delivery time starts once we have everything, and we'll confirm your dates as soon as we do.") +
 p("If you don't see our emails later on, take a quick look in Promotions or Spam."))

T["TR-02 Onboarding complete"] = ("We've started, here are your dates", "Your delivery date is inside.",
 h("We've started") + HI +
 p("Thanks, we've got everything we need and we're now working on your <strong>{{ params.PACKAGE }}</strong>.") +
 box("<strong>Started:</strong> {{ params.START_DATE }}<br><strong>Expected delivery:</strong> {{ params.DELIVERY_DATE }} (working days)") +
 p("We'll email your documents when they're ready. If we need to check anything first, we'll ask."))

T["TR-03 Documents delivered"] = ("Your documents are ready", "They're attached, with how to ask for changes.",
 h("Your documents are ready") + HI +
 p("Your <strong>{{ params.PACKAGE }}</strong> documents are attached. Take your time, and check that every date, job title and name is right.") +
 p("Want changes? You have <strong>{{ params.REVISIONS }} rounds</strong>. Reply once with everything you'd like changed, and that counts as one round.") +
 p("Happy with it? Just let us know and we'll wrap up your order.") +
 btn("Reply with your feedback", "mailto:" + MAIL))

T["TR-04 Executive branding strategy for approval"] = ("Your branding plan: a quick review, please", "We won't publish anything until you say so.",
 h("Your personal branding plan") + HI +
 p("Your branding plan is attached. Please read it through before we write or publish anything for you.") +
 ul(["Check that every detail about your experience and qualifications is right, since it goes out under your name.",
     "Tell us who you most want to reach: the roles, industries and kinds of people.",
     "Reply with a yes, or send your changes in one message."]) +
 p("We won't post or send any connection requests until you've said yes. Your 30 days start once onboarding is complete."))

T["TR-05 Order completed and deletion notice"] = ("All done, thank you", "And what happens to your files.",
 h("All done") + HI +
 p("Your <strong>{{ params.PACKAGE }}</strong> order is complete. Thank you for trusting us with your career documents.") +
 p("Please keep your own copies of the final files. We'll delete your documents and details from our email, devices and WhatsApp within 90 days. Want that sooner, or a copy of what we hold? Just reply and ask.") +
 p("Good luck with your search. One tip: check each employer's rules for your country before you apply."))

T["TR-06 Privacy request received"] = ("We've got your request", "You'll hear back within a month.",
 h("We've got your request") + HI +
 p("Thanks for getting in touch about your personal information. We'll reply within one month, and it's free.") +
 p("We may ask you to confirm it's you. If so, we'll ask for as little as possible, and never a copy of your ID unless there's no other way.") +
 p("Anything to add? Just reply to this email."))

T["TR-07 Newsletter welcome"] = ("Welcome to Yireh Careers", "Weekly remote jobs, each linked to the employer's own posting.",
 h("Welcome to Yireh Careers") +
 p('Hi {{ contact.FIRSTNAME | default:"there" }},') +
 p("Thanks for signing up. Each week we'll send you recent remote jobs across lots of fields and experience levels. Every job links straight to the employer's own posting, and shows when it was posted and who can apply.") +
 btn("Browse open jobs", "https://yirehcareers.vercel.app/?utm_source=email&utm_medium=email&utm_campaign=welcome") +
 p("One tip: employers decide who they can hire, so check their rules for your country before you apply. Applying never costs you anything with us.") +
 p("If you'd ever like a hand with your CV, cover letter or LinkedIn, we do that too, from $29. No pressure, and the job board stays free."))

meta = {}
for name, v in T.items():
    subj, pre, body = v[0], v[1], v[2]
    nl = name.startswith("TR-07")
    fn = name.split(" ")[0].lower() + ".html"
    open(os.path.join(OUT, fn), "w", encoding="utf-8").write(wrap(pre, subj, body, newsletter=nl))
    meta[name] = {"subject": subj, "file": fn}
json.dump(meta, open(os.path.join(OUT, "templates.json"), "w"), indent=1)
print(json.dumps(meta, indent=1))


# ---- Gmail canned-response pack (plain text), built from the same copy ----
import re
def plain(body):
    t = re.sub(r'<h1[^>]*>.*?</h1>', '', body)
    t = re.sub(r'<p[^>]*><a [^>]*display:inline-block[^>]*>.*?</a></p>', '', t)
    t = re.sub(r'<li[^>]*>', '- ', t); t = t.replace('</li>', '\n')
    t = re.sub(r'</p>|</h1>|</div>|</ul>', '\n\n', t); t = t.replace('<br>', '\n')
    t = re.sub(r'<a [^>]*>(.*?)</a>', r'\1', t); t = re.sub(r'<[^>]+>', '', t)
    t = html.unescape(t)
    for a, b in [('{{ params.FIRSTNAME | default:"there" }}', '[First name]'), ('{{ params.PACKAGE }}', '[Package]'),
                 ('{{ params.START_DATE }}', '[date]'), ('{{ params.DELIVERY_DATE }}', '[date]'), ('{{ params.REVISIONS }}', '[2 or 3]')]:
        t = t.replace(a, b)
    t = re.sub(r'\n[ \t]+', '\n', t); t = re.sub(r'\n{3,}', '\n\n', t).strip()
    return t

GMAIL_WHEN = {
 "TR-01": "Send when you have confirmed the customer's payment. Attach nothing.",
 "TR-02": "Send when you have their CV and answers. Fill in both dates.",
 "TR-03": "Send with the finished documents attached. Choose 2 or 3 revision rounds (Essential 2, Professional 3, Executive 3).",
 "TR-04": "Executive only. Send with the branding plan attached, before anything is published.",
 "TR-05": "Send when the order is closed. Starts the 90-day deletion clock: diarise the delete-by date in the client log.",
 "TR-06": "Send within a few days of someone asking about their personal information. You then have one month to answer.",
}
out = ["# Gmail replies for customer emails (Yireh Careers)\n",
       "Generated by `drafts/emails/build_emails.py` from the same copy as the Brevo templates. Do not edit by hand.\n",
       "**Why Gmail and not Brevo for these:** orders happen on WhatsApp, so Brevo never learns that a customer paid or finished onboarding; Brevo cannot attach each customer's documents; Brevo cannot send authenticated mail from a Gmail address; and keeping customers out of Brevo keeps their details in fewer places. Gmail sends from the real mailbox and the customer's reply stays in the same thread as their documents.\n",
       "**One-time setup in Gmail (on a computer):** Settings (gear), See all settings, Advanced, Templates: Enable, Save. Then for each email below: write a new message, paste the subject and body, tap the three dots at the bottom right, Templates, Save draft as template, Save as new template, and give it the name shown. To use one: new message, three dots, Templates, pick it, fill in the [brackets], send.\n"]
for name, v in T.items():
    key = name.split(" ")[0]
    if key == "TR-07":
        continue
    out.append(f"## {name}\n")
    out.append(f"When: {GMAIL_WHEN[key]}\n")
    out.append(f"Template name in Gmail: `{key} {name.split(' ', 1)[1]}`\n")
    out.append("Subject:\n\n```\n" + v[0] + "\n```\n")
    body = plain(v[2]) + "\n\nThanks,\nThe Yireh Careers team\n\nQuestions? Reply here, or message us on WhatsApp: +90 533 822 5854"
    out.append("Body:\n\n```\n" + body + "\n```\n")
out.append("## Not in Gmail\nThe welcome email (TR-07, Brevo template 40) and the weekly jobs email stay in Brevo, because the sign-up form feeds Brevo.\n")
open(os.path.join(OUT, "..", "gmail-customer-emails.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")
print("wrote gmail-customer-emails.md")
