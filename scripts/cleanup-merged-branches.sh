#!/usr/bin/env bash
# Delete remote branches whose work is already in main.
#
# Run this on Major's Mac. The cloud session cannot: `git push --delete`
# returns HTTP 403 through the agent proxy, and the GitHub tools available
# there expose create_branch and list_branches but no delete-branch.
#
# Safety: this does NOT trust any hardcoded list. For every branch it
# re-checks, at run time, that the branch is fully contained in main. A
# branch holding even one commit that main does not have is skipped and
# reported. Nothing unmerged is ever deleted.
#
#   bash cleanup-merged-branches.sh            # dry run, shows what would go
#   bash cleanup-merged-branches.sh --execute  # actually delete
#
set -uo pipefail

EXECUTE=0
[[ "${1:-}" == "--execute" ]] && EXECUTE=1

REPOS=(
  "https://github.com/MajorDream444/major-ai-os"
  "https://github.com/MajorDream444/Major-OS-AMA-OS--Command"
  "https://github.com/MajorDream444/major-moves-series"
  "https://github.com/MajorDream444/maimacademy"
  "https://github.com/MajorDream444/maim_10_pillars"
)

# Never delete these, even if they look merged.
PROTECTED='^(main|master|develop|HEAD)$'

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

total_del=0 total_keep=0

for url in "${REPOS[@]}"; do
  name="$(basename "$url")"
  echo
  echo "=============================================================="
  echo "  $name"
  echo "=============================================================="

  git clone -q --bare "$url" "$WORK/$name" 2>/dev/null || {
    echo "  ! could not clone — skipping"; continue; }
  cd "$WORK/$name" || continue

  default="$(git symbolic-ref --short HEAD 2>/dev/null | sed 's|refs/heads/||')"
  default="${default:-main}"

  merged=() unmerged=()
  while read -r b; do
    [[ -z "$b" || "$b" =~ $PROTECTED || "$b" == "$default" ]] && continue
    if git merge-base --is-ancestor "$b" "$default" 2>/dev/null; then
      merged+=("$b")
    else
      n="$(git rev-list --count "$default".."$b" 2>/dev/null || echo '?')"
      unmerged+=("$b ($n commits not in $default)")
    fi
  done < <(git for-each-ref --format='%(refname:short)' refs/heads/)

  if ((${#unmerged[@]})); then
    echo
    echo "  KEEPING — these hold work that is not in $default:"
    printf '    %s\n' "${unmerged[@]}"
    total_keep=$((total_keep + ${#unmerged[@]}))
  fi

  if ((${#merged[@]} == 0)); then
    echo; echo "  nothing merged to delete"
    continue
  fi

  echo
  echo "  MERGED into $default — safe to delete (${#merged[@]}):"
  printf '    %s\n' "${merged[@]}"
  total_del=$((total_del + ${#merged[@]}))

  if (( EXECUTE )); then
    echo
    echo "  deleting..."
    printf '%s\n' "${merged[@]}" | xargs -n 15 git push -q "$url" --delete \
      && echo "  done" || echo "  ! some deletions failed — see above"
  fi
  cd - >/dev/null || true
done

echo
echo "=============================================================="
printf "  %d branch(es) safe to delete · %d kept as unmerged\n" "$total_del" "$total_keep"
if (( ! EXECUTE )); then
  echo "  DRY RUN — nothing was deleted."
  echo "  Re-run with --execute to delete."
fi
echo "=============================================================="
