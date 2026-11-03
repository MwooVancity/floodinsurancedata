#!/usr/bin/env bash
# Failure alert for the cloud jobs (owner 2026-10-29: the site must run with no one reading chat).
# Usage (last step of a job, GH_TOKEN set): tools/job_alert.sh fail|ok "<workflow name>" <other workflow file> <max days>
# fail: one open issue per job ("Job failed: <name>"); later failures add nothing while it is open (one email per problem).
# ok:   closes that issue if open, then checks the OTHER job succeeded within <max days> (a job that stopped running
#       cannot report itself, so the daily and monthly jobs watch each other) and opens an issue if not.
# Never fails the job itself: an alert problem must not hide or replace the real result.
set -u
mode=$1; name=$2; other=${3:-}; maxdays=${4:-0}
run_url="${GITHUB_SERVER_URL:-https://github.com}/${GITHUB_REPOSITORY:-}/actions/runs/${GITHUB_RUN_ID:-}"
owner=${GITHUB_REPOSITORY_OWNER:-}

open_issue() {   # $1 title, $2 body: create the issue unless one with this title is open (owner 2026-11-03: one email per problem, not per retry)
  n=$(gh issue list --state open --search "in:title \"$1\"" --json number,title -q ".[] | select(.title==\"$1\") | .number" | head -1)
  [ -n "$n" ] || gh issue create --title "$1" --body "@$owner $2"
}

if [ "$mode" = warn ]; then   # job_alert.sh warn "<title>" "<body>": an early warning; the job still passes
  open_issue "$2" "$3" || true
  exit 0
fi

if [ "$mode" = fail ]; then
  open_issue "Job failed: $name" "The $name job failed on $(date -u +%F). Steps before the failure may have finished, so the live site may or may not have changed. Log: $run_url" || true
  exit 0
fi

n=$(gh issue list --state open --json number,title -q ".[] | select(.title==\"Job failed: $name\") | .number" | head -1)
[ -n "$n" ] && { gh issue close "$n" --comment "Passed again on $(date -u +%F): $run_url" || true; }
[ "$other" = - ] && exit 0   # deploy.yml watches no other job

last=$(gh run list --workflow "$other" --status success --limit 1 --json createdAt -q '.[0].createdAt' 2>/dev/null)
if [ -z "$last" ]; then age=9999; else age=$(( ( $(date -u +%s) - $(date -u -d "$last" +%s) ) / 86400 )); fi
if [ "$age" -gt "$maxdays" ]; then
  open_issue "Job not running: $other" "$other has not succeeded for $age days (limit $maxdays). Check the Actions tab." || true
else
  t=$(gh issue list --state open --json number,title -q ".[] | select(.title==\"Job not running: $other\") | .number" | head -1)
  [ -n "$t" ] && { gh issue close "$t" --comment "$other succeeded again." || true; }
fi
exit 0
