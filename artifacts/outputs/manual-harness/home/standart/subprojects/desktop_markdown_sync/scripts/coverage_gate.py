#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("coverage_xml", type=Path)
    parser.add_argument("--warn-under", type=float, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    text = args.coverage_xml.read_text(encoding="utf-8")
    match = re.search(r'line-rate="([0-9.]+)"', text)
    if not match:
        raise ValueError("coverage.xml does not contain a line-rate attribute")
    line_rate = float(match.group(1))
    percent = round(line_rate * 100, 2)
    print(f"coverage percent: {percent}")
    if percent < args.warn_under:
        print(
            "::warning::Coverage "
            f"{percent}% is below the warning threshold of {args.warn_under:.2f}%."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
