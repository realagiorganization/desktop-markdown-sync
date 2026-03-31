from __future__ import annotations

import argparse
import json
from pathlib import Path

from .config import SyncConfig
from .desktop_backend import PlasmaDesktopBackend
from .render import write_fixtures
from .service import SyncService
from .snapshot import load_snapshot, write_snapshot


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="desktop-markdown-sync")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("export")
    subparsers.add_parser("apply")
    subparsers.add_parser("daemon")
    subparsers.add_parser("snapshot-json")

    snapshot_parser = subparsers.add_parser("snapshot")
    snapshot_parser.add_argument("--output", type=Path, required=True)

    render_parser = subparsers.add_parser("render-fixtures")
    render_parser.add_argument("--snapshot", type=Path, required=True)
    render_parser.add_argument("--fixtures-dir", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    config = SyncConfig.from_env()
    backend = PlasmaDesktopBackend()
    service = SyncService(config=config, backend=backend)

    if args.command == "export":
        service.export_once()
        return 0
    if args.command == "apply":
        service.apply_once()
        return 0
    if args.command == "daemon":
        service.run_forever()
        return 0
    if args.command == "snapshot-json":
        desktops = [desktop.to_dict() for desktop in backend.capture_state()]
        print(json.dumps(desktops, indent=2, sort_keys=True))
        return 0
    if args.command == "snapshot":
        path = write_snapshot(args.output)
        print(path)
        return 0
    if args.command == "render-fixtures":
        snapshot = load_snapshot(args.snapshot)
        written = write_fixtures(snapshot, args.fixtures_dir)
        print(f"wrote {len(written)} fixture files")
        return 0
    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
