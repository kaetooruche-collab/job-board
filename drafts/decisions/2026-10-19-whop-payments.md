# Decision review: could card payments go through Whop? (19 Oct 2026)

Status: RESEARCH ONLY. Nothing changed on the site. KT's existing decision (15 Oct) stands: no payment of any kind on the website; payment is arranged on WhatsApp.

## What could not be done
KT asked for the Claude in Chrome extension to open KT's own Whop account. That extension is not connected to this cloud session (no Chrome tools were available), so KT's actual account (KYC status, payout method, holds, classification, tax mode) was NOT inspected. Everything below comes from Whop's public pages read on 19 Oct 2026. The checklist at the end shows what KT should look at in the account.

## What Whop says (public pages)
- **Payout countries:** over 200, and the list includes Cyprus and Turkey. Not on the sanctioned list. Payout options depend on the country. KYC means details, a linked bank and an ID upload. https://docs.whop.com/manage-your-business/manage-payouts/set-up-payouts
- **Fees (standard):** 2.7% + $0.30 per card payment; +1.5% for international cards; +1% for currency conversion; $15 per dispute. Payouts: local bank transfer in your country "varies"; bank wire $23; crypto 5% + $1; instant bank 4% + $2.50. Optional extras (tax 2%, billing 0.5%, orchestration 0.8%) stack on top. https://whop.com/network/pricing/
- **Worked examples (international card):** $29 order costs about $1.81 (6.2%); $49 about $2.85 (5.8%); $149 about $8.05 (5.4%), before the payout fee and before any dispute.
- **Allowed businesses:** CV and LinkedIn writing services are not on the prohibited list. Risk areas on the list: "platform manipulation (fake followers, likes or artificial engagement)" and "identity services (fake employment references)". Our LinkedIn work is manual, targeted networking and real content, so it should be fine, but Whop classifies each business by what it actually sells, re-checks regularly, pauses payouts if it cannot verify what is sold, and can terminate and withhold funds for non-correctable violations. Describe the Executive and LinkedIn Growth products carefully (manual, no fake engagement). https://docs.whop.com/trust-and-safety/trust-safety-overview/what-is-not-allowed-on-whop
- **Responsibility:** the seller is responsible for chargebacks, refunds, the $15 fee, and taxes (VAT/sales tax) unless the optional tax mode is switched on; Whop is merchant of record only for card-network and settlement purposes. https://whop.com/seller-terms/

## Assessment
- **Why it could help:** volume is the biggest lever. Many buyers cannot easily send an international bank transfer or crypto. A card/wallet link removes that friction, and the buyer pays the card fee only in the sense that KT absorbs about 5 to 6 percent (bank transfers and crypto cost KT nothing because the client pays fees).
- **Fit:** Whop is built for digital products and communities, but fixed-price service "products" with a monthly option are possible (packages, add-ons, LinkedIn Growth as a subscription).
- **Risks:** (1) a new account with a services business may face payout holds or reserves, so test small first; (2) chargebacks: $15 plus loss of funds, so keep WhatsApp and email records and the staged refund policy; (3) tax is KT's job unless tax mode is enabled; (4) KYC needs ID and bank in the country selected; Northern Cyprus is not a separate option, so KT's ID, bank and the company's registration must match what Whop accepts; (5) the Whop terms and privacy exposure must be reflected in KT's own terms if buyers are sent there; (6) a card checkout on the website would reverse the 15 Oct decision.

## Recommendation (for KT to decide)
Conditional yes, as a card option sent as a link in WhatsApp after the package is agreed (the same place the bank and crypto details are given), not on the website. That keeps the site free of a processor, stays inside the 15 Oct decision, and still removes buyer friction.
Pilot: create one Whop product (Essential, $29), complete KYC, make a small test purchase with KT's own card, withdraw to KT's bank, and note the real payout fee and timing. Only after the money arrives, add the other packages. If KT wants Whop buttons on the site, that is a separate decision (KT says OVERRIDE) and needs the services terms updated first.

## Checklist: what to check in KT's Whop account (5 minutes)
1. Dashboard > Balances: is Whop Payments set up and KYC complete? Which country is selected?
2. Which payout methods does Whop offer for that country, and what is the fee shown at Withdraw (local bank, wire, crypto)?
3. Is there any hold, reserve, or "action required" notice on the account or business classification?
4. Business page: how is the business classified, and does the product description say "CV and LinkedIn career services" (no promise of followers or engagement)?
5. Tax mode: "You handle tax", "Whop calculates; you remit" or "Whop collects and remits"? (KT should confirm with an accountant which applies.)
6. Is the account owner KT personally or KAYZ Global Ltd, and does the bank account name match?
Send screenshots or the answers and Claude will turn them into a go/no-go.

## Update 19 Oct 2026: what KT's screenshot of Whop Settings > Tax shows
Only this one page was seen (scrolled partway). Read from the image:
- **Business address on the account:** a full street address in Kyrenia, TRNC, Cyprus (apartment, block and door number, street, postcode 99300), shown with a flag icon.
- **Tax registrations:** none added. Whop's own text says: to collect tax in the UK add a UK VAT registration; for EU sales add a VAT registration for the buyer's country or an EU OSS registration. So no UK or EU tax is being collected.
- **"States you collect tax in":** "Collecting in all US states", with every state listed. So US sales tax collection is switched on by default.
- **Not visible (above the fold, and other pages):** which tax mode is selected (the optional Whop tax features cost 2% when tax is collected), the product tax category, KYC/verification status, payout method and fee, risk/holds, checkout settings, legal settings.

What it means (not tax advice; an accountant should confirm):
1. US sales tax is on by default. Whether CV/LinkedIn writing is taxable differs by US state, and with tax collection on, Whop adds tax at checkout and may charge its 2% tax fee. Check the product's tax category and consider switching collection off if an accountant agrees it does not apply.
2. No UK VAT or EU OSS registration means Whop will not collect VAT for UK/EU buyers. Whether VAT applies to a human-delivered CV service from a non-EU seller needs an accountant's answer; do not assume either way.
3. The street address on the account may appear on buyer receipts or checkout. If it is a home address, check Settings > Legal and Checkout, and consider using town-only or the company's registered address if Whop allows it.
4. Still needed before any button goes on the site: Settings > Verifications, Payments, Risk, Legal and Checkout screenshots, plus Dashboard > Balances (payout method and fee).

## Update 23 Oct 2026: the Whop account KT showed is a "connected account of Chatwait"
Two more screenshots (Developer page and Home) show:
- A blue banner: "You are viewing a connected account of Chatwait". The account is named only by an auto-generated ID (dc5d9d77-eb49-486d-883e-fad8ff84ad9a), the balance is $0.00, there are no API keys, no website, and a "Personal" account sits next to it in the account switcher.
- Whop's docs say a connected account is an Account object created by a **platform** under its own account (Whop for Platforms). The platform can onboard accounts, facilitate payments on their behalf, take application fees and manage payouts. https://docs.whop.com/manage-your-business/manage-payouts/connected-accounts.md and https://docs.whop.com/developer/platforms/enroll-connected-accounts.md
- Reading (not confirmed): this account was created for KT through Chatwait, not as KT's own stand-alone Whop business. Who controls fees, payouts, KYC, branding and what buyers see may depend on Chatwait's arrangement. Unknown: what Chatwait is and what terms KT accepted.
- Consequences if used for Kaeto Career Services: buyers would see an ID-only business name unless it can be renamed; a platform fee may apply on top of Whop's; payout and verification rules may be the platform's. Recommendation: unless KT owns Chatwait or knowingly wants this arrangement, create a separate stand-alone Whop business (the "+" next to the account switcher) under KT's own details, and complete its own verification and payout setup there. Do not build the site's checkout on this connected account until this is resolved.
