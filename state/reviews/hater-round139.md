# Hater round 139 (light, text only)

## home
- MINOR File is unchanged from HEAD (no source-line or completeness-card change applies); nothing new to fault.
Verdict: PASS

## louisiana
- MINOR Source lines now print once per dataset, at its first card (identical text only; I verified 0 duplicates left, 0 distinct lines removed, and a different date or base keeps its own line, e.g. Policies "2021 to 2026", "Policies; Claims", Claims "1978-2026"). Later policy and claims cards, and any card reached from the "On this page" menu, show no source line beside the figure; the date sits only at the first card. Not misleading, because the text was identical before.
- MINOR "The federal datasets behind this page" names every dataset (7) but prints no as-of dates; each dataset's date is on its first-card source line. Every listed dataset has a source line with its date on the page.
- MINOR "Are these counts complete?" lost "Download check: policies N of N fetched; claims N of N fetched". Provenance sentence ("Built from all 389,523 ... none missing") remains and is consistent.
- MINOR The first Policies source line now sits under the second-home surcharge sentence in "Am I required to buy it?", so the first-printed source is far from the cost figures it dates.
Verdict: PASS

## palm-beach-county-fl
- MINOR Source lines now print once per dataset, at its first card (identical text only; I verified 0 duplicates left, 0 distinct lines removed, and a different date or base keeps its own line, e.g. Policies "2021 to 2026", "Policies; Claims", Claims "1978-2026"). Later policy and claims cards, and any card reached from the "On this page" menu, show no source line beside the figure; the date sits only at the first card. Not misleading, because the text was identical before.
- MINOR "The federal datasets behind this page" names every dataset (10) but prints no as-of dates; each dataset's date is on its first-card source line. Every listed dataset has a source line with its date on the page.
- MINOR "Are these counts complete?" lost "Download check: policies N of N fetched; claims N of N fetched". Provenance sentence ("Built from all 74,041 ... none missing") remains and is consistent.
- MINOR Claim count is exactly 10,000 (data/all-counties/12099.json rows=10000), a round number that looks like an API page cap; larger counties exceed it (Miami-Dade 59,161), so likely coincidence, but not proven here.
Verdict: PASS

## new-york-county-ny
- MINOR Source lines now print once per dataset, at its first card (identical text only; I verified 0 duplicates left, 0 distinct lines removed, and a different date or base keeps its own line, e.g. Policies "2021 to 2026", "Policies; Claims", Claims "1978-2026"). Later policy and claims cards, and any card reached from the "On this page" menu, show no source line beside the figure; the date sits only at the first card. Not misleading, because the text was identical before.
- MINOR "The federal datasets behind this page" names every dataset (9) but prints no as-of dates; each dataset's date is on its first-card source line. Every listed dataset has a source line with its date on the page.
- MINOR "Are these counts complete?" lost "Download check: policies N of N fetched; claims N of N fetched". Provenance sentence ("Built from all 2,587 ... none missing") remains and is consistent.
Verdict: PASS

## dixie-county-fl
- MINOR Source lines now print once per dataset, at its first card (identical text only; I verified 0 duplicates left, 0 distinct lines removed, and a different date or base keeps its own line, e.g. Policies "2021 to 2026", "Policies; Claims", Claims "1980-2024"). Later policy and claims cards, and any card reached from the "On this page" menu, show no source line beside the figure; the date sits only at the first card. Not misleading, because the text was identical before.
- MINOR "The federal datasets behind this page" names every dataset (9) but prints no as-of dates; each dataset's date is on its first-card source line. Every listed dataset has a source line with its date on the page.
- MINOR "Are these counts complete?" lost "Download check: policies N of N fetched; claims N of N fetched". Provenance sentence ("Built from all 435 ... none missing") remains and is consistent.
Verdict: PASS

## levy-county-fl
- MINOR Source lines now print once per dataset, at its first card (identical text only; I verified 0 duplicates left, 0 distinct lines removed, and a different date or base keeps its own line, e.g. Policies "2021 to 2026", "Policies; Claims", Claims "1982-2026"). Later policy and claims cards, and any card reached from the "On this page" menu, show no source line beside the figure; the date sits only at the first card. Not misleading, because the text was identical before.
- MINOR "The federal datasets behind this page" names every dataset (10) but prints no as-of dates; each dataset's date is on its first-card source line. Every listed dataset has a source line with its date on the page.
- MINOR "Are these counts complete?" lost "Download check: policies N of N fetched; claims N of N fetched". Provenance sentence ("Built from all 750 ... none missing") remains and is consistent.
Verdict: PASS

## sonoma-county-ca
- MINOR Source lines now print once per dataset, at its first card (identical text only; I verified 0 duplicates left, 0 distinct lines removed, and a different date or base keeps its own line, e.g. Policies "2021 to 2026", "Policies; Claims", Claims "1978-2026"). Later policy and claims cards, and any card reached from the "On this page" menu, show no source line beside the figure; the date sits only at the first card. Not misleading, because the text was identical before.
- MINOR "The federal datasets behind this page" names every dataset (9) but prints no as-of dates; each dataset's date is on its first-card source line. Every listed dataset has a source line with its date on the page.
- MINOR "Are these counts complete?" lost "Download check: policies N of N fetched; claims N of N fetched". Provenance sentence ("Built from all 2,295 ... none missing") remains and is consistent.
Verdict: PASS

## wakulla-county-fl
- MINOR Source lines now print once per dataset, at its first card (identical text only; I verified 0 duplicates left, 0 distinct lines removed, and a different date or base keeps its own line, e.g. Policies "2021 to 2026", "Policies; Claims", Claims "1984-2026"). Later policy and claims cards, and any card reached from the "On this page" menu, show no source line beside the figure; the date sits only at the first card. Not misleading, because the text was identical before.
- MINOR "The federal datasets behind this page" names every dataset (9) but prints no as-of dates; each dataset's date is on its first-card source line. Every listed dataset has a source line with its date on the page.
- MINOR "Are these counts complete?" lost "Download check: policies N of N fetched; claims N of N fetched". Provenance sentence ("Built from all 1,197 ... none missing") remains and is consistent.
Verdict: PASS

## claims
- MINOR New #bycounty sentence is true: sum of claims.rows over the 2,905 data/all-counties files with claims = 2,567,024; sum over the 51 data/states/*/agg.json = 2,595,243; gap 28,219 claims with no county. But the page prints no U.S. total next to it, so "the U.S. total" is not a figure the reader can see or compare.
Verdict: PASS

## renters
- MINOR Texas sentence matches Property Code 92.0135(a-1)(1) (read live from tcss.legis.texas.gov: notices "not required for a tenant under a lease with a term of less than 30 days"). "Some leases are exempt" is slightly loose: the exemption is from the two notices, not from the lease rules, and (a-1)(2) also exempts 90-day sale-contract occupancies. "including" keeps it true.
Verdict: PASS

