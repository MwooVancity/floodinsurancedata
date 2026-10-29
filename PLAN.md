# PLAN: floodinsurancedata.com
Rules live in CLAUDE.md. This file is the state and the next moves only; history is in git and
`docs/archive/PLAN-2026-10-29.md`. Keep it under 80 lines: when a line is done, delete it.

## Goal and scoreboard
The most helpful flood-insurance page for every US county, for a scared reader on a phone (user, not Google).
Scoreboard, the only measure of progress: pages indexed · impressions · clicks · queries on page 1 · AI citations.
2026-10-29 (Search Console, data 10-23..10-27): 101 impressions, 1 click, average position 46; sitemap 110 read, 0 errors;
louisiana "Submitted and indexed". Top queries: Arkansas, Florida (position 19.5), Utah. Read: `tools/gsc_read.mjs`.

## Where we are (2026-10-29)
- Live: home + 51 states + 52 counties + 404 (111 pages), template reviewed (light round 18 PASS), live gate clean.
- Queue: 1,803 counties pass the build; the daily GitHub job publishes 20 reviewed ones a day (owner 2026-10-29; 25 max per release).
- Data: as of 2026-07-31; monthly cloud refresh on the 3rd (claims carry over; only the last 3 loss years re-pulled).
- Reviews: no wrong live figure in rounds 12-19 (round 19 caught an overstated new figure before release); open defects are wording and layout.

## Next moves, in order (each has a "done when")
1. Search Console: DONE (the calcscrape service account already has owner access). Re-read weekly; owner clicks
   "Validate fix" on the Datasets report (the citation fix shipped 10-29; louisiana was last crawled 10-26).
2. 2026-11-03 refresh run: check time, download size and all 51 states done. Done when the numbers are here.
3. One batch after step 2, then one light check (≤ ~90k tokens) and release:
   - search boxes on tables with 16+ rows, with a "no matches" line;
   - "Outside a high-risk zone?" line on the "Am I required" card, worded "of paid claim dollars", with its period;
   - take-up (homes with flood insurance): verify the penetration source, then show it or delete the idea.
3b. Same batch: (i) a gate check + mutation for each defect class found in rounds 16-19 (CLAUDE.md rule, not yet
   done; biggest miss); (ii) round 13-19 MINORs: condo "leave both out", overstated glide wording where the gap is
   tiny, Maine duplicate disaster line, "Assigned in error" vs "Claim deleted in error", thin zones in the dropdown;
   (iii) glossary of terms used on the page (FEMA wording, sourced); (iv) one line each for renters, landlords,
   second homes and businesses; (v) ZIP names: "near <place>" fallback where no place covers 25%.
3c. Reader tools (owner 2026-10-29 "do it all"; ship standard in CLAUDE.md: oracle, edge suites, fuzz, kill switch, staged), lowest risk first, each with a script that types edge cases into
   the real page (permanent release check) and one light review. All: nothing leaves the phone, rules from
   rules_registry, numbers tagged, no verdict words, below the quote checker, readable without JavaScript.
   - Deadline planner (flood date in): proof of loss +60 days; FEMA aid window from the DECLARATION date (source first);
     guards: future/empty date, local-date parsing, past 60 days, private policies set their own deadlines.
   - (Ponytail 10-29: first try a "compare with" link that opens two county pages; build a tool only if that falls short.)
   - Compare two places: published places only, same level, base labelled, "too few", one lazy JSON (size cap),
     stacked on a phone, numbers only, no "safer/cheaper".
   - Decode my policy page: FEMA field names; clean $ and commas; flag monthly-for-yearly and out-of-range;
     premium vs premium-only median, deductible vs mix, coverage vs $250,000, zone in plain words; FEMA's own
     pay-less text only. Photo reading later, in-browser only, reader confirms each value.
   - Renewal-jump check: DROPPED by the ponytail ladder (the cap rule is already on the page; risky). Was: premium only, reasons listed before any
     comparison (coverage change, lost discount, non-primary 25%, new map, lapse), never "illegal".
4. Links: build ONE data story from data we hold ("counties paying furthest below FEMA's full-risk price").
   Done when it is live. Pitching it to local news needs the owner (outreach is outbound).
5. Pace: 20 a day now (owner). After 4 weeks of step-1 data: 25 if most pages are indexed; drop to 10 if not; stop if
   site-wide impressions fall. Done when the decision and its numbers are written here.

## Deleted 2026-10-29 (Musk step 2)
- Five dead tools with no callers: collect_county_small, collect_penetration, collect_stormevents, finish_states, gen_counties.
- Full review rounds as the default: scripts first, then one light check per batch (CLAUDE.md budget).
- The premium-rise calculator and the paid-referral idea (owner: too risky until a licensing check).
- 140 lines of this plan (session logs and finished batches, now in docs/archive).

## Helpfulness checklist A-N (every review judges every line; detail in docs/HATER-PROMPT.md)
- A: screen 1 answers how much, am I required, how fast, does it pay out, is my quote normal. PASS (round 18).
- B: every situation served (buyer, renewal, flooded, condo...). Renter, landlord, second home, business: OPEN.
- C: truth (figures equal the source, bases named, no contradictions). PASS.
- D: confusion traps (codes, bases, "too few"). PASS.
- E: plain language. PASS.
- F: action and contacts. Phone, claims, deadlines: PASS. State insurance department contacts: OPEN.
- G: phone UI. Table search: OPEN (step 3). Everything else PASS.
- H: accessibility. PASS (text check only; no screen-reader test run).
- I: trust (anonymous by choice, sources, methodology). Error-report contact: OPEN, owner decision.
- J: navigation (menu, breadcrumbs, bordering counties, 404). PASS.
- K: speed. PASS. Print layout: OPEN.
- L: Spanish. OPEN, large.
- M: freshness. PASS.
- N: consistency across pages. PASS.

## Parked (not now, and why)
- ZIP pages: only after counties index well (step 5).
- Spanish, state contacts, print layout: real but slower than steps 1-4.
- AdSense: after four weeks of Search Console data; owner decides.
