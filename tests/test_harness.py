from __future__ import annotations

import json
from pathlib import Path

from desktop_markdown_sync.harness import (
    FIXTURE_PACK_SPECS,
    FixturePackSpec,
    fixture_pack_entries,
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


def test_recursive_fixture_pack_entries_preserve_nested_paths(tmp_path) -> None:
    source_root = tmp_path / "fixtures" / "collections"
    nested_file = source_root / "retro" / "16-bit" / "index.md"
    nested_file.parent.mkdir(parents=True, exist_ok=True)
    nested_file.write_text("# Nested fixture\n", encoding="utf-8")

    spec = FixturePackSpec(
        name="nested",
        source_dir="fixtures/collections",
        file_glob="*.md",
        target_dir="mirror/collections",
        recursive=True,
    )

    entries = fixture_pack_entries(tmp_path, spec)

    assert entries == [nested_file]


def test_sync_harness_home_preserves_recursive_collection_layout(tmp_path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / "fixtures" / "console-games" / "handheld").mkdir(parents=True, exist_ok=True)
    source_file = repo_root / "fixtures" / "console-games" / "handheld" / "pocket.md"
    source_file.write_text("# Pocket Fixture\n", encoding="utf-8")

    spec = FixturePackSpec(
        name="console-games",
        source_dir="fixtures/console-games",
        file_glob="*.md",
        target_dir="subprojects/desktop_markdown_sync/fixtures/console-games",
        recursive=True,
    )

    entries = fixture_pack_entries(repo_root, spec)
    destination_root = tmp_path / "mirror"
    relative_entry = entries[0].relative_to(repo_root / spec.source_dir)
    destination = destination_root / spec.target_dir / relative_entry
    destination.parent.mkdir(parents=True, exist_ok=True)

    for entry in entries:
        target = destination_root / spec.target_dir / entry.relative_to(repo_root / spec.source_dir)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(entry.read_bytes())

    assert destination.read_text(encoding="utf-8") == "# Pocket Fixture\n"
