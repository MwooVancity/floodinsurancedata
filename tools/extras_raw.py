"""Streaming pass over the raw pulls for the figures no competitor shows (report Tier 1, items 1-19). Nothing is
held per record, only per-county value lists, so Florida's 1.1M policies fit in memory. Same cohort as ffcalc
(single-family primary residences) for every premium figure; shares of all policies use policy units.
Writes data/states/<slug>/extras.json and per-county blocks merged into data/all-counties/<geoid>.json,
plus data/us/cost_hist.json (national cost histogram for the "vs the U.S." comparison).
Usage: python -I tools/extras_raw.py [ST ...]"""
import collections, csv, glob, gzip, json, os, statistics, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ffcalc
import metrics as MX
from codes import NONPAY_REASON, CAUSE, DEDUCTIBLE, truthy
from agg_raw import NAMES, slug, RAW, ROOT, FIPS

RR2_NEW = "2021-10-01"     # new NFIP policies from this date are rated under Risk Rating 2.0 (rules_registry: rr2_start)
import datetime
from agg_raw import asof as _asof
_A = datetime.date.fromisoformat(_asof())
RECENT_FROM = "2020"   # fixed start, so the period never drifts between refreshes
LOSS_TO = str(_A.year - 1); LOSS_FROM = str(_A.year - 10)   # ten whole loss years before the as-of year (debate 11-05: no 1978+ average)
NB_FROM = str(_A.replace(year=_A.year - 1) + datetime.timedelta(days=1))   # first written in the 12 months to the as-of date

def f(v):
    try: return float(v) if v not in ("", None) else None
    except ValueError: return None

def med(xs): return round(statistics.median(xs)) if xs else None
def pct(a, b): return round(100 * a / b, 1) if b else None

def rows(ds, st):
    for p in sorted(glob.glob(os.path.join(RAW, ds, st, "*.csv.gz"))):
        yield from csv.DictReader(gzip.open(p, "rt", encoding="utf-8"))

# Renters (11-07): residential occupancy only, codes from FEMA's NfipPolicies data dictionary (metric_defs.json, sha-checked
# by recheck): 1, 2, 3 legacy residential; 11, 12, 13, 14 (mobile home), 16 (unit in a multi-unit building) Risk Rating 2.0.
# Out: 4, 6, 17, 18, 19 non-residential; 15 condo association; blank or any code FEMA adds later.
RENTER_OCC = {"1", "2", "3", "11", "12", "13", "14", "16"}

def new_acc():
    return {"condo_cost": [], "units": 0, "mand_units": 0, "tenant_units": 0, "condo_unit_units": 0, "rcbap_units": 0, "elev_units": 0,
            "gf_units": 0, "prem_new": [], "prem_old": [], "prem_elev": [], "prem_low": [], "sf_n": 0, "sf_max_cov": 0,
            "rc_n": 0, "rc_over": 0, "fee": [], "hfiaa": [], "reserve": [], "icc": [], "ded": collections.Counter(),
            "cost_hist": collections.Counter(), "cost_hist_new": collections.Counter(), "zone_hist": {}, "zone_hist_exact": {}, "renter_hist": collections.Counter(), "renter_units": 0, "frp_hist_exact": {}, "all_cost": [], "sf_cost": [], "sf_prem": [], "sf_new_cost": [],
            "trend": collections.defaultdict(lambda: [0, []])}   # year -> [single-family records, their costs > 0]

def policies(st):
    acc = collections.defaultdict(new_acc)
    for r in rows("NfipPolicies", st):
        u = int(f(r["policyCount"]) or 0)
        keys = ["ST"] + [g for g in [(r["censusGeoid"] or "")[:5]] if g[:2] == FIPS[st]]   # never another state's county
        sf = ffcalc.is_sf_home(r)
        prem, cost = f(r[ffcalc.PREM]), f(r["policyCost"])
        for k in keys:
            if len(k) not in (2, 5): continue
            a = acc[k]; a["units"] += u
            if truthy(r["mandatoryPurchaseFlag"]): a["mand_units"] += u
            if truthy(r["tenantIndicator"]): a["tenant_units"] += u
            if k == "ST" and r["occupancyType"].strip() in RENTER_OCC and truthy(r["tenantIndicator"]) and not (f(r["totalBuildingInsuranceCoverage"]) or 0) and (f(r["totalContentsInsuranceCoverage"]) or 0) > 0:
                a["renter_units"] += u   # renters page (owner 11-06): tenant, contents-only policies; cost histogram below
                if cost and cost > 0: a["renter_hist"][round(cost)] += 1
            if r["condominiumCoverageTypeCode"] == "U":
                a["condo_unit_units"] += u
                if cost and cost > 0: a["condo_cost"].append(cost)   # backlog r12 Horry: what condo-unit owners pay (premium plus fees)
            if r["condominiumCoverageTypeCode"] in ("H", "L"): a["rcbap_units"] += u
            if truthy(r["elevatedBuildingIndicator"]): a["elev_units"] += u
            if r["grandfatheringTypeCode"] in ("2", "3"): a["gf_units"] += u
            if cost and cost > 0: a["all_cost"].append(cost)    # every policy type: the "all policies" average (county too: hater r5)
            if not sf: continue
            a["sf_n"] += 1
            if cost and cost > 0:
                a["cost_hist"][round(cost)] += 1
                if k == "ST":   # backlog 1: U.S. cost by zone group (A high-risk, V coastal high-risk, B/C/X moderate-low); D and blank left out
                    _z = (r["ratedFloodZone"] or "").upper()[:1]
                    _zg = "A" if _z == "A" else "V" if _z == "V" else "X" if _z in ("B", "C", "X") else None
                    if _zg: a["zone_hist"].setdefault(_zg, collections.Counter())[round(cost)] += 1
                    _ze = (r["ratedFloodZone"] or "").strip().upper()   # exact zone (AE, X, VE, AO...): zone pages' own median
                    if _ze: a["zone_hist_exact"].setdefault(_ze, collections.Counter())[round(cost)] += 1
                    _frp = f(r["fullRiskPremium"])   # premium only, before fees: what the rate moves toward
                    if _ze and _frp and _frp > 0: a["frp_hist_exact"].setdefault(_ze, collections.Counter())[round(_frp)] += 1
                if (r["originalNBDate"] or "")[:10] >= NB_FROM: a["sf_new_cost"].append(cost); a["cost_hist_new"][round(cost)] += 1
                a["sf_cost"].append(cost)
            if prem and prem > 0: a["sf_prem"].append(prem)
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
    # 11-09 "is it rising?": the same cohort and cost on the as-of day of each of the 5 years before (pull_bulk.trend writes
    # the rows); none on disk (first run, failed pass) = no trend, so no page shows one
    for r in rows("NfipPoliciesTrend", st):
        if not ffcalc.is_sf_home(r): continue
        c = f(r["policyCost"])
        for k in ["ST"] + [g for g in [(r["censusGeoid"] or "")[:5]] if g[:2] == FIPS[st] and len(g) == 5]:
            t = acc[k]["trend"][int(r["year"])]; t[0] += 1
            if c and c > 0: t[1].append(c)
    out = {}
    for k, a in acc.items():
        n_ded = sum(a["ded"].values())
        out[k] = {"lender_required_pct": pct(a["mand_units"], a["units"]), "tenant_pct": pct(a["tenant_units"], a["units"]),
                  "condo_unit_pct": pct(a["condo_unit_units"], a["units"]), "condo_building_pct": pct(a["rcbap_units"], a["units"]),
                  "condo_unit_cost_median": med(a["condo_cost"]) if len(a["condo_cost"]) >= MX.CONST["min_priced"] else None, "condo_unit_cost_n": len(a["condo_cost"]),
                  "elevated_pct": pct(a["elev_units"], a["units"]), "grandfathered_pct": pct(a["gf_units"], a["units"]),
                  "prem_new_median": med(a["prem_new"]), "prem_new_n": len(a["prem_new"]),
                  "prem_old_median": med(a["prem_old"]), "prem_old_n": len(a["prem_old"]),
                  "cost_new_median": med(a["sf_new_cost"]), "cost_new_n": len(a["sf_new_cost"]),
                  "prem_elevated_median": med(a["prem_elev"]), "prem_elevated_n": len(a["prem_elev"]),
                  "prem_not_elevated_median": med(a["prem_low"]), "prem_not_elevated_n": len(a["prem_low"]),
                  "at_building_max_pct": pct(a["sf_max_cov"], a["sf_n"]), "replacement_over_250k_pct": pct(a["rc_over"], a["rc_n"]),
                  "replacement_n": a["rc_n"], "fee_mean": round(statistics.mean(a["fee"])) if a["fee"] else None,
                  "hfiaa_mean": round(statistics.mean(a["hfiaa"])) if a["hfiaa"] else None,
                  "reserve_mean": round(statistics.mean(a["reserve"])) if a["reserve"] else None,
                  "icc_premium_mean": round(statistics.mean(a["icc"])) if a["icc"] else None,
                  "deductibles": {str(d): pct(c, n_ded) for d, c in a["ded"].most_common(4)}, "sf_n": a["sf_n"]}
        if k == "ST":   # histograms and counts the home page sums into exact U.S. figures
            out[k]["cost_hist"] = dict(a["cost_hist"]); out[k]["cost_hist_new"] = dict(a["cost_hist_new"])
            out[k]["cost_hist_zone"] = {g: dict(h) for g, h in a["zone_hist"].items()}
            out[k]["cost_hist_zone_exact"] = {g: dict(h) for g, h in a["zone_hist_exact"].items()}
            out[k]["renter_hist"] = dict(a["renter_hist"]); out[k]["renter_units"] = a["renter_units"]
            out[k]["frp_hist_zone_exact"] = {g: dict(h) for g, h in a["frp_hist_exact"].items()}
            out[k]["ded_counts"] = {str(d): c for d, c in a["ded"].items()}
        out[k]["averages"] = {"sf_cost_median": med(a["sf_cost"]), "sf_cost_mean": round(statistics.mean(a["sf_cost"])) if a["sf_cost"] else None,   # every state and county (hater r5)
                              "sf_prem_median": med(a["sf_prem"]), "sf_prem_mean": round(statistics.mean(a["sf_prem"])) if a["sf_prem"] else None,
                              "all_cost_median": med(a["all_cost"]), "all_cost_mean": round(statistics.mean(a["all_cost"])) if a["all_cost"] else None,
                              "sf_n": len(a["sf_cost"]), "sf_prem_n": len(a["sf_prem"]), "all_n": len(a["all_cost"])}
        # a year's median only when 30+ are priced, FEMA gives a cost for 90%+ of that year's single-family records here, and
        # that year's record count is within half to twice today's (older records may place homes in other county codes:
        # Connecticut's 2022 planning regions); the as-of year is this run's own rows, the headline's rule (gate C17 checks)
        _tr = sorted(a["trend"].items()) + [(_A.year, [a["sf_n"], a["sf_cost"]])]
        out[k]["cost_trend"] = [{"year": y, "n": len(cs), "sf_n": n,
                                 "median": med(cs) if len(cs) >= MX.CONST["min_priced"] and 100 * len(cs) >= MX.CONST["trend_fill_pct"] * n
                                 and a["sf_n"] <= 2 * n <= 4 * a["sf_n"] else None}
                                for y, (n, cs) in _tr] if a["trend"] else []
    return out

def net(r): return sum(f(r[c]) or 0 for c in ("netBuildingPaymentAmount", "netContentsPaymentAmount", "netIccPaymentAmount"))

def claims(st):
    acc = collections.defaultdict(lambda: {"n": 0, "unpaid": 0, "reason": collections.Counter(), "cause": collections.Counter(),
                                           # event: [paid claims, paid $, loss years, unpaid claims]
                                           "depth": [], "event": collections.defaultdict(lambda: [0, 0.0, collections.Counter(), 0]), "icc_n": 0, "icc": [],
                                           "dmg": [], "paid_b": [], "over_cov": 0, "dmg_n": 0, "elev_paid": [], "low_paid": [],
                                           "dec": collections.defaultdict(lambda: [0, 0]),   # decade of loss: [claims, paid something]
                                           "zone": collections.defaultdict(lambda: [0, 0, 0.0]),
                                           "recent": [0, 0, collections.Counter()]})   # loss year RECENT_FROM+: [claims, paid, reason codes of the unpaid] (claims research page)   # zone on the claim, loss years LOSS_FROM..LOSS_TO: [claims, paid, dollars]
    for r in rows("NfipClaims", st):
        paid = net(r)
        err = r["nonPaymentReasonBuilding"] in ("98", "99")   # bookkeeping, not claims (agg_raw drops them too)
        for k in ["ST"] + [g for g in [r["countyCode"] or ""] if g[:2] == FIPS[st]]:
            if len(k) not in (2, 5): continue
            a = acc[k]
            if err:   # only the claims page's "left out" count sees them (build_site subtracts ERR_CODES from "recent")
                if str(r["yearOfLoss"] or "")[:4] >= RECENT_FROM: a["recent"][0] += 1; a["recent"][2][r["nonPaymentReasonBuilding"]] += 1
                continue
            a["n"] += 1
            if r["yearOfLoss"]:   # hater r6/r7: is a low paid share one era or every era?
                dc = a["dec"][str(r["yearOfLoss"])[:3] + "0s"]; dc[0] += 1; dc[1] += paid > 0
            if LOSS_FROM <= str(r["yearOfLoss"] or "")[:4] <= LOSS_TO:   # 11-09: counties too (zone_split: claims outside zones A and V)
                zc = a["zone"][(r["ratedFloodZone"] or "").strip().upper() or "blank"]; zc[0] += 1
                if paid > 0: zc[1] += 1; zc[2] += paid
            if str(r["yearOfLoss"] or "")[:4] >= RECENT_FROM:
                rc = a["recent"]; rc[0] += 1
                if paid > 0: rc[1] += 1
                else: rc[2][r["nonPaymentReasonBuilding"] if r["nonPaymentReasonBuilding"] in NONPAY_REASON else "none"] += 1
            if paid <= 0:
                a["unpaid"] += 1
                if r["nonPaymentReasonBuilding"] in NONPAY_REASON: a["reason"][r["nonPaymentReasonBuilding"]] += 1
                ev = (r["floodEvent"] or "").strip()
                if ev: a["event"][ev][3] += 1   # backlog r8-r10: paid share by named flood needs the unpaid claims too
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
                              "filed": v[0] + v[3], "paid_pct": round(100 * v[0] / (v[0] + v[3]), 1),   # every claim filed under this name, and the share that paid
                              "years": sorted(y for y in v[2] if y)}   # years of loss on its paid claims
                             for e, v in sorted(((e, v) for e, v in a["event"].items() if v[0] > 0), key=lambda kv: -kv[1][1])[:8]],
                  "icc_claims": a["icc_n"], "icc_avg": round(statistics.mean(a["icc"])) if a["icc"] else None,
                  "damage_median": med(a["dmg"]), "paid_building_median": med(a["paid_b"]),
                  "damage_over_coverage_pct": pct(a["over_cov"], a["dmg_n"]), "damage_n": a["dmg_n"],
                  "avg_paid_elevated": round(statistics.mean(a["elev_paid"])) if len(a["elev_paid"]) >= 30 else None,
                  "avg_paid_not_elevated": round(statistics.mean(a["low_paid"])) if len(a["low_paid"]) >= 30 else None,
                  "elevated_paid_n": len(a["elev_paid"]), "paid_n": paid_n,
                  "by_decade": {d: {"n": v[0], "paid_pct": pct(v[1], v[0])} for d, v in sorted(a["dec"].items())}}
        rc = a["recent"]   # FEMA's data has no open/closed field: a zero-payment claim is "no recorded payment", never "denied"
        out[k]["recent"] = {"from": RECENT_FROM, "n": rc[0], "paid_n": rc[1], "unpaid_reasons": dict(rc[2])}
        if k == "ST": out[k]["by_zone"] = {z: {"n": v[0], "paid_n": v[1], "paid": round(v[2])} for z, v in a["zone"].items()}; out[k]["_pb"] = a["paid_b"]
        else:   # same split as the zone pages: a zone on the claim, first letter not A or V = outside the high-risk zones
            kz = [(z, v) for z, v in a["zone"].items() if z != "blank"]; oz = [v for z, v in kz if z[0] not in "AV"]
            out[k]["zone_split"] = {"from": LOSS_FROM, "to": LOSS_TO, "known_n": sum(v[0] for _, v in kz), "known_paid_n": sum(v[1] for _, v in kz),
                                    "known_paid": round(sum(v[2] for _, v in kz)), "out_n": sum(v[0] for v in oz), "out_paid_n": sum(v[1] for v in oz),
                                    "out_paid": round(sum(v[2] for v in oz)), "blank_n": (a["zone"].get("blank") or [0])[0]}
            zs = out[k]["zone_split"]; zs["out_pct"] = pct(zs["out_n"], zs["known_n"]); zs["out_paid_pct"] = pct(zs["out_paid"], zs["known_paid"])
    return out

NAT_PB = {}
def write_claim_size():   # top-3 compare 11-09: the U.S. median paid building claim (same base as each state's paid_building_median)
    if set(NAT_PB) != set(NAMES): return print("claim_size: not every state ran, file left as it was")
    xs = [x for v in NAT_PB.values() for x in v]
    if len(xs) < MX.CONST["min_priced"]: return
    json.dump({"n": len(xs), "p50": med(xs), "asof": _asof()},
              open(os.path.join(ROOT, "data", "us", "claim_size.json"), "w"))

def run(st):
    if not all(os.path.exists(os.path.join(RAW, ds, st + ".done")) for ds in ("NfipPolicies", "NfipClaims")):
        print(st, "skipped: pull not finished"); return
    p, c = policies(st), claims(st)
    d = os.path.join(ROOT, "data", "states", slug(st)); os.makedirs(d, exist_ok=True)
    os.makedirs(os.path.join(ROOT, "data", "us"), exist_ok=True)
    for key in ("cost_hist", "cost_hist_new", "cost_hist_zone", "cost_hist_zone_exact", "frp_hist_zone_exact", "renter_hist"):   # all single-family policies / those first bought in the past year / by zone group
        hp = os.path.join(ROOT, "data", "us", key + ".json")
        allh = json.load(open(hp)) if os.path.exists(hp) else {}
        allh[st] = p["ST"].pop(key); json.dump(allh, open(hp, "w"))
    hp = os.path.join(ROOT, "data", "us", "claims_zone.json")   # national claims by zone: summed over all 51 on the zone pages
    allh = json.load(open(hp)) if os.path.exists(hp) else {}
    allh[st] = {"from": LOSS_FROM, "to": LOSS_TO, "by_zone": c.get("ST", {}).pop("by_zone", {})}; json.dump(allh, open(hp, "w"))
    NAT_PB[st] = c.get("ST", {}).pop("_pb", [])   # national claim size: only written when every state ran in this process
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
    write_claim_size()
