# Master prompt: build and fix floodinsurancedata.com with real QC

Owner 2026-10-27: "our site is pure garbage. we have no qc." This is the ONE work brief. Give it whole to any
session or agent that builds or fixes pages. `CLAUDE.md` is the spec (reader, datasets, page types);
`docs/HATER-PROMPT.md` is the reviewer's brief and stays separate, because the reviewer must not be the builder.
Older prompts are in `docs/archive/` and are history, not orders.

## Why QC failed (round 5, 2026-10-27: 5 blockers, 14 majors on the 3 sample pages, 93 pages live)
1. **Gates checked consistency, not truth.** V2 proves a number equals the data at its path. It never asked whether
   that path means what the label says. "A new policy costs about $1,466" pointed at full-risk median + mean fees for
   EXISTING policies; new buyers really pay $1,139. It passed every gate.
2. **Rules were written from a summary, with no effective date.** The Citizens rule said "any zone" today; it is
   true only from 2027 for homes under $400K outside the high-risk zone, and left out the 2023 rule inside it.
3. **Reviews ran before fixes.** 7 of 15 round-4 BLOCKER/MAJOR items were NOT FIXED at round 5. Each round cost
   ~200k tokens to re-find known defects.
4. **Failed pages stayed live.** `--hotfix` skipped the review to remove wrong text, and pages that never passed
   stayed up.

## The loop (in this order, every time; no step skipped)

**Step 0. Stop the harm.** Any BLOCKER that is wrong live text a reader could act on (a wrong rule, a wrong price
direction) is fixed or deleted from the live site first, via `python -I tools/release.py --ship --hotfix "<reason>"`.
A hotfix may only remove or correct the text a review named, nothing new.

**Step 1. Work the open defect list, not a new review.** The list is the latest `state/reviews/hater-round<N>.md`
(its page sections, `## Classes` and `Previous items`). For every BLOCKER and MAJOR, write one line into
`state/reviews/fixlog-round<N>.md`: defect, root cause layer (data, metric definition, rule, template, missing
card), the fix, and the proof (the file and line, the recomputed number, the URL). No line = not fixed. A defect is
fixed at its source for every page (a class), never patched on one page.

**Step 2. Every screen-1 figure gets a meaning check (truth QC, new).** For each figure a reader acts on (median,
new-buyer price, renewal price, below-full-risk share, unpaid share, required-to-buy share), `tools/metrics.py`
holds a plain definition: who is counted, which FEMA field, which time window, which policy types. Then a separate
script recomputes it straight from the raw files in `.cache/raw/` with no shared code (`tools/truth_check.py`, to
be written; it must not import `ffcalc`, `agg_raw` or `metrics`), and fails if the page's number differs or the
label's words ("new", "renewal", "single-family", "all policies") do not match the definition's population. Each
mismatch class found gets a mutation test in `tools/test_gate.py`.

**Step 3. Every rule gets a date check (law QC, new).** Each `rule()` in `tools/rules_registry.py` carries:
effective date, any phase-in end date, who it covers and who it does not, the official source URL and the exact
quoted sentence it rests on (from WebSearch or the official page this session, never memory). A rule whose
coverage changes on a future date must say both states on the page ("until Jan 1, 2027 ... from then ...").
`recheck.py` re-fetches each quote; a missing quote fails. One rule = one home on the page: the short form links to
the long form and may not contradict it.

**Step 4. Beat #1 before review (SEO QC).** For each page type, the builder runs the hater's SEO step itself first:
WebSearch the real query, list what the top 3 give (price drivers, ways to lower the bill, a quote check, an average
that reconciles with ours), and either show it from our data or print a gap line naming why no public data holds
it. Write that list into the fixlog. No review is requested while a known #1 gap is unanswered.

**Step 5. Gates, once.** `python -I tools/release.py` (build, every gate, truth check, mutation suite, phone check,
Google gate). Batch all fixes first; run the gates once, not after each edit.

**Step 6. Review only when the fixlog is complete.** A review round starts only when every prior BLOCKER/MAJOR has a
fixlog line with proof. Small fix (only some cards changed): a cheap delta check on those cards only. Template
rework: one full round on the 3 samples (`hater.py prep` -> fresh agent -> `hater.py record`). The reviewer reads
the fixlog only AFTER writing its own defect list, and marks each item FIXED / NOT FIXED with evidence.

**Step 7. Ship only on PASS.** `python -I tools/release.py --ship`. Pages without a current PASS (`review.py ok`)
are not indexable. Live pages that fail a later round get Step 0, then this loop.

## Defects found = new checks, same day
Every defect class a review finds becomes, in this order of preference: a builder rule (wrong text impossible),
a truth-check definition, a rule date/quote, or a gate check with a mutation test of the shipped bug. A class that
becomes none of these is written in the fixlog with why. That is how the next review starts higher.

## Hard rules for the builder
- Never type a number, date, law or source into a template (`tp()`, `m()`, `claim()`, `rule()` only).
- Never fake or estimate a figure; null and a printed gap line beat a guess.
- Never call anything fixed, live or passing without the file, recompute or live page checked this turn.
- One background job at a time; no polling; ship only via `release.py`; never push or run wrangler by hand.
- No caps on helpful cards; delete only wrong, repeated, padding or no-mechanism text (CLAUDE.md, Musk steps).
- The same paragraph never appears twice on a page; shared definitions live on `/methodology/` with a one-line
  link, so pages differ by their data, not by name swaps.

## Current work queue (from round 5; tick in the fixlog, not here)
1. Step 0: Citizens rule (home + every Florida page) and the new-policy price / "quote can land high" claim.
2. New-buyer median from `originalNBDate` in the last 12 months; renewal median separately.
3. Home page: price drivers, ways to lower the bill (deductible, elevation data already in extras), quote check,
   a mean that reconciles with the averages top results show.
4. County "why sites differ" table: the mean and all-types rows the state table has.
5. Official FEMA policy-count comparison (PIF workbook) on every page, or delete the "not yet compared" line.
6. Event table: catch-all FEMA labels kept, with year fallback (Louisiana 1995).
7. Explain zones that share one price (mass point), partial claim years flagged, download dates agree, v2/v3 URLs agree.
8. One NRI definition per page; ZIP town labels never blank; "full-risk price" explained in plain words on screen 1.
9. Broward and Palm Beach: own quick review after the samples pass (flagged by `review.flags()`).
