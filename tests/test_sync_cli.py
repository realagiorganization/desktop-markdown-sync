from __future__ import annotations

import json

from desktop_markdown_sync import cli
from desktop_markdown_sync.models import DesktopState


class FakeBackend:
    def capture_state(self) -> list[DesktopState]:
        return [DesktopState(desktop_name="research", desktop_index=1, current=True)]


class FakeService:
    def __init__(self) -> None:
        self.exported = False
        self.applied = False
        self.daemon = False

    def export_once(self) -> list[str]:
        self.exported = True
        return []

    def apply_once(self) -> None:
        self.applied = True

    def run_forever(self) -> None:
        self.daemon = True


def test_export_command(monkeypatch) -> None:
    fake_service = FakeService()
    monkeypatch.setattr(cli, "PlasmaDesktopBackend", lambda: FakeBackend())
    monkeypatch.setattr(cli, "SyncService", lambda config, backend: fake_service)

    assert cli.main(["export"]) == 0
    assert fake_service.exported is True


def test_apply_command(monkeypatch) -> None:
    fake_service = FakeService()
    monkeypatch.setattr(cli, "PlasmaDesktopBackend", lambda: FakeBackend())
    monkeypatch.setattr(cli, "SyncService", lambda config, backend: fake_service)

    assert cli.main(["apply"]) == 0
    assert fake_service.applied is True


def test_snapshot_then_render_fixtures_round_trip(tmp_path, monkeypatch) -> None:
    snapshot_payload = [
        {
            "desktop_index": 1,
            "desktop_id": "desktop-1",
            "desktop_name": "SSH 1: sample",
            "windows": [],
        }
    ]

    def fake_write_snapshot(path):
        path.write_text(json.dumps(snapshot_payload), encoding="utf-8")
        return path

    monkeypatch.setattr(cli, "write_snapshot", fake_write_snapshot)

    snapshot_path = tmp_path / "snapshot.json"
    fixtures_dir = tmp_path / "fixtures"

    assert cli.main(["snapshot", "--output", str(snapshot_path)]) == 0
    assert (
        cli.main(
            [
                "render-fixtures",
                "--snapshot",
                str(snapshot_path),
                "--fixtures-dir",
                str(fixtures_dir),
            ]
        )
        == 0
    )

    rendered = (fixtures_dir / "desktop-01.md").read_text(encoding="utf-8")
    assert "Desktop 01 - SSH 1: sample" in rendered
    assert "Visible content sources:" in rendered
