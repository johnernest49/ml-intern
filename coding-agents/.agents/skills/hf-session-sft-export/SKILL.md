---
name: hf-session-sft-export
description: Inspect or run the SFT export adapter, with real Hub writes outside the Codex-only baseline unless separately approved.
---

# HF Session SFT Export

Use this skill to inspect or reason about the ML Intern SFT export workflow. The
Codex-only baseline is adapter help, source-script inspection, and local tests.
Real exports upload to the Hub and require separate HF credentials plus explicit
user approval.

The production logic lives in `../scripts/build_sft.py`. Do not duplicate it in
agent skills. Use the adapter in this skill to preserve arguments and delegate
to the original script.

## What It Does

`build_sft.py` reads session JSONL rows from a source HF dataset and writes raw
multi-turn tool-calling SFT rows to a target HF dataset:

- default source: `smolagents/ml-intern-sessions`
- default target: `smolagents/ml-intern-sft`
- output path pattern: `sft/YYYY-MM-DD/<session_id>.jsonl`

The original script attaches tags via `agent/sft/tagger.py` and preserves
messages and tool schemas for downstream SFT slicing.

## Required Environment

For real exports, one of these must be set:

- `HF_SFT_WRITE_TOKEN`
- `HF_SESSION_UPLOAD_TOKEN`
- `HF_TOKEN`
- `HF_ADMIN_TOKEN`

The adapter does not print token values. Help commands do not require tokens.

## Baseline Commands

Show help:

```bash
../.venv/bin/python .agents/skills/hf-session-sft-export/scripts/build_sft_adapter.py --help
```

Out-of-baseline real export for one explicit UTC date:

```bash
../.venv/bin/python .agents/skills/hf-session-sft-export/scripts/build_sft_adapter.py --date 2026-04-24
```

Out-of-baseline real export for trailing days:

```bash
../.venv/bin/python .agents/skills/hf-session-sft-export/scripts/build_sft_adapter.py --days 7
```

## Safety

This uploads to a dataset repo on real runs. Confirm target repo, date range,
token availability, and explicit approval before executing. Source session
uploads may also be controlled by `save_sessions`, `session_dataset_repo`,
redaction, heartbeat saves, and final shutdown flushes; do not assume Codex help
checks imply Hub write access.
