# Daily run log

One line per run: date | threads scanned | logged | unmatched | skipped as noise

2026-09-23 | 286 threads scanned | 194 logged (across 172 threads) | 54 unmatched | 50 skipped as noise, 23 skipped as duplicate

Discovery paginated through 286 unique Gmail threads matching `newer_than:1d` (six pages of up to
50). 26 were dropped up front as plain automated/marketing noise (Intuit/Invoicely/Deluxe payment
and marketing notices, CompanyCam download links, `support@app.iink.com` payment/status/message
notifications, Send.co "new view" alerts, `ssomail.verisk.com` one-time codes, `oneinc.com` carrier
payment notices, a LinkedIn digest that slipped past the sender filter, a mailer-daemon bounce, and
four bare "Automatic reply" auto-responses with no substantive content), plus 3 Google Calendar
"Updated invitation" notices (scheduling-tool bodies, not email dialogue). The remaining 257 threads
were fanned out to 43 `sonnet` subagents (~6 threads each, dispatched concurrently across three
waves of 15/14/14 to respect this session's concurrent-subagent cap; two batches in wave 1 were
denied once by the permission classifier on first dispatch and retried successfully). Of those 257:
172 threads produced at least one new checklist entry (194 entries total — several threads bundled
multiple distinct insureds in one bulk status email, or contained more than one new dated event),
18 were pure duplicates of already-logged entries, 21 were noise the subagents caught only after
opening the thread (auto-acks, a vendor invoice, an internal automation report, a one-line reply
with no surname), and 54 had real dialogue but no matching open card on the Insured Appraisals board.

Checklist name: followed `runbooks/daily-email-to-trello.md` ("📋 Chain of Events") over the
scheduled-task prompt's stale "📧 Email log" text, consistent with the 2026-09-20 and 2026-09-22
runs' notes that the runbook is the maintained spec.

Recurring board-scope finding (continues from 2026-09-22): several more "unmatched" insureds turned
out to have a card on a *different* Trello board ("PA FILES"), not "Insured Appraisals" which this
run is scoped to — Heather Rozzell and Phillip & Amber Underwood (seen twice). Worth deciding
whether this run's scope should extend to that board.

Duplicate-checklist housekeeping notes surfaced by subagents this run (not fixed, flagged for a
human pass): several cards now carry two or even three separate checklists all named "📋 Chain of
Events" (Joe Sanchez, Srinivas Manthena, Mike Russell, Sal Marcuz, Kishore Bulusu & Anupama Mantha,
Lawrence Russell) — each subagent appended to whichever one already matched that thread's history
rather than creating a fourth, but these should be merged.

Unmatched insureds named in email with no card on the Insured Appraisals board:
- Miguel Cruz, Conifer claim PL2503538, 2702 Eagle Pass, Mesquite — attorney and carrier threads
- Griebel (Marissa Griebel), Allied Trust release agreement
- Rahul Parekh
- Katonna Cunningham, USAA claim 022550340 — recurred across 4 threads
- Mohammadershad Shaik & Sameena Mohammad, Nationwide claim 300571-GR
- Liberty Mutual claim 061852446-01 — insured never named in thread, appraiser Triston Bannister
- Lakeland West Capital XXVI / Adam McKey
- State Farm claim 43-0B3Z-137 — insured never named in thread, adjuster Eric Beasley
- Geoffrey and Latisha Mburu
- Rita Aparicio, Progressive claim 1654020-264402
- Lalitha Ranganathan & Venkateswaran Tekkalur, National General claims 260142775 and 260240713 —
  recurred across 4 threads
- Sapna Narendra / Narendra Sohanlal, Safeco claim 060801867-01 — recurring gap
- Urvish Patel, Allstate claim 0814050795, 128 Sunberry Ln, Caddo Mills
- Monique E. Johnston & Brian C. Johnston, TxDMV claim 061603262-01 — recurred across 3 threads
- Judy Hopkins, Allstate claim 0837193036
- Venkata Kota, Liberty Mutual claim 061322821 — recurring gap
- Jian Qu
- Richard E. Burns, USAA claim 011431280 — recurred across 3 threads
- Kayla Thomas, Nationwide claim 212300-GR, 3208 Jackal Dr, Lorena
- Chakravarthy, Allstate claim 000834698317
- Cadalia & Eliakim Gonsales, claim 01-008-405968 — recurring gap
- Patricia & Peter Mwangi, SageSure claim HO-2025-775945050
- Brijesh Patel, 10608 Pluchea Cove property only (his other two properties matched existing cards)
- Shaoze Ouyang, Allstate claim 000827477167, 13024 Tantivy Dr, Austin
- Stephanie Cook / William P Benavidez, claim 5393X455B
- Bryan Obermeyer, State Farm claim 43-96M4-53F, 1212 Dora St, Bedford
- Mildred Davis, claim 0817538218 — recurring gap
- Curtis & Jamie Shakotko, claim 01-009-856585, 1131 W Walker St, Denison
- Devangi, 617 Oxford Dr, Wylie (surname not given)
- Alina Oslobodyanyuk / Valerii Naida, 2304 Airport Dr, Leander
- Billy Thomas, 7820 Emerald Hill Way, N Richland Hills
- Hitarth Trivedi, 12475 Cajun Dr, Frisco
- Brackett, Prosperity Bank mortgage-waiver dispute
- Becker — two open candidate cards (Jessica Becker Matthews, Stephen Becker), could not disambiguate
- Sairam Chowdary (Kapa), Legacy Roofing estimate thread

Also flagged: Heather Rozzell and Phillip & Amber Underwood (recurred twice) have cards, but on the
"PA FILES" board rather than "Insured Appraisals" — see board-scope note above.

2026-09-22 | 327 threads scanned | 213 logged | 74 unmatched | 37 skipped as noise, 3 skipped as duplicate

Discovery paginated through 327 unique Gmail threads matching `newer_than:1d` (seven pages of up
to 50). 27 were dropped up front as plain automated noise (Send.co "new view" alerts, `support@
app.iink.com` payment/status notifications, Invoicely, CompanyCam, Trustpilot, a service-now
auto-ack, Chase/Square marketing and payment receipts, SignWell e-sign completion notices, a
stray LinkedIn digest, and 8 pure carrier auto-reply/bounce stubs with no human content). The
remaining 300 were fanned out to 50 `sonnet` subagents (~6 threads each, dispatched concurrently
across three waves of 17/17/16 to respect this session's concurrent-subagent cap). Of those 300:
213 logged, 3 skipped as exact duplicates of already-logged entries, 10 more skipped at the
subagent level as noise (automated notices, bounces, or internal self-addressed reports mixed
into an otherwise-real thread), and 74 unmatched.

Checklist name: followed `runbooks/daily-email-to-trello.md` ("📋 Chain of Events") over the
scheduled-task prompt's stale "📧 Email log" text, consistent with the 2026-09-20 run's note that
the runbook is the maintained spec.

Recurring board-scope finding (new this run, worth Joseph's attention): a large and growing share
of "unmatched" threads (21 of the 74) actually have a matching card — but that card lives on a
*different* Trello board (mostly "PA FILES", one on "OA APPRAISAL TASK"), not "Insured Appraisals"
which this run is scoped to per `config/contractors.json`. Recurring names hit this repeatedly:
Tim Redwine (3x), John Surgeon (2x), plus Natividad, Griebel, Bradshaw, Bierschenk, Balakrishnan,
Gandla, Munigety/Bitla, Kayla Thomas, Ganatra, Cho/Deolveira, Parikh, David Larson, Abilene
Swimming Club, Lakeland West Capital, Roussos, Suzanne Ramos, Mondragon, Underwood, Bernal, and
Zamarripa/Billy Thomas. If Joseph wants these logged too, the runbook's board scope needs to
either add "PA FILES" (and any other relevant boards) to Phase 2's `search_cards` call, or this
gap will keep recurring daily without ever getting card entries.

Security note: subagents encountered at least 7 separate instances this run of text embedded in
email bodies or Trello card descriptions/checklist names that read as instructions directed at an
AI agent (e.g. fake "CARD DATA FIXED" directives, a fabricated "(Claude) UPDATE" checklist entry,
a "RULE 8" escalation-demand block, "AI OA REVIEW" directive blocks, and text about "Trello
connector limitations"). In every case the subagent correctly treated this as untrusted data,
took no action on it, and logged only genuine dialogue. Worth Joseph knowing this pattern exists
across both channels (email and card content) in case it's worth investigating the source.

Unmatched insureds named in email with no card on the Insured Appraisals board (different-board
matches listed separately above are not repeated here):
- Ziqi Wang, claim TXHO-00044466
- Kostas Papageorgiou, claim 1185237, 2910 Ocean Mist Ct, Seabrook TX
- Francisco Gabino, claim 01-010-084862
- Dayna Schmidt / Nicholas Coleman, claim 3300577729 — recurred across 2 threads
- Miguel Cruz, claim PL2503538
- Lalitha Ranganathan & Venkateswaran Tekkalur, claim 260240713
- Dena (surname unknown), Liberty Mutual claim 061826503, Waco TX
- Russell Peter (no claim# given)
- Freddie Besa, Allstate claim 0831659222
- Shaoze Ouyang, Allstate claim 000827477167 — recurred across 2 threads
- Cody Wherley, Allstate claim 000795806488
- Unidentified insured, Allstate claim 000839601316
- Ben & Danielle Jackson, claim 060545725-01, 1700 Blufftop Cir, Round Rock TX
- Mario Gutierrez, 1334 Sayles Blvd
- Arthur Green, claim 0830981956
- Unidentified insured, claim 53-0G7S-634, 313 Thelma
- Unidentified insured, claim 53-0K0D-995
- James McFarland, 1103 Quaker Ridge Dr, Austin TX
- Richard Burns, USAA claim 011431280-800 — recurred across 3 threads
- Katonna Cunningham, claim 022550340-801
- Unidentified insured, Economy Preferred claim 7010483200-1
- Justin Carroll, claim 4387S386F
- Annette Hoya, Allstate claim 0758954366
- ARC Aerospace and Defense Systems, claim 43-00B6W-626
- Sydney & Christopher Spears, USAA claim 027287724
- Baldomero Alvarado, Allstate claim 0809413628
- Jeffrey Bruner, USAA claim 003273567
- Unidentified insured, USAA claim 020076526, 1108 Reed St, Hurst TX
- Judy Jordan, American National claim 42-G-4XT130
- John Brackett, State Farm claim 4396G351K
- Bryan Obermeyer, claim 43-96M4-53F, 1212 Dora St, Bedford TX
- Sairam Chowdary (no claim# given)
- No Stress Claims bulk status-check email — bundled ~34 separate files in one thread, could not
  be safely split without a clearer per-insured breakdown
- Swapnil Kadam / Cadalia Gonsales / Jaqueline "Jackie" Cortez — 3 files bundled in one thread,
  none matched cleanly (Cortez has a similarly-named card under a different first name)
- Cadalia & Eliakim Gonsales, claim 01008405968-02 — recurring gap
- Unidentified insured — panel-only thread (appraisers Mark Followwell, Alex Rippee)

Different-board matches (card exists, just not on "Insured Appraisals" — see board-scope finding
above): Veronica Natividad, Marissa/Joel Griebel, Andrew Bradshaw, Thomas Bierschenk, Veeramuthu
Balakrishnan, Bharath Gandla, Kishore Kumar Munigety & Neelima Bitla, Kayla Thomas, Manish & Avani
Ganatra, Hoseong Cho & Penelope Deolveira, John Surgeon, Deepa Parikh, David Larson, Abilene
Swimming Club Inc., Lakeland West Capital, Shannon Roussos, Suzanne Ramos, Fidencia Mondragon,
Phillip & Amber Underwood, Ofelia Bernal, Ignacio Apolinar Zamarripa, Billy Thomas, Tim Redwine.

Data-quality notes for Joseph to spot-check:
- Duplicate "📋 Chain of Events" checklists (two on one card) were hit again this run on: Lawrence
  Russell, Shellie Downing, Chad Raymond, Farassati, Hernando Velasquez (two checklists that
  actually track two different sides of the file — contractor vs. carrier appraiser — so may be
  intentional, not a duplication bug), and Shaikh. Same long-running issue noted in prior runs.
- Good news: the recurring "Rong Dai" ambiguity (7+ open rental-property cards, flagged unmatched
  in nearly every prior run since 2026-08-15) was resolved this run — 3 of his threads matched
  cleanly by claim number to 3 distinct cards.
- Two threads (1a094954d26aeb82 and 19fdee2f843541d8) turned out to be the same underlying
  Carolyn Wisco/Frank Torres file reached via two different search hits; entries were merged onto
  one card rather than logged twice.
- A contractor email (texcoroofs-style bulk thread) referenced Cadalia & Eliakim Gonsales again —
  this claim has now recurred as an unmatched gap across at least 3 separate runs.

2026-09-16 | 263 threads scanned | 188 logged | 43 unmatched | 24 skipped as noise, 16 skipped as duplicate

Highest-volume run to date. Discovery paginated through 263 unique Gmail threads matching
`newer_than:1d` (six pages of 50); ~20 were dropped up front as plain automated noise (Deluxe/
Chase/OnStar/GMC marketing, a Verisk OTP email, Google Maps contribution thanks, three Send.co
"new view" alerts, six `support@app.iink.com` job/approval notifications with no real dialogue,
two pure Allstate auto-ack/undeliverable stubs, two State Farm/Progressive autoreplies, and one
internal "inspection reminders did not go out" system alert to Joseph himself). The remaining 243
threads were fanned out to 41 `sonnet` subagents (~6 threads each, dispatched concurrently; the
session's 20-concurrent-subagent cap was hit on first dispatch for one batch, which was retried
once a slot freed and completed normally).

Unmatched insureds named in email with no card on the Insured Appraisals board:
- Billy Thomas (no claim #, ref via Lawgical/Wynn thread)
- Nelvyn Minter, Claim #1209034
- Max Holthaus, 2010 Ridgeview Rd, Salina KS — still open from prior runs
- 3847 Port Royal Dr, Dallas TX (GAF QuickMeasure forward, no insured name)
- Veeramuthu Balakrishnan, claim 061862649-01
- Alina Oslobodyanyuk/Valerii Naida, claim HO-2025-573928484
- Devangi (surname not given), claim 060629198
- Mildred Davis, claim 0817538218 — still open from 2026-09-15
- Margaret Grant(?), claim 01-009-473140 — a "Margaret Grant" gap was also flagged 2026-09-05
- Curtis and Jamie Shakotko, claim 01-009-856585
- Hitarth Trivedi, claim JFE8094 — recurred across 3 separate threads this run
- Vijaya Bandi, claim 1601394-264402
- Billy Thomas, claim 0819148271, N Richland Hills TX
- Sailaja Mahendrakar & Bharath, claim 0820685766
- Oleksii (surname unknown), claim 01-009-376909
- "Mary J" insured, Kansas, State Farm wear-and-tear denial
- Johanna Aguirre Strauss, Allstate claim 0832455752
- Sapna Narendra, claim 060801867-01
- Kalyan Parajuli, claim 01009528773 (AFICS/Homesite)
- Attorney Michael P. Bowman's client (insured not named in thread)
- Manish P. Ganatra, National General ref 260837392
- Ofelia Bernal, claim 0827947599 — two ambiguous "Bernal" cards on the board, neither matches
- Mongeau v. State Farm (no claim # given)
- New Pilgrim Rest Baptist Church, claim 0694377 (Brotherhood Mutual, commercial)
- Tarak Railkar & Anagha Railkar, claim 170529AB-001
- Allstate claim 000834698317 — insured never named in thread, recurring gap
- Sheldrake (real attorney correspondence, no card found under that name — needs a human to confirm the right card)
- Matt Riehs / Hackberry Ranchettes Lot 1 & 2, Salado TX (fence estimate, no claim #)
- Claim 5043827229-1, Foremost Insurance — recurring gap since 2026-09-09
- "Brackett" check inquiry, contractor AH Exteriors Co — recurring gap since 2026-09-05
- John Dye v. State Farm
- Jett Baker, file JDM1543, Wynn Corps LLC — recurred across 2 threads; still no matching card
- MRIDA Realty LLC / Ajay Jain, claim 196263AB — recurring gap since 2026-09-15
- Richard "Rong" Dai, 7 Kansas rental properties bundled in one status-check email (ambiguous across multiple existing Dai cards) + Christopher & Lisa Sirridge — recurring ambiguity, needs Joseph to disambiguate
- Daniel Tucker / RoofingNearMeGC, homeowner referred to only as "Sean" (no surname)
- Solomon & April Griffin, claim 033932-GR — recurring gap since 2026-09-05
- Lakeland West Capital LLC, claim KY26K2203157 (TDI complaint correspondence)
- Somya Roy, contractor Patrick Davis
- Satir, Vault Insurance claim 26PRTX899373228
- Griebel (Marissa), Allied Trust claim 2610333 — recurring gap since 2026-09-15
- Bruce Pettengill, claim 0834459380, Allstate — recurred across 2 threads
- Daniel Romero, Claim No. 2512794 (named in a Lawgical Firm bulk status update, but that claim # actually belongs to Miriam Cruz Zamora — looks like a copy/paste error in the source email, flagging rather than guessing)
- Claim 43-99M7-92V, State Farm — insured never named in thread

Resolved since 2026-09-15: Yen-Thi Kim Nguyen, John Surgeon, and Alonzo Haynes (all repeat
flags from 2026-08-15 onward) did not resurface as gaps this run.

Data-quality notes for Joseph to spot-check:
- Duplicate "📋 Chain of Events" checklists (two checklists with the same name on one card) were
  found on at least 10 cards this run: Praveen Mandali, KISHORE BULUSU & ANUPAMA MANTHA, Jin Baik
  (three checklists, not two), Chad Raymond, RAVI BHASIN, RAMON VILLAGOMEZ, HERNANDO VELASQUEZ,
  Mike Russell, GEORGE & SANDRA MAHLER TEER, and Joe Sanchez. In every case the subagent logged to
  the checklist with the most existing items and left the other untouched, per instructions — these
  are worth merging by hand.
- The Brenda Cealfarhi and (per a 2026-09-05 note) some older cards carry a checklist literally
  named "📧 Email log" instead of "📋 Chain of Events" — a second naming convention still lingers on
  the board from before this run's standard was set.
- A contractor (Texco Roofing, on the Karen Thiesse file) asked Joseph's office directly to
  "inflate" a new estimate if one had to be prepared. This was not written to the card — the
  existing log entry there already uses sanitized wording — but Joseph should be aware of the ask.
- One subagent reported observing other checklist items appearing on the Rudy Mejia Jr. and Ramon
  Villagomez cards mid-run that it did not write itself — consistent with multiple concurrent
  subagents in this run legitimately converging on the same high-traffic cards, not an error.

Unmatched insureds named in email with no card on the Insured Appraisals board:
- Suzanne Ramos (State Farm 43-0K2L-462)
- Mildred Davis (Allstate 0817538218)
- Billy / "Brackett" insured (contractor ahexteriorsco@gmail.com)
- Mohammadershad Shaik (Nationwide claim 300571-GR)
- Yen-Thi Kim Nguyen (TXIA appraisal with Michael Peterman) — also flagged 2026-08-15, still no card
- Brown (surname only, ambiguous — "Estimate Brown"/"Weather Report Brown" attachments, sender Erica@crosscountrypublicadjusting.com)
- Thiese / Thiese (Texco Roofing contact, texcoroofs@gmail.com)
- Beverly "Bev" George (State Farm 43-0M2M-552, Arlington TX)
- Tammana Nalini (John Wynn referral)
- Francisco and Isidra Gabino (claim 01010084862)
- Harold Booze
- Richard "Rong" Dai — multi-property status request, ambiguous which of his several open cards; also Lisa & Chris Sirridge, same thread
- Dale Henderson
- Michelle Hawkins
- Travelers claim JHM0516 (insured not named in thread — raccoon/ceiling loss)
- Stephanie Cook / William P Benavidez (claim 5393X455B)
- MRIDA Realty LLC / Ajay Jain (claim 196263AB)
- Karen Thiesse (Texco Roofs contact Kaisa Lupardus)
- Yatrik Munshi (Liberty Mutual claim 060515276-01)
- Salazar (ambiguous — San Antonio property, 3 open Salazar cards, none match)
- Jikai Chen
- Jerado/Jerardo Vaquera (Assurant claim 00201953271, 917 Desert Sage St)
- Richard and Phyllis Pender (claim 43-0B3Z-137)
- William "Stan" O'Hagan
- Angela Whitney (claim 01-009-632647)
- Jeff & Francine Perez (claim 068339-GR)
- Allstate claim 000834698317 (insured not named in thread)
- Alonzo Haynes (El Paso, Roto-Rooter/Assurant referral) — also flagged 2026-08-15, still no card
- Leticia Perez (Farmers claim 7010512803-1)
- Gustavo Uretafrias (RYZE Claims umpire process, claim 00300107088)
- Timothy & Valerie Redwine / Tim Redwine (claim 067417-GR and Legacy Roofing contact — same surname, two separate threads)
- Katonna Cunningham / Richard Burns (USAA claims 022550340-801 / 011431280-800)
- Robert Sloan ("Airman Robert Sloan", USAA claim)
- John Surgeon — also flagged 2026-08-15 as part of "John & Misti Surgeon", still no card
- Max Holthaus (2010 Ridgeview Rd, Salina, KS)
- Alex Salazar (claim 5378H495P)
- Eric Copeland & Tanya Rodriguez (State Farm 53-0K0D-995)
- Arthur Greene (Allstate claim 0830981956)
- Chet Cochrane (Travelers claim JHM1751)
- Veronica Natividad (Farmers claim 5044232547-1)
- Karl McGettrick (claim 43-98F2-10H)
- Marissa Griebel (Allied Trust claim 2610333)
- Lakeland West Capital / Veronica Renobato (no individual insured named)
- Benjamin Jackson (Liberty Mutual/Safeco claim 060545725-01)
- Kishore Kumar Munigety & Neelima Bitla (claim 7010483200-1-2)
- Claim HO-2026-224324287 (insured never named in thread; panel appraisers Blake Pyka & Steven Smallwood)
- Solomon & April Griffin (Nationwide claim 033932-GR) — also flagged 2026-09-05, still no card
- Venkata Nomula (claim 017781911)
- Somya Roy
- Shannon Roussos

Data-quality notes for Joseph to spot-check:
- An orchestration mixup caused batches 36 and 38 to each be dispatched twice (a genuine retry accidentally duplicated already-succeeded work, while the two batches that had actually failed to launch — 39 and 41 — were caught and dispatched separately). Subagents check for duplicate checklist substance before writing, but please glance at these cards for a possible doubled 2026-09-14 entry: George Savage - PAID, Suresh Velagapalli and Kalpana Kotapati, Guadalupe Hernandez & Alejandro Rodriguez, KISHORE BULUSU & ANUPAMA MANTHA, Timothy Mclaine - 09-16.
- Several cards already carry two separate checklists both named "📋 Chain of Events" (pre-existing, not created by this run) — worth merging: Mike Russell, Ramesh Muthukrishnan, Joe Sanchez - 09-16.
- A subagent flagged that the JESUS VIDAL and Dixie Smith cards carry identical checklist wording for an umpire-acceptance event (2026-09-08–09-11) — possibly a mismatch from an earlier run, worth a glance.
- One subagent flagged an unresolved identity/assignment dispute on the Sandra Gonzales card: the carrier's appraiser questioned why Joseph's office holds a document for a different named appraiser and asserted Joseph is not the insured's appraiser on this file; office maintained that he is.

2026-09-05 | 192 threads scanned | 144 logged | 32 unmatched | 9 skipped as noise, 7 skipped as duplicate

Unmatched insureds named in email with no card on the Insured Appraisals board:
- Margaret Grant
- Derik Disney (2317 Grant Ct, Salina, KS)
- Carlos Tremino/Trevino (claim 0822639431)
- Blanca Cazares
- John & Misti Surgeon (StarStone/Praetorian claim CSMH-00000041)
- Kenny Hancock / Kamron Chapman (Stronghouse Pro referral)
- Unnamed Princeton, TX homeowner (via Guillermo Osornio / Linear Roofing)
- Bart McKay
- Marc Dumais
- Thomas Bierschenk
- Solomon & April Griffin (Nationwide claim 033932-GR)
- Dora Solis-Gates / NextGen Construction contact (insured not named)
- Don Demonteverde
- Huy Hoang / Huy Trong Hoang
- Velasquez family — ambiguous, 3 candidate cards on the board (Hernando, Luis, Adela), needs Joseph to disambiguate
- Irma Muralles Ortiz / Gustavo Adolfo Contreras Lone (Missouri City, TX, claim 1622936)
- Joe & Elvira Ramirez (claim 0104850)
- Jacqueline E. Nations
- State Farm claim 53-0B4Z-843 (insured not named in thread)
- Travelers claim JHM0516 (insured not named in thread)
- Liberty Mutual claim 061826503-01, Waco, TX (insured not named in thread)
- Yen-Thi Kim Nguyen (SageSure claim HO-2025-415944117)
- Allstate claim 000834698317 (insured not named in thread)
- Alonzo Haynes (El Paso, referred by Roto-Rooter, denied Assurant claim, potential PA engagement)

Cards that exist but on a different board ("PA FILES"), not "Insured Appraisals" — not true gaps, but flagged:
- Jett Baker
- Patricia & Peter Mwangi

Data-quality notes for Joseph to spot-check:
- Some older cards (e.g. Carlos Solis) already carry a checklist named "📧 Email log" instead of this run's "📋 Chain of Events" — two naming conventions are now on the board; consider merging or renaming.
- Possible near-duplicate concurrent writes: Mike Russell (batch22 + batch27), Koteshwar Pilla Rao (batch07 + batch22), Bernard Nganga and Miriam Cruz Zamora (batch01 + batch30) — different threads about the same file processed in parallel batches; likely fine but worth a glance.
- One subagent (batch10) reported it initially cross-wired checklist writes across 4 cards (Coffman, Maldonado, Mogollon, Cooper) before self-correcting and re-verifying each card in place — worth a spot-check of those 4.

2026-09-08 | RUN FAILED — no Gmail/Trello tools in session | 0 scanned | 0 logged

`ListConnectors` reports Gmail and Trello as `connected: true, enabledInChat: true`, but no
Gmail or Trello tool (searched via `ToolSearch` for `mcp__Gmail__search_threads`, `trelloSearch`,
`trelloReadChecklist`, `trelloWriteChecklist`, etc., and by broad keyword) was reachable in this
session — nothing beyond the built-in Bash/Read/Edit/etc. tools and the GitHub MCP tools loaded.
No email was read, no Trello card was touched, no destructive action was taken. This looks like
the exact failure mode `runbooks/schedules.md` already diagnosed: a Routine created through the
API cannot carry connector grants, so a session it fires starts with no Gmail/Trello/Send tools.
Worth checking whether this run's trigger is still one of the old `[NEEDS CONNECTORS]` API
Routines rather than a Routines-UI schedule with Gmail + Trello attached — see schedules.md for
the one-time fix.

2026-09-07 | 69 threads scanned | 46 logged | 11 unmatched | 10 skipped as noise, 2 skipped as duplicate

Unmatched insureds named in email with no card on the Insured Appraisals board:
- Dora Solis-Gates / NextGen Construction Group contact (insured not named) — still open from prior runs
- Linear Roofing "Estimate Needed Only" thread (justinb@linearroofing.com) — window bid price question, insured not named in thread
- "Graham" — Position Estimate from David Preddy (opposing appraiser), no matching card
- Eduardo Socarras (No Stress Claims referral, claims 53-98C7-20R and 0791389760)
- Cynthia Jones Moore (No Stress Claims referral, claim 0822796115)
- Adam & Robin Wilder (No Stress Claims referral, claim 0812571388)
- Jikai Chen — only similarly-named cards on board are Shih-Ying Chen and Peter Chen, neither matches
- Angela Whitney (claim 01-009-632647)
- Grant Caldwell (claim 43-0B5H-822, El Paso, TX) — a different Caldwell family (Christopher & Karshanika, Manvel TX) has a card, not a match
- Carlos Valdez / AFICS claim 01-009-524372 — insured not named in thread
- "Coleman", 5218 Lotus St — thread resurfaced from March 2025, likely stale
- Suzanne Ramos (State Farm claim 43-0K2L-462) — 6 similarly-named "Ramos" cards on the board, none an exact match
- Marissa Griebel (Allied Trust claim 2610333)

Resolved since 2026-09-05: Blanca Cazares and Huy Hoang / Huy Trong Hoang, previously unmatched, now have cards and were logged successfully today.

Data-quality notes for Joseph to spot-check:
- Thread 1a07902b7d2e81ba (No Stress Claims bulk status-check reply) bundles 3+ separate files in one email — the subagent could not safely split it onto individual cards without a clearer per-insured breakdown, so it went to the unmatched list as one entry covering all three claims above.
- Threads 1a07712c32b68d3d and 1a06d882f3c314bf (TWIA claim 1275532) both matched the same card, "WILLIAM and ANNETTA WOMACK - 09-08" — worth confirming that's the right card given the claim correspondence goes through M&M Build Group / Bill Womack (Invesco), not directly through a Womack household contact.

2026-09-09 | 255 threads scanned | 184 logged | 55 unmatched | 5 skipped as noise, 12 skipped as duplicate

Discovery found 296 threads matching `newer_than:1d` across 6 pages; 41 were dropped before dispatch as
plain non-dialogue noise (invoicely payment notifications, iink bank-transfer notifications, DocuSign/
Adobe Sign/signNow e-signature confirmations, State Farm/Allstate auto-replies and portal boilerplate,
SiriusXM/choicehotels/awin/LinkedIn marketing, CompanyCam, a mail-bounce). The remaining 255 were
dispatched to 43 `sonnet` subagents (~6 threads each, all concurrent); 7 batches hit this session's
20-concurrent-subagent cap on the first dispatch and were retried once slots freed — all 43 completed.

Unmatched insureds named in email with no card on the Insured Appraisals board:
- Bart McKay — still open from prior runs (2026-09-05)
- Albert Rodriguez / Steven Rodriguez (Legacy Roofing GC roof inspection/report threads)
- Geoffrey and Latisha Mburu (State Farm claim 53-0B4Z-843) — the claim itself was flagged unmatched on 2026-09-05 too
- Yolanda Reyes (Texas Bulldog Law deposition threads; two separate threads, same gap)
- Patrick Masota
- Sharon Peter (vs. Travelers)
- Western Inn / Western Inn Hamilton — looks like a new commercial claim (Great Lakes Insurance SE), not yet on the board
- Irma Muralles Ortiz & Gustavo Adolfo Contreras (Missouri City, TX, claim 1622936) — still open from 2026-09-05
- Raquel Garcia / Hernandez
- Landgrebe (Riverstone BC umpire service request)
- Alfredo Rincon (only a different "Alexander Rincon" card exists)
- Kathryn Napoleon / Deselous Napoleon (Pearland, TX — two related Napoleon claims, neither matched cleanly)
- Cengiz Satir
- Roel Garcia (Acculynx photos)
- Bill Womack / TWIA claim 1275532 re-assignment thread (separate from the already-logged Womack card)
- Texco Roofing demand-letter thread — insured not named
- Ziqi Wang / Jane Huang
- Meghana & Karan Wadhwani
- Cadalia Gonsales and Eliakim Gonsales
- Ann & Tom Bierschenk
- Willy Coulter
- Peter Sharon
- Benjamin Jackson
- Richard and Phyllis Pender
- Cook/Benavidez
- Besa
- Kishore Vine
- Imran Shaik
- Jeff & Francine Perez
- Abilene Swimming Club, Inc. (commercial insured)
- 300 Quarry Rock CV, Liberty Hill — still open from prior runs, insured name not stated in thread
- Tim Redwine (Legacy Roofing claim-status thread) — still open from prior runs
- State Farm claim 43-97L7-57D — insured not named in thread
- Foremost claim 5043827229-1 — insured not named in thread
- Allstate claim 000795806488 — insured not named in thread
- Travelers claim A3G4425 — insured not named in thread
- Crawford & Company claim 036322810-800 — insured not named in thread
- Travelers claim JHM0516 — still open from 2026-09-05, insured not named in thread
- Legacy Roofing GC denial letter, claim 53-0M6M-778 — insured not named in thread

Resolved since 2026-09-05/07: nothing newly confirmed resolved this run — several names above (Bart McKay,
Irma Muralles Ortiz/Gustavo Adolfo Contreras, Travelers JHM0516, 300 Quarry Rock CV) are the same gaps
recurring across multiple runs and likely need a card created or an existing card's name corrected.

Data-quality notes for Joseph to spot-check:
- Two subagent runs (batches covering Andrei/Marie Estacio, KAL SHAH, JOSE VILLALTA, ROXANNE DYLLA;
  and Scott Povlick, Edgar Garcia Valdez, Rachel Cooper, Mazen Nabil Doha) reported that this session's
  safety classifier was rate-limited during their self-review step — their actions are very likely fine
  (both reported clean completions with specific per-card results) but are flagged for a spot-check.
- Thread 1a0815fd34f0a734 (Roxanna North bulk status-check) bundled 4 separate insureds (Britney
  Menchaca, Jason and Leticia Sharp, Jeanette Miranda, Jin Baik) — the same item was logged once on
  each of the 4 matching cards rather than invented as a single combined entry.
- Threads 19f60c365031ba7e and 19f168df5061d378 (Tania Morei umpire pick) turned out to be the same
  underlying Gmail thread reached via two different search hits — logged once, second marked duplicate.
- Batch 9's subagent reported it had to correct an initial mis-placement before finishing (cross-checked
  and re-verified in place) — worth a glance at the KAL SHAH / JEREMY CHAMPAGNE / ROXANNE DYLLA cards.

2026-09-10 | 210 threads scanned | 146 logged | 44 unmatched | 13 skipped as noise, 9 skipped as duplicate

Unmatched insureds named in email with no card on the Insured Appraisals board:
- Stephanie Cook / William Benavidez (Cook Appraisal claim 5393X455B)
- Swati Agarwal
- Angela Whitney
- Hoseong Cho & Penelope Deolveira
- Chet Cochrane
- Nalini Tammana
- Reggie Crocker
- Seenivasan Gopalsamy / Sakunthala Authimoolam
- Hitarth Trivedi

Data-quality notes for Joseph to spot-check:
- Jin Baik's card was found with TWO checklists both named "📋 Chain of Events" (likely from a prior
  run's card-creation race) — subagents were instructed to treat both as one for dedup purposes and
  add to whichever had more items, but the two checklists themselves were not merged. Worth checking
  the board for other cards with this same duplicate-checklist issue.
- Thread 1a0815fd34f0a734 (Roxanna North bulk status-check) recurred from the 2026-09-09 run — same
  bundle of 4 insureds (Britney Menchaca, Jason and Leticia Sharp, Jeanette Miranda, Jin Baik), new
  activity since then, logged once per matching card as before.
- Four subagent launches were blocked once by the permission classifier on first attempt (batches
  covering: Cook/Yanez/Tessier/Mcknab/Cartmill/Shipman; Kranig/Docs/Whitney/Bansal/Sirridge/Adams;
  Elimam/Taskiran/Mottu/Sharp/Paluri/Baptiste; Keefe/DeLeon/Malone-Mondragon-Ciambrone/Cohen/Joseph) —
  all four succeeded on immediate retry with no changes to the request.
- Batch covering C&C Long Investment / claim A00833380 included a bounced (mailer-daemon) message in
  the thread alongside real correspondence — the bounce was skipped, the real exchange was logged.

2026-09-11 | 234 threads scanned | 174 logged | 31 unmatched | 10 skipped as noise, 17 skipped as duplicate

Unmatched insureds named in email with no card on the Insured Appraisals board:
- Travelers claim A3G4425 (insured not named in thread)
- Davis Appraisal (claim 0817585771, 3795 Robinson St, Beaumont TX) — 8+ unrelated "Davis" cards on
  the board, none matching claim number or address
- HO-2026-224324287 (insured not named; appraiser Blake Pyka)
- Ben & Danielle Jackson (expired check reissue / signing-routing question)
- Kishore Jonnavittula
- Eloy Aguilar
- Steven Drachenberg (claim 061624395, 1501 Casey Ln, Round Rock)
- Srikanth Koppisetty (claim 062074716-01, 486 Martha Dr, Buda TX) — a different Koppisetty card
  exists on the board (different claim/address, already Paid), not a match
- HO-2026-772243977 (SageSure, insured not named in thread)
- Cadalia Gonsales / Eliakim Gonsales (claim 01-008-405968-02) — recurred across two threads today
- Baldomero Alvarado (2916 Highgate Ln, Allstate claim 0809413628)
- Heidi Romanick
- Bulfrano Bueno
- Monique E. Johnston & Brian C. Johnston (claim 061603262-01) — recurred across two threads today
- Linda & Chris Nelon
- Russell Peter (attorney-client email setup)
- Harold Booze
- Liberty Mutual claim 061826503-01 (insured not named in thread)
- Veeramuthu Balakrishnan
- Allstate claim 000834698317 (insured not named in thread)
- Ronald Orr
- Nationwide claim 057046-GR (insured not named in thread)
- Joe & Elvira Ramirez (claim 0104850)
- Marline Ponce DeLeon / Joseph McGettrick
- Leticia Perez (Farmers claim)
- Annie/Alonzo Haynes (Allstate)
- Kishore Kumar Munigety & Neelima Bitla (claim 7010483200-1-2)
- Foremost claim 5043827229-1 (insured not named in thread)
- Jampani Srinivas (AAA claim 017541983)
- John & Misti Surgeon (StarStone claim CSMH-00000041)
- Benavidez/Cook (State Farm claim 5393X455B, appraiser Chad Sanders)

Data-quality notes for Joseph to spot-check:
- This was an unusually high-volume day (234 candidate threads vs. ~35-190 on prior runs) — discovery
  paginated through 268 raw Gmail threads matching newer_than:1d, of which ~34 were dropped up front
  as plain automated noise (Invoicely payment notices, Send.co view alerts, Verisk OTP/survey mail,
  CompanyCam links, LinkedIn, marketing, iink approval reminders, e-signature/SignWell notices,
  calendar-invite mechanics, and auto-replies) before the remaining 234 were fanned out to 39 sonnet
  subagents (~6 threads each, dispatched concurrently across three waves).
- Two more cards found with duplicate "📋 Chain of Events" checklists (same pre-existing issue noted
  for Jin Baik on 2026-09-05): Ravi Bhasin and Jun Tian. Subagents wrote to the checklist matching the
  thread's topic on each and did not merge the duplicates — still worth Joseph merging by hand.
- One subagent (batch covering Rowe Biggs/Ronald Orr/Nationwide 057046-GR/Robert Martinez/Stovall/
  Chavez) reported it briefly mis-wrote a Biggs-related line onto the Robert Martinez card before
  self-correcting; spot-checked the Robert Martinez card afterward and its checklist is clean (all 10
  items are genuinely about that file, no stray content).
- Yen-Thi Kim Nguyen, flagged unmatched on 2026-09-05, now has a matching card ("Kim Nguyen") and was
  logged today — that gap appears resolved.

2026-09-14 | RUN FAILED — no Gmail/Trello tools in session | 0 scanned | 0 logged

Same failure mode as 2026-09-08, recurring after three successful runs (09-09, 09-10, 09-11).
`ListConnectors` again reports Gmail and Trello as `connected: true, enabledInChat: true`, but
no Gmail or Trello tool was reachable via `ToolSearch` — tried the exact names from the runbook
(`mcp__Gmail__search_threads`, `mcp__Trello__trelloSearch`, `mcp__Trello__trelloReadChecklist`,
`mcp__Trello__trelloWriteChecklist`, `mcp__Gmail__get_thread`) plus broad keyword sweeps
("email inbox message thread", "board card list workspace", "gmail search threads", "trello
search card checklist") — nothing beyond built-in Bash/Read/Edit/etc. and GitHub MCP tools
loaded. No email was read, no Trello card was touched, no destructive action was taken.

Per `runbooks/schedules.md`, this is the diagnosed failure where a Routine created through the
API cannot carry connector grants, so a session it fires starts with no Gmail/Trello/Send
tools. That the previous three runs succeeded suggests the Routines-UI fix was in place and
then this firing reverted to (or duplicated) the old disabled `[NEEDS CONNECTORS]` API Routine.
Worth Joseph re-checking that only the Routines-UI schedule is enabled and the old API Routine
is actually deleted, not just disabled.

Manual rerun attempted same day after a user request. Mid-session, github/Send/Trello MCP
servers briefly reported "disconnected" then "reconnecting"; github and two resource-listing
tools came back, but Gmail, Trello and Send tool schemas never did — repeated `ToolSearch`
calls (exact runbook names, plus "trelloSearch", "trello checklist add item card board",
"mail message search read", "Gmail") all returned no match, and `ListConnectors` kept
reporting all three as `connected: true, enabledInChat: true` throughout. Same result: 0
scanned, 0 logged, nothing touched. The connector grant is clearly not reaching this session's
tool list regardless of retries within a session — this needs a fix outside the session
(recreate/re-verify the Routines-UI schedule per `runbooks/schedules.md`), not another rerun.

2026-09-17 | RUN FAILED — Trello MCP server would not connect | 0 scanned | 0 logged

Different failure mode from 2026-09-08/09-14. `ListConnectors` reported Trello as
`connected: true, enabledInChat: true` throughout, and Gmail tools (`mcp__Gmail__search_threads`,
`mcp__Gmail__get_thread`) loaded normally via `ToolSearch`. But every Trello tool
(`mcp__Trello__trelloSearch`, `trelloReadChecklist`, `trelloWriteChecklist`) was unreachable —
`ToolSearch` reported the server itself failed with `CONNECT_TIMEOUT` ("MCP server Trello
connection timed out after 30000ms"), not a missing-grant symptom. Retried `ToolSearch` twice
more (immediately, then after a ~20s wait) with the same timeout each time.

Since Phase 1 discovery needs `trelloSearch` to match threads to cards and Phase 2 needs the
checklist tools to log anything, no useful work is possible with Gmail alone — per token
discipline, no Gmail search was run and no email body was read. No Trello card was touched, no
email was sent. This looks like a transient Trello-side outage or timeout rather than the
Routines-grant issue from 09-08/09-14 (that one showed `ListConnectors` conflicting with a
totally absent tool list at server-list level; this one is the Trello server itself timing out
on connect). Worth a rerun; if this recurs, worth checking Trello's own status/API health
alongside the Routines-UI schedule setup in `runbooks/schedules.md`.

2026-09-19 | 204 threads scanned | 157 logged | 27 unmatched | 10 skipped as noise, 10 skipped as duplicate

Both Gmail and Trello tools loaded and connected normally this run — no repeat of 09-08/09-14/
09-17's connector failures. Discovery paginated through 230 unique Gmail threads matching
`newer_than:1d` (five pages of up to 50); 26 were dropped up front as plain automated noise
(Trello/LinkedIn already excluded by query; plus Dropbox share notices, CompanyCam, QuickBooks/
Invoicely payment notices, `support@app.iink.com` signature/job notifications, a mailer-daemon
bounce, two Send.co "new view" marketing alerts, two Deluxe/Semrush marketing emails, and four
carrier auto-ack/autoreply stubs with no substantive content: two Allstate "We've received your
email" and two State Farm "Automatic reply"). The remaining 204 threads were fanned out to 34
`sonnet` subagents (~6 threads each, dispatched concurrently).

Unmatched insureds named in email with no card on the Insured Appraisals board:
- Kelly Way (contact Patricia Morton), 1339 Douglas Avenue, Flossmoor, IL 60422 — new claim, no card yet
- Insured unclear — attorney Michael Bowman thread re "Claim" (tsvenky@hotmail.com / nishant@vprealtyservices.com)
- Atman Raval & Jigisha Raval, claim 061678536-01, Safeco/Liberty Mutual
- SageSure claim HO-2026-149561270 — insured name never stated in thread
- Sairam Chowdary Kapa / Sravani Machineni, 1528 Sibley Way, Leander, TX
- Kimberly Johnson — Stronghouse appraisal demand letter thread
- Jerry Vaquera, claim #00201953271 (insured of record PennyMac Loan Services LLC)
- Harrold Booze — PA fee thread
- Michael Beasom, claim 42-G-4XT130
- Francisco Gabino, claim 01-010-084862, carrier AFICS
- Thomas Bierschenk, claim 530D0J727
- Prashanna Dhungana — roofing estimate thread
- Maribel Benavides, claim 0000222523, Wellington Insurance Group
- Annie R. Haynes & Alonzo Haynes, Allstate claim 0835428731
- Claudia & Juan Ron, claim HO-2026-589318010, 16110 Glen Mar Dr, Houston, TX
- Suzanne Ramos, State Farm claim 43-0K2L-462 — 6 "Ramos" cards on the board, none match
- Cadalia & Eliakim Gonsales, Homesite/AFICS claim 01-008-405968
- Redwine (surname only, from signed award PDF), Nationwide claim 067417-GR
- Benjamin/Danielle Jackson, 1700 Blufftop Cir, Round Rock TX, Liberty Mutual claim #060545725-01 — recurred across 2 threads
- Bruce Pettengill, Allstate — recurring gap since 09-16; card exists but only on the separate "PA FILES" board, not this one
- Rental-property water/termite umpire file between appraisers Clay Heath and Eric Anderson — insured never named in thread

Also flagged but not counted above (card(s) exist, just ambiguous — needs Joseph to disambiguate,
not a missing-card gap): Momtazul Karim (2 candidate cards), Morales (5 candidate cards),
Williams (10+ candidate cards), and a Legacy Roofing supplement-quote thread subject "Sairam"
with no insured name given.

2026-09-20 | 183 threads scanned | 62 logged (80 checklist entries — two bulk status-update emails each bundled ~10-20 separate files into one thread) | 98 unmatched | 15 skipped as noise, 8 skipped as duplicate

Highest-volume run to date. Discovery paginated through 183 unique Gmail threads matching
`newer_than:1d` (four pages of up to 50); 8 were dropped up front as plain automated noise
(a mailer-daemon bounce, three Send.co "new view" alerts, one `support@app.iink.com` claim-check
delivery notification, one LinkedIn digest, and two carrier auto-ack/autoreply stubs: USAA
"Your Email...Has Been Received" and a State Farm "Automatic reply"). The remaining 175 threads
were fanned out to 29 `sonnet` subagents (~6 threads each, dispatched concurrently in one
message); one batch (threads 1a0bca271925e15c etc.) hit this session's 20-concurrent-subagent
cap on first dispatch and was retried once slots freed — all 29 completed, plus the retry.
Two threads (Rise Public Adjusting status-update request, and a related "Additional Files"
follow-up) each bundled a large multi-file status list into a single email; subagents split
these into one checklist entry per identifiable insured on a matched card, which is why logged
entries (80) exceed logged threads (62).

Note on checklist name: the scheduled-task prompt said dialogue goes in a "📧 Email log"
checklist, but `runbooks/daily-email-to-trello.md` on this branch specifies "📋 Chain of Events"
(the same timeline the weekly page renders). Followed the runbook as authoritative since it's
the maintained spec and the prompt is a static/older copy — all entries this run went to
"📋 Chain of Events". Worth reconciling the scheduled-task prompt text if "📧 Email log" was
intentional.

Unmatched insureds named in email with no card on the Insured Appraisals board:
- Ziqi Wang
- Cadalia & Eliakim Gonsales, Homesite/AFICS claim 01-008-405968 — recurring gap
- Oscar Padilla
- Abilene Swimming Club, Inc. — recurring gap
- Judy Jordan
- Gustavo Uretafrias, RYZE Claims claim 00300107088 — recurred across 2 threads, recurring gap
- Veeramuthu Balakrishnan, claim 061862649-01 — recurring gap
- Chet Cochrane, Travelers claim JHM1751 — recurring gap
- Sarah Jimeson-Wong & Jack Wong, Nationwide claim 539787-GQ — recurred across 3 threads
- No insured named, 2448 Loch Haven Ct, Frisco, Liberty Mutual claim 060515276-01
- No insured named, claim 43-0G5R-270
- Alonzo Haynes — recurring gap
- Nicholas Coleman / Dayna Schmidt, Tower Hill claim 3300577729 — recurred across 4 threads; 3
  candidate "Coleman" cards exist on the board, none matches this claim
- Bruce Pettengill, Allstate — recurring gap
- Venkata Nomula, claim 017781911 — recurring gap
- Justin Carroll
- Heather & Brian Bevil
- Cynthia Madden, Allstate claim 0819700996, North Richland Hills — 2 candidate "Madden" cards
  on the board, neither matches
- Jayesh Patel, Safeco claim 060448447-01, 1606 Pheasant Creek Dr, Wylie
- Juan Gonzales, Conifer claim PL2503426, 1318 Jasmine Dr, Lewisville
- Annette Hoya, Allstate claim 0758954366
- Baldomero Alvarado, Allstate claim 0809413628 — recurring gap
- Devangi Nagar, claim 170529AB-001
- Omar Lopez, 3489 Jefferson Dr, Frisco
- Bryan Obermeyer, 1212 Dora St, Bedford
- Jeffrey Bruner, USAA claim 003273567
- Merrick Ales, 8509 Granada Hills Dr, Austin
- William & Maureen Rollo, 11402 Hare Trail
- Kayla Thomas, 3208 Jackal Dr, Lorena
- Urvish Patel, 128 Sunberry Ln, Caddo Mills
- Solomon & April Griffin, Nationwide claim 033932-GR — recurring gap
- Wadhwani — recurring gap
- Gordon Cloutier, Allstate claim 0817988678
- Fidencia Mondragon
- Seenivasan Gopalsamy / Sakunthala Authimoolam — recurring gap
- Griebel (Marissa), Allied Trust claim 2610333 — recurring gap
- Margaret Grant, claim 01-009-473140 — recurring gap
- Sailaja / Bharath Mahendrakar, claim 0820685766 — recurring gap
- Vijaya Bandi, claim 1601394-264402 — recurring gap
- Hitarth Trivedi, claim JFE8094 — recurring gap
- Kalyan Parajuli, claim 01009528773 — recurring gap
- Curtis Redwine
- Tim Redwine, claim 067417-GR — recurring gap
- Multiple properties, no insured named (iink signature-needed bundle thread)
- No insured named, USAA claim 023053010-801, Bangs TX (Rise Public Adjusting settlement letter)
- Kimberly Johnson — recurring gap
- Ariel Abad
- Reina Ayala
- Rong Dai — 7+ open rental-property "Dai" cards, ambiguous which; recurred across 3 threads
  today, recurring gap
- Judy Hopkins, 1115 Maria Dr
- Troy, 525 Louise St
- David Larson, 1325 Marina Grand Ter
- Jerardo Vaquero — recurring gap
- Lakeland West Capital 26, 1905 Tulane Dr, Lufkin — recurred across 4 threads today
- ARC Aerospace and Defense Systems, claim 43-...
- Spears, USAA claim 027287724
- Kishore Jonnavittula — recurring gap
- Heather Rozzell
- Winson Varghese (fire/microbial claim, ESX file) — recurred across 3 threads; the only
  "Varghese" card on the board is "MARY VARGHESE - $1000- paid" (unrelated Hail & Wind claim) —
  a subagent created an empty "📋 Chain of Events" checklist on that card while investigating
  the possible match, then correctly left it empty once it confirmed the claim didn't match;
  harmless but worth a glance
- Andrew Bradshaw, USAA claim 020622939-804
- Ronald Orr, Allstate claim 0831160627 — recurring gap
- Jeff & Francine Perez, claim 068339-GR — recurring gap
- Dena Williams
- Cody Wherley, Allstate claim 000795806488
- Jett Baker, Travelers claim JDM1543 — recurring gap
- Thomas Bierschenk, State Farm claim 53-0D0J-727 — recurring gap
- Nalini Tammana, Liberty Mutual claim 061746230 — recurring gap
- Insured unknown, 15808 Dink Pearson roof report
- Bueno — recurring gap
- Venkata Kota, Liberty Mutual claim 061322821
- Brackett (John Brackett), State Farm claim 4396G351K — recurring gap
- Tarak & Anagha Railkar, claim 170529AB-001 — recurring gap
- Sapna Narendra, claim 060801867-01 — recurring gap
- Mario (surname not given), 1334 Sayles Blvd, Abilene
- Owen / Brandy McLerran, 84 Roundabout Ln, Huntsville
- Hetvi Shah, Safeco claim 060540937-01
- James McKinney
- Curtis Salter
- Gabriela Carias Green
- Susan & Travis Crow
- Mildred Davis — recurring gap
- Johanna Aguirre Strauss, Allstate claim 0832455752 — recurring gap
- Hitanshu Bhakta d/b/a Western Inn — recurring gap
- Willie Burton
- Scott Mongeau
- John Dye — recurring gap
- Sheldrake — recurring gap
- Alphonso & Mary Ransaw
- Shayla Myricks
- Zandral Washington
- Viswanath Venugopal
- Max Holthaus — recurring gap
- Ricardo & Sylvia Ramos
- Lionel Miller
- Sang Du
- Kris'es Wholesale Seafood Inc.
- Letecia Rodriguez & Kenneth Osorio
- Donald Matson
- Daniel Porter
- Bianca Asteris
- Israel Rojas
- Phyllis Giambrone
- Kevin Locke
- Juan Rivera
- Barca (Miguel/Michael), Conifer claim PL2503538
- Ignacio, Allstate claim 0826374308, Dallas
- Andreanna Galvan, Allstate claim 0831659222, Austin
- Arthur, Allstate claim 0830981956, Leonard
- Dayna, Tower Hill claim, 270 Harvest Creek Dr
- Lalitha Ranganathan; Atman & Jigisha Raval — recurring gap
- Brian and Monique, Nationwide claim, 6313 Serpentine Dr, Killeen
- Marc Dumais — recurring gap

Data-quality notes for Joseph to spot-check:
- The Rise Public Adjusting "Status Update Request" and "Additional Files" bulk emails alone
  account for roughly 30 of the unmatched names above — none of those files have a card on this
  board yet, which may mean they belong on a different board (e.g. "PA FILES") or simply haven't
  been created here.
- See the Winson Varghese note above re: an empty checklist created on the wrong card by mistake
  during investigation — no content was written to it, safe to ignore or delete.

2026-09-25 | 338 threads scanned | 209 logged | 52 unmatched | 64 skipped as noise, 13 skipped as duplicate

Discovery paginated through 338 unique Gmail threads matching `newer_than:1d` (seven pages of up
to 50 via THREAD_VIEW_MINIMAL). 52 were dropped up front as plainly non-file-dialogue: Trello's
own notification digests, Invoicely payment receipts, `support@app.iink.com` platform automations
(job-revision/payment/approval-request notices), Google Drive/Dropbox/CompanyCam share notices,
Verisk one-time-code emails, marketing (Marriott, SiriusXM, a debt-collection-service pitch, a
Google Ads newsletter), automated carrier "We've Received Your Email"/"Automatic reply" stubs,
and two internal ops-automation emails Joseph sends himself (an inspection-reminders run report
and a bulk estimates-sent action-item list).

The remaining 286 threads were fanned out to 48 `sonnet` subagents (~6 threads each, dispatched
concurrently in one message); 10 batches plus one small leftover batch hit this session's
20-concurrent-subagent cap on first dispatch and were retried once slots freed — all 48
completed. Several cards had no "📋 Chain of Events" checklist yet and got one created; a few
long-running threads (e.g. Prasanna Govindarajan, Clayton Moke, Amy Hildebrand) were backfilled
with their full multi-week history in one pass since none of it had been logged before.

Note on checklist name: as in the 2026-09-20 run, the scheduled-task prompt said dialogue goes
in a "📧 Email log" checklist, but `runbooks/daily-email-to-trello.md` on this branch still
specifies "📋 Chain of Events". Followed the runbook as authoritative — all entries this run went
to "📋 Chain of Events". One card (Mark Celebron) already had a pre-existing "📧 Email log"
checklist from an earlier run/convention; left it untouched and created a separate
"📋 Chain of Events" checklist rather than reusing it, per the runbook's exact-name instruction.

Unmatched insureds named in email with no card on the Insured Appraisals board:
- Steven Rodriguez — Powerhaus Solutions demand, no claim # given
- Porter, 5418 Lost Tree, San Antonio, TX 78244 — new referral from Remy's Roofing
- Annette Hoya — card exists, but only on other boards ("PA FILES", "John Wynn - appraisals")
- Alex Salazar, claim 5378H495P — 4 candidate "Salazar" cards on the board, none match
- Steven Knight
- Jeaqueline Lima
- Trealla Epps
- Somya Roy
- No insured named, claim 53-93X4-55B
- John Castaneda Jr.
- Cynthia Madden, Allstate claim 0819700996 — recurred across 2 threads
- Bruce Pettengill, Allstate claim 0834459380 — recurring gap
- Abilene Swimming Club, Inc., Selective claim 22898532 — recurring gap
- Veronica Natividad
- Billy Thomas
- Mohammadershad Shaik & Sameena Mohammad, Nationwide claim 300571-GR — recurred across 2 threads
- Kamran Siddiqui
- Cruz (surname only, attorney rep-contract follow-up) — 9 candidate "Cruz" cards, none confirmable
- Johanna Aguirre Strauss — card exists, but only on the "PA FILES" board
- Robert Huddle — card exists, but only on the "PA FILES" board — recurred across 2 threads
- Deepa Parikh — card exists, but only on the "PA FILES" board
- Billy Ray
- Urvish Patel, 128 Sunberry Ln, Caddo Mills
- Joseph McGettrick / McGettrick family
- Sairam Chowdary
- Misti/John Surgeon, StarStone claim CSMH-00000041
- Momtazul Karim, Travelers — 2 candidate cards exist but under a different carrier (State Farm)
- Cadalia & Eliakim Gonsales, Homesite/AFICS claim 01-008-405968 — recurring gap, recurred across
  2 threads
- Darlean Fulton
- ARC Aerospace / Syeda Nargis
- Lakeland West Capital XXVI / Adam McKey
- Walker — "Walker v. Homeowners of America" — 2 candidate "Walker" cards, neither matches this
  carrier/attorney
- Dena Williams
- Jakai Chen
- Ben & Danielle Jackson — recurring gap
- Francisco (surname not given), AFICS claim 01-010-084862
- Richard Burns, claim 01008405968-02
- Katonna Cunningham, claim 022550340-801
- Marline Ponce De Leon
- Lauren Brandon
- Shaoze Ouyang, Allstate claim 000827477167
- No insured named, Liberty Mutual claim 060448447 ("Pheasant" address)
- David Larson, claim 01010023446
- No insured named, claim HO-2026-224324287
- Veeramuthu Balakrishnan — recurring gap
- Abdelaziz, State Farm claim 1697W017W
- Alonzo Haynes — recurring gap

Data-quality notes for Joseph to spot-check:
- Several names above recur day over day (Balakrishnan, Gonsales, Jackson, Pettengill, Haynes,
  Abilene Swimming Club) — worth checking whether these files belong on a different board, need a
  card created here, or are already closed elsewhere.
- Four insureds (Aguirre Strauss, Huddle, Parikh, Hoya) have real cards, but on the "PA FILES" or
  other boards rather than "Insured Appraisals" — the runbook scopes card search to the Insured
  Appraisals board only, so these read as unmatched even though a card exists.
