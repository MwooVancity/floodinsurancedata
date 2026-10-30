# PLAN: floodinsurancedata.com
Rules live in CLAUDE.md. This file is the state and the next moves only; history is in git and
`docs/archive/PLAN-2026-10-29.md`. Keep it under 80 lines: when a line is done, delete it.

## First, before any work: ponytail (owner 2026-10-29)
Does it need to exist? Does a sentence on the page already answer it? Is it in the code already, or does the
browser already do it? Only then the least code. Tests scale with harm; reviews only where a reader could be hurt.

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
1. Search Console: connected; re-read weekly. Owner: click "Validate fix" on the Datasets report.
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
   - Deadline planner: LIVE 2026-10-29 on louisiana, palm-beach-county-fl, broward-county-fl (staged; round 21 PASS).
     Go to "all" in tools_flags.json on 2026-11-12 if no errors or complaints; then fix the round-21 MINORs. Was: proof of loss +60 days; FEMA aid window from the DECLARATION date (source first);
     guards: future/empty date, local-date parsing, past 60 days, private policies set their own deadlines.
   - (Ponytail 10-29: first try a "compare with" link that opens two county pages; build a tool only if that falls short.)
   - Compare two places: published places only, same level, base labelled, "too few", one lazy JSON (size cap),
     stacked on a phone, numbers only, no "safer/cheaper".
   - Decode my policy page: FEMA field names; clean $ and commas; flag monthly-for-yearly and out-of-range;
     premium vs premium-only median, deductible vs mix, coverage vs $250,000, zone in plain words; FEMA's own
     pay-less text only. Photo reading later, in-browser only, reader confirms each value.
   - Renewal-jump check: DROPPED by the ponytail ladder (the cap rule is already on the page; risky). Was: premium only, reasons listed before any
     comparison (coverage change, lost discount, non-primary 25%, new map, lapse), never "illegal".
3d. Links (owner 10-29), guards first: a monthly outside-link checker that stops a release on a dead link; outside
   links only to .gov or FloodSmart (gate); 3-5 related links per page chosen from data, never a fixed block; link
   text names the destination. Add: DisasterAssistance.gov beside the aid rule; FEMA's provider finder beside "how to
   buy"; state insurance department (needs a sourced list of 51); "compare with" a bordering county.
3e. LIVE 2026-10-29: county flood-map dates and new-map notices (FEMA CSB, all six value shapes handled, unknown
   stops the build); NOAA sea-level trend on county pages with a gauge inside the county (round 28: a bordering
   county can be on the other coast). Both refresh monthly. OPEN: sea level on state pages.
4. Links: build ONE data story from data we hold ("counties paying furthest below FEMA's full-risk price").
   Done when it is live. Pitching it to local news needs the owner (outreach is outbound).
5. Pace: 20 a day now (owner). After 4 weeks of step-1 data: 25 if most pages are indexed; drop to 10 if not; stop if
   site-wide impressions fall. Done when the decision and its numbers are written here.

## Scale guard (measured 2026-10-29: full build 165 s for 103 pages, about 1.6 s a page)
A daily full rebuild at 2,000 pages is about 55 min a day, over GitHub's free compute. BEFORE 400 live pages: the daily
job builds only the new counties, the states that list them, home and sitemap (about 3 min); the full rebuild runs
monthly after the refresh. Tool fuzz runs on one page; presence on all. Flagged-page reviews: weekly batch, cheap model, capped.

## Every month, every year (edge cases first; the jobs run themselves, sessions check them)
What can break, and the guard already in place (or OPEN):
- FEMA API down, slow or renamed fields: pull_raw stops before agg_raw, so the site keeps last month's data and the
  as-of date ages. A median moving more than 25% stops the commit (`jump_check.py`); a session looks, then reruns.
- A state's count stops matching: that state's claims re-pull in full; still wrong = refresh stops, nothing half-written.
- GitHub: the claims cache can be evicted (10 GB): the next run pulls in full (slow, not wrong). $12 compute: ~5 h/month used.
- FEMA wording or rule pages change: recheck.py re-fetches every rule excerpt each release; a missing excerpt stops it.
- A big storm: claims, events and disaster lists grow on their own; no code change. Check the events lead that week.
- Congress lets the NFIP lapse (reauthorization deadlines, often Sep 30): OPEN, add a sourced "no new policies during a
  lapse" rule the day it happens. January: year ranges, "since 1978" and decade labels roll over; check one page.
Calendar:
- Daily: 20 reviewed counties published (queue of 1,803 done about late January 2027); next session reports deploys.
- Weekly: read Search Console (`tools/gsc_read.mjs`), write the numbers in the scoreboard.
- Monthly, the 3rd: FEMA refresh; check time, size and 51 states done.
- Quarterly: one light review of the template on the 3 samples; prune any line in this file that is done.
- Yearly: domain renewal (owner); NRI and Community Status Book updates (refresh picks them up); NFIP lapse watch.
Milestones: 2026-11-03 first refresh check -> 11-12 deadline planner to all pages -> 11-26 four weeks of Search Console
data decide the pace -> late January 2027 queue done -> decide ZIP pages and AdSense from the numbers.

## Helpfulness checklist A-N (lines in docs/HATER-PROMPT.md; every review judges all 14)
Round 18-21: A, C, D, E, H, J, M, N pass. OPEN: B renters/landlords/second homes/business lines; F state insurance
department contacts; G table search; I error-report contact (owner); K print layout; L Spanish.

## Parked: ZIP pages (after counties index well); Spanish, state contacts, print layout (slower than steps 1-4);
AdSense (after four weeks of Search Console data; owner decides).
