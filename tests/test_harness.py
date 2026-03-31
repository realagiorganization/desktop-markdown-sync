from __future__ import annotations

import json
from pathlib import Path

from desktop_markdown_sync.harness import (
    FIXTURE_PACK_SPECS,
    fixture_pack_manifest,
    sync_harness_home,
)


def test_fixture_pack_manifest_discovers_each_pack() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    manifest = fixture_pack_manifest(repo_root)

    assert [entry["name"] for entry in manifest] == [spec.name for spec in FIXTURE_PACK_SPECS]
    assert all(entry["files"] for entry in manifest)


def test_sync_harness_home_mirrors_fixture_pack_hashes(tmp_path) -> None:
    repo_root = Path(__file__).resolve().parents[1]

    manifest_path = sync_harness_home(repo_root=repo_root, output_root=tmp_path)
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))

    mirrored_home = tmp_path / "home" / "standart"
    assert mirrored_home.exists()
    assert (mirrored_home / "subprojects" / "desktop_markdown_sync").exists()

    for pack in payload["packs"]:
        assert pack["file_count"] > 0
        for file_entry in pack["files"]:
            assert file_entry["source_sha256"] == file_entry["target_sha256"]
