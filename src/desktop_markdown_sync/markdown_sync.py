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


def validate_desktops(desktops: list[DesktopState]) -> list[DesktopState]:
    seen_indexes: set[int] = set()
    current_count = 0
    for desktop in desktops:
        if desktop.desktop_index in seen_indexes:
            raise ValueError(f"duplicate desktop_index: {desktop.desktop_index}")
        seen_indexes.add(desktop.desktop_index)
        current_count += int(desktop.current)
    if current_count > 1:
        raise ValueError("at most one desktop may be marked current")
    expected_indexes = list(range(1, len(desktops) + 1))
    actual_indexes = sorted(seen_indexes)
    if actual_indexes != expected_indexes:
        raise ValueError(f"desktop indexes must be contiguous starting at 1; got {actual_indexes}")
    return desktops


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
    if not isinstance(payload, dict):
        raise TypeError("desktop-state payload must decode to an object")
    windows = payload.get("windows", [])
    if not isinstance(windows, list):
        raise TypeError("desktop-state windows must be a list")
    return DesktopState(
        desktop_name=str(payload["desktop_name"]),
        desktop_index=int(payload["desktop_index"]),
        current=bool(payload.get("current", False)),
        windows=[
            WindowState(
                title=_window_field(window, "title"),
                wm_class=_window_field(window, "wm_class"),
                window_id=_window_field(window, "window_id"),
                command=_window_field(window, "command"),
            )
            for window in windows
        ],
    )


def _window_field(window: object, field_name: str) -> str:
    if not isinstance(window, dict):
        raise TypeError(f"window entry must be an object, got {type(window).__name__}")
    value = window.get(field_name, "")
    if not isinstance(value, str):
        raise TypeError(f"window field {field_name!r} must be a string")
    return value


def write_desktops(markdown_dir: Path, desktops: list[DesktopState]) -> list[Path]:
    validate_desktops(desktops)
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
    return validate_desktops(desktops)


def fingerprint_desktops(desktops: list[DesktopState]) -> str:
    validate_desktops(desktops)
    canonical = json.dumps([desktop.to_dict() for desktop in desktops], sort_keys=True)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
