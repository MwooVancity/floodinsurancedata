"""Cloudflare API token expiry (owner 2026-10-29: the site runs with no one watching). Prints RENEW when the token
expires within 30 days, so the job opens an alert issue weeks before deploys stop. Never fails the job: an expired
token already fails the deploy step itself. Usage: python -I tools/token_check.py (CLOUDFLARE_API_TOKEN, _ACCOUNT_ID)."""
import datetime, json, os, urllib.request

def days_left(expires_on, today):   # Cloudflare gives "2027-01-01T00:00:00Z" or nothing (no expiry)
    if not expires_on: return None
    return (datetime.date.fromisoformat(expires_on[:10]) - today).days

def verify(tok, acct):   # a user token answers on /user, an account token on /accounts/<id>
    for path in ("/user/tokens/verify", f"/accounts/{acct}/tokens/verify"):
        try:
            r = urllib.request.urlopen(urllib.request.Request("https://api.cloudflare.com/client/v4" + path,
                                       headers={"Authorization": "Bearer " + tok}), timeout=30)
            d = json.load(r)
            if d.get("success"): return d.get("result") or {}
        except Exception: pass
    return None

if __name__ == "__main__":
    assert days_left(None, datetime.date(2026, 1, 1)) is None
    assert days_left("2026-01-31T00:00:00Z", datetime.date(2026, 1, 1)) == 30
    res = verify(os.environ.get("CLOUDFLARE_API_TOKEN", ""), os.environ.get("CLOUDFLARE_ACCOUNT_ID", ""))
    if res is None: print("token: could not verify (the deploy step will show whether it works)")
    else:
        n = days_left(res.get("expires_on"), datetime.date.today())
        print("token:", res.get("status"), "| no expiry" if n is None else f"| expires in {n} days")
        if n is not None and n <= 30: print(f"RENEW: the Cloudflare API token expires in {n} days")
