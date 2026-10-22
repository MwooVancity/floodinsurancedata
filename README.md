# floodinsurance

Static data site: for every US place, what NFIP flood-insurance policyholders actually pay, how far
below FEMA's full-risk price, how often it floods, and how to pay less. Public federal data only.

Read `CLAUDE.md` first (the whole spec). Owner decisions and status: `docs/OPEN-ITEMS.md`.
Reader spec + verified dataset catalog: `docs/reader-spec.md`.

## Pipeline
```bash
python -I tools/collect_small.py   # CRS, disaster declarations, housing assistance -> data/
python -I tools/collect.py         # NFIP policies + claims + NRI -> aggregates
python -I tools/build_page.py      # static HTML -> dist/
```
Collector note: page NFIP queries at `$top=1000` with `propertyState` in the filter and NO
`$orderby` (orderby 503s the API), dedupe by id. Sum `policyCount`, never count rows.

Separate from calcscrape and the river site in every way (domain, hosting, Search Console, ads).
