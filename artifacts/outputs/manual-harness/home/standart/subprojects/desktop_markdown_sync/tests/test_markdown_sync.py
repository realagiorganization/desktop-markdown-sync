from __future__ import annotations

from desktop_markdown_sync.markdown_sync import (
    desktop_path,
    fingerprint_desktops,
    parse_markdown,
    render_markdown,
    slugify,
)
from desktop_markdown_sync.models import DesktopState, WindowState


def test_render_and_parse_round_trip() -> None:
    desktop = DesktopState(
        desktop_name="Research Notes",
        desktop_index=2,
        current=True,
        windows=[
            WindowState(title="Docs", wm_class="firefox.Firefox", command="firefox https://kde.org")
        ],
    )

    rendered = render_markdown(desktop)
    parsed = parse_markdown(rendered)

    assert parsed.desktop_name == "Research Notes"
    assert parsed.desktop_index == 2
    assert parsed.current is True
    assert parsed.windows[0].command == "firefox https://kde.org"


def test_slugify_and_path_are_deterministic(tmp_path) -> None:
    desktop = DesktopState(desktop_name="Work / Main", desktop_index=1)

    assert slugify("Work / Main") == "work-main"
    assert desktop_path(tmp_path, desktop).name == "01-work-main.md"


def test_fingerprint_changes_when_window_changes() -> None:
    baseline = [DesktopState(desktop_name="A", desktop_index=1, windows=[WindowState(title="one")])]
    changed = [DesktopState(desktop_name="A", desktop_index=1, windows=[WindowState(title="two")])]

    assert fingerprint_desktops(baseline) != fingerprint_desktops(changed)
