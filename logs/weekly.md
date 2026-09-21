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

2026-09-21 | 169 pages refreshed (1 chunked: No Stress Claims) | 5 created | 1691 open files | 5 new clients (Easy Button Construction, Michael Young Roofing & Construction Inc., Rusty Coffman - Infinite Roofing, Baker Law, Ellah Development)

Tools connected this run. Roster + all per-client Trello pulls fanned out across ~35 subagents
(haiku for roster/tallies, opus for Linear/Strong House Pro rep attribution, sonnet for
everything else), writing raw card data to disk only -- the orchestrator never held card
content, per the token-discipline rule. Pages built deterministically from the aggregated data
via `tools/build_rep_pages.py` (the proven, tested renderer) rather than hand-authored per
page, then leak-scanned clean before publish. Publish fanned out across 19 subagents (17
EditSite batches, 1 CreateSite batch for the 5 new clients, 1 dedicated chunked-publish agent
for No Stress Claims) -- all 19 succeeded, zero failures, no empty pages.

Found and fixed mid-run: the `trelloSearch` 50-card pagination cap (previously thought specific
to No Stress Claims and Vince) also silently truncated LINEAR roofing (50 reported vs. 465
actual), Strong House Pro (50 vs. 120), and Cross country Public Adjusting (50 vs. 95). Re-pulled
all three via the reliable `list_by_board` method before building pages -- see the runbook's
updated pagination section. Also fixed a `clean_insured()` gap in `build_rep_pages.py`: a card
name with a note run on with no space before the hyphen ("Bunch-position sent to umpire") was
leaking the note as if it were part of the insured's name; the split regex now also breaks on a
hyphen immediately followed by a lowercase letter.

Rep attribution: LINEAR roofing 389 by label, 41 by Gmail cascade, 35 unassigned (of which ~12
are current staff not on the canonical rep list -- see run report). Strong House Pro 89 by
label, 9 by Gmail, 22 unassigned (14 likely-stale-roster reps). Both companies' rep-attribution
agents flagged the canonical `reps[]` list in config as probably missing a number of active
people -- worth Joseph reviewing.

One new-client label needs a human call: "Rusty Coffman - infinite roofing" was auto-created as
its own new client page, but Rusty Coffman is already a named rep on the LINEAR roofing /
Strong House Pro pages -- Joseph should confirm whether this is a separate company he runs or
should be folded into his existing rep page(s).

