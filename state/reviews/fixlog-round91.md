# Fixlog round 91 (from hcu-critique-2026-11-07.md BLOCKERs, plus the 11-07 county-run failure)

- BLOCKER "closed with no payment" on county/state pages: FEMA Claims v3 has no open/closed field. Root: build_page.py payout card + quick answer wording, notes.py "unpaid" note, build_site.py /data/ text. Fix: "no recorded payment" everywhere; payout note says a recent claim may still be paid. Proof: grep of every dist/*.html finds 0 "closed with/without payment".
- BLOCKER same county, two payout shares (Harris 51.1% county page vs 57.9% claims page). Root: claims page drops FEMA codes 98/99 (entered in error), county pages count them; neither said so. Fix: county payout note names the base and points at the claims page. Open: one base everywhere needs the cloud refresh (extras_raw excluding 98/99) plus recheck.py; backlog.
- County run 42404143419 failed: build needs PIL, installed only in a later step, so all 20 new counties hit ModuleNotFoundError; multi-line message broke GITHUB_OUTPUT. Fix: pillow installed in the add step; message = last line; add_counties.py stops (sets nothing aside) on ModuleNotFoundError/ImportError.
- ZIP JSON key order changed every build (set iteration): 1,000 files churned per deploy. Fix: sorted(used). Proof: two builds, diff -rq identical.

# Rounds 94-96 (hcu-critique MAJORs)
- Screen 1 lacked risk, zone cost, pay-less: quick answers added (FEMA county rating; two largest zones' medians; CRS share and top discount). P4 room: duplicate lender note cut, claim amount left to the payout card, "this year's bills / buying" moved beside the quote checker. Proof: phone_check PASS Brevard, Palm Beach, Harris.
- Jargon tile "Share of these homes below FEMA's full-risk price": now "Still pay less than FEMA's full-risk price; their bills rise toward it (how fast)", claim() checked, links #gap.
- Misleading elevated vs not-elevated medians: deleted. Coverage-in-force totals and claims-vs-units disclaimer: deleted.
- LOMA dead end: outcomes collapsed to removed / already outside / denied / other; 44 CFR 72.5 no-fee rule (eCFR raw) and FEMA Online LOMC link (read raw from the US runner, manual-rule-read) on county, AE/zone and map pages.
- No "is my map changing": county note says when FEMA's book lists no new map; FEMA preliminary-map rule on county and map pages.
- "No wait" cell dropped the paid-in-time condition: now "Can start at closing, if paid in time" (FIM quote).
- No official contact: state insurance regulator line, 39 states confirmed by their own page titles (tools/fetch_insurance_depts.py), NAIC directory for the rest.
- State pages: parish/county picker on screen 1. Home: 6 exact zones linked. AE etc.: full-risk median on its own base + glide rule. Renters: not-covered lines replace the lender line.
- Condo hedge: single-family cohort now leaves out FEMA condominium coverage codes U/A/H/L (ffcalc.is_sf_home, shared; recheck independent); test_calc fails on old code. Lands with the next forced refresh.
- 80% sameness: google_gate S2 measures 53% median / 60% max (names masked), prose 44%; under the limit, no rule text moved off pages.
