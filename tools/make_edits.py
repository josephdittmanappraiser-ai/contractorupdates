#!/usr/bin/env python3
"""
Turn "old page -> new page" into a list of EditSite string replacements.

A page past the ~90KB ceiling cannot be republished with `fullHtml`, and the
chunked path in the weekly runbook exists for a page that was regenerated from
scratch. When the change is additive -- a handful of new files spliced into their
stages, a section appended -- the whole diff is a few KB, and EditSite's own
`edits` array carries it in one call instead of fourteen.

Every replacement is checked to match exactly once in the live document, and the
edits are replayed locally to prove they reproduce the new page byte for byte
before anything is published.

    python3 tools/make_edits.py <before.html> <after.html> <edits.json>
"""
import difflib, json, sys

MAX_PAD = 6000

# Two passes, because neither alone is usable here. Diffing runs over LINES -- these
# pages are ~320 dense lines, one per file block, and a character-level
# SequenceMatcher over 200KB does not finish. But a line of context is a whole 4KB
# file block, so the anchors are then shrunk back to the smallest run of CHARACTERS
# that still matches exactly once. Every byte in an anchor is a byte that has to be
# retyped into a tool call, and retyping is where a publish goes wrong.


def offsets(lines):
    out, n = [], 0
    for l in lines:
        out.append(n)
        n += len(l)
    out.append(n)
    return out


def shrink(before, i1, i2, insert, lo_cap, hi_cap):
    """Smallest window around [i1,i2) that appears exactly once in `before`.

    Capped so an anchor never reaches into a neighbouring change: edits apply in
    sequence, so quoting text another edit is about to rewrite makes this one
    unmatchable by the time it runs. Returns None when uniqueness is unreachable
    inside the cap, and the caller merges the two changes into a single edit.
    """
    pad = 8
    while pad <= MAX_PAD:
        lo, hi = max(lo_cap, i1 - pad), min(hi_cap, i2 + pad)
        old = before[lo:hi]
        if before.count(old) == 1:
            return old, before[lo:i1] + insert + before[i2:hi]
        if lo == lo_cap and hi == hi_cap:
            return None
        pad *= 2
    return None


def regions(before_lines, after_lines):
    """Every change as (start, end, replacement) in `before` coordinates."""
    before, after = "".join(before_lines), "".join(after_lines)
    bo, ao = offsets(before_lines), offsets(after_lines)
    out = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(
            None, before_lines, after_lines, autojunk=False).get_opcodes():
        if tag == 'equal':
            continue
        # A line-level region bundles unrelated changes -- a stage's count and the
        # file spliced into it further down are one opcode, so the anchor drags in
        # every block between them. The regions are small enough to diff by
        # character, which separates them into their own minimal edits.
        ba, aa = bo[i1], ao[j1]
        bseg, aseg = before[ba:bo[i2]], after[aa:ao[j2]]
        for t, a1, a2, b1, b2 in difflib.SequenceMatcher(
                None, bseg, aseg, autojunk=False).get_opcodes():
            if t != 'equal':
                out.append([ba + a1, ba + a2, aseg[b1:b2]])
    return before, out


def build(before_lines, after_lines):
    """Edits in the order EditSite will apply them, each anchored in the document
    as it stands at that point.

    Uniqueness has to be judged against the evolving document, not the original.
    Bumping one stage's count from 5 to 6 makes a later `"count">6 files</` anchor --
    unique when the diff was taken -- match in two places by the time it runs.
    """
    before, regs = regions(before_lines, after_lines)
    while True:
        doc, shift, edits, merged = before, 0, [], False
        for k, (i1, i2, ins) in enumerate(regs):
            lo_cap = (regs[k - 1][1] + shift) if k else 0
            hi_cap = (regs[k + 1][0] + shift) if k + 1 < len(regs) else len(doc)
            got = shrink(doc, i1 + shift, i2 + shift, ins, lo_cap, hi_cap)
            if got is None:                       # anchor needs its neighbour's text
                nxt = regs[k + 1]
                regs[k:k + 2] = [[i1, nxt[1], ins + before[i2:nxt[0]] + nxt[2]]]
                merged = True
                break
            old, new = got
            edits.append({'old_string': old, 'new_string': new})
            doc = doc.replace(old, new, 1)
            shift += len(new) - len(old)
        if not merged:
            return edits


def replay(before, edits):
    doc = before
    for e in edits:
        if doc.count(e['old_string']) != 1:
            raise SystemExit('edit is not uniquely applicable during replay')
        doc = doc.replace(e['old_string'], e['new_string'], 1)
    return doc


def main(bpath, apath, out):
    before, after = open(bpath).read(), open(apath).read()
    edits = build(before.splitlines(keepends=True), after.splitlines(keepends=True))
    got = replay(before, edits)
    if got != after:
        raise SystemExit('replay does not reproduce the new page -- refusing to emit edits')
    json.dump(edits, open(out, 'w'), indent=1)
    payload = sum(len(e['old_string']) + len(e['new_string']) for e in edits)
    print(f'{len(edits)} edits, {payload} bytes of payload '
          f'(page {len(before)} -> {len(after)})')
    for i, e in enumerate(edits, 1):
        print(f'  {i:2d}. -{len(e["old_string"]):6d} +{len(e["new_string"]):6d}  '
              f'{e["old_string"][:70]!r}')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
