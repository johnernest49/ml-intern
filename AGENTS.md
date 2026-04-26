# Codex CLI Compatibility Mission

This repository is being converted into a **Codex CLI compatible agent project**.
That is the main goal for future agents working here.

The existing ML Intern codebase is the source system we are adapting. It is a
Python ML engineering agent with Hugging Face research, docs, datasets, jobs,
sandbox validation, telemetry, SFT export, KPI rollups, a FastAPI backend, and a
React frontend. The compatibility work should make those workflows easier for
Codex CLI to understand, reuse, and operate safely.

## Primary Goal

Make this project first-class for Codex CLI by adding and maintaining:

- clear `AGENTS.md` guidance for future agents;
- Codex-discoverable skills under `coding-agents/.agents/skills`;
- Codex custom subagent definitions under `coding-agents/.codex/agents`;
- lightweight adapters for existing project scripts instead of duplicated logic;
- safe instructions for HF research, sandboxing, training jobs, Hub operations,
  telemetry exports, KPI rollups, and frontend/backend work;

The supported Codex launch surface is `coding-agents/`. Run `cd coding-agents`
before starting Codex so local skills and custom agents are discoverable. Treat
the repository root as source context only unless the user explicitly asks to
move files into the root or change production code.

## What Not To Do

- Do not rewrite the ML Intern runtime just to make it "agent compatible".
- Do not duplicate large scripts or source files inside skills.
- Do not modify `agent/`, `backend/`, `frontend/`, `scripts/`, tests, configs, or
  packaging unless the user explicitly asks for project-source changes.
- Do not embed secrets, tokens, OAuth credentials, or private URLs.
- Do not launch HF Jobs, upload to the Hub, delete repos, change repo visibility,
  or use paid/long-running compute without explicit user approval.
- Do not require other assistant CLIs, custom tool servers, external model
  provider keys, or non-Codex plugins for the default compatibility workflow.

## Current Compatibility Layout

- `coding-agents/AGENTS.md`: operational guide when launching Codex from
  `coding-agents/`.
- `coding-agents/README.md`: overview and usage.
- `coding-agents/.codex/config.toml`: Codex local config stub.
- `coding-agents/.codex/agents/`: custom Codex agents:
  `ml_intern_orchestrator`, `hf_researcher`, `repo_mapper`, `script_adapter`,
  and `verifier`.
- `coding-agents/.agents/skills/`: Codex skills.

Future compatibility work should usually extend this structure, not create a
parallel one.

## Source Project Map

Use the existing project as source of truth:

- `agent/`: Python agent runtime.
- `agent/core/agent_loop.py`: main async agent loop.
- `agent/core/tools.py`: built-in tool registration.
- `agent/tools/`: HF docs, papers, datasets, jobs, sandbox, repo, GitHub, and
  local tools.
- `agent/prompts/`: current behavior rules for ML research, sandbox validation,
  training jobs, and safety.
- `agent/core/session.py`, `agent/core/session_uploader.py`,
  `agent/core/telemetry.py`: session and telemetry plumbing.
- `agent/sft/`: SFT trajectory tagging.
- `scripts/build_sft.py`: source script for SFT export.
- `scripts/build_kpis.py`: source script for KPI rollups.
- `backend/`: FastAPI app.
- `frontend/`: React/Vite web UI.
- `tests/unit/`: regression tests.

When creating Codex skills or adapters, reference these files and delegate to
them rather than copying their internals.

## Conversion Principles

- Codex only for the default compatibility path.
- Preserve the behavior and safety rules already present in ML Intern prompts
  and tools.
- Use progressive disclosure: put concise instructions in `SKILL.md`, and only
  add helper scripts or references when they materially help the agent.
- Keep adapters small: resolve the real repo root, check required environment,
  print the delegated command, pass arguments through unchanged, and return the
  original script exit code.
- Prefer read-only Codex subagents for discovery and verification. Use a focused
  worker only for narrow edits inside the compatibility bundle.
- Keep future agents oriented: explain what the skill/agent is for, when to use
  it, what it must not do, and how to verify it.

## Safety Rules To Preserve

For ML work:

1. Research current papers, docs, and examples before implementation.
2. Validate dataset schema, splits, samples, and format.
3. Validate model existence, tokenizer, size, architecture, and access.
4. Check current HF APIs instead of relying on memory.
5. Use sandbox or small-run validation before expensive jobs.

For HF Jobs and Hub operations:

- The Codex-only baseline is read-only research, repo inspection, metadata
  checks, local validation, and adapter help checks.
- Ask for explicit approval before paid compute, long-running jobs, uploads,
  repo deletion, visibility changes, or broad write operations.
- Require separately configured HF credentials for any Hub write or HF Job; a
  Codex subscription alone is not enough for those operations.
- Never print token values.
- Never silently substitute datasets, models, methods, sequence length, or output
  destination.
- Ensure training outputs persist with Hub pushes or explicit artifact handling.
- Run one pilot job before batch or ablation launches.

## Verification

Recommended local setup:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
```

Compatibility smoke checks:

```bash
cd coding-agents
../.venv/bin/python scripts/check_metadata.py
rg -n 'coding-agents[/]\.agents|u[v]\b|/skills[ ]add|mcp[_]servers' ../coding-agents
../.venv/bin/python .agents/skills/hf-session-sft-export/scripts/build_sft_adapter.py --help
../.venv/bin/python .agents/skills/hf-kpi-rollup/scripts/build_kpis_adapter.py --help
../.venv/bin/python -m pytest ../tests/unit/test_build_sft.py ../tests/unit/test_build_kpis.py ../tests/unit/test_kpis_scheduler.py ../tests/unit/test_user_quotas.py
```

Metadata checks should confirm:

- every `SKILL.md` has valid YAML-style frontmatter with lowercase `name` and a
  useful `description`;
- `coding-agents/.codex/agents/*.toml` parses and includes `name`,
  `description`, and `developer_instructions`;
- skills do not request broad shell access without a deliberate reason;
- compatibility-only work stays inside `coding-agents/` unless the user changes
  scope.

## How Future Agents Should Proceed

1. Read this file first.
2. Launch from `coding-agents/` and read `coding-agents/AGENTS.md` before
   editing the compatibility bundle.
3. Inspect the relevant source project files before drafting skills or adapters.
4. Make the smallest compatibility change that advances Codex CLI usability.
5. Verify adapters, metadata, and affected source-script tests.
6. Report exactly what changed and any remaining gaps.
