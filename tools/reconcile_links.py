#!/usr/bin/env python3
"""
Produce one authoritative link per rep, and list every superseded link.

This run created pages under full names taken from the board export (Melvin
Pierce) while the earlier roster used initials derived from email addresses
(M. Pierce). Same person, two pages. Joseph chose to leave the old links live,
so the deliverable is a sheet that says plainly which link is current.

    python3 tools/reconcile_links.py
"""
import json, os, glob, sys

sys.path.insert(0, os.path.dirname(__file__))
from build_rep_pages import canon, titlecase  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), '..')
CFG = json.load(open(os.path.join(ROOT, 'config', 'contractors.json')))
MAN = json.load(open(os.path.join(ROOT, 'work', 'pages', 'manifest.json')))

# file -> shareId, as actually published (progress logs are the record of truth)
published = {}
for tsv in sorted(glob.glob(os.path.join(ROOT, 'work', 'publish', 'done*.tsv'))):
    for line in open(tsv):
        parts = line.rstrip('\n').split('\t')
        if len(parts) >= 2 and parts[1].strip():
            published[parts[0].strip()] = parts[1].strip()
for extra in glob.glob(os.path.join(ROOT, 'work', 'publish', 'results*.json')):
    for row in json.load(open(extra)):
        published.setdefault(row['file'], row['shareId'])

current, pending = [], []
for m in MAN:
    done = m['file'] in published
    sid = published.get(m['file']) or (m['shareId'] if m['action'] == 'edit' else None)
    # An 'edit' page already has a URL, but until this run republishes it the page
    # still shows the previous content. Say so rather than implying it is current.
    row = {'company': m['label'], 'rep': m['rep'], 'files': m['files'], 'shareId': sid,
           'url': f"https://www.send.co/a/{sid}" if sid else None,
           'stale': bool(sid) and not done}
    (current if sid else pending).append(row)

live_ids = {r['shareId'] for r in current if r['shareId']}
superseded = []
for c in CFG['contractors']:
    if c.get('pageMode') != 'per-rep':
        continue
    for rp in c.get('reps', []):
        sid = rp.get('shareId')
        if sid and sid not in live_ids:
            match = next((r for r in current
                          if r['company'] == c['label'] and canon(r['rep']) == canon(rp['name'])), None)
            superseded.append({'company': c['label'], 'oldName': rp['name'], 'oldShareId': sid,
                               'replacedBy': match['url'] if match else 'company unassigned page'})

current.sort(key=lambda r: (r['company'], -r['files'], r['rep']))
out = ["# Contractor status links — current as of this run", "",
       f"{len(current)} live rep pages. Send each rep ONLY the link on their row.", ""]
for comp in sorted({r['company'] for r in current}):
    out += [f"## {comp}", "", "| Rep | Files | Link |", "|---|---|---|"]
    out += [f"| {r['rep']} | {r['files']} | {r['url']}"
            f"{' *(refresh pending)*' if r['stale'] else ''} |"
            for r in current if r['company'] == comp]
    out.append("")
if pending:
    out += ["## Not yet published", ""] + [f"- {r['rep']} ({r['company']}, {r['files']} files)" for r in pending] + [""]
if superseded:
    out += ["## Superseded links — do NOT send these", "",
            "Left live by choice. Each shows an outdated file list.", "",
            "| Company | Old page | Old link | Current page |", "|---|---|---|---|"]
    out += [f"| {s['company']} | {s['oldName']} | https://www.send.co/a/{s['oldShareId']} | {s['replacedBy']} |"
            for s in superseded]

path = os.path.join(ROOT, 'work', 'LINKS.md')
open(path, 'w').write("\n".join(out) + "\n")
fresh = sum(1 for r in current if not r['stale'])
print(f"live+current: {fresh}   awaiting refresh: {len(current)-fresh}   "
      f"not yet created: {len(pending)}   superseded: {len(superseded)}")
print(f"written: work/LINKS.md")
