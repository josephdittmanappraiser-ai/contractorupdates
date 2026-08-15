#!/usr/bin/env python3
"""
Build per-rep contractor status pages from a Trello board export.

Deterministic: the page content is computed from the CSV, not written by a model,
so two runs over the same export produce byte-identical pages. A publisher agent
only has to upload the result.

    python3 tools/build_rep_pages.py <board-export.csv> [outdir]
"""
import csv, json, re, sys, os, collections, html

CFG = json.load(open(os.path.join(os.path.dirname(__file__), '..', 'config', 'contractors.json')))
PER_REP_LABELS = {c['label']: c for c in CFG['contractors'] if c.get('pageMode') == 'per-rep'}

# Spelling variants of one person. Same surname + different first name is NEVER merged.
ALIAS = {
    "sergio dehoyos": ["sergio de hoyos", "sergio dehoyas", "sergio d", "sergio"],
    "heather griffiths": ["heather griffin", "heather griffins", "heather"],
    "zacharias khan": ["zach khan"], "kristopher bigham": ["kris bigham"],
    "grant reber": ["grant rebar"], "paul ravel": ["paul revel"],
    "stephen vaughn": ["stephan vaughn"], "robert ferguson": ["robertf"],
    "rusty coffman": ["rusty"], "stephen gossett": ["stephen b. gossett"],
    "andres soto": ["andres"], "mazin shahin": ["mazin"], "kevin salazar": ["kevin"],
}
_LOOK = {}
for _c, _vs in ALIAS.items():
    _LOOK[_c] = _c
    for _v in _vs:
        _LOOK[_v] = _c


def canon(s):
    return _LOOK.get(re.sub(r'\s+', ' ', (s or '').strip().lower()), re.sub(r'\s+', ' ', (s or '').strip().lower()))


def titlecase(s):
    return " ".join(w[:1].upper() + w[1:] for w in s.split())


# ---------------------------------------------------------------- sanitizing
SHORTHAND = re.compile(r'\b(oa|ad|doa|ff|sou|cn|ho|pa|est|inv)\b', re.I)


def clean_insured(card_name, desc):
    """Reduce a Trello card name to the insured's name.

    Joseph appends operator notes to card names -- 'DO NOT MESSAGE ANYONE (BEN
    DITTMAN IS OA)', 'I paid $1,250 for umpire fee. charge back.' None of that may
    reach a client page.
    """
    s = card_name or ''
    s = re.sub(r'(?i)-\s*(oa|ad|doa|ff|sou|cn)\b', r' - \1', s)  # GRASSI-oa -> GRASSI - oa
    s = re.sub(r'\[[^\]]*\]', ' ', s)          # [CN: 033232/14003 Goodman St]
    s = re.sub(r'\([^)]*\)', ' ', s)           # ( BEN DITTMAN IS OA )
    s = re.split(r'\s+-\s+|\s*/\s*|,', s)[0]   # cut at the first note separator
    keep = []
    for tok in s.split():
        if any(ch.isdigit() for ch in tok) or '$' in tok:
            break
        if SHORTHAND.fullmatch(tok):
            break
        keep.append(tok)
    out = " ".join(keep).strip(" -–—:;.")
    # A plausible person's name: 2+ alphabetic words, nothing shouty left over.
    words = [w for w in out.split() if re.fullmatch(r"[A-Za-z'’.\-]+", w)]
    if len(words) >= 2:
        return titlecase(" ".join(words))
    m = re.search(r'(?:insured|name)\s*[:\-]\s*([A-Za-z][A-Za-z\'’.\- ]{3,40})', desc or '', re.I)
    if m:
        return titlecase(m.group(1).strip())
    return titlecase(" ".join(words)) if words else "(name withheld)"


ADDR = re.compile(r'(?:loss address|address)\s*[:\-]\s*(.+)', re.I)
CLAIM = re.compile(r'claim\s*#?\s*[:\-]\s*([A-Za-z0-9\-/]+)', re.I)
NOTE = re.compile(r'\[(\d{4}-\d{2}-\d{2})\]\s*(.+)')


def extract(desc):
    d = desc or ''
    a = ADDR.search(d)
    c = CLAIM.search(d)
    addr = re.sub(r'\s+', ' ', a.group(1)).strip()[:80] if a else ''
    addr = re.split(r'\s{2,}|\n', addr)[0]
    claim = c.group(1).strip() if c else ''
    notes = NOTE.findall(d)
    return addr, claim, (notes[-1][1].strip() if notes else '')


# ---------------------------------------------------------------- staging
def stage_for(list_name):
    ln = (list_name or '').lower()
    for st in CFG['stageMap']:
        for m in st['matchers']:
            if m in ln:
                return st
    return CFG['stageMap'][-1]


def excluded(list_name, card_name, desc):
    ln = (list_name or '').lower()
    if any(x in ln for x in CFG['excludeLists']):
        return True
    blob = f"{card_name} {desc}".lower()
    return any(m.lower() in blob for m in CFG.get('excludeCardMarkers', []))


# ---------------------------------------------------------------- rendering
CSS = open(os.path.join(os.path.dirname(__file__), '..', 'templates', 'status-page.html')).read()
CSS = CSS[CSS.index('<style>'):CSS.index('</style>') + 8]

E = html.escape


def render(display_name, files, updated):
    by = collections.defaultdict(list)
    for f in files:
        by[f['stage']['stage']].append(f)
    stages = sorted(by.items(), key=lambda kv: -next(
        s['order'] for s in CFG['stageMap'] if s['stage'] == kv[0]))

    total = len(files)
    active = sum(1 for f in files if 4 <= f['stage']['order'] <= 9)
    needs = sum(1 for f in files if f['needs_you'])
    settled = sum(1 for f in files if f['stage']['stage'].startswith('Settled'))

    out = [f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">',
           '<meta name="viewport" content="width=device-width, initial-scale=1">',
           f'<title>{E(display_name)}</title></head><body>',
           '<section class="head"><p class="eyebrow">TX Insurance Appraisals</p>',
           f'<h1>{E(display_name)}</h1>',
           f'<p class="sub">Where every file you sent us currently stands. Updated {E(updated)}.</p></section>',
           '<section class="tiles">',
           f'<div class="tile"><span class="n">{total}</span><span class="l">Open files</span></div>',
           f'<div class="tile"><span class="n">{active}</span><span class="l">In appraisal</span></div>',
           f'<div class="tile alert"><span class="n">{needs}</span><span class="l">Need you</span></div>',
           f'<div class="tile good"><span class="n">{settled}</span><span class="l">Settled</span></div>',
           '</section>']

    for name, items in stages:
        st = next(s for s in CFG['stageMap'] if s['stage'] == name)
        items.sort(key=lambda f: f['activity'], reverse=True)
        out.append('<section class="stage"><div class="stage-head">'
                   f'<h2>{E(name)}</h2><span class="count">{len(items)} '
                   f'file{"s" if len(items) != 1 else ""}</span></div>'
                   f'<p class="stage-blurb">{E(st["blurb"])}</p>')
        for f in items:
            meta = " &middot; ".join(x for x in [E(f['addr']), (f"Claim {E(f['claim'])}" if f['claim'] else '')] if x)
            out.append(f'<div class="file{" needs-you" if f["needs_you"] else ""}">'
                       f'<div class="file-top"><h3>{E(f["insured"])}</h3>'
                       f'<span class="when">last activity {E(f["activity"][:10])}</span></div>'
                       + (f'<p class="meta">{meta}</p>' if meta else '')
                       + f'<p class="what">{E(f["what"])}</p>'
                       + ('<p class="ask">Need from you: approval of the estimate, or a signed agreement '
                          'from the homeowner, before this can move.</p>' if f['needs_you'] else '')
                       + '</div>')
        out.append('</section>')

    out.append('<section class="foot"><p>Questions on any file here? Reply to your last email '
               'thread with us, or call 737-258-3127.</p>'
               '<p class="fine">This page refreshes every Monday morning. Bookmark it &mdash; '
               'the link stays the same.</p></section>')
    out.append(CSS)
    out.append('</body></html>')
    return "\n".join(out)


# ---------------------------------------------------------------- main
APPROVED = set()
_lbl = os.path.join(os.path.dirname(__file__), '..', 'work', 'rep-labels-to-create.md')
if os.path.exists(_lbl):
    for _line in open(_lbl):
        if _line.startswith('| ') and 'Label to create' not in _line and '---' not in _line:
            APPROVED.add(canon(_line.strip().strip('|').split('|')[0].strip()))


def main(csv_path, outdir='work/pages'):
    rows = list(csv.DictReader(open(csv_path, encoding='utf-8-sig')))
    os.makedirs(outdir, exist_ok=True)
    updated = "Saturday, August 15, 2026"

    buckets = collections.defaultdict(lambda: collections.defaultdict(list))
    dropped = collections.Counter()

    for r in rows:
        labels = (r.get('Labels') or '')
        for lab, cfg in PER_REP_LABELS.items():
            if lab.lower() not in labels.lower():
                continue
            name, desc, lst = r.get('Card Name', ''), r.get('Card Description', ''), r.get('List Name', '')
            if excluded(lst, name, desc):
                dropped['excluded list/marker'] += 1
                continue
            rep = canon(r.get('Sales Person') or '')
            # A rep only earns their own page if a Trello label exists for them
            # (the approved 2-or-more-files list). Everyone else -- blanks, one-off
            # reps, spellings nobody labelled -- lands on the company's unassigned
            # page rather than generating a page for a single file.
            if rep not in APPROVED:
                rep = '__unassigned__'
            st = stage_for(lst)
            addr, claim, note = extract(desc)
            if not claim:
                claim = (r.get('Claim #') or '').strip()
            buckets[lab][rep].append({
                'insured': clean_insured(name, desc),
                'addr': addr, 'claim': claim,
                'activity': (r.get('Last Activity Date') or '')[:10],
                'stage': st,
                'needs_you': st['order'] == 3,
                # NOTE deliberately unused: the trailing [YYYY-MM-DD] notes are
                # internal (staff names, dollar figures, carrier strategy). A
                # deterministic builder cannot safely paraphrase them, so the page
                # shows the stage's plain-language blurb.
                'what': st['blurb'],
            })

    manifest = []
    for lab, reps in buckets.items():
        cfg = PER_REP_LABELS[lab]
        company = cfg['company']
        known = {canon(rp['name']): rp.get('shareId') for rp in cfg.get('reps', [])}
        for rep, files in sorted(reps.items(), key=lambda kv: -len(kv[1])):
            if rep == '__unassigned__':
                disp, slug = f"{company} — Unassigned Files", f"{lab[:6].lower()}-unassigned"
                sid = cfg.get('unassignedShareId')
            else:
                disp = f"{titlecase(rep)} — {company}"
                slug = re.sub(r'[^a-z0-9]+', '-', f"{lab[:6]}-{rep}".lower()).strip('-')
                sid = known.get(rep)
            path = os.path.join(outdir, f"{slug}.html")
            open(path, 'w').write(render(disp, files, updated))
            manifest.append({'label': lab, 'rep': titlecase(rep), 'title': disp,
                             'file': path, 'shareId': sid, 'files': len(files),
                             'action': 'edit' if sid else 'create'})

    json.dump(manifest, open(os.path.join(outdir, 'manifest.json'), 'w'), indent=1)
    e = sum(1 for m in manifest if m['action'] == 'edit')
    print(f"pages built: {len(manifest)}  (edit existing: {e}, create new: {len(manifest)-e})")
    print(f"files placed: {sum(m['files'] for m in manifest)}   dropped: {dict(dropped)}")
    return manifest


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else 'work/pages')
