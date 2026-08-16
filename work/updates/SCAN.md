# Thread scan — mechanical, no judgement

You are not deciding anything. You are collecting two facts per file: which threads exist, and
what date the newest message in each one carries. Another pass decides what it means.

This exists because judgement at this step has failed twice on files the client caught himself.
Both times an agent ran a search, read the preview, saw an old date, and reported the file quiet
— while the thread ran months further and contained the decision to go to umpire.
`search_threads` returns a *preview* of a thread. The messages it leaves out are the recent ones.

So: **a search result tells you a thread id exists. Nothing more.** The only way to learn what a
thread contains is `get_thread`.

Load tools first:

```
ToolSearch query "select:mcp__Gmail__search_threads,mcp__Gmail__get_thread"
```

Your input file is named in your prompt: `{"cardId","insured","claim","address","searchAfter"}`.

## Per file

**1. Collect thread ids.** Run each of these with `view: "THREAD_VIEW_METADATA_ONLY"`,
`pageSize: 20`. Collect every thread id returned. Do not read the results for meaning.

- `"<claim number>"` if the file has one
- `"<insured surname>"`
- `"<street portion of address>"` — no city, state or zip

**2. Open every id you collected.** `get_thread` with `messageFormat: "METADATA_ONLY"` — that
returns dates and senders with no bodies, so it is cheap. Every id. Not the ones that look
promising; not the ones whose preview seemed recent. Every id.

**3. Record, per thread:** its id, the date of its newest message, and that message's sender.

Drop a thread only if every message in it is from `do-not-reply@trello.com`. Keep everything
else, including bulk status emails covering several claims — auto-replies and bounces get
judged later, not here.

## Return

```json
{"batch":0,"results":[
  {"cardId":"...","searchAfter":"2026-06-17",
   "threads":[{"id":"19c20c...","newest":"2026-08-13","from":"robert@..."}],
   "newestOverall":"2026-08-13","hasNewer":true}],
 "checked":0}
```

`hasNewer` is pure arithmetic: `newestOverall > searchAfter`. Do not reason about it.
`threads` must list every id your searches returned — an id you collected but did not open is
the exact failure this pass exists to prevent, and the audit script checks for it.

If a search returns nothing at all, return `"threads": []` and `"newestOverall": null`.

## Hygiene

No bodies, no summaries, no Trello writes, no Send, no email, no git. Overwrite your output file
every 5 files so a restart resumes cleanly.
