---
name: desktop-window-fixture-ocr
description: Capture or refresh the desktop_markdown_sync fixture set for KDE virtual desktops. Use when the task is to describe each virtual desktop in a separate markdown fixture, combining KWin DBus metadata, screenshot inspection, OCR when available, and AT-SPI accessibility labels via the bundled Rust helper.
---

# Desktop Window Fixture OCR

Use this skill when working inside `/home/standart/subprojects/desktop_markdown_sync`.

## Goal

Produce or refresh a text-only fixture set with exactly one markdown file per live virtual desktop. Each fixture should describe:

- the desktop name and id
- layout shape
- every tracked window on that desktop
- visible content hints from titles, screenshot review, OCR, and accessibility labels

## Workflow

1. Refresh the KWin snapshot:
   `python3 -m desktop_markdown_sync.cli snapshot --output .cache/live-desktop-snapshot.json`
2. If screenshot review is needed, capture desktops with `spectacle` or the repo-native KDE capture path.
3. If OCR is available, run:
   `skills/desktop-window-fixture-ocr/scripts/run_ocr_if_available.sh <image>`
4. If AT-SPI is enabled, query labels and names with the Rust helper:
   `cargo run --manifest-path skills/desktop-window-fixture-ocr/helpers/accessibility-probe/Cargo.toml -- status`
5. Render fixtures:
   `python3 -m desktop_markdown_sync.cli render-fixtures --snapshot .cache/live-desktop-snapshot.json --fixtures-dir fixtures`

## Accessibility helper

The Rust helper is intentionally small and CLI-first. It can:

- report whether the session accessibility bus is enabled
- emit the accessibility bus address
- query `Name`, `Description`, role, and child count from an AT-SPI accessible object when the caller already knows the service and object path

## References

- For the fixture format and fallback rules, read `references/fixture-format.md`.
- For scripted snapshot collection, read `scripts/collect_fixture_context.py`.
