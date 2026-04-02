from __future__ import annotations

from pathlib import Path
from typing import TypeAlias

from .fixture_notes import desktop_note_for

DesktopPayload: TypeAlias = dict[str, object]
WindowPayload: TypeAlias = dict[str, object]


def _require_mapping_field(mapping: DesktopPayload | WindowPayload, field_name: str) -> object:
    if field_name not in mapping:
        raise KeyError(f"missing required field: {field_name}")
    return mapping[field_name]


def _normalize_sources(value: object) -> tuple[str, ...]:
    if isinstance(value, tuple) and all(isinstance(item, str) for item in value):
        return value
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return tuple(value)
    if isinstance(value, str):
        return (value,)
    raise TypeError("sources must be a string sequence")


def _format_sources(sources: tuple[str, ...]) -> str:
    return ", ".join(f"`{source}`" for source in sources)


def _window_lines(window: WindowPayload) -> list[str]:
    info = _require_mapping_field(window, "info")
    if not isinstance(info, dict):
        raise TypeError("window info must be a dictionary")
    title = _require_mapping_field(window, "title")
    if not isinstance(title, str):
        raise TypeError("window title must be a string")
    window_class = info.get("resourceClass", "unknown")
    desktop_file = info.get("desktopFile", "unknown")
    geometry = (
        f"{int(info.get('x', 0))},{int(info.get('y', 0))} "
        f"{int(info.get('width', 0))}x{int(info.get('height', 0))}"
    )
    state = []
    if info.get("fullscreen"):
        state.append("fullscreen")
    if info.get("minimized"):
        state.append("minimized")
    if info.get("keepAbove"):
        state.append("keep-above")
    state_text = ", ".join(state) if state else "normal"
    content_hint = infer_content_hint(title=title, window_class=window_class)
    return [
        f"- Title: `{title}`",
        f"- Class: `{window_class}`",
        f"- Desktop file: `{desktop_file}`",
        f"- Geometry: `{geometry}`",
        f"- State: `{state_text}`",
        f"- Content hint: {content_hint}",
    ]


def infer_content_hint(*, title: str, window_class: str) -> str:
    lowered_title = title.lower()
    if "discord" in lowered_title:
        return (
            "Discord workspace window; the title points at the `#main` channel "
            "in the Real AGI Corp. server."
        )
    if "firefox" in lowered_title:
        return (
            "Firefox browser window; page content is not encoded in the title, "
            "so treat it as a browser surface requiring OCR or accessibility "
            "follow-up."
        )
    if "visual studio code" in lowered_title or "desktop_markdown_sync" in lowered_title:
        return "VS Code workspace window focused on this subproject."
    if any(token in lowered_title for token in ["konsole", "kitty", "terminal", "tmux"]):
        return (
            "Terminal session. The reliable semantic content comes from the "
            "title and any visible prompt text captured in the fixture notes."
        )
    if "remmina" in window_class.lower():
        return "Remote desktop session managed by Remmina."
    if "xwaylandvideobridge" in lowered_title:
        return "Auxiliary Xwayland bridge helper; not user-authored workspace content."
    return (
        "Generic desktop application window; use OCR or accessibility follow-up for finer labels."
    )


def render_fixture(desktop: DesktopPayload) -> str:
    desktop_index = _require_mapping_field(desktop, "desktop_index")
    desktop_id = _require_mapping_field(desktop, "desktop_id")
    desktop_name = _require_mapping_field(desktop, "desktop_name")
    windows = _require_mapping_field(desktop, "windows")
    if not isinstance(desktop_index, int):
        raise TypeError("desktop_index must be an integer")
    if not isinstance(desktop_id, str):
        raise TypeError("desktop_id must be a string")
    if not isinstance(desktop_name, str):
        raise TypeError("desktop_name must be a string")
    if not isinstance(windows, list):
        raise TypeError("windows must be a list")
    notes = desktop_note_for(desktop_index)
    lines = [
        f"# Desktop {desktop_index:02d} - {desktop_name}",
        "",
        f"- Desktop id: `{desktop_id}`",
        f"- Window count: `{len(windows)}`",
        f"- Layout summary: {notes['layout']}",
        f"- Layout sources: {_format_sources(_normalize_sources(notes['layout_sources']))}",
        f"- Visible content summary: {notes['visible']}",
        "- Visible content sources: "
        f"{_format_sources(_normalize_sources(notes['visible_sources']))}",
        "",
        "## Windows",
    ]
    if not windows:
        lines.extend(
            [
                "",
                "No KWin-managed windows were present for this desktop at capture time.",
            ]
        )
    for index, window in enumerate(windows, start=1):
        lines.extend(
            [
                "",
                f"### Window {index}",
                *_window_lines(window),
            ]
        )
    lines.append("")
    return "\n".join(lines)


def write_fixtures(snapshot: list[DesktopPayload], fixtures_dir: Path) -> list[Path]:
    fixtures_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for desktop in snapshot:
        path = fixtures_dir / f"desktop-{desktop['desktop_index']:02d}.md"
        path.write_text(render_fixture(desktop))
        written.append(path)
    return written
