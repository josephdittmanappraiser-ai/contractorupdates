#!/usr/bin/env python3
"""Scaffold a new storm report page.

Usage:
  python3 tools/new_storm.py --date 2026-10-03 --hail 1.25 --wind 60 \
      --areas "Converse, Kirby, Windcrest" --headline "Half-dollar hail across Converse" \
      --source "https://www.weather.gov/ewx/" [--outages 1200] [--notes "Spotters reported..."]

Creates storms/<date>-<slug>.html, registers it in the STORMS list in
tools/build_site.py (so it appears on the Storm Reports index), adds it to the
sitemap, and regenerates the site. Edit the "What happened" text in
build_site.py afterwards if you have more detail, then rerun build_site.py.
"""
import argparse, re, datetime, os, subprocess, sys, json, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G = os.path.join(ROOT, "tools", "build_site.py")
q = json.dumps  # safe double-quoted Python string literal

def hail_name(inches):
    table = [(0.75, "penny"), (0.88, "nickel"), (1.0, "quarter"), (1.25, "half-dollar"), (1.5, "ping-pong ball"),
             (1.75, "golf ball"), (2.0, "hen egg"), (2.5, "tennis ball"), (2.75, "baseball"), (4.0, "softball")]
    name = "pea"
    for size, n in table:
        if inches >= size:
            name = n
    return name

ap = argparse.ArgumentParser()
ap.add_argument("--date", required=True, help="YYYY-MM-DD")
ap.add_argument("--hail", type=float, default=0, help="max hail diameter in inches")
ap.add_argument("--wind", type=int, default=0, help="max gust mph")
ap.add_argument("--areas", required=True, help="comma-separated towns")
ap.add_argument("--headline", required=True)
ap.add_argument("--source", action="append", default=[], help="URL, repeatable")
ap.add_argument("--outages", type=int, default=0)
ap.add_argument("--notes", default="")
a = ap.parse_args()

d = datetime.date.fromisoformat(a.date)
label = d.strftime("%B %-d, %Y")
slug = a.date + "-" + re.sub(r"[^a-z0-9]+", "-", a.headline.lower()).strip("-")
var = "storm_" + slug.replace("-", "_")
sev = "Severe" if (a.hail >= 1.0 or a.wind >= 58) else "Sub-severe"
hail_txt = ('%.2f" (%s) hail' % (a.hail, hail_name(a.hail))) if a.hail else "no significant hail"
wind_txt = ("%d mph gusts" % a.wind) if a.wind else "no damaging wind reported"
summary = hail_txt + "; " + wind_txt + (("; %s outages" % format(a.outages, ",")) if a.outages else "") + "."
areas_html = "".join("<span>%s</span>" % html.escape(t.strip()) for t in a.areas.split(","))
sources_html = "".join('<li><a href="%s" rel="noopener" target="_blank">%s</a></li>' % (html.escape(u), html.escape(u)) for u in a.source) \
    or "<li>NWS Austin/San Antonio warnings and local storm reports</li>"
notes_html = html.escape(a.notes) if a.notes else "Fill in the NWS warning times, hail sizes, spotter reports and impacts for this event."

TEMPLATE = r'''
__VAR__ = page_hero(__HERO_TITLE__, __HERO_SUB__, imgkey="storm1", root="../", crumbs='<a href="../index.html">Home</a> › <a href="index.html">Storm Reports</a> › __LABEL__') + f"""
<section class="section"><div class="wrap">
  <div class="stats">
    <div class="stat"><b>__DAY__</b><span>__WEEKDAY__ storm</span></div>
    <div class="stat"><b>__HAIL__</b><span>Max hail (__HAILNAME__)</span></div>
    <div class="stat"><b>__WIND__ mph</b><span>Max gusts</span></div>
    <div class="stat"><b>__OUTAGES__</b><span>Power outages reported</span></div>
  </div>
</div></section>
<section class="section alt"><div class="wrap"><article class="article">
<h2>What happened</h2>
<p>__NOTES__</p>
<h2>Areas affected</h2>
<div class="areas" style="margin-bottom:1.5em">__AREAS__</div>
{dia("hail-size-chart", root="../")}
<h2>What to do this week</h2>
<ol>
<li><strong>Photograph what you can see from the ground</strong>: dented gutters, torn screens, chipped paint, granules at downspouts.</li>
<li><strong>Get a free roof inspection</strong> and a dated photo report before you decide anything.</li>
<li><strong>Be careful who you sign with.</strong> <a href="../blog/7-questions-before-you-sign-with-a-roofer-after-a-storm.html">Seven questions to ask first</a>.</li>
</ol>
{dia("where-hail-hides", root="../")}
<h2>Sources</h2><ul class="small">__SOURCES__</ul>
</article></div></section>
<section class="section"><div class="wrap split"><div>{lead_form(root="../", title="Was your house under this storm?", sub="Tell us the address and we will come take a look. Free, with photos.")}</div><div><span class="eyebrow">Local, on the roof, honest</span><h2>Converse Roofer</h2><p>Based in Converse. Photo-documented inspections, written estimates, no deductible games.</p><a class="btn primary lg" href="{TEL}">📞 {PHONE}</a></div></div></section>"""
write(__PATH__, layout(__PAGE_TITLE__, __DESC__, __VAR__, root="../", active="hail-storm-september-11-2026.html", canonical=__CANON__))
'''
page = (TEMPLATE
    .replace("__VAR__", var)
    .replace("__HERO_TITLE__", q(label + " storm: " + a.headline))
    .replace("__HERO_SUB__", q(summary + " Areas: " + a.areas + "."))
    .replace("__LABEL__", html.escape(label))
    .replace("__DAY__", html.escape(label.split(",")[0]))
    .replace("__WEEKDAY__", d.strftime("%A"))
    .replace("__HAIL__", '%.2f&quot;' % a.hail)
    .replace("__HAILNAME__", hail_name(a.hail))
    .replace("__WIND__", str(a.wind))
    .replace("__OUTAGES__", format(a.outages, ","))
    .replace("__NOTES__", notes_html.replace("{", "{{").replace("}", "}}"))
    .replace("__AREAS__", areas_html)
    .replace("__SOURCES__", sources_html.replace("{", "{{").replace("}", "}}"))
    .replace("__PATH__", q("storms/" + slug + ".html"))
    .replace("__PAGE_TITLE__", q(label + " Storm Report: " + a.headline + " | Converse Roofer"))
    .replace("__DESC__", q(summary + " Areas: " + a.areas + "."))
    .replace("__CANON__", q("storms/" + slug + ".html")))

entry = (" dict(slug=%s, path=%s, date=%s, label=%s,\n      title=%s, summary=%s,\n      areas=%s, img=\"storm2\", severity=%s),\n"
         % (q(slug), q("storms/" + slug + ".html"), q(a.date), q(label), q(a.headline), q(summary), q(a.areas), q(sev)))

g = open(G).read()
assert "STORMS = [\n" in g and "def storms_index():" in g, "build_site.py layout changed; update new_storm.py"
g = g.replace("STORMS = [\n", "STORMS = [\n" + entry, 1)
g = g.replace("def storms_index():", page + "\ndef storms_index():", 1)
open(G, "w").write(g)
subprocess.run([sys.executable, G], check=True, stdout=subprocess.DEVNULL)

sm = os.path.join(ROOT, "sitemap.xml")
s = open(sm).read()
s = s.replace("</urlset>", "  <url><loc>https://converseroofer.com/storms/%s.html</loc><lastmod>%s</lastmod></url>\n</urlset>" % (slug, a.date))
open(sm, "w").write(s)
print("created storms/%s.html, added it to the Storm Reports index and the sitemap" % slug)
