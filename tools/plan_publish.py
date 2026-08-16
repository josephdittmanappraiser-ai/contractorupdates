#!/usr/bin/env python3
"""
Split the 103 pages into publish batches a subagent can work through.

Publishing is the expensive half of the run: every byte of every page passes through a
model message. So the work is divided by BYTES, not by page count -- eight batches of
"thirteen pages each" means one agent carrying 300KB while another carries 40KB, and the
run finishes when the unlucky one does.

Pages past the single-call ceiling get chunk directories instead, and are listed
separately: they need the sentinel walk in tools/split_page.py, one agent each.

    python3 tools/plan_publish.py [batches]
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(__file__))
import split_page  # noqa: E402
from build_rep_pages import MAX_PAGE_BYTES  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), '..')
SINGLE_CALL_BYTES = 90_000


def main(nbatches=8, only=None, skip=None):
    man = json.load(open(os.path.join(ROOT, 'work', 'pages', 'manifest.json')))
    only, skip = set(only or []), set(skip or [])
    small, big = [], []
    for m in man:
        path = os.path.join(ROOT, m['file'])
        if not os.path.exists(path) or not m.get('shareId'):
            continue
        if (only and m['file'] not in only) or m['file'] in skip:
            continue
        size = os.path.getsize(path)
        (big if size > SINGLE_CALL_BYTES else small).append(dict(m, bytes=size))

    # Longest-first into whichever batch is currently lightest.
    small.sort(key=lambda m: -m['bytes'])
    batches = [[] for _ in range(nbatches)]
    load = [0] * nbatches
    for m in small:
        i = load.index(min(load))
        batches[i].append(m)
        load[i] += m['bytes']

    out = os.path.join(ROOT, 'work', 'publish', 'batches')
    os.makedirs(out, exist_ok=True)
    for old in os.listdir(out):
        os.remove(os.path.join(out, old))
    for i, b in enumerate(batches, 1):
        if not b:
            continue
        with open(os.path.join(out, f'batch{i}.tsv'), 'w') as fh:
            for m in b:
                fh.write(f"{m['shareId']}\t{m['file']}\n")
        print(f"batch{i}: {len(b):2d} pages, {load[i-1]/1000:6.0f}KB")

    for m in big:
        plan = split_page.main(os.path.join(ROOT, m['file']))
        print(f"  CHUNKED  {m['shareId']}  {m['file']}  {plan['calls']} calls")

    json.dump({'batches': nbatches, 'chunked': [{'shareId': m['shareId'], 'file': m['file']}
                                                for m in big]},
              open(os.path.join(out, 'plan.json'), 'w'), indent=1)
    print(f"\n{len(small)} pages in {nbatches} batches, {len(big)} chunked")


if __name__ == '__main__':
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 8)
