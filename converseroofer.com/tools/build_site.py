import os, html
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHONE = "832-503-5866"; TEL = "tel:+18325035866"; SMS = "sms:+18325035866"
BRAND = "Converse Roofer"; DOMAIN = "https://converseroofer.com"

IMGS = {
 "hero":   ("1600585154340-be6161a56a0c","Two-story brick home with a new architectural shingle roof in Converse, TX","house"),
 "roof1":  ("1632759145351-1d592919f522","Close-up of asphalt shingles on a residential roof","roof"),
 "roof2":  ("1605276374104-dee2a0ed3cd6","New roof installation in progress","roof"),
 "roofer1":("1635424710928-0544e8512eae","Roofer inspecting shingles on a pitched roof","tools"),
 "roofer2":("1581094288338-2314dddb7ece","Contractor in a hard hat reviewing a job","tools"),
 "crew":   ("1504307651254-35680f356dfd","Roofing crew working together on a job site","tools"),
 "storm1": ("1527482797697-8795b05a13fe","Lightning striking during a severe thunderstorm over Texas","storm"),
 "storm2": ("1500674425229-f692875b0ab7","Dark storm clouds rolling in over a neighborhood","storm"),
 "storm3": ("1534088568595-a066f410bcda","Supercell thunderstorm building at dusk","storm"),
 "storm4": ("1510798831971-661eb04b3739","Storm front approaching over open land","storm"),
 "hail1":  ("1594156596782-656c93e4d504","Hailstones on the ground after a storm","hail"),
 "hail2":  ("1523413651479-597eb2da0ad6","Heavy rain and hail during a thunderstorm","hail"),
 "house1": ("1570129477492-45c003edd2be","Single-story home with a hip roof","house"),
 "house2": ("1564013799919-ab600027ffc6","Brick home with a dimensional shingle roof","house"),
 "house3": ("1580587771525-78b9dba3b914","Suburban home with a gabled roof and driveway","house"),
 "house4": ("1518780664697-55e3ad937233","Craftsman-style home exterior","house"),
 "house5": ("1568605114967-8130f3a36994","Home exterior with fresh roofing","house"),
 "house6": ("1449844908441-8829872d2607","Home exterior at dusk with new roof","house"),
 "house7": ("1583608205776-bfd35f0d9f83","Modern home with a standing-seam metal roof","house"),
 "house8": ("1600596542815-ffad4c1539a9","Two-story home with a complex roofline","house"),
 "house9": ("1600047509807-ba8f99d2cdde","Family home with a new composition roof","house"),
 "house10":("1613977257363-707ba9348227","Ranch-style home with a low-slope roof","house"),
 "house11":("1512917774080-9991f1c4c750","Home exterior with pool and tile roof","house"),
 "rain":   ("1428592953211-077101b2021b","Rain streaming down a window during a storm","storm"),
 "ladder": ("1541888946425-d81bb19240f5","Ladder set against a home during roof work","tools"),
 "handshake":("1556761175-5973dc0f32e7","Homeowner and contractor reviewing an estimate","shield"),
 "docs":   ("1554224155-6726b3ff858f","Insurance paperwork and a calculator on a desk","shield"),
 "team":   ("1521737711867-e3b97375f902","Roofing team planning a job","tools"),
 "gutter": ("1621905251189-08b45d6a269e","Contractor working along the roof edge","tools"),
}
def img(key, root="", cls="", w=1200, attrs=""):
    pid, alt, fb = IMGS[key]
    clsattr = ('class="' + cls + '"') if cls else ""
    fallback = root + "assets/img/ph-" + fb + ".svg"
    return ('<img src="https://images.unsplash.com/photo-' + pid + '?auto=format&fit=crop&w=' + str(w) + '&q=70" alt="' + html.escape(alt) + '" '
            'loading="lazy" ' + clsattr + ' ' + attrs + ' '
            "onerror=\"this.onerror=null;this.src='" + fallback + "'\">")

NAV = [("index.html","Home"),("hail-storm-september-11-2026.html","9/11 Hail Storm"),("weather.html","Weather"),("gallery.html","Photos"),("blog/index.html","Blog"),("about.html","About Us"),("contact.html","Contact")]

def lead_form(root="", compact=False, title="Get Your Free Roof Inspection", sub="No cost, no pressure. We'll look at your roof, photograph any hail damage, and tell you honestly what it needs."):
    notes_field = "" if compact else '<div><label for="f-notes">Anything we should know?</label><textarea id="f-notes" name="notes" rows="3" placeholder="Leaks, missing shingles, dents on gutters or AC unit, best time to call…"></textarea></div>'
    return f'''
<div class="lead-card">
  <h3>{title}</h3>
  <p class="sub">{sub}</p>
  <form class="form" data-lead novalidate>
    <div class="row">
      <div><label for="f-name">Name</label><input id="f-name" name="name" required autocomplete="name" placeholder="Your name"></div>
      <div><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" required autocomplete="tel" placeholder="(210) 555-0123"></div>
    </div>
    <div><label for="f-address">Property address</label><input id="f-address" name="address" required autocomplete="street-address" placeholder="Street address, city"></div>
    <div class="row">
      <div><label for="f-storm">Were you hit by the 9/11 hail storm?</label>
        <select id="f-storm" name="storm"><option>Yes — Sept 11, 2026 storm</option><option>Not sure</option><option>Different storm / date</option><option>No storm — repair or replacement quote</option></select></div>
      <div><label for="f-claim">Have you contacted your insurance company?</label>
        <select id="f-claim" name="insurance_contacted"><option>Not yet</option><option>Yes, waiting on their inspection</option><option>Yes, their adjuster already came out</option><option>Not using insurance</option></select></div>
    </div>
    {notes_field}
    <div class="hp"><label>Leave blank<input name="company" tabindex="-1" autocomplete="off"></label></div>
    <button class="btn primary lg block" type="submit">Request My Free Inspection</button>
    <p class="fine">Or call / text <a href="{TEL}"><b>{PHONE}</b></a>. By submitting you agree to be contacted by phone or text about your roof. No spam, ever.</p>
    <div class="msg" role="status"></div>
  </form>
</div>'''

def layout(title, desc, body, root="", active=None, canonical="", extra_head="", storm_bar=True, schema=""):
    nav = "".join('<a href="' + root + h + '"' + (' class="active"' if h==active else '') + '>' + t + '</a>' for h,t in NAV)
    bar = f'<div class="storm-bar">⚠️ Hit by the <a href="{root}hail-storm-september-11-2026.html">September 11 hail storm</a>? Golf-ball hail fell on Converse &amp; Kirby. <a href="{root}contact.html">Free inspection</a> · <a href="{TEL}">{PHONE}</a></div>' if storm_bar else ""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{DOMAIN}/{canonical}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{DOMAIN}/{canonical}">
<meta property="og:image" content="https://images.unsplash.com/photo-{IMGS['hero'][0]}?auto=format&fit=crop&w=1200&q=70">
<link rel="icon" href="{root}favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/css/style.css">
{extra_head}
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "RoofingContractor",
  "name": "{BRAND}",
  "url": "{DOMAIN}/",
  "telephone": "+1-{PHONE}",
  "image": "{DOMAIN}/assets/img/logo.svg",
  "priceRange": "Free inspections",
  "address": {{"@type": "PostalAddress", "addressLocality": "Converse", "addressRegion": "TX", "addressCountry": "US"}},
  "areaServed": ["Converse TX","Kirby TX","Windcrest TX","Universal City TX","Live Oak TX","Schertz TX","Cibolo TX","Selma TX","St. Hedwig TX","San Antonio TX"],
  "description": "{html.escape(desc)}"
}}
</script>
{schema}
</head>
<body>
{bar}
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{root}index.html"><img src="{root}assets/img/logo.svg" alt="" width="40" height="40"><span>Converse Roofer<small>Hail &amp; storm roofing · Converse, TX</small></span></a>
    <button class="nav-toggle" aria-label="Menu" aria-expanded="false" aria-controls="nav">☰</button>
    <nav class="nav" id="nav">{nav}<a class="btn primary" href="{TEL}">📞 {PHONE}</a></nav>
  </div>
</header>
<main>
{body}
</main>
<section class="cta-band">
  <div class="wrap">
    <div><h2>Think your roof took hail on 9/11?</h2><p>Free inspection, photo report, and straight answers. Serving Converse, Kirby, Windcrest, Universal City &amp; NE San Antonio.</p></div>
    <div style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn dark lg" href="{TEL}">Call {PHONE}</a><a class="btn ghost lg" href="{root}contact.html" style="border-color:#fff">Request Online</a></div>
  </div>
</section>
<footer class="site-footer">
  <div class="wrap">
    <div class="cols">
      <div>
        <a class="brand" href="{root}index.html" style="margin-bottom:12px"><img src="{root}assets/img/logo.svg" alt="" width="40" height="40"><span>Converse Roofer</span></a>
        <p>Local storm-damage roofing for Converse and the northeast side of San Antonio. Free hail inspections, written estimates, repairs and full replacements.</p>
        <a class="phone" href="{TEL}">{PHONE}</a><br><small>Call or text · 7 days a week</small>
      </div>
      <div><h4>Pages</h4><ul>{"".join(f'<li><a href="{root}{h}">{t}</a></li>' for h,t in NAV)}</ul></div>
      <div><h4>Services</h4><ul><li><a href="{root}contact.html">Free hail inspections</a></li><li><a href="{root}contact.html">Storm damage documentation</a></li><li><a href="{root}contact.html">Roof replacement</a></li><li><a href="{root}contact.html">Roof repair &amp; leaks</a></li><li><a href="{root}contact.html">Gutters &amp; emergency tarping</a></li></ul></div>
      <div><h4>Service area</h4><ul><li>Converse</li><li>Kirby &amp; Windcrest</li><li>Universal City &amp; Live Oak</li><li>Schertz, Cibolo &amp; Selma</li><li>St. Hedwig</li><li>NE San Antonio</li></ul></div>
    </div>
    <div class="bottom"><span>© <span data-year></span> {BRAND} · converseroofer.com</span><span>Texas law prohibits roofers from paying or waiving insurance deductibles (Tex. Bus. &amp; Com. Code §27.02). We never do.</span></div>
    <p style="font-size:.8rem;color:#7f8ea3;margin:14px 0 0">Converse Roofer is a roofing contractor, not a licensed public adjuster. We do not adjust, negotiate or settle insurance claims on behalf of homeowners. We document roof damage and provide written repair estimates; all coverage decisions are made between you and your insurance company.</p>
  </div>
</footer>
<div class="call-bar"><a href="{TEL}">📞 Tap to call {PHONE} — free inspection</a></div>
<script src="{root}assets/js/config.js"></script>
<script src="{root}assets/js/main.js"></script>
</body>
</html>'''

def write(path, content):
    p = os.path.join(OUT, path); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w").write(content); print("wrote", path)

def page_hero(title, sub, root="", imgkey="storm2", crumbs=""):
    crumb_html = ('<div class="crumbs">' + crumbs + '</div>') if crumbs else ''
    return f'''<section class="hero small"><img class="bg" src="https://images.unsplash.com/photo-{IMGS[imgkey][0]}?auto=format&fit=crop&w=1800&q=60" alt="" onerror="this.onerror=null;this.src='{root}assets/img/ph-bg.svg'"><div class="shade"></div>
<div class="wrap"><div>{crumb_html}<h1>{title}</h1><p class="lead">{sub}</p></div></div></section>'''

# ---------------- HOME ----------------
home = f'''
<section class="hero">
  <img class="bg" src="https://images.unsplash.com/photo-{IMGS['hero'][0]}?auto=format&fit=crop&w=1800&q=60" alt="Converse roofing company completing a roof replacement on a brick home in Converse, TX" onerror="this.onerror=null;this.src='assets/img/ph-bg.svg'"><div class="shade"></div>
  <div class="wrap">
    <div>
      <span class="badge">Converse roofing · Storm response · Sept 11 hail</span>
      <h1 style="margin-top:14px">Converse Roofer: hail damage roof repair &amp; roof replacement in Converse, TX</h1>
      <p class="lead">Converse Roofer is the local Converse roofing company homeowners call after a storm. Golf-ball hail hit Converse, Kirby and Windcrest on September 11. Whether you need Converse roof repair, a full roof replacement, or a free roof inspection to find out which, we'll get on the roof, photograph it, and give you a straight answer.</p>
      <div class="cta"><a class="btn primary lg" href="{TEL}">📞 Call {PHONE}</a><a class="btn ghost lg" href="#inspection">Free Roof Inspection</a></div>
      <div class="trust"><span>Local Converse roofing company</span><span>Free roof inspections</span><span>Written estimates &amp; photo reports</span><span>Emergency roof repair</span></div>
      <div class="wx-mini" id="wx-mini"><span class="ic">🌤️</span><div><span class="t">—</span><small>Loading live Converse weather…</small></div></div>
    </div>
    <div id="inspection">{lead_form(compact=True, title="Free Roof Inspection in Converse, TX", sub="No cost, no pressure. A Converse roofer will check your roof, photograph any hail damage, and tell you honestly whether you need roof repair, roof replacement, or nothing at all.")}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="stats">
      <div class="stat"><b>1.75"+</b><span>Golf-ball hail confirmed over Kirby / Converse on 9/11</span></div>
      <div class="stat"><b>60 mph</b><span>Wind gusts in the NWS severe thunderstorm warning</span></div>
      <div class="stat"><b>8,000+</b><span>CPS Energy customers lost power that night</span></div>
      <div class="stat"><b>$0</b><span>Cost of a Converse Roofer inspection and photo report</span></div>
    </div>
    <p class="small" style="text-align:center;margin-top:12px">Storm figures from NWS Austin/San Antonio warnings and KENS 5 / KSAT reporting. <a href="hail-storm-september-11-2026.html">Read the full Converse hail storm report →</a></p>
  </div>
</section>

<section class="section alt">
  <div class="wrap">
    <span class="eyebrow">Converse roofing services</span>
    <h2>Roof repair, roof replacement and storm damage roofing in Converse, TX</h2>
    <p class="lead" style="max-width:760px">One local Converse roofing crew handles the inspection, the insurance paperwork, and the build. Converse roof repair for hail damage, roof leak repair, emergency roof repair and full roof replacement, all from one phone number.</p>
    <div class="grid c3" style="margin-top:28px">
      <div class="card"><div class="img">{img('roofer1')}</div><div class="body"><h3>Free roof inspection</h3><p>Searching "roof inspection near me" after the storm? A Converse Roofer inspector walks the roof, marks hail hits, checks vents, gutters, screens and AC fins, and hands you a photo report you keep whether or not you hire us for the Converse roof repair.</p><a class="more" href="contact.html">Book a free roof inspection →</a></div></div>
      <div class="card"><div class="img">{img('roof1')}</div><div class="body"><h3>Hail damage roof repair</h3><p>Converse roof repair for bruised shingles, cracked vents, dented flashing and lifted ridge cap. We document every hit so your hail damage roof repair is covered by insurance, not out of pocket.</p><a class="more" href="blog/what-golf-ball-hail-does-to-a-shingle-roof.html">What hail does to a roof →</a></div></div>
      <div class="card"><div class="img">{img('roof2')}</div><div class="body"><h3>Roof replacement in Converse, TX</h3><p>Full shingle roof replacement with architectural or Class 4 impact-resistant shingles, plus metal roofing. Tear-off, decking check, ice-and-water at valleys, new flashing, ridge vent and cleanup.</p><a class="more" href="gallery.html">See Converse roofing projects →</a></div></div>
      <div class="card"><div class="img">{img('rain')}</div><div class="body"><h3>Roof leak &amp; emergency roof repair</h3><p>Water coming in tonight? Call for emergency Converse roof repair and we'll tarp it first, then trace the leak to its source: flashing, pipe boots, valleys or storm damage.</p><a class="more" href="{TEL}">Call {PHONE} now →</a></div></div>
      <div class="card"><div class="img">{img('docs')}</div><div class="body"><h3>Storm damage documentation</h3><p>Every inspection produces a dated, slope-by-slope photo report and a written repair estimate for your Converse roof repair or replacement. It's yours to share with your insurance company or anyone else. Coverage decisions stay between you and your insurer.</p><a class="more" href="contact.html">Get a written estimate →</a></div></div>
      <div class="card"><div class="img">{img('gutter')}</div><div class="body"><h3>Gutters, metal &amp; more</h3><p>Seamless gutters, gutter guards, standing-seam metal roofing, skylights, ventilation and decking. From Converse roof repair to a new metal roof, if it's on a Converse home, Converse Roofer works on it.</p><a class="more" href="contact.html">Get a Converse roofing quote →</a></div></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <div>{img('hail1')}</div>
    <div>
      <span class="eyebrow">Why it matters now</span>
      <h2>Hail damage doesn't leak on day one. It leaks in February.</h2>
      <p>A golf-ball hailstone hitting a shingle at 60+ mph knocks the protective granules loose and bruises the asphalt mat underneath. The roof looks fine from the driveway. Six months of Texas sun later, those bruises crack, and the Converse roof repair you could have had insurance pay for becomes a leak you pay for yourself.</p>
      <ul class="checks">
        <li>Insurance policies have filing deadlines. Most Texas policies want the claim within a year of the storm, and some are shorter.</li>
        <li>Adjusters look for a pattern of fresh hits. The longer you wait, the harder the damage is to tie to the September 11 storm.</li>
        <li>A free roof inspection from a local Converse roofer gives you a dated photo record either way.</li>
      </ul>
      <a class="btn primary" href="contact.html">Schedule My Free Roof Inspection</a>
    </div>
  </div>
</section>

<section class="section dark">
  <div class="wrap">
    <span class="eyebrow">How Converse Roofer works</span>
    <h2>Four steps from "was that hail?" to a finished roof</h2>
    <div class="steps" style="margin-top:28px">
      <div class="step"><h3>Free roof inspection</h3><p>A Converse roofer comes out, gets on the roof, and photographs everything. You get the report the same day.</p></div>
      <div class="step"><h3>You decide what's next</h3><p>Pay for the repair directly, or contact your insurance company yourself with our photo report and written estimate in hand.</p></div>
      <div class="step"><h3>Your insurer inspects</h3><p>If you file, your insurance company sends its own adjuster. On request we can be on site to show them the damage we documented and answer questions about our repair estimate.</p></div>
      <div class="step"><h3>Build it right</h3><p>Tear-off, decking check, ice-and-water at valleys, new flashing, ridge vent, magnet sweep. Converse roofing done once, done right.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <span class="eyebrow">Recent Converse roofing work &amp; storm photos</span>
    <h2>Converse roof repair and roof replacement across the NE side of San Antonio</h2>
    <div class="gallery" style="margin-top:24px">
      <figure>{img('house2',w=800)}<figcaption>Converse roof replacement · architectural shingles</figcaption></figure>
      <figure>{img('roof1',w=800)}<figcaption>Hail-bruised shingles before Converse roof repair</figcaption></figure>
      <figure>{img('house3',w=800)}<figcaption>Converse roofing · roof replacement in Kirby</figcaption></figure>
      <figure>{img('storm1',w=800)}<figcaption>Sept 11 storm cell over Converse</figcaption></figure>
      <figure>{img('crew',w=800)}<figcaption>Converse Roofer crew on a tear-off</figcaption></figure>
      <figure>{img('house7',w=800)}<figcaption>Standing-seam metal roofing · Schertz</figcaption></figure>
      <figure>{img('hail2',w=800)}<figcaption>Hail and heavy rain, Sept 11</figcaption></figure>
      <figure>{img('house5',w=800)}<figcaption>Class 4 shingle roof replacement · Windcrest</figcaption></figure>
    </div>
    <p style="text-align:center;margin-top:20px"><a class="btn dark" href="gallery.html">View the full Converse roofing gallery</a></p>
  </div>
</section>

<section class="section alt">
  <div class="wrap narrow">
    <span class="eyebrow">Roofer near me · Converse, TX 78109</span>
    <h2>Looking for a roofer near you in Converse?</h2>
    <p>If you've been searching for a <strong>roofer near me</strong>, a <strong>roofing company in Converse, TX</strong>, or <strong>roof repair near me</strong> since the September 11 hail storm, here's the short version: Converse Roofer is a local Converse roofing contractor, not a storm-chasing crew from out of state. We do free roof inspections, hail damage roof repair, roof leak repair, emergency roof repair, and full roof replacement for homes in Converse, Kirby, Windcrest, Universal City, Live Oak, Schertz, Cibolo, Selma and St. Hedwig.</p>
      <h3>Converse roof repair</h3>
      <p>Not every hail-hit roof needs replacing. Converse roof repair covers bruised or cracked shingles on one slope, damaged pipe boots and vents, lifted ridge cap, and flashing that's letting water in. We tell you when a repair is the right call and when it isn't, and we put both in writing.</p>
      <h3>Roof replacement in Converse, TX</h3>
      <p>When the hit count in the adjuster's test squares says replacement, we handle the whole Converse roofing job: tear-off, decking, synthetic underlayment, ice-and-water shield, drip edge, starter, architectural or Class 4 impact-resistant shingles, ridge ventilation and a magnet sweep of the yard. Ask about the insurance discount for Class 4 shingles before you pick a product.</p>
      <h3>Emergency roof repair and roof leak repair</h3>
      <p>Active leak, missing shingles, tree limb through the decking? Call the number at the top of this page. Emergency Converse roof repair starts with a tarp the same day, then a proper fix once the weather clears.</p>
      <h3>Storm damage roofing</h3>
      <p>Hail damage Converse roof repair and wind damage repairs are most of what a Converse roofer does in a year like this one. We know what NWS reported for the September 11 storm, we photograph the collateral damage on vents, gutters and screens, and we put the repair cost in writing. If you use insurance, you pay your deductible and nothing more. Read our <a href="hail-storm-september-11-2026.html">Converse hail storm report</a> or our <a href="blog/how-to-file-a-hail-damage-claim-in-texas.html">homeowner's guide to Texas hail claims</a>.</p>
      <p class="small" style="margin-top:14px">Converse Roofer is a roofing contractor, not a public adjuster. We do not adjust, negotiate or settle insurance claims on your behalf. We document damage and provide a written repair estimate; coverage decisions are made between you and your insurance company.</p>
      <p><a class="btn primary" href="contact.html">Get a free Converse roofing quote</a></p>
  </div>
</section>

<section class="section alt" style="padding-top:0">
  <div class="wrap">
    <span class="eyebrow">From the Converse Roofer blog</span>
    <h2>Straight talk about hail, Converse roof repair and insurance</h2>
    <div class="grid c3" style="margin-top:24px">
      {{blog_cards_home}}
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap narrow faq">
    <span class="eyebrow">Questions Converse homeowners ask</span>
    <h2>Converse roofing FAQ</h2>
    <details open><summary>My roof looks fine from the ground. Do I still need a roof inspection?</summary><p>Yes. Hail bruising on asphalt shingles is almost impossible to see from the driveway. The tell-tale signs are on the roof itself: granule loss, soft spots in the mat, dented vents and dinged gutter lips. A free roof inspection from a Converse roofer settles it in 45 minutes.</p></details>
    <details><summary>How much does Converse roof repair cost?</summary><p>It depends on what's damaged. A pipe boot or a handful of shingles is a small job. Slope-wide hail damage is often something homeowners take to their insurance company, in which case your cost is usually the deductible. Converse Roofer gives you a written price for any Converse roof repair before work starts, free.</p></details>
    <details><summary>How much does a roof replacement cost in Converse?</summary><p>Roof size, pitch, layers to tear off, decking condition and the shingle you choose all drive the price. If your insurance company approves a replacement, your out-of-pocket cost is usually your deductible. Get a free inspection and we'll quote it either way.</p></details>
    <details><summary>Do you offer emergency roof repair in Converse?</summary><p>Yes. If you have an active leak or storm damage, call {PHONE}. We tarp first to stop the water, then schedule the permanent Converse roof repair.</p></details>
    <details><summary>Are you a local Converse roofer or a storm chaser?</summary><p>Local. Converse Roofer is based in Converse, TX, with a local number that still works after the out-of-town trucks leave. Ask for our insurance certificate and references; we expect it.</p></details>
    <details><summary>Will filing a claim raise my rates?</summary><p>In Texas, insurers generally can't surcharge you for a single weather-related claim that wasn't your fault. Rates across the whole area rise after big storms whether you file or not. Ask your agent to confirm how your specific policy handles "act of God" claims.</p></details>
    <details><summary>Can you cover my deductible?</summary><p>No, and any Converse roofing company that offers to is breaking Texas law (it's been a criminal offense since 2019). Your insurer can require proof you paid it. We'll help you understand your deductible up front so there are no surprises.</p></details>
    <details><summary>What if my insurance company says there's no damage?</summary><p>That decision is between you and your insurer. You keep our photo report and written estimate and can share them with your insurance company. For questions about your rights under a Texas policy, the Texas Department of Insurance consumer line is 800-252-3439, and licensed public adjusters and attorneys can represent you in a dispute. Converse Roofer is a roofing contractor and does not negotiate or settle claims.</p></details>
  </div>
</section>
'''

# ---------------- BLOG POSTS ----------------
posts = []
def post(slug, title, desc, date, minutes, imgkey, body, tags):
    posts.append(dict(slug=slug, title=title, desc=desc, date=date, minutes=minutes, img=imgkey, body=body, tags=tags))

post("what-golf-ball-hail-does-to-a-shingle-roof",
 "What Golf-Ball Hail Actually Does to a Shingle Roof (With Photos)",
 "Golf-ball hail hit Converse on September 11. Here's what 1.75-inch hail does to asphalt shingles, why the damage hides for months, and what an inspector looks for.",
 "September 14, 2026", 6, "roof1", f'''
<p>On the night of September 11, 2026, trained spotters reported 1.5-inch hail between Converse and Kirby, and photos posted from Converse neighborhoods showed stones in the 2 to 2.5-inch range. The National Weather Service warning that night called for golf-ball hail (1.75") and 60 mph gusts. That's well past the size that damages a standard asphalt roof.</p>
<p>Here's what happens to your shingles when a stone that size lands, and why the damage is so easy to miss.</p>

<h2>Hail sizes, in plain English</h2>
<table class="data"><tr><th>Common name</th><th>Diameter</th><th>Typical roof result</th></tr>
<tr><td>Dime / penny</td><td>0.70–0.75"</td><td>Granule scuffing on older or brittle roofs</td></tr>
<tr><td>Quarter</td><td>1.00"</td><td>NWS "severe" threshold. Bruising on 3-tab and aged shingles</td></tr>
<tr><td>Ping-pong ball</td><td>1.50"</td><td>Bruising on most architectural shingles, dented soft metals</td></tr>
<tr><td>Golf ball</td><td>1.75"</td><td>Widespread mat fractures, cracked vents, dented gutters, damaged window screens</td></tr>
<tr><td>Tennis / baseball</td><td>2.50–2.75"</td><td>Punctures through shingles, broken skylights, siding holes</td></tr></table>

<h2>The three layers of damage</h2>
<h3>1. Granule loss</h3>
<p>The colored ceramic granules on top of a shingle are its sunscreen. A hail strike blasts them off in a roughly round pattern, exposing the black asphalt underneath. You'll often find a pile of granules at the bottom of downspouts the morning after a storm.</p>
<h3>2. The bruise</h3>
<p>Press a thumb on a hail hit and it feels soft, like a bruise on an apple. The fiberglass mat under the asphalt has fractured. This is the damage that matters to an adjuster, and it's invisible from the ground.</p>
<h3>3. The crack</h3>
<p>Over the following months, sun and heat cycles open those fractures into cracks. Water gets to the decking. That's the leak that shows up in winter, long after everyone has forgotten the storm.</p>
<figure class="fig">{img('roof1', root='../')}<figcaption>Granule loss and bruising are what an inspector is looking for. The pattern of fresh hits helps tie the damage to a specific storm date.</figcaption></figure>

<h2>What else gets hit</h2>
<p>Adjusters look at "collateral" damage to confirm hail size and direction. On September 11 the storm moved southwest at 15 mph, so north- and east-facing slopes generally took the brunt. Check these:</p>
<ul>
<li><strong>Gutters and downspouts:</strong> dings along the top lip and outer face.</li>
<li><strong>Roof vents and turbines:</strong> soft aluminum dents easily and shows hail size clearly.</li>
<li><strong>AC condenser fins:</strong> flattened fins on the side facing the storm.</li>
<li><strong>Window screens and beading:</strong> torn screens, dented metal frames.</li>
<li><strong>Painted surfaces:</strong> chipped paint on fascia, decks and mailboxes.</li>
<li><strong>Vehicles:</strong> if your car was dented in the driveway, your roof was hit at least as hard.</li>
</ul>

<div class="callout"><strong>Don't get on the roof yourself.</strong> Hail-damaged shingles are slippery, and walking on them can make bruising worse. Call us and we'll do it for free with a harness and a camera.</div>

<h2>Does every hail-hit roof need replacing?</h2>
<p>No. A newer Class 4 impact-resistant roof may shrug off golf-ball hail with cosmetic marks only. A 3-tab roof from 2012 probably won't. The honest answer comes from counting hits in a 10x10 test square on each slope, which is exactly what your adjuster will do. We count first, then tell you whether it's worth filing.</p>
<p><a href="../contact.html">Book a free inspection</a> or call <a href="{TEL}">{PHONE}</a>. We serve Converse, Kirby, Windcrest, Universal City, Live Oak, Schertz and Cibolo.</p>
''', ["Hail damage","Inspections"])

post("how-to-file-a-hail-damage-claim-in-texas",
 "How to File a Hail Damage Roof Claim in Texas: Step by Step",
 "A homeowner's guide to filing a hail claim in Texas after the September 11 storm: deadlines, what to say, the adjuster visit, deductibles, and what to do if you're denied.",
 "September 13, 2026", 8, "docs", f'''
<p>If the September 11 storm hit your house, the claim process is less scary than it sounds. Here's how it generally goes, in order, with the Texas-specific rules that matter.</p>
<div class="callout blue"><strong>General information, not claim advice.</strong> Converse Roofer is a roofing contractor, not a licensed public adjuster. We inspect roofs, document damage and provide written repair estimates. We do not file, negotiate or settle insurance claims for homeowners. For help with a claim itself, contact your agent, a licensed public adjuster, or the Texas Department of Insurance.</div>

<h2>Step 1: Get the roof inspected before you call</h2>
<p>Calling your insurer before you know what's up there can work against you. A claim with no damage found still goes on your record. A free inspection from a local roofer gives you photos, a hit count per slope, and a written repair estimate, so you can make your own decision about filing.</p>

<h2>Step 2: Read your policy (the two things that matter)</h2>
<ul>
<li><strong>Deductible.</strong> Many Texas policies now carry a percentage wind/hail deductible, often 1% to 2% of the dwelling coverage. On a $300,000 home a 2% deductible is $6,000. Know this number before you file.</li>
<li><strong>RCV vs. ACV.</strong> Replacement Cost Value pays what a new roof costs (part up front, the "depreciation" after the work is done). Actual Cash Value pays a depreciated amount and you cover the gap. Some carriers have quietly moved roofs to ACV schedules. Check.</li>
</ul>

<h2>Step 3: File the claim</h2>
<p>Call the claims number on your policy or file through the app. Keep it factual: "My roof was damaged by hail in the September 11, 2026 storm. I've had it inspected and there is hail damage on multiple slopes." Give the date of loss as <strong>September 11, 2026</strong>. Write down the claim number.</p>
<div class="callout blue"><strong>Deadlines.</strong> Texas policies typically require "prompt" notice and many set a one-year filing window from the date of loss. Some are shorter. Filing a few weeks after a storm is fine. Filing 14 months later usually isn't.</div>

<h2>Step 4: The adjuster visit</h2>
<p>Your carrier assigns an adjuster who'll schedule a roof visit, usually within one to three weeks after a big regional storm. You can ask your roofer to be present so the adjuster can see the damage documented in the inspection report and ask questions about the repair estimate. The adjuster, not the roofer, decides what the policy covers.</p>
<figure class="fig">{img('handshake', root='../')}<figcaption>A written repair estimate and dated photos are the two documents most homeowners share with their insurance company.</figcaption></figure>

<h2>Step 5: The estimate and the first check</h2>
<p>You'll receive a scope of work (usually an Xactimate printout) and, on an RCV policy, a first check for the ACV amount minus your deductible. Compare it with your contractor's written estimate. Items that are sometimes left off an initial estimate include drip edge, ice-and-water shield in valleys, starter strip, ridge cap, code-required ventilation, and steep or high-roof labor. If something you need is missing, you can ask your insurance company about it directly; your contractor can supply the estimate and photos you'll want to reference.</p>

<h2>Step 6: The work, and the depreciation check</h2>
<p>Once the roof is done we send the carrier the invoice and completion photos, and they release the recoverable depreciation. You pay your deductible to us directly, and that's it.</p>

<h2>Texas rules every homeowner should know</h2>
<ul>
<li><strong>Deductible waivers are illegal.</strong> Since September 2019, a contractor who offers to pay, waive or "absorb" your deductible is committing a Class B misdemeanor, and your insurer can require proof you paid it. Walk away from anyone who offers.</li>
<li><strong>No state roofing license.</strong> Texas doesn't license roofers. That's why you check for general liability insurance, a local physical presence, and references you can actually call.</li>
<li><strong>You choose your contractor.</strong> Your insurer can suggest a "preferred vendor" but can't require you to use one.</li>
<li><strong>Prompt payment.</strong> Texas Insurance Code Chapter 542 sets deadlines for carriers to acknowledge, investigate and pay claims. Slow-walking has consequences.</li>
<li><strong>Help if you're stuck.</strong> The Texas Department of Insurance consumer help line is <strong>800-252-3439</strong>.</li>
</ul>

<h2>If the claim is denied or underpaid</h2>
<ol>
<li>Ask for the denial in writing with the adjuster's photos.</li>
<li>Request a re-inspection with a different adjuster. Bring your own photo report.</li>
<li>Ask your agent whether your policy has an <strong>appraisal clause</strong> and how it works. A licensed public adjuster or an attorney can represent you in a dispute; a roofing contractor cannot.</li>
<li>File a complaint with TDI if the carrier isn't following the process.</li>
</ol>
<p>Whatever route you take, the roof still needs a written estimate and someone to fix it. <a href="../contact.html">Book a free inspection</a> or call <a href="{TEL}">{PHONE}</a>.</p>
''', ["Insurance","Guides"])

post("7-questions-before-you-sign-with-a-roofer-after-a-storm",
 "7 Questions to Ask Before You Sign With a Roofer After a Hail Storm",
 "Out-of-town crews are already knocking doors in Converse and Kirby after the 9/11 hail storm. Ask these seven questions before you sign anything.",
 "September 15, 2026", 5, "handshake", f'''
<p>Within 48 hours of the September 11 storm there were trucks with out-of-state plates working the streets around Converse and Kirby. Some of those companies are fine. Some will be gone by Thanksgiving, and your warranty goes with them. Here's how to tell the difference in a five-minute conversation.</p>

<h2>1. "Where's your office?"</h2>
<p>Not a PO box, not a "regional headquarters" in Dallas. Where do you go if the roof leaks in March? A local roofer has a Converse or San Antonio address, a local phone number, and a truck you'll see at the H-E-B on FM 78.</p>

<h2>2. "Can I see your general liability insurance certificate?"</h2>
<p>Texas doesn't license roofers, so insurance is the paper that matters. Ask for the certificate and call the agent listed on it. If a worker gets hurt on your roof and the company isn't insured, that can become your problem.</p>

<h2>3. "Who's actually going to be on my roof?"</h2>
<p>Many storm companies are sales organizations that sub everything out to whoever's available. Ask who the crew lead is, how long they've worked with the company, and whether a supervisor will be on site.</p>

<h2>4. "What happens with my deductible?"</h2>
<p>The only correct answer is "you pay it." Anyone offering to waive it, "eat" it, or hand you a rebate that happens to equal it is offering to commit insurance fraud with your name on the claim. It's been a criminal offense in Texas since 2019.</p>
<div class="callout"><strong>Red flag phrases:</strong> "free roof," "we'll handle the deductible," "sign now so we can hold your spot," "we're only in the neighborhood this week."</div>

<h2>5. "What's in the contract, and can I take it home?"</h2>
<p>A fair contract spells out the shingle brand and line, underlayment, ice-and-water locations, ventilation, decking replacement price per sheet, cleanup, and the payment schedule. You should never be asked to sign before the adjuster has even come out. Watch for "assignment of benefits" language that hands control of your claim to the contractor.</p>

<h2>6. "What warranty do you offer, and who backs it?"</h2>
<p>There are two: the manufacturer's material warranty (30 years to lifetime on most architectural shingles) and the contractor's workmanship warranty. The second one is only as good as the company's ability to answer the phone in five years.</p>

<h2>7. "Can I talk to three customers from the last year?"</h2>
<p>Not testimonials on a website. Phone numbers. A roofer who's proud of their work has no trouble producing them.</p>
<figure class="fig">{img('crew', root='../')}<figcaption>Ask who will be on your roof and whether a supervisor stays on site. It's a fair question and a good roofer expects it.</figcaption></figure>

<h2>What we'll tell you if you ask us</h2>
<p>We're based in Converse. We're insured and we'll send the certificate before we ever set foot on your roof. You pay your deductible, we never touch it. You get a written estimate before you sign, and you sign nothing until you've decided how you're paying for the work. <a href="../contact.html">Book a free inspection</a> or call <a href="{TEL}">{PHONE}</a>.</p>
''', ["Choosing a roofer","Insurance"])

post("9-signs-your-roof-took-hail-damage",
 "Hail Hit Your Neighborhood? 9 Signs to Check From the Ground Today",
 "You don't need a ladder to spot most of these. Nine ground-level signs your Converse-area roof took hail damage on September 11, and what to do next.",
 "September 12, 2026", 4, "hail2", f'''
<p>You can't safely inspect shingles from the ground, but you can absolutely tell whether it's worth having someone come out. Walk around your house with your phone and check these nine things. Photograph anything you find; the timestamp is useful later.</p>

<ol>
<li><strong>Granules in the downspout splash blocks.</strong> Black or colored sand piled where the downspouts drain. Fresh granule loss is the first sign of hail impact.</li>
<li><strong>Dented gutters.</strong> Run your hand along the top lip of the gutter. Round dents you can feel mean stones big enough to bruise shingles.</li>
<li><strong>Dinged downspouts and gutter end caps.</strong> Especially on the north and east sides, where the September 11 storm was coming from.</li>
<li><strong>Torn or dimpled window screens.</strong> Look for small tears and dents in the aluminum frame.</li>
<li><strong>Chipped paint on fascia, deck rails and the mailbox.</strong> Hail knocks small round chips out of painted surfaces.</li>
<li><strong>Flattened fins on the AC condenser.</strong> The side facing the storm will look combed flat. This is also worth mentioning to your insurer.</li>
<li><strong>Dents in soft-metal roof vents</strong> that you can see from the yard with a zoom lens or binoculars. Aluminum turtle vents show every hit.</li>
<li><strong>Shingle pieces or tabs in the yard.</strong> With 60 mph gusts, some roofs lost tabs outright.</li>
<li><strong>Your car.</strong> If your vehicle was outside and has dents, your roof took the same hail.</li>
</ol>
<figure class="fig">{img('gutter', root='../')}<figcaption>Gutters and roof-edge metal record hail size better than anything else you can see from the ground.</figcaption></figure>

<h2>Found two or more? Get it inspected.</h2>
<p>Two or more of these signs almost always means shingle damage on the roof itself. That doesn't automatically mean you need a new roof, but it means the roof needs eyes on it, and the sooner the better while the damage is clearly fresh.</p>
<p>Our inspection is free and comes with a photo report you keep regardless. <a href="../contact.html">Request one here</a> or call <a href="{TEL}">{PHONE}</a>.</p>
''', ["Hail damage","Checklists"])

post("class-4-impact-resistant-shingles-bexar-county",
 "Class 4 Impact-Resistant Shingles: Worth It in Bexar County?",
 "Bexar County gets hail nearly every year. Here's what Class 4 shingles are, what they cost extra, the insurance discount, and when they're worth it on a Converse home.",
 "September 10, 2026", 6, "house5", f'''
<p>If you're replacing a roof after a hail claim, you'll be asked whether you want to upgrade to Class 4 impact-resistant shingles. Here's a straight answer on what you're buying.</p>

<h2>What "Class 4" means</h2>
<p>UL 2218 is a test where a 2-inch steel ball is dropped from 20 feet onto a shingle, twice in the same spot. If the shingle doesn't crack, it passes Class 4, the highest rating. A 2-inch steel ball hits harder than a 2-inch hailstone, so it's a conservative test. Class 4 shingles use a more flexible asphalt blend (often SBS-modified) and sometimes a reinforced mat.</p>

<h2>What they cost</h2>
<p>Roughly 10 to 25 percent more for materials than a standard architectural shingle from the same manufacturer. On a typical Converse roof that's usually a few hundred to a couple thousand dollars over the standard product. If you're on an insurance replacement, that upgrade cost is yours, not the carrier's.</p>

<h2>The insurance discount</h2>
<p>Most Texas carriers offer a premium discount for a documented Class 4 roof, commonly in the 5 to 30 percent range on the wind/hail portion of your premium. Ask your agent for the exact figure before you decide. On many policies the discount pays back the upgrade within a few years.</p>
<div class="callout blue"><strong>Read the fine print.</strong> Some carriers pair the discount with a "cosmetic damage exclusion," meaning they won't pay to replace a Class 4 roof that's dented but not leaking. Make sure you know which you're getting.</div>

<h2>When it's worth it</h2>
<ul>
<li>You plan to stay in the house more than five years.</li>
<li>Your roof has been replaced for hail more than once already.</li>
<li>Your carrier offers a meaningful discount without a cosmetic exclusion.</li>
</ul>
<h2>When it's not</h2>
<ul>
<li>You're selling within a couple of years.</li>
<li>Your carrier's discount is small or comes with a cosmetic exclusion you're not comfortable with.</li>
</ul>
<figure class="fig">{img('house5', root='../')}<figcaption>Class 4 shingles look the same as standard architectural shingles. The difference is what happens underneath when a stone hits.</figcaption></figure>
<p>We install Class 4 lines from the major manufacturers and will price both options side by side on your estimate. <a href="../contact.html">Get a quote</a> or call <a href="{TEL}">{PHONE}</a>.</p>
''', ["Materials","Guides"])

def blog_card(p, root=""):
    return f'''<div class="card"><div class="img"><a href="{root}blog/{p['slug']}.html">{img(p['img'], root=root, w=800)}</a></div><div class="body"><div class="meta">{p['date']} · {p['minutes']} min read</div><h3><a href="{root}blog/{p['slug']}.html" style="color:inherit;text-decoration:none">{p['title']}</a></h3><p>{p['desc']}</p><a class="more" href="{root}blog/{p['slug']}.html">Read more →</a></div></div>'''

blog_cards_home = "".join(blog_card(p) for p in posts[:3])
home = home.replace("{blog_cards_home}", blog_cards_home)
write("index.html", layout("Converse Roofer | Converse Roofing, Roof Repair & Roof Replacement in Converse, TX",
  "Converse Roofer: local Converse roofing company for hail damage roof repair, roof replacement, roof leak and emergency roof repair. Free roof inspections after the Sept 11, 2026 hail storm. Call 832-503-5866.",
  home, root="", active="index.html", canonical=""))

# blog index
blog_index = page_hero("Roofing Blog", "Plain-English guides on hail damage, roof repair and picking a roofer, written for Converse and NE San Antonio homeowners.", root="../", imgkey="storm3", crumbs='<a href="../index.html">Home</a> › Blog') + f'''
<section class="section"><div class="wrap"><div class="grid c3">{"".join(blog_card(p, root="../") for p in posts)}</div></div></section>
<section class="section alt"><div class="wrap narrow">{lead_form(root="../", title="Have a roof question?", sub="Ask us anything. If you'd rather we just come look, that's free too.")}</div></section>'''
write("blog/index.html", layout("Roofing Blog | Hail, Insurance & Roof Guides | Converse Roofer",
  "Guides on hail damage, roof repair and choosing a roofer, from Converse Roofer in Converse, TX.", blog_index, root="../", active="blog/index.html", canonical="blog/"))

for i,p in enumerate(posts):
    others = [q for q in posts if q is not p][:3]
    body = page_hero(p['title'], p['desc'], root="../", imgkey=p['img'], crumbs='<a href="../index.html">Home</a> › <a href="index.html">Blog</a>') + f'''
<section class="section"><div class="wrap"><article class="article">
<div class="meta">{p['date']} · {p['minutes']} min read · {" · ".join(p['tags'])}</div>
{p['body']}
<div class="hr"></div>
<div class="callout"><strong>Free hail inspection in Converse, Kirby, Windcrest &amp; NE San Antonio</strong>Call or text <a href="{TEL}">{PHONE}</a> or <a href="../contact.html">request online</a>. Same-day photo report, no obligation.</div>
</article></div></section>
<section class="section alt"><div class="wrap"><h2>More from the blog</h2><div class="grid c3">{"".join(blog_card(q, root="../") for q in others)}</div></div></section>'''
    schema = f'''<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BlogPosting","headline":"{html.escape(p['title'])}","description":"{html.escape(p['desc'])}","datePublished":"2026-09-{p['date'].split()[1].strip(',').zfill(2)}","author":{{"@type":"Organization","name":"{BRAND}"}},"publisher":{{"@type":"Organization","name":"{BRAND}"}},"mainEntityOfPage":"{DOMAIN}/blog/{p['slug']}.html"}}</script>'''
    write(f"blog/{p['slug']}.html", layout(f"{p['title']} | Converse Roofer Blog", p['desc'], body, root="../", active="blog/index.html", canonical=f"blog/{p['slug']}.html", schema=schema))

# ---------------- HAIL STORM REPORT ----------------
storm = page_hero("September 11, 2026 Hail Storm: Converse &amp; Kirby Damage Report",
 "Golf-ball hail, 60 mph gusts and 8,000+ power outages on the northeast side of San Antonio. What fell, where, and what it means for your roof.",
 imgkey="storm1", crumbs='<a href="index.html">Home</a> › 9/11 Hail Storm') + f'''
<section class="section"><div class="wrap">
  <div class="stats">
    <div class="stat"><b>Fri 9/11</b><span>~10:00–11:15 PM CDT</span></div>
    <div class="stat"><b>1.75"</b><span>Golf-ball hail in NWS warning; 2–2.5" stones photographed in Converse</span></div>
    <div class="stat"><b>60 mph</b><span>Wind gusts, storm moving SW at 15 mph</span></div>
    <div class="stat"><b>8,000+</b><span>CPS Energy outages, ~4,600 around Kirby &amp; Converse</span></div>
  </div>
</div></section>

<section class="section alt"><div class="wrap"><article class="article">
<h2>What happened</h2>
<p>Late on Friday, September 11, 2026, a severe thunderstorm formed along a front and dropped into the northeast suburbs of San Antonio. The National Weather Service office in Austin/San Antonio issued a Severe Thunderstorm Warning at <strong>10:12 PM CDT</strong> for a storm located over Kirby, near Converse, moving southwest at 15 mph, with golf-ball size hail and 60 mph wind gusts. Follow-up warnings at 10:26 PM and 10:34 PM tracked the storm toward China Grove and the south side, with hail sizes stepping down to quarter and then nickel size as it moved away from our area.</p>
<p>Trained spotters reported hail up to 1.5 inches between Converse and Kirby. Photos shared by residents on social media and KSAT Connect showed stones in the 2 to 2.5-inch range in Converse neighborhoods, alongside cracked windshields and broken car windows. Dime to golf-ball hail was reported in the Paloma subdivision. Pockets of the storm produced more than 2 inches of rain, with frequent cloud-to-ground lightning and localized street flooding.</p>
<p>CPS Energy reported more than 8,000 customers without power that night, most of them on the east side. About 4,600 of those outages were concentrated around Kirby and Converse.</p>

<div class="two-img">{img('hail1')}{img('storm4')}</div>

<h2>Areas in the warning polygon</h2>
<p>The NWS warnings listed these communities as impacted:</p>
<div class="areas" style="margin-bottom:1.5em"><span>Converse</span><span>Kirby</span><span>Windcrest</span><span>Universal City</span><span>Live Oak</span><span>Randolph AFB</span><span>Schertz</span><span>Cibolo</span><span>Alamo Heights</span><span>Terrell Hills</span><span>Olmos Park</span><span>St. Hedwig</span><span>China Grove</span><span>Elmendorf</span><span>Zuehl</span><span>Sandy Oaks</span><span>Calaveras Lake</span><span>Stinson Airport area</span><span>Lackland AFB</span><span>San Antonio</span></div>
<p>The heaviest, largest hail was in the first warning box, centered on <strong>Kirby and Converse</strong>. If you live between Loop 1604, I-10 and FM 78, your roof was almost certainly under the core of the storm.</p>

<h2>Timeline</h2>
<table class="data">
<tr><th>Time (CDT)</th><th>Event</th></tr>
<tr><td>~10:05 PM</td><td>Special Weather Statement issued ahead of the storm</td></tr>
<tr><td>10:12 PM</td><td>Severe Thunderstorm Warning: storm over Kirby near Converse, golf-ball hail, 60 mph gusts, moving SW 15 mph</td></tr>
<tr><td>10:26 PM</td><td>Warning update: storm near China Grove, 7 mi NE of Stinson Municipal Airport; quarter-size hail, 60 mph gusts; valid until 11:15 PM</td></tr>
<tr><td>10:34 PM</td><td>Warning update: nickel-size hail, 60 mph gusts, continuing southwest</td></tr>
<tr><td>Overnight</td><td>CPS Energy outages peak above 8,000; crews restore power through Saturday</td></tr>
<tr><td>Sat 9/12</td><td>KSAT publishes viewer hail photos and video; roofers begin canvassing Converse and Kirby</td></tr>
</table>

<h2>What golf-ball hail means for your roof</h2>
<p>The NWS "severe" threshold is 1-inch hail. Converse got 1.75 inches and larger, driven by 60 mph wind. That combination:</p>
<ul>
<li>Bruises and fractures the mat on standard 3-tab and most architectural asphalt shingles.</li>
<li>Dents aluminum vents, gutters, downspouts and AC fins, which adjusters use to confirm the storm.</li>
<li>Tears window screens and chips paint on north- and east-facing surfaces.</li>
<li>Cracks skylights and damages solar panel frames.</li>
</ul>
<p>Because the storm moved southwest, north- and east-facing roof slopes generally took the direct hits. A roof can be badly damaged on one or two slopes and look untouched from the street.</p>
<figure class="fig">{img('roof1')}<figcaption>Typical hail bruising on an asphalt shingle. This is the damage adjusters count in a 10x10 test square on each slope.</figcaption></figure>

<h2>What to do this week</h2>
<ol>
<li><strong>Photograph what you can see from the ground</strong>: dented gutters, torn screens, chipped paint, granules at downspouts, car damage. Timestamps matter.</li>
<li><strong>Get a free roof inspection</strong> from a local roofer before you call your insurer. You'll know what the roof actually needs, and you'll have a dated photo report and written estimate.</li>
<li><strong>If there's damage, decide how you'll pay for it.</strong> If you contact your insurance company, the date of loss is September 11, 2026. <a href="blog/how-to-file-a-hail-damage-claim-in-texas.html">Here's a homeowner's guide to the process</a>.</li>
<li><strong>Be careful who you sign with.</strong> Out-of-town crews are already door-knocking. <a href="blog/7-questions-before-you-sign-with-a-roofer-after-a-storm.html">Seven questions to ask first</a>.</li>
<li><strong>Never let anyone "cover" your deductible.</strong> It's illegal in Texas and can void your claim.</li>
</ol>

<h2>Sources</h2>
<ul class="small">
<li>NWS Austin/San Antonio Severe Thunderstorm Warnings, September 11, 2026, 10:12 PM, 10:26 PM and 10:34 PM CDT</li>
<li><a href="https://www.kens5.com/article/weather/severe-weather/san-antonio-thunderstorm-hail-cps-power-outage/273-ebff8fdf-c42a-4a95-b500-1f970c7d45bc" rel="noopener" target="_blank">KENS 5: Power outages in San Antonio area amid Friday night storms</a></li>
<li><a href="https://www.ksat.com/weather/2026/09/12/viewers-share-photos-videos-of-hailstones-and-rain-across-san-antonio-on-ksat-connect/" rel="noopener" target="_blank">KSAT: Viewers share photos, videos of hailstones and rain across San Antonio</a></li>
<li><a href="https://www.stormersite.com/hail_reports/converse_texas/all" rel="noopener" target="_blank">Stormersite hail reports, Converse, TX</a></li>
</ul>
<p class="small">Storm photos on this page are representative images. Add your own photos from Converse neighborhoods to the gallery as they come in.</p>
</article></div></section>

<section class="section"><div class="wrap split">
  <div>{lead_form(title="Was your house under this storm?", sub="Tell us your address and we'll check it against the warning polygon and come take a look. Free, with photos.")}</div>
  <div>
    <span class="eyebrow">Why homeowners call us first</span>
    <h2>Local, on the roof, and honest about what we find</h2>
    <ul class="checks">
      <li>Based in Converse. We were here before the storm and we'll be here after the out-of-town trucks leave.</li>
      <li>Every inspection comes with a photo report and written estimate you keep, whatever you decide to do.</li>
      <li>We don't adjust or negotiate insurance claims. We document the damage and fix the roof.</li>
      <li>We never touch your deductible. Ever.</li>
    </ul>
    <a class="btn primary lg" href="{TEL}">📞 {PHONE}</a>
  </div>
</div></section>'''
write("hail-storm-september-11-2026.html", layout("September 11, 2026 Hail Storm Report: Converse & Kirby, TX | Converse Roofer",
  "Full report on the Sept 11, 2026 hail storm: golf-ball hail over Converse and Kirby, 60 mph gusts, 8,000+ CPS outages, NWS timeline, and what it means for your roof.",
  storm, active="hail-storm-september-11-2026.html", canonical="hail-storm-september-11-2026.html"))

# ---------------- WEATHER ----------------
weather = page_hero("Converse, TX Live Weather &amp; Storm Alerts", "Current conditions, 7-day forecast, hail and severe-storm risk, and active National Weather Service alerts for Converse and the northeast side of San Antonio.", imgkey="storm2", crumbs='<a href="index.html">Home</a> › Weather') + f'''
<section class="section"><div class="wrap">
  <span class="eyebrow">Active alerts</span>
  <h2>NWS alerts for Converse</h2>
  <div id="wx-alerts"><div class="alert info"><h4>Checking for alerts…</h4><p>Pulling active alerts from the National Weather Service.</p></div></div>
</div></section>

<section class="section alt"><div class="wrap">
  <div class="wx-now">
    <div class="wx-card">
      <span class="eyebrow">Right now · Converse, TX</span>
      <div class="wx-big"><span class="ic" id="wx-icon">🌡️</span><div><div class="t"><span id="wx-temp">—</span></div><div id="wx-desc">Loading…</div></div></div>
      <div class="wx-kv">
        <div><span>Feels like</span><b id="wx-feels">—</b></div>
        <div><span>Humidity</span><b id="wx-hum">—</b></div>
        <div><span>Wind</span><b id="wx-wind">—</b></div>
        <div><span>Gusts</span><b id="wx-gust">—</b></div>
        <div><span>Precip (last hr)</span><b id="wx-precip">—</b></div>
        <div><span>Updated</span><b id="wx-updated">—</b></div>
      </div>
    </div>
    <div class="wx-card">
      <span class="eyebrow">Hail &amp; severe storm risk · next 48 hours</span>
      <p><span class="risk-pill low" id="wx-risk">Calculating…</span></p>
      <p>Risk is estimated from the forecast weather code, rain probability and peak gusts. It's a homeowner's heads-up, not an official outlook. For official severe weather outlooks see the <a href="https://www.spc.noaa.gov/products/outlook/" target="_blank" rel="noopener">Storm Prediction Center</a> and <a href="https://www.weather.gov/ewx/" target="_blank" rel="noopener">NWS Austin/San Antonio</a>.</p>
      <h3 style="margin-top:14px">If hail is in the forecast</h3>
      <ul class="checks" style="font-size:.95rem">
        <li>Move vehicles into the garage or under cover.</li>
        <li>Bring in patio cushions and cover the AC condenser if you can do it safely.</li>
        <li>Close blinds and stay away from windows during the storm.</li>
        <li>Afterward, photograph hail on the ground next to a coin or ruler before it melts.</li>
      </ul>
    </div>
  </div>
  <h3 style="margin-top:32px">7-day forecast</h3>
  <p class="wx-note">Days with thunderstorm or strong-gust potential are highlighted.</p>
  <div class="wx-days" id="wx-days"><div class="wx-day">Loading…</div></div>
  <p class="wx-note" style="margin-top:10px">Weather data from <a href="https://open-meteo.com/" target="_blank" rel="noopener">Open-Meteo</a>. Alerts from the <a href="https://www.weather.gov/" target="_blank" rel="noopener">National Weather Service</a>. Coordinates: 29.518, -98.316 (Converse, TX). Times are Central.</p>
</div></section>

<section class="section"><div class="wrap"><article class="article">
<h2>Hail season on the northeast side</h2>
<p>Bexar County sits on the southern edge of Texas hail alley. Our biggest hail months are April through June, but as the <a href="hail-storm-september-11-2026.html">September 11, 2026 storm</a> proved, a single front in early fall can drop golf-ball stones with no warning beyond a few minutes. The northeast side of San Antonio, from Windcrest out through Converse, Kirby, Universal City and Schertz, takes a disproportionate share of those storms because of how cells track off the Hill Country and along I-35 and I-10.</p>
<h3>Recent severe weather affecting Converse and Kirby</h3>
<table class="data">
<tr><th>Date</th><th>Event</th><th>Roof impact</th></tr>
<tr><td>Sept 11, 2026</td><td>Severe thunderstorm, golf-ball hail (2–2.5" photographed), 60 mph gusts, 8,000+ outages</td><td>Widespread shingle bruising, dented metal, screen damage across Converse and Kirby</td></tr>
<tr><td>Late May 2026</td><td>Damaging wind storm in Kirby: downed trees, a truck pushed several houses down the street</td><td>Lifted and missing shingles, ridge cap damage, tree impacts</td></tr>
</table>
<p class="small">Want your street checked against a specific storm date? <a href="contact.html">Send us the address</a> and we'll pull the radar and warning history for that day.</p>
</article></div></section>
<script src="assets/js/weather.js" defer></script>'''
write("weather.html", layout("Converse, TX Weather, Hail Risk & NWS Alerts | Converse Roofer",
  "Live weather for Converse, TX: current conditions, 7-day forecast, hail and severe storm risk, and active NWS alerts. Updated automatically.",
  weather, active="weather.html", canonical="weather.html"))
# home page also needs weather.js
idx = open(os.path.join(OUT,"index.html")).read().replace('<script src="assets/js/main.js"></script>', '<script src="assets/js/main.js"></script>\n<script src="assets/js/weather.js" defer></script>')
open(os.path.join(OUT,"index.html"),"w").write(idx)

# ---------------- GALLERY ----------------
gal = [("house2","Full replacement, architectural shingles · Converse",""),("roof1","Hail bruising on a 12-year-old roof · Kirby",""),("storm1","The Sept 11 storm cell over the NE side","tall"),
 ("house3","Complete tear-off and re-roof · Windcrest",""),("crew","Crew on a Saturday tear-off",""),("house7","Standing-seam metal · Schertz",""),("hail1","Hail on the ground after the storm",""),
 ("house5","Class 4 impact-resistant shingles · Universal City","tall"),("gutter","New seamless gutters and drip edge",""),("house4","Craftsman re-roof with ridge vent",""),("storm3","Storm building west of Converse",""),
 ("roofer1","Inspection: marking hits in a test square",""),("house8","Multi-slope replacement · Live Oak",""),("ladder","Set up for an inspection",""),("house9","Composition roof · Cibolo",""),("hail2","Hail and heavy rain on the 11th",""),
 ("house6","Finished at dusk · Converse",""),("roofer2","Walking the estimate with a homeowner",""),("house10","Low-slope re-roof · St. Hedwig",""),("house11","Tile roof repair · NE San Antonio",""),("storm2","Storm clouds over FM 78",""),("house1","Hip roof replacement · Kirby","")]
gallery = page_hero("Photos: Our Work &amp; the Storms Behind It", "Roof replacements, repairs, inspections and storm shots from Converse, Kirby, Windcrest, Universal City, Schertz and around the northeast side.", imgkey="house2", crumbs='<a href="index.html">Home</a> › Photos') + f'''
<section class="section"><div class="wrap">
  <div class="gallery">{"".join(f'<figure class="{c}">{img(k, w=900)}<figcaption>{t}</figcaption></figure>' for k,t,c in gal)}</div>
  <p class="small" style="margin-top:18px">Gallery photos are placeholders until your own job and storm photos are added. Drop images into <code>assets/img/</code> and update the captions in <code>gallery.html</code>.</p>
</div></section>
<section class="section alt"><div class="wrap split">
  <div>
    <span class="eyebrow">Send us your storm photos</span>
    <h2>Got hail photos from September 11?</h2>
    <p>Text them to <a href="{SMS}">{PHONE}</a> with your street name. We're building a block-by-block map of where the biggest stones fell in Converse and Kirby, and it helps every neighbor when the hail size is documented.</p>
    <a class="btn primary" href="{SMS}">💬 Text photos to {PHONE}</a>
  </div>
  <div>{img('storm4')}</div>
</div></section>'''
write("gallery.html", layout("Photo Gallery: Roof Replacements & Storm Damage | Converse Roofer",
  "Photos of roof replacements, hail damage inspections and storms across Converse, Kirby, Windcrest and NE San Antonio.", gallery, active="gallery.html", canonical="gallery.html"))

# ---------------- ABOUT ----------------
about = page_hero("About Converse Roofer", "A local storm-restoration roofing company based in Converse, Texas. We handle the inspection, the insurance conversation and the build, and we answer the phone afterward.", imgkey="team", crumbs='<a href="index.html">Home</a> › About Us') + f'''
<section class="section"><div class="wrap split">
  <div>{img('roofer2')}</div>
  <div>
    <span class="eyebrow">Who we are</span>
    <h2>Roofers from the neighborhood, not from the storm</h2>
    <p>Every big hail storm brings a wave of out-of-town companies to Converse. They set up in a hotel off I-10, knock every door in the subdivision, and leave when the claims dry up. When the roof leaks two years later, the number's disconnected.</p>
    <p>We started Converse Roofer to be the other option: a company with a Converse address, a local phone number, and a reputation on the same streets we live on. We specialize in hail and wind damage because that's what this part of Bexar County gets, and we've built our whole process around giving homeowners clear documentation and a fair written price, so nobody gets taken advantage of.</p>
    <a class="btn primary" href="{TEL}">📞 Call {PHONE}</a>
  </div>
</div></section>

<section class="section alt"><div class="wrap">
  <span class="eyebrow">How we work</span>
  <h2>What you can expect from us</h2>
  <div class="grid c3" style="margin-top:24px">
    <div class="icon-card"><div class="ic">📷</div><h3>Photos of everything</h3><p>Every inspection is documented slope by slope. You get the report whether you hire us or not.</p></div>
    <div class="icon-card"><div class="ic">🤝</div><h3>No pressure, no gimmicks</h3><p>We don't ask you to sign before you've decided how you're paying for the work, and we don't do "free roof" pitches. You pay your deductible, we never touch it.</p></div>
    <div class="icon-card"><div class="ic">🛡️</div><h3>Insured, in writing</h3><p>We'll send our general liability certificate before we set foot on your roof. Call the agent on it if you want to verify.</p></div>
    <div class="icon-card"><div class="ic">📋</div><h3>Scope you can read</h3><p>Shingle brand and line, underlayment, ice-and-water, flashing, ventilation and decking pricing are all spelled out before you sign.</p></div>
    <div class="icon-card"><div class="ic">🧲</div><h3>Clean job sites</h3><p>Tarps over landscaping, magnet sweeps for nails, and a walk-around with you before we leave.</p></div>
    <div class="icon-card"><div class="ic">📞</div><h3>We answer the phone</h3><p>Same number before, during and after the job. Workmanship warranty backed by a company that's still here.</p></div>
  </div>
</div></section>

<section class="section"><div class="wrap split">
  <div>
    <span class="eyebrow">Services</span>
    <h2>Everything a storm can throw at a roof</h2>
    <ul class="checks">
      <li>Free hail and wind damage inspections with photo reports</li>
      <li>Written repair estimates and dated photo reports you can share with your insurance company</li>
      <li>Full roof replacement: architectural, Class 4 impact-resistant, and metal</li>
      <li>Roof repairs, leak tracing and emergency tarping</li>
      <li>Decking replacement, ridge and soffit ventilation</li>
      <li>Seamless gutters, downspouts and gutter guards</li>
      <li>Skylight, vent and flashing replacement</li>
    </ul>
    <a class="btn dark" href="contact.html">Request a Free Inspection</a>
  </div>
  <div>{img('house8')}</div>
</div></section>

<section class="section dark"><div class="wrap">
  <span class="eyebrow">Where we work</span>
  <h2>Converse and the northeast side of San Antonio</h2>
  <p class="lead">We stay close so we can be on your roof fast and back on it later if you ever need us.</p>
  <div class="areas" style="margin-top:18px"><span>Converse</span><span>Kirby</span><span>Windcrest</span><span>Universal City</span><span>Live Oak</span><span>Schertz</span><span>Cibolo</span><span>Selma</span><span>St. Hedwig</span><span>Garden Ridge</span><span>Randolph AFB area</span><span>NE San Antonio (78109, 78219, 78239, 78244)</span></div>
</div></section>

<section class="section alt"><div class="wrap">
  <span class="eyebrow">Reviews</span>
  <h2>What neighbors say</h2>
  <p class="small">Placeholder slots. Paste in real Google reviews (with the reviewer's permission) or embed your Google Business Profile reviews widget here before launch.</p>
  <div class="grid c3" style="margin-top:12px">
    <div class="quote"><div class="stars">★★★★★</div><p>[Google review text goes here]</p><footer>— Homeowner, Converse</footer></div>
    <div class="quote"><div class="stars">★★★★★</div><p>[Google review text goes here]</p><footer>— Homeowner, Kirby</footer></div>
    <div class="quote"><div class="stars">★★★★★</div><p>[Google review text goes here]</p><footer>— Homeowner, Universal City</footer></div>
  </div>
</div></section>'''
write("about.html", layout("About Us | Converse Roofer, Local Storm Roofing in Converse, TX",
  "Converse Roofer is a locally based storm-damage roofing company serving Converse, Kirby, Windcrest and NE San Antonio. Free inspections, insurance help, honest work.", about, active="about.html", canonical="about.html"))

# ---------------- CONTACT ----------------
contact = page_hero("Free Roof Inspection &amp; Contact", f"Call or text {PHONE}, or send the form and we'll get back to you the same day. Serving Converse, Kirby, Windcrest, Universal City, Live Oak, Schertz and Cibolo.", imgkey="house3", crumbs='<a href="index.html">Home</a> › Contact') + f'''
<section class="section"><div class="wrap split" style="align-items:start">
  <div>{lead_form()}</div>
  <div>
    <span class="eyebrow">Reach us directly</span>
    <h2>Fastest: call or text</h2>
    <p style="font-size:2rem;font-weight:800;margin:0"><a href="{TEL}" style="color:var(--navy);text-decoration:none">{PHONE}</a></p>
    <p class="small">7 days a week · Storm emergencies any time</p>
    <div style="display:flex;gap:10px;flex-wrap:wrap;margin:14px 0 28px"><a class="btn primary" href="{TEL}">📞 Call now</a><a class="btn dark" href="{SMS}">💬 Text us</a></div>
    <h3>What happens after you reach out</h3>
    <div class="steps" style="grid-template-columns:1fr;gap:12px">
      <div class="step"><h3 style="font-size:1.05rem">We call you back the same day</h3><p>Usually within the hour during business hours. We'll ask about the storm date, what you've noticed, and your insurance situation.</p></div>
      <div class="step"><h3 style="font-size:1.05rem">Roof inspection within 1–2 days</h3><p>About 45 minutes. We get on the roof, photograph every slope, and check gutters, vents, screens and the AC unit.</p></div>
      <div class="step"><h3 style="font-size:1.05rem">You get the honest answer</h3><p>Damage or no damage, with the photos and a written estimate to back it up. What you do next is up to you.</p></div>
    </div>
    <h3 style="margin-top:28px">Service area</h3>
    <div class="areas"><span>Converse</span><span>Kirby</span><span>Windcrest</span><span>Universal City</span><span>Live Oak</span><span>Schertz</span><span>Cibolo</span><span>Selma</span><span>St. Hedwig</span><span>NE San Antonio</span></div>
  </div>
</div></section>
<section class="section alt"><div class="wrap narrow faq">
  <h2>Before you call</h2>
  <details open><summary>Is the inspection really free?</summary><p>Yes. No trip charge, no obligation, and you keep the photo report. We make our money building roofs, not inspecting them.</p></details>
  <details><summary>Do I need to be home?</summary><p>For the roof itself, no. For the walk-through of what we found, it helps. Most homeowners do the report review by phone with the photos texted over.</p></details>
  <details><summary>My insurance company already scheduled an inspection. Can you still come?</summary><p>Yes, and ideally before it, so you have our photo report and written estimate in hand. If you'd like us on site during their inspection to show the damage we documented, tell us the date and time.</p></details>
  <details><summary>Do you handle my insurance claim?</summary><p>No. Converse Roofer is a roofing contractor, not a public adjuster, and Texas law keeps those roles separate. We document the damage, give you a written estimate, and do the work. You file and manage the claim with your insurance company; a licensed public adjuster or attorney can represent you if there's a dispute.</p></details>
</div></section>'''
write("contact.html", layout(f"Free Roof Inspection in Converse, TX | Call {PHONE} | Converse Roofer",
  f"Request a free hail damage roof inspection in Converse, Kirby, Windcrest or NE San Antonio. Call or text {PHONE}. Same-day callback, photo report, no obligation.", contact, active="contact.html", canonical="contact.html"))

# ---------------- sitemap, robots, 404 ----------------
urls = ["", "hail-storm-september-11-2026.html","weather.html","gallery.html","about.html","contact.html","blog/"] + [f"blog/{p['slug']}.html" for p in posts]
write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{DOMAIN}/{u}</loc><lastmod>2026-09-16</lastmod></url>\n" for u in urls) + "</urlset>\n")
write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
write("404.html", layout("Page not found | Converse Roofer", "That page doesn't exist.", f'<section class="section"><div class="wrap narrow" style="text-align:center;padding:60px 20px"><h1>Page not found</h1><p class="lead">That link is broken or the page moved. Try the home page, or just call us.</p><a class="btn primary lg" href="{TEL}">📞 {PHONE}</a> <a class="btn dark lg" href="index.html">Home</a></div></section>', canonical="404.html", storm_bar=False))
