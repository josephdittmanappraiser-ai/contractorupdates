# Publish task

Republish a batch of contractor status pages to Send. Each page fits in one call.

Load the tool first:

```
ToolSearch query "select:mcp__Send__EditSite"
```

Your batch file is named in your prompt. It is TSV, one page per line:

```
<shareId>\t<path to the html file>
```

For each line, in order:

1. `cat <path>` in Bash. Use `cat`, **not** the Read tool — Read prefixes every line with a
   line number, and those line numbers would be published.
2. Call `EditSite` with `shareIdOrUrl` set to that shareId and `fullHtml` set to exactly those
   bytes.
3. Append `<shareId>\t<path>\tok` to your progress log (named in your prompt) as you go, so a
   restart resumes instead of repeating.

## Rules

- Copy the file contents **verbatim**. Do not reformat, re-indent, re-wrap, pretty-print,
  minify, or "fix" the HTML. These pages carry real insured names, addresses and claim numbers,
  and a page is a legal-adjacent record of what a contractor was told.
- **Never call `CreateSite`.** That mints a new URL and strands every contractor holding the
  old link. The share URL must never change.
- One page per `EditSite` call.
- If a call fails, report the exact error and retry that page once. Do not skip ahead silently.
- Do not commit to git. Do not send email. Do not touch a page that is not in your batch.

## Verifying

After each publish, `EditSite` reports a byte delta. Treat a mismatch as a prompt to check, not
as proof of loss — the tool's own counter has been seen to disagree with the file over
multi-byte characters. To settle it, call `GetSite` and compare against the file on disk.

## Return

```json
{"batch":0,"published":["shareId",...],"failed":[{"shareId":"","error":""}],"notes":""}
```
