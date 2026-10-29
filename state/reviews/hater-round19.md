# Hater round 19 (light check)

Scope: the new "Outside a high-risk zone?" note in the "Am I required to buy it?" card, and the "Search this table" inline script. Read-only: page text and source files were extracted with short Python scripts. No browser run, no screenshots, no web search.

## home

- No defects found. Scan of visible text in dist/index.html (about 6,700 characters) shows no undefined, NaN, null, [object, TODO or lorem. Title and H1 are present. Neither change appears on this page.

Verdict: PASS

## louisiana

- MAJOR: The note "Outside a high-risk zone? 21.4% of NFIP flood-claim dollars here paid buildings rated outside the high-risk zones." does not say what it means for the reader. The card asks "Am I required to buy it?", and the note never says whether a home outside the zone must buy, or should. A newcomer can read it as reassurance or as a warning with no action attached. Fix: state the takeaway in plain words, for example "Homes outside the zone still file and collect flood claims."
- MAJOR: "paid buildings" does not match the number. collect_claims_extra.py defines outside_sfha_pct as the share of paid net claim dollars (building plus contents plus ICC), not building-only. tools/metrics.py has an entry named outside_sfha_dollars that is building-only (netBuildingPaymentAmount, "of paid claim dollars"). Two definitions share one name. The rendered 21.4 comes from data.claims_extra.outside_sfha_pct, so the collect_claims_extra definition is the one shown. Fix: reword to "paid claim dollars (building and contents)" and reconcile metrics.py.
- MAJOR: No period in the sentence. The neighbouring sentence in the same card says "all years, not inflation-adjusted", but this share is also an all-years figure and does not say so. "here" means the whole state. Fix: add "(all years, whole state)".
- MAJOR (unverified): tools/collect_claims_extra.py computes `(r.get("ratedFloodZone") or "")[:1] not in ("A","V")`, so a claim with a blank zone code is counted as outside the high-risk zone. I did not count blank-zone claims (no network). If they are material, 21.4 is overstated. Check the blank share before this sentence ships.
- MINOR: "NFIP flood-claim dollars" and "rated" are jargon for a newcomer. "High-risk zones" is never defined beside the note.
- MINOR (script, see below): empty result gives no message.

Search script: reads correctly. It filters only tbody rows of section.card tables with 16 or more rows, by textContent. An empty query restores all rows, and it uses only the first tbody. Not run in a browser.

Verdict: FAIL

## palm-beach-county-fl

- MAJOR: The note "Outside a high-risk zone? 45.5% of NFIP flood-claim dollars here paid buildings rated outside the high-risk zones." has the same three defects as Louisiana: no takeaway for "required to buy", "paid buildings" wrong for a building plus contents figure, and no period or county scope. Fix as above.
- MAJOR (unverified): same blank-zone counting as Louisiana (tools/collect_claims_extra.py). A blank zone counts as outside. Check before shipping.
- MINOR: "rated" and "NFIP flood-claim dollars" are jargon. "Here" is not clearly the county.
- MINOR (script): no empty-result message and no match count.
- The number matches data/c/palm-beach-county-fl/data.json claims_extra.outside_sfha_pct (45.5).
- Search script: reads correctly, same as Louisiana. Not run in a browser.

Verdict: FAIL

## broward-county-fl

- MAJOR: The note "Outside a high-risk zone? 7.6% of NFIP flood-claim dollars here paid buildings rated outside the high-risk zones." has the same three defects as Louisiana: no takeaway for "required to buy", "paid buildings" wrong for a building plus contents figure, and no period or county scope. Fix as above.
- MAJOR (unverified): same blank-zone counting as Louisiana. Check before shipping.
- MINOR: "rated" and "NFIP flood-claim dollars" are jargon. "Here" is not clearly the county.
- MINOR (script): no empty-result message and no match count.
- The number matches data/c/broward-county-fl/data.json claims_extra.outside_sfha_pct (7.6).
- Search script: reads correctly, same as Louisiana. Not run in a browser.

Verdict: FAIL
