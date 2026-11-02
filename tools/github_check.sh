#!/usr/bin/env bash
# Master GitHub check: this repo only, one read-only pass, no agent. Prints only what needs a look.
# Failed runs in 7 days, active workflows whose last run failed, scheduled jobs silent over 2 days, open issues.
now=$(date -u +%s); week=$(date -u -d "7 days ago" +%FT%TZ)
for r in MwooVancity/floodinsurancedata; do
  gh run list -R "$r" --limit 100 --json workflowName,conclusion,createdAt,headBranch \
    -q "[.[]|select(.createdAt>=\"$week\" and (.conclusion==\"failure\" or .conclusion==\"timed_out\" or .conclusion==\"startup_failure\"))]|group_by(.workflowName+.headBranch)|.[]|\"$r FAILED \(.[0].workflowName) x\(length) on \(.[0].headBranch), last \(.[0].createdAt)\""
  gh api "repos/$r/actions/workflows" --paginate -q '.workflows[]|select(.state=="active")|"\(.id)|\(.name)"' 2>/dev/null | while IFS='|' read -r id name; do
    last=$(gh api "repos/$r/actions/workflows/$id/runs?per_page=1" -q '.workflow_runs[0]|"\(.conclusion) \(.created_at) \(.event)"' 2>/dev/null)
    [ "${last%% *}" = failure ] && echo "$r LAST RUN FAILED $name: $last"
    sched=$(gh api "repos/$r/actions/workflows/$id/runs?event=schedule&per_page=1" -q '.workflow_runs[0].created_at // empty' 2>/dev/null)
    if [ -n "$sched" ]; then
      age=$(( (now - $(date -u -d "$sched" +%s)) / 3600 ))
      [ "$age" -gt 48 ] && [ "$age" -lt 1440 ] && echo "$r SCHEDULE SILENT $name: ${age}h"
    fi
  done
  gh issue list -R "$r" --state open --limit 10 --json number,title -q ".[]|select(.title|test(\"Job \"))|\"$r ISSUE #\(.number) \(.title)\"" 2>/dev/null
done
echo "check done $(date -u +%H:%M)"
