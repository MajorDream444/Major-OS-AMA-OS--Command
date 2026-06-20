# Codex Environment Setup — HAMAL / Major OS

## Purpose

This file is the source-of-truth guide for configuring Codex local environments for the HAMAL / Major OS ecosystem.

The operating model is:

```text
GitHub = source of truth
Local folder = Obsidian working vault / cloned repo
Codex = execution worktree
Graphify = context map
Airtable / Notion = operational databases
```

## Confirmed Repositories

These repositories are visible and available through GitHub connector access:

```text
MajorDream444/Major-OS-AMA-OS--Command
MajorDream444/HAMAL_MOB_PLAYBOOKS
MajorDream444/hanzo-lux-codex-repo
MajorDream444/Major-AI-OS
MajorDream444/major-prime-os
MajorDream444/Major-AI-OS-SUBSTACK
MajorDream444/AMA-PAYMENT
MajorDream444/build-while-you-heal
MajorDream444/mpos-marketing
```

Current source-of-truth split:

```text
Command / context:
MajorDream444/Major-OS-AMA-OS--Command

Playbooks / SOPs / skills audits:
MajorDream444/HAMAL_MOB_PLAYBOOKS

Tooling / MCP / executable integrations:
MajorDream444/hanzo-lux-codex-repo
```

## Canon Folder Decision

`HAMAL_MOB_OS_CANON` can exist locally as an Obsidian vault, but the GitHub source of truth should currently be:

```text
MajorDream444/Major-OS-AMA-OS--Command
```

unless a dedicated `HAMAL_MOB_OS_CANON` GitHub repository is intentionally created later.

Do not let the canon live only as a loose local/iCloud folder.

## Recommended Local Folder Layout

Use a local non-iCloud folder for cloned repos:

```bash
mkdir -p ~/Code
cd ~/Code

git clone https://github.com/MajorDream444/Major-OS-AMA-OS--Command.git
git clone https://github.com/MajorDream444/HAMAL_MOB_PLAYBOOKS.git
git clone https://github.com/MajorDream444/hanzo-lux-codex-repo.git
```

Then open the correct cloned folder in Obsidian using:

```text
Open folder as vault
```

Recommended vault for canon:

```text
~/Code/Major-OS-AMA-OS--Command
```

## Codex Environment Names

Create three Codex environments:

```text
MAJOR_OS_COMMAND
HAMAL_PLAYBOOKS
HANZO_LUX_CODEX
```

Point them at:

```text
~/Code/Major-OS-AMA-OS--Command
~/Code/HAMAL_MOB_PLAYBOOKS
~/Code/hanzo-lux-codex-repo
```

## Standard Setup Script

Use this setup script in each Codex environment:

```bash
cd "$CODEX_WORKTREE_PATH"

# Node projects
if [ -f package.json ]; then
  npm install
fi

# Python projects
if [ -f requirements.txt ]; then
  pip install -r requirements.txt
fi

# Standard HAMAL / Codex workspace folders
mkdir -p .codex
mkdir -p docs
mkdir -p agents
mkdir -p skills
mkdir -p playbooks
mkdir -p outputs
mkdir -p tmp

# Env placeholder only. Never commit real secrets.
if [ ! -f .env ] && [ -f .env.example ]; then
  cp .env.example .env
fi

echo "HAMAL Codex environment ready"
git status
```

## Important Note About Variables

In the Codex Local Environment UI, the `Variables` button beside Setup Script shows only built-in Codex script variables:

```text
CODEX_SOURCE_TREE_PATH
CODEX_WORKTREE_PATH
```

That popup is not a place to add custom API keys.

Do not put secrets in:

- Setup Script
- Actions
- committed Markdown files
- Obsidian notes

Use local `.env` files only.

## Required `.env.example`

Each executable repo should include a `.env.example` like this:

```env
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GITHUB_TOKEN=
TELEGRAM_BOT_TOKEN=
AIRTABLE_API_KEY=
AIRTABLE_BASE_ID=
NOTION_TOKEN=
FIRECRAWL_API_KEY=
TAVILY_API_KEY=
```

## Recommended `.gitignore`

Use this baseline:

```gitignore
# Secrets
.env
.env.local
*.pem
*.key

# Node / Python
node_modules/
__pycache__/
.venv/
venv/
dist/
build/

# Codex / temp
.cache/
tmp/
outputs/tmp/

# OS
.DS_Store

# Obsidian local UI state
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.obsidian/cache/
```

## Recommended Codex Actions

Actions are toolbar buttons. They are not for secrets.

### Git Status

```bash
cd "$CODEX_WORKTREE_PATH"
git status
```

### Pull Latest

```bash
cd "$CODEX_WORKTREE_PATH"
git pull origin main
```

### Save Canon Update

```bash
cd "$CODEX_WORKTREE_PATH"
git add .
git commit -m "Update HAMAL / Major OS canon"
git push origin main
```

### Run Graphify

```bash
cd "$CODEX_WORKTREE_PATH"
graphify . --update --wiki
```

### Open Folder

```bash
open "$CODEX_WORKTREE_PATH"
```

## Agent Rule

Before Codex works on any repo, it must identify:

```yaml
source_of_truth_context: MajorDream444/Major-OS-AMA-OS--Command
source_of_truth_playbooks: MajorDream444/HAMAL_MOB_PLAYBOOKS
source_of_truth_execution: MajorDream444/hanzo-lux-codex-repo
assigned_mob: TBD
workflow: TBD
memory_target: TBD
artifact_target: TBD
kpi: TBD
economic_purpose: TBD
```

## Operating Rule

Major should not manually maintain repetitive repo structure.

If a file, folder, or setup doc is missing and connector access allows it, the assistant or Codex should create it.

Major's role should stay near 10%:

```text
Vision
Decision
Review
Relationships
Closing
```

Agents/Codex should handle the other 90%:

```text
file creation
repo setup
schema drafting
playbook updates
audit docs
handoffs
automation specs
```
