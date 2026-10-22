# Claude Code — Toolbox Register

**Issue #41 · Claude Code portion only.** This records *this* runtime. It must not be
copied to Cowork or Codex — neither's capabilities can be inferred from mine.

| | |
|---|---|
| Runtime | Claude Code (cloud container, claude.ai/code) |
| Inspected | 2026-10-17 |
| Primary repo / branch | `MajorDream444/Major-OS-AMA-OS--Command` @ `claude/maim-ecosystem-wireframe-xk8swp` |
| Secondary repo | `MajorDream444/major-ai-os` @ `e1dcc1c` (detached, added via `add_repo`) |
| Identity scope | GitHub account active; account email held privately, not recorded here |

---

## 1. The routing fact that governs everything else

**MCP tool calls do not traverse this container's network. Shell commands do.**

Evidence — same session, same moment:

```
shell DNS:  api.vercel.com    NO DNS
            api.stripe.com    NO DNS
            api.airtable.com  NO DNS
            api.resend.com    NO DNS
            google.com        NO DNS
            github.com        resolves
            api.anthropic.com resolves
```

Yet Vercel and Stripe MCP calls succeeded repeatedly in the same session. The MCP
host brokers those requests; my container never dials them.

**Consequences, both directions:**

- ✅ Use the **MCP tool** for every SaaS API. It works even though the host is unresolvable from the shell.
- ❌ Never use `curl` / `Bash` for a SaaS API. It will fail, and the failure says nothing about the service.
- ❌ **Never treat a shell DNS or HTTP result as evidence about the public internet.** This is the single most expensive mistake made this sprint — see §5.1.

---

## 2. Instructions in force

| Path | Bytes | Applies to |
|---|---|---|
| `Major-OS-AMA-OS--Command/AGENTS.md` | 1714 | agent roster, daily loop, Graphify rules |
| `major-ai-os/CLAUDE.md` | 3218 | canonical repo instructions |
| user-level `CLAUDE.md` | — | **absent** |

**Graphify (per AGENTS.md):** `graphify-out/GRAPH_REPORT.md` exists but is **stale and
irrelevant to MAIM** — built from commit `943bc572`, 252 nodes covering Command Center
cockpit JS (`saveState()`, `pushActivity()`, `renderAll()`), **zero MAIM nodes**. Did not
rely on it; did not run `graphify update .` (AGENTS.md requires approval). `wiki/index.md`
absent.

---

## 3. Skills, commands, plugins

| Location | Contents | State |
|---|---|---|
| `/root/.claude/skills/` | `session-start-hook`, `synced` | listed |
| `/root/.claude/commands/` | — | **absent** |
| `/root/.claude/plugins/` | — | **absent** |
| `Command/.claude/` | `ecc-tools.json`, `homunculus`, `identity.json`, `skills/Major-OS-AMA-OS--Command` | listed |
| `major-ai-os/.claude/commands/` | `add-new-experiment-landing-page.md`, `feature-development.md` | listed, **never invoked** |
| `major-ai-os/.claude/skills/` | `Major-AI-OS` | listed |

Host-provided skills (`artifact-design`, `artifact-capabilities`, `code-review`,
`pdf`, `docx`, `xlsx`, `webapp-testing`, etc.) are surfaced by the harness, not by these
directories. Invoked this session: **`artifact-design`** only.

**Do not invent slash commands.** The only repo-defined ones are the two markdown files
above; neither has a verified trigger in this runtime.

---

## 4. MCP connections — observed state

Connection state is **volatile**; servers dropped and reconnected repeatedly this session.
"Listed" ≠ "authenticated" ≠ "write tested."

| Server | Read tested | Write tested | Notes |
|---|---|---|---|
| **Stripe** | ✅ products, prices, webhooks, sessions | ✅ test-mode only | Two contexts: `livemode:false` and `livemode:true`. **Always call `list_available_accounts_or_orgs` first.** No live write performed. |
| **Vercel** | ✅ projects, domains, deployments, env metadata | ✅ protection-bypass rotate | Env **values** return empty for `sensitive`/`secret` type — metadata only |
| **GitHub** | ✅ issues, PRs, diffs, commits | ✅ issue comments, comment edit | Scope: the two repos above |
| **Claude_Code_Remote** | ✅ `add_repo` | ✅ repo attach | **This is the route to add a repository.** |
| Airtable | listed | ❌ | **UNVERIFIED** — never called |
| Resend | listed | ❌ | **UNVERIFIED** — never called |
| Google Calendar | listed | ❌ | **UNVERIFIED** |
| Cloudflare | partial | ❌ | **No DNS/zone tools** — only D1, KV, R2, Workers, Hyperdrive, docs search. Cannot read DNS records. |
| Fathom, Notion, Slack, Figma, Canva, Shopify, Supabase, Linear, v0, HeyGen | listed | ❌ | **UNVERIFIED** |
| HyperFrames (HeyGen) | — | — | **requires auth**, cannot be completed from this session |

**Airtable and Resend are launch-critical and completely untested from this runtime.** No
read receipt exists for either. Any claim that order persistence or email delivery works is
unsupported by my evidence.

---

## 5. Tool-selection failures and corrected routes

### 5.1 🔴 Shell DNS used as evidence about the internet

**What happened.** Queried `majoraimindset.com` via shell resolver, got NXDOMAIN across
every record type, and reported the domain was not live — contradicting the founder's own
Vercel evidence.

**Why it was wrong.** The container resolver is allowlisted. `google.com` and
`cloudflare.com` return NXDOMAIN here too. The result was an artifact of my sandbox.

**Cost.** A false blocker in a launch gate, asserted confidently, requiring public retraction.

**Correct route:**
| Need | Use |
|---|---|
| Is a domain attached / verified? | `mcp__Vercel__list_project_domains` |
| Is production deployed, at what commit? | `mcp__Vercel__list_deployments` (`target: production`) |
| Is a domain registered? | `mcp__Vercel__get_domain_availability` |
| Does a site serve content publicly? | **Cannot be answered here** — needs an unrestricted network |

### 5.2 🔴 Credential posted in a GitHub comment

Posted a webhook URL containing a Vercel protection-bypass token while reporting on
credential hygiene. **Redaction alone does not close this — GitHub retains edit history.**
Remediated by rotation via `update_project_protection_bypass` (`revoke` + `regenerate`).

**Rule adopted:** credentials by **name or env-ID only** (`WmVKYfiOn7sW6Ife`), never value;
endpoints by `we_…` ID and host, never full URL.

### 5.3 Recommended a platform feature that does not exist

Advised exempting `/api/stripe-webhook` from Deployment Protection. **Vercel has no
path-scoped exception.** Found only after checking `search_vercel_documentation` — which
also showed Vercel documents the query-parameter bypass as its *worked Stripe example*, so
the implementation under review was correct and my criticism was misdirected.

**Rule:** search the platform's own docs **before** recommending a platform capability.

### 5.4 Trusted a "build passed" claim instead of running it

PR #40 stated the static build passed. Running `python3 maim/build.py` produced
`SyntaxError: f-string expression part cannot include a backslash` — a PEP 701 issue making
it Python-3.12-only, with the build Python **unpinned**.

**Rule:** run the build and the test suite. A green claim from another agent is a hypothesis.

### 5.5 Wrong MCP parameter name

`PostWebhookEndpointsWebhookEndpoint` rejected `webhook_endpoint`; the path param is `id`.

**Rule:** on schema error call `stripe_api_details` rather than guessing a second time.

### 5.6 Searched for a repo-access tool under guessed names

`ToolSearch "select:mcp__claude-code-remote__list_repos"` returned nothing; the working
route was `mcp__Claude_Code_Remote__add_repo`. Three rounds of "I lack repo access" were
avoidable.

**Rule:** to reach a repository, call `add_repo` first.

---

## 6. Execution limits

- **Egress:** allowlisted. Only `github.com` and `api.anthropic.com` resolve. No SaaS API, no `*.vercel.app`, no public web.
- **No browser-driven checkout.** Chromium + Playwright 1.56.1 are installed at `/opt/pw-browsers`, but with no egress they cannot reach a hosted checkout page. **Hosted Stripe Checkout cannot be completed from this runtime** — it needs a human on an open network.
- **No `vercel` or `stripe` CLI.** Only the MCP servers.
- **Secret env values unreadable.** Vercel returns `""` for `sensitive`/`secret` types — I can prove a variable *exists*, never what it is set to. This is why I can no longer independently verify the production commerce hold (#37).
- Available: `git` 2.43.0 · `gh` 2.89.0 · `node` 22.22.0 · `npm` 10.9.4 · `python3` **3.11.17** · `jq` 1.7 · `rg` 14.1.0 · `docker` 29.8.2 · `gcloud` 570.0.0 · `gsutil` 5.37 · `bq`
- **Python 3.11.17 is the local build interpreter** — directly relevant to §5.4.

---

## 7. Startup routing for this runtime

1. `add_repo` → clone → `register_repo_root` before claiming repository access.
2. SaaS state → **MCP tool**. Never `curl`.
3. Any DNS/HTTP result from the shell is about *this container*, never the internet.
4. Stripe: `list_available_accounts_or_orgs` first; confirm `livemode` before any write.
5. Platform capability questions → that platform's docs tool before advising.
6. Verify build/test claims by executing them.
7. Credentials by name/ID only. Exposure is closed by rotation, not redaction.
8. Mark Airtable, Resend, Calendar, Fathom **UNVERIFIED** until a read receipt exists.
