#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "$ROOT_DIR"

echo "Major OS / AMA OS Command Center"
echo "Mode: run scaffold"
echo

echo "This repo is currently at the clean boot layer."
echo "Read START_HERE.md, SYSTEM_CORE.md, and HANDOFF_COMMAND_CENTER.md before adding runtime features."
echo

echo "Canonical split:"
echo "Command Center = Major-OS-AMA-OS--Command"
echo "Reusable AI OS = Major-AI-OS"
echo "App Factory = 52in52"
echo "Operations DB = Airtable"
echo "Human Dashboard = Notion"
