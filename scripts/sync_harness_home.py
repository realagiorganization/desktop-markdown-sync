#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from desktop_markdown_sync.harness import sync_harness_home


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", type=Path, required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    manifest_path = sync_harness_home(repo_root=repo_root, output_root=args.output_root)
    print(manifest_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
