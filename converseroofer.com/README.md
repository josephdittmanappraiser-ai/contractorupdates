# converseroofer.com

Static lead-generation site for Converse Roofer (Converse, TX). No build step, no
framework: plain HTML, one stylesheet, three small scripts. Upload the folder to any
static host and it works.

## Pages

| File | Purpose |
|---|---|
| `index.html` | Home: hero + lead form, storm stats and track map, services, process, diagrams, photos, blog teasers, FAQ |
| `hail-storm-september-11-2026.html` | Report on the Sept 11, 2026 hail storm (NWS timeline, areas hit, diagrams, sources) |
| `weather.html` | Live Converse weather: NWS alerts, current conditions, 48-hr hail/storm risk, 7-day forecast |
| `gallery.html` | Photo gallery plus storm maps and diagrams |
| `blog/index.html` + 5 posts | Hail damage, Texas claim process, choosing a roofer, ground-level checklist, Class 4 shingles |
| `about.html` | Who we are, how we work, services, service area map, review slots |
| `contact.html` | Free inspection form, call/text buttons, what-happens-next, FAQ |
| `areas/` (6 pages + index) | Service-area pages: Converse, Kirby & Windcrest, Universal City & Live Oak, Schertz/Cibolo/Selma, St. Hedwig, NE San Antonio |
| `storms/index.html` | Storm Reports index; every storm gets its own dated page |
| `404.html`, `sitemap.xml`, `robots.txt`, `.htaccess` | Housekeeping, redirects, custom 404 |

The phone number lives in `assets/js/config.js` and `tools/build_site.py`. Change both
and rerun the generator.

## Before / after going live

1. **Lead form.** Set `formEndpoint` in `assets/js/config.js` to a Formspree or Basin URL
   so submissions email you. Until then the form opens an email draft on the visitor's
   device. Set `leadEmail` for that fallback.
2. **Photos.** Photo slots load stock images from Unsplash's CDN with an illustrated
   fallback (`assets/img/scene-*.svg`) if a photo fails. Replace with real job and storm
   photos: drop files in `assets/img/` and swap the `IMGS` table in `tools/build_site.py`.
3. **Reviews.** `about.html` has three placeholder review cards.
4. **Analytics.** Paste your GA4 Measurement ID into `gaId` in `assets/js/config.js`.
   `assets/js/analytics.js` then loads gtag and sends `call_click` (with placement:
   header, hero, mobile bar, CTA band, body), `text_click`, `form_start`,
   `generate_lead` and `outbound_click` events. Optional `adsCallConversion` fires a
   Google Ads conversion on every call click.
5. **Search Console.** Verify by DNS TXT at the registrar or by HTML tag (add the tag
   to the `<head>` block in `tools/build_site.py`), then submit `sitemap.xml`.

## Live weather

`assets/js/weather.js` calls Open-Meteo (no API key) for conditions and the 7-day
forecast, and api.weather.gov for active NWS alerts at Converse (29.518, -98.316).

## Adding a storm report (the cadence)

After any NWS-warned hail or wind event in the service area, run:

```
python3 tools/new_storm.py --date 2026-10-03 --hail 1.25 --wind 60 \
  --areas "Converse, Kirby, Windcrest" --headline "Half-dollar hail across Converse" \
  --source "https://www.weather.gov/ewx/" --outages 1200 --notes "NWS warning at ..."
```

That creates `storms/<date>-<slug>.html`, lists it on the Storm Reports index, and
adds it to the sitemap. Edit the generated "What happened" text in `tools/build_site.py`
for more detail, rerun `python3 tools/build_site.py`, then deploy and resubmit the
sitemap in Search Console. Schema (breadcrumbs, FAQ) is generated automatically for
every page that has a breadcrumb trail or a FAQ block.

## Regenerating

- `python3 tools/build_site.py` rebuilds every HTML page from one layout.
- `python3 tools/build_art.py` regenerates the blog cover art and fallback scenes.
