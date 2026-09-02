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


UNMATCHED = 'Not yet matched to a rep'


def roster_html(doc, records):
    """Every insured on this page, grouped by the Legacy rep who brought them in.

    Driven off the page's own `<h3>` entries rather than off the Trello pull, so the
    roster and the sections above can never show a different set of people. A name
    the attribution pass could not place lands in its own group rather than being
    guessed at or quietly dropped.

    Deliberately just the insured's name: a file's status is the business of the
    sections above, and repeating it here would give two places to disagree.
    """
    # A card name and the page's own heading are not always spelled the same -- the
    # card carries operator suffixes the page strips ("-estimate created", a market
    # tag) and sometimes names a second insured. Match on the exact string first, then
    # on shared name tokens, so those variants land on the right rep instead of in the
    # unmatched bucket.
    NOISE = {'and', 'the', 'dfw', 'houston', 'austin', 'estimate', 'created', 'sent',
             'email', 'phone', 'description', 'claim'}

    def toks(s):
        s = re.sub(r'&#x27;|&amp;|&middot;', ' ', s.lower())
        return {t for t in re.split(r'[^a-z]+', s) if len(t) > 2 and t not in NOISE}

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
        return best[0] if len(set(best)) == 1 else UNMATCHED

    # page names, in page order, excluding any roster this is replacing
    body = doc.split('<section class="reps">')[0]
    names = list(dict.fromkeys(re.findall(r'<h3>(.*?)</h3>', body)))

    by = collections.defaultdict(list)
    for n in names:
        by[rep_for(n)].append(n)
    for k in by:
        # One line per insured. A rep can hold two cards for the same homeowner --
        # a settled file and a fresh demand -- and the board spells them differently
        # ("Momtazul Karim", "MOMTAZUL KARIM"), which reads as a bug rather than as
        # two deals. Keep the first spelling the page itself uses.
        seen, uniq = set(), []
        for n in by[k]:
            if n.lower() not in seen:
                seen.add(n.lower())
                uniq.append(n)
        by[k] = sorted(uniq, key=lambda s: s.lower())
    reps = sorted(by, key=lambda k: (k == UNMATCHED, -len(by[k]), k))

    cards = []
    for r in reps:
        rows = "".join(f'<li>{n}</li>' for n in by[r])   # already escaped on the page
        cards.append(f'<div class="rep"><div class="rep-top"><h3>{E(r)}</h3>'
                     f'<span class="when">{len(by[r])} file{"s" if len(by[r]) != 1 else ""}'
                     f'</span></div><ul class="rep-files">{rows}</ul></div>')
    return ('<hr class="rep-divider"><section class="reps">'
            f'<div class="stage-head"><h2>Files by salesperson</h2>'
            f'<span class="count">{len(reps)} reps &middot; '
            f'{sum(len(v) for v in by.values())} insureds</span></div>'
            '<p class="stage-blurb">The same files as above, grouped by the Legacy Roofing '
            'rep who brought them in. Names only &mdash; the status of each file is in the '
            'sections above.</p>\n' + "\n".join(cards) + '\n</section>\n')


CSS = """
  /* Roster: the same files again, grouped by the rep who brought them in, so a
     salesperson can find their own book without reading the whole page. Names only --
     status lives once, in the stage sections above. */
  .rep-divider{margin:34px 0 18px; border:0; border-top:2px solid var(--accent); opacity:.4}
  .reps .stage-head h2{color:var(--accent)}
  .rep{
    background:var(--card); border:1px solid var(--line); border-radius:var(--radius);
    padding:14px 18px; margin-bottom:10px;
  }
  .rep-top{display:flex; align-items:baseline; justify-content:space-between; gap:10px}
  .rep h3{margin:0; font-size:15.5px; letter-spacing:-.01em}
  ul.rep-files{
    margin:9px 0 0; padding:0; list-style:none;
    display:grid; grid-template-columns:repeat(auto-fill,minmax(220px,1fr)); gap:2px 18px;
  }
  ul.rep-files li{font-size:13.5px; color:var(--muted); padding:1px 0}
  @media(max-width:520px){ ul.rep-files{grid-template-columns:1fr} }
"""


def main(attributed, page=PAGE):
    doc = open(page).read()
    before = len(doc.encode())

    for stage, blocks in collections.OrderedDict(
            (s, [f for f in NEW if f['stage'] == s])
            for s in dict.fromkeys(f['stage'] for f in NEW)).items():
        doc = insert_into_stage(doc, E(stage), blocks)

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
    doc = doc.replace('<section class="foot">', roster_html(doc, records) + '<section class="foot">')
    doc = doc.replace('  .foot{border-top', CSS.rstrip() + '\n\n  .foot{border-top')

    open(page, 'w').write(doc)
    nonascii = [c for c in doc if ord(c) > 127]
    print(f'{page}: {before} -> {len(doc.encode())} bytes')
    print(f'files {total} (settled {settled}, referred out {referred}, needs-you {needs})')
    print(f'roster reps: {len(set(r["rep"] or "unmatched" for r in records))}')
    print(f'non-ascii characters: {len(nonascii)}')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else PAGE)
