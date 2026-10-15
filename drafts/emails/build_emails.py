"""Builds the Brevo email templates (HTML) into this folder. Run: python3 build_emails.py"""
import os, html
OUT = os.path.dirname(os.path.abspath(__file__))
WA = "https://wa.me/905338225854"
MAIL = "trueremote.jobs@gmail.com"
ADDR = "KAYZ Global Ltd · Şehit Mehmet Mustafa Sokak, No: 171, Girne – Merkez, 9930, North Cyprus"

def wrap(preheader, title, body, newsletter=False):
    unsub = ('<p style="margin:10px 0 0;">You are receiving this because you signed up for job alerts. '
             '<a href="{{ unsubscribe }}" style="color:#9db4d6;">Unsubscribe</a></p>') if newsletter else \
            '<p style="margin:10px 0 0;">You are receiving this message because you contacted or bought from Kaeto Career Services.</p>'
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light dark"><meta name="supported-color-schemes" content="light dark">
<title>{html.escape(title)}</title>
<style>
@media (prefers-color-scheme: dark){{
 .bg{{background:#0b1220!important}} .card{{background:#131c2e!important}}
 .tx{{color:#e6ebf5!important}} .mu{{color:#a9b4c7!important}} .box{{background:#1a2740!important;border-color:#2c3f63!important}}
}}
@media only screen and (max-width:620px){{ .wrap{{width:100%!important}} .pad{{padding:22px 18px!important}} }}
</style></head>
<body class="bg" style="margin:0;padding:0;background:#eef2f8;">
<div style="display:none;max-height:0;overflow:hidden;opacity:0;">{html.escape(preheader)}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" class="bg" style="background:#eef2f8;"><tr><td align="center" style="padding:24px 12px;">
<table role="presentation" class="wrap" width="600" cellpadding="0" cellspacing="0" style="width:600px;max-width:100%;">
<tr><td style="background:#0f2a4d;background-image:linear-gradient(135deg,#0f2a4d,#1d4f91);padding:26px 28px;border-radius:12px 12px 0 0;">
<div style="font:700 22px Arial,Helvetica,sans-serif;color:#ffffff;letter-spacing:.2px;">True Remote</div>
<div style="font:13px Arial,Helvetica,sans-serif;color:#b9cdea;margin-top:4px;">Kaeto Career Services · CVs, cover letters and LinkedIn profiles</div></td></tr>
<tr><td class="card pad" style="background:#ffffff;padding:30px 28px;font:16px/1.6 Arial,Helvetica,sans-serif;color:#1b2536;">
<div class="tx">{body}
<p style="margin:26px 0 0;">Kind regards,<br><strong>Kaeto</strong><br><span class="mu" style="color:#55627a;">Kaeto Career Services · True Remote</span></p></div></td></tr>
<tr><td style="background:#0f2a4d;padding:22px 28px;border-radius:0 0 12px 12px;font:12.5px/1.6 Arial,Helvetica,sans-serif;color:#b9cdea;">
<p style="margin:0;"><strong style="color:#ffffff;">Kaeto Career Services · True Remote</strong></p>
<p style="margin:6px 0 0;">WhatsApp (chat only): <a href="{WA}" style="color:#9db4d6;">+90 533 822 5854</a><br>
Email (documents and questions): <a href="mailto:{MAIL}" style="color:#9db4d6;">{MAIL}</a></p>
<p style="margin:6px 0 0;">{ADDR}</p>{unsub}</td></tr>
</table></td></tr></table></body></html>"""

def p(t): return f'<p style="margin:0 0 14px;">{t}</p>'
def h(t): return f'<h1 style="margin:0 0 16px;font:700 22px/1.3 Arial,Helvetica,sans-serif;">{t}</h1>'
def box(t): return f'<div class="box" style="background:#f2f6fc;border:1px solid #d5e0f0;border-radius:8px;padding:14px 16px;margin:0 0 16px;">{t}</div>'
def ul(items): return '<ul style="margin:0 0 14px;padding-left:20px;">' + ''.join(f'<li style="margin:0 0 6px;">{i}</li>' for i in items) + '</ul>'
def btn(t, url): return f'<p style="margin:0 0 14px;"><a href="{url}" style="display:inline-block;background:#1d4f91;color:#ffffff;text-decoration:none;font-weight:700;padding:12px 22px;border-radius:8px;">{t}</a></p>'
SPAM = box("<strong>Can't find our emails?</strong> Please check your <strong>Promotions</strong> and <strong>Spam</strong> folders, and move our messages to your main inbox or add trueremote.jobs@gmail.com to your contacts so you do not miss anything.")
HI = p('Hi {{ params.FIRSTNAME | default:"there" }},')

T = {}
T["TR-01 Order received and onboarding"] = ("Thank you for your order: here is how to get started", "Your order is confirmed. Reply to this email with your documents so we can begin.",
 h("Thank you for your order") + HI +
 p("We have received your <strong>{{ params.PACKAGE }}</strong> order. Before we can start, we need to complete a short onboarding. <strong>Your delivery time starts when onboarding is complete</strong>, not when you pay.") +
 box('<strong>To complete onboarding, reply to this email with:</strong>' + ul([
   "your current CV (Word, PDF or plain text) and your LinkedIn profile link, if you have one;",
   "the job titles or fields you are applying for, and any countries or regions you can work from;",
   "two or three job postings you like, if you have them;",
   "anything you want included or left out (for example career gaps or a career change).",
 ])) +
 p("<strong>Please send documents by email, not WhatsApp.</strong> WhatsApp is fine for chatting and asking questions, but we only accept documents by email so they are kept in one place.") +
 p("Please do not send passport or ID numbers, bank details, passwords or other sensitive information. We do not need them. Email is not end-to-end encrypted, so only send what is needed for your CV or profile.") +
 p("Once we have what we need, we will confirm that onboarding is complete and tell you the dates. If anything is unclear, reply here or message us on WhatsApp.") + SPAM +
 btn("Questions? Chat on WhatsApp", WA))

T["TR-02 Onboarding complete"] = ("Onboarding complete: your timeline starts today", "Onboarding is complete. Your delivery clock has started.",
 h("Onboarding complete: we have started") + HI +
 p("Thank you. We have everything we need for your <strong>{{ params.PACKAGE }}</strong>, and work has begun.") +
 box("<strong>Your timeline</strong><br>Onboarding completed: {{ params.START_DATE }}<br>Expected delivery: {{ params.DELIVERY_DATE }}<br>" +
     '<span class="mu" style="color:#55627a;font-size:14px;">Timings are counted in working days from the date onboarding was completed.</span>') +
 p("We will email your documents to you as soon as they are ready. If we need to clarify anything, we will write to you first.") +
 p("Please check each employer's eligibility rules before you apply: we do not guarantee interviews, job offers or any particular outcome.") + SPAM)

T["TR-03 Documents delivered"] = ("Your documents are ready", "Your documents are attached. Here is how revisions work.",
 h("Your documents are ready") + HI +
 p("Your <strong>{{ params.PACKAGE }}</strong> documents are attached to this email. Please read them carefully and check that every date, job title, employer name and figure is correct.") +
 box("<strong>How revisions work</strong>" + ul([
   "Your package includes <strong>{{ params.REVISIONS }} rounds of revisions</strong>.",
   "Please send <strong>all your changes together in one reply</strong>. One consolidated message counts as one round.",
   "Tell us when you are happy and approve the final version, so we can close your order.",
 ])) +
 p("Please keep your own copies of the files. We will delete ours after your order is completed, as set out in our terms.") +
 SPAM + btn("Reply with your feedback", "mailto:" + MAIL))

T["TR-04 Executive branding strategy for approval"] = ("Your personal branding strategy: please review and approve", "Review your branding direction before we publish anything.",
 h("Your personal branding strategy") + HI +
 p("Your personal branding direction is attached. Please review it before we write or publish anything on your behalf.") +
 box("<strong>What we need from you</strong>" + ul([
   "Check that every claim about your experience, achievements and qualifications is <strong>accurate</strong>. You are responsible for the accuracy of what is published in your name.",
   "Tell us which target audiences, roles and kinds of connections you want us to focus on.",
   "Reply with your <strong>written approval</strong>, or send your changes in one message.",
 ])) +
 p("We will not publish posts or send connection requests until you approve. The 30-day LinkedIn service period starts when onboarding is complete.") + SPAM)

T["TR-05 Order completed and deletion notice"] = ("Your order is complete", "Your order is complete. Here is what happens to your files.",
 h("Your order is complete") + HI +
 p("Your <strong>{{ params.PACKAGE }}</strong> order is now complete. Thank you for trusting us with your career documents.") +
 box("<strong>What happens to your information</strong>" + ul([
   "We delete your documents and personal details from our email, devices and WhatsApp within <strong>90 days</strong> of completion.",
   "Payment records held by our payment provider follow that provider's own retention policy.",
   "You can ask us to delete your information sooner, or ask for a copy, by replying to this email.",
 ])) +
 p("Please keep your own copies of all final files. If you want to leave feedback, reply to this email.") +
 p("Good luck with your search. Please check each employer's eligibility rules before applying."))

T["TR-06 Privacy request received"] = ("We received your request about your information", "We have received your request and will respond within one month.",
 h("We received your request") + HI +
 p("Thank you for contacting us about your personal information. We have received your request and will reply within <strong>one month</strong>. It is free of charge.") +
 p("To protect your information, we may need to confirm that the request comes from you. If so, we will ask for the minimum needed, and never a copy of your passport or ID unless there is no other way.") +
 p("If you have more details to add, reply to this email.") + SPAM)

T["TR-07 Newsletter welcome"] = ("Welcome to True Remote job alerts", "You are on the list. Here is what to expect.",
 h("Welcome to True Remote") +
 p('Hi {{ contact.FIRSTNAME | default:"there" }},') +
 p("Thanks for signing up. True Remote lists remote jobs from employers' own career pages, so every listing links to the real posting, shows its source and posting date, and states where applicants may live as the employer says it.") +
 box("<strong>What to expect</strong>" + ul([
   "A weekly email with recent remote jobs across many fields and experience levels.",
   "Each job shows what the employer states about eligibility. Some jobs are marked \"not confirmed\" when the posting is unclear.",
   "We never charge job seekers to apply or to see an apply link.",
 ])) +
 p("<strong>Please check each employer's eligibility rules before you apply.</strong> We cannot verify that an employer can hire in your country.") +
 btn("Browse open jobs", "https://northcyprusremotejobboard.vercel.app/") +
 p("We also offer paid CV, cover letter and LinkedIn writing if you would like help. It is optional and the job board stays free.") + SPAM)

import json
meta = {}
for name, v in T.items():
    subj, pre, body = v[0], v[1], v[2]
    nl = name.startswith("TR-07")
    fn = name.split(" ")[0].lower() + ".html"
    open(os.path.join(OUT, fn), "w", encoding="utf-8").write(wrap(pre, subj, body, newsletter=nl))
    meta[name] = {"subject": subj, "file": fn}
json.dump(meta, open(os.path.join(OUT, "templates.json"), "w"), indent=1)
print(json.dumps(meta, indent=1))
