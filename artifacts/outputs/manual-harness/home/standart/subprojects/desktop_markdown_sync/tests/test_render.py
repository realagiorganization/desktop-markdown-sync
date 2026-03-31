from __future__ import annotations

import unittest

from desktop_markdown_sync.render import infer_content_hint


class RenderTests(unittest.TestCase):
    def test_infer_content_hint_for_discord(self) -> None:
        hint = infer_content_hint(title="#main | Real AGI Corp. - Discord", window_class="discord")
        self.assertIn("Discord", hint)

    def test_infer_content_hint_for_terminal(self) -> None:
        hint = infer_content_hint(title="tmux", window_class="org.wezfurlong.wezterm")
        self.assertIn("Terminal", hint)


if __name__ == "__main__":
    unittest.main()
