#!/usr/bin/env python3
"""Hand edits to any in-game text (the drip editor's Text tab), kept safe for the game.

hood/data/text_edits.json = {bank: {row: text}} is an overlay applied LAST, after everything apply_hood.py and
apply_move_desc.py write, so an edit survives re-running them. The editor also writes it straight into the
bank's .gmm so the next ROM build picks it up.

check() is what keeps edits from breaking the game. Against the ORIGINAL text (base commit 77565981b):
  * only characters the game's font/encoder has (charmap.txt); straight quotes become curly ones
  * the same {STRVAR_..}/{YESNO}/{WAIT}/... command tokens as the original (scripts fill those buffers),
    in any order; {COLOR n}/{SIZE n} formatting may be added or removed
  * no line wider (in pixels, the real font's glyph widths) than the bank's widest original line
  * no more lines per text box than the bank's originals use
  * no longer than the bank's buffers take: the longest original row of the bank (string buffers are sized for
    it), 900 for map script banks (expanded into 1024-char buffers), and per row for the banks the game copies
    into fixed arrays without a size check (box names, Frontier names; species names are capped at 10)
  * the row keeps its original ending code (\\r / \\n / \\f / none), rows can't be added or removed, and
    generated banks (trainer names) are read-only
Text the hood scripts already wrote that goes past a limit is allowed to stay that size (it's in the game now).
"""
import json
import re
import struct
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MSG = ROOT / "files/msgdata/msg"
EDITS = ROOT / "hood/data/text_edits.json"
BASE = "77565981b"
BS = "\\"
READ_ONLY = {"msg_0729": "trainer names are generated from the trainer data at build time"}
STRICT_ROWS = {"msg_0024", "msg_0028"}        # copied into fixed u16 arrays with no size check
CAP = {"msg_0237": 10}                         # species names -> 11-unit nickname arrays
FORMAT_TOKENS = {"COLOR", "SIZE", "UNK_FF02"}
SCRIPT_BANK_CAP = 900
TOKEN_PX = 40                                  # a {STRVAR} (a name, a number...) counts as this wide
ROW_RE = re.compile(r'(<row id="[^"]*" index="(\d+)">.*?<language name="English">)(.*?)(</language>)', re.S)
PART_RE = re.compile(r"\\[nrf]|\{[^{}]*\}|\\|.", re.S)


def xml_unescape(s):
    return s.replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"').replace("&amp;", "&")


def xml_escape(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def rows_of(src):
    return {int(m.group(2)): xml_unescape(m.group(3)) for m in ROW_RE.finditer(src)}

# ------------------------------------------------------------------ charmap + font


def load_charmap():
    chars, commands = {}, set()
    for line in (ROOT / "charmap.txt").read_text(encoding="utf-8").splitlines():
        line = line.split("//")[0]
        m = re.match(r"\s*([0-9A-Fa-f]{4})=(.+)$", line)
        if not m:
            continue
        v = m.group(2)
        if len(v) == 1:
            chars.setdefault(v, int(m.group(1), 16))
        elif v.startswith("{") and v.endswith("}"):
            commands.add(v[1:-1].split(" ")[0])
    return chars, commands


CHARS, COMMANDS = load_charmap()
COMMANDS.add("TRNAME")                          # trainer-name marker, handled by the encoder itself
FONT = (ROOT / "files/graphic/font/font_00000000.bin").read_bytes()
_HS, _WSTART, NGLYPHS = struct.unpack_from("<III", FONT)
WIDTHS = list(FONT[_WSTART:_WSTART + NGLYPHS])


def char_px(c):
    code = CHARS.get(c)
    if code is None:
        return 6
    g = code - 1
    return WIDTHS[g] if 0 <= g < NGLYPHS else WIDTHS[427]


def glyph_atlas():
    """All glyphs as a 32-wide grid of 16x16 cells (RGBA): ink, shadow, transparent."""
    from PIL import Image
    im = Image.new("RGBA", (32 * 16, ((NGLYPHS + 31) // 32) * 16), (0, 0, 0, 0))
    px = im.load()
    colors = {1: (56, 56, 64, 255), 2: (200, 200, 208, 255), 3: (232, 232, 232, 255)}
    for i in range(NGLYPHS):
        g = FONT[_HS + i * 64:_HS + i * 64 + 64]
        ox, oy = (i % 32) * 16, (i // 32) * 16
        for t, (tx, ty) in enumerate(((0, 0), (8, 0), (0, 8), (8, 8))):
            for y in range(8):
                for x in range(8):
                    p = (g[t * 16 + y * 2 + x // 4] >> ((x % 4) * 2)) & 3
                    if p in colors:
                        px[ox + tx + 7 - x, oy + ty + y] = colors[p]
    return im

# ------------------------------------------------------------------ measuring


def parts(text):
    return PART_RE.findall(text)


def token_name(tok):
    return tok[1:-1].split(" ")[0]


def command_tokens(text):
    return Counter(p for p in parts(text) if p.startswith("{") and token_name(p) not in FORMAT_TOKENS)


def boxes(text):
    """[[line, ...], ...]: boxes split at \\r / \\f, lines at \\n (the trailing ending code doesn't open a box)."""
    out, box, line = [], [], []
    for p in parts(text):
        if p == BS + "n":
            box.append(line)
            line = []
        elif p in (BS + "r", BS + "f"):
            box.append(line)
            out.append(box)
            box, line = [], []
        else:
            line.append(p)
    if line or box or not out:
        box.append(line)
        out.append(box)
    return out


def line_px(line):
    return sum(TOKEN_PX if p.startswith("{") and token_name(p).startswith("STRVAR") else
               0 if p.startswith("{") else char_px(p) for p in line)


def units(text):
    n = 0
    for p in parts(text):
        if p.startswith("{"):
            n += 3 + len([a for a in p[1:-1].split(" ", 1)[1:] for _ in a.split(",")])
        else:
            n += 1
    return n


def measure(text):
    bx = boxes(body(text))
    return {"px": max((line_px(l) for b in bx for l in b), default=0),
            "lines": max((len(b) for b in bx), default=0), "units": units(text)}


def ending(text):
    """The run of \\r / \\n / \\f codes the text ends with."""
    m = re.search(r"(?:\\[nrf])+$", text)
    return m.group(0) if m else ""


def body(text):
    return text[:len(text) - len(ending(text))]

# ------------------------------------------------------------------ banks


def bank_files():
    return sorted(MSG.glob("msg_*.gmm"))


def is_script_bank(name):
    return bool(re.match(r"msg_\d{4}_[A-Z]", name))


def base_banks(names):
    """{name: {row: text}} from the base commit, in one git process."""
    req = "".join(f"{BASE}:files/msgdata/msg/{n}.gmm\n" for n in names).encode()
    out = subprocess.run(["git", "cat-file", "--batch"], cwd=ROOT, input=req, capture_output=True, check=True).stdout
    res, pos = {}, 0
    for n in names:
        nl = out.index(b"\n", pos)
        head = out[pos:nl].split()
        pos = nl + 1
        if len(head) < 3 or head[1] == b"missing":
            res[n] = {}
            continue
        size = int(head[2])
        res[n] = rows_of(out[pos:pos + size].decode("utf-8"))
        pos += size + 1
    return res


class Limits:
    def __init__(self, name, base):
        self.name = name
        m = [measure(t) for t in base.values()] or [{"px": 0, "lines": 0, "units": 0}]
        self.px = max(x["px"] for x in m) or 220
        self.lines = max(x["lines"] for x in m) or 1
        self.units = max(x["units"] for x in m)
        if is_script_bank(name):
            self.units = max(self.units, SCRIPT_BANK_CAP)
        if name in CAP:
            self.units = CAP[name]

    def for_row(self, name, base_text, current):
        cur = measure(current)
        if name in CAP:
            room = CAP[name]
        elif name in STRICT_ROWS:
            room = max(measure(base_text)["units"], cur["units"])
        else:
            room = max(self.units, cur["units"])
        return {"px": max(self.px, cur["px"]), "lines": max(self.lines, cur["lines"]), "units": room}


def normalize(text, current):
    """Curly quotes, the original's ending code."""
    text = text.replace("'", "’")
    out, open_q = [], True
    for c in text:
        if c == '"' and '"' not in CHARS:
            out.append("“" if open_q else "”")
            open_q = not open_q
        else:
            out.append(c)
    return body("".join(out)) + ending(current)


def check(name, base_text, current, text, limits):
    """(normalized text, [errors]) for setting row text in bank `name`."""
    errors = []
    if name in READ_ONLY:
        return text, [f"read-only: {READ_ONLY[name]}"]
    text = normalize(text, current)
    bad = sorted({p for p in parts(text) if len(p) == 1 and p not in CHARS and p != BS})
    if bad:
        errors.append("characters the game can't show: " + " ".join(bad))
    if BS in [p for p in parts(text)]:
        errors.append("stray backslash (only \\n, \\r, \\f are codes)")
    for p in parts(text):
        if p.startswith("{"):
            if token_name(p) not in COMMANDS:
                errors.append(f"unknown code {p}")
            elif token_name(p) in FORMAT_TOKENS and not re.fullmatch(r"\{\w+ \d+(, \d+)*\}", p):
                errors.append(f"bad formatting code {p} (use e.g. {{COLOR 1}})")
    want = command_tokens(base_text)
    if command_tokens(text) != want and command_tokens(text) != command_tokens(current):
        missing = want - command_tokens(text)
        extra = command_tokens(text) - want
        if missing:
            errors.append("missing code(s) the game fills in: " + " ".join(missing.elements()))
        if extra:
            errors.append("code(s) not in the original: " + " ".join(extra.elements()))
    blank = lambda t: not re.sub(r"\\[nrf]", "", t).strip()
    if not blank(base_text) and not blank(current) and blank(text):
        errors.append("can't be empty")
    lim = limits.for_row(name, base_text, current)
    for i, box in enumerate(boxes(body(text)), 1):
        if len(box) > lim["lines"]:
            errors.append(f"box {i} has {len(box)} lines (max {lim['lines']})")
        for line in box:
            w = line_px(line)
            if w > lim["px"]:
                errors.append(f"line too wide: {w}px (max {lim['px']}px): “{''.join(line)[:30]}…”")
    n = units(text)
    if n > lim["units"]:
        errors.append(f"too long: {n} (max {lim['units']})")
    return text, errors

# ------------------------------------------------------------------ the overlay


def load_edits():
    return json.loads(EDITS.read_text(encoding="utf-8")) if EDITS.exists() else {}


def save_edits(edits):
    EDITS.write_text(json.dumps(edits, indent=2, ensure_ascii=False), encoding="utf-8")


def write_rows(name, rows):
    """Set rows {idx: text} in the bank's .gmm, keeping everything else byte for byte."""
    path = MSG / f"{name}.gmm"
    src = path.read_text(encoding="utf-8")

    def sub(m):
        i = int(m.group(2))
        return m.group(1) + xml_escape(rows[i]) + m.group(4) if i in rows else m.group(0)
    path.write_text(ROW_RE.sub(sub, src), encoding="utf-8", newline="\n")


def apply(Bank, only=None):
    """Re-apply the overlay through apply_hood's Bank cache (call before Bank.save_all())."""
    for name, rows in load_edits().items():
        if only and name not in only:
            continue
        bank = Bank.get(name)
        for i, text in rows.items():
            if int(i) in bank.rows:
                bank.set(int(i), text)


if __name__ == "__main__":
    edits = load_edits()
    for name, rows in edits.items():
        write_rows(name, {int(i): t for i, t in rows.items()})
    print(f"text edits: {sum(len(r) for r in edits.values())} rows in {len(edits)} banks written")
    sys.exit(0)
