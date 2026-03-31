#!/usr/bin/env python3
from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    output = subprocess.check_output(["git", "ls-files", "*.md"], cwd=ROOT, text=True)
    checked = 0
    for relative_path in output.splitlines():
        path = ROOT / relative_path
        text = path.read_text(encoding="utf-8")
        if text and not text.endswith("\n"):
            raise ValueError(f"{relative_path}: missing trailing newline")
        if "\t" in text:
            raise ValueError(f"{relative_path}: contains tab characters")
        if "```" in text and text.count("```") % 2 != 0:
            raise ValueError(f"{relative_path}: unbalanced fenced code blocks")
        checked += 1
    print(f"checked markdown files: {checked}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
