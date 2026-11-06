Paste everything below into ChatGPT, then paste the attached research report (docs/research-map-first-2026-11-06.md) under it.

---

You are reviewing a redesign plan for floodinsurancedata.com. Be blunt and specific; no generic SEO advice. One rule is never negotiable: never show a wrong, estimated or misleading number. Also fixed: aggregates only (no address-level data), no premium calculator or quotes, no advice or verdicts, law text only quoted from official sources, static fast pages.

The site: static pages on Cloudflare, about 3 weeks old, anonymous publisher, no backlinks. Search Console, 28 days: 285 impressions, 0 clicks, position about 44. Pages: home, 51 states, about 212 counties (20 added a day, ordered by search demand), 7 flood-zone pages. Data: every FEMA NFIP flood policy in force and every claim since 1978, by county, ZIP and zone; plus FEMA disaster declarations, National Risk Index, CRS discounts, sea level.

Demand (Google Keyword Planner, US, band floors per month, corrected 11-06): generic terms 38,800 (incl. "flood insurance"), state 13,510, zone words 7,530, county 7,350, towns 3,050. The biggest single terms are "flood zone map" and "fema flood map by address" (10K-100K band each). Keyword Planner bands run 3-10x above real counts (Ahrefs).

The owner's idea: make the site "map first", ideally with a literal map. Our research (attached) concluded:
1. Map searchers already have FEMA's map. What they lack is what the map cannot say: must I buy, what it costs here, what floods paid out here, is the map changing. We show that on screen 1 with one button to FEMA's map.
2. No literal map yet. FEMA's map servers refused connections from two networks on 11-06. The only working copy (Esri) is an 8-month-old snapshot that drops low-risk zone X, so an empty result is ambiguous. Google does not tap a "show map" button, so a map earns no ranking. A tap-to-load map (Leaflet, 46 KB) ships last, only if a cloud job reaches FEMA, FEMA's legend colours are read raw and the layer's date is printed.
3. No new URLs per county (doorway risk); retitle existing pages "flood zones" first; one hub /flood-zone-map/; new single pages for claims, renters, ZIP rates.
4. Build order with dated Search Console kill numbers (in the report).

Questions:
1. Where is this plan wrong? Attack the "no literal map" call hardest: is there a truthful map the reader would value enough to choose us over FEMA, and could it work without FEMA's servers (e.g. pre-rendered county images from FEMA's downloadable county shapefiles, built monthly in the cloud)? What breaks it?
2. For each keyword category in the report's table, is the owner page and first phone screen the most helpful possible? What would you add or cut?
3. What is the single most linkable thing we could publish from this data, and to whom exactly?
4. Is the build order right? Reorder it if not, with your reason.
5. What visual or UI changes would make a homeowner on a phone trust this site within 5 seconds, without a named author?
6. Which of the continue/kill numbers are unrealistic for a site at position 44 with 0 links?
Answer in under 900 words.
