# Hater round 7 (built dist/ pages + 61 phone screenshots in round7/)

**Method.**
- **Screenshots:** I looked at all 61: home-00..08, louisiana-00..26 and palm-beach-county-fl-00..24.
- **Pages:** I pulled the visible text, title, meta and JSON-LD of the three built pages.
- **Number check:** a script resolved every `data-p` path against data/states/louisiana/{agg,data,extras}.json, data/c/palm-beach-county-fl/{agg,data,extras}.json and data/states/florida for the "Florida:" comparisons. That is 408 figures on Louisiana and 142 on Palm Beach. All match the files within display rounding.
- **Figures with no `data-p`:** I checked share_below, prem/frp medians, zone units, penetration, multiloss, NRI, storm events, IA totals, the state table (51 rows, 4,580,802 units, which matches "4.6M"), the 42 county rows, and the Palm Beach Florida rank (8th of 55). All match.
- **Definitions read:** tools/metrics.py and tools/rules_registry.py.
- **Not read:** the gate code.
- **Quote checkers:** I did not run them in a browser. I read their scripts and computed by hand what each prints for its page's median.
- **One FEMA rule checked on the web:** 44 CFR 61.11 on govinfo.gov, the source the page itself cites.
- **SERP:** three WebSearch queries, below.
- **Order of work:** I wrote this defect list before reading hater-round6.md.
- **Not verified:** the home "Average premium alone $1,000" row (I found no U.S. aggregate file to check it against), the declaration counts (67 / 22; the definition of which declaration types count is not on the page), and the ZIP and parish search boxes, which I did not run.

**SERP (WebSearch, 2026-10-28):**
- **"flood insurance cost":** Kiplinger ($888, Policygenius/FEMA), Bankrate, NerdWallet ($899 a year / $75 a month), Fox Business, Progressive. Insurify gives an NFIP median of $786. All lead with one national number, then cost by state and cost by zone.
- **"flood insurance cost Louisiana":** MoneyGeek ($750 average), Insurance Journal ("Louisiana braces for higher costs"), Insurify ($1,470 single-family median; Plaquemines $4,752), Policygenius ($752; $560 in zones B/C/X).
- **"flood insurance cost palm beach county FL":** NerdWallet FL guide (Palm Beach $528, West Palm Beach $349), MoneyGeek FL ($466), Miami Herald / Sun Sentinel stories on ZIP-level increases (33469 +342%), and a stale pbc.gov 2018 stats page.

**Quote checkers, computed from the scripts:**
- **home** (`v<713 / <1055 / <1309 / <2150`).
  - Input 1055 (the median) prints "$1,055 is above the middle of U.S. single-family policies (half pay $713 to $1,309)."
  - The typical value is called "above the middle".
- **louisiana** (`P={p25:863,p50:1086,p75:1273,p90:1905}`).
  - Input 1086 prints "$1,086 is in the upper-middle — more than about half of existing policies here. (half pay $863 to $1,273, typical $1,086). Renewing? Policies whose term began in 2026 typically pay $1,215."
- **palm-beach-county-fl** (`P={p25:517,p50:670,p75:1034,p90:1297}`).
  - Input 670 prints "$670 is in the upper-middle — more than about half of existing policies here. (half pay $517 to $1,034, typical $670). Renewing? Policies whose term began in 2026 typically pay $679."
- **Defects in all three:**
  - The median itself is labelled above or upper-middle.
  - The state and county scripts print a sentence-ending period followed by a parenthetical and a second period: "here. (half pay … $670)."
  - Below p25 the scripts print "below the lowest quarter", but the value is *in* the lowest quarter.
  - The arithmetic and bands are otherwise correct.

## home

- **MINOR** (checker labels the median wrong).
  - **What it prints:** "$1,055 is above the middle" for an input equal to the median, because of `v<1055` then `v<1309`. The placeholder "e.g. 1060" also lands "above the middle".
  - **Why it hurts:** a reader paying exactly typical is told they are above it.
- **MINOR** (search box dead-ends).
  - **What happens:** the placeholder says "Type your state or county…", but only 42 counties are listed. Typing an uncovered county (e.g. "orange county fl") hides every row of both tables and prints nothing: no "no page yet, see your state" line.
  - **Why it hurts:** on a phone this looks broken, and the page gives no next step.
- **MINOR** (label vs value).
  - **The mismatch:** "County pages: 42 counties so far, listed by number of policies" (home-06), but the column and the sort are "Insured units".
  - **Why it matters:** units are not policies; the page itself makes that distinction elsewhere.
- **MINOR** (screen 1 numbers on different bases).
  - **The numbers:** "Built from 3,490,299 NFIP policy records" sits next to "4.6M insured units".
  - **Partly explained:** the gap is condo units, and the note above explains units.
  - **Still a misread:** a reader still sees 3.5M vs 4.6M "policies" on one screen.
- **MINOR**. The "Why do sites quote different prices?" note says "Premium plus fees except the last row" (home-03), but the last row's label already says "before the federal fees", so the note is redundant. I could not verify the $1,000 itself.
- **GAP 1** (vs NerdWallet / Policygenius / Bankrate). There is no cost by flood zone (A/V vs X) on home. Every top-3 result answers it as the second question, and the site holds `cost_by_zone` per state.
- **GAP 2**.
  - **What is missing:** a line naming the figures the searcher just saw ($899 NerdWallet, $888 Policygenius, $786 Insurify) and which of our rows each matches.
  - **Why ours lands higher:** our lead number is $1,055, which is $156–269 above all three. Our premium-only mean is $1,000; theirs are older premium-only averages or include other policy types.
- **GAP 3**. Private flood. Top results say when a lender must accept private flood (42 U.S.C. 4012a(b)) and whether private flood can be cheaper. We say only "Private flood insurance is not in this data."
- **GAP 4**. No territories (Puerto Rico, USVI, Guam), and no line saying they are left out.
- **GAP 5**. Home has no JSON-LD, while state and county pages do.
- **What we have that no top result has:**
  - **The list:** FEMA's own full-record median per state (51 rows), new-buyer vs existing price, and a fees-vs-premium reconciliation.
  - **Where it is:** the $1,055 and "Buying? $995" are on screen 1. The per-state table starts at home-03, which is fine.
- **Would a searcher bail?**
  - **What they see:** screen 1 answers "how much" faster than NerdWallet ($1,055, $88 a month, and the new-buyer price).
  - **Where they bail:** at home-03, if they are hunting for "my zone" pricing, because nothing on home gives it.
- **Templated?** "Three things to know first" is the same rule text as the state and county pages. Law text has to be the same everywhere, so I log it as a class item, not a defect.

Verdict: PASS

## louisiana

- **BLOCKER** (rule misstated; reader can act on it and be uncovered).
  - **The sentence (louisiana-05):** "Exceptions: no wait if you buy while making, increasing, extending or renewing a mortgage, **or change coverage at renewal**; … (44 CFR §61.11)."
  - **What the cited regulation says:** 44 CFR §61.11 (govinfo, CFR-2024) has no renewal exception. Its paragraph (d) says the 30-day wait applies to "any new policy, added coverage, or increase in the amount of coverage", except under (a) map revision, (b) loan closing and (c) post-wildfire. Paragraph (e) says mid-term increases are "subject to any applicable waiting periods".
  - **The registry:** the `wait_exceptions` entry in rules_registry.py has no source excerpt for the renewal clause. Its two excerpts cover only the mortgage and map-revision clauses.
  - **The harm:** a Louisiana homeowner who raises coverage at renewal in hurricane season, believing there is no wait, can be under-covered for 30 days. Either delete the clause, or source it to FEMA's Flood Insurance Manual with the exact condition.
  - **Also missing:** the real post-wildfire exception (61.11(c)).
- **MAJOR** (misleading reassurance on "would it pay to rebuild").
  - **The headline (louisiana-09):** "Not in full for 21.5% of the 212,784 single-family policies here that report a rebuilding cost."
  - **What the reader takes from it:** the other 78.5% would be rebuilt in full.
  - **What the page's own figures say:**
    - Only 64.8% of single-family policies carry the full $250,000 building limit, so about a third carry less.
    - 16.1% of paid claims had damage above the coverage.
    - The rcv_80 rule printed just below means anyone insured under 80% of rebuilding cost gets depreciated value.
  - **Effect:** the headline counts only the cap and ignores the underinsurance the same card proves.
  - **A second problem:** the note says "A policy can carry the full limit on a home whose reported rebuilding cost is lower". That is a program-rule claim with no registry source. The 64.8% vs 21.5% gap may also be unreported rebuild costs.
- **MINOR** (checker copy).
  - **Wording:** "below the lowest quarter — cheaper than about 75%" should be "in the lowest quarter".
  - **Punctuation:** "here. (half pay $863 to $1,273, typical $1,086)." has two sentence ends.
  - **The median:** an input of exactly $1,086 is called "upper-middle".
- **MINOR** (headline pool).
  - **The split:** the title, meta, hero and checker still use the mixed 2025/2026-term $1,086, while 2026-term policies pay $1,215.
  - **Why it is now a MINOR:** it is mitigated, because the "Renewing? $1,215" line is on screen 1 and the checker now appends it.
- **MINOR** (wording). "Half of homeowners here pay between $863 and $1,273" (louisiana-03). It is half of single-family primary-home *policies*, not half of Louisiana homeowners; only 22% of homes have NFIP cover.
- **MINOR** (events vs years on different bases).
  - **The definitions:** event totals include ICC (`event_paid` = building + contents + ICC in metrics.py), while yearly totals exclude it.
  - **The visible clash:** Katrina $13.3B + Rita $412.9M = $13.72B in the table, above the 2005 bar of $13,559,493,222.
  - **What the page says:** the events note says only "only claims that paid something" and does not say it adds ICC.
- **MINOR**. "Among the five costliest years, these have no named event … : 1995" uses a plural subject for one year (louisiana-08).
- **MINOR**. The cost bar (louisiana-04) has no axis values, and the unlabelled tick at the far right is p90 ($1,905).
- **MINOR**. "up to 35% in Jefferson Parish" on screen 21 is qualified only two paragraphs later by "A community named for the parish covers its unincorporated area only." Kenner and Gretna residents read 35% as theirs.
- **MINOR**. JSON-LD BreadcrumbList item 1 is `https://floodinsurancedata.com/flood-insurance/`, and dist/ has no flood-insurance/index.html, so the breadcrumb points to a 404.
- **MINOR**. JSON-LD says "NfipPolicies v3 / NfipClaims v3", but the citation and source-list URLs are the "-redacted-policies-v2" / "-claims-v2" pages. This is not fixed from round 6.
- **MINOR**. "downloaded October 25, 2026" (louisiana-01) vs "The newest of these downloads was October 26, 2026" (louisiana-26), and JSON-LD `dateModified` 2026-10-25.
- **MINOR**. "Mid summer severe storms (2016)" lost the hyphen, and the data-q value is "Mid-summer". The parish sort is case-sensitive: "Jefferson Davis" comes before "Jefferson", and "LaSalle" before "Lafayette".
- **MINOR**. H1 "Flood insurance in Louisiana" drops "cost", the query word that the title carries.
- **GAP 1** (vs Insurify). There is no "find your parish" link on screen 1, and the parish table starts at louisiana-12, the 13th phone screen. Insurify's parish list is one tap.
- **GAP 2** (vs Insurify). Plaquemines "$4,752" (Insurify) vs our "$1,231" is unreconciled. There is no parish-level full-risk or mean column. The state row "Full-risk premium plus average fees $1,466" matches Insurify's $1,470 state figure, but the page never says so.
- **GAP 3** (vs Insurance Journal / Policygenius). The question "how much more will I pay as I rise to full risk?" is unanswered, beyond the $859 → $1,220 premiums and the 18% cap. No "years to full risk at 18%" figure is given.
- **GAP 4**. Private flood (see Classes).
- **GAP 5**. No NOAA storm-events panel at state level, though the county template has one.
- **GAP 6**. Per-parish penetration and multi-loss counts are in data.json but not in the parish table.
- **What we have that no top result has:**
  - **The data:** the full-record claims history, unpaid reasons from 107,750 claims, the CRS discount by community, the 56.6% below-full-risk share with its gap, cost by zone with n, and download completeness.
  - **Where it sits:** screen 1 carries the cost, renewal, buyer, payout and the requirement. Unpaid reasons and CRS are 7–20 screens down.
- **Would a searcher bail?** Screen 1 answers "how much" outright ($1,086, $91 a month, $863–$1,273), faster than MoneyGeek or Insurify. The bail point is the parish question, at about louisiana-03, when no parish link appears.

Verdict: FAIL

## palm-beach-county-fl

- **BLOCKER** (same template rule as Louisiana). On palm-beach-county-fl-05, "or change coverage at renewal" is not in 44 CFR §61.11, which says increases wait 30 days. In South Florida in hurricane season, this is the most actionable wrong sentence on the site.
- **MAJOR** (wrong count, broken lookup).
  - **The claim:** "All 71 ZIPs with NFIP policies here are in the lookup" (palm-beach-county-fl-11).
  - **What the ZD object actually holds:**
    - 71 keys, but only 61 of them are five-digit ZIPs.
    - 10 are ZIP+4 strings ("33418-4628", "33437-4265", …).
    - 5 are not Palm Beach County ZIPs: 32507 "Warrington" (Pensacola), 32333 "Havana", 34401 and 34417 (Ocala area), and 34394.
  - **What a reader sees:** typing 32507 on the Palm Beach page prints "32507 (Warrington): 1 policy units". That is wrong and ungrammatical.
  - **Why it matters:** the count is wrong, and the lookup vouches for mis-geocoded records. A competitor screenshot writes itself.
- **MAJOR** (misleading reassurance on rebuild; same template as Louisiana).
  - **The figures:** "Not in full for 50.6% … above the $250,000 building limit" next to "91.5% insured to the building maximum".
  - **The unsourced note:** it still asserts, without a source, that "A policy can carry the full limit on a home whose reported rebuilding cost is lower".
  - **What the numbers imply:** 27,755 of 50,781 report a rebuild cost. Even if every non-reporter were insured at the maximum, at most about 73% could be at the cap, given that only 50.6% of reporters have rebuild costs above it. So the 91.5% needs over-insurance, or the field means something else.
  - **The reader's question:** whether "my home would be rebuilt", which this card does not settle.
- **MAJOR** (scary screen-1 figure, carried over from round 6).
  - **The tile:** "Does it pay out here? 43.5% of claims here paid something (Florida: 69.9%) … $15,396" (palm-beach-county-fl-01).
  - **What a reader concludes:** a just-flooded reader concludes their claim will probably not pay.
  - **What the page doesn't show:** which years the 6,077 unpaid claims came from. Irene 1999's average was $9,656 and the catch-all "Flooding" average $2,625, so they are likely old small-rain claims. The paid share in recent named storms is not shown either.
  - **What we have:** the reasons table exists, but the era breakdown that would make 43.5% readable does not. Until it does, the comparison invites a wrong decision, such as "not worth buying".
- **MINOR** (checker copy). It has the same three defects as Louisiana: "below the lowest quarter", ". (" punctuation, and the median called "upper-middle".
- **MINOR** (copy). "downloaded October 25, 2026 with every record for Florida, every record the download listed was received, none missing" (palm-beach-county-fl-01) is a comma splice that reads like two drafts merged.
- **MINOR** (events note).
  - **The note:** "these have no named event in this table, because FEMA filed their claims under a general label: 2025, 1995, 2014".
  - **The problem:** 1995 does have a named event in the data, Hurricane Opal, with 7 claims and $1,356,819 (extras.claims.events.6). The table drops it, though it out-pays the listed Wilma at $1.12M. The stated reason is therefore false for 1995.
  - **Note on the data:** Opal making landfall in the Panhandle with a $193,831 average here is itself a geocoding red flag worth a line.
- **MINOR**. Events include ICC while the year bars exclude it (same as Louisiana; no visible clash here).
- **MINOR**. ZIP labels: "33437" and "33446" have no town, and "33428 Watergate" is a CDP name where residents say Boca Raton (palm-beach-county-fl-11/12). This is not fixed from rounds 5 and 6.
- **MINOR**. "Half of homeowners here pay between $517 and $1,034". That is policyholders, not homeowners, and only 13% of homes are insured.
- **MINOR**. "To check a quote, use the checker at the top" (palm-beach-county-fl-04), but the checker is a section below the hero, not at the top.
- **MINOR**. "How often is this county a flood disaster?" lists hurricane declarations that were mostly wind (Milton 2024, Nicole 2022). The headline says "flood disaster"; the body says "floods or storms".
- **MINOR**. NOAA's "$71.1 million" (1996–2025) sits a few screens from NFIP's "$72.0 million" (1978–2026). They mean different things and are easily merged. NOAA dates use a hyphen "1996-2025"; the rest of the page uses an en dash.
- **MINOR**. The "No CRS discount (15)" list is not alphabetical ("Westlake; Atlantis; Belle Glade…").
- **MINOR**. JSON-LD has v3 text with v2 URLs, the breadcrumb points to a 404 (/flood-insurance/), and `dateModified` is 10-25 vs the newest download 10-26.
- **GAP 1** (vs NerdWallet FL). Private flood and Citizens. The page does not say whether Citizens or a lender accepts a private flood policy, or how private compares. This is the state where it matters most.
- **GAP 2** (vs NerdWallet / MoneyGeek). There is no row naming $528 (NerdWallet) or $466 (MoneyGeek) and saying which of ours they match. Our "Typical premium only $507" sits between them, unmentioned.
- **GAP 3** (vs Miami Herald / Sun Sentinel). There is no ZIP-level below-full-risk share or full-risk median. The news results answer "how much will my ZIP rise"; we give only the ZIP's median today.
- **GAP 4**. No cost by municipality, though the CRS table names 40 towns and a reader thinks in towns.
- **What we have that no top result has:**
  - **The data:** FEMA's own full-record ZIP medians for 71 lookup keys (61 real), the unpaid-claim reasons, the CRS discount for all 40 communities, a Florida comparison on every tile, the Citizens rule, and the NOAA flood count.
  - **Where it sits:** the ZIP range is on screen 1. The lookup is at palm-beach-county-fl-11.
- **Would a searcher bail?** Screen 1 answers outright ($670, $56 a month, a ZIP range of $450–$1,825), better than NerdWallet's one-line $528. The bail risk is at palm-beach-county-fl-01, where "43.5% paid" reads as "it won't pay".

Verdict: FAIL

## Classes

**Every state and county page (shared template):**
- **BLOCKER.** The `wait_exceptions` text adds "or change coverage at renewal", which the cited 44 CFR §61.11 contradicts. It is on every page that prints that rule.
- **MAJOR.** The rebuild card's headline counts only the $250,000 cap, and its note makes an unsourced claim about the over-limit rule. It appears on every page with replacement-cost data.
- **MINOR: checker script.**
  - "below the lowest quarter".
  - The median is labelled upper-middle.
  - "here. (…)." punctuation.
  - It compares against existing policies only. It never shows the new-buyer distribution, though "Buying?" appears above it.
- **MINOR: events vs years.** Event totals include ICC, year bars exclude it, and the events note doesn't say so.
- **MINOR: wording.** "Half of homeowners here pay between …" means policyholders.
- **MINOR: JSON-LD.**
  - The breadcrumb item 1 is /flood-insurance/, which has no page.
  - The "v3" text sits with v2 citation URLs.
  - `dateModified` is earlier than the newest download date.
- **MINOR: shared paragraphs.** Already flooded, Yearly cap, waiting exceptions, claim-closure explainer and elevated caveat appear word for word on every page. They are law and program text, so being the same is correct. A rater still sees the same blocks on every page; the local data around them is what carries each page.
- **GAP.** Private flood and lender acceptance, and no reconciliation that names the competitor figures the SERP shows.

**State template:**
- **GAP.** No "find your parish/county" link on screen 1; the county table is about 12 screens down.
- **GAP.** No NOAA panel.
- **GAP.** No per-county full-risk or mean column.
- **MINOR.** Case-sensitive county sort.

**County template:**
- **MAJOR.** The ZIP lookup ingests ZIP+4 strings and out-of-county ZIPs, and the "All N ZIPs" count includes them.
- **MINOR.** The events table drops low-count named events while the note says those years have no named event.
- **MINOR.** ZIP town names are blank or are CDP names.

**Home template:**
- **MINOR.** The search box gives no "no match" message.
- **MINOR.** "number of policies" sits under an "Insured units" column.

## Previous items (round-6 BLOCKER/MAJOR)

**home**
- **BLOCKER** headline vs #1 (no premium-only row, no cost by zone): **PARTLY**.
  - **Fixed:** a premium-only row now exists ("Average premium alone … $1,000", home-03).
  - **Still missing:** nothing names $899/$888/$786, and there is still no cost by zone on home (`grep -i zone dist/index.html` finds only the "high-risk zone" rule text).
  - **New tag:** under this round's rules it is GAP 1 and GAP 2, not blocking.
- **MAJOR** templated "Three things to know first": **NOT FIXED** (the same rule text). It is reclassified as a class note, because the text is law.
- **MAJOR** private flood gap: **NOT FIXED** (home-03 still has one line). It is now GAP 3.

**louisiana**
- **MAJOR** 1995 hidden under the catch-all: **FIXED**. The events table now has "Flooding (1978–1998): FEMA's general label, many separate floods 97,855 / $1.1 billion" (louisiana-08), and the note names 1995.
- **MAJOR** Plaquemines $4,752 unreconciled: **NOT FIXED**. It is now GAP 2.
- **MAJOR** reader cannot find their parish: **NOT FIXED**. The screen-1 nav (louisiana-00/01) still has no parish link. It is now GAP 1.
- **MAJOR** zone note contradicts the legacy-code rows: **PARTLY**.
  - **Fixed:** the note now says older maps used A1–A30 and that "Policies keep the label they were rated with, so the old labels are counted on their own" (louisiana-02). The contradiction is gone.
  - **Still there:** 17 legacy rows in the cost table (louisiana-10/11). That is now a MINOR.
- **MAJOR** rebuild tiles misleading: **PARTLY**.
  - **Fixed:** the rcv_80 rule was added (louisiana-10), and the note was rewritten.
  - **Still there:** the headline still counts only the cap, and the new note makes an unsourced rule claim. It is still MAJOR.
- **MAJOR** stale $1,086 pool: **PARTLY**. "Renewing? $1,215" is on screen 1 and appended to the checker output, but the title, meta and checker bands are still the mixed pool. It is now a MINOR.
- **MAJOR** scaled shared text: **NOT FIXED** (still word for word). It is reclassified to a class MINOR because the text is law and program rules.

**palm-beach-county-fl**
- **MAJOR** scary 43.5% unexplained: **NOT FIXED**.
  - **Fixed:** the "many with no specific reason" line is gone, and the card now leads with the top reason.
  - **Still missing:** there is no era breakdown or recent-storm paid share. It is still MAJOR.
- **MAJOR** rebuild tiles: **PARTLY**. The same state as Louisiana; still MAJOR.
- **MAJOR** scaled shared text: **NOT FIXED**. Reclassified to a class MINOR.
- **MAJOR** private flood and Citizens context: **PARTLY**.
  - **Fixed:** the full Citizens rule is on palm-beach-county-fl-02 (matches §627.351).
  - **Still missing:** private flood acceptance is absent. It is now GAP 1.

**Also checked (round-6 minors):**
- **Fixed:**
  - The checker placeholders are now local (e.g. 1060 / 1090 / 670).
  - The claims chart now says "Totals for the latest two years are not final".
  - The "Many unpaid claims are no-damage or paperwork closures" tile is gone.
- **Not fixed:**
  - v2/v3 JSON-LD.
  - The Oct 25/26 dates.
  - The Mid-summer hyphen.
  - The parish sort.
  - The Opal drop.
  - The 33437/33446/Watergate ZIP labels.
  - The CRS list order.
  - Home JSON-LD.
  - Territories.

**Tally (14 round-6 BLOCKER/MAJOR items):** FIXED 1, PARTLY 6, NOT FIXED 7. Of the 13 that are not fully fixed, 10 are now tagged GAP, MINOR or class notes under this round's rules. 3 are still MAJOR: Louisiana rebuild, Palm Beach rebuild and Palm Beach 43.5%.
