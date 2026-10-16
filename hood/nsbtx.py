"""Minimal NSBTX (BTX0/TEX0) reader/writer for the overworld sprite textures.

Only palette-16 (format 3) textures are decoded; edits are written back in place,
so the file layout and size never change.
"""
import struct


def _read_dict(b, off):
    count = b[off + 1]
    p = off + 8 + (count + 1) * 4          # skip header + patricia tree
    unit = struct.unpack_from("<H", b, p)[0]
    datas = [b[p + 4 + i * unit:p + 4 + (i + 1) * unit] for i in range(count)]
    names_off = p + 4 + count * unit
    names = [b[names_off + 16 * i:names_off + 16 * (i + 1)].rstrip(b"\0").decode("latin1") for i in range(count)]
    return list(zip(names, datas))


def parse(data):
    b = bytearray(data)
    assert b[:4] in (b"BTX0", b"BMD0")
    n = struct.unpack_from("<H", b, 0x0E)[0]
    t = next(o for o in (struct.unpack_from("<I", b, 0x10 + 4 * i)[0] for i in range(n)) if b[o:o + 4] == b"TEX0")
    tex_dict_off = struct.unpack_from("<H", b, t + 0x0E)[0]
    tex_data_off = struct.unpack_from("<I", b, t + 0x14)[0]
    pal_dict_off = struct.unpack_from("<I", b, t + 0x34)[0]
    pal_data_off = struct.unpack_from("<I", b, t + 0x38)[0]
    texs = []
    for name, d in _read_dict(b, t + tex_dict_off):
        param = struct.unpack_from("<I", d, 0)[0]
        texs.append(dict(name=name, off=t + tex_data_off + ((param & 0xFFFF) << 3),
                         w=8 << ((param >> 20) & 7), h=8 << ((param >> 23) & 7),
                         fmt=(param >> 26) & 7, c0=(param >> 29) & 1))
    pals = []
    for name, d in _read_dict(b, t + pal_dict_off):
        pals.append(dict(name=name, off=t + pal_data_off + (struct.unpack_from("<H", d, 0)[0] << 3)))
    return b, texs, pals


def get_palette(b, pal, n=16):
    cols = []
    for i in range(n):
        c = struct.unpack_from("<H", b, pal["off"] + 2 * i)[0]
        cols.append(((c & 31) << 3, ((c >> 5) & 31) << 3, ((c >> 10) & 31) << 3))
    return cols


def set_palette(b, pal, cols):
    for i, (r, g, bl) in enumerate(cols):
        struct.pack_into("<H", b, pal["off"] + 2 * i, (r >> 3) | ((g >> 3) << 5) | ((bl >> 3) << 10))


def get_pixels(b, tex):
    w, h = tex["w"], tex["h"]
    out = []
    for y in range(h):
        row = []
        for x in range(w):
            v = b[tex["off"] + (y * w + x) // 2]
            row.append((v >> 4) if x & 1 else (v & 15))
        out.append(row)
    return out


def set_pixels(b, tex, rows):
    w = tex["w"]
    for y, row in enumerate(rows):
        for x in range(0, w, 2):
            b[tex["off"] + (y * w + x) // 2] = (row[x] & 15) | ((row[x + 1] & 15) << 4)
