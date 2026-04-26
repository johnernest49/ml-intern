---
name: ml-intern-orchestration
description: Decompose ML Intern tasks into safe main-agent and subagent workflows while preserving project scope and context hygiene.
---

# ML Intern Orchestration

Use this skill when a task spans research, codebase exploration, implementation,
or verification in the ML Intern project.

## Ground Rules

- Launch from `coding-agents/`. Treat `..` as the project root.
- Keep compatibility edits inside `coding-agents/` unless the user explicitly
  asks for project source changes.
- Main agent owns the plan, safety decisions, final synthesis, and integration.
- Prefer read-only subagents first. Use workers only for focused edits with a
  narrow write scope.
- Use direct subagents only. Do not ask subagents to spawn nested subagents.
- Never run HF Jobs, upload to Hub, delete repos, or use paid/long-running
  compute without explicit user approval.
- Do not require other assistant CLIs, custom tool servers, external model
  provider keys, or non-Codex plugins for the default workflow.

## Default Flow

1. Restate the task internally as an outcome and constraints.
2. Map required project surfaces: `../agent`, `../scripts`, `../backend`,
   `../frontend`, and tests only as needed.
3. For ML implementation questions, research current papers, docs, examples,
   datasets, and model availability before coding.
4. Use sandbox-first validation for non-trivial training or inference scripts.
5. Verify with the narrowest meaningful commands.
6. Report what changed, evidence, and remaining risks.

## Reliability Rules

- Preserve the requested ML scope: model, dataset, training method, sequence
  length, metrics, and output destination should not change without user
  approval.
- If a tool call or command fails repeatedly for the same reason, stop retrying
  unchanged and pick a different strategy backed by logs or docs.
- Diagnose the actual error before changing implementation. For API/import
  errors, check current docs or examples. For OOM, keep effective batch size
  where possible, enable checkpointing, or move to larger hardware before
  changing the task.
- Record checkpoint summaries after major decisions, edit groups, verification
  passes, and any context-compaction/restore boundary.
- Before declaring completion, verify outputs or tests. If verification cannot
  run, state the concrete blocker and the smallest next check.

## Long Sessions

The main orchestrator should keep a compact task ledger:

- Goal, constraints, and active assumptions.
- Subagents launched, their scope, and their returned evidence.
- Decisions made and why they are final for this task.
- Open risks, blockers, and the next verification step.

Checkpoint after each subagent result, edit group, or verification pass. A
checkpoint should let a resumed or forked session continue without rereading the
whole bundle.

## Subagent Pattern

Use subagents for bounded side work:

- `repo_mapper`: file/test orientation plus source workflow surfaces such as
  tools, sessions, approvals, telemetry, frontend/backend event flow, and tests.
- `hf_researcher`: current HF docs, papers, datasets, models, and examples.
- `script_adapter`: bundle-local wrappers and helper scripts.
- `verifier`: metadata checks, adapter smoke tests, and targeted test runs.

Keep each handoff concrete: include root path, files to inspect or edit, success
criteria, and forbidden actions.
