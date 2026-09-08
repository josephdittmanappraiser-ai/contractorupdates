# Daily run log

One line per run: date | threads scanned | logged | unmatched | skipped as noise

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
