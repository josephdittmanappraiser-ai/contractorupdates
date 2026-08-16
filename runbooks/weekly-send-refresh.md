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

## Pages too big for one call

EditSite takes the document as a tool parameter, so a page only publishes if it fits in one
model message. Roughly **90KB is the ceiling**; past that the call fails and — this is the
dangerous part — **the live page silently keeps last week's content**. Two clients are past it:
No Stress Claims (383 files, 284KB) and Legacy Roofing (160 files, 126KB).

Do not solve this by trimming each file's chain of events. That was tried; it guts the history
the pages exist to show and still did not get No Stress under the limit — 383 files cost ~126KB
before a single event is printed.

Publish in pieces instead:

```
python3 tools/split_page.py work/pages/company-no-stress-claims.html
```

That writes `work/publish/chunks/<page>/` — a skeleton, numbered ~18KB chunks, and `plan.json`.
The split is verified in memory before anything is written: the chunks provably reassemble to
the built page byte for byte, or the script aborts.

Then, one EditSite call per step, in order:

1. `fullHtml` = the skeleton. It holds the header and count tiles plus a `<!--MORE-->` sentinel,
   so a contractor loading the page mid-publish sees a real page, not a fragment.
2. For each chunk: one edit, `<!--MORE-->` → chunk contents + newline + `<!--MORE-->`. The
   sentinel walks down the document. One chunk per call, never two.
3. Cleanup: one atomic batch deleting every `<!--C:NN-->` marker line, plus the sentinel.

Step 3 is the integrity check. Each chunk starts with a numbered marker, and edits are atomic,
so a chunk that never landed fails the cleanup batch by name instead of shipping a page with a
hole in it. Re-run that chunk's step, then retry cleanup.

Give this to a `sonnet` subagent, one per page. It retypes the chunk bodies verbatim from `cat`
(not Read — Read prefixes line numbers), and the fidelity matters: these bytes are real insured
names, addresses and claim numbers.

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

### `trelloSearch` pagination loops — handle it explicitly

On high-volume labels the `nextCursor` stops advancing and keeps returning the same page, so
a naive paginate-until-`hasNextPage`-is-false loop never terminates. Observed on
*No Stress Claims* and *Vince - assured value claims*, both of which capped at exactly 50
unique cards.

Every subagent must:
1. Dedupe by card id as it pages.
2. Stop when a page adds **zero** new ids, not when `hasNextPage` goes false.
3. Report the unique count it actually reached, and whether it stopped on a loop.

A count landing on exactly 50 or exactly 100 is a truncation signal, not a real total — say so
in the run summary and add a footer line to that client's page noting older files are not
shown. Do not silently present a truncated list as complete.

### Never cap the file list

Show **every** open file the client has. No per-stage caps, no "top N most recent", no
trimming a long page for readability. A client with 372 open files gets all 372 — they are
the ones most likely to be chasing a status, and a file missing from the page reads as a file
nobody is working. Send handles large pages; a 66KB page published fine.

The only acceptable omission is one the tooling forced (a genuine pagination cap), and that
must be stated in the page footer and the run summary.

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

**Drop non-file cards first.** Discard a card if either:
- its list name matches anything in `excludeLists` — those lists hold contact records, agent
  rules, dividers and staff tasks, not files; or
- its name or description contains an `excludeCardMarkers` string, e.g. `[NOT AN APPRAISAL]`,
  which Joseph writes on a card to take it out of the appraisal pipeline.

A "Repeat clients" contact card showing up as a file on a status page is the most likely way
this run embarrasses itself.

**Stage mapping.** Lowercase the Trello list name, test `stageMap[].matchers` as substrings,
first hit wins. Unmatched → `New / intake`. Order stages descending by `order`
(Settled first, New/intake last). Skip empty stages.

If a card lands in `New / intake` only because nothing matched, note the list name in the run
summary — it usually means a new list was added to the board and `stageMap` needs an entry.

**Voice.** One or two plain sentences per file. A roofer must understand it without knowing
the trade's jargon.

**Sanitize the card name — it is not safe to print.** Joseph appends operator notes directly
to card names, and they leak straight onto a client page. Caught in testing:
`Jerrel Hofman - DO NOT MESSAGE ANYONE ( BEN DITTMAN IS OA)`,
`Jeff McCulloch - I paid $1,250 for umpire fee. charge back.`,
`Rong Dai [CN: 033232/14003 Goodman St]`, `MARY KRANIG - roofer/ ff 08-14`.

Reduce every card name to the insured's name: drop bracketed and parenthesised segments, cut
at the first note separator (` - `, `/`, `,`), and drop tokens containing a digit, `$`, or
internal shorthand. If the remainder is not plainly a person's name, take the name from the
card description instead. Never guess, and never print the raw name as a fallback.

Never put on a page:
- raw Trello list names (they contain operator instructions)
- internal shorthand — OA, AD, DOA, ff, "position", "comparison"
- dollar figures, settlement posture, or anything about negotiating strategy
- staff names
- another client's files — this is the one that actually hurts if it slips

**A card carrying two client labels belongs on BOTH pages.** It is a file the two are working
jointly — a PA firm and a law firm on the same claim, say — and each already knows the other
is involved. Do not drop it from both as "ambiguous": that hides the file from everyone, which
is worse than either client seeing it. The no-cross-client rule exists to stop a file appearing
on the page of a client with *no* connection to it, not to suppress genuine joint work.

Mark a file `needs-you` (with a one-line `ask`) **only** when it is genuinely blocked on the
contractor: their approval of an estimate, a scope of work, a homeowner signature they must
chase. Not for anything that is merely waiting on the carrier.

### Per-rep mode (Linear, Stronghouse) — attribution cascade

Every claim is tied to a rep somewhere in email. Work the cheap bulk pass first, then fall
back to per-file identifiers for whatever is left. Do not stop at the surname pass — on its
own it left roughly half of Stronghouse's files unattributed.

**Pass 0 — the rep label on the card. Authoritative. Always check this first.**
If a card carries a label matching a rep in that company's `reps[]` (by `name`, or by
`labelName` when set), that rep owns the file. Full stop — do not run the email passes for
that card, and never let an email match override a label. Joseph puts the roofer on the card
deliberately; email inference is only a fallback for cards he has not labelled yet.

Rep labels sit alongside the company label, e.g. `LINEAR roofing` + `DFW` + `Zach Khan`.
Company labels, market labels and everything in `nonClientLabels` are not rep labels.

Note: the connector can **attach** an existing label (`trelloWriteCard action:"attach_label"`)
but **cannot create** one. New rep labels have to be made in the Trello UI first; after that a
run can attach them.

**Pass 1 — bulk surname index (one or two searches, covers most files).**
`view: "THREAD_VIEW_MINIMAL"`, `pageSize: 50`:
```
to:<domain> newer_than:180d
from:<domain> newer_than:180d
```
Subjects name the insured ("Khang truong appraisal invoice"); recipients/sender name the rep.
Map surname → rep. Cheap, and it resolves the bulk in a handful of calls.

**Pass 2 — claim number (per remaining file, and the most reliable signal there is).**
Take the claim # off the card and search it verbatim:
```
"0820277473"
```
Claim numbers are unique, so a hit is unambiguous in a way a surname never is. Read the
recipients/sender of any hit and map to a rep. Try the claim number both with and without
punctuation — the board stores forms like `7010350940-1-1` and `600-1348144`.

**Pass 3 — loss address (per file still unresolved).**
Search the street portion only — no city, no state, no ZIP:
```
"906 CAMBRIDGE DR"
```
House number plus street name is specific enough to be safe, and it survives the formatting
differences between the card and the email body.

Only after all three passes does a file go to the **unassigned** page. Report the count that
got there and which pass resolved the rest, so the cascade can be tuned.

Never guess between two reps. If two reps appear on the same claim, prefer the one on the most
recent thread, and if that is still ambiguous, use the unassigned page and say so.

**Cost control.** Passes 2 and 3 are one search per unresolved file, so they only ever run on
the residue Pass 1 could not place — never on the full file list. Batch them inside the
client's own subagent; do not fan out one subagent per file.

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
