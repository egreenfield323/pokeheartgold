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
          "skrrt": ("skrrt", 8000), "bling": ("bling", 11025), "chaching": ("chaching", 8000),
          "fwoosh": ("fwoosh", 8000), "smash": ("smash", 8000)}
# New samples live in the battle wave archive, which stays in the sound heap for the whole battle: every KB
# here is a KB less for the music and fanfares (too much and the game hangs loading the level-up fanfare).
# So only the sounds nothing in the game can do are new; the rest borrow the game's own battle effects:
BUILTIN = {"whoosh": 1916, "bonk": 1827, "splat": 1928, "spray": 1941, "zap": 1968, "alarm": 1824,
           "bass": 1973, "crack": 2005, "ember": 1937, "leer": 1930, "sand": 1923, "gust": 2043,
           "jet": 2064, "surf": 1944, "splash": 1945, "thunder": 2007, "rage": 1967, "flame": 2124, "leaf": 2121,
           "razor": 1885, "bite": 1934, "crunch": 1972, "slash": 1910, "smoke": 1983, "cough": 1924, "burn": 2010,
           "burn2": 2011, "chop": 2039, "shadow": 1923, "shadow2": 1903, "loyal": 1928, "loyal2": 1920,
           "confuse": 1855, "confuse2": 1838, "twave": 1970, "twave2": 1952, "dteam": 1836,
           "wpulse": 1999, "wpulse2": 2023, "faint": 1838, "toxic": 1859, "toxic2": 1979, "protect": 1990,
           "tdown": 1925, "tdown2": 1847, "tbolt": 2114, "tbolt2": 1952, "clock": 1841, "vineboom": 1973}    # Wing Attack, Pound, Egg Bomb, Water Gun, ThunderShock,
#                                            Screech, Earthquake, Bone Club, ...


# original move name (msg_0750) -> gunfx variant
#   1 sniper, 2 shotgun, 3 spray & pray, 4 point blank, 5 gangsta tilt (the everyday gun moves),
#   6 drive-by, 7 chain swing, 8 chain dangle, 9 make it rain, 10 full auto, 11 RPG (legendaries),
#   12 Molotov, 13 brick toss, 14 egg ya house, 15 hose down, 16 bat swing, 17 taser, 18 car alarm,
#   19 bass drop, 20 hot shot, 21 stare down, 22 talk trash, 23 pocket sand, 24 fan blast, 25 catch flight,
#   26 hydrant wave, 27 power line, 28 road rage, 29 fire breath (Molotov), 30 zaza leaf, 31 stomp out,
#   32 grill chomp, 33 hollow point, 34 switchblade, 35 hot box, 36 burnout, 37 hi-yah chop, 38 magic 8-ball,
#   39 loyalty, 40 flashlight, 41 stun taser, 42 bass boost, 43 squad up, 44 water bomb, 45 sneak diss,
#   46 dirty sprite, 47 duck n cover, 48 smackdown, 49 big taser, 50 clock it
MOVES = {
    "Tackle": 5, "Double Kick": 5, "Lick": 5,
    "Fury Attack": 3, "Triple Kick": 3, "Pin Missile": 3, "Spike Cannon": 3, "Swift": 3,
    "Scratch": 4,
    "Wing Attack": 2,
    "Iron Head": 1,
    "Quick Attack": 6,
    "Psychic": 7, "Confusion": 8,
    "Pay Day": 9,
    "Hyper Beam": 10,
    "Aeroblast": 11, "Sacred Fire": 11, "Roar of Time": 11, "Spacial Rend": 11, "Shadow Force": 11,
    "Psycho Boost": 11, "Doom Desire": 11, "Judgment": 11, "Crush Grip": 11, "Magma Storm": 11,
    "Fire Blast": 12,
    "Rock Throw": 13, "Rock Slide": 13,
    "Egg Bomb": 14,
    "Water Gun": 15, "Bone Club": 16, "ThunderShock": 17, "Screech": 18, "Earthquake": 19,
    "Hypnosis": 8, "Sky Attack": 11, "Giga Impact": 10,
    "Ember": 20, "Leer": 21, "Growl": 22, "Sand-Attack": 23, "Gust": 24,
    "Fly": 25, "Surf": 26, "Thunder": 27, "Dragon Rage": 28, "Flamethrower": 29, "Razor Leaf": 30, "Pound": 31,
    "Bite": 32, "Crunch": 33, "Slash": 34, "SmokeScreen": 35, "Flame Wheel": 36, "Brick Break": 37,
    "Shadow Ball": 38, "Return": 39,
    "Confuse Ray": 40, "Thunder Wave": 41, "Supersonic": 42, "Double Team": 43, "Water Pulse": 44,
    "Faint Attack": 45, "Toxic": 46, "Protect": 47, "Take Down": 48, "Thunderbolt": 49, "Foresight": 50,
}


def move_ids():
    gmm = subprocess.run(["git", "show", "77565981b:files/msgdata/msg/msg_0750.gmm"], cwd=ROOT,
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
    return {**seqs, **BUILTIN}


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


# the showcase pads these archives (with a trailing filler member nothing loads) to fixed sizes
SDAT_SIZE = 9_200_000
FIXED_SIZE = {"a/0/1/0": 600_000, "a/0/2/9": 2_900_000, "a/0/0/4": 14_745_600, "a/1/1/4": 1_310_720,
              "a/0/8/1": 5_832_704,
              # everything else the build touches (text, learnsets, trainers, icons, title, intro, item icons)
              "a/0/2/7": 5_111_808, "a/0/0/2": 65_536, "a/0/3/3": 65_536, "a/0/5/8": 1_835_008, "a/2/5/6": 655_360, "a/2/4/8": 196_608, "a/0/2/0": 655_360, "a/0/4/6": 917_504, "a/1/7/4": 589_824, "a/0/1/8": 524_288, "a/1/2/0": 196_608}


def showcase(rom_path, out_path, order=None, pad_to=None, pad_in_script=None):
    """Test copy of a built ROM where FMJ (Tackle) plays every effect back to back (or just `order`).
    pad_to pads the script to a fixed size so the ROM layout - and so savestates - stay the same."""
    import struct
    import ndspy.rom
    import animscript as A
    rom = ndspy.rom.NintendoDSRom.fromFile(rom_path)
    sdat = ndspy.soundArchive.SDAT(rom.getFileByName(SDAT))
    names = [n for n, _ in sdat.sequences]
    seqs = {**{k: names.index(f"SEQ_SE_HOOD_{k.upper()}") for k in SOUNDS}, **BUILTIN}
    narc = ndspy.narc.NARC(rom.getFileByName("a/0/2/9"))
    first = len(narc.files) - len(gunfx.DONOR)
    for i, ps in enumerate(gunfx.DONOR):
        gunfx.LOAD[ps] = first + i
    head, calls, subs = [], [], []
    if not order:                              # every effect - and Fly's second turn (97) right after its first,
        order = sorted(set(MOVES.values()))    # or the attacker stays vanished for the rest of the reel
        order.insert(order.index(25) + 1, 97)
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
    if pad_in_script:                  # same size as an earlier showcase (savestates) - zeros after End never run
        words += [0] * (pad_in_script - len(words))
    anims = ndspy.narc.NARC(rom.getFileByName("a/0/1/0"))
    anims.files[move_ids()["Tackle"]] = struct.pack(f"<{len(words)}I", *words)
    if pad_to:     # keep the archive's size fixed (savestates) - padding goes after move 400's script (not used in the test battle),
        assert len(words) <= pad_to, (len(words), pad_to)   # not in the script (big scripts overflow the heap)
        anims.files[400] = anims.files[400] + bytes(4 * (pad_to - len(words)))
    rom.setFileByName("a/0/1/0", anims.save())
    for path, target in FIXED_SIZE.items():    # fixed archive sizes: tweaks never move the ROM layout (savestates)
        narc = ndspy.narc.NARC(rom.getFileByName(path))
        if target is None:                     # sprite archives: today's size plus a quarter of headroom, rounded
            target = (len(rom.getFileByName(path)) * 5 // 4 + 0xFFFF) & ~0xFFFF
            FIXED_SIZE[path] = target
        narc.files.append(b"")
        room = target - len(narc.save())
        assert room >= 0, f"{path} outgrew its fixed showcase size; raise FIXED_SIZE"
        narc.files[-1] = bytes(room)
        assert len(narc.save()) == target
        rom.setFileByName(path, narc.save())
    sdat = rom.getFileByName(SDAT)           # the sound archive is read by its internal offsets: pad the tail
    assert len(sdat) <= SDAT_SIZE, "sound archive outgrew its fixed showcase size; raise SDAT_SIZE"
    rom.setFileByName(SDAT, sdat + bytes(SDAT_SIZE - len(sdat)))
    rom.saveToFile(out_path)
    print("showcase:", order, len(words), "words ->", out_path)


if __name__ == "__main__":
    import sys
    showcase(sys.argv[1], sys.argv[2])
