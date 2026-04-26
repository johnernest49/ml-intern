#!/usr/bin/env python3
"""Validate Codex compatibility bundle metadata."""

from __future__ import annotations

import re
import sys
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENTS_DIR = ROOT / ".codex" / "agents"
SKILLS_DIR = ROOT / ".agents" / "skills"


def _check_agents() -> list[str]:
    errors: list[str] = []
    for path in sorted(AGENTS_DIR.glob("*.toml")):
        try:
            data = tomllib.loads(path.read_text())
        except tomllib.TOMLDecodeError as exc:
            errors.append(f"{path.relative_to(ROOT)}: invalid TOML: {exc}")
            continue
        for key in ("name", "description", "developer_instructions"):
            if not str(data.get(key, "")).strip():
                errors.append(f"{path.relative_to(ROOT)}: missing {key}")
    return errors


def _check_skills() -> list[str]:
    errors: list[str] = []
    frontmatter_re = re.compile(r"\A---\n(.*?)\n---\n", re.S)
    name_re = re.compile(r"^name: [a-z0-9-]+$", re.M)
    description_re = re.compile(r"^description: .\S.*$", re.M)

    for path in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        text = path.read_text()
        match = frontmatter_re.match(text)
        rel = path.relative_to(ROOT)
        if not match:
            errors.append(f"{rel}: missing YAML-style frontmatter")
            continue
        frontmatter = match.group(1)
        if not name_re.search(frontmatter):
            errors.append(f"{rel}: missing lowercase hyphenated name")
        if not description_re.search(frontmatter):
            errors.append(f"{rel}: missing useful description")
    return errors


def main() -> int:
    errors = _check_agents() + _check_skills()
    if errors:
        print("metadata check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("metadata ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
