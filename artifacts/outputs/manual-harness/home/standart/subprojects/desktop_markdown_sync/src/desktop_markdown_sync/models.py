from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass(slots=True)
class WindowState:
    title: str
    wm_class: str = ""
    window_id: str = ""
    command: str = ""

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(slots=True)
class DesktopState:
    desktop_name: str
    desktop_index: int
    current: bool = False
    windows: list[WindowState] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return {
            "desktop_name": self.desktop_name,
            "desktop_index": self.desktop_index,
            "current": self.current,
            "windows": [window.to_dict() for window in self.windows],
        }
