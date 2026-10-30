"""Gunshot battle effects for Hood HeartGold: muzzle flashes at the gun, tracers, casings, smoke, crosshairs.

Three particle files are rebuilt from donors (a/0/2/9) with new textures and retuned emitters:
  GUN   (Pin Missile's):  SPARK spark burst, FLASH big muzzle flash, TRACER bullet streak (follows its emitter)
  KIT   (file 62):        CASING brass casings that fly out and fall, CROSS red crosshair that zooms in
  SMOKE (file 84):        PUFF gun smoke, DIRT dirt kicked up by bullets
build_files(narc_files) -> {donor id: new bytes}; variant(k, sounds) -> animation script words.
"""
import math
import struct

import fxart
import spa

GUN, KIT, SMOKE, CAR, BLING, CASH, ROCKET = 0, 1, 2, 3, 4, 5, 6  # particle system slots used by the scripts
BOTTLE, BRICK, EGG, FIRE, HOUSE, YOLK = 7, 8, 9, 10, 11, 12
HYDRANT, JET, SPLASH, SLUGGER, TASER, BOLTS, FOB, RINGS, SUB, CRACK = range(13, 23)
CHIPS, BURST, SHADES, BUBBLE, POCKET, SAND, FAN, WIND, GLINT = range(23, 32)
(PLANE, WHAM, WAVE, DUCK, CABLE, XRAY, HONK, CONE, BOOZE, BREATH, LEAF, HAZE, BOOT, STOMP, TOPJAW, BOTJAW, GLITZ,
 SLUG, SHATTER, SLASH, TIRE, SMOG, COUGH, WHEEL, TRAIL, BLOCKS, CHOP, HIYAH, EIGHT, ANSWER, HEART) = range(32, 63)
(TORCH, BEAM, HUH, STUN, STATIC, ZZZT, BOOMBOX, SOUNDWAVE, BWOMP, SQUAD, SQUAD2, SQUADUP, BALLOON, DRENCH, SPLOOSH,
 DISS, SLAP, OOOH, CUP, GOOP, DIRTY, LID, NOPE, CHAIR, CLANG, SMACKDN, BIGTASER, MEGABOLT, BZZT,
 EYES, CIRCLE, CLOCKED) = range(63, 95)
(BELT, WELT, WHAP, SHIV, SHIVD, TWERK, DEFDOWN, BRUH, STAMP, TAXED, COINS, CAN, TANGLE, STUCK, SPIT, GOBSPLAT,
 PTOO) = range(95, 112)
(KICKS, LACED, CRATE, FWBURST, BOOOM, CART, CARTL, CRASH, PHONES, LOCKED, BUMP, DOMECHK, GRAB, YANK,
 YOINK) = range(112, 127)
(POOLF, CHILLIN, TAPE, BARRIER, NOEXIT, LOOKBUB, FIST, CHEAP, JAMGUN, JAMMED, CIGAR, SNOOZE, NIGHT, MAG, HEALS,
 RELOADED) = range(127, 143)
# effect animations (a/0/6/1): status conditions, items, stat changes, level up
(HENNY, AHHH, DRIPS, STASH, STASHG, SNORE, SNOREZ, BADBATCH, TOXB, BURNS, BURNF, ICED, ICEG, TASED, JAGS, WHERE,
 QMARKS, CRUSH, HEARTS2, GAINS, UPS, DOWNBAD, DOWNS, CLOUT, CLOUTUPS) = range(143, 168)
STOREBAG, LOOKS = 168, 169
FELICIA, CLAIM = 170, 171                                     # Catch Flight: BYE FELICIA!, the suitcase
(TUMBLE, SCORE, ARMS, HANDS, MGUN, BILLRAIN, RAINSIGN, CHECK, PAYOUT, CASHSPARK, BODYBAG, SLAMDUST, BODIED,
 GEYSER, SPLOSH, BEAMUP, FINGER, POKED, TAPEROLL, TAPED, VEST, RICO, BPROOF, JAR, CUSS) = range(172, 197)
(MIC, ROAST, SPEAKER, SOAKER, AIRHORN, PIE, MUDSPLAT, BACKHAND, SLAPSTAR, NINEVOLT, ACIDSPLAT, FIREHOSE, WETHIT, ALARMCLK,
 CHANCLA, SPOON, SHAKER, SALTY, NAILS, BOOT, DUMPSTER, SLOPBALL, PEBBLE, YOUUP, OUTLET, ZAPRING, PAYLIGHTS, BLANKIE,
 RAINCLOUD, HEADLOCK, FUNNEL, MICRO, BOOMCLOUD, SERVER, AUDIT, WALLET, BUCKET, TIPS, SHOE, STINKCLOUD,
 DIRTBIKE, DURAG, ZIPPED, SOULFOOD, CHOPPER, DASHDUST, BILLS10, PEPPER, MILK) = range(197, 246)
(BOARD, BIGSPLASH, PIGEON, POOPSPLAT, TANNING, SUN, HEAT, GRILL, SWEATY, TRUNK, FEATHERS, HOOPTIE, SOOT, SHIELD,
 TOMSPLAT, PHONESIG, WIFI, STOREGLASS, GLASSFX, CLOCKIN, JANITOR, CFAN, FANBLADES, BIC, ZAPAURA, REGISTER, RECEIPT,
 COINS2, SPA, SPASTEAM, HYPE, CONFETTI) = range(246, 278)
(FIDGET, WHIRLS, NEONSIGN, NEONBEAM, BOOK, COLOGNE, FUMES11, BMX) = range(278, 286)
LAST_KIT = BMX
DONOR = {GUN: 73, KIT: 62, SMOKE: 84, CAR: 82, BLING: 168, CASH: 47, ROCKET: 349,
         BOTTLE: 349, BRICK: 349, EGG: 349, FIRE: 84, HOUSE: 168, YOLK: 84,
         HYDRANT: 349, JET: 84, SPLASH: 84, SLUGGER: 168, TASER: 349, BOLTS: 349, FOB: 349, RINGS: 62,
         SUB: 168, CRACK: 168,
         CHIPS: 82, BURST: 84, SHADES: 168, BUBBLE: 349, POCKET: 82, SAND: 84, FAN: 82, WIND: 84,
         GLINT: 349,
         PLANE: 82, WHAM: 168, WAVE: 82, DUCK: 349, CABLE: 168, XRAY: 82, HONK: 82, CONE: 349, BOOZE: 349,
         BREATH: 84, LEAF: 82, HAZE: 84, BOOT: 168, STOMP: 82, TOPJAW: 168, BOTJAW: 168, GLITZ: 349, SLUG: 82,
         SLASH: 82, TIRE: 349, SMOG: 84, COUGH: 349, WHEEL: 82, TRAIL: 84, BLOCKS: 82, CHOP: 168,
         HIYAH: 168, EIGHT: 82, ANSWER: 168, HEART: 82,
         TORCH: 82, BEAM: 168, HUH: 168, STUN: 82, STATIC: 168, ZZZT: 168, BOOMBOX: 82, SOUNDWAVE: 84, BWOMP: 168,
         SQUAD: 82, SQUAD2: 168, SQUADUP: 168, BALLOON: 349, DRENCH: 82, SPLOOSH: 168, DISS: 168, SLAP: 82,
         OOOH: 168, CUP: 349, GOOP: 84, DIRTY: 168, LID: 82, NOPE: 168, CHAIR: 82, CLANG: 168, SMACKDN: 168,
         BIGTASER: 82, MEGABOLT: 168, BZZT: 168, EYES: 82, CIRCLE: 168, CLOCKED: 168,
         BELT: 168, WELT: 82, WHAP: 168, SHIV: 82, SHIVD: 168, TWERK: 82, DEFDOWN: 168, BRUH: 168, STAMP: 168,
         TAXED: 168, COINS: 82, CAN: 82, TANGLE: 168, STUCK: 168, SPIT: 349, GOBSPLAT: 168, PTOO: 168,
         KICKS: 82, LACED: 168, CRATE: 82, FWBURST: 168, BOOOM: 168, CART: 82, CARTL: 82, CRASH: 168, PHONES: 82,
         LOCKED: 168, BUMP: 168, DOMECHK: 168, GRAB: 168, YANK: 168, YOINK: 168,
         POOLF: 82, CHILLIN: 168, TAPE: 82, BARRIER: 168, NOEXIT: 168, LOOKBUB: 168, FIST: 168, CHEAP: 168,
         JAMGUN: 82, JAMMED: 168, CIGAR: 82, SNOOZE: 84, NIGHT: 168, MAG: 168, HEALS: 84, RELOADED: 168,
         HENNY: 168, AHHH: 168, DRIPS: 84, STASH: 168, STASHG: 84, SNORE: 168, SNOREZ: 84, BADBATCH: 168, TOXB: 84,
         BURNS: 168, BURNF: 84, ICED: 168, ICEG: 84, TASED: 168, JAGS: 84, WHERE: 168, QMARKS: 84, CRUSH: 168,
         HEARTS2: 84, GAINS: 168, UPS: 84, DOWNBAD: 168, DOWNS: 84, CLOUT: 168, CLOUTUPS: 84,
         STOREBAG: 168, LOOKS: 168, FELICIA: 168, CLAIM: 168,
         TUMBLE: 82, SCORE: 168, ARMS: 82, HANDS: 168, MGUN: 82, BILLRAIN: 84, RAINSIGN: 168, CHECK: 168,
         PAYOUT: 168, CASHSPARK: 84, BODYBAG: 168, SLAMDUST: 84, BODIED: 168, GEYSER: 82, SPLOSH: 84, BEAMUP: 168,
         FINGER: 82, POKED: 168, TAPEROLL: 82, TAPED: 168, VEST: 168, RICO: 84, BPROOF: 168, JAR: 82, CUSS: 168,
         MIC: 82, ROAST: 84, SPEAKER: 168, SOAKER: 82, AIRHORN: 82, PIE: 349,
         MUDSPLAT: 168, BACKHAND: 168, SLAPSTAR: 84, NINEVOLT: 349, ACIDSPLAT: 168,
         FIREHOSE: 82, WETHIT: 84, ALARMCLK: 82, CHANCLA: 168, SPOON: 82,
         SHAKER: 82, SALTY: 168, NAILS: 84, BOOT: 168, DUMPSTER: 82, SLOPBALL: 349,
         PEBBLE: 349, YOUUP: 168, OUTLET: 82, ZAPRING: 84, PAYLIGHTS: 168, BLANKIE: 168, RAINCLOUD: 82,
         HEADLOCK: 82, FUNNEL: 82, MICRO: 82, BOOMCLOUD: 168, SERVER: 168,
         AUDIT: 82, WALLET: 168, BUCKET: 82, TIPS: 84, SHOE: 349,
         STINKCLOUD: 84, DIRTBIKE: 82, DURAG: 82, ZIPPED: 168,
         SOULFOOD: 82, CHOPPER: 82, DASHDUST: 84, BILLS10: 82, PEPPER: 82, MILK: 82,
         BOARD: 82, BIGSPLASH: 168, PIGEON: 82, POOPSPLAT: 168, TANNING: 82, SUN: 168, HEAT: 84, GRILL: 82, SWEATY: 84,
         TRUNK: 82, FEATHERS: 84, HOOPTIE: 82, SOOT: 84, SHIELD: 82, TOMSPLAT: 168, PHONESIG: 168, WIFI: 84,
         STOREGLASS: 168, GLASSFX: 84, CLOCKIN: 82, JANITOR: 82, CFAN: 82, FANBLADES: 82, BIC: 82, ZAPAURA: 84,
         REGISTER: 168, RECEIPT: 82, COINS2: 84, SPA: 82, SPASTEAM: 84, HYPE: 168, CONFETTI: 84,
         FIDGET: 82, WHIRLS: 84, NEONSIGN: 168, NEONBEAM: 84, BOOK: 82, COLOGNE: 82, FUMES11: 84, BMX: 82}
LOAD = dict(DONOR)                                            # particle file each kit loads (battlefx repoints)   # small files: the battle heap can't fit big ones twice
SPARK, FLASH, TRACER = 0, 1, 2
CASING, CROSS = 0, 1
PUFF, DIRT = 1, 0
RIDE, WINDOW = 2, 0                                           # CAR: the lowrider + its gun flashes (riding along)
PARKED, BOUNCE = 3, 1                                         # CAR: parked (stays), one hydraulics-bounce frame
STAND = 0                                                     # HYDRANT / TASER / FOB: the prop, standing there
JET_E, JET_P = 0, 1                                           # JET: water shot from the nozzle at the enemy / player
SWING_E, SWING_P = 0, 1                                       # SLUGGER: the bat swung by the player / the enemy
TASER_P = 1                                                   # TASER: the device pointing left (enemy holding it)
ZAP = 0                                                       # BOLTS: crackling lightning bolts
RING = 1                                                      # RINGS: a sound-wave ring blasting outward
BOX, PUMP = 0, 1                                              # SUB: the subwoofer, the cone pumping on a beat
SPLIT = 1                                                     # CRACK: the ground splitting open
BAG, CHIP_E, CHIP_P = 2, 0, 1                                 # CHIPS: the HOT chips bag, chips thrown each way
TONGUE, EMBER = 1, 0                                          # BURST: flames licking up, embers
SLIDE, LANDED = 0, 1                                          # SHADES: one pose of the slide down, the shades on
TING, SWEAT = 2, 1                                            # GLINT: a lens glint, sweat drops flying off
TALK, BANG = 0, 2                                             # BUBBLE: a cussing speech bubble (flown), a red "!"
SIGN, GRAIN_E, GRAIN_P = 2, 0, 1                              # POCKET: "POCKET SAND!", sand thrown each way
CLOUD = 1                                                     # SAND: the dust cloud
BODY, BLADES = 2, 0                                           # FAN: the box fan, its spinning blades
GUST_E, GUST_P = 0, 1                                         # WIND: gust lines blowing at the enemy / the player
FAN_AT = {"player": (-30, 22), "enemy": (30, 6)}            # the fan, behind the attacker (px from its origin)
TARGET_FROM_ATTACKER = {"player": (121, 59), "enemy": (-121, -59)}   # defender origin - attacker origin, px
GUST_AIM = (0, 10)                                            # where on the target the wind hits
GUST_FRAMES = 13


def aim_path(side, frm, aim):
    """(dx, dy) screen px from `frm` (px from the attacker) to `aim` (px from the target), y up."""
    (tx, ty) = TARGET_FROM_ATTACKER[side]
    return tx + aim[0] - frm[0], ty + aim[1] - frm[1]


def gust_path(side):
    """(dx, dy) screen px from the fan to the target (y up)."""
    return aim_path(side, FAN_AT[side], GUST_AIM)


BAG_AT = {"player": (26, 22), "enemy": (-26, 22)}           # the chip bag, in their hand
CHIP_AIM, CHIP_FRAMES = (0, 14), 12
HAND_AT = {"player": (16, 18), "enemy": (-16, 14)}          # where the sand comes out
SAND_AIM, SAND_FRAMES = (0, 24), 10                          # right in the face
SHADES_AT = {"player": (40, 50), "enemy": (-46, 20)}        # where the shades land (between them, up high)
SHADES_DROP = 32

# ---- set 4 emitters (per kit)
POSE, HOLD = 0, 1                                             # the 64px stop-motion kits: one pose, the held one
POP = 0                                                       # the 64px sign kits: the burst popping up
PASS, JETSMOKE = 2, 0                                         # JET: the jet's pass, smoke
SUIT = 1                                                      # CLAIM: the suitcase (a kit drawn over the jet's)
WAVE_E, WAVE_P, FOAM = 2, 3, 0                                # WAVE: a crest rolling each way, foam splashing up
DUCK_E, DUCK_P = 0, 1                                         # DUCK: the rubber duck riding along each way
BONES, SPARKS = 2, 0                                          # XRAY: the flickering skeleton, sparks
HONK_A, HONK_B, STEAM = 2, 3, 0                               # HONK: two HONK!s, steam off their head
SWIG, LIGHTER = 0, 2                                          # BOOZE: the bottle at their mouth, the lighter flame
FIRE_E, FIRE_P = 0, 1                                         # BREATH: fire breathed each way
LEAF_E, LEAF_P, BIGLEAF = 0, 1, 2                             # LEAF: leaves thrown each way, the big leaf
HAZE1 = 1                                                     # HAZE: the haze rolling over the target
DUST = 0                                                      # STOMP: dust thrown up
SPARKLE = 2                                                   # GLITZ: bling sparkles
DOT, HOLE, IMPACT = 2, 3, 0                                   # SLUG: the laser-sight dot, the bullet hole, sparks
SLASH_A, SLASH_B, SLASH_C, GLEAM = 1, 2, 3, 0                 # SLASH: three slash angles, the blade's gleam
TIRE_UP, TIRE_FLAT, HISS = 0, 1, 2                            # TIRE: the tire, the flat, air hissing out
SMOG1, SMOG2 = 1, 0                                           # SMOG: big smoke everywhere, wisps at the target
PUFFUP = 0                                                    # COUGH: a *cough* cloud rising
SPIN, ROLL, SMOKE1 = 2, 3, 0                                  # WHEEL: spinning in place, rolling (flown), tire smoke
FIRETRAIL = 1                                                 # TRAIL: flames left behind the wheel (flown)
HALF_L, HALF_R, CHUNKS = 2, 3, 0                              # BLOCKS: the stack's two halves (poses), chunks
CHARGE, ROLL8, WISPS = 3, 2, 0                                # EIGHT: the 8-ball growing, rolling (flown), dark wisps
LOCKET, SLAM, HEARTS_E, HEARTS_P = 2, 3, 0, 1                 # HEART: the pendant, it flying in, hearts each way
# ---- set 5 emitters (per kit)
TORCH_E, TORCH_P, SWIRL = 1, 2, 0                             # TORCH: the flashlight aimed each way, dizzy swirls
BEAM_E, BEAM_P = 0, 1                                         # BEAM: the cone of light each way
STUN_E, STUN_P, ARC_E, ARC_P = 1, 2, 0, 3                     # STUN: the stun gun each way, crackles shot each way
RING_X, RING_HOLD = 0, 1                                      # STATIC: a ring blasting out, the ring holding them
BOX5, THUMP, NOTES_E, NOTES_P = 1, 2, 0, 3                    # BOOMBOX: the boombox, it pumping, notes each way
SWAVE_E, SWAVE_P = 0, 1                                       # SOUNDWAVE: ")" arcs each way
FIG, FIG_S, POOF = 1, 2, 0                                    # SQUAD: a homie (big / small), the poof he appears in
FIG2, FIG2_S = 0, 1                                           # SQUAD2: the other homie (big / small)
DROPS = 2                                                     # BALLOON: water dripping off them
CROWN, SPLASHDROPS = 1, 0                                     # DRENCH: the splash, drops flying
SLAP_POSE, SLAP_HOLD, POWS = 1, 2, 0                          # SLAP: the palm coming down, landed, impact lines
HELD, BUBBLES = 0, 2                                          # CUP: the cup in hand, bubbles rising off them
GOOP_SPLAT, GOOP_DRIPS = 1, 0                                 # GOOP: the purple splat, drips
LIDUP, LIDFLASH, PINGS = 1, 2, 0                              # LID: the shield, its flash, deflection pings
CHAIR_POSE, CHAIR_HOLD, STARS = 1, 2, 0                       # CHAIR: the chair coming down, landed, dizzy stars
BIG_E, BIG_P, ZIGS = 1, 2, 0                                  # BIGTASER: the XL taser each way, crackling
STRIKE, STRIKE2 = 0, 1                                        # MEGABOLT: the bolt, a second smaller one
EYES_R, EYES_L = 1, 2                                         # EYES: the eyes emoji looking right / left
TORCH_AT = {"player": (28, 30), "enemy": (-28, 30)}          # the flashlight (px from the attacker)
TORCH_SCALE, BEAM_AIM = 1.25, (0, 22)                         # ...shining in their eyes
TILE = 75                                                     # emitter header byte: texture tile counts (bits 0-3)
TEXEL = .74                                                   # screen px per texel of a 64px texture at scale 1.0
STUN_AT = {"player": (25, 9), "enemy": (-24, 17)}            # the stun gun, in their hand
STUN_TIP = {"player": (39, 10), "enemy": (-38, 16)}          #   its prongs
STUN_FRAMES = 10
BOX_AT = {"player": (-26, 48), "enemy": (26, 38)}            # the boombox, up on their shoulder
LID_AT = {"player": (52, 62), "enemy": (-28, 16)}            # the trash-can lid: mid-screen / in front of them
NOTE_FRAMES = 14
BEAT_AIM = (0, 24)
# ---- set 6 emitters (per kit)
BELT_E, BELT_P = 0, 1                                         # BELT: the belt swung by the player / the enemy
SNAPS, WELT1 = 0, 1                                           # WELT: whip-crack snaps, the welt left on them
SKULLS, SHIV_E, SHIV_P = 0, 1, 2                              # SHIV: poison skulls rising, the shiv each way
WIGGLE_R, WIGGLE_L = 0, 3                                     # TWERK: motion lines on the right / left
COIN_E, COIN_P, MONEYBAG = 0, 3, 1                            # COINS: coins flowing back each way, the bag
STR_E, STR_P, CAN1 = 0, 3, 1                                  # CAN: string sprayed each way, the can
TANGLED, TANGLE_HOLD = 0, 1                                   # TANGLE: the string landing, staying on them
DRIBBLE = 2                                                   # SPIT: drips running off them
CAN_AT = {"player": (30, 20), "enemy": (-30, 20)}            # the silly-string can, in their hand
NOZZLE_UP = 20                                                #   its nozzle, above the can's centre
STRING_AIM, STRING_FRAMES = (0, 22), 12
BAG_SPOT = {"player": (22, 24), "enemy": (-22, 24)}          # the money bag, next to them
COIN_FRAMES = 16
# ---- set 7 emitters (per kit)
ZOOMS, SHOES = 0, 1                                           # KICKS: speed lines, the sneaker
FUSE, BOX7, GLITTER = 0, 1, 3                                 # CRATE: fuse sparks, the crate, firework glitter
CART_GO, CART_FLIP = 1, 2                                     # CART / CARTL: rolling at them, flipped over
MOTES, CANS, CANS_THUMP = 0, 1, 2                             # PHONES: focus pulled in, the headphones, thumping
CART_RUN, CART_FRAMES = (100, 48), 12                         # the cart's run (px), and the battler's frames
CART_LIFE = 2 * CART_FRAMES                                   # MoveBattlerBy steps every other frame
# ---- set 8 emitters (per kit)
RIPPLES, FLOATIE = 0, 1                                       # POOLF: water ripples, the pool float
TAPE_A, TAPE_B = 1, 2                                         # TAPE: the two strips of the X
SPUTTERS, GUNUP = 0, 1                                        # JAMGUN: the dud's sputter, the gun held up
RINGS8, CIGAR_R, CIGAR_L = 0, 1, 2                            # CIGAR: smoke rings, the cigar pointing right / left
ZZZ = 0                                                       # SNOOZE: Zzz rising
PLUSES = 0                                                    # HEALS: + crosses rising
# ---- set 9 emitters (per kit)
HOPS, TUMBLE_GO = 0, 1                                        # TUMBLE: bounce marks, the tumbleweed rolling by
STARS9, MILL_HERE, MILL_THERE = 0, 1, 2                       # ARMS: impact stars, the windmill (short / long)
BILLS_E, GUN_R, GUN_L, BILLS_P = 0, 1, 2, 3                   # MGUN: bills shot up each way, the money gun each way
RAIN_A, RAIN_B = 0, 1                                         # BILLRAIN: bills raining down (light / dark)
GUSH, HYD, CAP_OFF = 0, 1, 2                                  # GEYSER: water shooting up, the hydrant, its cap flying
RAINBACK, COLUMN = 0, 1                                       # SPLOSH: water raining back down, the gushing column
BOOP, FINGER_R, FINGER_L = 0, 1, 2                            # FINGER: poke burst, the finger pointing right / left
ROLL9, STRIP_A, STRIP_B = 1, 2, 3                             # TAPEROLL: the roll circling, two angles of tape strip
SPARKS9, SLUGS = 0, 1                                         # RICO: ricochet sparks, spent slugs dropping
COIN_IN, JAR1 = 0, 1                                          # JAR: a coin dropping in, the swear jar
TUMBLE_SPEED = 5                                              # px a frame: the tumbleweed crossing the whole screen
TUMBLE_Y = 70                                                 # its screen height: the clear lane between the HP boxes
MILL_SPIN = 0x1C00                                            # the windmill's spin per frame
# ---- set 10 emitters (per kit)
SPIT_E, MIC_R, MIC_L, SPIT_P = 0, 1, 2, 3                     # MIC: spit flying each way, the mic each way
NOTES10 = 1                                                   # ROAST: music notes off the speaker (0: the flames)
SOAK_E, SOAKER_R, SOAKER_L, SOAK_P = 0, 1, 2, 3               # SOAKER: the water each way, the blaster each way
RINGS_E, HORN_R, HORN_L, RINGS_P = 0, 1, 2, 3                 # AIRHORN: blast rings each way, the horn each way
MUDDRIP = 2                                                   # PIE: mud running off them (THROWN: the pie)
PHONE = 1                                                     # MUDSPLAT: the phone filming it (POP: the splat)
FIZZ = 2                                                      # NINEVOLT: acid bubbling off them (THROWN: the 9V)
HELD9V = 1                                                    # ACIDSPLAT: the 9V at their tongue (POP: the splat)
HOSE_E, NOZ_SPIN, WILD, HOSE_P = 0, 1, 2, 3                   # FIREHOSE: the blast each way, the nozzle whipping
#                                                               round, water going everywhere
RINGING, CLOCK_A, CLOCK_B = 0, 1, 2                           # ALARMCLK: ring marks, the clock rattling left / right
FLY_E, FLY_P = 0, 1                                           # CHANCLA: thrown in at the opp / at you
FLIES, SPOON_R, SPOON_L = 0, 1, 2                             # SPOON: flies, the shank each way
SALT, SHAKE_UP, SHAKE_A, SHAKE_B = 0, 1, 2, 3                 # SHAKER: salt, the shaker coming in, shaking (2 poses)
NAILS1, GLITTER = 0, 1                                        # NAILS: the acrylics scattered, glitter
STINK, DUMP, COON = 0, 1, 2                                   # DUMPSTER: stink lines, the dumpster, the raccoon
SLOPDRIP = 2                                                  # SLOPBALL: slop running off them (THROWN: the slop)
PING = 2                                                      # PEBBLE: the ping (THROWN: the pebble)
CRACKLES, OUTLET1 = 0, 1                                      # OUTLET: crackles, the outlet full of cords
RING_BIG, RING_SMALL = 0, 1                                   # ZAPRING: the shock ring blasting out, little ones
RAIN, CLOUD = 0, 1                                            # RAINCLOUD: rain, the little cloud
GASP, COLLAR_L, COLLAR_R = 0, 1, 2                            # HEADLOCK: gasps, the collar (leash off to the left /
#                                                               to the right: back towards the attacker)
DEBRIS, TWIST_A, TWIST_B, AUNTIE = 0, 1, 2, 3                 # FUNNEL: flying trash, the tornado (two flips), auntie
ARCS, MICRO1 = 0, 1                                           # MICRO: sparks in the microwave, the microwave
RECEIPTS_E, GLASS, FOLDER, RECEIPTS_P = 0, 1, 2, 3            # AUDIT: receipts flying back each way, the
#                                                               magnifying glass, the AUDIT folder
BUCKPUFF, BUCKET1, STICKS_UP, STICKS_DN = 0, 1, 2, 3          # BUCKET: the hit puffs, the bucket, the sticks
FUMES = 2                                                     # SHOE: funk rising off them (THROWN: the sneaker)
CLOUD10, STENCH = 0, 1                                        # STINKCLOUD: the cloud, stench lines
STREAKS, BIKE_R, BIKE_L, BIKE_FLY = 0, 1, 2, 3                # DIRTBIKE: speed lines, the bike each way, flying off
FLICK, DURAG_R, DURAG_L = 0, 1, 2                             # DURAG: drops flicked off, the durag each way
ZEES, PLATE, PLATE_GONE = 0, 1, 2                             # SOULFOOD: z's, the plate, the plate being demolished
HELI, SPOT = 1, 2                                             # CHOPPER: the helicopter, its spotlight
CUTS, BILLS_E, BILLS_P = 0, 2, 3                              # BILLS10: paper cuts, bills flung each way
MIST_E, CAN_R, CAN_L, MIST_P = 0, 1, 2, 3                     # PEPPER: the spray each way, the can each way
MILKPOUR, JUG_UP, JUG_TIP, TEARS3 = 0, 1, 2, 3                # MILK: the milk, the jug (coming in / tipped), tears
MOUTH_AT = {"player": (8, 40), "enemy": (-10, 30)}            # the attacker's mouth (px from its centre)
SOAKER_AT = {"player": (26, 18), "enemy": (-26, 18)}          # the Super Soaker in their hands...
SOAKER_TIP = {"player": (50, 20), "enemy": (-50, 20)}         # ...its nozzle
HORN_AT = {"player": (26, 30), "enemy": (-26, 26)}            # the air horn up at their shoulder...
HORN_TIP = {"player": (48, 30), "enemy": (-48, 26)}           # ...its trumpet
NOZ_AT = {"player": (26, 18), "enemy": (-26, 18)}             # the fire hose nozzle in their hands...
NOZ_TIP = {"player": (50, 20), "enemy": (-50, 20)}            # ...and its tip
CHANCLA_SPEED, CHANCLA_FRAMES = 9, 14                         # Mama's throw: px a frame, frames to land
PEPPER_AT = {"player": (24, 22), "enemy": (-24, 20)}          # the pepper spray in their hand...
PEPPER_TIP = {"player": (40, 22), "enemy": (-40, 20)}         # ...its nozzle
# ---- set 11 emitters (per kit)
FLOPDROPS, BOARD_R, BOARD_L = 0, 1, 2                         # BOARD: splash drops, the diving board each way
GLOB, WINGS_UP, WINGS_DN = 0, 1, 2                            # PIGEON: the dropping, the pigeon (wings up / down)
GLARE, CHAIR10, REFLECTOR = 0, 1, 2                           # TANNING: glare twinkles, the beach chair, the reflector
WAVES10 = 1                                                   # HEAT: heat waves
TWINKLE, SMILE, RAY_A, RAY_B = 0, 1, 2, 3                     # GRILL: the twinkle, the gold smile, shine (two angles)
BASS_E, CAR10, BASS_P = 0, 1, 3                               # TRUNK: bass rings each way, the car
SPUTTER, HOOP_R, HOOP_L = 0, 1, 2                             # HOOPTIE: sputter puffs, the hooptie (pipe right / left)
SOOTCLOUD, BANG10 = 0, 1                                      # SOOT: the black cloud, the backfire flash
PINGS10, SHIELD1, TOM_E, TOM_P = 0, 1, 2, 3                   # SHIELD: pings, the riot shield, tomatoes each way
WIFI_E, WIFI_P = 0, 1                                         # WIFI: wifi waves each way
STARS10, PCLOCK, MOON, MOON_UP = 0, 1, 2, 3                   # CLOCKIN: stars, the punch clock, the moon rising / up
PUDDLE10, MOP_A, MOP_B, WETSIGN = 0, 1, 2, 3                  # JANITOR: the puddle, the mop (2 poses), WET FLOOR sign
SWOOSH, FAN_A, FAN_B = 0, 1, 2                                # CFAN: swooshes, the fan (two spin poses)
SLICES, BLADES_E, BLADES_P = 0, 2, 3                          # FANBLADES: cuts, the blades flying each way
FLICKS, LIGHTER1 = 0, 1                                       # BIC: sparks, the lighter
STRIP_1, STRIP_2, STRIP_3 = 1, 2, 3                           # RECEIPT: the receipt wrapping round them (3 angles)
DRAIN_E, DRAIN_P = 0, 1                                       # COINS2: their money draining back each way
MUDBUBS, TUB, SPAFACE = 0, 1, 2                               # SPA: mud bubbles, the tub, the turban + cucumbers
TOMATO_SPEED, TOMATO_FRAMES = 6, 14                           # tomatoes thrown at the riot shield
PHONE_UP = {"player": (10, 66), "enemy": (-10, 56)}           # the phone held up high, hunting for signal
CFAN_AT = {"player": (62, 78), "enemy": (-30, 66)}            # the ceiling fan, up over them
# ---- set 12 emitters (per kit)
SPARKS11, SPIN1 = 0, 1                                        # FIDGET: grinding sparks, the spinner spinning
ZEES11, BOOK_SHUT, BOOK_OPEN = 0, 1, 2                        # BOOK: z's, the book closed / open
MIST_E11, BOTTLE_R11, BOTTLE_L11, MIST_P11 = 0, 1, 2, 3       # COLOGNE: spritz each way, the bottle each way
DUST11, BIKE_R, BIKE_L = 0, 1, 2                              # BMX: dust, the bike riding right / left
NEON_AT = {"player": (-12, 70), "enemy": (36, 46)}             # the neon sign, up behind them
COLOGNE_TIP = {"player": (30, 40), "enemy": (-30, 32)}        # the atomizer, held up by their face
HYD_TOP = 16                                                  # the hydrant's open main, px above its centre
LAUNCH = {"player": 40, "enemy": 70}                          # px the blast throws the foe up (by attacker side:
#                                                               the opp sits high, more would throw it off the top)


def _angle(dx, dy):
    """Particle rotation (0x10000 a turn, counter-clockwise on screen) for art pointing right to point at (dx, dy)."""
    return round(math.degrees(math.atan2(dy, dx)) / 360 * 0x10000) & 0xFFFF


def torch_geometry(side):
    """(rotation, lens, beam centre, beam scale): the flashlight aimed at their eyes, the beam from lens to face."""
    cx, cy = TORCH_AT[side]
    dx, dy = aim_path(side, TORCH_AT[side], BEAM_AIM)
    d = math.hypot(dx, dy)
    ux, uy = dx / d, dy / d
    nose = (.92 - .5) * 64 * TEXEL * TORCH_SCALE                 # texture centre -> lens, px
    lens = (cx + ux * nose, cy + uy * nose)
    length = d - nose
    centre = (round(lens[0] + ux * length / 2), round(lens[1] + uy * length / 2))
    return _angle(dx, dy), lens, centre, length / (64 * TEXEL)


JET_SCALE, JET_SPEED, JET_Y = 3, 4, 70                        # the jet at 4:1 (nearly screen-wide), px per frame (it and
#                                                               whoever it's carrying), its centre's screen y
JET_HALF = 100                                                # half its width on screen (+ a little): starts off-screen
BATTLER_AT = {"player": (64, 140), "enemy": (190, 90)}        # battler centres on screen
FALL_SPEED, FALL_FRAMES = 8, 8                                # the suitcase, px per frame, out of the jet's belly
LADDER_X = 9 * 3                                              # the rope ladder: 9 texels right of the jet's centre
CARRY_FRAMES = 56
WAVE_FROM = {"player": (-330, -12), "enemy": (336, 36)}    # the tidal wave's centre: off-screen, mid-height
WAVE_SPEED, WAVE_SCALE = 8, 5.0                              # a wall of water the height of the screen
LEAF_FRAMES, HEART_FRAMES, BREATH_FRAMES = 12, 12, 14
ROLL_FRAMES, EIGHT_FRAMES = 12, 16
FLY = 14                                                      # frames a flown set-3 piece takes to reach the target
BILLBOARD = 0x30                                              # flag bits 4-5: draw type (1 = stretched along its
#                                                               velocity - invisible on a piece riding its emitter)
JET_FRAMES, JET_G = 18, .012
HYDRANT_AT = {"player": (34, 6), "enemy": (-34, -4)}        # beside the attacker, towards the target
NOZZLE = {"player": (12, 1), "enemy": (-12, 1)}             # the open cap facing the target
JET_AIM = {"player": (74, 52), "enemy": (-68, -45)}         # nozzle -> target body, per attacker side
CAR_START, CAR_ROAD = -250, 2                                 # car spawn, pixels from the target (x, y up)
GUN_ON_CAR = (30, 23)                                         # the gun at the window, pixels from the car centre
CAR_LIFE = 90
PENDANT = 1                                                   # BLING: the chain + medallion (follows its emitter)
BILLS, STACK = 0, 1                                           # CASH: fluttering dollar bills, the bankroll
TO_ENEMY, TO_PLAYER = 0, 1                                    # ROCKET: an RPG round flying each way
# battler particle origins (sBattleAnimEmitterPositions, kind 0, perspective 0): player and enemy
ORIGIN = {"player": (-9616, -5464), "enemy": (11056, 4400)}
ROCKET_FRAMES = 18
THROWN = 1                                                    # BOTTLE/BRICK/EGG: the object, riding its emitter
THROW_PEAK = 30                                               # pixels the lob rises above the straight line
EMBERS, BLAZE = 0, 1                                          # FIRE: flames licking upward
HOME = 1                                                      # HOUSE: somebody's house
DRIP, SPLAT = 0, 1                                            # YOLK: egg splat + yolk dripping down
EMITTER_PIXEL = 172                                           # MoveEmitter's offset unit (BATTLE_ANIM_EMITTER_PIXEL)
THROW_FRAMES = 20
CAR_SPEED = 5                                                 # screen pixels per frame (at the enemy's depth)
TICK = 2                                                      # frames per script tick (scripts run at 30 Hz)
CAR_SCALE = 1.9                                               # 64px texture -> ~90px car on screen

# where the gun's muzzle sits relative to the battler's particle origin, in screen pixels (y up). Back
# sprites hold the gun on the right pointing right, front sprites mirror it (measured on Cyndaquil/Hoothoot).
MUZZLE = {"player": (31, 9), "enemy": (-30, 17)}
# particle units per screen pixel (x, y) at each battler's depth - measured in-game: the camera is a
# perspective one, so the far (enemy) side needs more units per pixel than the near (player) side
SCALE = {"near": (171, 167), "far": (169, 170)}             # (the particle camera is effectively flat)
VEL_UNITS = 355                                               # particle velocity units per screen pixel (measured)
PS_SCALE = {}

# the standard prelude every move script starts with (battler sprite copies, as in Spike Cannon)
PRELUDE = [56, 57, 0, 57, 1, 57, 2, 57, 3, 58, 4, 0, 0, 0, 58, 5, 0, 1, 1, 58, 6, 0, 2, 2, 58, 7, 0, 3, 3,
           45, 78, 1, 0]
PRELUDE_END = [1, 59, 60, 0, 60, 1, 60, 2, 60, 3]


def rgb(r, g, b):
    return (b >> 3) << 10 | (g >> 3) << 5 | r >> 3


BRASS, RED, SMOKE_GRAY, DIRT_BROWN = rgb(230, 180, 60), rgb(255, 0, 0), rgb(165, 165, 165), rgb(160, 110, 50)


# ------------------------------------------------------------------ textures

def _a5i3(w, h, alpha):
    """alpha(x, y) in 0..1 -> A5I3 texels using palette index 0 (white)."""
    return bytes((round(max(0.0, min(1.0, alpha(x, y))) * 31) << 3) for y in range(h) for x in range(w))


def _star_quarter(n, rays, width, core):
    """Quarter of a flash centred on the bottom-right corner (the hardware mirrors it into the full star).
    rays: (angle, length 0..1); width: half-width of a spike at its base, in radians."""
    c = n - 0.5

    def a(x, y):
        dx, dy = c - x, c - y
        r = math.hypot(dx, dy) / n
        ang = math.atan2(dy, dx)                               # 0..pi/2 inside the quarter
        v = 1.0 if r < core * .45 else max(0.0, 1 - (r - core * .45) / (core * .55)) ** .6   # solid hot core
        for t, L in rays:
            d = abs(ang - t)
            if r < L:                                          # spike tapers to a point at length L
                half = width * (1 - r / L)
                if d < half:
                    v = max(v, (1 - d / half) ** .35 * (1 - (r / L) ** 3))
        return v
    return a


def tex_spark(n=16):
    rays = [(0.0, 1.0), (math.pi / 2, 1.0), (math.pi / 4, .75)]
    return _a5i3(n, n, _star_quarter(n, rays, .42, .45))


def tex_flash(n=32):
    # long fat horizontal flame, shorter vertical + diagonal tongues, big hot core
    rays = [(0.0, 1.0), (math.pi / 2, .62), (math.pi / 4, .7), (math.pi / 7, .5), (5 * math.pi / 14, .45)]
    return _a5i3(n, n, _star_quarter(n, rays, .4, .5))


def tex_tracer(n=32):
    """A3I5 32x32: a hot streak along the attacker->target diagonal (symmetric, so it reads either way)."""
    d = (128, -64)                                             # screen direction player -> enemy
    L = math.hypot(*d)
    ux, uy = d[0] / L, d[1] / L
    out = bytearray()
    for y in range(n):
        for x in range(n):
            px, py = x - n / 2 + .5, y - n / 2 + .5
            along = px * ux + py * uy
            across = abs(-px * uy + py * ux)
            taper = max(0.0, 1 - abs(along) / 15)
            if across <= 1.1 * taper + .3 and taper > 0:
                idx, a = (1, 7) if across < .8 and taper > .3 else (2, 6)
            elif across <= 2.2 * taper + .3 and taper > 0:
                idx, a = 3, 4
            else:
                idx, a = 0, 0
            out.append(a << 5 | idx)
    return bytes(out)


TRACER_PAL = [0x0000, 0x7FFF, 0x5FFF, 0x03FF]                 # -, white, pale yellow, yellow (BGR555)


def tex_casing(n=16):
    """Quarter of a brass casing lying sideways (mirrored into a 2:1 capsule with a rim groove)."""
    c = n - 0.5

    def a(x, y):
        dx, dy = (c - x) / n, (c - y) / n
        if dx > .5 or dy > .24:
            return 0.0
        if dx > .38:                                           # rounded end
            return 1.0 if (dx - .38) ** 2 + (dy * 1.4) ** 2 < .12 ** 2 * 2.2 else 0.0
        return .65 if abs(dx - .3) < .04 else 1.0             # rim groove
    return _a5i3(n, n, a)


def tex_crosshair(n=32):
    """Quarter of a sniper reticle: ring, crosshair lines with a gap, centre dot, tick marks."""
    c = n - 0.5

    def a(x, y):
        dx, dy = c - x, c - y
        r = math.hypot(dx, dy)
        v = 0.0
        if abs(r - n * .72) < 1.1:
            v = 1.0                                            # ring
        if (dx < 1.0 or dy < 1.0) and n * .2 < r < n * .98:
            v = 1.0                                            # lines (gap at the centre)
        if r < 1.6:
            v = 1.0                                            # dot
        if abs(r - n * .45) < .7 and (dx < 3 or dy < 3):
            v = 1.0                                            # inner ticks
        return v
    return _a5i3(n, n, a)


SIGN_SCALE, SIGN_POP = fxart.SIGN_SCALE, fxart.SIGN_POP
ONE_TO_ONE = SIGN_SCALE / 2                 # props with text in the art: one texel per screen px (divide by a held pop)


FLOWN = {(PIE, THROWN), (NINEVOLT, THROWN), (SLOPBALL, THROWN), (PEBBLE, THROWN), (SHOE, THROWN)}   # set 10: flown by MoveEmitter (no self_dest)


def build_files(files):
    """{kit slot: rebuilt particle file} from the NARC member list (each keeps its donor's size)."""
    out = {}
    b = bytearray(files[DONOR[GUN]])
    spa.set_texture(b, 0, tex_spark())
    spa.set_texture(b, 1, tex_flash())
    spa.set_texture(b, 2, tex_tracer(), TRACER_PAL)
    out[GUN] = bytes(b)

    b = bytearray(files[DONOR[KIT]])
    rs = spa.resources(bytes(b))
    spa.set_texture(b, 0, tex_casing())
    spa.set_texture(b, 1, tex_crosshair())
    spa.edit(b, rs[CASING], clr=BRASS, clr_anm=(rgb(255, 230, 120), rgb(170, 120, 30)), gen=2, scl=.32,
             life=26, scl_anm=(1.0, 1.0, 1.0, 0, 255))
    spa.edit(b, rs[CROSS], clr=RED, clr_anm=(RED, rgb(255, 60, 60)), life=40, scl=1.25,
             scl_anm=(2.6, 1.0, 1.0, 110, 255))
    out[KIT] = bytes(b)

    b = bytearray(files[DONOR[SMOKE]])
    rs = spa.resources(bytes(b))
    # gun smoke: slow puffs that drift straight up, spread out, grow and fade (no trail)
    spa.edit(b, rs[PUFF], clr=SMOKE_GRAY, clr_anm=(rgb(225, 225, 225), rgb(120, 120, 128)), scl=.55,
             life=80, emtr_life=14, gen=1, gen_intvl=3, axis=(0, 1, 0), vel=(.006, .008), gravity=(0, .00006, 0),
             scl_anm=(.6, 1.6, 2.8, 50, 150), rndm=(90, 60, 160), air_resist=180, child_gen=0,
             child_clr=rgb(150, 150, 155))
    spa.edit(b, rs[DIRT], clr=DIRT_BROWN, clr_anm=(rgb(170, 120, 60), rgb(100, 70, 40)), scl=.45, emtr_life=3,
             child_clr=rgb(120, 85, 45))
    out[SMOKE] = bytes(b)

    b = bytearray(files[DONOR[CAR]])
    rs = spa.resources(bytes(b))
    texels, pal = fxart.to_a3i5(fxart.lowrider(), 32)
    spa.set_texture(b, 1, texels, pal)
    white = rgb(255, 255, 255)
    spa.edit(b, rs[RIDE], clr=white, clr_anm=(white, white), alpha=(31, 31, 31), scl=CAR_SCALE, flags_off=1 << 13,
             scl_anm=(1.0, 1.0, 1.0, 0, 255), gen=1, emtr_life=1, life=CAR_LIFE, axis=(1, 0, 0),
             vel=(0, CAR_SPEED * VEL_UNITS / 4096), air_resist=128)
    for res, life in ((PARKED, 80), (BOUNCE, 4)):              # the same lowrider, parked
        spa.edit(b, rs[res], clr=white, clr_anm=(white, white), alpha=(31, 31, 31), scl=CAR_SCALE, gen=1,
                 emtr_life=1, life=life, vel=(0, 0), init_pos=0, scl_anm=(1.0, 1.0, 1.0, 0, 255),
                 flags_on=1 << 14, flags_off=(1 << 13) | (1 << 15))
    # window flashes: born with the car, same speed, hidden until the gun reaches the target, then strobing
    spa.set_texture(b, 0, tex_spark())
    life = int((-CAR_START - GUN_ON_CAR[0] + 60) / CAR_SPEED)  # gone once the gun is 60px past them
    gold = rgb(255, 230, 90)
    spa.edit(b, rs[WINDOW], clr=gold, clr_anm=(rgb(255, 255, 220), gold), scl=.9, gen=1, emtr_life=1, life=life,
             axis=(1, 0, 0), vel=(0, CAR_SPEED * VEL_UNITS / 4096), air_resist=128, init_pos=0,
             gravity=(0, 0, 0), scl_anm=(1.0, 1.0, 1.0, 0, 255), alpha=(31, 31, 31), flick=140,
             flags_off=1 << 13)                                 # strobing the whole way in
    out[CAR] = bytes(b)

    b = bytearray(files[DONOR[BLING]])
    rs = spa.resources(bytes(b))
    texels, pal = fxart.to_a3i5(fxart.chain(), 30)
    spa.set_texture(b, 0, texels, pal)
    spa.edit(b, rs[PENDANT], clr=white, scl=1.5, gen=1, emtr_life=1, life=SWING_STEP, vel=(0, 0), init_pos=0,
             scl_anm=(1.0, 1.0, 1.0, 0, 255), alpha=(31, 31, 31), flags_off=1 << 13)
    struct.pack_into("<h", b, rs[PENDANT]["cngc"] + 12, 0)    # no pull towards a point
    out[BLING] = bytes(b)

    b = bytearray(files[DONOR[CASH]])
    rs = spa.resources(bytes(b))
    texels, pal = fxart.to_a3i5(fxart.bill(), 4)
    spa.set_texture(b, 0, texels, pal)
    texels, pal = fxart.to_a3i5(fxart.cash_stack(), 10)
    spa.set_texture(b, 1, texels, pal)
    spa.edit(b, rs[BILLS], clr=white, clr_anm=(white, white), scl=.42, gen=1, emtr_life=26, life=70,
             vel=(.025, -.02), gravity=(0, -.0032, 0), air_resist=124, alpha=(31, 31, 31), radius=2.8,
             scl_anm=(1.0, 1.0, 1.0, 0, 255), rndm=(60, 80, 120))
    spa.edit(b, rs[STACK], clr=white, clr_anm=(white, white), scl=1.3, gen=1, emtr_life=1, life=34,
             vel=(0, 0), init_pos=0, alpha=(31, 31, 20), scl_anm=(.6, 1.0, 1.0, 40, 255),
             flags_off=(1 << 12) | (1 << 13))                   # no rotation: held up straight
    struct.pack_into("<H", b, rs[STACK]["spin"], 0)            # held up, not spinning
    out[CASH] = bytes(b)

    b = bytearray(files[DONOR[ROCKET]])
    rs = spa.resources(bytes(b))
    texels, pal = fxart.to_a3i5(fxart.rocket(), 24)
    spa.set_texture(b, 1, texels, pal)
    (px, py), (ex, ey) = ORIGIN["player"], ORIGIN["enemy"]
    dist = math.hypot(ex - px, ey - py)
    ax, ay = (ex - px) / dist, (ey - py) / dist
    speed = dist / ROCKET_FRAMES / 4096
    for res, sign, rtt in ((TO_ENEMY, 1, 0), (TO_PLAYER, -1, 0x8000)):
        spa.edit(b, rs[res], gen=1, emtr_life=1, life=ROCKET_FRAMES, scl=1.1, init_pos=0, vel=(0, speed),
                 axis=(sign * ax, sign * ay, 0), air_resist=128, alpha=(31, 31, 31),
                 scl_anm=(1.0, 1.0, 1.0, 0, 255), flags_off=(1 << 15) | (1 << 13) | (1 << 12),
                 flags_on=1 << 14)                              # self-destruct, or the script waits forever
        struct.pack_into("<H", b, rs[res]["off"] + 56, rtt)     # fixed rotation: nose towards the target
        if "grvt" in rs[res]:
            spa.edit(b, rs[res], gravity=(0, 0, 0))
    out[ROCKET] = bytes(b)

    # thrown objects: one copy of the rocket file each, the object riding (and spinning on) its emitter
    for ps, art, spin, size in ((BOTTLE, fxart.molotov(), 0x0A00, .9), (BRICK, fxart.brick(), 0x0C00, .9),
                                (EGG, fxart.egg(), 0x0500, .55)):
        b = bytearray(files[DONOR[ps]])
        rs = spa.resources(bytes(b))
        texels, pal = fxart.to_a3i5(art, 24)
        spa.set_texture(b, 1, texels, pal)
        # the arc: MoveEmitter flies the emitter straight at the target while the object (following it) is
        # thrown upward under gravity, landing back on the line as the flight ends (MoveEmitterArc crashes)
        h = THROW_PEAK * VEL_UNITS / 4096                       # particle-local motion: velocity units
        g = 8 * h / THROW_FRAMES ** 2
        # NOT self-destructing: MoveEmitter owns the emitter and deletes it when the flight ends - if SPL freed it
        # first the task would write to freed memory (that froze the game)
        spa.edit(b, rs[THROWN], gen=1, emtr_life=1, life=THROW_FRAMES + 2, scl=size, init_pos=0, axis=(0, 1, 0),
                 clr=white,                                      # untinted: the art's own colours
                 vel=(0, g * THROW_FRAMES / 2), gravity=(0, -g, 0), air_resist=128, alpha=(31, 31, 31),
                 scl_anm=(1.0, 1.0, 1.0, 0, 255), tex=1,
                 flags_on=(1 << 15) | (1 << 12), flags_off=(1 << 13) | (1 << 14))
        struct.pack_into("<hhH", b, rs[THROWN]["off"] + 52, spin, spin, 0)   # tumbling
        out[ps] = bytes(b)
    # fire: short tongues of flame rising straight up (the donor's blast goes sideways), embers floating up
    b = bytearray(files[DONOR[FIRE]])
    rs = spa.resources(bytes(b))
    spa.edit(b, rs[BLAZE], axis=(0, 1, 0), vel=(.004, .018), gravity=(0, .0009, 0), life=18, emtr_life=8, gen=1,
             gen_intvl=2, scl=.55, scl_anm=(.6, 1.15, .25, 60, 150), child_gen=0, rndm=(70, 60, 120),
             air_resist=124, flags_off=1 << 13)
    spa.edit(b, rs[EMBERS], axis=(0, 1, 0), vel=(.012, .026), gravity=(0, .0005, 0), life=16, emtr_life=8,
             scl=.3, rndm=(60, 60, 160), air_resist=124)
    out[FIRE] = bytes(b)

    # the house that gets egged: pops up and stays for the whole bit
    b = bytearray(files[DONOR[HOUSE]])
    rs = spa.resources(bytes(b))
    texels, pal = fxart.to_a3i5(fxart.house(), 30)
    spa.set_texture(b, 0, texels, pal)
    spa.edit(b, rs[HOME], clr=white, scl=1.0, gen=1, emtr_life=1, life=170, vel=(0, 0), init_pos=0,
             scl_anm=(.3, 1.08, 1.0, 25, 255), alpha=(31, 31, 31), flags_off=(1 << 13) | (1 << 15))
    struct.pack_into("<h", b, rs[HOME]["cngc"] + 12, 0)
    out[HOUSE] = bytes(b)

    # yolk: a yellow splat that sags, drops running down
    b = bytearray(files[DONOR[YOLK]])
    rs = spa.resources(bytes(b))
    yellow, pale = rgb(255, 214, 40), rgb(255, 246, 190)
    spa.edit(b, rs[SPLAT], clr=yellow, clr_anm=(pale, yellow), scl=.45, life=40, emtr_life=2, gen=1,
             axis=(0, 1, 0), vel=(.004, 0), gravity=(0, -.00025, 0), scl_anm=(.4, 1.2, 1.0, 30, 200),
             child_gen=0, child_clr=yellow, air_resist=110)
    spa.edit(b, rs[DRIP], clr=yellow, clr_anm=(pale, yellow), scl=.22, life=36, emtr_life=6, gen=1,
             vel=(.004, -.004), gravity=(0, -.0007, 0), child_clr=yellow, air_resist=120)
    out[YOLK] = bytes(b)

    def mirrored(b, art, colors=32, flip=True):
        """Append art flipped left-right as a new texture: the enemy's copy of a held prop. (Turning the particle
        round 180 instead points it the right way but hangs it upside down.) Returns (b, texture index)."""
        from PIL import Image as _Image
        texels, pal = fxart.to_a3i5(art.transpose(_Image.FLIP_LEFT_RIGHT) if flip else art, colors)
        data, idx = spa.add_texture(bytes(b), 1, art.width, art.height, texels, pal)
        return bytearray(data), idx

    def single(ps, art, colors, res, **edit):
        """A copy of the donor with `art` as its colour texture and emitter `res` edited as a single prop."""
        bb = bytearray(files[DONOR[ps]])
        rr = spa.resources(bytes(bb))
        tex = rr[res]["tex"]
        colors = min(colors, spa.textures(bytes(bb))[tex][6] // 2)  # the slot's palette size (more = garbage)
        texels, pal = fxart.to_a3i5(art, colors)
        spa.set_texture(bb, tex, texels, pal)
        base = dict(gen=1, emtr_life=1, vel=(0, 0), init_pos=0, clr=white, air_resist=128, alpha=(31, 31, 31),
                    scl_anm=(1.0, 1.0, 1.0, 0, 255), flags_on=1 << 14, flags_off=(1 << 12) | (1 << 13) | (1 << 15))
        if "clr" in rr[res]:
            base["clr_anm"] = (white, white)                    # the art's own colours, no tint cycling
        base.update(edit)
        spa.edit(bb, rr[res], **base)
        if not base["flags_on"] & (1 << 12):                    # no rotation unless asked (the donor spins)
            struct.pack_into("<hhH", bb, rr[res]["off"] + 52, 0, 0, 0)
        if "cngc" in rr[res]:
            struct.pack_into("<h", bb, rr[res]["cngc"] + 12, 0)
        if "spin" in rr[res]:
            struct.pack_into("<H", bb, rr[res]["spin"], 0)
        return bb, rr

    # Hose Down: a big hydrant, and water shot out of its nozzle on a ballistic arc (velocity + gravity)
    b, rs = single(HYDRANT, fxart.hydrant(), 24, STAND, scl=1.25, life=75)
    out[HYDRANT] = bytes(b)
    b = bytearray(files[DONOR[JET]])
    rs = spa.resources(bytes(b))
    blue, foam = rgb(70, 140, 255), rgb(230, 245, 255)
    for res, (dx, dy) in ((JET_E, JET_AIM["player"]), (JET_P, JET_AIM["enemy"])):
        vx = dx * VEL_UNITS / 4096 / JET_FRAMES
        vy = dy * VEL_UNITS / 4096 / JET_FRAMES + JET_G * JET_FRAMES / 2
        sp = math.hypot(vx, vy)
        spa.edit(b, rs[res], clr=blue, clr_anm=(foam, blue), scl=.3, life=JET_FRAMES + 2, emtr_life=24, gen=2,
                 gen_intvl=1, init_pos=0, axis=(vx / sp, vy / sp, 0), vel=(.006, sp), gravity=(0, -JET_G, 0),
                 air_resist=128, rndm=(60, 20, 40), child_gen=0, flags_off=1 << 13)
    out[JET] = bytes(b)
    b = bytearray(files[DONOR[SPLASH]])
    rs = spa.resources(bytes(b))
    spa.edit(b, rs[1], clr=foam, clr_anm=(foam, blue), scl=.5, life=24, emtr_life=8, gen=1, child_gen=0,
             vel=(.02, .01), gravity=(0, -.0008, 0))
    spa.edit(b, rs[0], clr=blue, clr_anm=(foam, blue), scl=.25, life=22, emtr_life=8, gen=2,
             vel=(.03, .02), gravity=(0, -.0016, 0))
    out[SPLASH] = bytes(b)

    # Bat Swing: the bat's handle is the texture's centre, so the particle's rotation swings it from the hands
    b, rs = single(SLUGGER, fxart.bat_swing(), 30, SWING_E, scl=1.6, life=10, flags_on=(1 << 14) | (1 << 12))
    spa.edit(b, rs[SWING_P], gen=1, emtr_life=1, vel=(0, 0), init_pos=0, clr=white, air_resist=128,
             alpha=(31, 31, 31), scl_anm=(1.0, 1.0, 1.0, 0, 255), scl=1.6, life=10,
             flags_on=(1 << 14) | (1 << 12), flags_off=(1 << 13) | (1 << 15))
    struct.pack_into("<h", b, rs[SWING_P]["cngc"] + 12, 0)
    struct.pack_into("<hhH", b, rs[SWING_E]["off"] + 52, -0x0E00, -0x0E00, 0x5000)   # raised behind -> down-forward
    struct.pack_into("<hhH", b, rs[SWING_P]["off"] + 52, 0x0E00, 0x0E00, 0x3000)     # mirrored for the enemy
    out[SLUGGER] = bytes(b)

    # Taser: the device (pointing right; the enemy's copy turned round) and crackling bolts round the target
    b, rs = single(TASER, fxart.taser(), 24, STAND, scl=1.2, life=60)
    b, flip = mirrored(b, fxart.taser(), 24)
    spa.edit(b, rs[TASER_P], gen=1, emtr_life=1, vel=(0, 0), init_pos=0, clr=white, air_resist=128,
             alpha=(31, 31, 31), scl_anm=(1.0, 1.0, 1.0, 0, 255), scl=1.2, life=60, gravity=(0, 0, 0),
             tex=flip, flags_on=1 << 14, flags_off=(1 << 13) | (1 << 15))
    struct.pack_into("<H", b, rs[TASER_P]["off"] + 56, 0)                     # upright
    out[TASER] = bytes(b)
    b, rs = single(BOLTS, fxart.bolt(), 24, ZAP, scl=1.1, life=3, emtr_life=26, gen=2, init_pos=1, radius=.9,
                   flags_on=(1 << 14) | (1 << 13))
    out[BOLTS] = bytes(b)

    # Panic button: a key fob, and sound-wave rings that blast out and fade
    b, rs = single(FOB, fxart.keyfob(), 24, STAND, scl=1.3, life=60)
    out[FOB] = bytes(b)
    b = bytearray(files[DONOR[RINGS]])
    rs = spa.resources(bytes(b))
    spa.set_texture(b, rs[RING]["tex"], fxart.ring_quarter())
    red = rgb(255, 50, 50)
    spa.edit(b, rs[RING], clr=red, clr_anm=(rgb(255, 255, 255), red), scl=1.0, life=18, emtr_life=1, gen=1,
             scl_anm=(.3, 1.6, 2.8, 120, 200), alpha=(31, 28, 0), vel=(0, 0), init_pos=0, flags_off=1 << 13)
    out[RINGS] = bytes(b)

    # Bass Drop: a subwoofer box (and its cone pumping on each hit), the ground cracking open
    b, rs = single(SUB, fxart.speaker(), 30, BOX, scl=1.25, life=110)
    spa.edit(b, rs[PUMP], gen=1, emtr_life=1, vel=(0, 0), init_pos=0, clr=white, air_resist=128,
             alpha=(31, 31, 31), scl_anm=(1.0, 1.22, 1.0, 60, 140), scl=1.25, life=6,
             flags_on=1 << 14, flags_off=(1 << 13) | (1 << 15))
    struct.pack_into("<h", b, rs[PUMP]["cngc"] + 12, 0)
    out[SUB] = bytes(b)
    b, rs = single(CRACK, fxart.ground_crack(), 12, SPLIT, scl=1.7, life=100, scl_anm=(.2, 1.0, 1.0, 70, 255))
    out[CRACK] = bytes(b)
    # ---- set 3 -------------------------------------------------------------------------------------------
    # Hot Shot: a big bag of HOT chips, ripped open; fistfuls of chips thrown in their face (static emitters on
    # the bag shooting tumbling chips at the target, one per direction)
    orange, yellow, red = rgb(255, 140, 30), rgb(255, 235, 120), rgb(220, 40, 20)

    def spray(b, rs, res, side, frm, aim, frames, **edit):
        """Emitter res shoots its particles from `frm` (px from the attacker) at `aim` (px from the target)."""
        dx, dy = aim_path(side, frm, aim)
        d = math.hypot(dx, dy)
        args = dict(axis=(dx / d, dy / d, 0), life=frames + 2, init_pos=1, air_resist=128,
                    flags_on=1 << 14, flags_off=(1 << 15) | BILLBOARD)
        if "chld" in rs[res]:
            args["child_gen"] = 0
        args.update(edit)
        if "grvt" not in rs[res]:
            args.pop("gravity", None)                        # (this emitter has no gravity block)
        args["vel"] = (args.pop("spread", 0), d * VEL_UNITS / 4096 / frames)
        spa.edit(b, rs[res], **args)
        if "grvt" in rs[res] and "gravity" not in edit:
            spa.edit(b, rs[res], gravity=(0, 0, 0))
        if "cngc" in rs[res]:
            struct.pack_into("<h", b, rs[res]["cngc"] + 12, 0)

    b, rs = single(CHIPS, fxart.chip_bag(), 32, BAG, scl=ONE_TO_ONE / 1.12, life=60, scl_anm=(.3, 1.12, 1.0, 30, 255))
    spa.set_texture(b, 0, fxart.chip())
    for res, sd in ((CHIP_E, "player"), (CHIP_P, "enemy")):
        spray(b, rs, res, sd, BAG_AT[sd], CHIP_AIM, CHIP_FRAMES, tex=0, clr=rgb(255, 100, 30),
              clr_anm=(rgb(255, 170, 60), rgb(230, 40, 20)), scl=.55, emtr_life=5, gen=2, gen_intvl=1, radius=.25,
              spread=.008, alpha=(31, 31, 31), scl_anm=(1.0, 1.0, 1.0, 0, 255), flick=0,
              flags_on=(1 << 14) | (1 << 12) | (1 << 13))
        struct.pack_into("<hhH", b, rs[res]["off"] + 52, -0x1400, 0x1400, 0)       # tumbling
    spa.edit(b, rs[3], flags_on=1 << 14)                     # the car's last emitter: unused
    out[CHIPS] = bytes(b)
    # the hit: tongues of flame shooting up (a new flame shape), embers popping out
    b = bytearray(files[DONOR[BURST]])
    rs = spa.resources(bytes(b))
    spa.set_texture(b, 1, fxart.flame_tongue())
    spa.set_texture(b, 0, fxart.speck())
    spa.edit(b, rs[TONGUE], clr=orange, clr_anm=(yellow, red), scl=.6, life=16, emtr_life=10, gen=1, gen_intvl=1,
             axis=(0, 1, 0), vel=(.008, .014), gravity=(0, .0006, 0), radius=.8, init_pos=1, air_resist=126,
             alpha=(31, 31, 0), scl_anm=(.4, 1.1, .6, 50, 160), rndm=(80, 40, 100), child_gen=0,
             flags_off=1 << 13)
    spa.edit(b, rs[EMBER], tex=0, clr=yellow, clr_anm=(rgb(255, 255, 200), orange), scl=.25, life=20,
             emtr_life=4, gen=3, axis=(0, 1, 0), vel=(.03, .02), gravity=(0, -.0015, 0), air_resist=122,
             alpha=(31, 31, 0), scl_anm=(1.0, 1.0, .5, 0, 160), child_gen=0, flags_off=BILLBOARD)
    out[BURST] = bytes(b)

    # Stare Down (Leer): "deal with it" shades sliding down slow (velocity with air resistance: they ease to a
    # stop), a glint off the lens, sweat drops flying off the target
    # (stop-motion: air resistance doesn't brake a particle to a stop, so the slide is a pose per step)
    b, rs = single(SHADES, fxart.deal_shades(), 30, SLIDE, scl=2.0, life=SWING_STEP)
    spa.edit(b, rs[LANDED], gen=1, emtr_life=1, life=54, vel=(0, 0), init_pos=0, clr=white, air_resist=128,
             alpha=(31, 31, 31), scl=2.0, scl_anm=(1.0, 1.0, 1.0, 0, 255), flags_on=1 << 14,
             flags_off=(1 << 12) | (1 << 13) | (1 << 15))
    struct.pack_into("<hhH", b, rs[LANDED]["off"] + 52, 0, 0, 0)
    for k in ("cngc", "spin"):
        if k in rs[LANDED]:
            struct.pack_into("<h" if k == "cngc" else "<H", b, rs[LANDED][k] + (12 if k == "cngc" else 0), 0)
    out[SHADES] = bytes(b)
    b, rs = single(GLINT, fxart.sweat_drop(), 24, SWEAT, scl=.5, life=24, emtr_life=3, gen=2, init_pos=1, radius=.5,
                   axis=(0, 1, 0), vel=(.02, .02), air_resist=124, flags_off=(1 << 12) | (1 << 15) | BILLBOARD)
    spa.edit(b, rs[SWEAT], gravity=(0, -.0018, 0), alpha=(31, 31, 0))
    spa.set_texture(b, rs[TING]["tex"], fxart.glint())
    spa.edit(b, rs[TING], clr=rgb(255, 255, 255), clr_anm=(rgb(255, 255, 255), rgb(255, 250, 200)), scl=.7, life=12,
             emtr_life=1, gen=1, vel=(0, 0), init_pos=0, air_resist=128, alpha=(31, 31, 0),
             scl_anm=(.2, 1.4, .3, 60, 160), child_gen=0, flags_on=(1 << 14) | (1 << 12),
             flags_off=(1 << 13) | (1 << 15) | BILLBOARD)
    struct.pack_into("<hhH", b, rs[TING]["off"] + 52, 0x0800, 0x0800, 0)            # a little twinkle spin
    out[GLINT] = bytes(b)

    # Talk Trash: cussing speech bubbles flown at the target, a red "!" popping over them
    b, rs = single(BUBBLE, fxart.speech_bubble(), 8, TALK, scl=.85, life=FLY + 2,
                   flags_on=1 << 15, flags_off=(1 << 12) | (1 << 13) | (1 << 14))
    spa.set_texture(b, rs[BANG]["tex"], fxart.bang())
    spa.edit(b, rs[BANG], clr=rgb(235, 30, 30), scl=.55, life=14, emtr_life=1, gen=1, vel=(0, 0), init_pos=0,
             air_resist=128, alpha=(31, 31, 0), scl_anm=(.3, 1.3, 1.0, 40, 255), child_gen=0,
             flags_on=1 << 14, flags_off=(1 << 12) | (1 << 13) | (1 << 15))
    struct.pack_into("<hhH", b, rs[BANG]["off"] + 52, 0, 0, 0)
    out[BUBBLE] = bytes(b)

    # Pocket Sand: "POCKET SAND!" bursts out over them, a cone of sand blasted into the target's face, a dust cloud
    b, rs = single(POCKET, fxart.pocket_sand_sign(), 32, SIGN, scl=ONE_TO_ONE / 1.2, life=44, scl_anm=(.2, 1.2, 1.0, 30, 255))
    tan, pale = rgb(225, 195, 130), rgb(250, 235, 195)
    spa.set_texture(b, 0, fxart.speck())
    for res, sd in ((GRAIN_E, "player"), (GRAIN_P, "enemy")):
        spray(b, rs, res, sd, HAND_AT[sd], SAND_AIM, SAND_FRAMES, tex=0, clr=rgb(205, 165, 95),
              clr_anm=(rgb(235, 205, 140), rgb(170, 125, 65)), scl=.55, emtr_life=6, gen=8, gen_intvl=1, radius=.2, spread=.022, alpha=(31, 31, 20),
              scl_anm=(.8, 1.0, 1.3, 0, 200), flick=0, gravity=(0, -.0006, 0))
    spa.edit(b, rs[3], flags_on=1 << 14)                     # the car's last emitter: unused
    out[POCKET] = bytes(b)
    b = bytearray(files[DONOR[SAND]])
    rs = spa.resources(bytes(b))
    spa.set_texture(b, 1, fxart.dust_cloud())
    spa.edit(b, rs[CLOUD], tex=1, clr=tan, clr_anm=(pale, tan), scl=.8, life=40, emtr_life=8, gen=1,
             gen_intvl=2, axis=(0, 1, 0), vel=(.012, .004), gravity=(0, .0002, 0), radius=.7, init_pos=1,
             air_resist=118, alpha=(31, 26, 0), scl_anm=(.5, 1.3, 1.8, 40, 150), rndm=(90, 60, 120),
             child_gen=0, flags_off=1 << 13)
    spa.edit(b, rs[0], flags_on=1 << 14)                     # unused
    out[SAND] = bytes(b)

    # Fan Blast: the box fan, its blades (a separate particle spinning on the grill), gust lines flown at them
    b, rs = single(FAN, fxart.box_fan(), 24, BODY, scl=1.15, life=96, scl_anm=(.3, 1.05, 1.0, 30, 255))
    spa.set_texture(b, rs[BLADES]["tex"], fxart.fan_blades())
    steel = rgb(175, 195, 220)
    spa.edit(b, rs[BLADES], clr=steel, clr_anm=(steel, steel), gravity=(0, 0, 0), scl=.78, flick=0, life=96, emtr_life=1, gen=1, vel=(0, 0), init_pos=0,
             air_resist=128, alpha=(31, 31, 31), scl_anm=(.3, 1.05, 1.0, 30, 255),
             flags_on=(1 << 14) | (1 << 12), flags_off=(1 << 13) | (1 << 15) | BILLBOARD)
    struct.pack_into("<hhH", b, rs[BLADES]["off"] + 52, 0x1C00, 0x1C00, 0)        # whirring
    for res in (1, 3):                                       # the car's other emitters: unused, kept harmless
        spa.edit(b, rs[res], flags_on=1 << 14)
    out[FAN] = bytes(b)
    # gusts: static emitters ON the fan, shooting wind lines at the target (MoveEmitter can only start a flight
    # at the attacker's centre, so flown lines came out of the attacker instead of the fan)
    b = bytearray(files[DONOR[WIND]])
    rs = spa.resources(bytes(b))
    paths = {sd: gust_path(sd) for sd in ("player", "enemy")}
    tilt = -sum(math.degrees(math.atan2(abs(dy), abs(dx))) for dx, dy in paths.values()) / 2
    spa.set_texture(b, 0, fxart.wind_streak(angle=tilt))   # one texture: the line is the same both ways
    for res, sd in ((GUST_E, "player"), (GUST_P, "enemy")):
        dx, dy = paths[sd]
        d = math.hypot(dx, dy)
        speed = d * VEL_UNITS / 4096 / GUST_FRAMES
        spa.edit(b, rs[res], tex=0, clr=rgb(235, 245, 255), clr_anm=(rgb(255, 255, 255), rgb(190, 215, 240)),
                 scl=.95, life=GUST_FRAMES + 1, emtr_life=7, gen=1, gen_intvl=2, axis=(dx / d, dy / d, 0),
                 vel=(0, speed), init_pos=1, radius=.45, air_resist=128, alpha=(31, 28, 0),
                 scl_anm=(1.0, 1.0, 1.0, 0, 255), rndm=(0, 0, 0), child_gen=0, gravity=(0, 0, 0),
                 flags_on=1 << 14, flags_off=(1 << 12) | (1 << 13) | (1 << 15) | BILLBOARD)
        struct.pack_into("<hhH", b, rs[res]["off"] + 52, 0, 0, 0)
        if "cngc" in rs[res]:
            struct.pack_into("<h", b, rs[res]["cngc"] + 12, 0)  # no pull towards a point
    out[WIND] = bytes(b)

    # ---- set 4 ---------------------------------------------------------------------------------------------
    NEEDS = {"clr_anm": "clr", "scl_anm": "scl", "alpha": "alp", "flick": "alp", "gravity": "grvt",
             "child_gen": "chld", "child_clr": "chld"}

    def prop(b, rs, res, **edit):
        """Emitter res as one particle (a prop): no tint, no drift, no spin unless asked; self-destructs."""
        r = rs[res]
        base = dict(gen=1, emtr_life=1, vel=(0, 0), init_pos=0, clr=white, air_resist=128, alpha=(31, 31, 31),
                    scl_anm=(1.0, 1.0, 1.0, 0, 255), clr_anm=(white, white), child_gen=0, gravity=(0, 0, 0),
                    flags_on=1 << 14, flags_off=(1 << 12) | (1 << 13) | (1 << 15) | BILLBOARD)
        base.update(edit)
        for k, block in NEEDS.items():
            if k in base and block not in r:
                del base[k]
        spa.edit(b, r, **base)
        if not base["flags_on"] & (1 << 12):
            struct.pack_into("<hhH", b, r["off"] + 52, 0, 0, 0)
        if "cngc" in r:
            struct.pack_into("<h", b, r["cngc"] + 12, 0)
        if "spin" in r:
            struct.pack_into("<H", b, r["spin"], 0)

    def rot(b, rs, res, spin=0, init=0):
        """Rotation: spin per frame (needs flag bit 12) and the starting angle (0x10000 = a full turn)."""
        struct.pack_into("<hhH", b, rs[res]["off"] + 52, spin, spin, init & 0xFFFF)

    def mover(b, rs, res, vx, vy, **edit):
        """A prop gliding at (vx, vy) screen px per frame (y up)."""
        v = math.hypot(vx, vy)
        prop(b, rs, res, axis=(vx / v, vy / v, 0), vel=(0, v * VEL_UNITS / 4096), **edit)

    def follower(b, rs, res, **edit):
        """One particle riding an emitter that MoveEmitter flies (so: no self-destruct)."""
        args = dict(flags_on=1 << 15, flags_off=(1 << 12) | (1 << 13) | (1 << 14) | BILLBOARD)
        args.update(edit)
        prop(b, rs, res, **args)

    def tex(b, idx, art, colors=32):
        if isinstance(art, bytes):
            spa.set_texture(b, idx, art)
            return
        colors = min(colors, spa.textures(bytes(b))[idx][6] // 2)
        texels, pal = fxart.to_a3i5(art, colors)
        spa.set_texture(b, idx, texels, pal)

    def kit(ps):
        bb = bytearray(files[DONOR[ps]])
        return bb, spa.resources(bytes(bb))


    def thrown(b, rs, size, spin):
        """Res THROWN as a lobbed object riding its emitter (see the Molotov / brick / egg)."""
        h = THROW_PEAK * VEL_UNITS / 4096
        g = 8 * h / THROW_FRAMES ** 2
        prop(b, rs, THROWN, life=THROW_FRAMES + 2, scl=size, axis=(0, 1, 0), vel=(0, g * THROW_FRAMES / 2),
             gravity=(0, -g, 0), tex=1, flags_on=(1 << 15) | (1 << 12), flags_off=(1 << 13) | (1 << 14) | BILLBOARD)
        rot(b, rs, THROWN, spin)

    def sign(ps, lines, **colors):
        b, rs = kit(ps)
        tex(b, 0, fxart.burst_sign(lines, **colors), 30)
        prop(b, rs, POP, scl=SIGN_SCALE, life=28, scl_anm=SIGN_POP)
        out[ps] = bytes(b)

    def poses(ps, art, scl, hold_life):
        b, rs = kit(ps)
        tex(b, 0, art, 30)
        prop(b, rs, POSE, scl=scl, life=SWING_STEP)
        prop(b, rs, HOLD, scl=scl, life=hold_life)
        out[ps] = bytes(b)

    # Catch Flight (Fly): HOOD AIR crossing the sky, then dive-bombing the target; smoke where it hits
    b, rs = kit(PLANE)
    tex(b, 1, fxart.jet())
    tex(b, 0, fxart.soft_puff())
    mover(b, rs, PASS, JET_SPEED, 0, scl=ONE_TO_ONE * JET_SCALE, life=round((256 + 2 * JET_HALF) / JET_SPEED))
    prop(b, rs, JETSMOKE, tex=0, clr=rgb(150, 150, 155), clr_anm=(rgb(230, 230, 230), rgb(110, 110, 115)), scl=.8,
         life=30, emtr_life=3, gen=4, init_pos=1, radius=.6, vel=(.03, 0), alpha=(31, 26, 0),
         scl_anm=(.6, 1.4, 2.0, 40, 150), air_resist=118)
    out[PLANE] = bytes(b)
    sign(WHAM, ["WHAM!"])

    # Ride Da Wave (Surf): a hydrant wave rolling across the block, a rubber duck riding it, foam on impact
    b, rs = kit(WAVE)
    tex(b, 1, fxart.wave_crest())
    tex(b, 0, fxart.soft_puff())
    mover(b, rs, WAVE_E, WAVE_SPEED, 0, scl=WAVE_SCALE, life=84)
    mover(b, rs, WAVE_P, -WAVE_SPEED, 0, scl=WAVE_SCALE, life=84)
    foam = rgb(225, 240, 255)
    prop(b, rs, FOAM, tex=0, clr=foam, clr_anm=(rgb(255, 255, 255), rgb(120, 180, 255)), scl=.55, life=26,
         emtr_life=4, gen=4, axis=(0, 1, 0), vel=(.03, .035), gravity=(0, -.0016, 0), init_pos=1, radius=.5,
         alpha=(31, 31, 0), air_resist=124)
    out[WAVE] = bytes(b)
    b, rs = kit(DUCK)
    tex(b, 1, fxart.rubber_duck(), 24)
    mover(b, rs, DUCK_E, WAVE_SPEED, 0, scl=1.2, life=84)
    mover(b, rs, DUCK_P, -WAVE_SPEED, 0, scl=1.2, life=84)
    out[DUCK] = bytes(b)

    # Power Line (Thunder): the snapped cable swinging down (poses), the x-ray skeleton, sparks
    poses(CABLE, fxart.power_cable(), 1.6, 56)
    b, rs = kit(XRAY)
    tex(b, 1, fxart.skeleton())
    tex(b, 0, fxart.glint())
    prop(b, rs, BONES, scl=1.25, life=40, flick=230)
    prop(b, rs, SPARKS, tex=0, clr=rgb(255, 250, 140), clr_anm=(rgb(255, 255, 255), rgb(255, 220, 40)), scl=.45,
         life=8, emtr_life=22, gen=3, init_pos=1, radius=.7, vel=(.05, 0), alpha=(31, 31, 0),
         flags_on=(1 << 14) | (1 << 13))
    out[XRAY] = bytes(b)

    # Road Rage (Dragon Rage): HONK!s, steam blasting off their head; traffic cones lobbed
    b, rs = kit(HONK)
    tex(b, 1, fxart.burst_sign(["HONK!"], fill=(250, 60, 40, 255), text=(255, 255, 255, 255)))
    tex(b, 0, fxart.soft_puff())
    prop(b, rs, HONK_A, scl=SIGN_SCALE, life=22, scl_anm=SIGN_POP)
    prop(b, rs, HONK_B, scl=SIGN_SCALE, life=22, scl_anm=SIGN_POP)
    prop(b, rs, STEAM, tex=0, clr=rgb(245, 245, 250), clr_anm=(rgb(255, 255, 255), rgb(200, 200, 210)), scl=.5,
         life=22, emtr_life=26, gen=2, gen_intvl=1, axis=(0, 1, 0), vel=(.012, .03), init_pos=1, radius=.3,
         alpha=(31, 28, 0), scl_anm=(.6, 1.2, 1.8, 30, 150), air_resist=122)
    out[HONK] = bytes(b)
    b, rs = kit(CONE)
    tex(b, 1, fxart.traffic_cone(), 24)
    thrown(b, rs, .8, 0x0B00)
    out[CONE] = bytes(b)

    # Molotov (Flamethrower): a swig from the bottle, spat through a lighter (fire breath), the bottle lobbed
    b, rs = kit(BOOZE)
    tex(b, 1, fxart.liquor_bottle(), 24)
    tex(b, 0, fxart.soft_puff(hard=1.6))
    prop(b, rs, SWIG, scl=ONE_TO_ONE, life=26)
    rot(b, rs, SWIG, init=0x2400)                                # tipped back
    thrown(b, rs, .8, 0x0A00)
    prop(b, rs, LIGHTER, tex=0, clr=rgb(255, 170, 40), clr_anm=(rgb(255, 240, 120), rgb(255, 90, 20)), scl=.35,
         life=40, flick=90)
    out[BOOZE] = bytes(b)
    b, rs = kit(BREATH)
    tex(b, 1, fxart.flame_blob())
    for res, sd in ((FIRE_E, "player"), (FIRE_P, "enemy")):
        spray(b, rs, res, sd, (12 if sd == "player" else -12, 30), (0, 16), BREATH_FRAMES, tex=1,
              clr=rgb(255, 130, 30), clr_anm=(rgb(255, 235, 110), rgb(220, 40, 20)), scl=.7, emtr_life=22, gen=2,
              gen_intvl=1, radius=.15, spread=.008, alpha=(31, 31, 0), scl_anm=(.4, 1.0, 1.6, 30, 200))
    out[BREATH] = bytes(b)

    # Zaza Leaf (Razor Leaf): a big leaf behind them, leaves flung like shuriken, the haze rolling in
    b, rs = kit(LEAF)
    tex(b, 1, fxart.big_weed_leaf())
    tex(b, 0, fxart.weed_leaf())
    green = rgb(80, 200, 60)
    for res, sd in ((LEAF_E, "player"), (LEAF_P, "enemy")):
        spray(b, rs, res, sd, (10 if sd == "player" else -10, 26), (0, 18), LEAF_FRAMES, tex=0, clr=green,
              clr_anm=(rgb(140, 240, 110), rgb(40, 150, 40)), scl=1.05, emtr_life=6, gen=2, gen_intvl=1, radius=.2,
              spread=.006, alpha=(31, 31, 31), flick=0, flags_on=(1 << 14) | (1 << 12) | (1 << 13))
        rot(b, rs, res, spin=0x1C00)
    prop(b, rs, BIGLEAF, scl=1.4, life=50, scl_anm=(.2, 1.15, 1.0, 30, 255), flags_on=(1 << 14) | (1 << 12))
    rot(b, rs, BIGLEAF, spin=0x0180)
    out[LEAF] = bytes(b)
    b, rs = kit(HAZE)
    tex(b, 1, fxart.tall_puff())
    prop(b, rs, HAZE1, tex=1, clr=rgb(150, 190, 130), clr_anm=(rgb(190, 225, 170), rgb(110, 140, 100)), scl=.9,
         life=44, emtr_life=22, gen=1, gen_intvl=2, init_pos=1, radius=1.0, vel=(.006, 0), alpha=(26, 22, 0),
         scl_anm=(.5, 1.3, 2.0, 40, 150), air_resist=120, flags_on=(1 << 14) | (1 << 13))
    prop(b, rs, 0, life=1)
    out[HAZE] = bytes(b)

    # Stomp Out (Pound): the boot coming down (poses), STOMP!, dust
    poses(BOOT, fxart.work_boot(), 1.5, 14)
    b, rs = kit(STOMP)
    tex(b, 1, fxart.burst_sign(["STOMP!"]))
    tex(b, 0, fxart.soft_puff())
    prop(b, rs, 2, scl=SIGN_SCALE, life=28, scl_anm=SIGN_POP)
    prop(b, rs, DUST, tex=0, clr=rgb(190, 165, 120), clr_anm=(rgb(230, 210, 170), rgb(150, 125, 90)), scl=.6,
         life=24, emtr_life=2, gen=6, init_pos=1, radius=.7, vel=(.05, 0), alpha=(31, 26, 0),
         scl_anm=(.6, 1.3, 1.8, 40, 150), air_resist=116)
    out[STOMP] = bytes(b)

    # Grill Chomp (Bite): the two jaws closing (poses), sparkles off the gold
    poses(TOPJAW, fxart.jaw(True), 1.3, 8)
    poses(BOTJAW, fxart.jaw(False), 1.3, 8)
    b, rs = kit(GLITZ)
    tex(b, 0, fxart.glint())
    gold = rgb(255, 220, 80)
    prop(b, rs, SPARKLE, tex=0, clr=gold, clr_anm=(rgb(255, 255, 220), gold), scl=.5, life=14, emtr_life=2, gen=3,
         init_pos=1, radius=.8, alpha=(31, 31, 0), scl_anm=(.2, 1.4, .6, 50, 160), flags_on=(1 << 14) | (1 << 12))
    rot(b, rs, SPARKLE, spin=0x0900)
    out[GLITZ] = bytes(b)

    # Hollow Point (Crunch): a laser-sight dot settling on them, then BANG - a bullet hole punched in, sparks
    b, rs = kit(SLUG)
    tex(b, 1, fxart.bullet_hole())
    tex(b, 0, fxart.laser_dot())
    red = rgb(255, 30, 30)
    prop(b, rs, DOT, tex=0, clr=red, clr_anm=(rgb(255, 120, 120), red), scl=.55, life=SWING_STEP, flick=40)
    prop(b, rs, HOLE, scl=1.15, life=38, scl_anm=(.3, 1.15, 1.0, 20, 255))
    prop(b, rs, IMPACT, tex=0, clr=rgb(255, 230, 120), clr_anm=(rgb(255, 255, 230), rgb(255, 140, 30)), scl=.3,
         life=12, emtr_life=2, gen=8, init_pos=1, radius=.3, vel=(.09, 0), alpha=(31, 31, 0), air_resist=118,
         flags_on=(1 << 14) | (1 << 13))
    prop(b, rs, 1, life=1)
    out[SLUG] = bytes(b)

    # Switchblade (Slash): three slashes at different angles, the blade's gleam; the tire, slashed flat, hissing
    b, rs = kit(SLASH)
    tex(b, 1, fxart.slash_arc())
    tex(b, 0, fxart.glint())
    for res, ang in ((SLASH_A, 0), (SLASH_B, 0x2800), (SLASH_C, 0xD400)):
        prop(b, rs, res, scl=1.3, life=9, alpha=(31, 31, 0), scl_anm=(.6, 1.25, 1.0, 40, 255))
        rot(b, rs, res, init=ang)
    prop(b, rs, GLEAM, tex=0, clr=rgb(255, 255, 255), scl=.6, life=10, scl_anm=(.2, 1.4, .3, 50, 160),
         alpha=(31, 31, 0))
    out[SLASH] = bytes(b)
    b, rs = kit(TIRE)
    tex(b, 1, fxart.tire(), 24)
    tex(b, 0, fxart.soft_puff())
    prop(b, rs, TIRE_UP, scl=1.0, life=56)
    prop(b, rs, TIRE_FLAT, scl=1.0, life=44, scl_anm=(1.0, 1.0, .85, 0, 120))
    prop(b, rs, HISS, tex=0, clr=rgb(240, 240, 245), scl=.35, life=14, emtr_life=16, gen=2, gen_intvl=1,
         init_pos=1, radius=.3, vel=(.045, 0), alpha=(30, 24, 0), scl_anm=(.6, 1.2, 1.8, 30, 150))
    out[TIRE] = bytes(b)

    # Hot Box (SmokeScreen): smoke everywhere, wisps over the target; *cough* clouds
    b, rs = kit(SMOG)
    tex(b, 1, fxart.tall_puff())
    tex(b, 0, fxart.soft_puff())
    smoke = rgb(170, 175, 160)
    prop(b, rs, SMOG1, tex=1, clr=smoke, clr_anm=(rgb(215, 220, 205), rgb(130, 135, 125)), scl=1.3, life=64,
         emtr_life=36, gen=1, gen_intvl=2, init_pos=1, radius=2.6, vel=(.005, 0), gravity=(0, .0002, 0),
         alpha=(24, 20, 0), scl_anm=(.5, 1.4, 2.2, 40, 160), air_resist=124, flags_on=(1 << 14) | (1 << 13))
    prop(b, rs, SMOG2, tex=0, clr=smoke, clr_anm=(rgb(235, 235, 225), rgb(150, 150, 140)), scl=.6, life=30,
         emtr_life=24, gen=2, gen_intvl=2, axis=(0, 1, 0), vel=(.006, .012), init_pos=1, radius=.7,
         alpha=(28, 22, 0), scl_anm=(.5, 1.2, 1.8, 40, 150), air_resist=122)
    out[SMOG] = bytes(b)
    b, rs = kit(COUGH)
    tex(b, 1, fxart.cough_bubble(), 24)
    prop(b, rs, PUFFUP, scl=.9, life=26, axis=(0, 1, 0), vel=(0, .9 * VEL_UNITS / 4096),
         scl_anm=(.3, 1.15, 1.0, 40, 255))
    out[COUGH] = bytes(b)

    # Burnout (Flame Wheel): the flaming tire spinning in place in its own smoke, then rolling in (flown) with
    # flames trailing it (a second flown emitter dropping flames)
    b, rs = kit(WHEEL)
    tex(b, 1, fxart.flame_wheel())
    tex(b, 0, fxart.soft_puff())
    prop(b, rs, SPIN, scl=1.0, life=30, scl_anm=(.4, 1.05, 1.0, 30, 255), flags_on=(1 << 14) | (1 << 12))
    rot(b, rs, SPIN, spin=-0x2600)
    follower(b, rs, ROLL, scl=1.0, life=ROLL_FRAMES + 2, flags_on=(1 << 15) | (1 << 12))
    rot(b, rs, ROLL, spin=-0x2600)
    prop(b, rs, SMOKE1, tex=0, clr=rgb(160, 160, 165), clr_anm=(rgb(230, 230, 235), rgb(110, 110, 115)), scl=.6,
         life=26, emtr_life=28, gen=2, gen_intvl=1, axis=(0, 1, 0), vel=(.02, .02), init_pos=1, radius=.4,
         alpha=(30, 24, 0), scl_anm=(.5, 1.3, 2.0, 40, 150), air_resist=120)
    out[WHEEL] = bytes(b)
    b, rs = kit(TRAIL)
    tex(b, 1, fxart.flame_blob())
    prop(b, rs, FIRETRAIL, tex=1, clr=rgb(255, 130, 30), clr_anm=(rgb(255, 235, 110), rgb(220, 40, 20)), scl=.55,
         life=14, emtr_life=ROLL_FRAMES + 2, gen=2, gen_intvl=1, axis=(0, 1, 0), vel=(.004, .008), alpha=(31, 31, 0),
         scl_anm=(1.0, 1.0, .3, 0, 120), flags_on=0,
         flags_off=(1 << 12) | (1 << 13) | (1 << 14) | (1 << 15) | BILLBOARD)
    prop(b, rs, 0, life=1)
    out[TRAIL] = bytes(b)

    # Hi-Yah Chop (Brick Break): a stack of bricks on their head - the two halves (one art, the right half turned
    # round) as stop-motion poses so they can split apart - and a giant karate hand chopping down (poses)
    b, rs = kit(BLOCKS)
    tex(b, 1, fxart.half_stack())
    tex(b, 0, fxart.chunk())
    prop(b, rs, HALF_L, scl=1.75, life=SWING_STEP)
    prop(b, rs, HALF_R, scl=1.75, life=SWING_STEP)
    rot(b, rs, HALF_R, init=0x8000)
    brick = rgb(190, 70, 50)
    prop(b, rs, CHUNKS, tex=0, clr=brick, clr_anm=(rgb(220, 110, 85), rgb(140, 45, 30)), scl=.5, life=30,
         emtr_life=2, gen=7, init_pos=1, radius=.5, axis=(0, 1, 0), vel=(.07, .05), gravity=(0, -.003, 0),
         air_resist=126, flags_on=(1 << 14) | (1 << 12) | (1 << 13))
    rot(b, rs, CHUNKS, spin=0x1400)
    prop(b, rs, 1, life=1)
    out[BLOCKS] = bytes(b)
    poses(CHOP, fxart.big_hand(), 1.5, 16)
    sign(HIYAH, ["HI-YAH!"], fill=(255, 140, 30, 255))

    # Magic 8-Ball (Shadow Ball): the ball growing in their hands in dark wisps, rolling over (flown), the answer
    b, rs = kit(EIGHT)
    tex(b, 1, fxart.eight_ball())
    tex(b, 0, fxart.soft_puff())
    prop(b, rs, CHARGE, scl=1.0, life=20, scl_anm=(.2, 1.0, 1.0, 120, 255))
    follower(b, rs, ROLL8, scl=1.0, life=EIGHT_FRAMES + 2, flags_on=(1 << 15) | (1 << 12))
    rot(b, rs, ROLL8, spin=-0x0C00)
    prop(b, rs, WISPS, tex=0, clr=rgb(90, 40, 140), clr_anm=(rgb(150, 90, 210), rgb(40, 10, 70)), scl=.55, life=22,
         emtr_life=20, gen=2, gen_intvl=1, axis=(0, 1, 0), vel=(.012, .02), init_pos=1, radius=.6,
         alpha=(28, 22, 0), scl_anm=(.5, 1.2, 1.6, 40, 150), air_resist=122)
    out[EIGHT] = bytes(b)
    b, rs = kit(ANSWER)
    tex(b, 0, fxart.eight_answer(), 30)
    prop(b, rs, POP, scl=ONE_TO_ONE / 1.15, life=44, scl_anm=(.2, 1.15, 1.0, 30, 255))
    out[ANSWER] = bytes(b)

    # Loyalty (Return): the RIDE OR DIE pendant glowing, hearts flying, the pendant slamming in (flown)
    b, rs = kit(HEART)
    tex(b, 1, fxart.heart_pendant())
    tex(b, 0, fxart.heart())
    prop(b, rs, LOCKET, scl=ONE_TO_ONE / 1.2, life=30, scl_anm=(.3, 1.2, 1.0, 30, 255))
    follower(b, rs, SLAM, scl=ONE_TO_ONE, life=HEART_FRAMES + 2)
    pink = rgb(255, 90, 150)
    for res, sd in ((HEARTS_E, "player"), (HEARTS_P, "enemy")):
        spray(b, rs, res, sd, (10 if sd == "player" else -10, 30), (0, 18), HEART_FRAMES, tex=0, clr=pink,
              clr_anm=(rgb(255, 170, 200), rgb(230, 40, 110)), scl=.5, emtr_life=8, gen=2, gen_intvl=1,
              radius=.2, spread=.01, alpha=(31, 31, 31), flick=0)
    out[HEART] = bytes(b)

    # ---- set 5 ---------------------------------------------------------------------------------------------
    FIXED_ROT = (1 << 12) | (1 << 13)                         # flags_off for sprays whose rotation is set by hand

    # Flashlight (Confuse Ray): a big flashlight aimed at their eyes, the beam, dizzy swirls, HUH?!
    b, rs = kit(TORCH)
    tex(b, 1, fxart.flashlight())
    tex(b, 0, fxart.dizzy_swirl())
    for res, sd in ((TORCH_E, "player"), (TORCH_P, "enemy")):
        prop(b, rs, res, scl=TORCH_SCALE, life=62, scl_anm=(.4, 1.1, 1.0, 30, 255))
        rot(b, rs, res, init=torch_geometry(sd)[0])
    violet = rgb(200, 90, 255)
    prop(b, rs, SWIRL, tex=0, clr=violet, clr_anm=(rgb(255, 170, 255), rgb(140, 40, 220)), scl=.42, life=40,
         scl_anm=(.3, 1.2, 1.0, 40, 255), flags_on=(1 << 14) | (1 << 12))
    rot(b, rs, SWIRL, spin=-0x1400)
    prop(b, rs, 3, life=1)
    out[TORCH] = bytes(b)
    b, rs = kit(BEAM)
    tex(b, 0, fxart.light_cone(), 30)
    for res, sd in ((BEAM_E, "player"), (BEAM_P, "enemy")):
        ang, _, _, scale = torch_geometry(sd)
        prop(b, rs, res, scl=scale, life=48, flick=50)
        rot(b, rs, res, init=ang)
    out[BEAM] = bytes(b)
    sign(HUH, ["HUH?!"], fill=(170, 90, 255, 255), text=(255, 235, 60, 255))

    # Stun Taser (Thunder Wave): the stun gun snapping, crackles shot at them, rings of static locking them up
    b, rs = kit(STUN)
    tex(b, 1, fxart.stun_gun())
    tex(b, 0, fxart.crackle())
    prop(b, rs, STUN_E, scl=1.1, life=50, scl_anm=(.4, 1.1, 1.0, 30, 255))
    b, flip = mirrored(b, fxart.stun_gun())
    prop(b, rs, STUN_P, scl=1.1, life=50, scl_anm=(.4, 1.1, 1.0, 30, 255), tex=flip)
    cyan = rgb(120, 220, 255)
    for res, sd in ((ARC_E, "player"), (ARC_P, "enemy")):
        spray(b, rs, res, sd, STUN_TIP[sd], (0, 22), STUN_FRAMES, tex=0, clr=cyan,
              clr_anm=(rgb(200, 240, 255), rgb(40, 110, 255)), scl=.3, emtr_life=8, gen=1, gen_intvl=1, radius=.2,
              spread=.02, alpha=(31, 31, 31), scl_anm=(1.0, 1.0, 1.0, 0, 255), flick=60,
              flags_on=(1 << 14) | (1 << 13))
    out[STUN] = bytes(b)
    b, rs = kit(STATIC)
    tex(b, 0, fxart.static_ring(), 30)
    prop(b, rs, RING_X, scl=1.5, life=14, scl_anm=(.3, 1.2, 1.6, 90, 200), alpha=(31, 31, 0))
    prop(b, rs, RING_HOLD, scl=1.3, life=44, flick=110)
    out[STATIC] = bytes(b)
    sign(ZZZT, ["ZZZT!"], fill=(80, 200, 255, 255), text=(255, 240, 40, 255))

    # Bass Boost (Supersonic): a boombox on their shoulder, pumping - sound waves and notes rattle their skull
    b, rs = kit(BOOMBOX)
    tex(b, 1, fxart.boombox())
    tex(b, 0, fxart.music_note())
    prop(b, rs, BOX5, scl=ONE_TO_ONE / 1.1, life=64, scl_anm=(.3, 1.1, 1.0, 30, 255))
    prop(b, rs, THUMP, scl=ONE_TO_ONE, life=6, scl_anm=(1.0, 1.2, 1.0, 90, 170))
    pink = rgb(255, 110, 210)
    for res, sd in ((NOTES_E, "player"), (NOTES_P, "enemy")):
        spray(b, rs, res, sd, BOX_AT[sd], BEAT_AIM, NOTE_FRAMES, tex=0, clr=pink,
              clr_anm=(rgb(255, 230, 120), rgb(255, 80, 200)), scl=.5, emtr_life=4, gen=1, gen_intvl=2, radius=.3,
              spread=.012, alpha=(31, 31, 31), scl_anm=(.6, 1.1, 1.0, 40, 255), flick=0,
              flags_off=(1 << 15) | BILLBOARD | FIXED_ROT)
    out[BOOMBOX] = bytes(b)
    b, rs = kit(SOUNDWAVE)
    tex(b, 1, fxart.sound_arc())
    for res, sd in ((SWAVE_E, "player"), (SWAVE_P, "enemy")):
        spray(b, rs, res, sd, BOX_AT[sd], BEAT_AIM, NOTE_FRAMES - 2, tex=1, clr=rgb(255, 120, 220),
              clr_anm=(rgb(255, 255, 255), rgb(240, 60, 200)), scl=1.0, emtr_life=5, gen=1, gen_intvl=2, radius=0,
              alpha=(31, 31, 18), scl_anm=(.5, 1.3, 1.6, 60, 200), flick=0, flags_off=(1 << 15) | BILLBOARD | FIXED_ROT)
        rot(b, rs, res, init=_angle(*aim_path(sd, BOX_AT[sd], BEAT_AIM)))
    out[SOUNDWAVE] = bytes(b)
    sign(BWOMP, ["BWOMP!"], fill=(255, 80, 200, 255), text=(255, 255, 255, 255))

    # Squad Up (Double Team): the homies pop out of nowhere, one after another
    b, rs = kit(SQUAD)
    tex(b, 1, fxart.squad_hoodie())
    tex(b, 0, fxart.soft_puff())
    prop(b, rs, FIG, scl=1.45, life=56, scl_anm=(.3, 1.1, 1.0, 30, 255))
    prop(b, rs, FIG_S, scl=1.0, life=56, scl_anm=(.3, 1.1, 1.0, 30, 255))
    prop(b, rs, POOF, tex=0, clr=rgb(170, 150, 210), clr_anm=(rgb(240, 230, 255), rgb(110, 90, 150)), scl=.5, life=20,
         emtr_life=2, gen=5, init_pos=1, radius=.6, vel=(.04, 0), alpha=(30, 24, 0), scl_anm=(.6, 1.3, 1.8, 40, 150),
         air_resist=116)
    prop(b, rs, 3, life=1)
    out[SQUAD] = bytes(b)
    b, rs = kit(SQUAD2)
    tex(b, 0, fxart.squad_cap(), 30)
    prop(b, rs, FIG2, scl=1.45, life=56, scl_anm=(.3, 1.1, 1.0, 30, 255))
    prop(b, rs, FIG2_S, scl=1.0, life=56, scl_anm=(.3, 1.1, 1.0, 30, 255))
    out[SQUAD2] = bytes(b)
    sign(SQUADUP, ["SQUAD", "UP!"], fill=(150, 90, 240, 255), text=(255, 220, 40, 255))

    # Water Bomb (Water Pulse): a water balloon lobbed - SPLOOSH - and they're dripping
    b, rs = kit(BALLOON)
    tex(b, 1, fxart.water_balloon(), 24)
    tex(b, 0, fxart.droplet())
    thrown(b, rs, .85, 0x0700)
    water = rgb(80, 160, 255)
    prop(b, rs, DROPS, tex=0, clr=water, clr_anm=(rgb(200, 235, 255), water), scl=.25, life=20, emtr_life=30, gen=1,
         gen_intvl=3, init_pos=1, radius=.7, axis=(0, -1, 0), vel=(0, .025), alpha=(31, 31, 0))
    prop(b, rs, 0, life=1)
    out[BALLOON] = bytes(b)
    b, rs = kit(DRENCH)
    tex(b, 1, fxart.splash_crown())
    tex(b, 0, fxart.droplet())
    prop(b, rs, CROWN, scl=1.7, life=26, scl_anm=(.3, 1.15, 1.0, 25, 255), alpha=(31, 31, 0))
    prop(b, rs, SPLASHDROPS, tex=0, clr=water, clr_anm=(rgb(220, 240, 255), water), scl=.3, life=26, emtr_life=2,
         gen=8, init_pos=1, radius=.4, axis=(0, 1, 0), vel=(.06, .05), gravity=(0, -.004, 0), air_resist=126)
    for res in (2, 3):
        prop(b, rs, res, life=1)
    out[DRENCH] = bytes(b)
    sign(SPLOOSH, ["SPLOOSH!"], fill=(60, 150, 255, 255), text=(255, 255, 255, 255))

    # Sneak Diss (Faint Attack): they vanish, "UR MID" pops up behind the target, and a palm comes down. OOOOH!
    b, rs = kit(DISS)
    tex(b, 0, fxart.diss_bubble(), 30)
    prop(b, rs, POP, scl=ONE_TO_ONE / 1.15, life=40, scl_anm=(.2, 1.15, 1.0, 30, 255))
    out[DISS] = bytes(b)
    b, rs = kit(SLAP)
    tex(b, 1, fxart.slap_hand())
    tex(b, 0, fxart.pow_lines())
    prop(b, rs, SLAP_POSE, scl=1.35, life=SWING_STEP)
    prop(b, rs, SLAP_HOLD, scl=1.35, life=12)
    prop(b, rs, POWS, tex=0, clr=rgb(255, 255, 255), clr_anm=(rgb(255, 255, 255), rgb(255, 220, 80)), scl=.9,
         life=10, scl_anm=(.5, 1.3, 1.5, 60, 200), alpha=(31, 31, 0))
    prop(b, rs, 3, life=1)
    out[SLAP] = bytes(b)
    sign(OOOH, ["OOOOH!"], fill=(255, 140, 30, 255), text=(255, 255, 255, 255))

    # Dirty Sprite (Toxic): a double cup of purple drank, thrown - it splashes all over them and they're bubbling
    b, rs = kit(CUP)
    tex(b, 1, fxart.double_cup(), 24)
    tex(b, 0, fxart.bubble())
    prop(b, rs, HELD, scl=1.0, life=16, scl_anm=(.4, 1.1, 1.0, 30, 255))
    thrown(b, rs, .9, 0x0900)
    drank = rgb(170, 70, 235)
    prop(b, rs, BUBBLES, tex=0, clr=drank, clr_anm=(rgb(230, 170, 255), rgb(120, 30, 190)), scl=.35, life=24,
         emtr_life=34, gen=1, gen_intvl=2, init_pos=1, radius=.8, axis=(0, 1, 0), vel=(.008, .03),
         scl_anm=(.4, 1.1, 1.3, 50, 200), alpha=(31, 31, 0), air_resist=126)
    out[CUP] = bytes(b)
    b, rs = kit(GOOP)
    tex(b, 1, fxart.goop())
    prop(b, rs, GOOP_SPLAT, tex=1, clr=drank, clr_anm=(rgb(220, 150, 255), drank), scl=.55, life=40, emtr_life=2,
         gen=2, init_pos=1, radius=.4, axis=(0, 1, 0), vel=(.006, 0), gravity=(0, -.0003, 0),
         scl_anm=(.4, 1.2, 1.0, 30, 200), air_resist=110)
    prop(b, rs, GOOP_DRIPS, tex=1, clr=drank, clr_anm=(rgb(220, 150, 255), rgb(110, 30, 170)), scl=.4, life=30,
         emtr_life=10, gen=1, gen_intvl=2, init_pos=1, radius=.8, axis=(0, -1, 0), vel=(.004, .008),
         gravity=(0, -.0008, 0), air_resist=120)
    out[GOOP] = bytes(b)
    sign(DIRTY, ["DIRTY!"], fill=(150, 60, 220, 255), text=(120, 255, 90, 255))

    # Duck n Cover (Protect): they duck behind a trash-can lid - everything pings off it. NOPE.
    b, rs = kit(LID)
    tex(b, 1, fxart.trash_lid())
    tex(b, 0, fxart.ping())
    prop(b, rs, LIDUP, scl=1.35, life=56, scl_anm=(.3, 1.15, 1.0, 25, 255))
    prop(b, rs, LIDFLASH, scl=1.35, life=10, scl_anm=(1.0, 1.3, 1.5, 0, 120), alpha=(26, 16, 0))
    prop(b, rs, PINGS, tex=0, clr=rgb(255, 255, 200), clr_anm=(rgb(255, 255, 255), rgb(255, 210, 60)), scl=.45,
         life=10, emtr_life=1, gen=1, scl_anm=(.3, 1.4, .6, 50, 160), alpha=(31, 31, 0))
    prop(b, rs, 3, life=1)
    out[LID] = bytes(b)
    sign(NOPE, ["NOPE."], fill=(110, 200, 255, 255), text=(225, 25, 25, 255))

    # Smackdown (Take Down): they charge in with a folding chair - CLANG - and see stars from the recoil
    b, rs = kit(CHAIR)
    tex(b, 1, fxart.folding_chair())
    tex(b, 0, fxart.star5())
    prop(b, rs, CHAIR_POSE, scl=1.5, life=SWING_STEP)
    prop(b, rs, CHAIR_HOLD, scl=1.5, life=12)
    prop(b, rs, STARS, tex=0, clr=rgb(255, 230, 60), clr_anm=(rgb(255, 255, 200), rgb(255, 200, 30)), scl=.35,
         life=7, alpha=(31, 31, 31))
    prop(b, rs, 3, life=1)
    out[CHAIR] = bytes(b)
    b, rs = kit(CLANG)
    tex(b, 0, fxart.impact_burst(), 30)
    prop(b, rs, POP, scl=1.6, life=12, scl_anm=(.3, 1.2, 1.0, 40, 255), alpha=(31, 31, 0))
    out[CLANG] = bytes(b)
    sign(SMACKDN, ["SMACK", "DOWN!"], fill=(230, 30, 30, 255), text=(255, 230, 40, 255))

    # Big Taser (Thunderbolt): an XL taser held high, crackling - then a giant bolt drops out of the sky on them
    b, rs = kit(BIGTASER)
    tex(b, 1, fxart.big_taser())
    tex(b, 0, fxart.zigzag())
    prop(b, rs, BIG_E, scl=ONE_TO_ONE / 1.1, life=52, scl_anm=(.3, 1.1, 1.0, 30, 255))
    b, flip = mirrored(b, fxart.big_taser(flip=True), flip=False)          # (the XL stays readable)
    prop(b, rs, BIG_P, scl=ONE_TO_ONE / 1.1, life=52, scl_anm=(.3, 1.1, 1.0, 30, 255), tex=flip)
    prop(b, rs, ZIGS, tex=0, clr=rgb(255, 240, 80), clr_anm=(rgb(255, 255, 255), rgb(120, 200, 255)), scl=.45,
         life=4, emtr_life=24, gen=2, init_pos=1, radius=.9, alpha=(31, 31, 31), flags_on=(1 << 14) | (1 << 13))
    prop(b, rs, 3, life=1)
    out[BIGTASER] = bytes(b)
    b, rs = kit(MEGABOLT)
    tex(b, 0, fxart.mega_bolt(), 30)
    prop(b, rs, STRIKE, scl=2.2, life=24, flick=90)
    prop(b, rs, STRIKE2, scl=1.5, life=10, flick=140)
    rot(b, rs, STRIKE2, init=0x0E00)
    out[MEGABOLT] = bytes(b)
    sign(BZZT, ["BZZZT!!"], fill=(255, 225, 30, 255), text=(40, 60, 230, 255))

    # Clock It (Foresight): side-eye... then the thumbnail red circle and arrow on them. U GOT CLOCKED
    b, rs = kit(EYES)
    tex(b, 1, fxart.side_eye())
    prop(b, rs, EYES_R, scl=1.2, life=6)
    prop(b, rs, EYES_L, scl=1.2, life=6)
    rot(b, rs, EYES_L, init=0x8000)
    for res in (0, 3):
        prop(b, rs, res, life=1)
    out[EYES] = bytes(b)
    b, rs = kit(CIRCLE)
    tex(b, 0, fxart.clocked_circle(), 30)
    prop(b, rs, POP, scl=2.0, life=46, scl_anm=(1.6, .95, 1.0, 20, 255))
    out[CIRCLE] = bytes(b)
    sign(CLOCKED, ["U GOT", "CLOCKED"], fill=(255, 255, 255, 255), text=(230, 20, 20, 255))

    # ---- set 6 ---------------------------------------------------------------------------------------------
    def no_offset(b, rs, res):
        """Clear the resource's built-in position offset (the 64px kits' res 3 sits ~40px up)."""
        b[rs[res]["off"] + 4:rs[res]["off"] + 16] = bytes(12)

    def no_delay(ps, res):
        """Clear the resource's start delay (header u16 at +50: file 168's res 1 waits 10 frames before it shows)."""
        bb = bytearray(out[ps])
        struct.pack_into("<H", bb, spa.resources(bytes(bb))[res]["off"] + 50, 0)
        out[ps] = bytes(bb)

    # Belt Whip (Vine Whip): the belt comes off and cracks down on them twice, buckle first. WHAP!
    b, rs = kit(BELT)
    tex(b, 0, fxart.belt_swing(), 30)
    for res, (spin, init) in ((BELT_E, (-0x1000, 0x5000)), (BELT_P, (0x1000, 0x3000))):    # (as the bat swings)
        prop(b, rs, res, scl=2.4, life=9, flags_on=(1 << 14) | (1 << 12))
        rot(b, rs, res, spin, init)
    out[BELT] = bytes(b)
    b, rs = kit(WELT)
    tex(b, 1, fxart.belt_welt())
    tex(b, 0, fxart.whip_snap())
    prop(b, rs, WELT1, scl=ONE_TO_ONE / 1.15, life=22, scl_anm=(.5, 1.15, 1.0, 30, 255))
    prop(b, rs, SNAPS, tex=0, clr=rgb(255, 245, 210), clr_anm=(rgb(255, 255, 255), rgb(255, 200, 80)), scl=.6,
         life=12, emtr_life=1, gen=4, init_pos=1, radius=.7, vel=(.05, 0), alpha=(31, 31, 0),
         scl_anm=(.5, 1.2, .8, 50, 200), air_resist=120, flags_on=(1 << 14) | (1 << 12))
    rot(b, rs, SNAPS, 0x0800, 0)
    for res in (2, 3):
        prop(b, rs, res, life=1)
    out[WELT] = bytes(b)
    sign(WHAP, ["WHAP!"], fill=(150, 80, 35, 255), text=(255, 215, 40, 255))

    # Shiv (Poison Sting): they dash in - jab, jab, jab - with a toothbrush shiv. Skulls rise off them. SHIV'D!
    b, rs = kit(SHIV)
    tex(b, 1, fxart.shiv())
    tex(b, 0, fxart.skull())
    prop(b, rs, SHIV_E, scl=1.3, life=SWING_STEP)
    prop(b, rs, SHIV_P, scl=1.3, life=SWING_STEP)
    rot(b, rs, SHIV_P, init=0x8000)
    tox = rgb(120, 235, 60)
    prop(b, rs, SKULLS, tex=0, clr=tox, clr_anm=(rgb(210, 255, 160), rgb(80, 190, 40)), scl=.5, life=30,
         emtr_life=14, gen=1, gen_intvl=3, init_pos=1, radius=.8, axis=(0, 1, 0), vel=(.006, .03),
         scl_anm=(.4, 1.1, 1.0, 40, 255), alpha=(31, 31, 0), air_resist=126)
    prop(b, rs, 3, life=1)
    out[SHIV] = bytes(b)
    sign(SHIVD, ["SHIV'D!"], fill=(120, 230, 60, 255), text=(70, 20, 110, 255))

    # Twerk On Em (Tail Whip): they turn round and twerk on them - so disrespectful the foe's guard drops. BRUH.
    b, rs = kit(TWERK)
    tex(b, 0, fxart.wiggle_lines())
    pink = rgb(255, 120, 200)
    for res, init in ((WIGGLE_R, 0), (WIGGLE_L, 0x8000)):
        prop(b, rs, res, tex=0, clr=pink, clr_anm=(rgb(255, 255, 255), pink), scl=.95, life=6, alpha=(31, 31, 0))
        rot(b, rs, res, init=init)
        no_offset(b, rs, res)
    for res in (1, 2):
        prop(b, rs, res, life=1)
    out[TWERK] = bytes(b)
    b, rs = kit(DEFDOWN)
    tex(b, 0, fxart.cracked_shield(), 30)
    prop(b, rs, POP, scl=ONE_TO_ONE / 1.15, life=36, scl_anm=(.3, 1.15, 1.0, 30, 255))
    out[DEFDOWN] = bytes(b)
    sign(BRUH, ["BRUH."], fill=(60, 110, 220, 255), text=(255, 255, 255, 255))

    # Tax (Absorb): an IRS stamp comes down - TAXED - and their coins flow straight into the user's money bag
    poses(STAMP, fxart.rubber_stamp(), ONE_TO_ONE, 12)
    no_delay(STAMP, HOLD)
    b, rs = kit(TAXED)
    tex(b, 0, fxart.taxed_mark(), 30)
    prop(b, rs, POP, scl=ONE_TO_ONE, life=70, scl_anm=(1.5, 1.0, 1.0, 12, 255))
    out[TAXED] = bytes(b)
    b, rs = kit(COINS)
    tex(b, 1, fxart.money_bag())
    tex(b, 0, fxart.coin())
    prop(b, rs, MONEYBAG, scl=ONE_TO_ONE / 1.1, life=56, scl_anm=(.3, 1.1, 1.0, 30, 255))
    gold = rgb(255, 205, 40)
    for res, sd in ((COIN_E, "player"), (COIN_P, "enemy")):   # from the target back to the attacker's bag
        other = "enemy" if sd == "player" else "player"
        spray(b, rs, res, other, (0, 20), BAG_SPOT[sd], COIN_FRAMES, tex=0, clr=gold,
              clr_anm=(rgb(255, 250, 190), rgb(220, 150, 20)), scl=.7, emtr_life=18, gen=1, gen_intvl=2,
              radius=.5, spread=.006, alpha=(31, 31, 31), scl_anm=(1.0, 1.0, .7, 0, 200), flick=0,
              flags_on=(1 << 14) | (1 << 12))
        rot(b, rs, res, 0x0C00, 0)                            # flipping over
        no_offset(b, rs, res)
    prop(b, rs, 2, life=1)
    out[COINS] = bytes(b)

    # Silly String (String Shot): a can of silly string - PSSSHHH - neon string all over them. STUCK!
    b, rs = kit(CAN)
    tex(b, 1, fxart.silly_can())
    tex(b, 0, fxart.squiggle())
    prop(b, rs, CAN1, scl=ONE_TO_ONE / 1.1, life=56, scl_anm=(.3, 1.1, 1.0, 30, 255))
    for res, sd in ((STR_E, "player"), (STR_P, "enemy")):
        at = CAN_AT[sd]
        spray(b, rs, res, sd, (at[0], at[1] + NOZZLE_UP), STRING_AIM, STRING_FRAMES, tex=0, clr=rgb(255, 60, 170),
              clr_anm=(rgb(150, 255, 60), rgb(255, 60, 200)), scl=.6, emtr_life=8, gen=2, gen_intvl=1, radius=.15,
              spread=.012, alpha=(31, 31, 31), scl_anm=(.5, 1.2, 1.2, 40, 255), flick=0, rndm=(0, 40, 0),
              flags_on=(1 << 14) | (1 << 12))
        rot(b, rs, res, 0x0900, 0)
        no_offset(b, rs, res)
    prop(b, rs, 2, life=1)
    out[CAN] = bytes(b)
    b, rs = kit(TANGLE)
    tex(b, 0, fxart.string_tangle(), 30)
    prop(b, rs, TANGLED, scl=1.5, life=10, scl_anm=(.4, 1.1, 1.0, 50, 255))
    prop(b, rs, TANGLE_HOLD, scl=1.5, life=44)
    out[TANGLE] = bytes(b)
    no_delay(TANGLE, TANGLE_HOLD)
    sign(STUCK, ["STUCK!"], fill=(255, 60, 170, 255), text=(150, 255, 60, 255))

    # Spit (Bubble): they lean back... PTOO! A loogie lobs over and splats right on them. It's running.
    b, rs = kit(SPIT)
    tex(b, 1, fxart.loogie(), 24)
    tex(b, 0, fxart.gob_drip())
    thrown(b, rs, .8, 0x0600)
    gob = rgb(200, 240, 170)
    prop(b, rs, DRIBBLE, tex=0, clr=gob, clr_anm=(rgb(240, 255, 230), gob), scl=.35, life=22, emtr_life=30, gen=1,
         gen_intvl=3, init_pos=1, radius=.6, axis=(0, -1, 0), vel=(0, .02), alpha=(31, 31, 0))
    prop(b, rs, 0, life=1)
    out[SPIT] = bytes(b)
    b, rs = kit(GOBSPLAT)
    tex(b, 0, fxart.spit_splat(), 30)
    prop(b, rs, POP, scl=1.05, life=44, scl_anm=(.3, 1.15, 1.0, 25, 255))
    out[GOBSPLAT] = bytes(b)
    sign(PTOO, ["PTOO!"], fill=(90, 170, 70, 255), text=(255, 255, 255, 255))

    # ---- set 7 ---------------------------------------------------------------------------------------------
    # Lace Up (Agility): a fresh pair of kicks, then they're zipping back and forth. LACED UP!
    b, rs = kit(KICKS)
    tex(b, 1, fxart.sneaker())
    tex(b, 0, fxart.speed_lines())
    prop(b, rs, SHOES, scl=1.0, life=24, scl_anm=(.3, 1.15, 1.0, 30, 255), alpha=(31, 31, 0))
    prop(b, rs, ZOOMS, tex=0, clr=rgb(255, 255, 255), clr_anm=(rgb(255, 255, 255), rgb(255, 230, 120)), scl=.9,
         life=8, alpha=(31, 31, 0))
    for res in (2, 3):
        prop(b, rs, res, life=1)
    out[KICKS] = bytes(b)
    sign(LACED, ["LACED", "UP!"], fill=(225, 35, 45, 255), text=(255, 255, 255, 255))

    # Go Out Loud (Selfdestruct): a crate of fireworks, the fuse fizzing... then the whole sky goes off. BOOOM!
    b, rs = kit(CRATE)
    tex(b, 1, fxart.fireworks_crate())
    tex(b, 0, fxart.twinkle())
    prop(b, rs, BOX7, scl=ONE_TO_ONE / 1.1, life=46, scl_anm=(.3, 1.1, 1.0, 30, 255))
    prop(b, rs, FUSE, tex=0, clr=rgb(255, 220, 80), clr_anm=(rgb(255, 255, 220), rgb(255, 120, 30)), scl=.45,
         life=12, emtr_life=36, gen=2, init_pos=1, radius=.1, axis=(0, 1, 0), vel=(.03, .025),
         gravity=(0, -.002, 0), alpha=(31, 31, 0), air_resist=124)
    prop(b, rs, GLITTER, tex=0, clr=rgb(255, 120, 200), clr_anm=(rgb(120, 230, 255), rgb(255, 230, 60)), scl=.6,
         life=34, emtr_life=2, gen=8, init_pos=1, radius=.6, vel=(.07, 0), alpha=(31, 31, 0), air_resist=118,
         scl_anm=(1.0, 1.1, .4, 50, 160))
    no_offset(b, rs, GLITTER)
    prop(b, rs, 2, life=1)
    out[CRATE] = bytes(b)
    b, rs = kit(FWBURST)
    tex(b, 0, fxart.firework_burst(), 30)
    prop(b, rs, POP, scl=1.9, life=22, scl_anm=(.2, 1.15, 1.35, 40, 150), alpha=(31, 31, 0))
    prop(b, rs, 1, scl=1.2, life=18, scl_anm=(.2, 1.2, 1.4, 40, 150), alpha=(31, 31, 0))
    out[FWBURST] = bytes(b)
    no_delay(FWBURST, 1)
    sign(BOOOM, ["BOOOM!"], fill=(255, 60, 90, 255), text=(255, 240, 60, 255))

    # Roll Out (Rollout): they come barrelling in riding a shopping cart - CRASH - the cart flips
    for ps, art, sd in ((CART, fxart.shopping_cart(), "player"), (CARTL, fxart.shopping_cart(left=True), "enemy")):
        b, rs = kit(ps)
        tex(b, 1, art)
        sx = 1 if sd == "player" else -1
        mover(b, rs, CART_GO, sx * CART_RUN[0] / CART_LIFE, sx * CART_RUN[1] / CART_LIFE, scl=1.45,
              life=CART_LIFE - 6)                      # gone as it hits (the flipped one takes over)
        prop(b, rs, CART_FLIP, scl=1.45, life=30)
        rot(b, rs, CART_FLIP, init=-sx * 0x2400)              # tipped onto its nose
        for res in (0, 3):
            prop(b, rs, res, life=1)
        out[ps] = bytes(b)
    sign(CRASH, ["CRASH!"], fill=(255, 150, 30, 255), text=(255, 255, 255, 255))

    # Lock In (Focus Energy): the headphones go on, the world goes quiet and red, everything pulls in. LOCKED IN.
    b, rs = kit(PHONES)
    tex(b, 1, fxart.headphones())
    tex(b, 0, fxart.focus_mote())
    prop(b, rs, CANS, scl=1.2, life=56, scl_anm=(1.8, .95, 1.0, 20, 255))
    prop(b, rs, CANS_THUMP, scl=1.2, life=6, scl_anm=(1.0, 1.18, 1.0, 90, 170))
    prop(b, rs, MOTES, tex=0, clr=rgb(255, 70, 50), clr_anm=(rgb(255, 230, 200), rgb(255, 40, 40)), scl=.5, life=20,
         emtr_life=24, gen=2, gen_intvl=2, init_pos=1, radius=1.6, vel=(-.06, 0), alpha=(0, 31, 31),
         air_resist=128)
    prop(b, rs, 3, life=1)
    out[PHONES] = bytes(b)
    sign(LOCKED, ["LOCKED", "IN."], fill=(30, 30, 40, 255), text=(255, 60, 60, 255))

    # Dome Check (Headbutt): a running headbutt - BONK - and a big bump swells up on their dome
    b, rs = kit(BUMP)
    tex(b, 0, fxart.dome_bump(), 30)
    prop(b, rs, POP, scl=1.0, life=48, scl_anm=(.1, 1.3, 1.0, 40, 255))
    prop(b, rs, 1, scl=1.0, life=6, scl_anm=(1.0, 1.2, 1.0, 90, 170))
    out[BUMP] = bytes(b)
    no_delay(BUMP, 1)
    sign(DOMECHK, ["DOME", "CHECK!"], fill=(255, 120, 140, 255), text=(255, 255, 255, 255))

    # Pickpocket (Fury Swipes - it plays once per hit, so it's quick): a hand dips in, comes up with the wallet
    poses(GRAB, fxart.grab_hand(), 1.15, 10)
    poses(YANK, fxart.hand_wallet(), 1.15, 10)
    no_delay(GRAB, HOLD)
    no_delay(YANK, HOLD)
    sign(YOINK, ["YOINK!"], fill=(70, 160, 60, 255), text=(255, 255, 255, 255))

    # ---- set 8 ---------------------------------------------------------------------------------------------
    # Pool Float (Aqua Ring): a sprinkle-donut pool float round their waist - ripples, bobbing, healing. CHILLIN'
    b, rs = kit(POOLF)
    tex(b, 1, fxart.pool_float())
    tex(b, 0, fxart.ripple())
    prop(b, rs, FLOATIE, scl=1.3, life=64, scl_anm=(.3, 1.1, 1.0, 30, 255))
    prop(b, rs, RIPPLES, tex=0, clr=rgb(120, 200, 255), clr_anm=(rgb(230, 245, 255), rgb(60, 150, 255)), scl=1.2,
         life=24, scl_anm=(.5, 1.4, 2.2, 90, 200), alpha=(31, 26, 0))
    for res in (2, 3):
        prop(b, rs, res, life=1)
    out[POOLF] = bytes(b)
    sign(CHILLIN, ["CHILLIN'"], fill=(90, 200, 255, 255), text=(255, 255, 255, 255))

    # Block Off (Mean Look): CAUTION tape slapped across them in an X, a ROAD CLOSED barricade in front. NO EXIT.
    b, rs = kit(TAPE)
    tex(b, 1, fxart.caution_tape())
    for res, ang in ((TAPE_A, 0x1400), (TAPE_B, -0x1400)):
        prop(b, rs, res, scl=1.7, life=60, scl_anm=(1.5, 1.0, 1.0, 12, 255))
        rot(b, rs, res, init=ang)
    for res in (0, 3):
        prop(b, rs, res, life=1)
    out[TAPE] = bytes(b)
    b, rs = kit(BARRIER)
    tex(b, 0, fxart.barricade(), 30)
    prop(b, rs, POP, scl=ONE_TO_ONE / 1.1, life=50, scl_anm=(.3, 1.1, 1.0, 25, 255))
    out[BARRIER] = bytes(b)
    sign(NOEXIT, ["NO", "EXIT."], fill=(30, 30, 35, 255), text=(255, 220, 30, 255))

    # Cheap Shot (Sucker Punch): "YO LOOK!!" - they look - and a fist comes right at them. CHEAP SHOT!
    b, rs = kit(LOOKBUB)
    tex(b, 0, fxart.look_bubble(), 30)
    prop(b, rs, POP, scl=ONE_TO_ONE / 1.15, life=30, scl_anm=(.2, 1.15, 1.0, 30, 255))
    out[LOOKBUB] = bytes(b)
    poses(FIST, fxart.fist_front(), 1.15, 10)
    no_delay(FIST, HOLD)
    sign(CHEAP, ["CHEAP", "SHOT!"], fill=(255, 90, 40, 255), text=(255, 255, 255, 255))

    # Jam the Gun (Disable): their gun pops up over them - click... click... - a sad sputter. JAMMED!
    b, rs = kit(JAMGUN)
    tex(b, 1, fxart.pistol_up())
    tex(b, 0, fxart.sputter())
    prop(b, rs, GUNUP, scl=1.35, life=56, scl_anm=(.3, 1.1, 1.0, 30, 255))
    prop(b, rs, SPUTTERS, tex=0, clr=rgb(190, 190, 195), clr_anm=(rgb(240, 240, 240), rgb(120, 120, 125)), scl=.5,
         life=18, axis=(0, 1, 0), vel=(0, .012), scl_anm=(.5, 1.0, 1.3, 60, 200), alpha=(28, 24, 0))
    for res in (2, 3):
        prop(b, rs, res, life=1)
    out[JAMGUN] = bytes(b)
    sign(JAMMED, ["JAMMED!"], fill=(150, 150, 160, 255), text=(230, 30, 30, 255))

    # Sleeper (Sleep Powder): a fat cigar in their mouth - one long drag, smoke rings - and they nod off. Zzz.
    b, rs = kit(CIGAR)
    tex(b, 1, fxart.cigar())
    tex(b, 0, fxart.smoke_ring())
    for res, ang in ((CIGAR_R, 0), (CIGAR_L, 0x8000)):
        prop(b, rs, res, scl=.9, life=70, scl_anm=(.3, 1.1, 1.0, 30, 255))
        rot(b, rs, res, init=ang)
    prop(b, rs, RINGS8, tex=0, clr=rgb(215, 215, 225), clr_anm=(rgb(250, 250, 255), rgb(150, 150, 165)), scl=.7,
         life=30, axis=(0, 1, 0), vel=(0, .016), scl_anm=(.4, 1.1, 1.8, 60, 200), alpha=(30, 26, 0))
    prop(b, rs, 3, life=1)
    out[CIGAR] = bytes(b)
    b, rs = kit(SNOOZE)
    tex(b, 0, fxart.zee())
    prop(b, rs, ZZZ, tex=0, clr=rgb(150, 170, 255), clr_anm=(rgb(230, 235, 255), rgb(110, 120, 255)), scl=.55,
         life=26, emtr_life=30, gen=1, gen_intvl=8, axis=(.4, 1, 0), vel=(0, .02),
         scl_anm=(.4, 1.2, 1.0, 50, 255), alpha=(31, 31, 0))
    prop(b, rs, 1, life=1)
    out[SNOOZE] = bytes(b)
    sign(NIGHT, ["NIGHT", "NIGHT"], fill=(60, 50, 140, 255), text=(255, 240, 120, 255))

    # Reload (Recover): a fat magazine slams up into place - CHK-CHK - and they patch up. RELOADED.
    poses(MAG, fxart.magazine(), 1.1, 14)
    no_delay(MAG, HOLD)
    b, rs = kit(HEALS)
    tex(b, 0, fxart.plus_cross())
    prop(b, rs, PLUSES, tex=0, clr=rgb(110, 255, 120), clr_anm=(rgb(230, 255, 230), rgb(60, 220, 90)), scl=.5,
         life=26, emtr_life=20, gen=1, gen_intvl=3, init_pos=1, radius=.9, axis=(0, 1, 0), vel=(.004, .022),
         scl_anm=(.4, 1.1, .8, 50, 200), alpha=(31, 31, 0))
    prop(b, rs, 1, life=1)
    out[HEALS] = bytes(b)
    sign(RELOADED, ["RELOADED"], fill=(60, 60, 70, 255), text=(255, 205, 60, 255))

    # ---- effect animations (a/0/6/1): status conditions, items, stat changes, level up -------------------
    def motes(ps, art, hi, lo, scl=.5, axis=(0, 1, 0), vel=(.004, .022), life=26, emtr=18, intvl=3, radius=.9,
              **extra):
        """Little tinted shapes drifting off the battler (res 0); res 1 unused."""
        b, rs = kit(ps)
        tex(b, 0, art)
        prop(b, rs, 0, tex=0, clr=lo, clr_anm=(hi, lo), scl=scl * 1.6, life=life, emtr_life=emtr, gen=1, gen_intvl=intvl,
             init_pos=1, radius=radius, axis=axis, vel=vel, scl_anm=(.4, 1.1, .8, 50, 200), alpha=(31, 31, 0),
             **extra)
        prop(b, rs, 1, life=1)
        out[ps] = bytes(b)

    # Hennessy (Potion) and every other heal: the bottle tips up over them, glug glug
    b, rs = kit(HENNY)
    tex(b, 0, fxart.henny_bottle(), 30)
    prop(b, rs, POSE, scl=ONE_TO_ONE, life=SWING_STEP)
    prop(b, rs, HOLD, scl=ONE_TO_ONE, life=34)
    rot(b, rs, HOLD, init=0x5800)                             # tipped right over: pouring
    out[HENNY] = bytes(b)
    # using any item from the bag: the corner-store THANK YOU bag drops on them
    poses(STOREBAG, fxart.thank_you_bag(), ONE_TO_ONE, 30)
    sign(LOOKS, ["GOOD", "LOOKS!"], fill=(255, 255, 255, 255), text=(220, 30, 40, 255))
    sign(FELICIA, ["BYE", "FELICIA!"], fill=(255, 140, 200, 255), text=(255, 255, 255, 255))
    b, rs = kit(CLAIM)                                        # the suitcase (its own kit: drawn over the jet's)
    b, case = mirrored(b, fxart.suitcase(), 16, flip=False)
    mover(b, rs, SUIT, 0, -FALL_SPEED, scl=ONE_TO_ONE, tex=case, life=FALL_FRAMES - 1)   # 32px at 2:1; gone as it hits
    out[CLAIM] = bytes(b)
    sign(AHHH, ["GLUG", "GLUG!"], fill=(250, 170, 40, 255), text=(255, 255, 255, 255))
    motes(DRIPS, fxart.amber_drip(), rgb(255, 200, 90), rgb(200, 110, 20), scl=.42, axis=(0, -1, 0),
          vel=(.002, .02), radius=.3, emtr=20, intvl=2)
    # held item / berry: reaching into the stash
    sign(STASH, ["STASH!"], fill=(70, 150, 70, 255), text=(255, 255, 255, 255))
    motes(STASHG, fxart.ice_glint(), rgb(255, 255, 220), rgb(120, 230, 120), scl=.5, emtr=10)
    sign(SNORE, ["5 MORE", "MINUTES"], fill=(70, 60, 150, 255), text=(255, 240, 140, 255))
    motes(SNOREZ, fxart.snore_z(), rgb(230, 235, 255), rgb(120, 130, 255), scl=.55, axis=(.5, 1, 0),
          vel=(.002, .016), intvl=6, life=30, radius=.2)
    sign(BADBATCH, ["BAD", "BATCH"], fill=(150, 60, 190, 255), text=(170, 255, 90, 255))
    motes(TOXB, fxart.toxic_bubble(), rgb(220, 160, 255), rgb(150, 60, 200), scl=.55)
    sign(BURNS, ["IT", "BURNS!"], fill=(255, 140, 30, 255), text=(255, 255, 220, 255))
    motes(BURNF, fxart.flame_blob(16, 16), rgb(255, 240, 120), rgb(255, 70, 20),
          scl=.6, emtr=14, intvl=2, vel=(.006, .03))
    sign(ICED, ["ICED", "OUT"], fill=(90, 180, 255, 255), text=(255, 255, 255, 255))
    motes(ICEG, fxart.ice_glint(), rgb(255, 255, 255), rgb(130, 210, 255), scl=.7, emtr=16, vel=(.002, .006),
          radius=1.1)
    sign(TASED, ["TASED!"])
    motes(JAGS, fxart.spark_jag(), rgb(255, 255, 200), rgb(255, 220, 30), scl=.6, emtr=16, intvl=2,
          vel=(.01, .01), radius=1.0)
    sign(WHERE, ["WHERE", "AM I?"], fill=(255, 255, 255, 255), text=(40, 40, 200, 255))
    motes(QMARKS, fxart.qmark(), rgb(255, 255, 255), rgb(255, 210, 60), scl=.6, intvl=5, radius=.7)
    sign(CRUSH, ["CRUSHIN'"], fill=(255, 90, 160, 255), text=(255, 255, 255, 255))
    motes(HEARTS2, fxart.fat_heart(), rgb(255, 200, 220), rgb(255, 60, 130), scl=.55, intvl=4)
    sign(GAINS, ["GAINS!"], fill=(230, 40, 40, 255), text=(255, 255, 255, 255))
    motes(UPS, fxart.arrow(), rgb(255, 230, 200), rgb(255, 80, 60), scl=.6, intvl=3, vel=(.002, .035), radius=1.0)
    sign(DOWNBAD, ["DOWN", "BAD"], fill=(60, 90, 200, 255), text=(255, 255, 255, 255))
    motes(DOWNS, fxart.arrow(up=False), rgb(200, 220, 255), rgb(60, 110, 255), scl=.6, intvl=3, axis=(0, -1, 0),
          vel=(.002, .03), radius=1.0)
    sign(CLOUT, ["CLOUT", "UP!"])
    motes(CLOUTUPS, fxart.arrow(), rgb(255, 255, 200), rgb(255, 200, 30), scl=.6, intvl=3, vel=(.002, .035),
          radius=1.0)
    # ---- set 9 ---------------------------------------------------------------------------------------------
    # Flop (Splash): they flop around like a fish... nothing. A tumbleweed rolls by. The judges hold up a 0/10.
    b, rs = kit(TUMBLE)
    tex(b, 1, fxart.tumbleweed())
    tex(b, 0, fxart.hop_ticks())
    mover(b, rs, TUMBLE_GO, TUMBLE_SPEED, 0, scl=1.0, life=round((256 + 80) / TUMBLE_SPEED),
          flags_on=(1 << 14) | (1 << 12))
    rot(b, rs, TUMBLE_GO, spin=-0x0900)                       # rolling (clockwise: it's going right)
    prop(b, rs, HOPS, tex=0, scl=.8, life=8, alpha=(31, 31, 0), scl_anm=(.6, 1.2, 1.0, 60, 255))
    for res in (2, 3):
        prop(b, rs, res, life=1)
    out[TUMBLE] = bytes(b)
    b, rs = kit(SCORE)
    tex(b, 0, fxart.scorecard(), 30)
    prop(b, rs, POP, scl=ONE_TO_ONE / 1.15, life=46, scl_anm=(.2, 1.15, 1.0, 30, 255))
    prop(b, rs, 1, life=1)
    out[SCORE] = bytes(b)

    # Windmill (Flail): arms windmilling like a madman, then they run in swinging. HANDS!
    b, rs = kit(ARMS)
    tex(b, 1, fxart.windmill_arms())
    tex(b, 0, fxart.smack_star())
    for res, life in ((MILL_HERE, 18), (MILL_THERE, 30)):
        prop(b, rs, res, scl=1.35, life=life, flags_on=(1 << 14) | (1 << 12))
        rot(b, rs, res, spin=MILL_SPIN)
    prop(b, rs, STARS9, tex=0, clr=rgb(255, 230, 60), clr_anm=(rgb(255, 255, 230), rgb(255, 170, 30)), scl=.5,
         life=12, gen=4, init_pos=1, radius=.4, vel=(.07, 0), alpha=(31, 31, 0), air_resist=120)
    prop(b, rs, 3, life=1)
    out[ARMS] = bytes(b)
    sign(HANDS, ["HANDS!"], fill=(230, 40, 40, 255), text=(255, 255, 255, 255))

    # Make It Rain (Rain Dance): a neon money gun, brrrrt - bills shot sky high - and it rains money on the block
    b, rs = kit(MGUN)
    tex(b, 1, fxart.money_gun())
    b, left = mirrored(b, fxart.money_gun())
    tex(b, 0, fxart.bill_flutter())
    for res, t in ((GUN_R, 1), (GUN_L, left)):
        prop(b, rs, res, tex=t, scl=1.0, life=60, scl_anm=(.3, 1.1, 1.0, 30, 255))
    for res, sx in ((BILLS_E, 1), (BILLS_P, -1)):
        d = math.hypot(.5, 1)
        prop(b, rs, res, tex=0, clr=rgb(110, 210, 100), clr_anm=(rgb(200, 255, 190), rgb(60, 160, 60)), scl=.5,
             life=24, gen=2, gen_intvl=2, emtr_life=24, axis=(sx * .5 / d, 1 / d, 0), vel=(.04, .36),
             gravity=(0, -.014, 0), air_resist=122, alpha=(31, 31, 0), flags_on=(1 << 14) | (1 << 12))
        rot(b, rs, res, spin=sx * 0x0700)
    out[MGUN] = bytes(b)
    b, rs = kit(BILLRAIN)
    tex(b, 0, fxart.bill_flutter())
    for res, hi, lo, spin in ((RAIN_A, rgb(210, 255, 200), rgb(100, 200, 90), 0x0500),
                              (RAIN_B, rgb(150, 220, 140), rgb(50, 140, 60), -0x0400)):
        prop(b, rs, res, tex=0, clr=lo, clr_anm=(hi, lo), scl=.5, life=60, gen=1, gen_intvl=2, emtr_life=44,
             init_pos=1, radius=3.0, axis=(0, -1, 0), vel=(.012, .2), alpha=(31, 31, 0), air_resist=128,
             flags_on=(1 << 14) | (1 << 12))
        rot(b, rs, res, spin=spin)
    out[BILLRAIN] = bytes(b)
    sign(RAINSIGN, ["MAKE IT", "RAIN!"], fill=(70, 190, 80, 255), text=(255, 255, 255, 255))

    # Insurance (Assurance): the payout - a giant novelty check, $1000000 - and they smack the foe with it
    poses(CHECK, fxart.novelty_check(), SIGN_SCALE, 24)                     # 2:1: the amount has to read
    no_delay(CHECK, HOLD)
    sign(PAYOUT, ["CLAIM", "PAID!"], fill=(40, 120, 220, 255), text=(255, 255, 255, 255))
    b, rs = kit(CASHSPARK)
    tex(b, 0, fxart.cash_twinkle())
    prop(b, rs, 0, tex=0, clr=rgb(255, 220, 60), clr_anm=(rgb(255, 255, 220), rgb(255, 190, 40)), scl=.55, life=16,
         gen=2, emtr_life=5, init_pos=1, radius=.9, vel=(.02, .02), scl_anm=(.3, 1.2, .4, 50, 160), alpha=(31, 31, 0))
    prop(b, rs, 1, life=1)
    out[CASHSPARK] = bytes(b)

    # Body Bag (Slam): a flying body slam - WHUMP - and a body bag zips up over them. BODIED.
    poses(BODYBAG, fxart.body_bag(), ONE_TO_ONE, 36)
    no_delay(BODYBAG, HOLD)
    b, rs = kit(SLAMDUST)
    tex(b, 0, fxart.slam_dust())
    prop(b, rs, 0, tex=0, clr=rgb(200, 180, 140), clr_anm=(rgb(240, 225, 200), rgb(150, 130, 100)), scl=.8,
         life=26, gen=6, emtr_life=2, init_pos=1, radius=.5, vel=(.12, 0), scl_anm=(.5, 1.3, 1.8, 60, 200),
         alpha=(28, 24, 0), air_resist=118)
    prop(b, rs, 1, life=1)
    out[SLAMDUST] = bytes(b)
    sign(BODIED, ["BODIED."], fill=(30, 30, 35, 255), text=(255, 255, 255, 255))

    # Beam Me Up (Waterfall): a hydrant under them blows its top - the water blasts them sky high
    b, rs = kit(GEYSER)
    tex(b, 1, fxart.street_hydrant())
    b, cap = mirrored(b, fxart.hydrant_bonnet(), flip=False)
    tex(b, 0, fxart.gush_drop())
    prop(b, rs, HYD, scl=1.1, life=84, scl_anm=(.3, 1.1, 1.0, 30, 255))
    mover(b, rs, CAP_OFF, 1.2, 7, tex=cap, scl=.7, life=30, flags_on=(1 << 14) | (1 << 12))   # gone off the top
    rot(b, rs, CAP_OFF, spin=0x1400)
    prop(b, rs, GUSH, tex=0, clr=rgb(110, 190, 255), clr_anm=(rgb(235, 250, 255), rgb(60, 150, 255)), scl=.6,
         life=22, gen=4, gen_intvl=1, emtr_life=40, axis=(0, 1, 0), vel=(.03, .6), gravity=(0, -.008, 0),
         alpha=(31, 31, 12), air_resist=128)
    prop(b, rs, 3, life=1)
    out[GEYSER] = bytes(b)
    b, rs = kit(SPLOSH)
    tex(b, 0, fxart.splash_glob())
    tex(b, 1, fxart.water_column())
    prop(b, rs, COLUMN, tex=1, clr=rgb(90, 170, 255), clr_anm=(rgb(170, 220, 255), rgb(50, 130, 240)), scl=.7,
         life=18, gen=1, gen_intvl=1, emtr_life=40, axis=(0, 1, 0), vel=(.004, .5), alpha=(20, 16, 0),
         scl_anm=(.7, 1.0, 1.3, 60, 200), air_resist=128)
    prop(b, rs, RAINBACK, tex=0, clr=rgb(110, 190, 255), clr_anm=(rgb(230, 248, 255), rgb(60, 150, 255)), scl=.3,
         life=30, gen=3, emtr_life=16, init_pos=1, radius=1.4, axis=(0, -1, 0), vel=(.03, .1),
         gravity=(0, -.015, 0), alpha=(31, 31, 0), air_resist=128)
    out[SPLOSH] = bytes(b)
    sign(BEAMUP, ["BEAM", "ME UP!"], fill=(60, 150, 255, 255), text=(255, 255, 255, 255))

    # Poke (Peck): a finger jabbing them in the chest - poke poke POKE. POKED.
    b, rs = kit(FINGER)
    tex(b, 1, fxart.pointing_hand())
    b, left = mirrored(b, fxart.pointing_hand())
    tex(b, 0, fxart.poke_lines())
    for res, t in ((FINGER_R, 1), (FINGER_L, left)):
        prop(b, rs, res, tex=t, scl=1.2, life=SWING_STEP)
    prop(b, rs, BOOP, tex=0, clr=rgb(255, 255, 255), clr_anm=(rgb(255, 255, 255), rgb(255, 230, 120)), scl=.7,
         life=8, scl_anm=(.4, 1.3, 1.0, 60, 255), alpha=(31, 31, 0))
    prop(b, rs, 3, life=1)
    out[FINGER] = bytes(b)
    sign(POKED, ["POKED!"], fill=(70, 110, 230, 255), text=(255, 255, 255, 255))

    # Duct Tape (Wrap): a roll of duct tape whips round and round them, strip after strip. TAPED UP!
    b, rs = kit(TAPEROLL)
    tex(b, 1, fxart.duct_tape_roll())
    b, strip = mirrored(b, fxart.duct_strip(), flip=False)
    prop(b, rs, ROLL9, scl=.8, life=SWING_STEP, flags_on=(1 << 14) | (1 << 12))
    rot(b, rs, ROLL9, spin=0x1800)
    for res, ang in ((STRIP_A, 0x0700), (STRIP_B, -0x0900)):
        prop(b, rs, res, tex=strip, scl=1.5, life=56, scl_anm=(1.4, 1.0, 1.0, 12, 255))
        rot(b, rs, res, init=ang)
    prop(b, rs, 0, life=1)
    out[TAPEROLL] = bytes(b)
    sign(TAPED, ["TAPED", "UP!"], fill=(150, 155, 165, 255), text=(255, 255, 255, 255))

    # Kevlar (Harden): the vest drops on - then bang, ping, ping - the rounds bounce right off. BULLET PROOF.
    poses(VEST, fxart.kevlar_vest(), ONE_TO_ONE, 54)
    no_delay(VEST, HOLD)
    b, rs = kit(RICO)
    tex(b, 0, fxart.ricochet())
    tex(b, 1, fxart.flat_slug())
    prop(b, rs, SPARKS9, tex=0, clr=rgb(255, 230, 90), clr_anm=(rgb(255, 255, 230), rgb(255, 150, 30)), scl=.75,
         life=8, scl_anm=(.4, 1.3, .8, 40, 160), alpha=(31, 31, 0))
    prop(b, rs, SLUGS, tex=1, clr=rgb(220, 170, 60), clr_anm=(rgb(255, 230, 140), rgb(190, 130, 40)), scl=.5,
         life=24, axis=(0, 1, 0), vel=(.05, .12), gravity=(0, -.014, 0), air_resist=128, flags_on=(1 << 14) | (1 << 12))
    rot(b, rs, SLUGS, spin=0x0900)
    out[RICO] = bytes(b)
    sign(BPROOF, ["BULLET", "PROOF"], fill=(40, 40, 50, 255), text=(255, 220, 60, 255))

    # Curse Out (Curse): they go OFF - #@&! - and every cuss costs a coin in the swear jar
    b, rs = kit(JAR)
    tex(b, 1, fxart.swear_jar())
    tex(b, 0, fxart.coin_disc())
    prop(b, rs, JAR1, scl=ONE_TO_ONE / 1.1, life=74, scl_anm=(.3, 1.1, 1.0, 30, 255))
    prop(b, rs, COIN_IN, tex=0, clr=rgb(255, 205, 50), clr_anm=(rgb(255, 245, 170), rgb(230, 170, 30)), scl=.45,
         life=10, axis=(0, -1, 0), vel=(0, .2), gravity=(0, -.02, 0), air_resist=128)
    for res in (2, 3):
        prop(b, rs, res, life=1)
    out[JAR] = bytes(b)
    b, rs = kit(CUSS)
    tex(b, 0, fxart.burst_sign(["#@&!"], fill=(210, 25, 30, 255), text=(255, 230, 60, 255)), 30)
    b, other = mirrored(b, fxart.burst_sign(["@#!%"], fill=(30, 30, 35, 255), text=(255, 80, 80, 255)), 30,
                        flip=False)
    prop(b, rs, 0, scl=SIGN_SCALE, life=14, scl_anm=SIGN_POP)
    prop(b, rs, 1, tex=other, scl=SIGN_SCALE, life=14, scl_anm=SIGN_POP)
    out[CUSS] = bytes(b)
    no_delay(CUSS, 1)

    # ---- set 10 --------------------------------------------------------------------------------------------
    def drops(b, rs, res, side, frm, aim, frames, hi, lo, scl, **edit):
        """A spray of tinted alpha shapes (tex 0) from frm (px from the attacker) at aim (px from the target)."""
        args = dict(tex=0, clr=lo, clr_anm=(hi, lo), scl=scl, emtr_life=16, gen=2, gen_intvl=1, radius=.15,
                    spread=.012, alpha=(31, 31, 20), scl_anm=(1.0, 1.0, 1.0, 0, 255), flick=0)
        args.update(edit)
        spray(b, rs, res, side, frm, aim, frames, **args)

    def held(b, rs, res_r, res_l, art, scl, life, **edit):
        """A prop held out towards the target: res_r points right (the player's), res_l is its mirror."""
        b, left = mirrored(b, art)
        tex(b, 1, art)
        for res, t in ((res_r, 1), (res_l, left)):
            prop(b, rs, res, tex=t, scl=scl, life=life, **edit)
        return b

    def drain(b, rs, res, side, frames, **edit):
        """Emitter res (at the target) sends its particles back across at the attacker."""
        dx, dy = TARGET_FROM_ATTACKER[side]
        d = math.hypot(dx, dy)
        args = dict(axis=(-dx / d, -dy / d, 0), vel=(.01, d * VEL_UNITS / 4096 / frames), life=frames + 2)
        args.update(edit)
        prop(b, rs, res, **args)

    POPIN = (.3, 1.1, 1.0, 30, 255)

    # Spit Stream (BubbleBeam): a PA speaker pumping the beat behind them, mic in hand, they SPIT BARS - spit
    # flying on every line - and the foe gets roasted. Literally.
    b, rs = kit(MIC)
    b = held(b, rs, MIC_R, MIC_L, fxart.microphone(), .9, 56, scl_anm=POPIN)
    tex(b, 0, fxart.spit_fleck())
    for res, sd, ang in ((SPIT_E, "player", 0), (SPIT_P, "enemy", 0x8000)):    # streaks pointing the way they fly
        drops(b, rs, res, sd, MOUTH_AT[sd], (0, 26), 10, rgb(255, 255, 255), rgb(200, 225, 240), .85, emtr_life=4,
              gen=2, spread=.015, radius=.15, alpha=(31, 31, 10))
        rot(b, rs, res, init=ang)
    out[MIC] = bytes(b)
    b, rs = kit(ROAST)
    tex(b, 0, fxart.roast_flame())
    tex(b, 1, fxart.eighth_notes())
    prop(b, rs, 0, tex=0, clr=rgb(255, 120, 20), clr_anm=(rgb(255, 240, 120), rgb(230, 50, 10)), scl=.5, life=16,
         gen=2, gen_intvl=2, emtr_life=24, init_pos=1, radius=.9, axis=(0, 1, 0), vel=(.01, .02),
         alpha=(31, 31, 0), scl_anm=(.4, 1.2, .6, 50, 160))
    prop(b, rs, NOTES10, tex=1, clr=rgb(255, 220, 60), clr_anm=(rgb(255, 255, 200), rgb(255, 120, 200)), scl=.55,
         life=24, gen=1, axis=(.3, 1, 0), vel=(.01, .03), alpha=(31, 31, 0), scl_anm=(.4, 1.1, 1.0, 50, 255))
    out[ROAST] = bytes(b)
    b, rs = kit(SPEAKER)
    tex(b, 0, fxart.pa_speaker(), 30)
    prop(b, rs, POP, scl=1.3, life=70, scl_anm=POPIN)
    prop(b, rs, 1, scl=1.3, life=6, scl_anm=(1.0, 1.12, 1.0, 90, 170))         # thump
    out[SPEAKER] = bytes(b)
    no_delay(SPEAKER, 1)

    # Sprinkler (Water Sport): summer on the block - a Super Soaker, the sprinkler dance, everybody gets wet
    b, rs = kit(SOAKER)
    b = held(b, rs, SOAKER_R, SOAKER_L, fxart.super_soaker(), 1.0, 60, scl_anm=POPIN)
    tex(b, 0, fxart.fizz_drop())
    for res, sd in ((SOAK_E, "player"), (SOAK_P, "enemy")):
        drops(b, rs, res, sd, SOAKER_TIP[sd], (0, 22), 14, rgb(230, 248, 255), rgb(70, 160, 255), .35, emtr_life=8,
              gen=3, spread=.04, radius=.1)
    out[SOAKER] = bytes(b)

    # Horn Blast (Horn Attack): the DJ drop - BWAAP, BWAAP, BWAAAAP - each blast blows them further back
    b, rs = kit(AIRHORN)
    b = held(b, rs, HORN_R, HORN_L, fxart.air_horn(), 1.0, 70, scl_anm=POPIN)
    tex(b, 0, fxart.blast_ring())
    for res, sd in ((RINGS_E, "player"), (RINGS_P, "enemy")):
        drops(b, rs, res, sd, HORN_TIP[sd], (0, 24), 8, rgb(255, 255, 255), rgb(255, 230, 120), .9, emtr_life=3,
              gen=1, spread=0, radius=0, alpha=(31, 28, 0), scl_anm=(.4, 1.2, 2.2, 0, 200))
    out[AIRHORN] = bytes(b)

    # Mud Pie (Mud Shot): a pie to the face - then they pull out the phone and film it. POSTED.
    b, rs = kit(PIE)
    tex(b, 1, fxart.mud_pie(), 24)
    tex(b, 0, fxart.mud_drip())
    thrown(b, rs, .8, 0x0300)
    prop(b, rs, MUDDRIP, tex=0, clr=rgb(110, 70, 35), clr_anm=(rgb(160, 110, 60), rgb(90, 55, 25)), scl=.35,
         life=24, emtr_life=30, gen=1, gen_intvl=3, init_pos=1, radius=.6, axis=(0, -1, 0), vel=(0, .02),
         alpha=(31, 31, 0))
    prop(b, rs, 0, life=1)
    out[PIE] = bytes(b)
    b, rs = kit(MUDSPLAT)
    tex(b, 0, fxart.mud_splat(), 30)
    b, phone = mirrored(b, fxart.phone_rec(), 24, flip=False)
    prop(b, rs, POP, scl=1.1, life=50, scl_anm=(.3, 1.15, 1.0, 25, 255))
    prop(b, rs, PHONE, tex=phone, scl=ONE_TO_ONE / 1.1, life=40, scl_anm=POPIN)
    out[MUDSPLAT] = bytes(b)
    no_delay(MUDSPLAT, PHONE)

    # Backhand (DoubleSlap, once per hit): the pimp hand - fur cuff, a gem ring on every finger
    poses(BACKHAND, fxart.pimp_hand(), 1.1, 8)
    no_delay(BACKHAND, HOLD)
    b, rs = kit(SLAPSTAR)
    tex(b, 0, fxart.impact_ring())
    prop(b, rs, 0, tex=0, clr=rgb(255, 230, 80), clr_anm=(rgb(255, 255, 255), rgb(255, 170, 40)), scl=.9, life=10,
         scl_anm=(.4, 1.4, 1.8, 60, 200), alpha=(31, 31, 0))
    prop(b, rs, 1, life=1)
    out[SLAPSTAR] = bytes(b)

    # Battery Acid (Acid): they lick a 9-volt to check it - ZAP - then chuck it at them. Acid everywhere. TSSSS!
    b, rs = kit(NINEVOLT)
    tex(b, 1, fxart.nine_volt(), 24)
    tex(b, 0, fxart.acid_glob())
    thrown(b, rs, 1.0, 0)                                                     # no spin: the 9V stays readable
    prop(b, rs, FIZZ, tex=0, clr=rgb(140, 255, 60), clr_anm=(rgb(230, 255, 200), rgb(90, 200, 30)), scl=.4,
         life=18, emtr_life=30, gen=1, gen_intvl=2, init_pos=1, radius=.9, axis=(0, 1, 0), vel=(.01, .02),
         alpha=(31, 31, 0), scl_anm=(.3, 1.2, 1.4, 60, 200))
    prop(b, rs, 0, life=1)
    out[NINEVOLT] = bytes(b)
    b, rs = kit(ACIDSPLAT)
    tex(b, 0, fxart.acid_splat(), 30)
    b, nine = mirrored(b, fxart.nine_volt_lick(), 24, flip=False)
    prop(b, rs, POP, scl=1.15, life=46, scl_anm=(.3, 1.15, 1.0, 25, 255))
    prop(b, rs, HELD9V, tex=nine, scl=ONE_TO_ONE, life=24)
    out[ACIDSPLAT] = bytes(b)
    no_delay(ACIDSPLAT, HELD9V)

    # Fire Hose (Hydro Pump): the hose gets away from them - whipping round like a snake, soaking THEM - then
    # they wrestle it onto the foe and blast them clean across. HOSED!
    b, rs = kit(FIREHOSE)
    tex(b, 1, fxart.hose_nozzle())
    tex(b, 0, fxart.fizz_drop())
    prop(b, rs, NOZ_SPIN, scl=1.1, life=4, flags_on=(1 << 14) | (1 << 12))
    rot(b, rs, NOZ_SPIN, spin=0x2400)
    prop(b, rs, WILD, tex=0, clr=rgb(70, 160, 255), clr_anm=(rgb(230, 248, 255), rgb(60, 150, 255)), scl=.45,
         life=18, gen=3, emtr_life=4, init_pos=0, vel=(.3, 0), alpha=(31, 31, 0), air_resist=124)
    for res, sd in ((HOSE_E, "player"), (HOSE_P, "enemy")):
        drops(b, rs, res, sd, NOZ_TIP[sd], (0, 20), 10, rgb(235, 250, 255), rgb(60, 150, 255), .55, emtr_life=30,
              gen=4, spread=.03, radius=.3, alpha=(31, 28, 12))
    out[FIREHOSE] = bytes(b)
    b, rs = kit(WETHIT)
    tex(b, 0, fxart.fizz_drop())
    for res, gen, scl in ((0, 6, .35), (1, 3, .55)):
        prop(b, rs, res, tex=0, clr=rgb(90, 170, 255), clr_anm=(rgb(230, 248, 255), rgb(60, 150, 255)), scl=scl,
             life=18, gen=gen, emtr_life=24, gen_intvl=2, init_pos=1, radius=.5, axis=(0, 1, 0), vel=(.18, .1),
             gravity=(0, -.02, 0), alpha=(31, 31, 0), air_resist=124)
    out[WETHIT] = bytes(b)

    # Rise n Slap (Wake-Up Slap): the alarm clock rattling over them... then Mama's chancla comes flying in
    b, rs = kit(ALARMCLK)
    tex(b, 1, fxart.alarm_clock())
    tex(b, 0, fxart.ring_lines())
    for res, ang in ((CLOCK_A, 0x0600), (CLOCK_B, -0x0600)):
        prop(b, rs, res, scl=.9, life=4)
        rot(b, rs, res, init=ang)
    prop(b, rs, RINGING, tex=0, clr=rgb(255, 255, 255), clr_anm=(rgb(255, 255, 255), rgb(255, 230, 100)),
         scl=1.0, life=4)
    prop(b, rs, 3, life=1)
    out[ALARMCLK] = bytes(b)
    b, rs = kit(CHANCLA)
    tex(b, 0, fxart.chancla(), 30)
    for res, vx in ((FLY_E, -CHANCLA_SPEED), (FLY_P, CHANCLA_SPEED)):          # thrown in from off-screen
        mover(b, rs, res, vx, -1.5, scl=1.0, life=CHANCLA_FRAMES, flags_on=(1 << 14) | (1 << 12))
        rot(b, rs, res, spin=0x1800)
    out[CHANCLA] = bytes(b)
    no_delay(CHANCLA, FLY_P)

    # Dirty Shiv (Poison Jab): a commissary spoon filed into a shank, flies buzzing - shanked. TETANUS!
    b, rs = kit(SPOON)
    b = held(b, rs, SPOON_R, SPOON_L, fxart.shank_spoon(), 1.0, SWING_STEP)
    tex(b, 0, fxart.fly_bug())
    prop(b, rs, FLIES, tex=0, clr=rgb(40, 40, 40), clr_anm=(rgb(70, 70, 70), rgb(20, 20, 20)), scl=.35, life=30,
         gen=1, gen_intvl=3, emtr_life=24, init_pos=1, radius=1.0, vel=(.04, 0), alpha=(31, 31, 0), air_resist=120)
    prop(b, rs, 3, life=1)
    out[SPOON] = bytes(b)

    # Salt Water (Brine): a giant salt shaker over them - shake shake shake - salt in the wound. SALTY.
    b, rs = kit(SHAKER)
    tex(b, 1, fxart.salt_shaker())
    tex(b, 0, fxart.salt_grains())
    prop(b, rs, SHAKE_UP, scl=1.1, life=SWING_STEP)
    for res, ang in ((SHAKE_A, 0x7000), (SHAKE_B, -0x7000 & 0xFFFF)):          # upside down, waggling
        prop(b, rs, res, scl=1.1, life=4)
        rot(b, rs, res, init=ang)
    prop(b, rs, SALT, tex=0, clr=rgb(255, 255, 255), clr_anm=(rgb(255, 255, 255), rgb(220, 225, 235)), scl=.5,
         life=20, gen=2, emtr_life=4, init_pos=1, radius=.25, axis=(0, -1, 0), vel=(.02, .12),
         gravity=(0, -.01, 0), alpha=(31, 31, 0), air_resist=128)
    out[SHAKER] = bytes(b)
    sign(SALTY, ["SALTY."], fill=(240, 240, 245, 255), text=(60, 120, 220, 255))

    # Dirty Nails (Toxic Spikes): a handful of long glittery press-on acrylics flung all over their side
    b, rs = kit(NAILS)
    tex(b, 0, fxart.acrylic_nail())
    tex(b, 1, fxart.glitter_tall())
    prop(b, rs, NAILS1, tex=0, clr=rgb(255, 80, 180), clr_anm=(rgb(255, 200, 235), rgb(230, 40, 150)), scl=.55,
         life=56, gen=10, init_pos=1, radius=1.0, alpha=(31, 31, 31), scl_anm=(.2, 1.1, 1.0, 40, 255))
    prop(b, rs, GLITTER, tex=1, clr=rgb(255, 230, 120), clr_anm=(rgb(255, 255, 255), rgb(255, 120, 220)), scl=.6,
         life=14, gen=1, gen_intvl=3, emtr_life=40, init_pos=1, radius=1.4, alpha=(31, 31, 0))
    out[NAILS] = bytes(b)

    # The Boot (Stun Spore): the parking boot, clamped right on them - CLANK - they ain't going nowhere. BOOTED!
    poses(BOOT, fxart.parking_boot(), 1.15, 50)
    no_delay(BOOT, HOLD)

    # Gutter Slop (Sludge): a raccoon pops out of the dumpster next to them and hurls trash juice. EWWW!
    b, rs = kit(DUMPSTER)
    tex(b, 1, fxart.dumpster())
    b, coon = mirrored(b, fxart.raccoon(), flip=False)
    tex(b, 0, fxart.stink_lines())
    prop(b, rs, DUMP, scl=1.1, life=64, scl_anm=POPIN)
    prop(b, rs, COON, tex=coon, scl=.9, life=40, scl_anm=(.2, 1.15, 1.0, 60, 255))
    prop(b, rs, STINK, tex=0, clr=rgb(150, 170, 60), clr_anm=(rgb(210, 230, 140), rgb(110, 130, 40)), scl=.6,
         life=24, gen=1, gen_intvl=4, emtr_life=40, init_pos=1, radius=.6, axis=(0, 1, 0), vel=(.004, .02),
         alpha=(31, 31, 0))
    prop(b, rs, 3, life=1)
    out[DUMPSTER] = bytes(b)
    b, rs = kit(SLOPBALL)
    tex(b, 1, fxart.slop_ball(), 24)
    tex(b, 0, fxart.mud_drip())
    thrown(b, rs, .85, 0x0500)
    prop(b, rs, SLOPDRIP, tex=0, clr=rgb(110, 115, 45), clr_anm=(rgb(160, 165, 80), rgb(80, 85, 30)), scl=.4,
         life=24, emtr_life=30, gen=1, gen_intvl=2, init_pos=1, radius=.8, axis=(0, -1, 0), vel=(0, .02),
         alpha=(31, 31, 0))
    prop(b, rs, 0, life=1)
    out[SLOPBALL] = bytes(b)

    # Pebble Spray (Rock Blast, once per hit): a pebble at their window, 2am. YOU UP?
    b, rs = kit(PEBBLE)
    tex(b, 1, fxart.rock_chunk(), 24)
    tex(b, 0, fxart.impact_ring())
    thrown(b, rs, .5, 0x0800)
    prop(b, rs, PING, tex=0, clr=rgb(255, 255, 200), clr_anm=(rgb(255, 255, 255), rgb(255, 220, 80)), scl=.6, life=8,
         scl_anm=(.4, 1.3, 1.6, 60, 200), alpha=(31, 31, 0))
    prop(b, rs, 0, life=1)
    out[PEBBLE] = bytes(b)
    sign(YOUUP, ["YOU UP?"], fill=(70, 50, 150, 255), text=(255, 230, 120, 255))

    # Live Socket (Discharge): six cords in one outlet - crackle - ZAP - BLACKOUT. Who ain't pay the lights?!
    b, rs = kit(OUTLET)
    tex(b, 1, fxart.outlet_cords())
    tex(b, 0, fxart.crackle())
    prop(b, rs, OUTLET1, scl=1.1, life=70, scl_anm=POPIN)
    prop(b, rs, CRACKLES, tex=0, clr=rgb(255, 240, 80), clr_anm=(rgb(255, 255, 255), rgb(120, 220, 255)), scl=.5,
         life=4, gen=1, init_pos=1, radius=.7, alpha=(31, 31, 31))
    for res in (2, 3):
        prop(b, rs, res, life=1)
    out[OUTLET] = bytes(b)
    b, rs = kit(ZAPRING)
    tex(b, 0, fxart.zap_ring())
    prop(b, rs, RING_BIG, tex=0, clr=rgb(255, 240, 80), clr_anm=(rgb(255, 255, 255), rgb(120, 220, 255)), scl=1.2,
         life=16, scl_anm=(.2, 2.6, 3.6, 120, 200), alpha=(31, 28, 0))
    prop(b, rs, RING_SMALL, tex=0, clr=rgb(255, 240, 80), clr_anm=(rgb(255, 255, 255), rgb(255, 230, 60)), scl=.6,
         life=10, gen=2, emtr_life=8, gen_intvl=2, init_pos=1, radius=.8, scl_anm=(.3, 1.2, 1.4, 60, 200),
         alpha=(31, 31, 0))
    out[ZAPRING] = bytes(b)
    sign(PAYLIGHTS, ["PAY THE", "LIGHTS!"], fill=(40, 40, 50, 255), text=(255, 230, 60, 255))

    # Fetal Pos. (Defense Curl): post-breakup. Under the blankie with a pint of ice cream, a rain cloud overhead
    poses(BLANKIE, fxart.sad_blankie(), 1.3, 44)
    no_delay(BLANKIE, HOLD)
    b, rs = kit(RAINCLOUD)
    tex(b, 1, fxart.rain_cloud())
    tex(b, 0, fxart.raindrop())
    prop(b, rs, CLOUD, scl=1.0, life=60, scl_anm=POPIN)
    prop(b, rs, RAIN, tex=0, clr=rgb(110, 160, 255), clr_anm=(rgb(220, 235, 255), rgb(90, 140, 240)), scl=.45,
         life=14, gen=2, gen_intvl=2, emtr_life=44, init_pos=1, radius=.5, axis=(0, -1, 0), vel=(0, .18),
         alpha=(31, 31, 0))
    for res in (2, 3):
        prop(b, rs, res, life=1)
    out[RAINCLOUD] = bytes(b)

    # Choke Hold (Constrict): a spiked choke-collar snapped round their neck - the leash yanks them, three
    # times. LEASHED!
    b, rs = kit(HEADLOCK)
    b = held(b, rs, COLLAR_L, COLLAR_R, fxart.choke_collar(), 1.1, 56, scl_anm=(1.6, 1.0, 1.0, 20, 255))
    tex(b, 0, fxart.gasp_puff())
    prop(b, rs, GASP, tex=0, clr=rgb(235, 240, 255), clr_anm=(rgb(255, 255, 255), rgb(190, 200, 220)), scl=.45,
         life=14, axis=(0, 1, 0), vel=(.01, .02), alpha=(31, 31, 0), scl_anm=(.4, 1.2, 1.4, 60, 200))
    prop(b, rs, 3, life=1)
    out[HEADLOCK] = bytes(b)

    # Tornado (Twister): a trash tornado touches down on them - and auntie goes round in it, still in her
    # lawn chair, unbothered
    b, rs = kit(FUNNEL)
    b = held(b, rs, TWIST_A, TWIST_B, fxart.trash_tornado(), 1.5, 4)          # flipped back and forth: spinning
    b, auntie = mirrored(b, fxart.auntie_chair(), flip=False)
    tex(b, 0, fxart.trash_bit())
    prop(b, rs, AUNTIE, tex=auntie, scl=.75, life=4)
    prop(b, rs, DEBRIS, tex=0, clr=rgb(200, 60, 50), clr_anm=(rgb(240, 240, 230), rgb(150, 150, 160)), scl=.4,
         life=16, gen=2, gen_intvl=2, emtr_life=40, init_pos=1, radius=1.3, axis=(0, 1, 0), vel=(.08, .04),
         alpha=(31, 31, 0), air_resist=122, flags_on=(1 << 14) | (1 << 12))
    rot(b, rs, DEBRIS, spin=0x1400)
    out[FUNNEL] = bytes(b)

    # Kaboom (Explosion): foil in the microwave. Sparks... ding... KABOOM. WHO DID THIS?!
    b, rs = kit(MICRO)
    tex(b, 1, fxart.microwave())
    tex(b, 0, fxart.crackle())
    prop(b, rs, MICRO1, scl=ONE_TO_ONE / 1.1, life=50, scl_anm=(.3, 1.1, 1.0, 30, 255))
    prop(b, rs, ARCS, tex=0, clr=rgb(120, 220, 255), clr_anm=(rgb(255, 255, 255), rgb(90, 180, 255)), scl=.4,
         life=4, gen=2, init_pos=1, radius=.3, alpha=(31, 31, 31))
    for res in (2, 3):
        prop(b, rs, res, life=1)
    out[MICRO] = bytes(b)
    b, rs = kit(BOOMCLOUD)
    tex(b, 0, fxart.kaboom_cloud(), 30)
    prop(b, rs, POP, scl=2.4, life=26, scl_anm=(.2, 1.1, 1.3, 50, 160), alpha=(31, 31, 0))
    prop(b, rs, 1, scl=1.5, life=20, scl_anm=(.2, 1.2, 1.4, 40, 150), alpha=(31, 31, 0))
    out[BOOMCLOUD] = bytes(b)
    no_delay(BOOMCLOUD, 1)

    # Jumpscare (Astonish): lights out... a process server bursts out of the bush with the papers. SERVED!
    b, rs = kit(SERVER)
    tex(b, 0, fxart.process_server(), 30)
    prop(b, rs, POP, scl=1.9, life=36, scl_anm=(.4, 1.1, 1.0, 120, 255))
    prop(b, rs, 1, life=1)
    out[SERVER] = bytes(b)

    # IRS Audit (Giga Drain): the magnifying glass, the AUDIT folder, receipts flying back - and their wallet,
    # empty, a moth flying out
    b, rs = kit(AUDIT)
    tex(b, 1, fxart.magnifier())
    b, folder = mirrored(b, fxart.audit_folder(), 24, flip=False)
    tex(b, 0, fxart.receipt())
    prop(b, rs, GLASS, scl=1.0, life=SWING_STEP)
    prop(b, rs, FOLDER, tex=folder, scl=SIGN_SCALE, life=34, scl_anm=(1.6, 1.0, 1.0, 20, 255))
    for res, sd in ((RECEIPTS_E, "player"), (RECEIPTS_P, "enemy")):
        drain(b, rs, res, sd, 18, tex=0, clr=rgb(255, 255, 255), clr_anm=(rgb(255, 255, 255), rgb(150, 255, 150)),
              scl=.5, gen=1, gen_intvl=2, emtr_life=18, init_pos=1, radius=.5, alpha=(31, 31, 20),
              flags_on=(1 << 14) | (1 << 12))
        rot(b, rs, res, spin=0x0600)
    out[AUDIT] = bytes(b)
    b, rs = kit(WALLET)
    tex(b, 0, fxart.empty_wallet(), 30)
    prop(b, rs, POP, scl=1.0, life=36, scl_anm=POPIN)
    prop(b, rs, 1, life=1)
    out[WALLET] = bytes(b)

    # Beat the Box (Belly Drum): the bucket drummer - sticks flying on an upside-down paint bucket, tips
    # raining in - till it costs them. MAXED OUT.
    b, rs = kit(BUCKET)
    tex(b, 1, fxart.paint_bucket())
    b, sticks = mirrored(b, fxart.drumsticks(), 16, flip=False)
    tex(b, 0, fxart.box_dust())
    prop(b, rs, BUCKET1, scl=1.0, life=64, scl_anm=POPIN)
    for res, ang in ((STICKS_UP, 0x1C00), (STICKS_DN, -0x0400 & 0xFFFF)):
        prop(b, rs, res, tex=sticks, scl=.9, life=4)
        rot(b, rs, res, init=ang)
    prop(b, rs, BUCKPUFF, tex=0, clr=rgb(255, 200, 120), clr_anm=(rgb(255, 255, 220), rgb(255, 150, 60)), scl=.45,
         life=10, gen=2, init_pos=1, radius=.3, vel=(.03, 0), alpha=(31, 26, 0), scl_anm=(.4, 1.2, 1.5, 60, 200))
    out[BUCKET] = bytes(b)
    b, rs = kit(TIPS)
    tex(b, 0, fxart.dollar_fold())
    prop(b, rs, 0, tex=0, clr=rgb(110, 200, 100), clr_anm=(rgb(200, 255, 190), rgb(60, 150, 60)), scl=.5, life=30,
         gen=1, gen_intvl=3, emtr_life=30, init_pos=1, radius=1.2, axis=(0, -1, 0), vel=(.01, .08),
         alpha=(31, 31, 0), flags_on=(1 << 14) | (1 << 12))
    rot(b, rs, 0, spin=0x0500)
    prop(b, rs, 1, life=1)
    out[TIPS] = bytes(b)

    # Stink Bomb (Sludge Bomb): they kick off a sneaker at them - and the foot funk wipes the foe out. PEE-YEW!
    b, rs = kit(SHOE)
    tex(b, 1, fxart.busted_sneaker(), 24)
    tex(b, 0, fxart.stink_puff())
    thrown(b, rs, .9, 0x0900)
    prop(b, rs, FUMES, tex=0, clr=rgb(150, 210, 60), clr_anm=(rgb(210, 250, 150), rgb(110, 160, 40)), scl=.6,
         life=30, gen=1, gen_intvl=3, emtr_life=30, init_pos=1, radius=1.2, axis=(0, 1, 0), vel=(.01, .012),
         alpha=(24, 20, 0), scl_anm=(.5, 1.2, 1.6, 60, 200))
    prop(b, rs, 0, life=1)
    out[SHOE] = bytes(b)
    b, rs = kit(STINKCLOUD)
    tex(b, 0, fxart.stink_puff())
    tex(b, 1, fxart.stench_wave())
    prop(b, rs, CLOUD10, tex=0, clr=rgb(140, 200, 50), clr_anm=(rgb(200, 245, 140), rgb(100, 150, 30)), scl=1.0,
         life=30, gen=6, emtr_life=2, init_pos=1, radius=.8, vel=(.05, 0), alpha=(26, 22, 0),
         scl_anm=(.4, 1.3, 1.8, 60, 200), air_resist=118)
    prop(b, rs, STENCH, tex=1, clr=rgb(120, 180, 40), clr_anm=(rgb(190, 240, 120), rgb(90, 140, 20)), scl=.6,
         life=22, gen=1, gen_intvl=4, emtr_life=40, init_pos=1, radius=.8, axis=(0, 1, 0), vel=(.004, .02),
         alpha=(31, 31, 0))
    out[STINKCLOUD] = bytes(b)

    # Kamikaze (Double-Edge): a dirt bike, front wheel up, straight into them - both of them eat it. YOLO!
    b, rs = kit(DIRTBIKE)
    tex(b, 0, fxart.speed_streak())
    b, left = mirrored(b, fxart.dirt_bike())
    tex(b, 1, fxart.dirt_bike())
    for res, t, sx in ((BIKE_R, 1, 1), (BIKE_L, left, -1)):                    # wheelie, riding along under them
        mover(b, rs, res, sx * CART_RUN[0] / CART_LIFE, sx * CART_RUN[1] / CART_LIFE, tex=t, scl=1.2,
              life=CART_LIFE - 2)
        rot(b, rs, res, init=sx * 0x0A00)
    mover(b, rs, BIKE_FLY, 1.5, 5, scl=1.2, life=30, flags_on=(1 << 14) | (1 << 12))      # flying off
    rot(b, rs, BIKE_FLY, spin=0x0C00)
    prop(b, rs, STREAKS, tex=0, clr=rgb(255, 255, 255), clr_anm=(rgb(255, 255, 255), rgb(255, 230, 150)), scl=.7,
         life=8, alpha=(31, 31, 0))
    out[DIRTBIKE] = bytes(b)

    # Splash Whip (Aqua Tail): they pull off a wet durag and snap them with the tail. SNAP!
    b, rs = kit(DURAG)
    b = held(b, rs, DURAG_R, DURAG_L, fxart.durag(), 1.3, 10, scl_anm=(.6, 1.05, 1.0, 120, 255))
    tex(b, 0, fxart.water_flick())
    prop(b, rs, FLICK, tex=0, clr=rgb(110, 190, 255), clr_anm=(rgb(230, 248, 255), rgb(60, 150, 255)), scl=.5,
         life=14, gen=4, init_pos=1, radius=.3, vel=(.08, 0), gravity=(0, -.01, 0), alpha=(31, 31, 0))
    prop(b, rs, 3, life=1)
    out[DURAG] = bytes(b)

    # Didnt See It (Amnesia): "WHO DID IT?" - lips zipped, shades on, whistling. Ain't see nothin'.
    b, rs = kit(ZIPPED)
    tex(b, 0, fxart.shades_zip(), 24)
    b, who = mirrored(b, fxart.who_bubble(), 8, flip=False)
    prop(b, rs, POP, scl=ONE_TO_ONE, life=50, scl_anm=(1.5, 1.0, 1.0, 20, 255))
    prop(b, rs, 1, tex=who, scl=SIGN_SCALE, life=26, scl_anm=SIGN_POP)
    out[ZIPPED] = bytes(b)
    no_delay(ZIPPED, 1)

    # Nap (Rest): a heaping plate of soul food... gone in seconds... and they're out cold. THE ITIS.
    b, rs = kit(SOULFOOD)
    tex(b, 1, fxart.soul_plate())
    tex(b, 0, fxart.nap_z())
    prop(b, rs, PLATE, scl=1.1, life=18, scl_anm=POPIN)
    prop(b, rs, PLATE_GONE, scl=1.1, life=26, scl_anm=(1.0, 1.0, .1, 0, 60))   # ...demolished
    prop(b, rs, ZEES, tex=0, clr=rgb(150, 170, 255), clr_anm=(rgb(230, 235, 255), rgb(110, 120, 255)), scl=.55,
         life=28, gen=1, gen_intvl=8, emtr_life=40, axis=(.5, 1, 0), vel=(0, .02), alpha=(31, 31, 0),
         scl_anm=(.4, 1.2, 1.0, 50, 255))
    prop(b, rs, 3, life=1)
    out[SOULFOOD] = bytes(b)

    # Chase Down (Pursuit): the Feds' helicopter spotlight finds them... then a flying tackle. GOTCHA!
    b, rs = kit(CHOPPER)
    tex(b, 1, fxart.helicopter())
    b, beam = mirrored(b, fxart.spotlight(), 16, flip=False)
    prop(b, rs, HELI, scl=ONE_TO_ONE, life=56)
    prop(b, rs, SPOT, tex=beam, scl=1.6, life=50, scl_anm=(.2, 1.0, 1.0, 40, 255))
    for res in (0, 3):
        prop(b, rs, res, life=1)
    out[CHOPPER] = bytes(b)
    b, rs = kit(DASHDUST)
    tex(b, 0, fxart.speed_streak())
    prop(b, rs, 0, tex=0, clr=rgb(255, 255, 255), clr_anm=(rgb(255, 255, 255), rgb(220, 220, 230)), scl=.8,
         life=10, gen=2, emtr_life=6, gen_intvl=1, init_pos=1, radius=.5, alpha=(31, 31, 0))
    prop(b, rs, 1, life=1)
    out[DASHDUST] = bytes(b)

    # Paper Cut (Air Slash): a flurry of PAST DUE bills - fwip fwip fwip - paper cuts. OWWW!
    b, rs = kit(BILLS10)
    tex(b, 1, fxart.past_due())
    tex(b, 0, fxart.cut_mark())
    for res, sd in ((BILLS_E, "player"), (BILLS_P, "enemy")):                    # flat, not spinning: it reads
        spray(b, rs, res, sd, (24 if sd == "player" else -24, 26), (0, 24), 12, clr=white, clr_anm=(white, white),
              scl=ONE_TO_ONE, gen=1, gen_intvl=4, emtr_life=13, radius=.3, spread=.01, alpha=(31, 31, 31),
              scl_anm=(1.0, 1.0, 1.0, 0, 255))
    prop(b, rs, CUTS, tex=0, clr=rgb(230, 30, 40), clr_anm=(rgb(255, 120, 120), rgb(200, 20, 30)), scl=.6, life=16,
         alpha=(31, 31, 0), scl_anm=(.3, 1.2, 1.0, 80, 255))
    prop(b, rs, 1, life=1)
    out[BILLS10] = bytes(b)

    # Pepper Spray (PoisonPowder): pssssht, right in the eyes - tears - and somebody dumps the milk on them
    b, rs = kit(PEPPER)
    b = held(b, rs, CAN_R, CAN_L, fxart.pepper_can(), .9, 44, scl_anm=POPIN)
    tex(b, 0, fxart.pepper_mist())
    for res, sd in ((MIST_E, "player"), (MIST_P, "enemy")):
        drops(b, rs, res, sd, PEPPER_TIP[sd], (0, 28), 12, rgb(255, 200, 120), rgb(240, 110, 30), .55, emtr_life=16,
              gen=3, spread=.03, radius=.2, alpha=(26, 22, 0), scl_anm=(.4, 1.0, 1.8, 0, 200))
    out[PEPPER] = bytes(b)
    b, rs = kit(MILK)
    tex(b, 1, fxart.milk_carton())
    tex(b, 0, fxart.raindrop())
    prop(b, rs, JUG_UP, scl=1.0, life=SWING_STEP)
    prop(b, rs, JUG_TIP, scl=1.0, life=30)
    rot(b, rs, JUG_TIP, init=0x6000)
    prop(b, rs, MILKPOUR, tex=0, clr=rgb(255, 255, 255), clr_anm=(rgb(255, 255, 255), rgb(225, 230, 240)), scl=.55,
         life=14, gen=3, gen_intvl=1, emtr_life=24, axis=(0, -1, 0), vel=(.02, .25), gravity=(0, -.02, 0),
         alpha=(31, 31, 10))
    prop(b, rs, TEARS3, tex=0, clr=rgb(110, 180, 255), clr_anm=(rgb(220, 240, 255), rgb(80, 150, 255)), scl=.4,
         life=10, gen=2, emtr_life=24, gen_intvl=3, init_pos=1, radius=.4, axis=(0, -1, 0), vel=(.02, .1),
         alpha=(31, 31, 0))
    out[MILK] = bytes(b)
    SET10_82 = [MIC, SOAKER, AIRHORN, FIREHOSE, ALARMCLK, SPOON, SHAKER, DUMPSTER, OUTLET, RAINCLOUD, HEADLOCK, FUNNEL,
                MICRO, AUDIT, BUCKET, DIRTBIKE, DURAG, SOULFOOD, CHOPPER, BILLS10, PEPPER, MILK]
    # ---- set 11 --------------------------------------------------------------------------------------------
    def added(b, art, colors=24):
        """Append art (unflipped) as a new texture; returns (b, its index)."""
        return mirrored(b, art, colors, flip=False)

    # Belly Flop (Body Slam): a diving board pops up - boing, boing, BOING - a full belly flop onto them, and
    # a wall of water explodes up off the floor
    b, rs = kit(BOARD)
    b = held(b, rs, BOARD_R, BOARD_L, fxart.diving_board(), 1.2, 64, scl_anm=POPIN)
    tex(b, 0, fxart.fizz_drop())
    prop(b, rs, FLOPDROPS, tex=0, clr=rgb(90, 170, 255), clr_anm=(rgb(230, 248, 255), rgb(60, 150, 255)), scl=.45,
         life=26, gen=14, init_pos=1, radius=.8, axis=(0, 1, 0), vel=(.22, .3), gravity=(0, -.025, 0),
         alpha=(31, 31, 0), air_resist=126)
    prop(b, rs, 3, life=1)
    out[BOARD] = bytes(b)
    b, rs = kit(BIGSPLASH)
    tex(b, 0, fxart.splash_crown_big(), 30)
    prop(b, rs, POP, scl=1.9, life=24, scl_anm=(.3, 1.1, 1.15, 40, 180), alpha=(31, 31, 0))
    prop(b, rs, 1, scl=1.3, life=18, scl_anm=(.3, 1.1, 1.2, 40, 160), alpha=(31, 31, 0))
    out[BIGSPLASH] = bytes(b)
    no_delay(BIGSPLASH, 1)

    # Pigeon Drop (Mud Bomb): a fat city pigeon flaps over... stops right above them... looks down... SPLAT
    b, rs = kit(PIGEON)
    tex(b, 1, fxart.pigeon())
    b, down = added(b, fxart.pigeon(wings_up=False), 32)
    tex(b, 0, fxart.glob_drop())
    prop(b, rs, WINGS_UP, scl=1.0, life=4)
    prop(b, rs, WINGS_DN, tex=down, scl=1.0, life=4)
    prop(b, rs, GLOB, tex=0, clr=rgb(250, 250, 245), clr_anm=(rgb(255, 255, 255), rgb(225, 225, 215)), scl=.6,
         life=12, axis=(0, -1, 0), vel=(0, .05), gravity=(0, -.03, 0), alpha=(31, 31, 31), air_resist=128)
    prop(b, rs, 3, life=1)
    out[PIGEON] = bytes(b)
    b, rs = kit(POOPSPLAT)
    tex(b, 0, fxart.poop_splat(), 30)
    prop(b, rs, POP, scl=1.1, life=52, scl_anm=(.3, 1.15, 1.0, 40, 255))
    prop(b, rs, 1, life=1)
    out[POOPSPLAT] = bytes(b)

    # Heat Lamp (Sunny Day): beach chair, shades, the foil reflector under the chin - and the sun cranks it up
    b, rs = kit(TANNING)
    tex(b, 1, fxart.beach_chair())
    b, refl = added(b, fxart.tan_reflector(), 24)
    tex(b, 0, fxart.tiny_spark())
    prop(b, rs, CHAIR10, scl=1.3, life=80, scl_anm=POPIN)
    prop(b, rs, REFLECTOR, tex=refl, scl=.9, life=70, scl_anm=POPIN)
    prop(b, rs, GLARE, tex=0, clr=rgb(255, 255, 220), clr_anm=(rgb(255, 255, 255), rgb(255, 230, 120)), scl=.5,
         life=10, gen=1, gen_intvl=4, emtr_life=60, init_pos=1, radius=.6, alpha=(31, 31, 0),
         scl_anm=(.3, 1.3, .3, 60, 160))
    prop(b, rs, 3, life=1)
    out[TANNING] = bytes(b)
    b, rs = kit(SUN)
    tex(b, 0, fxart.cool_sun(), 30)
    prop(b, rs, POP, scl=1.5, life=80, scl_anm=(.2, 1.1, 1.0, 40, 255))
    prop(b, rs, 1, scl=1.5, life=8, scl_anm=(1.0, 1.15, 1.0, 90, 170))
    out[SUN] = bytes(b)
    no_delay(SUN, 1)
    b, rs = kit(HEAT)
    tex(b, 1, fxart.heat_wave())
    tex(b, 0, fxart.tiny_spark())
    prop(b, rs, WAVES10, tex=1, clr=rgb(255, 200, 120), clr_anm=(rgb(255, 245, 210), rgb(255, 150, 80)), scl=.7,
         life=24, gen=1, gen_intvl=3, emtr_life=56, init_pos=1, radius=1.6, axis=(0, 1, 0), vel=(.004, .015),
         alpha=(22, 18, 0))
    prop(b, rs, 0, life=1)
    out[HEAT] = bytes(b)

    # Grill Flash (Scary Face): a giant gold grill flashed right at them - the shine sweeps the screen, they
    # shield their eyes, sweating, backing up
    b, rs = kit(GRILL)
    tex(b, 1, fxart.grill_smile())
    b, ray = added(b, fxart.light_ray(), 16)
    tex(b, 0, fxart.tiny_spark())
    prop(b, rs, SMILE, scl=1.3, life=56, scl_anm=(.2, 1.1, 1.0, 50, 255))
    for res, ang in ((RAY_A, 0x1400), (RAY_B, -0x0C00 & 0xFFFF)):
        prop(b, rs, res, tex=ray, scl=2.4, life=6, alpha=(31, 31, 0))
        rot(b, rs, res, init=ang)
    prop(b, rs, TWINKLE, tex=0, clr=rgb(255, 255, 230), clr_anm=(rgb(255, 255, 255), rgb(255, 220, 80)), scl=.8,
         life=10, scl_anm=(.2, 1.6, .2, 60, 160), alpha=(31, 31, 0))
    out[GRILL] = bytes(b)
    b, rs = kit(SWEATY)
    tex(b, 0, fxart.sweat_bead())
    prop(b, rs, 0, tex=0, clr=rgb(140, 200, 255), clr_anm=(rgb(230, 245, 255), rgb(90, 160, 255)), scl=.45,
         life=20, gen=1, gen_intvl=4, emtr_life=40, init_pos=1, radius=.6, axis=(0, 1, 0), vel=(.04, .03),
         gravity=(0, -.006, 0), alpha=(31, 31, 0))
    prop(b, rs, 1, life=1)
    out[SWEATY] = bytes(b)

    # Trunk Rattle (SonicBoom): a car rolls up, trunk popped on a wall of subs - BOOM - the whole car jumps,
    # the bass rolls out in waves and shakes their feathers loose
    b, rs = kit(TRUNK)
    tex(b, 1, fxart.car_trunk_subs())
    tex(b, 0, fxart.bass_ring())
    prop(b, rs, CAR10, scl=1.6, life=4)
    for res, sd in ((BASS_E, "player"), (BASS_P, "enemy")):
        spray(b, rs, res, sd, (30, 34) if sd == "player" else (-40, 6), (0, 18), 14, tex=0, clr=rgb(200, 90, 255),
              clr_anm=(rgb(255, 220, 255), rgb(150, 60, 255)), scl=.9, gen=1, emtr_life=1, radius=0,
              alpha=(31, 26, 0), scl_anm=(.4, 1.3, 2.4, 0, 200))
    prop(b, rs, 2, life=1)
    out[TRUNK] = bytes(b)
    b, rs = kit(FEATHERS)
    tex(b, 0, fxart.feather())
    prop(b, rs, 0, tex=0, clr=rgb(220, 200, 170), clr_anm=(rgb(255, 250, 235), rgb(180, 150, 110)), scl=.55,
         life=40, gen=6, init_pos=1, radius=.6, axis=(0, 1, 0), vel=(.06, .03), gravity=(0, -.004, 0),
         alpha=(31, 31, 0), air_resist=118, flags_on=(1 << 14) | (1 << 12))
    rot(b, rs, 0, spin=0x0400)
    prop(b, rs, 1, life=1)
    out[FEATHERS] = bytes(b)

    # Exhaust (Smog): a beat-up hooptie backs up next to them... sputter, sputter... BANG - backfire, a wall of
    # black smoke in their face
    b, rs = kit(HOOPTIE)
    b = held(b, rs, HOOP_R, HOOP_L, fxart.hooptie_rear(), 1.3, 4)
    tex(b, 0, fxart.soot_puff())
    prop(b, rs, SPUTTER, tex=0, clr=rgb(70, 70, 75), clr_anm=(rgb(140, 140, 145), rgb(40, 40, 44)), scl=.45,
         life=16, gen=1, axis=(0, 1, 0), vel=(.02, .02), alpha=(28, 24, 0), scl_anm=(.5, 1.2, 1.6, 60, 200))
    prop(b, rs, 3, life=1)
    out[HOOPTIE] = bytes(b)
    b, rs = kit(SOOT)
    tex(b, 0, fxart.soot_puff())
    tex(b, 1, fxart.backfire())
    prop(b, rs, SOOTCLOUD, tex=0, clr=rgb(40, 40, 45), clr_anm=(rgb(110, 110, 115), rgb(20, 20, 24)), scl=1.0,
         life=40, gen=8, emtr_life=3, init_pos=1, radius=.6, vel=(.07, .01), alpha=(30, 26, 0),
         scl_anm=(.4, 1.3, 2.0, 60, 220), air_resist=116)
    prop(b, rs, BANG10, tex=1, clr=rgb(255, 160, 40), clr_anm=(rgb(255, 255, 200), rgb(255, 90, 20)), scl=.9,
         life=8, scl_anm=(.3, 1.4, 1.0, 80, 255), alpha=(31, 31, 0))
    out[SOOT] = bytes(b)

    # Riot Shield (Light Screen): a riot shield - FEDS crossed out, MINE in marker - and tomatoes start flying
    # in and splatting on it
    b, rs = kit(SHIELD)
    tex(b, 1, fxart.riot_shield())
    b, tom = added(b, fxart.tomato(), 24)
    tex(b, 0, fxart.tiny_spark())
    prop(b, rs, SHIELD1, scl=ONE_TO_ONE, life=70)
    for res, vx in ((TOM_E, -TOMATO_SPEED), (TOM_P, TOMATO_SPEED)):            # thrown in from the foe's side
        mover(b, rs, res, vx, 1.2, tex=tom, scl=.7, life=TOMATO_FRAMES, flags_on=(1 << 14) | (1 << 12))
        rot(b, rs, res, spin=0x0C00)
    prop(b, rs, PINGS10, tex=0, clr=rgb(255, 255, 230), clr_anm=(rgb(255, 255, 255), rgb(150, 210, 255)), scl=.6,
         life=8, gen=3, init_pos=1, radius=.3, vel=(.04, 0), alpha=(31, 31, 0))
    out[SHIELD] = bytes(b)
    b, rs = kit(TOMSPLAT)
    tex(b, 0, fxart.tomato_splat(), 30)
    prop(b, rs, POP, scl=.8, life=40, scl_anm=(.2, 1.15, 1.0, 60, 255))
    prop(b, rs, 1, life=1)
    out[TOMSPLAT] = bytes(b)

    # Full Bars (Signal Beam): phone up, no signal - they wander left, right, up on their toes... FULL BARS -
    # and the wifi blasts the foe
    b, rs = kit(PHONESIG)
    tex(b, 0, fxart.phone_signal(), 24)
    b, full = added(b, fxart.phone_signal(bars=4), 24)
    prop(b, rs, POP, scl=ONE_TO_ONE, life=4)
    prop(b, rs, 1, tex=full, scl=ONE_TO_ONE, life=40, scl_anm=(1.4, 1.0, 1.0, 20, 255))
    out[PHONESIG] = bytes(b)
    no_delay(PHONESIG, 1)
    b, rs = kit(WIFI)
    tex(b, 0, fxart.wifi_arc())
    for res, sd, ang in ((WIFI_E, "player", 0x1300), (WIFI_P, "enemy", 0x9300)):
        spray(b, rs, res, sd, PHONE_UP[sd], (0, 22), 14, tex=0, clr=rgb(80, 220, 255),
              clr_anm=(rgb(230, 255, 255), rgb(40, 160, 255)), scl=.9, gen=1, gen_intvl=3, emtr_life=18, radius=0,
              alpha=(31, 31, 0), scl_anm=(.6, 1.2, 1.8, 0, 200))
        rot(b, rs, res, init=ang)
    out[WIFI] = bytes(b)

    # Bulletproof (Reflect): the corner-store bulletproof glass slams down in front of them. The foe charges
    # it - BONK - slides down it, and the sign flips to SHUT
    b, rs = kit(STOREGLASS)
    tex(b, 0, fxart.store_glass(), 30)
    b, shut = added(b, fxart.store_glass(closed=True), 30)
    prop(b, rs, POP, scl=ONE_TO_ONE, life=SWING_STEP)
    prop(b, rs, 1, tex=shut, scl=ONE_TO_ONE, life=24)
    out[STOREGLASS] = bytes(b)
    no_delay(STOREGLASS, 1)
    b, rs = kit(GLASSFX)
    tex(b, 0, fxart.crack_star())
    prop(b, rs, 0, tex=0, clr=rgb(255, 255, 255), clr_anm=(rgb(255, 255, 255), rgb(190, 220, 255)), scl=.8,
         life=24, scl_anm=(.3, 1.2, 1.0, 80, 255), alpha=(31, 31, 0))
    prop(b, rs, 1, life=1)
    out[GLASSFX] = bytes(b)

    # Night Shift (Night Shade): night falls, the moon comes up, they clock in - then the janitor shift: mop,
    # WET FLOOR sign... and the foe wipes out on it
    b, rs = kit(CLOCKIN)
    tex(b, 1, fxart.punch_clock())
    b, moon = added(b, fxart.crescent_moon(), 16)
    tex(b, 0, fxart.tiny_spark())
    prop(b, rs, PCLOCK, scl=ONE_TO_ONE / 1.1, life=34, scl_anm=POPIN)
    prop(b, rs, MOON, tex=moon, scl=1.0, life=SWING_STEP)
    prop(b, rs, STARS10, tex=0, clr=rgb(255, 255, 200), clr_anm=(rgb(255, 255, 255), rgb(255, 230, 120)), scl=.4,
         life=60, gen=6, init_pos=1, radius=2.6, alpha=(31, 31, 0), scl_anm=(.3, 1.0, 1.0, 60, 255))
    prop(b, rs, MOON_UP, tex=moon, scl=1.0, life=70)
    out[CLOCKIN] = bytes(b)
    b, rs = kit(JANITOR)
    tex(b, 1, fxart.mop())
    b, wet = added(b, fxart.wet_floor_sign(), 16)
    tex(b, 0, fxart.puddle())
    for res, ang in ((MOP_A, 0x0C00), (MOP_B, -0x0800 & 0xFFFF)):
        prop(b, rs, res, scl=1.1, life=4)
        rot(b, rs, res, init=ang)
    prop(b, rs, WETSIGN, tex=wet, scl=ONE_TO_ONE / 1.1, life=50, scl_anm=POPIN)
    prop(b, rs, PUDDLE10, tex=0, clr=rgb(120, 190, 255), clr_anm=(rgb(220, 240, 255), rgb(90, 160, 255)), scl=1.4,
         life=50, alpha=(26, 26, 0), scl_anm=(.3, 1.0, 1.0, 40, 255))
    out[JANITOR] = bytes(b)

    # Wind Shank (Air Cutter): a cheap ceiling fan cranked to HIGH, wobbling harder and harder... the blades fly
    # off and slice right through them
    b, rs = kit(CFAN)
    tex(b, 1, fxart.ceiling_fan())
    b, turned = added(b, fxart.ceiling_fan(angle=45), 24)
    tex(b, 0, fxart.whoosh_arc())
    prop(b, rs, FAN_A, scl=1.3, life=4)
    prop(b, rs, FAN_B, tex=turned, scl=1.3, life=4)
    prop(b, rs, SWOOSH, tex=0, clr=rgb(230, 240, 255), clr_anm=(rgb(255, 255, 255), rgb(170, 200, 255)), scl=.9,
         life=8, alpha=(28, 24, 0), flags_on=(1 << 14) | (1 << 12))
    rot(b, rs, SWOOSH, spin=0x2000)
    prop(b, rs, 3, life=1)
    out[CFAN] = bytes(b)
    b, rs = kit(FANBLADES)
    b, blade = added(b, fxart.fan_blade(), 24)
    tex(b, 0, fxart.cut_mark())
    for res, sd in ((BLADES_E, "player"), (BLADES_P, "enemy")):
        spray(b, rs, res, sd, CFAN_AT[sd], (0, 22), 10, tex=blade, clr=white, clr_anm=(white, white), scl=.9, gen=1,
              gen_intvl=3, emtr_life=10, radius=.3, spread=.02, alpha=(31, 31, 31), scl_anm=(1.0, 1.0, 1.0, 0, 255),
              flags_on=(1 << 14) | (1 << 12))
        rot(b, rs, res, spin=0x3000)
    prop(b, rs, SLICES, tex=0, clr=rgb(230, 30, 40), clr_anm=(rgb(255, 140, 140), rgb(200, 20, 30)), scl=.8,
         life=14, alpha=(31, 31, 0), scl_anm=(.3, 1.3, 1.0, 80, 255))
    prop(b, rs, 1, life=1)
    out[FANBLADES] = bytes(b)

    # Spark Up (Spark): flick... flick... flick... nothing. Fourth flick - ZZZAP - lit up like a power line, and
    # they charge in crackling
    b, rs = kit(BIC)
    tex(b, 1, fxart.bic_lighter())
    tex(b, 0, fxart.tiny_spark())
    prop(b, rs, LIGHTER1, scl=.8, life=44, scl_anm=POPIN)
    prop(b, rs, FLICKS, tex=0, clr=rgb(255, 220, 80), clr_anm=(rgb(255, 255, 255), rgb(255, 150, 40)), scl=.4,
         life=8, gen=3, init_pos=1, radius=.1, axis=(0, 1, 0), vel=(.05, .03), gravity=(0, -.01, 0), alpha=(31, 31, 0))
    for res in (2, 3):
        prop(b, rs, res, life=1)
    out[BIC] = bytes(b)
    b, rs = kit(ZAPAURA)
    tex(b, 0, fxart.crackle())
    for res, scl, gen in ((0, .6, 2), (1, .9, 1)):
        prop(b, rs, res, tex=0, clr=rgb(255, 240, 80), clr_anm=(rgb(255, 255, 255), rgb(120, 220, 255)), scl=scl,
             life=4, gen=gen, gen_intvl=2, emtr_life=30, init_pos=1, radius=1.0, alpha=(31, 31, 31))
    out[ZAPAURA] = bytes(b)

    # Big Tax (Mega Drain): the register rings them up - and the receipt just keeps coming, wrapping them up like
    # a mummy - then the drawer pops open and their HP drains right in. Cha-ching.
    b, rs = kit(REGISTER)
    tex(b, 0, fxart.cash_register(), 30)
    b, opened = added(b, fxart.cash_register(open_=True), 30)
    prop(b, rs, POP, scl=1.1, life=70, scl_anm=POPIN)
    prop(b, rs, 1, tex=opened, scl=1.1, life=30)
    out[REGISTER] = bytes(b)
    no_delay(REGISTER, 1)
    b, rs = kit(RECEIPT)
    tex(b, 1, fxart.receipt_strip())
    for res, ang in ((STRIP_1, 0x0800), (STRIP_2, -0x0A00 & 0xFFFF), (STRIP_3, 0x1800)):
        prop(b, rs, res, scl=1.3, life=56, scl_anm=(.1, 1.0, 1.0, 40, 255))
        rot(b, rs, res, init=ang)
    prop(b, rs, 0, life=1)
    out[RECEIPT] = bytes(b)
    b, rs = kit(COINS2)
    tex(b, 0, fxart.dime())
    for res, sd in ((DRAIN_E, "player"), (DRAIN_P, "enemy")):
        drain(b, rs, res, sd, 18, tex=0, clr=rgb(255, 210, 60), clr_anm=(rgb(255, 250, 200), rgb(220, 160, 30)),
              scl=.45, gen=1, gen_intvl=2, emtr_life=22, init_pos=1, radius=.6, alpha=(31, 31, 10))
    out[COINS2] = bytes(b)

    # Mud Bath (Mud Sport): spa day - they sink into a tub of mud, towel turban, cucumbers on the eyes. Ahhh.
    b, rs = kit(SPA)
    tex(b, 1, fxart.mud_tub())
    b, face = added(b, fxart.spa_face(), 24)
    tex(b, 0, fxart.fizz_drop())
    prop(b, rs, TUB, scl=1.4, life=80, scl_anm=POPIN)
    prop(b, rs, SPAFACE, tex=face, scl=1.0, life=60, scl_anm=(1.5, 1.0, 1.0, 20, 255))
    prop(b, rs, MUDBUBS, tex=0, clr=rgb(140, 100, 60), clr_anm=(rgb(190, 150, 100), rgb(100, 70, 40)), scl=.4,
         life=16, gen=1, gen_intvl=4, emtr_life=60, init_pos=1, radius=.9, axis=(0, 1, 0), vel=(.006, .012),
         alpha=(31, 31, 0), scl_anm=(.3, 1.2, 1.5, 70, 220))
    prop(b, rs, 3, life=1)
    out[SPA] = bytes(b)
    b, rs = kit(SPASTEAM)
    tex(b, 1, fxart.steam_wisp())
    prop(b, rs, 1, tex=1, clr=rgb(240, 240, 250), clr_anm=(rgb(255, 255, 255), rgb(220, 220, 235)), scl=.7, life=30,
         gen=1, gen_intvl=5, emtr_life=60, init_pos=1, radius=1.2, axis=(0, 1, 0), vel=(.004, .015), alpha=(20, 16, 0))
    prop(b, rs, 0, life=1)
    out[SPASTEAM] = bytes(b)

    # Hype Up (Psych Up): their hype man pops up next to them yelling through a megaphone, foam #1 finger going -
    # confetti everywhere, they're bouncing, glowing
    b, rs = kit(HYPE)
    tex(b, 0, fxart.hype_man(), 30)
    b, finger = added(b, fxart.foam_finger(), 16)
    prop(b, rs, POP, scl=1.2, life=4)
    prop(b, rs, 1, tex=finger, scl=ONE_TO_ONE, life=4)
    out[HYPE] = bytes(b)
    no_delay(HYPE, 1)
    b, rs = kit(CONFETTI)
    tex(b, 0, fxart.confetti())
    for res, hi, lo in ((0, rgb(255, 80, 120), rgb(80, 200, 255)), (1, rgb(255, 230, 60), rgb(120, 255, 120))):
        prop(b, rs, res, tex=0, clr=lo, clr_anm=(hi, lo), scl=.5, life=40, gen=10, emtr_life=2, init_pos=1,
             radius=.4, axis=(0, 1, 0), vel=(.2, .2), gravity=(0, -.01, 0), alpha=(31, 31, 0), air_resist=118,
             flags_on=(1 << 14) | (1 << 12))
        rot(b, rs, res, spin=0x0800)
    out[CONFETTI] = bytes(b)
    SET10_82 += [BOARD, PIGEON, TANNING, GRILL, TRUNK, HOOPTIE, SHIELD, CLOCKIN, JANITOR, CFAN, FANBLADES, BIC,
                 RECEIPT, SPA]

    # ---- set 12 --------------------------------------------------------------------------------------------
    # Fidget Spin (Gyro Ball): a big gold fidget spinner, faster and faster - flung like a buzzsaw, grinding
    # sparks off them, and it comes right back
    b, rs = kit(FIDGET)
    tex(b, 1, fxart.fidget_spinner())
    tex(b, 0, fxart.tiny_spark())
    prop(b, rs, SPIN1, scl=1.0, life=4, flags_on=(1 << 14) | (1 << 12))
    rot(b, rs, SPIN1, spin=0x3000)
    prop(b, rs, SPARKS11, tex=0, clr=rgb(255, 220, 80), clr_anm=(rgb(255, 255, 255), rgb(255, 130, 30)), scl=.45,
         life=12, gen=4, init_pos=1, radius=.4, axis=(0, 1, 0), vel=(.12, .06), gravity=(0, -.015, 0),
         alpha=(31, 31, 0))
    for res in (2, 3):
        prop(b, rs, res, life=1)
    out[FIDGET] = bytes(b)
    b, rs = kit(WHIRLS)
    tex(b, 0, fxart.whoosh_arc())
    prop(b, rs, 0, tex=0, clr=rgb(255, 230, 120), clr_anm=(rgb(255, 255, 255), rgb(255, 200, 60)), scl=.9, life=6,
         alpha=(28, 24, 0), scl_anm=(.6, 1.2, 1.4, 60, 200), flags_on=(1 << 14) | (1 << 12))
    rot(b, rs, 0, spin=0x3000)
    prop(b, rs, 1, life=1)
    out[WHIRLS] = bytes(b)

    # Neon Beam (Aurora Beam): the corner-store LIQUOR sign buzzing... flickering... BZZT - it comes on full,
    # and the neon blasts them
    b, rs = kit(NEONSIGN)
    tex(b, 0, fxart.neon_sign(lit=False), 30)
    b, lit = added(b, fxart.neon_sign(), 30)
    prop(b, rs, POP, scl=ONE_TO_ONE, life=4)
    prop(b, rs, 1, tex=lit, scl=ONE_TO_ONE, life=4)
    out[NEONSIGN] = bytes(b)
    no_delay(NEONSIGN, 1)
    b, rs = kit(NEONBEAM)
    tex(b, 0, fxart.glow_dot())
    for res, sd in ((0, "player"), (1, "enemy")):
        spray(b, rs, res, sd, NEON_AT[sd], (0, 22), 12, tex=0, clr=rgb(255, 80, 200),
              clr_anm=(rgb(120, 230, 255), rgb(255, 60, 200)), scl=.6, gen=3, gen_intvl=1, emtr_life=22, radius=.2,
              spread=.012, alpha=(31, 31, 10), scl_anm=(.6, 1.0, 1.3, 0, 200))
    out[NEONBEAM] = bytes(b)

    # Snooze (Yawn): they read the foe the most boring book ever - TERMS & CONDITIONS - page... after page...
    b, rs = kit(BOOK)
    tex(b, 1, fxart.tos_book())
    b, opened = added(b, fxart.tos_book(open_=True), 16)
    tex(b, 0, fxart.nap_z())
    prop(b, rs, BOOK_SHUT, scl=ONE_TO_ONE / 1.1, life=16, scl_anm=POPIN)
    prop(b, rs, BOOK_OPEN, tex=opened, scl=ONE_TO_ONE, life=4)
    prop(b, rs, ZEES11, tex=0, clr=rgb(150, 170, 255), clr_anm=(rgb(230, 235, 255), rgb(110, 120, 255)), scl=.55,
         life=28, gen=1, gen_intvl=7, emtr_life=40, axis=(.5, 1, 0), vel=(0, .02), alpha=(31, 31, 0),
         scl_anm=(.4, 1.2, 1.0, 50, 255))
    prop(b, rs, 3, life=1)
    out[BOOK] = bytes(b)

    # Cologne (Sweet Scent): pssht pssht pssht pssht - WAY too much - then right at the foe: a purple cloud of it
    b, rs = kit(COLOGNE)
    b = held(b, rs, BOTTLE_R11, BOTTLE_L11, fxart.cologne_bottle(), .9, 60, scl_anm=POPIN)
    tex(b, 0, fxart.glow_dot())
    for res, sd in ((MIST_E11, "player"), (MIST_P11, "enemy")):
        drops(b, rs, res, sd, COLOGNE_TIP[sd], (0, 24), 12, rgb(255, 210, 255), rgb(200, 110, 255), .5, emtr_life=6,
              gen=3, spread=.03, radius=.2, alpha=(24, 20, 0), scl_anm=(.4, 1.0, 1.8, 0, 200))
    out[COLOGNE] = bytes(b)
    b, rs = kit(FUMES11)
    tex(b, 0, fxart.stink_puff())
    for res, scl, gen in ((0, .9, 6), (1, .5, 3)):
        prop(b, rs, res, tex=0, clr=rgb(190, 110, 240), clr_anm=(rgb(250, 210, 255), rgb(150, 70, 220)), scl=scl,
             life=36, gen=gen, emtr_life=3, init_pos=1, radius=.7, vel=(.04, .01), alpha=(24, 20, 0),
             scl_anm=(.4, 1.3, 1.8, 60, 220), air_resist=118)
    out[FUMES11] = bytes(b)

    # Spin the Blk (Rapid Spin): they hop on a kid's BMX, streamers flying, and ride laps round the foe
    b, rs = kit(BMX)
    b = held(b, rs, BIKE_R, BIKE_L, fxart.bmx_bike(), 1.0, 4)
    tex(b, 0, fxart.soot_puff())
    prop(b, rs, DUST11, tex=0, clr=rgb(210, 190, 150), clr_anm=(rgb(240, 230, 210), rgb(170, 150, 110)), scl=.45,
         life=14, gen=2, init_pos=1, radius=.2, vel=(.04, .01), alpha=(26, 22, 0), scl_anm=(.4, 1.2, 1.6, 60, 200))
    prop(b, rs, 3, life=1)
    out[BMX] = bytes(b)
    SET10_82 += [FIDGET, BOOK, COLOGNE, BMX]

    for ps in SET10_82:                                       # file 82's emitters sit at built-in offsets (res 3
        b = bytearray(out[ps])                                #  ~40 px up): set 10 places everything itself
        rs = spa.resources(bytes(b))
        for res in range(len(rs)):
            no_offset(b, rs, res)
        out[ps] = bytes(b)
    # the donors tile their small textures 2x2 (or 2x1) mirrored - quarters of a shape; sets 5-6 are whole shapes
    for ps in range(TORCH, LAST_KIT + 1):
        b = bytearray(out[ps])
        for r in spa.resources(bytes(b)):
            b[r["off"] + TILE] &= 0xF0
        out[ps] = bytes(b)

    # (TRACER and the THROWN objects aren't listed: MoveEmitter deletes them when the flight ends, so they must
    #  NOT self-destruct - see below)
    for ps, res in ((GUN, SPARK), (GUN, FLASH), (KIT, CASING), (KIT, CROSS), (SMOKE, PUFF),
                    (SMOKE, DIRT), (CAR, RIDE), (CAR, WINDOW), (BLING, PENDANT), (CASH, BILLS), (CASH, STACK),
                    (ROCKET, TO_ENEMY), (ROCKET, TO_PLAYER), (FIRE, EMBERS), (FIRE, BLAZE), (HOUSE, HOME),
                    (YOLK, DRIP), (YOLK, SPLAT), (CAR, PARKED), (CAR, BOUNCE), (HYDRANT, STAND),
                    (JET, JET_E), (JET, JET_P), (SPLASH, 0), (SPLASH, 1), (SLUGGER, SWING_E), (SLUGGER, SWING_P),
                    (TASER, STAND), (TASER, TASER_P), (BOLTS, ZAP), (FOB, STAND), (RINGS, RING), (SUB, BOX),
                    (SUB, PUMP), (CRACK, SPLIT), (CHIPS, BAG), (CHIPS, CHIP_E), (CHIPS, CHIP_P), (BURST, TONGUE),
                    (BURST, EMBER), (SHADES, SLIDE), (GLINT, TING), (GLINT, SWEAT), (BUBBLE, BANG), (POCKET, SIGN),
                    (POCKET, GRAIN_E), (POCKET, GRAIN_P), (SAND, CLOUD), (FAN, BODY), (FAN, BLADES),
                    (WIND, GUST_E), (WIND, GUST_P),
                    (PLANE, PASS), (PLANE, JETSMOKE), (FELICIA, POP), (CLAIM, SUIT), (WHAM, POP), (WAVE, WAVE_E),
                    (WAVE, WAVE_P), (WAVE, FOAM), (DUCK, DUCK_E), (DUCK, DUCK_P), (CABLE, POSE), (CABLE, HOLD),
                    (XRAY, BONES), (XRAY, SPARKS), (HONK, HONK_A), (HONK, HONK_B), (HONK, STEAM), (BOOZE, SWIG),
                    (BOOZE, LIGHTER), (BREATH, FIRE_E), (BREATH, FIRE_P), (LEAF, LEAF_E), (LEAF, LEAF_P),
                    (LEAF, BIGLEAF), (HAZE, HAZE1), (BOOT, POSE), (BOOT, HOLD), (STOMP, 2), (STOMP, DUST),
                    (TOPJAW, POSE), (TOPJAW, HOLD), (BOTJAW, POSE), (BOTJAW, HOLD), (GLITZ, SPARKLE),
                    (SLUG, DOT), (SLUG, HOLE), (SLUG, IMPACT), (SLASH, SLASH_A), (SLASH, SLASH_B), (SLASH, SLASH_C), (SLASH, GLEAM),
                    (TIRE, TIRE_UP), (TIRE, TIRE_FLAT), (TIRE, HISS), (SMOG, SMOG1), (SMOG, SMOG2), (COUGH, PUFFUP),
                    (WHEEL, SPIN), (WHEEL, SMOKE1), (BLOCKS, HALF_L), (BLOCKS, HALF_R), (BLOCKS, CHUNKS), (CHOP, POSE), (CHOP, HOLD), (HIYAH, POP),
                    (EIGHT, CHARGE), (EIGHT, WISPS), (ANSWER, POP), (HEART, LOCKET), (HEART, HEARTS_E),
                    (HEART, HEARTS_P),
                    (TORCH, TORCH_E), (TORCH, TORCH_P), (TORCH, SWIRL), (BEAM, BEAM_E), (BEAM, BEAM_P), (HUH, POP),
                    (STUN, STUN_E), (STUN, STUN_P), (STUN, ARC_E), (STUN, ARC_P), (STATIC, RING_X),
                    (STATIC, RING_HOLD), (ZZZT, POP), (BOOMBOX, BOX5), (BOOMBOX, THUMP), (BOOMBOX, NOTES_E),
                    (BOOMBOX, NOTES_P), (SOUNDWAVE, SWAVE_E), (SOUNDWAVE, SWAVE_P), (BWOMP, POP), (SQUAD, FIG),
                    (SQUAD, FIG_S), (SQUAD, POOF), (SQUAD2, FIG2), (SQUAD2, FIG2_S), (SQUADUP, POP),
                    (BALLOON, DROPS), (DRENCH, CROWN), (DRENCH, SPLASHDROPS), (SPLOOSH, POP), (DISS, POP),
                    (SLAP, SLAP_POSE), (SLAP, SLAP_HOLD), (SLAP, POWS), (OOOH, POP), (CUP, HELD), (CUP, BUBBLES),
                    (GOOP, GOOP_SPLAT), (GOOP, GOOP_DRIPS), (DIRTY, POP), (LID, LIDUP), (LID, LIDFLASH),
                    (LID, PINGS), (NOPE, POP), (CHAIR, CHAIR_POSE), (CHAIR, CHAIR_HOLD), (CHAIR, STARS),
                    (CLANG, POP), (SMACKDN, POP), (BIGTASER, BIG_E), (BIGTASER, BIG_P), (BIGTASER, ZIGS),
                    (MEGABOLT, STRIKE), (MEGABOLT, STRIKE2), (BZZT, POP), (EYES, EYES_R), (EYES, EYES_L),
                    (CIRCLE, POP), (CLOCKED, POP),
                    (BELT, BELT_E), (BELT, BELT_P), (WELT, WELT1), (WELT, SNAPS), (WHAP, POP), (SHIV, SHIV_E),
                    (SHIV, SHIV_P), (SHIV, SKULLS), (SHIVD, POP), (TWERK, WIGGLE_R), (TWERK, WIGGLE_L),
                    (DEFDOWN, POP), (BRUH, POP), (STAMP, POSE), (STAMP, HOLD), (TAXED, POP), (COINS, MONEYBAG),
                    (COINS, COIN_E), (COINS, COIN_P), (CAN, CAN1), (CAN, STR_E), (CAN, STR_P), (TANGLE, TANGLED),
                    (TANGLE, TANGLE_HOLD), (STUCK, POP), (SPIT, DRIBBLE), (GOBSPLAT, POP), (PTOO, POP),
                    (KICKS, SHOES), (KICKS, ZOOMS), (LACED, POP), (CRATE, BOX7), (CRATE, FUSE), (CRATE, GLITTER),
                    (FWBURST, POP), (FWBURST, 1), (BOOOM, POP), (CART, CART_GO), (CART, CART_FLIP),
                    (CARTL, CART_GO), (CARTL, CART_FLIP), (CRASH, POP), (PHONES, CANS), (PHONES, CANS_THUMP),
                    (PHONES, MOTES), (LOCKED, POP), (BUMP, POP), (BUMP, 1), (DOMECHK, POP), (GRAB, POSE),
                    (GRAB, HOLD), (YANK, POSE), (YANK, HOLD), (YOINK, POP),
                    (POOLF, FLOATIE), (POOLF, RIPPLES), (CHILLIN, POP), (TAPE, TAPE_A), (TAPE, TAPE_B),
                    (BARRIER, POP), (NOEXIT, POP), (LOOKBUB, POP), (FIST, POSE), (FIST, HOLD), (CHEAP, POP),
                    (JAMGUN, GUNUP), (JAMGUN, SPUTTERS), (JAMMED, POP), (CIGAR, CIGAR_R), (CIGAR, CIGAR_L),
                    (CIGAR, RINGS8), (SNOOZE, ZZZ), (NIGHT, POP), (MAG, POSE), (MAG, HOLD),
                    (HEALS, PLUSES), (RELOADED, POP),
                    *((ps, r) for ps in range(HENNY, LAST_KIT + 1) for r in (0, 1) if (ps, r) not in FLOWN)):
        flag = spa.resources(out[ps])[res]["flag"]
        assert flag >> 14 & 1, f"kit {ps} emitter {res} never finishes (no self_dest): WaitForParticles would hang"
    for ps, res in ((GUN, TRACER), (BOTTLE, THROWN), (BRICK, THROWN), (EGG, THROWN), (BUBBLE, TALK),
                    (CONE, THROWN), (BOOZE, THROWN),
                    (WHEEL, ROLL), (TRAIL, FIRETRAIL), (EIGHT, ROLL8), (HEART, SLAM),
                    (BALLOON, THROWN), (CUP, THROWN), (SPIT, THROWN), *FLOWN):
        flag = spa.resources(out[ps])[res]["flag"]
        assert not flag >> 14 & 1, f"kit {ps} emitter {res} is flown by MoveEmitter: it must not self-destruct"
    return out


# ------------------------------------------------------------------ script pieces

def _u(v):
    return v & 0xFFFFFFFF


def func(fid, *args):
    return [45, fid, len(args), *(_u(a) for a in args)]


def wait(n):
    return [0, n]


def wait_frames(n):
    """A wait lasting about n frames (measured: wait(k) takes 2 * (k + 1))."""
    return wait(max(0, round(n / 2) - 1))


def se(seq):
    return [5, seq] if seq is not None else []


_SIDE = ["player"]                                            # whose turn the script being built is for


def _depth(who):
    """'near' or 'far' for the attacker (who=0) / defender (who=1) of the current script side."""
    attacker_near = _SIDE[0] == "player"
    return "near" if (who == 0) == attacker_near else "far"


_SLOT = {}                                                    # kit -> particle-system slot, for the variant being built


def _ps(kit):
    """The engine has only 16 particle-system slots (particleSystems[16], followed by emitters[16]): kit numbers
    go past that, so each animation puts its kits in slots 0, 1, 2."""
    return _SLOT[kit]


def emit_at(ps, res, who, off=(0, 0)):
    """Emitter at the attacker (who=0) or defender (who=1) plus an offset in screen pixels (y up).
    (Particles always draw over the Pokémon: their sprites sit at the back of the depth range and draw first, as
    opaque polygons - no depth or alpha puts a particle behind one.)"""
    if off == (0, 0):
        return [46, _ps(ps), res, 3 if who == 0 else 4]
    sx, sy = PS_SCALE.get(ps, SCALE)[_depth(who)]
    x, y = round(off[0] * sx), round(off[1] * sy)
    # ConfigureFromScript: zMode, battlerOrder 0, position mode 4/5 (battler A/B + offset), axis, flags,
    # camera; then the offset args {ignoreSide, x, y, z}
    return [46, _ps(ps), res, 17, 55, 6, 0, 0, 4 + who, 0, 0, 0, 55, 4, 1, _u(x), _u(y), 0]


def muzzle(ps, res, side, back=0):
    x, y = MUZZLE[side]
    return emit_at(ps, res, 0, (x - back if x > 0 else x + back, y))


def tracer(slot, frames, off=(0, 0), start=2, delay=0):
    """Bullet streak flown from the barrel to the target (+ off pixels), with MoveEmitter."""
    return [47, _ps(GUN), slot, TRACER, 3] + func(65, slot, off[0], off[1], delay, frames, 0, 0, start << 16, 0)


def shake_defender(amp, count):
    return func(36, amp, 0, 1, count, 264)


def shake_attacker(amp, count):
    return func(36, amp, amp // 2, 1, count, 258)


def recoil(px, back_frames=4):
    return func(52, 1, -px, 258), func(52, back_frames, px, 258)


def flash_screen(steps=6):
    return [85, steps]


# ------------------------------------------------------------------ the five feels

def _sniper(side, s):
    w = func(33, 0, 1, 0, 12, 0)                              # the world goes dark...
    w += emit_at(KIT, CROSS, 1) + wait(34)                     # ...red crosshair locks on, beat of silence
    kick, back = recoil(10)
    w += se(s["boom"]) + flash_screen(8) + kick
    w += muzzle(GUN, FLASH, side) + muzzle(GUN, SPARK, side)
    w += tracer(1, 2, start=1) + wait(2)
    w += emit_at(GUN, FLASH, 1) + emit_at(GUN, SPARK, 1) + func(48) + func(68, 5, 0, 1, 3, 0)
    w += back + wait(6) + muzzle(SMOKE, PUFF, side) + wait(10)
    w += func(33, 0, 1, 12, 0, 0)
    return w


def _shotgun(side, s):
    kick, back = recoil(14, 6)
    w = se(s["boom2"]) + flash_screen(6) + kick + func(9)
    w += muzzle(GUN, FLASH, side) + muzzle(GUN, SPARK, side) + muzzle(GUN, SPARK, side, back=4)
    for slot, off in enumerate([(0, 0), (12, 7), (-12, -6), (7, -12), (-7, 12)], 1):
        w += tracer(slot, 4, off, start=1)
    w += wait(4) + emit_at(GUN, FLASH, 1) + emit_at(GUN, SPARK, 1)
    for off in ((10, 9), (-9, -7)):
        w += emit_at(GUN, SPARK, 1, off)
    w += func(48) + shake_defender(5, 4) + muzzle(SMOKE, PUFF, side) + back + wait(12)
    return w


def _spray(side, s):
    w = shake_attacker(2, 26)                                  # the shooter can't hold it steady
    jit = [(0, 0), (14, -9), (-10, 12), (18, 6), (-16, -4), (6, 16), (-4, -14)]
    dirt = [(14, -16), (-12, -18), (6, -20), (-17, -14), (11, -12), (-4, -19)]
    for i in range(7):
        w += se(s["pop"]) + muzzle(GUN, SPARK, side) + tracer(1 + i % 4, 3, jit[i], start=1)
        w += muzzle(KIT, CASING, side, back=18)
        if i < len(dirt):
            w += emit_at(SMOKE, DIRT, 1, dirt[i])
        w += wait(4)
    w += emit_at(GUN, SPARK, 1) + shake_defender(3, 4) + wait(8)
    return w


def _point_blank(side, s):
    w = func(57, 8, 70, -34, 258) + wait(9)                    # walk right up to them
    w += func(36, 1, 0, 1, 6, 258) + wait(8)                   # menacing pause
    w += se(s["boom"]) + flash_screen(12)
    w += emit_at(GUN, FLASH, 1, (-10, 4)) + emit_at(GUN, SPARK, 1)
    w += func(50, 4, 1) + func(48) + func(68, 6, 2, 1, 4, 0) + wait(10)
    w += muzzle(SMOKE, PUFF, side) + func(57, 10, -70, 34, 258) + wait(12)
    return w


def _gangsta(side, s):
    w = func(4, 0, 0x1C00, 14, 1, 0, 40) + wait(12)            # tilt it sideways
    for i in range(2):
        kick, back = recoil(4, 2)
        w += se(s["pop"]) + kick + muzzle(GUN, FLASH, side) + muzzle(GUN, SPARK, side)
        w += tracer(1 + i, 3, start=1) + muzzle(KIT, CASING, side, back=18) + back + wait(5)
    w += emit_at(GUN, SPARK, 1) + shake_defender(3, 3) + wait(4)
    w += muzzle(SMOKE, PUFF, side) + wait(14) + func(19) + wait(10)   # blow the smoke, little hop
    return w




def _drive_by(side, s):
    """Hop in the car off-screen, roll past the target blasting out the window, dip, come back."""
    w = func(19) + wait(8)                                     # hop up...
    w += func(57, 10, -130, 0, 258) + wait(12)                 # ...and run out of frame to get the car
    w += se(s["skrrt"]) + emit_at(CAR, RIDE, 1, (CAR_START, CAR_ROAD))
    w += emit_at(CAR, WINDOW, 1, (CAR_START + GUN_ON_CAR[0], CAR_ROAD + GUN_ON_CAR[1]))
    first = (-CAR_START - GUN_ON_CAR[0] - 25) / CAR_SPEED - 18  # frames until the gun lines up (-18 measured)
    for i in range(6):                                         # rounds land while it rolls past
        w += wait_frames(first if i == 0 else 6)
        w += se(s["pop"]) + emit_at(GUN, SPARK, 1, ((i * 37 % 9 - 4) * 3, (i * 23 % 7 - 3) * 3))
        if i % 2 == 0:
            w += emit_at(SMOKE, DIRT, 1, ((i - 3) * 9, -14))
        w += shake_defender(3, 2)
    w += wait(30)                                              # and they're gone
    w += func(57, 10, 130, 0, 258) + wait(12)                  # back like nothing happened
    return w


def _fly_turn2_first(side, s):
    """Test only (the showcase always plays variant 0): Catch Flight with the turns swapped, to see turn 2."""
    one, two = _catch_flight(side, s)
    return two, one


def _calibrate(side, s):
    """Test only: the same offset (40px left of the target) in three kits - where does each really land?"""
    w = emit_at(GUN, FLASH, 1, (-40, 0)) + wait(14)
    w += emit_at(YOLK, SPLAT, 1, (-40, 0)) + wait(14)
    w += emit_at(HOUSE, HOME, 1, (-40, 0)) + wait(30)
    return w


SWING_STEP = 4                                                # frames each pose of the swinging chain shows
# (= wait(1): one script tick takes ~2 frames, plus the tick the commands run in)


def _chain_swing(side, s, swings=3, dark=True):
    """Psychic: an iced-out chain swung in front of their face like a hypnotist's watch (stop-motion:
    one short-lived chain per pose along the pendulum arc)."""
    purple = rgb(70, 0, 110)
    w = func(33, 0, 1, 0, 9, purple) + wait(4) if dark else []
    poses = 10                                                 # per swing (there and back)
    for k in range(swings * poses):
        ph = 2 * math.pi * k / poses
        x = 15 * math.sin(ph) - 8                              # (the particle origin sits right of their face)
        y = 16 - 3 * math.cos(2 * ph)                          # rides up a little at the ends
        w += emit_at(BLING, PENDANT, 1, (round(x), round(y)))
        if k % (poses // 2) == poses // 4:                     # at each end of the swing
            end = 1 if math.sin(ph) > 0 else -1
            w += se(s["bling"]) + emit_at(GUN, SPARK, 1, (end * 15 - 8, 10))
            w += func(4, 0, 0x0C00, 6, 0 if end > 0 else 2)    # their head follows it
        w += wait(1)
    w += func(34, 8, 0, 2, purple, 14, 0) + shake_defender(3, 4) + emit_at(GUN, FLASH, 1) + wait(8)
    if dark:
        w += func(33, 0, 1, 9, 0, purple)
    return w


def _payday(side, s):
    """Make it rain: flash the bankroll, then a storm of bills flutters down on them."""
    w = se(s["chaching"]) + func(19) + emit_at(CASH, STACK, 0, (6, 52)) + wait(14)
    w += emit_at(CASH, BILLS, 1, (0, 62))                       # it's raining
    for k in range(4):
        w += wait(6) + emit_at(GUN, SPARK, 1, ((k * 29 % 21) - 10, (k * 17 % 13) - 4)) + shake_defender(2, 2)
        if k == 2:
            w += se(s["chaching"])
    return w + wait(30)


def _explosion(side, s, big=True):
    """A big hit on the target: fireball flash, sparks flying, dirt, smoke, the whole field shaking."""
    w = se(s["boom2"]) + flash_screen(12 if big else 6)
    w += emit_at(GUN, FLASH, 1) + emit_at(GUN, FLASH, 1, (8, 6)) + emit_at(GUN, SPARK, 1)
    for off in ((14, 10), (-12, 8), (10, -8), (-14, -6)):
        w += emit_at(GUN, SPARK, 1, off)
    w += emit_at(SMOKE, DIRT, 1, (-10, -14)) + emit_at(SMOKE, DIRT, 1, (12, -14))
    w += func(48) + func(68, 6, 3, 1, 5, 0) + shake_defender(5, 5)
    w += wait(6) + emit_at(SMOKE, PUFF, 1, (0, 4)) + emit_at(SMOKE, PUFF, 1, (-10, -2))
    return w


def _full_auto(side, s):
    """Hyper Beam: a minigun barrage - brass pouring out, the shooter shaking, then everything goes up."""
    w = shake_attacker(2, 60) + func(68, 2, 1, 1, 20, 0)       # the whole screen rattles
    jit = [(0, 0), (12, -8), (-9, 10), (16, 5), (-14, -4), (5, 14), (-4, -12), (10, 10)]
    for i in range(18):
        if i % 2 == 0:
            w += se(s["pop"])
        w += muzzle(GUN, SPARK, side) + tracer(1 + i % 6, 3, jit[i % len(jit)], start=1)
        if i % 2:
            w += muzzle(KIT, CASING, side, back=18)
        if i % 4 == 0:
            w += emit_at(GUN, SPARK, 1, (jit[(i + 3) % 8][0] // 2, jit[(i + 5) % 8][1] // 2))
        if i % 6 == 5:
            w += flash_screen(4)
        w += wait(1)
    w += muzzle(SMOKE, PUFF, side) + wait(4)
    return w + _explosion(side, s) + wait(14)


def _rpg(side, s):
    """Legendary finisher: shoulder an RPG, fwoosh, a smoking rocket crosses the field, KABOOM."""
    kick, back = recoil(12, 8)
    w = se(s["fwoosh"]) + kick + muzzle(GUN, FLASH, side) + muzzle(SMOKE, PUFF, side, back=20)
    w += emit_at(ROCKET, TO_ENEMY if side == "player" else TO_PLAYER, 0, MUZZLE[side])
    mx, my = MUZZLE[side]
    t = 0
    for k in (1, 2, 4):                                        # smoke trail left behind it
        w += wait_frames(ROCKET_FRAMES / 5 * (k - t))
        t = k
        f = k / 5
        dx, dy = (128 * f, 64 * f) if side == "player" else (-128 * f, -64 * f)
        w += emit_at(SMOKE, PUFF, 0, (round(mx * (1 - f) + dx), round(my * (1 - f) + dy)))
    w += wait_frames(ROCKET_FRAMES / 5) + back
    return w + _explosion(side, s) + wait(20)


def _throw(kit, slot=1, at=(0, 0)):
    """Lob the kit's object from the attacker at the target (+ `at` screen pixels from it): MoveEmitter flies
    the emitter in a line while the object, riding it, goes up and comes down (its own gravity)."""
    sx = SCALE[_depth(1)][0] / EMITTER_PIXEL               # MoveEmitter offsets are 172-unit pixels, x mirrored
    sy = SCALE[_depth(1)][1] / EMITTER_PIXEL               # by the attacker's side
    side = 1 if _SIDE[0] == "player" else -1
    ox, oy = round(at[0] * sx * side), round(at[1] * sy * side)
    return se_key("whoosh") + [47, _ps(kit), slot, THROWN, 3] + func(65, slot, ox, oy, 0, THROW_FRAMES, 0, 0, 0, 0)


def se_key(key):
    return ["SE", key]                                        # resolved to a sound id by variant()


def _molotov(side, s):
    """Flamethrower: a Molotov tumbles over and shatters; flames lick up and they dance around on fire."""
    orange = rgb(255, 120, 20)
    w = func(19) + wait(4) + _throw(BOTTLE) + wait_frames(THROW_FRAMES)
    w += se(s["smash"]) + emit_at(GUN, SPARK, 1, (0, -4)) + emit_at(FIRE, BLAZE, 1, (0, -8))
    w += emit_at(FIRE, EMBERS, 1, (0, -6)) + func(34, 8, 0, 2, orange, 14, 0)
    for k in range(4):                                         # hot hot hot: hopping side to side
        dx = (6, -12, 12, -6)[k]                                # nets to zero: they end up where they started
        w += func(57, 3, dx, 0, 264) + emit_at(FIRE, BLAZE, 1, ((-7, 7, -3, 5)[k], -8)) + wait(4)
    w += emit_at(FIRE, EMBERS, 1, (0, 0)) + shake_defender(2, 4) + wait(14)
    return w


def _brick(side, s):
    """Rock Throw: a brick tumbles across - BONK - they drop, lie there seeing stars, then slowly get up."""
    down = -10 if side == "player" else 10                    # MoveBattlerBy mirrors the enemy's y
    w = func(19) + wait(4) + _throw(BRICK) + wait_frames(THROW_FRAMES)
    w += se(s["bonk"]) + emit_at(GUN, FLASH, 1, (0, 12)) + emit_at(GUN, SPARK, 1, (0, 14))
    w += emit_at(SMOKE, DIRT, 1, (-8, -12)) + emit_at(SMOKE, DIRT, 1, (8, -12))
    w += func(57, 3, 0, down, 264) + func(36, 2, 0, 1, 3, 264) + wait(4)      # knocked down on the spot
    for k in range(16):                                        # out cold: stars round the head, slow wobble
        ang = k * math.pi / 4
        w += emit_at(GUN, SPARK, 1, (round(12 * math.cos(ang)), round(14 + 4 * math.sin(ang))))
        if k % 8 == 0:
            w += func(4, 0, 0x0500, 12, 0 if k % 16 == 0 else 2)
        w += wait(3)
    w += func(57, 16, 0, -down, 264) + wait(18)               # ...and slowly back up
    return w


def _egg(side, s):
    """Egg Bomb: egg ya house - their house pops up and gets egged, then they catch the last one."""
    yolk = rgb(255, 220, 60)
    hx, hy = (42, 20) if side == "player" else (-42, 20)      # their house: behind them, standing on their ground
    w = se(s["bling"]) + emit_at(HOUSE, HOME, 1, (hx, hy)) + wait(12)
    for k, (dx, dy) in enumerate(((-8, 6), (9, -4))):           # two on the house...
        w += func(19) + _throw(EGG, 1 + k, (hx + dx, hy + dy)) + wait_frames(THROW_FRAMES)
        w += se(s["splat"]) + emit_at(YOLK, SPLAT, 1, (hx + dx, hy + dy)) + emit_at(YOLK, DRIP, 1, (hx + dx, hy + dy - 2))
        w += wait(6)
    w += func(19) + _throw(EGG, 3) + wait_frames(THROW_FRAMES)  # ...and one for them
    w += se(s["splat"]) + emit_at(YOLK, SPLAT, 1, (0, 10)) + emit_at(YOLK, DRIP, 1, (0, 8))
    w += func(34, 8, 0, 2, yolk, 14, 0) + shake_defender(2, 3) + wait(30)
    return w


def _fly(ps, res, slot, frames, at=(0, 0)):
    """Create kit ps's emitter res at the attacker and fly it (MoveEmitter) to the target + at (screen px)."""
    sx = SCALE[_depth(1)][0] / EMITTER_PIXEL
    sy = SCALE[_depth(1)][1] / EMITTER_PIXEL
    side = 1 if _SIDE[0] == "player" else -1
    return [47, _ps(ps), slot, res, 3] + func(65, slot, round(at[0] * sx * side), round(at[1] * sy * side), 0, frames,
                                         0, 0, 0, 0)


def _hose(side, s):
    """Water Gun: a hydrant pops up beside them, cap off, and it HOSES the target - the water really comes out
    of the nozzle and arcs over."""
    blue = rgb(80, 150, 255)
    hx, hy = HYDRANT_AT[side]
    nx, ny = hx + NOZZLE[side][0], hy + NOZZLE[side][1]
    w = se(s["bonk"]) + emit_at(HYDRANT, STAND, 0, (hx, hy)) + wait(10)
    w += se(s["spray"]) + emit_at(JET, JET_E if side == "player" else JET_P, 0, (nx, ny))
    w += wait_frames(JET_FRAMES) + func(34, 8, 0, 2, blue, 14, 0)
    for k in range(3):                                          # getting drenched
        w += emit_at(SPLASH, 1, 1, ((-6, 6, 0)[k], (8, 2, 14)[k])) + emit_at(SPLASH, 0, 1, (0, 6))
        w += shake_defender(2, 3) + wait(5)
        if k == 1:
            w += se(s["spray"])
    return w + wait(16)


def _bat(side, s):
    """Bone Club: walk up, wind up, and swing the bat THROUGH them - CRACK - they reel."""
    px = -30 if side == "player" else 30                       # the hands, at the end of the walk-up
    w = func(57, 6, 60, -30, 258) + wait(8)                    # step in
    w += emit_at(SLUGGER, SWING_E if side == "player" else SWING_P, 1, (px, 6)) + se(s["whoosh"]) + wait(3)
    w += se(s["crack"]) + flash_screen(8) + emit_at(GUN, FLASH, 1, (0, 10)) + emit_at(GUN, SPARK, 1, (4, 14))
    w += func(48) + shake_defender(5, 4) + func(68, 4, 2, 1, 3, 0) + wait(8)
    w += func(57, 8, -60, 30, 258) + wait(10)
    return w + wait(6)


def _taser(side, s):
    """ThunderShock: pull the taser, prongs fly, and they light up - bolts crackling all over them."""
    tx, ty = MUZZLE[side]
    w = emit_at(TASER, STAND if side == "player" else TASER_P, 0, (tx - (6 if side == "player" else -6), ty)) + wait(8)
    w += se(s["pop"]) + tracer(1, 4, (-4, 3), start=1) + tracer(2, 4, (4, -3), start=1) + wait_frames(5)
    w += se(s["zap"]) + emit_at(BOLTS, ZAP, 1, (0, 8)) + flash_screen(4)
    for k in range(8):                                          # zzzzt: strobing, twitching
        if k == 4:
            w += se(s["zap"])
        w += func(34, 8, 0, 1, rgb(255, 255, 80) if k % 2 == 0 else rgb(20, 20, 40), 16, 0)
        w += func(36, 3, 1, 1, 2, 264) + wait(2)
    return w + wait(10)


def _car_alarm(side, s):
    """Screech: they mash the panic button on a key fob - the alarm screams and sound waves blast the target."""
    w = emit_at(FOB, STAND, 0, (8, 30)) + wait(8)
    for k in range(6):
        if k % 3 == 0:
            w += se(s["alarm"])
        w += emit_at(RINGS, RING, 1, (0, 8)) + emit_at(RINGS, RING, 0, (8, 30))
        w += func(34, 8, 1, 1, rgb(255, 40, 40) if k % 2 == 0 else rgb(255, 255, 255), 12, 0)
        w += func(36, 3, 0, 1, 3, 264) + wait(5)
    return w + wait(10)


def _bass_drop(side, s):
    """Earthquake: a subwoofer drops in and every bass hit pumps the cone, quakes the screen and cracks the
    ground open under the target."""
    bx, by = (-26, 50) if side == "player" else (26, 30)
    w = emit_at(SUB, BOX, 0, (bx, by)) + wait(8)
    for k in range(8):
        w += se(s["bass"]) + emit_at(SUB, PUMP, 0, (bx, by))
        w += func(68, 4 + k // 3, 2, 1, 2, 0) + func(36, 3, 2, 1, 2, 264) + func(36, 2, 1, 1, 2, 258)
        if k == 1:
            w += emit_at(CRACK, SPLIT, 1, (0, -20))
        w += emit_at(SMOKE, DIRT, 1, ((k % 3 - 1) * 14, -18))
        if k % 2 == 0:
            w += flash_screen(2)
        w += wait(5)
    w += func(48) + func(68, 6, 3, 1, 4, 0) + wait(16)
    return w


def cry(mode, param):
    """PlayCry: the attacker's own cry (modes 9/10 are Growl's distorted takes)."""
    return [65, mode, _u(-117), param]


def _hot_shot(side, s):
    """Ember: they rip open a big bag of HOT chips and fling fistfuls in the target's face - who catches fire."""
    at = BAG_AT[side]
    throw = CHIP_E if side == "player" else CHIP_P
    orange = rgb(255, 120, 20)
    w = emit_at(CHIPS, BAG, 0, at) + wait(10)                                   # the bag
    w += func(19) + se(s["crack"]) + emit_at(BURST, EMBER, 0, at) + wait(4)     # RRIP - it's that hot
    for k in range(3):                                                          # three handfuls
        if k != 1:
            w += se(s["ember"])
        w += emit_at(CHIPS, throw, 0, (at[0], at[1] + (4, -2, 8)[k])) + func(9) + wait(4)
    w += wait_frames(CHIP_FRAMES - 6)
    w += emit_at(BURST, TONGUE, 1, (0, -6)) + emit_at(BURST, EMBER, 1, (0, 6)) + se(s["fwoosh"])
    w += func(34, 8, 0, 2, orange, 14, 0) + shake_defender(3, 5) + func(48) + wait(18)
    return w


def _stare_down(side, s):
    """Leer (Stare Down): lights down, red. "Deal with it" shades slide down into place - THUMP - the lens
    glints, and the target's sweating bullets and backing up."""
    at = SHADES_AT[side]
    dark = rgb(70, 0, 0)
    w = func(33, 0, 1, 0, 12, dark) + wait(4)
    steps = 9
    for k in range(steps):                                                      # ...sliiiide down (easing in)
        y = at[1] + round(SHADES_DROP * (1 - k / (steps - 1)) ** 1.6)
        w += emit_at(SHADES, SLIDE, 0, (at[0], y)) + wait(1)
    w += emit_at(SHADES, LANDED, 0, at)
    w += se(s["bass"]) + func(68, 3, 2, 1, 2, 0) + wait(4)                     # they're on. THUMP
    w += se(s["leer"]) + emit_at(GLINT, TING, 0, (at[0] - 12, at[1])) + wait(10)   # *ting*
    w += emit_at(GLINT, SWEAT, 1, (0, 28)) + func(34, 8, 0, 2, rgb(150, 175, 255), 12, 0)
    w += func(57, 10, 14, 0, 264) + func(36, 2, 0, 1, 8, 264) + wait(8)        # backing up, shaking
    w += emit_at(GLINT, SWEAT, 1, (6, 24)) + wait(12)
    w += func(57, 8, -14, 0, 264) + func(33, 0, 1, 12, 0, dark) + wait(10)
    return w


def _talk_trash(side, s):
    """Growl: they run their mouth - cussing speech bubbles fly across, and every one lands."""
    w = cry(9, 100) + shake_attacker(1, 14)
    for k in range(3):
        w += _fly(BUBBLE, TALK, 1 + k, FLY, ((-8, 8, 0)[k], (6, 14, 22)[k])) + wait(5)
    w += wait_frames(FLY - 10)
    for k in range(3):                                                          # each one hits
        w += emit_at(BUBBLE, BANG, 1, ((-10, 10, 0)[k], 30)) + func(36, 2, 0, 1, 2, 264)
        w += func(34, 3, 0, 1, rgb(255, 80, 80), 8, 0) + wait(4)
    w += cry(10, 127) + wait(14)
    return w


def _pocket_sand(side, s):
    """Sand-Attack: "POCKET SAND!" - and a fistful of sand right in the target's eyes."""
    hand = HAND_AT[side]
    throw = GRAIN_E if side == "player" else GRAIN_P
    w = emit_at(POCKET, SIGN, 0, (hand[0] // 3, 58)) + se(s["sand"]) + func(19) + wait(8)
    for k in range(2):                                                          # SHA-SHA!
        w += se(s["sand"]) + emit_at(POCKET, throw, 0, (hand[0], hand[1] + 3 * k)) + func(9) + wait(4)
    w += wait_frames(SAND_FRAMES - 4)
    w += emit_at(SAND, CLOUD, 1, (0, 20)) + emit_at(SAND, CLOUD, 1, (-8, 12))
    w += func(34, 8, 0, 2, rgb(215, 185, 120), 13, 0)
    w += func(4, 0, 0x0700, 10, 0) + func(36, 2, 0, 1, 6, 264) + wait(10)       # rubbing their eyes
    w += func(4, 0, 0x0700, 10, 2) + wait(16)
    return w


def _fan_blast(side, s):
    """Gust: a box fan drops in next to them, cranks to high, and blows the target clean back."""
    at = FAN_AT[side]                                       # right behind them, blowing past at the target
    gust = GUST_E if side == "player" else GUST_P
    w = emit_at(FAN, BLADES, 0, (at[0], at[1] + 1)) + emit_at(FAN, BODY, 0, at) + wait(8)
    w += se(s["gust"])
    push = 18
    for k in range(5):                                                          # waves of gusts off the grill
        w += emit_at(WIND, gust, 0, (at[0], at[1] + (0, 7, -6, 4, -3)[k]))
        if k == 2:                                                              # the first lines land:
            w += func(57, 10, push, 0, 264) + func(36, 2, 1, 1, 8, 264)          # blown back, flapping
        if k == 3:
            w += se(s["gust"])
        w += wait(3)
    w += wait_frames(GUST_FRAMES) + func(57, 8, -push, 0, 264) + wait(12)
    return w


def bmove(side, role, frames, right, up):
    """MoveBattlerBy in screen px (right, up). The game mirrors moves for battlers on the enemy side."""
    on_player_side = (side == "player") == (role == 258)
    dx, dy = (right, -up) if on_player_side else (-right, up)
    return func(57, frames, dx, dy, role)


def stop_motion(ps, pose, who, start, end, steps, ease=1.6):
    """One short-lived pose per step from start to end (screen px), easing in."""
    w = []
    for k in range(steps):
        t = (k / (steps - 1)) ** ease
        w += emit_at(ps, pose, who, (round(start[0] + (end[0] - start[0]) * t),
                                     round(start[1] + (end[1] - start[1]) * t))) + wait(1)
    return w


def _jet_from(sd):
    """Emit offset (vs the battler on side sd) that starts the jet off-screen left at JET_Y."""
    x, y = BATTLER_AT[sd]
    return (-(x + JET_HALF), y - JET_Y)


def _catch_flight(side, s):
    """Fly (two turns). Turn 1: a beat-up bright-yellow budget jet (Spirit) putters across, they grab the
    rope ladder and get hauled off - BYE FELICIA! Turn 2: it comes back over the opp and drops a suitcase on their
    head - BONK - and they drop back in from the sky."""
    foe = "enemy" if side == "player" else "player"
    start = _jet_from(side)
    one = se(s["jet"]) + emit_at(PLANE, PASS, 0, start)
    one += wait_frames((-start[0] - LADDER_X) / JET_SPEED - 2)
    one += se(s["whoosh"]) + bmove(side, 258, CARRY_FRAMES, JET_SPEED * CARRY_FRAMES, 6) + wait_frames(18)
    one += emit_at(FELICIA, POP, 1, (0, 48)) + se(s["pop"]) + wait_frames(CARRY_FRAMES - 4)
    one += func(40, 2, 1)                                                    # ...gone (SetBattlerVanished)
    start = _jet_from(foe)
    two = se(s["jet"]) + emit_at(PLANE, PASS, 1, start)
    two += wait_frames((-start[0] - LADDER_X) / JET_SPEED - FALL_FRAMES)
    two += emit_at(CLAIM, SUIT, 1, (0, 10 + FALL_SPEED * FALL_FRAMES)) + se(s["whoosh"]) + wait_frames(FALL_FRAMES)
    two += emit_at(PLANE, JETSMOKE, 1, (0, 10)) + flash_screen(8)
    two += se(s["bonk"]) + shake_defender(5, 4) + func(48) + func(68, 5, 2, 1, 4, 0) + wait(14)
    two += bmove(side, 258, 1, 0, 150) + wait(1) + func(40, 2, 0)            # back in, from the sky
    two += bmove(side, 258, 10, 0, -150) + wait(12)
    return one, two


def _hydrant_wave(side, s):
    """Surf: the whole block floods - a wall of water the height of the screen sweeps across both of them,
    a rubber duck riding the crest."""
    blue = rgb(40, 90, 220)
    fx, fy = WAVE_FROM[side]
    sx = 1 if side == "player" else -1
    wave = WAVE_E if side == "player" else WAVE_P
    duck = DUCK_E if side == "player" else DUCK_P
    w = func(33, 0, 1, 0, 10, blue) + se(s["surf"]) + wait(2)
    w += emit_at(WAVE, wave, 1, (fx, fy)) + emit_at(DUCK, duck, 1, (fx - sx * 20, fy + 56)) + wait(5)
    w += emit_at(WAVE, wave, 1, (fx, fy - 26)) + se(s["surf"])
    w += wait_frames(abs(fx) / WAVE_SPEED - 30)
    w += se(s["splash"]) + emit_at(WAVE, FOAM, 1, (0, 10)) + emit_at(WAVE, FOAM, 0, (0, 10))
    w += func(34, 8, 0, 2, blue, 14, 0) + shake_defender(3, 6) + func(68, 3, 2, 1, 4, 0) + wait(8)
    w += emit_at(WAVE, FOAM, 1, (-10, 4)) + se(s["splash"]) + wait(20)
    w += func(33, 0, 1, 10, 0, blue) + wait(6)
    return w


def _power_line(side, s):
    """Thunder: a live power line snaps, swings down on the target and lights them up - you can see the skeleton."""
    night = rgb(10, 10, 40)
    w = func(33, 0, 1, 0, 12, night) + wait(4)
    w += stop_motion(CABLE, POSE, 1, (10, 110), (10, 34), 7)
    w += emit_at(CABLE, HOLD, 1, (10, 34))
    w += se(s["thunder"]) + flash_screen(6) + emit_at(XRAY, SPARKS, 1, (0, 22)) + emit_at(XRAY, BONES, 1, (0, 18))
    for k in range(8):                                                       # BZZZZT
        w += func(34, 3, 0, 1, rgb(0, 0, 0) if k % 2 == 0 else rgb(255, 250, 120), 16, 0)
        w += func(36, 2, 1, 1, 2, 264) + wait(2)
        if k % 3 == 0:
            w += flash_screen(2)
        if k == 4:
            w += se(s["thunder"])
    w += wait(8) + func(33, 0, 1, 12, 0, night) + wait(6)
    return w


def _road_rage(side, s):
    """Dragon Rage: they go red, steam blasting out, HONK! HONK! - and start launching traffic cones."""
    sx = 1 if side == "player" else -1
    w = func(34, 2, 0, 1, rgb(255, 30, 30), 15, 0) + shake_attacker(2, 18)
    w += emit_at(HONK, STEAM, 0, (sx * 6, 36)) + se(s["rage"]) + wait(6)
    w += se(s["alarm"]) + emit_at(HONK, HONK_A, 0, (sx * 34, 54)) + wait(8)
    w += se(s["alarm"]) + emit_at(HONK, HONK_B, 0, (sx * -8, 62)) + wait(6)
    for k in range(3):                                                       # cones, cones, cones
        w += func(9) + _throw(CONE, 1 + k, ((-10, 10, 0)[k], (6, 2, 14)[k])) + wait(4)
    w += wait_frames(THROW_FRAMES - 16)
    for k in range(3):
        w += se(s["bonk"]) + shake_defender(3, 2) + func(34, 4, 0, 1, rgb(255, 140, 40), 10, 0) + wait(4)
    return w + wait(10)


def _molotov2(side, s):
    """Flamethrower (Molotov): a swig of the good stuff, sprayed through a lighter - then the bottle's lobbed."""
    sx = 1 if side == "player" else -1
    orange = rgb(255, 120, 20)
    fire = FIRE_E if side == "player" else FIRE_P
    w = emit_at(BOOZE, SWIG, 0, (sx * 12, 34)) + func(19) + wait(12)          # glug glug
    w += emit_at(BOOZE, LIGHTER, 0, (sx * 22, 26)) + se(s["fwoosh"]) + wait(5)  # *flick*
    w += se(s["flame"]) + emit_at(BREATH, fire, 0, (0, 0)) + func(9) + wait(10)
    w += emit_at(BREATH, fire, 0, (0, 0)) + func(34, 8, 0, 2, orange, 14, 0) + shake_defender(2, 8) + wait(12)
    w += _throw(BOOZE, 1, (0, 4)) + wait_frames(THROW_FRAMES)                 # and the bottle
    w += se(s["smash"]) + emit_at(BURST, TONGUE, 1, (0, -6)) + emit_at(BURST, EMBER, 1, (0, 4)) + flash_screen(6)
    w += shake_defender(4, 4) + func(48) + wait(16)
    return w


def _zaza_leaf(side, s):
    """Razor Leaf (Zaza Leaf): the big leaf rises behind them, the leaves fly like shuriken - and the target's zooted."""
    sx = 1 if side == "player" else -1
    leaf = LEAF_E if side == "player" else LEAF_P
    w = emit_at(LEAF, BIGLEAF, 0, (sx * -16, 42)) + se(s["leaf"]) + wait(10)
    for k in range(3):
        w += se(s["razor"]) + emit_at(LEAF, leaf, 0, (0, 4 * k - 4)) + wait(4)
    w += wait_frames(LEAF_FRAMES - 8)
    w += func(34, 8, 0, 2, rgb(80, 200, 60), 12, 0) + shake_defender(2, 4) + emit_at(HAZE, HAZE1, 1, (0, 16))
    w += wait(6) + func(4, 0, 0x0600, 16, 0) + wait(16)                      # ...whoa
    w += func(4, 0, 0x0600, 16, 2) + wait(18)
    return w


def _stomp_out(side, s):
    """Pound (Stomp Out): a giant boot comes down out of the sky. STOMP!"""
    sx = 1 if side == "player" else -1
    w = stop_motion(BOOT, POSE, 1, (0, 120), (0, 30), 6)
    w += emit_at(BOOT, HOLD, 1, (0, 30))
    w += se(s["bonk"]) + emit_at(STOMP, 2, 1, (sx * -30, 56)) + emit_at(STOMP, DUST, 1, (0, -8))
    w += func(68, 4, 2, 1, 3, 0) + shake_defender(4, 3) + bmove(side, 264, 3, 0, -8) + wait(10)
    w += bmove(side, 264, 8, 0, 8) + wait(10)
    return w


def _grill_chomp(side, s):
    """Bite (Grill Chomp): a mouth full of gold grillz chomps down on them. Twice."""
    w = []
    for chomp in range(2):
        for k in range(4):                                                   # jaws closing
            w += emit_at(TOPJAW, POSE, 1, (0, 50 - 5 * k)) + emit_at(BOTJAW, POSE, 1, (0, -14 + 5 * k)) + wait(1)
        w += emit_at(TOPJAW, HOLD, 1, (0, 32)) + emit_at(BOTJAW, HOLD, 1, (0, 4))
        w += se(s["bite"]) + flash_screen(3) + shake_defender(3, 3) + emit_at(GLITZ, SPARKLE, 1, (0, 18))
        w += func(34, 4, 0, 1, rgb(255, 60, 60), 12, 0) + wait(6)
    return w + wait(8)


def _hollow_point(side, s):
    """Crunch (Hollow Point): a red laser-sight dot dances over them... settles dead centre... BANG."""
    import random
    rnd = random.Random(7)
    w = se(s["leer"])
    for k in range(12):                                                      # the dot hunting, then settling
        a = 20 * (1 - k / 11) ** 1.5
        w += emit_at(SLUG, DOT, 1, (round(rnd.uniform(-a, a)), 22 + round(rnd.uniform(-a, a)))) + wait(1)
    for k in range(4):                                                       # locked on. hold it...
        w += emit_at(SLUG, DOT, 1, (0, 22)) + wait(1)
    w += se(s["boom"]) + muzzle(GUN, FLASH, side) + flash_screen(10)         # BANG
    w += emit_at(SLUG, HOLE, 1, (0, 22)) + emit_at(SLUG, IMPACT, 1, (0, 22)) + emit_at(GUN, SPARK, 1, (0, 22))
    w += se(s["crunch"]) + func(48) + shake_defender(6, 4) + func(68, 5, 3, 1, 4, 0)
    w += func(34, 8, 0, 2, rgb(255, 50, 50), 13, 0) + wait(18)
    return w


def _switchblade(side, s):
    """Slash (Switchblade): the blade flicks open, they dash in - slash, slash, slash - and slash the tire too."""
    sx = 1 if side == "player" else -1
    tire = (sx * 34, -4)
    w = emit_at(TIRE, TIRE_UP, 1, tire) + emit_at(SLASH, GLEAM, 0, (sx * 16, 26)) + se(s["bling"]) + wait(8)
    w += bmove(side, 258, 6, 60, 30) + wait(7)                               # dash in
    for k, res in enumerate((SLASH_A, SLASH_B, SLASH_C)):
        w += se(s["slash"]) + emit_at(SLASH, res, 1, ((-4, 4, 0)[k], (20, 14, 18)[k])) + shake_defender(2, 2)
        w += func(34, 3, 0, 1, rgb(255, 60, 60), 10, 0) + wait(3)
    w += se(s["slash"]) + emit_at(SLASH, SLASH_B, 1, tire) + wait(2)          # ...and the tire
    w += emit_at(TIRE, TIRE_FLAT, 1, (tire[0], tire[1] - 3)) + emit_at(TIRE, HISS, 1, tire) + se(s["spray"])
    w += bmove(side, 258, 8, -60, -30) + wait(14)
    return w


def _hot_box(side, s):
    """SmokeScreen (Hot Box): they hotbox the whole battlefield. Can't see a thing. *cough* *cough*"""
    sx = 1 if side == "player" else -1
    haze = rgb(110, 120, 100)
    w = func(33, 0, 1, 0, 11, haze) + se(s["smoke"]) + emit_at(SMOG, SMOG1, 0, (sx * 24, 24)) + wait(8)
    w += emit_at(SMOG, SMOG1, 1, (0, 20)) + emit_at(SMOG, SMOG2, 1, (0, 10)) + wait(10)
    for k in range(3):
        w += emit_at(COUGH, PUFFUP, 1, ((k - 1) * 14, 42 + (k % 2) * 6)) + se(s["cough"])
        w += shake_defender(2, 3) + func(34, 4, 0, 1, rgb(170, 175, 160), 12, 0) + wait(8)
    w += wait(12) + func(33, 0, 1, 11, 0, haze) + wait(6)
    return w


def _burnout(side, s):
    """Flame Wheel (Burnout): the tire spins in place in a cloud of smoke and catches fire - then it's launched."""
    sx = 1 if side == "player" else -1
    at = (sx * 22, 10)
    w = emit_at(WHEEL, SPIN, 0, at) + emit_at(WHEEL, SMOKE1, 0, at) + se(s["burn"]) + shake_attacker(1, 14)
    w += wait(14)
    w += se(s["burn2"]) + _fly(WHEEL, ROLL, 1, ROLL_FRAMES) + _fly(TRAIL, FIRETRAIL, 2, ROLL_FRAMES)
    w += wait_frames(ROLL_FRAMES)
    w += emit_at(BURST, TONGUE, 1, (0, -6)) + emit_at(BURST, EMBER, 1, (0, 4)) + se(s["fwoosh"])
    w += func(34, 8, 0, 2, rgb(255, 120, 20), 14, 0) + shake_defender(4, 4) + func(48) + wait(16)
    return w


def _hi_yah(side, s):
    """Brick Break (Hi-Yah Chop): a stack of bricks balanced on their head; a giant karate hand comes down -
    HI-YAH! - the stack splits clean in two and the chop lands on their head."""
    sx = 1 if side == "player" else -1
    top = 48                                                                 # the stack, on their head
    w = []
    for k in range(9):                                                       # the hand comes down on it
        t = (k / 8) ** 1.6
        w += emit_at(BLOCKS, HALF_L, 1, (0, top)) + emit_at(BLOCKS, HALF_R, 1, (0, top))
        w += emit_at(CHOP, POSE, 1, (0, round(128 - (128 - (top + 30)) * t))) + wait(1)
    w += se(s["chop"]) + emit_at(HIYAH, POP, 1, (sx * -34, 70)) + flash_screen(5)
    w += emit_at(BLOCKS, CHUNKS, 1, (0, top))
    for k in range(1, 7):                                                    # CRACK - in two, flying apart
        dx, dy = 6 * k, top - (k * k) // 2
        w += emit_at(BLOCKS, HALF_L, 1, (-dx, dy)) + emit_at(BLOCKS, HALF_R, 1, (dx, dy))
        if k < 4:
            w += emit_at(CHOP, POSE, 1, (0, top + 30 - 6 * k))
        w += wait(1)
    w += emit_at(CHOP, HOLD, 1, (0, top + 8)) + se(s["bonk"])                # ...right on the head
    w += shake_defender(4, 4) + bmove(side, 264, 3, 0, -8) + func(68, 3, 2, 1, 3, 0) + wait(8)
    w += bmove(side, 264, 8, 0, 8) + wait(10)
    return w


def _magic_8ball(side, s):
    """Shadow Ball (Magic 8-Ball): a Magic 8-Ball grows in their hands in dark wisps, rolls over and gives
    the answer: OUTLOOK NOT GOOD."""
    sx = 1 if side == "player" else -1
    dark = rgb(40, 10, 60)
    w = func(33, 0, 1, 0, 11, dark) + emit_at(EIGHT, CHARGE, 0, (sx * 4, 26))
    w += emit_at(EIGHT, WISPS, 0, (sx * 4, 24)) + se(s["shadow"]) + wait(10)
    w += _fly(EIGHT, ROLL8, 1, EIGHT_FRAMES) + wait_frames(EIGHT_FRAMES)
    w += se(s["shadow2"]) + emit_at(ANSWER, POP, 1, (sx * -34, 50)) + flash_screen(4)
    w += func(34, 8, 0, 2, rgb(120, 40, 200), 14, 0) + shake_defender(3, 4) + func(48) + wait(18)
    w += func(33, 0, 1, 11, 0, dark) + wait(6)
    return w


def _loyalty(side, s):
    """Return (Loyalty): RIDE OR DIE. The pendant glows, the love flies - and then it hits them for real."""
    sx = 1 if side == "player" else -1
    pink = rgb(255, 120, 180)
    hearts = HEARTS_E if side == "player" else HEARTS_P
    w = emit_at(HEART, LOCKET, 0, (sx * 10, 46)) + se(s["loyal"]) + func(34, 2, 0, 1, pink, 10, 0) + wait(10)
    for k in range(3):
        w += emit_at(HEART, hearts, 0, (0, 2 * k)) + se(s["loyal2"]) + wait(4)
    w += _fly(HEART, SLAM, 1, HEART_FRAMES) + wait_frames(HEART_FRAMES)
    w += flash_screen(6) + func(34, 8, 0, 2, pink, 14, 0) + shake_defender(4, 4) + func(48) + se(s["bonk"])
    return w + wait(14)


def _chain_dangle(side, s):
    """Confusion: a quicker dangle, no lights-down."""
    return _chain_swing(side, s, swings=2, dark=False)


# ------------------------------------------------------------------ set 5: the everyday moves

def _flashlight(side, s):
    """Confuse Ray (Flashlight): lights out - *click* - a flashlight right in their eyes. Swirly-eyed. HUH?!"""
    sx = 1 if side == "player" else -1
    _, _, beam, _ = torch_geometry(side)
    night = rgb(5, 5, 25)
    w = func(33, 0, 1, 0, 12, night) + wait(4)
    w += emit_at(TORCH, TORCH_E if side == "player" else TORCH_P, 0, TORCH_AT[side]) + se(s["confuse"]) + wait(8)
    w += emit_at(BEAM, BEAM_E if side == "player" else BEAM_P, 0, beam) + flash_screen(3)       # *click*
    w += func(34, 8, 0, 2, rgb(255, 255, 220), 15, 0) + func(36, 2, 0, 1, 4, 264) + wait(10)   # blinded
    w += se(s["confuse2"]) + emit_at(TORCH, SWIRL, 1, (-7, 24)) + emit_at(TORCH, SWIRL, 1, (7, 24))
    w += func(4, 0, 0x0900, 10, 0) + wait(8)
    w += emit_at(HUH, POP, 1, (sx * -30, 58)) + wait(8)
    w += func(4, 0, 0x0900, 10, 2) + se(s["confuse2"]) + wait(14)
    w += func(33, 0, 1, 12, 0, night) + wait(6)
    return w


def _stun_taser(side, s):
    """Thunder Wave (Stun Taser): the stun gun snaps, crackles shoot over, rings of static lock them up stiff."""
    sx = 1 if side == "player" else -1
    w = emit_at(STUN, STUN_E if side == "player" else STUN_P, 0, STUN_AT[side]) + se(s["twave"]) + wait(6)
    w += emit_at(STUN, ARC_E if side == "player" else ARC_P, 0, STUN_TIP[side]) + func(9)
    w += wait_frames(STUN_FRAMES + 4)
    w += se(s["twave2"]) + emit_at(STATIC, RING_X, 1, (0, 20)) + emit_at(STATIC, RING_HOLD, 1, (0, 20))
    w += flash_screen(3)
    for k in range(9):                                                       # locked up, twitching (ends lit)
        if k in (2, 5):
            w += emit_at(STATIC, RING_X, 1, (0, 20))
        if k == 3:
            w += se(s["twave2"]) + emit_at(ZZZT, POP, 1, (sx * -30, 58))
        w += func(34, 8, 0, 1, rgb(255, 255, 80) if k % 2 == 0 else rgb(30, 30, 70), 14, 0)
        w += func(36, 2, 0, 1, 2, 264) + wait(2)
    w += func(36, 1, 0, 1, 8, 264) + wait(14)
    return w


def _bass_boost(side, s):
    """Supersonic (Bass Boost): a boombox up on their shoulder, bass so heavy the target's head rattles."""
    sx = 1 if side == "player" else -1
    at = BOX_AT[side]
    notes, wave = (NOTES_E, SWAVE_E) if side == "player" else (NOTES_P, SWAVE_P)
    w = emit_at(BOOMBOX, BOX5, 0, at) + wait(8)
    for k in range(4):                                                       # BWOMP. BWOMP. BWOMP. BWOMP.
        w += se(s["bass"]) + emit_at(BOOMBOX, THUMP, 0, at) + emit_at(SOUNDWAVE, wave, 0, at)
        if k % 2 == 0:
            w += emit_at(BOOMBOX, notes, 0, at)
        w += func(68, 2, 1, 1, 2, 0) + func(36, 1, 1, 1, 2, 258)
        if k:
            w += func(4, 0, 0x0A00, 4, 0 if k % 2 else 2)                    # head bobbing (it can't help it)
        w += wait(5)
    w += emit_at(BWOMP, POP, 1, (sx * -30, 58)) + func(68, 4, 2, 1, 3, 0) + shake_defender(3, 5)
    w += func(34, 8, 0, 2, rgb(255, 120, 220), 12, 0) + wait(16)
    return w


SQUAD_SPOTS = {"player": [(-44, 6), (46, 6), (98, 58)], "enemy": [(42, 4), (-42, 4), (-78, 12)]}
#                 (the player's third homie: back row, smaller, standing up above the HP box - it draws over him)


def _squad_up(side, s):
    """Double Team (Squad Up): poof, poof, poof - the whole squad's standing behind them. SQUAD UP!"""
    big = side == "player"                                                   # near side: the homies are bigger
    figs = [(SQUAD, FIG if big else FIG_S), (SQUAD2, FIG2 if big else FIG2_S), (SQUAD, FIG_S)]
    dim = rgb(40, 20, 70)
    w = func(33, 0, 1, 0, 8, dim) + se(s["dteam"]) + func(19)
    for k, (x, y) in enumerate(SQUAD_SPOTS[side]):
        w += emit_at(SQUAD, POOF, 0, (x, y)) + emit_at(*figs[k], 0, (x, y))
        if k == 2:
            w += se(s["dteam"])
        w += wait(3)
    w += shake_attacker(2, 8) + emit_at(SQUADUP, POP, 0, (0, 62 if big else 50)) + wait(14)
    for x, y in SQUAD_SPOTS[side]:                                           # ...and they're gone
        w += emit_at(SQUAD, POOF, 0, (x, y)) + wait(3)
    w += wait(6) + func(33, 0, 1, 8, 0, dim) + wait(4)
    return w


def _water_bomb(side, s):
    """Water Pulse (Water Bomb): a water balloon lobbed right on them. SPLOOSH. Dripping and dazed."""
    sx = 1 if side == "player" else -1
    blue = rgb(60, 140, 255)
    w = func(19) + se(s["wpulse"]) + wait(4) + _throw(BALLOON, 1, (0, 16)) + wait_frames(THROW_FRAMES)
    w += se(s["wpulse2"]) + emit_at(DRENCH, CROWN, 1, (0, 14)) + emit_at(DRENCH, SPLASHDROPS, 1, (0, 22))
    w += flash_screen(3) + func(34, 8, 0, 2, blue, 14, 0) + shake_defender(3, 4) + wait(4)
    w += emit_at(SPLOOSH, POP, 1, (sx * -30, 58)) + emit_at(BALLOON, DROPS, 1, (0, 14)) + wait(8)
    w += func(4, 0, 0x0700, 10, 0) + wait(10) + func(4, 0, 0x0700, 10, 2) + wait(14)
    return w


def _sneak_diss(side, s):
    """Faint Attack (Sneak Diss): they vanish - "UR MID" pops up behind the target - and a palm comes down on the
    back of their head. OOOOH!"""
    sx = 1 if side == "player" else -1
    w = se(s["faint"]) + func(36, 2, 0, 1, 3, 258) + wait(4) + func(40, 2, 1) + wait(8)      # gone
    w += emit_at(DISS, POP, 1, (sx * 26, 42)) + se(s["leer"]) + wait(6)                    # from behind them
    w += func(4, 0, 0x0800, 8, 0) + wait(12)                                                # ...huh?
    w += stop_motion(SLAP, SLAP_POSE, 1, (sx * 14, 96), (sx * 4, 40), 4)
    w += emit_at(SLAP, SLAP_HOLD, 1, (sx * 4, 38)) + se(s["bonk"]) + emit_at(SLAP, POWS, 1, (0, 34))
    w += flash_screen(4) + func(48) + shake_defender(4, 3) + bmove(side, 264, 3, 0, -6) + wait(4)
    w += emit_at(OOOH, POP, 1, (sx * -32, 56)) + func(4, 0, 0x0800, 8, 2) + bmove(side, 264, 6, 0, 6) + wait(14)
    w += func(40, 2, 0) + func(36, 2, 0, 1, 3, 258) + wait(8)                               # back, innocent
    return w


def _dirty_sprite(side, s):
    """Toxic (Dirty Sprite): a double cup of the purple stuff - thrown. It's all over them and they're bubbling."""
    sx = 1 if side == "player" else -1
    purple = rgb(160, 60, 230)
    w = emit_at(CUP, HELD, 0, (sx * 22, 30)) + se(s["toxic"]) + func(19) + wait(8)
    w += _throw(CUP, 1, (0, 18)) + wait_frames(THROW_FRAMES)
    w += se(s["splat"]) + emit_at(GOOP, GOOP_SPLAT, 1, (0, 22)) + emit_at(GOOP, GOOP_DRIPS, 1, (0, 18))
    w += func(34, 8, 0, 2, purple, 14, 0) + shake_defender(3, 3) + wait(4)
    w += emit_at(CUP, BUBBLES, 1, (0, 10)) + se(s["toxic2"]) + emit_at(DIRTY, POP, 1, (sx * -30, 58))
    for k in range(3):                                                       # badly poisoned: pulsing purple
        w += func(34, 8, 0, 1, purple, 12, 0) + func(36, 2, 0, 1, 2, 264) + wait(6)
        if k == 1:
            w += se(s["toxic2"])
    return w + wait(12)


def _duck_n_cover(side, s):
    """Protect (Duck n Cover): they duck behind a trash-can lid and everything pings right off it. NOPE."""
    sx = 1 if side == "player" else -1
    # the enemy holds it up in front of itself; the player's Pokémon (seen from behind) holds it out towards
    # the foe, up in the middle of the screen - drawn over their back it'd look like it was behind them
    at = LID_AT[side]
    w = bmove(side, 258, 3, 0, -10) + emit_at(LID, LIDUP, 0, at) + se(s["protect"]) + wait(6)   # duck!
    w += emit_at(LID, LIDFLASH, 0, at) + flash_screen(3) + func(34, 2, 0, 1, rgb(200, 230, 255), 12, 0) + wait(5)
    for dx, dy in ((10, 14), (-8, 4), (6, -10)):                             # ping. ping. ping.
        w += emit_at(LID, PINGS, 0, (at[0] + sx * dx, at[1] + dy)) + se(s["bling"])
        w += func(36, 1, 0, 1, 2, 258) + wait(4)
    w += emit_at(NOPE, POP, 0, (at[0] + sx * 4, 58)) + wait(14)
    w += bmove(side, 258, 6, 0, 10) + wait(8)
    return w


def _smackdown(side, s):
    """Take Down (Smackdown): they charge in with a steel folding chair - CLANG - and stagger back seeing stars."""
    sx = 1 if side == "player" else -1
    w = bmove(side, 258, 4, -8, -4) + se(s["tdown"]) + wait(6)               # winding up
    w += bmove(side, 258, 6, 72, 36) + wait(6)                               # CHARGE
    w += stop_motion(CHAIR, CHAIR_POSE, 1, (sx * -20, 100), (0, 40), 4)
    w += emit_at(CHAIR, CHAIR_HOLD, 1, (0, 36)) + se(s["tdown2"]) + emit_at(CLANG, POP, 1, (0, 24))
    w += emit_at(SMACKDN, POP, 1, (sx * -36, 62)) + flash_screen(8) + func(48) + shake_defender(6, 4)
    w += func(68, 5, 3, 1, 4, 0) + bmove(side, 264, 3, 0, -8) + wait(8)
    w += bmove(side, 264, 8, 0, 8) + bmove(side, 258, 8, -64, -32) + wait(10)               # back off
    w += se(s["bonk"]) + shake_attacker(2, 4)                                                # the recoil
    for k in range(10):                                                      # seeing stars
        a = k * math.pi / 4
        for ph in (0, math.pi):
            w += emit_at(CHAIR, STARS, 0, (round(14 * math.cos(a + ph)), round(44 + 4 * math.sin(a + ph))))
        w += wait(2)
    return w + wait(4)


def _big_taser(side, s):
    """Thunderbolt (Big Taser): an XL taser held up high, crackling - and a giant bolt drops out of the sky."""
    sx = 1 if side == "player" else -1
    night = rgb(10, 10, 40)
    at = (sx * 18, 58)
    w = func(33, 0, 1, 0, 12, night) + emit_at(BIGTASER, BIG_E if side == "player" else BIG_P, 0, at) + wait(6)
    w += emit_at(BIGTASER, ZIGS, 0, at) + se(s["tbolt"]) + shake_attacker(1, 14) + wait(14)   # charging up
    w += emit_at(MEGABOLT, STRIKE, 1, (0, 54)) + se(s["tbolt2"]) + flash_screen(8)            # KRAKOOM
    w += emit_at(MEGABOLT, STRIKE2, 1, (sx * 10, 70)) + emit_at(BIGTASER, ZIGS, 1, (0, 16))
    for k in range(9):                                                       # (ends on the lit step)
        if k == 2:
            w += emit_at(BZZT, POP, 1, (sx * -34, 60))
        if k == 4:
            w += emit_at(MEGABOLT, STRIKE2, 1, (sx * -12, 66)) + flash_screen(3) + se(s["tbolt2"])
        w += func(34, 8, 0, 1, rgb(255, 250, 90) if k % 2 == 0 else rgb(0, 0, 0), 16, 0)
        w += func(36, 2, 1, 1, 2, 264) + wait(2)
    w += func(48) + wait(10) + func(33, 0, 1, 12, 0, night) + wait(6)
    return w


def _clock_it(side, s):
    """Foresight (Clock It): the eyes emoji over their head, looking away... looking away... SNAP - right at the
    target. BWOMM: red circle, red arrow, U GOT CLOCKED."""
    sx = 1 if side == "player" else -1
    at = (sx * 4, 62)
    look_at, look_away = (EYES_R, EYES_L) if side == "player" else (EYES_L, EYES_R)
    w = se(s["clock"])
    for k in range(5):                                                       # whistling, minding their business
        w += emit_at(EYES, look_away, 0, (at[0] - sx * (k % 2), at[1])) + wait(2)
    w += se(s["leer"])
    for k in range(5):                                                       # ...wait.
        w += emit_at(EYES, look_at, 0, (at[0] + sx * (2 if k == 0 else 0), at[1])) + wait(2)
    w += se(s["vineboom"]) + emit_at(CIRCLE, POP, 1, (sx * -2, 16)) + flash_screen(4)       # BWOMM
    w += func(68, 6, 3, 1, 3, 0) + func(33, 0, 1, 0, 6, rgb(60, 0, 0))
    for k in range(8):                                                       # staring them down the whole time
        w += emit_at(EYES, look_at, 0, at) + wait(2)
        if k == 2:
            w += emit_at(CLOCKED, POP, 1, (sx * -34, 62)) + shake_defender(2, 4)
    for k in range(6):
        w += emit_at(EYES, look_at, 0, at) + wait(2)
    w += func(33, 0, 1, 6, 0, rgb(60, 0, 0)) + wait(6)
    return w


# ------------------------------------------------------------------ set 6

def _belt_whip(side, s):
    """Vine Whip (Belt Whip): the belt comes off - CRACK, CRACK - buckle first. A $ welt, and WHAP!"""
    sx = 1 if side == "player" else -1
    swing = BELT_E if side == "player" else BELT_P
    w = bmove(side, 258, 6, 50, 25) + se(s["whoosh"]) + wait(8)                # step in
    for k in range(2):
        w += emit_at(BELT, swing, 1, (sx * -30, 8 + 6 * k)) + se(s["vwhip"]) + wait(3)
        w += se(s["vwhip2"]) + emit_at(WELT, SNAPS, 1, (sx * 4, 22 - 8 * k)) + flash_screen(3)
        w += emit_at(WELT, WELT1, 1, (sx * 2, 24 - 10 * k)) + shake_defender(3, 3)
        w += func(34, 3, 0, 1, rgb(255, 60, 60), 12, 0) + wait(5)
    w += emit_at(WHAP, POP, 1, (sx * -32, 60)) + func(48) + func(68, 4, 2, 1, 3, 0) + wait(10)
    w += bmove(side, 258, 8, -50, -25) + wait(12)
    return w


def _shiv(side, s):
    """Poison Sting (Shiv): they dash in - jab, jab, jab - with a toothbrush shiv. Skulls float off them. SHIV'D!"""
    sx = 1 if side == "player" else -1
    jab = SHIV_E if side == "player" else SHIV_P
    green = rgb(110, 230, 50)
    w = bmove(side, 258, 6, 64, 32) + se(s["whoosh"]) + wait(7)                # dash in
    for k in range(3):
        y = (20, 12, 26)[k]
        w += emit_at(SHIV, jab, 1, (sx * -46, y)) + wait(1)                    # pull back...
        w += emit_at(SHIV, jab, 1, (sx * -20, y)) + se(s["psting"])           # ...STAB
        w += shake_defender(2, 2) + func(34, 3, 0, 1, green, 12, 0) + wait(1)
    w += se(s["psting2"]) + emit_at(SHIV, SKULLS, 1, (0, 20)) + emit_at(SHIVD, POP, 1, (sx * -32, 60))
    w += bmove(side, 258, 8, -64, -32) + wait(6)
    for k in range(3):                                                         # poisoned: pulsing green
        w += func(34, 8, 0, 1, green, 12, 0) + func(36, 2, 0, 1, 2, 264) + wait(6)
    return w + wait(6)


def _twerk(side, s):
    """Tail Whip (Twerk On Em): they turn round and twerk on the foe - wiggle wiggle wiggle - so disrespectful the
    foe's guard drops: the DEF shield cracks, they flinch back. BRUH."""
    sx = 1 if side == "player" else -1
    w = se(s["twhip"]) + bmove(side, 258, 3, 0, -6) + wait(3)                   # drop it low
    for k in range(10):                                                        # wiggle wiggle wiggle
        d = 1 if k % 2 == 0 else -1
        w += bmove(side, 258, 2, 9 * d, 4 * d)
        w += emit_at(TWERK, WIGGLE_R if d > 0 else WIGGLE_L, 0, (d * 30, 14))
        if k == 5:
            w += se(s["twhip"])
        w += wait(1)
    w += bmove(side, 258, 3, 0, 6) + wait(3)
    w += emit_at(DEFDOWN, POP, 1, (sx * -34, 34)) + se(s["leer"]) + func(34, 8, 0, 2, rgb(80, 140, 255), 13, 0)
    w += emit_at(BRUH, POP, 1, (sx * -30, 62)) + bmove(side, 264, 8, sx * 12, 0) + wait(6)
    w += func(36, 2, 0, 1, 6, 264) + wait(14)                                  # shook
    w += bmove(side, 264, 8, -sx * 12, 0) + wait(10)
    return w


def _tax(side, s):
    """Absorb (Tax): an IRS stamp comes down on them - TAXED - and their coins pour into the user's money bag."""
    sx = 1 if side == "player" else -1
    w = stop_motion(STAMP, POSE, 1, (0, 100), (0, 34), 5)
    w += emit_at(STAMP, HOLD, 1, (0, 34)) + se(s["bonk"]) + emit_at(TAXED, POP, 1, (0, 18)) + flash_screen(3)
    w += shake_defender(4, 3) + func(68, 3, 2, 1, 2, 0) + wait(8)
    w += emit_at(COINS, MONEYBAG, 0, BAG_SPOT[side]) + se(s["absorb"]) + wait(4)
    w += emit_at(COINS, COIN_E if side == "player" else COIN_P, 1, (0, 20))
    w += func(34, 8, 0, 1, rgb(40, 40, 60), 10, 0) + wait_frames(COIN_FRAMES)
    for k in range(3):                                                         # cha-ching
        if k != 1:
            w += se(s["bling"])
        w += func(34, 2, 0, 1, rgb(120, 255, 120), 12, 0) + wait(6)
    w += se(s["absorb2"]) + wait(12)
    return w


def _silly_string(side, s):
    """String Shot (Silly String): a can of neon silly string, shaken up - PSSSHHH - all over them. STUCK!"""
    sx = 1 if side == "player" else -1
    at = CAN_AT[side]
    nozzle = (at[0], at[1] + NOZZLE_UP)
    w = emit_at(CAN, CAN1, 0, at) + wait(6) + shake_attacker(2, 6) + wait(8)    # shake it up
    for k in range(3):
        w += se(s["sshot"]) + emit_at(CAN, STR_E if side == "player" else STR_P, 0, nozzle) + wait(5)
    w += wait_frames(STRING_FRAMES - 8)
    w += emit_at(TANGLE, TANGLED, 1, (0, 22)) + se(s["sshot2"]) + wait_frames(10)
    w += emit_at(TANGLE, TANGLE_HOLD, 1, (0, 22)) + func(34, 8, 0, 2, rgb(255, 80, 190), 12, 0)
    w += emit_at(STUCK, POP, 1, (sx * -32, 60)) + bmove(side, 264, 6, 0, -5) + wait(4)
    for k in range(3):                                                         # struggling, slow
        w += func(36, 1, 0, 1, 3, 264) + wait(6)
    w += bmove(side, 264, 10, 0, 5) + wait(10)
    return w


def _spit(side, s):
    """Bubble (Spit): they lean way back... hawk... PTOO! A loogie lobs over and splats right on them. Running."""
    sx = 1 if side == "player" else -1
    w = bmove(side, 258, 8, -8, 5) + se(s["bubble"]) + wait(10)                # hhhhwwk...
    w += bmove(side, 258, 3, 16, -8) + emit_at(PTOO, POP, 0, (sx * 30, 56)) + wait(2)   # PTOO
    w += _throw(SPIT, 1, (0, 22)) + bmove(side, 258, 6, -8, 3) + wait_frames(THROW_FRAMES) + wait(1)
    w += se(s["splat"]) + emit_at(GOBSPLAT, POP, 1, (0, 22)) + emit_at(SPIT, DRIBBLE, 1, (0, 16))
    w += func(34, 8, 0, 2, rgb(190, 240, 150), 13, 0) + shake_defender(3, 3) + wait(6)
    w += func(4, 0, 0x0700, 10, 0) + wait(10) + func(4, 0, 0x0700, 10, 2) + wait(18)   # ew
    return w


# ------------------------------------------------------------------ set 7

def _lace_up(side, s):
    """Agility (Lace Up): a fresh pair of kicks pops in, *bling* - and they're zipping side to side. LACED UP!"""
    sx = 1 if side == "player" else -1
    w = emit_at(KICKS, SHOES, 0, (sx * 6, -10)) + se(s["bling"]) + wait(8)
    w += func(34, 2, 0, 1, rgb(255, 245, 140), 12, 0) + wait(8)
    for k, d in enumerate((1, -1, -1, 1, 1, -1, -1, 1)):                  # zip zip (nets to zero)
        w += bmove(side, 258, 2, d * 22, 0) + emit_at(KICKS, ZOOMS, 0, (-d * 18, 12 + 6 * (k % 2)))
        if k % 2 == 0:
            w += se(s["smoke"])
        w += wait(1)
    w += emit_at(LACED, POP, 0, (sx * 30, 62 if side == "player" else 52))
    w += func(34, 2, 0, 1, rgb(255, 245, 140), 12, 0) + wait(16)
    return w


def _go_out_loud(side, s):
    """Selfdestruct (Go Out Loud): they light a crate of fireworks... fizzzz... and the whole sky goes off. BOOOM!"""
    sx = 1 if side == "player" else -1
    crate = (sx * -26, 20)
    w = emit_at(CRATE, BOX7, 0, crate) + wait(6)
    w += emit_at(CRATE, FUSE, 0, (crate[0] + 22, crate[1] + 24)) + se(s["sdestruct"]) + shake_attacker(1, 16)
    w += wait(18)
    w += se(s["kaboom"]) + flash_screen(10) + func(68, 8, 4, 1, 5, 0)                      # BOOOM
    for who, (x, y) in ((0, (0, 20)), (0, (sx * 62, 46)), (1, (0, 20))):
        w += emit_at(FWBURST, POP, who, (x, y)) + emit_at(CRATE, GLITTER, who, (x, y))
    w += emit_at(BOOOM, POP, 0, (sx * 60, 70)) + shake_defender(5, 5)
    w += func(34, 8, 0, 2, rgb(255, 200, 80), 15, 0) + wait(8)
    for who, (x, y) in ((0, (sx * 30, 64)), (1, (sx * -26, 46)), (0, (sx * 96, 24))):       # ...and the finale
        w += se(s["boom"]) + emit_at(FWBURST, 1, who, (x, y)) + emit_at(CRATE, GLITTER, who, (x, y))
        w += flash_screen(3) + wait(5)
    return w + wait(14)


def _roll_out(side, s):
    """Rollout (Roll Out): they come barrelling in riding a shopping cart and smash into them - CRASH."""
    sx = 1 if side == "player" else -1
    cart = CART if side == "player" else CARTL
    rx, ry = CART_RUN
    w = bmove(side, 258, 4, -sx * 6, -sx * 3) + wait(4)                         # wind up
    w += emit_at(cart, CART_GO, 0, (0, 6)) + bmove(side, 258, CART_FRAMES, sx * rx, sx * ry) + se(s["rollout"])
    w += wait_frames(CART_LIFE / 2) + se(s["rollout"]) + wait_frames(CART_LIFE / 2 - 2)
    w += se(s["rollout2"]) + se(s["bonk"]) + emit_at(cart, CART_FLIP, 1, (sx * -18, -4)) + flash_screen(5)
    w += emit_at(CRASH, POP, 1, (sx * -30, 60)) + func(48) + shake_defender(5, 4) + func(68, 5, 3, 1, 4, 0)
    w += wait(10)
    w += bmove(side, 258, 10, -sx * (rx - 6), -sx * (ry - 3)) + wait(14)        # walk it off
    return w


def _lock_in(side, s):
    """Focus Energy (Lock In): headphones on, lights down red, everything pulls in towards them. LOCKED IN."""
    sx = 1 if side == "player" else -1
    head = (0, 46 if side == "player" else 36)
    dark = rgb(50, 0, 0)
    w = func(33, 0, 1, 0, 10, dark) + emit_at(PHONES, CANS, 0, head) + se(s["focus"]) + wait(8)
    w += emit_at(PHONES, MOTES, 0, (0, 22))
    for k in range(3):                                                          # boom, boom, boom
        w += emit_at(PHONES, CANS_THUMP, 0, head) + se(s["bass"]) + func(34, 2, 0, 1, rgb(255, 40, 40), 13, 0)
        w += func(36, 1, 0, 1, 2, 258) + wait(7)
    w += emit_at(LOCKED, POP, 0, (sx * 34, 66 if side == "player" else 54)) + wait(16)
    w += func(33, 0, 1, 10, 0, dark) + wait(6)
    return w


def _dome_check(side, s):
    """Headbutt (Dome Check): a running headbutt straight to the dome - BONK - and a big bump swells up."""
    sx = 1 if side == "player" else -1
    w = bmove(side, 258, 4, -8, -4) + wait(5)                                   # head down...
    w += bmove(side, 258, 5, 72, 36) + se(s["tdown"]) + wait(5)                 # CHARGE
    w += se(s["bonk"]) + flash_screen(5) + func(48) + shake_defender(5, 3) + func(68, 4, 2, 1, 3, 0)
    w += emit_at(BUMP, POP, 1, (sx * -4, 34)) + wait(4)
    w += bmove(side, 258, 8, -64, -32) + emit_at(DOMECHK, POP, 1, (sx * -34, 62)) + wait(8)
    for k in range(2):                                                          # throb... throb
        w += emit_at(BUMP, 1, 1, (sx * -4, 34)) + func(34, 3, 0, 1, rgb(255, 80, 100), 10, 0) + wait(8)
    return w + wait(6)


def _pickpocket(side, s):
    """Fury Swipes (Pickpocket): a hand dips into their pocket... and comes back up with the wallet. YOINK!
    (multi-hit: this plays once per hit, so it's quick)"""
    sx = 1 if side == "player" else -1
    x = sx * -10
    w = stop_motion(GRAB, POSE, 1, (x, 96), (x, 30), 3)
    w += emit_at(GRAB, HOLD, 1, (x, 28)) + se(s["swipe"]) + shake_defender(2, 2) + wait(3)
    w += stop_motion(YANK, POSE, 1, (x, 30), (x, 96), 4, ease=.7)
    w += emit_at(YOINK, POP, 1, (sx * -34, 58)) + se(s["bling"]) + func(34, 3, 0, 1, rgb(120, 230, 110), 10, 0)
    return w + wait(12)


# ------------------------------------------------------------------ set 8

def _pool_float(side, s):
    """Aqua Ring (Pool Float): a sprinkle-donut pool float round their waist - ripples, bobbing. CHILLIN'."""
    sx = 1 if side == "player" else -1
    w = emit_at(POOLF, FLOATIE, 0, (0, 2)) + se(s["aring"]) + wait(6)
    for k in range(3):                                                         # bob... bob... bob
        w += emit_at(POOLF, RIPPLES, 0, (0, -4)) + bmove(side, 258, 6, 0, 4) + wait(4)
        w += bmove(side, 258, 6, 0, -4) + func(34, 2, 0, 1, rgb(90, 190, 255), 11, 0) + wait(4)
    w += emit_at(CHILLIN, POP, 0, (sx * 30, 62 if side == "player" else 52)) + se(s["splash"]) + wait(18)
    return w


def _block_off(side, s):
    """Mean Look (Block Off): lights down, CAUTION tape slapped across them in an X, a ROAD CLOSED barricade
    drops in front. NO EXIT."""
    sx = 1 if side == "player" else -1
    dark = rgb(40, 30, 0)
    w = func(33, 0, 1, 0, 10, dark) + se(s["mlook"]) + wait(6)
    w += emit_at(TAPE, TAPE_A, 1, (0, 26)) + se(s["slash"]) + shake_defender(2, 2) + wait(5)
    w += emit_at(TAPE, TAPE_B, 1, (0, 26)) + se(s["slash"]) + shake_defender(2, 2) + wait(6)
    w += emit_at(BARRIER, POP, 1, (sx * -30, -6)) + se(s["bonk"]) + func(68, 3, 2, 1, 2, 0) + wait(6)
    w += emit_at(NOEXIT, POP, 1, (sx * -36, 62)) + se(s["mlook2"]) + wait(22)
    w += func(33, 0, 1, 10, 0, dark) + wait(6)
    return w


def _cheap_shot(side, s):
    """Sucker Punch (Cheap Shot): "YO LOOK!!" - the foe glances away - and a fist comes right at them."""
    sx = 1 if side == "player" else -1
    w = emit_at(LOOKBUB, POP, 0, (sx * 28, 58)) + se(s["leer"]) + wait(10)
    w += bmove(side, 264, 4, sx * 6, 0) + wait(6)                              # ...huh? where?
    w += stop_motion(FIST, POSE, 1, (sx * -60, 30), (sx * -6, 24), 3, ease=1)
    w += emit_at(FIST, HOLD, 1, (sx * -4, 24)) + se(s["sucker"]) + se(s["bonk"]) + flash_screen(4)
    w += func(48) + shake_defender(4, 3) + emit_at(CHEAP, POP, 1, (sx * -32, 60)) + wait(12)
    w += bmove(side, 264, 6, -sx * 6, 0) + wait(10)
    return w


def _jam_gun(side, s):
    """Disable (Jam the Gun): their gun pops up over them... click... click... a sad sputter. JAMMED!"""
    sx = 1 if side == "player" else -1
    w = emit_at(JAMGUN, GUNUP, 1, (sx * -36, 30)) + wait(8)
    for k in range(2):                                                         # click... click...
        w += se(s["disable"]) + emit_at(JAMGUN, SPUTTERS, 1, (sx * -34, 60)) + wait(8)
    w += emit_at(JAMMED, POP, 1, (sx * 6, 60)) + se(s["faint"]) + flash_screen(2)
    w += func(34, 8, 0, 2, rgb(120, 120, 135), 13, 0) + func(36, 1, 0, 1, 3, 264) + wait(20)
    return w


def _sleeper(side, s):
    """Sleep Powder (Sleeper): a fat lit cigar pops in their mouth. One long drag... smoke rings... they sink,
    eyes heavy, lights dim. Zzz. NIGHT NIGHT."""
    sx = 1 if side == "player" else -1
    cig = CIGAR_L if side == "player" else CIGAR_R                            # sticking out towards the attacker
    mouth = (sx * -24, 16)
    w = emit_at(CIGAR, cig, 1, mouth) + se(s["ember"]) + wait(8)
    w += func(34, 8, 0, 1, rgb(255, 140, 40), 10, 0) + wait(8)                # a long drag... (the tip glows)
    for k in range(3):                                                         # ...and smoke rings
        w += emit_at(CIGAR, RINGS8, 1, (sx * -6 + sx * 4 * k, 26)) + se(s["smoke"]) + wait(6)
    w += bmove(side, 264, 12, 0, -6) + func(34, 8, 0, 2, rgb(40, 40, 120), 14, 0)   # nodding off
    w += emit_at(SNOOZE, ZZZ, 1, (sx * 12, 44)) + se(s["sleep"]) + wait(4)
    w += emit_at(NIGHT, POP, 1, (sx * -36, 62)) + wait(24)
    w += bmove(side, 264, 8, 0, 6) + wait(10)
    return w


def _reload(side, s):
    """Recover (Reload): a fat magazine slams up into place - CHK-CHK - and they patch right up. RELOADED."""
    sx = 1 if side == "player" else -1
    at = (sx * 24, 24)
    w = stop_motion(MAG, POSE, 0, (at[0], -16), at, 4)
    w += emit_at(MAG, HOLD, 0, at) + se(s["crack"]) + shake_attacker(1, 2) + wait(4)       # CHK
    w += se(s["bonk"]) + shake_attacker(1, 2) + wait(4)                                    # CHK
    w += emit_at(HEALS, PLUSES, 0, (0, 20)) + se(s["absorb"])
    for k in range(3):
        w += func(34, 2, 0, 1, rgb(110, 255, 120), 12, 0) + wait(6)
    w += emit_at(RELOADED, POP, 0, (sx * 30, 62 if side == "player" else 52)) + se(s["bling"]) + wait(16)
    return w


# ------------------------------------------------------------------ set 9

def _self_sign(side):
    """A sign over the attacker (the player's sits lower: clear of the foe's HP box)."""
    return (30 if side == "player" else -30, 62 if side == "player" else 52)


def _flop(side, s):
    """Splash (Flop): flop... flop... FLOP. Nothing happens. A tumbleweed rolls by. The judges: 0/10."""
    sx = 1 if side == "player" else -1
    w = []
    for k in range(2):                                                          # flop, flop
        w += bmove(side, 258, 3, -sx * 4, 16) + se(s["flop"]) + wait(3)
        w += bmove(side, 258, 3, sx * 4, -16) + wait(2) + emit_at(TUMBLE, HOPS, 0, (0, -16)) + wait(2)
    w += bmove(side, 258, 4, 0, 22) + se(s["flop"]) + wait(4)                   # the big one...
    w += bmove(side, 258, 3, 0, -28) + wait(2) + emit_at(TUMBLE, HOPS, 0, (0, -22)) + wait(6)   # ...flat on it
    x, y = BATTLER_AT[side]
    w += emit_at(TUMBLE, TUMBLE_GO, 0, (-(x + 40), y - TUMBLE_Y)) + se(s["gust"]) + wait(22)   # ...
    w += emit_at(SCORE, POP, 0, (sx * 40, 50 if side == "player" else 44)) + se(s["faint"]) + wait(10)
    w += bmove(side, 258, 6, 0, 6) + wait(16)
    return w


def _windmill(side, s):
    """Flail (Windmill): arms windmilling like a maniac - then they run in swinging. HANDS!"""
    sx = 1 if side == "player" else -1
    w = emit_at(ARMS, MILL_HERE, 0, (0, 20)) + se(s["flail"]) + wait(9)          # winding up
    w += bmove(side, 258, 5, 72, 36) + se(s["whoosh"]) + wait(5)                 # here they come
    w += emit_at(ARMS, MILL_THERE, 1, (sx * -24, 22))
    for k in range(4):                                                         # wap wap wap wap
        w += emit_at(ARMS, STARS9, 1, (sx * (-8 + 6 * (k % 2)), (28, 12, 22, 6)[k]))
        w += se(s["bonk"] if k % 2 else s["flail2"]) + shake_defender(3, 2) + wait(3)
    w += emit_at(HANDS, POP, 1, (sx * -34, 62)) + flash_screen(4) + func(48) + func(68, 4, 2, 1, 3, 0) + wait(8)
    w += bmove(side, 258, 8, -72, -36) + wait(10)
    return w


def _make_it_rain(side, s):
    """Rain Dance (Make It Rain): a neon money gun - brrrrrt - bills sky high, and it rains money on the block."""
    sx = 1 if side == "player" else -1
    foe = "enemy" if side == "player" else "player"
    dark = rgb(0, 30, 10)
    at = (sx * 28, 24)
    w = func(33, 0, 1, 0, 10, dark) + emit_at(MGUN, GUN_R if side == "player" else GUN_L, 0, at) + wait(6)
    w += emit_at(MGUN, BILLS_E if side == "player" else BILLS_P, 0, (at[0] + sx * 16, at[1] + 8))   # brrrrt
    for k in range(3):
        w += se(s["chaching"]) + shake_attacker(1, 2) + wait(6)
    w += emit_at(BILLRAIN, RAIN_A, 1, (0, BATTLER_AT[foe][1] - 10))            # it's raining (the whole block)
    w += emit_at(BILLRAIN, RAIN_B, 0, (sx * 30, BATTLER_AT[side][1] - 10)) + se(s["raindance"]) + wait(6)
    w += emit_at(BILLRAIN, RAIN_A, 0, (sx * 70, BATTLER_AT[side][1] - 10))
    w += emit_at(RAINSIGN, POP, 0, _self_sign(side)) + wait(10) + se(s["chaching"]) + wait(24)
    w += func(33, 0, 1, 10, 0, dark) + wait(6)
    return w


def _insurance(side, s):
    """Assurance (Insurance): the payout - a giant novelty check, $1000000 - flashed, then smacked across their
    face. CLAIM PAID!"""
    sx = 1 if side == "player" else -1
    dx, dy = TARGET_FROM_ATTACKER[side]
    w = emit_at(CHECK, HOLD, 0, (sx * 22, 44)) + se(s["chaching"]) + wait(4)   # look at this
    w += emit_at(CASHSPARK, 0, 0, (sx * 22, 44)) + wait(8)
    w += stop_motion(CHECK, POSE, 1, (sx * 22 - dx, 44 - dy), (sx * -10, 28), 5) + se(s["whoosh"])
    w += emit_at(CHECK, HOLD, 1, (sx * -10, 26)) + se(s["bonk"]) + flash_screen(5)    # SMACK
    w += func(48) + shake_defender(5, 3) + func(68, 4, 2, 1, 3, 0) + emit_at(CASHSPARK, 0, 1, (0, 20))
    w += emit_at(PAYOUT, POP, 1, (sx * -34, 66)) + se(s["assure"]) + wait(20)
    return w


def _body_bag(side, s):
    """Slam (Body Bag): a flying body slam - WHUMP - then a body bag zips up over them. BODIED."""
    sx = 1 if side == "player" else -1
    w = bmove(side, 258, 5, 20, 40) + se(s["whoosh"]) + wait(5)                   # up...
    w += bmove(side, 258, 4, 52, -4) + wait(4)                                   # ...and down on them
    w += se(s["rollout"]) + se(s["bonk"]) + flash_screen(6) + func(68, 6, 3, 1, 4, 0) + func(48)
    w += emit_at(SLAMDUST, 0, 1, (0, -14)) + shake_defender(5, 4) + wait(8)
    w += bmove(side, 258, 8, -72, -36) + wait(8)
    w += stop_motion(BODYBAG, POSE, 1, (0, 110), (0, 24), 4)
    w += emit_at(BODYBAG, HOLD, 1, (0, 24)) + se(s["bonk"]) + wait(3)
    w += se(s["swipe"]) + shake_defender(2, 3) + wait(4)                         # zzzip (wriggling in there)
    w += emit_at(BODIED, POP, 1, (sx * -36, 66)) + wait(16)
    return w


def _beam_me_up(side, s):
    """Waterfall (Beam Me Up): a big yellow hydrant pops up under them... the top blows off... and the water
    blasts them sky high. They come down soaked."""
    sx = 1 if side == "player" else -1
    foot = (0, -20) if side == "player" else (0, -8)                         # under their feet (yours: clear of
    top = (foot[0], foot[1] + HYD_TOP)                                         #  the message box)
    up = LAUNCH[side]
    w = emit_at(GEYSER, HYD, 1, foot) + se(s["bonk"]) + wait(8)
    w += func(36, 1, 0, 1, 4, 264) + wait(6)                                   # rumbling...
    w += emit_at(GEYSER, CAP_OFF, 1, top) + se(s["wfall"]) + flash_screen(3)    # POP
    w += emit_at(GEYSER, GUSH, 1, top) + emit_at(SPLOSH, COLUMN, 1, top) + wait(2)
    w += bmove(side, 264, 8, 0, up) + wait(8)                                  # BEAMED UP (untinted: a blue
#                                                                                foe vanishes into the column)
    w += emit_at(BEAMUP, POP, 1, (-44, 34) if side == "player" else (60, 70)) + se(s["splash"])   # (clear of HP boxes)
    for k in range(4):                                                         # riding the jet
        w += bmove(side, 264, 3, 0, 5 if k % 2 == 0 else -5) + wait(3)
    w += bmove(side, 264, 5, 0, -up) + emit_at(SPLOSH, RAINBACK, 1, (0, 60)) + wait(5)  # ...and down
    w += se(s["wfall2"]) + se(s["bonk"]) + func(48) + shake_defender(4, 3) + func(68, 4, 2, 1, 3, 0)
    w += func(34, 8, 0, 2, rgb(90, 170, 255), 12, 0) + wait(14)                # soaked
    return w


def _poke(side, s):
    """Peck (Poke): a finger jabbing them in the chest. Poke. Poke. POKE. POKED!"""
    sx = 1 if side == "player" else -1
    hand = FINGER_R if side == "player" else FINGER_L
    chest = (sx * 2, 18)
    w = stop_motion(FINGER, hand, 1, (sx * -80, 24), (sx * -28, 18), 3, ease=1)
    for k, back in enumerate((-40, -42, -54)):
        w += emit_at(FINGER, hand, 1, (sx * -26 if k < 2 else sx * -22, 18)) + emit_at(FINGER, BOOP, 1, chest)
        w += se(s["peck"]) + shake_defender(2 if k < 2 else 4, 1)
        if k == 2:                                                               # the last one: hard
            w += flash_screen(3) + func(48) + func(34, 8, 0, 1, rgb(255, 120, 120), 12, 0)
        w += wait(1) + emit_at(FINGER, hand, 1, (sx * back, 20)) + wait(1)
    for k in range(4):                                                         # ...and it lingers there
        w += emit_at(FINGER, hand, 1, (sx * -54, 20)) + wait(1)
    w += emit_at(POKED, POP, 1, (sx * -34, 62)) + wait(14)
    return w


def _duct_tape(side, s):
    """Wrap (Duct Tape): a roll of duct tape whips round and round them, strip after strip. TAPED UP!"""
    sx = 1 if side == "player" else -1
    w = []
    for k in range(13):                                                        # round and round
        a = k * 2 * math.pi / 8
        w += emit_at(TAPEROLL, ROLL9, 1, (round(sx * 40 * math.cos(a)), round(22 + 14 * math.sin(a))))
        if k in (3, 7, 11):
            j = k // 4
            w += emit_at(TAPEROLL, (STRIP_A, STRIP_B)[j % 2], 1, (0, (36, 22, 8)[j])) + se(s["sshot"])
            w += shake_defender(1, 1)
        w += wait(1)
    w += func(34, 8, 0, 2, rgb(160, 165, 175), 13, 0) + bmove(side, 264, 4, 0, -4) + wait(3)   # squeezed
    w += emit_at(TAPED, POP, 1, (sx * -34, 62)) + func(36, 1, 0, 1, 4, 264) + wait(12)
    w += bmove(side, 264, 6, 0, 4) + wait(10)
    return w


def _kevlar(side, s):
    """Harden (Kevlar): the vest drops on - BANG - ping - ping - the rounds bounce right off. BULLET PROOF."""
    sx = 1 if side == "player" else -1
    w = stop_motion(VEST, POSE, 0, (0, 100), (0, 14), 4)
    w += emit_at(VEST, HOLD, 0, (0, 14)) + se(s["harden"]) + shake_attacker(1, 2) + wait(6)
    for k, (x, y) in enumerate(((8, 20), (-6, 10), (10, 2))):
        at = (sx * x, y)
        w += se(s["boom"] if k == 0 else s["bling"]) + emit_at(RICO, SPARKS9, 0, at) + emit_at(RICO, SLUGS, 0, at)
        w += flash_screen(2) + func(34, 2, 0, 1, rgb(255, 255, 255), 10, 0) + func(36, 1, 0, 1, 2, 258) + wait(6)
    w += emit_at(BPROOF, POP, 0, _self_sign(side)) + se(s["bling"]) + wait(16)
    return w


def _curse_out(side, s):
    """Curse (Curse Out): they go OFF - #@&! @#!% - and every cuss costs a coin in the swear jar. Clink. Clink."""
    sx = 1 if side == "player" else -1
    jar = (sx * -38, 14)
    w = emit_at(JAR, JAR1, 0, jar) + wait(6)
    for k, (x, y) in enumerate(((26, 50), (-6, 64), (34, 34), (6, 56))):
        w += emit_at(CUSS, k % 2, 0, (sx * x, y)) + se(s["curse"] if k % 2 == 0 else s["rage"])
        w += func(34, 2, 0, 1, rgb(255, 40, 40), 13, 0) + func(36, 2, 0, 1, 2, 258) + wait(2)
        w += emit_at(JAR, COIN_IN, 0, (jar[0], jar[1] + 52)) + wait(4) + se(s["bling"]) + wait(2)
    w += se(s["curse2"]) + wait(14)
    return w


# ------------------------------------------------------------------ set 10

def _foe_sign(side):
    """A sign over the target, clear of the HP boxes."""
    return (-34 if side == "player" else 34, 62)


def _foe_feet(side):
    """Offset of the target's feet (yours: kept clear of the message box)."""
    return (0, -10) if side == "player" else (0, 8)


def _spit_bars(side, s):
    """BubbleBeam (Spit Stream): a PA speaker drops in behind them and the beat kicks in - mic up, head bobbing,
    they SPIT BARS, spit flying on every line - and the foe gets roasted. Literally."""
    sx = 1 if side == "player" else -1
    mouth = MOUTH_AT[side]
    amp = (-40, 22) if side == "player" else (44, 14)                          # behind them (yours: on screen)
    w = emit_at(SPEAKER, POP, 0, amp) + wait(4)
    w += emit_at(MIC, MIC_R if side == "player" else MIC_L, 0, (mouth[0] + sx * 12, mouth[1] - 8)) + wait(2)
    for k in range(5):                                                         # boom... bap. boom... bap.
        w += emit_at(SPEAKER, 1, 0, amp) + emit_at(ROAST, NOTES10, 0, (amp[0], amp[1] + 36)) + se(s["bass"])
        w += bmove(side, 258, 2, sx * 3, 4) + wait(2)
        if k >= 1:                                                             # (the beat drops, then the bars)
            w += emit_at(MIC, SPIT_E if side == "player" else SPIT_P, 0, mouth) + se(s["leer"])
        w += bmove(side, 258, 2, -sx * 3, -4) + wait(3)
    w += emit_at(ROAST, 0, 1, (0, 18)) + se(s["burn"]) + func(34, 8, 0, 2, rgb(255, 110, 30), 13, 0)
    w += shake_defender(2, 4) + wait(20)
    return w


def _super_soaker(side, s):
    """Water Sport (Sprinkler): summer on the block - pump the Super Soaker, then the sprinkler dance,
    soaking them on every tick. SUMMERTIME!"""
    sx = 1 if side == "player" else -1
    w = emit_at(SOAKER, SOAKER_R if side == "player" else SOAKER_L, 0, SOAKER_AT[side]) + wait(4)
    w += shake_attacker(1, 4) + se(s["wsport"]) + wait(8)                       # pump pump
    for k, step in enumerate((5, 5, 5, -15, 5, 5, 5, -15)):                    # tick tick tick... shhhh
        w += bmove(side, 258, 2, sx * step, 0)
        if step > 0:
            w += emit_at(SOAKER, SOAK_E if side == "player" else SOAK_P, 0, SOAKER_TIP[side])
        if k % 2 == 0:
            w += se(s["surf"] if k == 4 else s["wsport"])
        w += wait(2 if step > 0 else 3)
    w += func(34, 8, 0, 2, rgb(90, 170, 255), 12, 0) + shake_defender(2, 3)
    w += wait(18)
    return w


def _horn_blast(side, s):
    """Horn Attack (Horn Blast): the DJ drop - BWAAP - BWAAP - BWAAAAAP. Every blast blows them further back,
    and the last one blows them clean off the screen."""
    sx = 1 if side == "player" else -1
    w = emit_at(AIRHORN, HORN_R if side == "player" else HORN_L, 0, HORN_AT[side]) + wait(6)
    for k in range(2):                                                         # BWAAP. BWAAP.
        w += emit_at(AIRHORN, RINGS_E if side == "player" else RINGS_P, 0, HORN_TIP[side]) + se(s["horn"])
        w += shake_attacker(1, 2) + wait_frames(8) + bmove(side, 264, 3, sx * 8, sx * 4) + shake_defender(2, 2) + wait(5)
    w += emit_at(AIRHORN, RINGS_E if side == "player" else RINGS_P, 0, HORN_TIP[side]) + se(s["horn"]) + se(s["alarm"])
    w += wait_frames(8) + flash_screen(3)
    w += bmove(side, 264, 5, sx * 110, sx * 50) + func(68, 4, 3, 1, 3, 0) + wait(14)   # BWAAAAAP: gone
    w += bmove(side, 264, 8, -sx * 126, -sx * 58) + wait(10)                         # ...walks back in
    return w


def _mud_pie(side, s):
    """Mud Shot (Mud Pie): a pie right in the face - then they pull out the phone and film it. POSTED."""
    sx = 1 if side == "player" else -1
    w = bmove(side, 258, 6, -8, 5) + wait(6)                                   # wind up
    w += bmove(side, 258, 3, 16, -8) + _throw(PIE, 1, (0, 26)) + wait(2) + bmove(side, 258, 6, -8, 3)
    w += wait_frames(THROW_FRAMES) + se(s["splat"]) + se(s["mudshot"]) + emit_at(MUDSPLAT, POP, 1, (0, 26))
    w += emit_at(PIE, MUDDRIP, 1, (0, 16)) + func(34, 8, 0, 2, rgb(110, 70, 35), 13, 0) + shake_defender(3, 3)
    w += wait(8) + emit_at(MUDSPLAT, PHONE, 0, (sx * 30, 36)) + wait(8)          # filming...
    w += flash_screen(2) + se(s["pop"]) + wait(4) + wait(18)
    return w


def _backhand(side, s):
    """DoubleSlap (Backhand, once per hit - so it's quick): the pimp hand, swung right across their face."""
    sx = 1 if side == "player" else -1
    w = stop_motion(BACKHAND, POSE, 1, (sx * -64, 30), (sx * -4, 26), 3, ease=1)
    w += emit_at(BACKHAND, HOLD, 1, (0, 26)) + emit_at(SLAPSTAR, 0, 1, (sx * 4, 26)) + se(s["dslap"])
    w += flash_screen(2) + shake_defender(3, 2) + wait(2)
    w += stop_motion(BACKHAND, POSE, 1, (sx * 14, 26), (sx * 44, 30), 2, ease=1) + wait(6)
    return w


def _battery_acid(side, s):
    """Acid (Battery Acid): they lick a 9-volt to see if it's still good - ZAP - yep. Then chuck it at them:
    acid everywhere, sizzling. TSSSS!"""
    mouth = MOUTH_AT[side]
    w = emit_at(ACIDSPLAT, HELD9V, 0, (mouth[0], mouth[1] - 2)) + wait(8)       # *lick*
    w += se(s["zap"]) + flash_screen(2) + func(34, 2, 0, 1, rgb(255, 240, 60), 15, 0) + shake_attacker(2, 4)
    w += wait(10)
    w += bmove(side, 258, 3, 16, -8) + _throw(NINEVOLT, 1, (0, 24)) + wait(2) + bmove(side, 258, 6, -16, 8)
    w += wait_frames(THROW_FRAMES) + se(s["splat"]) + se(s["acid"]) + emit_at(ACIDSPLAT, POP, 1, (0, 24))
    w += emit_at(NINEVOLT, FIZZ, 1, (0, 20)) + func(34, 8, 0, 2, rgb(120, 230, 40), 14, 0) + flash_screen(2)
    w += se(s["burn"]) + shake_defender(2, 6) + wait(4)
    w += wait(20)
    return w


def _fire_hose(side, s):
    """Hydro Pump (Fire Hose): the hose gets away from them - whipping round like a snake, spraying everywhere,
    soaking THEM, knocking them back - till they wrestle it round and blast the foe clean across. HOSED!"""
    sx = 1 if side == "player" else -1
    at = NOZ_AT[side]
    w = se(s["hpump"])
    for k in range(10):                                                        # it's ALIVE
        x, y = (0, 6, 10, 6, 0, -6, -10, -6, 0, 4)[k], (0, 6, 0, -6, 0, 6, 0, -6, 0, 3)[k]
        w += emit_at(FIREHOSE, NOZ_SPIN, 0, (at[0] + x, at[1] + y)) + emit_at(FIREHOSE, WILD, 0, (at[0] + x, at[1] + y))
        if k == 3:
            w += bmove(side, 258, 8, -12, -6) + func(34, 2, 0, 1, rgb(70, 150, 255), 13, 0)   # soaked, shoved back
        w += wait(1)
    w += bmove(side, 258, 6, 12, 6) + emit_at(FIREHOSE, HOSE_E if side == "player" else HOSE_P, 0, NOZ_TIP[side])
    w += se(s["hpump"]) + wait_frames(10)                                       # got it - AIM
    w += emit_at(WETHIT, 0, 1, (0, 20)) + emit_at(WETHIT, 1, 1, (0, 24)) + se(s["surf"])
    w += func(34, 8, 0, 2, rgb(70, 150, 255), 13, 0) + bmove(side, 264, 18, sx * 16, sx * 8)
    w += func(68, 4, 3, 1, 8, 0) + wait(10) + wait(16)
    w += bmove(side, 264, 8, -sx * 16, -sx * 8) + wait(10)
    return w


def _rise_n_slap(side, s):
    """Wake-Up Slap (Rise n Slap): an alarm clock rattling over their head - BRRRING - and then Mama's
    chancla comes flying in from off-screen. GET UP!"""
    sx = 1 if side == "player" else -1
    at = (sx * -6, 54)
    w = se(s["alarm"])
    for k in range(8):                                                         # BRRRRRING
        w += emit_at(ALARMCLK, CLOCK_A if k % 2 == 0 else CLOCK_B, 1, (at[0] + (k % 2) * 2, at[1]))
        w += emit_at(ALARMCLK, RINGING, 1, at) + wait(1)
    fly = FLY_E if side == "player" else FLY_P
    w += emit_at(CHANCLA, fly, 1, (sx * CHANCLA_SPEED * CHANCLA_FRAMES, 22 + round(1.5 * CHANCLA_FRAMES)))
    w += se(s["whoosh"]) + wait_frames(CHANCLA_FRAMES)                          # (from off-screen)
    w += se(s["dslap"]) + se(s["wslap"]) + flash_screen(5) + func(48) + shake_defender(5, 3)
    w += func(68, 4, 2, 1, 3, 0) + wait(4) + wait(18)
    return w


def _dirty_shiv(side, s):
    """Poison Jab (Dirty Shiv): a commissary spoon filed into a shank, flies buzzing round it. Jab jab. TETANUS!"""
    sx = 1 if side == "player" else -1
    jab = SPOON_R if side == "player" else SPOON_L
    w = emit_at(SPOON, FLIES, 1, (0, 20)) + bmove(side, 258, 6, 64, 32) + se(s["whoosh"]) + wait(7)
    for k, y in enumerate((22, 12)):
        w += emit_at(SPOON, jab, 1, (sx * -50, y)) + wait(1)                    # pull back...
        w += emit_at(SPOON, jab, 1, (sx * -24, y)) + se(s["bonk"]) + shake_defender(3, 2)   # ...SHANK
        w += func(34, 3, 0, 1, rgb(140, 200, 60), 12, 0) + wait(2)
    w += se(s["psting2"]) + bmove(side, 258, 8, -64, -32) + wait(8)
    w += func(34, 8, 0, 2, rgb(140, 200, 60), 12, 0) + wait(14)
    return w


def _salty(side, s):
    """Brine (Salt Water): a giant salt shaker over them - shake shake shake - salt in the wound. SALTY."""
    sx = 1 if side == "player" else -1
    at = (sx * -4, 50)
    w = stop_motion(SHAKER, SHAKE_UP, 1, (sx * -70, 100), at, 4)
    for k in range(8):                                                         # shake shake shake
        w += emit_at(SHAKER, SHAKE_A if k % 2 == 0 else SHAKE_B, 1, (at[0], at[1] + (k % 2) * 4))
        w += emit_at(SHAKER, SALT, 1, (at[0], at[1] - 22))
        if k % 3 == 0:
            w += se(s["sand"])
        w += wait(1)
    w += se(s["brine"]) + func(34, 8, 0, 2, rgb(255, 255, 255), 14, 0) + shake_defender(3, 4) + wait(6)
    w += emit_at(SALTY, POP, 1, _foe_sign(side)) + wait(20)
    return w


def _dirty_nails(side, s):
    """Toxic Spikes (Dirty Nails): a handful of long glittery press-on acrylics flung all over their side.
    WATCH YO STEP!"""
    w = bmove(side, 258, 4, -6, 3) + wait(4) + bmove(side, 258, 3, 12, -6) + se(s["whoosh"]) + wait(6)   # flick
    ground = (0, -26) if side == "player" else (0, 4)                          # the floor in front of them
    w += emit_at(NAILS, NAILS1, 1, ground) + se(s["tspikes"]) + bmove(side, 258, 4, -6, 3)
    w += emit_at(NAILS, GLITTER, 1, ground) + se(s["bling"]) + wait(8)
    w += se(s["toxic2"])
    return w + wait(22)


def _the_boot(side, s):
    """Stun Spore (The Boot): the parking boot drops on them - CLANK. They try to walk off... they ain't going
    nowhere. BOOTED!"""
    sx = 1 if side == "player" else -1
    feet = (0, -22) if side == "player" else (0, 4)                            # round their feet
    w = stop_motion(BOOT, POSE, 1, (feet[0], 100), feet, 4)
    w += emit_at(BOOT, HOLD, 1, feet) + se(s["bonk"]) + se(s["sleep"]) + func(68, 3, 2, 1, 2, 0) + wait(6)
    for k in range(3):                                                         # *tug* *tug* *tug*
        w += bmove(side, 264, 2, sx * 6, 0) + wait(2) + bmove(side, 264, 2, -sx * 6, 0)
        w += func(36, 1, 0, 1, 1, 264) + wait(3)
    w += func(34, 8, 0, 2, rgb(255, 220, 40), 13, 0) + wait(18)
    return w


def _gutter_slop(side, s):
    """Sludge (Gutter Slop): a raccoon pops out of the dumpster next to them - and hurls the trash juice. EWWW!"""
    sx = 1 if side == "player" else -1
    dump = (-24, 4) if side == "player" else (34, -2)                          # behind them (yours: on screen)
    w = emit_at(DUMPSTER, DUMP, 0, dump) + emit_at(DUMPSTER, STINK, 0, (dump[0], dump[1] + 24)) + wait(10)
    w += emit_at(DUMPSTER, COON, 0, (dump[0], dump[1] + 30)) + se(s["toxic2"]) + wait(10)     # ...!
    w += _throw(SLOPBALL, 1, (0, 24)) + wait_frames(THROW_FRAMES) + wait(1)
    w += se(s["splat"]) + emit_at(SLOPBALL, SLOPDRIP, 1, (0, 22)) + emit_at(DUMPSTER, STINK, 1, (0, 30))
    w += func(34, 8, 0, 2, rgb(130, 140, 50), 13, 0) + shake_defender(3, 3) + se(s["sludge"])
    w += wait(20)
    return w


def _pebble_spray(side, s):
    """Rock Blast (Pebble Spray, once per hit - quick): a pebble at their window, 2am. YOU UP?"""
    w = _throw(PEBBLE, 1, (0, 40)) + wait_frames(THROW_FRAMES) + wait(1)
    w += emit_at(PEBBLE, PING, 1, (0, 40)) + se(s["bling"]) + shake_defender(2, 2)
    w += emit_at(YOUUP, POP, 1, _foe_sign(side)) + wait(10)
    return w


def _live_socket(side, s):
    """Discharge (Live Socket): six cords plugged into one outlet... crackle crackle... ZAP - everybody fried -
    and then the whole block goes dark. Who ain't pay the lights?!"""
    sx = 1 if side == "player" else -1
    at = (-30, 4) if side == "player" else (34, 0)
    w = emit_at(OUTLET, OUTLET1, 0, at) + wait(6)
    for k in range(5):                                                         # crackle crackle
        w += emit_at(OUTLET, CRACKLES, 0, (at[0] + (-8 + 5 * k), at[1] + (6, -4, 10, -2, 4)[k]))
        if k % 2 == 0:
            w += se(s["zap"])
        w += wait(2)
    w += se(s["dcharge"]) + flash_screen(6) + emit_at(ZAPRING, RING_BIG, 0, (0, 20))   # ZZZZAP
    w += emit_at(ZAPRING, RING_SMALL, 1, (0, 22)) + emit_at(ZAPRING, RING_BIG, 1, (0, 22)) + func(68, 5, 3, 1, 4, 0)
    for k in range(4):
        c = rgb(255, 240, 60) if k % 2 == 0 else rgb(0, 0, 0)
        w += func(34, 8, 0, 1, c, 15, 0) + func(34, 2, 0, 1, c, 12, 0) + wait(2)
    w += func(33, 0, 1, 0, 16, rgb(0, 0, 0)) + se(s["faint"]) + wait(14)       # ...BLACKOUT
    w += func(33, 0, 1, 16, 4, rgb(0, 0, 0)) + wait(2) + func(33, 0, 1, 4, 16, rgb(0, 0, 0)) + wait(4)   # flicker
    w += emit_at(PAYLIGHTS, POP, 1, _foe_sign(side)) + wait(14)
    w += func(33, 0, 1, 16, 0, rgb(0, 0, 0)) + func(48) + wait(8)
    return w


def _fetal_pos(side, s):
    """Defense Curl (Fetal Pos.): post-breakup. Curled up under the blankie with a pint of ice cream, and a
    little rain cloud following them around. NOT TODAY."""
    sx = 1 if side == "player" else -1
    w = bmove(side, 258, 6, 0, -8) + se(s["dcurl"]) + wait(4)                  # curl up
    w += stop_motion(BLANKIE, POSE, 0, (0, 96), (0, 12), 4)
    w += emit_at(BLANKIE, HOLD, 0, (0, 12)) + se(s["dcurl2"]) + wait(4)
    w += emit_at(RAINCLOUD, CLOUD, 0, (sx * 2, 62)) + emit_at(RAINCLOUD, RAIN, 0, (sx * 2, 54)) + wait(6)
    for k in range(3):                                                         # (sniff)
        w += func(36, 1, 0, 1, 2, 258) + wait(5)
    w += func(34, 2, 0, 1, rgb(90, 140, 230), 12, 0) + wait(16)
    w += bmove(side, 258, 6, 0, 8) + wait(6)
    return w


def _choke_hold(side, s):
    """Constrict (Choke Hold): a spiked choke-collar snaps round their neck - the leash yanks them back,
    three times, they go red. LEASHED!"""
    sx = 1 if side == "player" else -1
    neck = (sx * -2, 22) if side == "player" else (sx * -2, 28)
    w = emit_at(HEADLOCK, COLLAR_L if side == "player" else COLLAR_R, 1, neck) + se(s["constrict"]) + wait(8)   # *snap*
    for k in range(3):                                                         # YANK
        w += bmove(side, 264, 2, -sx * 8, -sx * 4) + se(s["whoosh"] if k < 2 else s["bonk"]) + wait(2)
        w += emit_at(HEADLOCK, GASP, 1, (sx * -14, 30)) + func(34, 8, 0, 1, rgb(230, 50, 50), 12, 0)
        w += bmove(side, 264, 4, sx * 8, sx * 4) + wait(5)
    w += shake_defender(2, 3) + wait(16)
    return w


def _tornado(side, s):
    """Twister (Tornado): a trash tornado touches down right on them - and round and round in it goes auntie,
    still in her lawn chair, sipping her drink."""
    w = emit_at(FUNNEL, DEBRIS, 1, (0, 20)) + se(s["twister"])
    for k in range(16):
        x = (0, 3, 5, 3, 0, -3, -5, -3)[k % 8]
        w += emit_at(FUNNEL, TWIST_A if k % 2 == 0 else TWIST_B, 1, (x, 26))
        a = k * 2 * math.pi / 8                                                 # auntie, orbiting
        w += emit_at(FUNNEL, AUNTIE, 1, (round(36 * math.cos(a)), round(34 + 22 * math.sin(a))))
        if k == 4:
            w += bmove(side, 264, 6, 0, 10)                                    # picked up...
        if k == 12:
            w += bmove(side, 264, 4, 0, -10) + se(s["twister"])                # ...dropped
        if k % 3 == 0:
            w += shake_defender(2, 1)
        w += wait(1)
    w += func(48) + func(34, 8, 0, 2, rgb(150, 150, 160), 10, 0) + wait(12)
    return w


def _kaboom(side, s):
    """Explosion (Kaboom): foil in the microwave. Sparks... sparks... ding... KABOOM. WHO DID THIS?!"""
    sx = 1 if side == "player" else -1
    at = (sx * 30, 26)
    w = emit_at(MICRO, MICRO1, 0, at) + wait(8)
    for k in range(4):                                                         # bzzt bzzt
        w += emit_at(MICRO, ARCS, 0, (at[0] - sx * 8, at[1] + (k % 2) * 3)) + se(s["zap"]) + wait(4)
    w += se(s["bling"]) + wait(6)                                              # ...ding.
    w += se(s["kaboom"]) + flash_screen(10) + func(68, 8, 5, 1, 6, 0)          # KABOOM
    w += emit_at(BOOMCLOUD, POP, 0, (sx * 20, 24)) + emit_at(BOOMCLOUD, 1, 1, (0, 20))
    w += func(34, 8, 0, 2, rgb(255, 120, 30), 15, 0) + func(34, 2, 0, 2, rgb(255, 120, 30), 15, 0)
    w += shake_defender(5, 5) + wait(10)
    w += se(s["explo"]) + emit_at(BOOMCLOUD, 1, 0, (sx * 50, 50)) + flash_screen(3) + wait(8)
    w += wait(20)
    return w


def _jumpscare(side, s):
    """Astonish (Jumpscare): the lights go down... and a process server bursts out of the bush waving the
    papers. They jump out of their skin. SERVED!"""
    sx = 1 if side == "player" else -1
    dark = rgb(0, 0, 0)
    w = func(33, 0, 1, 0, 12, dark) + wait(12)                                  # ...quiet...
    w += emit_at(SERVER, POP, 1, (sx * -36, 22)) + se(s["astonish"]) + flash_screen(2)   # !!!
    w += bmove(side, 264, 2, 0, 24) + wait(3)
    w += bmove(side, 264, 4, 0, -24) + shake_defender(3, 4) + se(s["astonish2"]) + wait(4)
    w += wait(16)
    w += func(33, 0, 1, 12, 0, dark) + wait(8)
    return w


def _irs_audit(side, s):
    """Giga Drain (IRS Audit): a magnifying glass going over them... the AUDIT folder slammed down... every
    receipt flies back to the user, and their wallet's left empty - a moth flies out. AUDITED."""
    sx = 1 if side == "player" else -1
    w = se(s["leer"])
    for k in range(7):                                                         # hmmmm...
        w += emit_at(AUDIT, GLASS, 1, (sx * (-24 + 8 * k), (30, 36, 30, 24, 30, 36, 30)[k])) + wait(1)
    w += emit_at(AUDIT, FOLDER, 1, (0, 28)) + se(s["bonk"]) + flash_screen(3) + shake_defender(3, 2) + wait(6)
    w += emit_at(AUDIT, RECEIPTS_E if side == "player" else RECEIPTS_P, 1, (0, 26)) + se(s["absorb"])
    w += func(34, 8, 0, 1, rgb(40, 40, 60), 10, 0) + wait_frames(18)
    w += emit_at(WALLET, POP, 1, (sx * -34, 18)) + se(s["faint"])               # ...empty
    for k in range(3):                                                         # (the user heals)
        w += func(34, 2, 0, 1, rgb(120, 255, 120), 12, 0) + wait(5)
    w += se(s["wpulse2"]) + wait(16)
    return w


def _beat_the_box(side, s):
    """Belly Drum (Beat the Box): the street bucket drummer - sticks flying on an upside-down paint bucket,
    tips raining in... till it costs them. MAXED OUT."""
    sx = 1 if side == "player" else -1
    box = (sx * 30, 4)
    top = (box[0], box[1] + 24)
    w = emit_at(BUCKET, BUCKET1, 0, box) + wait(8) + emit_at(TIPS, 0, 0, (sx * 30, 70))
    for k in range(12):                                                        # ba-dum ba-dum tss
        if k % 2 == 0:
            w += emit_at(BUCKET, STICKS_UP, 0, (top[0] - sx * 4, top[1] + 10))
        else:
            w += emit_at(BUCKET, STICKS_DN, 0, top) + emit_at(BUCKET, BUCKPUFF, 0, (box[0], box[1] + 18))
            w += se(s["bdrum"] if k % 4 == 1 else s["bonk"]) + func(36, 1, 0, 1, 1, 258)
        w += wait(1)
    w += func(34, 2, 0, 1, rgb(255, 40, 40), 14, 0) + shake_attacker(2, 3) + se(s["focus"]) + wait(6)   # (half HP)
    w += func(34, 2, 0, 1, rgb(255, 40, 40), 14, 0) + wait(18)
    return w


def _stink_bomb(side, s):
    """Sludge Bomb (Stink Bomb): they kick a sneaker off right at them - and the foot funk wipes them out."""
    w = bmove(side, 258, 4, -6, 3) + wait(4)                                    # wind up the leg
    w += bmove(side, 258, 3, 14, -6) + _throw(SHOE, 1, (0, 22)) + wait(2) + bmove(side, 258, 6, -8, 3)
    w += wait_frames(THROW_FRAMES) + se(s["bonk"]) + se(s["sbomb"]) + emit_at(STINKCLOUD, CLOUD10, 1, (0, 22))
    w += emit_at(STINKCLOUD, STENCH, 1, (0, 30)) + emit_at(SHOE, FUMES, 1, (0, 18))
    w += func(34, 8, 0, 2, rgb(150, 200, 40), 14, 0) + shake_defender(3, 5) + wait(8)
    w += bmove(side, 264, 8, 0, -8) + se(s["toxic2"]) + wait(16)
    w += bmove(side, 264, 8, 0, 8) + wait(6)
    return w


def _kamikaze(side, s):
    """Double-Edge (Kamikaze): a dirt bike, front wheel up, straight into them at full throttle - CRASH - the
    bike goes flying, and they eat it too. YOLO!"""
    sx = 1 if side == "player" else -1
    rx, ry = CART_RUN
    w = bmove(side, 258, 4, -6, -3) + se(s["rollout"]) + wait(4)                # rev it
    w += emit_at(DIRTBIKE, BIKE_R if side == "player" else BIKE_L, 0, (0, -12))
    w += bmove(side, 258, CART_FRAMES, rx, ry) + se(s["rollout"])
    for k in range(5):                                                         # speed lines behind them
        w += emit_at(DIRTBIKE, STREAKS, 0, (sx * (-26 + k * rx // 6), 6 + k * ry // 6)) + wait(2)
    w += wait_frames(CART_LIFE - 20)
    w += se(s["dedge"]) + se(s["bonk"]) + flash_screen(6) + emit_at(DIRTBIKE, BIKE_FLY, 1, (sx * -14, 0))
    w += func(48) + shake_defender(5, 4) + func(68, 6, 3, 1, 4, 0)
    w += wait(10) + bmove(side, 258, 10, -(rx - 6), -(ry - 3)) + wait(10)
    w += se(s["tdown2"]) + shake_attacker(3, 3) + func(34, 2, 0, 1, rgb(255, 60, 60), 12, 0) + wait(10)   # recoil
    return w


def _splash_whip(side, s):
    """Aqua Tail (Splash Whip): they pull off a wet durag and snap them with the tail. SNAP!"""
    sx = 1 if side == "player" else -1
    w = bmove(side, 258, 6, 40, 20) + se(s["surf"]) + wait(4)                   # step in, wind up
    w += bmove(side, 258, 3, -6, -3) + wait(4)
    w += emit_at(DURAG, DURAG_R if side == "player" else DURAG_L, 1, (sx * -30, 28)) + se(s["vwhip2"])
    w += emit_at(DURAG, FLICK, 1, (sx * 2, 38)) + flash_screen(3) + func(48) + shake_defender(4, 3)
    w += func(34, 8, 0, 2, rgb(90, 170, 255), 12, 0) + wait(14)
    w += bmove(side, 258, 8, -34, -17) + wait(8)
    return w


def _didnt_see_it(side, s):
    """Amnesia (Didnt See It): "WHO DID IT?" from off-screen - lips zipped, shades on, whistling. Ain't see
    nothin'."""
    sx = 1 if side == "player" else -1
    face = (0, 32) if side == "player" else (0, 24)
    w = emit_at(ZIPPED, 1, 0, (sx * -30, 40 if side == "player" else 44)) + se(s["leer"]) + wait(12)   # WHO?
    w += emit_at(ZIPPED, POP, 0, face) + se(s["amnesia"]) + wait(6)             # zip.
    for k in range(4):                                                         # *whistling*
        w += bmove(side, 258, 3, 4 if k % 2 == 0 else -4, 0) + wait(4)
    w += func(34, 2, 0, 1, rgb(255, 150, 200), 12, 0) + wait(18)
    return w


def _nap(side, s):
    """Rest (Nap): a heaping plate of soul food... gone in seconds... and they're out cold. THE ITIS."""
    sx = 1 if side == "player" else -1
    plate = (sx * 26, 6)
    dark = rgb(10, 10, 50)
    w = emit_at(SOULFOOD, PLATE, 0, plate) + wait(8)
    w += emit_at(SOULFOOD, PLATE_GONE, 0, plate)
    for k in range(4):                                                         # *demolishing it*
        w += se(s["bite"]) + shake_attacker(1, 2) + wait(3)
    w += func(33, 0, 1, 0, 10, dark) + bmove(side, 258, 8, 0, -8) + se(s["rest"]) + wait(4)   # ...and down
    w += emit_at(SOULFOOD, ZEES, 0, (sx * 8, 40)) + wait(6)
    for k in range(3):                                                         # healing up
        w += func(34, 2, 0, 1, rgb(110, 255, 120), 11, 0) + wait(6)
    w += se(s["sleep"]) + wait(8) + bmove(side, 258, 8, 0, 8) + func(33, 0, 1, 10, 0, dark) + wait(8)
    return w


def _chase_down(side, s):
    """Pursuit (Chase Down): the Feds' helicopter spotlight finds them... then a flying tackle. GOTCHA!"""
    sx = 1 if side == "player" else -1
    dark = rgb(0, 0, 30)
    w = func(33, 0, 1, 0, 8, dark) + emit_at(CHOPPER, HELI, 1, (sx * 20, 58 if side == "player" else 70))
    w += se(s["jet"]) + wait(6) + emit_at(CHOPPER, SPOT, 1, (sx * 8, 34)) + se(s["leer"]) + wait(14)   # there
    w += emit_at(DASHDUST, 0, 0, (sx * -20, 10)) + bmove(side, 258, 5, 72, 36) + se(s["razor"]) + wait(5)   # GO
    w += se(s["bonk"]) + flash_screen(5) + func(48) + shake_defender(5, 3) + func(68, 4, 2, 1, 3, 0)
    w += wait(10) + bmove(side, 258, 8, -72, -36)
    w += func(33, 0, 1, 8, 0, dark) + wait(10)
    return w


def _paper_cut(side, s):
    """Air Slash (Paper Cut): a flurry of PAST DUE bills - fwip fwip fwip - paper cuts everywhere. OWWW!"""
    sx = 1 if side == "player" else -1
    w = emit_at(BILLS10, BILLS_E if side == "player" else BILLS_P, 0, (sx * 24, 26)) + se(s["aslash"])
    w += wait_frames(12)
    for k, (x, y) in enumerate(((-6, 30), (6, 20), (-2, 12), (8, 32))):        # ow. ow. ow. OW.
        w += emit_at(BILLS10, CUTS, 1, (sx * x, y)) + se(s["slash"] if k % 2 == 0 else s["aslash"])
        w += shake_defender(2, 1) + func(34, 3, 0, 1, rgb(255, 80, 80), 11, 0) + wait(3)
    w += wait(18)
    return w


def _pepper_spray(side, s):
    """PoisonPowder (Pepper Spray): pssssht, right in the eyes - they're running in circles crying - and
    somebody dumps the milk on their face. MY EYES!"""
    sx = 1 if side == "player" else -1
    w = emit_at(PEPPER, CAN_R if side == "player" else CAN_L, 0, PEPPER_AT[side]) + wait(8)
    w += emit_at(PEPPER, MIST_E if side == "player" else MIST_P, 0, PEPPER_TIP[side]) + se(s["sleep"])
    w += wait_frames(14) + func(34, 8, 0, 2, rgb(255, 110, 40), 14, 0) + emit_at(MILK, TEARS3, 1, (0, 24))
    w += se(s["toxic2"])
    for dx, dy in ((10, 0), (0, 6), (-10, 0), (0, -6)):                         # running round in circles
        w += bmove(side, 264, 3, dx, dy) + wait(3)
    w += stop_motion(MILK, JUG_UP, 1, (sx * -50, 100), (sx * -10, 60), 3)        # here, here...
    w += emit_at(MILK, JUG_TIP, 1, (sx * -10, 60)) + emit_at(MILK, MILKPOUR, 1, (sx * -2, 52)) + se(s["splash"])
    w += wait(12) + func(34, 8, 0, 2, rgb(170, 60, 220), 12, 0) + wait(10)
    return w


# ------------------------------------------------------------------ set 11

def _belly_flop(side, s):
    """Body Slam (Belly Flop): a diving board pops up under them - boing, boing, BOING - up, over, and a full
    belly flop right onto the foe. A wall of water explodes up off the floor. Their belly's bright red."""
    sx = 1 if side == "player" else -1
    w = emit_at(BOARD, BOARD_R if side == "player" else BOARD_L, 0, (-24, 12) if side == "player" else (24, 2))
    w += wait(6)
    for k, h in enumerate((8, 12)):                                            # boing... boing...
        w += bmove(side, 258, 3, 0, -4) + wait(3) + bmove(side, 258, 4, 0, 4 + h) + se(s["rollout"]) + wait(4)
        w += bmove(side, 258, 4, 0, -h) + wait(4)
    w += bmove(side, 258, 3, 0, -6) + wait(3)                                   # ...BOING
    w += bmove(side, 258, 8, 36, 70) + se(s["whoosh"]) + wait(8)                # sky high
    w += bmove(side, 258, 4, 36, -34) + wait(4)                                 # FLOP
    w += se(s["bslam"]) + se(s["splash"]) + flash_screen(6) + func(68, 6, 4, 1, 5, 0)
    w += emit_at(BIGSPLASH, POP, 1, (0, 10)) + emit_at(BOARD, FLOPDROPS, 1, (0, 20)) + emit_at(BIGSPLASH, 1, 1, (sx * -20, 0))
    w += func(48) + shake_defender(5, 4) + func(34, 8, 0, 2, rgb(90, 170, 255), 13, 0) + wait(10)
    w += bmove(side, 258, 10, -72, -36) + func(34, 2, 0, 1, rgb(255, 60, 60), 14, 0) + wait(8)   # (owww)
    w += shake_attacker(2, 3) + wait(10)
    return w


def _pigeon_drop(side, s):
    """Mud Bomb (Pigeon Drop): a fat city pigeon flaps over... stops right above them... looks down... and
    lets go. SPLAT. Right on top of their head."""
    sx = 1 if side == "player" else -1
    top = 74 if side == "player" else 62
    w = []
    for k in range(9):                                                         # flap flap flap...
        x = sx * (-130 + k * 16)
        w += emit_at(PIGEON, WINGS_UP if k % 2 == 0 else WINGS_DN, 1, (x, top + (2 if k % 2 else 0))) + wait(1)
    for k in range(4):                                                         # ...hover... look down...
        w += emit_at(PIGEON, WINGS_UP if k % 2 == 0 else WINGS_DN, 1, (sx * 2, top + (k % 2) * 2))
        if k == 1:
            w += se(s["leer"])
        w += wait(1)
    w += emit_at(PIGEON, GLOB, 1, (sx * 2, top - 14)) + se(s["mbomb"])         # ...bombs away
    for k in range(4):
        w += emit_at(PIGEON, WINGS_UP if k % 2 == 0 else WINGS_DN, 1, (sx * (2 + k * 18), top + 4 + k * 4)) + wait(1)
    w += wait(1) + emit_at(POOPSPLAT, POP, 1, (0, 34)) + se(s["splat"])
    w += func(34, 8, 0, 2, rgb(255, 255, 255), 13, 0) + shake_defender(2, 4)
    for k in range(5):                                                         # (and off it goes)
        w += emit_at(PIGEON, WINGS_UP if k % 2 == 0 else WINGS_DN, 1, (sx * (74 + k * 18), top + 20 + k * 6)) + wait(1)
    return w + wait(16)


def _heat_lamp(side, s):
    """Sunny Day (Heat Lamp): beach chair out, foil reflector under the chin - the sun in shades cranks it up,
    the whole field goes gold and wavy, and they bake. Golden brown."""
    sx = 1 if side == "player" else -1
    gold = rgb(255, 170, 40)
    w = func(33, 0, 1, 0, 9, gold) + emit_at(SUN, POP, 0, (sx * 96, 110 if side == "player" else 40))
    w += se(s["sunny"]) + wait(6)
    w += emit_at(TANNING, CHAIR10, 0, (sx * -4, -10)) + emit_at(TANNING, REFLECTOR, 0, (0, 22)) + wait(4)
    w += emit_at(HEAT, WAVES10, 0, (0, 20)) + emit_at(HEAT, WAVES10, 1, (0, 20)) + emit_at(TANNING, GLARE, 0, (0, 24))
    for k in range(5):                                                         # baking...
        w += emit_at(SUN, 1, 0, (sx * 96, 110 if side == "player" else 40))
        w += func(34, 2, 0, 1, rgb(220, 120, 50), 9 + k, 0) + wait(6)
    w += se(s["bling"]) + func(34, 2, 0, 1, rgb(190, 100, 40), 15, 0) + wait(12)
    w += func(33, 0, 1, 9, 0, gold) + wait(6)
    return w


def _grill_flash(side, s):
    """Scary Face (Grill Flash): a giant gold grill flashed right at them - the shine sweeps across the screen
    like a lighthouse - they shield their eyes, sweating, backing away."""
    sx = 1 if side == "player" else -1
    face = (0, 34) if side == "player" else (0, 24)
    w = emit_at(GRILL, SMILE, 0, face) + se(s["sface"]) + wait(8)
    w += emit_at(GRILL, TWINKLE, 0, (face[0] + sx * 12, face[1] + 4)) + se(s["bling"]) + wait(4)
    for k in range(6):                                                         # *SHINE* sweeping
        w += emit_at(GRILL, RAY_A if k % 2 == 0 else RAY_B, 0, (face[0] + sx * 60, face[1] + (6 if k % 2 else -6)))
        if k == 1:
            w += flash_screen(3) + func(34, 8, 0, 1, rgb(255, 250, 200), 15, 0)
        w += wait(2)
    w += emit_at(SWEATY, 0, 1, (sx * -8, 34)) + se(s["sface2"]) + bmove(side, 264, 10, sx * 14, sx * 6)
    for k in range(3):                                                         # shook
        w += func(36, 1, 0, 1, 2, 264) + wait(5)
    w += bmove(side, 264, 8, -sx * 14, -sx * 6) + wait(10)
    return w


def _trunk_rattle(side, s):
    """SonicBoom (Trunk Rattle): a car rolls up, trunk popped on a wall of subs - BOOM - BOOM - BOOM - the
    whole car jumps on every hit, the bass rolls out in rings, and it shakes their feathers clean off."""
    sx = 1 if side == "player" else -1
    car = (30, 34) if side == "player" else (-40, 6)                            # (on screen, between them)
    w = []
    for k in range(4):                                                         # rolling up
        w += emit_at(TRUNK, CAR10, 0, (car[0] - sx * (30 - k * 10), car[1])) + wait(1)
    for k in range(4):                                                         # BOOM (the car jumps)
        w += emit_at(TRUNK, CAR10, 0, (car[0], car[1] + 6)) + emit_at(TRUNK, BASS_E if side == "player" else BASS_P, 0, car)
        w += se(s["bass"] if k < 3 else s["sboom"]) + func(68, 3, 2, 1, 2, 0) + wait(1)
        w += emit_at(TRUNK, CAR10, 0, car) + wait(1)
        if k >= 1:
            w += shake_defender(2 + k, 2)
        if k == 2:
            w += emit_at(FEATHERS, 0, 1, (0, 30))
        w += emit_at(TRUNK, CAR10, 0, car) + wait(1)
    w += emit_at(TRUNK, CAR10, 0, car) + se(s["alarm"]) + func(48) + wait(1)    # (and somebody's car alarm)
    for k in range(5):
        w += emit_at(TRUNK, CAR10, 0, car) + wait(1)
    return w + wait(8)


def _exhaust(side, s):
    """Smog (Exhaust): a beat-up hooptie backs up right next to them... sputter... sputter... BANG - the muffler
    backfires and a wall of black smoke rolls over them. Cough, cough."""
    sx = 1 if side == "player" else -1
    at = (sx * -50, 4)
    pipe = (at[0] + sx * 30, at[1] - 16)
    hoop = HOOP_R if side == "player" else HOOP_L
    w = []
    for k in range(5):                                                         # backing up... beep beep
        w += emit_at(HOOPTIE, hoop, 1, (at[0] - sx * (48 - k * 12), at[1])) + wait(1)
    for k in range(6):                                                         # sputter... sputter...
        w += emit_at(HOOPTIE, hoop, 1, (at[0], at[1] + (k % 2)))
        if k % 2 == 0:
            w += emit_at(HOOPTIE, SPUTTER, 1, pipe) + se(s["smog"])
        w += wait(1)
    w += emit_at(HOOPTIE, hoop, 1, (at[0], at[1] + 3)) + emit_at(SOOT, BANG10, 1, pipe)   # BANG
    w += se(s["boom"]) + flash_screen(3) + emit_at(SOOT, SOOTCLOUD, 1, (sx * -6, 18))
    for k in range(5):
        w += emit_at(HOOPTIE, hoop, 1, at) + wait(1)
    w += func(34, 8, 0, 2, rgb(60, 60, 65), 14, 0) + se(s["cough"]) + shake_defender(2, 5) + wait(12)
    return w


def _riot_shield(side, s):
    """Light Screen (Riot Shield): out comes a riot shield - FEDS crossed out, MINE in marker - and here come
    the tomatoes. Splat. Splat. Splat. Not a scratch."""
    sx = 1 if side == "player" else -1
    at = (sx * 30, 20)
    tom = TOM_E if side == "player" else TOM_P
    start = (at[0] + sx * TOMATO_SPEED * TOMATO_FRAMES, at[1] - round(1.2 * TOMATO_FRAMES))
    w = emit_at(SHIELD, SHIELD1, 0, at) + se(s["lscreen"]) + func(34, 2, 0, 1, rgb(150, 200, 255), 10, 0) + wait(8)
    for k, dy in enumerate((10, -6, 4)):                                       # incoming
        w += emit_at(SHIELD, tom, 0, (start[0], start[1] + dy)) + se(s["whoosh"]) + wait_frames(TOMATO_FRAMES)
        w += emit_at(TOMSPLAT, POP, 0, (at[0] + sx * 4, at[1] + dy)) + emit_at(SHIELD, PINGS10, 0, (at[0], at[1] + dy))
        w += se(s["splat"]) + func(36, 1, 0, 1, 1, 258) + wait(3)
    w += func(34, 2, 0, 1, rgb(150, 200, 255), 12, 0) + wait(16)
    return w


def _full_bars(side, s):
    """Signal Beam (Full Bars): phone up - no signal. They wander left... right... up on their toes... FULL
    BARS - and the wifi blasts right into the foe. Scrambled."""
    sx = 1 if side == "player" else -1
    up = PHONE_UP[side]
    w = se(s["leer"])
    x = 0
    for dx, steps in ((-10, 4), (20, 6), (-10, 4)):                            # *wandering, phone in the air*
        w += bmove(side, 258, steps * 2, dx, 0)
        for k in range(steps):
            x += dx / steps
            w += emit_at(PHONESIG, POP, 0, (up[0] + round(x) * (1 if side == "player" else -1), up[1] + (k % 2))) + wait(1)
    w += bmove(side, 258, 3, 0, 6) + wait(2)                                    # tippy toes...
    w += emit_at(PHONESIG, 1, 0, (up[0], up[1] + 6)) + se(s["bling"]) + wait(6)   # FULL BARS
    w += emit_at(WIFI, WIFI_E if side == "player" else WIFI_P, 0, (up[0], up[1] + 6)) + se(s["sbeam"])
    w += wait_frames(14)
    for k in range(6):                                                         # scrambled
        c = (rgb(255, 80, 200), rgb(80, 220, 255), rgb(255, 230, 60))[k % 3]
        w += func(34, 8, 0, 1, c, 13, 0) + func(36, 1, 0, 1, 1, 264) + wait(2)
    w += bmove(side, 258, 4, 0, -6) + wait(10)
    return w


def _bulletproof(side, s):
    """Reflect (Bulletproof): the corner-store bulletproof glass slams down in front of them. The foe charges
    straight at it - BONK - slides down it... and the little sign flips to SHUT."""
    sx = 1 if side == "player" else -1
    at = (sx * 34, 18)
    w = stop_motion(STOREGLASS, POP, 0, (at[0], 110), at, 4) + se(s["bonk"]) + func(68, 3, 2, 1, 2, 0)
    for k in range(4):                                                         # (open for business)
        w += emit_at(STOREGLASS, POP, 0, at) + wait(1)
    w += bmove(side, 264, 5, -sx * 40, -sx * 18)                                # the foe charges...
    for k in range(3):
        w += emit_at(STOREGLASS, POP, 0, at) + wait(1)
    w += emit_at(STOREGLASS, POP, 0, at) + emit_at(GLASSFX, 0, 0, (at[0] + sx * 6, at[1] + 8))   # BONK
    w += se(s["bonk"]) + se(s["reflect"]) + flash_screen(3) + shake_defender(3, 2) + wait(1)
    for k in range(4):                                                         # ...sliiiide down the glass
        w += emit_at(STOREGLASS, POP, 0, at) + bmove(side, 264, 2, 0, -3) + wait(1)
    w += emit_at(STOREGLASS, 1, 0, at) + se(s["disable"]) + wait(8)             # SHUT.
    w += bmove(side, 264, 8, sx * 40, sx * 18 + 12) + wait(10)
    return w


def _night_shift(side, s):
    """Night Shade (Night Shift): night falls, the moon rises, they clock in - ka-CHUNK - and it's mop time:
    mop, mop, WET FLOOR sign... and the foe wipes out on it."""
    sx = 1 if side == "player" else -1
    night = rgb(10, 10, 60)
    w = func(33, 0, 1, 0, 12, night) + emit_at(CLOCKIN, STARS10, 1, (sx * -40, 60))
    w += stop_motion(CLOCKIN, MOON, 0, (sx * -60, 30), (sx * -40, 76 if side == "player" else 40), 4)
    w += emit_at(CLOCKIN, MOON_UP, 0, (sx * -40, 76 if side == "player" else 40)) + se(s["nshade"])
    w += emit_at(CLOCKIN, PCLOCK, 0, (sx * 32, 24)) + wait(8) + se(s["bonk"]) + shake_attacker(1, 2) + wait(8)   # CHUNK
    floor = (0, -18) if side == "player" else (0, 8)
    w += emit_at(JANITOR, PUDDLE10, 1, floor)
    for k in range(6):                                                         # mop mop mop
        w += emit_at(JANITOR, MOP_A if k % 2 == 0 else MOP_B, 1, (sx * (-30 + (k % 2) * 12), floor[1] + 24))
        if k % 2 == 0:
            w += se(s["surf"] if k == 0 else s["swipe"])
        w += wait(1)
    w += emit_at(JANITOR, WETSIGN, 1, (sx * -38, floor[1] + 20)) + wait(8)
    w += bmove(side, 264, 3, sx * 6, 14) + se(s["whoosh"]) + wait(3)           # ...whoa- WHOA-
    w += bmove(side, 264, 3, sx * 6, -22) + se(s["bonk"]) + func(48) + flash_screen(3)   # WIPEOUT
    w += func(68, 4, 3, 1, 3, 0) + shake_defender(3, 3) + wait(10)
    w += bmove(side, 264, 8, -sx * 12, 8) + wait(6) + func(33, 0, 1, 12, 0, night) + wait(6)
    return w


def _wind_shank(side, s):
    """Air Cutter (Wind Shank): a cheap ceiling fan cranked to HIGH - wobbling worse and worse - till the
    blades rip off and go flying straight through them."""
    sx = 1 if side == "player" else -1
    at = CFAN_AT[side]
    w = se(s["acutter"])
    for k in range(16):                                                        # faster... wobblier...
        wob = (0, 2, 0, -2)[k % 4] * (1 + k // 5)
        w += emit_at(CFAN, FAN_A if k % 2 == 0 else FAN_B, 0, (at[0] + wob, at[1] + abs(wob) // 2))
        if k > 6 and k % 3 == 0:
            w += emit_at(CFAN, SWOOSH, 0, (at[0], at[1] - 6))
        w += wait(1) if k < 8 else wait(0)                                      # (spinning up)
    w += se(s["crack"]) + flash_screen(2) + emit_at(FANBLADES, BLADES_E if side == "player" else BLADES_P, 0, at)
    w += se(s["acutter"]) + wait_frames(10)
    for k, (x, y) in enumerate(((-6, 30), (6, 18), (0, 8))):                   # shank. shank. shank.
        w += emit_at(FANBLADES, SLICES, 1, (sx * x, y)) + se(s["slash"]) + shake_defender(2, 1) + wait(3)
    w += func(48) + func(34, 8, 0, 1, rgb(255, 80, 80), 12, 0) + wait(14)
    return w


def _spark_up(side, s):
    """Spark (Spark Up): flick... flick... flick... nothing. Fourth flick - ZZZAP - they light up like a power
    line, every hair standing up, and charge in crackling."""
    sx = 1 if side == "player" else -1
    hand = (sx * 26, 26)
    w = emit_at(BIC, LIGHTER1, 0, hand) + wait(6)
    for k in range(3):                                                         # click. click. click.
        w += emit_at(BIC, FLICKS, 0, (hand[0], hand[1] + 14)) + se(s["disable"]) + wait(7)
    w += se(s["spark"]) + flash_screen(5) + emit_at(ZAPAURA, 0, 0, (0, 20)) + emit_at(ZAPAURA, 1, 0, (0, 20))   # ZAP
    for k in range(6):
        w += func(34, 2, 0, 1, rgb(255, 240, 60) if k % 2 == 0 else rgb(0, 0, 0), 15, 0) + wait(2)
    w += func(34, 2, 0, 1, rgb(255, 240, 60), 14, 0)
    w += bmove(side, 258, 5, 72, 36) + se(s["whoosh"]) + wait(5)                # CHARGE
    w += se(s["spark2"]) + flash_screen(4) + emit_at(ZAPAURA, 1, 1, (0, 20)) + func(48) + shake_defender(4, 3)
    w += func(34, 8, 0, 1, rgb(255, 240, 60), 14, 0) + wait(8)
    w += bmove(side, 258, 8, -72, -36) + wait(10)
    return w


def _big_tax(side, s):
    """Mega Drain (Big Tax): the register rings them up - and the receipt just keeps coming, wrapping round them
    like a mummy - then the drawer pops open and their HP drains right in. Cha-ching."""
    sx = 1 if side == "player" else -1
    reg = (sx * -30, 14)
    w = emit_at(REGISTER, POP, 0, reg) + se(s["chaching"]) + wait(8)
    for k, (res, y) in enumerate(((STRIP_1, 36), (STRIP_2, 20), (STRIP_3, 6))):   # the receipt. keeps. going.
        w += emit_at(RECEIPT, res, 1, (0, y)) + se(s["sshot"]) + shake_defender(1, 1) + wait(6)
    w += func(34, 8, 0, 2, rgb(240, 240, 230), 11, 0) + wait(4)
    w += emit_at(REGISTER, 1, 0, reg) + se(s["bling"]) + emit_at(COINS2, DRAIN_E if side == "player" else DRAIN_P, 1, (0, 22))
    w += se(s["mdrain"]) + func(34, 8, 0, 1, rgb(40, 40, 60), 10, 0) + wait_frames(18)
    for k in range(3):                                                         # (the user heals)
        w += func(34, 2, 0, 1, rgb(120, 255, 120), 12, 0) + wait(5)
    w += se(s["chaching"]) + wait(14)
    return w


def _mud_bath(side, s):
    """Mud Sport (Mud Bath): spa day. A tub of warm mud slides in, they sink right down into it - towel turban,
    cucumbers on the eyes - bubbles, steam. Ahhhh."""
    sx = 1 if side == "player" else -1
    head = (0, 30) if side == "player" else (0, 24)
    w = emit_at(SPA, TUB, 0, (0, -4)) + se(s["msport"]) + wait(6)
    w += bmove(side, 258, 10, 0, -14) + wait(6)                                  # siiink in
    w += emit_at(SPA, SPAFACE, 0, (head[0], head[1] - 12)) + se(s["bling"])
    w += emit_at(SPA, MUDBUBS, 0, (0, 2)) + emit_at(SPASTEAM, 1, 0, (0, 14)) + wait(6)
    for k in range(4):                                                         # ahhhh
        w += func(34, 2, 0, 1, rgb(255, 180, 200), 9, 0) + se(s["bubble"] if k % 2 else s["msport2"]) + wait(8)
    w += bmove(side, 258, 8, 0, 14) + wait(10)
    return w


def _hype_up(side, s):
    """Psych Up (Hype Up): their hype man pops up beside them yelling into a megaphone, foam #1 finger going -
    confetti everywhere, they're bouncing on their toes, glowing. LET'S GO."""
    sx = 1 if side == "player" else -1
    man = (sx * -44, 26) if side == "player" else (sx * -44, 20)
    w = se(s["psych"])
    for k in range(14):                                                        # LET'S GOOOOO
        jit = (0, 2, -1, 2)[k % 4]
        w += emit_at(HYPE, POP, 0, (man[0] + jit, man[1] + abs(jit)))
        w += emit_at(HYPE, 1, 0, (sx * 34, 50 + (k % 2) * 4 if side == "player" else 44 + (k % 2) * 4))
        if k % 4 == 0:
            w += bmove(side, 258, 2, 0, 6) + se(s["horn"] if k == 4 else s["bling"])
        if k % 4 == 2:
            w += bmove(side, 258, 2, 0, -6)
        if k == 6:
            w += emit_at(CONFETTI, 0, 0, (0, 40)) + emit_at(CONFETTI, 1, 0, (sx * 20, 46)) + flash_screen(2)
        w += wait(1)
    w += func(34, 2, 0, 1, rgb(255, 220, 60), 14, 0) + wait(4) + func(34, 2, 0, 1, rgb(255, 220, 60), 14, 0) + wait(12)
    return w


# ------------------------------------------------------------------ set 12

def _fidget_spin(side, s):
    """Gyro Ball (Fidget Spin): a big gold fidget spinner whirring on their hand - faster, faster - then flung
    at the foe like a buzzsaw, grinding sparks off them, and boomeranging right back."""
    sx = 1 if side == "player" else -1
    hand = (sx * 22, 30)
    dx, dy = TARGET_FROM_ATTACKER[side]
    w = se(s["gyro"])
    for k in range(12):                                                        # vvvvVVVVRRRR
        w += emit_at(FIDGET, SPIN1, 0, hand)
        if k % 3 == 2:
            w += emit_at(WHIRLS, 0, 0, hand)
        w += wait(1)
    path = [(hand[0] + (dx - hand[0]) * t / 6, hand[1] + (dy + 22 - hand[1]) * t / 6) for t in range(1, 7)]
    for x, y in path:                                                          # FLUNG
        w += emit_at(FIDGET, SPIN1, 0, (round(x), round(y))) + wait(0)
    for k in range(6):                                                         # grrrrrind
        w += emit_at(FIDGET, SPIN1, 1, (sx * (k % 2), 22)) + emit_at(FIDGET, SPARKS11, 1, (sx * -6, 18))
        if k % 2 == 0:
            w += se(s["gyro2"]) + shake_defender(2, 1)
        w += wait(1)
    w += func(48) + flash_screen(2)
    for x, y in reversed(path):                                                # ...and back
        w += emit_at(FIDGET, SPIN1, 0, (round(x), round(y))) + wait(0)
    for k in range(4):
        w += emit_at(FIDGET, SPIN1, 0, hand) + wait(1)
    return w + wait(8)


def _neon_beam(side, s):
    """Aurora Beam (Neon Beam): the corner-store LIQUOR sign behind them buzzes... flickers... BZZT, it comes
    on full - and blasts them with neon. They come out glowing pink and blue."""
    at = NEON_AT[side]
    dim = rgb(20, 0, 40)
    w = func(33, 0, 1, 0, 8, dim)
    for k, lit in enumerate((0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1)):              # bzzt... bzt... bzzzt
        w += emit_at(NEONSIGN, 1 if lit else POP, 0, at)
        if lit and k in (1, 4, 6):
            w += se(s["zap"])
        w += wait(1)
    w += se(s["bling"])
    for k in range(12):                                                        # ON - and the neon hits them
        w += emit_at(NEONSIGN, 1, 0, at)
        if k == 1:
            w += emit_at(NEONBEAM, 0 if side == "player" else 1, 0, at) + se(s["sbeam"])
        if k >= 6:
            c = rgb(255, 80, 200) if k % 2 else rgb(80, 220, 255)
            w += func(34, 8, 0, 1, c, 13, 0) + func(36, 1, 0, 1, 1, 264)
        w += wait(1)
    w += func(48) + func(33, 0, 1, 8, 0, dim) + wait(8)
    return w


def _snooze(side, s):
    """Yawn (Snooze): they pull out the most boring book ever written - TERMS & CONDITIONS, volume 37 - and read
    it to them. Page... after page... after page. The foe nods off."""
    sx = 1 if side == "player" else -1
    at = (sx * 34, 40) if side == "player" else (sx * 34, 32)
    w = emit_at(BOOK, BOOK_SHUT, 0, at) + se(s["yawn"]) + wait(10)
    for k in range(10):                                                        # *droning*
        w += emit_at(BOOK, BOOK_OPEN, 0, (at[0] + (k % 2), at[1]))
        if k % 3 == 0:
            w += se(s["sshot"])                                                # (page flip)
        if k == 4:
            w += emit_at(BOOK, ZEES11, 1, (sx * 10, 44)) + se(s["yawn2"])
        if k >= 4 and k % 2 == 0:
            w += bmove(side, 264, 3, 0, -2)                                    # nodding...
        w += wait(1)
    w += func(34, 8, 0, 2, rgb(60, 60, 150), 12, 0) + wait(16)
    w += bmove(side, 264, 6, 0, 6) + wait(6)
    return w


def _cologne(side, s):
    """Sweet Scent (Cologne): pssht. pssht. pssht. pssht. WAY too much on themselves - then the rest right at
    the foe. A purple cloud. The foe chokes."""
    sx = 1 if side == "player" else -1
    tip = COLOGNE_TIP[side]
    w = emit_at(COLOGNE, BOTTLE_R11 if side == "player" else BOTTLE_L11, 0, (tip[0] - sx * 18, tip[1] - 4)) + wait(6)
    for k in range(4):                                                         # on themselves... and again...
        w += emit_at(FUMES11, 1, 0, (sx * 4, 30 + (k % 2) * 4)) + se(s["sscent"]) + shake_attacker(1, 1) + wait(4)
    w += func(34, 2, 0, 1, rgb(200, 120, 255), 10, 0) + wait(4)
    for k in range(2):                                                         # ...and at YOU
        w += emit_at(COLOGNE, MIST_E11 if side == "player" else MIST_P11, 0, tip) + se(s["sscent"]) + wait(5)
    w += wait_frames(8) + emit_at(FUMES11, 0, 1, (0, 22))
    w += func(34, 8, 0, 2, rgb(190, 110, 240), 13, 0) + se(s["cough"]) + shake_defender(2, 5) + wait(16)
    return w


def _spin_block(side, s):
    """Rapid Spin (Spin the Blk): they hop on a kid's BMX, streamers flying, and ride laps round the foe -
    dust everywhere - then pedal home."""
    sx = 1 if side == "player" else -1
    dx, dy = TARGET_FROM_ATTACKER[side]
    loop = [(dx + sx * x, dy + y) for x, y in ((-46, -6), (-20, -24), (20, -24), (46, -6), (20, 14), (-20, 14))]
    pts = [(0, 0)] + loop + loop + [(0, 0)]
    w = se(s["rspin"])
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):                               # pedal pedal pedal
        bike = BIKE_R if x1 >= x0 else BIKE_L
        w += bmove(side, 258, 4, round(x1 - x0), round(y1 - y0))
        for k in range(2):
            t = (k + 1) / 2
            x, y = round(x0 + (x1 - x0) * t), round(y0 + (y1 - y0) * t)
            w += emit_at(BMX, bike, 0, (x, y - 14))
            if k == 1:
                w += emit_at(BMX, DUST11, 0, (x - sx * 12, y - 18))
            w += wait(1)
        if (x1, y1) == loop[0]:
            w += se(s["bonk"]) + shake_defender(3, 2)
    w += func(48) + wait(10)
    return w


# ------------------------------------------------------------------ effect animations (a/0/6/1)
# The battler it's about is the script's "attacker" (InitMoveAnimData passes it as both), so all of these emit
# at who=0. Status ones replay every turn (poison/burn damage, still asleep...): keep them short.

def _sign_at(side):
    return (30 if side == "player" else -30, 50 if side == "player" else 52)   # player: clear of the foe's HP box


def _condition(sign_kit, motes, tint, sound, shake=0):
    def anim(side, s):
        w = emit_at(motes, 0, 0, (0, 8)) + se(s[sound])
        if shake:
            w += shake_attacker(shake, 4)
        w += func(34, 2, 0, 1, tint, 12, 0) + wait(4)
        w += emit_at(sign_kit, POP, 0, _sign_at(side)) + wait(18)
        return w
    return anim


def _henny(side, s):
    """Hennessy (Potion) / any heal: the bottle swoops in over their head and tips right up. GLUG GLUG."""
    at = (-6 if side == "player" else 6, 50)
    w = stop_motion(HENNY, POSE, 0, (at[0], 96), at, 3)
    w += emit_at(HENNY, HOLD, 0, at) + se(s["splash"]) + wait(2)
    w += emit_at(DRIPS, 0, 0, (at[0] - 8, 34)) + se(s["absorb"])
    for _ in range(3):
        w += func(34, 2, 0, 1, rgb(255, 190, 80), 12, 0) + wait(6)
    w += emit_at(AHHH, POP, 0, _sign_at(side)) + wait(16)
    return w


def _store_run(side, s):
    """Any item used from the bag: a corner-store THANK YOU bag drops in over their head, rustles. GOOD LOOKS!"""
    at = (-4 if side == "player" else 4, 46)
    w = stop_motion(STOREBAG, POSE, 0, (at[0], 100), at, 4)
    w += emit_at(STOREBAG, HOLD, 0, at) + se(s["bonk"]) + shake_attacker(1, 2) + wait(4)
    w += se(s["sand"]) + func(34, 2, 0, 1, rgb(255, 255, 255), 10, 0) + wait(6)          # *crinkle crinkle*
    w += emit_at(LOOKS, POP, 0, _sign_at(side)) + wait(16)
    return w


def _stash(side, s):
    """Held item / berry: they dig into the stash."""
    w = emit_at(STASHG, 0, 0, (0, 10)) + se(s["pop"]) + shake_attacker(1, 2)
    w += func(34, 2, 0, 1, rgb(140, 255, 140), 10, 0) + wait(4)
    w += emit_at(STASH, POP, 0, _sign_at(side)) + se(s["bling"]) + wait(16)
    return w


def _clout_up(side, s):
    """Level up: CLOUT UP! (Rare Candy is "Clout")."""
    w = emit_at(CLOUTUPS, 0, 0, (0, 0)) + se(s["chaching"])
    w += func(34, 2, 0, 1, rgb(255, 230, 90), 14, 0) + wait(4)
    w += emit_at(CLOUT, POP, 0, _sign_at(side)) + wait(18)
    return w


_asleep = _condition(SNORE, SNOREZ, rgb(70, 70, 160), "sleep")
_poisoned = _condition(BADBATCH, TOXB, rgb(170, 60, 220), "toxic2")
_burned = _condition(BURNS, BURNF, rgb(255, 90, 20), "burn")
_frozen = _condition(ICED, ICEG, rgb(150, 220, 255), "bling")
_paralyzed = _condition(TASED, JAGS, rgb(255, 230, 40), "twave", shake=2)
_confused = _condition(WHERE, QMARKS, rgb(255, 255, 255), "confuse")
_crushin = _condition(CRUSH, HEARTS2, rgb(255, 120, 180), "loyal")
_gains = _condition(GAINS, UPS, rgb(255, 80, 60), "focus")
_down_bad = _condition(DOWNBAD, DOWNS, rgb(60, 110, 255), "tdown")


VARIANTS = {97: _fly_turn2_first, 99: _calibrate, 7: _chain_swing, 8: _chain_dangle, 9: _payday, 10: _full_auto, 11: _rpg,
            12: _molotov, 13: _brick, 14: _egg, 15: _hose, 16: _bat, 17: _taser, 18: _car_alarm, 19: _bass_drop,
            20: _hot_shot, 21: _stare_down, 22: _talk_trash, 23: _pocket_sand, 24: _fan_blast,
            25: _catch_flight, 26: _hydrant_wave, 27: _power_line, 28: _road_rage, 29: _molotov2, 30: _zaza_leaf,
            31: _stomp_out, 32: _grill_chomp, 33: _hollow_point, 34: _switchblade, 35: _hot_box, 36: _burnout,
            37: _hi_yah, 38: _magic_8ball, 39: _loyalty,
            40: _flashlight, 41: _stun_taser, 42: _bass_boost, 43: _squad_up, 44: _water_bomb, 45: _sneak_diss,
            46: _dirty_sprite, 47: _duck_n_cover, 48: _smackdown, 49: _big_taser, 50: _clock_it,
            51: _belt_whip, 52: _shiv, 53: _twerk, 54: _tax, 55: _silly_string, 56: _spit,
            57: _lace_up, 58: _go_out_loud, 59: _roll_out, 60: _lock_in, 61: _dome_check, 62: _pickpocket,
            63: _pool_float, 64: _block_off, 65: _cheap_shot, 66: _jam_gun, 67: _sleeper, 68: _reload,
            69: _flop, 70: _windmill, 71: _make_it_rain, 72: _insurance, 73: _body_bag, 74: _beam_me_up, 75: _poke,
            76: _duct_tape, 77: _kevlar, 78: _curse_out,
            79: _spit_bars, 80: _super_soaker, 81: _horn_blast, 82: _mud_pie, 83: _backhand, 84: _battery_acid,
            85: _fire_hose, 86: _rise_n_slap, 87: _dirty_shiv, 88: _salty,
            89: _dirty_nails, 90: _the_boot, 91: _gutter_slop, 92: _pebble_spray, 93: _live_socket, 94: _fetal_pos,
            95: _choke_hold, 96: _tornado, 98: _kaboom, 100: _jumpscare,
            120: _irs_audit, 121: _beat_the_box, 122: _stink_bomb, 123: _kamikaze, 124: _splash_whip,
            125: _didnt_see_it, 126: _nap, 127: _chase_down, 128: _paper_cut, 129: _pepper_spray,
            130: _belly_flop, 131: _pigeon_drop, 132: _heat_lamp, 133: _grill_flash, 134: _trunk_rattle,
            135: _exhaust, 136: _riot_shield, 137: _full_bars, 138: _bulletproof, 139: _night_shift, 140: _wind_shank,
            141: _spark_up, 142: _big_tax, 143: _mud_bath, 144: _hype_up,
            145: _fidget_spin, 146: _neon_beam, 147: _snooze, 148: _cologne, 149: _spin_block,
            101: _asleep, 102: _poisoned, 103: _burned, 104: _frozen, 105: _paralyzed, 106: _confused,
            107: _crushin, 108: _clout_up, 109: _store_run, 110: _stash, 112: _gains, 113: _down_bad, 114: _henny,
            1: _sniper, 2: _shotgun, 3: _spray, 4: _point_blank, 5: _gangsta, 6: _drive_by}


# particle kits each animation uses: the battle heap only fits a few particle systems at once
KITS = {97: (PLANE, FELICIA, CLAIM), 99: (GUN, HOUSE, YOLK), 1: (GUN, KIT, SMOKE), 2: (GUN, SMOKE), 3: (GUN, KIT, SMOKE), 4: (GUN, SMOKE),
        5: (GUN, KIT, SMOKE), 6: (GUN, SMOKE, CAR), 7: (GUN, BLING), 8: (GUN, BLING), 9: (GUN, CASH), 10: (GUN, KIT, SMOKE),
        11: (GUN, SMOKE, ROCKET), 12: (GUN, BOTTLE, FIRE), 13: (GUN, BRICK, SMOKE), 14: (EGG, HOUSE, YOLK),
        15: (HYDRANT, JET, SPLASH), 16: (GUN, SLUGGER), 17: (GUN, TASER, BOLTS), 18: (FOB, RINGS),
        19: (SUB, CRACK, SMOKE), 20: (CHIPS, BURST), 21: (SHADES, GLINT), 22: (BUBBLE,), 23: (POCKET, SAND),
        24: (FAN, WIND), 25: (PLANE, FELICIA, CLAIM), 26: (WAVE, DUCK), 27: (CABLE, XRAY), 28: (HONK, CONE),
        29: (BOOZE, BREATH, BURST), 30: (LEAF, HAZE), 31: (BOOT, STOMP), 32: (TOPJAW, BOTJAW, GLITZ),
        33: (SLUG, GUN), 34: (SLASH, TIRE), 35: (SMOG, COUGH), 36: (WHEEL, TRAIL, BURST),
        37: (BLOCKS, CHOP, HIYAH), 38: (EIGHT, ANSWER), 39: (HEART,),
        40: (TORCH, BEAM, HUH), 41: (STUN, STATIC, ZZZT), 42: (BOOMBOX, SOUNDWAVE, BWOMP),
        43: (SQUAD, SQUAD2, SQUADUP), 44: (BALLOON, DRENCH, SPLOOSH), 45: (DISS, SLAP, OOOH), 46: (CUP, GOOP, DIRTY),
        47: (LID, NOPE), 48: (CHAIR, CLANG, SMACKDN), 49: (BIGTASER, MEGABOLT, BZZT), 50: (EYES, CIRCLE, CLOCKED),
        51: (BELT, WELT, WHAP), 52: (SHIV, SHIVD), 53: (TWERK, DEFDOWN, BRUH), 54: (STAMP, TAXED, COINS),
        55: (CAN, TANGLE, STUCK), 56: (SPIT, GOBSPLAT, PTOO),
        57: (KICKS, LACED), 58: (CRATE, FWBURST, BOOOM), 59: (CART, CARTL, CRASH), 60: (PHONES, LOCKED),
        61: (BUMP, DOMECHK), 62: (GRAB, YANK, YOINK),
        63: (POOLF, CHILLIN), 64: (TAPE, BARRIER, NOEXIT), 65: (LOOKBUB, FIST, CHEAP), 66: (JAMGUN, JAMMED),
        67: (CIGAR, SNOOZE, NIGHT), 68: (MAG, HEALS, RELOADED),
        69: (TUMBLE, SCORE), 70: (ARMS, HANDS), 71: (MGUN, BILLRAIN, RAINSIGN), 72: (CHECK, PAYOUT, CASHSPARK),
        73: (BODYBAG, SLAMDUST, BODIED), 74: (GEYSER, SPLOSH, BEAMUP), 75: (FINGER, POKED), 76: (TAPEROLL, TAPED),
        77: (VEST, RICO, BPROOF), 78: (JAR, CUSS),
        79: (SPEAKER, MIC, ROAST), 80: (SOAKER,), 81: (AIRHORN,), 82: (PIE, MUDSPLAT),
        83: (BACKHAND, SLAPSTAR), 84: (NINEVOLT, ACIDSPLAT), 85: (FIREHOSE, WETHIT),
        86: (ALARMCLK, CHANCLA), 87: (SPOON,), 88: (SHAKER, SALTY), 89: (NAILS,), 90: (BOOT,),
        91: (DUMPSTER, SLOPBALL), 92: (PEBBLE, YOUUP), 93: (OUTLET, ZAPRING, PAYLIGHTS),
        94: (BLANKIE, RAINCLOUD), 95: (HEADLOCK,), 96: (FUNNEL,), 98: (MICRO, BOOMCLOUD),
        100: (SERVER,), 120: (AUDIT, WALLET), 121: (BUCKET, TIPS),
        122: (SHOE, STINKCLOUD), 123: (DIRTBIKE,), 124: (DURAG,), 125: (ZIPPED,),
        126: (SOULFOOD,), 127: (CHOPPER, DASHDUST), 128: (BILLS10,), 129: (PEPPER, MILK),
        130: (BOARD, BIGSPLASH), 131: (PIGEON, POOPSPLAT), 132: (SUN, TANNING, HEAT), 133: (GRILL, SWEATY),
        134: (TRUNK, FEATHERS), 135: (HOOPTIE, SOOT), 136: (SHIELD, TOMSPLAT), 137: (PHONESIG, WIFI),
        138: (STOREGLASS, GLASSFX), 139: (CLOCKIN, JANITOR), 140: (CFAN, FANBLADES), 141: (BIC, ZAPAURA),
        142: (REGISTER, RECEIPT, COINS2), 143: (SPA, SPASTEAM), 144: (HYPE, CONFETTI),
        145: (FIDGET, WHIRLS), 146: (NEONSIGN, NEONBEAM), 147: (BOOK,), 148: (COLOGNE, FUMES11), 149: (BMX,),
        101: (SNORE, SNOREZ), 102: (BADBATCH, TOXB), 103: (BURNS, BURNF), 104: (ICED, ICEG),
        105: (TASED, JAGS), 106: (WHERE, QMARKS), 107: (CRUSH, HEARTS2), 108: (CLOUT, CLOUTUPS),
        109: (STOREBAG, LOOKS), 110: (STASH, STASHG), 112: (GAINS, UPS), 113: (DOWNBAD, DOWNS), 114: (HENNY, DRIPS, AHHH)}


def variant(k, sounds):
    """Animation script words for feel k; sounds = {"pop": seq, "boom": seq, ...}."""
    kits = KITS[k]
    _SLOT.clear()
    _SLOT.update({ps: i for i, ps in enumerate(kits)})
    frees = [w for i in range(len(kits)) for w in (53, i)]

    def body(side):
        _SIDE[0] = side
        # WaitForTasks, then put both Pokémon back exactly where they belong (MoveBattlerBy moves dx // duration
        # per frame, so a move and its "undo" can disagree by a few pixels), WaitForParticles, free, End
        got = VARIANTS[k](side, sounds)
        tail = [1] + func(62, 2) + func(62, 8) + [50] + frees + [4]
        if isinstance(got, tuple):                                 # a two-turn move (Fly): turn 1, turn 2
            one, two = got[0] + tail, got[1] + tail
            w = [13, 2, 1 + len(one)] + one + two                  # JumpByVariantBit0: bit 0 set = the hit
        else:
            w = got + tail
        while "SE" in w:                                            # sound markers from helpers
            i = w.index("SE")
            w[i:i + 2] = [5, sounds[w[i + 1]]]
        return w

    head = (PRELUDE + [51, 0, LOAD[kits[0]]] + PRELUDE_END +
            [w for i, ps in enumerate(kits[1:], 1) for w in (51, i, LOAD[ps])])
    p, e = body("player"), body("enemy")
    # JumpBySide attacker: [64, 0, off->player, off->enemy]; offsets count from their own word
    j = len(head)
    words = head + [64, 0, 2, 1 + len(p)] + p + e
    assert words[j + 2] + j + 2 == j + 4 and words[j + 3] + j + 3 == j + 4 + len(p)
    return words
