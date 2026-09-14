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

