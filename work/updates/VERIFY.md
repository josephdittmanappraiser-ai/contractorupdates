# Verify "nothing newer" — and fix it where it is wrong

A previous pass reported these files quiet past a certain date. On one file that claim was
wrong twice in a row, with a confident explanation attached both times. Your job is to settle
it per file, and correct the ones that are wrong.

Load tools first:

```
ToolSearch query "select:mcp__Gmail__search_threads,mcp__Gmail__get_thread,mcp__Trello__trelloReadChecklist,mcp__Trello__trelloWriteChecklist"
```

Your input file is named in your prompt: records of
`{"cardId","insured","claim","address","stage","clients","searchAfter","claimedNoNewer"}`.
`cardId` is a raw 24-char id. Wrap it for Trello as
`ari:cloud:trello::card/workspace/65d7eb00496a914bf3ffb423/<cardId>`

## The trap you are here to avoid

**`search_threads` shows you a preview of a thread, not the thread.** The messages it leaves out
are usually the recent ones — on the file that started this, the preview ended in March while the
thread ran to August and contained the decision to go to umpire. Two agents read the preview and
reported the file quiet.

So `search_threads` is for finding thread **ids**. Nothing else. Every judgement about what a
thread contains comes from `get_thread`.

## Per file

**1. Search for anything after `searchAfter`.** Run each of these, `pageSize: 20`:

- `"<claim number>" after:<searchAfter>` — quote the claim number, use `YYYY/MM/DD`
- `"<insured surname>" after:<searchAfter>`
- `"<street portion of address>" after:<searchAfter>` — no city, state or zip

Discard hits that are only `do-not-reply@trello.com` digests, marketing, calendar invites,
auto-replies, out-of-office notices and bounces. Note that a bulk status email covering several
claims **does** count if it says something about this claim.

**2. If nothing real comes back**, the file is genuinely quiet. Return
`"verified": true, "hasNewer": false` and one sentence in `"evidence"` naming the searches you
ran. Do not invent a reason the file is quiet — "no email after <date> on claim, surname or
address searches" is the whole answer.

**3. If something real comes back**, `get_thread` each id with `messageFormat: "PLAIN_TEXT"` and
read to the last message. Then:

- Build the events after `searchAfter` as `{"date":"YYYY-MM-DD","event":"one plain sentence"}`.
- Write each new one to the card's `📋 Chain of Events` checklist —
  `trelloReadChecklist` action `list_by_card` first, then `trelloWriteChecklist` action
  `add_item`, pos `bottom`, text `YYYY-MM-DD — <event sentence>`. Read the existing items and
  skip duplicates. **Never write a card description.**
- Write a fresh `"update"`: one or two sentences on where the file stands now and what happens
  next.
- Set `"needed"` only if the file genuinely waits on **this contractor** — their approval, a
  signature they must chase, photos, a measurement, a decision. `null` when it waits on the
  carrier, the opposing appraiser, an umpire, the homeowner or Joseph.

## Never write, in any field

Dollar figures or settlement amounts · negotiation strategy or how strong a position is · staff
names (Erwin, Imee, Geralden, Sheila, Kristelle, Stephanie, Mark, Flo, Jia Ever) · the shorthand
OA / AD / DOA / ff / SOU / CN — write "the carrier's appraiser", "the signed agreement", "follow
up" · homeowner phone numbers or email addresses · anything disparaging · the words "debt
collection", "past due", "charge back".

Audience for every word: the roofing contractor who referred the file.

## Hygiene

One file at a time; keep conclusions, never accumulate email bodies. Overwrite your output file
every 4 files so a restart resumes cleanly. No email. No Send. No git.

## Return

```json
{"batch":0,"results":[{"cardId":"...","verified":true,"hasNewer":false,"evidence":"...",
 "newEvents":[{"date":"...","event":"..."}],"update":null,"needed":null,
 "trelloItemsAdded":0}],
 "checked":0,"corrected":0}
```

`update` stays null when `hasNewer` is false — the existing one still stands.
