"""Builds the 30-day free outreach plan PDF (25 Oct - 24 Nov 2026). Run: python3 drafts/marketing/build_plan_pdf.py (needs Node + Playwright)."""
import os, subprocess, textwrap
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
SITE = "https://yirehcareers.vercel.app"

def utm(src, camp): return f"{SITE}/?utm_source={src}&utm_medium=social&utm_campaign={camp}"
def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
def copybox(title, body, tag=""):
    body = esc(body).replace("\n", "<br>")
    return f'<div class="copy"><div class="ct">{title}<span>{tag}</span></div><div class="cb">{body}</div></div>'

def table(rows, head):
    th = "".join(f"<th>{h}</th>" for h in head)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'

CH_NAME = "Yireh Careers: Verified Remote Jobs"
CH_DESC = ("Remote jobs checked by a person. Every listing links to the employer's own posting and shows who can apply, "
           "so you can skip the ones that aren't open to you. New roles every week. Check each employer's eligibility rules before you apply.")

CH_FIRST = "We've renamed! This channel is now Yireh Careers: Verified Remote Jobs.\n\nSame idea, better checking: every job links to the employer's own posting and shows who can apply. New roles every Tuesday.\n\nKnow someone job hunting? Forward this."
R1 = ("I checked 1,000+ \"remote\" job posts for who can actually apply. Only about 2 in 100 are open to applicants anywhere.\n\n"
"Context: I run a small job board (Yireh Careers) and every listing gets read for where the employer says applicants must live.\n\n"
"On 24 Oct, 1,029 remote roles on the board:\n- about 1.6% were open to applicants anywhere\n- about 26% didn't say who could apply at all\n- the rest named a country or region\n\n"
"If you apply from outside the US, these lines are worth hunting for before you spend an hour on a cover letter:\n"
"1. \"Must reside in...\" or \"authorised to work in...\"\n2. \"Overlap with [time zone] hours\"\n3. \"We hire through [country] payroll\"\n4. A state or country in the location field, even when the title says Remote\n5. Silence. If the posting never says, ask before you apply\n\n"
"What's the worst \"remote\" posting you've seen?\n\n(Disclosure: I made the board, so I'm biased. Link in the comments if the mods allow it.)")
R2 = ("Applying to remote jobs and hearing nothing? Check this before you blame your CV.\n\n"
"A lot of \"remote\" roles are only open in one country. If you're not there, your application can be ignored whatever your CV says.\n\n"
"My 30-second filter before I apply:\n1. Search the posting for \"reside\", \"authorised\" and \"time zone\"\n2. Check the location field: a country there beats the word Remote in the title\n3. Look for the company's payroll or hiring-entity country\n4. Still unclear? Email and ask before you apply\n\n"
"It saves hours a week. What do you check before applying?\n\n(I run a free job board that shows who can apply on every listing. Happy to share the link if it's allowed here.)")
R3 = ("What's the most frustrating \"remote\" posting you've seen?\n\n"
"Mine: Remote in the title, \"must be located in [one state]\" on line 14 of the description.\n\n"
"I keep a list of the sneaky ones while building a job board that labels who can apply. Share yours and I'll add the best ones to a \"read this first\" guide.")
R5 = ("How to read a remote job posting in 2 minutes (for people applying from outside the US)\n\n"
"1. Location field: country or state? That's the real rule.\n2. Search \"reside\", \"authorised to work\", \"visa\", \"sponsor\", \"time zone\", \"overlap\".\n"
"3. Payroll: \"we hire through an employer of record\" is often a good sign for international hires. It isn't a promise.\n4. Pay: shown or hidden? If hidden, ask before interview two.\n5. Date: a posting over 30 days old is usually stale.\n\n"
"I put these checks into a free board: each card shows who can apply, the original posting date and a link to the employer's own page. Mods: remove this if links aren't allowed. Not selling anything.")
F1 = ("Tired of applying for \"remote\" jobs and finding out halfway down that it's \"US residents only\"?\n\n"
"We read the whole posting for you. Every job on Yireh Careers shows who can apply, the original posting date and a direct link to the employer's own page. We never charge you to apply.\n\n"
f"See today's roles: {utm('facebook','fb-pain')}\n\nPlease check each employer's eligibility rules before you apply.")
F2 = ("Quick tip for remote job hunters: before you spend an hour on an application, search the posting for the words \"reside\", \"authorised\" and \"time zone\".\n\n"
"If the role is limited to one country, you'll usually find it there.\n\n"
f"We label this on every listing: {utm('facebook','fb-tip')}")
F3 = ("5 remote roles posted this week, with who can apply:\n\n[Paste the post from data/whatsapp_post.txt or /kit (Facebook tab), 4 to 5 jobs]\n\n"
f"All the roles and filters: {utm('facebook','fb-weekly')}")
F4 = ("Quick poll for remote job hunters: what wastes the most of your time?\n\nA. Roles that turn out to be one-country only\nB. Hidden pay\nC. Jobs that are already closed\nD. Applying and hearing nothing\n\n"
"Comment your letter. We're building the board around your answers.")
F5 = ("\"Remote\" does not always mean \"anywhere\". 3 phrases to watch for in a posting:\n\n1. \"Must reside in...\"\n2. \"Authorised to work in...\"\n3. \"Overlap with [time zone] hours\"\n\n"
f"On Yireh Careers every card says who can apply, or says \"unclear\" when the employer doesn't. {utm('facebook','fb-phrases')}")
REPLY_LINK = "Happy to share it: a free board where each card shows who can apply, the original posting date and a link to the employer's own posting. It's yirehcareers.vercel.app (I run it, so I'm biased)."
REPLY_CV = "If your CV is part of the problem, we do a free quick CV check: you email it, we reply with the three things we'd fix first. Message me and I'll send the details."
CH_POST = "New this week on the board, 3 to 5 roles with who can apply. Tap the links, they go straight to the employer's own page.\n\n[paste data/whatsapp_post.txt]\n\nForward this to one friend who's job hunting."

W = [  # (date, time, where, what, how)
 ("<b>Sun 25 Oct</b>", "19:00", "WhatsApp Channel", "Rename to the new name, paste the new description, upload the YC picture", "Channel, tap name, Edit. Text on page 3."),
 ("", "19:30", "Reddit", "Join the 5 subreddits. Read each one's rules (sidebar, \"Rules\"). Fill the rules table, page 4", "Write down: links allowed? self-promo allowed? post age or karma minimum?"),
 ("", "20:00", "Facebook", "Search and request to join 5 groups (criteria, page 5). Approval can take days", "Answer any entry questions honestly"),
 ("<b>Mon 26 Oct</b>", "18:00", "Check", "Open one tagged link on your phone, then GoatCounter: does the visit show with its source?", "Tagged links on pages 6 to 9"),
 ("<b>Tue 27 Oct</b>", "09:30", "Email", "The first weekly job email goes out (scheduled)", "Nothing to do. Claude drafts it"),
 ("", "10:00", "WhatsApp Channel", "Post the weekly roles (Claude: ask for \"weekly post\")", "Open two of the links first"),
 ("<b>Tue 27 to Sun 1 Nov</b>", "17:00 daily", "Reddit + Facebook", "15 minutes: 3 helpful comments a day on Reddit (no links), react and comment in approved Facebook groups", "Answer questions about remote work. Be useful first"),
 ("<b>Thu 29 Oct</b>", "20:30", "Facebook (first approved group)", "Post F1 (pain point)", "Use the tagged link. Reply to every comment within 24h"),
 ("<b>Sat 31 Oct</b>", "20:00", "Facebook (second group)", "Post F2 (tip)", "Different group from F1"),
 ("<b>Sun 1 Nov</b>", "18:00", "Review 1", "Fill the scorecard (page 12)", "GoatCounter, Brevo list size, channel followers"),
 ("<b>Tue 3 Nov</b>", "09:30 / 10:00", "Email + Channel", "Weekly email, then channel post", "As every Tuesday"),
 ("", "16:30", "Reddit: r/remotework", "Post R1 (data post)", "Text post. Link only in a comment, only if rules allow. Stay 2 hours and reply"),
 ("<b>Wed 4 Nov</b>", "20:30", "Facebook", "Post F3 (this week's roles)", "From /kit, Facebook tab"),
 ("<b>Thu 5 Nov</b>", "16:30", "Reddit: r/jobsearch", "Post R2 (30-second filter)", "Check this sub's rules first. If no links allowed, skip the link"),
 ("<b>Sat 7 Nov</b>", "20:00", "Facebook", "Post F1 in a third group", "Reuse the best format"),
 ("<b>Sun 8 Nov</b>", "18:00", "Review 2", "Scorecard. Which post got the most clicks?", "Keep what works"),
 ("<b>Tue 10 Nov</b>", "09:30 / 10:00", "Email + Channel", "As every Tuesday", ""),
 ("", "16:30", "Reddit: r/remotejobs", "Post R1 again, adapted (change title and first line)", "Never copy and paste the same post across subs"),
 ("<b>Wed 11 Nov</b>", "20:30", "Facebook", "Post F4 (poll)", "Polls bring comments. Reply to all"),
 ("<b>Thu 12 Nov</b>", "16:30", "Reddit: r/WorkOnline", "Post R3 (question post)", "No link in the post"),
 ("<b>Sat 14 Nov</b>", "20:00", "Facebook", "Post F5 (3 phrases)", ""),
 ("<b>Sun 15 Nov</b>", "18:00", "Review 3", "Scorecard. Kill any group with 3 posts and almost no clicks", "Page 10 rules"),
 ("<b>Tue 17 Nov</b>", "09:30 / 10:00", "Email + Channel", "As every Tuesday", ""),
 ("", "16:30", "Reddit: r/careerguidance", "Post R5 (how to read a posting)", "Advice post. Link only if rules allow"),
 ("<b>Wed 18 to Sat 21 Nov</b>", "20:30", "Facebook (best 2 groups)", "Repeat your best-performing format with fresh wording; add 2 new groups", "Two posts a week per group maximum"),
 ("<b>Thu 19 Nov</b>", "17:00", "Reddit", "Comment an update under your best post (new number, new tip)", "Keeps a good post alive"),
 ("<b>Sun 22 Nov</b>", "18:00", "Review 4", "Scorecard", ""),
 ("<b>Tue 24 Nov</b>", "09:30 / 10:00", "Email + Channel", "As every Tuesday", ""),
 ("", "18:00", "Month review", "Decide month 2: more of what worked, the services question, paid ads (page 12)", "Ask Claude to read the numbers with you"),
]

CSS = """
@font-face{font-family:Inter;src:url(file://%s/fonts/inter-latin.woff2);font-weight:100 900}
*{box-sizing:border-box}body{font-family:Inter,Arial,sans-serif;color:#1c2733;margin:0;font-size:11.5px;line-height:1.5}
.page{padding:15mm 14mm 14mm;page-break-after:always;position:relative;min-height:297mm}
.page:last-child{page-break-after:auto}
.cover{background:linear-gradient(160deg,#0b1220,#16305c 70%%,#1d4ed8);color:#fff;padding:0;min-height:297mm;display:flex;flex-direction:column;justify-content:center;padding:25mm 20mm}
.mark{width:70px;height:70px;border-radius:16px;background:linear-gradient(135deg,#3b82f6,#1d4ed8);display:flex;align-items:center;justify-content:center;margin-bottom:18px}
.cover h1{font-size:38px;line-height:1.1;margin:0 0 12px;letter-spacing:-1px}.cover p{font-size:15px;color:#c7d6f5;max-width:420px}
.pill{display:inline-block;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.25);border-radius:20px;padding:5px 12px;margin:14px 6px 0 0;font-size:12px}
h2{font-size:21px;margin:0 0 4px;color:#0f2a4d;letter-spacing:-.4px}.sub{color:#5b6877;margin:0 0 12px}
h3{font-size:13px;margin:12px 0 4px;color:#1d4ed8}
.band{height:5px;width:46px;background:#1d4ed8;border-radius:3px;margin:0 0 12px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}.grid3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px}
.card{border:1px solid #dde3ec;border-radius:10px;padding:10px 12px;background:#f7f9fc;break-inside:avoid}
.card b.n{display:inline-flex;width:22px;height:22px;border-radius:50%%;background:#1d4ed8;color:#fff;align-items:center;justify-content:center;font-size:11px;margin-right:6px}
.big{font-size:26px;font-weight:800;color:#1d4ed8;line-height:1}
.good{background:#ecfdf5;border-color:#a7f3d0}.warn{background:#fffbeb;border-color:#fde68a}.bad{background:#fef2f2;border-color:#fecaca}
table{width:100%%;border-collapse:collapse;font-size:10.2px;margin:6px 0}th{background:#0f2a4d;color:#fff;text-align:left;padding:5px 6px}
td{padding:5px 6px;border-bottom:1px solid #e6ebf2;vertical-align:top}tr:nth-child(even) td{background:#f7f9fc}tr{break-inside:avoid}
.copy{border:1px solid #bcd0f7;border-left:5px solid #1d4ed8;border-radius:8px;margin:8px 0;background:#fff;break-inside:avoid}
.ct{background:#eaf1ff;padding:5px 10px;font-weight:700;color:#0f2a4d;display:flex;justify-content:space-between}.ct span{font-weight:500;color:#5b6877}
.cb{padding:8px 11px;font-size:10.6px;white-space:normal}
.foot{position:absolute;bottom:7mm;left:14mm;right:14mm;font-size:9px;color:#8a96a6;display:flex;justify-content:space-between}
.tl{display:flex;gap:6px;margin:8px 0}.tl div{flex:1;border-radius:8px;padding:8px;color:#fff;font-size:10.5px}
ul{margin:4px 0 4px 16px;padding:0}li{margin:2px 0}
""" % ROOT

def page(inner, n):
    return f'<div class="page">{inner}<div class="foot"><span>Yireh Careers · 30-day free outreach plan</span><span>{n}</span></div></div>'

P = []
P.append(f'''<div class="page cover"><div class="mark"><svg width="46" height="46" viewBox="0 0 100 100" fill="none"><g stroke-width="11" stroke-linecap="round" stroke-linejoin="round"><path d="M25 31 L48 56 M48 56 L48 82" stroke="#fff"/><path d="M48 56 L83 17" stroke="#bfdbfe"/></g></svg></div>
<h1>30-day free outreach plan</h1><p>Where to post, what to say, when to do it and what to measure. One person, about 30 minutes a day, no ad budget.</p>
<div><span class="pill">25 Oct to 24 Nov 2026</span><span class="pill">All times: Istanbul (UTC+3)</span><span class="pill">Goal: job board visitors, then weekly email signups</span></div></div>''')

P.append(page(f'''<h2>The plan on one page</h2><div class="band"></div>
<div class="tl"><div style="background:#0f2a4d"><b>Week 0</b><br>25 to 26 Oct<br>Set up</div><div style="background:#1d4ed8"><b>Week 1</b><br>27 Oct to 1 Nov<br>Be useful first</div><div style="background:#2563eb"><b>Weeks 2 to 3</b><br>2 to 15 Nov<br>First posts</div><div style="background:#0d9488"><b>Week 4</b><br>16 to 24 Nov<br>Double down, review</div></div>
<div class="grid"><div class="card good"><b>What we post</b><p>Pain-point posts that <b>help first</b>: how to spot a "remote" job that isn't open to you. The board is the answer, never the headline.</p></div>
<div class="card good"><b>The hook nobody else has</b><p class="big">1.6%</p><p>Of 1,029 remote roles on our board (24 Oct), about 1.6% were open to applicants anywhere. It's our own data, dated and true. Refresh the number before each post (ask Claude).</p></div>
<div class="card"><b>Where</b><p>5 Reddit communities, 5 Facebook groups, your WhatsApp Channel every Tuesday, the weekly email every Tuesday.</p></div>
<div class="card"><b>What we measure</b><p>Visits per source (tagged links), email signups, channel followers, comments. One scorecard, every Sunday, page 12.</p></div></div>
<h3>Should we advertise the career services yet? My recommendation: no, not in posts.</h3>
<div class="card warn"><ul><li><b>Why:</b> strangers in a community trust a helpful stranger, not a seller. Selling a $29 to $149 service in week one gets posts removed and accounts flagged.</li>
<li><b>Also:</b> your own strategy review says we don't yet know who the paying customer is. Month one is for learning who shows up.</li>
<li><b>The soft bridge:</b> when someone in a comment says their CV is the problem, use the free CV check reply (page 9). It's free, it's a reply and not an ad, and it feeds your enquiry log.</li>
<li><b>Month 2 test:</b> if the board brings 500+ visits and people ask about CVs, add one services post in groups that allow it.</li></ul></div>
<h3>What "marketing data" can I give you honestly?</h3>
<div class="card"><p>I have <b>no performance data for Yireh Careers yet</b> (GoatCounter needs your login) and I couldn't open Reddit or Facebook from here to read live rules. So the timings and targets below are <b>starting hypotheses from standard community-marketing practice</b>, not proven for your audience. The plan is built to test them: two posting windows, one scorecard, and keep or kill rules. Paid ads: not recommended in month one (page 12).</p></div>''', 2))

P.append(page(f'''<h2>Week 0: set up (Sunday 25 Oct)</h2><div class="band"></div>
<h3>1. Rename the old WhatsApp Channel</h3>
<div class="card"><p>Open the channel, tap its name, Edit. Picture: <b>yc-mark.png</b> (drafts/whatsapp-profile).</p></div>
{copybox("Channel name", CH_NAME, "")}{copybox("Channel description", CH_DESC, f"{len(CH_DESC)} characters")}
{copybox("First post after renaming", CH_FIRST, "Sun 25 Oct, 19:15")}
<h3>2. Tagged links (so you know what works)</h3>
<p>Every link carries its source. Use exactly these; they show in GoatCounter under the source name.</p>
{table([["Reddit",f"{SITE}/?utm_source=reddit&amp;utm_medium=social&amp;utm_campaign=<i>subname</i>"],["Facebook",f"{SITE}/?utm_source=facebook&amp;utm_medium=social&amp;utm_campaign=<i>groupname</i>"],["WhatsApp channel",f"{SITE}/?utm_source=whatsapp&amp;utm_medium=channel&amp;utm_campaign=weekly"]],["Source","Link pattern"])}
<h3>3. Your profile is part of the post</h3>
<div class="card"><p><b>Reddit:</b> use your own account. Bio: "Building Yireh Careers, a free verified remote job board." Being open about it builds trust. <b>Facebook:</b> a normal profile that looks like a person. Never fake accounts or fake reviews.</p></div>''', 3))

P.append(page(f'''<h2>Reddit: 5 communities</h2><div class="band"></div>
<p class="sub">Reddit removes anything that feels like an ad. New accounts and link posts are the fastest way to be removed. So week 1 is comments only.</p>
{table([["<b>r/remotework</b>","People working or looking for remote work","R1 data post","Tue 3 Nov"],["<b>r/remotejobs</b>","Remote job seekers","R1 adapted","Tue 10 Nov"],["<b>r/jobsearch</b>","Job seekers, all kinds","R2 filter post","Thu 5 Nov"],["<b>r/WorkOnline</b>","Online work seekers","R3 question post","Thu 12 Nov"],["<b>r/careerguidance</b>","People asking for career advice","R5 advice post","Tue 17 Nov"]],["Community","Who is there","Post","Date (16:30)"])}
<div class="card bad"><b>Rules check (do on Sun 25 Oct).</b> I could not open Reddit from here, so I have not read their current rules. Subreddits change them often. For each one, read the sidebar rules, then tick:</div>
{table([["r/remotework","☐","☐","☐","☐"],["r/remotejobs","☐","☐","☐","☐"],["r/jobsearch","☐","☐","☐","☐"],["r/WorkOnline","☐","☐","☐","☐"],["r/careerguidance","☐","☐","☐","☐"]],["Subreddit","Links allowed?","Self-promo allowed?","Min account age or karma?","Needs a flair?"])}
<h3>How to post on Reddit</h3>
<ul><li><b>If links are banned:</b> post the value version with no link. Put the board in your profile bio. Share the link only if someone asks (reply on page 9).</li>
<li><b>One post per community per week, maximum.</b> Never paste the same text in two communities.</li><li>Stay 2 hours after posting and answer every comment. Replies decide whether the post lives.</li>
<li><b>Best window (hypothesis):</b> Tue to Thu, 16:30 Istanbul (morning in the US East). Test one 20:00 post in week 3.</li><li>Never ask for upvotes. Never send unrequested private messages.</li></ul>
<div class="card good"><b>If a post is removed:</b> don't argue. Read the removal note, thank the mods, and move on. A calm account lasts.</div>''', 4))

P.append(page(f'''<h2>Facebook: 5 groups</h2><div class="band"></div>
<p class="sub">I can't browse Facebook from here, so I won't invent group names. Search these phrases in Facebook's search box, choose "Groups", and pick the best 5 using the checklist.</p>
{table([["1","&quot;remote jobs&quot; or &quot;work from home jobs&quot; (global, English)","Biggest reach, most noise"],["2","&quot;remote jobs Nigeria&quot; or &quot;remote jobs Kenya&quot; or &quot;remote work Africa&quot;","Strong demand for roles open outside the US"],["3","&quot;remote jobs Philippines&quot; or &quot;remote work India&quot; or &quot;virtual assistant jobs&quot;","Large job-seeking communities"],["4","&quot;graduate jobs&quot; or your country's &quot;students and graduates career&quot; groups","Early-career audience (we say entry-level and junior, never &quot;for graduates&quot;)"],["5","&quot;expats Cyprus&quot; or &quot;jobs North Cyprus&quot; or &quot;Turkey remote work&quot;","Your home market. Easier to be trusted"]],["#","Search for","Why"])}
<h3>Pick a group only if it ticks these</h3>
<div class="grid"><div class="card good"><ul><li>5,000+ members</li><li>Posts in the last 24 hours</li><li>Rules allow links, or links in the first comment</li></ul></div><div class="card warn"><ul><li>Not a "post your link" spam wall</li><li>Admins answer members</li><li>English or a language you can reply in</li></ul></div></div>
<h3>How to post on Facebook</h3>
<ul><li><b>Request now, post later.</b> Approval takes days. Comment and react for the first week before posting.</li><li>Use <b>plain text</b>, one clear idea, the tagged link on its own line. Facebook hides posts with long link previews in some groups; if the first one doesn't show, put the link in the first comment.</li>
<li><b>Best window (hypothesis):</b> 20:00 to 21:30 Istanbul, when evening readers in Africa and Asia are online. Test one lunchtime post (13:00) in week 3.</li><li>Maximum two posts a week in any group. Reply to every comment within 24 hours.</li><li>If admins ask you to stop, stop and thank them.</li></ul>
<div class="card"><b>Don't</b> use "work from home and earn $5,000", fake urgency, or promise income. Your difference is that you check things; keep it that way.</div>''', 5))

for title, body, n in [("Copy library 1 of 3: Reddit", None, 6), ("Copy library 2 of 3: Facebook", None, 7), ("Copy library 3 of 3: replies, channel and comments", None, 8)]:
    pass
P.append(page(f'''<h2>Copy 1 of 3: Reddit posts</h2><div class="band"></div>
{copybox("R1: the data post", R1, "r/remotework Tue 3 Nov; adapt for r/remotejobs Tue 10 Nov")}{copybox("R2: the 30-second filter", R2, "r/jobsearch Thu 5 Nov")}''', 6))
P.append(page(f'''<h2>Copy 1 continued</h2><div class="band"></div>
{copybox("R3: the question post", R3, "r/WorkOnline Thu 12 Nov")}{copybox("R5: how to read a posting", R5, "r/careerguidance Tue 17 Nov")}
<div class="card warn"><b>Before posting R1:</b> refresh the numbers from the live board (ask Claude: "give me today's worldwide percentage"). Never post a number you haven't just checked.</div>''', 7))
P.append(page(f'''<h2>Copy 2 of 3: Facebook posts</h2><div class="band"></div>
{copybox("F1: the pain point", F1, "Thu 29 Oct, Sat 7 Nov, in different groups")}{copybox("F2: the tip", F2, "Sat 31 Oct")}{copybox("F3: this week's roles", F3, "Wed 4 Nov")}
{copybox("F4: the poll", F4, "Wed 11 Nov")}{copybox("F5: three phrases", F5, "Sat 14 Nov")}''', 8))
P.append(page(f'''<h2>Copy 3 of 3: replies, channel post</h2><div class="band"></div>
{copybox("Reply: someone asks for the link", REPLY_LINK, "")}{copybox("Reply: someone says their CV is the problem", REPLY_CV, "the only mention of services")}
{copybox("Weekly Channel post (every Tuesday 10:00, after the email)", CH_POST, "")}
<div class="card"><b>Voice rules for every post</b><ul><li>Say "I" on Reddit (you're a person), "we" for the brand elsewhere. No personal name or photo on the brand.</li><li>Say who can apply as the employer states it. Never say "worldwide" unless the posting does.</li><li>No "guaranteed", "no work permit needed", "only job board". Always tell people to check each employer's eligibility rules.</li><li>Short sentences. One idea. One link.</li></ul></div>''', 9))

P.append(page(f'''<h2>Calendar: 25 Oct to 24 Nov</h2><div class="band"></div><p class="sub">All times Istanbul (UTC+3). Every Tuesday: weekly email 09:30, channel post 10:00.</p>
{table([[a,b,c,d,e] for a,b,c,d,e in W[:15]],["Day","Time","Where","What","How"])}''', 10))
P.append(page(f'''<h2>Calendar, continued</h2><div class="band"></div>
{table([[a,b,c,d,e] for a,b,c,d,e in W[15:]],["Day","Time","Where","What","How"])}''', 11))

P.append(page(f'''<h2>What to track: the Sunday scorecard</h2><div class="band"></div><p class="sub">Fill this in every Sunday at 18:00. It takes 10 minutes. GoatCounter: kayzglobal.goatcounter.com, filter by source.</p>
{table([["Visits from Reddit","GoatCounter, source = reddit","","","",""],["Visits from Facebook","source = facebook","","","",""],["Visits from the channel","source = whatsapp","","","",""],["Email signups (week)","GoatCounter event conversion-signup","","","",""],["Email list size","Brevo, Job alerts","","","",""],["Channel followers","WhatsApp","","","",""],["Free CV check requests","event conversion-check","","","",""],["Best post this week","Which one, and why","","","",""]],["Number","Where to find it","Wk 1","Wk 2","Wk 3","Wk 4"])}
<div class="grid"><div class="card good"><b>Keep</b><p>Any group or sub where a post got 10+ clicks or 3+ real comments. Do more there.</p></div><div class="card bad"><b>Kill</b><p>Any group with 3 posts and almost no clicks, or any post that got removed twice. Replace it.</p></div></div>
<h3>Starting targets (assumptions, not promises)</h3>
<div class="grid3"><div class="card"><p class="big">1,000</p><p>visits in 30 days</p></div><div class="card"><p class="big">60</p><p>email signups</p></div><div class="card"><p class="big">100</p><p>channel followers</p></div></div>
<p class="sub">If you beat them, raise them. If you miss them, that's information, not failure: it tells us which channel to drop.</p>
<h3>Month 2 decision gate (Tue 24 Nov)</h3>
<div class="card"><ul><li><b>Paid ads:</b> not yet. Consider a small test (for example $5 a day on Facebook for 7 days) only if organic posts show people click and sign up. Spending before you know the message works is the expensive way to learn.</li><li><b>Services posts:</b> allowed to test once the board brings 500+ visits and CV questions appear in comments.</li><li><b>Email:</b> keep the Tuesday email. It is your best asset: people who gave you their address.</li></ul></div>''', 12))
html = f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{''.join(P)}</body></html>"
open(os.path.join(HERE, "plan.html"), "w", encoding="utf-8").write(html)
js = f"""const {{ chromium }} = require('playwright');
(async()=>{{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://{HERE}/plan.html');await p.evaluate(()=>document.fonts.ready);
await p.pdf({{path:'{HERE}/Yireh-Careers-30-day-outreach-plan.pdf',format:'A4',printBackground:true,margin:{{top:'0',bottom:'0',left:'0',right:'0'}}}});await b.close();}})();"""
open("/tmp/_plan.js", "w").write(js); subprocess.run(["node", "/tmp/_plan.js"], check=True, cwd=ROOT)
os.remove(os.path.join(HERE, "plan.html")); print("built")
