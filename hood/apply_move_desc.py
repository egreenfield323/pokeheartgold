#!/usr/bin/env python3
"""Hood move summaries: hood/data/move_desc.json (original move name -> description) into the move
description bank (msg_0749), word-wrapped to the original's line width and line count. Move indices come
from the unmodded names (base commit), so it can be re-run any time.
Run from the repo root:  python hood/apply_move_desc.py
"""
import json
import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import apply_hood as ah  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def main():
    desc = {k: v for k, v in json.loads((ROOT / "hood/data/move_desc.json").read_text(encoding="utf-8")).items()
            if not k.startswith("_")}
    names = ah.head_rows("msg_0750")
    orig = ah.head_rows("msg_0749")
    index = {v: k for k, v in names.items()}
    width = max(len(line) for t in orig.values() for line in t.split("\\n"))     # 21 in the original
    bank = ah.Bank.get("msg_0749")
    errors = []
    for name, text in desc.items():
        if name not in index:
            errors.append(f"{name}: no such move")
            continue
        lines = textwrap.wrap(ah.fix_quotes(text), width - 1)
        if len(lines) > 5:
            errors.append(f"{name}: {len(lines)} lines (max 5): {text}")
            continue
        bank.set(index[name], "\\n".join(lines))
    if errors:
        sys.exit("\n".join(errors))
    import text_edits                          # hand edits from the drip editor's Text tab win
    text_edits.apply(ah.Bank, only={"msg_0749"})
    bank.save()
    print(f"move summaries: {len(desc)} rewritten")


if __name__ == "__main__":
    main()
