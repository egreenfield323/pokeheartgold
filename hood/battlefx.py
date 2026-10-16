"""Put Hood HeartGold's battle effects into a ROM: new particle files, new sound effects, move scripts.

    patch(rom)   (called from patch_rom.py after the move-animation archive is in place)

- particle kits (gunfx.build_files) are appended to a/0/2/9 as new members, so the moves they were
  cloned from keep their own graphics;
- the synthesized sounds (gunsounds) become new waves in the battle wave archive (751), new single-note
  instruments in the battle bank (751) and new sequences at the end of the sound archive, so no existing
  sound is replaced;
- the mapped moves' animation scripts (a/0/1/0) are replaced by gunfx variants.
"""
import re
import subprocess
from pathlib import Path

import ndspy.narc
import ndspy.soundArchive
import ndspy.soundBank
import ndspy.soundSequence as Q
import ndspy.soundWave
import numpy as np

import gunfx
import gunsounds

ROOT = Path(__file__).resolve().parent.parent
SDAT = "data/sound/gs_sound_data.sdat"
BATTLE = 751                                                  # BANK_SE_BATTLE / its wave archive

# effect sound key -> (synth name, sample rate)
SOUNDS = {"pop": ("pop", 11025), "boom": ("deagle", 11025), "boom2": ("street_echo", 11025),
          "skrrt": ("skrrt", 9000), "bling": ("bling", 11025), "chaching": ("chaching", 9000),
          "fwoosh": ("fwoosh", 9000), "whoosh": ("whoosh", 8000), "smash": ("smash", 11025),
          "bonk": ("bonk", 8000), "splat": ("splat", 8000)}
# (rates kept low on purpose: these all join the battle wave archive, which lives in the sound heap for the
#  whole battle - it grew 85K -> 124K at 16 kHz and the game froze on the next turn)

# original move name (msg_0750) -> gunfx variant
#   1 sniper, 2 shotgun, 3 spray & pray, 4 point blank, 5 gangsta tilt (the everyday gun moves),
#   6 drive-by, 7 chain swing, 8 chain dangle, 9 make it rain, 10 full auto, 11 RPG (legendaries),
#   12 Molotov, 13 brick toss, 14 egg ya house
MOVES = {
    "Tackle": 5, "Double Kick": 5, "Lick": 5,
    "Fury Attack": 3, "Triple Kick": 3, "Pin Missile": 3, "Spike Cannon": 3, "Swift": 3,
    "Scratch": 4, "Crunch": 4,
    "Wing Attack": 2,
    "Iron Head": 1,
    "Quick Attack": 6,
    "Psychic": 7, "Confusion": 8,
    "Pay Day": 9,
    "Hyper Beam": 10,
    "Aeroblast": 11, "Sacred Fire": 11, "Roar of Time": 11, "Spacial Rend": 11, "Shadow Force": 11,
    "Psycho Boost": 11, "Doom Desire": 11, "Judgment": 11, "Crush Grip": 11, "Magma Storm": 11,
    "Flamethrower": 12, "Fire Blast": 12,
    "Rock Throw": 13, "Rock Slide": 13,
    "Egg Bomb": 14,
}


def move_ids():
    gmm = subprocess.run(["git", "show", "HEAD:files/msgdata/msg/msg_0750.gmm"], cwd=ROOT,
                         capture_output=True, check=True).stdout.decode("utf-8")
    return {m.group(2): int(m.group(1)) for m in re.finditer(r'index="(\d+)".*?English">(.*?)</language>', gmm, re.S)}


def _resample(x, rate):
    if rate == gunsounds.RATE:
        return x
    t = np.linspace(0, len(x) - 1, int(len(x) * rate / gunsounds.RATE))
    return np.interp(t, np.arange(len(x)), x).astype("float32")


def add_sounds(rom):
    """Add every effect sound; returns {key: new sequence id}."""
    sdat = ndspy.soundArchive.SDAT(rom.getFileByName(SDAT))
    _, swar = sdat.waveArchives[BATTLE]
    _, bank = sdat.banks[BATTLE]
    archive_slot = bank.waveArchiveIDs.index(BATTLE)
    _, model = sdat.sequences[1910]                            # a battle move SE: same player/volume setup
    shots = gunsounds.shots()
    seqs = {}
    for key, (name, rate) in SOUNDS.items():
        x = _resample(shots[name], rate)
        data = gunsounds.adpcm(x)
        data += bytes(-len(data) % 4)
        swar.waves.append(ndspy.soundWave.SWAV.fromData(
            data, waveType=ndspy.soundWave.WaveType.ADPCM, isLooped=False, sampleRate=rate,
            time=16756991 // rate, loopOffset=1, totalLength=len(data) // 4 - 1))
        wave = len(swar.waves) - 1
        bank.instruments.append(ndspy.soundBank.SingleNoteInstrument(ndspy.soundBank.NoteDefinition(
            wave, archive_slot, pitch=60, attack=127, decay=127, sustain=127, release=127, pan=64)))
        inst = len(bank.instruments) - 1
        ticks = int(len(x) / rate * 96) + 8                    # 120 bpm, 48 ticks a beat
        seq = Q.SSEQ(bankID=BATTLE, volume=127, channelPressure=model.channelPressure,
                     polyphonicPressure=model.polyphonicPressure, playerID=model.playerID)
        seq.events = [Q.InstrumentSwitchSequenceEvent(inst >> 7, inst & 0x7F),
                      Q.TrackVolumeSequenceEvent(127),
                      Q.NoteSequenceEvent(60, 127, ticks),
                      Q.EndTrackSequenceEvent()]
        sdat.sequences.append((f"SEQ_SE_HOOD_{key.upper()}", seq))
        seqs[key] = len(sdat.sequences) - 1
    rom.setFileByName(SDAT, sdat.save())
    return seqs


def add_particles(rom):
    """Append the particle kits; points gunfx at the new members."""
    narc = ndspy.narc.NARC(rom.getFileByName("a/0/2/9"))
    built = gunfx.build_files(narc.files)
    for ps, donor in gunfx.DONOR.items():
        narc.files.append(built[ps])
        gunfx.LOAD[ps] = len(narc.files) - 1
    rom.setFileByName("a/0/2/9", narc.save())


def patch(rom):
    seqs = add_sounds(rom)
    add_particles(rom)
    ids = move_ids()
    anims = ndspy.narc.NARC(rom.getFileByName("a/0/1/0"))
    import struct
    for name, k in MOVES.items():
        w = gunfx.variant(k, seqs)
        anims.files[ids[name]] = struct.pack(f"<{len(w)}I", *w)
    rom.setFileByName("a/0/1/0", anims.save())
    print(f"battle effects: {len(MOVES)} moves, {len(gunfx.DONOR)} particle kits, {len(seqs)} sounds")


def showcase(rom_path, out_path, order=None, pad_to=None):
    """Test copy of a built ROM where FMJ (Tackle) plays every effect back to back (or just `order`).
    pad_to pads the script to a fixed size so the ROM layout - and so savestates - stay the same."""
    import struct
    import ndspy.rom
    import animscript as A
    rom = ndspy.rom.NintendoDSRom.fromFile(rom_path)
    sdat = ndspy.soundArchive.SDAT(rom.getFileByName(SDAT))
    names = [n for n, _ in sdat.sequences]
    seqs = {k: names.index(f"SEQ_SE_HOOD_{k.upper()}") for k in SOUNDS}
    narc = ndspy.narc.NARC(rom.getFileByName("a/0/2/9"))
    first = len(narc.files) - len(gunfx.DONOR)
    for i, ps in enumerate(gunfx.DONOR):
        gunfx.LOAD[ps] = first + i
    head, calls, subs = [], [], []
    order = order or sorted(set(MOVES.values()))
    for _ in order:
        head += [0, 40, 10, 0]                                 # Wait 40; Call ->
        calls.append(len(head) - 1)
    head += [4]
    off = len(head)
    for n, k in enumerate(order):
        w = gunfx.variant(k, seqs)
        for i, name, args in A.disasm(w):
            if w[i] == 4:
                w[i] = 11                                      # End -> Return
        head[calls[n]] = off - calls[n]
        subs += w
        off += len(w)
    words = head + subs
    anims = ndspy.narc.NARC(rom.getFileByName("a/0/1/0"))
    anims.files[move_ids()["Tackle"]] = struct.pack(f"<{len(words)}I", *words)
    if pad_to:     # keep the archive's size fixed (savestates) - padding goes after move 400's script (not used in the test battle),
        assert len(words) <= pad_to, (len(words), pad_to)   # not in the script (big scripts overflow the heap)
        anims.files[400] = anims.files[400] + bytes(4 * (pad_to - len(words)))
    rom.setFileByName("a/0/1/0", anims.save())
    rom.saveToFile(out_path)
    print("showcase:", order, len(words), "words ->", out_path)


if __name__ == "__main__":
    import sys
    showcase(sys.argv[1], sys.argv[2])
