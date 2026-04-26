#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "$ROOT_DIR"

echo "Major OS / AMA OS Command Center"
echo "Mode: dev scaffold"
echo

echo "Checking boot files..."
required_files=(
  "README.md"
  "SYSTEM_CORE.md"
  "START_HERE.md"
  "HANDOFF_COMMAND_CENTER.md"
  "docs/HANDOFF_COMMAND_CENTER.md"
  ".env.example"
)

missing=0
for file in "${required_files[@]}"; do
  if [[ -f "$file" ]]; then
    echo "ok: $file"
  else
    echo "missing: $file"
    missing=1
  fi
done

if [[ "$missing" -ne 0 ]]; then
  echo
  echo "Boot scaffold is incomplete. Add the missing files before building dashboard features."
  exit 1
fi

echo
echo "No dashboard app is wired yet. This script currently validates the boot layer only."
echo "Next source-of-truth file: HANDOFF_COMMAND_CENTER.md"
