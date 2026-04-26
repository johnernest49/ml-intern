---
name: ml-intern-frontend-backend
description: Orient frontend and backend work in ML Intern, including FastAPI, React/Vite, stores, hooks, and likely test commands.
---

# ML Intern Frontend And Backend

Use this skill for project orientation around `../backend` and `../frontend`.

## Backend

- FastAPI entrypoint: `../backend/main.py`.
- Routes: `../backend/routes/`.
- Session and quota support: `../backend/session_manager.py`,
  `../backend/user_quotas.py`, `../backend/kpis_scheduler.py`.
- Agent integration flows through backend route and session management code into
  `../agent`.

### Backend Endpoint Groups

- Health and model helpers: `GET /api/health`, `GET /api/health/llm`,
  `GET /api/config/model`, and `POST /api/title`. Title generation uses
  `openai/openai/gpt-oss-120b:cerebras` through HF Router/Cerebras and falls
  back to the user message on failure.
- Auth routes: `GET /auth/login`, `GET /auth/callback`, `GET /auth/logout`,
  `GET /auth/status`, `GET /auth/me`, and `GET /auth/org-membership`.
  OAuth config comes from `OAUTH_CLIENT_ID`, `OAUTH_CLIENT_SECRET`,
  `OPENID_PROVIDER_URL`, `HF_OAUTH_ORG_ID`, and `SPACE_HOST`. OAuth state is
  stored in memory with a 5-minute TTL. Successful login sets a 7-day HttpOnly
  `hf_access_token` cookie; `SPACE_HOST` enables the production HTTPS redirect
  URI and secure cookie flag.
- Session lifecycle: `POST /api/session`, `POST /api/session/restore-summary`,
  `GET /api/session/{session_id}`, `GET /api/sessions`,
  `DELETE /api/session/{session_id}`, and `POST /api/shutdown/{session_id}`.
  Session capacity is capped globally and per user; the dev auth bypass uses
  the `dev` owner and skips the per-user cap.
- Session ownership: most routes call the session-owner check. Production auth
  validates Bearer tokens or the `hf_access_token` cookie; local dev returns
  the default `dev` user.
- Chat and reconnect: `POST /api/chat/{session_id}` accepts either `text` or an
  approvals array and streams SSE until `turn_complete`, `approval_required`,
  `error`, `interrupted`, or `shutdown`. `GET /api/events/{session_id}` lets the
  frontend reattach to an active processing session without submitting input;
  keepalive comments prevent proxy timeouts.
- Approvals: `POST /api/approve` and chat approval continuations pass
  `approved`, rejection `feedback`, optional `edited_script`, and optional
  `namespace` through to the source agent loop.
- Model, quota, and jobs access: `POST /api/session/{session_id}/model`,
  `GET /api/user/quota`, and `GET /api/user/jobs-access`. The backend model
  catalog is `moonshotai/Kimi-K2.6`,
  `bedrock/us.anthropic.claude-opus-4-6-v1`,
  `MiniMaxAI/MiniMax-M2.7`, and `zai-org/GLM-5.1`. Model switches are
  session-scoped; unknown models are rejected. Anthropic paths require HF org
  membership, and the Claude cap is charged when a user message is submitted.
  HF Jobs approvals can be blocked with upgrade-required, namespace-required,
  or invalid-namespace responses.
- History controls: `GET /api/session/{session_id}/messages`,
  `POST /api/interrupt/{session_id}`, `POST /api/undo/{session_id}`,
  `POST /api/truncate/{session_id}`, and `POST /api/compact/{session_id}`.
  Interrupt cancels the live turn directly; undo emits `undo_complete`; compact
  emits `compacted`; truncate edits in-memory history before a chosen user
  message.
- Telemetry and feedback: `POST /api/feedback/{session_id}` appends `feedback`
  events and saves when enabled. `POST /api/pro-click/{session_id}` records
  `pro_cta_click` and saves when enabled.

### Backend Cleanup

- Session deletion and normal session teardown delete owned sandbox Spaces.
- Interrupt/cancellation kills sandbox processes, cancels tracked HF Jobs, and
  emits cancelled/interrupted states.
- Shutdown and backend session death trigger final save/upload flushes when
  `save_sessions` is enabled.
- HF token extraction for session creation and jobs access is Bearer header,
  then `hf_access_token` cookie, then `HF_TOKEN` fallback. Never print token
  values in compatibility docs or checks.

Likely checks:

```bash
../.venv/bin/python -m pytest ../tests/unit/test_kpis_scheduler.py ../tests/unit/test_user_quotas.py
../.venv/bin/python -m pytest ../tests/unit
```

## Frontend

- Vite/React app: `../frontend/src/main.tsx` and `../frontend/src/App.tsx`.
- Layout: `../frontend/src/components/Layout/AppLayout.tsx`.
- Chat UI: `../frontend/src/components/Chat/`.
- Session sidebar: `../frontend/src/components/SessionSidebar/`.
- Stores and hooks: `../frontend/src/store/`, `../frontend/src/hooks/`,
  `../frontend/src/lib/`.
- API helpers: `../frontend/src/utils/api.ts`.
- SSE adapter: `../frontend/src/lib/sse-chat-transport.ts` maps backend events
  into AI SDK message/tool events and detects approval continuations.
- Chat state: `../frontend/src/hooks/useAgentChat.ts` and
  `../frontend/src/store/agentStore.ts` track activity status, pending
  approvals, tool panels, job URLs, restore state, model state, quota blocks,
  and jobs namespace prompts.
- Approval UI: `../frontend/src/components/Chat/ToolCallGroup.tsx` supports
  batch and per-tool approval, rejection feedback, edited scripts, undo of local
  decisions, and namespace selection for blocked HF Jobs approvals.
- Expired or oversized sessions use
  `../frontend/src/components/Chat/ExpiredBanner.tsx` to restore with summary
  or start over.
- `../frontend/src/components/JobsUpgradeDialog.tsx` handles jobs upgrade and
  namespace-selection flows; `../frontend/src/components/ClaudeCapDialog.tsx`
  handles Claude quota fallback.
- The store keeps per-session UI snapshots for processing/activity state, plan,
  right-panel data, and research-agent status, while mirroring the active
  session into flat fields for components.
- The right panel follows a single-artifact model: script/input/output for the
  active tool artifact rather than multiple competing panels.
- Reconnect-to-stream checks session info, then subscribes to `/api/events` only
  when the backend says the session is still processing.
- Tool error and rejection states persist across renders. Edited `hf_jobs`
  scripts and approval namespace choices are stored by `tool_call_id` and sent
  with the next approval continuation.
- HF Jobs URLs/statuses are tracked by `tool_call_id` from tool output or
  `tool_state_change` payloads.
- Blocked jobs and Claude quota failures surface through `JobsUpgradeDialog`
  and `ClaudeCapDialog`; do not collapse those into generic error guidance.

Likely checks from `../frontend`:

```bash
npm run lint
npm run build
```

## Workflow

Read local patterns before editing. Keep UI changes consistent with the current
design system, state stores, and transport abstractions. For backend changes,
add or update focused unit tests near the behavior touched.

When documenting compatibility behavior, preserve the source event names and
ownership rules: sessions belong to users, approvals continue an in-progress
turn, and quota/jobs gates can reject a continuation before the agent resumes.
