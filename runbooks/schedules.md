# Schedules — how the two runs get triggered

## Status: created but disabled, one manual step needed

Both Routines exist in the account and are **disabled**:

| Routine | Cron (UTC) | Local |
|---|---|---|
| `[NEEDS CONNECTORS] Daily — contractor email → Trello log` | `20 11 * * *` | ~06:20 CT daily |
| `[NEEDS CONNECTORS] Weekly — refresh contractor Send pages` | `12 12 * * 1` | ~07:12 CT Mondays |

They are disabled on purpose. Routines created through the API cannot carry connector grants
on this account — the API rejects the `connectors` parameter with *"not available for this
organization"* — so a session fired from them would start with **no Gmail, Trello or Send
tools** and could only report that it was unable to do anything.

### The fix (one time, ~3 minutes)

Recreate both in the **claude.ai Routines UI**, which does let you attach connectors:

1. Open Routines on claude.ai → **New routine**.
2. Paste the matching prompt from below.
3. Set the schedule from the table above.
4. Attach connectors: **Gmail**, **Trello**, **Send**. (The weekly run needs all three;
   the daily run needs Gmail and Trello.)
5. Point it at this repo and environment.
6. Delete the two disabled `[NEEDS CONNECTORS]` Routines so nothing runs twice.

Cron is UTC. The local times above assume CDT (UTC−5); they land an hour earlier once
Central goes back to CST in November. Shift the hour by one if that matters.

---

## Daily prompt

```
Daily contractor email→Trello log for Joseph Dittman, TX Insurance Appraisals.

Repo: contractorupdates. The spec lives on branch `claude/contractor-weekly-updates-euy56o` —
if `runbooks/daily-email-to-trello.md` is not present on the current branch, run
`git fetch origin claude/contractor-weekly-updates-euy56o && git checkout claude/contractor-weekly-updates-euy56o` first.

READ AND FOLLOW `runbooks/daily-email-to-trello.md` EXACTLY. It is the spec, not a suggestion.

In short: find the last 24h of real file dialogue in Gmail (contractors, carriers, opposing
appraisers, umpires, PAs, attorneys, homeowners), and log each exchange onto the matching
Trello card on the Insured Appraisals board in its `📧 Email log` checklist.

Non-negotiables:
- Fan out to `sonnet` subagents, ~6 threads each, dispatched concurrently. The orchestrator
  must never pull email bodies into its own context. Discovery uses THREAD_VIEW_MINIMAL;
  subagents read with PLAIN_TEXT. Never FULL_CONTENT.
- Dialogue goes ONLY in the `📧 Email log` checklist via trelloWriteChecklist add_item.
  NEVER write a card description — `trelloWriteCard update` caps desc at 2048 chars and
  replaces it wholesale, destroying file history on longer cards.
- Skip Trello's own notification digests (do-not-reply@trello.com) — logging them loops.
- Check existing checklist items first and skip duplicates.
- Send no email. Create no cards. Move no cards between lists.

Finish by appending one line to `logs/daily.md`, committing and pushing to
`claude/contractor-weekly-updates-euy56o`, and reporting: threads scanned, exchanges logged,
and any insured named in email that has no card on the board.
```

## Weekly prompt

```
Weekly contractor status page refresh for Joseph Dittman, TX Insurance Appraisals.

Repo: contractorupdates. The spec lives on branch `claude/contractor-weekly-updates-euy56o` —
if `runbooks/weekly-send-refresh.md` is not present on the current branch, run
`git fetch origin claude/contractor-weekly-updates-euy56o && git checkout claude/contractor-weekly-updates-euy56o` first.

READ AND FOLLOW `runbooks/weekly-send-refresh.md` EXACTLY, using `config/contractors.json`
for the roster and stage map and `templates/status-page.html` for the page design and the
rules on what must never appear on a client page.

In short: for every client with open files on the Insured Appraisals board, regenerate their
Send status page so it shows where their files stand as of this morning.

Non-negotiables:
- THE SHARE URL MUST NEVER CHANGE. If the client already has a `shareId` in the config, use
  `mcp__Send__EditSite` with `fullHtml`. Only call `CreateSite` for a client with no page yet,
  then write the new shareId back into `config/contractors.json`.
- One subagent per client page, all dispatched concurrently. The orchestrator never holds
  card data. Subagents keep only card name, list name, url, lastActivityAt, loss address,
  claim # and the most recent dated note — and return compact JSON, not prose.
- Models by difficulty: `opus` for Linear/Stronghouse (they need per-rep attribution from
  Gmail), `sonnet` for ordinary company pages, `haiku` for tallies and roster diffing.
- Never put one client's files on another client's page. Never expose raw Trello list names,
  internal shorthand (OA, AD, DOA, ff), dollar figures, negotiation strategy or staff names.
- Send NO email. Make NO Trello writes — this run only reads the board.
- Pick up any new client label automatically; flag new ones so Joseph can fix the display name.

Finish by committing the updated config, appending one line to `logs/weekly.md`, pushing to
`claude/contractor-weekly-updates-euy56o`, and reporting: pages refreshed, pages created,
files with no rep resolved, and any page that came out empty.
```

---

## Running one by hand

Either run works as a plain chat message in a session that has the connectors — paste the
prompt above. Useful for testing a runbook change before it goes on the schedule.
