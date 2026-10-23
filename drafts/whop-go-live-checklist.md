# Whop card checkout: go-live checklist

Status 23 Oct 2026: sandbox only. The code is on branch `claude/optimistic-hopper-nv0qun` (not merged to main). Nothing below is done until ticked, and the live site shows no card buttons until `site-config.js` has mode `live`.

## A. KT, in Whop (production business, not the sandbox)
- [ ] Create your own stand-alone Whop business (not a connected account of anyone else). Name: Kaeto Career Services.
- [ ] Complete identity verification (Verifications) and add the payout method; note the payout fee shown at Withdraw (Balances).
- [ ] Check Risk or holds settings; note any reserve or hold period.
- [ ] Settings: Legal (the business name and address buyers see on receipts), Checkout branding, notification emails, invoice prefix.
- [ ] Tax: decide with an accountant what applies to CV services (US sales-tax collection is currently on for the old account; no UK VAT or EU OSS registration). Set the tax mode to match.
- [ ] Create the two products (copy from the sandbox: names, descriptions, $29 and $49, one-time, no compare-at price) and the same plan settings: card only, the three checkout questions, button label "Purchase".
- [ ] Send Claude the live plan IDs or give a live key through the environment secret (restricted to products, plans and checkout links).

## B. Claude, after A
- [ ] Create two live checkout configurations (plan plus redirect to `https://northcyprusremotejobboard.vercel.app/thanks`; use the final domain if it has changed).
- [ ] Put the live URLs in `site-config.js`, set mode `live`, run tests and the monitor rule, push a preview and test.
- [ ] Confirm the Vercel production domain is public (previews are behind Vercel login; production must not be).

## C. KT approval and merge
- [ ] KT reviews: privacy page wording (Whop paragraph), services copy, and decides on withdrawal-right wording (distance-selling rules for EU or UK buyers) with a professional. Claude has not published any new refund or withdrawal terms.
- [ ] KT approves the merge to main.

## D. After merge, with real money (KT does the purchase)
- [ ] Buy Essential yourself with a real card (refund it afterwards). Check: the receipt email and what it shows (business name, address), the payment appears in Whop with the three answers, the redirect to `/thanks` works, money arrives (Balances) and a withdrawal reaches your bank.
- [ ] Check the first live monitor run is green and GoatCounter records `pay-essential` and `pay-professional` events.
- [ ] Remove the sandbox API key in Whop (Developer page) and from the environment secrets.
