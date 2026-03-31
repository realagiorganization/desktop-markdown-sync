#!/usr/bin/env python3
from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    output = subprocess.check_output(["git", "ls-files", "*.sh"], cwd=ROOT, text=True)
    checked = 0
    for relative_path in output.splitlines():
        if not relative_path:
            continue
        subprocess.run(["bash", "-n", relative_path], cwd=ROOT, check=True)
        checked += 1
    print(f"checked shell syntax: {checked}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
