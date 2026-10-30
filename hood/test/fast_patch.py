"""Re-patch only the particle kits + move scripts of a built hood-soulsilver.nds in place (seconds, not the
full ~2.5 min patch_rom.py). For animation iteration; run patch_rom.py once at the end.
    python -I hood/test/fast_patch.py
"""
import sys, struct
sys.path.insert(0, 'hood')
import ndspy.rom, ndspy.narc, ndspy.soundArchive
import battlefx, gunfx
ORIG = 'C:/Users/Evan/Documents/dsume/Roms/4840 - Pokemon - SoulSilver Version (v10) (E).nds'
orig = ndspy.rom.NintendoDSRom.fromFile(ORIG)
built = gunfx.build_files(ndspy.narc.NARC(orig.getFileByName('a/0/2/9')).files)
rom = ndspy.rom.NintendoDSRom.fromFile('hood-soulsilver.nds')
narc = ndspy.narc.NARC(rom.getFileByName('a/0/2/9'))
n0 = len(ndspy.narc.NARC(orig.getFileByName('a/0/2/9')).files)
narc.files = narc.files[:n0]
for ps in gunfx.DONOR:
    narc.files.append(built[ps])
    gunfx.LOAD[ps] = len(narc.files) - 1
rom.setFileByName('a/0/2/9', narc.save())
sdat = ndspy.soundArchive.SDAT(rom.getFileByName(battlefx.SDAT))
names = [n for n, _ in sdat.sequences]
seqs = {**{k: names.index(f"SEQ_SE_HOOD_{k.upper()}") for k in battlefx.SOUNDS}, **battlefx.BUILTIN}
ids = battlefx.move_ids()
anims = ndspy.narc.NARC(rom.getFileByName('a/0/1/0'))
for name, k in battlefx.MOVES.items():
    w = gunfx.variant(k, seqs)
    anims.files[ids[name]] = struct.pack(f"<{len(w)}I", *w)
rom.setFileByName('a/0/1/0', anims.save())
rom.saveToFile('hood-soulsilver.nds')
print('fast-patched', len(narc.files))
