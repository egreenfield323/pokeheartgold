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
           "tdown": 1925, "tdown2": 1847, "tbolt": 2114, "tbolt2": 1952, "clock": 1841, "vineboom": 1973,
           "vwhip": 2123, "vwhip2": 2127, "psting": 1905, "psting2": 2120, "twhip": 1844, "absorb": 1956,
           "absorb2": 2003, "sshot": 1919, "sshot2": 1964, "bubble": 1997,
           "sdestruct": 1993, "kaboom": 2113, "rollout": 1920, "rollout2": 1954, "focus": 1965, "swipe": 1908,
           "aring": 2085, "mlook": 1948, "mlook2": 1985, "sucker": 1849, "disable": 1840, "sleep": 1960,
           "flop": 1826, "flail": 1833, "flail2": 1920, "raindance": 2044, "assure": 1926, "wfall": 1995,
           "wfall2": 2060, "peck": 1926, "harden": 2038, "curse": 1830, "curse2": 2016,
           "bbeam2": 2024, "wsport": 2118, "horn": 1926, "mudshot": 2045, "dslap": 1828, "acid": 1999,
           "hpump": 2109, "wslap": 1977, "brine": 2070, "tspikes": 1922, "sludge": 2060, "constrict": 1918,
           "twister": 1837, "dcharge": 1969, "dcurl": 1864, "dcurl2": 2006, "explo": 2096, "astonish": 2008,
           "astonish2": 2056, "bdrum": 2017, "sbomb": 1998, "dedge": 1846, "amnesia": 1991, "rest": 2013,
           "aslash": 1884, "bslam": 1927, "mbomb": 2093, "sunny": 1531, "sface": 1933, "sface2": 1948,
           "sboom": 1851, "smog": 1985, "lscreen": 1990, "sbeam": 1530, "reflect": 1990, "nshade": 1877,
           "acutter": 1913, "spark": 1971, "spark2": 2031, "mdrain": 1999, "msport": 1976, "msport2": 2046,
           "psych": 1950, "gyro": 2066, "gyro2": 2068, "yawn": 2047, "yawn2": 2057, "sscent": 2037,
           "rspin": 1883, "aeroblast": 2121, "xsense": 1930, "xsense2": 2113, "hfang": 1934, "haze": 1989,
           "barrier": 1988, "zen": 1896, "zen2": 1874, "lseed": 1839, "swagger": 2029, "safeguard": 2030,
           "rpolish": 2041, "ishard": 1852, "revenge": 1927, "mbomb2": 1894, "cbeam": 1882, "cbeam2": 1895,
           "minimize": 1984, "ifang": 1852, "lockon": 1801, "lockon2": 1840, "hhand": 2035, "sedge": 1972,
           "attract": 2025, "captivate": 1862, "iwind": 1915, "epower": 1938, "twind": 2121, "blizzard": 1946}    # Wing Attack, Pound, Egg Bomb, Water Gun, ThunderShock,
#                                            Screech, Earthquake, Bone Club, ...


# original move name (msg_0750) -> gunfx variant
#   1 sniper, 2 shotgun, 3 spray & pray, 4 point blank, 5 gangsta tilt (the everyday gun moves),
#   6 drive-by, 7 chain swing, 8 chain dangle, 9 make it rain, 10 full auto, 11 RPG (legendaries),
#   12 Molotov, 13 brick toss, 14 egg ya house, 15 hose down, 16 bat swing, 17 taser, 18 car alarm,
#   19 bass drop, 20 hot shot, 21 stare down, 22 talk trash, 23 pocket sand, 24 fan blast, 25 catch flight,
#   26 ride da wave (Surf), 27 power line, 28 road rage, 29 fire breath (Molotov), 30 zaza leaf, 31 stomp out,
#   32 grill chomp, 33 hollow point, 34 switchblade, 35 hot box, 36 burnout, 37 hi-yah chop, 38 magic 8-ball,
#   39 loyalty, 40 flashlight, 41 stun taser, 42 bass boost, 43 squad up, 44 water bomb, 45 sneak diss,
#   46 dirty sprite, 47 duck n cover, 48 smackdown, 49 big taser, 50 clock it, 51 belt whip, 52 shiv,
#   53 twerk on em, 54 tax, 55 silly string, 56 spit, 57 lace up, 58 go out loud, 59 roll out, 60 lock in,
#   61 dome check, 62 pickpocket, 63 pool float, 64 block off, 65 cheap shot, 66 jam the gun, 67 sleeper,
#   68 reload, 69 flop, 70 windmill, 71 make it rain (money gun), 72 insurance, 73 body bag, 74 beam me up,
#   75 poke, 76 duct tape, 77 kevlar, 78 curse out, 79 spit stream, 80 sprinkler, 81 horn blast, 82 mud pie,
#   83 backhand, 84 battery acid, 85 fire hose, 86 rise n slap, 87 dirty shiv, 88 salty, 89 dirty nails,
#   90 stun gun (tranq dart), 91 gutter slop, 92 pebble spray, 93 live socket, 94 fetal pos., 95 choke hold,
#   96 tornado, 98 kaboom, 100 jumpscare (97 / 99 are test variants, 101-114 effect animations),
#   120 irs audit, 121 beat the box, 122 stink bomb, 123 kamikaze, 124 splash whip, 125 didnt see it, 126 nap,
#   127 chase down, 128 paper cut, 129 pepper spray, 130 belly flop, 131 pigeon drop, 132 heat lamp,
#   133 grill flash, 134 trunk rattle, 135 exhaust, 136 riot shield, 137 full bars, 138 bulletproof (glass),
#   139 night shift, 140 wind shank (ceiling fan), 141 spark up, 142 big tax, 143 mud bath, 144 hype up,
#   145 fidget spin, 146 neon beam, 147 snooze (terms & conditions), 148 cologne, 149 spin the block (bmx),
#   150 air force (Aeroblast: jets + the giant sneaker stomp), 151 sixth sense (Extrasensory: the sky eye),
#   152 gold grill (wind-up teeth), 153 air it out, 154 barricade (furniture), 155 zen dome, 156 freeloader,
#   157 drip check, 158 yell woop, 159 security, 160 wax on, 161 beef, 162 big bass (the fish), 163 ice chip,
#   164 get even (the list), 165 car magnet, 166 one-two, 167 power bank, 168 duck down (clothes rack),
#   169 brain freeze, 170 lock on (binoculars), 171 night shank, 172 got ya back (handshake), 173 ice out,
#   174 stone cold, 175 rizz up (date night), 176 pickup line, 177 ice cold (window AC), 178 ground game
#   (pothole), 179 tailgate, 180 iced out (shaved-ice machine), 181 photo op (ring light)
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
"Sacred Fire": 11, "Roar of Time": 11, "Spacial Rend": 11, "Shadow Force": 11,
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
    "Vine Whip": 51, "Poison Sting": 52, "Tail Whip": 53, "Absorb": 54, "String Shot": 55, "Bubble": 56,
    "Agility": 57, "Selfdestruct": 58, "Rollout": 59, "Focus Energy": 60, "Headbutt": 61, "Fury Swipes": 62,
    "Aqua Ring": 63, "Mean Look": 64, "Sucker Punch": 65, "Disable": 66, "Sleep Powder": 67, "Recover": 68,
    "Splash": 69, "Flail": 70, "Rain Dance": 71, "Assurance": 72, "Slam": 73, "Waterfall": 74, "Peck": 75,
    "Wrap": 76, "Harden": 77, "Curse": 78,
    "BubbleBeam": 79, "Water Sport": 80, "Horn Attack": 81, "Mud Shot": 82, "DoubleSlap": 83, "Acid": 84,
    "Hydro Pump": 85, "Wake-Up Slap": 86, "Poison Jab": 87, "Brine": 88,
    "Toxic Spikes": 89, "Stun Spore": 90, "Sludge": 91, "Rock Blast": 92, "Discharge": 93, "Defense Curl": 94,
    "Constrict": 95, "Twister": 96, "Explosion": 98, "Astonish": 100,
    "Giga Drain": 120, "Belly Drum": 121, "Sludge Bomb": 122, "Double-Edge": 123, "Aqua Tail": 124, "Amnesia": 125,
    "Rest": 126, "Pursuit": 127, "Air Slash": 128, "PoisonPowder": 129,
    "Body Slam": 130, "Mud Bomb": 131, "Sunny Day": 132, "Scary Face": 133, "SonicBoom": 134, "Smog": 135,
    "Light Screen": 136, "Signal Beam": 137, "Reflect": 138, "Night Shade": 139, "Air Cutter": 140, "Spark": 141,
    "Mega Drain": 142, "Mud Sport": 143, "Psych Up": 144,
    "Gyro Ball": 145, "Aurora Beam": 146, "Yawn": 147, "Sweet Scent": 148, "Rapid Spin": 149,
    "Aeroblast": 150, "Extrasensory": 151,
    "Hyper Fang": 152, "Haze": 153, "Barrier": 154, "Zen Headbutt": 155, "Leech Seed": 156, "Swagger": 157,
    "Roar": 158, "Safeguard": 159, "Rock Polish": 160, "Rage": 161,
    "Magnitude": 162, "Ice Shard": 163, "Revenge": 164, "Magnet Bomb": 165, "Double Hit": 166, "Charge Beam": 167,
    "Minimize": 168, "Ice Fang": 169, "Lock-On": 170, "Night Slash": 171,
    "Helping Hand": 172, "Ice Beam": 173, "Stone Edge": 174, "Attract": 175, "Captivate": 176, "Icy Wind": 177,
    "Earth Power": 178, "Tailwind": 179, "Blizzard": 180, "Synthesis": 181,
    "Cut": 182, "Strength": 183, "Rock Smash": 184, "Dig": 185, "Fire Punch": 186,
    "ThunderPunch": 187, "AncientPower": 188, "Psybeam": 189, "Mud-Slap": 190, "Fire Fang": 191,
    "Thunder Fang": 192, "Charm": 193, "Growth": 194, "Stomp": 195, "Payback": 196,
    "Swords Dance": 197, "Aerial Ace": 198, "Thief": 199, "Sing": 200, "Sandstorm": 201,
    "Encore": 203, "Baton Pass": 204, "Metal Claw": 205, "Fire Spin": 206, "Taunt": 207, "Knock Off": 208, "Whirlwind": 209, "Seismic Toss": 210, "Low Kick": 211, "Dark Pulse": 212, "Future Sight": 213, "Fake Out": 214, "Nasty Plot": 215, "Iron Defense": 216, "Uproar": 217, "Endure": 218, "Last Resort": 219, "Close Combat": 220, "Calm Mind": 221, "Powder Snow": 222, "Thrash": 223, "Bounce": 224, "X-Scissor": 225, "Lava Plume": 226, "Stockpile": 227, "Counter": 228, "Crabhammer": 229, "Metal Sound": 230, "Bug Buzz": 231, "Whirlpool": 232,
    "Natural Gift": 234, "Roost": 235, "Fling": 236, "Dream Eater": 237, "Dragon Claw": 238, "U-turn": 239, "Dragon Pulse": 240, "Silver Wind": 241, "Hail": 242, "Embargo": 243, "Will-O-Wisp": 244, "Shock Wave": 245, "False Swipe": 246, "Substitute": 247, "Shadow Claw": 248, "Iron Tail": 249, "Hidden Power": 250, "Bullet Seed": 251, "Rock Tomb": 252, "Overheat": 253, "Energy Ball": 254, "Sleep Talk": 255, "Skill Swap": 256, "Focus Blast": 257, "Recycle": 258, "Pluck": 259, "Avalanche": 260, "Trick Room": 261, "Flash Cannon": 262, "Bulk Up": 263,
    "Torment": 264, "Snatch": 265, "Focus Punch": 266, "Drain Punch": 267, "Steel Wing": 268, "Flash": 269, "Stealth Rock": 270, "Grass Knot": 271, "Frustration": 272, "Facade": 273, "Secret Power": 274, "Rock Climb": 275, "Feint": 276, "Mist": 277, "Charge": 278, "Bug Bite": 279, "Wring Out": 280, "Magical Leaf": 281, "Endeavor": 282, "Odor Sleuth": 283, "Withdraw": 284, "Power Gem": 285, "Leech Life": 286, "Detect": 287, "Leaf Storm": 288, "Teleport": 289, "Spit Up": 290, "Ingrain": 291, "Fury Cutter": 292, "Destiny Bond": 293,
}


# effect animation (a/0/6/1, BATTLE_ANIMATION_*) -> gunfx variant: 100 + the effect id
EFFECTS = {1: 101, 2: 102, 3: 103, 4: 104, 5: 105, 6: 106, 7: 107, 8: 108, 9: 109, 10: 110, 12: 112, 13: 113, 14: 114}


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
    effects = ndspy.narc.NARC(rom.getFileByName("a/0/6/1"))
    for eid, k in EFFECTS.items():
        w = gunfx.variant(k, seqs)
        effects.files[eid] = struct.pack(f"<{len(w)}I", *w)
    rom.setFileByName("a/0/6/1", effects.save())
    import ballfx
    import codepatch
    import evofx
    ballfx.patch(rom)
    evofx.patch(rom)
    codepatch.patch(rom)                                       # (walking-homie text: the hood bank's too big to load whole)
    print(f"battle effects: {len(MOVES)} moves, {len(gunfx.DONOR)} particle kits, {len(seqs)} sounds")


# the showcase pads these archives (with a trailing filler member nothing loads) to fixed sizes
SDAT_SIZE = 9_200_000
FIXED_SIZE = {"a/0/1/0": 700_000, "a/0/2/9": 4_000_000, "a/0/0/4": 14_745_600, "a/1/1/4": 1_310_720,
              "a/0/8/1": 5_832_704, "a/0/0/8": 262_144, "a/0/9/5": 1_048_576, "a/0/6/1": 131_072, "a/1/1/9": 65_536,
              # everything else the build touches (text, learnsets, trainers, icons, title, intro, item icons)
              "a/0/2/7": 5_111_808, "a/0/0/2": 65_536, "a/0/3/3": 65_536, "a/0/5/8": 1_835_008, "a/2/5/6": 655_360, "a/2/4/8": 196_608, "a/0/2/0": 655_360, "a/0/4/6": 917_504, "a/1/7/4": 589_824, "a/0/1/8": 524_288, "a/1/2/0": 196_608}


def pad(rom, only=None):
    """Pad the archives the build touches (or just `only`) to fixed sizes, so tweaks never move the ROM layout
    (savestates). The padding is an extra all-zero member at the end (re-padding replaces it)."""
    for path, target in FIXED_SIZE.items():
        if only is not None and path not in only:
            continue
        narc = ndspy.narc.NARC(rom.getFileByName(path))
        if len(narc.files) > 1 and narc.files[-1] and not any(narc.files[-1]):
            narc.files.pop()                   # already padded once: redo it
        if target is None:                     # sprite archives: today's size plus a quarter of headroom, rounded
            target = (len(rom.getFileByName(path)) * 5 // 4 + 0xFFFF) & ~0xFFFF
            FIXED_SIZE[path] = target
        narc.files.append(b"")
        room = target - len(narc.save())
        assert room >= 0, f"{path} outgrew its fixed showcase size; raise FIXED_SIZE"
        narc.files[-1] = bytes(room)
        assert len(narc.save()) == target
        rom.setFileByName(path, narc.save())
    if only is not None:
        return
    sdat = rom.getFileByName(SDAT)           # the sound archive is read by its internal offsets: pad the tail
    assert len(sdat) <= SDAT_SIZE, "sound archive outgrew its fixed showcase size; raise SDAT_SIZE"
    rom.setFileByName(SDAT, sdat + bytes(SDAT_SIZE - len(sdat)))
    size = len(rom.save())                   # the padding can push it past the chip size in the header (128 MB):
    while 0x20000 << rom.deviceCapacity < size:   # DeSmuME then calls the header invalid
        rom.deviceCapacity += 1


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
    real = len(narc.files) - (1 if narc.files[-1] and not any(narc.files[-1]) else 0)   # skip pad()'s filler member
    first = real - len(gunfx.DONOR)
    for i, ps in enumerate(gunfx.DONOR):
        gunfx.LOAD[ps] = first + i
    if order:                                  # kits nothing here loads (the reel + the effect animations) are blanked
        used = {ps for k in [*order, *EFFECTS.values()] for ps in gunfx.KITS[k]}   # so a/0/2/9 fits its fixed size
        for i, ps in enumerate(gunfx.DONOR):
            if ps not in used:
                narc.files[first + i] = b""
        rom.setFileByName("a/0/2/9", narc.save())
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
    ids = move_ids()
    for name in MOVES:          # the test battle only ever uses Tackle: stub the other hood scripts (just End) so the
        if name != "Tackle":    # archive keeps its fixed size (savestates) however many animations there are
            anims.files[ids[name]] = struct.pack("<I", 4)
    anims.files[ids["Tackle"]] = struct.pack(f"<{len(words)}I", *words)
    if pad_to:     # keep the archive's size fixed (savestates) - padding goes after move 400's script (not used in the test battle),
        assert len(words) <= pad_to, (len(words), pad_to)   # not in the script (big scripts overflow the heap)
        anims.files[400] = anims.files[400] + bytes(4 * (pad_to - len(words)))
    rom.setFileByName("a/0/1/0", anims.save())
    pad(rom)
    rom.saveToFile(out_path)
    print("showcase:", order, len(words), "words ->", out_path)


if __name__ == "__main__":
    import sys
    showcase(sys.argv[1], sys.argv[2])
