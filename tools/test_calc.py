"""Fixture tests that exercise the PRODUCTION calculations in ffcalc.py (not a re-implementation),
with known answers: duplicate exclusion, refunds, nulls, multi-unit condo rows, non-SFH, percentiles,
full-risk gap, claims aggregation, and the cost-sample suppression rule. Run: python -I tools/test_calc.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I drops script dir
import ffcalc

PR = ffcalc.PREM   # premium-only field; policyCost = premium + fees
POL = [
    {"id": 1, "policyCost": 1000, PR: 900,  "fullRiskPremium": 3000, "ratedFloodZone": "AE", "occupancyType": 1,  "primaryResidenceIndicator": True,  "policyCount": 1},
    # id2: cost WITH fees (2000) is above full-risk 1500, but the PREMIUM (1400) is below it — the like-for-like
    # comparison must count it as below (the 2026-10-25 bug compared cost-with-fees and missed it).
    {"id": 2, "policyCost": 2000, PR: 1400, "fullRiskPremium": 1500, "ratedFloodZone": "AE", "occupancyType": 11, "primaryResidenceIndicator": True,  "policyCount": 1},
    {"id": 3, "policyCost": 3000, PR: 2900, "fullRiskPremium": 5000, "ratedFloodZone": "X",  "occupancyType": 1,  "primaryResidenceIndicator": True,  "policyCount": 1},
    {"id": 4, "policyCost": -50,  PR: -50,  "fullRiskPremium": 2000, "ratedFloodZone": "AE", "occupancyType": 1,  "primaryResidenceIndicator": True,  "policyCount": 1},  # refund excluded
    {"id": 5, "policyCost": None, PR: None, "fullRiskPremium": 2000, "ratedFloodZone": "AE", "occupancyType": 1,  "primaryResidenceIndicator": True,  "policyCount": 1},  # null cost excluded
    {"id": 6, "policyCost": 9999, PR: 9000, "fullRiskPremium": 9999, "ratedFloodZone": "VE", "occupancyType": 2,  "primaryResidenceIndicator": True,  "policyCount": 4},  # non-SFH condo, 4 units
]
P = ffcalc.aggregate_policies(POL)
assert P["units"] == 9, P["units"]                                  # 1*5 + 4
assert P["cohort_n"] == 5, P["cohort_n"]                            # ids 1-5 (SFH primary); id6 non-SFH
assert P["cost_n"] == 3, P["cost_n"]                                # ids 1,2,3 (−50 and null dropped)
assert P["cost_excluded"] == 2, P["cost_excluded"]
assert P["p50"] == 2000, P["p50"]
assert P["zone_units"] == {"AE": 4, "VE": 4, "X": 1}, P["zone_units"]   # zone mix counts all policies, not just valid-cost ones
assert P["zone_units_all"] == P["zone_units"], P["zone_units_all"]   # uncapped copy (zone pages); differs only past 12 zones
assert P["sfha_units"] == 8 and P["sfha_share_units"] == round(100 * 8 / 9, 1), (P["sfha_units"], P["sfha_share_units"])
assert P["share_below"] == 100.0 and P["below_n"] == 3, (P["share_below"], P["below_n"])  # ids 1,2,3 below on premium basis
assert P["gap_basis"] == "premium" and P["prem_median"] == 1400 and P["frp_median"] == 3000, P
assert round(1 - 0.99 ** 30, 2) == 0.26                             # rule odds_30
_mb = ffcalc._median_by([{"z": "AE", "v": 100}] * 50 + [{"z": "X", "v": 100}] * 49 + [{"z": "", "v": 100}] * 60 + [{"z": "AE", "v": -5}], "z", "v")
assert _mb == {"AE": {"median": 100, "n": 50}}, _mb                  # small groups, blanks and refunds stay out
assert ffcalc.premium_gap([{ffcalc.PREM: 100, "fullRiskPremium": 400}, {ffcalc.PREM: 500, "fullRiskPremium": 400}])["below_gap_median"] == 300   # only policies below full risk count
assert P["spread_ok"] is False, P["spread_ok"]                      # only 3 valid costs < 100 -> suppress
# hcu 11-07: a condo-unit policy coded single-family (legacy code 1) stays out of every single-family figure
_cu = dict(POL[0], id=7, policyCost=99999, condominiumCoverageTypeCode="U")
_PC = ffcalc.aggregate_policies([dict(r, condominiumCoverageTypeCode="N") for r in POL] + [_cu])
assert _PC["cohort_n"] == 5 and _PC["p50"] == 2000 and _PC["sf_no_condo"] is True, (_PC["cohort_n"], _PC["p50"])
assert ffcalc.is_sf_home(dict(POL[0], condominiumCoverageTypeCode=" n ")) and not ffcalc.is_sf_home(dict(POL[0], condominiumCoverageTypeCode="L"))

CLM = [
    {"yearOfLoss": 2017, "netBuildingPaymentAmount": 100, "netContentsPaymentAmount": 50},
    {"yearOfLoss": 2017, "netBuildingPaymentAmount": 200, "netContentsPaymentAmount": 0},
    {"yearOfLoss": 1999, "netBuildingPaymentAmount": 10,  "netContentsPaymentAmount": 5},
]
C = ffcalc.aggregate_claims(CLM, P["units"])
assert C["total_paid"] == 365, C["total_paid"]
assert C["by_year"]["2017"] == [2, 350], C["by_year"]["2017"]
assert C["year_min"] == 1999 and C["year_max"] == 2017
assert C["cumulative_per_100_current_units"] == round(100 * 3 / 9, 1)

# small fixture: per-zone/per-year medians need enough obs, so they stay empty here
assert P["cost_by_zone"] == {}, P["cost_by_zone"]
assert P["cost_by_year"] == {}, P["cost_by_year"]
assert P["coverage_building"] == 0 and P["coverage_contents"] == 0

# spread_ok + cost_by_zone populate once enough valid costs exist
big = [{"id": i, "policyCost": 1000 + i, "fullRiskPremium": 2000, "ratedFloodZone": "AE",
        "occupancyType": 1, "primaryResidenceIndicator": True, "policyCount": 1,
        "policyEffectiveDate": "2026-03-01", "totalBuildingInsuranceCoverage": 250000} for i in range(120)]
B = ffcalc.aggregate_policies(big)
assert B["spread_ok"] is True
assert B["cost_by_zone"]["AE"]["n"] == 120, B["cost_by_zone"]
assert B["cost_by_year"]["2026"]["n"] == 120, B["cost_by_year"]
assert B["coverage_building"] == 120 * 250000

# percentile convention edge cases (inclusive method), per review request
assert ffcalc.pctl([], 50) is None                       # empty
assert ffcalc.pctl([1200], 50) == 1200                   # single observation -> the value
assert ffcalc.pctl([1200], 25) == 1200
assert ffcalc.pctl([10, 20, 30, 40], 50) == 25           # even-sized -> interpolated midpoint
assert ffcalc.pctl([5, 5, 5, 5], 50) == 5                # repeated values
assert ffcalc.pctl([5, 5, 5, 5], 90) == 5
assert ffcalc.pctl([1, 2, 3, 4, 5], 50) == 3             # odd-sized -> middle

# years-to-full-risk glide path (the production formula build_page prints), incl. the yrs==1 edge
assert ffcalc.years_to_full_risk(1658, 3461) == 5        # Lee FL: matches the shipped page
assert ffcalc.years_to_full_risk(1000, 1100) == 1        # a tiny gap still rounds up to 1 renewal (yrs==1)
assert ffcalc.years_to_full_risk(2000, 1500) is None     # already above full-risk -> no glide
assert ffcalc.years_to_full_risk(1000, 1000) is None     # no gap
assert ffcalc.years_to_full_risk(0, 3000) is None        # no current median
assert ffcalc.years_to_full_risk(1000, None) is None     # no full-risk figure

# zone (ZONE_MIN=50) and per-ZIP (ZIP_MIN=25) publish thresholds
mix = ([{"id": f"a{i}", "policyCost": 1000 + i, "ratedFloodZone": "AE", "occupancyType": 1,
         "primaryResidenceIndicator": True, "policyCount": 1, "reportedZipCode": "33333"} for i in range(60)]
     + [{"id": f"x{i}", "policyCost": 2000 + i, "ratedFloodZone": "X", "occupancyType": 1,
         "primaryResidenceIndicator": True, "policyCount": 1, "reportedZipCode": "44444"} for i in range(40)]
     + [{"id": f"z{i}", "policyCost": 3000 + i, "ratedFloodZone": "AE", "occupancyType": 1,
         "primaryResidenceIndicator": True, "policyCount": 1, "reportedZipCode": "55555"} for i in range(10)])
M = ffcalc.aggregate_policies(mix)
assert M["cost_by_zone"]["AE"]["n"] == 70, M["cost_by_zone"]       # 60 + 10 AE, >= ZONE_MIN -> shown
assert "X" not in M["cost_by_zone"], M["cost_by_zone"]             # 40 < ZONE_MIN -> omitted
bzp = {d["zip"]: d for d in M["by_zip"]}
assert bzp["33333"]["cost_n"] == 60 and bzp["33333"]["median"] is not None
assert bzp["44444"]["cost_n"] == 40 and bzp["44444"]["median"] is not None
assert bzp["55555"]["cost_n"] == 10 and bzp["55555"]["median"] is None and bzp["55555"]["units"] == 10  # < ZIP_MIN

# ---- integration: build a real county page, smoke-check the render, and prove the gate catches a bad page.
# Exercises the shipping build_page.py + gate.py, not a re-implementation. Skips if the county data is absent.
import subprocess, tempfile, json as _json
TOOLS = os.path.dirname(os.path.abspath(__file__))
_lee = os.path.join(os.path.dirname(TOOLS), "data", "c", "lee-county-fl")   # the current pipeline (data/c), not the stale pre-2026-10-27 copy
_agg = os.path.join(_lee, "agg.json")
if os.path.exists(_agg) and os.path.exists(os.path.join(_lee, "data.json")):
    tmp = tempfile.mkdtemp()
    out = os.path.join(tmp, "index.html")
    env = dict(os.environ, FF_DIR=_lee, OUT_HTML=out, FF_COUNTYLABEL="Lee County, Florida",
               FF_COUNTYSHORT="Lee County", FF_OFFICIAL="132012", FF_SLUG="lee-county-fl",
               FF_GEOID="12071", FF_BASEURL="https://floodinsurancedata.com",
               FF_PLACES=os.path.join(tmp, "places.json"))
    rb = subprocess.run([sys.executable, "-I", os.path.join(TOOLS, "build_page.py")],
                        env=env, cwd=TOOLS, capture_output=True, text=True)
    assert rb.returncode == 0, "build_page failed: " + rb.stderr[-500:]
    page = open(out, encoding="utf-8").read()
    import re as _re2
    assert not _re2.search(r">\s*(None|nan|NaN|undefined)\s*<", page), "null leaked into page text"
    assert "$None" not in page and "None%" not in page and "$nan" not in page, "null leaked into a number"
    assert ">{}<" not in page and "{money(" not in page and "{P[" not in page, "raw template token leaked"

    def _gate(html_path):
        return subprocess.run([sys.executable, "-I", os.path.join(TOOLS, "gate.py"), _agg, html_path, "132012"],
                              capture_output=True, text=True).returncode
    assert _gate(out) == 0, "gate should PASS a good page"
    med = "$" + format(int(round(_json.load(open(_agg))["policies"]["p50"])), ",")
    bad = os.path.join(tmp, "bad.html")
    open(bad, "w", encoding="utf-8").write(page.replace(med, "$1"))   # strip the median the gate requires
    assert _gate(bad) == 1, "gate should FAIL when the required median is missing from the page"
    print("integration: build+smoke ok; gate PASS on good page, FAIL on median-stripped page")
else:
    print("integration: skipped (data/lee-county-fl not present)")

# a build must find nothing to write once refresh has assembled a state (dirty tracked files stopped the daily push)
import agg_raw as _AR, tempfile as _tf
_d = _tf.mkdtemp()
_json.dump({"claims_extra": {"x": 1}}, open(os.path.join(_d, "agg.json"), "w"))
_json.dump({"nri_counties": [{"fips": "1", "county": "A", "rating": "High", "extra": 2}]}, open(os.path.join(_d, "data.json"), "w"))
_AR.assemble(_d)
_a, _b = _json.load(open(os.path.join(_d, "agg.json"))), _json.load(open(os.path.join(_d, "data.json")))
assert _a["state_risk"] == [{"fips": "1", "county": "A", "rating": "High"}] and _a["nri"] is None and _b["claims_extra"] == {"x": 1}
os.utime(os.path.join(_d, "agg.json"), (1, 1)); _AR.assemble(_d)
assert os.path.getmtime(os.path.join(_d, "agg.json")) == 1, "assemble rewrote a finished state"

# outside share: dollars not counts, building+contents+ICC, a blank zone leaves both sides, unpaid claims ignored
_c = lambda z, b, c=0, i=0: {"ratedFloodZone": z, "netBuildingPaymentAmount": b, "netContentsPaymentAmount": c, "netIccPaymentAmount": i}
_x = _AR.claims_extra([_c("AE", 600), _c("X", 100, 200, 100), _c("VE", 0), _c("", 5000), _c(None, 900), _c("X", 0)])
assert _x["outside_sfha_pct"] == 40.0 and _x["paid_n"] == 4, _x
assert _AR.claims_extra([_c("", 5)])["outside_sfha_pct"] is None

# zone pages: the national zone histograms must be the same policies as the state zone tables (states drop thin zones only)
_zh = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "us", "cost_hist_zone.json")
if os.path.exists(_zh):
    import glob as _g
    def _zone_counts_agree(hist_n, state_n): return state_n <= hist_n and hist_n - state_n <= 0.02 * hist_n
    assert not _zone_counts_agree(1000, 900) and not _zone_counts_agree(900, 1000) and _zone_counts_agree(1000, 990)
    _hz, _sts = _json.load(open(_zh)), [_json.load(open(f))["policies"] for f in _g.glob(os.path.join(os.path.dirname(_zh), "..", "states", "*", "agg.json"))]
    for _gr, _m in (("A", "A"), ("V", "V"), ("X", "XBC")):
        _a = sum(sum(v.get(_gr, {}).values()) for v in _hz.values())
        _b = sum(d["n"] for s in _sts for z, d in (s.get("cost_by_zone") or {}).items() if z[:1] in _m)
        assert _zone_counts_agree(_a, _b), (_gr, _a, _b)

print("test_calc: all assertions passed (exercising ffcalc production functions)")


# S16 internal links (11-08): a county page missing a hub link fails; the same page with it passes
import linkcheck
_pg = {"/nfip/": "", "/flood-insurance/harris-county-tx/": "<a href='/nfip/'>n</a> <a href='/flood-zones/ae/'>AE</a>"}
assert linkcheck.fails(_pg, set(_pg)) == [], linkcheck.fails(_pg, set(_pg))
_pg["/flood-insurance/harris-county-tx/"] = "<a href='/flood-zones/ae/'>AE</a>"
assert linkcheck.fails(_pg, set(_pg)) == ["/flood-insurance/harris-county-tx/: no link to /nfip/"]
_pg["/flood-insurance/harris-county-tx/"] = "<a href='../../nfip/'>n</a>"
assert linkcheck.fails(_pg, set(_pg)) == ["/flood-insurance/harris-county-tx/: no link to a zone page"]
print("S16 link check: 3 cases ok")

# S16 graph: a broken internal link and an orphan both fail; a linked page passes
_g = {"/": "<a href='/a/'>a</a>", "/a/": "<a href='../b/'>b</a> <a href='/'>home</a>", "/b/": ""}
assert linkcheck.graph_fails(_g, set(_g)) == [], linkcheck.graph_fails(_g, set(_g))
_g["/a/"] = "<a href='/gone/'>x</a>"
assert sorted(linkcheck.graph_fails(_g, set(_g))) == ["/a/: links /gone/, which is not a built page", "/b/: orphan (no page links to it)"], linkcheck.graph_fails(_g, set(_g))
print("S16 graph check: 2 cases ok")
