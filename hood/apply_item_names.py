#!/usr/bin/env python3
"""Item names from hood/data/items.json into the game text, by item index (so it can be re-run any time, unlike
apply_hood.py, which finds items by their original name and so needs clean files): the name bank (msg_0222),
"a NAME" (msg_0223) and the plural (msg_0224). Hand edits from the drip editor's Text tab are re-applied on top.
Run from the repo root:  python hood/apply_item_names.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import apply_hood as ah  # noqa: E402
import text_edits  # noqa: E402


def main():
    items = ah.load("items.json")
    index = {}
    for i, name in ah.head_rows("msg_0222").items():
        index.setdefault(name, []).append(i)
    names, art, plural = ah.Bank.get("msg_0222"), ah.Bank.get("msg_0223"), ah.Bank.get("msg_0224")
    errors, changed = [], 0
    for old, (new, pl) in items.items():
        new, pl = ah.fix_quotes(new), ah.fix_quotes(pl)
        if len(new) > 12:
            errors.append(f"item {old}: {new!r} is longer than 12")
            continue
        if old not in index:
            errors.append(f"item {old}: no such item")
            continue
        for i in index[old]:
            for bank, text in ((names, new), (art, f"{ah.article(new)} {{COLOR 255}}{new}{{COLOR 0}}"), (plural, pl)):
                if bank.rows.get(i) != text:
                    bank.set(i, text)
                    changed += 1
    if errors or ah.ERRORS:
        sys.exit("\n".join(errors + ah.ERRORS))
    text_edits.apply(ah.Bank, only={"msg_0222", "msg_0223", "msg_0224"})
    ah.Bank.save_all()
    print(f"item names: {len(items)} items, {changed} text rows updated")


if __name__ == "__main__":
    main()
