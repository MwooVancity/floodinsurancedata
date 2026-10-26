# Master prompt: make floodinsurancedata.com the #1 result

Run this prompt in order, one step per session. Each step ends with release.py passing, a deploy, release.py --live, and a commit and push.

## The reader and the test
The reader is on a phone, scared or about to sign: a renewal that jumped, a house they want to buy, a mortgage letter saying "flood insurance required", water already in the street. They give the page 60 seconds. A step is done only when a page answers that reader's question **with a local number nobody else in the top 10 shows**. Showing that reader anything wrong is the one failure that cannot be undone, so the gates come before any gain.

## Our edge (say it on every page; never fake it)
We download **every** NFIP policy and claim record FEMA publishes for a place, reconcile the count with FEMA's own total, and compute every figure ourselves. Competitors use FEMA summary averages (and disagree by up to 54% for the same state) or modelled numbers. Every page states its record counts (gate G1), ships its figures as data.csv, and carries Dataset schema with measurementTechnique and a CSV distribution.

## Step 1: finish what is computable from the download (no new data)
Each item becomes one card with a ≤40-word answer-first lead, a source line, and metrics registered in metrics.py. Order:
1. Local figure next to the state and U.S. figures in the first tile row, plus the county's cost rank in its state.
2. Lender-required vs voluntary share (`mandatoryPurchaseFlag`).
3. Elevated vs not elevated: premium and average claim paid.
4. What floods here: cause of damage. Water depth stays OFF (mixed units) until a unit check passes.
5. Renters and condo owners: tenant, condo-unit and RCBAP shares.
6. What is in the bill: average federal fee, HFIAA surcharge, reserve fund, ICC premium.
7. Deductible choice: the shares, used to strengthen the quote checker.
8. Grandfathered and legacy discounts still in force.
9. ICC payouts: count and average.
10. New vs older policies (RR 2.0 start). **Blocked until** rules_registry has an official excerpt for the October 1, 2021 start date.
11. Claims-by-year chart with named storms labelled on the bars.

## Step 2: the FEMA workbooks (small keyless downloads)
- Official policies-in-force count and 12-month trend per state.
- Official FY denial (closed-without-payment) rate.
- Premium vs losses by community (HUDEX).
- Policy and loss by zone.

Pin FEMA's official row on top of the state table, and reconcile our count with theirs on the page.

## Step 3: the pages the search results leave open
- About 10 flood-zone pages (A, AE, AH, AO, V, VE, X shaded and unshaded, D) with real national and state numbers. 8 of 9 results for "zone X meaning" are spam today.
- County pages for every county above a policy floor. Rollout: 25, then all.
- ZIP rows inside the county page. A ZIP page only where its numbers differ from its county.
- Event pages for the biggest `floodEvent` values (Ian, Harvey, Ida, Katrina, Sandy).

The programmatic rule applies to all of these: no two pages more than 80% the same text, and every page has 3 to 5 links to related pages.

## Step 4: the downloads that only a few sites use
IHP "did people who had flood insurance get FEMA aid", seller-disclosure law by state (hand-keyed with a statute link), community map date and NFIP status, buyouts (HMA), NOAA high-tide flooding days, levees (USACE NLD), private-market size (state DOI).

## Step 5: the Search Console loop (weekly, after Search Console is connected)
Pull the queries for each page. For a query at position 8 to 30, with impressions, that the page does not answer in its first screen, add or move the card that answers it. Never write prose for a query. Never put a year or "best" in a title. lastmod moves only when the data changes.

## Gates (never loosened to ship)
Builds, numbers true (metric registry, claims, invariants, G1 provenance, recheck), live and usable on a phone (phone_check). A defect found twice becomes a gate check with a mutation in test_gate.py.
