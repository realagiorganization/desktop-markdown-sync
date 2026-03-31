# desktop-markdown-sync

[![CI](https://github.com/realagiorganization/desktop-markdown-sync/actions/workflows/ci.yml/badge.svg)](https://github.com/realagiorganization/desktop-markdown-sync/actions/workflows/ci.yml)
[![Package](https://img.shields.io/badge/package-Kali%20.deb-557C94)](https://github.com/realagiorganization/desktop-markdown-sync/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)

`desktop-markdown-sync` is a standalone Kali Linux subproject that keeps KDE Plasma virtual desktops and Markdown descriptions aligned in both directions.

The repo now has two complementary modes:

- sync mode: export live desktops into machine-readable Markdown and apply edited Markdown back onto the desktop
- fixture mode: capture richer text-only fixture files with KWin metadata, layout notes, OCR hooks, and accessibility follow-up

## Core workflow

1. `desktop-markdown-sync export` snapshots live virtual desktop state into Markdown files.
2. `desktop-markdown-sync daemon` watches for drift and applies edited Markdown back onto Plasma.
3. `desktop-markdown-sync snapshot --output ...` emits richer JSON for fixture generation.
4. `desktop-markdown-sync render-fixtures --snapshot ... --fixtures-dir fixtures` turns that snapshot into one Markdown fixture per desktop.

## Repository contents

- `src/desktop_markdown_sync/`: sync daemon, KWin/Plasma backend, snapshot, and rendering code
- `skills/desktop-markdown-sync-reconcile/`: Codex skill for safe Markdown-to-desktop reconciliation
- `skills/desktop-window-fixture-ocr/`: Codex skill for richer screenshot/OCR/accessibility fixture refreshes
- `packaging/`: systemd user service and `.deb` packaging assets
- `docker/Dockerfile`: container smoke path for the fixture tooling

## Main commands

```bash
make install-dev
make verify
make build-deb
make predictive-build-test-all
make docker-test
make act-run
```

## Notes

- Runtime reconstruction is intentionally best effort. Desktop names, current-desktop selection, and explicit launch commands are safe/default paths.
- The fixture/OCR path is text-first and does not commit screenshots by default.
