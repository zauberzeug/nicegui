#!/usr/bin/env bash
# Deterministic data helper for the release-notes skill (see SKILL.md).
# It gathers the parts a script can get right every time, so the model only has to
# do the judgment work (grouping tickets into stories, prose, substantive-commenter
# calls, final sponsor curation).
#
# Usage:
#   release-notes.sh dossier "<milestone>"            # full JSON dossier (default)
#   release-notes.sh verify  "<milestone>" [file]     # milestone set vs #s in file (default release.md)
#   release-notes.sh check-docs <slug> [slug...]      # HTTP status for each docs page
#
# Override the repo/sponsor org via env if ever reused elsewhere:
#   RELEASE_NOTES_REPO=owner/repo  RELEASE_NOTES_SPONSOR_ORG=org
set -euo pipefail

REPO="${RELEASE_NOTES_REPO:-zauberzeug/nicegui}"
SPONSOR_ORG="${RELEASE_NOTES_SPONSOR_ORG:-zauberzeug}"

die() { echo "error: $*" >&2; exit 1; }
command -v gh >/dev/null || die "gh not found"
command -v jq >/dev/null || die "jq not found"

milestone_numbers() {
  local milestone="$1"
  {
    gh issue list -R "$REPO" --milestone "$milestone" --state all --limit 300 --json number --jq '.[].number'
    gh pr list   -R "$REPO" --search "milestone:\"$milestone\"" --state all --limit 300 --json number --jq '.[].number'
  } | sort -un
}

dossier() {
  local milestone="${1:?milestone required}"

  local issue_nums pr_nums
  issue_nums=$(gh issue list -R "$REPO" --milestone "$milestone" --state all --limit 300 --json number --jq '.[].number')
  pr_nums=$(gh pr list -R "$REPO" --search "milestone:\"$milestone\"" --state all --limit 300 --json number --jq '.[].number')
  [ -n "${issue_nums}${pr_nums}" ] || die "no tickets found for milestone '$milestone' (check the exact name)"

  local tickets='[]' n obj
  for n in $issue_nums; do
    obj=$(gh issue view "$n" -R "$REPO" --json number,title,state,author,labels,body,comments --jq '{
      number, title, state, kind: "issue",
      author: (.author.login? // null),
      labels: [.labels[].name],
      commenters: ([.comments[] | .author.login? // empty] | unique),
      refs: ([(.body // "") | scan("#[0-9]+") | ltrimstr("#")] | unique)
    }')
    tickets=$(jq -c --argjson t "$obj" '. + [$t]' <<<"$tickets")
  done
  for n in $pr_nums; do
    obj=$(gh pr view "$n" -R "$REPO" --json number,title,state,author,labels,body,comments,reviews,commits --jq '{
      number, title, state, kind: "pr",
      author: (.author.login? // null),
      labels: [.labels[].name],
      committers: ([.commits[].authors[]? | .login? // empty] | unique),
      commenters: ([.comments[] | .author.login? // empty] | unique),
      reviewers: ([.reviews[] | .author.login? // empty] | unique),
      refs: ([(.body // "") | scan("#[0-9]+") | ltrimstr("#")] | unique)
    }')
    tickets=$(jq -c --argjson t "$obj" '. + [$t]' <<<"$tickets")
  done

  # Cross-references that point outside the milestone: classify issue/pr/discussion
  # and resolve the author, since discussion numbers (feature requests) are invisible
  # to `gh issue view` / `gh pr view` and are the easiest contributor to miss.
  local in_ms extra cross='[]' ref kind author
  in_ms=$(jq -c '[.[].number | tostring]' <<<"$tickets")
  extra=$(jq -r --argjson ms "$in_ms" '[.[].refs[]] | unique | map(select(IN($ms[]) | not)) | .[]' <<<"$tickets")
  local resp
  for ref in $extra; do
    if resp=$(gh api "repos/$REPO/issues/$ref" 2>/dev/null); then
      kind=$(jq -r 'if .pull_request then "pr" else "issue" end' <<<"$resp")
      author=$(jq -r '.user.login // "null"' <<<"$resp")
    else
      kind="discussion"
      author=$(gh api graphql -f query="{repository(owner:\"${REPO%/*}\",name:\"${REPO#*/}\"){discussion(number:$ref){author{login}}}}" --jq '.data.repository.discussion.author.login // "null"' 2>/dev/null || echo null)
    fi
    cross=$(jq -c --arg n "$ref" --arg k "$kind" --arg a "$author" '. + [{number: ($n | tonumber), kind: $k, author: $a}]' <<<"$cross")
  done

  local sponsors
  sponsors=$(gh api graphql -f query="{ organization(login: \"$SPONSOR_ORG\") { sponsorshipsAsMaintainer(first: 100, activeOnly: true) { nodes { sponsorEntity { ... on User { login name } ... on Organization { login name } } tier { monthlyPriceInDollars isOneTime } } } } }" \
    --jq '[.data.organization.sponsorshipsAsMaintainer.nodes[] | {login: .sponsorEntity.login, name: .sponsorEntity.name, monthly: .tier.monthlyPriceInDollars, oneTime: .tier.isOneTime}] | sort_by(-.monthly)')

  jq -n --arg ms "$milestone" --argjson tickets "$tickets" --argjson cross "$cross" --argjson sponsors "$sponsors" \
    '{milestone: $ms, tickets: $tickets, cross_references: $cross, sponsors: $sponsors}'
}

verify() {
  local milestone="${1:?milestone required}" file="${2:-release.md}"
  [ -f "$file" ] || die "file not found: $file"
  local ms rel
  ms=$(milestone_numbers "$milestone")
  rel=$(grep -oE '#[0-9]+' "$file" | tr -d '#' | sort -un)
  echo "Milestone tickets MISSING from $file (investigate each):"
  comm -23 <(echo "$ms") <(echo "$rel") | sed 's/^/  #/' || true
  echo "Numbers in $file NOT in the milestone (expected: cross-refs to discussions/older issues):"
  comm -13 <(echo "$ms") <(echo "$rel") | sed 's/^/  #/' || true
}

check_docs() {
  [ $# -gt 0 ] || die "usage: check-docs <slug> [slug...]"
  local slug code
  for slug in "$@"; do
    code=$(curl -s -o /dev/null -w '%{http_code}' "https://nicegui.io/documentation/$slug")
    printf '%s -> %s\n' "$slug" "$code"
  done
}

cmd="${1:-dossier}"
shift || true
case "$cmd" in
  dossier)    dossier "$@" ;;
  verify)     verify "$@" ;;
  check-docs) check_docs "$@" ;;
  *)          die "unknown command '$cmd' (use: dossier | verify | check-docs)" ;;
esac
