#!/usr/bin/env python3
"""
Catch chains of events that stopped short of the newest email.

The failure this exists for: an enrichment agent opened a 30-message thread, read the
first two thirds, and returned a confident nine-event timeline ending two months back --
with a status line saying the file had not moved since. It had. The contractor's own
words were what surfaced it, not the tooling.

Truncation lands on the recent end, which is the only end a contractor reads, and a
short timeline looks exactly like a quiet file. So compare every file's newest event
against the card's own last-activity date and make the gap visible before publishing.

A gap is a signal, not a verdict -- a card can be touched for a Trello move with no new
email. That is what `staleReason` is for. An unexplained gap over the threshold is a
file to re-read.

    python3 tools/check_timeline_freshness.py <board-export.csv> [days]

Exits non-zero when any file is unexplained-stale, so it can gate a publish.
"""
import csv, datetime, glob, json, os, sys

ROOT = os.path.join(os.path.dirname(__file__), '..')
DEFAULT_DAYS = 14


def load_enrichment():
    up = os.path.join(ROOT, 'work', 'updates')
    out = {}
    for f in sorted(glob.glob(os.path.join(up, 'out*.json'))) + \
             sorted(glob.glob(os.path.join(up, 'rerun', 'out*.json'))):
        try:
            d = json.load(open(f))
        except Exception:
            continue
        for r in (d.get('results') if isinstance(d, dict) else d) or []:
            if r.get('cardId'):
                out[r['cardId'].strip()] = r
    return out


def load_activity(csv_path):
    act = {}
    with open(csv_path, encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            cid = (r.get('Card ID') or r.get('id') or '').strip()
            la = (r.get('Last Activity Date') or r.get('Last Activity') or '').strip()
            if cid:
                act[cid[-24:]] = la[:10]
    return act


def main(csv_path, days=DEFAULT_DAYS):
    enrich, act = load_enrichment(), load_activity(csv_path)
    stale, explained, current, undated = [], [], 0, 0

    for cid, r in enrich.items():
        tl = r.get('timeline') or []
        if not tl:
            continue
        newest = max(str(e.get('date', ''))[:10] for e in tl)
        la = act.get(cid, '')
        try:
            behind = (datetime.date.fromisoformat(la) - datetime.date.fromisoformat(newest)).days
        except ValueError:
            undated += 1
            continue
        if behind <= days:
            current += 1
        elif r.get('staleReason'):
            explained.append({'cardId': cid, 'daysBehind': behind, 'reason': r['staleReason']})
        else:
            stale.append({'cardId': cid, 'newestEvent': newest, 'lastActivity': la,
                          'daysBehind': behind})

    stale.sort(key=lambda s: -s['daysBehind'])
    path = os.path.join(ROOT, 'work', 'updates', 'stale-timelines.json')
    json.dump(stale, open(path, 'w'), indent=1)

    print(f"timeline current (within {days}d of card activity): {current}")
    print(f"gap explained by the agent:                         {len(explained)}")
    print(f"no usable dates:                                    {undated}")
    print(f"UNEXPLAINED STALE:                                  {len(stale)}")
    for s in stale[:10]:
        print(f"   {s['daysBehind']:4d}d behind   last event {s['newestEvent']}   {s['cardId']}")
    if len(stale) > 10:
        print(f"   ... and {len(stale)-10} more")
    print(f"written: work/updates/stale-timelines.json")
    return 1 if stale else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_DAYS))
