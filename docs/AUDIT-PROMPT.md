MASTER AUDIT: floodinsurancedata.com (owner 2026-11-04; run monthly, and before any big batch)
Auditor: a fresh agent that built nothing here. Read-only. Script first; AI judges only what a
script cannot. Every finding = evidence (file:line, URL, number, command output) or it is dropped.
Severity: BLOCKER (wrong or misleading live text, data loss, ship broken) / MAJOR (wastes money
or tokens, or blocks rank) / MINOR. Report max 25 lines, sorted by severity, each with its fix and its cost.

1. TRUTH (the one unforgivable sin)
- Recompute 10 random live figures from raw FEMA files; any mismatch = BLOCKER.
- Every base labelled (median vs mean, homes vs all policies, as-of date)? Same figure, different number across pages?
- Every law sentence: is the official text, fetched today, still saying it? Any rewording beyond the quote?
- Any sentence with no source behind it, any "should/safe" verdict, any advice?

2. READER (phone, 30 seconds, scared)
- Live page at 390 px: are the 6 answers on screen 1? Any faint, tiny, overflowing or overlapping text, on ALL pages, not a sample?
- Tools: 1,000 fuzz inputs; any NaN, blank or wrong date?
- Read 3 random pages as the reader: any confusing, repeated or padded block? Name it.

3. GOOGLE / RANK
- Search Console: indexed vs submitted, impressions, clicks, position, top 50 queries. Which query has no page that answers it?
- Real Google search for 10 of our queries: who holds the top 3, and what do they give that we don't?
- Near-duplicate check: any two pages more than 80% alike? Any page with thin unique text?
- Links: broken, orphans, depth; backlinks count (0 = top MAJOR).

4. MONEY
- Revenue path status: ads gate date, referral licensing/FTC status, anonymity decision. Any blocker with no date = MAJOR.
- Traffic needed for $1,000/month at sourced rates; months to get there at the current trend.

5. MACHINERY
- Every gate and check ID: when did it last catch a real defect? Zero in 30 days and guards no number or law = delete.
- Every cloud job: minutes per run, failures in 30 days, projected to 2,000 pages. Anything over 10% of total time gets "only what changed".
- Rollback, refresh and publish: did each run successfully this month? Prove with the run log.
- Two writers on any file or job? Anything piling up on the laptop or in the repo?

6. TOKENS AND PROCESS
- Tokens per change to the scoreboard, this month vs last.
- Review rounds: how many found nothing new? Defect classes found twice and still not a script check?
- CLAUDE.md under 8 KB, PLAN.md under 6 KB? Backlog items older than 30 days that no real query asks for = delete.
- Commits that were rework (fix of a fix): count, and the root-cause layer for each.

7. SCALE (at ~2,000 counties, 24 months)
- For each layer above: the number where it breaks, measured, never guessed.

OUTPUT: the 25-line list, then the 3 deletions and the 1 build that move the scoreboard most. Nothing else.
Cost: script parts near zero; one fresh agent plus real searches, about 100-150k tokens.
