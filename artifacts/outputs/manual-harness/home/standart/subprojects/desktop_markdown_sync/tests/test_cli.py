from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from desktop_markdown_sync.cli import main

SAMPLE_SNAPSHOT = [
    {
        "desktop_index": 1,
        "desktop_id": "desktop-1",
        "desktop_name": "SSH 1: sample",
        "windows": [
            {
                "uuid": "{win-1}",
                "title": "~ : tmux: client — Konsole",
                "icon": "utilities-terminal",
                "subtext": "Activate running window on SSH 1: sample",
                "info": {
                    "resourceClass": "org.kde.konsole",
                    "desktopFile": "org.kde.konsole",
                    "x": 0,
                    "y": 0,
                    "width": 1920,
                    "height": 1200,
                    "fullscreen": True,
                    "minimized": False,
                    "keepAbove": False,
                },
            }
        ],
    },
    {
        "desktop_index": 2,
        "desktop_id": "desktop-2",
        "desktop_name": "Desktop 2",
        "windows": [],
    },
]


class CliTests(unittest.TestCase):
    def test_render_fixtures_writes_one_file_per_desktop(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            snapshot_path = tmp / "snapshot.json"
            fixtures_dir = tmp / "fixtures"
            snapshot_path.write_text(json.dumps(SAMPLE_SNAPSHOT))
            exit_code = main(
                [
                    "render-fixtures",
                    "--snapshot",
                    str(snapshot_path),
                    "--fixtures-dir",
                    str(fixtures_dir),
                ]
            )
            self.assertEqual(exit_code, 0)
            files = sorted(fixtures_dir.glob("desktop-*.md"))
            self.assertEqual(len(files), 2)
            self.assertIn("Window count: `1`", files[0].read_text())
            self.assertIn("No KWin-managed windows were present", files[1].read_text())


if __name__ == "__main__":
    unittest.main()
