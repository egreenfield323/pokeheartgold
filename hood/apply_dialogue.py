#!/usr/bin/env python3
"""Write the hand-written hood dialogue (hood/data/dialogue/<bank>.json) into the message banks, without
re-running the whole reskin (apply_hood.py only works on clean files).

Every row goes through the same checks apply_hood.py makes (the original's command tokens, the original's ending
code, lines of at most 38 characters) and through text_edits.check (characters the font has, pixel width, lines
per text box, buffer size). Rows the hand-edit overlay (hood/data/text_edits.json) owns are rewritten there too,
or the overlay would put the old text back; a house-break-in threat (apply_house_threats.py) that opens the old
row is kept in front of the new text.
Run from the repo root:  python hood/apply_dialogue.py [bank ...] [--dry-run]
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import apply_house_threats as aht  # noqa: E402
import text_edits as te  # noqa: E402

DIALOGUE = Path(__file__).resolve().parent / "data" / "dialogue"
BS = "\\"


def tokens(t):
    return sorted(x for x in re.findall(r"\{[^}]*\}", t) if not x.startswith(("{COLOR", "{SIZE")))


def plain_lines(t):
    t = re.sub(r"\{[^}]*\}", "", t)
    return re.split(r"\\[nrf]", t)


def load(bank):
    raw = json.loads((DIALOGUE / f"{bank}.json").read_text(encoding="utf-8"))
    rows = {}
    for k, v in raw.items():
        if k.startswith("_"):
            continue
        rows[int(k)] = v.replace("\n", BS + "n").replace("\r", BS + "r").replace("\f", BS + "f")
    return rows


def gmm_name(name):
    """The bank's .gmm stem: the json may leave off the map suffix (msg_0542 for msg_0542_T20)."""
    hits = list(te.MSG.glob(name + ".gmm")) or list(te.MSG.glob(name + "_*.gmm"))
    if len(hits) != 1:
        sys.exit(f"{name}: no single message bank matches ({[h.stem for h in hits]})")
    return hits[0].stem


def threat_of(text):
    for t in aht.THREATS:
        tt = t.replace("'", "’")
        if text.startswith(tt + BS + "r"):
            return tt
    return None


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    names = args or sorted(p.stem for p in DIALOGUE.glob("*.json"))
    gmm = {n: gmm_name(n) for n in names}                  # msg_0542.json -> msg_0542_T20.gmm
    banks = [gmm[n] for n in names]
    base = te.base_banks(banks)
    edits = te.load_edits()
    errors, written, staged = [], 0, {}
    for name, bank in gmm.items():
        rows = load(name)
        current = te.rows_of((te.MSG / f"{bank}.gmm").read_text(encoding="utf-8"))
        limits = te.Limits(bank, base[bank])
        out = {}
        for i, text in rows.items():
            if i not in base[bank]:
                errors.append(f"{bank}[{i}]: no such row")
                continue
            orig, cur = base[bank][i], current.get(i, "")
            over = edits.get(bank, {}).get(str(i))
            threat = threat_of(over) if over else None
            if threat and not text.startswith(threat):
                text = threat + BS + "r" + text
            if tokens(text) != tokens(orig):
                errors.append(f"{bank}[{i}]: codes differ from the original: {tokens(orig)} vs {tokens(text)}")
            for ln in plain_lines(text):
                if len(ln) > 38:
                    errors.append(f"{bank}[{i}]: line over 38 chars ({len(ln)}): {ln!r}")
            final, errs = te.check(bank, orig, cur, text, limits)
            errors += [f"{bank}[{i}]: {e}" for e in errs]
            out[i] = final
            if over is not None:
                edits[bank][str(i)] = final
        staged[bank] = out
        written += len(out)
    if errors:
        print("\n".join(errors))
        sys.exit(f"{len(errors)} problem(s). Nothing was written.")
    if not dry:
        for bank, out in staged.items():
            te.write_rows(bank, out)
        te.save_edits(edits)
    print(f"dialogue: {written} rows in {len(banks)} banks {'checked' if dry else 'written'}")


if __name__ == "__main__":
    main()
