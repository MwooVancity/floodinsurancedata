## home
- (1) Visible text (scripts, styles, comments removed, whitespace collapsed) is identical to the git HEAD build; no difference.
- (2) No adslot, no iframe, no "Advertisement" on the page. Correct.
- (3) No new wrong or misleading statement from the change; earlier MINOR and GAP notes from rounds 213 to 215 carry over unchanged.
Verdict: PASS

## louisiana
- (1) Visible text (scripts, styles, comments removed, whitespace collapsed) is identical to the git HEAD build; no difference.
- (2) Exactly one aside.adslot and one iframe, src="/ad-frame" (no .html), sandbox="allow-scripts allow-popups allow-popups-to-escape-sandbox" (no allow-top-navigation, no allow-same-origin); title and label "Advertisement" present. MINOR: markup checked, not a browser render; position after the opening answer carried from round 215, not re-measured.
- (3) No new wrong or misleading statement from the change; earlier MINOR and GAP notes from rounds 213 to 215 carry over unchanged.
Verdict: PASS

## palm-beach-county-fl
- (1) Visible text (scripts, styles, comments removed, whitespace collapsed) is identical to the git HEAD build; no difference.
- (2) Exactly one aside.adslot and one iframe, src="/ad-frame" (no .html), sandbox="allow-scripts allow-popups allow-popups-to-escape-sandbox" (no allow-top-navigation, no allow-same-origin); title and label "Advertisement" present. MINOR: markup checked, not a browser render; position after the opening answer carried from round 215, not re-measured.
- (3) No new wrong or misleading statement from the change; earlier MINOR and GAP notes from rounds 213 to 215 carry over unchanged.
Verdict: PASS

## new-york-county-ny
- (1) Visible text (scripts, styles, comments removed, whitespace collapsed) is identical to the git HEAD build; no difference.
- (2) Exactly one aside.adslot and one iframe, src="/ad-frame" (no .html), sandbox="allow-scripts allow-popups allow-popups-to-escape-sandbox" (no allow-top-navigation, no allow-same-origin); title and label "Advertisement" present. MINOR: markup checked, not a browser render; position after the opening answer carried from round 215, not re-measured.
- (3) No new wrong or misleading statement from the change; earlier MINOR and GAP notes from rounds 213 to 215 carry over unchanged.
Verdict: PASS

## dixie-county-fl
- (1) Visible text (scripts, styles, comments removed, whitespace collapsed) is identical to the git HEAD build; no difference.
- (2) Exactly one aside.adslot and one iframe, src="/ad-frame" (no .html), sandbox="allow-scripts allow-popups allow-popups-to-escape-sandbox" (no allow-top-navigation, no allow-same-origin); title and label "Advertisement" present. MINOR: markup checked, not a browser render; position after the opening answer carried from round 215, not re-measured.
- (3) No new wrong or misleading statement from the change; earlier MINOR and GAP notes from rounds 213 to 215 carry over unchanged.
Verdict: PASS

## levy-county-fl
- (1) Visible text (scripts, styles, comments removed, whitespace collapsed) is identical to the git HEAD build; no difference.
- (2) Exactly one aside.adslot and one iframe, src="/ad-frame" (no .html), sandbox="allow-scripts allow-popups allow-popups-to-escape-sandbox" (no allow-top-navigation, no allow-same-origin); title and label "Advertisement" present. MINOR: markup checked, not a browser render; position after the opening answer carried from round 215, not re-measured.
- (3) No new wrong or misleading statement from the change; earlier MINOR and GAP notes from rounds 213 to 215 carry over unchanged.
Verdict: PASS

## sonoma-county-ca
- (1) Visible text (scripts, styles, comments removed, whitespace collapsed) is identical to the git HEAD build; no difference.
- (2) Exactly one aside.adslot and one iframe, src="/ad-frame" (no .html), sandbox="allow-scripts allow-popups allow-popups-to-escape-sandbox" (no allow-top-navigation, no allow-same-origin); title and label "Advertisement" present. MINOR: markup checked, not a browser render; position after the opening answer carried from round 215, not re-measured.
- (3) No new wrong or misleading statement from the change; earlier MINOR and GAP notes from rounds 213 to 215 carry over unchanged.
Verdict: PASS

## wakulla-county-fl
- (1) Visible text (scripts, styles, comments removed, whitespace collapsed) is identical to the git HEAD build; no difference.
- (2) Exactly one aside.adslot and one iframe, src="/ad-frame" (no .html), sandbox="allow-scripts allow-popups allow-popups-to-escape-sandbox" (no allow-top-navigation, no allow-same-origin); title and label "Advertisement" present. MINOR: markup checked, not a browser render; position after the opening answer carried from round 215, not re-measured.
- (3) No new wrong or misleading statement from the change; earlier MINOR and GAP notes from rounds 213 to 215 carry over unchanged.
Verdict: PASS

## headers and frame
- dist/_headers: `/*` keeps X-Frame-Options: DENY; git diff against HEAD adds only a `/ad-frame` block (`! X-Frame-Options` then SAMEORIGIN), next to the existing `/ad-frame.html` block. No other path is relaxed.
- dist/ad-frame.html: noindex meta; body holds only the atOptions script and one Adsterra script (bauval.org). Nothing else.
- Cloudflare Pages serves ad-frame.html at /ad-frame by its clean-URL behaviour (and 307s the .html form to it, as the owner observed). I cannot verify that offline. Also unverified offline: that `! Header` detach works so the response carries a single SAMEORIGIN value rather than "DENY, SAMEORIGIN". Only a live `curl -I https://<site>/ad-frame` (one SAMEORIGIN, 200, no redirect) plus a page still returning DENY proves it.
Verdict: PASS
