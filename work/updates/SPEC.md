# Chain-of-events enrichment — task spec

You back-read the full email history for a batch of appraisal files, build a dated chain of
events, write it onto the Trello card, and return JSON.

**Audience for every word you write: the ROOFING CONTRACTOR who referred the file.** Not the
homeowner, not the carrier, not Joseph's staff. You work for Joseph Dittman, TX Insurance
Appraisals.

Load tools first:

```
ToolSearch query "select:mcp__Gmail__search_threads,mcp__Gmail__get_thread,mcp__Trello__trelloReadChecklist,mcp__Trello__trelloWriteChecklist"
```

Your input file is named in your prompt: an array of
`{"cardId","insured","claim","address","stage","rep","clients"}`.
`cardId` is a raw 24-char id. Wrap it for Trello as
`ari:cloud:trello::card/workspace/65d7eb00496a914bf3ffb423/<cardId>`

## Per file

**1. Find every thread — not just one.** `view: "THREAD_VIEW_MINIMAL"`, `pageSize: 20`. Try in
order, and keep going even after a hit so you collect the full picture (up to 6 threads):

- the claim number, quoted verbatim — unique, most reliable
- the insured's surname, quoted
- the street portion of the address, quoted, no city/state/zip

Ignore `do-not-reply@trello.com` digests, marketing, and empty calendar invites.
Many files appear only inside a **bulk status-check email covering several claims** — that still
counts. Cite what it says about *this* claim.

**2. Read each thread in full**, `messageFormat: "PLAIN_TEXT"`, every message oldest to newest.
This is a back-read: the whole history is the point, not just the latest state.

**3. Build the chain of events.** Every action taken or received, oldest first, as
`{"date":"YYYY-MM-DD","event":"one plain sentence"}`. Typical events: file received from the
contractor, demand sent to the carrier, carrier acknowledged, carrier named their appraiser,
inspection scheduled / held / rescheduled, estimate written, estimate sent, approval received,
agreement signed, positions exchanged, umpire named, award signed. Name who acted.
Merge duplicates — several emails about one action is ONE event. Aim for 4–15. Skip auto-replies,
read receipts and bounce noise.

**4. Write a current status** — one or two sentences on where the file stands today and what
happens next. It must say something the stage name alone does not.

**5. Flag what is needed from the contractor.** `needed` is one specific sentence, and only when
the file genuinely waits on **this contractor**: their approval of an estimate, a scope of work,
photos, a measurement, a homeowner signature they must chase, a decision. It renders in RED on
their page. Set `null` when the file waits on the carrier, the opposing appraiser, an umpire, the
homeowner directly, or Joseph. Never invent an ask to fill the field.

## Never write, in any field

- dollar figures or settlement amounts
- negotiation strategy, or how strong or weak a position is
- staff names — Erwin, Imee, Geralden, Sheila, Kristelle, Stephanie, Mark, Flo, Jia Ever
- internal shorthand OA / AD / DOA / ff / SOU / CN — write "the carrier's appraiser",
  "the signed agreement", "follow up"
- homeowner phone numbers or email addresses
- anything disparaging about the homeowner, carrier or contractor
- the words "debt collection", "past due", "charge back"

## 6. Write it to Trello

Trello is the durable record; the web page is only a view of it.

- `trelloReadChecklist` action `list_by_card` → find a checklist named `📋 Chain of Events`.
  If absent: `trelloWriteChecklist` action `create`, name `📋 Chain of Events`, pos `bottom`.
- For each event not already there: `trelloWriteChecklist` action `add_item`, pos `bottom`,
  text `YYYY-MM-DD — <event sentence>`. Read the existing items first and skip duplicates so a
  re-run never doubles up.
- **Never write a card description.** `trelloWriteCard` action `update` caps `desc` at 2048
  characters and replaces it wholesale, destroying file history. Checklists only.

## No email found

Set `"update": null`, `"timeline": []`, `"noEmail": true`, and write nothing to Trello. That is a
normal outcome — say so rather than guessing. Never fabricate history.

## Hygiene

Work one file at a time and keep only your conclusions — never accumulate email bodies.
After every 4 files, overwrite your output file with results so far so a container restart
resumes cleanly. Send no email. Do not publish to Send. Do not commit to git.

## Return exactly

```json
{"batch":0,"results":[{"cardId":"...","update":"...","needed":null,"asOf":"2026-08-14",
 "timeline":[{"date":"...","event":"..."}],"trelloItemsAdded":0,"noEmail":false}],
 "withEmail":0,"noEmail":0,"flaggedNeeded":0}
```
