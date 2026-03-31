from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path

from .codex_reconcile import maybe_run_codex
from .config import SyncConfig
from .desktop_backend import PlasmaDesktopBackend
from .markdown_sync import fingerprint_desktops, parse_markdown, read_desktops, write_desktops


@dataclass(slots=True)
class SyncService:
    config: SyncConfig
    backend: PlasmaDesktopBackend

    def export_once(self) -> list[Path]:
        desktops = self.backend.capture_state()
        written = write_desktops(self.config.markdown_dir, desktops)
        self._write_manifest(fingerprint_desktops(desktops))
        return written

    def apply_once(self) -> None:
        desktops = read_desktops(self.config.markdown_dir)
        self.backend.apply_state(desktops)
        self._write_manifest(fingerprint_desktops(desktops))

    def run_forever(self) -> None:
        self.config.markdown_dir.mkdir(parents=True, exist_ok=True)
        self.config.state_dir.mkdir(parents=True, exist_ok=True)
        last_markdown_mtime = self._markdown_mtime()
        last_fingerprint = self._read_manifest()
        while True:
            desktops = self.backend.capture_state()
            current_fingerprint = fingerprint_desktops(desktops)
            markdown_mtime = self._markdown_mtime()
            if current_fingerprint != last_fingerprint:
                write_desktops(self.config.markdown_dir, desktops)
                last_fingerprint = current_fingerprint
                self._write_manifest(current_fingerprint)
                last_markdown_mtime = self._markdown_mtime()
            elif markdown_mtime > last_markdown_mtime:
                changed_files = sorted(self.config.markdown_dir.glob("*.md"))
                if changed_files and self.config.enable_codex_reconcile:
                    changed_text = changed_files[-1].read_text(encoding="utf-8")
                    maybe_run_codex(
                        self.config.codex_bin,
                        changed_files[-1],
                        changed_text,
                        desktops,
                        self.backend.skill_path(),
                    )
                parsed = [
                    parse_markdown(path.read_text(encoding="utf-8")) for path in changed_files
                ]
                self.backend.apply_state(parsed)
                last_fingerprint = fingerprint_desktops(parsed)
                self._write_manifest(last_fingerprint)
                last_markdown_mtime = markdown_mtime
            time.sleep(self.config.poll_seconds)

    def _manifest_path(self) -> Path:
        return self.config.state_dir / "manifest.json"

    def _write_manifest(self, fingerprint: str) -> None:
        self.config.state_dir.mkdir(parents=True, exist_ok=True)
        self._manifest_path().write_text(json.dumps({"fingerprint": fingerprint}), encoding="utf-8")

    def _read_manifest(self) -> str:
        path = self._manifest_path()
        if not path.exists():
            return ""
        return json.loads(path.read_text(encoding="utf-8")).get("fingerprint", "")

    def _markdown_mtime(self) -> float:
        latest = 0.0
        for path in self.config.markdown_dir.glob("*.md"):
            latest = max(latest, path.stat().st_mtime)
        return latest
