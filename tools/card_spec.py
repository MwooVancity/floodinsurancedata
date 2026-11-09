"""One line per page card: what its data covers, what it leaves out, and when it must appear (2026-10-28).
gate.py H12: a shown card prints every `must` phrase (its stated limits) and none of its `never` phrases (claims its data
cannot back). gate.py H13: when `shown_when(agg, data, extras)` is true the card is on the page (a card that vanishes
while its data exists is a silent drop). Built by reading each card's inputs (tools/card_map.py -> state/card-map.json).
Cut from the page 2026-10-28 (answer none of cost / required / quote fair / pay less / payouts / risk): NOAA storm
history (county-coded only: misses coastal flooding and surge), premium trend, state "dropping insurance" trend, state
risk tile map, outside-the-zone note, take-up cards (FEMA take-up restored 11-08 by the owner)."""

import metrics as MX
def _ev(x):   # named floods the events table lists: losses within two calendar years, 20+ paid claims (MX.CONST event_min)
    return [e for e in (x.get("claims") or {}).get("events") or []
            if e.get("years") and int(e["years"][-1]) - int(e["years"][0]) <= 1 and (e.get("claims") or 0) >= MX.CONST["event_min"]]

CARDS = [
    {"title": r"Which floods paid out the biggest totals",
     "covers": "paid NFIP claims grouped by FEMA's event name; the 8 largest events by dollars (extras_raw keeps 8)",
     "must": ["or more paid claims here", "include code-upgrade (ICC)"],
     "never": ["all floods", "every flood"],
     "shown_when": lambda a, d, x: len(_ev(x)) >= 2},
    {"title": r"Why do flood claims here go unpaid",
     "covers": "closed-without-payment claims by FEMA's building non-payment reason; the 5 commonest reasons, the rest in one row",
     "must": ["Reason recorded"],
     "never": ["paperwork closures", "no specific reason recorded"],
     "shown_when": lambda a, d, x: ((x.get("claims") or {}).get("unpaid_n") or 0) >= 10
                                   and any(r["code"] not in ("97", "98", "99") for r in (x.get("claims") or {}).get("unpaid_reasons") or [])},
    {"title": r"Would a policy here pay to rebuild",
     "covers": "single-family policies reporting a rebuilding cost; coverage at the $250,000 limit over all single-family policies",
     "must": ["80% of its full rebuilding cost", "different bases"],
     "never": ["count different policies"],
     "shown_when": lambda a, d, x: ((x.get("policies") or {}).get("replacement_n") or 0) >= 30
                                   and (x.get("policies") or {}).get("replacement_over_250k_pct") is not None},
    {"title": r"Do flood claims here actually pay out",
     "covers": "every NFIP claim since 1978; paid = building + contents + ICC above zero",
     "must": ["includes Increased Cost of Compliance"],
     "never": ["your claim will"],
     "shown_when": lambda a, d, x: bool((d.get("claims_extra") or {}).get("claims"))},
    {"title": r"Flood insurance claims in .+: what floods pay out",
     "covers": "paid NFIP claim dollars by year of loss (building + contents; ICC excluded)",
     "must": [],   # the not-final note is conditional on the as-of year: gate C13 owns it (11-08)
     "never": [],
     "shown_when": lambda a, d, x: bool((a.get("claims") or {}).get("by_year"))},
    {"title": r"What does it cost in my flood zone",
     "covers": "median single-family cost per rated zone with 50+ priced policies",
     "must": ["Zones with fewer than"],
     "never": [],
     "shown_when": lambda a, d, x: bool((a.get("policies") or {}).get("cost_by_zone"))},
    {"title": r"How often is .* a flood disaster",
     "covers": "flood and storm declarations (DR, EM, FM) for the place; the list shows only the latest",
     "must": ["Only the latest are listed"],
     "never": [],
     "shown_when": lambda a, d, x: False},   # always built; the count can be 0
    {"title": r"Can I pay less",
     "covers": "single-family deductible mix (4 commonest), elevated vs not-elevated median premium",
     "must": ["commonest deductibles"],
     "never": ["elevating saves"],
     "shown_when": lambda a, d, x: bool((x.get("policies") or {}).get("deductibles"))},
]
