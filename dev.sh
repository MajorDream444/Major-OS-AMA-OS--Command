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
  "index.html"
  "styles.css"
  "app.js"
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
echo "Starting Command Center UI scaffold..."
echo "URL: http://localhost:4173"
echo

if command -v python3 >/dev/null 2>&1; then
  python3 -m http.server 4173
else
  echo "python3 is required to run the static dev server."
  exit 1
fi
