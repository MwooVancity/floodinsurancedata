#!/usr/bin/env bash
# Deploy dist/, then every live page must equal the page that passed (gate_live.py). If not, put the previous
# release back (HEAD~1's dist passed the day before), check it, and exit 1 so the job fails and alerts.
# DRILL_CORRUPT=1 (drill only): change one built page after the deploy, so live differs and the rollback must run.
set -e
W="npx --yes wrangler@4.86.0"
n=$(find dist -type f | wc -l); echo "files: $n"; [ "$n" -lt 19000 ]   # Cloudflare free plan: 20,000 files a deploy
$W deploy
sleep 30
[ "${DRILL_CORRUPT:-}" = 1 ] && echo "<!-- drill -->" >> dist/index.html
if python -I tools/gate_live.py; then exit 0; fi
echo "ROLLBACK: live differs from what passed; deploying the previous release"
git checkout HEAD~1 -- dist
$W deploy
sleep 30
python -I tools/gate_live.py && echo "ROLLBACK OK: previous release is live"
exit 1
