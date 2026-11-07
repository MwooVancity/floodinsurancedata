# Round 79 (LIGHT: page text only, changed parts only; no screenshots, no web search, so no SEO-vs-#1 pass)
Judged: new /flood-insurance/claims/ page + dist/data/claims-2020-counties.csv (inside "home"), the home claims-columns note link, the county "Why do flood claims here go unpaid?" card link (read on palm-beach-county-fl). Other pages: CSS-only change, not re-read; round-78 PASS carried.

## home
1. **MAJOR** claims page, "Left out: 15,151 records FEMA coded "Claim deleted in error" or "Assigned in error", which are record keeping, not claims." The page asserts these records are not claims. Nothing quoted from FEMA supports it: "Claim deleted in error" can as easily mean a real claim removed by mistake, and "Assigned in error" can mean a claim attached to the wrong policy or place. Unsupported inference (truth guardrail 3). The exclusion is stated (good) and 5.4% of records, but the reason is asserted, not sourced. Fix: state only what FEMA's labels say ("FEMA labels these records as deleted or assigned in error; we cannot tell whether a payment belongs elsewhere") and give the effect, e.g. the U.S. share if they were counted as unpaid (about 78.9% vs 83.4%, recompute from raw before printing).
2. **MAJOR** claims page, caveat placement. The headline "83.4% had a recorded payment" and the 68-row table (Terrebonne 52.7%) read as "47% of claims refused". The only statement that recent claims may still be paid ("no field saying whether a claim is still open") is in "What these numbers cannot tell you", below a 68-row table, far from the figure. Caveats must sit beside the figure (checklist C). Fix: one line under the big number and one under the county table heading: "Includes claims from 2020 to August 2026 that may still be open."
3. MINOR the county card (palm-beach) still lists "Assigned in error 432" as a reason claims went unpaid, and its note calls such rows paperwork; the claims page drops code 98/99 entirely. Same data, two bases, and the link goes from one to the other without saying so. Add "the county-by-county page leaves these out" to the card note, or align wording once item 1 is fixed.
4. MINOR table "Not an actual flood" is the top reason in ~35 counties. It is FEMA's label and the page says a reason is FEMA's record, not a finding; acceptable. Page title/H1 "How often do NFIP flood claims get paid?" invites a per-claim chance reading; the closing paragraph denies that. Consider "Share of NFIP claims with a recorded payment".
5. GAP no way to find one's county in a 68-row table (no filter/search, checklist G); "County as coded on each claim record, which can differ from where the building stands" is adequate for the base, but could add that the county pages' own claim counts use the same coding.
6. PASS wording on "No recorded payment does not mean a claim was denied"; no denial language, no advice, no verdict; 500+ claim floor stated; base (losses 2020 on, building/contents/ICC payment above $0) stated; source and as-of date (Aug 31, 2026) shown; reason table says "ten most common", shares use all 44,379 no-payment claims as base; US table sums to 44,155 of 44,379, rest unlisted but disclosed by "ten most common". CSV columns match the page (spot-checked first rows: Terrebonne 603 / 318 / 52.7%). Home link text "How often claims get paid, county by county" is clear.
Verdict: FAIL

## louisiana
Not re-read (CSS only; round-78 PASS carried).
Verdict: PASS

## palm-beach-county-fl
Card link "How often claims get paid, county by county" present and works; see home item 3 (MINOR). Palm Beach has 426 recent claims, below the 500 floor, so it is not on the claims page; the link text does not promise it is.
Verdict: PASS

## new-york-county-ny
Not re-read (CSS only; round-78 PASS carried).
Verdict: PASS

## fairfield-county-ct
Not re-read (CSS only). It appears on the claims page (862 claims, 81.9%), figures match the CSV row format.
Verdict: PASS

## santa-rosa-county-fl
Not re-read (CSS only). On the claims page: 1,323 claims, 80.7%.
Verdict: PASS

## Classes
- Home/new claims page: unsourced "not claims" assertion; open-claims caveat not beside the figure.
- County template: the unpaid-reasons card counts codes 98/99 as reasons; the claims page excludes them (basis difference, link does not say so).

## Previous items
Round 78: all seven pages PASS, no BLOCKER/MAJOR recorded. Nothing to mark.
