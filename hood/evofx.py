"""The evolution scene as a glow-up: money instead of sparkles, and a GLOW UP! sign when the new form shows.

The scene (evolution_scene.c) creates the emitters of a/1/1/9 member 0 at fixed points: 0 at the start, 1 2 7 8
9 11 while it narrows in, 3 4 5 6 10 at the flash, 12 at the reveal. Texture 0 (the sparkle most of them use)
becomes a dollar sign and their tints go gold and green; 12 becomes the sign (texture 3 was unused).

    patch(rom)   (called from battlefx.patch)
"""
import struct

import ndspy.narc

import fxart
import spa


TILE = 75
EVO_PX = .673          # screen px per texel at particle scale 1.0 in this scene's camera: signs show at 2:1


def _bgr(r, g, b):
    return (b >> 3) << 10 | (g >> 3) << 5 | r >> 3


def build(data):
    texels, pal = fxart.to_a3i5(fxart.burst_sign(["GLOW", "UP!"]), 32)
    data = spa.replace_texture(data, 3, 1, 64, 64, texels, pal)
    b = bytearray(data)
    spa.set_texture(b, 0, fxart.dollar())
    gold, green = _bgr(255, 215, 50), _bgr(70, 220, 90)
    for i, r in enumerate(spa.resources(bytes(b))):
        if r["tex"] != 0 or i == 12:
            continue
        c = gold if i % 2 == 0 else green
        edit = dict(clr=c)
        if "clr" in r:
            edit["clr_anm"] = (_bgr(255, 255, 200), c)
        if "chld" in r:
            edit["child_clr"] = c
        spa.edit(b, r, **edit)
        b[r["off"] + TILE] &= 0xF0                           # a whole $, not four mirrored quarters
    r = spa.resources(bytes(b))[12]                          # the reveal: one big sign, held a beat
    edit = dict(tex=3, gen=1, emtr_life=1, life=70, scl=2 / EVO_PX, init_pos=0, vel=(0, 0), clr=0x7FFF,
                scl_anm=fxart.SIGN_POP, clr_anm=(0x7FFF, 0x7FFF), alpha=(31, 31, 31),
                flags_off=(1 << 12) | (1 << 13) | 0x30)
    spa.edit(b, r, **edit)
    struct.pack_into("<hhH", b, r["off"] + 52, 0, 0, 0)
    b[r["off"] + TILE] &= 0xF0
    return bytes(b)


# the scene's sounds (overlay 95 literal pools; all bank 751, the battle bank - same as the hood samples)
SCENE = 95
SOUND_SWAP = {"SEQ_SE_DP_W278": "SEQ_SE_HOOD_SKRRT", "SEQ_SE_DP_W080C": "SEQ_SE_HOOD_CHACHING",
              "SEQ_SE_DP_W361": "SEQ_SE_HOOD_BLING", "SEQ_SE_DP_W255B": "SEQ_SE_HOOD_POP",
              "SEQ_SE_DP_BOWA3": "SEQ_SE_HOOD_BOOM2"}


def patch_sounds(rom):
    import ndspy.code
    import ndspy.soundArchive
    from battlefx import SDAT
    names = [n for n, _ in ndspy.soundArchive.SDAT(rom.getFileByName(SDAT)).sequences]
    swap = {names.index(a): names.index(b) for a, b in SOUND_SWAP.items()}
    ovs = rom.loadArm9Overlays()
    ov = ovs[SCENE]
    code = bytearray(ov.data)
    hits = 0
    for i in range(0, len(code) - 3, 4):
        v = struct.unpack_from("<I", code, i)[0]
        if v in swap:
            struct.pack_into("<I", code, i, swap[v])
            hits += 1
    assert hits == 8, hits
    ov.data = bytes(code)
    old = len(rom.files[ov.fileID])
    packed = ov.save(compress=True)
    # same 0x200 slot in the ROM, so nothing after it moves (savestates)
    assert (len(packed) + 0x1FF) // 0x200 == (old + 0x1FF) // 0x200, (len(packed), old)
    rom.files[ov.fileID] = packed
    ov.compressedSize = len(packed)
    rom.arm9OverlayTable = ndspy.code.saveOverlayTable(ovs)


def patch(rom):
    narc = ndspy.narc.NARC(rom.getFileByName("a/1/1/9"))
    narc.files[0] = build(narc.files[0])
    rom.setFileByName("a/1/1/9", narc.save())
    patch_sounds(rom)
    print("evolution: glow-up particles + sounds")
