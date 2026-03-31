from __future__ import annotations

import json
import re
import subprocess
from collections import defaultdict
from pathlib import Path

WINDOW_MATCH_RE = re.compile(
    (
        r'\(sssida\{sv\}\) "([^"]+)", "([^"]*)", "([^"]*)", '
        r'[^\]]*?"subtext" = \[Variant\(QString\): "([^"]*)"\]'
    ),
    re.S,
)
WINDOW_INFO_RE = re.compile(r'"([^"]+)" = \[Variant\(([^)]+)\): ([^\]]+)\]')
DESKTOP_RE = re.compile(r"\((\d+), '([^']+)', '([^']+)'\)")


def _run(*args: str) -> str:
    return subprocess.check_output(args, text=True)


def _parse_variant(value: str):
    value = value.strip()
    if value in {"true", "false"}:
        return value == "true"
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.startswith("{") and value.endswith("}") and '"' in value:
        return re.findall(r'"([^"]*)"', value)
    try:
        return float(value) if "." in value else int(value)
    except ValueError:
        return value


def collect_snapshot() -> list[dict]:
    raw_matches = _run(
        "qdbus6",
        "--literal",
        "org.kde.KWin",
        "/WindowsRunner",
        "org.kde.krunner1.Match",
        "",
    )
    windows_by_uuid: dict[str, dict] = {}
    for match in WINDOW_MATCH_RE.finditer(raw_matches):
        match_id, title, icon, subtext = match.groups()
        if not match_id.startswith("0_{"):
            continue
        uuid = match_id[2:]
        if uuid in windows_by_uuid:
            continue
        info_raw = _run(
            "qdbus6",
            "--literal",
            "org.kde.KWin",
            "/KWin",
            "org.kde.KWin.getWindowInfo",
            uuid,
        )
        info = {
            key: _parse_variant(value)
            for key, _type_name, value in WINDOW_INFO_RE.findall(info_raw)
        }
        windows_by_uuid[uuid] = {
            "uuid": uuid,
            "title": title,
            "icon": icon,
            "subtext": subtext,
            "info": info,
        }

    raw_desktops = _run(
        "gdbus",
        "introspect",
        "--session",
        "--dest",
        "org.kde.KWin",
        "--object-path",
        "/VirtualDesktopManager",
    )
    desktops_match = re.search(r"desktops = \[(.*)\];", raw_desktops, re.S)
    if desktops_match is None:
        raise RuntimeError("unable to parse desktop metadata from KWin")
    desktops = [
        {
            "desktop_index": int(index) + 1,
            "desktop_id": desktop_id,
            "desktop_name": desktop_name,
        }
        for index, desktop_id, desktop_name in DESKTOP_RE.findall(desktops_match.group(1))
    ]

    grouped: dict[str, list[dict]] = defaultdict(list)
    for window in windows_by_uuid.values():
        desktop_ids = window["info"].get("desktops", [])
        if isinstance(desktop_ids, str):
            desktop_ids = [desktop_ids]
        for desktop_id in desktop_ids:
            grouped[desktop_id].append(window)

    result = []
    for desktop in desktops:
        windows = sorted(
            grouped.get(desktop["desktop_id"], []),
            key=lambda item: (
                int(item["info"].get("layer", 0)),
                int(item["info"].get("y", 0)),
                int(item["info"].get("x", 0)),
                item["title"],
            ),
        )
        result.append({**desktop, "windows": windows})
    return result


def write_snapshot(path: Path) -> Path:
    snapshot = collect_snapshot()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(snapshot, indent=2) + "\n")
    return path


def load_snapshot(path: Path) -> list[dict]:
    return json.loads(path.read_text())
