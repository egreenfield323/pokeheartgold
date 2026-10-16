#!/usr/bin/env python3
"""Build a playable Hood HeartGold ROM from YOUR OWN dump of Pokémon HeartGold (US).

    python hood/patch_rom.py path/to/heartgold.nds [out.nds]

No compiler or Nintendo SDK needed: every asset the mod changes is rebuilt with the game's
own encoders (hood/bin/msgenc.exe, hood/bin/nitrogfx.exe) and swapped into the ROM's archives.

Before patching it self-tests: it rebuilds untouched originals from the decomp and checks they
match your ROM byte-for-byte. If they don't, your ROM isn't the US HeartGold this targets and
nothing is written.

Needs: Python 3 with Pillow and ndspy (`pip install ndspy pillow`).
"""
import hashlib
import json
import re
import shutil
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

import ndspy.narc
import ndspy.rom

ROOT = Path(__file__).resolve().parent.parent
BIN = ROOT / "hood/bin"
MSGENC, GFX = str(BIN / "msgenc.exe"), str(BIN / "nitrogfx.exe")
EXPECTED_SHA1 = {"4fcded0e2713dc03929845de631d0932ea2b5a37",   # pokeheartgold.us.nds
                 "f8dc38ea20c17541a43b58c5e6d18c1732c7e582"}   # pokesoulsilver.us.nds
TMP = Path(tempfile.mkdtemp(prefix="hoodhg_"))


def run(*args):
    r = subprocess.run([str(a) for a in args], capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"tool failed: {' '.join(map(str, args))}\n{r.stdout}{r.stderr}")


def head(rel):
    return subprocess.run(["git", "show", f"HEAD:{rel}"], cwd=ROOT, capture_output=True, check=True).stdout


def changed(prefix):
    out = subprocess.run(["git", "status", "--porcelain", "--", prefix], cwd=ROOT, capture_output=True, text=True).stdout
    return [line[3:].strip() for line in out.splitlines() if line[:2].strip() == "M"]


class Narc:
    def __init__(self, rom, path):
        self.rom, self.path = rom, path
        self.narc = ndspy.narc.NARC(rom.getFileByName(path))
        self.dirty = 0

    def get(self, i):
        return self.narc.files[i]

    def set(self, i, data):
        if self.narc.files[i] != data:
            self.narc.files[i] = data
            self.dirty += 1

    def save(self):
        if self.dirty:
            self.rom.setFileByName(self.path, self.narc.save())


# ---------------------------------------------------------------- builders

MSG_KEYS = dict(re.findall(r"msg/(msg_\w+)\.bin: MSGENCFLAGS \+= -k (0x[0-9A-Fa-f]+)",
                           (ROOT / "files/msgdata/msg.mk").read_text()))


def encode_gmm(name, text):
    src, out = TMP / f"{name}.gmm", TMP / f"{name}.bin"
    src.write_bytes(text)
    run(MSGENC, "-e", "-c", ROOT / "charmap.txt", "--gmm", "-k", MSG_KEYS[name], "-H", TMP / f"{name}.h", src, out)
    return out.read_bytes()


def trname_gmm(trainers):
    rows = "".join(
        f'\n\t<row id="msg_0729_{i:05d}" index="{i}">\n\t\t<attribute name="window_context_name">used</attribute>\n'
        f'\t\t<language name="English">{t["name"].replace("&", "&amp;")}</language>\n\t</row>'
        for i, t in enumerate(trainers))
    return f'<?xml version="1.0"?>\n<body language="English">{rows}\n</body>\n'.encode("utf-8")


def gfx(png_bytes_or_path, ext, *flags, key=None):
    """Run nitrogfx on a PNG (path, or bytes + its .key) and return the output bytes."""
    if isinstance(png_bytes_or_path, bytes):
        p = TMP / "in.png"
        p.write_bytes(png_bytes_or_path)
        k = Path(str(p) + ".key")
        if key is not None:
            k.write_bytes(key)
        elif k.exists():
            k.unlink()
    else:
        p = png_bytes_or_path
    out = TMP / f"out.{ext}"
    run(GFX, p, out, *flags)
    return out.read_bytes()


SPRITE = ("-scanfronttoback", "-handleempty")
PAL8 = ("-bitdepth", "8", "-nopad", "-comp", "10")
ICON = ("-clobbersize", "-version101")


def pokegra_member(species, k, source):
    """source(rel) -> (png bytes, key bytes or None). Mirrors pokegra.mk."""
    d = f"files/poketool/pokegra/pokegra/{species:04d}"
    if k < 4:
        sex, view = ("female", "male")[k % 2], ("back", "front")[k // 2]
        png, key = source(f"{d}/{sex}/{view}.png")
        return gfx(png, "NCGR", *SPRITE, key=key)
    view = "front" if k == 4 else "back"
    for sex in ("male", "female"):
        png, _ = source(f"{d}/{sex}/{view}.png")
        if png:
            return gfx(png, "NCLR", *PAL8)
    return None


def from_head(rel):
    png = head(rel)
    try:
        key = head(rel + ".key")
    except subprocess.CalledProcessError:
        key = None
    return png, key


def from_disk(rel):
    p = ROOT / rel
    k = Path(str(p) + ".key")
    return p.read_bytes(), (k.read_bytes() if k.exists() else None)


def otherpoke_lines():
    out = []
    for line in (ROOT / "files/poketool/pokegra/otherpoke.txt").read_text().splitlines():
        parts = line.split()
        if len(parts) >= 2:
            idx = int(Path(parts[1]).stem)
            out.append((parts[0], idx, Path(parts[1]).suffix[1:], tuple(parts[2:])))
    return out


# ---------------------------------------------------------------- self-test

def self_test(rom):
    print("self-test: rebuilding untouched originals and comparing with your ROM ...")
    msg = Narc(rom, "a/0/2/7")
    for name in ("msg_0237", "msg_0750", "msg_0001"):
        assert encode_gmm(name, head(f"files/msgdata/msg/{name}.gmm")) == msg.get(int(name[4:])), name
    trainers = json.loads(head("files/poketool/trainer/trainers.json"))["trainers"]
    assert encode_gmm("msg_0729", trname_gmm(trainers)) == msg.get(729), "trainer names"
    pers = Narc(rom, "a/0/0/2")
    old = json.loads(head("files/poketool/personal/personal.json"))["baseStats"]
    for i in (155, 246):
        assert bytes(old[i][k] for k in ("hp", "atk", "def", "speed", "spatk", "spdef")) == pers.get(i)[:6], "stats"
    pg = Narc(rom, "a/0/0/4")
    for sp in (1, 155, 249):
        for k in range(6):
            data = pokegra_member(sp, k, from_head)
            if data is not None:
                assert data == pg.get(sp * 6 + k), f"pokegra {sp}-{k}"
    icons = Narc(rom, "a/0/2/0")
    for n in (8, 162):
        assert gfx(head(f"files/poketool/icongra/poke_icon/poke_icon_{n:08d}.png"), "NCGR", *ICON) == icons.get(n), "icon"
    mm = Narc(rom, "a/0/8/1")
    assert head("files/data/mmodel/mmodel/mmodel_00000303.NSBTX") == mm.get(303), "mmodel"
    for rel in ("a/0/5/8", "a/2/5/6", "a/2/4/8"):
        assert head(f"files/{rel}") == rom.getFileByName(rel), rel
    print("self-test passed: this ROM matches the decomp.")


# ---------------------------------------------------------------- patch

SKIP = set()


def patch(rom):
    # text
    if "text" in SKIP:
        print("skipping text"); return _after_text(rom)
    msg = Narc(rom, "a/0/2/7")
    banks = sorted({Path(p).stem for p in changed("files/msgdata/msg") if p.endswith(".gmm")})
    for name in banks:
        assert encode_gmm(name, head(f"files/msgdata/msg/{name}.gmm")) == msg.get(int(name[4:8])), f"original {name}"
        msg.set(int(name[4:8]), encode_gmm(name, (ROOT / f"files/msgdata/msg/{name}.gmm").read_bytes()))
    trainers = json.loads((ROOT / "files/poketool/trainer/trainers.json").read_text(encoding="utf-8"))["trainers"]
    msg.set(729, encode_gmm("msg_0729", trname_gmm(trainers)))
    msg.save()
    print(f"text: {len(banks) + 1} message banks")

    _after_text(rom)


def _after_text(rom):
    # base stats / types (personal: hp atk def spe spa spd type1 type2 ...)
    pers = Narc(rom, "a/0/0/2")
    old = json.loads(head("files/poketool/personal/personal.json"))["baseStats"]
    new = json.loads((ROOT / "files/poketool/personal/personal.json").read_text())["baseStats"]
    types = dict(re.findall(r"#define (TYPE_\w+)\s+(\d+)", (ROOT / "include/constants/pokemon.h").read_text()))
    n = 0
    for i, (a, b) in enumerate(zip(old, new)):
        if a == b:
            continue
        d = bytearray(pers.get(i))
        d[0:6] = bytes(b[k] for k in ("hp", "atk", "def", "speed", "spatk", "spdef"))
        d[6], d[7] = int(types[b["types"][0]]), int(types[b["types"][1]])
        pers.set(i, bytes(d))
        n += 1
    pers.save()
    print(f"stats: {n} species")

    # learnsets, trainer sprites, Pokéwalker: whole archives
    assert head("files/poketool/personal/wotbl.narc") == rom.getFileByName("a/0/3/3"), "original learnsets"
    rom.setFileByName("a/0/3/3", (ROOT / "files/poketool/personal/wotbl.narc").read_bytes())
    for rel in ("a/0/5/8", "a/2/5/6", "a/2/4/8", "a/0/1/0"):
        assert head(f"files/{rel}") == rom.getFileByName(rel), f"original {rel}"
        rom.setFileByName(rel, (ROOT / "files" / rel).read_bytes())
    print("learnsets, trainer sprites, Pokéwalker: replaced")

    # battle effects: gun animations, particle kits, synthesized sounds
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import battlefx
    battlefx.patch(rom)

    # battle sprites
    pg = Narc(rom, "a/0/0/4")
    touched = {int(Path(p).parts[4]) for p in changed("files/poketool/pokegra/pokegra")}
    for j, sp in enumerate(sorted(touched)):
        if j % 50 == 0:
            print(f"  battle sprites {j}/{len(touched)} ...", flush=True)
        for k in range(6):
            data = pokegra_member(sp, k, from_disk)
            if data is not None:
                pg.set(sp * 6 + k, data)
    pg.save()
    print(f"battle sprites: {len(touched)} species")

    # alternate forms
    op = Narc(rom, "a/1/1/4")
    for png, idx, ext, flags in otherpoke_lines():
        if (ROOT / png).stat().st_size:
            op.set(idx, gfx(ROOT / png, ext, *flags))
    op.save()
    print(f"alternate forms: {op.dirty} files")

    # icons
    ic = Narc(rom, "a/0/2/0")
    for p in changed("files/poketool/icongra/poke_icon"):
        if p.endswith(".png"):
            ic.set(int(Path(p).stem.split("_")[-1]), gfx(ROOT / p, "NCGR", *ICON))
    ic.save()
    print(f"icons: {ic.dirty}")

    # overworld textures, title Ho-Oh, Celebi cutscene
    mm = Narc(rom, "a/0/8/1")
    for p in ([] if "mmodel" in SKIP else changed("files/data/mmodel/mmodel")):
        assert head(p) == mm.get(int(Path(p).stem.split("_")[-1])), f"original {p}"
        mm.set(int(Path(p).stem.split("_")[-1]), (ROOT / p).read_bytes())
    mm.save()
    for rel, narc in (("files/demo/title/titledemo/titledemo_00000025.NSBMD", "a/0/4/6"),
                      ("files/demo/legend/legend_00000075.NSBMD", "a/1/7/4")):
        nn = Narc(rom, narc)
        assert head(rel) == nn.get(int(Path(rel).stem.split("_")[-1])), f"original {rel}"
        nn.set(int(Path(rel).stem.split("_")[-1]), (ROOT / rel).read_bytes())
        nn.save()
    print(f"overworld: {mm.dirty} textures; title Ho-Oh + Celebi cutscene")

    # bag icons
    icons2 = Narc(rom, "a/0/1/8")
    for p in changed("files/itemtool/itemdata/item_icon"):
        idx = int(Path(p).stem.split("_")[-1])
        assert head(p) == icons2.get(idx), f"original {p}"
        icons2.set(idx, (ROOT / p).read_bytes())
    icons2.save()
    print(f"item icons: {icons2.dirty}")

    # intro (Oak's portrait, Marill)
    intro = Narc(rom, "a/1/2/0")
    for p in changed("files/demo/intro/intro"):
        idx = int(Path(p).stem.split("_")[-1])
        assert head(p) == intro.get(idx), f"original {p}"
        intro.set(idx, (ROOT / p).read_bytes())
    intro.save()
    print(f"intro: {intro.dirty} files")


def main():
    global SKIP
    for a in list(sys.argv):
        if a.startswith("--skip="):
            SKIP = set(a[7:].split(","))
            sys.argv.remove(a)
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src = Path(sys.argv[1])
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else src.with_name("hood-heartgold.nds")
    for tool in (MSGENC, GFX):
        if not Path(tool).exists():
            sys.exit(f"missing {tool} (build it: see hood/README.md)")
    data = src.read_bytes()
    sha = hashlib.sha1(data).hexdigest()
    if sha not in EXPECTED_SHA1:
        print(f"note: ROM sha1 {sha} isn't a known clean dump; the per-file checks will decide")
    rom = ndspy.rom.NintendoDSRom(data)
    code = bytes(rom.idCode).decode("latin1", "replace")
    if code not in ("IPKE", "IPGE"):
        sys.exit(f"this ROM's game code is {code!r}; needs US HeartGold ('IPKE') or US SoulSilver ('IPGE'). "
                 "Nothing was written.")
    print("ROM:", {"IPKE": "HeartGold (US)", "IPGE": "SoulSilver (US)"}[code])
    try:
        self_test(rom)
    except AssertionError as e:
        sys.exit(f"self-test FAILED ({e}): this ROM doesn't match the decomp. Nothing was written.")
    try:
        patch(rom)
    except AssertionError as e:
        sys.exit(f"an original file didn't match ({e}); this ROM isn't the one the mod targets. Nothing was written.")
    rom.saveToFile(str(out))
    shutil.rmtree(TMP, ignore_errors=True)
    print(f"\nwrote {out}  ->  open it in melonDS")


if __name__ == "__main__":
    main()
