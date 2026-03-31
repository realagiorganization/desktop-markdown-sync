from __future__ import annotations

from pathlib import Path


def test_packaging_assets_exist() -> None:
    root = Path(__file__).resolve().parents[1]

    assert (root / "scripts" / "build_deb.py").exists()
    assert (
        root
        / "packaging"
        / "debian"
        / "usr"
        / "lib"
        / "systemd"
        / "user"
        / "desktop-markdown-sync.service"
    ).exists()
    assert "wmctrl" in (root / "scripts" / "build_deb.py").read_text(encoding="utf-8")
