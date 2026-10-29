# Hater round 25 (light check, strict scope)

Read-only check of extracted page text. Scope limited as requested. No web search, no deploy, no commit.

## home

- MAJOR: Source line is "Source: federalreserve.gov, floodsmart.gov, flsenate.gov, govinfo.gov (official pages, checked October 25, 2026). Not endorsed by FEMA." It is in the site's standard format (matches the `Source:` line pattern on louisiana), but it names no FEMA host while the card links "FEMA's flood map" to msc.fema.gov (verified in the card bytes). The line fails its own standard: it must name the official sites behind the card's rules.
- MAJOR: "In Florida, Citizens homes with wind cover need it in a high-risk zone since 2023; outside one, since January 2026 if they cost $400,000 or more to rebuild, and from January 2027 for all others." "Citizens" is never defined (Florida's state insurer), and three cutoff dates are packed into one sentence that a shop-counter reader cannot parse. The dates were not verified in this review (no web, no statute read), so they remain unproven here.
- MINOR: "federal help to buy or build" is jargon; a reader will not know what it covers.
- MINOR: "Check your zone on FEMA's flood map ." has a stray space before the period.
- MINOR: "checked October 25, 2026" is a claim of a check made four days before today (2026-10-29). Not re-checked in this review, so the date stays unverified here.
- Checked and clean: "Most policies start 30 days after you buy, but there is no wait if you buy it with a new or refinanced mortgage." Matches the 30-day rule on floodsmart.gov as cited. The "�" I saw in console output is a display artifact; the file bytes contain the correct section sign.

Verdict: FAIL

## louisiana

- Scope check only: "Already flooded?" block contains "your signed, sworn statement of the amount you are claiming". Present. No other defects graded (out of scope).

Verdict: PASS

## palm-beach-county-fl

- Scope check only: "Already flooded?" block contains "your signed, sworn statement of the amount you are claiming". Present. No other defects graded (out of scope).

Verdict: PASS

## broward-county-fl

- Scope check only: "Already flooded?" block contains "your signed, sworn statement of the amount you are claiming". Present. No other defects graded (out of scope).

Verdict: PASS

## maine

- Scope check only: "Already flooded?" block contains "your signed, sworn statement of the amount you are claiming". Present. No other defects graded (out of scope).

Verdict: PASS
