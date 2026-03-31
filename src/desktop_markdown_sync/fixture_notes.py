from __future__ import annotations

from collections.abc import Mapping, Sequence

FixtureSources = tuple[str, ...]
FixtureNote = dict[str, str | FixtureSources]

DEFAULT_LAYOUT_SOURCES: FixtureSources = ("kwin-metadata",)
DEFAULT_VISIBLE_SOURCES: FixtureSources = ("kwin-metadata",)


def _sources(*values: str) -> FixtureSources:
    return tuple(values)


NOTES_BY_DESKTOP_INDEX: dict[int, FixtureNote] = {
    1: {
        "visible": "Foreground terminal text shows `standard@kali-strix1 ~`, a timeout for `10.100.0.44`, then a second prompt `standard@kali14 ~` with the partial token `ZEKS_`.",
        "visible_sources": _sources("screenshot", "kwin-metadata"),
        "layout": "The desktop behaves like a stacked fullscreen SSH workspace: two Konsole tmux clients report identical fullscreen geometry and only the top client is visibly readable.",
        "layout_sources": _sources("kwin-metadata", "screenshot"),
    },
    2: {
        "visible": "The visible frame shows a Kali login dialog centered on the screen. The screenshot suggests a remote login prompt even though the window title names a Remmina session.",
        "visible_sources": _sources("screenshot", "kwin-metadata"),
        "layout": "A fullscreen Remmina window occupies the full desktop and a fullscreen Konsole tmux client is also present in the stack.",
        "layout_sources": _sources("kwin-metadata"),
    },
    3: {
        "visible": "The readable surface is still terminal-first, with the remote host label in the title bar and the same timeout/prompt residue at the top-left.",
        "visible_sources": _sources("screenshot", "kwin-metadata"),
        "layout": "Two fullscreen kitty windows and one fullscreen Konsole client are stacked at identical geometry, so this desktop is primarily an overlapped SSH terminal pile rather than a tiled layout.",
        "layout_sources": _sources("kwin-metadata"),
    },
    4: {
        "visible": "A small interactive terminal window is visible over a dotted wallpaper field, which matches the floating `wezterm` client reported by KWin.",
        "visible_sources": _sources("screenshot", "kwin-metadata"),
        "layout": "Four fullscreen kitty SSH clients are stacked underneath one floating `wezterm` window near the center-left.",
        "layout_sources": _sources("kwin-metadata", "screenshot"),
    },
    5: {
        "visible": "The desktop is dominated by one fullscreen xfce4-terminal session with several floating `wezterm` `tmux` windows offset diagonally over it.",
        "visible_sources": _sources("screenshot", "kwin-metadata"),
        "layout": "This is the busiest remote-terminal desktop in the capture: one fullscreen base layer plus six floating terminal overlays in a loose cascade.",
        "layout_sources": _sources("kwin-metadata", "screenshot"),
    },
    6: {
        "visible": "The screenshot shows the Kali wallpaper and application launcher overlay while the tracked working window is a fullscreen gnome-terminal named `ssh-kali14`.",
        "visible_sources": _sources("screenshot", "kwin-metadata"),
        "layout": "The captured app stack is simple: a single fullscreen gnome-terminal with the launcher panel over the top at capture time.",
        "layout_sources": _sources("kwin-metadata", "screenshot"),
    },
    7: {
        "visible": "The visible frame is mostly black with the KDE application launcher open on the right, which is consistent with stacked fullscreen terminal sessions obscuring each other.",
        "visible_sources": _sources("screenshot", "kwin-metadata"),
        "layout": "Three fullscreen `main [xfce4-terminal]` windows and one fullscreen `ssh-kali14 [xfce4-terminal]` window occupy the same origin and size.",
        "layout_sources": _sources("kwin-metadata"),
    },
    8: {
        "visible": "No managed application windows were present. The capture reads as wallpaper-only desktop space.",
        "visible_sources": _sources("kwin-metadata", "screenshot"),
        "layout": "Empty desktop reserved as a spacer between the main tmux desktop and the emulator-specific terminals.",
        "layout_sources": _sources("kwin-metadata"),
    },
    9: {
        "visible": "This is the most information-dense desktop: fullscreen qterminal behind overlapping Firefox, Discord, Konsole, VS Code, and launcher surfaces. Readable text includes project notes, package-management output, and an active Codex session panel.",
        "visible_sources": _sources("screenshot", "kwin-metadata"),
        "layout": "One fullscreen qterminal anchors the desktop while Discord, Firefox, Konsole, and VS Code share the right and center portions in overlapping non-fullscreen windows.",
        "layout_sources": _sources("kwin-metadata", "screenshot"),
    },
    10: {
        "visible": "No live cool-retro-term window was tracked during the capture.",
        "visible_sources": _sources("kwin-metadata"),
        "layout": "Reserved terminal desktop with no active window content.",
        "layout_sources": _sources("kwin-metadata"),
    },
    11: {
        "visible": "No live deepin-terminal window was tracked during the capture.",
        "visible_sources": _sources("kwin-metadata"),
        "layout": "Reserved terminal desktop with no active window content.",
        "layout_sources": _sources("kwin-metadata"),
    },
    12: {
        "visible": "The visible content matches a fullscreen tmux client terminal with the same timeout and prompt residue seen on the SSH desktops.",
        "visible_sources": _sources("screenshot", "kwin-metadata"),
        "layout": "Single fullscreen Konsole tmux client on a desktop named for `foot`, indicating the naming plan is ahead of the actual live window inventory.",
        "layout_sources": _sources("kwin-metadata"),
    },
    13: {
        "visible": "No live gnome-terminal window was tracked during the capture.",
        "visible_sources": _sources("kwin-metadata"),
        "layout": "Reserved terminal desktop with no active window content.",
        "layout_sources": _sources("kwin-metadata"),
    },
    14: {
        "visible": "No live guake window was tracked during the capture.",
        "visible_sources": _sources("kwin-metadata"),
        "layout": "Reserved terminal desktop with no active window content.",
        "layout_sources": _sources("kwin-metadata"),
    },
    15: {
        "visible": "No live kgx window was tracked during the capture.",
        "visible_sources": _sources("kwin-metadata"),
        "layout": "Reserved terminal desktop with no active window content.",
        "layout_sources": _sources("kwin-metadata"),
    },
    16: {
        "visible": "No live kitty window was tracked during the capture.",
        "visible_sources": _sources("kwin-metadata"),
        "layout": "Reserved terminal desktop with no active window content.",
        "layout_sources": _sources("kwin-metadata"),
    },
    17: {
        "visible": "No live konsole window was tracked during the capture.",
        "visible_sources": _sources("kwin-metadata"),
        "layout": "Reserved terminal desktop with no active window content.",
        "layout_sources": _sources("kwin-metadata"),
    },
    18: {
        "visible": "No live lxterminal window was tracked during the capture.",
        "visible_sources": _sources("kwin-metadata"),
        "layout": "Reserved terminal desktop with no active window content.",
        "layout_sources": _sources("kwin-metadata"),
    },
    19: {
        "visible": "No live mate-terminal window was tracked during the capture.",
        "visible_sources": _sources("kwin-metadata"),
        "layout": "Reserved terminal desktop with no active window content.",
        "layout_sources": _sources("kwin-metadata"),
    },
    20: {
        "visible": "No live mlterm window was tracked during the capture.",
        "visible_sources": _sources("kwin-metadata"),
        "layout": "Reserved terminal desktop with no active window content.",
        "layout_sources": _sources("kwin-metadata"),
    },
}


def _normalize_sources(raw_value: object, *, default: FixtureSources) -> FixtureSources:
    if raw_value is None:
        return default
    if isinstance(raw_value, str):
        return (raw_value,)
    if isinstance(raw_value, Sequence) and not isinstance(raw_value, (str, bytes)):
        return tuple(str(item) for item in raw_value)
    raise TypeError(f"unsupported fixture source value: {raw_value!r}")


def desktop_note_for(desktop_index: int) -> FixtureNote:
    note = NOTES_BY_DESKTOP_INDEX.get(desktop_index, {})
    if not isinstance(note, Mapping):
        raise TypeError(f"fixture note must be a mapping: {note!r}")
    normalized: FixtureNote = {
        "layout": str(note.get("layout", "No additional manual layout note recorded.")),
        "layout_sources": _normalize_sources(
            note.get("layout_sources"),
            default=DEFAULT_LAYOUT_SOURCES,
        ),
        "visible": str(note.get("visible", "No manual screenshot note recorded.")),
        "visible_sources": _normalize_sources(
            note.get("visible_sources"),
            default=DEFAULT_VISIBLE_SOURCES,
        ),
    }
    return normalized
