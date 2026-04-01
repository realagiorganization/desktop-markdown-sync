from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class SyncConfig:
    markdown_dir: Path
    state_dir: Path
    poll_seconds: float = 5.0
    codex_bin: str = "codex"
    enable_codex_reconcile: bool = True

    def __post_init__(self) -> None:
        self.markdown_dir = Path(self.markdown_dir).expanduser()
        self.state_dir = Path(self.state_dir).expanduser()
        if self.poll_seconds <= 0:
            raise ValueError("poll_seconds must be > 0")
        if not self.codex_bin.strip():
            raise ValueError("codex_bin must not be blank")

    @classmethod
    def from_env(cls) -> SyncConfig:
        home = Path(os.environ.get("HOME", "~")).expanduser()
        markdown_dir = Path(
            os.environ.get("DMS_MARKDOWN_DIR", home / "Documents" / "desktop-markdown-sync")
        ).expanduser()
        state_dir = Path(
            os.environ.get("DMS_STATE_DIR", home / ".local" / "state" / "desktop-markdown-sync")
        ).expanduser()
        poll_seconds = float(os.environ.get("DMS_POLL_SECONDS", "5"))
        codex_bin = os.environ.get("DMS_CODEX_BIN", "codex")
        enable_codex_reconcile = (
            os.environ.get("DMS_ENABLE_CODEX_RECONCILE", "true").strip().lower() != "false"
        )
        return cls(
            markdown_dir=markdown_dir,
            state_dir=state_dir,
            poll_seconds=poll_seconds,
            codex_bin=codex_bin,
            enable_codex_reconcile=enable_codex_reconcile,
        )
