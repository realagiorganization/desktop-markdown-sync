#!/usr/bin/env python3
from __future__ import annotations

import json

from desktop_markdown_sync.snapshot import collect_snapshot


def main() -> int:
    snapshot = collect_snapshot()
    print(json.dumps(snapshot, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
