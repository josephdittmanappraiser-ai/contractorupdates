# Contractor updates

Keeps every contractor and referral partner current on their appraisal files without
Joseph answering "any update on so-and-so?" one email at a time.

Two scheduled runs, one shared source of truth.

```
  Gmail ──daily──▶ Trello card  ──weekly──▶ Send page ──▶ contractor's bookmark
          (log the      (📧 Email log        (one link,
           dialogue)     checklist)           stable URL)
```

**Trello is the source of truth.** Nothing here keeps a second copy of file state.
The pages are a read-only view of the Insured Appraisals board, written in language a
roofer understands.

---

## The two runs

| | Daily | Weekly |
|---|---|---|
| When | ~06:20 CT, every day | Mondays ~07:12 CT |
| Reads | last 24h of Gmail | the whole board |
| Writes | `📧 Email log` checklist on cards | the Send pages |
| Sends email | never | never |
| Runbook | [`runbooks/daily-email-to-trello.md`](runbooks/daily-email-to-trello.md) | [`runbooks/weekly-send-refresh.md`](runbooks/weekly-send-refresh.md) |

The daily run does the expensive reading, so Monday is just a summary of work already logged.

## Who gets a page

Every Trello label with at least one open card counts as a client, minus the ones listed in
`nonClientLabels` (markets like *Houston*, difficulty tags like *Hard*, staff tags like
*Erwin's task*). New contractors are picked up automatically — the first weekly run after
their label appears creates their page.

- **Linear Roofing** and **Stronghouse Pro** get **one page per rep**, plus an
  *unassigned* page for files whose rep could not be resolved from email.
  These two are affiliated: the same person often holds both a `@linearroofing.com` and a
  `@stronghousepro.com` address, and is treated as one rep.
- **Everyone else** gets **one page per company**, all reps sharing it.

## What a contractor sees

Their open files grouped by a plain-language stage, furthest-along first, each with one or
two sentences on what is actually happening. Files blocked on *them* are called out in
orange with a specific ask.

Deliberately absent: raw Trello list names, internal shorthand (OA, AD, DOA, ff), dollar
figures, negotiation strategy, staff names, and — most importantly — any other client's files.

The nine client-facing stages, defined in `config/contractors.json`:

```
9 Settled / invoicing                      4 Appraisal demanded / waiting on carrier
8 In umpire                                3 Estimate sent - needs sign-off
7 Negotiating with the carrier's appraiser 2 Estimate being prepared
6 Inspected / building our position        1 New / intake
5 Inspection scheduling
```

## Layout

```
config/contractors.json          roster, stage map, non-client labels, shareIds
runbooks/daily-email-to-trello.md
runbooks/weekly-send-refresh.md
templates/status-page.html       reference page: structure, CSS, writing rules
logs/                            one line per run
```

---

## Cost control

Both runs fan out to subagents. The orchestrator discovers and dispatches; it never pulls
email bodies or full card descriptions into its own context. Subagents return a few fields,
not narratives.

Models are matched to the work: `opus` only for rep attribution, `sonnet` for ordinary page
builds and email logging, `haiku` for counting and diffing. Discovery uses
`THREAD_VIEW_MINIMAL`; body reads use `PLAIN_TEXT`. Never `FULL_CONTENT`.

## Two things that will break it

**Writing to a Trello card description.** `trelloWriteCard action:"update"` caps `desc` at
2048 characters and replaces it wholesale — longer cards lose their history silently. All
dialogue goes in the `📧 Email log` checklist (`add_item` takes 16KB and only appends).

**Calling `CreateSite` for a client that already has a page.** That mints a new URL and
strands everyone holding the old link. Once a `shareId` exists in the config, refreshes go
through `EditSite`.

## Changing how it behaves

Edit the runbook — that is the spec both runs follow. Common adjustments:

- **Reword a stage, or re-bucket a Trello list** → `stageMap` in `config/contractors.json`
- **Stop a label getting a page** → add it to `nonClientLabels`
- **Split a company by rep** → set its `pageMode` to `per-rep` and list the reps
- **Fix a rep's name or address** → the `reps` array for that client

## Not wired up

Emailing contractors their link. The weekly run refreshes pages and stops; Joseph shares the
links. Switching this on means adding a draft-generation phase to the weekly runbook —
drafts for review first, not direct sends.
