
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


=== RESEARCH REPORT (evidence) ===

# Put FEMA's map one tap away

"Map first" works as a redesign of titles and first screens, not as a map widget. The site should keep every URL and keep one page per place. It should put a "find your zone on FEMA's map" action plus a three-row local zone key (is insurance required, median cost here, share of insured homes per zone group) on the first phone screen of every county and state page, and retitle those pages so they name flood zones before cost. It should not draw a literal map of FEMA's zones yet. FEMA's own map servers refused connections from both the laptop and Anthropic's cloud on 2026-11-06. The only reachable copy (Esri's) is an eight-month-old snapshot that deletes low-risk zone X. Google also never taps a "load map" button, so map pixels earn no ranking. The win is the pairing nobody offers: top results either send the reader to FEMA's lookup with no local numbers, or quote one undated national average next to a quote form. Our NFIP aggregates by county and zone fill that gap. Demand is smaller than PLAN.md says. Keyword Planner stores its bands as 50/500/5,000/50,000, and `tools/kwp_rank.py` read those as range floors, which overstated every total 5x until it was fixed today. The corrected monthly band floors are generic 38,800, state 13,510, zone 7,530, county 7,350 and town 3,050, so the earlier "34K county map" and "37K zone" figures in PLAN.md are 5x too high. Being #1 in every category is not achievable: FEMA owns the address lookup, big finance publishers own head cost terms, and quote intent conflicts with the no-quote rule. Realistic #1 targets are zone cost, "is flood insurance required", claims and ZIP rates, with page 1 for states and mid-size towns.

## FEMA's map can be linked today but not safely drawn

On 2026-11-06, every FEMA flood-map service failed during the secure connection handshake: hazards.fema.gov's NFHL MapServer (both REST paths), the layer-28 point query and msc.fema.gov. The failure came from the laptop and from Anthropic's servers, while a control request to Google succeeded. That points to filtering or an outage on FEMA's side, not a client bug ([FEMA NFHL page](https://www.fema.gov/flood-maps/national-flood-hazard-layer); [ArcGIS item for FEMA's NFHL](https://www.arcgis.com/sharing/rest/content/items/ae38b6f94eaf4abf97f986fa01921e13?f=json)). Whether a Cloudflare Worker or GitHub Actions runner can reach FEMA is untested, and that is the question every embedded-map design depends on. FEMA also documents no address deep link into the Map Service Center. The browser check of msc.fema.gov could not run because the browser extension was not connected, so the MSC address link stays unverified. The only documented parameter found is a community search (`availabilitySearch?addcommunity=`), cited in a county document ([Allen County IN](https://www.allencounty.in.gov/DocumentCenter/View/11195)).

The one copy that answered is Esri's "USA Flood Hazard Areas" feature service. It needs no key, allows any website to read it (open CORS), and returned a point query in 0.47 s. Its own description makes it unsafe as an answer: it was **"created from the March 3, 2026 snapshot"**, it is refreshed annually, and it removes unshaded zone X ("Area of Minimal Flood Hazard") along with D, open water and unmapped areas. An empty result can therefore mean low-risk, undetermined, water or unmapped ([Esri item ccd29fb4](https://www.arcgis.com/home/item.html?id=ccd29fb4bd5e4b44a2d61638829a5d7e)). It only draws at 1:400,000 scale or closer, so a county-wide view of a large county shows nothing. It is licensed under the Esri Master License Agreement, whose terms for anonymous public use were not read. Esri's raster copy, which does include every zone, returned "Token Required" ([Esri item 11955f1b](https://www.arcgis.com/home/item.html?id=11955f1b47ec41a3af86650824e0c634)). The notes disagree on which Esri copy is current. One cites an older "Reduced Set" layer with a March 2026 edit date; the other shows that item was last modified in 2020 by a California agency. Treat the services5 "USA_Flood_Hazard_Areas_view" copy as the live one, and drop the Reduced Set.

The address side is weak too. The Census Geocoder is free and fast, but it returns a street-range point estimated from address ranges, not the house itself, and does not say so. Near a zone line that can produce the wrong zone ([Census Geocoder documentation](https://www.census.gov/programs-surveys/geography/technical-documentation/complete-technical-documentation/census-geocoder.html)). The cost of building a map is small: Leaflet 1.9.4 measured about 46 KB gzipped against about 451 KB for MapLibre 6.16, and US Geological Survey (USGS) basemap tiles answered with open CORS ([USGS National Map basemap](https://basemap.nationalmap.gov/arcgis/rest/services/USGSTopo/MapServer)). The constraints are truth and reachability, not bytes. The verdict: link out to FEMA now. Revisit a tap-to-load map only after three things hold: a job proves it can reach FEMA, FEMA's legend colours are read raw, and the map carries a printed as-of date. The legal climate supports caution. Zillow stopped showing numeric First Street climate scores in late 2025 after pushback from a regional listing service ([The Real Deal](https://therealdeal.com/national/2025/12/01/zillow-drops-climate-risk-scores-after-industry-pushback)), and a New York couple sued over a flood rating they called false ([HousingWire](https://www.housingwire.com/articles/ny-couple-claims-zillows-climate-risk-data-harmed-home-sale/)).

## Twelve keyword categories, five realistic #1s

WebSearch only approximates Google, and several result sets were flooded with keyword-stuffed spam on hacked university and corporate domains. So the real Google top 3 is unknown for "flood zone map florida", "flood zone x meaning" and "cost zone AE". The pattern across categories is still consistent: competitors either send readers to FEMA's lookup, or print one stale, unlabelled national number beside a quote form. Searches for "fema flood map by address" end at FEMA's Map Service Center. The guides ranked around it, such as protectmyzip, are about 1,000 words with a button to FEMA and no zone, cost, claims or map dates ([protectmyzip](https://protectmyzip.com/resources/fema-flood-map-by-address)). FEMA's own /flood-maps page is a hub that defines no zone letters and lists no costs ([FEMA Flood Maps](https://www.fema.gov/flood-maps)), and app reviewers call FEMA's site "clunky" and hard on a phone ([App Store reviews](https://apps.apple.com/us/app/flood-zone-map/id908554933)).

County map searches end at JavaScript-only county map viewers, such as Pinellas's, whose page text is empty to a crawler ([Pinellas FMSC](https://floodmaps.pinellas.gov/)), and at news about remaps. Harris County is the live case: draft maps released in February 2026 sit next to the current FEMA map, with final approval projected around 2028 ([Click2Houston](https://www.click2houston.com/news/local/2026/02/12/fema-releases-draft-flood-maps-for-harris-county-some-neighborhoods-see-reduced-risk); [MAAPnext](https://maapnext.harriscountytx.gov)). Zone glossaries quote undated national figures. Kin gives a "$786" median and a "$39" Preferred Risk Policy, a product that looks discontinued (unconfirmed) ([Kin Zone X](https://www.kin.com/glossary/flood-zone-x)). Cost publishers disagree with each other. Policygenius says "$888" from 2023 data on a page last updated May 30, 2024 ([Policygenius](https://www.policygenius.com/homeowners-insurance/how-much-does-flood-insurance-cost)). NerdWallet ([NerdWallet](https://www.nerdwallet.com/article/insurance/flood-insurance-cost)) and Bankrate ([Bankrate](https://www.bankrate.com/insurance/homeowners-insurance/cost-of-flood-insurance)) show other figures, but those were reported in search summaries only and not read raw. "Is flood insurance required" results include archived 2013-2021 FloodSmart copies ([UNT archive](https://webarchive.library.unt.edu/web/20161103000314/https://www.floodsmart.gov/floodsmart/pages/about/when_insurance_is_required.jsp)). Claims searches return old PDFs, scrapers and a ValuePenguin study that now answers "410 Gone" ([Zillow 2017](https://www.zillow.com/research/12-counties-third-flood-insurance-17236); [ValuePenguin](https://www.valuepenguin.com/flood-insurance-policies-study)).

The table maps each category to one page and gives honest odds. Volumes are the coordinator's corrected band floors where given, and the keyword note's band floors otherwise.

| Category (floor/mo) | Top results give | They miss | Owner page | First phone screen | Realistic ceiling |
|---|---|---|---|---|---|
| Map / by address (3 terms in the 10K-100K band) | FEMA MSC; how-to guides that link to it | Local cost, required share, claims after the lookup | New single hub `/flood-zone-map/` + home | H1 "Flood zone map" > address form or button to FEMA > "we never show your zone; FEMA's map does" > state links | #2-#5 behind FEMA |
| State map / state insurance (13,510) | Regulators, Bankrate/Insurify guides, spam | Fresh (Aug 2026) medians, county chooser with zone mix | `/flood-insurance/<state>/` | H1 "Florida flood zones and flood insurance cost" > county picker + FEMA button > state median, high-risk share, claims paid | Page 1 for 100-1K states; #1 for TX/FL/CA needs links |
| Zone meaning/cost (7,530) | Spam, Kin/compare.com glossaries, one national figure | Exact-zone medians by state, outside-zone claims share | `/flood-zones/<z>/` (phase 1 shipped) | Keep: meaning > required > FEMA button > two cost tiles; add H2 "Zones B and C: old names for X" | **Best #1 odds on the site** |
| County map / insurance (7,350) | County viewers (JS-only), remap news | Text page with cost by zone, map status, claims | `/flood-insurance/<county>/` | H1 "Flood zones in Palm Beach County: find yours on FEMA's map, and what each zone costs here" > FEMA action > 3-row local key > required | Long-tail page 1; #1 rarely beats the county government |
| Generic cost (38,800 incl. head) | Policygenius $888 (2023), NerdWallet, Bankrate | Base labels (median vs mean, fees, single-family), currency | Home | "How much is flood insurance? $1,066 median" via `tp()` > monthly > new-buyer median > state table | Page 1 for "average"; #1 needs links |
| NFIP / head term | FloodSmart, CRS reports, Wikipedia | A current national median | Home (no /nfip/ page) | One `rule()` line on what NFIP is and its authorization status | Very low |
| Town (3,050) | Local news (WBEZ 2023), FloodSmart city pages | 2026 counts, ZIP range, outside-zone claims | County page naming main towns | "Cook County, Illinois (includes Chicago)" > median > ZIP range > outside-zone claim share | Page 1 for mid towns |
| Renters (~1,000) | NerdWallet, FEMA, FloodSmart: same three facts | What renters actually pay | New single page `/flood-insurance/renters/` | Median cost of tenant contents-only policies + count > what it covers via `rule()` > 30-day wait | Page 1 plausible |
| Required (~200) | Archives, Neptune, spam | Current quoted rule + local share flagged lender-required | Home section | Rule sentence (exists) > lender-flagged share > outside-zone claim share | **#1 plausible** |
| Claims (~100) | FEMA how-to, PDFs, scrapers | Paid share, unpaid reasons, typical paid amount | New single page `/flood-insurance/claims/` + place sections | National paid share and median paid (fixed loss years) > top unpaid reasons > deadlines via `rule()` | **#1 plausible; best link asset** |
| ZIP rates (~100) | Policygenius 2023 means at 5+ policies; 2023 news | Current medians at 30+ priced policies | One tool URL `/flood-insurance/zip/` | ZIP box > median, count, range, county fallback labelled | **#1 plausible** |
| Quote / companies (~1,100) | Lead-gen forms, affiliate "best" lists | Nothing we may honestly add | Existing "is my quote normal?" checker + FloodSmart link | Don't target | None; don't pursue |

Sources for the table rows are cited in the prose above. Additional sources: [TDI](https://www.tdi.texas.gov/consumer/storms/flood-insurance.html), [WBEZ](https://www.wbez.org/environment-public-health/2023/08/09/thousands-in-chicago-face-flood-risk-research-shows), [FEMA renters release](https://fema.gov/press-release/20210318/yes-renters-can-buy-flood-insurance-0), [FEMA file your claim](https://fema.gov/flood-insurance/resources-practitioners/file-your-claim) and [WLRN 2023 ZIP projections](https://www.wlrn.org/environment/2023-05-10/flood-insurance-costs-will-soar-in-florida-see-the-expected-increases-in-your-zip-code).

The reader's questions after seeing a zone follow the order already in CLAUDE.md: am I required, what does it cost here, has it flooded and paid out here, is the map changing, is my building really in it. Agent and lender checklists converge on that order ([midflorida.com](https://midflorida.com/blog/insights/may-2024/what-to-consider-before-buying-a-house-in-a-flood); [bluefieldgroup.com](https://joshhileman.bluefieldgroup.com/blog/what-to-know-when-purchasing-a-home-in-a-fema-flood-zone/)). The map answers only question zero, "which zone". Every other answer is data the site already holds. The most decision-changing local line is the county's share of claims outside high-risk zones, shown beside FEMA's national figure that **one-third of NFIP claims in 2013-2023 came from outside high-risk areas** ([FEMA Fast Facts PDF](https://agents.floodsmart.gov/sites/default/files/media/document/2025-07/fema-nfip-fast-facts-flood-insurance-infographic-11-2024.pdf)). The two use different bases: FEMA counts claims, while the site measures paid claim dollars. Never print them side by side without both labels.

## Google rewards the text answers, not the map

Google's guidance settles how a tap-to-load map is treated: "Google Search does not interact with your page." Lazy loading must not depend on "user actions, such as scrolling or clicking" ([Google lazy-loading guide](https://developers.google.com/search/docs/crawling-indexing/javascript/lazy-loading)). A map behind a button is invisible to Google by design. That suits phone bytes and responsiveness, so every fact a map conveys must also be HTML text. No map or place rich result exists for informational pages. Dataset markup describes CSV metadata, not values, and is not guaranteed to display ([Dataset structured data](https://developers.google.com/search/docs/appearance/structured-data/dataset)). The real algorithm risk at about 2,000 county pages is the spam policy on doorways ("pages ... created to rank for specific, similar search queries") and on scaled content ([Google spam policies](https://developers.google.com/search/docs/essentials/spam-policies)). An identical map module adds shared boilerplate, not uniqueness. County pages already measure 76% alike once names and numbers are masked ([PLAN.md](C:/Users/mwoo7/Desktop/floodinsurance/PLAN.md)), and only per-county figures lower that: the local zone key, map status dates, claims outside the zones.

That rules out a parallel `/flood-zone-map/<county>/` page next to each `/flood-insurance/<county>/`. Two pages per county for near-identical queries is the doorway pattern. Re-URLing buys nothing either. John Mueller says a URL alone "brings minimal additional 'signal'" ([Search Engine Roundtable](https://www.seroundtable.com/google-urls-minimal-additional-signals-for-search-engines-38680.html)), and a move costs "a few weeks or more" of ranking churn plus redirects kept "at least 1 year" ([Google site-move guide](https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes)). Cloudflare Pages caps redirects at 2,100 rules ([Cloudflare Pages limits](https://developers.cloudflare.com/pages/platform/limits/)). A move would also confound the 2026-11-26 Search Console read. Google's helpful-content test asks for "original information, reporting, research, or analysis" and "substantial value when compared to other pages in search results" ([Creating helpful content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)). Sourced, dated county aggregates pass that test; a reskinned FEMA link does not.

Links in this niche go to data stories with a local cut. Examples are Penn State's county map of claims outside the high-risk zones ([PSIRC](https://www.psirc.psu.edu/assets/NFIP_Insights_for_PA.one-pager.2022-09-05.pdf)), UNC's 2025 outside-zone study ([InsuranceNewsNet](https://insurancenewsnet.com/oarticle/unc-study-sees-flooding-outside-nc-high-risk-areas-can-ai-reveal-blind-spots)), First Street's 2020 "undercounting by 70%" launch ([Community Impact](https://communityimpact.com/houston/bellaire-meyerland-west-university/austin/2020/07/03/analysis-fema-may-be-undercounting-national-total-flood-risk-by-as-much-as-70)), and post-disaster "where to check your flood risk" explainers like NPR's after the July 2025 Texas floods ([NPR](https://www.npr.org/2025/07/12/nx-s1-5464735/flood-risk-information-sources-texas)). No maintained, readable county claims table was found anywhere, so a national claims page with a dated download is the site's best chance at links. A working "find your zone" entry also helps the site get onto explainer lists, which argues for the FEMA action on screen 1 even though Google never uses it.

## One skeleton, existing look, guards written before code

Every page type gets the same first phone screen, about 650-750 px usable at 390x844: a breadcrumb, an H1 of at most two lines naming the place and "flood zones", one FEMA action, two or three stat tiles from `tp()`, a single "Sources: NFIP Policies v3, as of <date>" line, and jump links. Everything else moves below. On county pages the three-row key is the centrepiece. It has rows for A/AE, V/VE and X; for each zone group it shows "required?" via `rule()`, the median cost here and the share of insured homes here. The "is my quote normal?" checker moves to screen 2, where CLAUDE.md requires it to stay. The visual system in `tools/theme.py` stays: one sans font, navy, and AA contrast already enforced by `phone_check`. Stanford's credibility guidelines put verifiability, restraint with promotion, visible freshness and "avoid errors of all types" first ([Stanford Web Credibility](https://credibility.stanford.edu/guidelines/index.html)), and an anonymous site can't lean on the "real people" guidelines. A visible corrections route is the cheapest fix. Zone colours must copy FEMA's legend once read raw. FEMA's symbology page reset the connection, and a colour that differs from the map the reader opens next misleads them ([FEMA symbology](https://hazards.fema.gov/femaportal/resources/symbology.htm)). Performance has room: Core Web Vitals pass at a load time (LCP) of 2.5 s or less, a tap response (INP) of 200 ms or less, and a layout shift (CLS) of 0.1 or less ([web.dev](https://web.dev/articles/vitals)), and a FEMA link or GET form adds about 0.3 KB. County pages already weigh 25.9 KB gzipped, above the 20 KB target, so the redesign should also cut bytes.

The worst risks are truth risks, and one rule guards most of them: the site never computes or draws a zone for an address, it hands the address to FEMA. The table states each guard, the test that proves it, and the number where it breaks at full planned size.

| Risk | Guard | Test that fails without it | Breaks at |
|---|---|---|---|
| Reader treats our key as their zone | County aggregates only; official status line via `rule()` from FEMA text read raw | Gate rejects "your zone is", "you are in zone" | Never, while there is no address-level output |
| MSC link pattern dead or wrong | Use only a link verified in a browser; monthly text check (not just a 200 status) | Mutated query parameter must fail the check | Any FEMA URL change |
| FEMA down | Link only; page renders fully without FEMA | Gates pass with FEMA unreachable (already true) | Never for a link; every outage for an embed |
| Stale layer (if a map is ever drawn) | Print the layer's own as-of date and a note that FEMA's map is official | Build fails if the layer date is unreadable or too old | Any county remapped since Mar 3, 2026 |
| Doorway / scaled content | One page per place, per-county key, no twin URLs | Masked-similarity report at the 11-26 review | Over 25% of 3-week-old counties "crawled, not indexed" |
| Screen-1 overflow | `phone_check` asserts the FEMA action and first tile within 700 px | Adding a paragraph above must fail | Each new screen-1 line |
| Hub cannibalising counties | Hub template has no county `tp()` keys | Gate check | Any county number on the hub |
| Tile terms (if an embed ships) | USGS tiles; OSM only with visible attribution, no prefetch, Referer kept | `phone_check` asserts attribution is visible | OSM may block "without notice" ([OSMF tile policy](https://operations.osmfoundation.org/policies/tiles/)) |
| Cloudflare limits | About 4,100 files at 2,000 counties against a 20,000 cap; no per-page redirects | Sitemap URL set identical before and after the redesign | About 9,500 pages; 2,100 redirects |
| Build time | "Only what changed" for the live gate past 500 pages | Timing from a real run | Live gate near the 45-minute job limit at about 5,000 pages |

## Ranked build plan, smallest test first

The baseline is 285 impressions and 0 clicks in the 28 days to 2026-11-03, 79% of them on desktop ([PLAN.md](C:/Users/mwoo7/Desktop/floodinsurance/PLAN.md)). The continue/kill numbers below are set against that baseline. They are judgement calls to revise once the 11-26 read lands, not measurements.

| Rank | Build | Why first | Search Console check (date) | Continue if | Kill / revert if |
|---|---|---|---|---|---|
| 1 | Retitle state and county pages "flood zones" first, at about 60-70 characters; add an H1 line and a FEMA-map button on screen 1. Template change only, no new data | Cheapest; tests whether map intent lands on existing pages | 2026-12-04, 28 days | Pages get ≥30 impressions on queries containing "flood zone" or "flood map" | Under 10 such impressions, or total impressions fall below the prior 28 days: restore old titles |
| 2 | Three-row local zone key on the county screen 1 (fields exist: zone units, median by zone group) | The information gain FEMA's map lacks | 2026-12-18 | Clicks ≥5 on map-intent queries across county pages | 0 clicks with ≥100 map-intent impressions: the key isn't earning the click; rework the snippet |
| 3 | Zone pages: "B and C" H2; exact-zone tiles once all 51 states carry the field | Best #1 odds; data is already in code | 2027-01-08 | Average position ≤15 on "flood insurance cost zone ae/x" | Position worse than 40: stop zone investment |
| 4 | Hub `/flood-zone-map/`, only after the MSC link is verified in a browser | Head map terms (3 terms in the 10K-100K band) | 2027-01-29 | ≥200 impressions, position ≤20 | Under 50 impressions: fold into home, 301 one URL |
| 5 | National `/flood-insurance/claims/` with a dated CSV; deadlines via `rule()` after a raw read of the standard policy text | Link asset; open SERP | 2027-02-01 (PLAN's 3-referring-domains date) | ≥1 new referring domain, or ≥100 impressions | Neither: keep the place sections, drop pitching |
| 6 | ZIP tool `/flood-insurance/zip/` at the reader-tools standard, split per state (the national file is about 1.2 MB raw) | Stale competitor SERP | 2 weeks on 3 sample pages, then 2027-03-01 | Position ≤10 on "rates by zip code" | No impressions after 4 weeks live |
| 7 | Renters page, only if the cloud count of tenant contents-only policies passes the 30-policy floor nationally and in most states | Data no one has | Count first; check 4 weeks after launch | ≥100 impressions | Cohort too thin: no page |
| 8 | Cloud test: can a GitHub Actions run or a Worker reach hazards.fema.gov? Only if yes, add map-status lines (effective map date, preliminary maps, LOMR count) | Unlocks a decision-changing buyer line | One run | Reachable: build the status line | Unreachable: drop every FEMA-pull item |
| 9 | Tap-to-load embedded map (Leaflet, FEMA polygons, USGS tiles) | Last; reader value only, no ranking value | Only if rank 1-2 show map queries landing and bouncing | FEMA reachable, legend read raw, Esri terms read | Any of those three unmet: never ship |

Delete in the same batches: the `data-p` attributes (2.8 KB a page, no reader), the 49 per-bar `<title>` strings in the claims chart, and titles of 99-109 characters and descriptions of 261-274 characters that get truncated in search results. Off the build list: an interactive US map (an agent judged it "decoration" on 11-06), static county map images (wrong-zone risk), zone-by-address computation, twin map URLs, per-page redirects, quote or companies pages, and a separate /nfip/ page. Merging "Why sites quote different prices" into the cost card is the owner's call, because cutting a block is owner-only.

## Conclusion

The research changes what "map first" means. Map searchers do not need another map; they have FEMA's. They need what FEMA's map cannot say: whether that zone forces a purchase, what it costs and pays out locally, and whether the map is about to change. The site already holds most of those numbers, so the redesign is mostly reordering, retitling and one new local key. It is not a mapping project, and it should be judged by Search Console within four weeks rather than by how it looks.

Two caveats limit any ranking promise. First, demand is a fifth of what PLAN.md recorded, so the county-map prize is about 7,350 searches a month at the band floor, not 34,000. Second, the Google top 3 for several categories is unmeasured because the test index was overrun with spam. Two facts gate the most valuable truth features, the map-status line and any future embed: whether FEMA's servers answer a cloud job, and whether the MSC address link works. Settle both before anything that depends on FEMA data is built.


=== APPENDIX A: live pages (open them) ===
https://floodinsurancedata.com/
https://floodinsurancedata.com/flood-insurance/florida/
https://floodinsurancedata.com/flood-insurance/palm-beach-county-fl/
https://floodinsurancedata.com/flood-zones/ae/
https://floodinsurancedata.com/flood-zones/x/

=== APPENDIX B: first ~120 words each page shows today (live text, 2026-11-06) ===

[/]
Flood Insurance Data NFIP records · 50 states and DC · 212 counties What flood insurance costs in your state From FEMA's own records of existing policies and claims, not quotes: what policyholders pay, whether you're required to buy it, and how fast it starts. $1,066 U.S. median a year $89 Per month 4.5M Insured units in force Median and per month: what existing single-family primary-home policies pay, premium plus fees. Insured units: every NFIP policy unit in force on August 31, 2026, including condos, rentals and businesses. Buying? Policies first bought in the past year typically pay $1,011 (187,522 policies). Why sites differ . Built from 3,446,101 NFIP policy records and 2,680,429 claim records downloaded from FEMA (one record can cover several insured units, such


[/flood-insurance/palm-beach-county-fl/]
Flood Insurance Data Flood insurance › Florida › Palm Beach County Flood insurance in Palm Beach County, Florida In Palm Beach County, Florida, the median NFIP flood insurance policy on a single-family primary home costs $673 a year (premium plus fees, policies in force as of August 31, 2026). $673 Median / yr, single-family primary home $56 A month, spread over the year $518 – $1,041 Half pay between 23.2% Share of these homes below FEMA's full-risk price That is 32% below the Florida median of $985 and 37% below the U.S. median of $1,066 ; 8th lowest of 55 Florida counties with 100 + priced policies. By ZIP it ranges from $451 ( 33484 ) to $1,830 ( 33480 Palm Beach ); find your ZIP


[/flood-zones/ae/]
Flood Insurance Data Flood zone AE: what it means, who must insure, what it costs Zone AE is a high-risk area: land with a 1 percent or greater chance of flooding in any given year, where FEMA has worked out how high the water from that flood would reach (44 CFR §59.1, §64.3). A 1 percent or greater chance a year works out to a 26% or greater chance of at least one such flood over 30 years. Must I buy? Federal law requires it only in a high-risk zone (A or V) with a federally regulated or backed mortgage, or federal help to buy or build (42 U.S.C. §4012a). Outside those zones, a lender may still require it. Check your address on FEMA's flood map


=== APPENDIX C: top search terms per group (Keyword Planner US). Left column is Google's stored band value: 50 = 10-100, 500 = 100-1K, 5000 = 1K-10K, 50000 = 10K-100K a month. Group totals are band floors. ===

== generic: 428 keywords, 28 with 10+/mo, floor total 38,800/mo
  50000.0  flood zone map
  50000.0  flood insurance
  50000.0  fema flood map by address
  5000.0  nfip
  5000.0  how much is flood insurance
  5000.0  flood zone map by address
  5000.0  flood zone by address
  5000.0  flood insurance quote
  5000.0  flood insurance for renters
  5000.0  flood insurance cost
  5000.0  fema flood insurance
  500.0  what flood zone am i in

== state: 153 keywords, 109 with 10+/mo, floor total 13,510/mo
  5000.0  flood zone map north carolina
  5000.0  flood zone map new york
  5000.0  flood zone map new jersey
  5000.0  flood zone map louisiana
  5000.0  flood zone map florida
  5000.0  flood insurance texas
  5000.0  flood insurance florida
  5000.0  flood insurance california
  500.0  flood zone map wisconsin
  500.0  flood zone map washington
  500.0  flood zone map virginia
  500.0  flood zone map texas

== zone: 33 keywords, 24 with 10+/mo, floor total 7,530/mo
  5000.0  flood zone x meaning
  5000.0  flood zone x
  5000.0  flood zone ao
  5000.0  flood zone ae meaning
  5000.0  flood zone ae
  5000.0  flood zone a
  500.0  flood zone ve meaning
  500.0  flood zone ve
  500.0  flood zone v
  500.0  flood zone shaded x
  500.0  flood zone d meaning
  500.0  flood zone d

== county: 3657 keywords, 285 with 10+/mo, floor total 7,350/mo
  5000.0  pinellas county flood zone map
  5000.0  harris county flood zone map
  500.0  volusia county flood zone map
  500.0  st tammany parish flood zone map
  500.0  st johns county flood zone map
  500.0  skagit county flood zone map
  500.0  sarasota county flood zone map
  500.0  polk county flood zone map
  500.0  pima county flood zone map
  500.0  pierce county flood zone map
  500.0  pasco county flood zone map
  500.0  palm beach county flood zone map

== town: 5181 keywords, 170 with 10+/mo, floor total 3,050/mo
  5000.0  flood insurance chicago
  500.0  flood insurance sacramento
  500.0  flood insurance new orleans
  500.0  flood insurance houston
  500.0  flood insurance hartford
  50.0  flood insurance west sacramento
  50.0  flood insurance west palm beach
  50.0  flood insurance visalia
  50.0  flood insurance virginia beach
  50.0  flood insurance victoria
  50.0  flood insurance vero beach
  50.0  flood insurance vancouver
