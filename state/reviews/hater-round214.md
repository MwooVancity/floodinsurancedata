## home
- (1) Visible text: identical to HEAD (round 213 build); template hash changed 3f68f296d4448640 to d2090978a5a164ec, which is expected from the ad markup. Only the git copy was compared, since round213 text snapshots are hashes only.
- (2) No adslot, no iframe, no "Advertisement" on the page. Correct.
- (3) Checked as a skeptical homeowner: no new statement. MINOR carried over: "Lowest:" list is in table order, not lowest-first.
Verdict: PASS

## louisiana
- (1) Visible text (scripts and styles removed, tags stripped) identical to round 213 build; no difference.
- (2) Exactly one aside.adslot, before the first section heading and after the opening answer; iframe src="/ad-frame.html", sandbox="allow-scripts allow-popups allow-popups-to-escape-sandbox" (no allow-top-navigation, no allow-same-origin); title and label "Advertisement" present. MINOR: markup checked, not a browser render of the ad.
- (3) No new wrong or misleading statement from the change; earlier MINOR and GAP notes from round 213 carry over unchanged.
Verdict: PASS

## palm-beach-county-fl
- (1) Visible text (scripts and styles removed, tags stripped) identical to round 213 build; no difference.
- (2) Exactly one aside.adslot, before the first section heading and after the opening answer; iframe src="/ad-frame.html", sandbox="allow-scripts allow-popups allow-popups-to-escape-sandbox" (no allow-top-navigation, no allow-same-origin); title and label "Advertisement" present. MINOR: markup checked, not a browser render of the ad.
- (3) No new wrong or misleading statement from the change; earlier MINOR and GAP notes from round 213 carry over unchanged.
Verdict: PASS

## new-york-county-ny
- (1) Visible text (scripts and styles removed, tags stripped) identical to round 213 build; no difference.
- (2) Exactly one aside.adslot, before the first section heading and after the opening answer; iframe src="/ad-frame.html", sandbox="allow-scripts allow-popups allow-popups-to-escape-sandbox" (no allow-top-navigation, no allow-same-origin); title and label "Advertisement" present. MINOR: markup checked, not a browser render of the ad.
- (3) No new wrong or misleading statement from the change; earlier MINOR and GAP notes from round 213 carry over unchanged.
Verdict: PASS

## dixie-county-fl
- (1) Visible text (scripts and styles removed, tags stripped) identical to round 213 build; no difference.
- (2) Exactly one aside.adslot, before the first section heading and after the opening answer; iframe src="/ad-frame.html", sandbox="allow-scripts allow-popups allow-popups-to-escape-sandbox" (no allow-top-navigation, no allow-same-origin); title and label "Advertisement" present. MINOR: markup checked, not a browser render of the ad.
- (3) No new wrong or misleading statement from the change; earlier MINOR and GAP notes from round 213 carry over unchanged.
Verdict: PASS

## levy-county-fl
- (1) Visible text (scripts and styles removed, tags stripped) identical to round 213 build; no difference.
- (2) Exactly one aside.adslot, before the first section heading and after the opening answer; iframe src="/ad-frame.html", sandbox="allow-scripts allow-popups allow-popups-to-escape-sandbox" (no allow-top-navigation, no allow-same-origin); title and label "Advertisement" present. MINOR: markup checked, not a browser render of the ad.
- (3) No new wrong or misleading statement from the change; earlier MINOR and GAP notes from round 213 carry over unchanged.
Verdict: PASS

## sonoma-county-ca
- (1) Visible text (scripts and styles removed, tags stripped) identical to round 213 build; no difference.
- (2) Exactly one aside.adslot, before the first section heading and after the opening answer; iframe src="/ad-frame.html", sandbox="allow-scripts allow-popups allow-popups-to-escape-sandbox" (no allow-top-navigation, no allow-same-origin); title and label "Advertisement" present. MINOR: markup checked, not a browser render of the ad.
- (3) No new wrong or misleading statement from the change; earlier MINOR and GAP notes from round 213 carry over unchanged.
Verdict: PASS

## wakulla-county-fl
- (1) Visible text (scripts and styles removed, tags stripped) identical to round 213 build; no difference.
- (2) Exactly one aside.adslot, before the first section heading and after the opening answer; iframe src="/ad-frame.html", sandbox="allow-scripts allow-popups allow-popups-to-escape-sandbox" (no allow-top-navigation, no allow-same-origin); title and label "Advertisement" present. MINOR: markup checked, not a browser render of the ad.
- (3) No new wrong or misleading statement from the change; earlier MINOR and GAP notes from round 213 carry over unchanged.
Verdict: PASS

## ad-frame and privacy
- dist/ad-frame.html: noindex meta present; body holds only the atOptions script and one Adsterra script (bauval.org); nothing else. MINOR: not in sitemap or robots.txt, which is fine given noindex.
- Privacy page names Adsterra, bauval.org, sandboxed frame, new-tab click-through, cookies and device details, and the pages where it is not shown. It matches what the frame does. MINOR: "cannot send you to another site on its own" is true for top navigation but a popup the script opens after a click is allowed by allow-popups-to-escape-sandbox; the page does say clicks open a new tab.
Verdict: PASS
