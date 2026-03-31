from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD_DIR = ROOT / "dist" / "deb-build"
PKG_ROOT = BUILD_DIR / "desktop-markdown-sync"
VERSION = "0.1.0"


def write_file(path: Path, content: str, mode: int | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    if mode is not None:
        path.chmod(mode)


def main() -> int:
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)

    shutil.copytree(ROOT / "packaging" / "debian", PKG_ROOT)
    shutil.copytree(ROOT / "src", PKG_ROOT / "opt" / "desktop-markdown-sync" / "src")
    shutil.copytree(
        ROOT / "skills",
        PKG_ROOT / "opt" / "desktop-markdown-sync" / "skills",
    )

    write_file(
        PKG_ROOT / "usr" / "bin" / "desktop-markdown-sync",
        (
            "#!/usr/bin/env bash\n"
            "export PYTHONPATH=/opt/desktop-markdown-sync/src${PYTHONPATH:+:$PYTHONPATH}\n"
            'exec /usr/bin/python3 -m desktop_markdown_sync.cli "$@"\n'
        ),
        mode=0o755,
    )

    control = """Package: desktop-markdown-sync
Version: 0.1.0
Section: utils
Priority: optional
Architecture: all
Maintainer: standart <standart@example.com>
Depends: python3, wmctrl
Description: Two-way Markdown and KDE Plasma desktop synchronization
 Watches KDE Plasma virtual desktops and keeps one Markdown file per desktop.
 When Markdown changes externally, the daemon attempts to restore desktop names
 and launch intents back onto the local Kali desktop.
"""
    write_file(PKG_ROOT / "DEBIAN" / "control", control)

    postinst = """#!/usr/bin/env bash
set -euo pipefail
echo "Installed desktop-markdown-sync."
echo "Enable with: systemctl --user enable --now desktop-markdown-sync.service"
"""
    write_file(PKG_ROOT / "DEBIAN" / "postinst", postinst, mode=0o755)

    package_path = ROOT / "dist" / f"desktop-markdown-sync_{VERSION}_all.deb"
    package_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["dpkg-deb", "--root-owner-group", "--build", str(PKG_ROOT), str(package_path)],
        check=True,
    )
    print(package_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
