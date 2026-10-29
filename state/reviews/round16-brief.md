
You are the harshest critic this website will ever face, and you know exactly what it takes to rank #1 on Google
for a money topic. Find every reason to refuse publishing these pages of floodinsurancedata.com, a site that shows
what NFIP flood insurance costs and pays out per US state and county, built from FEMA's full public record
downloads. You did not build it and owe it nothing. Assume it is wrong until you prove otherwise.

Pages under review: https://floodinsurancedata.com/, https://floodinsurancedata.com/flood-insurance/louisiana/, https://floodinsurancedata.com/flood-insurance/palm-beach-county-fl/, https://floodinsurancedata.com/flood-insurance/maine/, https://floodinsurancedata.com/flood-insurance/nebraska/

## The checklist comes first (owner 2026-10-28: "user, not Google")
Read the "User, not Google: the helpfulness checklist" section of C:\Users\mwoo7\Desktop\floodinsurance\PLAN.md
(lines A-N). For EVERY line, on EVERY page, say PASS or name the defect, quoting the text or naming the screenshot.
A line marked OPEN there is a known gap: tag it GAP, never MAJOR. Judge confusion for a newcomer who knows nothing
about flood insurance: any word, code, number or layout that would make them misread, hesitate or give up.

## Judge as six people at once
1. **A frightened homeowner on a phone**, just told they are in a flood zone or just flooded, with 30 seconds. What
   confuses, misleads, scares wrongly, buries the answer, or uses jargon? What would they do next, and does the page
   let them?
2. **A FEMA/NFIP analyst** (Risk Rating 2.0, policies vs policy units, premium vs total cost with fees, claims by
   year of loss, closed without payment, SFHA zones A/V, CRS, penetration rates, ICC, NRI). What is technically
   wrong, mislabeled, mis-defined, compared across different bases or eras, or true but misleading?
3. **A competitor** (ValuePenguin, floodfigures.com, FEMA FloodSmart) hunting for one screenshot to mock.
4. **A Google search quality rater** (YMYL): who is responsible, trust, thin or templated text, filler,
   repetition, unsupported claims, structured data that claims more than the page shows.
5. **A copy editor**: grammar, clipped sentences, numbers that disagree on the page, inconsistent rounding, labels
   that disagree with their values, dates that disagree.
6. **The SEO strategist who must beat today's #1 result.** For each page, search Google (WebSearch) for the query
   a real reader types (home: "flood insurance cost"; louisiana: "flood insurance cost Louisiana"; palm-beach-county-fl: "flood insurance cost palm beach county FL"; maine: "flood insurance cost Maine"; nebraska: "flood insurance cost Nebraska") and read the top 3 results' titles and what they answer. Then answer, with evidence:
   - Does our title, description and H1 match what that searcher wants, better than #1's?
   - Does our first phone screen answer the query outright, faster than #1?
   - What does #1 give the reader that we do not (a fact, a tool, a next step)? Each gap is a defect.
   - What do we give that no top result has (our information gain)? Is it on screen 1 or buried?
   - Would a searcher click back to Google? Where exactly would they bail?
   - Does anything look like scaled, templated or doorway content that Google demotes (name-swapped text,
     the same sentences on every page, thin cards)?
   - Trust and authorship signals #1 has and we lack.
   Each gap vs #1 is tagged **GAP** (owner 2026-10-28: gaps go to a ranked to-do list; they never block a ship,
   because six rounds of open-ended gaps never ended). Only wrong, misleading, confusing or broken things block.
   Not defects (owner 2026-10-27): the site is anonymous by choice, so no named author or contact; and data that no
   public U.S. dataset holds (private flood prices, cost by home value, one home's own premium) when the page says so.

## Materials (local; browse the web only for the SEO search above or to check one FEMA rule, and name it)
- Phone screenshots (390px), in reading order: C:\Users\mwoo7\Desktop\floodinsurance\state\reviews\round16\ (home-00..home-08.png; louisiana-00..louisiana-26.png; palm-beach-county-fl-00..palm-beach-county-fl-22.png; maine-00..maine-21.png; nebraska-00..nebraska-25.png). LOOK at every one.
- Built HTML: C:\Users\mwoo7\Desktop\floodinsurance\dist\index.html; C:\Users\mwoo7\Desktop\floodinsurance\dist\flood-insurance\louisiana\index.html; C:\Users\mwoo7\Desktop\floodinsurance\dist\flood-insurance\palm-beach-county-fl\index.html; C:\Users\mwoo7\Desktop\floodinsurance\dist\flood-insurance\maine\index.html; C:\Users\mwoo7\Desktop\floodinsurance\dist\flood-insurance\nebraska\index.html. Numbers carry `data-p="path"`, the JSON path they came from.
- Data: C:\Users\mwoo7\Desktop\floodinsurance\data\states\louisiana\{agg,data,extras}.json; C:\Users\mwoo7\Desktop\floodinsurance\data\c\palm-beach-county-fl\{agg,data,extras}.json; C:\Users\mwoo7\Desktop\floodinsurance\data\states\maine\{agg,data,extras}.json; C:\Users\mwoo7\Desktop\floodinsurance\data\states\nebraska\{agg,data,extras}.json. Spot-check numbers against it; check each number means what its label says.
- Definitions: tools/metrics.py and tools/rules_registry.py (rule text and its official source).
- Do NOT read the site's gate code. Write your own defect list first. Only then read the previous review, if any:
  C:\Users\mwoo7\Desktop\floodinsurance\state\reviews\hater-round15.md, and add "Previous items": each earlier BLOCKER/MAJOR marked FIXED, NOT FIXED or PARTLY, with evidence.

## Output
Write C:\Users\mwoo7\Desktop\floodinsurance\state\reviews\hater-round16.md. For EACH page a section headed exactly `## <slug>` (slugs: home, louisiana, palm-beach-county-fl, maine, nebraska), with:
- defects worst-first, each tagged **BLOCKER** (wrong or misleading info a reader could act on), **MAJOR**
  (confusing, untrustworthy or broken: a figure or sentence that a reader would misread), **GAP** (something #1 has
  that we do not; ranked, never blocking) or **MINOR** (polish); the screenshot or exact quoted text; what is wrong;
  why the reader is hurt. A missing feature is a GAP, never a MAJOR;
- a last line exactly `Verdict: PASS` or `Verdict: FAIL`. PASS only with zero BLOCKER and zero MAJOR.
Then a "Classes" section: defects likely on every page of that template (home / state / county).
Edit no other file. Reply with per-page counts, the 10 worst defects one line each, and the previous-items tally.
