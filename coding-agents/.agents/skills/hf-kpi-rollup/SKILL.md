---
name: hf-kpi-rollup
description: Inspect or run the KPI rollup adapter, with real Hub writes outside the Codex-only baseline unless separately approved.
---

# HF KPI Rollup

Use this skill to inspect or reason about the ML Intern session KPI rollup
workflow. The Codex-only baseline is adapter help, source-script inspection, and
local tests. Real rollups upload to the Hub and require separate HF credentials
plus explicit user approval.

The production logic lives in `../scripts/build_kpis.py`. Do not duplicate it in
agent skills. Use the adapter in this skill to preserve arguments and delegate
to the original script.

## What It Does

`build_kpis.py` reads session trajectory rows from a source HF dataset,
aggregates metrics for the most recently completed hour by default, and uploads
CSV rows to a target dataset.

- default source: `smolagents/ml-intern-sessions`
- default target: `smolagents/ml-intern-kpis`
- hourly output: `hourly/YYYY-MM-DD/HH.csv`
- daily backfill output: `daily/YYYY-MM-DD.csv`

Metrics include sessions, users, turns, LLM calls, tokens, cost, tool success,
failure and regenerate rates, time to first action, feedback, HF job outcomes,
Pro CTA clicks, and GPU hours by flavor.

## Required Environment

For real rollups, one of these must be set:

- `HF_KPI_WRITE_TOKEN`
- `HF_SESSION_UPLOAD_TOKEN`
- `HF_TOKEN`
- `HF_ADMIN_TOKEN`

The adapter does not print token values. Help commands do not require tokens.

## Baseline Commands

Show help:

```bash
../.venv/bin/python .agents/skills/hf-kpi-rollup/scripts/build_kpis_adapter.py --help
```

Out-of-baseline rollup for the last completed hour:

```bash
../.venv/bin/python .agents/skills/hf-kpi-rollup/scripts/build_kpis_adapter.py
```

Out-of-baseline backfill for 24 trailing hours:

```bash
../.venv/bin/python .agents/skills/hf-kpi-rollup/scripts/build_kpis_adapter.py --hours 24
```

Out-of-baseline rollup for one explicit UTC hour:

```bash
../.venv/bin/python .agents/skills/hf-kpi-rollup/scripts/build_kpis_adapter.py --datetime 2026-04-24T14
```

## Safety

This uploads to a dataset repo on real runs. Confirm target repo, time window,
token availability, and explicit approval before executing. Source telemetry
includes session saves, job outcomes, Pro CTA clicks, quotas, and GPU-hour
rollups; keep local adapter help checks separate from real Hub writes.
