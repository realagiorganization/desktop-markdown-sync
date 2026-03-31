# Agent Instructions

- Keep this subproject focused on Markdown plus KDE virtual desktop synchronization for Kali Linux.
- Keep `AGENTS.md`, `readme.md`, and `install.md` present.
- Preserve both operating modes:
  - two-way sync between Plasma desktops and Markdown files
  - richer fixture capture with OCR/accessibility follow-up
- Prefer KWin/Plasma metadata first, then screenshot inspection, then OCR and accessibility enrichment when available.
- Keep helper tooling text-first and repo-friendly; do not commit screenshots or other binary capture artifacts by default.
- Run `make verify` before commits and `make build-deb` before packaging-oriented commits.
