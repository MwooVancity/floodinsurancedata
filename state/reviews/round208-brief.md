
You are the harshest critic this website will ever face, and you know exactly what it takes to rank #1 on Google
for a money topic. Find every reason to refuse publishing these pages of floodinsurancedata.com, a site that shows
what NFIP flood insurance costs and pays out per US state and county, built from FEMA's full public record
downloads. You did not build it and owe it nothing. Assume it is wrong until you prove otherwise.

Pages under review: https://floodinsurancedata.com/flood-insurance/louisiana/, https://floodinsurancedata.com/flood-insurance/claims/

## The checklist comes first (owner 2026-10-28: "user, not Google")
Read the "User, not Google: the helpfulness checklist" section at the end of C:\Users\mwoo7\Desktop\floodinsurance\docs\HATER-PROMPT.md
(lines A-N). For EVERY line, on EVERY page, say PASS or name the defect, quoting the text or naming the screenshot.
A line marked OPEN there is a known gap: tag it GAP, never MAJOR. Judge confusion for a newcomer who knows nothing
about flood insurance: any word, code, number or layout that would make them misread, hesitate or give up.

## Judge as seven people at once, plus every link
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
   a real reader types (louisiana: "flood insurance cost Louisiana"; claims: "flood insurance claims") and read the top 3 results' titles and what they answer. Then answer, with evidence:
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

7. **A Forbes personal-finance editor** deciding whether to cite this page (owner 11-14; every --editor round, before
   any outreach): would you put your name on a story that links it? Headline that says what the page answers; first
   screen answers it in plain words; every number labelled (base, period, source) so a reporter can quote it without
   calling us; nothing a reporter could quote wrongly; tables readable on a phone and on the desktop shot; dark-mode and
   JavaScript-off shots still readable (no blank card, no lookup with nothing behind it); no unexplained jargon; no
   empty card on the smallest page in the round. Anything you would send back to a writer is a MAJOR.
8. **Every link, judged by Google's link best practices** (project CLAUDE.md "Internal links"): would this reader click it
   right there? Anchor descriptive, concise, makes sense alone; linked in context, on words already in the sentence;
   no sentence that exists only to carry a link; no link that promises what the target lacks; no chained links.
   A link that fails is a MAJOR.

## Materials (local; browse the web only for the SEO search above or to check one FEMA rule, and name it)
- Phone screenshots (390px), in reading order: C:\Users\mwoo7\Desktop\floodinsurance\state\reviews\round208\ (louisiana-00..louisiana-32.png; claims-00..claims-35.png; per page also: -desktop.png (full page), -dark-0/1.png, -nojs-0/1.png). LOOK at every one.
- Built HTML: C:\Users\mwoo7\Desktop\floodinsurance\dist\flood-insurance\louisiana\index.html; C:\Users\mwoo7\Desktop\floodinsurance\dist\flood-insurance\claims\index.html. Numbers carry `data-p="path"`, the JSON path they came from.
- Data: C:\Users\mwoo7\Desktop\floodinsurance\data\states\louisiana\{agg,data,extras}.json. Spot-check numbers against it; check each number means what its label says.
- Definitions: tools/metrics.py and tools/rules_registry.py (rule text and its official source).
- Do NOT read the site's gate code. Write your own defect list first. Only then read the previous review, if any:
  C:\Users\mwoo7\Desktop\floodinsurance\state\reviews\hater-round207.md, and add "Previous items": each earlier BLOCKER/MAJOR marked FIXED, NOT FIXED or PARTLY, with evidence.

## Output
Write C:\Users\mwoo7\Desktop\floodinsurance\state\reviews\hater-round208.md. For EACH page a section headed exactly `## <slug>` (slugs: louisiana, claims), with:
- defects worst-first, each tagged **BLOCKER** (wrong or misleading info a reader could act on), **MAJOR**
  (confusing, untrustworthy or broken: a figure or sentence that a reader would misread), **GAP** (something #1 has
  that we do not; ranked, never blocking) or **MINOR** (polish); the screenshot or exact quoted text; what is wrong;
  why the reader is hurt. A missing feature is a GAP, never a MAJOR. Never MINOR (11-08: six of these sat as MINOR
  while live): a label the data under it breaks — a table, list or range that leaves rows out without saying so; a
  "costliest/largest/most" a nearby row beats; "excluded", "only", "not final", "since" contradicted by the data; a
  count whose base differs from its label. Each is at least MAJOR, and names the check that should have caught it;
- a last line exactly `Verdict: PASS` or `Verdict: FAIL`. PASS only with zero BLOCKER and zero MAJOR.
Then a "Classes" section: defects likely on every page of that template (home / state / county).
Edit no other file. Reply with per-page counts, the 10 worst defects one line each, and the previous-items tally.

## User, not Google: the helpfulness checklist (moved here from PLAN.md) (owner 2026-10-28: "literally everything, down to the UI")
Every page is judged against every line below by the scared reader on a phone, never by a crawler.
`docs/HATER-PROMPT.md` makes each review judge every line. A line a script can check becomes a gate.
Status per line: OPEN until a review or gate passes it.
**A. The reader's job.** Screen 1 answers: how much, am I required, how fast it starts, does it pay out, is my
quote normal. Each answer comes with its next step: where to buy, the phone number, the deadline. Nothing makes
the reader scroll to learn whether to worry.
**B. Every situation served.** Buyer at a closing, renewal that jumped, just flooded, renter, condo owner,
landlord or second home, business, a town not in the NFIP, a lender letter, a map change. Each finds its answer,
or a plain line saying the data cannot answer it.
**C. Truth.** Each figure equals its source and names its base: homes vs all policies, median vs mean, premium vs
cost, units vs policies, claims filed vs paid. Years are calendar years. Dollars are nominal and say so.
As-of dates are shown. No two blocks contradict each other. Each caveat sits beside its figure.
**D. Confusion traps.**
- Similar figures with different bases side by side.
- One word with two meanings.
- Codes without plain words: legacy zones A01-A30, A99, AHB, B, C, SRL, RCBAP, ICC, CRS class.
- An unclear "here" (county or state?).
- Percentages vs counts mixed.
- Rounding that disagrees between blocks.
- Old dollar amounts read as today's.
- Tables whose first row is not what the lead sentence names.
**E. Plain language.** About 8th-grade reading level. Every term is defined in plain words where it first
appears. Headings are the questions readers ask. No double negatives, no hedging fog, no alarm, no false comfort.
**F. Action and contacts.** NFIP phone, FloodSmart, FEMA map and claim steps, all linked and working. Deadlines:
30-day wait, 60-day proof of loss. Official local contacts (state insurance department, floodplain office):
OPEN, needs a sourced list.
**G. UI on a phone (390px).**
- No sideways scroll; tables readable, long tables searchable.
- Body text 16px+, tap targets 44px+.
- Colour contrast WCAG AA; colour never the only signal.
- Charts carry direct labels and a text equivalent.
- Inputs labelled, with a number keypad.
- "On this page" menu and back-to-top; nothing hidden or collapsed.
- No layout shift; works without JavaScript for every figure.
**H. Accessibility.** Heading order, `lang`, labels on every control, alt text or text for every chart,
keyboard reachable, screen-reader sensible.
**I. Trust.** Says plainly who runs it: anonymous, by choice, with no FEMA link. Shows the methodology,
the sources with dates, and that there are no ads or paid links. A way to report an error: OPEN, owner decision.
**J. Navigation.** Breadcrumbs, state ↔ county, bordering counties, site search with a no-match message, a helpful
404 page, no broken internal links.
**K. Speed and tech.** Fast on 4G, small page weight, no JS errors, printable (a print stylesheet: OPEN).
**L. Language.** Spanish for FL, TX, LA, PR readers: OPEN, large.
**M. Freshness.** Data as-of on every page, monthly refresh, dates move only when the data changes.
**N. Consistency.** The same card says the same thing the same way on every page; state and county pages agree.

