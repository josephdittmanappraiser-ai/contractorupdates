#!/usr/bin/env python3
"""
Build per-rep contractor status pages from a Trello board export.

Deterministic: the page content is computed from the CSV, not written by a model,
so two runs over the same export produce byte-identical pages. A publisher agent
only has to upload the result.

    python3 tools/build_rep_pages.py <board-export.csv> [outdir]
"""
import csv, json, re, sys, os, glob, collections, html, datetime

CFG = json.load(open(os.path.join(os.path.dirname(__file__), '..', 'config', 'contractors.json')))
PER_REP_LABELS = {c['label']: c for c in CFG['contractors'] if c.get('pageMode') == 'per-rep'}
COMPANY_LABELS = {c['label']: c for c in CFG['contractors'] if c.get('pageMode') != 'per-rep'}

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


# "Email address:" also ends in "address:", and matching it put homeowners' personal
# email addresses on client-facing pages. Require the label to be the loss address.
ADDR = re.compile(r'(?<!e-mail )(?<!email )(?:loss address|property address|address)\s*[:\-]\s*(.+)', re.I)
CLAIM = re.compile(r'claim\s*#?\s*[:\-]\s*([A-Za-z0-9\-/]+)', re.I)
NOTE = re.compile(r'\[(\d{4}-\d{2}-\d{2})\]\s*(.+)')


def clean_addr(s):
    """A street address, or nothing. Card descriptions are free text and the address
    line picks up whatever sits next to it."""
    s = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', s)   # [text](mailto:...) -> text
    s = re.sub(r'\s+', ' ', s).strip(' .,;:-')
    if '@' in s or 'mailto' in s.lower():
        return ''
    if re.search(r'\(\d{3}\)\s?\d{3}-\d{4}|\b\d{3}-\d{3}-\d{4}\b', s):
        return ''
    return s[:80]


def extract(desc):
    d = desc or ''
    a = ADDR.search(d)
    c = CLAIM.search(d)
    addr = re.sub(r'\s+', ' ', a.group(1)).strip()[:80] if a else ''
    addr = clean_addr(re.split(r'\s{2,}|\n', addr)[0])
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


# Files where appraisal was invoked and the carrier never named an appraiser sit still
# while looking no different from a file that is progressing. Joseph asked for those
# called out once they pass 60 days -- it is the point where chasing the carrier stops
# being routine follow-up and becomes the thing holding the file up.
#
# Two things can start that clock, and the second matters as much as the first:
#   1. a demand that reached the carrier, and
#   2. the office writing, in as many words, that the file is still without a carrier
#      appraiser. Joseph's staff flag that themselves, and on several files it is the
#      only plain statement in the record -- the demand itself is buried in phrasing no
#      pattern will catch ("resent the appraisal demand to USAA for this claim").
STALL_DAYS = 60
AS_OF = datetime.date.today()

# A demand -- any wording.
DEMAND_RE = re.compile(
    r'\b(appraisal demand|demand letter|demand was sent|sent (?:the |a |an )?'
    r'(?:pre-?appraisal )?demand|invoked appraisal|appraisal (?:was )?invoked|'
    r'demanded appraisal)\b', re.I)
# ...that actually went to the carrier. "Sent to the homeowner for signature" is a letter
# sitting unsigned on a kitchen table; the carrier has not been told anything, and orange
# on that blames the carrier for a delay that is not theirs.
AT_CARRIER_RE = re.compile(
    r'\b(?:to|with) the carrier\b|\binvoked\b|'
    r'\bappraisal demand\b[^.;]{0,30}?\bto \w|'
    r'\bsent \w[\w&.\-]* the appraisal demand\b|'
    r'\bdemand (?:letter )?(?:was )?(?:sent|submitted|resent) to \w|'
    r"naming .{0,45} as the insured'?s appraiser", re.I)
TO_HOMEOWNER_RE = re.compile(
    r'\bto the (?:homeowner|insured|customer|client)\b|for (?:review and )?signature|'
    r'\bto sign\b|\bunsigned\b', re.I)
# The office saying it outright. This is the most reliable signal in the whole record.
NO_APPRAISER_RE = re.compile(
    r'\bwithout (?:a|an|any) (?:carrier|opposing) appraiser\b|'
    r'\bno (?:carrier |opposing )?appraiser (?:has been )?(?:named|assigned|appointed)\b|'
    r'\b(?:carrier|they) (?:has|have|had) not (?:yet )?(?:named|assigned|appointed)\b|'
    r'\bwaiting (?:on|for) (?:the )?carrier to (?:name|assign|appoint)\b',
    re.I)
# Any later mention of a carrier-side appraiser means one exists -- deliberately broad,
# because a missed orange flag is better than a wrong one on a client's page.
NAMED_RE = re.compile(
    r"\b(named (?:its|their|his|her|the)?\s*appraiser|appraiser (?:was |is |has been )?named|"
    r"carrier'?s appraiser|opposing appraiser|named .{0,25} as (?:its|their) appraiser|"
    r"appraiser assigned)\b", re.I)
# A file the insured pulled out of is not waiting on the carrier for anything.
WITHDRAWN_RE = re.compile(
    r'\b(withdrew|withdrawn|no longer want\w*|did not want|pulled the file|'
    r'cancell?ed the appraisal|rescinded|never actually been taken)\b', re.I)


def stalled_days(f):
    """Days since appraisal was invoked, if the carrier still has not named an appraiser.

    Only asked of files that have not reached inspection -- scheduling, inspecting,
    negotiating and umpire all presuppose an appraiser on the other side.
    """
    if f['stage']['order'] > 4:
        return None
    events = sorted(f.get('timeline') or [], key=lambda e: str(e.get('date', ''))[:10])

    def txt(e):
        return e.get('event', '') or ''

    anchors = [e for e in events
               if (DEMAND_RE.search(txt(e)) and AT_CARRIER_RE.search(txt(e))
                   and not TO_HOMEOWNER_RE.search(txt(e)))
               or NO_APPRAISER_RE.search(txt(e))]
    if not anchors:
        return None
    d0 = str(anchors[0].get('date', ''))[:10]

    # NO_APPRAISER_RE says an appraiser is missing and NAMED_RE says one is mentioned, so
    # the anchor matches both. Judge only what came after it.
    for e in events:
        if str(e.get('date', ''))[:10] <= d0:
            continue
        # "still without a carrier appraiser" contains the phrase "carrier appraiser",
        # so NAMED_RE fires on a sentence that says the opposite. A later restatement
        # that none exists must not cancel the flag it should be reinforcing.
        if NO_APPRAISER_RE.search(txt(e)):
            continue
        if NAMED_RE.search(txt(e)) or WITHDRAWN_RE.search(txt(e)):
            return None
    try:
        days = (AS_OF - datetime.date.fromisoformat(d0)).days
    except ValueError:
        return None
    return days if days > STALL_DAYS else None


# The steps a file walks through, condensed from the 11 stages. A contractor reading
# "Negotiating with the carrier's appraiser" knows what it means; they do not necessarily
# know how much of the process is behind them, which is the question they actually have.
TRACK = ['Intake', 'Estimate', 'Demand', 'Inspection', 'Negotiating', 'Umpire', 'Settled']
# Referred out (9) is not a point on this line -- those files get no strip at all.
STAGE_STEP = {1: 0, 2: 1, 3: 1, 4: 2, 5: 3, 6: 3, 7: 4, 8: 5, 10: 6, 11: 6}


def track_html(order):
    """Where this file sits in the process, as a strip of steps."""
    here = STAGE_STEP.get(order, 0)
    return ('<ol class="track">' + "".join(
        f'<li class="{"now" if i == here else "done" if i < here else "todo"}">{s}</li>'
        for i, s in enumerate(TRACK)) + '</ol>')


def ordered(events):
    """Oldest first. Agents return them in order, but the page must not depend on that."""
    return sorted(events, key=lambda e: str(e.get('date', ''))[:10])


def last_activity(f):
    """The card's own last-activity date understates a file whose newest email is newer --
    a Trello card only updates when someone touches it. Show whichever is later."""
    tl = f.get('timeline') or []
    newest = max([str(e.get('date', ''))[:10] for e in tl] + [(f.get('activity') or '')[:10]])
    return newest


def latest_html(events, n=3):
    """The newest events, open on the page.

    The full chain sits collapsed below this, and a collapsed thing is a thing most
    people never open. What a contractor wants first is what moved lately -- so the
    last few events are printed where they cannot be missed, and the history stays
    underneath for anyone who wants the whole story.
    """
    if not events:
        return ''
    events = ordered(events)
    recent = list(reversed(events[-n:]))
    rows = "".join(
        f'<li><span class="d">{E(str(ev.get("date", ""))[:10])}</span>{E(ev.get("event", ""))}</li>'
        for ev in recent)
    return f'<div class="latest"><p class="latest-h">Most recent activity</p><ol class="events">{rows}</ol></div>'


def chain_html(events):
    """Collapsed, dated history of everything done on or received for the file."""
    if not events:
        return ''
    events = ordered(events)
    rows = "".join(
        f'<li><span class="d">{E(str(ev.get("date", ""))[:10])}</span>{E(ev.get("event", ""))}</li>'
        for ev in events)
    n = len(events)
    return (f'<details class="chain"><summary>Full history from the start ({n} events)</summary>'
            f'<ol class="events">{rows}</ol></details>')


# A page larger than this is published in pieces by tools/split_page.py rather than
# in one EditSite call. The ceiling below is a backstop for absurd growth only --
# trimming history is a worse outcome than a multi-call publish, so it sits well
# above any real page. Two clients (No Stress, Legacy) exceed a single call.
MAX_PAGE_BYTES = 400_000


def render_fitted(display_name, files, updated):
    """Render, then trim timeline depth only if the page is beyond even a chunked publish.

    Trimming is announced on the page rather than done quietly.
    """
    html_out = render(display_name, files, updated)
    if len(html_out.encode()) <= MAX_PAGE_BYTES:
        return html_out, None
    for cap in (10, 6, 4, 3, 2):
        trimmed = []
        for f in files:
            g = dict(f)
            tl = f.get('timeline') or []
            if len(tl) > cap:
                g['timeline'] = tl[-cap:]
                g['trimmed'] = len(tl) - cap
            trimmed.append(g)
        html_out = render(display_name, trimmed, updated, cap=cap)
        if len(html_out.encode()) <= MAX_PAGE_BYTES:
            return html_out, cap
    return html_out, 2


def render(display_name, files, updated, cap=None):
    by = collections.defaultdict(list)
    for f in files:
        by[f['stage']['stage']].append(f)
    def rank(stage_name):
        o = next(s['order'] for s in CFG['stageMap'] if s['stage'] == stage_name)
        # Contractors want what still needs attention first, so settled work drops
        # to the bottom: unpaid-but-closed ahead of fully-paid, since an open
        # invoice is the only settled thing they might still act on.
        if stage_name.startswith('Settled'):
            return (0, 1 if 'outstanding' in stage_name else 0)
        return (1, o)
    stages = sorted(by.items(), key=lambda kv: rank(kv[0]), reverse=True)

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

    seen_settled = False
    for name, items in stages:
        st = next(s for s in CFG['stageMap'] if s['stage'] == name)
        items.sort(key=lambda f: f['activity'], reverse=True)
        is_settled = name.startswith('Settled')
        if is_settled and not seen_settled:
            seen_settled = True
            out.append('<hr class="settled-divider">'
                       '<p class="settled-lead">Closed files &mdash; nothing needed from you '
                       'on these.</p>')
        out.append(f'<section class="stage{" settled" if is_settled else ""}">'
                   '<div class="stage-head">'
                   f'<h2>{E(name)}</h2><span class="count">{len(items)} '
                   f'file{"s" if len(items) != 1 else ""}</span></div>'
                   f'<p class="stage-blurb">{E(st["blurb"])}</p>')
        for f in items:
            meta = " &middot; ".join(x for x in [E(f['addr']), (f"Claim {E(f['claim'])}" if f['claim'] else '')] if x)
            stalled = stalled_days(f)
            cls = ' needs-you' if f['needs_you'] else (' waiting' if stalled else '')
            out.append(f'<div class="file{cls}">'
                       f'<div class="file-top"><h3>{E(f["insured"])}</h3>'
                       f'<span class="when">last activity {E(last_activity(f))}</span></div>'
                       + (f'<p class="meta">{meta}</p>' if meta else '')
                       + ('' if is_settled or f['stage']['order'] == 9
                          else track_html(f['stage']['order']))
                       + f'<p class="what">{E(f["what"])}</p>'
                       + (f'<p class="ask">{E(f["ask"])}</p>' if f['needs_you'] else '')
                       + (f'<p class="waiting-note">Appraisal was invoked {stalled} days ago and '
                          'the carrier still has not named an appraiser. We are chasing them on '
                          'it.</p>' if stalled else '')
                       + latest_html(f.get('timeline'))
                       + chain_html(f.get('timeline'))
                       + '</div>')
        out.append('</section>')

    if cap:
        out.append('<section class="foot"><p class="fine">This client has enough open files that '
                   f'each history below shows its {cap} most recent events. Ask us for the full '
                   'history on any file.</p></section>')
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


BANNED = [
    (re.compile(r'\bDOA\b'), 'the signed agreement'),
    (re.compile(r'\bOA\b'), "the carrier's appraiser"),
    (re.compile(r'\bSOU\b'), 'the scope of work'),
    (re.compile(r'\bCN\b'), 'claim'),
    (re.compile(r'\bff\b'), 'follow up'),
    (re.compile(r'\$\s?[\d,]+(?:\.\d{2})?'), '[amount withheld]'),
    (re.compile(r'\b(Erwin|Imee|Geralden|Sheila|Kristelle|Stephanie|Jia Ever|Mark Tirones)\b'),
     'our office'),
    (re.compile(r'\b(debt collections?|past due|charge ?backs?)\b', re.I), 'the open invoice'),
    (re.compile(r'\(\d{3}\)\s?\d{3}-\d{4}'), ''),
    (re.compile(r'[\w.+-]+@[\w.-]+\.[a-z]{2,}'), ''),
]


def scrub(text):
    """Last line of defence before anything reaches a client page.

    The enrichment agents are told never to emit internal shorthand, dollar
    figures, staff names or homeowner contact details -- but across hundreds of
    files one will slip, and it did. Rendering is the only place every string
    passes through, so it enforces the rule rather than trusting the writer.
    """
    if not text:
        return text
    for pat, repl in BANNED:
        text = pat.sub(repl, text)
    # Expansions like OA -> "the carrier's appraiser" collide with an article already
    # in the sentence ("the OA" -> "the the carrier's appraiser"). Collapse those.
    text = re.sub(r'\b(the|a|an)\s+the\b', 'the', text, flags=re.I)
    text = re.sub(r'\bthe\s+the\b', 'the', text, flags=re.I)
    text = re.sub(r'\s+([,.;:])', r'\1', text)
    return re.sub(r'\s{2,}', ' ', text).strip(' ,;')


# Enrichment, keyed by card id. `rerun/` is loaded last and wins: it holds files whose
# timeline was found to stop short of the newest email and was re-read.
ENRICH = {}
_UP = os.path.join(os.path.dirname(__file__), '..', 'work', 'updates')
for _f in sorted(glob.glob(os.path.join(_UP, 'out*.json'))) + \
          sorted(glob.glob(os.path.join(_UP, 'rerun', 'out*.json'))):
    try:
        _d = json.load(open(_f))
    except Exception:
        continue
    for _r in (_d.get('results') if isinstance(_d, dict) else _d) or []:
        if _r.get('cardId'):
            ENRICH[_r['cardId'].strip()] = _r

# The verification pass returns only what a file GAINED, because it re-checked a claim that
# nothing had happened since a given date. So merge rather than replace: a verify record
# carrying three new events must not wipe the twelve already on the file.
for _f in (sorted(glob.glob(os.path.join(_UP, 'verify', 'out*.json')))
           + sorted(glob.glob(os.path.join(_UP, 'read', 'out*.json')))):
    try:
        _d = json.load(open(_f))
    except Exception:
        continue
    for _r in (_d.get('results') if isinstance(_d, dict) else _d) or []:
        _cid = (_r.get('cardId') or '').strip()
        if not _cid or not (_r.get('hasNewer') or _r.get('newEvents')):
            continue
        _base = ENRICH.setdefault(_cid, {'cardId': _cid, 'timeline': []})
        _tl = list(_base.get('timeline') or [])
        _seen = {(str(e.get('date', ''))[:10], (e.get('event') or '').strip().lower())
                 for e in _tl}
        for _e in _r.get('newEvents') or []:
            _k = (str(_e.get('date', ''))[:10], (_e.get('event') or '').strip().lower())
            if _k not in _seen:
                _seen.add(_k)
                _tl.append(_e)
        _base['timeline'] = _tl
        if _r.get('update'):
            _base['update'] = _r['update']
        if 'needed' in _r:
            _base['needed'] = _r['needed']


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
            en = ENRICH.get(r['Card ID'].strip(), {})
            buckets[lab][rep].append({
                'cardId': r['Card ID'].strip(),
                'insured': clean_insured(name, desc),
                'addr': addr, 'claim': claim,
                'activity': (r.get('Last Activity Date') or '')[:10],
                'stage': st,
                'timeline': [{'date': e.get('date', ''), 'event': scrub(e.get('event', ''))}
                             for e in (en.get('timeline') or [])],
                'ask': scrub(en.get('needed')) or ('Need from you: approval of the estimate, or a '
                                                   'signed agreement from the homeowner, before this '
                                                   'can move.'),
                'needs_you': bool(en.get('needed')) or st['order'] == 3,
                # Prefer the email-derived status; fall back to the stage blurb.
                # The trailing [YYYY-MM-DD] card notes are never used -- they are
                # internal (staff names, dollar figures, carrier strategy).
                'what': scrub(en.get('update')) or st['blurb'],
            })

    manifest = []

    # ---- company-mode clients: one page for the whole firm -------------------
    combuckets = collections.defaultdict(list)
    for r in rows:
        labels = (r.get('Labels') or '')
        for lab, cfg in COMPANY_LABELS.items():
            if lab.lower() not in labels.lower():
                continue
            name, desc, lst = r.get('Card Name', ''), r.get('Card Description', ''), r.get('List Name', '')
            if excluded(lst, name, desc):
                continue
            st = stage_for(lst)
            addr, claim, note = extract(desc)
            if not claim:
                claim = (r.get('Claim #') or '').strip()
            en = ENRICH.get(r['Card ID'].strip(), {})
            combuckets[lab].append({
                'cardId': r['Card ID'].strip(),
                'insured': clean_insured(name, desc), 'addr': addr, 'claim': claim,
                'activity': (r.get('Last Activity Date') or '')[:10], 'stage': st,
                'timeline': [{'date': e.get('date', ''), 'event': scrub(e.get('event', ''))}
                             for e in (en.get('timeline') or [])],
                'ask': scrub(en.get('needed')) or ('Need from you: approval of the estimate, or a '
                                                   'signed agreement from the homeowner, before this '
                                                   'can move.'),
                'needs_you': bool(en.get('needed')) or st['order'] == 3,
                'what': scrub(en.get('update')) or st['blurb'],
            })
    for lab, files in combuckets.items():
        cfg = COMPANY_LABELS[lab]
        slug = re.sub(r'[^a-z0-9]+', '-', f"company-{cfg['company']}".lower()).strip('-')
        path = os.path.join(outdir, f"{slug}.html")
        html_out, cap = render_fitted(cfg['company'], files, updated)
        open(path, 'w').write(html_out)
        manifest.append({'label': lab, 'rep': cfg['company'], 'title': cfg['company'],
                         'file': path, 'shareId': cfg.get('shareId'), 'files': len(files),
                         'action': 'edit' if cfg.get('shareId') else 'create',
                         'cardIds': [f['cardId'] for f in files]})

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
            html_out, cap = render_fitted(disp, files, updated)
            open(path, 'w').write(html_out)
            manifest.append({'label': lab, 'rep': titlecase(rep), 'title': disp,
                             'file': path, 'shareId': sid, 'files': len(files),
                             'action': 'edit' if sid else 'create',
                             'cardIds': [f['cardId'] for f in files]})

    json.dump(manifest, open(os.path.join(outdir, 'manifest.json'), 'w'), indent=1)
    e = sum(1 for m in manifest if m['action'] == 'edit')
    print(f"pages built: {len(manifest)}  (edit existing: {e}, create new: {len(manifest)-e})")
    print(f"files placed: {sum(m['files'] for m in manifest)}   dropped: {dict(dropped)}")
    return manifest


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else 'work/pages')
