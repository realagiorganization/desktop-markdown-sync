from __future__ import annotations

import configparser
import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from .models import DesktopState, WindowState


class CommandRunner(Protocol):
    def __call__(
        self, args: list[str], *, check: bool = True
    ) -> subprocess.CompletedProcess[str]: ...


def _default_runner(args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, check=check, text=True, capture_output=True)


@dataclass(slots=True)
class PlasmaDesktopBackend:
    runner: CommandRunner = _default_runner
    home: Path = Path(os.environ.get("HOME", "~")).expanduser()

    def capture_state(self) -> list[DesktopState]:
        desktops = self._parse_wmctrl_desktops(self._run_stdout(["wmctrl", "-d"]))
        windows = self._parse_wmctrl_windows(self._run_stdout(["wmctrl", "-l", "-x"]))
        for desktop in desktops:
            desktop.windows.extend(windows.get(desktop.desktop_index - 1, []))
        return desktops

    def apply_state(self, desktops: list[DesktopState]) -> None:
        self._set_desktop_count(len(desktops))
        self._set_desktop_names(desktops)
        for desktop in desktops:
            for window in desktop.windows:
                if window.command:
                    self._launch_command(window.command)
            if desktop.current:
                self._set_current_desktop(desktop.desktop_index)

    def skill_path(self) -> Path:
        return (
            Path(__file__).resolve().parents[2]
            / "skills"
            / "desktop-markdown-sync-reconcile"
            / "SKILL.md"
        )

    def _run_stdout(self, args: list[str]) -> str:
        return self.runner(args).stdout

    def _set_desktop_count(self, count: int) -> None:
        self.runner(["wmctrl", "-n", str(max(count, 1))])

    def _set_current_desktop(self, index: int) -> None:
        binary = shutil.which("qdbus6") or shutil.which("qdbus")
        if not binary:
            return
        self.runner([binary, "org.kde.KWin", "/KWin", "org.kde.KWin.setCurrentDesktop", str(index)])

    def _set_desktop_names(self, desktops: list[DesktopState]) -> None:
        kwriteconfig = shutil.which("kwriteconfig6") or shutil.which("kwriteconfig5")
        if not kwriteconfig:
            return
        config_path = self.home / ".config" / "kwinrc"
        parser = configparser.ConfigParser(strict=False)
        parser.optionxform = str
        if config_path.exists():
            parser.read(config_path, encoding="utf-8")
        if not parser.has_section("Desktops"):
            parser.add_section("Desktops")
        parser.set("Desktops", "Number", str(len(desktops)))
        for desktop in desktops:
            parser.set("Desktops", f"Name_{desktop.desktop_index}", desktop.desktop_name)
        with config_path.open("w", encoding="utf-8") as handle:
            parser.write(handle)
        binary = shutil.which("qdbus6") or shutil.which("qdbus")
        if binary:
            self.runner([binary, "org.kde.KWin", "/KWin", "reconfigure"])

    def _launch_command(self, command: str) -> None:
        subprocess.Popen(  # noqa: S603
            ["bash", "-lc", f"nohup {command} >/dev/null 2>&1 &"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    @staticmethod
    def _parse_wmctrl_desktops(text: str) -> list[DesktopState]:
        desktops: list[DesktopState] = []
        for raw_line in text.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            match = re.match(
                r"^(?P<index>\d+)\s+(?P<marker>[*-])\s+DG:\s+\S+\s+VP:\s+\S+\s+WA:\s+\S+\s+\S+\s+(?P<name>.+)$",
                line,
            )
            if not match:
                continue
            desktop_index = int(match.group("index")) + 1
            current = match.group("marker") == "*"
            desktop_name = match.group("name")
            desktops.append(
                DesktopState(
                    desktop_name=desktop_name,
                    desktop_index=desktop_index,
                    current=current,
                )
            )
        return desktops

    @staticmethod
    def _parse_wmctrl_windows(text: str) -> dict[int, list[WindowState]]:
        windows: dict[int, list[WindowState]] = {}
        for raw_line in text.splitlines():
            line = raw_line.rstrip()
            if not line:
                continue
            parts = line.split(None, 4)
            if len(parts) < 5:
                continue
            window_id, desktop_index_raw, _host, wm_class, title = parts
            if desktop_index_raw == "-1":
                continue
            desktop_index = int(desktop_index_raw)
            windows.setdefault(desktop_index, []).append(
                WindowState(title=title, wm_class=wm_class, window_id=window_id)
            )
        return windows
