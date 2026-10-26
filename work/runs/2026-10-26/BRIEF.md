# Shared brief — weekly refresh 2026-10-26 (Monday)

Read FIRST, in full: runbooks/weekly-send-refresh.md, templates/status-page.html, and config/contractors.json
(use Grep/Read with offset to pull only your clients' entries + the top-level stageMap, excludeLists,
excludeCardMarkers, nonClientLabels). Repo: /home/user/contractorupdates. Board ARI:
ari:cloud:trello::board/workspace/65d7eb00496a914bf3ffb423/666e58adc67768660a580af4

Load tools via ToolSearch: select:mcp__Trello__trelloReadCard,mcp__Trello__trelloSearch,mcp__Trello__trelloReadList,mcp__Send__EditSite,mcp__Send__GetSite,mcp__Send__CreateSite

Hard rules (violating any = failed run):
- READ-ONLY on Trello. No Trello writes. NO email (no Gmail send/draft/reply/forward). Gmail is read-only.
- Existing shareId => mcp__Send__EditSite with fullHtml. NEVER CreateSite for a client that has a shareId.
- A card with label X goes only on X's page (a card carrying two client labels goes on BOTH). Never on an unrelated client's page.
- Apply excludeLists / excludeCardMarkers, stage mapping, name sanitising, leak rules exactly as the runbook says.
  No raw Trello list names, no OA/AD/DOA/ff/SOU/CN shorthand, no $ figures, no staff names, no emails/phones, no non-ASCII
  chars above U+007F (use &mdash; &middot; &rsquo; entities instead of raw characters).
- Show EVERY open file; never cap. Dedupe by card id. If trelloSearch cursor stalls (page adds zero new ids) or count is
  exactly 50/100, verify via trelloReadCard list_by_board (filter labels client-side). State truncation in the page footer.
- Keep only name, list name, url, lastActivityAt, loss address, claim #, latest dated [YYYY-MM-DD] note per card. Discard rest.
- Date for pages: "Monday, October 26, 2026".
- Before publishing, run the leak scan from the runbook over your HTML and fix hits.
- Write each page's HTML to work/pages/ (company-<slug>.html) with Write, publish by `cat`-ing... (EditSite fullHtml must equal the file).
- After EACH page publishes, append a line `<shareId>\t<file>\t<fileCount>\tok` to work/runs/2026-10-26/progress-<yourname>.tsv BEFORE starting the next.
- 0 open cards for a client: do NOT touch the page; report it as empty.
- Do not commit/push git. Do not edit config/contractors.json.
- Return ONLY compact JSON, no prose.
