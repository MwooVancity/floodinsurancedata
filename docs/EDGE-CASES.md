# Master edge-case list (11-09)
One line per case: how it breaks, the guard that fails without it. Every guard runs in `release.py` or the cloud job named.
A new data shape becomes a line here and a case in the named test the same day (CLAUDE.md "Labels are claims").

## Input
- Empty, one row, zero units, no claims, one claim, one zone: per-place pages: `test_factory` (no_claims, one_claim, one_zone, zero_units).
- Refund (negative premium), $1 billion value, one-policy state: `test_site_factory` (refund_bucket, billion_bucket, one_policy_state); `test_factory` billion_flood.
- Source reorders rows: "largest/costliest" by file order: `test_factory` shuffled_order + gate C11/C12 rank by value.
- Date edges (Jan 1, Dec 31 as-of; Feb 29 snapshot): `test_factory`/`test_site_factory` asof_jan1/asof_dec31; `test_bulk` Feb 29.
- Leading zeros lost (states 01-09, ZIPs): `pull_bulk` STOP when geoid/ZIP columns are not text.
- FEMA codes 98/99 (claim opened or deleted in error) counted as claims: `test_raw` (code-98 record out).
- Under the 30-priced floor shown as a median: gate C14 on every page; `test_factory` under_floor.
- New FEMA code with no label: `recheck` data dictionary sha; codes.py labels only known codes.
- Address tool: odd FEMA fields, metres, no unit, -9999 sentinel, zone line, open water, FEMA error/silent: `test_zonemap` (22 cases + 3,000 fuzz, Chromium and WebKit), `live_zonemap` nightly vs real FEMA.

## Missing
- Feed down / FEMA 503: refresh stops, last month stays live (`refresh-data.yml`, before the 10th no note).
- First run, file never written (new figure before its data): page prints nothing; `test_factory` new_fields_11_08, cost_trend; `test_site_factory` missing_state, state_not_built, renters_empty, sealevel_empty, map_status_empty.
- Cost trend: old years with no cost on most policies: left out and named (fill 90%, 30 priced); `test_raw`, gate C17.
- Cost trend pass fails mid-way: its files are deleted, no page shows a trend (`pull_bulk` main).
- Older records in other county codes (Connecticut 2022 regions): a year whose policy count is under half or over twice today's is left out and named; `test_raw` 2021 row.
- A feed collected once and never again (county NRI + take-up, collector deleted 10-29): written by the monthly state job again (`collect_state_small.write_detail`, `test_raw`).
- A feed without its own date, or rows with mixed dates: no card, never the download day on it (`test_factory` takeup_no_date; state take-up date only when all rows agree; NRI version from FEMA's `NRI_VER`, two versions = none printed).
- A feed keyed to other areas (Connecticut's planning regions in NRI and take-up): a gap line saying so, never silence or a borrowed figure (`build_page` risk and take-up cards).
- Aid filed under a county name no county matches (spelling): `build_counties.unmatched` stops the build; tribal and school-area aid is printed as not placed.
- FEMA map-date text ("02/19/27(>)", "(NSFHA)", "(M)"): `mapdate.py`, tested in `test_tools`.
- A slow side source (FEMA API) runs the refresh past its limit and the month's main data is lost: side step bounded (75 min) and allowed to fail; policies and claims still commit (11-09).
- A step killed mid-write leaves half a JSON file to commit: side sources write a temp file and swap it in (`_dump`), `*.tmp` ignored.
- Unreachable law page: `recheck` stops the release; manual reads expire at 183 days.

## Scale
- 2,000 pages: live gate ~17 min (re-measure at 500, PLAN); 20,000-file Cloudflare cap stops at 19,000 (daily run).
- Cost trend: 5 extra filtered scans of the 3.7 GB file, ~23 M rows; timeout 150 min on the job.
- Same download twice: `refresh_plan` skips when FEMA's as-of month is unchanged.

## Two writers, two copies
- One single-family rule (`ffcalc.is_sf_home`) for headline, zone, ZIP and trend medians; gate C17 proves trend = headline within $1.
- One writer on master: `site-deploy` concurrency group (refresh + publish).
- One rule text: `rules_registry.py`; pages call `rule()`, never retype.

## Who can't see it
- New page type with no hub links: S16 `linkcheck` (orphan, missing hub, broken link).
- National pages: `test_site_factory` scans garbage text, dead links, llms.txt.

## The check itself is wrong
- Mutation no-op (rule stopped matching after a wording change): `test_gate` refuses a mutation that does not change the page.
- Loose match: every gate has a mutation that must fail (`test_gate`, `town_check --test`, factory must-block cost_trend_off).
- Too strict: gates block only the page that shows something wrong; a new county failing is set aside, the rest ship.

## Readers and Google
- Label vs data ("left out", "only", "costliest", "not final", "since"): gates C10-C17.
- Basis missing (median/mean, premium/cost): A4 (also column headers).
- Near-duplicate / thin: S2 sameness (53% median, 60% max, cap 80%); 11-26 checkpoint.
- Screen 1 too long: phone_check P4 (quote checker inside screen 2 at 390x844).

## Unattended
- A week with nobody: failed runs leave a note on the run page, read at every session start; the live site stays on the last good release; a live page differing from what passed redeploys the previous release.
- Cloudflare token (30 days) and domain (2027-10-23) warnings in the daily run.
