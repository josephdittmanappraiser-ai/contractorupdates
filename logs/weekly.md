# Weekly run log

One line per run: date | pages refreshed | created | open files | new clients

2026-09-09 | 103 pages refreshed (2 chunked) | 68 created | 1633 open files | 67 new clients (Cohen, Kenny North, Texco Roofing, Coastal Claims, Powerhaus Solutions, Waggoner Roofing, and 61 more -- see run report)

2026-09-14 | RUN FAILED — no Trello/Gmail/Send tools in session | 0 pages refreshed | 0 created

`ListConnectors` reports Trello, Gmail, and Send as `connected: true, enabledInChat: true`, but
no tool from any of the three was reachable via `ToolSearch` in this session — tried exact
names from the runbook (`mcp__Trello__trelloReadBoard`, `mcp__Trello__trelloSearch`,
`mcp__Trello__trelloReadCard`, `mcp__Trello__trelloWriteCard`, `mcp__Trello__trelloReadMember`,
`mcp__Send__CreateSite`, `mcp__Send__EditSite`, `mcp__Send__GetSite`, `mcp__Gmail__search_emails`,
`mcp__Gmail__get_thread`) plus broad keyword sweeps ("trello", "board label card list", "send
site html publish", "gmail search thread") — nothing beyond built-in Bash/Read/Edit/etc. and
GitHub MCP tools loaded. The explicit deferred-tools list surfaced by the harness this session
also contains zero Trello/Gmail/Send entries. No Trello board was read, no Gmail search ran, no
Send page was touched — `config/contractors.json` is unchanged from the 2026-09-09 run.

Same root cause already diagnosed in `runbooks/schedules.md` and hit by the daily run earlier
today (see `logs/daily.md` 2026-09-14 entry): a Routine created through the API cannot carry
connector grants, so a session it fires starts with no Gmail/Trello/Send tools. Worth Joseph
re-checking that only the Routines-UI weekly schedule (with Gmail+Trello+Send attached) is
enabled, and that the old API `[NEEDS CONNECTORS]` Routine is deleted, not just disabled — it
appears to have fired again today for both the daily and weekly runs.

2026-09-14 (rerun) | RUN FAILED — still no Trello/Gmail/Send tools | 0 pages refreshed | 0 created

Rerun attempted after the harness reported "MCP server disconnected" for Trello/Send/github mid-
session, then reported all three "reconnecting" and later "reconnected." Re-ran `ToolSearch`
after the reconnect notice (exact tool names, bare "trello"/"gmail" keywords, Send-specific
terms) — still zero Trello/Gmail/Send tools surfaced, only unrelated built-in tools. The
connection-state notifications are flapping without ever exposing a usable tool. No board read,
no email searched, no page touched; config unchanged. Not retrying again in this session —
this is an infrastructure issue on the Routine/connector side, not something fixable by
re-running the prompt.

2026-09-14 (manual retry) | 2 of 171 pages published (1 created, 1 edited) | 3 new clients found, 1 created | 1,677 open files across 171 pages | 3 new clients: Easy Button Construction, Baker Law, Rusty Coffman - infinite roofing (only the first is live -- see below)

Manual retry after connectors came back. All three worked this time -- the failures above were
a real infra issue, not this prompt. Roster, board export, freshening, build, gate and leak scan
all completed; publishing did not.

**Roster:** diffed board labels against `config/contractors.json`, added 3 new company entries.
*Easy Button Construction* (12 open cards) co-occurs with several existing company/rep labels
and stands alone on others -- reads as a genuine joint-referral contractor, not a label typo.
*Baker Law* (1 card) is a plain new client. *Rusty Coffman - infinite roofing* (1 card, no
LINEAR/Strong House Pro label on the card) may be the existing LINEAR rep Rusty Coffman doing
business under a different name -- flagged in the config entry's `_note` for Joseph rather than
guessed into that rep's existing page. Also flagged, not auto-merged: the label "A. Queen"
(2 open cards, LINEAR roofing) looks like a mistyped duplicate of the existing rep label
"Austin Queen"; those 2 files fall through to the normal per-rep attribution cascade instead.

**Board export:** 1,910 open cards, 67 lists, 166 labels -> `work/export-2026-09-14.csv`.

**Freshening (SCAN/READ):** of 591 open, non-settled files in scope, SCAN (metadata-only Gmail
probe) covered 434 of 591 -- 29 of 40 planned batches; batch 29 and 31-40 (~157 files) deferred.
Each 15-file SCAN batch cost 250-750K tokens, far more than planned, largely because several
subagents kept trying to "wait for a Gmail rate-limit cooldown" with a tool they don't have and
needed manual nudging back to synchronous retries -- worth tightening the SCAN.md/READ.md
instructions to rule that pattern out explicitly. Of the 303 files SCAN proved had newer mail,
READ (full thread read + Trello checklist write) covered 100 -- 10 of 31 planned batches,
stopped there to protect the publish budget. Real new events were written to each touched
card's Chain of Events checklist. **203 hasNewer=true files were not read this week** -- their
pages still show last week's chain, not silently stale, just not freshened; flagged for
priority in next week's run.

Worth Joseph's attention, surfaced during READ: a homeowner review note on one Linear card
(Momtazul Karim) says "no carrier and no claim number" but an email in the same thread shows a
real claim number already exists. Two Rong Dai (7-property homeowner) cards had checklist items
that read as already-duplicated across properties. One Ajay Palvai card has two 2026-09-08
checklist items that actually belong to a different client's (Nazmul Qureshi) claim -- left in
place, out of scope for this pass, but should be moved. One Abel Mondragon card has two
duplicate "Chain of Events" checklists and says "closed" 9/9 despite active correspondence on
9/14. A Satya Kallur card shows a carrier payment already cashed 6/30 that contradicts a later
7/25 depreciation request. Four cards (in READ batch 1: cardIds ending ...c258b2 and 3 others)
have no claim number or address on file at all and could not be verified from email.

**Build:** a bug in this week's own CSV-export step left `Sales Person` blank for every row.
That column (not a Trello label) is what `build_rep_pages.py` uses to sort LINEAR/Stronghouse
files onto each rep's own page rather than "unassigned" -- caught before publishing (every
per-rep page was about to silently collapse to unassigned), fixed by rederiving it from Pass-0
rep-label matching against the roster (480/1,910 cards), rebuilt clean. Worth fixing in
`runbooks/weekly-send-refresh.md` or the export step itself so this isn't rediscovered by hand
next time.

**Gate:** first pass found 2 unexplained-stale files (both were genuinely behind on real new
correspondence -- the exact search-preview-truncation trap the runbook warns about). A targeted
VERIFY pass re-read both and logged 8 and 6 new events respectively; second gate run came back
0 unexplained-stale.

**Leak scan:** clean. No shorthand, dollar figures, emails, or invisible characters. The scan's
"staff name" and "non-ascii" hits were both expected false positives (insureds sharing a staff
first name; the template's own visible middle-dot separator) and were left alone, not "fixed."

**What's blocked:** the Send MCP connector's OAuth token expired partway through publishing --
after Easy Button Construction was created and Texas Premier Roofing was edited, every further
`CreateSite`/`EditSite`/`GetSite` call failed with "requires re-authorization (token expired)."
This is a non-interactive session and cannot run the OAuth flow. **166 of 171 built pages are
ready and unpublished** (gate-clean, leak-scan-clean, sitting in `work/pages/`), and 2 new-client
pages (Baker Law, Rusty Coffman - infinite roofing) were never created. The publish plan is
preserved in `work/publish/w3batches/` (pub1.tsv-pub21.tsv, with done1-8.log/done9-15.log/
done16-21.log recording exactly what already succeeded) so a re-run can resume cleanly once
Joseph re-authorizes Send in claude.ai connector settings -- no other rework needed.

No page came out empty. No Trello writes beyond Chain of Events checklists on READ-touched
files. No email sent.
