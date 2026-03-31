from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from .models import DesktopState, WindowState

STATE_BLOCK_RE = re.compile(r"```desktop-state\n(.*?)\n```", re.DOTALL)


def slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.strip().lower())
    return slug.strip("-") or "desktop"


def desktop_path(markdown_dir: Path, desktop: DesktopState) -> Path:
    return markdown_dir / f"{desktop.desktop_index:02d}-{slugify(desktop.desktop_name)}.md"


def render_markdown(desktop: DesktopState) -> str:
    payload = json.dumps(desktop.to_dict(), indent=2, sort_keys=True)
    return (
        f"# Desktop: {desktop.desktop_name}\n\n"
        "Managed by `desktop-markdown-sync`.\n\n"
        "```desktop-state\n"
        f"{payload}\n"
        "```\n"
    )


def parse_markdown(text: str) -> DesktopState:
    match = STATE_BLOCK_RE.search(text)
    if not match:
        raise ValueError("missing ```desktop-state block")
    payload = json.loads(match.group(1))
    return DesktopState(
        desktop_name=payload["desktop_name"],
        desktop_index=int(payload["desktop_index"]),
        current=bool(payload.get("current", False)),
        windows=[
            WindowState(
                title=window.get("title", ""),
                wm_class=window.get("wm_class", ""),
                window_id=window.get("window_id", ""),
                command=window.get("command", ""),
            )
            for window in payload.get("windows", [])
        ],
    )


def write_desktops(markdown_dir: Path, desktops: list[DesktopState]) -> list[Path]:
    markdown_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for desktop in desktops:
        path = desktop_path(markdown_dir, desktop)
        path.write_text(render_markdown(desktop), encoding="utf-8")
        written.append(path)
    return written


def read_desktops(markdown_dir: Path) -> list[DesktopState]:
    desktops: list[DesktopState] = []
    for path in sorted(markdown_dir.glob("*.md")):
        desktops.append(parse_markdown(path.read_text(encoding="utf-8")))
    return desktops


def fingerprint_desktops(desktops: list[DesktopState]) -> str:
    canonical = json.dumps([desktop.to_dict() for desktop in desktops], sort_keys=True)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
