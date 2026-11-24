# Thin pages draft (PLAN 4f), 2026-11-24. Draft only, nothing applied.
Labels: V = read in a file this run; G = guess.

## Finding that changes the ZIP verdict
V: /flood-insurance/zip/ is a lookup whose answer is drawn by JS (builder tools/build_site.py ~l.1410-1458, `_zjs` + `pg`). The crawler's 241 words is the static shell only; a ZIP searcher sees an empty box until they type. The page has no answer sentence, no sample result, no "what the data cannot say" beyond one grey paragraph.
V (computed from dist/data/zip/*.json this run): 25,541 ZIPs listed; 7,201 have a ZIP median (floor ZIP_MIN=25 priced single-family policies, tools/ffcalc.py:32); 18,340 have none. Those 7,201 ZIPs hold 4,190,844 of 4,500,639 policy units (93.1%). So most ZIPs show "too few", but almost all policies sit in ZIPs that show a median. 617 ZIPs list 2+ counties with 10+ units each (3,920 list 2+ counties at all, most with 1-7 stray units).

## 1. /flood-insurance/zip/ (priority): EXPAND
Tests. Helpful: reader gets an answer before typing. Gain: ZIP-level median plus its policy count and the county comparison, which a ZIP query's top results (G, not checked this run) mostly give as one blended figure. HCU: real data, source and as-of shown, gap stated, no filler.
Add, in order (all computed in the builder's ZIP block where `_z3` is built, injected through the existing f-string `pg`; no hand-typed figure):
1. Answer sentence under the h1, built at build time: "Of the {N_ZIP:,} ZIPs in FEMA's NFIP policy records, {N_MED:,} have enough priced single-family policies ({ZIP_MIN}+) to show a ZIP median; those hold {SHARE}% of all policy units." Owner: new variables N_ZIP, N_MED, SHARE computed next to `_z3` (counted from `_z3`, the same dict the JSON files are written from, so page and files cannot disagree); ZIP_MIN imported already; number formatting via the page's existing formatters. Label base: "policy units, all building types" vs "priced single-family policies" stay separate, as the current note does.
2. Plain-words "how to read your result" under the form: median is premium plus fees, existing policies, one year; a ZIP below the floor gets the county figure labelled as the county. Owner: the existing grey note, rewritten as a short list; its numbers already come from `{ZIP_MIN}` and `{_ASOF_TXT}`.
3. Worked example, server-rendered so it also counts as page text and shows without JS: pick the ZIP with the most policy units from `_z3` and render it with the same `say()` logic ported to Python (or call the JS Python oracle in tools/test_ziptool.py, V: named in the comment l.1412). Owner: a small build-time function `zip_example()`; the figures are read from `_z3`, never typed. Edge: the example ZIP must have a median (pick max units among ZIPs with median not None) and one county.
4. "What this cannot tell you" card (the site's standard heading, as on the LOMA guide, V): not your premium, not your flood zone (link /flood-zone-map/), not a quote, not private-insurer prices, and a ZIP can cross counties. Owner: static text; any rule sentence through `rule("price_drivers")` already present.
5. Multi-county ZIP: the JS already lists each county (V, say()). Add one build-time sentence only if the count is a computed figure ("{N_MULTI} ZIPs appear in more than one county in FEMA's records, most with a handful of stray policies"); G: stray policies are mis-entered counties, which the page already says as a hedge ("may have been entered with the wrong county"), so keep that wording, do not upgrade it.
Edge cases:
- Invented number or law: every figure from `_z3`/`ZIP_MIN`/`rule()`; test = a gate that every digit run in the new block appears in the data or constants (G: gate C-series may already do this; not read).
- Null medians: example picks a ZIP with a median; the 18,340 without keep the existing "too few" text (V, say()). Test: tools/test_ziptool.py case for a null-median ZIP and a multi-county ZIP.
- Base labels: "policy units" (all types) vs "priced single-family policies" kept distinct in sentence 1.
- Zero results (ZIP not in file): existing message "No NFIP policy in FEMA's records lists ZIP" stays; do not imply the ZIP has no flood risk (add "That does not mean no flood risk" as static text; G on wording, owner reviews).
- Template text: this is a one-page template, not county/state, but still goes in the day's single batched release (CLAUDE.md Site).
Page-size: G, about 150-250 words static added; enough to be visible text, not padding.

## 2. /data/ (117 words): EXPAND slightly, one sentence block
Tests. Helpful: a downloader needs the columns and base. Gain: column definitions with bases (V: the CSV has 14 columns incl. median_cost, p25/p75/p90, full_risk_median, share_below_full_risk_pct, claims_since_1978, avg_paid_claim_usd, closed_no_payment_pct, builder l.~405). HCU: documentation of a real file.
Add: a column table built from the same `w.writerow([...])` header list (reuse the list, one source), each row naming base and unit (e.g. median_cost = premium plus fees, single-family, per year: confirm each against the agg code before writing, G until read); as-of date via `_ASOF_TXT`; the 25 ZIP-prefix JSON files are NOT offered (not a product) unless wanted. Edge: a blank cell means not available (already said); county floor 30 stated via the constant, not typed. Do not link-farm.

## 3. /terms/ (217 words): KEEP THIN on purpose
Legal page, no search demand, no reader question; padding it fails HCU. Only change worth making: it says "Last updated {RETR}" (V), confirm RETR is the date the text last changed, not the data retrieval date (G: could be mislabelled; check before the next release). No expansion.

## 4. /guides/ hub (117 words): EXPAND lightly
Tests. Helpful: a reader choosing between 10 guides needs one line each. Gain: low but real (each guide's own lede). HCU: hub with only link text is the thin pattern.
Add: under each link one sentence, taken from each guide's own computed answer line, not hand-written; the builder already collects `GUIDES` as (url, title) tuples (V, l.~1188), so extend the tuple with the guide's answer sentence where each guide builds. Order the list by the reader order in CLAUDE.md (risk, required, cost, ...). Edge: a guide that fails to build drops out of the list (existing behavior, V); a one-line summary must come from the same variables as the guide so hub and guide cannot disagree. Do not add a link block elsewhere.

## Not read
Live pages were not fetched (read dist/ copies, which the crawl report matched on word counts); top-3 SERP for "flood insurance rates by zip code" not checked; gates (tools/gate.py) and test_ziptool.py contents not opened; the Search Console figure (3 clicks, 31 impressions) was taken from the task text, not queried.
