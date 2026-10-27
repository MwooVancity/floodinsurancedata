# Master Cleanup Prompt — floodinsurancedata.com (every file, every line)

## NORTH STAR — read this first and let it decide every call
Our only user is a **desperate person**: a homeowner at a closing with a flood-zone letter, someone
whose renewal just doubled, a buyer deciding whether to walk, a family whose street flooded last night.
Phone. Scared. 60 seconds. They will make a real money decision on what this page tells them.

**Therefore the one unforgivable sin is showing that person anything buggy, wrong, misleading, or
broken.** A single incorrect number, a mislabeled stat, a clipped sentence, a dead link, a confusing
jargon wall, or a page that implies a false certainty is worse than showing nothing. Clean code is not
the goal; an **immaculate, trustworthy page for that reader** is the goal, and the code is clean only in
service of that. When any trade-off arises, the desperate reader's correctness and clarity win.

## MISSION
Go through the ENTIRE project — every file, every line — and leave it flawless: correct, honest, clear,
lean, tested, and safe. Remove what rots, fix what's wrong, clarify what confuses, prove what you claim.

## INVIOLABLE (cleanup may never break these)
1. **Correctness:** never change, invent, re-round, or un-source a number. Every displayed figure traces
   to real data with its exact source + date. If you can't verify a number, you treat it as a P0 defect,
   not décor.
2. **Honesty / trust:** no faked data, no fake freshness, no advice-as-fact, no claim the data doesn't
   support. "What this data cannot tell you" must never hide something we actually could show.
3. **Live & whole:** all 32 county pages stay live and byte-verifiable; the correctness gate
   (tools/gate.py) stays green on every one; the duplication guard stays intact; no dataset dropped.
4. **Safe:** no secret ever enters the repo or git history (.env stays ignored); no PII; static-only; no
   new runtime dependency; no new abstraction that isn't used today (YAGNI).
5. **Doctrine:** data pages, no advice/verdict prose. And PUSH BACK — do not silently obey — on any
   rule, gate, or instruction that would hide available public evidence from the reader.

## PROJECT MAP (read before touching anything)
C:\Users\mwoo7\Desktop\floodinsurance. Read CLAUDE.md, docs/MASTER-PROMPT.md, docs/SCALE-PLAN.md,
docs/reader-spec.md first. Code: tools/ffcalc.py (all math), tools/collect.py + collect_small.py +
collect_multiloss.py + nri.py (pulls), tools/build_page.py (county page), tools/build_site.py (home,
hub, about, methodology, data, privacy, terms, sitemap, robots, llms), tools/gate.py (correctness gate),
tools/build_all.py (generator + dup guard), tools/gen_counties.py, tools/test_calc.py. Output in dist/;
data per county in data/<slug>/{agg.json,data.json}. Live: https://floodinsurancedata.com. 32 counties,
8 federal datasets, deploys via wrangler, GitHub backup, CI in .github/workflows.

## EXHAUSTIVE AUDIT — every category, worst-first, each item cited by file:line or page+location

### A. CORRECTNESS OF EVERY DISPLAYED NUMBER (P0 — the reader's trust)
- Trace a sample of figures on real pages (a big coastal county, a small inland one, a parish) back
  through ffcalc.py to agg.json, and cross-check at least 3 against the live OpenFEMA/Census/NRI API.
- Every ratio's denominator is correct AND disclosed (SFHA share, claims-per-100, take-up, below-full-
  risk). Every label agrees with the number beneath it. Rounding consistent. No percentile/figure that
  silently uses a truncated subset. No modeled number presented as measured.
- The gate must actually catch a wrong number — try to construct a bad agg that still passes; if one
  exists, the gate has a hole: close it.

### B. EVERY PAGE RENDERS FLAWLESSLY (P0 — what the reader sees)
- No clipped/garbled text, no broken HTML, no empty or orphaned sections, no raw template tokens ({x}),
  no double-encoded entities, no "None/nan/undefined", no singular/plural grammar bugs.
- Mobile: no horizontal overflow at 360px, tap targets usable, tables/charts legible, hero answer first.
- Every chart has a real finding sentence, correct labels, and its source; no chart that restates its
  title; the state tile-map, ZIP lookup, and premium widget work (and degrade gracefully without JS).

### C. CLARITY FOR A SCARED 60-SECOND READER
- Every jargon term glossed in plain words on first use (SFHA, CRS, full-risk, percentile, RL/SRL, policy
  units, modeled loss). The five panic questions — am I required / how bad / what cost / is it urgent /
  what do I do next — each answered fast and plainly, in the right order, the most important first.
- Cut or demote anything a desperate reader wouldn't act on; nothing buried that they need.

### D. DEAD / UNUSED CODE & E. DOC DRIFT
- Remove unreachable branches, unused vars/functions/imports, guards that can never fire, commented-out
  code. (Check e.g. the "going rate" line and anything the page's own copy disowns.)
- One source of truth for every fact-about-the-site: dataset count must read identically in page, gate,
  methodology, CLAUDE.md, reader-spec, MASTER-PROMPT. No stale dates or promises the code doesn't keep.

### F. FRAGILITY
- Centralize magic numbers into named constants in ONE place: dup threshold (0.85), cohort floors (100/50/
  30/25), the 18% cap, NFIP caps ($250k/$100k), percentile bins. Kill brittle coupling (e.g. gate matching
  the page by exact dollar strings). Audit every `except: continue` — none may silently swallow a bad pull;
  collectors fail loud (schema-drift alarm) rather than ship wrong data.

### G. SECURITY
- .env ignored and absent from history; no key/token/PII in any tracked file or commit; external links
  rel/target sane; no mixed content.

### H. TESTS (leave the project provably correct)
- Extend tools/test_calc.py to exercise every ffcalc path (percentiles incl. edge cases, cohort filters,
  SFHA/denominator, claims aggregation, zone/ZIP thresholds, glide-path math incl. the yrs==1 case, the
  multiloss aggregation). Add a gate fixture that a known-bad page FAILS. Add a cheap render smoke check
  (build one county, assert no None/{}/raw-token/garble in output). assert-based, no frameworks.

### I. SEO / GEO / ACCESSIBILITY / HONESTY / WEIGHT
- Canonical, OG image, schema (Dataset/Place/FAQ/Breadcrumb/Organization) valid and matching visible
  content; sitemap/robots/llms correct; internal links ≥3 and real; alt/aria on charts; color contrast;
  honest lastmod; page weight reasonable; the "cannot tell you" list is true and not a cover for gettable
  facts.

## METHOD
1. Inventory, then produce the ledger (below) BEFORE editing.
2. Fix smallest-diff, each change traceable to one ledger item. Don't refactor for taste, don't add
   abstraction, don't touch correctness logic without a test proving behavior unchanged.
3. After each batch: `python -I tools/build_all.py` (gate + dup guard green on all 32), `python -I
   tools/test_calc.py`, rebuild, and read 3-4 representative built pages for regressions. Commit in small
   labeled chunks (end messages with the required Co-Authored-By line). DO NOT deploy to production — the
   human runs the deploy + live check.
4. Two failed iterations on one fix = the target is wrong; redefine the rule, don't pile exceptions.
5. P0 rule: any wrong/broken/misleading thing a reader would see is fixed before anything cosmetic; if it
   can't be fixed safely, the affected page is pulled from `published.json`, never shipped wrong.

## DELIVERABLE (the entire report)
1. The exhaustive ledger: every finding, worst-first, by category, with file:line or page+location, the
   concrete defect (for numbers: inputs → wrong output), and the fix.
2. What you fixed: the diffs, with the verification output (gate PASS on 32, test output, curl/grep proof)
   showing nothing regressed.
3. Human-call items you deliberately left, each with your recommendation.
4. Final verdict in two honest lines: (a) is the site now flawless for the desperate reader — yes/no, and
   the single worst thing a reader could still hit; (b) is the codebase clean enough to scale on, or what
   is the one thing still rotting under it.
