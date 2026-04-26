---
name: hf-sandbox-validation
description: Validate ML scripts with local or dry-run checks before any separately approved Hugging Face job.
---

# HF Sandbox Validation

Use this skill for non-trivial ML scripts before paid compute or long-running
jobs. The Codex-only baseline is local validation, dry runs, and static checks.
Remote sandboxes, HF Jobs, and paid compute require separate credentials and
explicit user approval.

## Pattern

1. Prefer local validation or a dry run appropriate to the code path.
2. Install the minimum dependencies.
3. Write or copy the candidate script.
4. Run a small data/model smoke test.
5. Fix import, schema, CUDA, dtype, logging, and persistence errors.
6. Only then request approval for any remote sandbox or full-scale HF Job.

In the source runtime, `sandbox_create` is approval-gated. Treat remote sandbox
creation as outside the Codex-only baseline; local static checks, dry runs, and
small tests remain the default compatibility path.

## Hardware Choice

- Use CPU only for pure data prep, tests, or static validation.
- For separately approved remote validation, use at least `t4-small` for CUDA,
  bf16, quantization, or model loading.
- Move up when OOM appears during validation instead of changing the user's
  requested training method.

## Evidence To Report

- Sandbox hardware and environment.
- Commands run.
- Dataset/model subset used.
- Logs proving training starts, loss prints, outputs save, and Hub push is
  configured when needed.
- Remaining differences between sandbox and full job.
