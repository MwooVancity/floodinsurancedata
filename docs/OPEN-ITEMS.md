# Open items — only what code cannot close

Updated 2026-10-22. Everything buildable is built, gated and committed. The items below are the only
things left, and none of them is code I can write — they are owner decisions, external throughput, or
empirical outcomes. This is the honest "what's left open."

## Owner decisions (cannot be automated)
- [ ] **Domain.** Working folder `floodinsurance` is local only; floodfigures.com is taken — pick another.
- [ ] **Search Console property** — own, separate from calcscrape and the river site.
- [ ] **Hosting project** — Cloudflare Pages/Workers, its own project. Set `FF_BASEURL` to the real domain
      and re-run `tools/build_all.py` so canonicals/sitemap/JSON-LD carry it.
- [ ] **Publisher name + contact email** for the methodology/about page.
- [ ] **Ads + consent banner** — only after a four-week Search Console review passes.

## External / time-bound (not code)
- [ ] **National data sweep.** Add every target county to `tools/counties.json` and run
      `python -I tools/build_all.py` (resumable; skips built counties). Bounded by FEMA API throughput:
      large-state counties (e.g. Harris TX, 222k policies) are intermittently 503-ing right now — the
      collector shrinks page size and resumes, but a full sweep runs over hours/days when the API is calm,
      not in one pass. Lee (FL) and Kanawha (WV) are built as the proven pilot.
- [ ] **Census ACS key** (free) — only needed later for the take-up rate (share of homes insured).

## Empirical (no one can certify in advance)
- [ ] **Whether it ranks.** Months of Search Console evidence, gated by the decision rule in the build plan.
- [ ] **Whether it is "the most helpful" flood page.** Provably it shows more verified, sourced,
      decision-relevant public data than any competitor inspected (8 datasets vs their 1–2), every number
      correct, sourced, dated and gate-checked. "The single most helpful page on Earth" is an empirical
      claim only real users and comparison can confirm — not something a build can stamp.

## Done (nothing left to build)
- [x] Reader spec + 8-dataset catalog, all verified live (`docs/reader-spec.md`).
- [x] Parameterized, 503-hardened, resumable collector; NRI (coastal + inland); CRS; declarations; housing.
- [x] Page builder: 9 data panels, inline-SVG charts, JSON-LD (Dataset/Place/FAQ/Breadcrumb), OG/meta,
      canonical, internal sibling links, quote-position widget.
- [x] Site builder: home + client-side lookup, methodology, data download (CSV), sitemap, robots, llms.txt.
- [x] Correctness gate (`tools/gate.py`) — both pilot counties PASS.
- [x] One-command generator (`tools/build_all.py`) + county list.
- [x] Two proven counties spanning extremes: Lee FL (coastal, 134k units) and Kanawha WV (inland, 1.3k).
