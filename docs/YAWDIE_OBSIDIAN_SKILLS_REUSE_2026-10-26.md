# Yawdie Obsidian skills reuse record

**Source reviewed:** `MajorDream444/obsidian-skills`

**Pinned revision:** `3ccff5338ea700537839b21900aa5358a0402c98`

**Upstream:** `kepano/obsidian-skills`

**License:** MIT, Copyright (c) 2026 Steph Ango (@kepano)

No source code or full skill text was copied into Yawdie. The attribution is retained because
the report conventions were informed by the upstream `obsidian-markdown` skill.

## Availability evidence

| Component | Available | Installed | Configured | Verified |
|---|---|---|---|---|
| Fork repository | Public GitHub repository at the pinned revision | No local checkout was found in the established project or skill locations | Not applicable | Repository tree, revision and MIT license verified read-only through GitHub |
| `obsidian-markdown` | Skill exists in the fork | Not installed in the discovered Codex, Claude or shared agent skill folders | Not applicable | Instructions read at the pinned revision; frontmatter, tags, internal-link and callout conventions reused in the deterministic report renderer |
| `obsidian-cli` | Skill exists in the fork | The `obsidian` executable is supplied by the Obsidian app, not installed as a Yawdie dependency | Requires an open Obsidian app and an explicitly targeted vault | `obsidian help` succeeded read-only; it warned that the installer is older than the loaded app package |
| Bases / JSON Canvas / Defuddle / Knap | Skills exist in the fork | Not found in installed skill locations | Not configured for Yawdie | Not invoked or verified; no current adapter need |

## Reuse boundary

The background worker continues to use the tested direct filesystem adapter. It does not depend
on Obsidian being open and does not inherit plugin or CLI configuration. The model returns bounded
JSON; the deterministic report renderer applies the relevant Obsidian Markdown conventions, so the
full skill is not copied into every local inference prompt.

If an optional interactive CLI adapter is added later, its allowlist should be limited to exact
vault targeting plus read-only operations on `Yawdie/Context`, `Yawdie/Briefs/Inbox` and
`Yawdie/Reports`, such as exact-path `read`, exact-folder `files` and exact-target metadata. Search
must be constrained to approved folders before it is exposed.

Explicitly denied to any model-facing adapter:

- `eval`, arbitrary `command`, plugin/theme or developer commands;
- delete, move, overwrite, append, prepend, property mutation or history restore;
- active-file defaults, unrestricted vault search or operations without `vault=Major OS`;
- Bases creation, Canvas mutation, web extraction or template generation until separately scoped.

The CLI is therefore reusable for a future operator-facing convenience layer, but it is neither
required nor enabled for Yawdie's queue, inference, context loading or report export.
