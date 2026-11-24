# PLAN 4e: do NFIP policy counts predict Search Console impressions per county page?

Run 2026-11-24, read-only. Window 2026-11-01..2026-11-22 (22 days), GSC API, dimension page (and page+query for the city check), rowLimit 25000 (API returned 320 page rows, far under the cap).

## Answer
**Policy count predicts impressions: weakly to moderately, yes in rank order, but the absolute numbers are tiny.** Spearman 0.54 over 329 counties (95% bootstrap CI 0.46..0.63), 0.60 for counties with Planner volume, 0.29 for counties without. The top policy quartile earns 60% of the 2,450 impressions, and all 329 pages together got 16 clicks. VERIFIED (computed this run).

## Method and joins (VERIFIED)
- Live counties: tools/counties.json, 329. Page URL pattern confirmed in dist/sitemap.xml: `https://floodinsurancedata.com/flood-insurance/<slug>/`.
- Policy count: `policy_units` in dist/data/counties.csv (the published file). state/county-queue.json `units` differs slightly (Miami-Dade 362,515 vs 366,669) but Spearman is the same to 3 decimals with either (0.544 vs 0.543).
- Slug-to-policy join: 329 of 329 matched, 0 unmatched. All 329 slugs are in the sitemap. GSC returned no county-pattern page outside counties.json.
- kw flag: `kw` in state/county-queue.json (Planner volume floor from kwp_rank.py): 247 counties kw>0, 82 kw==0, matching the PLAN 4e "247 + 82".
- Pages with 0 impressions are absent from the API: 240 of 329 appear, 89 are absent and treated as 0.
- Spearman uses average ranks for ties (many zeros); interval is a 1,000-resample bootstrap (seed 1).

## Correlation
| Group | n | Spearman | 95% CI | pages with impr > 0 | impressions | clicks |
|---|---|---|---|---|---|---|
| All | 329 | 0.544 | 0.458..0.626 | 240 | 2,450 | 16 |
| kw > 0 | 247 | 0.600 | 0.498..0.694 | 176 | 1,860 | 13 |
| kw == 0 | 82 | 0.292 | 0.086..0.490 | 64 | 590 | 3 |
| Only pages with impr > 0 | 240 | 0.476 | 0.369..0.569 | 240 | 2,450 | 16 |

## Impressions by policy-count quartile (all 329)
| Quartile | Policies | Counties | Impressions | Clicks | Pages with impr > 0 | Median impr | Mean impr |
|---|---|---|---|---|---|---|---|
| Q1 | 50-1,120 | 82 | 174 | 2 | 40 | 0 | 2.1 |
| Q2 | 1,126-3,256 | 82 | 249 | 2 | 53 | 1 | 3.0 |
| Q3 | 3,261-9,448 | 82 | 565 | 5 | 71 | 4 | 6.9 |
| Q4 | 9,686-362,515 | 83 | 1,462 | 7 | 76 | 12 | 17.6 |

Impression-weighted average position: Q1 31.9, Q2 31.0, Q3 30.0, Q4 42.9. Bigger counties get more impressions but not a better rank (Q4 is worse), so the gain is from more queries, not higher positions.

## Split by Planner volume (quartiles within each group)
kw > 0 (247):
| Q | Policies | n | Impressions | Pages > 0 | Median |
|---|---|---|---|---|---|
| Q1 | 50-1,011 | 61 | 113 | 28 | 0 |
| Q2 | 1,017-2,982 | 62 | 150 | 36 | 1 |
| Q3 | 2,998-11,438 | 62 | 341 | 52 | 3 |
| Q4 | 11,519-232,960 | 62 | 1,256 | 60 | 14.5 |

kw == 0 (82):
| Q | Policies | n | Impressions | Pages > 0 | Median |
|---|---|---|---|---|---|
| Q1 | 108-1,494 | 20 | 74 | 13 | 2 |
| Q2 | 1,860-3,806 | 21 | 141 | 17 | 2 |
| Q3 | 3,824-8,827 | 20 | 137 | 16 | 4 |
| Q4 | 8,884-362,515 | 21 | 238 | 18 | 6 |

Reading: the kw==0 group is flatter, and its Q1 median (2) is above the kw>0 Q1 median (0). The 82 no-volume counties do get impressions (590 total, 64 of 82 pages), so Planner zero is not a reliable gate (consistent with ChatGPT round 9). Per page the two groups are about equal: 1,860/247 = 7.5 vs 590/82 = 7.2 impressions (my arithmetic, not tested for significance).

## 15 largest-policy counties with 0 impressions
| County | Policies | kw |
|---|---|---|
| kings-county-ny | 18,645 | 0 |
| ascension-parish-la | 14,070 | 10 |
| glynn-county-ga | 13,680 | 10 |
| orange-county-tx | 11,937 | 0 |
| bergen-county-nj | 10,397 | 10 |
| barnstable-county-ma | 9,828 | 0 |
| hidalgo-county-tx | 9,686 | 10 |
| essex-county-ma | 8,933 | 10 |
| hancock-county-ms | 7,384 | 10 |
| davidson-county-tn | 4,829 | 0 |
| vermilion-parish-la | 4,485 | 10 |
| plaquemines-parish-la | 4,398 | 0 |
| hawaii-county-hi | 4,096 | 10 |
| kauai-county-hi | 3,830 | 0 |
| york-county-me | 3,824 | 0 |

Only 7 of the 83 top-quartile counties have 0 impressions; the largest silent county has 18,645 policies, far below Miami-Dade (362,515), so the very largest counties are never silent.

## 15 smallest-policy counties with the most impressions
Taken from the bottom half of counties by policy count (3,256 policies or fewer), ordered by impressions.
| County | Policies | kw | Impr | Clicks | Avg pos |
|---|---|---|---|---|---|
| st-louis-county-mo | 3,080 | 0 | 53 | 0 | 37.8 |
| salt-lake-county-ut | 1,193 | 10 | 51 | 0 | 46.8 |
| austin-county-tx | 508 | 10 | 14 | 0 | 33.5 |
| elkhart-county-in | 421 | 0 | 13 | 1 | 16.6 |
| sedgwick-county-ks | 991 | 10 | 13 | 0 | 13.4 |
| thurston-county-wa | 765 | 0 | 12 | 0 | 50.8 |
| yavapai-county-az | 1,585 | 10 | 12 | 0 | 37.8 |
| rogers-county-ok | 282 | 10 | 10 | 0 | 47.9 |
| bronx-county-ny | 3,222 | 0 | 9 | 0 | 7.8 |
| ramsey-county-mn | 454 | 0 | 8 | 0 | 15.5 |
| suwannee-county-fl | 467 | 10 | 8 | 0 | 14.9 |
| kanawha-county-wv | 1,262 | 0 | 8 | 0 | 45.2 |
| passaic-county-nj | 2,820 | 10 | 8 | 0 | 44.4 |
| lonoke-county-ar | 219 | 10 | 7 | 0 | 56.1 |
| weber-county-ut | 242 | 10 | 7 | 0 | 17.0 |

Top 10 overall by impressions: manatee-FL 106 (37,694 policies), brevard-FL 82, east-baton-rouge-LA 75, harris-TX 68 (226,917 policies, kw 1,010), st-louis-MO 53 (3,080), pasco-FL 53, salt-lake-UT 51, orange-CA 45, berkeley-SC 45, charlotte-FL 44.

## Edge cases
- **City queries on county pages (VERIFIED, page+query rows):** of 1,397 county-page impressions that carry a visible query, 915 (65%) come from queries that do not contain the county name. Examples: "flood insurance bradenton" and "bradenton flood insurance" on manatee-county-fl (67 together), "flood insurance corpus christi" on nueces-county-tx (21), "flood insurance lake charles la" on calcasieu-parish-la (19), "huntington beach flood zone map" on orange-county-ca (16), "flood insurance biloxi" on harrison-county-ms (16). So county impressions mostly come from city and region searches, which favors counties holding large cities and is part of why policy count (a size proxy) correlates. Google drops anonymized queries from page+query, so 1,397 is a subset of the 2,450 total.
- **Small-county outliers look city-driven (GUESS):** St. Louis County MO, Salt Lake County UT and Bronx NY probably rank for city or borough searches rather than for a large local NFIP market. I did not read their query lists one by one.
- **Zero-impression pages absent from the API:** 89 treated as 0 (stated above). "Median 0" in Q1 means no impressions recorded.
- **Short window, tiny counts:** most pages have under 20 impressions in 22 days, with many ties; the kw==0 CI is wide (0.09..0.49).
- **Possible inflation (GUESS, untested):** pages were built in queue order by policy count (PLAN 4e), so big counties are likely older and have had longer to earn impressions. Publish dates were not checked, so age is not controlled.
- **Correlation is not causation:** policy count is also a proxy for population and coastal search interest; this run does not separate them.

## What this means for PLAN 4e (GUESS)
Policy count is a usable rough prior for whether a county page gets any impressions, but it explains little of the absolute number, and total county-page clicks are 16. The 82 kw==0 pages perform per page like the kw>0 pages, so this data gives no reason to cut them. Bottom-quartile counties average 2.1 impressions in 22 days, so more small counties would add little.

## Not read or not run
- Page publish dates per county (no age control), per-day series, query lists of individual outlier counties, impressions before 11-01.
- Anonymized queries (hidden by Google in page+query).
- No site files edited, no release, no commit.

Scripts (scratchpad, not in the repo): C:\Users\mwoo7\AppData\Local\Temp\claude\3ac6fd66555d38eb\b9cb22b7-94f5-449b-812c-7939e0954e52\scratchpad\pull.mjs and an.py.
