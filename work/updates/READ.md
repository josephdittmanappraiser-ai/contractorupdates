# Read the threads the scan proved are newer

The scan already did the finding. For each file it opened every thread the searches turned up
and recorded the newest message date in each. You are handed those thread ids. **You do not
search.** Searching is how the last two passes went wrong — they searched, read a preview, and
concluded a file was quiet while its thread ran months further.

**Audience for every word you write: the ROOFING CONTRACTOR who referred the file.** Not the
homeowner, not the carrier, not Joseph's staff. You work for Joseph Dittman, TX Insurance
Appraisals.

Load tools first:

```
ToolSearch query "select:mcp__Gmail__get_thread,mcp__Trello__trelloReadChecklist,mcp__Trello__trelloWriteChecklist"
```

Your input file is named in your prompt:
`{"cardId","insured","claim","address","searchAfter","threads":[{"id","newest","from"}]}`.
`cardId` is a raw 24-char id. Wrap it for Trello as
`ari:cloud:trello::card/workspace/65d7eb00496a914bf3ffb423/<cardId>`

## Per file

**1. Open every thread whose `newest` is later than `searchAfter`.** `get_thread`,
`messageFormat: "PLAIN_TEXT"`. Read the messages after `searchAfter` — that is the part missing
from the file's record.

**2. Decide whether the thread is actually about this file.** The scan searched by surname,
claim number and street, so it collected threads about *other people who share a surname*. Check
the claim number, the property address, and the insured's full name. A thread about a different
insured is not this file's history — drop it and say so in `notes`. This is the one judgement
call in the pass, and getting it wrong puts one client's file on another client's page.

**3. Build the new events**, oldest first, as `{"date":"YYYY-MM-DD","event":"one plain sentence"}`.
Only events after `searchAfter`. Name who acted. Merge duplicates — several emails about one
action is ONE event. Skip auto-replies, read receipts, out-of-office notices and bounces.

**4. Write a fresh `update`** — one or two sentences on where the file stands today and what
happens next. It must say something the stage name alone does not.

**5. Set `needed`** only when the file genuinely waits on **this contractor**: their approval of
an estimate, a scope of work, photos, a measurement, a homeowner signature they must chase, a
decision. It renders in RED on their page. `null` when it waits on the carrier, the opposing
appraiser, an umpire, the homeowner directly, or Joseph. Never invent an ask to fill the field.

**6. Write the new events to Trello.** `trelloReadChecklist` action `list_by_card` → find the
checklist named `📋 Chain of Events` (create it with `trelloWriteChecklist` action `create`,
pos `bottom`, if absent). Add each new event with action `add_item`, pos `bottom`, text
`YYYY-MM-DD — <event sentence>`. Read the existing items first and skip duplicates so a re-run
never doubles up. **Never write a card description** — `trelloWriteCard` action `update` caps
`desc` at 2048 characters and replaces it wholesale, destroying file history.

## An empty message body does not mean nothing happened

The single most important action on a file — the position going to the carrier's appraiser — is
often sent as **attachments with no body text at all**. The message is a bare reply chain; the
event lives entirely in the filenames:

```
JENNIFER-COMPIAN1 JENNIFER~SCOMPIAN.ESX
JENNIFER-COMPIAN1_FINAL_DRAFT_DEPREC_CAR.pdf
photo_report_compressed_(3).pdf
```

That is a position being sent, and a pass that reads only prose records nothing for that date.
It happened: the file showed "no further correspondence" from mid-July while the position had
gone out on the 25th.

So **read the `attachments` array on every message, not just the text**, and treat a meaningful
attachment as an event in its own right:

| Attachment looks like | The event |
|---|---|
| `*.ESX`, `*ESTIMATE*`, `*DEPREC*`, `*_FINAL_DRAFT*` | our position or estimate was sent |
| `*photo*report*` | supporting photo documentation was sent |
| `*DOA*`, `*SOU*`, `*AGREEMENT*` | the signed agreement was exchanged |
| `*AWARD*` | an award was issued or circulated |
| `*INVOICE*`, `*W-9*` | an invoice or tax form was exchanged |

Describe what was sent in plain words — "sent his position: the estimate, the depreciation
summary and the photo report" — never the raw filename, which carries internal shorthand.
`get_thread` with `messageFormat: "PLAIN_TEXT"` returns `attachments` alongside the body, so
this costs nothing extra.

## Never write, in any field

Dollar figures or settlement amounts · negotiation strategy or how strong a position is · staff
names (Erwin, Imee, Geralden, Sheila, Kristelle, Stephanie, Mark, Flo, Jia Ever) · the shorthand
OA / AD / DOA / ff / SOU / CN — write "the carrier's appraiser", "the signed agreement", "follow
up" · homeowner phone numbers or email addresses · anything disparaging about the homeowner,
carrier or contractor · the words "debt collection", "past due", "charge back".

## Hygiene

One file at a time; keep only your conclusions, never accumulate email bodies. Overwrite your
output file every 4 files so a restart resumes cleanly. No email. No Send. No git.

## Return

```json
{"batch":0,"results":[{"cardId":"...","newEvents":[{"date":"...","event":"..."}],
 "update":"...","needed":null,"threadsRead":["19c20c..."],"threadsDropped":["19abc..."],
 "trelloItemsAdded":0,"notes":""}],
 "checked":0,"withNewEvents":0}
```

If every thread turned out to belong to someone else, return `"newEvents": []` and say which
threads you dropped and why. That is a real answer. "I found nothing" without naming what you
opened is not.
