#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "readme.md"
WORKFLOWS_DIR = ROOT / ".github" / "workflows"
REQUIRED_TOP_LEVEL_DOCS = ("AGENTS.md", "install.md", "readme.md", "DEVPLAN.md")
BADGE_RE = re.compile(r"actions/workflows/([^)/]+)\)")


def _assert_required_docs() -> None:
    missing = [name for name in REQUIRED_TOP_LEVEL_DOCS if not (ROOT / name).exists()]
    if missing:
        raise FileNotFoundError(f"missing required top-level docs: {', '.join(missing)}")


def _assert_workflow_badges() -> None:
    workflow_files = sorted(path.name for path in WORKFLOWS_DIR.glob("*.yml"))
    readme_text = README.read_text(encoding="utf-8")
    badge_files = sorted(set(BADGE_RE.findall(readme_text)))
    missing_badges = [name for name in workflow_files if name not in badge_files]
    stale_badges = [name for name in badge_files if name not in workflow_files]
    if missing_badges:
        raise ValueError(f"readme.md is missing badges for workflows: {', '.join(missing_badges)}")
    if stale_badges:
        raise ValueError(f"readme.md references unknown workflow badges: {', '.join(stale_badges)}")


def main() -> int:
    _assert_required_docs()
    _assert_workflow_badges()
    print("checked repo contract: docs and workflow badges are in sync")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
