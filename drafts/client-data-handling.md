# Client files: how to store, share, delete and answer data requests

For KT. Plain steps. Nothing here is published. Written 2026-10-15 from the research in this session (official pages read; items I could not verify are marked "check").

## 0. The recommendation in one paragraph

Use **Proton Drive (free account)** for client files. Reasons, all from Proton's own pages: files are end-to-end encrypted, the company is Swiss with servers in Switzerland, Germany or Norway, and its public **Data Processing Agreement applies automatically to "any business or organization using the Services, regardless of its legal form"**, so you do not have to sign anything to have the contract GDPR expects. Clients can upload through a link without making an account. Weak points: only 5 GB (plenty for CVs), the upload link shows the whole folder to whoever holds it (so use **one folder per client**), the free plan allows only **3 upload links at once** (switch each one off after the client uploads), and Proton's terms are unclear on whether a free account may be used for business, so **ask Proton in writing (template below) before you rely on it**.

**Fallback:** MEGA (20 GB free, upload-only "file request" links that let clients upload without seeing anything). I could not confirm that file requests are free, and I found no data processing agreement for it, so it is second choice. If you ever use MEGA: open it in a web browser (not an app store app), export and save your Recovery Key (if you forget the password without it, every file is lost), and turn on an authenticator-app 2FA.

**Avoid:** Google Forms/Drive (client must sign in; no consumer processing agreement), OneDrive personal, Box and Sync free plans (no usable upload link), WhatsApp as a storage place.

## 1. One-time setup (about 30 minutes, you must do this: it needs your login)

1. Go to proton.me in a browser and create a free account with a **business-only** email name (not your personal one). Use a long unique password and keep it in a password manager.
2. Turn on two-factor authentication with an authenticator app (Settings, Security).
3. Write down your recovery phrase or recovery file and keep it offline. Proton cannot read your files, so it cannot reset them for you.
4. In Proton Drive, create a top folder called `Clients`.
5. Send Proton this message and keep their reply (see the template in section 7). Until they answer, treat the account as provisional.
6. Install the log in section 5 as a spreadsheet (file: `client-data-log-template.csv`; open it in Google Sheets or Excel and keep it private).

## 2. For each new client (after they buy)

1. Pick a **client ID**: `C-2026-001`, `C-2026-002`... Never put the client's full name in a folder or file name.
2. Create `Clients/C-2026-001/` with three sub-folders: `01_Received`, `02_Working`, `03_Final`.
3. Create a **private upload link for `01_Received` only**: right-click it, Share, create a link, set the permission to **Editor** (this is what lets the client upload), set a password if you can. This link shows only that one folder.
4. Send the client this message (WhatsApp is fine for the message, not for the CV):
   > Hi [first name], thank you for choosing [package]. Please upload your current CV here: [link]. This link is private and only for your files. Please do not send your CV over WhatsApp. Also reply here with the roles you are targeting and your answers to these questions: [questions]. Your timeline starts when I have all of this.
5. When the CV has arrived, **switch the link off** (Share settings, delete link). This frees one of your 3 slots.
6. Work only inside `02_Working`. Put finished files in `03_Final`.
7. Add a row to the log: client ID, package, purchase date, onboarding-complete date.

If a client sends a CV on WhatsApp anyway: move it into `01_Received`, delete the file from the chat ("delete for everyone" and "delete for me"), turn off WhatsApp's automatic saving of media to the phone gallery, and ask them to use the link next time.

## 3. Delivering finished work

Send the final files by email attachment, or create a **view-only** Proton link with a password and an expiry date for `03_Final`. Tell the client to download and keep their own copy.

## 4. Closing a client and deleting

Decide when a client is **completed**: for Essential and Professional, when the final files and the included revision rounds are done; for Executive, when the 30-day service and the 500+ total connections target are both finished or the client ends the service. **Write the completion date in the log on that day.** Everything else follows from it.

**Your promise is deletion within 90 days of completion. Aim for day 45**, because Proton and other providers can keep backup copies for up to about 30 days after you delete (Proton: up to 30 days; MEGA says "at least 30 days"). Deleting by day 45 keeps the whole chain inside 90 days.

On the delete-by date:
1. Delete the client folder in Proton Drive, then open **Trash** and delete it permanently. Version history is removed with the file.
2. Delete any email attachments and drafts from Gmail, including Sent and Trash.
3. Delete the client's media from the WhatsApp chat, and the files from your phone, Downloads folder and desktop recycle bin.
4. Record "deleted on" and "deleted by" in the log.

Things you cannot delete yourself: the payment record at Payhip/Stripe/PayPal (kept as required for accounting) and the client's own copies. The privacy policy says so.

## 5. The log (private spreadsheet)

Columns: client ID, package, purchase date, onboarding-complete date, completed date, delete-by date (completed + 45 days), deleted-on date, data request received, data request answered. **Do not put names, emails or phone numbers in it.** Keep a second sheet or tab for the data requests (section 6). Look at the log once a week for 15 minutes: anything past its delete-by date gets deleted that day.

## 6. When someone asks for their data (access, correction, deletion, "stop emailing me")

Rules from the official guidance I read: you must reply **within one month**; it is **free**; you may ask for proof it is them but only what is reasonable (use the email or order number you already hold first; you do not need to keep a copy of their ID); you may extend by up to two further months only for genuinely complex requests, and only if you tell them within the first month; if you refuse, give your reason and tell them they can complain to the regulator. If a Turkish resident asks under the Turkish data protection law, the deadline is 30 days.

1. Put the date received in the request log and set a calendar reminder for day 28.
2. Reply with the template below.
3. Search: WhatsApp (their name and number, including linked devices), Gmail (their address and name, including Sent, Trash and Drafts), Proton Drive (their client folder), Payhip (customer record), Brevo (newsletter contact).
4. Do what they asked: send a copy, correct it, delete it, or stop emailing them. For a deletion request also remove them from Brevo and say honestly what you must keep (for example payment records).
5. Reply within the month and record the date.

Template reply:
> Hello [name], thank you for your request of [date]. To protect your information, please confirm [the email you used to order, or your order number]. I will answer by [date, one month from the day I have that confirmation]. If your request is complex I may need up to two more months and will tell you before the first month ends. There is no charge. You are also entitled to complain to [regulator].

## 7. Message to send Proton (keep their reply)

> Hello, I run a small one-person service writing CVs for individual clients. I plan to store clients' CVs and working files in a free Proton Drive account, and to receive CVs through Drive upload links. Does Proton's Free plan permit this kind of use for a small business, and does your Data Processing Agreement apply to Free accounts? Thank you.

## 8. If something goes wrong (a lost phone, a wrong email, a hacked account)

Write down what happened, when you found out, and whose files. In the UK and EU you must tell the data protection regulator **within 72 hours of becoming aware**, unless harm is unlikely, and tell the people affected without delay if the risk to them is high. Record every incident, even ones you do not report. In Turkey the law says "within the shortest time". Change passwords, remove lost-device access, and tell me; I will help you word the messages.

## 9. What I need from you to finish

1. Create the Proton account and send Proton the message in section 7. Tell me their reply.
2. Tell me your legal or trading name, your country (and city if you want it shown), and the email for privacy requests.
3. Tell me whether you use any AI tool on client documents (this must be disclosed in the policy).
4. Your Gmail: free personal or Google Workspace?
5. Do you keep your own invoices or receipts, and how long does your country require them to be kept?
