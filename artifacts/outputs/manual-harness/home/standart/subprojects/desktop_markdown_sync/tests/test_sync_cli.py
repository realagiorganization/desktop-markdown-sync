from __future__ import annotations

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
