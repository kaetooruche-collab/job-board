# Brevo setup guide for KT (about 45 minutes, in this order)

Everything the Brevo connector cannot create. The emails themselves are already in Brevo (templates 40-52); you are building the lists and the "if this, send that" rules. Menu names can differ slightly from this guide: the automation editor you screenshotted has three tabs on the left, **Triggers**, **Actions** and **Rules**.

Plan limits to keep in mind (free plan): 300 emails a day, and 2,000 different people can enter automations. You are far below both.

## Step 1. Create the lists (Contacts, Lists, Create a list)
Create these five. Put them in the same folder as list #11.
1. `Free CV check requested`
2. `Customers: Essential`
3. `Customers: Professional`
4. `Customers: Executive`
5. `Do not send`

Rename the existing list #11 ("North cyprus remote jobs Subscribers") to `Job alert subscribers`. (Renaming does not break the website sign-up form.)

Optional later: `LinkedIn Growth: active` (service emails only).

## Shortcut: let Brevo's AI automation builder draft them
Brevo has a builder that turns a plain sentence into an inactive workflow you then check and activate (it is a dashboard feature, not available through the API). Automations, Create, then look for the AI / "describe your automation" option. Paste one of these, then open the result and fix the email steps to the templates named in the steps below. Always read what it built before activating.

1. "When a contact is added to the list Job alert subscribers, send the email template 'Yireh MKT W1 Welcome (day 0)'. Wait 3 days, send 'Yireh MKT W2 Welcome (day 3)'. Wait 4 days. If the contact is in any of the lists Customers: Essential, Customers: Professional or Customers: Executive, stop; otherwise send 'Yireh MKT W3 Welcome (day 7)'."
2. "When a contact is added to the list Free CV check requested, wait 3 days and send 'Yireh MKT F1 Free check follow-up (day 3)'. Wait 5 days. If the contact is in any Customers list, stop; otherwise send 'Yireh MKT F2 Free check follow-up (day 8)'."
3. "When a contact is added to the list Customers: Essential, wait 1 day and send 'Yireh MKT P1 After order: check-in (day 1)'. Wait 9 days, send 'Yireh MKT P2 After order: feedback ask (day 10)'. Wait 11 days, send 'Yireh MKT P3 Essential upsell (day 21)'. Wait 39 days, send 'Yireh MKT P4 After order: how's the search (day 60)'." (Repeat for Professional with its P3, and for Executive: P1, P2, then wait 20 days and send 'Yireh MKT P3 Executive follow-on (day 30)', then wait 30 days and send P4.)

## Step 2. Welcome automation (Automations, Create, start from scratch)
Name: `Welcome series`.
1. **Triggers tab:** drag **Contact added to list** onto the canvas. Choose `Job alert subscribers`.
2. **Actions tab:** drag **Send an email**. Choose template **40 (Yireh MKT W1 Welcome)**. Sender Yireh Careers.
3. **Actions tab:** drag **Wait**. 3 days.
4. **Send an email**: template **41 (W2)**.
5. **Wait**: 4 days.
6. **Rules tab:** drag the **If / else** (condition) step. Condition: contact is in list `Customers: Essential` OR `Customers: Professional` OR `Customers: Executive`. 
   - If **yes**: end.
   - If **no**: **Send an email**, template **42 (W3)**.
7. **Settings** (left side): do not allow the same person to enter twice. Add the exit rule "contact added to `Do not send`" if the option is offered.
8. Press **Test** (it sends to a test contact), then **Activate automation**.

Your existing contacts do not receive it (it fires only for people added after you activate), which is what you want.

## Step 3. Free CV check follow-up
Name: `Free CV check follow-up`.
1. Trigger: **Contact added to list** `Free CV check requested`.
2. **Wait** 3 days, **Send an email** template **43 (F1)**.
3. **Wait** 5 days. **If / else**: contact is in any `Customers:` list. Yes: end. No: **Send an email** template **44 (F2)**.
4. Activate.

How it gets used: when you email someone their three fixes, also add them to `Free CV check requested` (Contacts, Add a contact, choose the list; use their first name).

## Step 4. After-order automations (three copies)
Only add people here **who said yes to occasional emails** (see the decision doc, section 3). Add them when their order is **complete**.

`After order: Essential`
- Trigger: **Contact added to list** `Customers: Essential`.
- Wait 1 day, send **45 (P1)**. Wait 9 days, send **46 (P2)**. Wait 11 days, send **47 (P3 Essential upsell)**. Wait 39 days, send **50 (P4)**.

`After order: Professional`
- Same, with template **48 (P3 Professional)** at day 21.

`After order: Executive`
- Trigger: `Customers: Executive`. Wait 1 day send **45**; wait 9 days send **46**; wait 20 days send **49 (P3 Executive follow-on, day 30)**; wait 30 days send **50**.

Tip: build the first one, then use Duplicate for the other two and change the trigger and the day-21 template.

## Step 5. Weekly jobs email (a campaign, not an automation)
1. Tell Claude "weekly email". Claude generates the digest from the live feed, creates a **draft campaign** in Brevo and sends you a test.
2. In Brevo: Campaigns, open the draft. **Recipients:** `Job alert subscribers`. Open **Advanced options** and **exclude** the list `Do not send`.
3. **Schedule** it: Tuesday morning is a starting point (the research has no proof of a best day; try Tuesday, then Thursday, and compare clicks).
4. Skip the send in a week with fewer than three fresh roles.

## Step 6. Monthly tip and the sunset flow
- **Monthly tip:** a campaign using template **52 (T1)**, once a month, same recipients and exclusion as above. Write a new tip each month (Claude drafts them).
- **Sunset** (build around week 8, when people have been on the list long enough): automation with trigger **Contact matches custom filters**: in `Job alert subscribers`, added more than 60 days ago, no email click in 60 days. Send **51 (S1)**, wait 14 days, **If / else**: clicked a link in an email? Yes: end. No: **Add to list** `Do not send` and remove from `Job alert subscribers`.

## Step 7. Clean up (optional, 5 minutes)
- Delete the old templates 20-33 (the True Remote and Kaeto sets). Keep 1-16 (your other projects). Keep 34-39 as a fallback.
- The old welcome automation that uses template 12: pause or delete it so people do not get two welcomes.
- Check that the campaign "Monday 5th October Job Update Email_copy" draft (old claims: pay, "worldwide") is deleted.

## Step 8. Checks before you rely on it
1. Add yourself to `Job alert subscribers` with a second address you control, and confirm W1 arrives within a few minutes.
2. Check the unsubscribe link in each email works and puts the person on Brevo's unsubscribed list.
3. Confirm a campaign to `Job alert subscribers` with `Do not send` excluded shows the right recipient count before you schedule.
