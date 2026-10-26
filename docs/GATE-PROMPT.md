# Master Gate Prompt — floodinsurancedata.com (rebuild the gates so they catch MEANING, not form)

📄 Planning doc only — running it changes the gates; this file itself doesn't change the site.

## NORTH STAR
The reader is a desperate person: a closing in 10 days, a renewal that jumped, a street that flooded last
night. Phone, 60 seconds, a real money decision. **Showing them a wrong, mislabeled or self-contradicting
figure is the one unforgivable sin.** A gate exists only to stop that from shipping. A gate that passes a
wrong page is worse than no gate, because it makes us say "verified".

## THE EVIDENCE — why this prompt exists (2026-10-25)
`tools/gate.py` had 29 checks. All 32 pages passed. Then a live walkthrough, an SXO comparison and a
phone task test found 9 defect classes. **The gate caught 0 of 9.**

| # | Defect that shipped | Pages | What the gate checked instead |
|---|---|---|---|
| 1 | "Share below full-risk" compared `policyCost` (premium + reserve fund + federal fee + HFIAA surcharge) with `fullRiskPremium` (premium only). Understated by 10–37 points. | 32 | that the words "not a quote" appear |
| 2 | "Most policyholders pay below…" printed at 34.5%; "a bill can climb toward" a number below the bill | 23 | nothing |
| 3 | FEMA IA rows (one per property *per disaster*) labeled "properties" | 32 | that the block exists |
| 4 | Timeline said "5,690 paid claims"; next panel said 2,910 paid | 32 | that the total $ appears |
| 5 | Headline used the composite risk rating; "higher than X%" used the expected-loss percentile | 32 | that NRI is present or a gap line is |
| 6 | NOAA data cited as "Source: FEMA OpenFEMA" | 32 | that "OpenFEMA" appears anywhere |
| 7 | Chart drew a premium-only line on a cost-with-fees axis | 32 | that the chart exists |
| 8 | Purchase rule stated narrower than 42 U.S.C. §4012a | 32 | nothing |
| 9 | Reader: answer tool last of 20 sections, aid section collapsed, 4.5px chart labels, clipped tables | 32 | nothing |

**Root cause (one layer, not nine):** every check asks "does the page agree with the JSON?" None asks
"does the JSON mean what the sentence says?" Wrong *meaning* passes because the page faithfully prints
it. Fix that layer. Do NOT add nine regexes (that is whack-a-mole; see Inviolable 2).

## THE EVIDENCE, ROUND 2 (2026-10-26): every check passed, a reader still found 15 defects
All 83 pages passed A–E, the mutation suite and the phone check. Then one person read **one** state page
(Vermont) and **one** county page (Jefferson Parish) on a phone as a frightened reader:

| # | Defect that shipped | Why every check passed it |
|---|---|---|
| 10 | County shown as a code ("20015", a Kansas county on a Vermont page; 8 Connecticut counties as "09001") | gates checked figures, never names |
| 11 | "Each county page lists its own towns" / "Open a county below" with no county pages | no check reads pointers |
| 12 | "Data effective October 22, 2026" (the download day) on claims back to 1978; "retrieved October 22" on data pulled Oct 25 | dates were free-typed strings |
| 13 | "Vermont/New York Flooding paid $43.3 million", no year | nothing asks "when?" |
| 14 | "Inside the high-risk zone it's 113.1%" | % checked against the JSON, which says 113.1 |
| 15 | "About 1 in 2 homes" beside 64.9% | arithmetic right, words wrong |
| 16 | Chart labels overprinted ("$1,0$8,17$1,376") | phone check measured font size, not collisions |
| 17 | "16th highest of 51 Louisiana counties" (parishes) | no unit vocabulary |
| 18 | "p25 / p75 / policyCount" in reader text | no vocabulary check |
| 19 | "0 of Vermont's 14 counties are rated High" beside $117M of floods | true, misleading, unchecked |
| 20 | Hawaii missing from the national pull; a helper import silently ran a collection | no completeness check on inputs |

**Root cause:** A–E guard the *numbers*. Nothing guarded the *words the reader reads* (names, dates,
units, ratios, pointers, labels), and gate 3 sampled 3 pages of 83. Round 2's first answer (H1–H7) is
seven output regexes: a backstop, not the fix (Inviolable 2).

## ROUND 2 DESIGN: make the reader's words impossible to get wrong
### F. Typed reader words (render-time, like metrics): wrong text cannot be produced
- `name(geoid)`: the only way to print a place. Census name, then NRI; no name means **build fails**,
  never a code. A geoid outside the page's state never reaches a table.
- `unit_word(state)`: county / parish / borough, singular and plural. Templates never type "county".
- `src(keys, effective=Period|Snapshot|Current, retrieved=manifest.pulled)`: an effective date is a
  typed value from the data (a claims year range, the policy snapshot, "current list"), never the
  retrieval day. The retrieval date comes only from the pull manifest.
- `share_words(p)`: the only way to say "N in 10" / "1 in N"; a share over 100 raises and forces an
  explanation sentence from the registry.
- `event_label(e)`: name plus year(s) of loss, from the records.
- `link_to(kind)`: a sentence that points somewhere ("each county page…") renders only if the target
  exists in the build.
- Vocabulary: reader text is built from metric labels and registry text; field names and statistics
  codes (p25, policyCount) are not in the vocabulary.
- H1–H7 stay as the backstop on the rendered page, each with its mutation.

### G. Coverage: every page, the live page, every template
- Gate 2 runs on **every** page at build **and** on the **live HTML** of every page after deploy
  (`gate_live.py`). A sample is never called verified.
- Gate 3 adds **P6 label collision**: no two rendered text boxes overlap (JS bounding boxes). It runs on
  the pages most likely to break: per template, the page whose percentiles sit closest together, the
  longest county name, and the smallest and largest page.
- Inputs: the pull's state set must equal the 51 names; each dataset's count must equal its manifest;
  helpers are imported only from modules with a `__main__` guard (a test greps for it).

### H. The reader read: a defect a human finds becomes a class, then a scan, then a check
- On every template change, one random page per template is read on a phone, screen by screen, as the
  frightened reader (a scripted capture plus a written defect list, worst first).
- Each defect is named as a class, and a scan runs that class over **all** pages *before* anyone says
  "fixed". Then it becomes an F function (preferred) or an H check, with a mutation.
- "Misleading but true" (#19) is a defect: a lead must name the measure's basis when real outcomes on
  the same page point the other way (rating vs claims).

## MISSION
Rebuild the checking so each defect class above is **impossible to render**, not merely detected after
the fact, and prove every check by making it fail on a reintroduced bug.

## INVIOLABLE
1. **Three gates only**, as CLAUDE.md says: (1) it builds, (2) it is true, (3) it is live and usable.
   Everything below lives inside those three. No gate zoo, no second gate file per concern.
2. **No whack-a-mole.** A check that needs an exception or a third patch is matching the wrong thing:
   redefine what it matches. No per-county exceptions, no allow-lists of phrases.
3. **Every check is proven by a failing fixture.** A check with no mutation that makes it fail is deleted.
4. **Never weaken a check to get a page through.** A failing page is fixed or unpublished.
5. **Facts come from sources, not memory.** Field meanings come from FEMA's `OpenFemaDataSetFields` API;
   legal and program rules come from a fetched official page (WebSearch/WebFetch), quoted in the registry.
6. **Doctrine stands:** data pages, no advice prose; pushing back on anything that hides public evidence.
7. **Cheapest path:** reuse `ffcalc.py`, `gate.py`, `test_calc.py`, the scratchpad `shots.py` and
   `chk.py` patterns. One background job at a time. No new dependency.

## THE DESIGN (inside gate 2, "it is true")

### A. Metric registry — one place that says what every number MEANS (kills #1, #3, #6, #7)
`tools/metrics.py`: every figure the page can print is one entry:
`key, dataset, fields, fema_definition (fetched text + sha256), unit, counts, denominator, source_name, source_url`.
- `unit` is a closed set, e.g. `usd_cost_with_fees`, `usd_premium_only`, `pct`, `count`.
- `counts` names what one unit of a count IS: `policy_record`, `policy_unit`, `claim_record`,
  `ia_damage_record`, `noaa_event`, `community`, `declaration`.
- The renderer prints a metric only through `fmt(key)` and its label through `label(key)`.
  `label()` refuses words that contradict `counts` (an `ia_damage_record` count can't be called
  "homes" or "properties").
- Comparisons go only through `compare(a, b)`, which **raises** unless `unit` matches. A chart that
  overlays two series goes through the same check.
- The source line under a panel is generated from the metrics it shows. Hand-typed source strings are
  removed, so a NOAA panel can't say FEMA.
- The gate re-fetches each FEMA field definition. A changed hash fails until a human re-reads the new
  text and updates the entry. That way FEMA changing a field can't silently change our meaning.

### B. Claims — sentences can't contradict their own numbers (kills #2, #5)
Every sentence that contains a figure, or a quantifier/direction word (most, majority, half, few,
above, below, more, less, higher, lower, rise, climb, fall), is built by `claim(...)` from metric keys
and a comparator, never typed free-hand in a template.
- `claim()` picks the word from the values ("most" only if >50; "climb toward" only if target > current).
- The gate re-evaluates every claim on the page from the registry. A template lint fails any literal
  digit or quantifier word in template prose outside `claim()`. This is structural, not regex over the
  output, so it can't drift.
- When two metrics describe the same thing on different bases (a composite rating vs a percentile),
  their `claim()` must name the basis of each. The registry marks them `same_topic_different_basis`.

### C. Invariants — panels can't contradict each other (kills #4)
One table, evaluated per county. For example:
- `claims_paid ≤ claims_filed`
- `paid_n + cwop_n == claims_filed` (within records with a payment field)
- zone rows + "other" == units
- every % == numerator/denominator, recomputed
- a hero tile equals the panel it summarizes
- a word that names a set ("paid claims") resolves to the metric for that set

### D. Independent recompute — the code itself can be wrong (catches what A–C can't)
`tools/recheck.py`: a deliberately separate, minimal code path (no `ffcalc` import). Each release it pulls
2 random counties straight from the API and recomputes the hero figures: median cost, share below
full-risk, claims filed and paid, SFHA share. They must match the page within rounding. It uses a
different code path on purpose; a shared bug can't hide in both. Logged to `state/recheck.jsonl`.

### E. Rules registry — the law and program facts the page states (kills #8)
`tools/rules_registry.py`: each rule the page asserts (purchase requirement, 30-day wait and its
exceptions, NFIP limits, the HFIAA 18% cap, Risk Rating 2.0 pricing basis, IA needing a declaration) is
one entry: the exact page wording, the official URL, a ≤15-word quoted excerpt, and the date checked.
- The page prints rule text only from this registry.
- The gate checks each URL still answers 200 and still contains the excerpt.

## GATE 3 ("live and usable") — the reader, measured (kills #9)
- **Every deploy (scripted, no agent):** Playwright at 390×844 on 3 counties (largest, a parish, the
  smallest).
  - No element wider than the viewport.
  - Smallest rendered text, including SVG text, ≥ 11px (computed with JS).
  - Screen 1 contains the median, the FEMA map button and the jump menu; the quote checker is within
    screen 2.
  - No `<details>` collapsed around data.
  - Total height recorded, so growth is visible.
- **Every template change (agent, fixed script):** the timed task test with the same 4 tasks (closing
  buyer AE, renewal shock, Zone X skeptic, just flooded). The agent gets screenshots only.
  - Pass means each task is answered within 5 screens with the page's own numbers, and the agent
    finds no contradiction.
  - Result logged to `state/reader-test.jsonl`.
  - A new defect class it finds becomes a check in A–E plus a fixture, never a one-off patch.
- **Every deploy (existing):** live body fetched, real content checked this session.

## PROOF — mutation suite (`tools/test_gate.py`)
- For each of the 9 rows in THE EVIDENCE, build a fixture page or agg with that exact bug reintroduced.
- Assert it fails **the intended check, with the intended message**, and no clean fixture fails.
- Then run all 29 existing checks against all mutations and print a table: which existing check
  caught which mutation.
- Any existing check that catches nothing and guards no known failure: delete it or fold it into
  A–E, and list it in the report.
- CI runs `test_calc.py` + `test_gate.py` on every PR.

## DELIVERABLES / DONE WHEN
1. `metrics.py`, `claim()`, the invariants table, `recheck.py`, `rules_registry.py`, the phone check
   script (in `tools/`), and `test_gate.py` with ≥9 mutations, each failing as intended.
2. `gate.py` slimmed to call A–E. The report lists each removed or folded check with its reason.
3. All 32 pages pass gates 1–3. The rebuilt live page bodies are checked this session.
4. One SXO comparison and one timed task test run at the end. Their findings are fixed or logged as
   open, with the data they need.
5. The CLAUDE.md "Gates" section is rewritten to this design (the file stays under ~200 lines). Each
   gate change is logged with its reason.
6. The final report goes worst first: what each layer now makes impossible, what is still only detected,
   and what still needs a human (rule wording, new dataset meaning).

### Round 2 done when
7. F functions replace every free-typed name, unit word, date, ratio phrase, event label and pointer in
   `build_page.py`. A source lint fails on a template string containing "county", a date literal, or "1 in ".
8. P6 (label collision) and the input-completeness tests exist, each with a failing fixture.
9. `release.py --live` ends with `gate_live.py` passing on every live page (done 2026-10-26: 83/83).
10. One reader read per template after the change, with zero defects, or each one logged with its class
    and its scan result over all pages.

Known open items (not yet checks): the state tile map is unlabelled squares; pages run about 20 phone
screens, with the flood history near screen 11; disaster titles repeat ("Severe Storm: Severe Storm…");
AK, MT, ND and WY show dashes for over half their counties (fewer than 30 priced policies, a real data limit).

## OUT OF SCOPE
New datasets, new page sections, copy rewrites, unless a claim contradicts its data. Ranking work. Ads.
