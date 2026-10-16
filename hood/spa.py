"""SPL particle resource files (NARC a/0/9/6): find, decode and replace the embedded textures.

Texture block: 0x20-byte header (magic, param, tex_size, pltt_offset, pltt_size, 2 reserved, block_size),
texels, then the palette. Replacements keep the size, format and palette length.
"""
import struct

from PIL import Image


def header(spa):
    magic, ver, res_num, tex_num = struct.unpack_from("<4s4sHH", spa, 0)
    return res_num, tex_num


def textures(spa):
    """[(offset, fmt, w, h, tex_size, pltt_offset, pltt_size)] in file order."""
    _, n = header(spa)
    out = []
    o = spa.find(b" TPS")
    if o < 0:
        o = spa.find(b"SPT1")
    while len(out) < n and o >= 0 and o + 0x20 <= len(spa):
        magic, param, tsz, poff, psz, _, _, bsz = struct.unpack_from("<4sIIIIIII", spa, o)
        fmt, s, t = param & 15, (param >> 4) & 15, (param >> 8) & 15
        out.append((o, fmt, 8 << s, 8 << t, tsz, poff, psz, param))
        o += bsz
    return out


def _bgr(c):
    return ((c & 31) * 255 // 31, (c >> 5 & 31) * 255 // 31, (c >> 10 & 31) * 255 // 31)


def decode(spa, tex):
    o, fmt, w, h, tsz, poff, psz, param = tex
    texel = spa[o + 0x20:o + 0x20 + tsz]
    pal = [_bgr(v) for v in struct.unpack_from(f"<{psz // 2}H", spa, o + poff)] if psz else []
    plt0 = param >> 16 & 1
    im = Image.new("RGBA", (w, h))
    px = im.load()
    for i in range(w * h):
        x, y = i % w, i // w
        if fmt == 1:     # A3I5
            v = texel[i]; c = pal[v & 31] if (v & 31) < len(pal) else (0, 0, 0); a = (v >> 5) * 255 // 7
        elif fmt == 6:   # A5I3
            v = texel[i]; c = pal[v & 7] if (v & 7) < len(pal) else (0, 0, 0); a = (v >> 3) * 255 // 31
        elif fmt == 2:
            v = texel[i // 4] >> (2 * (i % 4)) & 3; c = pal[v] if v < len(pal) else (0, 0, 0); a = 0 if (plt0 and v == 0) else 255
        elif fmt == 3:
            v = texel[i // 2] >> (4 * (i % 2)) & 15; c = pal[v] if v < len(pal) else (0, 0, 0); a = 0 if (plt0 and v == 0) else 255
        elif fmt == 4:
            v = texel[i]; c = pal[v] if v < len(pal) else (0, 0, 0); a = 0 if (plt0 and v == 0) else 255
        else:
            c, a = (255, 0, 255), 255
        px[x, y] = (*c, a)
    return im


BASE = 88
_FIELDS = [(24, 8), (25, 8), (26, 16), (27, 4), (28, 8), (29, 16)]   # flag bit -> size (grvt rndm mgnt spin scfld cngc)


def resources(spa):
    """[dict(off, flag, tex, child_tex, scl, clr, alp, texanm, chld, size)] for each emitter resource."""
    n, _ = header(spa)
    o, out = 0x20, []
    for _ in range(n):
        flag = struct.unpack_from("<I", spa, o)[0]
        r = {"off": o, "flag": flag, "tex": spa[o + 71], "draw": flag >> 4 & 3}
        p = o + BASE
        for bit, name, size in ((8, "scl", 12), (9, "clr", 12), (10, "alp", 8), (11, "texanm", 12), (16, "chld", 20)):
            if flag >> bit & 1:
                r[name] = p
                p += size
        if "chld" in r:
            r["child_tex"] = spa[r["chld"] + 15]
        if "texanm" in r:
            k = spa[r["texanm"] + 8]
            r["tex_ptn"] = list(spa[r["texanm"]:r["texanm"] + k])
        for (bit, size), name in zip(_FIELDS, ("grvt", "rndm", "mgnt", "spin", "scfld", "cngc")):
            if flag >> bit & 1:
                r[name] = p
                p += size
        r["size"] = p - o
        out.append(r)
        o = p
    return out


# ------------------------------------------------------------------ editing (in place, sizes never change)

def _fx(v):
    return int(round(v * 4096))


def edit(b, r, *, clr=None, life=None, emtr_life=None, scl=None, gen=None, vel=None, tex=None,
         scl_anm=None, clr_anm=None, alpha=None, gravity=None, child_clr=None, axis=None, gen_intvl=None,
         rndm=None, child_gen=None, radius=None, air_resist=None, flags_off=0, flags_on=0, alpha_timing=None,
         flick=None, init_pos=None):
    """Edit emitter resource r (from resources()) inside bytearray b. Colours are BGR555 ints.
    scl_anm = (start, mid, end, in 0-255, out 0-255) relative scales; clr_anm = (start, end);
    alpha = (start, mid, end) 0-31; gravity = (x, y, z) in units/frame^2 (fx16)."""
    o = r["off"]
    if flags_off or flags_on:                                  # e.g. 1 << 13 = random initial rotation
        assert not (flags_off | flags_on) & 0x03FF0F00, "flags that add/remove blocks would change the size"
        r["flag"] = (r["flag"] & ~flags_off) | flags_on
        struct.pack_into("<I", b, o, r["flag"])
    if clr is not None:
        struct.pack_into("<H", b, o + 34, clr)
    if vel is not None:
        struct.pack_into("<ii", b, o + 36, _fx(vel[0]), _fx(vel[1]))
    if scl is not None:
        struct.pack_into("<i", b, o + 44, _fx(scl))
    if gen is not None:
        struct.pack_into("<i", b, o + 16, _fx(gen))
    if emtr_life is not None:
        struct.pack_into("<H", b, o + 60, emtr_life)
    if life is not None:
        struct.pack_into("<H", b, o + 62, life)
    if tex is not None:
        b[o + 71] = tex
    if scl_anm is not None:
        assert "scl" in r, "no scale animation block"
        s0, s1, s2, i, out = scl_anm
        struct.pack_into("<hhhBB", b, r["scl"], _fx(s0), _fx(s1), _fx(s2), i, out)
    if clr_anm is not None:
        assert "clr" in r, "no colour animation block"
        struct.pack_into("<HH", b, r["clr"], *clr_anm)
    if alpha is not None:
        assert "alp" in r, "no alpha animation block"
        a0, a1, a2 = alpha
        struct.pack_into("<HH", b, r["alp"], a0 | a1 << 5 | a2 << 10, 0)
    if alpha_timing is not None:                               # (in, out) as 0-255 fractions of the life
        b[r["alp"] + 4:r["alp"] + 6] = bytes(alpha_timing)
    if flick is not None:                                      # random per-frame dimming, 0-255
        b[r["alp"] + 2] = flick
    if init_pos is not None:                                   # 0 = spawn exactly at the emitter
        r["flag"] = (r["flag"] & ~15) | init_pos
        struct.pack_into("<I", b, o, r["flag"])
    if gravity is not None:
        assert "grvt" in r, "no gravity field"
        struct.pack_into("<hhh", b, r["grvt"], *(_fx(v) for v in gravity))
    if child_clr is not None:
        assert "chld" in r
        struct.pack_into("<H", b, r["chld"] + 10, child_clr)
    if child_gen is not None:
        assert "chld" in r
        b[r["chld"] + 12] = child_gen
    if axis is not None:                                       # emission direction (unit vector)
        struct.pack_into("<hhh", b, o + 28, *(_fx(v) for v in axis))
    if gen_intvl is not None:                                  # frames between emissions
        b[o + 68] = gen_intvl
    if air_resist is not None:                                 # 0-255, lower slows particles more
        b[o + 70] = air_resist
    if rndm is not None:                                       # randomness 0-255: (scale, life, velocity)
        b[o + 64:o + 67] = bytes(rndm)
    if radius is not None:
        struct.pack_into("<i", b, o + 20, _fx(radius))


def set_texture(b, index, texels, palette=None):
    t = textures(bytes(b))[index]
    o, fmt, w, h, tsz, poff, psz, _ = t
    assert len(texels) == tsz, (len(texels), tsz)
    b[o + 0x20:o + 0x20 + tsz] = texels
    if palette is not None:
        pal = list(palette)[:psz // 2] + [0] * max(0, psz // 2 - len(palette))
        b[o + poff:o + poff + psz] = struct.pack(f"<{psz // 2}H", *pal)
