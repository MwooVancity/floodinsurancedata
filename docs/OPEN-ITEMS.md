# Open items — owner decides

Updated 2026-10-22. Technical work is done by Claude; these are the calls only the owner can make.

## Blockers before launch
- [ ] **Domain.** Not chosen. Working folder name `floodinsurance` is local only. (Competitor already
      holds floodfigures.com — pick something else.)
- [ ] **Search Console property** — own property, separate from calcscrape and the river site.
- [ ] **Hosting project** — Cloudflare Pages/Workers, its own project (not calcscrape's).
- [ ] **Publisher name + contact email** for the methodology/about page.

## Later (not blockers)
- [ ] Ads + consent banner — only after a four-week Search Console review passes.
- [ ] Census ACS API key (free) — needed for the take-up rate (share of homes insured).
- [ ] OpenFEMA commercial-reuse inquiry (attribution is required either way; already handled in footer).

## Done
- [x] Reader spec + 8-dataset catalog verified live (`docs/reader-spec.md`).
- [x] Pipeline seeds: `tools/collect.py` (NFIP policies + claims + NRI), `tools/collect_small.py`
      (CRS, declarations, housing), `tools/build_page.py` (static page).
- [x] First page: Lee County, FL (the template all others come from).

## Known data gaps
- NFHL per-address flood zone: ArcGIS point API resets from the dev environment; use client-side link
  to FEMA's Flood Map Service Center. Per-place zone MIX comes free from NFIP `ratedFloodZone`.
- National Risk Index county query: endpoint + fields verified; exact `State_County_FIPS_Code` match
  format confirmed in `tools/collect.py` (else the risk card shows an honest gap line).
