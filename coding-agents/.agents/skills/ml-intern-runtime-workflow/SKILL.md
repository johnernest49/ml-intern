---
name: ml-intern-runtime-workflow
description: Preserve ML Intern source-runtime behavior around sessions, approvals, telemetry, context compaction, cancellation, and config while working from Codex.
---

# ML Intern Runtime Workflow

Use this skill when compatibility work needs to describe or preserve the real
ML Intern agent loop. The source runtime is broader than the Codex bundle; keep
Codex defaults lightweight while documenting the source contracts accurately.

## Source Files

- `../agent/core/agent_loop.py`: turn loop, approval gates, retries,
  interrupts, shutdown, context-overflow handling, and final saves.
- `../agent/core/session.py`: session state, events, pending approvals, undo,
  compact operations, model updates, trajectory serialization, and redaction.
- `../agent/core/telemetry.py`: heartbeat saves, session uploads, and derived
  telemetry events.
- `../agent/config.py`: source runtime config model.
- `../agent/prompts/system_prompt_v3.yaml`: ML, safety, and headless-mode
  behavior rules.
- `../agent/main.py`: CLI commands, approval prompts, interrupt handling, model
  switching, and headless entrypoint.

## Session Lifecycle

The source runtime is event driven. A session receives user input, approval,
interrupt, undo, compact, and shutdown operations. It emits LLM deltas, tool
input/output, approval-required, tool-state-change, turn-complete, error,
interrupted, and shutdown events. Compatibility docs should preserve these names
when explaining frontend/backend or telemetry flows.

## Event Surface

Use the source event vocabulary when documenting runtime parity. Interactive
stream events include `ready`, `processing`, `assistant_chunk`,
`assistant_stream_end`, `assistant_message`, `tool_call`, `tool_output`,
`tool_state_change`, `approval_required`, `plan_update`, `tool_log`, `error`,
`interrupted`, `undo_complete`, `compacted`, `turn_complete`, and `shutdown`.
The backend SSE helper treats `turn_complete`, `approval_required`, `error`,
`interrupted`, and `shutdown` as stream-closing events for a turn or
continuation.

Telemetry and trajectory events also include `llm_call`, `hf_job_submit`,
`hf_job_complete`, `sandbox_create`, `sandbox_destroy`, `feedback`,
`jobs_access_blocked`, and `pro_cta_click`. These are source-runtime facts for
SFT/KPI exports and audit trails; the Codex compatibility baseline should not
try to synthesize them.

Terminal CLI rendering in `../agent/main.py` consumes the same event stream for
assistant chunks/messages, tool calls and outputs, tool logs, tool state
changes, compaction notices, approvals, interrupts, undo completion, errors,
shutdown, and turn completion. Keep terminal behavior described as source UI
behavior, not a requirement for Codex agents.

Session persistence is part of the source contract:

- `save_sessions` controls whether trajectories are saved and uploaded.
- `auto_save_interval` saves after user-turn intervals.
- `heartbeat_interval_s` saves during long-running turns so traces survive
  crashes or long HF Jobs.
- Saves redact secrets before writing local session logs.
- Shutdown and emergency cleanup perform final flushes when session saving is
  enabled.
- Restore-from-summary creates a new session seeded from prior messages instead
  of resurrecting an oversized context unchanged.

## Cleanup

Preserve cleanup behavior when describing interrupts, teardown, and shutdown:

- Interrupt sets the session cancellation flag directly, bypassing the normal
  submission queue.
- Cancellation during a running turn emits cancelled tool states when possible,
  kills sandbox-side processes, cancels tracked HF Jobs, and then emits
  `interrupted`.
- Cancellation during approved-tool execution marks approved tools as
  `cancelled`, runs the same cleanup path, increments the turn, and auto-saves
  if configured.
- Session teardown deletes owned sandbox Spaces and records `sandbox_destroy`.
- Explicit shutdown emits `shutdown`, stops the session loop, and triggers a
  save/upload when `save_sessions` is enabled.
- Backend session death performs a final save/upload flush when enabled, even if
  the browser disconnects without calling `/shutdown`.

## Approvals

The source runtime asks approval for:

- `sandbox_create`.
- `hf_jobs` run-style operations, including CPU jobs unless
  `confirm_cpu_jobs=false`.
- HF repo file uploads and deletes.
- HF repo git destructive or management operations such as delete branch/tag,
  merge PR, create repo, and update repo.
- Legacy private repo uploads unless `auto_file_upload=true`, plus repo
  creation.

`yolo_mode` disables approvals in the source runtime. Do not make that a Codex
default. Codex compatibility guidance should keep the baseline read-only or
local-validation-only unless the user explicitly approves broader operations.

## Config Knobs

Document these as source-runtime facts, not Codex prerequisites:

- `model_name` and provider routing through LiteLLM/HF Router.
- Available backend web models are `moonshotai/Kimi-K2.6`,
  `bedrock/us.anthropic.claude-opus-4-6-v1`,
  `MiniMaxAI/MiniMax-M2.7`, and `zai-org/GLM-5.1`.
- Web model switching is session-scoped; changing one browser tab/session does
  not mutate other active sessions.
- Anthropic/Claude web routes are gated by Hugging Face org membership, and the
  Claude daily quota is charged at message-submit time on first Anthropic use in
  a session, not at session creation or model switch time.
- HF Router token lookup for source LLM calls is `INFERENCE_TOKEN`, then the
  session/user HF token, then `HF_TOKEN`; the hosted Space may also set
  `X-HF-Bill-To`.
- CLI HF token lookup in `../agent/main.py` is `HF_TOKEN`, then
  `HfApi().token`, then `~/.cache/huggingface/token`. Interactive CLI prompts
  for a token when none is found, validates it, and saves it with
  `huggingface_hub.login()` when possible. Headless mode does not prompt; it
  exits with instructions to set `HF_TOKEN` or run `huggingface-cli login`.
- CLI flags include positional `prompt` for headless mode, `--model`/`-m`,
  `--max-iterations`, and `--no-stream`. Headless mode sets source-runtime
  `yolo_mode=True` and uses local tools.
- Backend title generation uses `openai/openai/gpt-oss-120b:cerebras` through
  the HF Router with low reasoning effort and falls back to a truncated user
  message if generation fails.
- Optional MCP server configuration with environment-variable substitution.
- `reasoning_effort` preference and per-model fallback cache.
- `max_iterations` for limiting LLM calls per turn.
- `save_sessions`, `session_dataset_repo`, `auto_save_interval`, and
  `heartbeat_interval_s`.
- `confirm_cpu_jobs`, `auto_file_upload`, and `yolo_mode`.

The Codex compatibility bundle must not require HF tokens, external provider
keys, web auth, or optional tool servers for the default workflow.

## Reliability Rules

- On repeated malformed tool calls or repeated failures, change strategy rather
  than retrying unchanged.
- On context overflow, compact or restore from summary before continuing.
- On transient LLM/provider failures, retry within the source-runtime retry
  pattern; on reasoning-effort errors, downgrade through the supported cascade.
- On interrupt or cancellation, report cancelled tool states and keep cleanup
  paths intact.
- For ML jobs, preserve the requested model, dataset, method, sequence length,
  and output destination unless the user approves a scope change.
- Before declaring completion, verify the requested output exists or explain the
  exact blocker and next recovery step.

## Headless Source Behavior

`system_prompt_v3.yaml` defines stricter autonomous behavior than interactive
Codex work: keep using tools, work until the time budget ends, run research and
validation loops, reserve final time for evaluation and saving, and ensure the
required output persists. Do not copy this into Codex as a default no-stop
policy; reference it when documenting or adapting source headless workflows.
