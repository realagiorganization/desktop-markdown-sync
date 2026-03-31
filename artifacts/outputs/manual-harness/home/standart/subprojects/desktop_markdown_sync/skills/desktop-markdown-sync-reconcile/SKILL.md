# desktop-markdown-sync reconcile

Use this skill when a Markdown desktop file changed and the local Kali Plasma desktop state now needs a safe reconstitution plan.

## Goal

- compare the changed Markdown desktop specification against the live desktop snapshot
- prefer safe changes first: desktop names, current-desktop selection, and launch commands explicitly present in Markdown
- avoid destructive window-management actions unless the user asked for them

## Inputs

- the changed Markdown file
- the current live desktop snapshot JSON
- the local repository scripts and docs in this subproject

## Required behavior

1. Summarize the drift between Markdown intent and current desktop state.
2. Propose the smallest safe restore plan.
3. Apply only safe local changes if asked to execute.
4. Keep the Markdown file as the source of truth when the user explicitly edited it.

