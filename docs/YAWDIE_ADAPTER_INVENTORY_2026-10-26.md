# Yawdie Adapter Inventory and Minimal Vault Integration

**Checked:** 2026-10-26 (Asia/Makassar)

**Runtime source:** `MajorDream444/Major-OS-AMA-OS--Command` at `5ef352f8050f6e702093cc64e6c4b7f067f1f3a0`

**Installed scope:** one local Ollama drafting worker, one SQLite queue, no publishing or external-write adapters

This register distinguishes code that exists from access that is enabled and behavior that was actually verified. Documentation, an Obsidian note, a configured plugin, an authenticated operator CLI, and a Yawdie worker adapter are different things.

## Current evidence

- `yawdie status`: service running; queued 0, running 0, completed 7, blocked 0.
- LaunchAgent `com.major.hamal.yawdie`: running as one process with private state at `~/.local/share/hamal-yawdie`; logs at `~/Library/Logs/HAMAL/Yawdie`.
- Ollama: listening only on `127.0.0.1:11434`; `llama3.2:latest` is installed. Worker source rejects non-loopback endpoints, cloud model metadata/names, and proxies.
- GitHub operator access: `gh` is authenticated as `MajorDream444`; read-only issue, PR and workflow-list commands succeeded for the Command repo. This is **not** inherited by the worker.
- Draft PR #5 is open from this branch. PR creation is an operator-authorized external write, not a Yawdie adapter.
- Deterministic worker tests: 28 passed. Command handoff scripts pass `node --check`.
- The worker suite emitted one Python future-compatibility `SyntaxWarning` for an invalid escape in URL punctuation trimming; tests still passed. This should be corrected in a later focused code change.
- The Substack engine TypeScript no-emit check did not return within the bounded observation window; no pass is claimed and no external API test was run.
- Overnight/sleep-wake observation is still in progress. Do not treat it as verified until the observation period ends.

## Priority adapter register

| Priority / adapter | Exact supported operations today | Existing path and revision | Status | Required access / minimum permission | Test and evidence | Still blocked |
|---|---|---|---|---|---|---|
| 1. Approved local repository reader | No worker operation yet. Proposed first slice: list/read UTF-8 text files and Git metadata only inside explicit repo roots; pin source SHA; reject symlinks, secrets, binaries, `.git`, build output and files above a size cap. | No Yawdie adapter. Graph and handoff conventions exist in `AGENTS.md`, `docs/GRAPHIFY_CONTEXT_LAYER.md`, and `docs/operations/YAWDIE_CROSS_REPO_RECONCILIATION_2026-10-25.md` at `5ef352f`. | **Absent** in worker; documented governance only. | Read-only filesystem permission to an allowlist of exact repository roots. No home-directory traversal. | Proposed: fixture repo + `python3 -m unittest ...test_repository_reader...`; receipt must include root, relative path, SHA, bytes, exclusions and denial cases. | Scope manifest, parser, symlink/size/secret exclusions and tests do not exist. |
| 2. Read-only GitHub issues/PRs/workflows | Operator can inspect repository metadata with `gh issue list`, `gh pr view`, `gh run list`. Worker supports none of these. | No worker adapter at `5ef352f`; current `gh` installation/auth is host state, not repo code. | **Absent** in worker; host access **enabled and verified read-only** for the Command repo. | Existing GitHub credential with metadata/read access; exact owner/repo allowlist. Current token has broader `repo` scope, so an unattended adapter should use a narrower credential or broker. | Verified: issue list returned `[]`; workflow list returned `[]`; PR #5 returned OPEN/DRAFT. Proposed fixture/API-contract tests plus a live read receipt. | Credential isolation, repository allowlist, pagination/rate handling and redacted receipts. No unattended write operations. |
| 3. Brief-to-job planning and dispatch | Submit `source-to-draft` or `operating-brief`; atomic content/task dedupe; explicit `--rerun`; watcher requires `Yawdie-Actionable: true`; template filenames excluded; one claim at a time; unsupported tasks return `blocked: adapter unavailable`. | `runtime/yawdie/yawdie.py`, `runtime/yawdie/worker.py` at `5ef352f`. | **Implemented, enabled, verified.** | Read source file; write private SQLite/artifact state; local loopback Ollama only. | `python3 -m unittest discover -s runtime/yawdie/tests -v`: 28/28 pass. Live jobs and recovery evidence are recorded in the runtime handoff. | Only two bounded draft schemas. No general delegation, adapter dispatch, publishing, messaging or commerce. |
| 4. Allowlisted verification commands in isolated workspaces | No worker command execution. Proposed slice: fixed command IDs mapped to fixed executable/argv templates, cwd inside a disposable/approved worktree, no shell, no model-authored argv, timeout, output cap, concurrency lock and redacted receipt. | No implementation. Existing test commands are human/operator runbooks only. | **Absent.** | Execute permission only for pinned local tools and write permission only in an isolated workspace; no production credentials. | Proposed denial-first tests for unknown command, argv injection, cwd escape, timeout, duplicate executor and output redaction; then one fixture-repo check. | Command manifest, worktree lifecycle and receipt schema. Arbitrary model-generated shell remains prohibited. |
| 5. Local brief/status interface | `yawdie brief`, `yawdie status`, `yawdie report`; service start/stop/uninstall; reports include jobs, attempts, artifact evidence and unsupported-action blocks. | `runtime/yawdie/yawdie.py`, `runtime/yawdie/service.py` at `5ef352f`. | **Implemented, enabled, verified.** | Local user read/write to private state; LaunchAgent control for the same user. | `yawdie status` returned running and 7 completed; unit suite covers status, dedupe, attempts, recovery and idempotent start. | `yawdie service status` is not a valid subcommand; use `yawdie status`. Overnight and real sleep/wake behavior remain unverified. |
| 6. Local health notifications | Queue/service health is available by CLI and private logs. A separate Codex heartbeat named `Yawdie overnight observation` is ACTIVE hourly through the bounded observation period. It observes; it is not a Yawdie notification transport. | Runtime status/report code at `5ef352f`; private Codex automation outside repo. | **Partial.** Health inspection works; local notification delivery is absent. | Read-only state/log access. Any macOS notification adapter would need only local notification permission and explicit severity rules. | Verified service/queue read. Observation has not elapsed; no notification delivery test was performed. | No Notification Center adapter, throttle/dedupe policy, sleep-gap detector or completed overnight evidence. |

## Secondary adapter assessment

| Adapter | Available code vs enabled/verified access | Minimum permission and safe test | Blocked work |
|---|---|---|---|
| Draft PR creation | No Yawdie adapter. Host `gh` can create PRs and PR #5 proves operator access. **Available to the operator, not enabled in Yawdie.** | Read/write pull-request permission on one allowlisted repo; test only with an explicitly approved draft PR and record URL/head SHA. | Approval gate, branch/worktree checks, redaction and prevention of merge/push to protected branches. Keep unattended creation disabled. |
| Substack intake/export | Command repo has local JSON handoff importers: `scripts/import_substack_asset_summary.js` and `scripts/import_substack_queue_handoffs.js` at `5ef352f`. The separate `SUBSTACK-AUTOMATION-ENGINE` at `650edb0eaa34e3b88250f6ed0fbe179de6282781` implements local article packets, dry-run publish checks, Airtable reads and render/publish queue JSON exports. **Local schemas are implemented; no live Substack API adapter exists.** | Read the two exact handoff JSON paths; write derived review copies only. Safe tests: `node --check scripts/*.js`; Substack fixture run in a disposable copy. | Current import commands write tracked workflow reports. Need isolated fixture tests, schema versioning and a Yawdie read-only intake adapter. Live publishing/export to Substack stays blocked. |
| Private asset reading | MAIM repo at `fcc5f6d2ad92ea213c9cd10dd05320e263adaa94` contains catalogue schema/import/test code in `docs/architecture/maim-asset-catalogue.md`, `scripts/import_maim_asset_manifest.py`, migrations and fixture tests. **No Yawdie reader and no private asset-folder approval are present.** | Read-only access to an explicit metadata/manifest folder; never binary-library crawl by default. Test against synthetic fixtures and retain manifest SHA/count, not asset contents. | Approved root, sensitivity labels, provenance/rights fields, file-size/binary policy and adapter code. Hosted database access is not implied. |
| Airtable | Yawdie has none. Substack engine implements GET/list pagination in `src/airtable/client.ts` at `650edb0`; `scripts/sync_airtable.ts` writes only local snapshots and explicitly says mutations are unimplemented. The previously inspected AMA MOB OS v2 vault has standalone scripts that POST/PATCH Airtable; they are not Yawdie adapters and were not run. | Read-only token scoped to one base/table, with exact field allowlist. Safe test: local fixture first; then a bounded GET that records base/table aliases, count and timestamp without record bodies or token values. | Approved base/table/schema, narrow credential injection, proxy/timeout/redaction controls and live read evidence. No Airtable write authority. |
| Provider-specific read-only verification | No generic Yawdie provider adapter. GitHub host reads are verified separately. Command docs mention Vercel, Stripe, Resend, Airtable and other systems, but documentation is not executable access. | One provider/account/resource allowlist per adapter, least-privilege read credential, a versioned receipt and freshness expiry. | Provider identity, authoritative resource IDs and scopes must be approved individually. No aggregate “all providers” adapter. |

## Obsidian inventory: Major OS

### Registered vaults

1. `Obsidian Vault` — not inspected.
2. `Major OS` — **selected by founder; inspected narrowly; local path remains private**.
3. `AMA MOB OS v2` — not selected for integration; its relevant scripts were classified only because they were encountered during the earlier ambiguity check.

### Relevant capabilities and truth status

| Capability | Instructions / documentation | Installed executable/plugin | Configured connection | Verified working capability |
|---|---|---|---|---|
| Human context and system map | `00_Dashboard/command_center.md`, `04_AI_Agents/_index.md`, `04_AI_Agents/_registry.md`, `99_Vault_Audit/20_canonical_map.md` | Obsidian Markdown | Vault registered in Obsidian/iCloud | Files readable locally. Operational claims inside them are not runtime evidence. |
| Templates and periodic notes | Core Templates/Daily Notes enabled; Periodic Notes 0.0.17 installed | Obsidian core + `periodic-notes` | Periodic-note config exists, but no dedicated Yawdie folder/template was found | Plugin installation/config presence only; no Yawdie flow verified. |
| Local semantic search/chat | `smart-connections` 4.3.0 and `.smart-env` | Plugin and local embedding cache present | Embeddings use local Transformers; chat adapter says Ollama, while another legacy field says `open_router` | Not invoked or verified. Conflicting provider fields make this unsuitable for inheritance by Yawdie. |
| Local GPT | `local-gpt` 4.2.2 installed | Plugin bundle present | No dedicated data file was found in the inspected config | Installed only; not verified. |
| Cloud AI plugins | `chatgpt-md`, Text Generator and Excalidraw AI-capable configuration are present | Plugin bundles present | Provider profiles/settings exist; secret values were not read or printed | Not verified and explicitly excluded from Yawdie. Their presence does not authorize cloud inference. |
| Agent definitions | Root registry describes L1-L4 agents and Telegram frontends | Mostly Markdown definitions; several entries explicitly say files are still to be created | No connection to Yawdie queue | Documented only. Do not claim these agents are running. |

### Stale or conflicting truth

- `00_Dashboard/command_center.md` was updated in April and labels systems/agents as running or deployed without receipts. It also references Gumroad and Shopify, now retired in current Command/MAIM doctrine. Treat it as historical context.
- `04_AI_Agents/_registry.md` calls itself the single source of truth, while GitHub is established as authoritative for versioned code/shared operating instructions. The registry is useful context but cannot override current repo instructions or execution evidence.
- The vault audit says the vault is not a Git repository and records architectural duplication, including an embedded mini-vault under `01_Projects/Major_AI_OS/`.
- Smart Connections contains a local Ollama chat-adapter setting and a conflicting OpenRouter platform field. Yawdie must not consume either configuration.
- Plugin installation, model/provider entries and agent notes are not proof of executable or authorized integrations.

## Smallest vault integration proposal

Do not add an Obsidian plugin and do not create a second queue. Add a read-only filesystem adapter only after approval of these exact folders inside the selected vault:

```text
Yawdie/
  Context/          # approved, bounded Markdown context only
  Briefs/
    Inbox/          # actionable founder briefs
  Reports/          # worker-generated human-readable report copies
  Templates/        # never actionable
```

Rules:

1. GitHub owns versioned code, schemas, shared operating instructions and adapter policy.
2. Obsidian owns private human context, working briefs and readable report copies.
3. The existing SQLite spool remains authoritative for source hashes, job state, attempts, dedupe and artifacts. Obsidian filenames/status fields never become a queue.
4. Read only `.md` files under `Yawdie/Context` and `Yawdie/Briefs/Inbox`; write only derived `.md` reports under `Yawdie/Reports`.
5. An inbox note is actionable only when it contains both `Yawdie-Actionable: true` and an allowed `Yawdie-Task`. Template paths and filenames containing `template` remain ineligible. Unchanged content/task dedupes atomically; a changed body is eligible; an intentional rerun uses the existing explicit `--rerun` path.
6. Exclude the rest of the vault by default, especially `.obsidian`, `.smart-env`, `09_Archive`, people, deals, client/private project folders, binaries, canvases, plugin data, caches and hidden files.
7. Resolve links only when the target remains inside the approved context roots. Never expand the whole vault or recursively copy it into prompts or Git.
8. Notes are untrusted context. Code blocks, command links, Dataview/Templater content, plugin instructions and embedded scripts never grant execution permission.
9. Report copies include job ID, source-relative path/hash, model, duration, attempts, final status, artifact path and explicit blocked adapters. Rejected/interrupted attempts remain in SQLite evidence.

## Proposed implementation order

1. **Approved repository reader** with a reusable path-policy/receipt layer.
2. **Major OS vault reader** using the same path policy plus the folder contract above; no watcher until fixture tests prove exclusions, template rejection and dedupe.
3. **Read-only GitHub inspection** through a narrow repo allowlist and separate least-privilege credential.
4. **Planner/dispatcher contracts** that translate approved brief items only into existing supported task types; unsupported operations remain blocked.
5. **Allowlisted isolated verification runner** with fixed command IDs and denial-first tests.
6. **Local health notification adapter** after the overnight/sleep evidence is complete.
7. Then evaluate read-only Substack handoffs, private asset manifests, Airtable and individual providers. Draft PR creation remains manual/approval-gated and all publishing, messaging, commerce and external writes remain disabled.

No runtime, service, plugin, vault file, credential, external record or queue history was changed during this inventory.
