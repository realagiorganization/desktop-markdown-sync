#!/usr/bin/env python3
from __future__ import annotations

import configparser
import json
import subprocess
import tomllib
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CHECK_SUFFIXES = {".json", ".toml", ".yaml", ".yml", ".md", ".service"}


def tracked_files() -> list[Path]:
    output = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True)
    return [
        ROOT / line
        for line in output.splitlines()
        if Path(line).suffix in CHECK_SUFFIXES and (ROOT / line).exists()
    ]


def check_json(path: Path) -> None:
    json.loads(path.read_text(encoding="utf-8"))


def check_toml(path: Path) -> None:
    tomllib.loads(path.read_text(encoding="utf-8"))


def check_yaml(path: Path) -> None:
    list(yaml.safe_load_all(path.read_text(encoding="utf-8")))


def check_markdown(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if text and not text.endswith("\n"):
        raise ValueError("missing trailing newline")


def check_service(path: Path) -> None:
    parser = configparser.ConfigParser()
    parser.read(path, encoding="utf-8")


def main() -> int:
    handlers = {
        ".json": check_json,
        ".toml": check_toml,
        ".yaml": check_yaml,
        ".yml": check_yaml,
        ".md": check_markdown,
        ".service": check_service,
    }
    checked = 0
    for path in tracked_files():
        handlers[path.suffix](path)
        checked += 1
    print(f"checked structured/text formats: {checked}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
