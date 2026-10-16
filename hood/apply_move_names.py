#!/usr/bin/env python3
"""Move names from hood/data/moves.json into the game text, by move index (so it can be re-run any time, unlike
apply_hood.py, which finds moves by their original name and so needs clean files):
the name bank (msg_0750), the CAPS bank (msg_0751) and the "X hit 'em with Y!" battle lines (msg_0003).
Hand edits from the drip editor's Text tab are re-applied on top.
Run from the repo root:  python hood/apply_move_names.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import apply_hood as ah  # noqa: E402
import text_edits  # noqa: E402


def main():
    moves = ah.load("moves.json")
    index = {v: k for k, v in ah.head_rows("msg_0750").items()}       # original name -> move number
    classes = ah._move_classes()
    names, caps, used = ah.Bank.get("msg_0750"), ah.Bank.get("msg_0751"), ah.Bank.get("msg_0003_EVERYWHERE")
    errors, changed = [], 0
    for old, new in moves.items():
        new = ah.fix_quotes(new)
        if len(new) > 12:
            errors.append(f"move {old}: {new!r} is longer than 12")
            continue
        if old not in index:
            errors.append(f"move {old}: no such move")
            continue
        m = index[old]
        verb = {0: "hit ’em with", 1: "hit ’em with"}.get(classes.get(m))
        if verb is None:   # status move: verb-phrase names read as actions, the rest as gear
            verb = "decided to" if new.split()[0] in ah.STATUS_VERBS else "pulled out"
        mon = "{STRVAR_1 1, 0, 0}"
        want = {(names, m): new, (caps, m): new.upper()}
        for k, prefix in enumerate([f"{mon}", f"The opp {mon}", f"The opp’s {mon}"]):
            want[(used, 3 * m + k)] = f"{prefix} {verb}\\n{new}!"
        for (bank, row), text in want.items():
            if bank.rows.get(row) != text:
                bank.set(row, text)
                changed += 1
    if errors or ah.ERRORS:
        sys.exit("\n".join(errors + ah.ERRORS))
    text_edits.apply(ah.Bank, only={"msg_0750", "msg_0751", "msg_0003_EVERYWHERE"})
    ah.Bank.save_all()
    print(f"move names: {len(moves)} moves, {changed} text rows updated")


if __name__ == "__main__":
    main()
