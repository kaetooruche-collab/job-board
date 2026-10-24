# Email design and voice (proposed)

Status: PROPOSED. This replaces the look and the copy of the first email set, which KT judged too long, too abrasive and visually weak. The voice rules are in `drafts/voice-and-copy-guide.md`; this note adds what changed and how it is checked.

## Copy: what changed and why

| First set | This set |
|---|---|
| Opened with a mood line ("Job hunting can feel like shouting into the void") | Opens with the point, in plain words, and uses the person's first name |
| Welcome, then a sales offer on day 7 | Welcome does one job; a promotional email only exists for people who ticked a separate box |
| Same offer in different words across a sequence | Every email in a sequence adds something new (a check, a checklist, the facts and price); the free-check follow-up is one email because a second would repeat it |
| Disclaimers repeated | Each legal point appears once, where it matters (deletion in the order-complete email, eligibility tip in the job email, cooling-off and refund wording left out until KT decides) |
| Silent on AI | Names the AI alternative, gives an honest checklist for using it, and says when you may not need us |
| Promotion mixed into service messages | Service emails are plain, carry no offers, and a test fails the build if they do |

Checks run by `tests/test_email_library.py`: no urgency or outcome words, at most one exclamation mark, no emoji, subject under 56 characters, 40-115 words in marketing emails, one button, unsubscribe link and postal address present, tracking parameters on site links, service emails carry no buttons, offers or prices (three whitelisted contract mentions), no personal name. **These tests check rules, not quality.** Quality is judged by you reading the copy, and later by replies and enquiries.

## Visual design

- A calm single column, 600px wide, on a warm paper background with a white card. Text wordmark "Yireh Careers" with a short blue rule; no heavy navy bars and no images (nothing to block or break).
- One headline (the subject line), body at 17px with generous line spacing, one full-width button on phones, one sign-off ("The Yireh Careers team"), a quiet footer with why you're getting it, the postal address, a one-tap unsubscribe and the privacy link.
- Job cards in the digest: bold linked title, a muted line (company, level, pay if stated, how long ago), and a pill that says **Who can apply** in the employer's own words, with "Worldwide" highlighted in green because it is the rarest and most useful answer.
- Dark mode and phone widths are built in.
- Service emails stay plain text: personal, reply-friendly and able to carry attachments.

## What I checked, and what I did not

Checked: each of the 13 Brevo emails renders in Chromium; I looked at desktop light, phone dark and phone light renders of the welcome, tips and digest emails and fixed a wrapping wordmark and unreadable dark-mode link colours.

**Not checked:** how Gmail (web and app), Outlook and Apple Mail draw them. Previews in a browser are not real inboxes. That is test T8 in `06-brevo-architecture.md`, and it needs a domain-authenticated test send to your own addresses.

Merge tags `{{ contact.FIRSTNAME | default:"there" }}` and `{{ unsubscribe }}` come from the first set (already accepted by Brevo); they are re-verified at send test.

## How to review the copy

Open `preview/index.html` in a browser for the 13 Brevo emails, and read `05-operational.md` for the 16 service emails. Mark anything that sounds like something you wouldn't say to a person's face. The words live in `email_data.py`; one edit there rebuilds every file.
