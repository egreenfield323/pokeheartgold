#!/usr/bin/env python3
"""Everybody you walk in on at home wants to know how you broke into their house (and threatens you).

For every house interior (maps named ..._HOUSE/_HOME/CONDOMINIUMS..., not gatehouses, lighthouses, warehouses or
the player's own house), each person standing in it (an object event whose sprite is a person) gets a new first
text box on the line they open with - the first message in their script - picked from THREATS. Mostly always:
about one in seven is left alone. Every new line goes through text_edits.check (width, lines per box, buffer
size, codes) and is saved through the hand-edit overlay (hood/data/text_edits.json), so it survives re-running
the hood scripts; re-running this is safe (a line that already opens with a threat is skipped).
Run from the repo root:  python hood/apply_house_threats.py [--dry-run]
"""
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_npcs as mn  # noqa: E402
import text_edits as te  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
BS = "\\"
THREATS = [
    "Ayo, how’d you get in my house?!\\nI KNOW I locked that door.",
    "Who let you in?! You got five\\nseconds before I call my cousin.",
    "Breaking and entering, huh?\\nYou picked the wrong crib.",
    "How’d you even get in here?!\\nI keep a bat by the door, bro.",
    "Ain’t nobody invite you in!\\nTouch my TV and it’s over.",
    "Did you just walk in?! This a\\nhouse, not a Poké Center!",
    "Yo, you broke in?! I’m calling\\nthe cops AND my mama.",
    "Bro picked the lock...\\nYou got some nerve, kid.",
    "How you get past the dog?!\\nAight. Hands where I can see ’em.",
    "Uh-uh. Not in MY house.\\nState your business. Quick.",
    "You came through the window,\\ndidn’t you? I see the mud.",
    "Ain’t no way you just walked in\\nhere like you pay rent!",
    "I got cameras, homie. Smile.\\nNow what you want?",
    "Who are you?! Put my remote\\ndown. Slowly. Real slow.",
    "Another one?! Third break-in\\nthis week. I’m moving.",
    "Hold up. HOLD UP. How’d you\\nget in here?! Talk fast.",
]
OPENERS = {t.split(BS + "n")[0] for t in THREATS}
SKIP = re.compile(r"GATEHOUSE|LIGHTHOUSE|WAREHOUSE|PLAYER_HOUSE|EXTERIOR|UNUSED|ELEVATOR")
MSG_RE = re.compile(r"\bmsg_(\d{4})_(\w+?)_(\d{5})\b")


def house_maps():
    """[(map name, map code)] for the house interiors."""
    out = []
    for line in (ROOT / "include/constants/maps.h").read_text().splitlines():
        m = re.match(r"#define MAP_(\w+)\s+\d+\s*//\s*MAP_(\w+)", line)
        if m and re.search(r"HOUSE|HOME|CONDOMINIUMS|MANSION", m.group(1)) and not SKIP.search(m.group(1)):
            out.append((m.group(1), m.group(2)))
    return out


def scripts_of(code):
    """{label: [lines]} of the map's script file."""
    files = list((ROOT / "files/fielddata/script/scr_seq").glob(f"scr_seq_*_{code}.s"))
    if not files:
        return {}
    blocks, cur = {}, None
    for line in files[0].read_text(encoding="utf-8").splitlines():
        m = re.match(r"^(\w+):", line)
        if m:
            cur = m.group(1)
            blocks[cur] = []
        elif cur:
            blocks[cur].append(line)
    return blocks


def first_message(blocks, label, seen=None):
    """(bank number, row) of the first message the script shows (following one GoTo/Call)."""
    seen = seen or set()
    if label in seen or label not in blocks:
        return None
    seen.add(label)
    for line in blocks[label]:
        m = MSG_RE.search(line)
        if m:
            return int(m.group(1)), m.group(2), int(m.group(3))
        j = re.search(r"\b(GoTo|Call|GoToIf\w*|CallIf\w*)\b.*?\b(scr_seq_\w+)", line)
        if j and j.group(1) in ("GoTo", "Call"):
            return first_message(blocks, j.group(2), seen)
        if line.strip() in ("End", "Return"):
            return None
    return None


def targets():
    """{bank: {row}} - the opening lines of the people in every house."""
    people_re = mn.NOT_PEOPLE
    found = {}
    for name, code in house_maps():
        ev = list((ROOT / "files/fielddata/eventdata/zone_event").glob(f"*_{code}.json"))
        if not ev:
            continue
        blocks = scripts_of(code)
        for obj in json.loads(ev[0].read_text(encoding="utf-8")).get("objects", []):
            sprite = obj.get("spriteId", "").replace("SPRITE_", "")
            if people_re.search(sprite) or sprite.startswith(("BALL", "MONSTER", "POKE")):
                continue
            m = re.match(r"_EV_(scr_seq_\w+)", str(obj.get("scriptId", "")))
            hit = m and first_message(blocks, m.group(1))
            if hit:
                bank = f"msg_{hit[0]:04d}_{hit[1]}"
                found.setdefault(bank, set()).add(hit[2])
    return found


def main():
    dry = "--dry-run" in sys.argv
    found = targets()
    edits = te.load_edits()
    names = sorted(found)
    base = te.base_banks(names)
    done = skipped = failed = 0
    for bank in names:
        path = te.MSG / f"{bank}.gmm"
        if not path.exists():
            continue
        cur = te.rows_of(path.read_text(encoding="utf-8"))
        limits = te.Limits(bank, base[bank])
        new_rows = {}
        for row in sorted(found[bank]):
            text = cur.get(row)
            if text is None or any(text.startswith(o) for o in OPENERS):
                continue
            h = int(hashlib.md5(f"{bank}:{row}".encode()).hexdigest(), 16)
            if h % 7 == 0:                                         # mostly always
                skipped += 1
                continue
            new, errors = te.check(bank, base[bank].get(row, ""), text, THREATS[h % len(THREATS)] + BS + "r" + text,
                                   limits)
            if errors:
                failed += 1
                print(f"  skipped {bank}[{row}]: {errors[0]}")
                continue
            new_rows[row] = new
        if new_rows and not dry:
            te.write_rows(bank, new_rows)
            edits.setdefault(bank, {}).update({str(r): t for r, t in new_rows.items()})
        done += len(new_rows)
    if not dry:
        te.save_edits(edits)
    print(f"house threats: {done} lines in {len(names)} houses{' (dry run)' if dry else ''}; {skipped} left alone, "
          f"{failed} didn't fit")


if __name__ == "__main__":
    main()
