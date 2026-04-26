---
name: hf-training-job
description: Plan Hugging Face training jobs safely while keeping launches outside the Codex-only baseline unless separately approved.
---

# HF Training Job

Use this skill when planning, reviewing, or debugging Hugging Face training jobs
for ML Intern workflows. The Codex-only baseline is read-only planning and local
validation. Launching or monitoring a real HF Job requires separately configured
HF credentials and explicit user approval.

## Baseline

- Research current docs and examples.
- Verify dataset schema, model availability, tokenizer, size, access, and
  expected dependencies.
- Prepare local or dry-run validation steps.
- Do not submit jobs, start paid compute, upload artifacts, or rely on private
  Hub access from Codex alone.

## Out Of Baseline

Before launching any HF Job or paid/long-running compute, require explicit user
approval and separate HF credentials. State the job purpose, expected hardware,
timeout, estimated duration, Hub outputs, and whether it writes to private or
public repos.

The current `hf_jobs` operations are `run`, `ps`, `logs`, `inspect`, `cancel`,
and scheduled `run`/`ps`/`inspect`/`delete`/`suspend`/`resume`. The source
approval gate still contains legacy checks for `uv` and scheduled `uv`, but
agents should not call `uv` as an `hf_jobs` operation. CPU-only jobs are still
approval-gated unless the source config sets `confirm_cpu_jobs=false`. Frontend
users may also need HF Jobs entitlement and an eligible paid organization
namespace before an approval continuation can resume.

## Preflight Checklist

Before job submission, confirm:

- Reference implementation and docs were checked.
- Dataset schema and format were verified.
- Model repo, tokenizer, and access were verified.
- Dependencies are installed in the job environment.
- `push_to_hub=True` and `hub_model_id` or output dataset repo are set when the
  result must persist.
- Timeout is sized for the model and task. Use at least 2 hours for training.
- Trackio or equivalent monitoring prints plain logs and exposes a dashboard.
- Batch or ablation plans run one pilot job first.

## Hardware Heuristics

- 1-3B params: `t4-small` for demos or `a10g-small` for production.
- 7-13B params: `a10g-large`.
- 30B+ params: `a100-large`.
- 70B+ params: `h100` or `h100x8` for distributed work.

`a10g-small` and `a10g-large` have the same 24 GB GPU memory; the difference is
CPU/RAM.

## Logging And Persistence

- Configure training logs as plain text: `disable_tqdm=True`,
  `logging_strategy="steps"`, and `logging_first_step=True`.
- Save checkpoints intentionally and push final artifacts to the Hub.
- Print the Trackio dashboard URL and final Hub URL.
- Never print tokens.
- HF Jobs and private/gated resources require separately configured HF
  credentials; a Codex subscription alone is not enough.

## Error Recovery

Diagnose the actual error from logs. Do not retry unchanged. For OOM, preserve
the requested method and sequence length: lower per-device batch size, increase
gradient accumulation to keep effective batch size, enable gradient checkpointing,
or move to larger hardware. Ask before changing task, method, dataset, model, or
sequence length.
