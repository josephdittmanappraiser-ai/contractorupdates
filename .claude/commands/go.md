---
description: Work autonomously — decide and act rather than checking in
---

Work this task through to a finished result without stopping to ask me things.

**Decide, don't ask.** Where a question has a reasonable answer, pick it, say which
assumption you made in one line, and keep going. Do not present me with options and wait.
If two readings of the task would produce materially different work, pick the one that
matches how this repo already does it.

**Find out rather than ask.** Most questions you would put to me are answerable from the
board export, the Trello cards, the Gmail threads, the runbooks or the config. Look first.
"Which rep owns this file?" and "does this label have a page?" are lookups, not questions.

**Verify instead of reporting.** Do not tell me something is done because a subagent said
so. Check the thing itself — `GetSite` the page and diff it against disk, re-run the
freshness gate, grep the built pages. A run that dies silently looks exactly like one that
succeeded, and that has already happened here.

**Keep going through partial failure.** If one file, page or batch fails, finish the rest
and tell me at the end what did not land and why. Do not stop the whole run on one error.

**Say what you actually did**, including what you skipped, what you assumed, and anything
you are unsure of. A confident summary that hides a gap is worse than no summary.

## Still stop and ask, only for these

- **Creating a new share URL** (`CreateSite`) for a client who already has one — that
  strands everyone holding the old link, and it cannot be undone.
- **Sending email to anyone.** No run in this repo sends email. If a task seems to need it,
  ask first.
- **Deleting or overwriting** Trello card descriptions, checklists, or published pages that
  you cannot rebuild from the export.
- **Adding a new client label to a client-facing page** where you would have to invent the
  display name a contractor sees.

Everything else — refreshing existing pages, writing checklist items, reading email,
rebuilding, committing, pushing — just do.
