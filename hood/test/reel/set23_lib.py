"""Applies one set-23 batch (thirty new move animations, .claude/plans/anim-set23-plan.md) to hood/gunfx.py and
hood/battlefx.py. A batch file calls apply(names, kits_code, scripts_code, table) where
  names        = new kit constants (["MILK23", ...]); they get the next free numbers after LAST_KIT, donor 82
  kits_code    = build_files code for those kits (pk/fin/burst...), inserted before the set 21 block
  scripts_code = the script functions, inserted before `VARIANTS = {`
  table        = {variant: (function name, (KIT, ...), "Original Move Name")}
Re-running a batch that is already in is refused (its first function name is checked)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HELPERS = '''
# ------------------------------------------------------------------ set 23: thirty new moves

_S23_AT = {"player": (64, 140), "enemy": (185, 81)}                # battler centres on screen (attacker side ->)


def _s23(side, who, xy):
    """Screen point (x, y down) -> emit_at offset for the attacker (who 0) / defender (who 1) of this side."""
    other = "enemy" if side == "player" else "player"
    bx, by = _S23_AT[side if who == 0 else other]
    return round(xy[0] - bx), round(by - xy[1])


def _p(side, a, b):
    """a on the player's turn, b on the enemy's."""
    return a if side == "player" else b


def _lerp(a, b, t):
    return round(a[0] + (b[0] - a[0]) * t), round(a[1] + (b[1] - a[1]) * t)


'''


def apply(names, kits_code, scripts_code, table, remap=()):
    gp, bp = ROOT / "hood/gunfx.py", ROOT / "hood/battlefx.py"
    s, bf = gp.read_text(encoding="utf-8"), bp.read_text(encoding="utf-8")
    first = next(iter(table.values()))[0]
    assert f"def {first}(" not in s, "batch already applied"
    for n in names:
        assert not re.search(r"\b" + n + r"\b", s), f"{n} already exists"
    for fn, _, move in table.values():
        assert not re.search(r"^def " + fn + r"\(", s, re.M), fn
        if f'"{move}":' in bf.split("MOVES = {")[1].split("\n}\n")[0]:
            assert move in remap, f"{move} already mapped (pass remap=[...] to move it to the new variant)"
    for v in table:
        assert not re.search(rf"^\s+{v}: ", s, re.M), f"variant {v} taken"
    # constants
    m = re.search(r"^LAST_KIT = (\w+)\n", s, re.M)
    mm = re.findall(rf"(?:range\((\d+), (\d+)\)|^{m.group(1)} = (\d+))", s[:m.start()], re.M)[-1]
    last = int(mm[1]) - 1 if mm[1] else int(mm[2])
    start = last + 1
    line = f"({', '.join(names)},) = range({start}, {start + len(names)})\n" if len(names) > 1 else f"{names[0]} = {start}\n"
    s = s[:m.start()] + line + f"LAST_KIT = {names[-1]}\n" + s[m.end():]
    a = "\nDONOR.update({WHIP21: 82"
    assert s.count(a) == 1
    i = s.index(a) + 1
    s = s[:i] + "DONOR.update({" + ", ".join(f"{n}: 82" for n in names) + "})\n" + s[i:]
    # kits
    anchor = "    # ---- set 21: common-move redo"
    assert s.count(anchor) == 1
    block = kits_code.rstrip("\n") + "\n    SET10_82 += [" + ", ".join(names) + "]\n\n"
    s = s.replace(anchor, block + anchor)
    # scripts
    if "def _s23(" not in s:
        scripts_code = HELPERS + scripts_code
    anchor = "\nVARIANTS = {"
    assert s.count(anchor) == 1
    s = s.replace(anchor, "\n" + scripts_code.strip("\n") + "\n\n" + anchor)
    # tables
    for anchor, rows in (("            298: _smooth_talk,\n", "".join(f"            {v}: {fn},\n" for v, (fn, _, _) in table.items())),
                         ("        298: (TALK21, TALKB21, SIGNS21),\n",
                          "".join(f"        {v}: ({', '.join(k)},),\n" for v, (_, k, _) in table.items()))):
        assert s.count(anchor) == 1, anchor
        s = s.replace(anchor, anchor + rows)
    # battlefx
    a = '"Fury Cutter": 292, "Destiny Bond": 293,\n'
    assert bf.count(a) == 1
    i = bf.index(a) + len(a)
    rows = bf[i:bf.index("}\n", i)]
    add = "    " + ", ".join(f'"{mv}": {v}' for v, (_, _, mv) in table.items() if mv not in remap) + ",\n"
    if add.strip() != ",":
        bf = bf[:i] + rows + add + bf[i + len(rows):]
    for v, (_, _, mv) in table.items():                       # shared moves move to their new variant
        if mv in remap:
            bf, n = re.subn(rf'"{re.escape(mv)}": \d+', f'"{mv}": {v}', bf)
            assert n == 1, mv
    gp.write_text(s, encoding="utf-8", newline="")
    bp.write_text(bf, encoding="utf-8", newline="")
    print(f"set 23: kits {start}-{start + len(names) - 1}, variants {sorted(table)}")
