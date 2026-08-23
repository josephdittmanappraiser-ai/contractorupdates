# Daily run — log the last 24h of file dialogue onto Trello

Every exchange from the last day that belongs to an appraisal file goes onto that file's Trello
card, so the weekly page refresh summarises work already recorded.

Load tools first:

```
ToolSearch query "select:mcp__Gmail__get_thread,mcp__Trello__trelloSearch,mcp__Trello__trelloReadChecklist,mcp__Trello__trelloWriteChecklist"
```

Your input file is named in your prompt: `{"threadId","subject","lastFrom","msgs"}`. Every
thread listed has at least one message from the last 24 hours — the search already proved that.

## Per thread

**1. Open it.** `get_thread`, `messageFormat: "PLAIN_TEXT"`. Read the messages **from the last
24 hours** — those are what you are logging. Earlier messages are context, not new entries.

> Do not judge a thread from a search preview. The preview shows the OLDEST messages and hides
> recent ones; on this very run, threads matching "last 24 hours" previewed as February. You have
> the thread id precisely so you never have to guess.

**2. Decide whether it is file dialogue at all.** Keep it if it is a contractor, carrier,
opposing appraiser, umpire, public adjuster, attorney or homeowner discussing a specific
appraisal. Drop marketing, receipts, security notices, calendar noise, and anything from
`do-not-reply@trello.com` — those are echoes of the board and logging them would loop.
Say what you dropped and why.

**3. Find the card.** `trelloSearch` on the insured's name, then the claim number. Board is
Insured Appraisals. Confirm the match on claim number or property address before writing — a
surname alone is not enough; roughly a quarter of surname matches on this board are a different
person. If you cannot confidently identify the card, log nothing and report it as unmatched.

**4. Write the exchange** to the card's `📧 Email log` checklist:
`trelloReadChecklist` action `list_by_card` → if there is no `📧 Email log`, create it with
`trelloWriteChecklist` action `create`, pos `bottom`. Then `add_item`, pos `bottom`, one item
per exchange, text:

```
YYYY-MM-DD — <who> <what happened, one plain sentence>
```

Read the existing items first and skip anything already logged, so a re-run never doubles up.

**A message with no body still counts.** Positions, estimates, awards and invoices are routinely
sent as attachments with an empty message. Log what was sent, described in plain words.

**Never write a card description.** `trelloWriteCard` action `update` caps `desc` at 2048
characters and replaces it wholesale, destroying the file's history. Checklists only.

## Do not

Create cards. Move cards between lists. Send email. Publish to Send. Commit to git.

## Return

```json
{"batch":0,"results":[{"threadId":"...","cardId":"...","insured":"...","itemsAdded":0,
  "events":["YYYY-MM-DD — ..."],"outcome":"logged|dropped|unmatched","why":""}],
 "threads":0,"logged":0,"dropped":0,"unmatched":0}
```
