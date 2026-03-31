# desktop-markdown-sync

[![Package](https://github.com/realagiorganization/desktop-markdown-sync/actions/workflows/package.yml/badge.svg)](https://github.com/realagiorganization/desktop-markdown-sync/actions/workflows/package.yml)
[![Quality](https://github.com/realagiorganization/desktop-markdown-sync/actions/workflows/quality.yml/badge.svg)](https://github.com/realagiorganization/desktop-markdown-sync/actions/workflows/quality.yml)
[![Coverage](https://github.com/realagiorganization/desktop-markdown-sync/actions/workflows/coverage.yml/badge.svg)](https://github.com/realagiorganization/desktop-markdown-sync/actions/workflows/coverage.yml)
[![Static Analysis](https://github.com/realagiorganization/desktop-markdown-sync/actions/workflows/static-analysis.yml/badge.svg)](https://github.com/realagiorganization/desktop-markdown-sync/actions/workflows/static-analysis.yml)
[![CodeQL](https://github.com/realagiorganization/desktop-markdown-sync/actions/workflows/codeql.yml/badge.svg)](https://github.com/realagiorganization/desktop-markdown-sync/actions/workflows/codeql.yml)
[![Kali Harness](https://github.com/realagiorganization/desktop-markdown-sync/actions/workflows/kali-harness.yml/badge.svg)](https://github.com/realagiorganization/desktop-markdown-sync/actions/workflows/kali-harness.yml)
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
- `docker/KaliHarness.Dockerfile`: Kali Linux harness with a parent-style `/home/standart` mirror and fixture-pack sync

## Main commands

```bash
make install-dev
make verify
make quality
make coverage
make static-analysis
make build-deb
make predictive-build-test-all
make docker-test
make docker-harness-test
make act-run
```

## Notes

- Runtime reconstruction is intentionally best effort. Desktop names, current-desktop selection, and explicit launch commands are safe/default paths.
- The fixture/OCR path is text-first and does not commit screenshots by default.
- The Kali harness emits `artifacts/outputs/kali-harness/mirror/harness-manifest.json` and records a fixture-pack UI demo video for CI artifact upload.
- `main` is intended to be merge-protected with required status checks for package, quality, coverage, static analysis, Kali harness, and CodeQL.
