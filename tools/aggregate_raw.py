#!/usr/bin/env python3
"""
Combine every work/weekly-*/raw/*.json data-pull batch into one CSV that
tools/build_rep_pages.py can consume.

    python3 tools/aggregate_raw.py work/weekly-2026-09-21/raw work/weekly-2026-09-21/board-export.csv
"""
import csv, json, os, sys, glob

FIELDS = ['Card ID', 'Card Name', 'Card Description', 'List Name', 'Labels',
          'Last Activity Date', 'Claim #', 'Sales Person']


def main(raw_dir, out_csv):
    rows = []
    seen = set()
    dupes = 0
    files = sorted(glob.glob(os.path.join(raw_dir, '*.json')))
    for fp in files:
        try:
            data = json.load(open(fp, encoding='utf-8'))
        except Exception as e:
            print(f"SKIP {fp}: {e}", file=sys.stderr)
            continue
        if not isinstance(data, list):
            print(f"SKIP {fp}: not a JSON array", file=sys.stderr)
            continue
        for r in data:
            cid = (r.get('cardId') or '').strip()
            lab = (r.get('labels') or '').strip()
            key = (cid, lab)
            if not cid:
                continue
            if key in seen:
                dupes += 1
                continue
            seen.add(key)
            rows.append({
                'Card ID': cid,
                'Card Name': r.get('cardName', ''),
                'Card Description': r.get('cardDescription', ''),
                'List Name': r.get('listName', ''),
                'Labels': lab,
                'Last Activity Date': r.get('lastActivityDate', ''),
                'Claim #': r.get('claimNumber', ''),
                'Sales Person': r.get('salesPerson', ''),
            })

    with open(out_csv, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)

    by_label = {}
    for r in rows:
        by_label[r['Labels']] = by_label.get(r['Labels'], 0) + 1

    print(f"files read: {len(files)}")
    print(f"rows written: {len(rows)}  (duplicate cardId+label pairs skipped: {dupes})")
    print(f"distinct labels: {len(by_label)}")
    for lab, n in sorted(by_label.items(), key=lambda kv: -kv[1]):
        print(f"  {lab}: {n}")


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
