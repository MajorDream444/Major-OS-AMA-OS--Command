# Interpretable Context Methodology — HAMAL / Major OS

## Purpose

This document locks the HAMAL / Major OS decision to use folders and Markdown files as the primary context infrastructure for skills, agents, playbooks, and operating memory.

We are not building a maze of prompts.
We are not depending only on chat history.
We are not turning every process into a complex framework before it is understood.

We are building interpretable context:

```text
folders + markdown + decision chains + agent-readable maps
```

## Core Thesis

A skill is not just a prompt.

A skill is a structured context package that an AI agent can navigate.

The package should include:

- the goal
- the voice
- the constraints
- the assumptions
- the decision chain
- the workflow
- the inputs
- the outputs
- the examples
- the validation rules
- the handoff path

## Why This Matters

Most AI work dies inside chat threads.

A good conversation creates insight, but if that insight stays trapped inside the chat, the system cannot reuse it.

HAMAL converts successful conversations into durable operating assets.

```text
Dialogue
→ decisions
→ markdown files
→ reusable skill
→ playbook
→ workflow
→ agent execution
```

## The Three-Layer Model

### Layer 1 — Dialogue

This is where the user and AI work through the task manually.

Purpose:

- discover what matters
- expose assumptions
- test tone
- refine workflow
- reveal hidden constraints

Layer 1 is not wasted time.
It is where the decision chain is born.

### Layer 2 — Structured Context

This is where the successful dialogue becomes markdown infrastructure.

The system extracts:

- goals
- constraints
- patterns
- decision rules
- examples
- preferred outputs
- failure modes

Then it stores them in files like:

```text
voice.md
tone.md
process.md
pillars.md
examples.md
validation.md
handoff.md
```

### Layer 3 — Automated Execution

This is where agents use the folder instead of requiring the full conversation again.

A simple instruction becomes enough:

```text
Use the scriptwriting skill and produce a 60-second reel script.
```

The agent reads the folder map, loads the right context files, executes the workflow, and saves the output.

## HAMAL Skill Folder Standard

Every serious skill should follow this pattern:

```text
/skill_name/
├── README.md
├── claude.md
├── codex.md
├── voice.md
├── tone.md
├── context.md
├── pillars.md
├── process.md
├── decision_chain.md
├── inputs.md
├── outputs.md
├── examples.md
├── validation.md
├── handoff.md
├── /research/
├── /templates/
├── /outputs/
└── /archive/
```

## Required File Roles

### README.md

Human overview.

Explains:

- what the skill does
- who it is for
- when to use it
- when not to use it
- expected outputs

### claude.md

Agent map for Claude-style agents.

Explains:

- which files to read first
- what sequence to follow
- what output to create
- what not to invent

### codex.md

Agent map for Codex / execution agents.

Explains:

- file paths
- scripts
- expected commands
- validation steps
- output locations

### voice.md

Defines how the output should sound.

Includes:

- communication style
- rhythm
- phrases to use
- phrases to avoid
- teaching philosophy
- examples of good voice

### tone.md

Defines emotional temperature.

Examples:

- direct but not harsh
- premium but not corporate
- clear but not boring
- powerful but not hype-heavy

### context.md

Defines background information the agent must know before acting.

Includes:

- project context
- audience context
- business context
- constraints
- definitions

### pillars.md

Defines the principles behind the skill.

The agent should use these as decision rules.

### process.md

Defines the workflow step by step.

The agent follows this before producing output.

### decision_chain.md

Captures why the process works.

This is the most important file for skill evolution.

It should include:

- what decisions were made
- why they were made
- what alternatives were rejected
- what constraints matter
- what assumptions are active

### inputs.md

Defines what the user or system must provide.

### outputs.md

Defines what the skill must produce.

### examples.md

Stores good examples, bad examples, and before/after samples.

### validation.md

Defines how to judge whether the output worked.

### handoff.md

Defines what the next agent, tool, or workflow should do after this skill runs.

## Skill Creation Workflow

Use this process when turning a conversation into a skill:

```text
1. Identify the successful dialogue
2. Extract the goal
3. Extract constraints
4. Extract assumptions
5. Extract model decisions that worked
6. Extract user corrections
7. Convert the pattern into markdown files
8. Create the skill folder
9. Add examples
10. Add validation rules
11. Add handoff rules
12. Test the skill on a new input
13. Update decision_chain.md with lessons
```

## Dialogue Extraction Checklist

When reviewing a chat, extract:

```yaml
primary_goal:
secondary_goal:
audience:
context:
constraints:
voice_rules:
tone_rules:
examples_used:
model_decisions_that_worked:
model_decisions_rejected:
assumptions:
required_inputs:
expected_outputs:
validation_rules:
next_agent_handoff:
```

## Skill Is Not Enough

A skill becomes valuable only when it connects to a playbook.

```text
Skill = capability
Playbook = sequence
Workflow = execution
System = repeatable business result
```

Example:

```text
voice.md + process.md + templates.md
= scriptwriting skill

scriptwriting skill + research skill + video direction skill + distribution skill
= media production playbook
```

## Folder Context Rule

Agents should not freestyle when a folder map exists.

Before producing output, the agent should read:

```text
README.md
claude.md or codex.md
context.md
process.md
validation.md
```

Then it may use other files as needed.

## Graphify Rule

When Graphify is available, every skill folder should eventually be graphified so the system can understand relationships between:

- skills
- playbooks
- agents
- tools
- outputs
- decisions
- revenue systems

## HAMAL Operating Rule

Do not create complexity before context.

First:

```text
folders + markdown + decision chains
```

Then:

```text
automation + MCPs + APIs + scripts
```

The Markdown folder system is the foundation.
Everything else plugs into it.
