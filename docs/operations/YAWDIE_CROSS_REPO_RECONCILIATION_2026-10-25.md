# Major Prime OS / AMA Command reconciliation — 25 October 2026
Status: review handover; no activation or migration authority. Founder decisions in this document supersede conflicting older architecture plans. Runtime claims remain evidence-bound.

## Verified scope
Read all 18 files (the complete recursive branch tree) at major-prime-os commit 6d467271c2510057bb76d29b6cbf62c12d371c4c. GitHub compare confirms two ahead, zero behind main b13d770e237493281475f0d5af50db448e5af337. Original branch claude/setup-repo-structure-7BKxl remains unmerged and unchanged by this handover.
Compared against AMA Command main 628764b8b9b084ece6f4788d08b53a82cbce36e9: boundaries, architecture, registries, repo map, Yawdie charter/runtime handoff, worker source, external-system contract and daily brief protocol. Graph report was inspected but is stale (built from 943bc572, May 11); it is not current runtime evidence.
Both major-prime-os and Major-OS-AMA-OS--Command have public visibility. Candidate private Command Center is a founder direction, not present repository privacy or deployed access control.

## Ownership and architecture
| Layer | Owner / responsibility |
|---|---|
| Major Prime OS | Candidate private ecosystem Command Center; cross-umbrella monitoring, priorities, evidence and founder decision queue |
| Yawdie H01 | One Chief of Staff identity and lead monitor; ecosystem scope; existing HAMAL seat retained |
| AMA Solutions | HAMAL operational agent organization; service/client delivery; Foundry OS |
| Foundry OS under AMA | EV/Mobility, Gold/Mining, Agriculture, Fisheries, Sports |
| MAIM | Academy, Design Studio, Spark Lab, books, 52 in 52 |
| Major Dream Williams | Personal brand, lifestyle ventures, Marine Foundation-related impact work |
| Existing AMA Command | Preserve operator UI, contracts, records and worker; proposed AMA operational console/adaptor to Prime rather than competing ecosystem authority |
| HAMAL_MOB_PLAYBOOKS | Existing doctrine/SOP source, referenced rather than copied |
| Execution repositories | Existing tool adapters and domain systems; no second control plane or credential pool |

Prime observes and coordinates across three umbrellas; HAMAL remains under AMA. Existing repo maps that make AMA Command the sole ecosystem entrypoint require a staged documentation update. Product ownership is distinct from where reusable code currently resides. No repository move, asset transfer or renaming is performed here.

## Complete branch file audit
| File | Finding / disposition |
|---|---|
| .gitignore | Preserves basic exclusions; add scoped env variants, private exports, generated contact lists and runtime databases in a later hardening PR; ignore rules cannot remove previously committed secrets. |
| .mcp.json | Duplicates Claude template endpoint/auth. HTTP REST service is not proof of MCP protocol compatibility; require initialize/tools/list/tool-call evidence. Keep inert pending validation. |
| AGENTS/scout-medspa-buyer/SKILL.md | Preserve original skill. Specialized Scout workflow, not new executive agent. Missing stable ID, source receipts, geography/eligibility, dedupe, acceptance and approval boundary. |
| AGENTS/state-keeper/PROMPT.md | Preserve original prompt. Useful session snapshot duty; map to H02 memory function. Snapshot is derived state, not proof of uptime. Add timestamps/source references via additive contract. |
| CONFIG/claude.json.template | Repeats .mcp.json and hardcoded local placeholder. Project key/CLI compatibility unverified; allowedTools empty differs from historical commit claim. Never copy over founder configuration. |
| CONFIG/env.example | Declares keys but runner does not source it; TELEGRAM_CHAT_ID absent; URL/key hardcoded elsewhere. Airtable/Notion variables have no corresponding implementation here. |
| CONFIG/openclaw.json.template | Has enabled:true and schedule without verified installed-version schema. Do not apply. Overlaps OS cron; potential double scheduling. No local config inspected or changed. |
| CRON/scout-cron.md | Installation recipe only. Repeated one-liner appends duplicate jobs; shell RC environment inheritance claim is unreliable for cron; timezone unspecified; executable bit needs attention (tree mode 100644). |
| DOCS/architecture.md | Describes an intended pipeline, not working adapters. No Yawdie or three-umbrella boundary; revise around founder ownership. |
| DOCS/setup.md | cp template to ~/.claude.json overwrites existing config; reject that recipe. Docker command unpinned, port published without explicit loopback bind, no service dependency/MCP verification. Replace with reviewable backup/diff/merge proposal only. |
| MCP/firecrawl.md | Conflates REST scrape endpoints with HTTP MCP. Health endpoint alone cannot validate tool transport or auth. Host-local claim unverified. |
| PROJECT_BRIEF.md | Narrow autonomous revenue brief conflicts with ecosystem monitoring scope; preserve as historical initiative, add current charter. |
| README.md | No actual UI or Chief of Staff implementation; stack list is not live integration evidence. Replace live implications with readiness labels. |
| SCRIPTS/firecrawl-curl.sh | Manual REST helper; hardcoded URL/key, JSON interpolation unsafe for quoted input, no timeout or fail-on-HTTP policy; pipeline can mask curl error. Preserve pending hardening. |
| SCRIPTS/scout-runner.sh | Does NOT execute Claude scouting. scrape_url is never called; no discovery/extraction/scoring/Airtable write; command is printed into log only. Offline path invokes send_telegram before definition, causing command-not-found under set -e. Success notification implies trigger without actual dispatch; notification errors swallowed. No lock, job ID, timeout, dedupe, budget or durable outcome receipt. |
| STATE/STATE_SNAPSHOT.md | Historical host claims lack fresh receipts. “Scout loop live — awaiting cron” internally contradictory. Config-patch recipe replaces skills object; do not execute. Preserve history and append evidence-based correction. |
| WORKFLOWS/bwyh-lead-flow.md | Proposed pipeline only; outbound messages and follow-ups require separate founder approval. BWYH owner/offer scope remains unresolved; medspa workflow is not all of Prime OS. |
| WORKFLOWS/scout-daily.md | Ten-target process specification, no executor. Add scoped inputs, sources, qualification checks, dedupe and draft-only output before activation. |

## Duplication and consolidation
| Overlap | Evidence | Safe treatment |
|---|---|---|
| Scout | Prime medspa skill; AMA A001 Scout; H07 research / H09 sales responsibilities | Keep A001 legacy identifier as alias/workflow and medspa specialization; H07 research produces candidate packets, H09 receives qualified sales drafts. Do not invent equivalence of all seats. |
| State Keeper | Prime prompt; AMA H02 memory; A010 meeting summaries | State Keeper is H02 function; A010 is legacy workflow alias. Preserve prompt and snapshot provenance. |
| Chief of Staff / monitoring | Existing H01 charter, A004 Ops Watcher, daily brief protocols; Prime proposed command role | One H01 Yawdie. A004 monitoring workflow reports to H01; Prime shows evidence rather than introducing a rival executive. |
| Rosters | A001–A010 mock UI vs H01–H12 worker roster | Explicit alias map needed. Ten mock rows and twelve seats are different representations, not 22 active agents. Only H06 local content handler exists in inspected worker. |
| Schedules | Prime cron 07:00 plus OpenClaw template schedule; existing worker 08:00/19:00 Asia/Makassar tick | Choose one host supervisor per job after approval; job dedupe/lease prevents duplicate execution. No scheduler installed here. |
| Firecrawl / Telegram | Prime helpers and config; existing repo map points to hanzo-lux-codex-repo tooling | Adapter inventory first; share validated adapters rather than copy credentials. Current execution tree inspected, but historic map coverage is not a live test. |
| Config / operational state | .mcp.json, Claude template, env template, hardcoded script values; snapshots, SQLite spool, UI localStorage, Airtable intent | One configuration contract with local secret injection; one operational record authority per type; derived views carry source/time. No local config replacement. |
| Approvals / UI | AMA artifact/decision queues and Prime intended UI | Reuse contracts and evaluated UI components; keep founder approval authoritative. Local browser decisions do not confer remote execution authorization. |

## Integration verification register
No access to the founder's actual OpenClaw host/session was available. This audit verifies repository evidence; it does not classify inaccessible local services as down. A connected chat app is not proof a repository runner has credentials.

| Component | Current evidence | Verdict / required proof |
|---|---|---|
| Cron | Recipe; snapshot says not installed; Prime Actions API has zero runs | HOLD live claim. Need redacted host crontab/supervisor inventory, explicit timezone, one schedule, timestamped successful job receipt; Actions absence says nothing about host cron. |
| OpenClaw | Template and historical gateway assertion; AMA contract says execution not implemented in mock UI | UNVERIFIED host. Need installed version, redacted config validation, read-only gateway health, skills loading and bounded dry-run receipt. No overwrite. |
| Firecrawl | REST helper, hardcoded loopback URL, MCP declarations | UNVERIFIED service and protocol. Need host health/auth, controlled scrape result and separate MCP initialize/tools/list/call proof against installed version. |
| Telegram | Conditional send implementation; missing chat ID in env example; historical live assertion | UNVERIFIED delivery. Need read-only identity/config evidence; delivery test only under separately scoped messaging approval; retain receipt and distinguish operational notification from prospect outreach. |
| WhatsApp | Historical link claim and known outbound formatting issue; no adapter in branch | HOLD outbound. Need current linked session and adapter evidence, then separately approved controlled delivery test. |
| Airtable | Key placeholder and architecture arrow; runner has no Airtable code; existing worker explicitly lacks adapter | NOT IMPLEMENTED in these runner paths. Need approved base/table schema, scoped adapter, read proof and separately scoped synthetic write/readback/cleanup test before “connected pipeline.” |
| Yawdie worker | Standard-library spool, leases/retries, local Ollama generation, planned slots and brief ticks in AMA repo | Source implementation exists; historical mocked tests are not live inference, overnight supervision or publication evidence. Keep its work; do not replace with placeholder runner. |

Host verification packet must include component/version, host alias (no credentials), checked_at, command/test, redacted result, source SHA, job ID, last success/failure and expiry. Default operational health freshness: 24 hours; after expiry show STALE, never silently green.

## Yawdie Chief of Staff specification
Identity: H01 Yawdie; aliases Yawds/Yadi retained for search. Founder Major Dream Williams is final authority. Ecosystem monitoring scope does not transfer HAMAL out of AMA.

Monitoring: maintain project/repository registry for MAIM, AMA and Major Dream; compare branch/PR/deployment status separately; track dependencies, failed/overdue work, fulfillment gates, integration health, budgets and evidence freshness. Read least-privilege metadata by default. Never infer delivery from merged code or activity from a named agent.

Delegation: issue bounded mission with mission_id, ecosystem/workspace, owner_agent_id, executor, source_refs and pinned commit, allowed_actions, denied_actions, acceptance checks, deadline/timezone, budget/billing route, dependency state and artifact target. Require acknowledgement before RUNNING. H02 owns memory/State Keeper; H07 research includes Scout; H04 engineering/release; H05 commerce; H06 creative; H09 relationships; H12 verification. Other existing H seats retained. No new autonomous agents are activated by this specification.

Lifecycle: PROPOSED → APPROVED_SCOPE → ASSIGNED → ACKNOWLEDGED → RUNNING → REVIEW → VERIFIED_DONE; WAITING/BLOCKED/FAILED/CANCELLED are explicit alternatives. Missing acknowledgement remains ASSIGNED. Completion requires acceptance evidence and actual artifact. Every event records timestamp, actor, source SHA and result; retries retain mission ID and new attempt ID.

Escalation:
- Immediate: suspected credential/private-data exposure, unauthorized send/deploy, wrong account/workspace, unapproved spend. Stop affected executor, preserve redacted evidence, request founder decision.
- High: failed checkout/fulfillment or critical dependency, repeated bounded failure, conflicting ownership; show blocker and bounded recovery proposal.
- Routine: stale telemetry, missed acknowledgement or deadline; flag in next brief. Proposed defaults: acknowledgement due within 4 business hours; overdue at recorded task deadline. Founder may tune.
- No retry may bypass an approval gate or silently switch billing/provider.

Founder approvals required: merging this branch; control-plane deployment; local OpenClaw/config/scheduler activation; autonomous outreach, publishing or external sends; new paid API budgets; production/data migration; irreversible deletion; repo visibility change. Approval record identifies exact action, target/account, source SHA/artifact version, budget, expiry and rollback. A changed artifact or expired scope requires re-review. Manual UI “approve” alone is not permission for a worker without an enforceable adapter contract.

Daily report: proposed 08:00 Asia/Makassar briefing, 19:00 close, not scheduled by this audit. Show (1) verified accomplishments with receipts, (2) planned/unacknowledged work, (3) three priority actions, (4) blockers/owner/deadline, (5) founder decisions with concrete options and consequences, (6) integration freshness, (7) spend/retries/failures, (8) Scout output and State Keeper snapshot links. Report “no verified execution” when appropriate; planned placements never count as publications. Keep private business/contact data out of public reports.

## Foundry Sports inventory
GitHub repository search for owner + sports returned FOUNDRY-SPORTS; foundry search additionally returned HAMAL-Foundry-OS, private HAMAL-Foundry-OS-Qatar and AFRICAN-VENTURE-FOUNDRY. Search results are not a complete Drive/local asset inventory.
- FOUNDRY-SPORTS main 4f21faf0fc024fc08f09d0e2541cdc2cea193ac7: one discovery README; no production implementation.
- discovery/prototype-v1 at 5954ee9f3c83c9de4921871fb36b36e25493850d: README; docs/COWORK-SPORTS-SPRINT-2.md; docs/GOOGLE-AI-STUDIO-SPORTS-HANDOFF.md; docs/OBED-SPORTS-FIELD-BRIEF.md; prototype/README.md; prototype/index.html; tests/workflow.test.cjs.
- Draft PR https://github.com/MajorDream444/FOUNDRY-SPORTS/pull/1 is open, unmerged. Describes synthetic Prepare → Deliver → Build prototype and seven passing Node test groups; those are author-reported, not re-run here. Browser/mobile/accessibility/visual approval remain incomplete. No live AI/authentication/institutional authority/ownership effect.
- HAMAL-Foundry-OS tree includes Qatar needs/opportunity landscape, workspace charter, Technical Reference Guide, canonical truth, chat context, capability/decision registers and source policy. Related context; do not duplicate it into Sports or imply its documents are a running product.
- Private Qatar repo existence verified; its contents and external asset stores were not audited here. AFRICAN-VENTURE-FOUNDRY is listed with size zero; no implementation claim.
Register Sports as AMA → Foundry → Sports. Link existing assets/PR; no new sports build or merge authorized.

## Safe PR / merge sequence
1. Publish this additive documentation handover on independent review branches in both repositories. Original source branch and all Scout/State Keeper files remain untouched.
2. Privacy decision: founder approves converting candidate repo to private or another existing private home; audit history/access and remove secrets/private operational data from proposed public artifacts. Do not assume visibility change erases historical exposure.
3. Architecture PR from pinned source: add founder ownership map, H01 charter, legacy-ID mapping and evidence statuses; retain original work/history. Update both repo entrypoints together; no relocation of runtime yet.
4. Separate runner-hardening PR: real scoped dispatch or explicitly labelled healthcheck-only behavior; function ordering, deadlines, lock/dedupe, JSON-safe payloads, secret loading, truthful exit/report semantics and no outbound defaults. Test offline health, missing dependencies, duplicate runs, malformed inputs, failed dispatch and denied outbound. Validate installed CLI and OpenClaw/MCP schemas rather than guessing.
5. Host evidence review and approved controlled smoke test. Backup/diff config proposal only; no overwrite, enabled agent or cron installation without separate approval.
6. Separate founder approval for merge at reviewed SHA. Recheck divergence, diff and checks first; no blanket merge. Runtime/scheduler/outreach activation is another gate after merge and is off by default.
Rollback: documentation branches can close without merge; runtime later must support disable/pause and retained events; restore config only from approved backup. No destructive migration proposed.

## Private Command Center MVP proposal
Reuse the existing dashboard/contracts after review; Prime initially aggregates read-only evidence from existing systems. No deployment in this task.
Views: Today/Top 3; MAIM/AMA/Major Dream ownership; tasks with acknowledgements; Needs Major decisions; integration evidence/freshness; Scout packets; State Keeper history; Foundry verticals with Sports asset links.
Minimal records: system, project, agent/alias, mission, event/evidence, decision and integration. All include workspace, source ref/SHA, status, verified_at and sensitivity; dedupe stable mission/event IDs.
Private access must be enforced server-side with founder-only authentication/authorization, no anonymous data/API, no secret in browser bundles, no public contact/financial records. localStorage is not the durable operational truth. Begin with synthetic/redacted fixtures and manual evidence imports; live read adapters are separately reviewed.
Acceptance: every status has provenance and freshness; simulated vs observed clearly distinguished; all three umbrellas and five Foundry verticals map correctly; approval cannot cause a send/deploy; no network writes in fixture mode; no loss of Scout/State Keeper history; restart/re-import dedupe; unauthorized access fails. UI polish follows these checks.

## GO / HOLD
| Work | Decision | Release condition |
|---|---|---|
| Founder ownership and H01 specification | GO as documented direction | Preserve implementation-status distinction |
| Scout + State Keeper preservation | GO | Original branch untouched; additive mapping only |
| Cross-repo handover / review branches | GO | Documentation only; no private payloads |
| Private MVP design / synthetic review | GO proposal | No deployed control plane |
| Merge original branch | HOLD | Reconciled architecture, hardened runner, reviewed checks and separate founder approval |
| Claim Scout executes daily | HOLD | Actual dispatch + qualified output + schedule receipt |
| Claim any listed integration live | HOLD | Component-specific fresh host/account evidence |
| Apply OpenClaw or Claude templates | HOLD | Version/schema review, backup/diff and separate approval |
| Private operational storage in current repos | HOLD | Both are public; approved privacy/access solution first |
| New control-plane deployment | HOLD | Separate founder approval and private-access acceptance |
| Autonomous outreach / follow-up / publication | HOLD | Separate scoped approval and tested adapters |
| Foundry Sports production claim / merge | HOLD | Review existing draft PR; remaining UI/accessibility checks; separate release decision |

## Next operator handover
Read this document, the pinned original branch and existing Yawdie charter before coding. First return a proposed alias/ownership diff and runner acceptance checklist. Do not copy local templates, install cron, send messages, deploy, merge or replace the existing worker. Host-only integration facts remain UNVERIFIED until redacted receipts arrive.
