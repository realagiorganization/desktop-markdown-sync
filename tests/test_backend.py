from __future__ import annotations

from desktop_markdown_sync.desktop_backend import PlasmaDesktopBackend


def test_parse_wmctrl_desktops() -> None:
    text = (
        "0  * DG: N/A VP: 0,0 WA: 0,0 1920x1080 research notes\n"
        "1  - DG: N/A VP: 0,0 WA: 0,0 1920x1080 chat ops\n"
    )

    desktops = PlasmaDesktopBackend._parse_wmctrl_desktops(text)

    assert [desktop.desktop_name for desktop in desktops] == ["research notes", "chat ops"]
    assert desktops[0].current is True
    assert desktops[1].desktop_index == 2


def test_parse_wmctrl_windows_groups_by_desktop() -> None:
    text = (
        "0x01 0 host firefox.Firefox Docs - Firefox\n"
        "0x02 1 host org.kde.konsole Konsole\n"
        "0x03 -1 host plasmashell.Plasmashell Desktop\n"
    )

    windows = PlasmaDesktopBackend._parse_wmctrl_windows(text)

    assert windows[0][0].wm_class == "firefox.Firefox"
    assert windows[1][0].title == "Konsole"
    assert -1 not in windows
