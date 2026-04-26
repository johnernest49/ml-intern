# ML Intern Coding Agents

This directory is a Codex-first compatibility bundle for the ML Intern project.
Launch Codex from this directory. This is the supported discovery surface for
local `.agents/skills` and `.codex/agents` definitions. Treat `..` as the real
project root and source context.

## Scope

- Keep compatibility bundle changes inside `coding-agents/`.
- Do not edit `../agent`, `../backend`, `../frontend`, `../scripts`, tests,
  project configs, or packaging files unless the user explicitly changes scope.
- Use the existing project workflows as source of truth. Prefer wrappers,
  instructions, and references over duplicated runtime logic.
- Never embed tokens, secrets, user credentials, OAuth data, or Hub write tokens
  in this directory.
- Do not require other assistant CLIs, custom tool servers, external model
  provider keys, or non-Codex plugins for the default path.

## Orchestration Contract

The main agent owns task framing, decomposition, final synthesis, safety
decisions, and integration choices, especially during long sessions. Subagents
should do bounded direct side work:

- Use read-only subagents first for codebase mapping, docs lookup, HF research,
  and verification planning.
- Use one focused worker only when edits inside `coding-agents/` are needed.
- Keep subagent tasks concrete and short. Ask for evidence: file paths,
  commands, outputs, and remaining risks.
- Main thread keeps a task ledger, integrates results after each subagent
  return, and makes final calls.
- Use direct subagents only; do not ask subagents to spawn nested subagents.
- Checkpoint long sessions after each major decision, completed edit group, or
  verification pass so a resumed agent can continue without rediscovery.

Useful Codex custom agents in this bundle:

- `ml_intern_orchestrator`: parent planning and synthesis.
- `repo_mapper`: read-only map of `../agent`, `../backend`, `../frontend`,
  `../scripts`, and tests.
- `hf_researcher`: read-only Hugging Face papers, docs, datasets, models, and
  examples research.
- `script_adapter`: bundle-local adapter and skill helper work.
- `verifier`: read-only or temporary-output verification.

Useful Codex skills in this bundle include:

- `ml-intern-runtime-workflow`: sessions, approvals, telemetry, event names,
  cleanup, compaction, cancellation, config, and source model/auth behavior.
- `ml-intern-tool-surface`: source tool families and safe Codex compatibility
  mapping without copying runtime implementations.
- `ml-intern-frontend-backend`: FastAPI, React/Vite, SSE, quotas, approvals,
  frontend state, and likely web checks.

## Safety Rules

- The Codex-only baseline is read-only HF research, repo inspection, local
  validation, adapter help checks, and local tests.
- Do not run Hugging Face Jobs, upload to Hub, delete repos, change repo
  visibility, or use paid or long-running compute without explicit user
  approval.
- Hub writes and HF Jobs require separately configured HF credentials; a Codex
  subscription alone does not grant those permissions.
- For HF token checks, accept environment variables only. Do not print token
  values.
- For training work, verify docs/examples and dataset schema before code or job
  submission.
- For non-trivial ML scripts, validate in a sandbox or local dry run before
  launching expensive work.
- For destructive commands, repo deletion, force pushes, or broad filesystem
  rewrites, stop and ask the user.

## Source Runtime Vs Codex Bundle

The source ML Intern runtime may use HF credentials, web authentication,
provider routing, optional external tool servers, session uploads, and frontend
approval flows. Those are source-runtime facts, not requirements for the
Codex-only compatibility path.

The default Codex bundle must remain usable without HF tokens, paid compute,
external model provider keys, web login state, or optional tool-server setup.
When documenting source behavior, distinguish clearly between read-only/local
Codex checks and real source operations that need credentials, entitlement, or
explicit approval.

## Project Orientation

The parent project is a Python ML agent using LiteLLM orchestration, Hugging
Face tools, sandbox and job tools, telemetry, SFT export, KPI rollups, a FastAPI
backend, and a React frontend.

Important source locations from the project root:

- `../agent/core/agent_loop.py`: primary agent loop.
- `../agent/core/tools.py`: built-in tool registration.
- `../agent/tools/`: HF docs, papers, datasets, jobs, sandbox, repo, and local
  tool implementations.
- `../agent/core/session.py` and `../agent/core/telemetry.py`: session
  lifecycle, redacted saves, uploads, and heartbeat persistence.
- `../agent/prompts/system_prompt_v3.yaml`: current ML workflow guidance.
- `../scripts/build_sft.py`: raw session trajectory to SFT export.
- `../scripts/build_kpis.py`: hourly KPI rollup.
- `../backend/`: FastAPI server.
- `../frontend/`: React/Vite client.
- `../tests/unit/`: focused unit tests.

## Verification Defaults

Before reporting success for this bundle, prefer:

```bash
../.venv/bin/python scripts/check_metadata.py
../.venv/bin/python .agents/skills/hf-session-sft-export/scripts/build_sft_adapter.py --help
../.venv/bin/python .agents/skills/hf-kpi-rollup/scripts/build_kpis_adapter.py --help
../.venv/bin/python -m pytest ../tests/unit/test_build_sft.py ../tests/unit/test_build_kpis.py ../tests/unit/test_kpis_scheduler.py ../tests/unit/test_user_quotas.py
```

Codex-only audit checks:

```bash
../.venv/bin/python scripts/check_metadata.py
rg -n 'coding-agents[/]\.agents|u[v]\b|/skills[ ]add|mcp[_]servers' ../coding-agents
```

Also check that only the compatibility surface changed unless the user expanded
scope.
