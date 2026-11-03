# Fixlog round 55

- MAJOR (FEMA audit 2026-11-03): 'policies whose term began in 2025' on an as-of of 07-31 held only Aug-Dec 2025 starts (one-year terms) and sat beside the 2026 group as if a whole year. Root cause: page layer labelled a calendar-year group of in-force policies as the full year. Fix: only the as-of year is shown, labelled by its month span from the data's as-of (build_page.py _yr_span). Proof: palm-beach and louisiana read 'began Jan–Jul 2026'; no 2025 row; round 55 PASS.
