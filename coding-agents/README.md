# Coding Agents Bundle

This folder adds Codex-only instructions, custom agents, and reusable skills for
the ML Intern project without changing the production runtime.

Start Codex from this directory:

```bash
cd coding-agents
codex
```

From here, `..` is the actual ML Intern project root. This is the supported
launch surface; starting Codex from the repository root is source-context only
and does not guarantee local skill or agent discovery.

The default path needs only Codex CLI authentication. HF Hub writes, HF Jobs,
paid compute, and private/gated Hub access require separate HF credentials and
explicit user approval.

The SFT and KPI skills include tiny adapters that call the original scripts:

```bash
../.venv/bin/python .agents/skills/hf-session-sft-export/scripts/build_sft_adapter.py --help
../.venv/bin/python .agents/skills/hf-kpi-rollup/scripts/build_kpis_adapter.py --help
```

These adapters do not duplicate script logic. They check token environment
variables for real runs, print the delegated command, and return the original
script exit code.

Runtime parity guidance lives in:

- `ml-intern-runtime-workflow`: source event vocabulary, sessions, approvals,
  cleanup, telemetry, model/auth behavior, compaction, and cancellation.
- `ml-intern-tool-surface`: built-in tool families, HF safety gates, and the
  Codex rule to reference or adapt source scripts instead of copying them.
- `ml-intern-frontend-backend`: FastAPI, SSE reconnect, quota/jobs gates,
  frontend state, approvals, and web checks.

## Layout

```text
coding-agents/
  AGENTS.md
  README.md
  .codex/
    config.toml
    agents/
  .agents/
    skills/
```

## Safety

This bundle is documentation and helper glue. It should not store secrets,
pre-approve paid compute, or silently upload to the Hub. The baseline workflow
is read-only research, repo inspection, local validation, adapter help checks,
and local tests. Any HF Job, Hub upload, repo deletion, visibility change, or
long-running compute action needs separate HF credentials and explicit user
approval.

## Verification

Run from this directory when auditing compatibility work:

```bash
../.venv/bin/python scripts/check_metadata.py
rg -n 'coding-agents[/]\.agents|u[v]\b|/skills[ ]add|mcp[_]servers' ../coding-agents
../.venv/bin/python .agents/skills/hf-session-sft-export/scripts/build_sft_adapter.py --help
../.venv/bin/python .agents/skills/hf-kpi-rollup/scripts/build_kpis_adapter.py --help
../.venv/bin/python -m pytest ../tests/unit/test_build_sft.py ../tests/unit/test_build_kpis.py ../tests/unit/test_kpis_scheduler.py ../tests/unit/test_user_quotas.py
```
