# Whop card checkout: go-live checklist

Status 23 Oct 2026: sandbox only. The code is on branch `claude/optimistic-hopper-nv0qun` (not merged to main). Nothing below is done until ticked, and the live site shows no card buttons until `site-config.js` has mode `live`.

## A0. Before anything is created in the production Whop
- [ ] Decide the services name (see `drafts/decisions/2026-10-23-services-brand-name.md`). It becomes the Whop business name, the receipt sender and the card statement descriptor, so decide before creating the business.
- [ ] Phone retest in the sandbox: redo one phone purchase with all three questions answered and check the customer profile (KT's first phone answers were lost in Claude's 13:13 UTC wipe), and test the 3-D Secure card (5385 3083 6013 5181, password Checkout1!). Turkish cards usually require 3-D Secure; Claude's headless browser could not complete it (the challenge window opened but never loaded).

## A. KT, in Whop (production business, not the sandbox)
- [ ] Refunds: Whop docs say a refund needs enough balance in the account. Check how and when new payments become available (Balances, any hold) so a refund before onboarding can always be paid. In Resolution Center, review the auto-refund (Auto respond) thresholds and keep them OFF or deliberately set, so they match the approved refund policy.
- [ ] Legal settings: set the terms and privacy links shown at checkout to our pages (the checkout says "you agree to ... terms and conditions"), once KT has approved the terms wording.
- [ ] Create your own stand-alone Whop business (not a connected account of anyone else). Name: Yireh Careers (decided 24 Oct). The business is an individual account until a company is registered.
- [ ] Complete identity verification (Verifications) and add the payout method; note the payout fee shown at Withdraw (Balances).
- [ ] Check Risk or holds settings; note any reserve or hold period.
- [ ] Settings: Legal (the business name and address buyers see on receipts), Checkout branding, notification emails, invoice prefix.
- [ ] Tax: decide with an accountant what applies to CV services (US sales-tax collection is currently on for the old account; no UK VAT or EU OSS registration). Set the tax mode to match.
- [ ] Keep adaptive pricing ON (local-currency display) on both live plans (KT decision 23 Oct: buyers see a familiar amount; per Whop docs it is free for sellers, replaces international card and FX fees with the domestic rate and lowers declines; the buyer's local price includes a small conversion fee). Check on a real purchase from outside the US that the fee shown in Whop is lower or the same, not higher.
- [ ] Create the two products (copy from the sandbox: names, descriptions, $29 and $49, one-time, no compare-at price) and the same plan settings: card only, the three checkout questions, button label "Purchase".
- [ ] Turn on the email notification for each new sale (Settings, Notifications) so you hear about an order straight away, and check that the notification tells you to open the customer profile for the three answers (they are under Customers, the customer, Custom fields, not on the payment page).
- [ ] Look in Whop (Settings) for a support email or contact setting for buyers and set it to trueremote.jobs@gmail.com; the receipt says "contact our support team", which is Whop's team by default.
- [ ] Set the same plan description on the live plans: "After payment, email your current CV (or tell us you do not have one) and your target roles to trueremote.jobs@gmail.com. Please do not send documents on WhatsApp. A full refund is available before onboarding is complete. We do not promise interviews or job offers." Then buy once with your own email and check whether it shows in the receipt.
- [ ] Plan to send each card buyer a short welcome email from trueremote.jobs@gmail.com the same day (what we need from them, timing starts when onboarding is complete); the Whop receipt does not do this. Claude can draft the wording.
- [ ] Send Claude the live plan IDs or give a live key through the environment secret (restricted to products, plans and checkout links).

## A2. Rule for every change to a Whop plan or product (learned on 23 Oct)
Updating a plan can silently remove other settings (a description change removed the three checkout questions). After ANY edit: send the complete configuration in one request, re-read the plan, and check: price, 3 questions with the right required flags, card only, adaptive pricing as decided, description. Then load the checkout in a browser and confirm the questions show.

## B. Claude, after A
- [ ] Create two live checkout configurations (plan plus redirect to `https://northcyprusremotejobboard.vercel.app/thanks`; use the final domain if it has changed).
- [ ] Put the live URLs in `site-config.js`, set mode `live`, run tests and the monitor rule, push a preview and test.
- [ ] Confirm the Vercel production domain is public (previews are behind Vercel login; production must not be).

## C. KT approval and merge
- [ ] KT reviews: privacy page wording (Whop paragraph), services copy, and decides on withdrawal-right wording (distance-selling rules for EU or UK buyers) with a professional. Claude has not published any new refund or withdrawal terms.
- [ ] KT approves the merge to main.

## D. After merge, with real money (KT does the purchase)
- [ ] After the live plans are created and before announcing anything, buy once and open Customers, the customer, Custom fields: all three answers must show.
- [ ] Buy Essential yourself with a real card (refund it afterwards). Check: the receipt email and what it shows (business name, address), the payment appears in Whop with the three answers, the redirect to `/thanks` works, money arrives (Balances) and a withdrawal reaches your bank.
- [ ] Check the first live monitor run is green and GoatCounter records `pay-essential` and `pay-professional` events.
- [ ] Remove the sandbox API key in Whop (Developer page) and from the environment secrets.
