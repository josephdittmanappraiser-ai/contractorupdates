#!/usr/bin/env python3
"""
One-off patch for the Legacy Roofing GC page: add the files that appeared on the
board since the last refresh, and append a roster section grouping every file by
the Legacy rep who brought it in.

The deal-update sections above are left byte-for-byte alone; this only inserts new
`.file` blocks into the stages they belong to, corrects the counts those insertions
change, and appends the roster.

    python3 tools/patch_legacy_page.py <attributed.json> [page]

`attributed.json` is the output of the rep-attribution pass: one object per open
Trello card carrying the Legacy Roofing label, with `insured`, `stage`, `order` and
`rep`. Roster grouping is driven entirely by that file so the page cannot disagree
with the attribution that produced it.
"""
import json, re, sys, os, collections, datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_rep_pages as B
from build_rep_pages import E, track_html   # same escaping and step strip as the builder

PAGE = 'work/pages/company-legacy-roofing-gc.html'

# ---------------------------------------------------------------- the new files
#
# Written from the Trello card plus the email thread behind it. Every one of these
# passes the same rules as the rest of the page: no dollar figures, no negotiating
# posture, no homeowner email addresses or phone numbers, no staff names, no raw
# Trello list names, no internal shorthand.
NEW = [
 dict(stage='Inspection scheduling', order=5, name='Albert Saucedo JR Antonia Leon-Saucedo',
      when='2026-08-27', meta='7024 Donato Pl Round Rock, TX 78665 &middot; Claim 202604180027',
      what='Hail claim covering the roof, gutters, garage door and fence staining. Legacy '
           'Roofing sent the claim details and the inspection paperwork on Aug 27, and the '
           'file is now in the queue for an appraisal inspection date.',
      events=[('2026-08-27', 'Legacy Roofing referred the claim with the loss address, claim '
                             'number and a description of the hail damage.')]),

 dict(stage='Appraisal demanded / waiting on carrier', order=4, name='RITIKA PAWAR AKSHAY DESAI',
      when='2026-08-31',
      what='Damage to the roof, gutters, garage doors and fence staining. The appraisal demand '
           'letter has gone out and we are waiting for the carrier to name their appraiser.',
      events=[('2026-08-31', 'Legacy Roofing referred the claim with a description of the '
                             'damage and the homeowner’s details.'),
              ('2026-08-31', 'Appraisal demand letter sent.')]),

 dict(stage='Appraisal demanded / waiting on carrier', order=4, name='Nimesh Patel',
      when='2026-08-31',
      what='Damage to the roof, gutters and garage door, plus a small section of interior '
           'repair in the two-story hallway. The appraisal demand letter has gone out and we '
           'are waiting for the carrier to name their appraiser.',
      events=[('2026-08-31', 'Legacy Roofing referred the claim with a description of the '
                             'damage and the homeowner’s details.'),
              ('2026-08-31', 'Appraisal demand letter sent.')]),

 dict(stage='Appraisal demanded / waiting on carrier', order=4, name='ANDREA NARVAEZ',
      when='2026-08-27', meta='Claim 53-0K6H-930',
      what='The roof is a total loss, with further damage to gutters, downspouts, fence and '
           'window screens and seals. The homeowner has signed, and the full appraisal demand '
           'package went to State Farm on Aug 26.',
      events=[('2026-08-17', 'Legacy Roofing referred the claim and asked to take it through '
                             'appraisal.'),
              ('2026-08-24', 'Legacy Roofing confirmed the homeowner had signed and sent the '
                             'inspection photos.'),
              ('2026-08-25', 'Our estimate was sent to Legacy Roofing for review and approved '
                             'the same day.'),
              ('2026-08-26', 'The appraisal demand and supporting documents were sent to State '
                             'Farm, with Legacy Roofing and the homeowner copied.')]),

 dict(stage='Estimate being prepared', order=2, name='JESUS VIDAL', when='2026-08-28',
      what='Hail damage to the roof, gutters and fence. Legacy Roofing sent the inspection '
           'report on Aug 28, the appraisal demand letter has gone to the homeowner, and our '
           'estimate is being prepared.',
      events=[('2026-08-27', 'Legacy Roofing asked us to start the file as soon as possible '
                             'and sent the paperwork.'),
              ('2026-08-28', 'Legacy Roofing sent the inspection report and the damage '
                             'description.'),
              ('2026-08-28', 'Appraisal demand letter sent to the homeowner.')]),

 dict(stage='Estimate being prepared', order=2, name='MANJEET CHHABRA ARMIT KHANUJA',
      when='2026-08-26', meta='15521 Bended Knee Dr Austin, TX 78717',
      what='The carrier denied the claim, so Legacy Roofing referred it for appraisal on '
           'Aug 26. The appraisal demand letter went out the same day and our estimate is '
           'being prepared.',
      events=[('2026-08-26', 'Legacy Roofing referred the denied claim with the loss address, '
                             'and confirmed it should go through appraisal.'),
              ('2026-08-26', 'Appraisal demand letter sent to the homeowner.')]),

 dict(stage='Estimate being prepared', order=2, name='AJAYA KHADKA', when='2026-08-24',
      what='Hail hits across the front and back slopes, both sides and the gutters. The '
           'appraisal demand letter has gone to the homeowner and our estimate is being '
           'prepared.',
      ask='We could not open the damage photos that were sent — please resend them so the '
          'estimate can be finished.',
      events=[('2026-08-21', 'Legacy Roofing referred the claim with the roof report and a '
                             'description of the hail damage.'),
              ('2026-08-24', 'Appraisal demand letter sent to the homeowner; we asked Legacy '
                             'Roofing to resend the photos, which would not open.')]),

 dict(stage='New / intake', order=1, name='Aseem Sharma', when='2026-08-21',
      what='Referred to us with damage to the roof and gutters. We are confirming the '
           'homeowner’s details before the appraisal demand letter can go out.',
      ask='We still need the homeowner’s email address and phone number before the demand '
          'letter can be sent.',
      events=[('2026-08-21', 'Legacy Roofing referred the claim, noting damage to the roof '
                             'and gutters.')]),

 dict(stage='New / intake', order=1, name='DARION TERRY', when='2026-08-19',
      meta='3904 Bronco Bend Loop Austin, TX 78744',
      what='Referred to us on Aug 18 and confirmed for appraisal. We are waiting on the rest '
           'of the file before the appraisal demand letter can go out.',
      ask='Still needed from Legacy Roofing: the carrier estimate, the EagleView report or '
          'roof sketch, a brief description of the damage, and the homeowner’s email '
          'address and phone number.',
      events=[('2026-08-18', 'Legacy Roofing referred the claim and sent the first paperwork.'),
              ('2026-08-19', 'Legacy Roofing sent more documents; we confirmed receipt and '
                             'asked for the remaining requirements.')]),
]


def file_html(f):
    """One `.file` block, in the same shape the page builder emits."""
    cls = 'file needs-you' if f.get('ask') else 'file'
    out = [f'<div class="{cls}"><div class="file-top"><h3>{E(f["name"])}</h3>'
           f'<span class="when">last activity {E(f["when"])}</span></div>']
    out.append(track_html(f['order']))
    if f.get('meta'):
        out.append(f'<p class="meta">{f["meta"]}</p>')   # already-entitied &middot;
    out.append(f'<p class="what">{E(f["what"])}</p>')
    if f.get('ask'):
        out.append(f'<p class="ask">{E(f["ask"])}</p>')
    ev = sorted(f['events'], key=lambda e: e[0])
    rows = "".join(f'<li><span class="d">{E(d)}</span>{E(t)}</li>'
                   for d, t in reversed(ev[-3:]))
    out.append('<div class="latest"><p class="latest-h">Most recent activity</p>'
               f'<ol class="events">{rows}</ol></div>')
    allrows = "".join(f'<li><span class="d">{E(d)}</span>{E(t)}</li>' for d, t in ev)
    out.append(f'<details class="chain"><summary>Full history from the start '
               f'({len(ev)} event{"s" if len(ev) != 1 else ""})</summary>'
               f'<ol class="events">{allrows}</ol></details>')
    return "".join(out) + '</div>\n'


def insert_into_stage(doc, stage_h2, blocks):
    """Drop new files into a stage, newest first, and correct that stage's count."""
    head = f'<h2>{stage_h2}</h2>'
    i = doc.index(head)
    sec = doc.rindex('<section class="stage', 0, i)
    end = doc.index('</section>', i)
    body = doc[sec:end]

    m = re.search(r'<span class="count">(\d+) files?</span>', body)
    n = int(m.group(1)) + len(blocks)
    body = body[:m.start()] + f'<span class="count">{n} file{"s" if n != 1 else ""}</span>' \
         + body[m.end():]

    # entries sit newest-activity-first; splice each one in front of the first
    # existing entry it is newer than.
    # The class boundary matters: `<div class="file-top">` also starts with `file`,
    # so a looser lookahead splits every card in two and the new block lands inside
    # one instead of between them.
    entries = re.split(r'(?=<div class="file[ "])', body)
    headmatter, rows = entries[0], entries[1:]
    for f in sorted(blocks, key=lambda x: x['when']):
        at = len(rows)
        for k, r in enumerate(rows):
            w = re.search(r'last activity (\d{4}-\d{2}-\d{2})', r)
            if w and w.group(1) < f['when']:
                at = k
                break
        rows.insert(at, file_html(f))
    return doc[:sec] + headmatter + "".join(rows) + doc[end:]


def page_roster(doc, records):
    """Feed the page's own entries to the builder's roster renderer.

    Driven off the page's `<h3>` headings rather than off the Trello pull, so the roster
    and the sections above can never show a different set of people, and rendered by
    `build_rep_pages.roster_html` so an off-cycle patch and a Monday rebuild produce the
    same markup.
    """
    # A card name and the page's own heading are not always spelled the same -- the
    # card carries operator suffixes the page strips ("-estimate created", a market
    # tag) and sometimes names a second insured. Match on the exact string first, then
    # on shared name tokens, so those variants land on the right rep instead of in the
    # unmatched bucket.
    NOISE = {'and', 'the', 'dfw', 'houston', 'austin', 'estimate', 'created', 'sent',
             'email', 'phone', 'description', 'claim'}

    def toks(x):
        x = re.sub(r'&#x27;|&amp;|&middot;', ' ', x.lower())
        return {t for t in re.split(r'[^a-z]+', x) if len(t) > 2 and t not in NOISE}

    exact, fuzzy = {}, []
    for r in records:
        if r.get('rep'):
            exact[re.sub(r'[^a-z]', '', r['insured'].lower())] = r['rep']
            fuzzy.append((toks(r['insured']), r['rep']))

    def rep_for(name):
        hit = exact.get(re.sub(r'[^a-z]', '', name.lower()))
        if hit:
            return hit
        nt = toks(name)
        best = [rep for ts, rep in fuzzy
                if nt & ts and (nt <= ts or ts <= nt or len(nt & ts) >= 2)]
        return best[0] if len(set(best)) == 1 else B.UNMATCHED

    body = doc.split('<section class="reps">')[0]
    # Which files are closed comes from the page itself: everything inside a
    # `stage settled` section, which is exactly what the green sections above show.
    closed = set()
    for sec in re.findall(r'<section class="stage settled">.*?</section>', body, re.S):
        closed.update(re.findall(r'<h3>(.*?)</h3>', sec))

    entries = [{'insured': n, 'rep': rep_for(n), 'closed': n in closed}
               for n in dict.fromkeys(re.findall(r'<h3>(.*?)</h3>', body))]
    return B.roster_html(entries) + '\n'


# The roster styles now live in templates/status-page.html, which is where the builder
# reads its CSS from, so a rebuilt page carries them already. Lift that exact block out
# to graft onto a page built before the template had it -- copying it here instead would
# give the two paths two stylesheets to drift apart.
CSS = B.CSS[B.CSS.index('  /* Roster:'):B.CSS.index('  .foot{border-top')]


# Files that have moved to Joseph's Assignments since the page was built. The board is
# the source of truth for stage, and this list is the board: a card sitting there is one
# Joseph is personally deciding, and it used to disappear from the page entirely because
# the list was excluded. `config/contractors.json` now maps it to a real stage, so a
# rebuild picks these up on its own -- this only carries them on an already-built page.
MOVED_TO_DECISION = ['KISHORE BULUSU ANUPAMA MANTHA']


def move_to_decision(doc, names):
    """Lift a file out of whatever stage it was in and into the decision stage.

    The file's history stays exactly as it was -- it is a real record of what happened.
    What gets replaced is the status line and the step strip, because the file is no
    longer where the old status said it was, and the ask is dropped outright: nothing is
    wanted from the contractor while the decision is ours.
    """
    st = next(s for s in B.CFG['stageMap'] if s['stage'] == B.DECIDING)
    moved = []
    for name in names:
        i = doc.index(f'<h3>{name}</h3>')
        # `<div class="file-top">` shares the prefix, so a plain rindex for
        # '<div class="file' lands on the card's inner header and slices the card in
        # half. Match the class boundary.
        start = [m.start() for m in re.finditer(r'<div class="file[ "]', doc[:i])][-1]
        end = doc.index('</div>\n', doc.index('</details>', i)) + len('</div>\n')
        block = doc[start:end]

        block = re.sub(r'<div class="file[^"]*"><div class="file-top">',
                       '<div class="file"><div class="file-top">', block, count=1)
        block = re.sub(r'<ol class="track">.*?</ol>', B.track_html(st['order']), block, count=1)
        block = re.sub(r'<p class="what">.*?</p>',
                       f'<p class="what">{E(st["blurb"])}</p>', block, count=1, flags=re.S)
        block = re.sub(r'<p class="ask">.*?</p>', '', block, count=1, flags=re.S)

        # drop it from the old stage, and correct that stage's count
        doc = doc[:start] + doc[end:]
        h2 = doc.rindex('<h2>', 0, start)
        m = re.compile(r'<span class="count">(\d+) files?</span>').search(doc, h2)
        n = int(m.group(1)) - 1
        doc = doc[:m.start()] + f'<span class="count">{n} file{"s" if n != 1 else ""}</span>' \
            + doc[m.end():]
        moved.append(block)

    if not moved:
        return doc
    # A new stage section, placed by its order among the ones already on the page.
    sec = (f'<section class="stage"><div class="stage-head"><h2>{E(B.DECIDING)}</h2>'
           f'<span class="count">{len(moved)} file{"s" if len(moved) != 1 else ""}</span></div>'
           f'<p class="stage-blurb">{E(st["blurb"])}</p>\n' + "".join(moved) + '</section>\n')
    for other in sorted((s for s in B.CFG['stageMap'] if s['order'] < st['order']),
                        key=lambda s: -s['order']):
        head = f'<h2>{E(other["stage"])}</h2>'
        if head in doc:
            return doc[:doc.rindex('<section class="stage', 0, doc.index(head))] + sec \
                 + doc[doc.rindex('<section class="stage', 0, doc.index(head)):]
    return doc.replace('<hr class="settled-divider">', sec + '<hr class="settled-divider">', 1)


def main(attributed, page=PAGE):
    doc = open(page).read()
    before = len(doc.encode())

    for stage, blocks in collections.OrderedDict(
            (s, [f for f in NEW if f['stage'] == s])
            for s in dict.fromkeys(f['stage'] for f in NEW)).items():
        doc = insert_into_stage(doc, E(stage), blocks)

    doc = move_to_decision(doc, MOVED_TO_DECISION)

    # counts, recomputed from what the document now actually holds
    total = doc.count('<h3>')
    settled = sum(s.count('<h3>') for s in re.findall(
        r'<section class="stage settled">.*?</section>', doc, re.S))
    referred = sum(s.count('<h3>') for s in re.findall(
        r'<section class="stage"><div class="stage-head"><h2>Referred out.*?</section>', doc, re.S))
    needs = doc.count('class="file needs-you"')
    tiles = (f'<section class="tiles">\n'
             f'<div class="tile"><span class="n">{total}</span><span class="l">Open files</span></div>\n'
             f'<div class="tile"><span class="n">{total - settled - referred}</span>'
             f'<span class="l">In appraisal</span></div>\n'
             f'<div class="tile alert"><span class="n">{needs}</span><span class="l">Need you</span></div>\n'
             f'<div class="tile good"><span class="n">{settled}</span><span class="l">Settled</span></div>\n'
             f'</section>')
    doc = re.sub(r'<section class="tiles">.*?</section>', lambda _: tiles, doc, count=1, flags=re.S)

    updated = datetime.date.today().strftime('%A, %B %-d, %Y')
    doc = re.sub(r'(<p class="sub">Where every file you sent us currently stands\. Updated )[^<]*',
                 lambda m: m.group(1) + updated + '.', doc, count=1)

    records = json.load(open(attributed))
    doc = doc.replace('<section class="foot">', page_roster(doc, records) + '<section class="foot">')
    doc = doc.replace('  .foot{border-top', CSS + '  .foot{border-top')

    open(page, 'w').write(doc)
    nonascii = [c for c in doc if ord(c) > 127]
    print(f'{page}: {before} -> {len(doc.encode())} bytes')
    print(f'files {total} (settled {settled}, referred out {referred}, needs-you {needs})')
    print(f'roster reps: {len(set(r["rep"] or "unmatched" for r in records))}')
    print(f'non-ascii characters: {len(nonascii)}')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else PAGE)
