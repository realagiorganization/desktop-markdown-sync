from __future__ import annotations

from dataclasses import asdict, dataclass, field


def _require_str(value: object, *, field_name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string, got {type(value).__name__}")
    return value


@dataclass(slots=True)
class WindowState:
    title: str
    wm_class: str = ""
    window_id: str = ""
    command: str = ""

    def __post_init__(self) -> None:
        self.title = _require_str(self.title, field_name="title")
        self.wm_class = _require_str(self.wm_class, field_name="wm_class")
        self.window_id = _require_str(self.window_id, field_name="window_id")
        self.command = _require_str(self.command, field_name="command")

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(slots=True)
class DesktopState:
    desktop_name: str
    desktop_index: int
    current: bool = False
    windows: list[WindowState] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.desktop_name = _require_str(self.desktop_name, field_name="desktop_name").strip()
        if not self.desktop_name:
            raise ValueError("desktop_name must not be empty")
        if isinstance(self.desktop_index, bool) or not isinstance(self.desktop_index, int):
            raise TypeError("desktop_index must be an integer")
        if self.desktop_index < 1:
            raise ValueError("desktop_index must be >= 1")
        if not isinstance(self.current, bool):
            raise TypeError("current must be a boolean")
        if not isinstance(self.windows, list):
            raise TypeError("windows must be a list of WindowState")
        if not all(isinstance(window, WindowState) for window in self.windows):
            raise TypeError("windows must contain only WindowState values")

    def to_dict(self) -> dict[str, object]:
        return {
            "desktop_name": self.desktop_name,
            "desktop_index": self.desktop_index,
            "current": self.current,
            "windows": [window.to_dict() for window in self.windows],
        }
