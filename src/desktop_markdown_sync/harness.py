from __future__ import annotations

import hashlib
import json
import shutil
from dataclasses import dataclass
from pathlib import Path

TOP_LEVEL_DOCS = (
    "AGENTS.md",
    "install.md",
    "readme.md",
    "README.agents.md",
    "DEVPLAN.md",
    "REQUESTED.predict_vs_actual.inline.md",
    "REQUESTED.tables_timings.md",
)


@dataclass(frozen=True, slots=True)
class FixturePackSpec:
    name: str
    source_dir: str
    file_glob: str
    target_dir: str
    recursive: bool = False


FIXTURE_PACK_SPECS = (
    FixturePackSpec(
        name="live-desktops",
        source_dir="fixtures",
        file_glob="desktop-*.md",
        target_dir="subprojects/desktop_markdown_sync/fixtures",
    ),
    FixturePackSpec(
        name="console-games",
        source_dir="fixtures/console-games",
        file_glob="*.md",
        target_dir="subprojects/desktop_markdown_sync/fixtures/console-games",
        recursive=True,
    ),
    FixturePackSpec(
        name="bhakti",
        source_dir="BHAKTI",
        file_glob="*.md",
        target_dir="subprojects/desktop_markdown_sync/BHAKTI",
    ),
    FixturePackSpec(
        name="pizzagame",
        source_dir="PIZZAGAME",
        file_glob="*.md",
        target_dir="subprojects/desktop_markdown_sync/PIZZAGAME",
    ),
    FixturePackSpec(
        name="shipgirls",
        source_dir="SHIPGIRLS",
        file_glob="*.md",
        target_dir="subprojects/desktop_markdown_sync/SHIPGIRLS",
    ),
)

REPO_MIRROR_ITEMS = (
    ".github",
    "docker",
    "packaging",
    "scripts",
    "skills",
    "src",
    "tests",
    "BHAKTI",
    "PIZZAGAME",
    "SHIPGIRLS",
    "fixtures",
    "Makefile",
    "pyproject.toml",
    "AGENTS.md",
    "DEVPLAN.md",
    "install.md",
    "readme.md",
    "REQUESTED.predict_vs_actual.inline.md",
    "REQUESTED.tables_timings.md",
)


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fixture_pack_entries(repo_root: Path, spec: FixturePackSpec) -> list[Path]:
    source_root = repo_root / spec.source_dir
    if spec.recursive:
        iterator = source_root.rglob(spec.file_glob)
    else:
        iterator = source_root.glob(spec.file_glob)
    return sorted(path for path in iterator if path.is_file())


def fixture_pack_manifest(repo_root: Path) -> list[dict[str, object]]:
    manifest = []
    for spec in FIXTURE_PACK_SPECS:
        files = fixture_pack_entries(repo_root, spec)
        manifest.append(
            {
                "name": spec.name,
                "source_dir": spec.source_dir,
                "target_dir": spec.target_dir,
                "files": [
                    {
                        "name": path.name,
                        "relative_path": str(path.relative_to(repo_root)),
                        "collection_path": str(path.relative_to(repo_root / spec.source_dir)),
                        "sha256": file_sha256(path),
                    }
                    for path in files
                ],
            }
        )
    return manifest


def _write_parent_like_docs(home_root: Path) -> None:
    docs = {
        "AGENTS.md": (
            "# Parent Repo Harness Notes\n\n"
            "This is a generated `/home/standart` harness root used for Docker-based "
            "desktop-markdown-sync fixture testing.\n"
        ),
        "install.md": (
            "# Harness install\n\n"
            "The Kali harness mirrors the standalone subproject under "
            "`/home/standart/subprojects/desktop_markdown_sync`.\n"
        ),
        "readme.md": (
            "# Harness Home\n\n"
            "This generated home directory mimics the parent-repo layout expected by "
            "desktop-markdown-sync integration tests.\n"
        ),
        "README.agents.md": (
            "# README.agents\n\n"
            "| File | Purpose |\n"
            "| --- | --- |\n"
            "| AGENTS.md | Generated harness instructions |\n"
        ),
        "DEVPLAN.md": (
            "# DEVPLAN\n\n"
            "- [x] Generate Kali harness home mirror.\n"
            "- [x] Sync fixture packs into the mirrored subproject.\n"
        ),
        "REQUESTED.predict_vs_actual.inline.md": (
            "# REQUESTED.predict_vs_actual.inline.md\n\n"
            "Generated inside the Docker harness home mirror.\n"
        ),
        "REQUESTED.tables_timings.md": (
            "# REQUESTED.tables_timings.md\n\nGenerated inside the Docker harness home mirror.\n"
        ),
    }
    for doc_name in TOP_LEVEL_DOCS:
        (home_root / doc_name).write_text(docs[doc_name], encoding="utf-8")


def _copy_repo_items(repo_root: Path, subproject_root: Path) -> None:
    for item_name in REPO_MIRROR_ITEMS:
        source = repo_root / item_name
        destination = subproject_root / item_name
        if not source.exists():
            continue
        if source.is_dir():
            shutil.copytree(source, destination, dirs_exist_ok=True)
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)


def sync_harness_home(repo_root: Path, output_root: Path) -> Path:
    home_root = output_root / "home" / "standart"
    if home_root.exists():
        shutil.rmtree(home_root)
    home_root.mkdir(parents=True, exist_ok=True)
    _write_parent_like_docs(home_root)

    subproject_root = home_root / "subprojects" / "desktop_markdown_sync"
    subproject_root.mkdir(parents=True, exist_ok=True)
    _copy_repo_items(repo_root, subproject_root)

    packs_manifest = []
    for spec in FIXTURE_PACK_SPECS:
        source_files = fixture_pack_entries(repo_root, spec)
        destination_dir = home_root / spec.target_dir
        destination_dir.mkdir(parents=True, exist_ok=True)
        synced_files = []
        for source in source_files:
            relative_source = source.relative_to(repo_root / spec.source_dir)
            destination = destination_dir / relative_source
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            synced_files.append(
                {
                    "name": source.name,
                    "collection_path": str(relative_source),
                    "source_sha256": file_sha256(source),
                    "target_sha256": file_sha256(destination),
                }
            )
        packs_manifest.append(
            {
                "name": spec.name,
                "source_dir": spec.source_dir,
                "target_dir": str(destination_dir.relative_to(home_root)),
                "file_count": len(synced_files),
                "files": synced_files,
            }
        )

    manifest = {
        "home_root": str(home_root),
        "subproject_root": str(subproject_root),
        "packs": packs_manifest,
    }
    manifest_path = output_root / "harness-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest_path
