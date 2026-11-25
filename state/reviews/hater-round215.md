## home
- (1) Visible text (scripts, styles and comments removed, tags stripped, whitespace collapsed) is identical to the git HEAD build; no difference. The home file is byte-identical to HEAD.
- (2) No adslot, no iframe, no "Advertisement" on the page. Correct.
- (3) No new wrong or misleading statement from the change; earlier MINOR and GAP notes from round 213 and 214 carry over unchanged.
Verdict: PASS

## louisiana
- (1) Visible text (scripts, styles and comments removed, tags stripped, whitespace collapsed) is identical to the git HEAD build; no difference. Raw HTML differs from HEAD (ad markup and stamp), visible text does not.
- (2) Exactly one aside.adslot, after the opening answer; one iframe src="/ad-frame.html", sandbox="allow-scripts allow-popups allow-popups-to-escape-sandbox" (no allow-top-navigation, no allow-same-origin); title and label "Advertisement" present. MINOR: markup checked, not a browser render of the ad.
- (3) No new wrong or misleading statement from the change; earlier MINOR and GAP notes from round 213 and 214 carry over unchanged.
Verdict: PASS

## palm-beach-county-fl
- (1) Visible text (scripts, styles and comments removed, tags stripped, whitespace collapsed) is identical to the git HEAD build; no difference. Raw HTML differs from HEAD (ad markup and stamp), visible text does not.
- (2) Exactly one aside.adslot, after the opening answer; one iframe src="/ad-frame.html", sandbox="allow-scripts allow-popups allow-popups-to-escape-sandbox" (no allow-top-navigation, no allow-same-origin); title and label "Advertisement" present. MINOR: markup checked, not a browser render of the ad.
- (3) No new wrong or misleading statement from the change; earlier MINOR and GAP notes from round 213 and 214 carry over unchanged.
Verdict: PASS

## new-york-county-ny
- (1) Visible text (scripts, styles and comments removed, tags stripped, whitespace collapsed) is identical to the git HEAD build; no difference. Raw HTML differs from HEAD (ad markup and stamp), visible text does not.
- (2) Exactly one aside.adslot, after the opening answer; one iframe src="/ad-frame.html", sandbox="allow-scripts allow-popups allow-popups-to-escape-sandbox" (no allow-top-navigation, no allow-same-origin); title and label "Advertisement" present. MINOR: markup checked, not a browser render of the ad.
- (3) No new wrong or misleading statement from the change; earlier MINOR and GAP notes from round 213 and 214 carry over unchanged.
Verdict: PASS

## dixie-county-fl
- (1) Visible text (scripts, styles and comments removed, tags stripped, whitespace collapsed) is identical to the git HEAD build; no difference. Raw HTML differs from HEAD (ad markup and stamp), visible text does not.
- (2) Exactly one aside.adslot, after the opening answer; one iframe src="/ad-frame.html", sandbox="allow-scripts allow-popups allow-popups-to-escape-sandbox" (no allow-top-navigation, no allow-same-origin); title and label "Advertisement" present. MINOR: markup checked, not a browser render of the ad.
- (3) No new wrong or misleading statement from the change; earlier MINOR and GAP notes from round 213 and 214 carry over unchanged.
Verdict: PASS

## levy-county-fl
- (1) Visible text (scripts, styles and comments removed, tags stripped, whitespace collapsed) is identical to the git HEAD build; no difference. Raw HTML differs from HEAD (ad markup and stamp), visible text does not.
- (2) Exactly one aside.adslot, after the opening answer; one iframe src="/ad-frame.html", sandbox="allow-scripts allow-popups allow-popups-to-escape-sandbox" (no allow-top-navigation, no allow-same-origin); title and label "Advertisement" present. MINOR: markup checked, not a browser render of the ad.
- (3) No new wrong or misleading statement from the change; earlier MINOR and GAP notes from round 213 and 214 carry over unchanged.
Verdict: PASS

## sonoma-county-ca
- (1) Visible text (scripts, styles and comments removed, tags stripped, whitespace collapsed) is identical to the git HEAD build; no difference. Raw HTML differs from HEAD (ad markup and stamp), visible text does not.
- (2) Exactly one aside.adslot, after the opening answer; one iframe src="/ad-frame.html", sandbox="allow-scripts allow-popups allow-popups-to-escape-sandbox" (no allow-top-navigation, no allow-same-origin); title and label "Advertisement" present. MINOR: markup checked, not a browser render of the ad.
- (3) No new wrong or misleading statement from the change; earlier MINOR and GAP notes from round 213 and 214 carry over unchanged.
Verdict: PASS

## wakulla-county-fl
- (1) Visible text (scripts, styles and comments removed, tags stripped, whitespace collapsed) is identical to the git HEAD build; no difference. Raw HTML differs from HEAD (ad markup and stamp), visible text does not.
- (2) Exactly one aside.adslot, after the opening answer; one iframe src="/ad-frame.html", sandbox="allow-scripts allow-popups allow-popups-to-escape-sandbox" (no allow-top-navigation, no allow-same-origin); title and label "Advertisement" present. MINOR: markup checked, not a browser render of the ad.
- (3) No new wrong or misleading statement from the change; earlier MINOR and GAP notes from round 213 and 214 carry over unchanged.
Verdict: PASS

## headers and frame
- dist/_headers: site-wide `/*` rule keeps X-Frame-Options: DENY; the only added rule is `/ad-frame.html` with `! X-Frame-Options` then `X-Frame-Options: SAMEORIGIN`. The git diff against HEAD shows only those 3 added lines, so every other path (including the pages themselves) is still DENY. SAMEORIGIN lets only our own origin frame the ad page.
- dist/ad-frame.html: noindex meta present; body holds only the atOptions script and one Adsterra script (bauval.org); nothing else.
- Doubt on syntax (MINOR, unverified): `! Header` detaching is real Cloudflare Pages syntax, but I did not test it live. Without the detach, Cloudflare joins matching rules' values ("DENY, SAMEORIGIN"), which browsers treat as invalid and so block the frame. Detach-then-set in one block is the documented pattern, yet the only proof is a live `curl -I /ad-frame.html` showing a single SAMEORIGIN value and a page still showing DENY; read that after deploy.
Verdict: PASS
