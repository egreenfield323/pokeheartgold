#!/usr/bin/env python3
"""Apply the Hood HeartGold reskin to the decomp's source data.

Run from the repo root:  python hood/apply_hood.py
Re-running is safe only on clean files (it maps ORIGINAL names to hood names),
so do `git checkout -- files/` first if you edit the data and want to re-apply.
"""
import json
import random
import re
import struct
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "hood" / "data"
MSG = ROOT / "files" / "msgdata" / "msg"

ERRORS = []

# ---------------------------------------------------------------- charmap

def load_charmap():
    chars = set()
    for line in (ROOT / "charmap.txt").read_text(encoding="utf-8").splitlines():
        line = line.split("//")[0].rstrip("\n")
        m = re.match(r"\s*[0-9A-Fa-f]{4}=(.+)$", line)
        if m and len(m.group(1)) == 1:
            chars.add(m.group(1))
    chars.add(" ")
    return chars

CHARMAP = load_charmap()


def fix_quotes(s):
    return s.replace("'", "’")


def strip_markup(s):
    s = re.sub(r"\{[^}]*\}", "", s)
    return s.replace("\\n", "\n").replace("\\r", "\n").replace("\\f", "\n")


def check_text(s, where, max_line=None):
    plain = strip_markup(s)
    bad = sorted({c for c in plain if c not in CHARMAP and c != "\n"})
    if bad:
        ERRORS.append(f"{where}: characters not in charmap: {bad!r}")
    if max_line:
        for ln in plain.split("\n"):
            if len(ln) > max_line:
                ERRORS.append(f"{where}: line too long ({len(ln)}>{max_line}): {ln!r}")


def wrap(text, width=34, end="\\r"):
    """Auto-format prose: '|' separates paragraphs; two lines per box."""
    paras = []
    for para in fix_quotes(text).split("|"):
        lines = textwrap.wrap(para.strip(), width) or [""]
        out = lines[0]
        for i, ln in enumerate(lines[1:], 1):
            out += ("\\n" if i % 2 == 1 else "\\f") + ln
        paras.append(out)
    return "\\r".join(paras) + end

# ---------------------------------------------------------------- gmm banks

ROW_RE = re.compile(r'(<row id="[^"]*" index="(\d+)">.*?<language name="English">)(.*?)(</language>)', re.S)


def xml_unescape(s):
    return s.replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"').replace("&amp;", "&")


def xml_escape(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class Bank:
    cache = {}

    def __init__(self, name):
        matches = list(MSG.glob(name + ".gmm")) or list(MSG.glob(name + "_*.gmm"))
        assert len(matches) == 1, name
        self.path = matches[0]
        self.src = self.path.read_text(encoding="utf-8")
        self.rows = {int(m.group(2)): xml_unescape(m.group(3)) for m in ROW_RE.finditer(self.src)}
        self.dirty = False

    @classmethod
    def get(cls, name):
        if name not in cls.cache:
            cls.cache[name] = Bank(name)
        return cls.cache[name]

    def set(self, idx, text, max_line=None):
        assert idx in self.rows, (self.path.name, idx)
        check_text(text, f"{self.path.name}[{idx}]", max_line)
        self.rows[idx] = text
        self.dirty = True

    def find(self, text):
        return [i for i, t in self.rows.items() if t == text]

    def save(self):
        if not self.dirty:
            return
        def sub(m):
            return m.group(1) + xml_escape(self.rows[int(m.group(2))]) + m.group(4)
        self.path.write_text(ROW_RE.sub(sub, self.src), encoding="utf-8", newline="\n")

    @classmethod
    def save_all(cls):
        for b in cls.cache.values():
            b.save()


def load(name):
    d = json.loads((DATA / name).read_text(encoding="utf-8"))
    return {k: v for k, v in d.items() if not k.startswith("_")}


def article(word):
    return "an" if word[:1].upper() in "AEIOU" else "a"

# ---------------------------------------------------------------- species

def apply_species():
    names = load("species.json")
    caps, art = Bank.get("msg_0237"), Bank.get("msg_0238")
    extra = [Bank.get("msg_0817"), Bank.get("msg_0820")]
    index = {}
    for old, new in names.items():
        new = fix_quotes(new)
        if len(new) > 10:
            ERRORS.append(f"species {old}: {new!r} is longer than 10")
        hits = caps.find(old)
        if not hits:
            ERRORS.append(f"species {old}: not found in msg_0237")
            continue
        i = hits[0]
        index[old] = i
        caps.set(i, new)
        art.set(i, f"{article(new)} {{COLOR 255}}{new}{{COLOR 0}}")
        for b in extra:
            if b.rows.get(i) == old:
                b.set(i, new)
    return index

# ---------------------------------------------------------------- moves

def apply_moves():
    moves = load("moves.json")
    names, caps, used = Bank.get("msg_0750"), Bank.get("msg_0751"), Bank.get("msg_0003_EVERYWHERE")
    ids = {}
    for old, new in moves.items():
        new = fix_quotes(new)
        if len(new) > 12:
            ERRORS.append(f"move {old}: {new!r} is longer than 12")
        hits = names.find(old)
        if not hits:
            ERRORS.append(f"move {old}: not found in msg_0750")
            continue
        m = hits[0]
        ids[old] = m
        names.set(m, new)
        caps.set(m, new.upper())
        mon = "{STRVAR_1 1, 0, 0}"
        verb = {0: "hit ’em with", 1: "hit ’em with"}.get(MOVE_CLASS.get(m))
        if verb is None:   # status move: verb-phrase names read as actions, the rest as gear
            verb = "decided to" if new.split()[0] in STATUS_VERBS else "pulled out"
        for k, prefix in enumerate([f"{mon}", f"The opp {mon}", f"The opp’s {mon}"]):
            used.set(3 * m + k, f"{prefix} {verb}\\n{new}!")
    return ids


STATUS_VERBS = {"Hit", "Lace", "Duck", "Squad", "Stay", "Lock", "Talk", "Mean", "Stare", "Run", "Jam", "Get",
                "Hide", "Dip", "Bulk", "Wait", "Pull", "Copy", "Patch", "Sweet", "Beat", "Peep", "Tough", "Pass",
                "Make", "Rise", "Hype", "Turn", "Diss", "Snatch", "Smooth", "Drop", "Yell", "Block", "Nap",
                "Sleep", "Snore", "Rizz", "Flop", "Eat", "Split", "Curse", "Gun", "Mean", "Swagger", "Shmoney",
                "Sharpen", "Bite", "Fake", "Wake", "Clap", "Chase", "Spin", "Grill", "Sing", "Bass", "Smoke",
                "Lights", "Fall", "Scope", "Run", "Last", "Spray", "Shake", "Flash", "Hype", "Mimic", "Reload", "Duck", "Go"}


def _move_classes():
    d = (ROOT / "files/poketool/waza/waza_tbl.narc").read_bytes()
    return {i: d[o + 2] for i, (o, s) in enumerate(narc_files(d)) if s >= 3}


MOVE_CLASS = None

# ---------------------------------------------------------------- items

def apply_items():
    items = load("items.json")
    names, art, plural = Bank.get("msg_0222"), Bank.get("msg_0223"), Bank.get("msg_0224")
    for old, (new, pl) in items.items():
        new, pl = fix_quotes(new), fix_quotes(pl)
        if len(new) > 12:
            ERRORS.append(f"item {old}: {new!r} is longer than 12")
        hits = names.find(old)
        if not hits:
            ERRORS.append(f"item {old}: not found in msg_0222")
            continue
        for i in hits:
            names.set(i, new)
            art.set(i, f"{article(new)} {{COLOR 255}}{new}{{COLOR 0}}")
            plural.set(i, pl)

# ---------------------------------------------------------------- trainer classes

def apply_trainer_classes():
    classes = load("trainer_classes.json")
    names, art = Bank.get("msg_0730"), Bank.get("msg_0731")
    for old, new in classes.items():
        if len(new) > 12:
            ERRORS.append(f"class {old}: {new!r} is longer than 12")
        hits = names.find(old)
        if not hits:
            ERRORS.append(f"class {old}: not found in msg_0730")
        for i in hits:
            names.set(i, new)
            art.set(i, f"{article(new)} {new}")

# ---------------------------------------------------------------- story text

def apply_story():
    story = load("story_text.json")
    for r in story["rows"]:
        Bank.get(r["bank"]).set(r["index"], fix_quotes(r["text"]), max_line=40)
    for r in story["replace"]:
        bank = Bank.get(r["bank"])
        hits = bank.find(fix_quotes(r["find"]))
        if not hits:
            ERRORS.append(f"{r['bank']}: text not found: {r['find']!r}")
        for i in hits if r.get("all") else hits[:1]:
            bank.set(i, fix_quotes(r["text"]), max_line=40)
    for bank_name, brules in story.get("bank_replace", {}).items():
        bank = Bank.get(bank_name)
        for i, t in bank.rows.items():
            new = t
            for r in brules:
                find, rep = fix_quotes(r["find"]), fix_quotes(r["text"])
                if chr(92) + "b" in find:          # word-boundary rule -> regex (no game codes inside)
                    new = re.sub(find, lambda m: rep, new)
                else:                              # literal (may contain \n game codes)
                    new = new.replace(find, rep)
            if new != t:
                bank.set(i, new)
    rules = [(re.compile(r["find"]), r["text"]) for r in story.get("global_replace", []) if "find" in r]
    for path in sorted(MSG.glob("*.gmm")):
        bank = Bank.get(path.stem)
        width = lambda x: max((len(l) for l in strip_markup(x).split(chr(10))), default=0)
        for i, t in bank.rows.items():
            new, limit = t, max(38, width(t))
            for rx, rep in rules:
                cand = rx.sub(rep, new)
                if cand != new and width(cand) > limit:
                    cand = reflow(cand, limit) or new      # re-wrap the box, or skip this swap
                if cand != new:
                    new = cand
            if new != t:
                bank.set(i, new)

def reflow(text, limit):
    """Re-wrap the words inside each text box (lines joined by \\n) so no line exceeds `limit`.
    Box breaks (\\r, \\f) and the number of lines per box are kept. Returns None if it can't fit."""
    BS = chr(92)
    parts = re.split(r"(\\[rf])", text)
    out = []
    for part in parts:
        if part in (BS + "r", BS + "f") or BS + "n" not in part:
            if part not in (BS + "r", BS + "f") and len(strip_markup(part)) > limit:
                return None
            out.append(part)
            continue
        lines = part.split(BS + "n")
        words = " ".join(lines).split(" ")
        rows, cur = [], ""
        for w in words:
            trial = (cur + " " + w).strip()
            if len(strip_markup(trial)) <= limit:
                cur = trial
            else:
                rows.append(cur)
                cur = w
        rows.append(cur)
        if len(rows) > len(lines) or any(len(strip_markup(r)) > limit for r in rows):
            return None
        out.append((BS + "n").join(rows))
    return "".join(out)


# ---------------------------------------------------------------- hand-written dialogue

def head_rows(bank):
    import subprocess
    rel = Bank.get(bank).path.relative_to(ROOT).as_posix()
    src = subprocess.run(["git", "show", f"HEAD:{rel}"], cwd=ROOT, capture_output=True, check=True).stdout.decode("utf-8")
    return {int(m.group(2)): xml_unescape(m.group(3)) for m in ROW_RE.finditer(src)}


def apply_dialogue():
    """hood/data/dialogue/<bank>.json: {row: text}. Tokens and box ending must match the original."""
    BS = chr(92)
    for path in sorted((DATA / "dialogue").glob("*.json")):
        bank = path.stem
        rows = {int(k): v for k, v in json.loads(path.read_text(encoding="utf-8")).items() if not k.startswith("_")}
        orig = head_rows(bank)
        for i, text in rows.items():
            text = text.replace(chr(10), BS + "n").replace(chr(13), BS + "r").replace(chr(12), BS + "f")
            text = fix_quotes(text)
            o = orig.get(i)
            if o is None:
                ERRORS.append(f"{bank}[{i}]: no such row")
                continue
            tok = lambda t: sorted(x for x in re.findall(r"\{[^}]*\}", t) if not x.startswith("{COLOR"))
            if tok(o) != tok(text):
                ERRORS.append(f"{bank}[{i}]: tokens differ: {tok(o)} vs {tok(text)}")
            for end in (BS + "r", BS + "n", BS + "f"):
                if text.endswith(end) and not o.endswith(end):
                    text = text[:-2]
            for end in (BS + "r", BS + "n", BS + "f"):
                if o.endswith(end) and not text.endswith(end):
                    text += end
            Bank.get(bank).set(i, text, max_line=38)


# ---------------------------------------------------------------- trainers.json

def apply_trainers():
    dlg = load("trainer_dialogue.json")
    pools, class_intros = dlg["pools"], dlg["class_intros"]
    named = {k: v for k, v in dlg["named"].items() if not k.startswith("_")}
    always = set(dlg.get("class_always", []))
    class_lines = {"TRMSG_INTRO": class_intros,
                   "TRMSG_LOSE": dlg.get("class_lose", {}),
                   "TRMSG_AFTER": dlg.get("class_after", {})}
    renames = dlg.get("rename_trainers", {})
    path = ROOT / "files/poketool/trainer/trainers.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    # msg_0728 is the in-game copy of these lines; trtbl maps each of its rows to (trainer, type)
    TYPES = ["TRMSG_INTRO", "TRMSG_LOSE", "TRMSG_AFTER", "TRMSG_DBL_INTRO_1", "TRMSG_DBL_LOSE_1",
             "TRMSG_DBL_AFTER_1", "TRMSG_DBL_1POKE_1", "TRMSG_DBL_INTRO_2", "TRMSG_DBL_LOSE_2",
             "TRMSG_DBL_AFTER_2", "TRMSG_DBL_1POKE_2", None, None, "TRMSG_HIT_POKE_FIRST_TIME",
             "TRMSG_CURRENT_POKE_HALF", "TRMSG_LAST_POKE", "TRMSG_LAST_POKE_HALF", "TRMSG_PHONE_REMATCH_INTRO",
             "TRMSG_PHONE_REMATCH_DBL_INTRO_1", "TRMSG_PHONE_REMATCH_DBL_INTRO_2", "TRMSG_WIN"]
    tbl = (ROOT / "files/poketool/trmsg/trtbl.narc").read_bytes()
    off, size = narc_files(tbl)[0]
    row_of = {}
    for r in range(size // 4):
        tr, ty = struct.unpack_from("<HH", tbl, off + 4 * r)
        row_of[(tr, TYPES[ty])] = r
    bank = Bank.get("msg_0728")
    for n, t in enumerate(data["trainers"]):
        rng = random.Random(n)
        name = t["name"].replace("{TRNAME}", "")
        if name in renames:
            t["name"] = "{TRNAME}" + renames[name]
        cls = t["class"]
        for msg in t["messages"]:
            typ, orig = msg["type"], msg["message"]
            end = "\\r" if orig.endswith("\\r") else "\\n"
            own = class_lines.get(typ, {}).get(cls)
            if name in named and typ in named[name]:
                line = named[name][typ]
            elif own and (cls in always or rng.random() < 0.6):
                line = rng.choice(own)
            elif typ in pools:
                line = rng.choice(pools[typ])
            else:
                continue
            msg["message"] = wrap(line, end=end)
            check_text(msg["message"], f"trainer {n} {name} {typ}", max_line=40)
            if (n, typ) in row_of:
                bank.set(row_of[(n, typ)], msg["message"])
            else:
                ERRORS.append(f"trainer {n} {typ}: no msg_0728 row")
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")

# ---------------------------------------------------------------- stats

STARTER_LINES = ["CHIKORITA", "BAYLEEF", "MEGANIUM", "CYNDAQUIL", "QUILAVA",
                 "TYPHLOSION", "TOTODILE", "CROCONAW", "FERALIGATR"]
AR_LINE = ["LARVITAR", "PUPITAR", "TYRANITAR"]


def apply_stats():
    path = ROOT / "files/poketool/personal/personal.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    by_name = {s["species"]: s for s in data["baseStats"]}
    for sp in STARTER_LINES:
        s = by_name[sp]
        for k in ("hp", "atk", "def", "speed", "spatk", "spdef"):
            s[k] = min(255, round(s[k] * 1.2))  # starters pack better heat: +20% stats
    for sp in AR_LINE:
        by_name[sp]["types"] = ["TYPE_STEEL", "TYPE_DARK"]
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")

# ---------------------------------------------------------------- learnsets (wotbl.narc)

def narc_files(buf):
    """Return (offset, size) of each member of a NARC, relative to the file."""
    assert buf[:4] == b"NARC"
    hdr = struct.unpack_from("<H", buf, 12)[0]
    assert buf[hdr:hdr + 4] == b"BTAF"
    fatb_size, count = struct.unpack_from("<IH", buf, hdr + 4)
    fat = [struct.unpack_from("<II", buf, hdr + 12 + 8 * i) for i in range(count)]
    fntb = hdr + fatb_size
    fntb_size = struct.unpack_from("<I", buf, fntb + 4)[0]
    fimg = fntb + fntb_size
    assert buf[fimg:fimg + 4] == b"GMIF"
    return [(fimg + 8 + a, b - a) for a, b in fat]


def apply_learnsets(species_idx, move_ids):
    """Give the AR15 line FMJ / Reload / Hollow Point / Steel Core (in place, same size)."""
    path = ROOT / "files/poketool/personal/wotbl.narc"
    buf = bytearray(path.read_bytes())
    files = narc_files(buf)
    swaps = {  # original move -> gun move, levels unchanged
        "Bite": "Tackle",        # FMJ at Lv.1
        "Leer": "Recover",       # Reload at Lv.1
        "Screech": "Crunch",     # Hollow Point
        "Rock Slide": "Iron Head",  # Steel Core
    }
    all_moves = {n: i for i, n in Bank.get("msg_0750").rows.items()}
    orig_ids = {name: move_ids.get(name) or all_moves[name] for name in list(swaps) + list(swaps.values())}
    for sp in AR_LINE:
        off, size = files[species_idx.get(sp) or Bank.get("msg_0237").find(sp)[0]]
        done = set()
        for p in range(off, off + size - 1, 2):
            v = struct.unpack_from("<H", buf, p)[0]
            if v == 0xFFFF:
                break
            lvl, mv = v >> 9, v & 0x1FF
            for old, new in swaps.items():
                if mv == orig_ids[old] and old not in done:
                    struct.pack_into("<H", buf, p, (lvl << 9) | orig_ids[new])
                    done.add(old)
        missing = set(swaps) - done
        if missing:
            ERRORS.append(f"learnset {sp}: did not find {sorted(missing)}")
    path.write_bytes(bytes(buf))

# ---------------------------------------------------------------- main

def main():
    global MOVE_CLASS
    MOVE_CLASS = _move_classes()
    species_idx = apply_species()
    move_ids = apply_moves()
    apply_items()
    apply_trainer_classes()
    apply_story()
    apply_dialogue()
    if ERRORS:
        print("\n".join(ERRORS))
        sys.exit("Aborted: fix the data above. Nothing was written.")
    apply_trainers()
    apply_stats()
    apply_learnsets(species_idx, move_ids)
    if ERRORS:
        print("\n".join(ERRORS))
        sys.exit("Errors after writing trainers/stats; check git diff.")
    Bank.save_all()
    print(f"Hood mod applied: {len(Bank.cache)} message banks, trainers, stats, learnsets.")


if __name__ == "__main__":
    main()
