from __future__ import annotations

NOTES_BY_DESKTOP_INDEX = {
    1: {
        "visible": (
            "Foreground terminal text shows `standard@kali-strix1 ~`, a timeout for "
            "`10.100.0.44`, then a second prompt `standard@kali14 ~` with the partial "
            "token `ZEKS_`."
        ),
        "layout": (
            "The desktop behaves like a stacked fullscreen SSH workspace: two Konsole "
            "tmux clients report identical fullscreen geometry and only the top client "
            "is visibly readable."
        ),
    },
    2: {
        "visible": (
            "The visible frame shows a Kali login dialog centered on the screen. The "
            "screenshot suggests a remote login prompt even though the window title "
            "names a Remmina session."
        ),
        "layout": (
            "A fullscreen Remmina window occupies the full desktop and a fullscreen "
            "Konsole tmux client is also present in the stack."
        ),
    },
    3: {
        "visible": (
            "The readable surface is still terminal-first, with the remote host label "
            "in the title bar and the same timeout or prompt residue at the top-left."
        ),
        "layout": (
            "Two fullscreen kitty windows and one fullscreen Konsole client are "
            "stacked at identical geometry, so this desktop is primarily an "
            "overlapped SSH terminal pile rather than a tiled layout."
        ),
    },
    4: {
        "visible": (
            "A small interactive terminal window is visible over a dotted wallpaper "
            "field, which matches the floating `wezterm` client reported by KWin."
        ),
        "layout": (
            "Four fullscreen kitty SSH clients are stacked underneath one floating "
            "`wezterm` window near the center-left."
        ),
    },
    5: {
        "visible": (
            "The desktop is dominated by one fullscreen xfce4-terminal session with "
            "several floating `wezterm` `tmux` windows offset diagonally over it."
        ),
        "layout": (
            "This is the busiest remote-terminal desktop in the capture: one "
            "fullscreen base layer plus six floating terminal overlays in a loose "
            "cascade."
        ),
    },
    6: {
        "visible": (
            "The screenshot shows the Kali wallpaper and application launcher overlay "
            "while the tracked working window is a fullscreen gnome-terminal named "
            "`ssh-kali14`."
        ),
        "layout": (
            "The captured app stack is simple: a single fullscreen gnome-terminal "
            "with the launcher panel over the top at capture time."
        ),
    },
    7: {
        "visible": (
            "The visible frame is mostly black with the KDE application launcher open "
            "on the right, which is consistent with stacked fullscreen terminal "
            "sessions obscuring each other."
        ),
        "layout": (
            "Three fullscreen `main [xfce4-terminal]` windows and one fullscreen "
            "`ssh-kali14 [xfce4-terminal]` window occupy the same origin and size."
        ),
    },
    8: {
        "visible": (
            "No managed application windows were present. The capture reads as "
            "wallpaper-only desktop space."
        ),
        "layout": (
            "Empty desktop reserved as a spacer between the main tmux desktop and "
            "the emulator-specific terminals."
        ),
    },
    9: {
        "visible": (
            "This is the most information-dense desktop: fullscreen qterminal behind "
            "overlapping Firefox, Discord, Konsole, VS Code, and launcher "
            "surfaces. Readable text includes project notes, package-management "
            "output, and an active Codex session panel."
        ),
        "layout": (
            "One fullscreen qterminal anchors the desktop while Discord, Firefox, "
            "Konsole, and VS Code share the right and center portions in "
            "overlapping non-fullscreen windows."
        ),
    },
    10: {
        "visible": "No live cool-retro-term window was tracked during the capture.",
        "layout": "Reserved terminal desktop with no active window content.",
    },
    11: {
        "visible": "No live deepin-terminal window was tracked during the capture.",
        "layout": "Reserved terminal desktop with no active window content.",
    },
    12: {
        "visible": (
            "The visible content matches a fullscreen tmux client terminal with the "
            "same timeout and prompt residue seen on the SSH desktops."
        ),
        "layout": (
            "Single fullscreen Konsole tmux client on a desktop named for `foot`, "
            "indicating the naming plan is ahead of the actual live window "
            "inventory."
        ),
    },
    13: {
        "visible": "No live gnome-terminal window was tracked during the capture.",
        "layout": "Reserved terminal desktop with no active window content.",
    },
    14: {
        "visible": "No live guake window was tracked during the capture.",
        "layout": "Reserved terminal desktop with no active window content.",
    },
    15: {
        "visible": "No live kgx window was tracked during the capture.",
        "layout": "Reserved terminal desktop with no active window content.",
    },
    16: {
        "visible": "No live kitty window was tracked during the capture.",
        "layout": "Reserved terminal desktop with no active window content.",
    },
    17: {
        "visible": "No live konsole window was tracked during the capture.",
        "layout": "Reserved terminal desktop with no active window content.",
    },
    18: {
        "visible": "No live lxterminal window was tracked during the capture.",
        "layout": "Reserved terminal desktop with no active window content.",
    },
    19: {
        "visible": "No live mate-terminal window was tracked during the capture.",
        "layout": "Reserved terminal desktop with no active window content.",
    },
    20: {
        "visible": "No live mlterm window was tracked during the capture.",
        "layout": "Reserved terminal desktop with no active window content.",
    },
}
