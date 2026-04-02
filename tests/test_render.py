from __future__ import annotations

import unittest

from desktop_markdown_sync.fixture_notes import desktop_note_for
from desktop_markdown_sync.render import infer_content_hint, render_fixture


class RenderTests(unittest.TestCase):
    def test_infer_content_hint_for_discord(self) -> None:
        hint = infer_content_hint(title="#main | Real AGI Corp. - Discord", window_class="discord")
        self.assertIn("Discord", hint)

    def test_infer_content_hint_for_terminal(self) -> None:
        hint = infer_content_hint(title="tmux", window_class="org.wezfurlong.wezterm")
        self.assertIn("Terminal", hint)

    def test_render_fixture_includes_note_sources(self) -> None:
        rendered = render_fixture(
            {
                "desktop_index": 1,
                "desktop_id": "desktop-1",
                "desktop_name": "SSH 1: sample",
                "windows": [],
            }
        )

        self.assertIn("- Layout sources: `kwin-metadata`, `screenshot`", rendered)
        self.assertIn("- Visible content sources: `screenshot`, `kwin-metadata`", rendered)

    def test_desktop_note_for_defaults_sources_for_unknown_desktop(self) -> None:
        note = desktop_note_for(999)

        self.assertEqual(note["layout_sources"], ("kwin-metadata",))
        self.assertEqual(note["visible_sources"], ("kwin-metadata",))


if __name__ == "__main__":
    unittest.main()
