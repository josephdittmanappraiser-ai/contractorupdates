# Daily run — read new email, log the dialogue onto Trello

**Cadence:** every morning, ~06:20 America/Chicago.
**Goal:** every contractor/carrier/homeowner exchange from the last 24h ends up on the
matching Trello card, so Monday's page refresh is a summary of work already logged.

---

## Token discipline (read this first)

The orchestrator must **never** pull full email bodies or full card descriptions into its
own context. It discovers, batches, and dispatches. Subagents do the reading.

| Work | Who | Model |
|---|---|---|
| Thread discovery, batching, run log | orchestrator | inherited |
| Read threads + write the card log | subagent, one per batch | `sonnet` |
| Pure counting / dedupe sweeps | subagent | `haiku` |

Rules that keep the cost flat:
- Discovery always uses `view: "THREAD_VIEW_MINIMAL"` — never `FULL_CONTENT`.
- Subagents read bodies with `messageFormat: "PLAIN_TEXT"`, never `FULL_CONTENT`.
- Every subagent returns **one line per thread**, not a narrative.
- Batch ~6 threads per subagent. Fewer, fatter subagents beat many thin ones.
- Dispatch all batches in a single message so they run concurrently.

---

## Phase 1 — Discover (orchestrator)

Load tools:
`ToolSearch query "select:mcp__Gmail__search_threads,mcp__Trello__trelloSearch,mcp__Trello__trelloReadChecklist,mcp__Trello__trelloWriteChecklist,mcp__Gmail__get_thread"`

Search Gmail with `view: "THREAD_VIEW_MINIMAL"`, `pageSize: 50`:

```
newer_than:1d -in:draft -from:do-not-reply@trello.com -from:notifications-noreply@linkedin.com
```

Then drop, from the returned list, anything that is plainly not file dialogue:
calendar invites with no body, marketing (`hp.com`, `bakerbrothersplumbing`, `iink` receipts),
Google security notices, CompanyCam download links, and **all Trello notification digests**
(`do-not-reply@trello.com` — these are echoes of the board, logging them would loop).

Keep a thread if any of these is true:
- sender or recipient domain belongs to a client in `config/contractors.json`
- it carries the Gmail label `AA - Roofers emailing us` (`Label_889619139836162734`)
- the subject or snippet names an insured that exists as an open card on the board
- it is from a carrier, opposing appraiser, umpire, PA or attorney about a named file

Batch the survivors into groups of ~6 `threadId`s.

## Phase 2 — Log (subagents, `sonnet`, dispatched concurrently)

Give each subagent its batch of thread IDs and this brief:

> For each threadId: `mcp__Gmail__get_thread` with `messageFormat: "PLAIN_TEXT"`.
> Identify the insured/file the thread is about. Find the matching open card:
> `mcp__Trello__trelloSearch` action `search_cards`, query = the insured surname,
> boardIds `["ari:cloud:trello::board/workspace/65d7eb00496a914bf3ffb423/666e58adc67768660a580af4"]`.
> If no card matches, or two match ambiguously, **do not create a card** — report it as unmatched.
>
> On the matched card, append to the checklist named `📧 Email log`:
> - `mcp__Trello__trelloReadChecklist` action `list_by_card` to find it
> - if absent, `trelloWriteChecklist` action `create`, name `📧 Email log`, pos `bottom`
> - `trelloWriteChecklist` action `add_item`, pos `bottom`, text:
>   `YYYY-MM-DD · <Who> (<Company>) → <direction>: <one sentence of what was actually said>`
>
> Example: `2026-08-15 · Zach Khan (Linear) → us: asked for the approved scope of work before he pays the appraisal invoice.`
>
> Idempotency: read the existing items first. If an item already covers that date + sender + substance, skip it. Never log the same exchange twice.
> Write what was *said*, including the ask. Do not editorialise, do not add next steps, do not change the card's list, name, description, labels or due date.
> Return one line per thread: `threadId | card name or UNMATCHED | logged|skipped-duplicate`.

### Never write to Trello card descriptions
`trelloWriteCard action:"update"` caps `desc` at 2048 characters and **replaces** it wholesale.
Many cards on this board are longer than that, so a description write silently destroys file
history. Dialogue goes in the `📧 Email log` checklist. Nothing else.

## Phase 3 — Run log (orchestrator)

Append one line to `logs/daily.md` in this repo and commit:

```
2026-08-15 | 34 threads scanned | 21 logged | 4 unmatched | 9 skipped as noise
```

List the unmatched insureds by name — those are files that exist in email but not on the
board, and Joseph needs to see them.

---

## Safety rules

- **Never send or reply to email.** This run reads only.
- **Never create Trello cards.** Unmatched threads get reported, not invented.
- **Never move a card between lists.** Stage changes are a human decision.
- Homeowner contact details already live on the cards; do not copy them into the log.
- If Gmail or Trello errors out, finish the batches that work, then report which failed.
