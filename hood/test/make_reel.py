"""Test-only: turn FMJ's animation (move 33) into a reel of the 5 candidate gunshots (gunfx.variant 1-5),
each with its own synthesized sound (gunsounds), so they can be compared in one battle.

    python -I hood/test/make_reel.py ROM

Everything is patched in place without moving any file (each archive keeps its exact size), so
savestates made mid-battle - which hold open file offsets - keep working.
"""
import struct
import sys
from pathlib import Path

import ndspy.narc
import ndspy.rom
import ndspy.soundArchive

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import animscript as A  # noqa: E402
import gunfx  # noqa: E402
import gunsounds  # noqa: E402

MOVE = 33
# reel slot k -> (sound name, battle sequence id to overwrite, its instrument, the SWAR 751 wave it plays)
SLOTS = {"pop": ("pop", 1908, 87, 10), "boom": ("deagle", 2004, 78, 4), "boom2": ("street_echo", 1993, 89, 3),
         "skrrt": ("skrrt", 1926, 91, 21), "bling": ("bling", 1910, 92, 17),
         "chaching": ("chaching", 1913, 80, 5), "fwoosh": ("fwoosh", 1914, 70, 25)}
SOUNDS = {key: seq for key, (_, seq, _, _) in SLOTS.items()}


def as_sub(w):
    w = list(w)
    for i, name, args in A.disasm(w):
        if w[i] == 4:
            w[i] = 11                     # End -> Return
    return w


ORDER = [int(x) for x in sys.argv[sys.argv.index("--order") + 1].split(",")] if "--order" in sys.argv else list(gunfx.VARIANTS)


def reel():
    head, calls, subs = [], [], []
    for k in ORDER:
        head += [0, 40, 10]               # Wait 40; Call ->
        calls.append(len(head))
        head += [0]
    head += [4]
    off = len(head)
    for n, k in enumerate(ORDER):
        sub = as_sub(gunfx.variant(k, SOUNDS))
        head[calls[n]] = off - calls[n]
        subs += sub
        off += len(sub)
    return head + subs


def fat_range(data, fid):
    fat = struct.unpack_from("<I", data, 0x48)[0]
    return struct.unpack_from("<II", data, fat + fid * 8)


def patch_member(data, rom, path, member, new, blank_ok=()):
    """Replace one NARC member in place; if it grows, blank the largest members in blank_ok to make room."""
    fid = rom.filenames.idOf(path)
    start, end = fat_range(data, fid)
    old = bytes(data[start:end])
    narc = ndspy.narc.NARC(old)
    if len(new) == len(narc.files[member]):                 # same size: overwrite the bytes where they are
        pos = old.find(narc.files[member])
        assert pos >= 0 and old.find(narc.files[member], pos + 1) < 0
        data[start + pos:start + pos + len(new)] = new
        return
    narc.files[member] = new
    for i in sorted(blank_ok, key=lambda i: -len(narc.files[i])):
        if len(narc.save()) <= len(old):
            break
        narc.files[i] = struct.pack("<I", 4)
    out = narc.save()
    if len(out) > len(old):
        sys.exit(f"{path}[{member}] does not fit")
    narc.files[member] = new + bytes(len(old) - len(out))
    out = narc.save()
    assert len(out) == len(old)
    data[start:end] = out


def patch_sounds(data, sdat_bytes):
    import numpy as np
    sdat = ndspy.soundArchive.SDAT(sdat_bytes)
    _, swar = sdat.waveArchives[751]
    shots = gunsounds.shots()
    sdat_off = data.find(sdat_bytes[:0x40])
    assert sdat_off > 0 and data[sdat_off:sdat_off + len(sdat_bytes)] == sdat_bytes
    info = struct.unpack_from("<I", sdat_bytes, 0x18)[0]
    fat = struct.unpack_from("<I", sdat_bytes, 0x20)[0]
    seqrec = info + struct.unpack_from("<I", sdat_bytes, info + 8)[0]
    warec = info + struct.unpack_from("<I", sdat_bytes, info + 8 + 12)[0]       # wave archive records
    o = info + struct.unpack_from("<I", sdat_bytes, warec + 4 + 4 * 751)[0]
    wfid = struct.unpack_from("<I", sdat_bytes, o)[0] & 0xFFFFFF
    wfo, wfs = struct.unpack_from("<II", sdat_bytes, fat + 12 + 16 * wfid)
    lo, hi = sdat_off + wfo, sdat_off + wfo + wfs
    assert data[lo:lo + 4] == b"SWAR"
    for k, (name, seq, inst, wave) in SLOTS.items():
        old = swar.waves[wave].data
        pos = data.find(old, lo, hi)
        assert pos > 0 and data.find(old, pos + 1, hi) < 0, f"wave {wave} not unique"
        x = shots[name]
        cap = (len(old) - 4) * 2                           # ADPCM samples that fit
        rate = min(gunsounds.RATE, int(cap / len(x) * gunsounds.RATE))
        if rate < gunsounds.RATE:                          # resample to fit the slot
            t = np.linspace(0, len(x) - 1, int(len(x) * rate / gunsounds.RATE))
            x = np.interp(t, np.arange(len(x)), x).astype("float32")
        enc = gunsounds.adpcm(x)
        assert len(enc) <= len(old)
        nwords = (len(enc) + 3) // 4
        data[pos:pos + len(old)] = enc + bytes(len(old) - len(enc))
        data[pos - 12:pos] = struct.pack("<BBHHHI", 2, 0, rate, 16756991 // rate, 1, nwords)
        # the sequence: one note on the instrument, long enough for the whole sample
        o = info + struct.unpack_from("<I", sdat_bytes, seqrec + 4 + 4 * seq)[0]
        fid = struct.unpack_from("<H", sdat_bytes, o)[0]
        fo, fs = struct.unpack_from("<II", sdat_bytes, fat + 12 + 16 * fid)
        doff = struct.unpack_from("<I", sdat_bytes, fo + 0x18)[0]
        ticks = int(len(x) / rate * 96) + 8                # 120 bpm, 48 ticks per beat
        ev = bytes([0x81, inst, 0xC1, 0x7F, 0x3C, 0x7F, 0x80 | ticks >> 7, ticks & 0x7F, 0xFF])
        assert doff + len(ev) <= fs
        p = sdat_off + fo + doff
        data[p:p + len(ev)] = ev
        print(f"sound {k} {name}: seq {seq} inst {inst} wave {wave} @ {rate} Hz, {len(x) / rate:.2f}s")


def main():
    rom_path = Path(sys.argv[1])
    data = bytearray(rom_path.read_bytes())
    rom = ndspy.rom.NintendoDSRom(bytes(data))
    patch_sounds(data, rom.getFileByName("data/sound/gs_sound_data.sdat"))
    ptcl = ndspy.narc.NARC(rom.getFileByName("a/0/2/9"))
    for ps, new in gunfx.build_files(ptcl.files).items():
        patch_member(data, rom, "a/0/2/9", gunfx.DONOR[ps], new)
    w = reel()
    n = len(ndspy.narc.NARC(rom.getFileByName("a/0/1/0")).files)
    patch_member(data, rom, "a/0/1/0", MOVE, struct.pack(f"<{len(w)}I", *w),
                 blank_ok=[i for i in range(300, n) if i != MOVE])
    assert len(data) == rom_path.stat().st_size
    rom_path.write_bytes(data)
    print("reel words:", len(w))


if __name__ == "__main__":
    main()
