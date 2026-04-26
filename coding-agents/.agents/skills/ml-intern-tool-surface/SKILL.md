---
name: ml-intern-tool-surface
description: Map ML Intern source tool families to safe Codex compatibility usage without duplicating runtime implementations.
---

# ML Intern Tool Surface

Use this skill when mapping source agent tools into Codex guidance, custom
agents, or compatibility skills. The source of truth is
`../agent/core/tools.py`; do not duplicate tool implementations inside
`coding-agents/`.

## Built-In Families

- Sandbox or local tools: `get_sandbox_tools()` by default, `get_local_tools()`
  in local mode. Local mode exposes `bash`, `read`, `write`, and `edit`.
  Remote `sandbox_create` is for source-runtime sandbox Spaces only and is
  approval-gated; use it for script validation and small-run checks only after
  the user approves the remote sandbox.
- `research`: delegates a read-only research sub-agent that can combine papers,
  docs, datasets, and examples in a separate context.
- HF docs: `explore_hf_docs`, `fetch_hf_docs`, and `find_hf_api` for current
  documentation and REST API lookup.
- Papers: `hf_papers` for discovery, snippets, paper reading, citation graphs,
  and dataset/model clues.
- Datasets: `hf_inspect_dataset` for splits, schema, row samples, and format
  checks before ML code or jobs.
- Planning: `plan_tool` tracks multi-step source-runtime tasks with one active
  item at a time.
- HF Jobs: `hf_jobs` for job execution and monitoring. Run-style operations are
  approval-gated and outside the Codex-only baseline.
- HF repo files: `hf_repo_files` for listing, reading, upload, and delete.
  Upload/delete are approval-gated.
- HF repo git: `hf_repo_git` for branch/tag/PR/repo operations. Destructive and
  repo-management actions are approval-gated.
- GitHub examples: `github_find_examples`, `github_list_repos`, and
  `github_read_file` support read-only implementation research and require
  `GITHUB_TOKEN`.
- Disabled legacy tool: `hf_private_repos` remains referenced by old prompt and
  approval logic, but it is not registered in the current built-in tool surface.
  Prefer `hf_repo_files` and `hf_repo_git` for source-runtime repo operations.
- Optional tool servers: source runtime can register additional tools when
  configured, while filtering several overlapping HF tool names. Do not require
  this for Codex compatibility.

## Codex Usage

For Codex skills, prefer references and adapters:

- Point to the source files and source tool names.
- Preserve safety gates and expected evidence.
- Use local commands, adapter help checks, and tests for the default path.
- Ask explicitly before HF Jobs, Hub writes, private/gated reads, repo
  management, paid compute, or long-running operations.
- Never silently substitute datasets, models, sequence length, training method,
  or output destinations.

## Research And Validation Flow

For ML implementation work, mirror the source prompt:

1. Research current papers, docs, and working examples.
2. Inspect dataset schema, splits, samples, and licenses.
3. Verify model repo, architecture, tokenizer, size, and access.
4. Run sandbox or local small-run validation.
5. Only then request approval for scale-out jobs or Hub writes.

If a tool family is missing from the Codex bundle, add concise instructions or a
small adapter that delegates to source code. Do not copy large source scripts or
tool internals into a skill.
