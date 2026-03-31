#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import tkinter as tk
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--cycles", type=int, default=2)
    parser.add_argument("--linger-ms", type=int, default=1200)
    return parser


def pack_preview(pack: dict[str, object]) -> str:
    files = pack.get("files", [])
    preview_lines = [
        f"Pack: {pack['name']}",
        f"File count: {pack['file_count']}",
        f"Target dir: {pack['target_dir']}",
        "",
    ]
    for file_entry in files[:6]:
        preview_lines.append(
            f"- {file_entry['name']}: "
            f"{str(file_entry['source_sha256'])[:12]} -> {str(file_entry['target_sha256'])[:12]}"
        )
    return "\n".join(preview_lines)


def main() -> int:
    args = build_parser().parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    packs = manifest["packs"]

    root = tk.Tk()
    root.title("desktop-markdown-sync harness fixture demo")
    root.geometry("1280x720")
    root.configure(bg="#11151c")

    header = tk.Label(
        root,
        text="Kali Harness Fixture Pack Sync",
        fg="#f4f1de",
        bg="#11151c",
        font=("DejaVu Sans", 28, "bold"),
        pady=16,
    )
    header.pack(fill=tk.X)

    frame = tk.Frame(root, bg="#11151c")
    frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    pack_list = tk.Listbox(
        frame,
        font=("DejaVu Sans Mono", 15),
        bg="#1b2430",
        fg="#e0fbfc",
        activestyle="none",
        width=28,
    )
    pack_list.pack(side=tk.LEFT, fill=tk.Y)

    preview = tk.Text(
        frame,
        font=("DejaVu Sans Mono", 15),
        bg="#0b132b",
        fg="#f8f9fa",
        wrap=tk.WORD,
    )
    preview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(20, 0))

    for pack in packs:
        pack_list.insert(tk.END, f"{pack['name']} ({pack['file_count']})")

    state = {"index": 0, "remaining": args.cycles * max(len(packs), 1)}

    def advance() -> None:
        if state["remaining"] <= 0:
            root.after(300, root.destroy)
            return
        current = packs[state["index"]]
        pack_list.selection_clear(0, tk.END)
        pack_list.selection_set(state["index"])
        pack_list.activate(state["index"])
        preview.delete("1.0", tk.END)
        preview.insert("1.0", pack_preview(current))
        state["index"] = (state["index"] + 1) % len(packs)
        state["remaining"] -= 1
        root.after(args.linger_ms, advance)

    root.after(200, advance)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
