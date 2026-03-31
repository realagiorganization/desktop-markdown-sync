from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from .models import DesktopState


@dataclass(slots=True)
class CodexReconcileResult:
    attempted: bool
    returncode: int | None
    stdout: str = ""
    stderr: str = ""


def build_prompt(
    markdown_path: Path,
    markdown_text: str,
    desktops: list[DesktopState],
    skill_path: Path,
) -> str:
    desktop_json = json.dumps([desktop.to_dict() for desktop in desktops], indent=2, sort_keys=True)
    return (
        "Use the desktop-markdown-sync reconciliation skill at "
        f"{skill_path}.\n\n"
        f"Markdown file changed: {markdown_path}\n\n"
        "Current live desktop snapshot:\n"
        f"{desktop_json}\n\n"
        "Changed markdown contents:\n"
        f"{markdown_text}\n\n"
        "Return a concise restore plan, then apply only safe local changes."
    )


def maybe_run_codex(
    codex_bin: str,
    markdown_path: Path,
    markdown_text: str,
    desktops: list[DesktopState],
    skill_path: Path,
) -> CodexReconcileResult:
    binary = shutil.which(codex_bin)
    if not binary:
        return CodexReconcileResult(attempted=False, returncode=None)
    prompt = build_prompt(markdown_path, markdown_text, desktops, skill_path)
    completed = subprocess.run(
        [binary, "exec", prompt],
        text=True,
        capture_output=True,
        check=False,
    )
    return CodexReconcileResult(
        attempted=True,
        returncode=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
    )
