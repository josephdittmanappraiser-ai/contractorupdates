# Weekly run — refresh every contractor's Send page

**Cadence:** Mondays, ~07:12 America/Chicago.
**Goal:** every client's link shows where their files actually stand as of this morning.
**Delivery:** refresh only. This run sends **no email** — Joseph shares links himself.

---

## The one rule that matters most

**The share URL must never change.** Contractors bookmark it.

- Client has no `shareId` in `config/contractors.json` → `mcp__Send__CreateSite` (two calls:
  `{intent, title}` alone, then `{html, intentId, title}`), then **write the shareId back to
  the config and commit**.
- Client already has a `shareId` → `mcp__Send__EditSite` with `fullHtml`. This keeps the URL.
  Never `CreateSite` for a client that already has a page — that forks a new link and strands
  everyone holding the old one.

`fullHtml` is correct here even though the tool calls it a last resort: the page is fully
regenerated from Trello every week, not reconstructed from memory, so there is no content
to silently drop.

---

## Token discipline

The orchestrator never holds card data. One subagent per client page; it pulls its own cards,
writes its own HTML, publishes, and returns ~4 fields.

| Work | Who | Model |
|---|---|---|
| Roster discovery, dispatch, config write-back, commit | orchestrator | inherited |
| Linear / Stronghouse pages (needs rep attribution) | subagent per company | `opus` |
| Ordinary company pages | subagent per 1–3 clients | `sonnet` |
| Open-card tallies, roster diffing | subagent | `haiku` |

Subagent hygiene, non-negotiable:
- Keep only `name`, `list.name`, `url`, `lastActivityAt`, loss address, claim #, and the most
  recent trailing `[YYYY-MM-DD]` note. Discard full descriptions as you go.
- Return compact JSON. No prose reports.
- Dispatch every client subagent in one message so they run concurrently.

---

## Phase 1 — Roster (orchestrator)

1. Read `config/contractors.json`.
2. Get every label on the board with at least one open card:
   `mcp__Trello__trelloReadBoard` action `list_labels` (paginate — there are >100).
3. Drop anything in `nonClientLabels`, and drop labels with zero open cards.
4. Anything left that is **not** in `contractors[]` is a new client. Add it with
   `pageMode: "company"`, `shareId: null`, and a best-guess `company` display name.
   Flag new clients in the run summary so Joseph can correct the display name.

## Phase 2 — Build (subagents, concurrent)

Each subagent gets: its label(s), the board ARI, `stageMap`, the page-mode, the existing
`shareId` (or null), and `templates/status-page.html` to follow.

**Stage mapping.** Lowercase the Trello list name, test `stageMap[].matchers` as substrings,
first hit wins. Unmatched → `New / intake`. Order stages descending by `order`
(Settled first, New/intake last). Skip empty stages.

**Voice.** One or two plain sentences per file. A roofer must understand it without knowing
the trade's jargon.

Never put on a page:
- raw Trello list names (they contain operator instructions)
- internal shorthand — OA, AD, DOA, ff, "position", "comparison"
- dollar figures, settlement posture, or anything about negotiating strategy
- staff names
- another client's files — this is the one that actually hurts if it slips

Mark a file `needs-you` (with a one-line `ask`) **only** when it is genuinely blocked on the
contractor: their approval of an estimate, a scope of work, a homeowner signature they must
chase. Not for anything that is merely waiting on the carrier.

**Per-rep mode (Linear, Stronghouse).** Build the rep index in bulk, not per file:
`to:<domain> newer_than:180d` and `from:<domain> newer_than:180d` with
`view: "THREAD_VIEW_MINIMAL"`. Subjects name the insured
("Khang truong appraisal invoice"), recipients name the rep. Map surname → rep.
Unmatched or ambiguous files go on that company's **unassigned** page. Never guess between reps.

## Phase 3 — Write back (orchestrator)

1. Record every `shareId` returned into `config/contractors.json` (including new clients and
   each per-rep entry).
2. Commit and push to `claude/contractor-weekly-updates-euy56o`.
3. Append to `logs/weekly.md`:

```
2026-08-17 | 14 pages refreshed | 2 created | 187 open files | new clients: Fox Roofing
```

4. Report to Joseph: pages refreshed, new clients found, files that could not be attributed
   to a rep, and any client whose page went empty (usually means their label was removed).

---

## Safety rules

- **No email.** Not to contractors, not to homeowners, not to carriers.
- **No Trello writes at all** in this run. It reads the board; the daily run writes to it.
- Never `CreateSite` for a client that already has a `shareId`.
- If a subagent fails, publish the rest and report the gap. A stale page is better than a
  wrong one, but a missing page is better than one with another client's files on it.
