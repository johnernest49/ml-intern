#!/usr/bin/env python3
"""Delegate to the project's scripts/build_kpis.py without duplicating logic."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

TOKEN_ENV_VARS = (
    "HF_KPI_WRITE_TOKEN",
    "HF_SESSION_UPLOAD_TOKEN",
    "HF_TOKEN",
    "HF_ADMIN_TOKEN",
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[5]


def _is_help(argv: list[str]) -> bool:
    return any(arg in {"-h", "--help"} for arg in argv)


def _check_env(argv: list[str]) -> int:
    if _is_help(argv):
        return 0
    if any(os.environ.get(name) for name in TOKEN_ENV_VARS):
        return 0
    names = ", ".join(TOKEN_ENV_VARS)
    print(f"Missing HF token. Set one of: {names}.", file=sys.stderr)
    return 1


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    env_status = _check_env(args)
    if env_status:
        return env_status

    root = _repo_root()
    script = root / "scripts" / "build_kpis.py"
    if not script.exists():
        print(f"Original script not found: {script}", file=sys.stderr)
        return 1

    cmd = [sys.executable, str(script), *args]

    if not _is_help(args):
        printable = " ".join(cmd)
        print(f"Running: {printable}", file=sys.stderr)
    return subprocess.run(cmd, cwd=root, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
