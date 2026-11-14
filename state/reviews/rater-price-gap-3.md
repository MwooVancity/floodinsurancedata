# Rater review 3: price-gap (2026-11-14)
Verdict: MINOR REVISION. BLOCKER 0, MAJOR 0.
Checked: page text, CSV (1,794 lines = header + 1,793 rows), PAPER-GATE-PROMPT rater part.
- Ads: pagead2 0 hits (pass). noindex,follow present (staging pass). No ld+json (allowed; no fake fields).
- Banned/advice/causal words (you should, best, worst, safest, significant, because, due to, driven by, caused, forecast, denied, peer, recommend): 0 hits.
- Labels vs data: title "1,793 U.S. counties" matches CSV; $100 line declared as the paper's choice with any-amount and $10 shares beside it; left-out counties (1,140 + 94) pooled 34.8% shown against listed 36.2%; Neptune/GAO bases labelled as different. No overclaim.
- Who/how/why: byline states publisher is not an insurance expert; AI-tools disclosure; Methods, Reproduce, Cite, Versions, Corrections present. Not scaled: one measure, table rows are data, text is specific.
MINOR (still open from rounds 1-2):
1. Lede quotes 36.2% twice for two bases (2,320,347 all counties vs 2,307,620 in 1,793 counties); reads as a repeat. Fix: lead with the 1,793-county base, move 2,320,347 to Results.
2. H1/title "gap" omits "$100 or more"; reader may take it as any amount (43.7%). Fix: add "$100+" to subtitle.
3. Lede is one long sentence for a phone reader; split in two.
