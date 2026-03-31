from __future__ import annotations

from pathlib import Path

from .fixture_notes import NOTES_BY_DESKTOP_INDEX


def _window_lines(window: dict) -> list[str]:
    info = window["info"]
    title = window["title"]
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


def render_fixture(desktop: dict) -> str:
    notes = NOTES_BY_DESKTOP_INDEX.get(desktop["desktop_index"], {})
    lines = [
        f"# Desktop {desktop['desktop_index']:02d} - {desktop['desktop_name']}",
        "",
        f"- Desktop id: `{desktop['desktop_id']}`",
        f"- Window count: `{len(desktop['windows'])}`",
        (f"- Layout summary: {notes.get('layout', 'No additional manual layout note recorded.')}"),
        (
            "- Visible content summary: "
            f"{notes.get('visible', 'No manual screenshot note recorded.')}"
        ),
        "",
        "## Windows",
    ]
    if not desktop["windows"]:
        lines.extend(
            [
                "",
                "No KWin-managed windows were present for this desktop at capture time.",
            ]
        )
    for index, window in enumerate(desktop["windows"], start=1):
        lines.extend(
            [
                "",
                f"### Window {index}",
                *_window_lines(window),
            ]
        )
    lines.append("")
    return "\n".join(lines)


def write_fixtures(snapshot: list[dict], fixtures_dir: Path) -> list[Path]:
    fixtures_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for desktop in snapshot:
        path = fixtures_dir / f"desktop-{desktop['desktop_index']:02d}.md"
        path.write_text(render_fixture(desktop))
        written.append(path)
    return written
