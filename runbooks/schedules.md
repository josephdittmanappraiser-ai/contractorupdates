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

Retested 2026-08-16: same rejection. Every other Routine on the account is enabled; these two
are the only disabled ones, which is the tell that nothing is refreshing the pages on a
schedule yet. Until the step below is done, the pages are a snapshot, not a live view.

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

Repo: contractorupdates, branch `claude/contractor-weekly-updates-euy56o`. If
`runbooks/weekly-send-refresh.md` is not on the current branch, run
`git fetch origin claude/contractor-weekly-updates-euy56o && git checkout claude/contractor-weekly-updates-euy56o` first.

READ AND FOLLOW `runbooks/weekly-send-refresh.md`. It is the spec, not a suggestion.

The pages are NOT written by a model. `tools/build_rep_pages.py` computes them from a Trello
board export, so two runs over the same data produce identical pages. Your job is to refresh
the inputs, run the builder, pass the gate, and publish.

1. EXPORT the Insured Appraisals board to CSV and put it somewhere readable.

2. FRESHEN the open files. Only open files — never anything settled or awaiting payment.
   a. SCAN, per `work/updates/SCAN.md`: collect thread ids from Gmail searches, then call
      get_thread with METADATA_ONLY on EVERY id and record each thread's newest message date.
      No bodies, no judgement. `search_threads` returns a PREVIEW and hides recent messages —
      three files were reported quiet on the strength of one before this split existed.
   b. READ, per `work/updates/READ.md`, only the files the scan proves have newer mail. Hand
      each agent the thread ids; it does not search. It checks that a thread really belongs to
      the file (about a quarter of handed threads belong to someone with the same surname),
      reads message ATTACHMENTS as well as text (a position often goes out as an empty message
      with an estimate attached), writes new events to the card's `📋 Chain of Events`
      checklist, and returns them.
   Fan out to `sonnet`, ~6 files per agent. Expect Gmail per-minute quota errors on the scan —
   pause and retry, never skip an id.

3. BUILD:  python3 tools/build_rep_pages.py <export.csv>

4. GATE:   python3 tools/check_timeline_freshness.py <export.csv>
   Non-zero exit means a file's newest event trails its card activity with no explanation.
   Re-read those before publishing. Do not publish past a failing gate.

5. PUBLISH only the pages that changed (`git status --porcelain work/pages/`), per
   `work/publish/PUBLISH.md`. Pages over ~90KB do not fit one EditSite call — run
   `tools/split_page.py` and publish them in chunks, then check the finished size equals
   plan.json's sourceBytes exactly.

Non-negotiables:
- THE SHARE URL MUST NEVER CHANGE. Existing shareId → EditSite. CreateSite only for a client
  with no page, then write the new shareId back to `config/contractors.json`.
- Never start a publish run while another is in flight. A late-finishing writer silently
  reverts pages and both runs report success.
- Never put one client's files on another client's page. Nothing on a page may carry a raw
  Trello list name, internal shorthand, a dollar figure, negotiation strategy, a staff name,
  or a homeowner's phone or email.
- Send NO email.

Finish by committing, appending a line to `logs/weekly.md`, pushing, and reporting: pages
refreshed, files gaining events, gate result, and anything left unpublished and why.
```

---

## Running one by hand

Either run works as a plain chat message in a session that has the connectors — paste the
prompt above. Useful for testing a runbook change before it goes on the schedule.
