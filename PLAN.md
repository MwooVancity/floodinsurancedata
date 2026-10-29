# PLAN: floodinsurancedata.com
Rules live in CLAUDE.md. This file is the state and the next moves only; history is in git and
`docs/archive/PLAN-2026-10-29.md`. Keep it under 80 lines: when a line is done, delete it.

## Goal and scoreboard
The most helpful flood-insurance page for every US county, for a scared reader on a phone (user, not Google).
Scoreboard, the only measure of progress: pages indexed · impressions · clicks · queries on page 1 · AI citations.
Today: all five UNKNOWN. That is the bottleneck. Work that cannot move the scoreboard waits.

## Where we are (2026-10-29)
- Live: home + 51 states + 52 counties + 404 (111 pages), template reviewed (light round 18 PASS), live gate clean.
- Queue: 1,803 counties pass the build; the daily GitHub job publishes 10 reviewed ones a day (25 max per release).
- Data: as of 2026-07-31; monthly cloud refresh on the 3rd (claims carry over; only the last 3 loss years re-pulled).
- Reviews: no wrong live figure in rounds 12-19 (round 19 caught an overstated new figure before release); open defects are wording and layout.

## Next moves, in order (each has a "done when")
1. OWNER, 10 minutes: Search Console access for Claude (or read it). Done when impressions, clicks and the top
   queries per page are written here, with a date. Repeat weekly. Until this exists, steps 4-5 are guesses.
2. 2026-11-03 refresh run: check time, download size and all 51 states done. Done when the numbers are here.
3. One batch after step 2, then one light check (≤ ~90k tokens) and release:
   - search boxes on tables with 16+ rows, with a "no matches" line;
   - "Outside a high-risk zone?" line on the "Am I required" card, worded "of paid claim dollars", with its period;
   - take-up (homes with flood insurance): verify the penetration source, then show it or delete the idea.
4. Links: build ONE data story from data we hold ("counties paying furthest below FEMA's full-risk price").
   Done when it is live. Pitching it to local news needs the owner (outreach is outbound).
5. Pace: after 4 weeks of step-1 data, 25 counties a day if most pages are indexed; hold at 10 if not; stop if
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
