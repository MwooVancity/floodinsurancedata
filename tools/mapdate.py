"""FEMA Community Status Book map-date reader (PLAN 3e). One function, tested by test_tools.py."""
import re

def map_date(v, today=None):
    """FEMA Community Status Book currentlyEffectiveMapDate -> (kind, date or None, note). FEMA's legend (OpenFEMA
    DataSetFields): (>) map date after the report date; (M) no elevation determined, all Zone A, C and X; (L) original
    FIRM by letter; NSFHA no special flood hazard area, all Zone C; E emergency program; (S) suspended; (W) withdrawn;
    N/A. Two-digit years: 70 or more = 19yy, below = 20yy (FIRMs start in the 1970s). Unknown text raises."""
    import datetime as _d
    today = today or _d.date.today()
    s = (v or "").strip()
    if s in ("", "N/A") or s.startswith(("E", "(S)", "(W)")) or s.endswith(("(S)", "(W)")): return ("none", None, "")
    if s == "(NSFHA)": return ("nsfha", None, "FEMA's map shows no high-risk flood area here (all Zone C)")
    if s == "(All Zone D)": return ("nsfha", None, "FEMA's map shows all Zone D here (flood risk not yet studied)")   # not in the legend; 9 rows, 2026-10-29
    mm = re.fullmatch(r"(\d{2})/(\d{2})/(\d{2})(\((?:>|M|L)\))?", s)
    if not mm: raise ValueError(f"unknown FEMA map date {v!r}")
    y = int(mm[3]); d = _d.date(1900 + y if y >= 70 else 2000 + y, int(mm[1]), int(mm[2]))
    note = {"(M)": "the map sets no flood heights here (all Zone A, C and X)", "(L)": "the original map was issued by letter (all Zone A, C and X)"}.get(mm[4] or "", "")
    return ("new" if d > today else "current", d, note)
