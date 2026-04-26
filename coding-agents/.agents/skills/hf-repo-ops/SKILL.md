---
name: hf-repo-ops
description: Inspect Hugging Face repos safely, with write operations outside the Codex-only baseline unless separately approved.
---

# HF Repo Ops

Use this skill for Hugging Face Hub repository inspection and for planning file
updates, dataset uploads, model pushes, or git-style operations. The Codex-only
baseline is read-only inspection. Writes require separately configured HF
credentials and explicit user approval.

## Safety

- Public read operations are fine. Private or gated reads require separately
  configured HF credentials.
- Ask before creating repos, uploading files, deleting files, changing
  visibility, force-pushing, or modifying protected resources.
- Source approval gates apply to `hf_repo_files` upload/delete and `hf_repo_git`
  destructive or management operations: delete branch, delete tag, merge PR,
  create repo, and update repo.
- Never embed or print access tokens.
- Prefer environment variables such as `HF_TOKEN`, `HF_ADMIN_TOKEN`, or
  workflow-specific tokens already documented by the project.
- Confirm repo type: `model`, `dataset`, or `space`.

## Write Checklist

Before any out-of-baseline write:

- Target repo ID and type.
- Exact files or paths.
- Public/private visibility impact.
- Commit message.
- Whether the operation is overwrite, append, or delete.
- Rollback path if something fails.

## Review Mode

For substantial changes, stage them as local files or branch-style diffs first.
Show the file list and intended Hub paths before upload. Prefer small commits
with clear messages and avoid bundling unrelated changes.
