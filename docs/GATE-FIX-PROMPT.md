# Master prompt: every edge case fixed at its source, every feed (owner 11-09)
Paste as the task, or run it whenever a reviewer, the owner or a live read finds something the gates passed.
Rules it obeys: CLAUDE.md (Truth, Labels are claims, Every fix) and `docs/EDGE-CASES.md` (the master case list).

---

You are fixing a class of defects, not one page. A page shipped something wrong, mislabelled or misleading and every
gate passed it. Gates passing is not proof: the gate was wrong too. Work these steps in order and finish them all in one batch.

1. **Name the defect in reader words.** What would a homeowner believe that is false? Quote the live sentence and the
   page. If wrong text is live now, ship the fix first with `release.py --ship --hotfix "reason"`, then do the rest.
2. **Find every page with it.** Script a search over all of `dist/`, not the sample. Report the count: pages hit / pages
   built. One hit is never the whole class.
3. **Trace it to its source, the one place it is made.** Walk the chain: FEMA raw field -> `pull_bulk`/`agg_raw`/
   `extras_raw` -> `data/` JSON -> `metrics.py` -> `build_page.py`/`build_site.py` (`tp()`, `rule()`, `claim()`) -> page.
   Name the first link where truth was lost: a raw field misread, the wrong base, a dropped row, a file-order pick,
   a rule paraphrased, a label the data does not support. Fix it there. Never patch the page, the template text or a
   single slug. If two places make the same figure or rule, delete one (one rule, one writer).
4. **Ask why the gate missed it.** Usually it checked number = data but not label = data, or its pattern stopped
   matching after a wording change. Either fix that check or add one (gate.py C-series for labels, V/A for numbers,
   `town_check`, `linkcheck`, `phone_check`). A check blocks only a page that shows something wrong; everything else ships.
5. **Prove the check with a failing test first.** In `test_gate.py`, a mutation that puts the defect back must FAIL the
   gate (`rsub()` asserts the page changed; a no-op mutation is refused). Too-loose test: would it also pass a correct
   page that says something slightly different? Too-strict test: run it on all built pages; zero false blocks.
6. **Run the edge-case sweep on the fixed code.** For each line of `docs/EDGE-CASES.md` that applies, add the shape:
   per-place data in `tools/test_factory.py`, national pages in `tools/test_site_factory.py`, cloud aggregation in
   `test_raw.py` / `test_bulk.py`, the address tool in `test_zonemap.py`. Always try: empty, one row, zero, huge (1e9),
   negative, reordered rows, a missing file (first run), date edges (Jan 1, Dec 31, Feb 29), a code FEMA adds later,
   a place with too few policies (under 30 priced), and the label words ("left out", "only", "since", "costliest",
   "not final", "largest") against the rows under them. A new shape that applies gets a line in EDGE-CASES.md.
7. **Recompute independently.** For any figure touched, recompute it from raw by a second path (`recheck.py`, an
   oracle in the test) and compare. Disagreement = stop; find which is wrong before shipping either.
8. **Write the fixlog line.** `state/reviews/fixlog-round<N>.md`: defect, root cause (the link from step 3), fix, the
   gate or test that now fails without it, pages hit (count).
9. **Ship and read it live.** `ast.parse` every edited file; one `release.py --ship` (gates, truth proof, mutations,
   factories, phone, Google gate); one light review only if visible text changed (`hater.py prep <N> <slugs> --local
   --light`, or `hater.py carry <N> passed` when the text is unchanged). Then read the real live URL of one hit page
   and quote the fixed sentence. Commit and push.

Report: the defect, its source, pages hit, the new check and its failing mutation, edge shapes added, live proof.
End with "Nothing left missing." only when every step above is done and seen.

## The feeds (this site's "gauges")
The river site's unit is a gauge; here it is a place's feed: one county's or state's rows in each dataset. Run steps 2-9
for any feed that breaks, and sweep every feed below for its traps once a month (after `refresh-data.yml`) and whenever
a source changes format. For each feed check: it arrived (rows = the source's own count), it is the right place
(geoid as text, the right county), it is the right base (label says which), and a missing or short feed prints nothing,
never last year's figure under this year's date.
- **NFIP Policies v3:** SUM `policyCount`, never count rows; negative premiums are refunds; condo units out of the
  single-family base; territories out; geoid text with leading zeros; older records may use other county codes
  (Connecticut 2022 regions); costs on past snapshot days may be missing (trend fill rule).
- **NFIP Claims v3:** codes 98/99 are not claims; `countyCode` may not be the property's county; the last two years are
  not final; catch-all event names ("Flooding") span many floods; dollars of the day.
- **FEMA NRI:** ratings are text that FEMA can rename; a county with no rating for a hazard; county, not address.
- **Disaster Declarations:** declaration date vs incident dates; statewide and tribal rows; flood types only, named.
- **Housing Assistance Owners:** flood-type declarations only; rows with no county stay at state level.
- **Community Status Book:** unincorporated areas; communities not in the NFIP; CRS class 10 = no discount; map dates.
- **IA Multiple-Loss:** counts only, never a property; suppressed small counts stay suppressed.
- **NFIP Residential Penetration:** its own as-of date, printed; county base, not the address.
- **NOAA Sea Level:** nearest station may be far or in another state (say which); no station = no line.
- **FEMA NFHL (address tool, map letters):** service down or silent = print nothing; -9999 and metres never shown;
  every zone within 15 m; LOMA counts only; "FEMA's map, not an official determination".
- **Census crosswalks (ZIP to town and county):** a ZIP spans counties; a ZIP from elsewhere typed on a policy.
- **Rules (laws, FEMA manuals):** raw text read this session, re-read by `recheck`; unreachable = manual read, 183 days.

## Never
- A fix that names a slug, a state or one wording instead of the rule that made it.
- An exception added to a gate for a third time: the gate matches the wrong thing; redefine what it matches.
- "Fixed" without the live sentence quoted from the real URL in the same report.
- A figure estimated, recalled or typed into a template; a guess in place of a printed gap line.
