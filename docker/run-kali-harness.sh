#!/usr/bin/env bash
set -euo pipefail

artifacts_root="${1:-/artifacts}"
repo_root="/opt/desktop-markdown-sync"

mkdir -p "${artifacts_root}/ui" "${artifacts_root}/logs"
cd "${repo_root}"

python3 -m pip install -e '.[dev]'
python3 scripts/sync_harness_home.py --output-root "${artifacts_root}/mirror"
python3 -m pytest -q tests/test_harness.py
bash scripts/record_fixture_pack_demo.sh \
  "${artifacts_root}/mirror/harness-manifest.json" \
  "${artifacts_root}/ui/fixture-pack-demo.mp4"
