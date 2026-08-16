#!/usr/bin/env python3
"""
Split an oversized status page into EditSite-sized pieces.

Send's EditSite takes the document as a tool parameter, so the whole page has to
pass through one model message. Two clients (No Stress Claims at 383 files,
Legacy Roofing at 160) are far past what fits, and the earlier workaround --
trimming each file's chain of events until the page shrank -- threw away the
history the pages exist to show.

So publish in pieces instead. A skeleton goes up first with a `<!--MORE-->`
sentinel where the file list belongs; each chunk then replaces the sentinel with
itself plus the sentinel again, so the marker walks down the document. The last
call deletes the sentinel. Every intermediate state is a loadable page, and the
final bytes equal the built file exactly -- verify_chunks() proves that before
anything is published.

    python3 tools/split_page.py work/pages/company-no-stress-claims.html [chunk_bytes]
"""
import json, os, sys

SENTINEL = '<!--MORE-->'
DEFAULT_CHUNK = 18_000

# A chunk may end here without leaving a half-written element on screen.
BREAK_PREFIXES = ('<section', '<hr class="settled-divider">', '<div class="file')


def split(path, chunk_bytes=DEFAULT_CHUNK):
    src = open(path).read()
    lines = src.split('\n')

    # Head, banner and the four count tiles go up first: a reader who lands
    # mid-publish sees a real page, not a fragment.
    start = next(i for i, l in enumerate(lines) if l.startswith('</section>')
                 or l.rstrip().endswith('</section>') and 'tiles' in lines[i - 1] + l)
    start = next(i for i, l in enumerate(lines) if 'Settled</span></div>' in l) + 1
    end = next(i for i, l in enumerate(lines) if l.startswith('<section class="foot"'))

    prefix, middle, suffix = lines[:start], lines[start:end], lines[end:]

    chunks, cur, size = [], [], 0
    for line in middle:
        breakable = any(line.startswith(p) for p in BREAK_PREFIXES)
        if cur and breakable and size + len(line) > chunk_bytes:
            chunks.append('\n'.join(cur))
            cur, size = [], 0
        cur.append(line)
        size += len(line.encode()) + 1
    if cur:
        chunks.append('\n'.join(cur))

    # Each chunk carries a marker as its first line. The publish agent retypes chunk
    # bodies by hand, and a chunk that silently failed to land would otherwise look
    # exactly like one that did. The final call deletes all markers in a single
    # atomic edit batch: a missing marker fails the batch instead of shipping a
    # page with a hole in it. Markers are gone from the finished document.
    chunks = [f'<!--C:{i:02d}-->\n{c}' for i, c in enumerate(chunks, 1)]

    skeleton = '\n'.join(prefix) + '\n' + SENTINEL + '\n' + '\n'.join(suffix)
    return src, skeleton, chunks


def verify(src, skeleton, chunks):
    """Replay every edit in memory, markers included. Publishing a page that does not
    reassemble is worse than not publishing it, so this runs before any chunk is
    written to disk."""
    doc = skeleton
    for c in chunks:
        assert doc.count(SENTINEL) == 1, 'sentinel must be unique at every step'
        doc = doc.replace(SENTINEL, c + '\n' + SENTINEL)
    for i in range(1, len(chunks) + 1):
        assert doc.count(f'<!--C:{i:02d}-->\n') == 1, f'marker {i} must be unique'
        doc = doc.replace(f'<!--C:{i:02d}-->\n', '')
    doc = doc.replace('\n' + SENTINEL + '\n', '\n')
    return doc == src


def main(path, chunk_bytes=DEFAULT_CHUNK):
    src, skeleton, chunks = split(path, chunk_bytes)
    if not verify(src, skeleton, chunks):
        sys.exit(f'ABORT: chunks of {path} do not reassemble to the source page')

    name = os.path.splitext(os.path.basename(path))[0]
    out = os.path.join(os.path.dirname(path), '..', 'publish', 'chunks', name)
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, '00-skeleton.html'), 'w').write(skeleton)
    for i, c in enumerate(chunks, 1):
        open(os.path.join(out, f'{i:02d}.html'), 'w').write(c)

    plan = {'page': path, 'sentinel': SENTINEL, 'dir': os.path.normpath(out),
            'skeleton': '00-skeleton.html', 'chunks': [f'{i:02d}.html' for i in range(1, len(chunks) + 1)],
            'markers': [f'<!--C:{i:02d}-->' for i in range(1, len(chunks) + 1)],
            'sourceBytes': len(src.encode()),
            'calls': len(chunks) + 2}
    json.dump(plan, open(os.path.join(out, 'plan.json'), 'w'), indent=1)
    print(f"{name}: {len(src.encode())} bytes -> skeleton + {len(chunks)} chunks "
          f"({plan['calls']} EditSite calls); reassembly verified")
    return plan


if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_CHUNK)
