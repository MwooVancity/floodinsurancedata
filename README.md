# floodinsurance

Static data site: for every US place, what NFIP flood-insurance policyholders actually pay, how far
below FEMA's full-risk price, how often it floods, and how to pay less. Public federal data only.

Read `CLAUDE.md` first (the whole spec). Owner decisions and status: `docs/OPEN-ITEMS.md`.
Reader spec + verified dataset catalog: `docs/reader-spec.md`.

## Build (one command)
```bash
python -I tools/build_all.py
```
Builds every county in `tools/counties.json` (collect → NRI → render → gate), then the site
(home, methodology, data CSV, sitemap, robots, llms.txt). Resumable: re-running skips built counties.
Set `FF_BASEURL=https://yourdomain` before the run so canonicals/sitemap/JSON-LD carry the real domain.
Add counties by appending to `tools/counties.json`. `tools/gate.py` fails the build on any bad page.
Collector note: page NFIP queries at `$top=1000` with `propertyState` in the filter and NO
`$orderby` (orderby 503s the API), dedupe by id. Sum `policyCount`, never count rows.

Separate from calcscrape and the river site in every way (domain, hosting, Search Console, ads).
