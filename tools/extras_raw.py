"""Streaming pass over the raw pulls for the figures no competitor shows (report Tier 1, items 1-19). Nothing is
held per record, only per-county value lists, so Florida's 1.1M policies fit in memory. Same cohort as ffcalc
(single-family primary residences) for every premium figure; shares of all policies use policy units.
Writes data/states/<slug>/extras.json and per-county blocks merged into data/all-counties/<geoid>.json,
plus data/us/cost_hist.json (national cost histogram for the "vs the U.S." comparison).
Usage: python -I tools/extras_raw.py [ST ...]"""
import collections, csv, glob, gzip, json, os, statistics, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ffcalc
from codes import NONPAY_REASON, CAUSE, DEDUCTIBLE, truthy
from agg_raw import NAMES, slug, RAW, ROOT, FIPS

RR2_NEW = "2021-10-01"     # new NFIP policies from this date are rated under Risk Rating 2.0 (rules_registry: rr2_start)

def f(v):
    try: return float(v) if v not in ("", None) else None
    except ValueError: return None

def med(xs): return round(statistics.median(xs)) if xs else None
def pct(a, b): return round(100 * a / b, 1) if b else None

def rows(ds, st):
    for p in sorted(glob.glob(os.path.join(RAW, ds, st, "*.csv.gz"))):
        yield from csv.DictReader(gzip.open(p, "rt", encoding="utf-8"))

def new_acc():
    return {"units": 0, "mand_units": 0, "tenant_units": 0, "condo_unit_units": 0, "rcbap_units": 0, "elev_units": 0,
            "gf_units": 0, "prem_new": [], "prem_old": [], "prem_elev": [], "prem_low": [], "sf_n": 0, "sf_max_cov": 0,
            "rc_n": 0, "rc_over": 0, "fee": [], "hfiaa": [], "reserve": [], "icc": [], "ded": collections.Counter(),
            "cost_hist": collections.Counter(), "all_cost": [], "sf_cost": [], "sf_prem": []}

def policies(st):
    acc = collections.defaultdict(new_acc)
    for r in rows("NfipPolicies", st):
        u = int(f(r["policyCount"]) or 0)
        keys = ["ST"] + [g for g in [(r["censusGeoid"] or "")[:5]] if g[:2] == FIPS[st]]   # never another state's county
        sf = ffcalc.isone(r["occupancyType"]) and ffcalc.istrue(r["primaryResidenceIndicator"])
        prem, cost = f(r[ffcalc.PREM]), f(r["policyCost"])
        for k in keys:
            if len(k) not in (2, 5): continue
            a = acc[k]; a["units"] += u
            if truthy(r["mandatoryPurchaseFlag"]): a["mand_units"] += u
            if truthy(r["tenantIndicator"]): a["tenant_units"] += u
            if r["condominiumCoverageTypeCode"] == "U": a["condo_unit_units"] += u
            if r["condominiumCoverageTypeCode"] in ("H", "L"): a["rcbap_units"] += u
            if truthy(r["elevatedBuildingIndicator"]): a["elev_units"] += u
            if r["grandfatheringTypeCode"] in ("2", "3"): a["gf_units"] += u
            if k == "ST" and cost and cost > 0: a["all_cost"].append(cost)    # every policy type: the "all policies" average
            if not sf: continue
            a["sf_n"] += 1
            if cost and cost > 0:
                a["cost_hist"][round(cost)] += 1
                if k == "ST": a["sf_cost"].append(cost)
            if k == "ST" and prem and prem > 0: a["sf_prem"].append(prem)
            if prem and prem > 0:
                (a["prem_new"] if (r["originalNBDate"] or "")[:10] >= RR2_NEW else a["prem_old"]).append(prem)
                (a["prem_elev"] if truthy(r["elevatedBuildingIndicator"]) else a["prem_low"]).append(prem)
            if (f(r["totalBuildingInsuranceCoverage"]) or 0) >= 250000: a["sf_max_cov"] += 1
            rc = f(r["buildingReplacementCost"])
            if rc and rc > 0:
                a["rc_n"] += 1; a["rc_over"] += rc > 250000
            for col, key in (("federalPolicyFee", "fee"), ("hfiaaSurcharge", "hfiaa"), ("reserveFundAssessment", "reserve"), ("iccPremium", "icc")):
                v = f(r[col])
                if v is not None and v >= 0: a[key].append(v)
            if r["buildingDeductibleCode"] in DEDUCTIBLE: a["ded"][DEDUCTIBLE[r["buildingDeductibleCode"]]] += 1
    out = {}
    for k, a in acc.items():
        n_ded = sum(a["ded"].values())
        out[k] = {"lender_required_pct": pct(a["mand_units"], a["units"]), "tenant_pct": pct(a["tenant_units"], a["units"]),
                  "condo_unit_pct": pct(a["condo_unit_units"], a["units"]), "condo_building_pct": pct(a["rcbap_units"], a["units"]),
                  "elevated_pct": pct(a["elev_units"], a["units"]), "grandfathered_pct": pct(a["gf_units"], a["units"]),
                  "prem_new_median": med(a["prem_new"]), "prem_new_n": len(a["prem_new"]),
                  "prem_old_median": med(a["prem_old"]), "prem_old_n": len(a["prem_old"]),
                  "prem_elevated_median": med(a["prem_elev"]), "prem_elevated_n": len(a["prem_elev"]),
                  "prem_not_elevated_median": med(a["prem_low"]), "prem_not_elevated_n": len(a["prem_low"]),
                  "at_building_max_pct": pct(a["sf_max_cov"], a["sf_n"]), "replacement_over_250k_pct": pct(a["rc_over"], a["rc_n"]),
                  "replacement_n": a["rc_n"], "fee_mean": round(statistics.mean(a["fee"])) if a["fee"] else None,
                  "hfiaa_mean": round(statistics.mean(a["hfiaa"])) if a["hfiaa"] else None,
                  "reserve_mean": round(statistics.mean(a["reserve"])) if a["reserve"] else None,
                  "icc_premium_mean": round(statistics.mean(a["icc"])) if a["icc"] else None,
                  "deductibles": {str(d): pct(c, n_ded) for d, c in a["ded"].most_common(4)}, "sf_n": a["sf_n"]}
        if k == "ST":
            out[k]["cost_hist"] = dict(a["cost_hist"])
            out[k]["averages"] = {"sf_cost_median": med(a["sf_cost"]), "sf_cost_mean": round(statistics.mean(a["sf_cost"])) if a["sf_cost"] else None,
                                  "sf_prem_median": med(a["sf_prem"]), "sf_prem_mean": round(statistics.mean(a["sf_prem"])) if a["sf_prem"] else None,
                                  "all_cost_median": med(a["all_cost"]), "all_cost_mean": round(statistics.mean(a["all_cost"])) if a["all_cost"] else None,
                                  "sf_n": len(a["sf_cost"]), "all_n": len(a["all_cost"])}
    return out

def net(r): return sum(f(r[c]) or 0 for c in ("netBuildingPaymentAmount", "netContentsPaymentAmount", "netIccPaymentAmount"))

def claims(st):
    acc = collections.defaultdict(lambda: {"n": 0, "unpaid": 0, "reason": collections.Counter(), "cause": collections.Counter(),
                                           "depth": [], "event": collections.defaultdict(lambda: [0, 0.0, collections.Counter()]), "icc_n": 0, "icc": [],
                                           "dmg": [], "paid_b": [], "over_cov": 0, "dmg_n": 0, "elev_paid": [], "low_paid": []})
    for r in rows("NfipClaims", st):
        paid = net(r)
        for k in ["ST"] + [g for g in [r["countyCode"] or ""] if g[:2] == FIPS[st]]:
            if len(k) not in (2, 5): continue
            a = acc[k]; a["n"] += 1
            if paid <= 0:
                a["unpaid"] += 1
                if r["nonPaymentReasonBuilding"] in NONPAY_REASON: a["reason"][r["nonPaymentReasonBuilding"]] += 1
                continue
            for ch in set(r["causeOfDamage"] or ""):
                if ch in CAUSE: a["cause"][ch] += 1
            d = f(r["waterDepth"])
            if d and 0 < d < 400: a["depth"].append(d)
            ev = (r["floodEvent"] or "").strip()
            if ev: e = a["event"][ev]; e[0] += 1; e[1] += paid; e[2][r["yearOfLoss"]] += 1
            icc = f(r["netIccPaymentAmount"]) or 0
            if icc > 0: a["icc_n"] += 1; a["icc"].append(icc)
            dmg, cov, pb = f(r["buildingDamageAmount"]), f(r["totalBuildingInsuranceCoverage"]), f(r["netBuildingPaymentAmount"])
            if dmg and dmg > 0 and pb and pb > 0:
                a["dmg"].append(dmg); a["paid_b"].append(pb); a["dmg_n"] += 1
                if cov and dmg > cov: a["over_cov"] += 1
            (a["elev_paid"] if truthy(r["elevatedBuildingIndicator"]) else a["low_paid"]).append(paid)
    out = {}
    for k, a in acc.items():
        n_reason = sum(a["reason"].values()); n_cause = sum(a["cause"].values()); paid_n = a["n"] - a["unpaid"]
        out[k] = {"unpaid_reasons": [{"code": c, "label": NONPAY_REASON[c], "pct": pct(v, n_reason), "n": v} for c, v in a["reason"].most_common(5)],
                  "unpaid_n": a["unpaid"], "unpaid_with_reason_pct": pct(n_reason, a["unpaid"]),
                  "causes": [{"code": c, "label": CAUSE[c], "pct": pct(v, n_cause)} for c, v in a["cause"].most_common(4)],
                  "depth_median_in": med(a["depth"]), "depth_n": len(a["depth"]),
                  "events": [{"name": e, "claims": v[0], "paid": round(v[1]), "avg": round(v[1] / v[0]),
                              "years": sorted(y for y in v[2] if y)}   # years of loss on its paid claims
                             for e, v in sorted(a["event"].items(), key=lambda kv: -kv[1][1])[:8]],
                  "icc_claims": a["icc_n"], "icc_avg": round(statistics.mean(a["icc"])) if a["icc"] else None,
                  "damage_median": med(a["dmg"]), "paid_building_median": med(a["paid_b"]),
                  "damage_over_coverage_pct": pct(a["over_cov"], a["dmg_n"]), "damage_n": a["dmg_n"],
                  "avg_paid_elevated": round(statistics.mean(a["elev_paid"])) if len(a["elev_paid"]) >= 30 else None,
                  "avg_paid_not_elevated": round(statistics.mean(a["low_paid"])) if len(a["low_paid"]) >= 30 else None,
                  "elevated_paid_n": len(a["elev_paid"]), "paid_n": paid_n}
    return out

def run(st):
    if not all(os.path.exists(os.path.join(RAW, ds, st + ".done")) for ds in ("NfipPolicies", "NfipClaims")):
        print(st, "skipped: pull not finished"); return
    p, c = policies(st), claims(st)
    d = os.path.join(ROOT, "data", "states", slug(st)); os.makedirs(d, exist_ok=True)
    hist = p["ST"].pop("cost_hist")
    os.makedirs(os.path.join(ROOT, "data", "us"), exist_ok=True)
    hp = os.path.join(ROOT, "data", "us", "cost_hist.json")
    allh = json.load(open(hp)) if os.path.exists(hp) else {}
    allh[st] = hist; json.dump(allh, open(hp, "w"))
    json.dump({"policies": p["ST"], "claims": c.get("ST", {})}, open(os.path.join(d, "extras.json"), "w"))
    for g in set(p) | set(c):
        if g == "ST": continue
        cp = os.path.join(ROOT, "data", "all-counties", g + ".json")
        if os.path.exists(cp):
            j = json.load(open(cp)); j["extras"] = {"policies": p.get(g, {}), "claims": c.get(g, {})}; json.dump(j, open(cp, "w"))
    s = p["ST"]; cl = c.get("ST", {})
    print(f"{st}: lender-required {s['lender_required_pct']}%, new vs old premium {s['prem_new_median']}/{s['prem_old_median']}, "
          f"top unpaid reason {(cl.get('unpaid_reasons') or [{}])[0].get('label')}, top event {(cl.get('events') or [{}])[0].get('name')}")

if __name__ == "__main__":
    for st in (sys.argv[1:] or sorted(NAMES)):
        run(st)
