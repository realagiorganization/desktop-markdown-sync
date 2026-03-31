#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

SEVERITY_ORDER = {"LOW": 1, "MEDIUM": 2, "HIGH": 3}


def main() -> int:
    report = json.loads(Path(".cache/bandit.json").read_text(encoding="utf-8"))
    failing = 0
    warnings = 0
    for result in report.get("results", []):
        severity = str(result.get("issue_severity", "LOW")).upper()
        text = result.get("issue_text", "bandit finding")
        filename = result.get("filename", "unknown")
        line = result.get("line_number", 1)
        if SEVERITY_ORDER.get(severity, 1) >= SEVERITY_ORDER["MEDIUM"]:
            failing += 1
            print(f"::error file={filename},line={line}::{severity} {text}")
        else:
            warnings += 1
            print(f"::warning file={filename},line={line}::{severity} {text}")
    print(f"bandit warnings: {warnings}; failures: {failing}")
    return 1 if failing else 0


if __name__ == "__main__":
    raise SystemExit(main())
