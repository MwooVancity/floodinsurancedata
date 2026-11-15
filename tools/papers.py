"""Research papers (owner 11-12: national data, "PubMed worthy"; docs/PAPER-GATE-PROMPT.md). One spec per paper; every U.S. county
in data/all-counties whose count base meets the minimum is ranked. Shares are numerator / denominator on ONE base (methods review 162
M1.1), each with a 90% Wilson interval (M1.3); readers see fifths (bands), never a bare rank. build_site.py writes each paper page +
CSV; build_counties.py writes .cache/papers.json once per build (PLAN E13). tools/paper_gate.py recomputes
every row from the raw county files with its own code (PLAN E22)."""
import json, math, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALL = os.path.join(ROOT, "data", "all-counties")
CACHE = os.path.join(ROOT, ".cache", "papers.json")
Z90 = 1.6448536269514722   # two-sided 90% normal quantile

SPECS = [
    {"key": "damage-over-coverage", "ready": True, "indexable": True, "title": "Flood damage over building coverage: NFIP claims by county",
     "num": ("extras", "claims", "underinsured", "over"), "den": ("extras", "claims", "underinsured", "n"), "min": 100,
     "window": ("extras", "claims", "underinsured"),
     "excess": ("extras", "claims", "underinsured", "excess_median"), "by_year": ("extras", "claims", "underinsured", "over_by_year"),
     "question": "In which U.S. counties did FEMA's recorded building damage on paid flood claims most often exceed the policy's building coverage, and by how much?",
     "unit": "paid single-family primary-home claims with recorded damage and coverage",
     "measure": "share of paid single-family primary-home NFIP claims whose recorded building damage (FEMA's actual cash value) was more than the policy's building coverage",
     "short": "damage over building coverage", "meets": "had recorded building damage over the building coverage",
     "fields": "buildingDamageAmount, totalBuildingInsuranceCoverage, netBuildingPaymentAmount, yearOfLoss, occupancyType, primaryResidenceIndicator, condominiumCoverageTypeCode, nonPaymentReasonBuilding, countyCode",
     "defs": ['FEMA defines buildingDamageAmount as "The actual cash value amount of damage to a main property in whole dollars."',
              'FEMA defines totalBuildingInsuranceCoverage as "Total Insurance Amount in whole dollars on the Building".'],
     "dataset": "FEMA OpenFEMA NFIP Claims v3", "api": "https://www.fema.gov/api/open/v3/NfipClaims",
     "base": "claims with a loss in the window on single-family primary homes (FEMA occupancy type 1 or 11, primary residence, not a condominium coverage type) with a building payment above $0, recorded building damage above $0 and building coverage above $0; here a claim counts as paid on its building payment alone; records FEMA coded deleted or assigned in error left out",
     "limits": ["Damage over coverage compares FEMA's recorded actual cash value with the building coverage on the policy; it is not the owner's uninsured loss, which also depends on contents, deductibles, replacement cost, other insurance and aid.",
                "Only insured, paid claims are in the base: homes without flood insurance are not.",
                "Where a county has at least 10 claims over coverage and one loss year holds over half of them (marked in the table), those claims cluster in one year, which may hold one flood or several; clustered claims are not independent, so that county's 90% range is narrower than it should be.",
                "Counties are those FEMA codes on the claim, which can differ from the property's county."],
     "prior": "No published ranking of this measure by county was found in searches on 2026-11-12 (WebSearch: NFIP claims damage exceeded coverage by county).",
     "prior_links": [], "prior_rules": [], "policy_col": False, "published": "2026-11-13",
     "rules": []},
    {"key": "outside-the-zone", "ready": True, "indexable": True, "title": "Outside the zone: paid flood claims rated outside high-risk zones",
     "num": ("extras", "claims", "zone_split", "out_paid_n"), "den": ("extras", "claims", "zone_split", "known_paid_n"), "min": 100,
     "window": ("extras", "claims", "zone_split"),
     "question": "In which U.S. counties are the most paid NFIP flood claims rated outside FEMA's high-risk zones (A and V)?",
     "unit": "claims with a payment and a rated zone",
     "measure": "share of paid NFIP claims with a rated flood zone whose zone is outside zones A and V (zones X, B, C and D)",
     "short": "paid claims outside zones A and V", "meets": "were rated outside zones A and V",
     "fields": "ratedFloodZone, netBuildingPaymentAmount, netContentsPaymentAmount, netIccPaymentAmount, yearOfLoss, nonPaymentReasonBuilding",
     "defs": [],
     "dataset": "FEMA OpenFEMA NFIP Claims v3", "api": "https://www.fema.gov/api/open/v3/NfipClaims",
     "base": "NFIP claims on every building type with a loss in the window, a payment above $0 and a rated flood zone; zone D (possible but undetermined hazard) counts as outside A and V; records FEMA coded deleted or assigned in error left out",
     "limits": ["This is a share of claims, not of homes, and not the chance that any home floods.",
                "The zone is the zone FEMA rated on the claim, which can differ from today's map.",
                "Claims with no rated zone are not in the base."],
     "prior": "No national ranking of counties on this base was found in searches on 2026-11-12.",
     "prior_links": [("Penn State's PSIRC",   # (anchor, url, text after): anchors stay under 12 words (S16 anchor_fails)
                      "https://www.psirc.psu.edu/assets/NFIP_Insights_for_PA.one-pager.2022-09-05.pdf",
                      "mapped Pennsylvania NFIP claims, including claims outside the Special Flood Hazard Area, from FEMA's 2019 claims release")],
     "prior_rules": ["fema_outside_third"], "policy_col": True, "published": "2026-11-13",
     # review outside-zone-4 M1: say only what FloodSmart states (current high-risk areas, 2014-2024); it does not say paid-only or all claims
     "prior_note": "FEMA's figure uses current high-risk areas and the years 2014 to 2024, and does not say whether it counts only paid claims; this page counts paid claims by the zone rated on each claim.",
     "policy_note": "Policy units outside A and V: the share of NFIP policy units in force in the county, every policy type, rated outside zones A and V.",
     "rules": []},
]

DED_MIN = 5000   # Deductible Choice threshold: the same "$5,000 or more" the deductible guide shows (D4 check)
def ded_units(rec, at_least):
    """Single-family primary-home policy units (SUM policyCount, extras_raw) whose building deductible is at least at_least dollars;
    None where the county has no deductible on record. Blank and unknown codes are never in deductible_units (counted out)."""
    u = _get(rec, ("extras", "policies", "deductible_units"))
    if not isinstance(u, dict) or not u: return None
    return sum(v for k, v in u.items() if str(k).isdigit() and int(k) >= at_least and isinstance(v, int))

def _ded_codes():
    import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # -I drops the script dir
    from codes import DEDUCTIBLE
    return (", ".join(f"{c} - ${d:,}" for c, d in sorted(DEDUCTIBLE.items(), key=lambda kv: kv[1]) if d >= DED_MIN),
            ", ".join(f"{c} - ${d:,}" for c, d in sorted(DEDUCTIBLE.items(), key=lambda kv: kv[1]) if d < DED_MIN))

SPECS.append(
    {"key": "deductible-choice", "ready": True, "indexable": True, "title": "Building deductibles on record: NFIP single-family homes by county",
     # statistician review: FEMA records the deductible on the policy, not an owner's choice; no choice word in any label (paper_gate LABEL)
     "num": lambda r: ded_units(r, DED_MIN), "den": lambda r: ded_units(r, 0), "min": 30,
     "question": f"In which U.S. counties do single-family primary homes insured by the NFIP most often have a building deductible of ${DED_MIN:,} or more on record?",
     "unit": "single-family primary-home policy units with a known building deductible",
     "measure": f"share of single-family primary-home NFIP policy units in force whose building deductible is ${DED_MIN:,} or more",
     "short": f"building deductibles of ${DED_MIN:,} or more", "meets": f"had a building deductible of ${DED_MIN:,} or more on record", "line_metric": "ded_amount",
     "fields": "buildingDeductibleCode, policyCount, occupancyType, primaryResidenceIndicator, condominiumCoverageTypeCode, censusGeoid",
     # rater: why the measure matters, in FEMA's words only (raw read of OpenFemaDataSetFields NfipPolicies v3, 2026-11-13), no advice
     "why": ['FEMA defines buildingDeductibleCode as "The total deductible amount in dollars for buildings, both main and appurtenant, that can be applied against the loss."',
             f"The FEMA codes counted as ${DED_MIN:,} or more, in the data dictionary's own form: {_ded_codes()[0]}. FEMA's standard codes below ${DED_MIN:,}, counted in the base but not the share: {_ded_codes()[1]}."],
     "defs": ['FEMA defines policyCount as "Insured units in an active status."',
              ],
     "dataset": "FEMA OpenFEMA NFIP Policies v3", "api": "https://www.fema.gov/api/open/v3/NfipPolicies",
     "base": "NFIP policies in force on the data date on single-family primary homes (FEMA occupancy type 1 or 11, primary residence, not a condominium coverage type), counted as policy units (sum of policyCount; every such record here holds one unit, which the check confirms); units with a blank building deductible code, or a code outside FEMA's standard list such as H (used only for Group Flood Insurance Policies), left out",
     "limits": ["FEMA records the building deductible on each policy; a deductible on record is not shown to be the owner's choice, and the data does not say who set it or why.",
                "Only the building deductible is counted; the contents deductible is separate and not in this measure.",
                "This is one snapshot of policies in force on the data date; it shows no change over time.",
                "A county's share says nothing about which deductible suits any one home.",
                "Counties come from the census geography FEMA codes on each policy (censusGeoid), which can differ from the property's county."],
     "prior": "No ranking of counties or states by the building deductible on record was found in searches on 2026-11-13 (WebSearch: NFIP policies deductible chosen by county; flood insurance deductible choice by county map; NFIP minimum deductible studies). Published work on NFIP deductible choice is national or for one state and does not rank counties:",
     "prior_links": [("Deductible Choice in Flood Insurance: Who Chooses the Maximum?",
                      "https://www.tandfonline.com/doi/full/10.1080/10527001.2020.1839320",
                      "(Taylor & Francis, 2020; owner-occupied single-family NFIP policies, national, not by county)"),
                     ("Michel-Kerjan and Kousky, Come Rain or Shine",
                      "https://media.rff.org/archive/files/sharepoint/Documents/Publications/Non-RFF_Pubs/09-09_Kousky_Come-Rain-or-Shine.pdf",
                      ": Evidence on Flood Insurance Purchases in Florida (Florida policies)")],
     "prior_rules": [], "policy_col": False, "published": "2026-11-13", "rules": []})
# Flood Calendar (11-13). Edge cases, written before the code, each with its test:
# - no loss_month_n / empty by_month / non-int counts -> county not listed (self-test cal_k({}) is None)
# - tied peak months -> every tied month named, one share (self-test 'tie'); a flag is checked on each tied month
# - peak month under ONE_YEAR_MIN claims -> never flagged (self-test); exactly half -> not over half (self-test)
# - month key outside 01-12 -> ignored (self-test); date read as text [5:7], so no time-zone shift (extras_raw)
# - by_year_month not adding up to by_month -> paper_gate fails (consistency check + mutation)
# - peak picked from the same claims -> share biased up; Limitations says so (no interval claims to fix it)
# - 404 of 416 counties flagged (11-13 data): the Abstract and Results print the flagged count, never a 'season'
# Review round 2 (statistician + rater, 11-13), edge cases before the code:
# - peak share is the max of 12 by construction, larger at small n (13.3% at n=100, 9.4% at 2000, floor 1/12): every row prints
#   the expected peak share at random for its own n and rows are ranked and put in fifths on share minus that (self-test: oracle values)
# - the null is a simulation: seeded by n and summed as integers, so paper_gate's own copy gets the same figure (gate oracle test)
# - tied months: the null is for the largest month whatever month it is, so ties need no change
# - flagged rows: the Wilson range assumes independent claims; the header says 'if claims were independent' (gate label check)
# - 'calendar' / 'season' in a label is a claim the data does not make (404 of 416 one-year): gate LABEL word check + mutation
# - distinct loss years in the peak month: zero-count year-months not counted (self-test)
# Review round 3 (statistician, 11-13), edge cases before the code:
# - the over-half flag fires in 404 of 416 (no power) and says nothing about other years: no 'repeats each year' / 'not a pattern' /
#   'mostly one year's flood' anywhere on the page (gate OVERCLAIM + mutation); graded columns instead (largest year's share, 10+ years)
# - a year with one claim counted as a year with claims (Greenbrier 2 years / 344): header says 'at least one claim' (gate header check
#   + mutation) and a second column counts years with ONE_YEAR_MIN+ claims (self-test: 9 claims is not a 10+ year)
# - tied peak months: each month graded on its own, joined with 'and' like the month names (self-test 'tie graded')
# - no year-months for a county: largest share 0.0, never a crash; the months_add_up gate fails that county anyway
# - largest year = the peak month itself (one storm, every claim): 100.0, never over 100 (self-test)
MONTHS = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
def _bm(rec):
    b = _get(rec, ("extras", "claims", "loss_month_n", "by_month"))
    b = {k: v for k, v in b.items() if k in {f"{i:02d}" for i in range(1, 13)} and isinstance(v, int) and v >= 0} if isinstance(b, dict) else {}
    return b if b and sum(b.values()) else None
def cal_k(rec): b = _bm(rec); return max(b.values()) if b else None   # claims in the peak month
def cal_n(rec): b = _bm(rec); return sum(b.values()) if b else None   # claims with a month of loss
NULL_R = 4000   # draws per county for the chance expectation
import functools
@functools.lru_cache(maxsize=None)
def chance_peak(n):
    """Expected peak-month share, in percent, if a county's n claims fell at random, each of the 12 months equally likely:
    the mean largest month over NULL_R seeded draws (seed = n, integer sum, so paper_gate's own copy matches to the digit)."""
    import numpy as np
    m = np.random.default_rng(n).multinomial(n, [1 / len(MONTHS)] * len(MONTHS), size=NULL_R).max(axis=1)
    return round(100 * int(m.sum()) / (NULL_R * n), 1)
SPECS.append(
    {"key": "flood-calendar", "ready": True, "indexable": True,
     "title": "Peak month of NFIP claims by county",   # statistician round 2: no calendar or season word (404 of 416 one-year)
     "num": cal_k, "den": cal_n, "min": 100, "window": ("extras", "claims", "loss_month_n"), "months": True, "null": chance_peak,
     "question": "In which month of the year do a U.S. county's NFIP flood claims most often fall, how much larger is that month's share than claims spread at random would give, and how much of that month is one year's claims?",
     "unit": "NFIP claims with a month of loss",
     "measure": "share of a county's NFIP claims, paid or not, whose date of loss falls in the county's peak month (the month of the year with the most claims there)",
     "short": "claims in the peak month", "meets": "fell in their county's peak month",
     "fields": "dateOfLoss, yearOfLoss, countyCode, nonPaymentReasonBuilding",
     "why_rules": ["wait_30"],
     # raw read of OpenFemaDataSetFields (NfipClaims v3) 2026-11-13
     "defs": ['FEMA defines dateOfLoss as "Date on which water first entered the insured building. When time is not specified in the field, it will default to T00:00:00.000Z".',
              'FEMA defines yearOfLoss as "Year in which the flood loss occurred".',
              'FEMA defines countyCode as "FIPS code uniquely identifying the primary County (e.g., 011 represents Broward County) associated with the project. Note, the County Code field may not reflect the individual county the property is located as projects can be associated with more than one county".'],
     "dataset": "FEMA OpenFEMA NFIP Claims v3", "api": "https://www.fema.gov/api/open/v3/NfipClaims",
     "base": "NFIP claims on every building type, paid or not, with a loss year in the window and a month in the date of loss, the month read from the date as FEMA writes it (no time-zone shift); records FEMA coded deleted or assigned in error (nonPaymentReasonBuilding 98 and 99) left out",
     "limits": ["Each county's 90% range is narrower than it should be for two reasons: the peak month is picked from the same claims it is measured on, so the share is the highest of twelve by construction (the expected share at random, beside each row, shows how much of it chance alone gives), and claims from one flood are not independent, which matters most in the marked rows where one year holds over half of the peak month. The ranges are those that would hold if claims were independent.",
                "A marked row means only that one year holds over half of the peak month's claims; that year may hold one flood or several. The mark does not say whether the month floods in other years and almost every listed county has one; the columns beside it give the largest year's share of the peak month and two counts of loss years with claims in it.",
                "A large excess over chance can come from one flood event: one storm's claims, all in one month, raise both the share and the excess.",
                "The expectation at random treats the twelve months as equally likely and ignores their different numbers of days.",
                "Claims count insured buildings that filed, not floods: one storm can bring thousands of claims, and a flood where few buildings are insured brings few.",
                "Ten loss years are a short record: a month with few or no claims here can still flood.",
                "Counties are those FEMA codes on the claim, which can differ from the property's county."],
     "prior": "No published ranking or table of U.S. counties by the calendar month of NFIP flood claims was found in searches on 2026-11-13 (WebSearch: NFIP flood claims by month of loss by county peak month; flood season by county NFIP claims seasonality map; dateOfLoss NFIP claims seasonality month analysis county). County tables of NFIP claims found in those searches count claims by year of loss, not by month.",
     "prior_links": [], "prior_rules": [], "policy_col": False, "published": "2026-11-13", "rules": [],
     # bug review 11-14: excess was computed from the unrounded share; one printed value changed, no fifth changed
     "corrections": [("2026-11-14", "Excess over chance is now the printed share minus the printed expected share. One county changed: Taylor County, FL (12123), from 56.5 to 56.4 points. No county changed rank or fifth.")]})
# Price Gap revised (11-14; methods review 162 M1-M9). Originality 11-14: GAO-27-108012 (Oct 1 2026) downloads every county's share of
# ALL NFIP policies "with premiums that do not fully reflect their flood risk as of April 2026" (any amount, no n, no gap size); Neptune
# gives national/state figures. The real difference here: a material line ($100+ a year), the gap's size per county, n and 90% range,
# single-family primary homes only, and the CRS split (M3). Edge cases: see paper_gate.py price-gap checks and the self-test below.
GAP_MIN, GAP_MED_MIN = 100, 30   # the $100 line; a median gap printed only from 30+ policies below (M2.8: never a figure from a few records)
def gap_ctx(rec):
    p = rec.get("policies") or {}; k, n, md = p.get("below_k"), p.get("below_n"), p.get("below_gap_median")
    if not (isinstance(k, int) and isinstance(n, int) and n): return {"any_k": None, "any_pct": None, "gap_med": None}
    return {"any_k": k, "any_pct": round(100 * k / n, 1), "gap_med": md if isinstance(md, (int, float)) and k >= GAP_MED_MIN else None}
SPECS.append(
    {"key": "price-gap", "ready": True, "indexable": False, "gap": True,   # M3.5: published None = staged noindex (paper_gate STAGED)
     "title": "The gap to FEMA's full-risk premium: NFIP single-family homes by county",   # no number in a title: county cards print it untagged (V1)
     "num": ("policies", "below100_k"), "den": ("policies", "below_n"), "min": 30,
     "question": f"In which U.S. counties do NFIP single-family primary homes most often pay a premium at least ${GAP_MIN} a year below FEMA's full-risk premium for the same policy, and how large is the gap there?",
     "unit": "single-family primary-home policies priced both ways",
     "measure": f"share of NFIP single-family primary-home policies in force whose premium is at least ${GAP_MIN} a year below the full-risk premium FEMA records on the same policy",
     "short": f"premiums ${GAP_MIN} or more below full-risk", "meets": f"had a premium at least ${GAP_MIN} a year below FEMA's full-risk premium", "line_metric": "gap_line",
     "fields": "totalInsurancePremiumOfThePolicy, fullRiskPremium, crsClassCode, policyCount, occupancyType, primaryResidenceIndicator, condominiumCoverageTypeCode, censusGeoid",
     "why": [f"The ${GAP_MIN} line is this paper's choice, so that a gap of a few dollars is not counted as a price gap; the share below by any amount and the median gap are in the table, and Results gives the pooled share by any amount, by $10 or more and by ${GAP_MIN} or more, so a reader can see how much the line moves the figure."],
     # raw read of OpenFemaDataSetFields (NfipPolicies v3) 2026-11-14
     "defs": ['FEMA defines fullRiskPremium as "The chargeable premium for a property based on its determined flood risk and the full cost to pay anticipated losses and expenses for that property."',
              'FEMA defines totalInsurancePremiumOfThePolicy as "Total Insurance Premium of the Policy in whole dollars. Negative values indicate a refund."',
              'FEMA defines crsClassCode as "The Community Rating System (CRS) Classification Credit Percentage used to rate the policy." and adds "Beginning with Risk Rating 2.0, there are no longer percentage discount differences for policies inside and outside of the SFHA."',
              'FEMA defines policyCount as "Insured units in an active status."'],
     "dataset": "FEMA OpenFEMA NFIP Policies v3", "api": "https://www.fema.gov/api/open/v3/NfipPolicies",
     "base": "NFIP policies in force on the data date on single-family primary homes (FEMA occupancy type 1 or 11, primary residence, condominium coverage type N or blank) with a premium above $0 and a full-risk premium above $0 (refunds and blanks left out); the gap is full-risk premium minus premium, both premium only, before fees and surcharges; counted as records, and every such single-family record here holds one policy unit, which the check confirms",
     "limits": ["FEMA's data dictionary does not say whether the full-risk premium is before or after the Community Rating System credit; Results gives the share by the CRS class code on the policy so a reader can see whether the class lines up with the share.",
                "The data does not say which discount puts a premium below full-risk (the yearly increase cap, pre-flood-map construction, a newly mapped area or another rule), and this paper does not say either.",
                "The gap is a yearly premium difference on one snapshot of policies in force; it is not what any one owner will pay next year.",
                "The median gap is over every policy below full-risk by any amount, and is printed only where 30 or more policies are below.",
                "Counties come from the census geography FEMA codes on each policy (censusGeoid), which can differ from the property's county.",
                "The table is ordered by share alone, not by count: a county with few policies can sit above a county with thousands whose 90% range overlaps its own, so counties within one fifth cannot be told apart and the order inside a fifth is not a ranking.",
                "Policies in one county share a flood map, a community and its rating, so they are not independent; each county's 90% range treats them as independent and is narrower than it should be.",
                "Every listed county gets its own 90% range, so about one range in ten would be expected to miss that county's true share by chance alone; no range is adjusted for the number of counties."],
     "prior": "Published work on this measure, read 2026-11-14: GAO's report GAO-27-108012 (October 1, 2026) gives, for every county with at least 10 properties and as a download, the percentage of all NFIP policies in a county with premiums that do not fully reflect their flood risk as of April 2026, by any amount, with no count of policies and no size of the gap. Neptune Flood's research group reports 1.5 million policyholders, 42% of the program, still paying below their full-risk price, about $2.6 billion a year; Neptune's 42% counts every NFIP policyholder, while this paper's share below by any amount counts only single-family primary homes priced both ways, so the two shares are on different bases. This paper differs in base (single-family primary homes only), in a material line (at least $100 a year, with the any-amount share beside it), in giving the gap's size, the policy count and a 90% range for every county, and in the CRS split.",
     "reconcile": ("12021", "GAO's download gives 0.765 (76.5%) of all NFIP policies there as of April 2026; the two differ in base (all policies against single-family primary homes) and date"),   # bug review 11-14: our as-of is printed from the data just before this; a typed "August 2026" went stale on refresh
     "prior_links": [("GAO-27-108012 interactive county map and data download", "https://files.gao.gov/multimedia/gao-27-108012/interactive/index.html"),
                     ("Neptune Flood analysis as reported by InsuranceNewsNet", "https://insurancenewsnet.com/oarticle/2-6-billion-in-nfip-subsidies-remain-five-years-into-risk-rating-2-0-neptune-flood-research-group-analysis-of-fema-data-shows")],
     "csv_note": f"share_pct, ci90_low_pct, ci90_high_pct and numerator count policies at least ${GAP_MIN} a year below full-risk; below_any_amount_n, below_any_amount_pct and median_gap_usd_below_any_amount count policies below by any amount (the median gap is blank where fewer than {GAP_MED_MIN} are below).",
     "prior_rules": [], "policy_col": False, "published": None, "rules": []})
READY = [s for s in SPECS if s.get("ready")]   # a paper ships only after tools/paper_gate.py and both reviews pass (PAPER-GATE-PROMPT)

def names():
    return json.load(open(os.path.join(ROOT, "data", "us", "county_names.json"), encoding="utf-8"))

def _get(rec, path):
    if callable(path): return path(rec)   # a derived count (Deductible Choice sums deductible amounts)
    v = rec
    for k in path: v = v.get(k) if isinstance(v, dict) else None
    return v

def wilson(k, n, z=Z90):
    """90% Wilson score interval for k of n, in percent, one decimal."""
    if not n: return None, None
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return max(0.0, round(100 * (c - h) / d, 1)) + 0.0, min(100.0, round(100 * (c + h) / d, 1)) + 0.0   # never "-0.0%" at k = 0

def rows(spec, recs=None):
    """Every county whose count base meets the minimum: share = num/den on one base, 90% interval, fifth (1 = highest share)."""
    recs = recs if recs is not None else load()
    out = []
    for g, r in recs.items():
        k, n = _get(r, spec["num"]), _get(r, spec["den"])
        if isinstance(k, int) and isinstance(n, int) and n >= spec["min"] and 0 <= k <= n:
            lo, hi = wilson(k, n)
            e = spec["null"](n) if spec.get("null") else None   # Flood Calendar: expected share at random for this n
            out.append({"geoid": g, "state": r.get("state", ""), "k": k, "n": n, "value": round(100 * k / n, 1), "lo": lo, "hi": hi,
                        "exp": e, "excess": None if e is None else round(round(100 * k / n, 1) - e, 1)})   # printed share minus printed expected (review 11-14)
    out.sort(key=lambda x: (-(x["k"] / x["n"] - (x["exp"] or 0) / 100), x["geoid"]))   # with a null: ranked on share minus chance (unrounded; printed excess stays in order, gate checks)   # with a null: ranked on share minus chance
    N = len(out)
    first = {}   # review 11-13: an equal printed share (or excess) always gets the same fifth (the fifth of its first, highest-placed row)
    for i, x in enumerate(out): x["fifth"] = first.setdefault(x["value"] if x["excess"] is None else x["excess"], 1 + (5 * i) // N)
    return out

ONE_YEAR_MIN = 10   # methods review underinsured-2 N1: fewer claims than this over coverage and one year holding most is noise, not a flag

def context(spec, rec, w0, w1):
    """Per-row context the statistics review asked for (methods review outside-zone-2, M1): the county's policy units outside
    zones A and V today (policies.sfha_share_units is the share inside A and V); the median amount over coverage (M1.4); the loss year
    holding over half of the county's numerator, if any (M1.8). None where FEMA's record has no value."""
    sf = _get(rec, ("policies", "sfha_share_units"))
    by = _get(rec, spec["by_year"]) if spec.get("by_year") else None
    top = max(by.items(), key=lambda kv: (kv[1], kv[0])) if isinstance(by, dict) and by else None   # M1.8: a year with over half
    ex = _get(rec, spec["excess"]) if spec.get("excess") else None
    out = {"pol_out": round(100 - sf, 1) if isinstance(sf, (int, float)) else None, "excess": ex if isinstance(ex, (int, float)) else None,
           "one_year": top[0] if top and 2 * top[1] > sum(by.values()) and sum(by.values()) >= ONE_YEAR_MIN else None}
    if spec.get("gap"): out.update(gap_ctx(rec))   # Price Gap M2: any-amount share and median gap beside the $100 share
    if spec.get("months"):   # Flood Calendar: tied peak months all named; each peak month's year-month holding over half (10+ claims)
        b = _bm(rec) or {}; ym = _get(rec, ("extras", "claims", "loss_month_n", "by_year_month")) or {}
        pk = max(b.values()) if b else 0
        out["peak"] = sorted(k for k, v in b.items() if v == pk)
        out["storm"] = []
        for mo in out["peak"] if pk >= ONE_YEAR_MIN else []:
            t = max(((y, v) for y, v in ym.items() if y[5:] == mo and isinstance(v, int)), key=lambda kv: (kv[1], kv[0]), default=None)
            if t and 2 * t[1] > pk: out["storm"].append(t[0])
        out["years"] = [sum(1 for y, v in ym.items() if y[5:] == mo and isinstance(v, int) and v > 0) for mo in out["peak"]]   # distinct loss years
        # review round 3 M1/M2: graded, not just a flag: years with ONE_YEAR_MIN+ claims, and the largest year's share of each peak month
        out["years10"] = [sum(1 for y, v in ym.items() if y[5:] == mo and isinstance(v, int) and v >= ONE_YEAR_MIN) for mo in out["peak"]]
        out["top_share"] = [round(100 * max((v for y, v in ym.items() if y[5:] == mo and isinstance(v, int)), default=0) / pk, 1) if pk else None for mo in out["peak"]]
    return out

def month_words(c):   # "September", "August and September"; flag "September 2017"
    return (" and ".join(MONTHS[int(x) - 1] for x in c["peak"]), " and ".join(f"{MONTHS[int(y[5:]) - 1]} {y[:4]}" for y in c["storm"]))

def pooled_boot(rows_, B=2000, seed=20261113):
    """90% range of the pooled share, resampling whole counties (review M2: claims in one county are not independent)."""
    import random
    rnd = random.Random(seed); n = len(rows_); vals = []
    for _ in range(B):
        s = [rows_[rnd.randrange(n)] for _ in range(n)]
        vals.append(100 * sum(x["k"] for x in s) / sum(x["n"] for x in s))
    vals.sort()
    return round(vals[int(0.05 * B)], 1), round(vals[int(0.95 * B) - 1], 1)

def all_pooled(spec, recs):
    """Pooled share over EVERY county with at least one record in the base (review outside-zone-3 M2): the figure to set beside FEMA's."""
    ks = [(_get(r, spec["num"]), _get(r, spec["den"])) for r in recs.values()]
    ks = [(k, n) for k, n in ks if isinstance(k, int) and isinstance(n, int) and n > 0 and 0 <= k <= n]
    return round(100 * sum(k for k, _ in ks) / sum(n for _, n in ks), 1), sum(n for _, n in ks)

def corr(pairs):
    """Pearson correlation of (x, y) pairs, two decimals (descriptive only; no test). None with fewer than 3 pairs."""
    pairs = [(x, y) for x, y in pairs if x is not None and y is not None]
    if len(pairs) < 3: return None
    n = len(pairs); mx = sum(x for x, _ in pairs) / n; my = sum(y for _, y in pairs) / n
    sxy = sum((x - mx) * (y - my) for x, y in pairs); sx = sum((x - mx) ** 2 for x, _ in pairs) ** 0.5; sy = sum((y - my) ** 2 for _, y in pairs) ** 0.5
    return round(sxy / (sx * sy), 2) if sx and sy else None

def excluded(spec, recs):
    """Counties with 1..min-1 records in the base (review M3: selection): count, median share, pooled share."""
    ex = [(_get(r, spec["num"]), _get(r, spec["den"])) for r in recs.values()]
    ex = [(k, n) for k, n in ex if isinstance(k, int) and isinstance(n, int) and 0 < n < spec["min"] and 0 <= k <= n]
    if not ex: return 0, None, None
    import statistics
    return len(ex), round(statistics.median(100 * k / n for k, n in ex), 1), round(100 * sum(k for k, _ in ex) / sum(n for _, n in ex), 1)

def skipped(spec, recs):
    nul = sum(1 for r in recs.values() if not isinstance(_get(r, spec["den"]), int) or _get(r, spec["den"]) == 0)
    small = sum(1 for r in recs.values() if isinstance(_get(r, spec["den"]), int) and 0 < _get(r, spec["den"]) < spec["min"])
    return nul, small

def window(spec, recs):
    if not spec.get("window"): return None, None   # a policy snapshot has no loss window
    for r in recs.values():
        w = _get(r, spec["window"])
        if isinstance(w, dict) and w.get("from"): return w["from"], w["to"]
    return None, None

def load():
    return {f[:5]: json.load(open(os.path.join(ALL, f))) for f in sorted(os.listdir(ALL)) if f.endswith(".json")}

def write_cache():
    recs = load(); out = {}
    for s in READY:
        rs = rows(s, recs)
        # named fields, never positions (bug review 11-14: a new field would have shifted the county card's figures)
        out[s["key"]] = {"pool": len(rs), "from_to": window(s, recs), "rows": {x["geoid"]: {"fifth": x["fifth"], "v": x["value"], "lo": x["lo"], "hi": x["hi"], "n": x["n"],
                                                   **(dict(zip(("peak", "storm"), month_words(context(s, recs[x["geoid"]], 0, 0))), exp=x["exp"]) if s.get("months") else {})} for x in rs}}
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    json.dump(out, open(CACHE, "w"))
    return out

def read_cache():
    try: return json.load(open(CACHE))
    except Exception: return {}

if __name__ == "__main__":   # self-check: interval, base, fifths
    lo, hi = wilson(10, 100); assert (lo, hi) == (6.1, 16.0), (lo, hi)   # hand-checked: z=1.64485, (0.1135 -+ 0.0512) / 1.0271
    S = {"num": ("a",), "den": ("b",), "min": 2}
    r = rows(S, {"1": {"a": 1, "b": 2}, "2": {"a": 3, "b": 1}, "3": {"a": 0, "b": 1}, "4": {"a": 2, "b": 2}, "5": {"a": None, "b": 5}})
    assert [(x["geoid"], x["value"]) for x in r] == [("4", 100.0), ("1", 50.0)], r   # k > n and n < min left out
    assert [x["fifth"] for x in r] == [1, 3]
    r = rows(S, {str(i): {"a": a, "b": 2} for i, a in enumerate([2, 1, 1, 1, 0])})   # three tied 50% rows span fifths 2-4
    assert [x["fifth"] for x in r] == [1, 2, 2, 2, 5], [x["fifth"] for x in r]
    assert str(wilson(0, 163)[0]) == "0.0" and str(wilson(163, 163)[1]) == "100.0", (wilson(0, 163), wilson(163, 163))
    T = {"by_year": ("y",), "excess": ("x",)}
    assert context(T, {"y": {"2021": 6, "2019": 4}, "x": 9}, 0, 0) == {"pol_out": None, "excess": 9, "one_year": "2021"}
    assert context(T, {"y": {"2021": 5, "2019": 5}}, 0, 0)["one_year"] is None   # exactly half is not over half
    assert context(T, {"y": {"2021": 6, "2019": 3}}, 0, 0)["one_year"] is None   # 9 claims: under ONE_YEAR_MIN, never flagged
    R = {"extras": {"policies": {"deductible_units": {"1250": 5, "5000": 3, "10000": 2}}}}
    assert (ded_units(R, DED_MIN), ded_units(R, 0)) == (5, 10) and ded_units({}, 0) is None
    L = lambda bm, ym=None: {"extras": {"claims": {"loss_month_n": {"by_month": bm, "by_year_month": ym or {}}}}}
    assert cal_k({}) is None and cal_n(L({})) is None and cal_n(L({"13": 5, "09": "x"})) is None   # empty, bad key, bad count
    C = {"months": True}
    c = context(C, L({"08": 6, "09": 6, "01": 1}, {"2017-08": 6, "2017-09": 3, "2020-09": 3}), 0, 0)
    assert c["peak"] == ["08", "09"] and c["storm"] == [] and cal_k(L({"08": 6, "09": 6})) == 6   # tie named; 6 < ONE_YEAR_MIN
    c = context(C, L({"09": 20, "01": 1}, {"2017-09": 11, "2018-09": 9}), 0, 0)
    assert c["storm"] == ["2017-09"] and month_words(c) == ("September", "September 2017"), c
    assert context(C, L({"09": 20}, {"2017-09": 10, "2018-09": 10}), 0, 0)["storm"] == []   # exactly half: not over half
    c = context(C, L({"09": 20, "01": 1}, {"2017-09": 11, "2018-09": 9, "2019-09": 0}), 0, 0); assert c["years"] == [2], c   # zero year-month not a year
    assert (c["years10"], c["top_share"]) == ([1], [55.0]), c   # 9 claims is not a 10+ year; 11 of 20 = 55.0%
    c = context(C, L({"08": 12, "09": 12}, {"2017-08": 12, "2016-09": 6, "2017-09": 6}), 0, 0)
    assert (c["years10"], c["top_share"], c["storm"]) == ([1, 0], [100.0, 50.0], ["2017-08"]), c   # tied months graded each
    assert context(C, L({"09": 120}), 0, 0)["top_share"] == [0.0]   # no year-months: 0.0, and paper_gate's months_add_up fails it
    assert [chance_peak(n) for n in (100, 473, 2000)] == [13.3, 10.6, 9.4]   # statistician's independent simulation, round 2
    N0 = {"num": ("a",), "den": ("b",), "min": 1, "null": lambda n: {100: 13.3, 2000: 9.4}[n]}
    r = rows(N0, {"1": {"a": 20, "b": 100}, "2": {"a": 300, "b": 2000}})   # excess 20.0 - 13.3 = 6.7 ranks above 15.0 - 9.4 = 5.6
    assert [(x["geoid"], x["excess"]) for x in r] == [("1", 6.7), ("2", 5.6)], r
    r = rows({**N0, "null": lambda n: 10.8}, {"1": {"a": 6725, "b": 10000}})   # bug review 11-14: excess is printed share minus printed expected
    assert r[0]["excess"] == round(r[0]["value"] - 10.8, 1), r
    r = rows(N0, {"1": {"a": 18, "b": 100}, "2": {"a": 300, "b": 2000}})   # higher share (18.0) but lower excess (4.7) ranks second
    assert [x["geoid"] for x in r] == ["2", "1"], r
    G = lambda k, n, md: {"policies": {"below_k": k, "below_n": n, "below_gap_median": md}}
    assert gap_ctx(G(29, 40, 500))["gap_med"] is None and gap_ctx(G(30, 40, 500)) == {"any_k": 30, "any_pct": 75.0, "gap_med": 500}   # 29 below: no median
    assert gap_ctx({})["any_pct"] is None and gap_ctx(G(None, 40, 5))["any_k"] is None   # old data: no column value, never a crash
    import re   # bug review 11-14: a paper's own text never types a month-year; only the cited study's fixed April 2026 snapshot
    for s in SPECS:
        for t in [s.get("reconcile", ("", ""))[1], s.get("csv_note", "")]:
            assert not re.search(r"\b(?!April )[A-Z][a-z]+ 20\d\d\b", t), (s["key"], t)
    print("papers self-test OK")
