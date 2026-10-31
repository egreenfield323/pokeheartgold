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
(JETS, KICK, STOMPFX, SKYEYE, CRYSTAL, COSMOS) = range(286, 292)
(TEETHR, TEETHL, TOWELS, HAZEFOG, FURNITURE, ZEN, ZENFX, COUSIN, LEECHFX, MIRROR, DRIPFX, SIREN, WOOP, SECURITY1, BUBBLES14, BUFFER, SHINE14, STEAK, STEAMFX) = range(292, 311)
(BASSFISH, BASSFX, ICECUP, ICEHIT, LISTBOOK, LISTFX, MAGNET14, BELL14, GLOVES, PHONE16, BANK16, BEAM16, RACK, SLUSH, JAWS16, BINOC, NIGHT16) = range(311, 328)
(SHAKE, SHAKEFX, DIAMONDS, ICEBLOCK, SPIKES, COLDSHADES, DATE, HEARTS16, PICKUP, BLUSH, ACUNIT, FLAKES, POTHOLE1, CONES, TAILGATE, GRILLSMOKE, SNOWMACH, SNOWSTORM, RINGLIGHT, FLASHES) = range(328, 348)
# set 17: common moves
(BOX17, CUTTER17, CUTL17, BAR17, PLATE17, CASE17, CROW17, LOOT17, SHOVEL17, DIRT17, STOVE17, GLOVEL17,
 FLAMES17) = range(348, 361)
(TGLOVE17, ZAPB17, ZAPS17, RELICS17, OGAURA17, POINTER17, PSYRING17, DIZZY17, TIRE17, MUDWAVE17, FOREMAN17, MARKS17,
 SIZZLE17) = range(361, 374)
(CABLES17, CABLESL17, JOLT17, ROSES17, LOVE17, GAINZ17, PUMP17, KICKS17, VEIN17, STUFF17, JUNK17) = range(374, 385)
(TWIRL17, AURA17, CARDS17, SLICE17, CLAW17, BAG17, MICS17, SLEEPZ17, BLOWER17, DUSTSTORM17, TRASH17) = range(385, 396)
# set 18: thirty more
(DJ18, DJFX18, DUFFEL18, KNUX18, POW18, CAR18, RINGFIRE18, CD18, NOTES18, COAT18, GEARS18, BROOM18, RING18, WET18, STARS18, CANDLE18, WAVES18, COOKIE18, SLIP18, BALL18, CORK18, AURA18, ARMOR18, PARTY18, LIGHTS18, AID18, SINK18, BOOM18, BRAWL18, BRAWLFX18, CALM18, SNOWCONE18, TABLE18, PLATES18, POGO18, SCISS18, SHINE18, LAMP18, BLOBS18, PANCAKE18, CLAP18, STRIKER18, PUCK18, CHALK18, MOSQ18, WELT18, TOILET18, FLUSH18) = range(396, 444)
# set 19: the TMs
(FRUIT19, MATTRESS19, HEAL19, TV19, DREAM19, LOBSTER19, LOBL19, SCOOT19, DRAGON19, GLITTER19, ICEBAG19, CUBES19, EVID19, MATCH19, WISP19, BALLOON19, ZAP19, FRISBEE19, DUMMY19, CLAWS19, WRECK19, TEDDY19, ORBS19, SEEDS19, SEEDFX19, TRUCK19, TRUCKL19, GRAVEL19, TOAST19, SMOKE19, CAN19, GREEN19, SLEEP19, CARDS19, MORTAR19, FIREWORK19, BIN19, GRAB19, GRABL19, PLOW19, SNOWWALL19, REMOTE19, SEPIA19, CAMERA19, FLASH19, GYM19, PISTOL19) = range(444, 491)
# set 20: last TMs + level-up
(CLOWN20, SWIPE20, PUNCHM20, PIGGY20, COINS20, IRON20, LIGHT20, LEGO20, LACES20, GAUGE20, STEAM20, FRONT20, SAFE20, CLIMB20, FOOTB20, FOG20, FOGFX20, AMP20, AMPFX20, BUGS20, BUGFX20, MOP20, FANNY20, MONEY20, TREAD20, SLEUTH20, FICUS20, CANDY20, GEMBEAM20, SHAKE20, SCOPE20, LEAVES20, EXIT20, MOUTH20, SPITFX20, CHAIR20, COMBO20, SLASH20, BFF20, LINK20) = range(491, 531)
LAST_KIT = LINK20
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
         FIDGET: 82, WHIRLS: 84, NEONSIGN: 168, NEONBEAM: 84, BOOK: 82, COLOGNE: 82, FUMES11: 84, BMX: 82,
         JETS: 82, KICK: 168, STOMPFX: 84, SKYEYE: 82, CRYSTAL: 82, COSMOS: 84,
         TEETHR: 82, TEETHL: 82, TOWELS: 82, HAZEFOG: 84, FURNITURE: 82, ZEN: 82, ZENFX: 84, COUSIN: 168, LEECHFX: 84, MIRROR: 82, DRIPFX: 84, SIREN: 82, WOOP: 168, SECURITY1: 168, BUBBLES14: 82, BUFFER: 82, SHINE14: 84, STEAK: 168, STEAMFX: 84,
         BASSFISH: 82, BASSFX: 84, ICECUP: 82, ICEHIT: 84, LISTBOOK: 168, LISTFX: 84, MAGNET14: 82, BELL14: 168, GLOVES: 82, PHONE16: 82, BANK16: 168, BEAM16: 84, RACK: 82, SLUSH: 82, JAWS16: 82, BINOC: 168, NIGHT16: 82,
         SHAKE: 82, SHAKEFX: 84, DIAMONDS: 84, ICEBLOCK: 168, SPIKES: 82, COLDSHADES: 82, DATE: 82, HEARTS16: 84, PICKUP: 168, BLUSH: 84, ACUNIT: 82, FLAKES: 84, POTHOLE1: 82, CONES: 82, TAILGATE: 82, GRILLSMOKE: 84, SNOWMACH: 82, SNOWSTORM: 84, RINGLIGHT: 82, FLASHES: 84}
DONOR.update({BOX17: 82, CUTTER17: 82, CUTL17: 168, BAR17: 82, PLATE17: 349, CASE17: 82, CROW17: 168, LOOT17: 349,
              SHOVEL17: 82, DIRT17: 84, STOVE17: 82, GLOVEL17: 168, FLAMES17: 84,
              TGLOVE17: 82, ZAPB17: 168, ZAPS17: 84, RELICS17: 82, OGAURA17: 84, POINTER17: 82, PSYRING17: 84,
              DIZZY17: 168, TIRE17: 82, MUDWAVE17: 84, FOREMAN17: 82, MARKS17: 168, SIZZLE17: 84,
              CABLES17: 82, CABLESL17: 168, JOLT17: 84, ROSES17: 82, LOVE17: 84, GAINZ17: 82, PUMP17: 84, KICKS17: 82,
              VEIN17: 84, STUFF17: 82, JUNK17: 349,
              TWIRL17: 82, AURA17: 84, CARDS17: 82, SLICE17: 168, CLAW17: 82, BAG17: 168, MICS17: 82, SLEEPZ17: 84,
              BLOWER17: 82, DUSTSTORM17: 84, TRASH17: 82})
DONOR.update({DJ18: 82, DJFX18: 84, DUFFEL18: 82, KNUX18: 82, POW18: 168, CAR18: 82, RINGFIRE18: 84, CD18: 82, NOTES18: 84, COAT18: 82, GEARS18: 84, BROOM18: 82, RING18: 82, WET18: 82, STARS18: 84, CANDLE18: 82, WAVES18: 84, COOKIE18: 82, SLIP18: 168, BALL18: 82, CORK18: 82, AURA18: 84, ARMOR18: 82, PARTY18: 82, LIGHTS18: 84, AID18: 82, SINK18: 82, BOOM18: 84, BRAWL18: 82, BRAWLFX18: 84, CALM18: 82, SNOWCONE18: 82, TABLE18: 82, PLATES18: 82, POGO18: 82, SCISS18: 82, SHINE18: 84, LAMP18: 82, BLOBS18: 84, PANCAKE18: 82, CLAP18: 82, STRIKER18: 82, PUCK18: 168, CHALK18: 82, MOSQ18: 82, WELT18: 84, TOILET18: 82, FLUSH18: 84})
DONOR.update({FRUIT19: 82, MATTRESS19: 82, HEAL19: 84, TV19: 82, DREAM19: 82, LOBSTER19: 82, LOBL19: 168, SCOOT19: 82, DRAGON19: 82, GLITTER19: 82, ICEBAG19: 82, CUBES19: 84, EVID19: 82, MATCH19: 82, WISP19: 84, BALLOON19: 82, ZAP19: 84, FRISBEE19: 82, DUMMY19: 82, CLAWS19: 168, WRECK19: 82, TEDDY19: 82, ORBS19: 84, SEEDS19: 82, SEEDFX19: 84, TRUCK19: 82, TRUCKL19: 168, GRAVEL19: 84, TOAST19: 82, SMOKE19: 84, CAN19: 82, GREEN19: 84, SLEEP19: 82, CARDS19: 82, MORTAR19: 82, FIREWORK19: 84, BIN19: 82, GRAB19: 82, GRABL19: 168, PLOW19: 82, SNOWWALL19: 84, REMOTE19: 82, SEPIA19: 84, CAMERA19: 82, FLASH19: 84, GYM19: 82, PISTOL19: 82})
DONOR.update({CLOWN20: 82, SWIPE20: 82, PUNCHM20: 82, PIGGY20: 82, COINS20: 84, IRON20: 82, LIGHT20: 82, LEGO20: 82, LACES20: 82, GAUGE20: 82, STEAM20: 84, FRONT20: 82, SAFE20: 82, CLIMB20: 82, FOOTB20: 82, FOG20: 82, FOGFX20: 84, AMP20: 82, AMPFX20: 84, BUGS20: 82, BUGFX20: 84, MOP20: 82, FANNY20: 82, MONEY20: 84, TREAD20: 82, SLEUTH20: 82, FICUS20: 82, CANDY20: 82, GEMBEAM20: 84, SHAKE20: 82, SCOPE20: 82, LEAVES20: 84, EXIT20: 82, MOUTH20: 82, SPITFX20: 84, CHAIR20: 82, COMBO20: 168, SLASH20: 82, BFF20: 82, LINK20: 84})
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
# ---- set 13 emitters (per kit): Lugia's moves
CONTRAIL13, JET_R, JET_L = 0, 1, 2                            # JETS: contrail puffs, a fighter jet flying right / left
RING13, GLINT13 = 0, 1                                        # STOMPFX: the shockwave, the TING
EYE_L, EYE_SHUT, EYE_R, STARS13 = 0, 1, 2, 3                  # SKYEYE: the sky eye looking left / shut / right, stars
SWIRL13, BALL13, CARDS_E, CARDS_P = 0, 1, 2, 3                # CRYSTAL: sparkles, the crystal ball, tarot cards each way
JET13_SPEED = 9                                               # px a frame
EYE13_AT = {"player": (64, 112), "enemy": (-62, 62)}          # the sky eye, top middle of the screen
BALL13_AT = {"player": (34, 30), "enemy": (-34, 24)}          # the crystal ball beside them
# ---- set 14 emitters (per kit)
CHOMPFX, TEETH_OPEN, TEETH_SHUT = 0, 1, 2                     # TEETHR / TEETHL: chomp stars, the teeth open / shut
FRESH, TOWEL_A, TOWEL_B, SPRAYCAN = 0, 1, 2, 3                # TOWELS: freshener mist, the towel (2 poses), the can
FOG14, FRESHGLINT = 0, 1                                      # HAZEFOG: the haze, fresh sparkles
DUST14, COUCH1, MATTRESS1, DRESSER1 = 0, 1, 2, 3              # FURNITURE: dust, couch, mattress, dresser
OMRING, BOWL = 0, 1                                           # ZEN: om rings, the singing bowl
ZENHIT, INCENSE = 0, 1                                        # ZENFX: the impact, incense smoke
DRAIN14_E, DRAIN14_P = 0, 1                                   # LEECHFX: HP draining back each way
TWINKLE14, MIRROR1, TAGS = 0, 1, 2                            # MIRROR: twinkles, the mirror, price tags
DRIPSPARK, DIZZY14 = 0, 1                                     # DRIPFX: drip sparkles, dizzy stars
WOOP_E, LIGHT_RED, LIGHT_BLUE, WOOP_P = 0, 1, 2, 3            # SIREN: sound waves each way, the light (red / blue)
NOPE14, STATUSBUB = 0, 1                                      # BUBBLES14: the bounce-off spark, the status bubble
SWIRLS14, BUFF_A, BUFF_B = 0, 1, 2                            # BUFFER: wax swirls, the buffer (2 poses)
SHINE_UP, SPEED14 = 1, 0                                      # SHINE14: sparkles, speed lines
STEAMPUFF, MEATHIT = 0, 1                                     # STEAMFX: anger steam, the meat slap
SHOCK16, FLOP_A, FLOP_B = 0, 1, 2                             # BASSFISH: shock rings, the fish flopping (2 poses)
ICE_E, CUP16, ICE_P = 0, 1, 3                                 # ICECUP: ice flicked each way, the cup
PULL16, MAG_R, MAG_L, HUBCAP16 = 0, 1, 2, 3                   # MAGNET14: pull lines, the magnet each way, a hubcap
PUNCH16, GLOVE_R, GLOVE_L = 0, 1, 2                           # GLOVES: punch stars, the glove each way
ZAPS16, BATT_LOW, BATT_HALF, BATT_FULL = 0, 1, 2, 3           # PHONE16: sparks, the phone at 1% / 50% / 100%
RUSTLE, RACK1, PEEK = 0, 1, 2                                 # RACK: rustle lines, the clothes rack, eyes peeking out
ICICLES, CUP_SLUSH = 0, 1                                     # SLUSH: icicles, the slushie
FROST16, JAWS_OPEN, JAWS_SHUT = 0, 1, 2                       # JAWS16: frost sparkles, the ice jaws open / shut
NOTES16, EYES16, SLASHES16, TORCH16 = 0, 1, 2, 3              # NIGHT16: whistled notes, glowing eyes, slashes, flashlight
ICECUP_AT = {"player": (28, 30), "enemy": (-28, 26)}         # the cup of ice, in their hand
PHONE16_AT = {"player": (30, 34), "enemy": (-30, 28)}         # the phone, held up
GOLDUP, HAND_SLAP, HAND_HOOK, HAND_BUMP = 0, 1, 2, 3          # SHAKE: the gold glow rising, the handshake (3 steps)
DIAM_E, DIAM_P = 0, 1                                         # DIAMONDS: the diamond jet each way
SPIKE_A, SPIKE_B, SPIKE_C = 1, 2, 3                           # SPIKES: three rock spikes (0: dust)
SHADES16 = 1                                                  # COLDSHADES: the shades going on
DATE1 = 1                                                     # DATE: the table for two
AC1, AC_SHAKE = 1, 2                                          # ACUNIT: the AC, it rattling
FLAKES_E, FLAKES_P = 0, 1                                     # FLAKES: snow blown each way
HOLE1, STEAMUP = 1, 0                                         # POTHOLE1: the pothole, steam
CONE_A, CONE_B = 1, 2                                         # CONES: cones flung up (two spins)
GATE1, GATEPUFF = 1, 0                                        # TAILGATE: the truck, grill smoke
MACH1, MACH_SHAKE = 1, 2                                      # SNOWMACH: the machine, it rattling
STORM_A, STORM_B = 0, 1                                       # SNOWSTORM: snow pouring (two layers)
RLIGHT, RL_GLOW = 1, 0                                        # RINGLIGHT: the light, the glow
# set 17
RES3_DROP = 18.6                                              # px per unit of scale file 82's res 3 shows BELOW its
#                                                               emitter (a polygon field that can't be cleared): props there are placed by eye
PEANUTS, BOXSHUT, BOXOPEN = 0, 1, 2                           # BOX17: packing peanuts, the box shut / sliced open
CUTSPARK, CUTOUT_R, CUTIN_R, CUTOUT_L = 0, 1, 2, 3            # CUTTER17: glints, the cutter (blade out / in) each way
CUTIN_L, XCUT = 0, 1                                          # CUTL17: the cutter blade in (left), the X cut
SWEAT17, BAR1, BAR2, BAR3 = 0, 1, 2, 3                        # BAR17: sweat, the barbell with 1 / 2 / 3 plates a side
ROLL_R, ROLL_L, SLAMPUFF = 0, 1, 2                            # PLATE17: a plate rolling off each way, the slam dust
SHARDS, CASE1, CASEBROKE = 0, 1, 2                            # CASE17: glass flying, the jewelry case, smashed
CROW_R, CROW_L = 0, 1                                         # CROW17: the crowbar swung each way
CHAIN_E, CHAIN_P, LOOTSPARK = 0, 1, 2                         # LOOT17: the chain flying back each way, bling
CLODS, SHOVEL1, HOLE17, BARRICADE = 0, 1, 2, 3                # SHOVEL17: dirt clods, the shovel, the hole, barricade
ERUPT, DUSTRING = 0, 1                                        # DIRT17: the dirt eruption, dust kicked out low
HEATUP, BURNER, HOTGLOVE_R, FIREGLOVE_R = 0, 1, 2, 3          # STOVE17: heat, the burner, the glove heating / on fire
FIREGLOVE_L, HOTGLOVE_L = 0, 1                                # GLOVEL17: the enemy's gloves (left)
FLAMEHIT, STEAM17 = 0, 1                                      # FLAMES17: the fire burst, steam off them
SMASH_CASE = {"player": (-40, 6), "enemy": (40, 20)}          # the jewelry case, px from the foe (in front of them)
CHAIN_FRAMES = 16
DIG_HOLE = {"player": (34, 12), "enemy": (-56, 0)}             # Lay Low's hole, px from the attacker (in the open)
ZSPARK, TGLOVE_R, TGLOVE_L = 0, 1, 2                          # TGLOVE17: taser sparks, the taped glove each way
ZAPBURST = 0                                                  # ZAPB17: the big zap
BOLTS17, SMOKE17 = 0, 1                                       # ZAPS17: bolts crackling round them, smoke
OGSPARK, PHONE17, VHS17, TAPE17 = 0, 1, 2, 3                  # RELICS17: gold sparkles, brick phone, VHS, cassette
SHAFTS, OGDUST = 0, 1                                         # OGAURA17: gold light rising, impact dust
DOT17, POINTER_R, POINTER_L = 0, 1, 2                         # POINTER17: the red dot, the laser pointer each way
PRINGS_E, PRINGS_P = 0, 1                                       # PSYRING17: psychedelic rings each way
SWIRL17 = 0                                                   # DIZZY17: the rainbow swirl over their head
MUDDROP, TIRE_R, TIRE_L, PUDDLE = 0, 1, 2, 3                  # TIRE17: mud flecks, the tire rolling each way, puddle
MUDSHEET, MUDDRIP17 = 0, 1                                      # MUDWAVE17: mud slung at them each way
GREASE, GRILLOPEN, GRILLSHUT = 0, 1, 2                        # FOREMAN17: grease smoke, the grill open / shut
MARKS = 0                                                     # MARKS17: grill marks
SIZZLEFX, SIZZSTEAM = 0, 1                                    # SIZZLE17: grease flames, steam
TGLOVE_AT = {"player": (30, 22), "enemy": (-30, 18)}          # the taser glove, px from the attacker
RELIC_AT = {"player": [(-34, 56), (0, 86), (34, 56)], "enemy": [(-34, 30), (0, 58), (34, 30)]}   # the OG relics
POINTER_AT = {"player": (30, 26), "enemy": (-30, 22)}         # the laser pointer, px from the attacker
POINTER_TIP = {"player": (52, 26), "enemy": (-52, 22)}
MUD_TIRE = {"player": (-52, 2), "enemy": (52, 14)}            # the stuck tire, px from the foe (beside them)
MUD_SPIN = 64                                                 # frames it spins
JSPARK17, CLAMPO_R, CLAMPS_R, BATT17 = 0, 1, 2, 3             # CABLES17: sparks, the clamps open / shut, the battery
CLAMPO_L, CLAMPS_L = 0, 1                                     # CABLESL17: the enemy's clamps (left)
JBOLT17, JSMOKE17 = 0, 1                                      # JOLT17: bolts crackling round them, smoke
WINK17, ROSES1 = 0, 1                                         # ROSES17: the wink, the gas-station roses
HEARTSUP17, HEARTPOP17 = 0, 1                                 # LOVE17: hearts floating up, a burst of hearts
POWDER17, TUB17, SHAKER17, CHUG17 = 0, 1, 2, 3                # GAINZ17: powder poof, the tub, the shaker, chugging it
CHEVRONS17, PUMPGLOW17 = 0, 1                                 # PUMP17: up-arrows rising, a red pump glow
KSPARK17, KICKS1, KICKSWRECKED, CROC1 = 0, 1, 2, 3            # KICKS17: fresh sparkle, the kicks / stepped on, the Croc
VEINS17, STOMPDUST17 = 0, 1                                   # VEIN17: anger veins, stomp dust
JUNKDUST17, STUFFBOX17, HOODIE17, PAD17 = 0, 1, 2, 3          # STUFF17: dust, the box, a hoodie, a controller (falling)
BOXERS17, PHOTO17 = 0, 1                                      # JUNK17: the heart boxers, the torn photo (falling)
CLAMPS_AT = {"player": (30, 26), "enemy": (-30, 22)}          # the jumper clamps, px from the attacker
STUFF_FALL = 5                                                # px a frame Get Back's stuff falls
GUN_TOSS, GUN_SLOW, GUN_FAST, GUN_HELD = 0, 1, 2, 3           # TWIRL17: the revolver tossed up / spinning slow, fast / held
TWIRL_SLOW, TWIRL_FAST, TOSS_FRAMES = 28, 20, 24              # frames of each
FLARES17, GUNHELD_L = 0, 1                                    # AURA17: red power flares, the enemy's held revolver
CARDTRAIL, DECK17, ACE17 = 0, 1, 2                            # CARDS17: the card's trail, the fanned deck, the ace
SLICE1 = 0                                                    # SLICE17: the slice
CLAWSPARK, CLAWOPEN, CLAWBAG, CABLE17 = 0, 1, 2, 3            # CLAW17: bling, the claw open / with the bag, cable
BAG1 = 0                                                      # BAG17: the foe's designer bag
ZZ17, MICSTAND, LIGHTER17, MASK17 = 0, 1, 2, 3                # MICS17: Zzz, the mic, a lighter up, the sleep mask
NOTES_E17, NOTES_P17 = 0, 1                                   # SLEEPZ17: slow-jam notes each way
SPECKS_R, BLOWER_R, BLOWER_L, PBAG_R = 0, 1, 2, 3             # BLOWER17: dust blast (player's), blower each way, bag
DUST_R, DUST_L = 0, 1                                         # DUSTSTORM17: the dust storm blowing each way
SPECKS_L, PBAG_L, SODA_R, SODA_L = 0, 1, 2, 3                   # TRASH17: dust blast (enemy's), bag, can tumbling
DECK_AT = {"player": (28, 30), "enemy": (-28, 26)}            # the fanned deck, px from the attacker
MIC_AT = {"player": (32, 16), "enemy": (-32, 14)}             # the mic stand
BLOWER_AT = {"player": (30, 16), "enemy": (-30, 14)}          # the leaf blower
BLOWER_TIP = {"player": (54, 12), "enemy": (-54, 10)}
WIND_SPEED = 5                                                # px a frame the trash blows across
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

    # ---- set 13: Lugia's moves ----------------------------------------------------------------------------
    # Air Force (Aeroblast): red alert - a squadron of fighter jets screams over - and from the heavens a GIANT
    # crispy white sneaker comes down and STOMPS them flat. Lifts back up. Not a crease on it. TING.
    b, rs = kit(JETS)
    tex(b, 1, fxart.fighter_jet())
    b, jet_l = mirrored(b, fxart.fighter_jet())
    for res, vx, t in ((JET_R, JET13_SPEED, 1), (JET_L, -JET13_SPEED, jet_l)):   # screaming across the sky
        mover(b, rs, res, vx, 0, tex=t, scl=1.1, life=44)
    tex(b, 0, fxart.contrail())
    prop(b, rs, CONTRAIL13, tex=0, clr=rgb(255, 255, 255), clr_anm=(rgb(255, 255, 255), rgb(200, 210, 230)), scl=5.5,
         life=40, alpha=(24, 20, 0), scl_anm=(.2, 1.0, 1.1, 30, 200))           # one long streak across the sky
    prop(b, rs, 3, life=1)
    out[JETS] = bytes(b)
    poses(KICK, fxart.mega_sneaker(), 2.4, 20)
    no_delay(KICK, HOLD)
    b, rs = kit(STOMPFX)
    tex(b, 0, fxart.shock_ring())
    tex(b, 1, fxart.glint_tall())
    prop(b, rs, RING13, tex=0, clr=rgb(255, 250, 220), clr_anm=(rgb(255, 255, 255), rgb(200, 180, 140)), scl=1.6,
         life=20, scl_anm=(.3, 2.2, 3.4, 100, 200), alpha=(31, 28, 0))
    prop(b, rs, GLINT13, tex=1, clr=rgb(255, 255, 255), clr_anm=(rgb(255, 255, 255), rgb(200, 230, 255)), scl=1.0,
         life=14, scl_anm=(.2, 1.4, .2, 60, 160), alpha=(31, 31, 0))
    out[STOMPFX] = bytes(b)

    # Sixth Sense (Extrasensory): the sky goes cosmic - a giant eye opens up there and locks onto them - a crystal
    # ball swirls (their future: a tombstone), Death cards fly, and the eye blasts them with psychic rings
    b, rs = kit(SKYEYE)
    tex(b, 1, fxart.sky_eye(state=0))
    b, open_r = added(b, fxart.sky_eye(state=2), 24)
    b, open_l = mirrored(b, fxart.sky_eye(state=2), 24)
    tex(b, 0, fxart.tiny_spark())
    prop(b, rs, EYE_SHUT, scl=1.9, life=4)
    prop(b, rs, EYE_R, tex=open_r, scl=1.9, life=4)
    prop(b, rs, EYE_L, tex=open_l, scl=1.9, life=4)
    prop(b, rs, STARS13, tex=0, clr=rgb(255, 255, 220), clr_anm=(rgb(255, 255, 255), rgb(220, 160, 255)), scl=.45,
         life=70, gen=14, init_pos=1, radius=4.0, alpha=(31, 31, 0), scl_anm=(.2, 1.0, 1.0, 60, 255))
    out[SKYEYE] = bytes(b)
    b, rs = kit(CRYSTAL)
    tex(b, 1, fxart.crystal_ball())
    b, card = added(b, fxart.tarot_death(), 24)
    tex(b, 0, fxart.tiny_spark())
    prop(b, rs, BALL13, scl=1.0, life=74, scl_anm=POPIN)
    prop(b, rs, SWIRL13, tex=0, clr=rgb(220, 160, 255), clr_anm=(rgb(255, 255, 255), rgb(180, 90, 255)), scl=.4,
         life=16, gen=1, gen_intvl=2, emtr_life=60, init_pos=1, radius=.7, vel=(.02, .02), alpha=(31, 31, 0))
    for res, sd in ((CARDS_E, "player"), (CARDS_P, "enemy")):
        spray(b, rs, res, sd, BALL13_AT[sd], (0, 22), 12, tex=card, clr=white, clr_anm=(white, white), scl=.8, gen=1,
              gen_intvl=3, emtr_life=12, radius=.3, spread=.02, alpha=(31, 31, 31), scl_anm=(1.0, 1.0, 1.0, 0, 255),
              flags_on=(1 << 14) | (1 << 12))
        rot(b, rs, res, spin=0x1C00)
    out[CRYSTAL] = bytes(b)
    b, rs = kit(COSMOS)
    tex(b, 0, fxart.psy_ring())
    for res, sd in ((0, "player"), (1, "enemy")):
        spray(b, rs, res, sd, EYE13_AT[sd], (0, 22), 12, tex=0, clr=rgb(240, 80, 220),
              clr_anm=(rgb(255, 220, 255), rgb(170, 60, 255)), scl=.9, gen=1, gen_intvl=2, emtr_life=16, radius=0,
              alpha=(31, 28, 0), scl_anm=(.4, 1.2, 1.8, 0, 200))
    out[COSMOS] = bytes(b)
    SET10_82 += [JETS, SKYEYE, CRYSTAL]

    # ---- set 14 --------------------------------------------------------------------------------------------
    # Gold Grill (Hyper Fang): gold wind-up chattering teeth - wound up, set down - clack clack clack across the
    # floor and CHOMP on their ankle, hanging on, till they kick it off
    for ps, flip in ((TEETHR, False), (TEETHL, True)):
        b, rs = kit(ps)
        b, shut = mirrored(b, fxart.wind_teeth(open_=False), flip=flip)
        if flip:
            b, op = mirrored(b, fxart.wind_teeth())
        else:
            tex(b, 1, fxart.wind_teeth())
            op = 1
        tex(b, 0, fxart.tiny_spark())
        prop(b, rs, TEETH_OPEN, tex=op, scl=1.15, life=4)
        prop(b, rs, TEETH_SHUT, tex=shut, scl=1.15, life=4)
        prop(b, rs, CHOMPFX, tex=0, clr=rgb(255, 230, 80), clr_anm=(rgb(255, 255, 255), rgb(255, 160, 40)), scl=.7,
             life=10, gen=4, init_pos=1, radius=.3, vel=(.08, 0), alpha=(31, 31, 0))
        prop(b, rs, 3, life=1)
        out[ps] = bytes(b)

    # Air It Out (Haze): the whole field's fogged up - they whip a dish towel like they're airing out the
    # bathroom, then psssht the air freshener, and it all clears out
    b, rs = kit(TOWELS)
    tex(b, 1, fxart.dish_towel())
    b, can = added(b, fxart.air_freshener())
    tex(b, 0, fxart.glow_dot())
    for res, ang in ((TOWEL_A, 0x1800), (TOWEL_B, -0x1400 & 0xFFFF)):
        prop(b, rs, res, scl=1.0, life=4)
        rot(b, rs, res, init=ang)
    prop(b, rs, SPRAYCAN, tex=can, scl=.8, life=30, scl_anm=POPIN)
    prop(b, rs, FRESH, tex=0, clr=rgb(150, 255, 220), clr_anm=(rgb(230, 255, 245), rgb(100, 220, 200)), scl=.5,
         life=20, gen=3, emtr_life=8, axis=(0, 1, 0), vel=(.06, .05), alpha=(26, 22, 0), scl_anm=(.4, 1.0, 1.8, 0, 200))
    out[TOWELS] = bytes(b)
    b, rs = kit(HAZEFOG)
    tex(b, 0, fxart.stink_puff())
    tex(b, 1, fxart.glint_tall())
    prop(b, rs, FOG14, tex=0, clr=rgb(170, 170, 180), clr_anm=(rgb(220, 220, 230), rgb(130, 130, 140)), scl=1.4,
         life=50, gen=4, emtr_life=2, init_pos=1, radius=1.6, vel=(.02, .005), alpha=(22, 22, 0),
         scl_anm=(.6, 1.2, 1.6, 40, 200), air_resist=120)
    prop(b, rs, FRESHGLINT, tex=1, clr=rgb(200, 255, 230), clr_anm=(rgb(255, 255, 255), rgb(140, 255, 210)), scl=.6,
         life=14, gen=1, gen_intvl=3, emtr_life=18, init_pos=1, radius=1.4, alpha=(31, 31, 0),
         scl_anm=(.2, 1.3, .2, 60, 160))
    out[HAZEFOG] = bytes(b)

    # Barricade (Barrier): they shove a couch in front of themselves - then a mattress - then a dresser on
    # top. Barricaded in.
    b, rs = kit(FURNITURE)
    tex(b, 1, fxart.couch())
    b, mat = added(b, fxart.mattress())
    b, dre = added(b, fxart.dresser())
    tex(b, 0, fxart.soot_puff())
    prop(b, rs, COUCH1, scl=1.3, life=SWING_STEP)
    prop(b, rs, MATTRESS1, tex=mat, scl=1.2, life=SWING_STEP)
    prop(b, rs, DRESSER1, tex=dre, scl=.9, life=SWING_STEP)
    prop(b, rs, DUST14, tex=0, clr=rgb(200, 180, 150), clr_anm=(rgb(240, 225, 200), rgb(160, 140, 110)), scl=.6,
         life=18, gen=5, init_pos=1, radius=.5, vel=(.08, 0), alpha=(26, 22, 0), scl_anm=(.4, 1.2, 1.7, 60, 200))
    out[FURNITURE] = bytes(b)

    # Zen Dome (Zen Headbutt): the singing bowl - DINNNG - om rings pulsing out, incense smoke, they glow and
    # float... then a full-speed headbutt
    b, rs = kit(ZEN)
    tex(b, 1, fxart.singing_bowl())
    tex(b, 0, fxart.om_ring())
    prop(b, rs, BOWL, scl=1.5, life=56, scl_anm=POPIN)
    prop(b, rs, OMRING, tex=0, clr=rgb(200, 140, 255), clr_anm=(rgb(255, 240, 255), rgb(150, 90, 255)), scl=.9,
         life=20, scl_anm=(.3, 2.0, 3.0, 100, 200), alpha=(31, 26, 0))
    for res in (2, 3):
        prop(b, rs, res, life=1)
    out[ZEN] = bytes(b)
    b, rs = kit(ZENFX)
    tex(b, 0, fxart.om_ring())
    tex(b, 1, fxart.steam_wisp())
    prop(b, rs, INCENSE, tex=1, clr=rgb(220, 210, 240), clr_anm=(rgb(255, 255, 255), rgb(180, 160, 220)), scl=.5,
         life=30, gen=1, gen_intvl=4, emtr_life=40, axis=(0, 1, 0), vel=(.004, .02), alpha=(22, 18, 0))
    prop(b, rs, ZENHIT, tex=0, clr=rgb(255, 120, 255), clr_anm=(rgb(255, 255, 255), rgb(170, 60, 255)), scl=1.2,
         life=14, scl_anm=(.3, 2.2, 3.0, 100, 200), alpha=(31, 28, 0))
    out[ZENFX] = bytes(b)

    # Freeloader (Leech Seed): the freeloading cousin hops over and plants himself right on top of them - feet
    # up, soda in hand - and their HP siphons back
    poses(COUSIN, fxart.freeloader(), 1.2, 44)
    no_delay(COUSIN, HOLD)
    b, rs = kit(LEECHFX)
    tex(b, 0, fxart.glow_dot())
    for res, sd in ((DRAIN14_E, "player"), (DRAIN14_P, "enemy")):
        drain(b, rs, res, sd, 18, tex=0, clr=rgb(120, 255, 100), clr_anm=(rgb(230, 255, 220), rgb(60, 200, 60)),
              scl=.5, gen=1, gen_intvl=2, emtr_life=24, init_pos=1, radius=.6, alpha=(31, 31, 10))
    out[LEECHFX] = bytes(b)

    # Drip Check (Swagger): a full-length mirror pops up - pose - pose - POSE - price tags flying, the drip
    # sparkling - and the foe gets dizzy just looking at it
    b, rs = kit(MIRROR)
    tex(b, 1, fxart.full_mirror())
    b, tag = added(b, fxart.price_tag())
    tex(b, 0, fxart.tiny_spark())
    prop(b, rs, MIRROR1, scl=1.2, life=70, scl_anm=POPIN)
    prop(b, rs, TAGS, tex=tag, scl=.7, life=30, gen=5, emtr_life=2, init_pos=1, radius=.4, vel=(.2, 0),
         alpha=(31, 31, 31), air_resist=120, flags_on=(1 << 14) | (1 << 12))
    rot(b, rs, TAGS, spin=0x0800)
    prop(b, rs, TWINKLE14, tex=0, clr=rgb(255, 255, 220), clr_anm=(rgb(255, 255, 255), rgb(255, 220, 80)), scl=.8,
         life=10, scl_anm=(.2, 1.6, .2, 60, 160), alpha=(31, 31, 0))
    prop(b, rs, 3, life=1)
    out[MIRROR] = bytes(b)
    b, rs = kit(DRIPFX)
    tex(b, 0, fxart.tiny_spark())
    prop(b, rs, DRIPSPARK, tex=0, clr=rgb(255, 240, 120), clr_anm=(rgb(255, 255, 255), rgb(120, 220, 255)), scl=.45,
         life=16, gen=2, gen_intvl=2, emtr_life=40, init_pos=1, radius=1.0, vel=(.01, .02), alpha=(31, 31, 0))
    prop(b, rs, DIZZY14, tex=0, clr=rgb(255, 230, 60), clr_anm=(rgb(255, 255, 200), rgb(255, 140, 40)), scl=.6,
         life=24, gen=1, gen_intvl=3, emtr_life=30, init_pos=1, radius=.5, axis=(0, 1, 0), vel=(.06, .01),
         alpha=(31, 31, 0))
    out[DRIPFX] = bytes(b)

    # Yell Woop (Roar): a police light starts spinning on their head - red, blue, red, blue - WOOP WOOP - and
    # the foe takes off running
    b, rs = kit(SIREN)
    tex(b, 1, fxart.police_light())
    b, blue = added(b, fxart.police_light(red=False))
    tex(b, 0, fxart.woop_wave())
    prop(b, rs, LIGHT_RED, scl=.8, life=4)
    prop(b, rs, LIGHT_BLUE, tex=blue, scl=.8, life=4)
    for res, sd in ((WOOP_E, "player"), (WOOP_P, "enemy")):
        spray(b, rs, res, sd, (0, 46), (0, 22), 12, tex=0, clr=rgb(255, 255, 255),
              clr_anm=(rgb(255, 120, 120), rgb(120, 160, 255)), scl=.9, gen=1, gen_intvl=3, emtr_life=24, radius=0,
              alpha=(31, 28, 0), scl_anm=(.6, 1.3, 1.8, 0, 200))
        if sd == "enemy":
            rot(b, rs, res, init=0x8000)
    out[SIREN] = bytes(b)
    sign(WOOP, ["WOOP", "WOOP!"], fill=(40, 60, 200, 255), text=(255, 255, 255, 255))

    # Security (Safeguard): a SECURITY bouncer steps up beside them, the velvet rope goes up - and a status
    # bubble floats over... and gets turned away at the rope
    b, rs = kit(SECURITY1)
    tex(b, 0, fxart.bouncer(), 30)
    b, rope = added(b, fxart.velvet_rope(), 24)
    prop(b, rs, POP, scl=ONE_TO_ONE / 1.1, life=74, scl_anm=POPIN)
    prop(b, rs, 1, tex=rope, scl=1.0, life=66, scl_anm=POPIN)
    out[SECURITY1] = bytes(b)
    no_delay(SECURITY1, 1)
    b, rs = kit(BUBBLES14)
    b, bub = added(b, fxart.status_bubble())
    tex(b, 0, fxart.tiny_spark())
    prop(b, rs, STATUSBUB, tex=bub, scl=.8, life=4)
    prop(b, rs, NOPE14, tex=0, clr=rgb(255, 230, 120), clr_anm=(rgb(255, 255, 255), rgb(255, 120, 80)), scl=.6,
         life=10, gen=5, init_pos=1, radius=.3, vel=(.1, 0), alpha=(31, 31, 0))
    for res in (2, 3):
        prop(b, rs, res, life=1)
    out[BUBBLES14] = bytes(b)

    # Wax On (Rock Polish): full car detail - an orbital buffer going in circles all over them, wax swirls,
    # sparkle, sparkle... then they zoom
    b, rs = kit(BUFFER)
    tex(b, 1, fxart.orbital_buffer())
    tex(b, 0, fxart.wax_swirl())
    for res, ang in ((BUFF_A, 0x0600), (BUFF_B, -0x0600 & 0xFFFF)):
        prop(b, rs, res, scl=.9, life=4)
        rot(b, rs, res, init=ang)
    prop(b, rs, SWIRLS14, tex=0, clr=rgb(240, 240, 255), clr_anm=(rgb(255, 255, 255), rgb(180, 200, 255)), scl=.7,
         life=14, alpha=(28, 24, 0), flags_on=(1 << 14) | (1 << 12))
    rot(b, rs, SWIRLS14, spin=0x1800)
    prop(b, rs, 3, life=1)
    out[BUFFER] = bytes(b)
    b, rs = kit(SHINE14)
    tex(b, 1, fxart.glint_tall())
    tex(b, 0, fxart.speed_streak())
    prop(b, rs, SHINE_UP, tex=1, clr=rgb(255, 255, 255), clr_anm=(rgb(255, 255, 255), rgb(200, 230, 255)), scl=.8,
         life=12, gen=1, gen_intvl=3, emtr_life=24, init_pos=1, radius=.9, scl_anm=(.2, 1.4, .2, 60, 160),
         alpha=(31, 31, 0))
    prop(b, rs, SPEED14, tex=0, clr=rgb(255, 255, 255), clr_anm=(rgb(255, 255, 255), rgb(220, 230, 255)), scl=.8,
         life=8, alpha=(31, 31, 0))
    out[SHINE14] = bytes(b)

    # Beef (Rage): steam pouring off them... and they start some BEEF - a giant raw T-bone steak, slapped right
    # across the foe. Twice.
    poses(STEAK, fxart.tbone_steak(), 1.2, 8)
    no_delay(STEAK, HOLD)
    b, rs = kit(STEAMFX)
    tex(b, 0, fxart.anger_steam())
    tex(b, 1, fxart.glint_tall())
    prop(b, rs, STEAMPUFF, tex=0, clr=rgb(255, 120, 100), clr_anm=(rgb(255, 255, 255), rgb(255, 80, 60)), scl=.6,
         life=18, gen=2, emtr_life=4, init_pos=1, radius=.3, axis=(0, 1, 0), vel=(.06, .04), alpha=(28, 24, 0),
         scl_anm=(.4, 1.2, 1.6, 60, 200))
    prop(b, rs, MEATHIT, tex=0, clr=rgb(255, 80, 80), clr_anm=(rgb(255, 230, 230), rgb(230, 40, 40)), scl=.9,
         life=12, gen=6, init_pos=1, radius=.4, vel=(.12, 0), alpha=(31, 31, 0))
    out[STEAMFX] = bytes(b)
    SET10_82 += [TEETHR, TEETHL, TOWELS, FURNITURE, ZEN, MIRROR, SIREN, BUBBLES14, BUFFER]

    # Big Bass (Magnitude): a GIANT largemouth bass drops out of the sky and flops - SLAM, SLAM, SLAM - the
    # whole field shakes
    b, rs = kit(BASSFISH)
    tex(b, 1, fxart.bass_fish())
    tex(b, 0, fxart.shock_ring())
    for res, ang in ((FLOP_A, 0x0C00), (FLOP_B, -0x0C00 & 0xFFFF)):
        prop(b, rs, res, scl=2.2, life=4)
        rot(b, rs, res, init=ang)
    prop(b, rs, SHOCK16, tex=0, clr=rgb(220, 200, 160), clr_anm=(rgb(255, 250, 230), rgb(170, 140, 100)), scl=1.6,
         life=18, scl_anm=(.3, 2.0, 3.0, 100, 200), alpha=(31, 26, 0))
    prop(b, rs, 3, life=1)
    out[BASSFISH] = bytes(b)
    b, rs = kit(BASSFX)
    tex(b, 0, fxart.fizz_drop())
    prop(b, rs, 0, tex=0, clr=rgb(90, 170, 255), clr_anm=(rgb(230, 248, 255), rgb(60, 150, 255)), scl=.45, life=22,
         gen=8, init_pos=1, radius=.8, axis=(0, 1, 0), vel=(.16, .2), gravity=(0, -.022, 0), alpha=(31, 31, 0))
    prop(b, rs, 1, life=1)
    out[BASSFX] = bytes(b)

    # Ice Chip (Ice Shard): a styrofoam cup of ice - flick flick flick - cubes pinging off them, fast
    b, rs = kit(ICECUP)
    tex(b, 1, fxart.foam_cup())
    tex(b, 0, fxart.ice_cube())
    prop(b, rs, CUP16, scl=.9, life=36, scl_anm=POPIN)
    for res, sd in ((ICE_E, "player"), (ICE_P, "enemy")):
        drops(b, rs, res, sd, ICECUP_AT[sd], (0, 24), 7, rgb(255, 255, 255), rgb(150, 210, 255), .45, emtr_life=3,
              gen=1, spread=.02, radius=.1, alpha=(31, 31, 31))
    prop(b, rs, 2, life=1)
    out[ICECUP] = bytes(b)
    b, rs = kit(ICEHIT)
    tex(b, 0, fxart.tiny_spark())
    prop(b, rs, 0, tex=0, clr=rgb(200, 240, 255), clr_anm=(rgb(255, 255, 255), rgb(120, 200, 255)), scl=.5, life=8,
         gen=3, init_pos=1, radius=.3, vel=(.08, 0), alpha=(31, 31, 0))
    prop(b, rs, 1, life=1)
    out[ICEHIT] = bytes(b)

    # Get Even (Revenge): out comes THE LIST - flip it open - their name, circled, X'd - then the book flies
    # over and SLAMS shut on them
    b, rs = kit(LISTBOOK)
    tex(b, 0, fxart.the_list(), 24)
    b, opened = added(b, fxart.the_list(open_=True), 16)
    prop(b, rs, POP, scl=ONE_TO_ONE, life=4)
    prop(b, rs, 1, tex=opened, scl=ONE_TO_ONE, life=4)
    out[LISTBOOK] = bytes(b)
    no_delay(LISTBOOK, 1)
    b, rs = kit(LISTFX)
    tex(b, 0, fxart.impact_ring())
    prop(b, rs, 0, tex=0, clr=rgb(255, 80, 80), clr_anm=(rgb(255, 255, 255), rgb(230, 30, 30)), scl=1.0, life=12,
         scl_anm=(.4, 1.6, 2.0, 60, 200), alpha=(31, 31, 0))
    prop(b, rs, 1, life=1)
    out[LISTFX] = bytes(b)

    # Car Magnet (Magnet Bomb): a giant horseshoe magnet - the foe gets dragged in - hubcaps come flying in
    # from everywhere and pile on - then it all goes off
    b, rs = kit(MAGNET14)
    tex(b, 1, fxart.horseshoe_magnet())
    b, left = mirrored(b, fxart.horseshoe_magnet())
    b, cap = added(b, fxart.hubcap())
    tex(b, 0, fxart.magnet_lines())
    for res, t in ((MAG_R, 1), (MAG_L, left)):
        prop(b, rs, res, tex=t, scl=1.0, life=60, scl_anm=POPIN)
    prop(b, rs, HUBCAP16, tex=cap, scl=.7, life=4, flags_on=(1 << 14) | (1 << 12))
    rot(b, rs, HUBCAP16, spin=0x1800)
    prop(b, rs, PULL16, tex=0, clr=rgb(255, 230, 120), clr_anm=(rgb(255, 255, 255), rgb(255, 150, 60)), scl=1.0,
         life=10, alpha=(31, 26, 0), scl_anm=(1.4, 1.0, .6, 0, 200))
    out[MAGNET14] = bytes(b)

    # One-Two (Double Hit): DING DING - the bell - and a red boxing glove pops them (once per hit: quick)
    b, rs = kit(BELL14)
    tex(b, 0, fxart.boxing_bell(), 30)
    prop(b, rs, POP, scl=.9, life=4)
    prop(b, rs, 1, life=1)
    out[BELL14] = bytes(b)
    b, rs = kit(GLOVES)
    b = held(b, rs, GLOVE_R, GLOVE_L, fxart.boxing_glove(), 1.0, 4)
    tex(b, 0, fxart.impact_ring())
    prop(b, rs, PUNCH16, tex=0, clr=rgb(255, 230, 80), clr_anm=(rgb(255, 255, 255), rgb(255, 150, 40)), scl=.9,
         life=10, scl_anm=(.4, 1.4, 1.8, 60, 200), alpha=(31, 31, 0))
    prop(b, rs, 3, life=1)
    out[GLOVES] = bytes(b)

    # Power Bank (Charge Beam): the phone's on 1%... plugged into the power bank... 50%... 100% - FULL BATTERY
    # - and it fires a beam
    b, rs = kit(PHONE16)
    tex(b, 1, fxart.phone_battery(level=0))
    b, half = added(b, fxart.phone_battery(level=1))
    b, full = added(b, fxart.phone_battery(level=2))
    tex(b, 0, fxart.tiny_spark())
    prop(b, rs, BATT_LOW, scl=ONE_TO_ONE, life=4)
    prop(b, rs, BATT_HALF, tex=half, scl=ONE_TO_ONE, life=4)
    prop(b, rs, BATT_FULL, tex=full, scl=ONE_TO_ONE, life=4)
    prop(b, rs, ZAPS16, tex=0, clr=rgb(255, 240, 80), clr_anm=(rgb(255, 255, 255), rgb(120, 220, 255)), scl=.45,
         life=8, gen=3, init_pos=1, radius=.4, vel=(.06, 0), alpha=(31, 31, 0))
    out[PHONE16] = bytes(b)
    b, rs = kit(BANK16)
    tex(b, 0, fxart.power_bank(), 30)
    prop(b, rs, POP, scl=.9, life=60, scl_anm=POPIN)
    prop(b, rs, 1, life=1)
    out[BANK16] = bytes(b)
    b, rs = kit(BEAM16)
    tex(b, 0, fxart.glow_dot())
    for res, sd in ((0, "player"), (1, "enemy")):
        spray(b, rs, res, sd, PHONE16_AT[sd], (0, 22), 10, tex=0, clr=rgb(120, 255, 120),
              clr_anm=(rgb(230, 255, 230), rgb(60, 220, 255)), scl=.7, gen=3, gen_intvl=1, emtr_life=20, radius=.2,
              spread=.01, alpha=(31, 31, 10), scl_anm=(.6, 1.0, 1.3, 0, 200))
    out[BEAM16] = bytes(b)

    # Duck Down (Minimize): a round clothing rack slides in and they duck right into it - the shirts rustle -
    # two eyes peek out
    b, rs = kit(RACK)
    tex(b, 1, fxart.clothes_rack())
    b, eyes = added(b, fxart.peek_eyes())
    tex(b, 0, fxart.whoosh_arc())
    prop(b, rs, RACK1, scl=1.4, life=4)
    prop(b, rs, PEEK, tex=eyes, scl=.6, life=4)
    prop(b, rs, RUSTLE, tex=0, clr=rgb(255, 255, 255), clr_anm=(rgb(255, 255, 255), rgb(220, 220, 230)), scl=.6,
         life=8, alpha=(28, 24, 0))
    prop(b, rs, 3, life=1)
    out[RACK] = bytes(b)

    # Brain Freeze (Ice Fang): a giant slushie, chugged - BRAIN FREEZE - icicles, shivering - then jaws of ice
    # CHOMP down on the foe
    b, rs = kit(SLUSH)
    tex(b, 1, fxart.slushie())
    tex(b, 0, fxart.icicle())
    prop(b, rs, CUP_SLUSH, scl=.8, life=30, scl_anm=POPIN)
    prop(b, rs, ICICLES, tex=0, clr=rgb(180, 230, 255), clr_anm=(rgb(255, 255, 255), rgb(120, 200, 255)), scl=.5,
         life=30, gen=6, init_pos=1, radius=.8, alpha=(31, 31, 0), scl_anm=(.2, 1.0, 1.0, 40, 255))
    for res in (2, 3):
        prop(b, rs, res, life=1)
    out[SLUSH] = bytes(b)
    b, rs = kit(JAWS16)
    tex(b, 1, fxart.frost_jaws())
    b, shut = added(b, fxart.frost_jaws(shut=True))
    tex(b, 0, fxart.tiny_spark())
    prop(b, rs, JAWS_OPEN, scl=1.2, life=4)
    prop(b, rs, JAWS_SHUT, tex=shut, scl=1.2, life=12)
    prop(b, rs, FROST16, tex=0, clr=rgb(200, 240, 255), clr_anm=(rgb(255, 255, 255), rgb(120, 200, 255)), scl=.5,
         life=14, gen=6, init_pos=1, radius=.6, vel=(.05, .02), alpha=(31, 31, 0))
    prop(b, rs, 3, life=1)
    out[JAWS16] = bytes(b)

    # Lock On (Lock-On): the binoculars come up - everything goes black but two circles - zoom... focus... LOCKED
    b, rs = kit(BINOC)
    tex(b, 0, fxart.binoculars(), 30)
    b, ret = added(b, fxart.scope_reticle(), 8)
    prop(b, rs, POP, scl=.9, life=44, scl_anm=POPIN)
    prop(b, rs, 1, tex=ret, scl=SIGN_SCALE, life=4)
    out[BINOC] = bytes(b)
    no_delay(BINOC, 1)

    # Night Shank (Night Slash): lights out - pitch black - two glowing eyes - shink, shink, shink - the
    # flashlight clicks on: fresh slash marks on the foe... and the attacker, whistling
    b, rs = kit(NIGHT16)
    tex(b, 1, fxart.claw_slashes())
    b, eyes = added(b, fxart.glow_eyes())
    b, beam = added(b, fxart.flashlight_click(), 16)
    tex(b, 0, fxart.whistle_note())
    prop(b, rs, EYES16, tex=eyes, scl=.8, life=4)
    prop(b, rs, SLASHES16, scl=1.1, life=40, scl_anm=(.2, 1.0, 1.0, 80, 255))
    prop(b, rs, TORCH16, tex=beam, scl=2.2, life=40, scl_anm=(.2, 1.0, 1.0, 120, 255))
    prop(b, rs, NOTES16, tex=0, clr=rgb(255, 255, 200), clr_anm=(rgb(255, 255, 255), rgb(255, 220, 120)), scl=.5,
         life=22, gen=1, gen_intvl=6, emtr_life=24, axis=(.4, 1, 0), vel=(0, .02), alpha=(31, 31, 0))
    out[NIGHT16] = bytes(b)
    SET10_82 += [BASSFISH, ICECUP, MAGNET14, GLOVES, PHONE16, RACK, SLUSH, JAWS16, NIGHT16]

    # Got Ya Back (Helping Hand): the secret handshake - SLAP - hook - slide - fist bump - EXPLODE - gold glow
    b, rs = kit(SHAKE)
    tex(b, 1, fxart.handshake(step=0))
    b, hook = added(b, fxart.handshake(step=1))
    b, bump = added(b, fxart.handshake(step=2))
    tex(b, 0, fxart.tiny_spark())
    prop(b, rs, HAND_SLAP, scl=1.6, life=4)
    prop(b, rs, HAND_HOOK, tex=hook, scl=1.6, life=4)
    prop(b, rs, HAND_BUMP, tex=bump, scl=1.6, life=4)
    prop(b, rs, GOLDUP, tex=0, clr=rgb(255, 220, 60), clr_anm=(rgb(255, 255, 220), rgb(255, 180, 40)), scl=.5, life=20,
         gen=2, gen_intvl=2, emtr_life=20, init_pos=1, radius=.8, axis=(0, 1, 0), vel=(.01, .03), alpha=(31, 31, 0))
    out[SHAKE] = bytes(b)
    b, rs = kit(SHAKEFX)
    tex(b, 0, fxart.camera_flash())
    prop(b, rs, 0, tex=0, clr=rgb(255, 240, 120), clr_anm=(rgb(255, 255, 255), rgb(255, 180, 40)), scl=1.4, life=12,
         scl_anm=(.2, 1.6, 2.0, 60, 200), alpha=(31, 31, 0))
    prop(b, rs, 1, tex=0, clr=rgb(255, 220, 80), clr_anm=(rgb(255, 255, 255), rgb(255, 160, 30)), scl=.5, life=20,
         gen=10, init_pos=1, radius=.3, vel=(.14, 0), alpha=(31, 31, 0))
    out[SHAKEFX] = bytes(b)

    # Ice Out (Ice Beam): a stream of diamonds blasts them - and they get iced out: frozen in a block of ice
    # encrusted with diamonds
    b, rs = kit(DIAMONDS)
    tex(b, 0, fxart.diamond())
    for res, sd in ((DIAM_E, "player"), (DIAM_P, "enemy")):
        spray(b, rs, res, sd, (22 if sd == "player" else -22, 28), (0, 22), 12, tex=0, clr=rgb(200, 240, 255),
              clr_anm=(rgb(255, 255, 255), rgb(120, 200, 255)), scl=.55, gen=3, gen_intvl=1, emtr_life=18, radius=.2,
              spread=.015, alpha=(31, 31, 10), flags_on=(1 << 14) | (1 << 12))
        rot(b, rs, res, spin=0x0C00)
    out[DIAMONDS] = bytes(b)
    b, rs = kit(ICEBLOCK)
    tex(b, 0, fxart.ice_block(), 30)
    prop(b, rs, POP, scl=1.5, life=44, scl_anm=(.2, 1.1, 1.0, 60, 255))
    prop(b, rs, 1, life=1)
    out[ICEBLOCK] = bytes(b)

    # Stone Cold (Stone Edge): shades on, slow, deadpan - and massive rock spikes burst up out of the ground
    # under the foe, one after another
    b, rs = kit(SPIKES)
    tex(b, 1, fxart.rock_spike())
    tex(b, 0, fxart.soot_puff())
    for res, scl in ((SPIKE_A, 1.5), (SPIKE_B, 1.2), (SPIKE_C, 1.0)):
        prop(b, rs, res, scl=scl, life=36, scl_anm=(.1, 1.15, 1.0, 120, 255))
    prop(b, rs, 0, tex=0, clr=rgb(170, 150, 120), clr_anm=(rgb(230, 215, 190), rgb(120, 100, 80)), scl=.7, life=20,
         gen=5, init_pos=1, radius=.5, vel=(.1, .02), alpha=(26, 22, 0), scl_anm=(.4, 1.2, 1.7, 60, 200))
    out[SPIKES] = bytes(b)
    b, rs = kit(COLDSHADES)
    b, shades = added(b, fxart.deal_shades_small())
    prop(b, rs, SHADES16, tex=shades, scl=1.0, life=SWING_STEP)
    for res in (0, 2, 3):
        prop(b, rs, res, life=1)
    out[COLDSHADES] = bytes(b)

    # Rizz Up (Attract): a candlelit table for two pops up - spaghetti, a rose - hearts everywhere, they wiggle
    # their eyebrows - and the foe swoons
    b, rs = kit(DATE)
    tex(b, 1, fxart.date_table())
    prop(b, rs, DATE1, scl=1.3, life=70, scl_anm=POPIN)
    for res in (0, 2, 3):
        prop(b, rs, res, life=1)
    out[DATE] = bytes(b)
    b, rs = kit(HEARTS16)
    tex(b, 0, fxart.fat_heart())
    prop(b, rs, 0, tex=0, clr=rgb(255, 80, 150), clr_anm=(rgb(255, 210, 230), rgb(230, 40, 110)), scl=.6, life=26,
         gen=1, gen_intvl=3, emtr_life=40, init_pos=1, radius=1.0, axis=(0, 1, 0), vel=(.01, .025), alpha=(31, 31, 0),
         scl_anm=(.4, 1.2, 1.0, 50, 255))
    prop(b, rs, 1, tex=0, clr=rgb(255, 80, 150), clr_anm=(rgb(255, 230, 240), rgb(230, 40, 110)), scl=.9, life=16,
         gen=8, init_pos=1, radius=.3, vel=(.12, 0), alpha=(31, 31, 0))
    out[HEARTS16] = bytes(b)

    # Pickup Line (Captivate): a smooth speech bubble - "U FROM TENNESSEE?" - and the foe blushes bright red
    b, rs = kit(PICKUP)
    tex(b, 0, fxart.pickup_bubble(), 30)
    prop(b, rs, POP, scl=SIGN_SCALE, life=44, scl_anm=SIGN_POP)
    prop(b, rs, 1, life=1)
    out[PICKUP] = bytes(b)
    b, rs = kit(BLUSH)
    tex(b, 0, fxart.fat_heart())
    prop(b, rs, 0, tex=0, clr=rgb(255, 80, 150), clr_anm=(rgb(255, 210, 230), rgb(230, 40, 110)), scl=.55, life=22,
         gen=1, gen_intvl=3, emtr_life=24, init_pos=1, radius=.6, axis=(0, 1, 0), vel=(.01, .03), alpha=(31, 31, 0))
    prop(b, rs, 1, life=1)
    out[BLUSH] = bytes(b)

    # Ice Cold (Icy Wind): a window AC cranked to MAX, rattling - a blast of snowflakes - the foe shivers, frozen
    b, rs = kit(ACUNIT)
    tex(b, 1, fxart.window_ac())
    prop(b, rs, AC1, scl=1.1, life=4)
    for res in (0, 2, 3):
        prop(b, rs, res, life=1)
    out[ACUNIT] = bytes(b)
    b, rs = kit(FLAKES)
    tex(b, 0, fxart.snowflake())
    for res, sd in ((FLAKES_E, "player"), (FLAKES_P, "enemy")):
        spray(b, rs, res, sd, (-30 if sd == "player" else 30, 30), (0, 22), 14, tex=0, clr=rgb(220, 240, 255),
              clr_anm=(rgb(255, 255, 255), rgb(150, 210, 255)), scl=.5, gen=3, gen_intvl=1, emtr_life=24, radius=.4,
              spread=.03, alpha=(31, 31, 10), flags_on=(1 << 14) | (1 << 12))
        rot(b, rs, res, spin=0x0800)
    out[FLAKES] = bytes(b)

    # Ground Game (Earth Power): the manhole under the foe starts rattling... clank, clank... then BLOWS - the
    # cover rockets up spinning on a geyser of sewer steam, and takes the foe with it
    b, rs = kit(POTHOLE1)
    tex(b, 1, fxart.manhole_flat())
    tex(b, 0, fxart.soot_puff())
    prop(b, rs, HOLE1, scl=.95, life=4)
    prop(b, rs, STEAMUP, tex=0, clr=rgb(220, 220, 210), clr_anm=(rgb(255, 255, 250), rgb(150, 160, 120)), scl=1.0,
         life=26, gen=3, gen_intvl=1, emtr_life=20, init_pos=1, radius=.3, axis=(0, 1, 0), vel=(.03, .2),
         alpha=(28, 24, 0), scl_anm=(.4, 1.3, 2.0, 60, 200), air_resist=124)
    for res in (2, 3):
        prop(b, rs, res, life=1)
    out[POTHOLE1] = bytes(b)
    b, rs = kit(CONES)
    b, disc = added(b, fxart.manhole_disc())
    mover(b, rs, CONE_A, .6, 7, tex=disc, scl=1.1, life=26, flags_on=(1 << 14) | (1 << 12))   # rocketing up
    rot(b, rs, CONE_A, spin=0x1C00)
    for res in (0, 2, 3):
        prop(b, rs, res, life=1)
    out[CONES] = bytes(b)

    # Tailgate (Tailwind): a pickup backs in, the tailgate drops - grill smoking, the cooler, a foam finger -
    # the whole squad hyped up and fast
    b, rs = kit(TAILGATE)
    tex(b, 1, fxart.pickup_tailgate())
    tex(b, 0, fxart.soot_puff())
    prop(b, rs, GATE1, scl=1.4, life=4)
    prop(b, rs, GATEPUFF, tex=0, clr=rgb(200, 200, 205), clr_anm=(rgb(250, 250, 250), rgb(150, 150, 155)), scl=.5,
         life=24, gen=1, gen_intvl=3, emtr_life=50, axis=(0, 1, 0), vel=(.01, .02), alpha=(24, 20, 0),
         scl_anm=(.4, 1.2, 1.8, 60, 200))
    for res in (2, 3):
        prop(b, rs, res, life=1)
    out[TAILGATE] = bytes(b)
    b, rs = kit(GRILLSMOKE)
    tex(b, 0, fxart.speed_streak())
    prop(b, rs, 0, tex=0, clr=rgb(255, 255, 255), clr_anm=(rgb(255, 255, 255), rgb(220, 230, 255)), scl=.8, life=8,
         alpha=(31, 31, 0))
    prop(b, rs, 1, life=1)
    out[GRILLSMOKE] = bytes(b)

    # Iced Out (Blizzard): a shaved-ice machine goes haywire - shaking, cranking itself - and buries the whole
    # block in snow
    b, rs = kit(SNOWMACH)
    tex(b, 1, fxart.shaved_ice_machine())
    prop(b, rs, MACH1, scl=1.2, life=4)
    for res in (0, 2, 3):
        prop(b, rs, res, life=1)
    out[SNOWMACH] = bytes(b)
    b, rs = kit(SNOWSTORM)
    tex(b, 0, fxart.snowflake())
    for res, scl in ((STORM_A, .55), (STORM_B, .35)):
        prop(b, rs, res, tex=0, clr=rgb(230, 245, 255), clr_anm=(rgb(255, 255, 255), rgb(170, 220, 255)), scl=scl,
             life=50, gen=2, gen_intvl=1, emtr_life=50, init_pos=1, radius=3.4, axis=(-.3, -1, 0), vel=(.02, .16),
             alpha=(31, 31, 0), flags_on=(1 << 14) | (1 << 12))
        rot(b, rs, res, spin=0x0600)
    out[SNOWSTORM] = bytes(b)

    # Photo Op (Synthesis): the ring light comes on - selfie - and a whole storm of paparazzi flashes - they
    # glow up (and heal)
    b, rs = kit(RINGLIGHT)
    tex(b, 1, fxart.ring_light())
    tex(b, 0, fxart.glow_dot())
    prop(b, rs, RLIGHT, scl=1.1, life=70, scl_anm=POPIN)
    prop(b, rs, RL_GLOW, tex=0, clr=rgb(255, 250, 210), clr_anm=(rgb(255, 255, 255), rgb(255, 230, 150)), scl=2.0,
         life=60, alpha=(14, 12, 0), scl_anm=(.4, 1.0, 1.0, 40, 255))
    for res in (2, 3):
        prop(b, rs, res, life=1)
    out[RINGLIGHT] = bytes(b)
    b, rs = kit(FLASHES)
    tex(b, 0, fxart.camera_flash())
    prop(b, rs, 0, tex=0, clr=rgb(255, 255, 255), clr_anm=(rgb(255, 255, 255), rgb(220, 230, 255)), scl=.9, life=4,
         gen=1, init_pos=1, radius=2.0, alpha=(31, 31, 31))
    prop(b, rs, 1, tex=0, clr=rgb(255, 250, 200), clr_anm=(rgb(255, 255, 255), rgb(255, 230, 120)), scl=.5, life=24,
         gen=2, gen_intvl=3, emtr_life=30, init_pos=1, radius=.8, axis=(0, 1, 0), vel=(.01, .02), alpha=(31, 31, 0))
    out[FLASHES] = bytes(b)
    SET10_82 += [SHAKE, SPIKES, COLDSHADES, DATE, ACUNIT, POTHOLE1, CONES, TAILGATE, SNOWMACH, RINGLIGHT]


    # ---- set 17: common moves ------------------------------------------------------------------------------
    def burst(b, rs, res, clr, hi, scl, n, speed, up=0, gravity=0., life=24, radius=.4, spin=0, **edit):
        """Res as a one-shot burst of n tinted particles flying out (and up) - chunks, sparks, peanuts."""
        args = dict(tex=0, clr=clr, clr_anm=(hi, clr), scl=scl, life=life, gen=n, init_pos=1, radius=radius,
                    axis=(0, 1, 0), vel=(speed, up), gravity=(0, -gravity, 0), alpha=(31, 31, 0))
        if spin:
            args["flags_on"] = (1 << 14) | (1 << 12)
        args.update(edit)
        prop(b, rs, res, **args)
        if spin:
            rot(b, rs, res, spin=spin)

    def unused(b, rs, *res):
        for r in res:
            prop(b, rs, r, life=1)

    def to_attacker(side, frm, frames):
        """(vx, vy) px a frame that carry something from `frm` (px from the foe) back to the attacker's chest."""
        dx, dy = TARGET_FROM_ATTACKER[side]
        return (-dx - frm[0]) / frames, (-dy - frm[1] + 20) / frames

    # Box Cutter (Cut): a FRAGILE box drops over the foe - the cutter clicks out, click, click - slash, slash -
    # the box bursts open in a spray of packing peanuts
    b, rs = kit(BOX17)
    tex(b, 1, fxart.fragile_box())
    b, opened = added(b, fxart.fragile_box_open(), 30)
    tex(b, 0, fxart.peanut())
    prop(b, rs, BOXSHUT, scl=ONE_TO_ONE, life=4)
    prop(b, rs, BOXOPEN, tex=opened, scl=ONE_TO_ONE, life=40)
    burst(b, rs, PEANUTS, rgb(250, 246, 225), rgb(255, 255, 255), .45, 16, .2, up=.3, gravity=.022, life=30,
          spin=0x0900)
    unused(b, rs, 3)
    out[BOX17] = bytes(b)
    b, rs = kit(CUTTER17)
    tex(b, 1, fxart.box_cutter())
    b, tucked = added(b, fxart.box_cutter(out=False))
    b, left = mirrored(b, fxart.box_cutter(), 24)
    tex(b, 0, fxart.tiny_spark())
    prop(b, rs, CUTOUT_R, scl=1.0, life=4)
    prop(b, rs, CUTIN_R, tex=tucked, scl=1.0, life=4)
    prop(b, rs, CUTOUT_L, tex=left, scl=1.0, life=4)
    burst(b, rs, CUTSPARK, rgb(255, 255, 220), rgb(255, 255, 255), .45, 4, .12, life=10)
    out[CUTTER17] = bytes(b)
    b, rs = kit(CUTL17)
    from PIL import Image as _Img
    tex(b, 0, fxart.box_cutter(out=False).transpose(_Img.FLIP_LEFT_RIGHT), 30)
    b, xcut = added(b, fxart.x_slash(), 16)
    prop(b, rs, CUTIN_L, scl=1.0, life=4)
    prop(b, rs, XCUT, tex=xcut, scl=1.15, life=14, scl_anm=(.4, 1.1, 1.0, 40, 255))
    out[CUTL17] = bytes(b)
    no_delay(CUTL17, XCUT)

    # Muscle (Strength): plates clank onto the bar, one, two, three - a shaky overhead press - and the whole
    # thing comes down on the foe. The little plates roll off.
    b, rs = kit(BAR17)
    tex(b, 1, fxart.barbell(plates=1))
    b, two = added(b, fxart.barbell(plates=2), 30)
    b, three = added(b, fxart.barbell(plates=3), 30)
    tex(b, 0, fxart.fizz_drop())
    prop(b, rs, BAR1, scl=1.4, life=4)
    prop(b, rs, BAR2, tex=two, scl=1.4, life=4)
    prop(b, rs, BAR3, tex=three, scl=1.4, life=4)
    burst(b, rs, SWEAT17, rgb(150, 210, 255), rgb(240, 250, 255), .35, 2, .08, up=.12, gravity=.012, life=18,
          emtr_life=24, gen_intvl=3, radius=.5)
    out[BAR17] = bytes(b)
    b, rs = kit(PLATE17)
    tex(b, 1, fxart.weight_plate(), 24)
    tex(b, 0, fxart.soot_puff())
    for res, d in ((ROLL_R, 1), (ROLL_L, -1)):
        mover(b, rs, res, d * 3.2, 0, tex=1, scl=.62, life=34, flags_on=(1 << 14) | (1 << 12))
        rot(b, rs, res, spin=-d * 0x1400)
    burst(b, rs, SLAMPUFF, rgb(200, 190, 170), rgb(250, 245, 235), .9, 8, .16, up=.03, life=24, radius=.6,
          alpha=(26, 20, 0), scl_anm=(.5, 1.3, 1.8, 60, 200))
    out[PLATE17] = bytes(b)

    # Smash n Grab (Rock Smash): a jewelry case in front of the foe - the crowbar winds up - SMASH - glass
    # everywhere, and the gold chain flies back to the attacker
    b, rs = kit(CASE17)
    tex(b, 1, fxart.jewelry_case())
    b, broke = added(b, fxart.jewelry_case(broken=True), 30)
    tex(b, 0, fxart.glass_shard())
    prop(b, rs, CASE1, scl=1.15, life=4)
    prop(b, rs, CASEBROKE, tex=broke, scl=1.15, life=46)
    burst(b, rs, SHARDS, rgb(170, 225, 255), rgb(255, 255, 255), .5, 16, .28, up=.22, gravity=.02, life=28,
          spin=0x0C00)
    unused(b, rs, 3)
    out[CASE17] = bytes(b)
    b, rs = kit(CROW17)
    tex(b, 0, fxart.crowbar(), 30)
    b, left = mirrored(b, fxart.crowbar(), 30)
    prop(b, rs, CROW_R, scl=1.1, life=4)
    prop(b, rs, CROW_L, tex=left, scl=1.1, life=4)
    out[CROW17] = bytes(b)
    no_delay(CROW17, CROW_L)
    b, rs = kit(LOOT17)
    tex(b, 1, fxart.gold_chain_loot(), 24)
    tex(b, 0, fxart.tiny_spark())
    for res, sd in ((CHAIN_E, "player"), (CHAIN_P, "enemy")):
        mover(b, rs, res, *to_attacker(sd, SMASH_CASE[sd], CHAIN_FRAMES), tex=1, scl=.85, life=CHAIN_FRAMES + 8)
    burst(b, rs, LOOTSPARK, rgb(255, 230, 90), rgb(255, 255, 230), .5, 6, .14, life=16)
    out[LOOT17] = bytes(b)

    # Lay Low (Dig): turn 1 - the shovel goes to work, dirt flying, they hop in the hole and a road barricade
    # goes up over it. Turn 2 - the ground rumbles under the foe... and they ERUPT out of it
    b, rs = kit(SHOVEL17)
    tex(b, 1, fxart.shovel_dig())
    b, hole = added(b, fxart.dirt_hole(), 24)
    b, horse = added(b, fxart.sawhorse(), 24)
    tex(b, 0, fxart.dirt_clod())
    prop(b, rs, SHOVEL1, scl=1.2, life=4)
    prop(b, rs, HOLE17, tex=hole, scl=1.3, life=4)
    prop(b, rs, BARRICADE, tex=horse, scl=1.1, life=4)
    burst(b, rs, CLODS, rgb(130, 85, 45), rgb(185, 135, 85), .55, 10, .14, up=.34, gravity=.026, life=26,
          spin=0x0800)
    out[SHOVEL17] = bytes(b)
    b, rs = kit(DIRT17)
    tex(b, 1, fxart.tall_puff())
    tex(b, 0, fxart.soot_puff())
    prop(b, rs, ERUPT, tex=1, clr=rgb(125, 85, 45), clr_anm=(rgb(190, 140, 90), rgb(100, 65, 35)), scl=.85,
         life=20, gen=3, gen_intvl=1, emtr_life=10, init_pos=1, radius=.5, axis=(0, 1, 0), vel=(.04, .36),
         gravity=(0, -.012, 0), alpha=(31, 28, 0), scl_anm=(.5, 1.2, 1.6, 60, 200))
    prop(b, rs, DUSTRING, tex=0, clr=rgb(170, 130, 85), clr_anm=(rgb(220, 190, 150), rgb(130, 95, 60)), scl=.7,
         life=22, gen=8, init_pos=1, radius=.5, axis=(0, 1, 0), vel=(.16, .02), alpha=(28, 22, 0),
         scl_anm=(.5, 1.2, 1.6, 60, 200))
    out[DIRT17] = bytes(b)

    # Hot Hands (Fire Punch): the glove goes on the stove's coil burner, cranked to HI - sizzling - FWOOSH, it
    # catches fire - and the flaming glove goes right in their face. They hop around smoking.
    b, rs = kit(STOVE17)
    tex(b, 1, fxart.coil_burner())
    b, hot = added(b, fxart.hot_glove(), 24)
    b, fire = added(b, fxart.flaming_glove(), 30)
    tex(b, 0, fxart.glow_dot())
    prop(b, rs, BURNER, scl=1.15, life=4)
    prop(b, rs, HOTGLOVE_R, tex=hot, scl=1.0, life=4)
    prop(b, rs, FIREGLOVE_R, tex=fire, scl=1.05, life=4)
    prop(b, rs, HEATUP, tex=0, clr=rgb(255, 120, 30), clr_anm=(rgb(255, 230, 120), rgb(230, 40, 10)), scl=.5,
         life=16, gen=2, gen_intvl=1, emtr_life=6, init_pos=1, radius=.4, axis=(0, 1, 0), vel=(.02, .16),
         alpha=(31, 31, 0), scl_anm=(1.0, 1.0, .3, 0, 140))
    out[STOVE17] = bytes(b)
    b, rs = kit(GLOVEL17)
    tex(b, 0, fxart.flaming_glove().transpose(_Img.FLIP_LEFT_RIGHT), 30)
    b, hot = mirrored(b, fxart.hot_glove(), 24)
    prop(b, rs, FIREGLOVE_L, scl=1.05, life=4)
    prop(b, rs, HOTGLOVE_L, tex=hot, scl=1.0, life=4)
    out[GLOVEL17] = bytes(b)
    no_delay(GLOVEL17, HOTGLOVE_L)
    b, rs = kit(FLAMES17)
    tex(b, 1, fxart.flame_tongue())
    tex(b, 0, fxart.soft_puff())
    prop(b, rs, FLAMEHIT, tex=1, clr=rgb(255, 120, 20), clr_anm=(rgb(255, 240, 120), rgb(220, 30, 10)), scl=.55,
         life=18, gen=3, gen_intvl=1, emtr_life=8, init_pos=1, radius=.7, axis=(0, 1, 0), vel=(.06, .16),
         alpha=(31, 31, 0), scl_anm=(.4, 1.2, .5, 50, 160))
    prop(b, rs, STEAM17, tex=0, clr=rgb(200, 200, 205), clr_anm=(rgb(255, 255, 255), rgb(130, 130, 135)), scl=.7,
         life=28, gen=1, gen_intvl=3, emtr_life=30, init_pos=1, radius=.5, axis=(0, 1, 0), vel=(.01, .1),
         alpha=(24, 20, 0), scl_anm=(.4, 1.2, 1.8, 60, 200))
    out[FLAMES17] = bytes(b)
    SET10_82 += [BOX17, CUTTER17, BAR17, CASE17, SHOVEL17, STOVE17]


    # Taser Punch (ThunderPunch): a boxing glove with a taser duct-taped to it - bzzt, bzzt - the punch - and
    # BZZZZT: the foe lit up, crackling, smoking
    b, rs = kit(TGLOVE17)
    tex(b, 1, fxart.taser_glove())
    b, left = mirrored(b, fxart.taser_glove(), 30)
    tex(b, 0, fxart.zig_spark())
    prop(b, rs, TGLOVE_R, scl=1.1, life=4)
    prop(b, rs, TGLOVE_L, tex=left, scl=1.1, life=4)
    burst(b, rs, ZSPARK, rgb(255, 240, 80), rgb(255, 255, 255), .5, 5, .18, up=.06, life=10, spin=0x1000)
    unused(b, rs, 3)
    out[TGLOVE17] = bytes(b)
    b, rs = kit(ZAPB17)
    tex(b, 0, fxart.zap_burst(), 30)
    prop(b, rs, ZAPBURST, scl=1.6, life=14, scl_anm=(.3, 1.2, 1.0, 40, 255), flags_on=(1 << 14) | (1 << 12))
    rot(b, rs, ZAPBURST, spin=0x0600)
    unused(b, rs, 1)
    out[ZAPB17] = bytes(b)
    b, rs = kit(ZAPS17)
    tex(b, 1, fxart.bolt_tall())
    tex(b, 0, fxart.soot_puff())
    prop(b, rs, BOLTS17, tex=1, clr=rgb(255, 240, 90), clr_anm=(rgb(255, 255, 255), rgb(255, 200, 30)), scl=.9,
         life=3, gen=2, gen_intvl=2, emtr_life=30, init_pos=1, radius=.8, alpha=(31, 31, 31),
         flags_on=(1 << 14) | (1 << 12))
    rot(b, rs, BOLTS17, spin=0x2000, init=0x1000)
    prop(b, rs, SMOKE17, tex=0, clr=rgb(70, 70, 75), clr_anm=(rgb(150, 150, 155), rgb(40, 40, 45)), scl=.7, life=30,
         gen=1, gen_intvl=3, emtr_life=24, init_pos=1, radius=.6, axis=(0, 1, 0), vel=(.01, .08), alpha=(26, 22, 0),
         scl_anm=(.4, 1.2, 1.8, 60, 200))
    out[ZAPS17] = bytes(b)

    # OG Power (AncientPower): the OG relics rise up glowing round them - a brick phone, a VHS tape, a mixtape -
    # and slam into the foe one after another. Then the OG aura: gold, all stats up
    b, rs = kit(RELICS17)
    tex(b, 1, fxart.brick_phone())
    b, vhs = added(b, fxart.vhs_tape(), 24)
    b, tape = added(b, fxart.cassette(), 24)
    tex(b, 0, fxart.tiny_spark())
    prop(b, rs, PHONE17, scl=.95, life=4)
    prop(b, rs, VHS17, tex=vhs, scl=ONE_TO_ONE, life=4)                        # (VHS on the label: 1:1)
    prop(b, rs, TAPE17, tex=tape, scl=.95, life=4)
    burst(b, rs, OGSPARK, rgb(255, 220, 60), rgb(255, 255, 220), .45, 6, .1, up=.04, life=16)
    out[RELICS17] = bytes(b)
    b, rs = kit(OGAURA17)
    tex(b, 1, fxart.light_shaft())
    tex(b, 0, fxart.soot_puff())
    prop(b, rs, SHAFTS, tex=1, clr=rgb(255, 210, 60), clr_anm=(rgb(255, 255, 210), rgb(255, 170, 30)), scl=.45,
         life=16, gen=1, gen_intvl=2, emtr_life=16, init_pos=1, radius=1.1, axis=(0, 1, 0), vel=(.01, .16),
         alpha=(22, 18, 0), scl_anm=(.6, 1.0, .6, 60, 200))
    prop(b, rs, OGDUST, tex=0, clr=rgb(180, 160, 120), clr_anm=(rgb(240, 225, 190), rgb(120, 100, 70)), scl=.7,
         life=18, gen=6, init_pos=1, radius=.4, axis=(0, 1, 0), vel=(.12, .03), alpha=(26, 22, 0),
         scl_anm=(.5, 1.2, 1.7, 60, 200))
    out[OGAURA17] = bytes(b)

    # Laser Sight (Psybeam): a laser pointer - the red dot wanders over the foe and they chase it like a cat -
    # it settles on their forehead - then the whole beam goes psychedelic and fries their brain
    b, rs = kit(POINTER17)
    tex(b, 1, fxart.laser_pointer())
    b, left = mirrored(b, fxart.laser_pointer(), 24)
    tex(b, 0, fxart.pointer_dot())
    prop(b, rs, POINTER_R, scl=1.0, life=4)
    prop(b, rs, POINTER_L, tex=left, scl=1.0, life=4)
    prop(b, rs, DOT17, tex=0, clr=rgb(255, 30, 30), clr_anm=(rgb(255, 200, 200), rgb(255, 30, 30)), scl=.55, life=4,
         alpha=(31, 31, 31))
    unused(b, rs, 3)
    out[POINTER17] = bytes(b)
    b, rs = kit(PSYRING17)
    tex(b, 0, fxart.wavy_ring())
    for res, sd in ((PRINGS_E, "player"), (PRINGS_P, "enemy")):
        spray(b, rs, res, sd, POINTER_TIP[sd], (0, 28), 12, tex=0, clr=rgb(255, 80, 200),
              clr_anm=(rgb(120, 255, 255), rgb(255, 60, 160)), scl=.7, gen=1, gen_intvl=2, emtr_life=24, radius=.1,
              alpha=(31, 31, 10), scl_anm=(.4, 1.0, 1.6, 0, 160))
    out[PSYRING17] = bytes(b)
    b, rs = kit(DIZZY17)
    tex(b, 0, fxart.hypno_swirl(), 30)
    prop(b, rs, SWIRL17, scl=.9, life=4)
    unused(b, rs, 1)
    out[DIZZY17] = bytes(b)

    # Mudslinging (Mud-Slap): a lifted truck pulls up next to the foe and its giant tire gets stuck spinning in
    # the mud - VRRRR - slinging a spray of mud all over them
    b, rs = kit(TIRE17)
    tex(b, 1, fxart.monster_tire())
    b, pud = added(b, fxart.mud_puddle(), 24)
    tex(b, 0, fxart.fizz_drop())
    for res, d in ((TIRE_R, 1), (TIRE_L, -1)):                                 # (one long particle: a re-emitted
        prop(b, rs, res, scl=1.25, life=MUD_SPIN, flags_on=(1 << 14) | (1 << 12))   # spinner would restart its turn)
        rot(b, rs, res, spin=-d * 0x1800)
    prop(b, rs, PUDDLE, tex=pud, scl=1.3, life=MUD_SPIN)
    burst(b, rs, MUDDROP, rgb(110, 70, 30), rgb(170, 125, 80), .35, 3, .14, up=.22, gravity=.022, life=22,
          emtr_life=MUD_SPIN - 10, gen_intvl=2)
    out[TIRE17] = bytes(b)
    b, rs = kit(MUDWAVE17)
    tex(b, 0, fxart.fizz_drop())
    tex(b, 1, fxart.mud_glob())
    for res, sd in ((MUDSHEET, "player"), (MUDDRIP17, "enemy")):
        sx = 1 if sd == "player" else -1
        dx, dy = TARGET_FROM_ATTACKER[sd]
        tire = MUD_TIRE[sd]
        spray(b, rs, res, sd, (dx + tire[0], dy + tire[1] + 8), (0, 16), 10, tex=0, clr=rgb(110, 72, 34),
              clr_anm=(rgb(160, 115, 70), rgb(85, 55, 25)), scl=.5, gen=4, gen_intvl=1, emtr_life=MUD_SPIN - 24,
              radius=.2, spread=.05, alpha=(31, 31, 0), gravity=(0, -.004, 0))
    out[MUDWAVE17] = bytes(b)

    # Hot Grill (Fire Fang): a contact grill opens up like jaws round the foe, sizzling - CHOMP - CHOMP - and they
    # come out with grill marks on them, smoking
    b, rs = kit(FOREMAN17)
    tex(b, 1, fxart.contact_grill())
    b, shut = added(b, fxart.contact_grill(shut=True), 30)
    tex(b, 0, fxart.soot_puff())
    prop(b, rs, GRILLOPEN, scl=1.55, life=4)
    prop(b, rs, GRILLSHUT, tex=shut, scl=1.55, life=4)
    prop(b, rs, GREASE, tex=0, clr=rgb(190, 190, 195), clr_anm=(rgb(250, 250, 250), rgb(120, 120, 125)), scl=.6,
         life=22, gen=1, gen_intvl=2, emtr_life=12, init_pos=1, radius=.7, axis=(0, 1, 0), vel=(.01, .1),
         alpha=(24, 20, 0), scl_anm=(.4, 1.2, 1.8, 60, 200))
    unused(b, rs, 3)
    out[FOREMAN17] = bytes(b)
    b, rs = kit(MARKS17)
    tex(b, 0, fxart.grill_marks(), 16)
    prop(b, rs, MARKS, scl=1.1, life=40, alpha=(31, 31, 0), scl_anm=(1.0, 1.0, 1.0, 0, 255))
    unused(b, rs, 1)
    out[MARKS17] = bytes(b)
    b, rs = kit(SIZZLE17)
    tex(b, 1, fxart.flame_tongue())
    tex(b, 0, fxart.soft_puff())
    prop(b, rs, SIZZLEFX, tex=1, clr=rgb(255, 130, 20), clr_anm=(rgb(255, 240, 120), rgb(230, 40, 10)), scl=.4,
         life=14, gen=3, gen_intvl=1, emtr_life=6, init_pos=1, radius=.9, axis=(0, 1, 0), vel=(.05, .14),
         alpha=(31, 31, 0), scl_anm=(.4, 1.2, .5, 50, 160))
    prop(b, rs, SIZZSTEAM, tex=0, clr=rgb(225, 225, 230), clr_anm=(rgb(255, 255, 255), rgb(150, 150, 155)), scl=.6,
         life=26, gen=1, gen_intvl=3, emtr_life=30, init_pos=1, radius=.6, axis=(0, 1, 0), vel=(.01, .1),
         alpha=(22, 18, 0), scl_anm=(.4, 1.2, 1.8, 60, 200))
    out[SIZZLE17] = bytes(b)
    SET10_82 += [TGLOVE17, RELICS17, POINTER17, TIRE17, FOREMAN17]


    # Taser Grill (Thunder Fang): a car battery, jumper cables - the clamps touch, SPARKS - then the clamps go
    # for the foe like jaws and CHOMP down. Lit up.
    b, rs = kit(CABLES17)
    tex(b, 1, fxart.jumper_clamps())
    b, shut = added(b, fxart.jumper_clamps(shut=True), 30)
    b, batt = added(b, fxart.car_battery(), 24)
    tex(b, 0, fxart.zig_spark())
    prop(b, rs, CLAMPO_R, scl=1.1, life=4)
    prop(b, rs, CLAMPS_R, tex=shut, scl=1.1, life=4)
    prop(b, rs, BATT17, tex=batt, scl=ONE_TO_ONE, life=4)                      # (12V on the label: 1:1)
    burst(b, rs, JSPARK17, rgb(255, 230, 90), rgb(255, 255, 255), .5, 8, .22, up=.1, gravity=.01, life=12,
          spin=0x1400)
    out[CABLES17] = bytes(b)
    b, rs = kit(CABLESL17)
    tex(b, 0, fxart.jumper_clamps().transpose(_Img.FLIP_LEFT_RIGHT), 30)
    b, shut = mirrored(b, fxart.jumper_clamps(shut=True), 30)
    prop(b, rs, CLAMPO_L, scl=1.1, life=4)
    prop(b, rs, CLAMPS_L, tex=shut, scl=1.1, life=4)
    out[CABLESL17] = bytes(b)
    no_delay(CABLESL17, CLAMPS_L)
    b, rs = kit(JOLT17)
    tex(b, 1, fxart.bolt_tall())
    tex(b, 0, fxart.soot_puff())
    prop(b, rs, JBOLT17, tex=1, clr=rgb(120, 220, 255), clr_anm=(rgb(255, 255, 255), rgb(255, 240, 60)), scl=1.0,
         life=3, gen=3, gen_intvl=2, emtr_life=26, init_pos=1, radius=1.0, alpha=(31, 31, 31),
         flags_on=(1 << 14) | (1 << 12))
    rot(b, rs, JBOLT17, spin=0x2800, init=0x2000)
    prop(b, rs, JSMOKE17, tex=0, clr=rgb(70, 70, 75), clr_anm=(rgb(160, 160, 165), rgb(40, 40, 45)), scl=.7,
         life=30, gen=1, gen_intvl=3, emtr_life=20, init_pos=1, radius=.6, axis=(0, 1, 0), vel=(.01, .08),
         alpha=(26, 22, 0), scl_anm=(.4, 1.2, 1.8, 60, 200))
    out[JOLT17] = bytes(b)

    # Rizz (Charm): a wink - *ting* - and gas-station roses slide on over, $4.99 sticker still on. The foe melts.
    b, rs = kit(ROSES17)
    tex(b, 1, fxart.gas_roses())
    tex(b, 0, fxart.wink_twinkle())
    prop(b, rs, ROSES1, scl=ONE_TO_ONE, life=4)
    prop(b, rs, WINK17, tex=0, clr=rgb(255, 255, 220), clr_anm=(rgb(255, 255, 255), rgb(255, 230, 120)), scl=.7,
         life=14, scl_anm=(.2, 1.3, .2, 60, 160), alpha=(31, 31, 0), flags_on=(1 << 14) | (1 << 12))
    rot(b, rs, WINK17, spin=0x0800)
    unused(b, rs, 2, 3)
    out[ROSES17] = bytes(b)
    b, rs = kit(LOVE17)
    tex(b, 0, fxart.puffy_heart())
    prop(b, rs, HEARTSUP17, tex=0, clr=rgb(255, 70, 140), clr_anm=(rgb(255, 210, 230), rgb(235, 40, 110)), scl=.6,
         life=26, gen=1, gen_intvl=3, emtr_life=36, init_pos=1, radius=.9, axis=(0, 1, 0), vel=(.01, .1),
         alpha=(31, 31, 0), scl_anm=(.4, 1.2, 1.0, 50, 255))
    prop(b, rs, HEARTPOP17, tex=0, clr=rgb(255, 70, 140), clr_anm=(rgb(255, 230, 240), rgb(235, 40, 110)), scl=.7,
         life=18, gen=8, init_pos=1, radius=.3, axis=(0, 1, 0), vel=(.2, .06), alpha=(31, 31, 0))
    out[LOVE17] = bytes(b)

    # Bulk Up (Growth): the GAINZ tub, two scoops into the shaker - shake, shake, SHAKE - chug it - and they pump
    # up, glowing, arrows going up
    b, rs = kit(GAINZ17)
    tex(b, 1, fxart.protein_tub())
    b, shaker = added(b, fxart.shaker_bottle(), 24)
    b, chug = added(b, fxart.shaker_chug(), 24)
    tex(b, 0, fxart.soft_puff())
    prop(b, rs, TUB17, scl=ONE_TO_ONE, life=4)
    prop(b, rs, SHAKER17, tex=shaker, scl=1.0, life=4)
    prop(b, rs, CHUG17, tex=chug, scl=1.0, life=4)
    burst(b, rs, POWDER17, rgb(150, 100, 60), rgb(220, 190, 150), .6, 6, .06, up=.06, life=18, alpha=(28, 22, 0),
          scl_anm=(.5, 1.2, 1.6, 60, 200))
    out[GAINZ17] = bytes(b)
    b, rs = kit(PUMP17)
    tex(b, 0, fxart.chevron())
    tex(b, 1, fxart.light_shaft())
    prop(b, rs, CHEVRONS17, tex=0, clr=rgb(255, 60, 40), clr_anm=(rgb(255, 220, 200), rgb(230, 30, 20)), scl=.5,
         life=20, gen=1, gen_intvl=2, emtr_life=30, init_pos=1, radius=.9, axis=(0, 1, 0), vel=(0, .16),
         alpha=(31, 31, 0))
    prop(b, rs, PUMPGLOW17, tex=1, clr=rgb(255, 80, 50), clr_anm=(rgb(255, 220, 180), rgb(230, 40, 20)), scl=.9,
         life=18, gen=2, gen_intvl=2, emtr_life=30, init_pos=1, radius=.9, axis=(0, 1, 0), vel=(0, .08),
         alpha=(22, 20, 0), scl_anm=(.6, 1.2, .8, 60, 200))
    out[PUMP17] = bytes(b)

    # Curb Stomp (Stomp): the foe's fresh white kicks, sparkling - and a GIANT Croc comes down on them. Creased.
    # The foe is livid.
    b, rs = kit(KICKS17)
    tex(b, 1, fxart.white_kicks())
    b, wrecked = added(b, fxart.white_kicks(wrecked=True), 24)
    b, croc = added(b, fxart.giant_croc(), 24)
    tex(b, 0, fxart.wink_twinkle())
    prop(b, rs, KICKS1, scl=1.1, life=4)
    prop(b, rs, KICKSWRECKED, tex=wrecked, scl=1.1, life=4)
    prop(b, rs, CROC1, tex=croc, scl=1.5, life=4)
    burst(b, rs, KSPARK17, rgb(255, 255, 255), rgb(255, 255, 220), .45, 3, .06, life=14,
          scl_anm=(.2, 1.3, .2, 60, 160))
    out[KICKS17] = bytes(b)
    b, rs = kit(VEIN17)
    tex(b, 0, fxart.anger_vein())
    tex(b, 1, fxart.dust_cloud())
    prop(b, rs, VEINS17, tex=0, clr=rgb(240, 30, 40), clr_anm=(rgb(255, 120, 120), rgb(220, 20, 30)), scl=.6, life=8,
         gen=1, gen_intvl=4, emtr_life=30, init_pos=1, radius=.7, alpha=(31, 31, 31), scl_anm=(.5, 1.3, 1.0, 60, 255))
    prop(b, rs, STOMPDUST17, tex=1, clr=rgb(200, 190, 170), clr_anm=(rgb(250, 245, 235), rgb(150, 140, 120)),
         scl=.8, life=22, gen=6, init_pos=1, radius=.5, axis=(0, 1, 0), vel=(.14, .02), alpha=(26, 20, 0),
         scl_anm=(.5, 1.2, 1.6, 60, 200))
    out[VEIN17] = bytes(b)

    # Get Back (Payback): throwing the ex's stuff out on the lawn - the hoodie, the controller, the heart boxers,
    # the torn photo rain down on them - and then the whole box. BONK.
    b, rs = kit(STUFF17)
    tex(b, 1, fxart.stuff_box())
    b, hood_ = added(b, fxart.hoodie(), 24)
    b, pad = added(b, fxart.game_controller(), 24)
    tex(b, 0, fxart.soft_puff())
    prop(b, rs, STUFFBOX17, scl=ONE_TO_ONE, life=4)
    fall = 26
    mover(b, rs, HOODIE17, -.5, -STUFF_FALL, tex=hood_, scl=1.0, life=fall, flags_on=(1 << 14) | (1 << 12))
    rot(b, rs, HOODIE17, spin=0x0500)
    mover(b, rs, PAD17, .4, -STUFF_FALL, tex=pad, scl=.8, life=fall, flags_on=(1 << 14) | (1 << 12))
    rot(b, rs, PAD17, spin=-0x0900)
    burst(b, rs, JUNKDUST17, rgb(200, 190, 170), rgb(250, 245, 235), .8, 8, .16, up=.03, life=22, radius=.6,
          alpha=(26, 20, 0), scl_anm=(.5, 1.3, 1.8, 60, 200))
    out[STUFF17] = bytes(b)
    b, rs = kit(JUNK17)
    tex(b, 1, fxart.heart_boxers(), 24)
    b, photo = added(b, fxart.torn_photo(), 24)
    mover(b, rs, BOXERS17, .3, -STUFF_FALL, tex=1, scl=.75, life=fall, flags_on=(1 << 14) | (1 << 12))
    rot(b, rs, BOXERS17, spin=0x0700)
    mover(b, rs, PHOTO17, -.3, -STUFF_FALL, tex=photo, scl=.7, life=fall, flags_on=(1 << 14) | (1 << 12))
    rot(b, rs, PHOTO17, spin=-0x0600)
    unused(b, rs, 2)
    out[JUNK17] = bytes(b)
    SET10_82 += [CABLES17, ROSES17, GAINZ17, KICKS17, STUFF17]


    # Gun Twirl (Swords Dance): the revolver spins round the finger like a movie - faster, FASTER - tossed up,
    # flipping - caught, *click* - and they're glowing red, power flaring off them
    b, rs = kit(TWIRL17)
    tex(b, 1, fxart.chrome_revolver())
    for res, spin, life in ((GUN_SLOW, 0x0C00, TWIRL_SLOW), (GUN_FAST, 0x2400, TWIRL_FAST)):   # one particle each: a
        prop(b, rs, res, scl=1.4, life=life, flags_on=(1 << 14) | (1 << 12))   # re-emitted spinner restarts its turn
        rot(b, rs, res, spin=-spin)
    prop(b, rs, GUN_HELD, scl=1.4, life=4, flags_on=(1 << 14) | (1 << 12))   # (rotating, still: same anchor as the spin)
    rot(b, rs, GUN_HELD)
    h = 12 * VEL_UNITS / 4096                                                  # tossed up (shows ~2.5x that), back down
    g = 8 * h / TOSS_FRAMES ** 2
    prop(b, rs, GUN_TOSS, tex=1, scl=1.4, life=TOSS_FRAMES, axis=(0, 1, 0), vel=(0, g * TOSS_FRAMES / 2),
         gravity=(0, -g, 0), flags_on=(1 << 14) | (1 << 12))
    rot(b, rs, GUN_TOSS, spin=-0x1800)
    out[TWIRL17] = bytes(b)
    b, rs = kit(AURA17)
    tex(b, 1, fxart.power_flare())
    b, left = mirrored(b, fxart.chrome_revolver(), 24)
    prop(b, rs, FLARES17, tex=1, clr=rgb(255, 50, 30), clr_anm=(rgb(255, 230, 160), rgb(220, 20, 20)), scl=.4,
         life=16, gen=1, gen_intvl=2, emtr_life=24, init_pos=1, radius=1.0, axis=(0, 1, 0), vel=(.01, .12),
         alpha=(28, 26, 0), scl_anm=(.5, 1.2, .6, 60, 200))
    prop(b, rs, GUNHELD_L, tex=left, scl=1.4, life=4, flags_on=(1 << 14) | (1 << 12))
    rot(b, rs, GUNHELD_L)
    out[AURA17] = bytes(b)

    # Ace Shot (Aerial Ace): the deck fans out - riffle - the ace of spades flicked out - it curves way out and
    # comes back round (never misses) - SLICE - and sticks in them
    b, rs = kit(CARDS17)
    tex(b, 1, fxart.card_fan())
    b, ace = added(b, fxart.ace_card(), 8)
    tex(b, 0, fxart.card_swoosh())
    prop(b, rs, DECK17, scl=1.0, life=4)
    prop(b, rs, ACE17, tex=ace, scl=ONE_TO_ONE / 2, life=4)                    # 32px card: the A at 1:1
    prop(b, rs, CARDTRAIL, tex=0, clr=rgb(255, 255, 255), clr_anm=(rgb(255, 255, 255), rgb(200, 220, 255)), scl=.6,
         life=8, alpha=(28, 20, 0))
    unused(b, rs, 3)
    out[CARDS17] = bytes(b)
    b, rs = kit(SLICE17)
    tex(b, 0, fxart.slash_single(), 16)
    prop(b, rs, SLICE1, scl=1.5, life=10, scl_anm=(.3, 1.2, 1.0, 80, 255))
    unused(b, rs, 1)
    out[SLICE17] = bytes(b)

    # Jack Em (Thief): the foe's designer bag sitting right there - an arcade claw comes down from the top of
    # the screen - wobble - CLAMP - and up it goes with the bag. Got it.
    b, rs = kit(CLAW17)
    tex(b, 1, fxart.claw_machine())
    b, grabbed = added(b, fxart.claw_machine(state=2), 30)
    b, cable = added(b, fxart.claw_cable(), 8)
    tex(b, 0, fxart.wink_twinkle())
    prop(b, rs, CLAWOPEN, scl=1.3, life=4)
    prop(b, rs, CLAWBAG, tex=grabbed, scl=1.3, life=4)
    prop(b, rs, CABLE17, tex=cable, scl=1.3, life=4)
    burst(b, rs, CLAWSPARK, rgb(255, 240, 150), rgb(255, 255, 255), .5, 3, .08, life=14, scl_anm=(.2, 1.3, .2, 60, 160))
    out[CLAW17] = bytes(b)
    b, rs = kit(BAG17)
    tex(b, 0, fxart.designer_bag(), 30)
    prop(b, rs, BAG1, scl=1.0, life=4)
    unused(b, rs, 1)
    out[BAG17] = bytes(b)

    # Drop a Track (Sing): lights down, a 50s mic stand - a slow jam drifts over - lighters up, swaying - the foe
    # sways too... a sleep mask drops over their eyes. Zzz.
    b, rs = kit(MICS17)
    tex(b, 1, fxart.retro_mic())
    b, lighter = added(b, fxart.zippo(), 24)
    b, mask = added(b, fxart.sleep_mask(), 24)
    tex(b, 0, fxart.snore_z())
    prop(b, rs, MICSTAND, scl=1.15, life=4)
    prop(b, rs, LIGHTER17, tex=lighter, scl=.8, life=4)
    prop(b, rs, MASK17, tex=mask, scl=1.0, life=4)
    prop(b, rs, ZZ17, tex=0, clr=rgb(200, 210, 255), clr_anm=(rgb(255, 255, 255), rgb(150, 160, 255)), scl=.5,
         life=30, gen=1, gen_intvl=8, emtr_life=40, axis=(.5, 1, 0), vel=(0, .1), alpha=(31, 31, 0),
         scl_anm=(.4, 1.4, 1.6, 80, 200))
    out[MICS17] = bytes(b)
    b, rs = kit(SLEEPZ17)
    tex(b, 0, fxart.double_note())
    for res, sd in ((NOTES_E17, "player"), (NOTES_P17, "enemy")):
        spray(b, rs, res, sd, (MIC_AT[sd][0], MIC_AT[sd][1] + 26), (0, 30), 26, tex=0, clr=rgb(255, 150, 220),
              clr_anm=(rgb(255, 230, 250), rgb(200, 120, 255)), scl=.6, gen=1, gen_intvl=5, emtr_life=40,
              radius=.3, spread=.01, alpha=(31, 31, 0))
    out[SLEEPZ17] = bytes(b)

    # Dust Up (Sandstorm): a gas leaf blower revs up - VRRRRM - and kicks up a dust storm that sweeps the whole
    # block: plastic bags, cans, everything blowing through. Everybody's eating dirt.
    b, rs = kit(BLOWER17)
    tex(b, 1, fxart.leaf_blower())
    b, left = mirrored(b, fxart.leaf_blower(), 24)
    b, pbag = added(b, fxart.plastic_bag(), 16)
    tex(b, 0, fxart.speck())
    prop(b, rs, BLOWER_R, scl=1.15, life=4)
    prop(b, rs, BLOWER_L, tex=left, scl=1.15, life=4)
    mover(b, rs, PBAG_R, WIND_SPEED, .6, tex=pbag, scl=.9, life=round(300 / WIND_SPEED), flags_on=(1 << 14) | (1 << 12))
    rot(b, rs, PBAG_R, spin=-0x0700)
    spray(b, rs, SPECKS_R, "player", BLOWER_TIP["player"], (0, 16), 14, tex=0, clr=rgb(200, 165, 110),
          clr_anm=(rgb(235, 210, 160), rgb(160, 120, 70)), scl=.5, gen=6, gen_intvl=1, emtr_life=30, radius=.25,
          spread=.03, alpha=(31, 28, 10))
    out[BLOWER17] = bytes(b)
    b, rs = kit(TRASH17)
    tex(b, 1, fxart.plastic_bag(64))
    b, can = added(b, fxart.crushed_can(), 16)
    tex(b, 0, fxart.speck())
    mover(b, rs, PBAG_L, -WIND_SPEED, .6, scl=.9, life=round(300 / WIND_SPEED), flags_on=(1 << 14) | (1 << 12))
    rot(b, rs, PBAG_L, spin=0x0700)
    for res, d in ((SODA_R, 1), (SODA_L, -1)):
        mover(b, rs, res, d * (WIND_SPEED + 1), -.3, tex=can, scl=.6, life=round(300 / (WIND_SPEED + 1)),
              flags_on=(1 << 14) | (1 << 12))
        rot(b, rs, res, spin=-d * 0x1200)
    spray(b, rs, SPECKS_L, "enemy", BLOWER_TIP["enemy"], (0, 16), 14, tex=0, clr=rgb(200, 165, 110),
          clr_anm=(rgb(235, 210, 160), rgb(160, 120, 70)), scl=.5, gen=6, gen_intvl=1, emtr_life=30, radius=.25,
          spread=.03, alpha=(31, 28, 10))
    out[TRASH17] = bytes(b)
    b, rs = kit(DUSTSTORM17)
    tex(b, 1, fxart.dust_swirl())
    for res, d in ((DUST_R, 1), (DUST_L, -1)):
        prop(b, rs, res, tex=1, clr=rgb(190, 150, 95), clr_anm=(rgb(230, 200, 150), rgb(150, 110, 60)), scl=1.6,
             life=50, gen=2, gen_intvl=1, emtr_life=40, init_pos=1, radius=2.6, axis=(d, .05, 0),
             vel=(.02, WIND_SPEED * VEL_UNITS / 4096), alpha=(20, 16, 0), scl_anm=(.6, 1.2, 1.6, 60, 200))
    out[DUSTSTORM17] = bytes(b)
    SET10_82 += [TWIRL17, CARDS17, CLAW17, MICS17, BLOWER17, TRASH17]


    # ---- set 18: thirty more ----------------------------------------------------------------------------
    # pk(): a kit whose props each get their own added texture (any size); res 0 is usually the particles.
    # Props on file 82's res 3 draw RES3_DROP * scale px low (the scripts lift them).
    def pk(ps, props, alpha=None, alpha1=None):
        b, rs = kit(ps)
        if alpha is not None:
            tex(b, 0, alpha)
        if alpha1 is not None:
            tex(b, 1, alpha1)
        for res, (art, scl, life, extra) in props.items():
            extra = dict(extra)
            b, t = added(b, art, extra.pop("colors", 24))
            spin = extra.pop("spin", None)
            move = extra.pop("move", None)
            if spin is not None:
                extra["flags_on"] = (1 << 14) | (1 << 12)
            if move:
                mover(b, rs, res, *move, tex=t, scl=scl, life=life, **extra)
            else:
                prop(b, rs, res, tex=t, scl=scl, life=life, **extra)
            if spin is not None:
                rot(b, rs, res, spin=spin)
        return b, rs

    def fin(ps, b, rs, used):
        for r in range(len(rs)):
            if r not in used:
                prop(b, rs, r, life=1)
        out[ps] = bytes(b)

    from PIL import Image as _I
    flipx = lambda im: im.transpose(_I.FLIP_LEFT_RIGHT)

    # Run It Back (Encore): DJ decks - the record spins, scratch scratch - REWIND - the foe gets pulled back and
    # has to run it all back
    b, rs = pk(DJ18, {1: (fxart.turntable(), 1.2, 4, {}), 2: (fxart.vinyl(), .62, 70, {"spin": -0x0C00})},
               alpha=fxart.rewind_arrows())
    burst(b, rs, 0, rgb(80, 220, 255), rgb(230, 255, 255), .55, 4, .12, life=14)
    fin(DJ18, b, rs, (0, 1, 2))
    b, rs = pk(DJFX18, {}, alpha=fxart.rewind_arrows(), alpha1=fxart.light_shaft())
    prop(b, rs, 0, tex=0, clr=rgb(80, 220, 255), clr_anm=(rgb(230, 255, 255), rgb(40, 160, 255)), scl=.6, life=16,
         gen=1, gen_intvl=3, emtr_life=30, init_pos=1, radius=.8, axis=(-1, 0, 0), vel=(0, .12), alpha=(31, 31, 0))
    prop(b, rs, 1, tex=0, clr=rgb(255, 255, 255), clr_anm=(rgb(255, 255, 255), rgb(120, 220, 255)), scl=1.0, life=10,
         alpha=(31, 31, 0), scl_anm=(.3, 1.4, 1.0, 60, 255))
    fin(DJFX18, b, rs, (0, 1))

    # Pass It Off (Baton Pass): a duffel bag full of cash - look left, look right - and it gets YEETED off-screen to
    # a teammate. Act natural.
    b, rs = pk(DUFFEL18, {1: (fxart.cash_duffel(), 1.1, 4, {}), 2: (fxart.cash_duffel(), 1.1, 40, {"move": (8, 1)}),
                          3: (flipx(fxart.cash_duffel()), 1.1, 40, {"move": (-8, 1)})}, alpha=fxart.dash_lines())
    burst(b, rs, 0, rgb(255, 255, 255), rgb(255, 255, 255), .6, 3, .05, life=12)
    fin(DUFFEL18, b, rs, (0, 1, 2, 3))

    # Brass Knucks (Metal Claw): gold knucks slide on - *shine* - jab, jab, POW
    b, rs = pk(KNUX18, {1: (fxart.brass_knuckles(), 1.0, 4, {}), 2: (flipx(fxart.brass_knuckles()), 1.0, 4, {})},
               alpha=fxart.wink_twinkle())
    prop(b, rs, 0, tex=0, clr=rgb(255, 250, 200), clr_anm=(rgb(255, 255, 255), rgb(255, 220, 90)), scl=.7, life=12,
         scl_anm=(.2, 1.3, .2, 60, 160), alpha=(31, 31, 0))
    fin(KNUX18, b, rs, (0, 1, 2))
    b, rs = pk(POW18, {0: (fxart.pow_burst(), 1.0, 8, {"scl_anm": (.3, 1.2, 1.0, 60, 255)}),
                       1: (fxart.pow_burst(), 1.6, 12, {"scl_anm": (.3, 1.25, 1.0, 60, 255)})})
    fin(POW18, b, rs, (0, 1))

    # Doughnuts (Fire Spin): a muscle car whips doughnuts round the foe - skrrrt - tire smoke everywhere - and
    # the burnt rubber goes up in a RING OF FIRE
    b, rs = pk(CAR18, {1: (fxart.muscle_car(), 1.0, 4, {}), 2: (flipx(fxart.muscle_car()), 1.0, 4, {})},
               alpha=fxart.soot_puff())
    prop(b, rs, 0, tex=0, clr=rgb(200, 200, 205), clr_anm=(rgb(250, 250, 250), rgb(130, 130, 135)), scl=.7, life=26,
         gen=2, init_pos=1, radius=.3, axis=(0, 1, 0), vel=(.04, .03), alpha=(24, 20, 0), scl_anm=(.4, 1.2, 1.9, 60, 200))
    fin(CAR18, b, rs, (0, 1, 2))
    b, rs = pk(RINGFIRE18, {}, alpha=fxart.speck(), alpha1=fxart.flame_tongue())
    prop(b, rs, 0, tex=1, clr=rgb(255, 120, 20), clr_anm=(rgb(255, 240, 120), rgb(220, 30, 10)), scl=.32, life=16,
         gen=3, gen_intvl=1, emtr_life=30, init_pos=1, radius=1.5, axis=(0, 1, 0), vel=(0, .1), alpha=(31, 31, 0),
         scl_anm=(.4, 1.2, .5, 50, 160))
    prop(b, rs, 1, tex=0, clr=rgb(255, 200, 60), clr_anm=(rgb(255, 255, 200), rgb(255, 100, 20)), scl=.3, life=18,
         gen=2, gen_intvl=2, emtr_life=30, init_pos=1, radius=1.3, axis=(0, 1, 0), vel=(.02, .14), alpha=(31, 31, 0))
    fin(RINGFIRE18, b, rs, (0, 1))

    # Diss Track (Taunt): the diss track drops - EXPLICIT - every note aimed straight at the foe. They're TIGHT.
    b, rs = pk(CD18, {1: (fxart.diss_cd(), ONE_TO_ONE, 4, {"colors": 30})}, alpha=fxart.wink_twinkle())
    prop(b, rs, 0, tex=0, clr=rgb(255, 255, 220), clr_anm=(rgb(255, 255, 255), rgb(255, 220, 90)), scl=.7, life=12,
         scl_anm=(.2, 1.3, .2, 60, 160), alpha=(31, 31, 0))
    fin(CD18, b, rs, (0, 1))
    b, rs = pk(NOTES18, {}, alpha=fxart.angry_note())
    for res, sd in ((0, "player"), (1, "enemy")):
        dx, dy = TARGET_FROM_ATTACKER[sd]
        spray(b, rs, res, sd, (round(dx * .4), round(dy * .4) + 30), (0, 24), 14, tex=0, clr=rgb(255, 60, 60),
              clr_anm=(rgb(255, 220, 220), rgb(230, 30, 30)), scl=.55, gen=1, gen_intvl=2, emtr_life=30, radius=.3,
              spread=.02, alpha=(31, 31, 0), flags_on=(1 << 14) | (1 << 12))
        rot(b, rs, res, spin=0x0600)
    fin(NOTES18, b, rs, (0, 1))

    # Bootleg (Knock Off): a shady trench coat sidles up - psst - flashes open: a wall of ROLEKS - the foe buys
    # one... and it falls apart in their hands. Gears everywhere.
    b, rs = pk(COAT18, {1: (fxart.trench_coat(open_=False), ONE_TO_ONE, 4, {}),
                        2: (fxart.trench_coat(), ONE_TO_ONE, 4, {"colors": 30})}, alpha=fxart.wink_twinkle())
    prop(b, rs, 0, tex=0, clr=rgb(255, 240, 150), clr_anm=(rgb(255, 255, 255), rgb(255, 210, 60)), scl=.6, life=12,
         gen=3, init_pos=1, radius=.8, scl_anm=(.2, 1.3, .2, 60, 160), alpha=(31, 31, 0))
    fin(COAT18, b, rs, (0, 1, 2))
    b, rs = pk(GEARS18, {}, alpha=fxart.gear_bit(), alpha1=fxart.light_shaft())
    prop(b, rs, 0, tex=0, clr=rgb(230, 190, 60), clr_anm=(rgb(255, 240, 150), rgb(180, 130, 30)), scl=.45, life=26,
         gen=12, init_pos=1, radius=.3, axis=(0, 1, 0), vel=(.18, .26), gravity=(0, -.024, 0), alpha=(31, 31, 0),
         flags_on=(1 << 14) | (1 << 12))
    rot(b, rs, 0, spin=0x1000)
    fin(GEARS18, b, rs, (0,))

    # Run Em Off (Whirlwind): grandma's broom comes out - sweep, sweep - GET OFF MY PORCH - swept clean off the
    # block
    b, rs = pk(BROOM18, {1: (fxart.grandma_broom(), 1.3, 4, {}), 2: (flipx(fxart.grandma_broom()), 1.3, 4, {})},
               alpha=fxart.soot_puff())
    prop(b, rs, 0, tex=0, clr=rgb(200, 185, 160), clr_anm=(rgb(245, 235, 215), rgb(150, 135, 110)), scl=.7, life=22,
         gen=4, init_pos=1, radius=.4, axis=(0, 1, 0), vel=(.1, .04), alpha=(24, 20, 0), scl_anm=(.4, 1.2, 1.8, 60, 200))
    fin(BROOM18, b, rs, (0, 1, 2))

    # Suplex (Seismic Toss): the ring drops in round the foe - DING DING - up... up... SUPLEX - the three count -
    # and the belt
    b, rs = pk(RING18, {1: (fxart.wrestling_ring(), 2.0, 4, {}), 2: (fxart.champ_belt(), 1.1, 4, {})},
               alpha=fxart.wink_twinkle())
    prop(b, rs, 0, tex=0, clr=rgb(255, 240, 150), clr_anm=(rgb(255, 255, 255), rgb(255, 210, 60)), scl=.6, life=14,
         gen=3, init_pos=1, radius=.8, scl_anm=(.2, 1.3, .2, 60, 160), alpha=(31, 31, 0))
    fin(RING18, b, rs, (0, 1, 2))

    # Leg Sweep (Low Kick): a puddle and a WET FLOOR sign - the foe walks right into it - SLIP - flat on their back,
    # stars
    b, rs = pk(WET18, {1: (fxart.wet_floor_aframe(), ONE_TO_ONE, 4, {}), 2: (fxart.water_puddle(), 1.3, 4, {})},
               alpha=fxart.fizz_drop())
    burst(b, rs, 0, rgb(120, 190, 255), rgb(240, 250, 255), .4, 12, .2, up=.3, gravity=.024, life=24)
    fin(WET18, b, rs, (0, 1, 2))
    b, rs = pk(STARS18, {}, alpha=fxart.tiny_spark())
    prop(b, rs, 0, tex=0, clr=rgb(255, 230, 60), clr_anm=(rgb(255, 255, 220), rgb(255, 200, 30)), scl=.5, life=4,
         alpha=(31, 31, 31))
    fin(STARS18, b, rs, (0,))

    # Dark Vibes (Dark Pulse): lights out - a black candle lit - skulls drift up - and pulses of pure bad vibes
    # roll over the foe
    b, rs = pk(CANDLE18, {1: (fxart.black_candle(), 1.0, 4, {})},
               alpha=fxart.skull_glyph())
    prop(b, rs, 0, tex=0, clr=rgb(170, 90, 255), clr_anm=(rgb(230, 200, 255), rgb(90, 30, 160)), scl=.5, life=30,
         gen=1, gen_intvl=4, emtr_life=40, init_pos=1, radius=1.0, axis=(0, 1, 0), vel=(.01, .06), alpha=(31, 31, 0))
    fin(CANDLE18, b, rs, (0, 1))
    b, rs = pk(WAVES18, {}, alpha=fxart.ring())
    for res, sd in ((0, "player"), (1, "enemy")):
        spray(b, rs, res, sd, (0, 24), (0, 22), 16, tex=0, clr=rgb(110, 30, 180), clr_anm=(rgb(200, 150, 255), rgb(40, 0, 80)),
              scl=.9, gen=1, gen_intvl=4, emtr_life=30, radius=.1, alpha=(31, 31, 0), scl_anm=(.5, 1.4, 2.2, 0, 160))
    fin(WAVES18, b, rs, (0, 1))

    # Premonition (Future Sight): a fortune cookie floats down glowing - crack - the fortune: UR TAKIN AN L
    b, rs = pk(COOKIE18, {1: (fxart.fortune_cookie(), 1.1, 4, {}), 2: (fxart.fortune_cookie(cracked=True), 1.1, 4, {})},
               alpha=fxart.speck())
    burst(b, rs, 0, rgb(225, 175, 90), rgb(255, 230, 170), .4, 10, .14, up=.12, gravity=.016, life=22)
    fin(COOKIE18, b, rs, (0, 1, 2))
    b, rs = pk(SLIP18, {0: (fxart.fortune_slip(), ONE_TO_ONE, 4, {"colors": 16})})
    fin(SLIP18, b, rs, (0,))

    # Ankle Break (Fake Out): dribble dribble - crossover one way - crossover the other - the foe's ankles GIVE
    b, rs = pk(BALL18, {1: (fxart.basketball(), .6, 4, {})}, alpha=fxart.dash_lines())
    burst(b, rs, 0, rgb(255, 255, 255), rgb(255, 255, 255), .5, 3, .05, life=10)
    fin(BALL18, b, rs, (0, 1))

    # Scheme (Nasty Plot): the conspiracy board goes up - red string everywhere - they lean in... it's all
    # connected. Evil glow.
    b, rs = pk(CORK18, {1: (fxart.conspiracy_board(), 1.3, 4, {})}, alpha=fxart.tiny_spark())
    prop(b, rs, 0, tex=0, clr=rgb(255, 60, 60), clr_anm=(rgb(255, 220, 220), rgb(220, 20, 20)), scl=.45, life=8,
         gen=2, init_pos=1, radius=1.0, alpha=(31, 31, 0))
    fin(CORK18, b, rs, (0, 1))
    b, rs = pk(AURA18, {}, alpha1=fxart.power_flare())
    prop(b, rs, 0, tex=1, clr=rgb(160, 40, 220), clr_anm=(rgb(240, 200, 255), rgb(90, 0, 150)), scl=.28, life=14,
         gen=1, gen_intvl=2, emtr_life=30, init_pos=1, radius=1.0, axis=(0, 1, 0), vel=(.01, .16), alpha=(20, 16, 0))
    fin(AURA18, b, rs, (0,))

    # Steel Plate (Iron Defense): kitchen armor - a pot CLANGS down on their head, a baking sheet up as a shield -
    # ping, ping, ping off of it
    b, rs = pk(ARMOR18, {1: (fxart.pot_helmet(), .9, 4, {}), 2: (fxart.baking_sheet(), 1.0, 4, {})},
               alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 255, 220), rgb(255, 255, 255), .45, 5, .14, life=10)
    fin(ARMOR18, b, rs, (0, 1, 2))

    # Turn Up (Uproar): lights down, the disco ball drops - the whole screen bouncing on the beat - until the
    # NOISE COMPLAINT gets slapped on. Record scratch.
    b, rs = pk(PARTY18, {1: (fxart.disco_ball(), 1.0, 70, {"spin": 0x0500}),
                         2: (fxart.noise_complaint(), ONE_TO_ONE, 4, {"colors": 30})}, alpha=fxart.glow_dot())
    fin(PARTY18, b, rs, (1, 2))
    b, rs = pk(LIGHTS18, {}, alpha=fxart.glow_dot())
    prop(b, rs, 0, tex=0, clr=rgb(255, 60, 200), clr_anm=(rgb(80, 220, 255), rgb(255, 230, 60)), scl=.9, life=8,
         gen=3, gen_intvl=2, emtr_life=60, init_pos=1, radius=3.0, alpha=(24, 20, 0))
    prop(b, rs, 1, tex=0, clr=rgb(255, 255, 255), clr_anm=(rgb(255, 255, 255), rgb(200, 230, 255)), scl=.35, life=6,
         gen=4, gen_intvl=2, emtr_life=60, init_pos=1, radius=2.6, alpha=(31, 31, 0))
    fin(LIGHTS18, b, rs, (0, 1))

    # Tough It Out (Endure): band-aid, band-aid, band-aid, ice pack - held together with nothing but spite
    b, rs = pk(AID18, {1: (fxart.bandaid(), .5, 4, {}), 2: (fxart.ice_pack(), .8, 4, {}),
                       3: (fxart.bandaid().rotate(45, resample=_I.BICUBIC), .5, 4, {})}, alpha=fxart.fizz_drop())
    burst(b, rs, 0, rgb(150, 210, 255), rgb(240, 250, 255), .3, 3, .08, up=.1, gravity=.012, life=16)
    fin(AID18, b, rs, (0, 1, 2, 3))

    # Plan Z (Last Resort): out of options - so they throw THE KITCHEN SINK
    b, rs = pk(SINK18, {1: (fxart.kitchen_sink(), 1.3, 4, {})}, alpha=fxart.fizz_drop())
    burst(b, rs, 0, rgb(120, 190, 255), rgb(240, 250, 255), .4, 4, .1, up=.3, gravity=.02, life=22, emtr_life=24,
          gen_intvl=2)
    fin(SINK18, b, rs, (0, 1))
    b, rs = pk(BOOM18, {}, alpha=fxart.soot_puff(), alpha1=fxart.tall_puff())
    prop(b, rs, 0, tex=0, clr=rgb(200, 190, 175), clr_anm=(rgb(250, 245, 235), rgb(130, 120, 110)), scl=1.0, life=28,
         gen=10, init_pos=1, radius=.6, axis=(0, 1, 0), vel=(.2, .08), alpha=(26, 22, 0), scl_anm=(.4, 1.3, 2.0, 60, 200))
    prop(b, rs, 1, tex=0, clr=rgb(120, 190, 255), clr_anm=(rgb(240, 250, 255), rgb(80, 150, 255)), scl=.35, life=24,
         gen=14, init_pos=1, radius=.3, axis=(0, 1, 0), vel=(.22, .3), gravity=(0, -.025, 0), alpha=(31, 31, 0))
    fin(BOOM18, b, rs, (0, 1))

    # Throwdown (Close Combat): the cartoon fight cloud - BAP BOP POW - stars, a shoe flies out, then a TOOTH
    b, rs = pk(BRAWL18, {1: (fxart.fight_cloud(), 1.7, 4, {}),
                         2: (fxart.flying_shoe(), .6, 30, {"move": (-3.5, 4), "spin": 0x0C00}),
                         3: (fxart.flying_tooth(), .45, 30, {"move": (3, 5), "spin": -0x1000})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 230, 60), rgb(255, 255, 220), .5, 4, .16, life=12)
    fin(BRAWL18, b, rs, (0, 1, 2, 3))
    b, rs = pk(BRAWLFX18, {}, alpha=fxart.soot_puff())
    prop(b, rs, 0, tex=0, clr=rgb(215, 205, 185), clr_anm=(rgb(250, 245, 235), rgb(160, 150, 130)), scl=.8, life=18,
         gen=2, gen_intvl=2, emtr_life=40, init_pos=1, radius=1.0, axis=(0, 1, 0), vel=(.06, .02), alpha=(26, 22, 0),
         scl_anm=(.4, 1.2, 1.6, 60, 200))
    fin(BRAWLFX18, b, rs, (0,))

    # Stay Calm (Calm Mind): lights soft - a scented candle, chamomile tea - cucumber slices on - breathe in...
    # breathe out...
    b, rs = pk(CALM18, {1: (fxart.tea_cup(), .9, 4, {}), 2: (fxart.scented_candle(), .9, 4, {}),
                        3: (fxart.cucumber_slice(), .4, 4, {})}, alpha=fxart.soft_puff())
    prop(b, rs, 0, tex=0, clr=rgb(235, 235, 240), clr_anm=(rgb(255, 255, 255), rgb(200, 200, 210)), scl=.5, life=30,
         gen=1, gen_intvl=4, emtr_life=60, init_pos=1, radius=.2, axis=(0, 1, 0), vel=(.01, .06), alpha=(18, 14, 0),
         scl_anm=(.4, 1.2, 1.8, 60, 200))
    fin(CALM18, b, rs, (0, 1, 2, 3))

    # Snow Cone: a rainbow snow cone - wind up - SPLAT, right in the face. Brain freeze.
    b, rs = pk(SNOWCONE18, {1: (fxart.snow_cone(), .9, 4, {}), 2: (fxart.syrup_splat(), 1.1, 4, {})},
               alpha=fxart.speck())
    burst(b, rs, 0, rgb(220, 240, 255), rgb(255, 255, 255), .45, 14, .2, up=.16, gravity=.016, life=24)
    fin(SNOWCONE18, b, rs, (0, 1, 2))

    # Crash Out (Thrash): the cookout table - they stare at it - shaking - and FLIP IT. Plates, cups, ribs, all of
    # it, onto the foe
    b, rs = pk(TABLE18, {1: (fxart.folding_table(), 1.3, 4, {}), 2: (fxart.folding_table(flipped=True), 1.3, 4, {})},
               alpha=fxart.speck())
    burst(b, rs, 0, rgb(170, 90, 40), rgb(230, 160, 90), .4, 10, .18, up=.3, gravity=.024, life=24)
    fin(TABLE18, b, rs, (0, 1, 2))
    b, rs = pk(PLATES18, {1: (fxart.paper_plate(), .6, 30, {"move": (4, 5), "spin": 0x1400}),
                          2: (fxart.paper_plate(), .6, 30, {"move": (-4, 5.5), "spin": -0x1400})}, alpha=fxart.soot_puff())
    burst(b, rs, 0, rgb(210, 200, 185), rgb(250, 245, 235), .8, 8, .16, up=.04, life=22, alpha=(26, 20, 0),
          scl_anm=(.4, 1.3, 1.8, 60, 200))
    fin(PLATES18, b, rs, (0, 1, 2))

    # Pogo Stick (Bounce): boing... boing... BOING - way up - and down on the foe's head
    b, rs = pk(POGO18, {1: (fxart.pogo_stick(), 1.0, 4, {})}, alpha=fxart.soot_puff())
    burst(b, rs, 0, rgb(200, 190, 170), rgb(250, 245, 235), .6, 5, .12, up=.02, life=18, alpha=(24, 20, 0),
          scl_anm=(.4, 1.2, 1.7, 60, 200))
    fin(POGO18, b, rs, (0, 1))

    # Shear Pain (X-Scissor): salon shears - snip snip snip - hair flying - a big X - and a fresh bald spot,
    # gleaming
    b, rs = pk(SCISS18, {1: (fxart.salon_scissors(), 1.0, 4, {}), 2: (fxart.salon_scissors(shut=True), 1.0, 4, {})},
               alpha=fxart.hair_tuft())
    burst(b, rs, 0, rgb(120, 80, 40), rgb(180, 130, 80), .3, 6, .14, up=.1, gravity=.012, life=26,
          flags_on=(1 << 14) | (1 << 12))
    rot(b, rs, 0, spin=0x0600)
    fin(SCISS18, b, rs, (0, 1, 2))
    b, rs = pk(SHINE18, {}, alpha=fxart.wink_twinkle(), alpha1=fxart.light_shaft())
    prop(b, rs, 0, tex=0, clr=rgb(255, 255, 255), clr_anm=(rgb(255, 255, 255), rgb(255, 250, 200)), scl=.6, life=16,
         scl_anm=(.2, 1.4, .2, 60, 160), alpha=(31, 31, 0))
    fin(SHINE18, b, rs, (0,))

    # Lava Lamp (Lava Plume): the lava lamp heats up... bubbling... and ERUPTS - wax blobs everywhere
    b, rs = pk(LAMP18, {1: (fxart.lava_lamp(), 1.3, 4, {})}, alpha=fxart.lava_blob())
    burst(b, rs, 0, rgb(255, 120, 30), rgb(255, 220, 120), .4, 2, .04, up=.08, life=16, emtr_life=30, gen_intvl=3)
    fin(LAMP18, b, rs, (0, 1))
    b, rs = pk(BLOBS18, {}, alpha=fxart.lava_blob())
    for res, sd in ((0, "player"), (1, "enemy")):
        spray(b, rs, res, sd, (-30 if sd == "player" else 30, 60), (0, 20), 18, tex=0, clr=rgb(255, 110, 30),
              clr_anm=(rgb(255, 230, 120), rgb(230, 50, 20)), scl=.6, gen=2, gen_intvl=1, emtr_life=24, radius=.2,
              spread=.06, alpha=(31, 31, 0), gravity=(0, -.004, 0))
    fin(BLOBS18, b, rs, (0, 1))

    # Stack Up (Stockpile): pancakes drop one by one onto the stack - higher, higher - butter, SYRUP - stocked up
    b, rs = pk(PANCAKE18, {1: (fxart.pancake(), 1.0, 4, {}), 2: (fxart.butter_syrup(), 1.0, 4, {})},
               alpha=fxart.soft_puff())
    prop(b, rs, 0, tex=0, clr=rgb(240, 240, 240), clr_anm=(rgb(255, 255, 255), rgb(200, 200, 200)), scl=.5, life=28,
         gen=1, gen_intvl=4, emtr_life=40, init_pos=1, radius=.3, axis=(0, 1, 0), vel=(.01, .06), alpha=(18, 14, 0),
         scl_anm=(.4, 1.2, 1.8, 60, 200))
    fin(PANCAKE18, b, rs, (0, 1, 2))

    # Clap Back (Counter): the clapperboard - TAKE 2 - SNAP - and SNAP again, harder
    b, rs = pk(CLAP18, {1: (fxart.clapperboard(), ONE_TO_ONE, 4, {}), 2: (fxart.clapperboard(shut=True), ONE_TO_ONE, 4, {})},
               alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 255, 220), rgb(255, 255, 255), .55, 8, .2, life=12)
    fin(CLAP18, b, rs, (0, 1, 2))

    # Hammer Time (Crabhammer): the carnival high striker - the mallet winds up - WHAM - the puck flies up - DING -
    # then the mallet comes down on the foe too
    b, rs = pk(STRIKER18, {1: (fxart.high_striker(), 1.6, 4, {}), 2: (fxart.mallet(), 1.2, 4, {}),
                           3: (flipx(fxart.mallet()), 1.2, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 230, 80), rgb(255, 255, 220), .5, 8, .2, life=14)
    fin(STRIKER18, b, rs, (0, 1, 2, 3))
    b, rs = pk(PUCK18, {0: (fxart.striker_puck(), .45, 4, {})})
    fin(PUCK18, b, rs, (0,))

    # Chalkboard (Metal Sound): a chalkboard - a fork - and the slowest, longest SCREEEECH. The foe's soul leaves.
    b, rs = pk(CHALK18, {1: (fxart.chalkboard(), ONE_TO_ONE, 4, {"colors": 24}), 2: (fxart.dinner_fork(), 1.0, 4, {})},
               alpha=fxart.speck())
    burst(b, rs, 0, rgb(240, 240, 240), rgb(255, 255, 255), .3, 3, .06, up=.02, gravity=.01, life=14)
    fin(CHALK18, b, rs, (0, 1, 2))

    # Mosquito (Bug Buzz): one mosquito. bzzzz. round their head. they swing - and SLAP THEMSELVES. Bites
    # everywhere.
    b, rs = pk(MOSQ18, {1: (fxart.mosquito(), .55, 4, {}), 2: (flipx(fxart.mosquito()), .55, 4, {})},
               alpha=fxart.dash_lines())
    prop(b, rs, 0, tex=0, clr=rgb(255, 255, 255), clr_anm=(rgb(255, 255, 255), rgb(220, 220, 220)), scl=.4, life=4,
         alpha=(20, 16, 0))
    fin(MOSQ18, b, rs, (0, 1, 2))
    b, rs = pk(WELT18, {}, alpha=fxart.glow_dot(), alpha1=fxart.light_shaft())
    prop(b, rs, 0, tex=0, clr=rgb(255, 70, 70), clr_anm=(rgb(255, 160, 160), rgb(230, 30, 30)), scl=.4, life=40,
         gen=6, init_pos=1, radius=.8, alpha=(31, 31, 0), scl_anm=(.2, 1.0, 1.0, 80, 255))
    fin(WELT18, b, rs, (0,))

    # Flush It (Whirlpool): a giant toilet round the foe - the handle - FLUSHHH - spinning, sinking, the TP roll
    # going round - and they pop back up soaked
    b, rs = pk(TOILET18, {1: (fxart.toilet(), 1.3, 4, {}), 2: (fxart.tp_roll(), .5, 4, {})}, alpha=fxart.fizz_drop())
    burst(b, rs, 0, rgb(120, 190, 255), rgb(240, 250, 255), .4, 12, .2, up=.34, gravity=.024, life=24)
    fin(TOILET18, b, rs, (0, 1, 2))
    b, rs = pk(FLUSH18, {}, alpha=fxart.swirl_water())
    prop(b, rs, 0, tex=0, clr=rgb(90, 170, 255), clr_anm=(rgb(220, 240, 255), rgb(40, 120, 230)), scl=1.6, life=50,
         alpha=(26, 24, 0), flags_on=(1 << 14) | (1 << 12), scl_anm=(.3, 1.0, .4, 40, 200))
    rot(b, rs, 0, spin=0x1400)
    prop(b, rs, 1, tex=0, clr=rgb(120, 190, 255), clr_anm=(rgb(240, 250, 255), rgb(80, 150, 255)), scl=.7, life=30,
         flags_on=(1 << 14) | (1 << 12), alpha=(20, 16, 0))
    rot(b, rs, 1, spin=-0x0C00)
    fin(FLUSH18, b, rs, (0, 1))
    SET10_82 += [DJ18, DUFFEL18, KNUX18, CAR18, CD18, COAT18, BROOM18, RING18, WET18, CANDLE18, COOKIE18, BALL18,
                 CORK18, ARMOR18, PARTY18, AID18, SINK18, BRAWL18, CALM18, SNOWCONE18, TABLE18, PLATES18, POGO18,
                 SCISS18, LAMP18, PANCAKE18, CLAP18, STRIKER18, CHALK18, MOSQ18, TOILET18]


    # ---- set 19: the TMs --------------------------------------------------------------------------------
    def spray2(b, rs, frm, aim, frames, art_tex=0, **edit):
        """res 0 = the player's spray, res 1 = the enemy's (frm per side: (player px, enemy px))."""
        for res, sd in ((0, "player"), (1, "enemy")):
            spray(b, rs, res, sd, frm[sd], aim, frames, tex=art_tex, **edit)

    # Fruit Throw (Natural Gift): a pineapple - BONK - then a whole watermelon - SPLAT
    b, rs = pk(FRUIT19, {1: (fxart.pineapple(), .6, 4, {}), 2: (fxart.watermelon(), .9, 4, {}),
                         3: (fxart.melon_splat(), 1.2, 4, {})}, alpha=fxart.fizz_drop())
    burst(b, rs, 0, rgb(240, 60, 80), rgb(255, 180, 190), .4, 14, .22, up=.3, gravity=.024, life=24)
    fin(FRUIT19, b, rs, (0, 1, 2, 3))

    # Crash Pad (Roost): an air mattress - pump, pump, pump - it puffs up - flop - healing
    b, rs = pk(MATTRESS19, {1: (fxart.air_mattress(flat=True), 1.2, 4, {}), 2: (fxart.air_mattress(), 1.2, 4, {})},
               alpha=fxart.soft_puff())
    burst(b, rs, 0, rgb(230, 240, 255), rgb(255, 255, 255), .5, 4, .1, life=16, alpha=(24, 18, 0))
    fin(MATTRESS19, b, rs, (0, 1, 2))
    b, rs = pk(HEAL19, {}, alpha=fxart.glow_dot())
    prop(b, rs, 0, tex=0, clr=rgb(120, 255, 140), clr_anm=(rgb(230, 255, 230), rgb(60, 220, 100)), scl=.32, life=22,
         gen=1, gen_intvl=2, emtr_life=30, init_pos=1, radius=1.0, axis=(0, 1, 0), vel=(.01, .1), alpha=(31, 31, 0))
    fin(HEAL19, b, rs, (0,))

    # Toss It (Fling): they yeet the whole old box TV
    b, rs = pk(TV19, {1: (fxart.crt_tv(), 1.0, 4, {})}, alpha=fxart.speck())
    burst(b, rs, 0, rgb(220, 220, 225), rgb(255, 255, 255), .45, 16, .26, up=.26, gravity=.024, life=24)
    fin(TV19, b, rs, (0, 1))

    # Dream Killer (Dream Eater): the foe's dream bubble - mansion, cash, chain - and a pin. POP.
    b, rs = pk(DREAM19, {1: (fxart.dream_bubble(), 1.3, 4, {}), 2: (fxart.safety_pin(), .7, 4, {})},
               alpha=fxart.soft_puff())
    burst(b, rs, 0, rgb(250, 250, 255), rgb(255, 255, 255), .5, 10, .2, life=16, alpha=(28, 22, 0))
    fin(DREAM19, b, rs, (0, 1, 2))

    # Claw Clap (Dragon Claw): a giant boiled lobster claw - snap, snap - CLAMPS on. Old Bay everywhere.
    b, rs = pk(LOBSTER19, {1: (fxart.lobster_claw(), 1.2, 4, {}), 2: (fxart.lobster_claw(shut=True), 1.2, 4, {})},
               alpha=fxart.speck())
    burst(b, rs, 0, rgb(230, 120, 40), rgb(255, 200, 120), .35, 14, .2, up=.16, gravity=.016, life=22)
    fin(LOBSTER19, b, rs, (0, 1, 2))
    b, rs = pk(LOBL19, {0: (flipx(fxart.lobster_claw()), 1.2, 4, {}), 1: (flipx(fxart.lobster_claw(shut=True)), 1.2, 4, {})})
    fin(LOBL19, b, rs, (0, 1))

    # U-Turn: a rental e-scooter zips in - BONK - pulls a U-turn and dips
    b, rs = pk(SCOOT19, {1: (fxart.e_scooter(), 1.1, 4, {}), 2: (flipx(fxart.e_scooter()), 1.1, 4, {})},
               alpha=fxart.dash_lines())
    burst(b, rs, 0, rgb(255, 255, 255), rgb(255, 255, 255), .6, 2, .05, life=10)
    fin(SCOOT19, b, rs, (0, 1, 2))

    # Dragon Beam (Dragon Pulse): the parade dragon dances in - firecrackers popping everywhere
    b, rs = pk(DRAGON19, {1: (fxart.dragon_head(), 1.2, 4, {}), 2: (flipx(fxart.dragon_head()), 1.2, 4, {})},
               alpha=fxart.firecracker_string())
    burst(b, rs, 0, rgb(255, 80, 40), rgb(255, 240, 120), .55, 3, .08, life=10)
    fin(DRAGON19, b, rs, (0, 1, 2))

    # Silver Dust (Silver Wind): a glitter-bomb envelope - they open it - silver glitter EVERYWHERE, forever
    b, rs = pk(GLITTER19, {1: (fxart.glitter_envelope(), 1.0, 4, {}), 2: (fxart.glitter_envelope(open_=True), 1.0, 4, {})},
               alpha=fxart.tiny_spark())
    prop(b, rs, 0, tex=0, clr=rgb(220, 225, 240), clr_anm=(rgb(255, 255, 255), rgb(160, 170, 200)), scl=.45, life=40,
         gen=6, gen_intvl=1, emtr_life=10, init_pos=1, radius=.4, axis=(0, 1, 0), vel=(.2, .26), gravity=(0, -.012, 0),
         alpha=(31, 31, 0), flags_on=(1 << 14) | (1 << 12))
    rot(b, rs, 0, spin=0x0C00)
    fin(GLITTER19, b, rs, (0, 1, 2))

    # Ice Storm (Hail): a giant bag of party ICE drops out the sky - bursts - cubes hailing on everybody
    b, rs = pk(ICEBAG19, {1: (fxart.ice_bag(), ONE_TO_ONE, 4, {})}, alpha=fxart.ice_cubelet())
    burst(b, rs, 0, rgb(200, 235, 255), rgb(255, 255, 255), .45, 14, .24, up=.2, gravity=.024, life=24)
    fin(ICEBAG19, b, rs, (0, 1))
    b, rs = pk(CUBES19, {}, alpha=fxart.ice_cubelet())
    prop(b, rs, 0, tex=0, clr=rgb(200, 235, 255), clr_anm=(rgb(255, 255, 255), rgb(150, 200, 255)), scl=.4, life=30,
         gen=2, gen_intvl=1, emtr_life=40, init_pos=1, radius=3.0, axis=(-.2, -1, 0), vel=(0, .4), alpha=(31, 31, 0),
         flags_on=(1 << 14) | (1 << 12))
    rot(b, rs, 0, spin=0x0800)
    fin(CUBES19, b, rs, (0,))

    # Confiscate (Embargo): CAUTION tape goes up round the foe - the item goes in an EVIDENCE bag
    b, rs = pk(EVID19, {1: (fxart.caution_strip(), ONE_TO_ONE, 4, {}), 2: (fxart.evidence_bag(), ONE_TO_ONE, 4, {})},
               alpha=fxart.glow_dot())
    prop(b, rs, 0, tex=0, clr=rgb(255, 60, 60), clr_anm=(rgb(255, 200, 200), rgb(60, 80, 255)), scl=1.6, life=6,
         alpha=(20, 16, 0))
    fin(EVID19, b, rs, (0, 1, 2))

    # Flick a Bic (Will-O-Wisp): strike a match - FSST - ghostly blue flames drift over and cling
    b, rs = pk(MATCH19, {1: (fxart.matchbox(), 1.0, 4, {}), 2: (fxart.matchbox(lit=True), 1.0, 4, {})},
               alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 230, 120), rgb(255, 255, 220), .4, 6, .14, life=10)
    fin(MATCH19, b, rs, (0, 1, 2))
    b, rs = pk(WISP19, {}, alpha=fxart.glow_dot())
    spray2(b, rs, {"player": (40, 30), "enemy": (-40, 26)}, (0, 20), 30, clr=rgb(100, 150, 255),
           clr_anm=(rgb(230, 240, 255), rgb(60, 80, 255)), scl=.55, gen=1, gen_intvl=5, emtr_life=24, radius=.2,
           spread=.02, alpha=(28, 24, 0))
    fin(WISP19, b, rs, (0, 1))

    # Static Shock (Shock Wave): a balloon rubbed on their head - squeak squeak - and ZAP
    b, rs = pk(BALLOON19, {1: (fxart.party_balloon(), .9, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 240, 90), rgb(255, 255, 255), .4, 4, .12, life=10)
    fin(BALLOON19, b, rs, (0, 1))
    b, rs = pk(ZAP19, {}, alpha=fxart.zig_spark())
    spray2(b, rs, {"player": (10, 56), "enemy": (-10, 46)}, (0, 24), 8, clr=rgb(255, 240, 90),
           clr_anm=(rgb(255, 255, 255), rgb(255, 200, 30)), scl=.7, gen=3, gen_intvl=1, emtr_life=8, radius=.2,
           spread=.03, alpha=(31, 31, 0), flags_on=(1 << 14) | (1 << 12))
    for r in (0, 1):
        rot(b, rs, r, spin=0x2000)
    fin(ZAP19, b, rs, (0, 1))

    # Graze (False Swipe): a frisbee screams right past their head - grazes them - one feather drifts down
    b, rs = pk(FRISBEE19, {1: (fxart.frisbee(), .6, 4, {})}, alpha=fxart.lone_feather())
    prop(b, rs, 0, tex=0, clr=rgb(250, 240, 220), clr_anm=(rgb(255, 255, 255), rgb(230, 210, 170)), scl=.55, life=70,
         axis=(0, -1, 0), vel=(0, .05), alpha=(31, 31, 0), flags_on=(1 << 14) | (1 << 12))
    rot(b, rs, 0, spin=0x0300)
    fin(FRISBEE19, b, rs, (0, 1))

    # Fall Guy (Substitute): POOF - a crash-test dummy takes the hit for them
    b, rs = pk(DUMMY19, {1: (fxart.crash_dummy(), 1.1, 4, {})}, alpha=fxart.soft_puff())
    burst(b, rs, 0, rgb(235, 235, 240), rgb(255, 255, 255), .8, 10, .16, life=20, alpha=(28, 22, 0),
          scl_anm=(.4, 1.3, 1.8, 60, 200))
    fin(DUMMY19, b, rs, (0, 1))

    # Shady Claw (Shadow Claw): lights dim - claws rip up out of the foe's own shadow
    b, rs = pk(CLAWS19, {0: (fxart.shadow_claws(), 1.3, 4, {}), 1: (flipx(fxart.shadow_claws()), 1.3, 4, {})})
    fin(CLAWS19, b, rs, (0, 1))

    # Steel Toe (Iron Tail): a wrecking ball swings in from off-screen - WHAM
    b, rs = pk(WRECK19, {1: (fxart.wrecking_ball(), 1.4, 4, {})}, alpha=fxart.soot_puff())
    burst(b, rs, 0, rgb(200, 190, 175), rgb(250, 245, 235), .9, 10, .2, up=.04, life=22, alpha=(26, 20, 0),
          scl_anm=(.4, 1.3, 1.8, 60, 200))
    fin(WRECK19, b, rs, (0, 1))

    # Hidden Strap (Hidden Power): a teddy bear - wobble - RIIIP - the stash inside: glowing power orbs
    b, rs = pk(TEDDY19, {1: (fxart.teddy_bear(), 1.0, 4, {}), 2: (fxart.teddy_bear(ripped=True), 1.0, 4, {})},
               alpha=fxart.soft_puff())
    burst(b, rs, 0, rgb(250, 250, 250), rgb(255, 255, 255), .45, 10, .2, up=.1, gravity=.008, life=26)
    fin(TEDDY19, b, rs, (0, 1, 2))
    b, rs = pk(ORBS19, {}, alpha=fxart.glow_dot())                            # (the bullets)
    spray2(b, rs, {"player": (52, 34), "enemy": (-52, 30)}, (0, 20), 6, clr=rgb(255, 230, 120),
           clr_anm=(rgb(255, 255, 230), rgb(255, 160, 40)), scl=.45, gen=2, gen_intvl=1, emtr_life=3, radius=.05,
           spread=.01, alpha=(31, 31, 0))
    fin(ORBS19, b, rs, (0, 1))
    b, rs = pk(PISTOL19, {1: (fxart.teddy_strap(), 1.0, 4, {}), 2: (flipx(fxart.teddy_strap()), 1.0, 4, {})},
               alpha=fxart.camera_flash())
    prop(b, rs, 0, tex=0, clr=rgb(255, 220, 80), clr_anm=(rgb(255, 255, 230), rgb(255, 140, 30)), scl=1.4, life=5,
         alpha=(31, 31, 0), scl_anm=(.4, 1.3, .6, 60, 160))
    fin(PISTOL19, b, rs, (0, 1, 2))

    # Bullet Spray (Bullet Seed): a bag of sunflower seeds - and they spit 'em like a machine gun
    b, rs = pk(SEEDS19, {1: (fxart.seed_bag(), .9, 4, {})}, alpha=fxart.speck())
    fin(SEEDS19, b, rs, (1,))
    b, rs = pk(SEEDFX19, {}, alpha=fxart.seed_shell())
    spray2(b, rs, {"player": (6, 40), "enemy": (-6, 32)}, (0, 22), 10, clr=rgb(60, 60, 60),
           clr_anm=(rgb(230, 230, 230), rgb(40, 40, 40)), scl=.35, gen=1, gen_intvl=1, emtr_life=30, radius=.1,
           spread=.01, alpha=(31, 31, 0), flags_on=(1 << 14) | (1 << 12))
    for r in (0, 1):
        rot(b, rs, r, spin=0x1400)
    fin(SEEDFX19, b, rs, (0, 1))

    # Rock Pile (Rock Tomb): beep, beep, beep - a dump truck backs up to the foe - tips - and buries them
    b, rs = pk(TRUCK19, {1: (fxart.dump_truck(), 1.4, 4, {}), 2: (fxart.dump_truck(tipped=True), 1.4, 4, {})},
               alpha=fxart.soot_puff())
    burst(b, rs, 0, rgb(190, 180, 165), rgb(240, 235, 225), .8, 6, .14, life=20, alpha=(26, 20, 0),
          scl_anm=(.4, 1.3, 1.8, 60, 200))
    fin(TRUCK19, b, rs, (0, 1, 2))
    b, rs = pk(TRUCKL19, {0: (flipx(fxart.dump_truck()), 1.4, 4, {}), 1: (flipx(fxart.dump_truck(tipped=True)), 1.4, 4, {})})
    fin(TRUCKL19, b, rs, (0, 1))
    b, rs = pk(GRAVEL19, {}, alpha=fxart.gravel())
    prop(b, rs, 0, tex=0, clr=rgb(150, 140, 130), clr_anm=(rgb(210, 200, 190), rgb(100, 95, 90)), scl=.5, life=24,
         gen=3, gen_intvl=1, emtr_life=24, init_pos=1, radius=.7, axis=(0, -1, 0), vel=(.02, .2), gravity=(0, -.01, 0),
         alpha=(31, 31, 0))
    fin(GRAVEL19, b, rs, (0,))

    # Overcook (Overheat): the toaster - ding - two charcoal slices fly out - smoke - the smoke alarm screaming
    b, rs = pk(TOAST19, {1: (fxart.toaster(), 1.0, 4, {}), 2: (fxart.toaster(burnt=True), 1.0, 4, {}),
                         3: (fxart.smoke_alarm(), .7, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 140, 40), rgb(255, 230, 120), .4, 6, .14, life=12)
    fin(TOAST19, b, rs, (0, 1, 2, 3))
    b, rs = pk(SMOKE19, {}, alpha=fxart.soot_puff())
    prop(b, rs, 0, tex=0, clr=rgb(50, 45, 45), clr_anm=(rgb(120, 110, 105), rgb(20, 20, 20)), scl=.8, life=36,
         gen=2, gen_intvl=2, emtr_life=40, init_pos=1, radius=.5, axis=(0, 1, 0), vel=(.04, .1), alpha=(26, 22, 0),
         scl_anm=(.4, 1.3, 2.0, 60, 200))
    prop(b, rs, 1, tex=0, clr=rgb(255, 120, 30), clr_anm=(rgb(255, 230, 120), rgb(220, 40, 10)), scl=.7, life=20,
         gen=6, init_pos=1, radius=.7, axis=(0, 1, 0), vel=(.06, .14), alpha=(31, 31, 0), scl_anm=(.4, 1.2, .5, 60, 160))
    fin(SMOKE19, b, rs, (0, 1))

    # Energy Drink (Energy Ball): crack - glug glug glug - eye twitch - and they fire a green ball of pure caffeine
    b, rs = pk(CAN19, {1: (fxart.energy_can(), ONE_TO_ONE, 4, {})}, alpha=fxart.fizz_drop())
    burst(b, rs, 0, rgb(160, 255, 100), rgb(240, 255, 220), .3, 6, .12, up=.18, gravity=.016, life=18)
    fin(CAN19, b, rs, (0, 1))
    b, rs = pk(GREEN19, {}, alpha=fxart.glow_dot())
    spray2(b, rs, {"player": (24, 28), "enemy": (-24, 24)}, (0, 22), 14, clr=rgb(120, 255, 60),
           clr_anm=(rgb(240, 255, 220), rgb(60, 220, 30)), scl=1.6, gen=1, gen_intvl=1, emtr_life=1, radius=0,
           alpha=(31, 31, 31))
    fin(GREEN19, b, rs, (0, 1))

    # Dream Talk (Sleep Talk): nightcap on - mumbling nonsense - and they swing at the foe in their sleep
    b, rs = pk(SLEEP19, {1: (fxart.nightcap(), .8, 4, {}), 2: (fxart.mumble_bubble(), 1.0, 4, {})},
               alpha=fxart.snore_z())
    prop(b, rs, 0, tex=0, clr=rgb(200, 210, 255), clr_anm=(rgb(255, 255, 255), rgb(150, 160, 255)), scl=.45,
         life=26, gen=1, gen_intvl=6, emtr_life=40, axis=(.5, 1, 0), vel=(0, .1), alpha=(31, 31, 0))
    fin(SLEEP19, b, rs, (0, 1, 2))

    # Trade Spots (Skill Swap): they trade cards - then they literally TRADE SPOTS
    b, rs = pk(CARDS19, {1: (fxart.trading_card(n=0), .7, 4, {}), 2: (fxart.trading_card(n=1), .7, 4, {})},
               alpha=fxart.wink_twinkle())
    prop(b, rs, 0, tex=0, clr=rgb(255, 255, 220), clr_anm=(rgb(255, 255, 255), rgb(255, 220, 90)), scl=.6, life=12,
         scl_anm=(.2, 1.3, .2, 60, 160), alpha=(31, 31, 0))
    fin(CARDS19, b, rs, (0, 1, 2))

    # Big Blast (Focus Blast): a firework mortar - the fuse - THOOMP - BOOM, a full Fourth of July on the foe
    b, rs = pk(MORTAR19, {1: (fxart.firework_mortar(), .9, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 220, 80), rgb(255, 255, 220), .35, 3, .1, up=.1, life=10)
    fin(MORTAR19, b, rs, (0, 1))
    b, rs = pk(FIREWORK19, {}, alpha=fxart.tiny_spark(), alpha1=fxart.light_shaft())
    prop(b, rs, 0, tex=0, clr=rgb(255, 60, 120), clr_anm=(rgb(120, 255, 255), rgb(255, 220, 40)), scl=.55, life=30,
         gen=40, init_pos=1, radius=.3, axis=(0, 1, 0), vel=(.4, 0), gravity=(0, -.012, 0), alpha=(31, 31, 0))
    prop(b, rs, 1, tex=0, clr=rgb(255, 240, 150), clr_anm=(rgb(255, 255, 255), rgb(255, 160, 40)), scl=.4, life=6,
         alpha=(31, 31, 0))
    fin(FIREWORK19, b, rs, (0, 1))

    # Dumpster (Recycle): the recycling bin - rummage, rummage - junk flying out - FOUND IT
    b, rs = pk(BIN19, {1: (fxart.recycling_bin(), 1.1, 4, {}), 2: (fxart.old_banana(), .6, 30, {"move": (-2, 4), "spin": 0x0A00}),
                       3: (fxart.old_banana().rotate(120, resample=_I.BICUBIC), .5, 30, {"move": (2.5, 4.5), "spin": -0x0C00})},
               alpha=fxart.wink_twinkle())
    prop(b, rs, 0, tex=0, clr=rgb(255, 240, 120), clr_anm=(rgb(255, 255, 255), rgb(255, 210, 60)), scl=.8, life=14,
         scl_anm=(.2, 1.3, .2, 60, 160), alpha=(31, 31, 0))
    fin(BIN19, b, rs, (0, 1, 2, 3))

    # Snack Grab (Pluck): the foe's berry sitting right there - a reacher-grabber stretches over - snap - got it
    b, rs = pk(GRAB19, {1: (fxart.reacher_grabber(), 1.2, 4, {}), 2: (fxart.reacher_grabber(shut=True), 1.2, 4, {}),
                        3: (fxart.berry(), .5, 4, {})}, alpha=fxart.wink_twinkle())
    prop(b, rs, 0, tex=0, clr=rgb(200, 200, 255), clr_anm=(rgb(255, 255, 255), rgb(150, 150, 255)), scl=.6, life=12,
         scl_anm=(.2, 1.3, .2, 60, 160), alpha=(31, 31, 0))
    fin(GRAB19, b, rs, (0, 1, 2, 3))
    b, rs = pk(GRABL19, {0: (flipx(fxart.reacher_grabber()), 1.2, 4, {}), 1: (flipx(fxart.reacher_grabber(shut=True)), 1.2, 4, {})})
    fin(GRABL19, b, rs, (0, 1))

    # Snow Plow (Avalanche): the city plow comes through and shoves a WALL of snow onto the foe
    b, rs = pk(PLOW19, {1: (fxart.snow_plow(), 1.2, 4, {}), 2: (flipx(fxart.snow_plow()), 1.2, 4, {})},
               alpha=fxart.soft_puff())
    burst(b, rs, 0, rgb(240, 245, 255), rgb(255, 255, 255), .7, 4, .12, up=.1, life=16, alpha=(28, 24, 0))
    fin(PLOW19, b, rs, (0, 1, 2))
    b, rs = pk(SNOWWALL19, {}, alpha=fxart.soft_puff(), alpha1=fxart.tall_puff())
    prop(b, rs, 0, tex=0, clr=rgb(240, 245, 255), clr_anm=(rgb(255, 255, 255), rgb(200, 220, 240)), scl=1.0, life=30,
         gen=16, init_pos=1, radius=.8, axis=(0, 1, 0), vel=(.16, .14), gravity=(0, -.008, 0), alpha=(31, 28, 0),
         scl_anm=(.4, 1.2, 1.4, 60, 200))
    fin(SNOWWALL19, b, rs, (0,))

    # Slow Mo (Trick Room): the remote - SLOW - everything goes sepia, rippling, slooow
    b, rs = pk(REMOTE19, {1: (fxart.tv_remote(), ONE_TO_ONE, 4, {})}, alpha=fxart.ring())
    prop(b, rs, 0, tex=0, clr=rgb(255, 220, 160), clr_anm=(rgb(255, 255, 240), rgb(200, 150, 90)), scl=1.0, life=40,
         gen=1, gen_intvl=8, emtr_life=40, alpha=(24, 16, 0), scl_anm=(.2, 2.0, 3.0, 120, 200))
    fin(REMOTE19, b, rs, (0, 1))
    b, rs = pk(SEPIA19, {}, alpha=fxart.ring())
    prop(b, rs, 0, tex=0, clr=rgb(255, 220, 160), clr_anm=(rgb(255, 255, 240), rgb(200, 150, 90)), scl=1.4, life=40,
         gen=1, gen_intvl=10, emtr_life=40, alpha=(20, 14, 0), scl_anm=(.2, 2.0, 3.0, 120, 200))
    fin(SEPIA19, b, rs, (0,))

    # Flash Bang (Flash Cannon): a disposable camera - click... click... FLASH - the foe sees spots for days
    b, rs = pk(CAMERA19, {1: (fxart.disposable_camera(), 1.0, 4, {})}, alpha=fxart.camera_flash())
    prop(b, rs, 0, tex=0, clr=rgb(255, 255, 255), clr_anm=(rgb(255, 255, 255), rgb(220, 230, 255)), scl=.7, life=4,
         alpha=(31, 31, 31))
    fin(CAMERA19, b, rs, (0, 1))
    b, rs = pk(FLASH19, {}, alpha=fxart.glow_dot())
    prop(b, rs, 0, tex=0, clr=rgb(200, 80, 255), clr_anm=(rgb(120, 255, 120), rgb(255, 80, 200)), scl=.6, life=30,
         gen=1, gen_intvl=3, emtr_life=30, init_pos=1, radius=1.2, alpha=(28, 24, 0))
    prop(b, rs, 1, tex=0, clr=rgb(255, 255, 255), clr_anm=(rgb(255, 255, 255), rgb(220, 230, 255)), scl=3.0, life=10,
         alpha=(31, 31, 0), scl_anm=(.3, 1.2, 1.4, 60, 200))
    fin(FLASH19, b, rs, (0, 1))

    # Hit the Gym (Bulk Up): kettlebell swings - one - two - THREE - towel over the shoulder - flex
    b, rs = pk(GYM19, {1: (fxart.kettlebell(), ONE_TO_ONE, 4, {}), 2: (fxart.sweat_towel(), .8, 4, {})},
               alpha=fxart.fizz_drop())
    burst(b, rs, 0, rgb(150, 210, 255), rgb(240, 250, 255), .3, 3, .1, up=.12, gravity=.012, life=16)
    fin(GYM19, b, rs, (0, 1, 2))
    SET10_82 += [FRUIT19, MATTRESS19, TV19, DREAM19, LOBSTER19, SCOOT19, DRAGON19, GLITTER19, ICEBAG19, EVID19,
                 MATCH19, BALLOON19, FRISBEE19, DUMMY19, WRECK19, TEDDY19, PISTOL19, SEEDS19, TRUCK19, TOAST19, CAN19, SLEEP19,
                 CARDS19, MORTAR19, BIN19, GRAB19, PLOW19, REMOTE19, CAMERA19, GYM19]


    # ---- set 20: last TMs + level-up ---------------------------------------------------------------------
    sparkle = lambda b, rs, r=0, c=rgb(255, 255, 220), scl=.6: prop(b, rs, r, tex=0, clr=c, clr_anm=(rgb(255, 255, 255), c),
                                                                      scl=scl, life=12, scl_anm=(.2, 1.3, .2, 60, 160), alpha=(31, 31, 0))
    puffs = lambda b, rs, r, c, n=8, life=22, scl=.7, up=.03: burst(b, rs, r, c, rgb(255, 255, 255), scl, n, .14, up=up, life=life,
                                                                    alpha=(26, 20, 0), scl_anm=(.4, 1.3, 1.8, 60, 200))

    b, rs = pk(CLOWN20, {1: (fxart.clown_nose(), .45, 4, {}), 2: (fxart.bike_horn(), .9, 4, {}), 3: (flipx(fxart.bike_horn()), .9, 4, {})},
               alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 80, 160), rgb(120, 255, 255), .45, 12, .2, up=.16, gravity=.012, life=22)
    fin(CLOWN20, b, rs, (0, 1, 2, 3))

    b, rs = pk(SWIPE20, {1: (fxart.card_reader(), 1.0, 4, {}), 2: (fxart.card_reader(approved=True), ONE_TO_ONE, 4, {}),
                         3: (fxart.credit_card(), .5, 4, {})}, alpha=fxart.wink_twinkle())
    sparkle(b, rs)
    fin(SWIPE20, b, rs, (0, 1, 2, 3))

    b, rs = pk(PUNCHM20, {1: (fxart.punch_machine(), ONE_TO_ONE, 4, {}), 2: (fxart.punch_machine(maxed=True), ONE_TO_ONE, 4, {})},
               alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 230, 80), rgb(255, 255, 220), .5, 8, .22, life=14)
    fin(PUNCHM20, b, rs, (0, 1, 2))

    b, rs = pk(PIGGY20, {1: (fxart.piggy_bank(), 1.0, 4, {})}, alpha=fxart.gold_coin())
    burst(b, rs, 0, rgb(255, 210, 60), rgb(255, 250, 200), .45, 8, .16, up=.2, gravity=.016, life=20)
    fin(PIGGY20, b, rs, (0, 1))
    b, rs = pk(COINS20, {}, alpha=fxart.gold_coin())
    for res, foe_side in ((0, "enemy"), (1, "player")):                       # (from the foe back to the attacker)
        spray(b, rs, res, foe_side, (0, 20), (34 if foe_side == "enemy" else -34, 30), 16, tex=0, clr=rgb(255, 210, 60),
              clr_anm=(rgb(255, 250, 200), rgb(230, 160, 20)), scl=.45, gen=1, gen_intvl=2, emtr_life=20, radius=.2,
              spread=.03, alpha=(31, 31, 0), flags_on=(1 << 14) | (1 << 12))
        rot(b, rs, res, spin=0x1000)
    fin(COINS20, b, rs, (0, 1))

    b, rs = pk(IRON20, {1: (fxart.clothes_iron(), 1.2, 4, {}), 2: (flipx(fxart.clothes_iron()), 1.2, 4, {})}, alpha=fxart.soft_puff())
    puffs(b, rs, 0, rgb(235, 240, 250), n=6, up=.12)
    fin(IRON20, b, rs, (0, 1, 2))

    b, rs = pk(LIGHT20, {1: (fxart.light_switch(), ONE_TO_ONE, 4, {}), 2: (fxart.light_switch(on=True), ONE_TO_ONE, 4, {}),
                         3: (fxart.light_bulb(), 1.2, 4, {})}, alpha=fxart.glow_dot())
    prop(b, rs, 0, tex=0, clr=rgb(255, 250, 180), clr_anm=(rgb(255, 255, 255), rgb(255, 240, 120)), scl=3.0, life=14,
         alpha=(28, 22, 0), scl_anm=(.3, 1.2, 1.4, 60, 200))
    fin(LIGHT20, b, rs, (0, 1, 2, 3))

    b, rs = pk(LEGO20, {1: (fxart.lego_brick(), .4, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 230, 80), rgb(255, 255, 220), .5, 6, .16, life=12)
    fin(LEGO20, b, rs, (0, 1))

    b, rs = pk(LACES20, {1: (fxart.tied_laces(), 2.0, 4, {})}, alpha=fxart.soft_puff())
    puffs(b, rs, 0, rgb(210, 200, 180), n=8)
    fin(LACES20, b, rs, (0, 1))

    b, rs = pk(GAUGE20, {1: (fxart.pressure_gauge(), .9, 4, {}), 2: (fxart.pressure_gauge(red=True), .9, 4, {})}, alpha=fxart.soft_puff())
    puffs(b, rs, 0, rgb(240, 240, 245), n=6, up=.14)
    fin(GAUGE20, b, rs, (0, 1, 2))
    b, rs = pk(STEAM20, {}, alpha=fxart.soft_puff(), alpha1=fxart.tall_puff())
    prop(b, rs, 0, tex=1, clr=rgb(240, 240, 245), clr_anm=(rgb(255, 255, 255), rgb(190, 190, 200)), scl=.7, life=24,
         gen=3, gen_intvl=1, emtr_life=16, init_pos=1, radius=.6, axis=(0, 1, 0), vel=(.04, .3), alpha=(26, 22, 0),
         scl_anm=(.4, 1.2, 1.6, 60, 200))
    fin(STEAM20, b, rs, (0,))

    b, rs = pk(FRONT20, {1: (fxart.cardboard_lambo(), 1.5, 4, {}), 2: (fxart.cardboard_lambo(fallen=True), 1.5, 4, {})},
               alpha=fxart.soft_puff())
    puffs(b, rs, 0, rgb(210, 200, 180), n=6)
    fin(FRONT20, b, rs, (0, 1, 2))

    b, rs = pk(SAFE20, {1: (fxart.wall_safe(), 1.0, 4, {}), 2: (fxart.wall_safe(open_=True), 1.0, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 230, 80), rgb(255, 255, 220), .5, 8, .2, life=14)
    fin(SAFE20, b, rs, (0, 1, 2))

    b, rs = pk(CLIMB20, {1: (fxart.climbing_wall(), 1.4, 4, {})}, alpha=fxart.dirt_clod())
    burst(b, rs, 0, rgb(150, 145, 140), rgb(210, 205, 200), .45, 8, .12, up=.1, gravity=.022, life=24)
    fin(CLIMB20, b, rs, (0, 1))

    b, rs = pk(FOOTB20, {1: (fxart.football(), .55, 4, {})}, alpha=fxart.dash_lines())
    burst(b, rs, 0, rgb(255, 255, 255), rgb(255, 255, 255), .5, 2, .05, life=10)
    fin(FOOTB20, b, rs, (0, 1))

    b, rs = pk(FOG20, {1: (fxart.fog_machine(), 1.0, 4, {}), 2: (flipx(fxart.fog_machine()), 1.0, 4, {})}, alpha=fxart.glow_dot())
    prop(b, rs, 0, tex=0, clr=rgb(190, 90, 255), clr_anm=(rgb(255, 120, 220), rgb(90, 160, 255)), scl=.9, life=10,
         gen=2, gen_intvl=3, emtr_life=40, init_pos=1, radius=2.6, alpha=(20, 16, 0))
    fin(FOG20, b, rs, (0, 1, 2))
    b, rs = pk(FOGFX20, {}, alpha=fxart.soft_puff(), alpha1=fxart.tall_puff())
    for res, d_ in ((0, 1), (1, -1)):
        prop(b, rs, res, tex=0, clr=rgb(235, 235, 245), clr_anm=(rgb(255, 255, 255), rgb(200, 200, 220)), scl=1.4, life=44,
             gen=2, gen_intvl=1, emtr_life=30, init_pos=1, radius=.5, axis=(d_, .1, 0), vel=(.05, .2), alpha=(22, 18, 0),
             scl_anm=(.4, 1.4, 2.2, 60, 200))
    fin(FOGFX20, b, rs, (0, 1))

    b, rs = pk(AMP20, {1: (fxart.guitar_amp(), 1.1, 4, {})}, alpha=fxart.zig_spark())
    burst(b, rs, 0, rgb(255, 240, 90), rgb(255, 255, 255), .45, 6, .16, up=.1, life=12)
    fin(AMP20, b, rs, (0, 1))
    b, rs = pk(AMPFX20, {}, alpha=fxart.ring(), alpha1=fxart.light_shaft())
    prop(b, rs, 0, tex=0, clr=rgb(255, 240, 120), clr_anm=(rgb(255, 255, 255), rgb(255, 200, 40)), scl=1.0, life=16,
         gen=1, gen_intvl=4, emtr_life=20, alpha=(28, 20, 0), scl_anm=(.3, 1.8, 2.6, 80, 200))
    prop(b, rs, 1, tex=1, clr=rgb(255, 240, 90), clr_anm=(rgb(255, 255, 220), rgb(255, 200, 30)), scl=.4, life=14,
         gen=1, gen_intvl=2, emtr_life=24, init_pos=1, radius=1.0, axis=(0, 1, 0), vel=(.01, .14), alpha=(26, 22, 0))
    fin(AMPFX20, b, rs, (0, 1))

    b, rs = pk(BUGS20, {1: (fxart.motel_pillow(), 1.0, 4, {})}, alpha=fxart.bed_bug())
    fin(BUGS20, b, rs, (1,))
    b, rs = pk(BUGFX20, {}, alpha=fxart.bed_bug())
    spray2(b, rs, {"player": (34, 30), "enemy": (-34, 26)}, (0, 18), 16, clr=rgb(120, 60, 30),
           clr_anm=(rgb(190, 120, 70), rgb(80, 40, 20)), scl=.35, gen=2, gen_intvl=1, emtr_life=24, radius=.3,
           spread=.04, alpha=(31, 31, 0), flags_on=(1 << 14) | (1 << 12))
    for r in (0, 1):
        rot(b, rs, r, spin=0x0800)
    fin(BUGFX20, b, rs, (0, 1))

    b, rs = pk(MOP20, {1: (fxart.mop_bucket(), 1.3, 4, {})}, alpha=fxart.fizz_drop())
    burst(b, rs, 0, rgb(150, 140, 100), rgb(220, 210, 170), .4, 3, .06, up=.0, gravity=.02, life=20, emtr_life=24, gen_intvl=2)
    fin(MOP20, b, rs, (0, 1))

    b, rs = pk(FANNY20, {1: (fxart.neon_fanny_pack(), 1.0, 4, {}), 2: (fxart.neon_fanny_pack(open_=True), 1.0, 4, {})},
               alpha=fxart.wink_twinkle())
    sparkle(b, rs, c=rgb(150, 255, 120))
    fin(FANNY20, b, rs, (0, 1, 2))
    b, rs = pk(MONEY20, {}, alpha=fxart.money_leaf())
    spray2(b, rs, {"player": (32, 34), "enemy": (-32, 30)}, (0, 20), 20, clr=rgb(100, 200, 90),
           clr_anm=(rgb(220, 255, 210), rgb(60, 150, 50)), scl=.5, gen=1, gen_intvl=2, emtr_life=24, radius=.3,
           spread=.05, alpha=(31, 31, 0), flags_on=(1 << 14) | (1 << 12))
    for r in (0, 1):
        rot(b, rs, r, spin=0x0900)
    fin(MONEY20, b, rs, (0, 1))

    b, rs = pk(TREAD20, {1: (fxart.treadmill(), 1.9, 4, {})}, alpha=fxart.fizz_drop())
    burst(b, rs, 0, rgb(150, 210, 255), rgb(240, 250, 255), .3, 2, .1, up=.12, gravity=.012, life=16, emtr_life=40, gen_intvl=3)
    fin(TREAD20, b, rs, (0, 1))

    b, rs = pk(SLEUTH20, {1: (fxart.sleuth_glass(), 1.0, 4, {}), 2: (fxart.deerstalker(), .8, 4, {})}, alpha=fxart.soot_puff())
    prop(b, rs, 0, tex=0, clr=rgb(150, 200, 60), clr_anm=(rgb(220, 255, 140), rgb(100, 150, 30)), scl=.6, life=26,
         gen=1, gen_intvl=3, emtr_life=30, init_pos=1, radius=.6, axis=(0, 1, 0), vel=(.01, .08), alpha=(24, 20, 0),
         scl_anm=(.4, 1.2, 1.6, 60, 200))
    fin(SLEUTH20, b, rs, (0, 1, 2))

    b, rs = pk(FICUS20, {1: (fxart.ficus(), 1.3, 4, {}), 2: (fxart.peek_eyes(), .5, 4, {})}, alpha=fxart.maple_leaf())
    burst(b, rs, 0, rgb(80, 170, 70), rgb(160, 230, 140), .35, 4, .1, up=.06, gravity=.008, life=20)
    fin(FICUS20, b, rs, (0, 1, 2))

    b, rs = pk(CANDY20, {1: (fxart.rock_candy(), 1.6, 4, {})}, alpha=fxart.wink_twinkle())
    sparkle(b, rs, c=rgb(255, 150, 240))
    fin(CANDY20, b, rs, (0, 1))
    b, rs = pk(GEMBEAM20, {}, alpha=fxart.wink_twinkle())
    spray2(b, rs, {"player": (30, 46), "enemy": (-30, 40)}, (0, 22), 12, clr=rgb(255, 120, 230),
           clr_anm=(rgb(255, 255, 255), rgb(200, 60, 220)), scl=.55, gen=2, gen_intvl=1, emtr_life=18, radius=.2,
           spread=.02, alpha=(31, 31, 0), flags_on=(1 << 14) | (1 << 12))
    for r in (0, 1):
        rot(b, rs, r, spin=0x0C00)
    fin(GEMBEAM20, b, rs, (0, 1))

    b, rs = pk(SHAKE20, {1: (fxart.milkshake(), 1.0, 4, {})}, alpha=fxart.fizz_drop())
    burst(b, rs, 0, rgb(255, 170, 200), rgb(255, 230, 240), .3, 2, .06, up=.1, gravity=.01, life=14, emtr_life=30, gen_intvl=3)
    fin(SHAKE20, b, rs, (0, 1))

    b, rs = pk(SCOPE20, {1: (fxart.periscope(), 1.0, 4, {}), 2: (flipx(fxart.periscope()), 1.0, 4, {})}, alpha=fxart.wink_twinkle())
    sparkle(b, rs)
    fin(SCOPE20, b, rs, (0, 1, 2))

    b, rs = pk(LEAVES20, {}, alpha=fxart.maple_leaf())
    spray2(b, rs, {"player": (20, 40), "enemy": (-20, 34)}, (0, 16), 22, clr=rgb(90, 180, 60),
           clr_anm=(rgb(200, 255, 150), rgb(40, 130, 40)), scl=.5, gen=3, gen_intvl=1, emtr_life=30, radius=1.0,
           spread=.08, alpha=(31, 31, 0), flags_on=(1 << 14) | (1 << 12))
    for r in (0, 1):
        rot(b, rs, r, spin=0x0E00)
    fin(LEAVES20, b, rs, (0, 1))

    b, rs = pk(EXIT20, {1: (fxart.exit_door(), ONE_TO_ONE, 4, {}), 2: (fxart.exit_door(open_=True), ONE_TO_ONE, 4, {})},
               alpha=fxart.glow_dot())
    prop(b, rs, 0, tex=0, clr=rgb(255, 255, 230), clr_anm=(rgb(255, 255, 255), rgb(255, 250, 200)), scl=2.4, life=16,
         alpha=(26, 20, 0), scl_anm=(.3, 1.2, 1.4, 60, 200))
    fin(EXIT20, b, rs, (0, 1, 2))

    b, rs = pk(MOUTH20, {1: (fxart.mouthwash(), .9, 4, {})}, alpha=fxart.fizz_drop())
    burst(b, rs, 0, rgb(90, 180, 255), rgb(220, 240, 255), .3, 3, .06, up=.1, gravity=.01, life=14)
    fin(MOUTH20, b, rs, (0, 1))
    b, rs = pk(SPITFX20, {}, alpha=fxart.fizz_drop())
    spray2(b, rs, {"player": (6, 46), "enemy": (-6, 36)}, (0, 22), 12, clr=rgb(80, 170, 255),
           clr_anm=(rgb(220, 240, 255), rgb(40, 120, 230)), scl=.5, gen=4, gen_intvl=1, emtr_life=20, radius=.1,
           spread=.02, alpha=(31, 31, 0), gravity=(0, -.004, 0))
    fin(SPITFX20, b, rs, (0, 1))

    b, rs = pk(CHAIR20, {1: (fxart.lawn_chair(), 1.4, 4, {})}, alpha=fxart.wink_twinkle())
    sparkle(b, rs, c=rgb(150, 255, 150))
    fin(CHAIR20, b, rs, (0, 1))

    b, rs = pk(COMBO20, {0: (fxart.burst_sign(["3 HIT!"], fill=(40, 40, 60, 255), text=(255, 230, 60, 255)), SIGN_SCALE, 4, {"colors": 30}),
                         1: (fxart.burst_sign(["5 HIT", "COMBO!"], fill=(220, 30, 40, 255), text=(255, 255, 255, 255)), SIGN_SCALE, 4, {"colors": 30})})
    fin(COMBO20, b, rs, (0, 1))
    b, rs = pk(SLASH20, {1: (fxart.slash_single(), 1.3, 6, {"scl_anm": (.3, 1.2, 1.0, 80, 255)}),
                         2: (fxart.burst_sign(["2 HIT!"], fill=(40, 40, 60, 255), text=(255, 255, 255, 255)), SIGN_SCALE, 4, {"colors": 30})},
               alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 255, 230), rgb(255, 255, 255), .45, 6, .2, life=10)
    fin(SLASH20, b, rs, (0, 1, 2))

    b, rs = pk(BFF20, {1: (fxart.bff_half(), ONE_TO_ONE, 4, {"colors": 16}), 2: (fxart.bff_half(right=True), ONE_TO_ONE, 4, {"colors": 16})},
               alpha=fxart.glow_dot())
    prop(b, rs, 0, tex=0, clr=rgb(160, 40, 220), clr_anm=(rgb(240, 200, 255), rgb(90, 0, 150)), scl=.5, life=24,
         gen=1, gen_intvl=2, emtr_life=40, init_pos=1, radius=1.0, axis=(0, 1, 0), vel=(.01, .06), alpha=(26, 22, 0))
    fin(BFF20, b, rs, (0, 1, 2))
    b, rs = pk(LINK20, {}, alpha=fxart.glow_dot())
    spray2(b, rs, {"player": (0, 30), "enemy": (0, 26)}, (0, 30), 20, clr=rgb(170, 60, 255),
           clr_anm=(rgb(240, 200, 255), rgb(100, 0, 160)), scl=.4, gen=1, gen_intvl=1, emtr_life=30, radius=0,
           alpha=(28, 24, 0))
    fin(LINK20, b, rs, (0, 1))
    SET10_82 += [CLOWN20, SWIPE20, PUNCHM20, PIGGY20, IRON20, LIGHT20, LEGO20, LACES20, GAUGE20, FRONT20, SAFE20, CLIMB20,
                 FOOTB20, FOG20, AMP20, BUGS20, MOP20, FANNY20, TREAD20, SLEUTH20, FICUS20, CANDY20, SHAKE20, SCOPE20,
                 EXIT20, MOUTH20, CHAIR20, SLASH20, BFF20]

    for ps in SET10_82:                                       # file 82's emitters sit at built-in offsets (res 3
        b = bytearray(out[ps])                                #  ~40 px up): set 10 places everything itself
        rs = spa.resources(bytes(b))
        for res in range(len(rs)):
            no_offset(b, rs, res)
        out[ps] = bytes(b)
    for ps in range(BOX17, LAST_KIT + 1):                     # set 17: every emitter square and on time (file 82's
        b = bytearray(out[ps])                                #  res 3 stretches its quad 1.4x and starts 6 frames
        for r in spa.resources(bytes(b)):                     #  late; 168's res 1 waits 10)
            struct.pack_into("<hH", b, r["off"] + 48, 0x1000, 0)
            b[r["off"] + TILE] &= 0x0F
            b[r["off"] + 76:r["off"] + 80] = bytes(4)          # polygon pivot offsets
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


# ------------------------------------------------------------------ set 13: Lugia's moves

def _air_force(side, s):
    """Aeroblast (Air Force): red alert, sirens - a squadron of fighter jets screams across the sky, contrails,
    a sonic boom - then from the heavens a GIANT crispy white sneaker descends... and STOMPS them flat. It lifts
    back up. Not a single crease. TING."""
    sx = 1 if side == "player" else -1
    bx, by = BATTLER_AT[side]
    red, night = rgb(120, 0, 0), rgb(0, 0, 40)
    w = []
    for k in range(3):                                                         # RED ALERT
        w += func(33, 0, 1, 0, 9, red) + se(s["alarm"]) + wait(5) + func(33, 0, 1, 9, 2, red) + wait(3)
    w += func(33, 0, 1, 2, 10, night)
    jet = JET_R if side == "player" else JET_L
    lanes = (40, 62, 28)                                                       # screen y of each jet
    for j, ly in enumerate(lanes):                                             # the squadron
        w += emit_at(JETS, jet, 0, (-sx * (bx + 40) if side == "player" else (256 - bx + 40), by - ly)) + se(s["jet"])
        w += wait(2)
    w += wait(6)
    for j, ly in enumerate(lanes):                                             # contrails left hanging
        w += emit_at(JETS, CONTRAIL13, 0, (128 - bx, by - ly)) + wait(1)
    w += wait(6)
    w += se(s["boom"]) + flash_screen(5) + func(68, 4, 3, 1, 3, 0) + wait(6)   # sonic boom
    foe = "enemy" if side == "player" else "player"
    top = BATTLER_AT[foe][1] + 30                                              # from above the top of the screen
    w += se(s["aeroblast"])
    w += stop_motion(KICK, POSE, 1, (0, top), (0, 46), 7, ease=.8)             # ...it descends...
    w += emit_at(STOMPFX, GLINT13, 1, (sx * 20, 60))
    for k in range(4):
        w += emit_at(KICK, POSE, 1, (0, 46 + (k % 2) * 2)) + wait(1)
    w += stop_motion(KICK, POSE, 1, (0, 40), (0, 6), 2, ease=1)                # STOMP
    w += emit_at(KICK, HOLD, 1, (0, 6)) + se(s["kaboom"]) + flash_screen(10) + func(68, 8, 5, 1, 6, 0)
    w += emit_at(STOMPFX, RING13, 1, (0, -16)) + bmove(side, 264, 2, 0, -12) + func(48)
    w += func(34, 8, 0, 2, rgb(255, 255, 255), 14, 0) + shake_defender(5, 4) + wait(12)
    w += stop_motion(KICK, POSE, 1, (0, 8), (0, top), 5, ease=1.4)             # lifts off...
    w += emit_at(STOMPFX, GLINT13, 1, (sx * 16, 70)) + se(s["bling"])          # TING. spotless.
    w += bmove(side, 264, 6, 0, 12) + wait(10) + func(33, 0, 1, 10, 0, night) + wait(6)
    return w


def _sixth_sense(side, s):
    """Extrasensory (Sixth Sense): the whole sky goes cosmic - a giant eye opens up there, looks around... locks
    on - a crystal ball swirls beside them (it shows the foe's future: a tombstone) - Death cards fly - and the
    eye blasts them with psychic rings."""
    sx = 1 if side == "player" else -1
    eye = EYE13_AT[side]
    look = EYE_R if side == "player" else EYE_L
    away = EYE_L if side == "player" else EYE_R
    cosmic = rgb(40, 0, 70)
    w = func(33, 0, 1, 0, 14, cosmic) + emit_at(SKYEYE, STARS13, 0, (eye[0], eye[1] - 30)) + se(s["xsense"])
    for k in range(6):                                                         # ...something's up there...
        w += emit_at(SKYEYE, EYE_SHUT, 0, eye) + func(68, 1, 1, 1, 1, 0) + wait(1)
    w += se(s["leer"]) + flash_screen(3)                                       # IT OPENS
    for k, res in enumerate((away, away, look, away, look, look, look, look)): # looking around... found you
        w += emit_at(SKYEYE, res, 0, eye) + wait(1)
    w += emit_at(CRYSTAL, BALL13, 0, BALL13_AT[side]) + emit_at(CRYSTAL, SWIRL13, 0, BALL13_AT[side])
    for k in range(5):
        w += emit_at(SKYEYE, look, 0, eye) + wait(1)
    w += emit_at(CRYSTAL, CARDS_E if side == "player" else CARDS_P, 0, BALL13_AT[side]) + se(s["slash"])
    for k in range(10):                                                        # the cards hit - then the rings
        w += emit_at(SKYEYE, look, 0, eye)
        if k in (3, 5, 7):
            w += se(s["slash"]) + shake_defender(2, 1)
        if k == 4:
            w += emit_at(COSMOS, 0 if side == "player" else 1, 0, eye) + se(s["xsense2"])
        w += wait(1)
    for k in range(8):                                                         # psychic overload
        w += emit_at(SKYEYE, look, 0, eye)
        w += func(34, 8, 0, 1, rgb(240, 80, 220) if k % 2 == 0 else rgb(0, 0, 0), 14, 0) + func(36, 2, 1, 1, 1, 264)
        w += wait(1)
    w += func(34, 8, 0, 1, rgb(240, 80, 220), 14, 0) + func(48) + flash_screen(4)
    for k in range(4):
        w += emit_at(SKYEYE, EYE_SHUT, 0, eye) + wait(1)
    w += func(33, 0, 1, 14, 0, cosmic) + wait(8)
    return w


# ------------------------------------------------------------------ set 14

def _gold_grill(side, s):
    """Hyper Fang (Gold Grill): gold wind-up chattering teeth - wound up, set down - clack clack clack across
    the floor, and CHOMP. On their ankle. Hanging on. Till the foe kicks them off."""
    sx = 1 if side == "player" else -1
    kitps = TEETHR if side == "player" else TEETHL
    dx, dy = TARGET_FROM_ATTACKER[side]
    start = (sx * 22, -6) if side == "player" else (sx * 22, -4)
    end = (dx - sx * 22, dy + 2)                                               # (their leg, clear of the HP box)
    w = []
    for k in range(4):                                                         # *wind wind wind*
        w += emit_at(kitps, TEETH_SHUT, 0, (start[0], start[1] + (k % 2))) + se(s["disable"]) + wait(2)
    for k in range(10):                                                        # clack clack clack across
        t = (k + 1) / 10
        x, y = round(start[0] + (end[0] - start[0]) * t), round(start[1] + (end[1] - start[1]) * t + (k % 2) * 3)
        w += emit_at(kitps, TEETH_OPEN if k % 2 == 0 else TEETH_SHUT, 0, (x, y))
        if k % 2:
            w += se(s["bite"])
        w += wait(1)
    for k in range(6):                                                         # CHOMP. hanging on.
        w += emit_at(kitps, TEETH_SHUT if k % 2 == 0 else TEETH_OPEN, 1, (sx * -18, 2 + (k % 2) * 2))
        if k == 0:
            w += emit_at(kitps, CHOMPFX, 1, (sx * -14, 6)) + se(s["hfang"]) + flash_screen(3) + bmove(side, 264, 2, 0, 10)
        if k == 2:
            w += bmove(side, 264, 3, 0, -10) + shake_defender(3, 3)
        w += wait(1)
    w += bmove(side, 264, 2, sx * 6, 0) + se(s["whoosh"])                     # *kick*
    for k in range(6):                                                         # flung off, tumbling away
        w += emit_at(kitps, TEETH_OPEN if k % 2 else TEETH_SHUT, 1, (sx * (-18 - k * 10), 2 + 8 * k - 2 * k * k)) + wait(1)
    w += bmove(side, 264, 3, -sx * 6, 0)
    return w + wait(10)


def _air_it_out(side, s):
    """Haze (Air It Out): fog all over the field - they whip a dish towel round like they're airing out the
    bathroom - then psssht the air freshener - and it's all fresh."""
    sx = 1 if side == "player" else -1
    w = emit_at(HAZEFOG, FOG14, 0, (sx * 30, 30)) + emit_at(HAZEFOG, FOG14, 1, (0, 20)) + se(s["haze"]) + wait(10)
    for k in range(10):                                                        # whip whip whip
        w += emit_at(TOWELS, TOWEL_A if k % 2 == 0 else TOWEL_B, 0, (sx * 26, 46 + (k % 2) * 4))
        if k % 2 == 0:
            w += se(s["whoosh"])
        w += wait(1)
    w += emit_at(TOWELS, SPRAYCAN, 0, (sx * 30, 38)) + wait(4)
    for k in range(2):                                                         # psssssht
        w += emit_at(TOWELS, FRESH, 0, (sx * 30, 52)) + se(s["sscent"]) + wait(5)
    w += emit_at(HAZEFOG, FRESHGLINT, 0, (sx * 30, 40)) + emit_at(HAZEFOG, FRESHGLINT, 1, (0, 30))
    w += func(34, 8, 0, 1, rgb(255, 255, 255), 12, 0) + func(34, 2, 0, 1, rgb(255, 255, 255), 12, 0) + se(s["bling"])
    return w + wait(16)


def _barricade(side, s):
    """Barrier (Barricade): a couch shoved in front of them - THUD - a mattress - THUD - a dresser on top -
    THUD. Barricaded. They peek out over it."""
    sx = 1 if side == "player" else -1
    base = (sx * 30, 4)
    w = []
    for res, frm, at in ((COUCH1, (sx * 90, 4), base), (MATTRESS1, (sx * 30, 100), (sx * 36, 30)),
                         (DRESSER1, (sx * 30, 110), (sx * 24, 42))):
        w += stop_motion(FURNITURE, res, 0, frm, at, 4)
        w += emit_at(FURNITURE, DUST14, 0, (at[0], at[1] - 14)) + se(s["bonk"]) + func(68, 2, 2, 1, 2, 0)
        hold = [(COUCH1, base), (MATTRESS1, (sx * 36, 30)), (DRESSER1, (sx * 24, 42))]
        for k in range(3):                                                     # (everything stays put)
            for r, p in hold:
                if r == res or [h[0] for h in hold].index(r) < [h[0] for h in hold].index(res):
                    w += emit_at(FURNITURE, r, 0, p)
            w += wait(1)
    for k in range(8):                                                         # barricaded in
        for r, p in ((COUCH1, base), (MATTRESS1, (sx * 36, 30)), (DRESSER1, (sx * 24, 42))):
            w += emit_at(FURNITURE, r, 0, p)
        if k == 2:
            w += se(s["barrier"]) + func(34, 2, 0, 1, rgb(110, 160, 255), 12, 0)
        w += wait(1)
    return w + wait(4)


def _zen_dome(side, s):
    """Zen Headbutt (Zen Dome): the singing bowl - DINNNG - om rings pulsing, incense smoke, they glow and float
    up... then snap - a full-speed headbutt."""
    sx = 1 if side == "player" else -1
    bowl = (sx * 40, 22) if side == "player" else (sx * 40, 10)                # (clear of the message box)
    w = emit_at(ZEN, BOWL, 0, bowl) + emit_at(ZENFX, INCENSE, 0, (bowl[0] + sx * 14, bowl[1] + 14)) + wait(4)
    for k in range(3):                                                         # DINNNNG
        w += emit_at(ZEN, OMRING, 0, (0, 20)) + se(s["zen"]) + func(34, 2, 0, 1, rgb(200, 140, 255), 10 + k, 0)
        w += wait(7)
    w += bmove(side, 258, 8, 0, 10) + wait(8)                                  # levitating...
    w += bmove(side, 258, 4, 72, 26) + se(s["whoosh"]) + wait(4)                # HEADBUTT
    w += emit_at(ZENFX, ZENHIT, 1, (sx * -8, 30)) + se(s["zen2"]) + flash_screen(5) + func(48) + shake_defender(5, 3)
    w += func(34, 8, 0, 1, rgb(220, 120, 255), 13, 0) + wait(10)
    w += bmove(side, 258, 8, -72, -36) + wait(8)
    return w


def _freeloader(side, s):
    """Leech Seed (Freeloader): the freeloading cousin hops over and plants himself right on top of them - feet
    up, soda in hand, comfy - and their HP starts siphoning back."""
    sx = 1 if side == "player" else -1
    dx, dy = TARGET_FROM_ATTACKER[side]
    head = (sx * -4, 46) if side == "player" else (sx * -4, 54)
    w = se(s["whoosh"])
    for k in range(6):                                                         # *hop*
        t = (k + 1) / 6
        x = round(-dx + (head[0] + dx) * t)
        y = round(-dy + 30 + (head[1] - (-dy + 30)) * t + 40 * t * (1 - t) * 4 / 4)
        w += emit_at(COUSIN, POSE, 1, (x, y)) + wait(1)
    w += emit_at(COUSIN, HOLD, 1, head) + se(s["bonk"]) + shake_defender(2, 2) + wait(6)
    w += se(s["lseed"]) + emit_at(LEECHFX, DRAIN14_E if side == "player" else DRAIN14_P, 1, (0, 20))
    w += func(34, 8, 0, 1, rgb(80, 200, 60), 12, 0) + wait_frames(18)
    for k in range(3):                                                         # (and the user's HP goes up)
        w += func(34, 2, 0, 1, rgb(120, 255, 120), 11, 0) + wait(5)
    return w + wait(8)


def _drip_check(side, s):
    """Swagger (Drip Check): a full-length mirror pops up - pose. pose. POSE. - price tags flying, the drip
    sparkling everywhere - and the foe gets dizzy just looking at it."""
    sx = 1 if side == "player" else -1
    mir = (sx * -36, 22)
    w = emit_at(MIRROR, MIRROR1, 0, mir) + emit_at(DRIPFX, DRIPSPARK, 0, (0, 24)) + wait(6)
    for k in range(3):                                                         # pose... pose... POSE
        w += bmove(side, 258, 2, sx * (4 if k % 2 == 0 else -4), 0) + emit_at(MIRROR, TWINKLE14, 0, (mir[0], mir[1] + 20))
        w += se(s["swagger"] if k == 2 else s["bling"]) + func(34, 2, 0, 1, rgb(255, 240, 160), 12, 0) + wait(7)
    w += emit_at(MIRROR, TAGS, 0, (0, 30)) + se(s["chaching"]) + wait(10)
    w += emit_at(DRIPFX, DIZZY14, 1, (0, 50)) + se(s["confuse"]) + func(34, 8, 0, 1, rgb(255, 80, 80), 12, 0)
    for k in range(4):                                                         # dizzy
        w += bmove(side, 264, 3, 4 if k % 2 == 0 else -4, 0) + wait(4)
    return w + wait(10)


def _yell_woop(side, s):
    """Roar (Yell Woop): a police light starts spinning on their head - red, blue, red, blue - WOOP WOOP - the
    foe takes one look and runs for it."""
    sx = 1 if side == "player" else -1
    head = (0, 52) if side == "player" else (0, 44)
    w = []
    for k in range(14):                                                        # WOOP WOOP
        red = k % 2 == 0
        w += emit_at(SIREN, LIGHT_RED if red else LIGHT_BLUE, 0, head)
        w += func(33, 0, 1, 0, 4, rgb(200, 0, 0) if red else rgb(0, 40, 220))
        if k == 1:
            w += emit_at(SIREN, WOOP_E if side == "player" else WOOP_P, 0, head) + se(s["alarm"])
        if k == 5:
            w += emit_at(WOOP, POP, 0, _self_sign(side))
        if k == 8:
            w += se(s["whoosh"]) + bmove(side, 264, 8, sx * 120, sx * 30)         # RUN
        w += wait(1)
    w += func(33, 0, 1, 4, 0, rgb(0, 40, 220)) + wait(6)
    w += bmove(side, 264, 8, -sx * 120, -sx * 30) + wait(8)
    return w


def _security(side, s):
    """Safeguard (Security): a SECURITY bouncer steps up beside them, arms crossed - the velvet rope goes up -
    a status bubble floats over... BONK, turned away at the rope."""
    sx = 1 if side == "player" else -1
    w = emit_at(SECURITY1, POP, 0, (sx * -36, 26)) + se(s["bonk"]) + wait(6)
    w += emit_at(SECURITY1, 1, 0, (sx * 32, 4)) + se(s["safeguard"]) + wait(8)
    dx, dy = TARGET_FROM_ATTACKER[side]
    for k in range(6):                                                         # here comes trouble...
        t = k / 5
        w += emit_at(BUBBLES14, STATUSBUB, 0, (round(dx + (sx * 40 - dx) * t), round(dy + (20 - dy) * t))) + wait(1)
    w += emit_at(BUBBLES14, NOPE14, 0, (sx * 40, 20)) + se(s["bonk"]) + flash_screen(2)   # ...not tonight.
    for k in range(5):
        t = k / 4
        w += emit_at(BUBBLES14, STATUSBUB, 0, (round(sx * 40 + (dx - sx * 40) * t), round(20 + (dy + 40 - 20) * t))) + wait(1)
    w += func(34, 2, 0, 1, rgb(140, 220, 255), 12, 0) + wait(16)
    return w


def _wax_on(side, s):
    """Rock Polish (Wax On): full car detail - an orbital buffer going round and round all over them, wax
    swirls, sparkle, sparkle - then they zoom."""
    sx = 1 if side == "player" else -1
    w = se(s["rpolish"])
    for k in range(12):                                                        # wax on...
        a = k * 2 * math.pi / 6
        x, y = round(14 * math.cos(a)), round(24 + 12 * math.sin(a))
        w += emit_at(BUFFER, BUFF_A if k % 2 == 0 else BUFF_B, 0, (x, y))
        if k % 3 == 0:
            w += emit_at(BUFFER, SWIRLS14, 0, (x, y - 6))
        w += wait(1)
    w += emit_at(SHINE14, SHINE_UP, 0, (0, 24)) + se(s["bling"]) + func(34, 2, 0, 1, rgb(255, 255, 255), 14, 0) + wait(8)
    for k, d in enumerate((1, -1, -1, 1)):                                     # ...ZOOM
        w += bmove(side, 258, 2, d * 22, 0) + emit_at(SHINE14, SPEED14, 0, (-d * 18, 14)) + wait(1)
    return w + wait(10)


def _beef(side, s):
    """Rage (Beef): steam pouring out of their ears... then they start some BEEF: a giant raw T-bone steak,
    slapped right across the foe. Twice."""
    sx = 1 if side == "player" else -1
    w = []
    for k in range(3):                                                         # fuming
        w += emit_at(STEAMFX, STEAMPUFF, 0, (sx * (6 - 12 * (k % 2)), 50)) + se(s["rage"])
        w += func(34, 2, 0, 1, rgb(255, 60, 40), 12, 0) + shake_attacker(1, 2) + wait(5)
    for k in range(2):                                                         # SLAP. SLAP.
        frm = (sx * -70, 30) if k == 0 else (sx * 50, 30)
        w += stop_motion(STEAK, POSE, 1, frm, (0, 26), 3, ease=1)
        w += emit_at(STEAK, HOLD, 1, (0, 26)) + emit_at(STEAMFX, MEATHIT, 1, (0, 26)) + se(s["splat"]) + se(s["bonk"])
        w += flash_screen(3) + shake_defender(4, 3) + func(34, 8, 0, 1, rgb(255, 80, 80), 12, 0) + wait(6)
    w += func(48) + wait(10)
    return w


def _big_bass(side, s):
    """Magnitude (Big Bass): a GIANT largemouth bass drops out of the sky into the middle of the field and
    flops - SLAM - SLAM - SLAM - the whole block shakes. Everybody gets it."""
    dx, dy = TARGET_FROM_ATTACKER[side]
    mid = (dx // 2, dy // 2 + 30)
    w = stop_motion(BASSFISH, FLOP_A, 0, (mid[0], mid[1] + 110), mid, 4) + se(s["whoosh"])
    for k in range(6):                                                         # FLOP. FLOP. FLOP.
        w += emit_at(BASSFISH, FLOP_A if k % 2 == 0 else FLOP_B, 0, (mid[0], mid[1] + (0 if k % 2 else 6)))
        if k % 2 == 1:
            w += emit_at(BASSFISH, SHOCK16, 0, (mid[0], mid[1] - 24)) + se(s["bass"]) + func(68, 3, 4, 1, 3, 0)
            w += shake_defender(3, 2) + shake_attacker(2, 2)
        if k == 3:
            w += emit_at(BASSFX, 0, 0, (mid[0], mid[1] - 10)) + se(s["splash"])
        w += wait(2)
    for k in range(4):
        w += emit_at(BASSFISH, FLOP_B, 0, (mid[0], mid[1] + k * 26)) + wait(1)
    w += func(48) + wait(8)
    return w


def _ice_chip(side, s):
    """Ice Shard (Ice Chip): a styrofoam cup of ice - flick, flick, flick - ice cubes pinging off them. Fast."""
    sx = 1 if side == "player" else -1
    w = emit_at(ICECUP, CUP16, 0, ICECUP_AT[side]) + wait(4)
    for k in range(3):                                                         # flick flick flick
        w += emit_at(ICECUP, ICE_E if side == "player" else ICE_P, 0, (ICECUP_AT[side][0], ICECUP_AT[side][1] + 10))
        w += se(s["ishard"]) + shake_attacker(1, 1) + wait(2)
        w += emit_at(ICEHIT, 0, 1, (sx * (-6 + k * 6), 24 - k * 6)) + se(s["bling"]) + shake_defender(1, 1) + wait(2)
    w += func(34, 8, 0, 1, rgb(150, 220, 255), 12, 0) + wait(8)
    return w


def _get_even(side, s):
    """Revenge (Get Even): out comes THE LIST - flip it open - their name, circled, X'd out - and the whole book
    flies over and SLAMS shut right on them."""
    sx = 1 if side == "player" else -1
    at = (sx * 34, 36) if side == "player" else (sx * 34, 30)
    w = []
    for k in range(5):                                                         # THE LIST
        w += emit_at(LISTBOOK, POP, 0, at) + wait(1)
    w += se(s["sshot"])
    for k in range(10):                                                        # *scribble scribble* ...X
        w += emit_at(LISTBOOK, 1, 0, at)
        if k in (3, 6):
            w += se(s["swipe"]) + shake_attacker(1, 1)
        w += wait(1)
    dx, dy = TARGET_FROM_ATTACKER[side]
    w += stop_motion(LISTBOOK, POP, 1, (at[0] - dx, at[1] - dy), (sx * -4, 26), 4, ease=1)
    w += emit_at(LISTBOOK, POP, 1, (sx * -4, 26)) + emit_at(LISTFX, 0, 1, (sx * -4, 26)) + se(s["revenge"])
    w += se(s["bonk"]) + flash_screen(4) + func(48) + shake_defender(5, 3)
    for k in range(3):
        w += emit_at(LISTBOOK, POP, 1, (sx * -4, 26)) + wait(1)
    return w + wait(8)


def _car_magnet(side, s):
    """Magnet Bomb (Car Magnet): a giant horseshoe magnet - the foe gets dragged in - hubcaps come flying in from
    everywhere and pile onto them - then it all goes off."""
    sx = 1 if side == "player" else -1
    at = (sx * 30, 26)
    w = emit_at(MAGNET14, MAG_R if side == "player" else MAG_L, 0, at) + se(s["mbomb2"]) + wait(4)
    w += bmove(side, 264, 12, -sx * 18, -sx * 8)                              # *VMMMM* dragged in
    for k in range(6):
        w += emit_at(MAGNET14, PULL16, 0, (at[0] + sx * 28, at[1])) + wait(2)
    for k, (fx, fy) in enumerate(((-90, 60), (60, 80), (90, -20))):            # hubcaps flying in
        for j in range(4):
            t = (j + 1) / 4
            w += emit_at(MAGNET14, HUBCAP16, 1, (round(fx * (1 - t)), round(20 + (fy - 20) * (1 - t)))) + wait(0)
        w += se(s["bonk"]) + shake_defender(1, 1)
    w += se(s["kaboom"]) + flash_screen(8) + func(68, 6, 4, 1, 4, 0) + func(48)  # BOOM
    w += func(34, 8, 0, 1, rgb(255, 140, 40), 14, 0) + shake_defender(5, 3) + wait(10)
    w += bmove(side, 264, 8, sx * 18, sx * 8) + wait(8)
    return w


def _one_two(side, s):
    """Double Hit (One-Two, once per hit - quick): DING DING - and a red boxing glove pops them."""
    sx = 1 if side == "player" else -1
    bell = (sx * 10, 68 if side == "player" else 66)                          # (over the foe, clear of the HP boxes)
    w = []
    for k in range(4):                                                         # DING DING
        w += emit_at(BELL14, POP, 1, (bell[0] + (k % 2) * 2, bell[1])) + wait(1)
        if k in (0, 2):
            w += se(s["bling"])
    glove = GLOVE_R if side == "player" else GLOVE_L
    w += stop_motion(GLOVES, glove, 1, (sx * -70, 24), (sx * -16, 22), 3, ease=1)
    w += emit_at(GLOVES, glove, 1, (sx * -14, 22)) + emit_at(GLOVES, PUNCH16, 1, (sx * 4, 22)) + se(s["bonk"])
    w += flash_screen(2) + shake_defender(3, 2) + wait(1)
    w += stop_motion(GLOVES, glove, 1, (sx * -20, 22), (sx * -60, 24), 2, ease=1)
    return w + wait(6)


def _power_bank(side, s):
    """Charge Beam (Power Bank): the phone's on 1%... plugged into the power bank... 50%... 100% - FULL BATTERY -
    and it fires a beam right at them."""
    sx = 1 if side == "player" else -1
    at = PHONE16_AT[side]
    w = emit_at(BANK16, POP, 0, (at[0] - sx * 34, at[1] - 30)) + wait(2)
    for res, n in ((BATT_LOW, 6), (BATT_HALF, 6), (BATT_FULL, 4)):            # charging...
        for k in range(n):
            w += emit_at(PHONE16, res, 0, at)
            if k == 0:
                w += se(s["cbeam"]) + emit_at(PHONE16, ZAPS16, 0, (at[0], at[1] - 18))
            w += wait(1)
    w += se(s["bling"]) + func(34, 2, 0, 1, rgb(120, 255, 120), 12, 0)
    for k in range(10):                                                        # 100% - FIRE
        w += emit_at(PHONE16, BATT_FULL, 0, at)
        if k == 1:
            w += emit_at(BEAM16, 0 if side == "player" else 1, 0, at) + se(s["cbeam2"])
        if k >= 5:
            w += func(34, 8, 0, 1, rgb(150, 255, 200), 12, 0) + func(36, 1, 0, 1, 1, 264)
        w += wait(1)
    return w + wait(8)


def _duck_down(side, s):
    """Minimize (Duck Down): a round clothing rack slides in and they duck right into it - the shirts rustle...
    two little eyes peek out."""
    sx = 1 if side == "player" else -1
    at = (0, 18) if side == "player" else (0, 14)
    w = stop_motion(RACK, RACK1, 0, (sx * -80, at[1]), at, 4)
    w += bmove(side, 258, 4, 0, -16) + se(s["minimize"])                       # *ducks in*
    for k in range(14):
        if k >= 7 and k not in (10, 11):                                       # (blink) - emitted first: drawn
            w += emit_at(RACK, PEEK, 0, (sx * 4, at[1] + 2))                   #  over the rack
        w += emit_at(RACK, RACK1, 0, (at[0] + (1 if k < 4 and k % 2 else 0), at[1]))
        if k < 4 and k % 2 == 0:
            w += emit_at(RACK, RUSTLE, 0, (sx * 14, at[1] + 14)) + se(s["sand"])
        w += wait(1)
    w += bmove(side, 258, 6, 0, 16) + wait(6)
    return w


def _brain_freeze(side, s):
    """Ice Fang (Brain Freeze): a giant slushie, chugged way too fast - BRAIN FREEZE - icicles, shivering - and
    then jaws of ice CHOMP down on the foe."""
    sx = 1 if side == "player" else -1
    mouth = MOUTH_AT[side]
    w = emit_at(SLUSH, CUP_SLUSH, 0, (mouth[0] + sx * 14, mouth[1] - 6)) + wait(4)
    for k in range(3):                                                         # *SLUUURP*
        w += se(s["bubble"]) + shake_attacker(1, 2) + wait(4)
    w += emit_at(SLUSH, ICICLES, 0, (0, 40)) + se(s["ifang"]) + flash_screen(2)   # BRAIN FREEZE
    for k in range(4):
        w += func(34, 2, 0, 1, rgb(120, 200, 255), 14, 0) + func(36, 2, 0, 1, 1, 258) + wait(3)
    for k in range(4):                                                         # ...then the jaws
        w += emit_at(JAWS16, JAWS_OPEN, 1, (0, 30 + k)) + wait(1)
    w += emit_at(JAWS16, JAWS_SHUT, 1, (0, 26)) + emit_at(JAWS16, FROST16, 1, (0, 26)) + se(s["bite"]) + se(s["crunch"])
    w += flash_screen(3) + shake_defender(4, 3) + func(34, 8, 0, 1, rgb(150, 220, 255), 14, 0) + func(48)
    return w + wait(12)


def _lock_on(side, s):
    """Lock-On (Lock On): binoculars up to their eyes - a red reticle slides around the foe... drifting...
    settling - *click* - LOCKED, flashing red."""
    sx = 1 if side == "player" else -1
    eyes = (sx * 16, 40) if side == "player" else (sx * 16, 30)
    w = emit_at(BINOC, POP, 0, eyes) + se(s["lockon"]) + wait(4)
    for k, (x, y) in enumerate(((-30, 40), (24, 30), (-14, 10), (10, 28), (-4, 18), (2, 22), (0, 20), (0, 20))):
        w += emit_at(BINOC, 1, 1, (x, y)) + wait(2)                             # hunting... settling
        if k in (2, 4, 6):
            w += se(s["disable"])
    w += se(s["lockon2"])
    for k in range(8):                                                         # LOCKED (blinking red)
        if k % 2 == 0:
            w += emit_at(BINOC, 1, 1, (0, 20))
        w += func(34, 8, 0, 1, rgb(255, 40, 40), 12, 0) if k == 1 else []
        w += wait(2)
    return w + wait(4)


def _night_shank(side, s):
    """Night Slash (Night Shank): lights out - pitch black - just two glowing eyes - shink. shink. shink. - the
    flashlight clicks on: fresh slash marks across the foe... and the attacker, whistling."""
    sx = 1 if side == "player" else -1
    head = (0, 34) if side == "player" else (0, 28)
    black = rgb(0, 0, 0)
    w = func(33, 0, 1, 0, 16, black) + func(34, 8, 0, 2, black, 15, 0) + func(34, 2, 0, 2, black, 15, 0) + se(s["faint"])
    for k in range(6):                                                         # ...two eyes
        w += emit_at(NIGHT16, EYES16, 0, head) + wait(1)
    for k in range(3):                                                         # shink. shink. SHINK.
        w += flash_screen(1) + se(s["slash"]) + wait(3)
    w += emit_at(NIGHT16, TORCH16, 0, (sx * 60, 24)) + se(s["disable"])         # *click*
    w += func(33, 0, 1, 16, 8, black) + emit_at(NIGHT16, SLASHES16, 1, (0, 22)) + shake_defender(4, 3)
    w += func(34, 8, 0, 1, rgb(255, 60, 60), 13, 0) + wait(6)
    w += emit_at(NIGHT16, NOTES16, 0, (sx * 14, 46)) + wait(14)                 # *whistling*
    w += func(33, 0, 1, 8, 0, black) + wait(6)
    return w


def _got_ya_back(side, s):
    """Helping Hand (Got Ya Back): the secret handshake - SLAP - hook the fingers - slide - fist bump -
    EXPLODE - and a gold glow goes up off them."""
    sx = 1 if side == "player" else -1
    at = (sx * 34, 64) if side == "player" else (sx * 30, 50)
    w = []
    for res, n, sound in ((HAND_SLAP, 4, "dslap"), (HAND_HOOK, 4, "swipe"), (HAND_SLAP, 3, "dslap"),
                          (HAND_BUMP, 5, "bonk")):
        for k in range(n):
            w += emit_at(SHAKE, res, 0, (at[0] + (k % 2), at[1]))
            if k == 0:
                w += se(s[sound])
            w += wait(1)
    w += emit_at(SHAKEFX, 0, 0, at) + emit_at(SHAKEFX, 1, 0, at) + se(s["bling"]) + flash_screen(3)   # EXPLODE
    w += emit_at(SHAKE, GOLDUP, 0, (0, 20)) + se(s["hhand"])
    for k in range(3):
        w += func(34, 2, 0, 1, rgb(255, 220, 60), 13, 0) + wait(5)
    return w + wait(6)


def _ice_out(side, s):
    """Ice Beam (Ice Out): a stream of diamonds blasts them - and they get ICED OUT: frozen solid in a block of
    ice, encrusted with diamonds. Sparkling."""
    sx = 1 if side == "player" else -1
    w = emit_at(DIAMONDS, DIAM_E if side == "player" else DIAM_P, 0, (sx * 22, 28)) + se(s["chaching"])
    w += wait_frames(12) + se(s["bling"])
    for k in range(4):
        w += func(34, 2, 0, 2, rgb(180, 230, 255), 10 + k, 0) + func(36, 1, 0, 1, 1, 264) + wait(3)
    w += emit_at(ICEBLOCK, POP, 1, (0, 20)) + se(s["ishard"]) + flash_screen(4)   # *KRRSSH* frozen
    w += func(34, 8, 0, 2, rgb(170, 220, 255), 15, 0) + wait(4)
    for k in range(3):                                                         # (bling bling)
        w += se(s["bling"]) + wait(5)
    return w + wait(8)


def _stone_cold(side, s):
    """Stone Edge (Stone Cold): shades on - slow - deadpan - and massive rock spikes burst up out of the ground
    under the foe, one, two, three."""
    sx = 1 if side == "player" else -1
    face = (0, 34) if side == "player" else (0, 26)
    w = stop_motion(COLDSHADES, SHADES16, 0, (face[0], face[1] + 30), face, 6, ease=.6)   # *slowly*
    for k in range(4):
        w += emit_at(COLDSHADES, SHADES16, 0, face) + wait(1)
    feet = (0, -16) if side == "player" else (0, 0)
    for k, (res, dx) in enumerate(((SPIKE_A, 0), (SPIKE_B, sx * -26), (SPIKE_C, sx * 24))):   # BOOM BOOM BOOM
        w += emit_at(COLDSHADES, SHADES16, 0, face)
        w += emit_at(SPIKES, res, 1, (feet[0] + dx, feet[1] + 18 - k * 4)) + emit_at(SPIKES, 0, 1, (feet[0] + dx, feet[1]))
        w += se(s["sedge"]) + func(68, 3, 3, 1, 2, 0) + shake_defender(3, 2) + wait(2)
        w += emit_at(COLDSHADES, SHADES16, 0, face) + wait(2)
    w += func(48) + flash_screen(3)
    for k in range(6):
        w += emit_at(COLDSHADES, SHADES16, 0, face) + wait(1)
    return w + wait(6)


def _rizz_up(side, s):
    """Attract (Rizz Up): a candlelit table for two pops up between them - spaghetti, a rose - hearts floating
    up, an eyebrow wiggle - and the foe swoons. Hearts bursting."""
    sx = 1 if side == "player" else -1
    dx, dy = TARGET_FROM_ATTACKER[side]
    table = (30, 34) if side == "player" else (-50, -20)                      # (clear of the HP boxes)
    w = emit_at(DATE, DATE1, 0, table) + se(s["attract"]) + wait(6)
    w += emit_at(HEARTS16, 0, 0, (table[0], table[1] + 16)) + wait(6)
    for k in range(2):                                                         # *eyebrow wiggle*
        w += bmove(side, 258, 2, 0, 3) + wait(2) + bmove(side, 258, 2, 0, -3) + wait(2)
    w += emit_at(HEARTS16, 1, 1, (0, 30)) + se(s["loyal"]) + func(34, 8, 0, 2, rgb(255, 100, 170), 13, 0)
    for k in range(3):                                                         # *swoon*
        w += bmove(side, 264, 4, sx * 4, -sx * 2) + wait(4) + bmove(side, 264, 4, -sx * 4, sx * 2) + wait(4)
    return w + wait(8)


def _pickup_line(side, s):
    """Captivate (Pickup Line): a smooth speech bubble - "U FROM TENNESSEE?" - (because you the only ten I
    see) - and the foe blushes bright red."""
    sx = 1 if side == "player" else -1
    w = emit_at(PICKUP, POP, 0, (sx * 34, 60 if side == "player" else 52)) + se(s["captivate"]) + wait(16)
    w += emit_at(BLUSH, 0, 1, (0, 30)) + se(s["loyal"])
    for k in range(4):                                                         # *blushing*
        w += func(34, 8, 0, 1, rgb(255, 60, 100), 14, 0) + func(36, 1, 0, 1, 1, 264) + wait(4)
    return w + wait(8)


def _ice_cold(side, s):
    """Icy Wind (Ice Cold): a window AC unit cranked all the way to MAX, rattling - a blast of snowflakes -
    the foe shivers, frosted over."""
    sx = 1 if side == "player" else -1
    at = (sx * -30, 30)
    w = []
    for k in range(6):                                                         # *rattle rattle*
        w += emit_at(ACUNIT, AC1, 0, (at[0] + (k % 2), at[1] + (k % 2))) + wait(1)
    w += emit_at(FLAKES, FLAKES_E if side == "player" else FLAKES_P, 0, at) + se(s["iwind"])
    for k in range(14):
        w += emit_at(ACUNIT, AC1, 0, (at[0] + (k % 2), at[1] + (k % 2)))
        if k >= 7:
            w += func(34, 8, 0, 1, rgb(160, 220, 255), 12, 0) + func(36, 1, 0, 1, 1, 264)
        w += wait(1)
    return w + wait(8)


def _ground_game(side, s):
    """Earth Power (Ground Game): the foe wanders onto a manhole cover... it starts rattling under them -
    clank... clank-clank... - then BLOWS: the cover rockets up on a geyser of sewer steam and launches them sky
    high. They land and stumble back."""
    sx = 1 if side == "player" else -1
    hole = (-36, -2) if side == "player" else (36, -6)                         # (in front of them, in the open)
    on = (-sx * 36, 10)                                                        # the foe's step onto it (screen px)
    w = []
    for k in range(4):                                                         # just a manhole...
        w += emit_at(POTHOLE1, HOLE1, 1, hole) + wait(1)
    w += bmove(side, 264, 8, *on)                                              # ...they step right onto it
    for k in range(8):
        w += emit_at(POTHOLE1, HOLE1, 1, hole) + wait(1)
    w += func(68, 2, 1, 1, 4, 0) + se(s["epower"])
    for k in range(10):                                                        # clank... clank-clank...
        jump = 3 if k in (2, 5, 6, 8, 9) else 0
        w += emit_at(POTHOLE1, HOLE1, 1, (hole[0], hole[1] + jump))
        if jump:
            w += se(s["bonk"]) + func(36, 1, 0, 1, 1, 264)
        w += wait(1)
    w += se(s["kaboom"]) + flash_screen(5) + func(68, 6, 4, 1, 4, 0)            # BOOM
    w += emit_at(CONES, CONE_A, 1, (hole[0], hole[1] + 6)) + emit_at(POTHOLE1, STEAMUP, 1, hole)
    w += bmove(side, 264, 4, 0, 34) + func(34, 8, 0, 1, rgb(200, 200, 160), 13, 0)   # LAUNCHED
    for k in range(6):
        w += emit_at(POTHOLE1, HOLE1, 1, hole) + wait(1)
    w += bmove(side, 264, 5, 0, -34)
    for k in range(5):
        w += emit_at(POTHOLE1, HOLE1, 1, hole) + wait(1)
    w += se(s["bonk"]) + shake_defender(4, 3) + func(48) + wait(6)
    w += bmove(side, 264, 8, -on[0], -on[1]) + wait(10)                        # stumbles back
    return w


def _tailgate(side, s):
    """Tailwind (Tailgate): a pickup backs in behind them, the tailgate drops - grill smoking, the cooler, a foam
    finger - and they're HYPED, zipping around."""
    sx = 1 if side == "player" else -1
    at = (-6, 18) if side == "player" else (40, 4)
    w = []
    for k in range(5):                                                         # backing up...
        w += emit_at(TAILGATE, GATE1, 0, (at[0] - sx * (40 - k * 10), at[1])) + wait(1)
    w += emit_at(TAILGATE, GATEPUFF, 0, (at[0] + sx * 6, at[1] + 10)) + se(s["bonk"]) + se(s["twind"])
    for k in range(14):
        w += emit_at(TAILGATE, GATE1, 0, at)
        if k in (4, 6, 8, 10):                                                 # zip zip zip
            d = 1 if k in (4, 10) else -1
            w += bmove(side, 258, 2, d * 22, 0) + emit_at(GRILLSMOKE, 0, 0, (-d * 18, 14))
        w += wait(1)
    return w + wait(6)


def _iced_out(side, s):
    """Blizzard (Iced Out): a shaved-ice machine goes haywire - shaking, cranking itself - and buries the whole
    block in snow."""
    sx = 1 if side == "player" else -1
    at = (sx * 30, 24)
    w = emit_at(SNOWMACH, MACH1, 0, at) + wait(4)
    for k in range(8):                                                         # it's going haywire
        w += emit_at(SNOWMACH, MACH1, 0, (at[0] + (2 if k % 2 else -2), at[1] + (k % 2) * 2))
        if k % 2 == 0:
            w += se(s["disable"])
        w += wait(1)
    w += func(33, 0, 1, 0, 8, rgb(200, 230, 255)) + se(s["blizzard"])
    dx, dy = TARGET_FROM_ATTACKER[side]
    w += emit_at(SNOWSTORM, STORM_A, 0, (dx // 2, dy // 2 + 70)) + emit_at(SNOWSTORM, STORM_B, 0, (dx // 2 + sx * 40, dy // 2 + 70))
    for k in range(16):                                                        # buried
        w += emit_at(SNOWMACH, MACH1, 0, (at[0] + (2 if k % 2 else -2), at[1]))
        if k >= 8:
            w += func(34, 8, 0, 1, rgb(220, 240, 255), 13, 0) + func(36, 1, 0, 1, 1, 264)
        w += wait(1)
    w += func(33, 0, 1, 8, 0, rgb(200, 230, 255)) + wait(6)
    return w


def _photo_op(side, s):
    """Synthesis (Photo Op): the ring light clicks on - pose - and a whole storm of paparazzi flashes - they
    glow all the way up (and heal)."""
    sx = 1 if side == "player" else -1
    w = emit_at(RINGLIGHT, RLIGHT, 0, (sx * 30, 32)) + emit_at(RINGLIGHT, RL_GLOW, 0, (0, 24)) + se(s["bling"]) + wait(6)
    for k in range(8):                                                         # *click* *click* *flash*
        w += emit_at(FLASHES, 0, 0, (sx * (40 - k * 9), 20 + (k * 13) % 30)) + se(s["disable"] if k % 2 else s["pop"])
        w += flash_screen(1) + wait(2)
    w += emit_at(FLASHES, 1, 0, (0, 20)) + se(s["absorb"])
    for k in range(4):                                                         # glowing up
        w += func(34, 2, 0, 1, rgb(255, 250, 180), 13, 0) + wait(5)
    return w + wait(6)


# ------------------------------------------------------------------ set 17: common moves

def _hold(ps, res, who, at, ticks, extra=lambda k: []):
    """Keep a life-4 prop up for `ticks` script ticks (re-emitted every tick); extra(k) adds words per tick."""
    w = []
    for k in range(ticks):
        w += emit_at(ps, res, who, at) + extra(k) + wait(1)
    return w


def _arc(frm, to, steps, height, ease=1.0):
    """Points along a lobbed arc from frm to to (screen px)."""
    pts = []
    for k in range(steps):
        t = (k / (steps - 1)) ** ease
        pts.append((round(frm[0] + (to[0] - frm[0]) * t),
                    round(frm[1] + (to[1] - frm[1]) * t + height * math.sin(math.pi * t))))
    return pts


def _box_cutter(side, s):
    """Cut (Box Cutter): a FRAGILE box drops over the foe, thud - the box cutter clicks out, click, click -
    slash, SLASH - and the box bursts open in a spray of packing peanuts, the foe dazed in the middle."""
    sx = 1 if side == "player" else -1
    box = (0, 14) if side == "player" else (0, 14)
    shut = lambda k: emit_at(BOX17, BOXSHUT, 1, box)
    w = se(s["whoosh"]) + stop_motion(BOX17, BOXSHUT, 1, (box[0], box[1] + 96), box, 5, ease=2.0)
    w += se(s["bonk"]) + func(68, 2, 2, 1, 2, 0) + shake_defender(2, 2) + _hold(BOX17, BOXSHUT, 1, box, 3)
    cut = (box[0] - sx * 50, box[1] + 4)
    out_, in_ = ((CUTTER17, CUTOUT_R), (CUTTER17, CUTIN_R)) if side == "player" else ((CUTTER17, CUTOUT_L), (CUTL17, CUTIN_L))
    for k, (ps, res) in enumerate((in_, in_, out_, in_, out_, out_, out_)):   # click... click-click... *click*
        w += shut(k) + emit_at(ps, res, 1, cut)
        if k in (2, 3, 4):
            w += se(s["disable"])
        if k == 4:
            w += emit_at(CUTTER17, CUTSPARK, 1, (cut[0] + sx * 20, cut[1] + 2))
        w += wait(1)
    for frm, to in (((-24, 26), (22, -18)), ((22, 26), (-24, -18))):            # slash... SLASH
        for k in range(3):
            t = k / 2
            at = (box[0] + sx * round(frm[0] + (to[0] - frm[0]) * t), box[1] + round(frm[1] + (to[1] - frm[1]) * t))
            w += shut(0) + emit_at(*out_, 1, at)
            if k == 1:
                w += se(s["slash"])
            w += wait(1)
        w += shut(0) + func(36, 1, 0, 1, 1, 264) + wait(1)
    w += emit_at(CUTL17, XCUT, 1, (box[0], box[1] + 4)) + shut(0) + se(s["slash"]) + wait(1)
    w += shut(0) + wait(1)
    w += emit_at(BOX17, PEANUTS, 1, (box[0], box[1] + 8)) + emit_at(BOX17, BOXOPEN, 1, box)   # POP
    w += se(s["pop"]) + se(s["bonk"]) + flash_screen(4) + shake_defender(3, 4) + func(48)
    w += wait(8) + shake_defender(1, 4) + wait(14)                             # dazed in the box
    return w


def _muscle(side, s):
    """Strength (Muscle): plates clank onto the bar - one, two, THREE - a shaky overhead press, sweat flying -
    and the whole barbell comes down on the foe. The little plates roll off."""
    head = (0, 80) if side == "player" else (0, 56)
    w = []
    for res in (BAR1, BAR2, BAR3):                                             # clank, clank, CLANK
        w += se(s["bonk"]) + func(36, 1, 0, 1, 1, 258) + _hold(BAR17, res, 0, head, 3)
    w += se(s["focus"]) + emit_at(BAR17, SWEAT17, 0, (0, 34))
    lift = round(RES3_DROP * 1.4)                                              # (BAR3 is res 3)
    for k in range(9):                                                         # nngh... NNNGH
        jit = (2 if k % 2 else -2) * (1 + k // 3)
        w += emit_at(BAR17, BAR3, 0, (head[0] + jit, head[1] + lift + k * 2))
        if k == 4:
            w += se(s["focus"])
        w += wait(1)
    dx, dy = TARGET_FROM_ATTACKER[side]
    for at in _arc((head[0], head[1] + lift + 18), (dx, dy + lift + 14), 6, 34, ease=1.3)[1:]:   # HEAVE
        w += emit_at(BAR17, BAR3, 0, at) + wait(1)
    w += se(s["bslam"]) + se(s["kaboom"]) + flash_screen(5) + func(68, 6, 4, 1, 4, 0)   # CRASH
    w += emit_at(PLATE17, SLAMPUFF, 1, (0, -4)) + shake_defender(4, 4) + func(48)
    w += emit_at(PLATE17, ROLL_R, 1, (16, -6)) + emit_at(PLATE17, ROLL_L, 1, (-16, -6))
    w += _hold(BAR17, BAR2, 1, (0, 10), 9, lambda k: se(s["bonk"]) if k in (2, 5) else [])
    return w + wait(4)


def _smash_n_grab(side, s):
    """Rock Smash (Smash n Grab): a glass jewelry case in front of the foe, iced out - the crowbar winds up...
    SMASH - glass everywhere - and the gold chain flies back to the attacker. Cha-ching."""
    sx = 1 if side == "player" else -1
    case = SMASH_CASE[side]
    crow = CROW_R if side == "player" else CROW_L
    w = se(s["bling"]) + _hold(CASE17, CASE1, 1, case, 4)
    for k in range(4):                                                         # winding up...
        w += emit_at(CASE17, CASE1, 1, case) + emit_at(CROW17, crow, 1, (case[0] - sx * (30 + k * 2), case[1] + 32 + k * 3))
        w += wait(1)
    for k, (x, y) in enumerate(((-22, 30), (-12, 20))):                        # ...swing
        w += emit_at(CASE17, CASE1, 1, case) + emit_at(CROW17, crow, 1, (case[0] + sx * x, case[1] + y)) + wait(1)
    w += emit_at(CASE17, SHARDS, 1, (case[0], case[1] + 12)) + emit_at(CASE17, CASEBROKE, 1, case)   # SMASH
    w += se(s["smash"]) + flash_screen(4) + func(68, 3, 3, 1, 2, 0)
    w += emit_at(CROW17, crow, 1, (case[0] - sx * 2, case[1] + 12))
    w += wait(2) + shake_defender(3, 3) + func(34, 8, 0, 1, rgb(180, 230, 255), 12, 0) + func(48)
    w += emit_at(LOOT17, CHAIN_E if side == "player" else CHAIN_P, 1, (case[0], case[1] + 14))    # the grab
    w += emit_at(LOOT17, LOOTSPARK, 1, (case[0], case[1] + 14)) + se(s["whoosh"])
    w += wait_frames(CHAIN_FRAMES) + se(s["chaching"]) + emit_at(LOOT17, LOOTSPARK, 0, (0, 20))
    w += func(34, 2, 0, 1, rgb(255, 220, 60), 12, 0) + wait(10)
    return w


def _lay_low(side, s):
    """Dig (Lay Low), two turns. Turn 1: the shovel goes to work - dirt flying - they hop in the hole and a road
    barricade goes up over it, light blinking. Turn 2: the ground rumbles under the foe... rumbles... and they
    ERUPT out of it, launching the foe."""
    sx = 1 if side == "player" else -1
    hole = DIG_HOLE[side]
    shovel = (hole[0] + sx * 4, hole[1] + 24)                                 # (stuck in the pile behind it)
    scene = lambda k: (emit_at(SHOVEL17, SHOVEL1, 0, shovel) + emit_at(SHOVEL17, HOLE17, 0, hole))
    one = []
    for k in range(3):                                                         # dig, dig, dig
        one += emit_at(SHOVEL17, SHOVEL1, 0, (shovel[0], shovel[1] + 6)) + wait(1)
        one += emit_at(SHOVEL17, SHOVEL1, 0, shovel) + emit_at(SHOVEL17, CLODS, 0, (hole[0], hole[1] + 4))
        one += se(s["sand"]) + wait(1)
    one += _hold(SHOVEL17, SHOVEL1, 0, shovel, 1) + se(s["bonk"]) + scene(0) + wait(1)
    one += bmove(side, 258, 6, hole[0], 14) + scene(0) + wait(1) + scene(0) + wait(1)   # hop...
    one += bmove(side, 258, 6, 0, -14 - 34) + scene(0) + wait(1) + scene(0) + wait(1)   # ...in
    one += func(40, 2, 1) + emit_at(SHOVEL17, CLODS, 0, (hole[0], hole[1] + 4))   # gone
    one += bmove(side, 258, 1, -hole[0], 34)
    for k in range(10):                                                        # the barricade goes up
        one += emit_at(SHOVEL17, BARRICADE, 0, (hole[0], hole[1] + 18 + max(0, 6 - k * 3))) + scene(0)
        if k == 2:
            one += se(s["bonk"])
        if k in (4, 7):
            one += se(s["disable"])
        one += wait(1)
    two = []
    for k, amp in enumerate((1, 2, 3)):                                        # rumble... rumble... RUMBLE
        two += func(68, 2, amp, 1, 3, 0) + emit_at(DIRT17, DUSTRING, 1, (0, -10)) + se(s["rollout"])
        two += shake_defender(amp, 2) + wait(6 - k)
    two += se(s["kaboom"]) + se(s["sand"]) + flash_screen(4) + func(68, 6, 4, 1, 4, 0)   # ERUPT
    two += emit_at(DIRT17, ERUPT, 1, (0, -8)) + emit_at(SHOVEL17, CLODS, 1, (0, -4)) + emit_at(SHOVEL17, CLODS, 1, (8, 4))
    two += bmove(side, 264, 4, 0, 34) + func(34, 8, 0, 1, rgb(170, 120, 70), 13, 0)
    for k in range(4):
        two += emit_at(SHOVEL17, HOLE17, 1, (0, -12)) + wait(1)
    two += func(40, 2, 0) + emit_at(DIRT17, DUSTRING, 0, (0, -6)) + emit_at(SHOVEL17, CLODS, 0, (0, -4))   # back
    two += bmove(side, 264, 5, 0, -34)
    for k in range(3):
        two += emit_at(SHOVEL17, HOLE17, 1, (0, -12)) + wait(1)
    two += se(s["bonk"]) + shake_defender(4, 3) + func(48) + wait(12)
    return one, two


def _lay_low_turn2_first(side, s):
    """Test only: Lay Low with the turns swapped, to see turn 2 in the showcase."""
    one, two = _lay_low(side, s)
    return two, one


def _hot_hands(side, s):
    """Fire Punch (Hot Hands): the glove goes on the stove's coil burner, cranked to HI - sizzling - FWOOSH, it
    catches fire - and the flaming glove goes right in their face. They hop around, smoking."""
    sx = 1 if side == "player" else -1
    stove = (36, 18) if side == "player" else (-54, 6)
    glove_on = (stove[0] - sx * 2, stove[1] + 16)
    hot, fire = ((STOVE17, HOTGLOVE_R), (STOVE17, FIREGLOVE_R)) if side == "player" else ((GLOVEL17, HOTGLOVE_L), (GLOVEL17, FIREGLOVE_L))
    burner = lambda k: emit_at(STOVE17, BURNER, 0, stove)
    w = se(s["disable"]) + _hold(STOVE17, BURNER, 0, stove, 3)                 # click, HI
    w += se(s["bonk"])
    for k in range(9):                                                         # tssss... TSSSSS
        w += emit_at(*hot, 0, (glove_on[0] + (k % 2), glove_on[1])) + burner(k)
        if k % 3 == 0:
            w += emit_at(STOVE17, HEATUP, 0, (stove[0], stove[1] + 8)) + se(s["burn2"])
        w += wait(1)
    w += se(s["fwoosh"]) + flash_screen(2)                                     # FWOOSH
    for k in range(3):
        w += emit_at(*fire, 0, (glove_on[0], glove_on[1] + k * 4)) + burner(k) + wait(1)
    dx, dy = TARGET_FROM_ATTACKER[side]
    for at in _arc((glove_on[0], glove_on[1] + 8), (dx - sx * 18, dy + 18), 4, 10, ease=1.5)[1:]:
        w += emit_at(*fire, 0, at) + wait(1)
    w += emit_at(FLAMES17, FLAMEHIT, 1, (0, 4)) + se(s["flame"]) + flash_screen(5)   # in the FACE
    w += func(34, 8, 0, 2, rgb(255, 110, 20), 14, 0) + shake_defender(4, 3) + func(48) + wait(4)
    w += emit_at(FLAMES17, STEAM17, 1, (0, 16))
    for k in range(4):                                                         # hot hot hot
        w += bmove(side, 264, 2, 0, 8) + wait(2) + bmove(side, 264, 2, 0, -8) + se(s["ember"]) + wait(2)
    return w + wait(8)


def _taser_punch(side, s):
    """ThunderPunch (Taser Punch): a boxing glove with a taser duct-taped to it - bzzt... BZZT - the punch - and
    BZZZZZT: the foe lit up and crackling, then smoking."""
    sx = 1 if side == "player" else -1
    at = TGLOVE_AT[side]
    glove = TGLOVE_R if side == "player" else TGLOVE_L
    tip = (at[0] + sx * 26, at[1] + 12)
    w = se(s["bonk"]) + _hold(TGLOVE17, glove, 0, at, 3)
    for k in range(2):                                                         # bzzt... BZZT
        w += emit_at(TGLOVE17, ZSPARK, 0, tip) + se(s["zap"])
        w += _hold(TGLOVE17, glove, 0, at, 3, lambda j: emit_at(TGLOVE17, glove, 0, (at[0] + (j % 2), at[1])) if k else [])
    dx, dy = TARGET_FROM_ATTACKER[side]
    w += _hold(TGLOVE17, glove, 0, (at[0] - sx * 8, at[1]), 1)                 # wind up
    for at2 in _arc(at, (dx - sx * 20, dy + 16), 4, 6, ease=1.6)[1:]:
        w += emit_at(TGLOVE17, glove, 0, at2) + wait(1)
    w += emit_at(ZAPB17, ZAPBURST, 1, (0, 14)) + emit_at(ZAPS17, BOLTS17, 1, (0, 14)) + se(s["tbolt"])
    w += flash_screen(4) + func(48)
    for k in range(6):                                                         # BZZZZZT
        w += func(34, 8, 0, 1, rgb(255, 245, 60) if k % 2 else rgb(40, 40, 60), 14, 0) + func(36, 2, 0, 1, 1, 264)
        if k == 2:
            w += se(s["zap"])
        w += wait(1)
    w += func(34, 8, 0, 1, rgb(255, 250, 120), 14, 0) + emit_at(ZAPS17, SMOKE17, 1, (0, 22))   # (ends bright)
    return w + wait(16)


def _og_power(side, s):
    """AncientPower (OG Power): the OG relics rise up round them glowing gold - a brick phone, a VHS tape, a
    mixtape - and slam into the foe one after another. Then the OG aura: gold light, all stats up."""
    sx = 1 if side == "player" else -1
    spots = list(RELIC_AT[side])
    spots[2] = (spots[2][0], spots[2][1] + round(RES3_DROP * .95))             # (the tape is res 3)
    relics = [(PHONE17, (sx * spots[0][0], spots[0][1])), (VHS17, spots[1]), (TAPE17, (sx * spots[2][0], spots[2][1]))]
    bob = lambda k, i: (0, 2 if (k + i) % 4 < 2 else -1)

    def up(k, rel, rise=0):
        w = []
        for i, (res, (x, y)) in enumerate(rel):
            b = bob(k, i)
            w += emit_at(RELICS17, res, 0, (x + b[0], y + b[1] - rise))
        return w
    w = emit_at(OGAURA17, SHAFTS, 0, (0, 10)) + se(s["psych"]) + func(34, 2, 0, 1, rgb(255, 210, 60), 10, 0)
    for k in range(5):                                                         # rising up out of the ground
        w += up(k, relics, rise=(4 - k) * 9) + wait(1)
    w += emit_at(RELICS17, OGSPARK, 0, (0, 40)) + se(s["bling"])
    for k in range(4):                                                         # hovering
        w += up(k, relics) + wait(1)
    dx, dy = TARGET_FROM_ATTACKER[side]
    left = list(relics)
    for n, (res, at) in enumerate(relics):                                     # bonk... bonk... BONK
        left = left[1:]
        for at2 in _arc(at, (dx + sx * (-10 + n * 10), dy + 16 - n * 4), 4, 12, ease=1.4)[1:]:
            w += emit_at(RELICS17, res, 0, at2) + up(n, left) + wait(1)
        w += emit_at(OGAURA17, OGDUST, 1, (0, 10)) + se(s["bonk"]) + shake_defender(2 + n, 2)
        if n == 2:
            w += flash_screen(4) + func(48) + func(68, 3, 3, 1, 3, 0)
        w += emit_at(RELICS17, res, 1, (sx * (-10 + n * 10), 16 - n * 4)) + up(n, left) + wait(1)
    w += emit_at(OGAURA17, SHAFTS, 0, (0, 10)) + emit_at(RELICS17, OGSPARK, 0, (0, 30)) + se(s["bling"])
    for k in range(3):                                                         # OG status
        w += func(34, 2, 0, 1, rgb(255, 210, 60), 13, 0) + wait(5)
    return w + wait(4)


def _laser_sight(side, s):
    """Psybeam (Laser Sight): a laser pointer - the red dot wanders over the foe and they chase it round like a
    cat - it stops dead on their forehead - then the beam goes full psychedelic. Brain fried, swirling."""
    sx = 1 if side == "player" else -1
    at = POINTER_AT[side]
    pointer = POINTER_R if side == "player" else POINTER_L
    low = 2 if side == "player" else -8                                       # (yours: clear of the message box)
    path = [(-22, low + 4), (-10, low), (6, low + 6), (20, low + 2), (8, low + 12), (-14, low + 8), (-20, low + 16),
            (-4, low + 20), (12, low + 14), (4, 26), (0, 30)]
    w = se(s["disable"]) + _hold(POINTER17, pointer, 0, at, 2)
    foe_x = 0
    for k, (x, y) in enumerate(path):                                          # the dot... and they chase it
        w += emit_at(POINTER17, pointer, 0, at) + emit_at(POINTER17, DOT17, 1, (x, y))
        if k % 3 == 1 and k < 9:
            step = max(-10, min(10, x - foe_x))
            w += bmove(side, 264, 3, step, 0)
            foe_x += step
        w += wait(1)
    w += bmove(side, 264, 3, -foe_x, 0)
    for k in range(4):                                                         # locked on
        w += emit_at(POINTER17, pointer, 0, at) + emit_at(POINTER17, DOT17, 1, (0, 30))
        w += (se(s["lockon"]) if k == 0 else []) + wait(1)
    w += emit_at(PSYRING17, PRINGS_E if side == "player" else PRINGS_P, 0, POINTER_TIP[side]) + se(s["psych"])
    for k in range(8):                                                         # *bwowowow*
        w += emit_at(POINTER17, pointer, 0, at) + emit_at(POINTER17, DOT17, 1, (0, 30))
        if k >= 3:
            w += func(34, 8, 0, 1, (rgb(255, 80, 200), rgb(80, 220, 255), rgb(255, 240, 80))[k % 3], 12, 0)
            w += func(36, 1, 0, 1, 1, 264)
        w += wait(1)
    w += se(s["confuse"]) + func(48)
    for k in range(8):                                                         # fried
        w += emit_at(DIZZY17, SWIRL17, 1, (0, 40 + (k % 2)))
        if k % 4 == 0:
            w += bmove(side, 264, 4, 4, 0)
        elif k % 4 == 2:
            w += bmove(side, 264, 4, -4, 0)
        w += wait(1)
    return w + wait(4)


def _mudslinging(side, s):
    """Mud-Slap (Mudslinging): a lifted truck's giant tire pulls up beside the foe - stuck in the mud, spinning -
    VRRRRRR - slinging a spray of mud all over them. Can't see a thing."""
    sx = 1 if side == "player" else -1
    tire = MUD_TIRE[side]
    w = emit_at(TIRE17, TIRE_R if side == "player" else TIRE_L, 1, tire)
    w += se(s["rollout"]) + wait(4)
    w += emit_at(TIRE17, MUDDROP, 1, (tire[0], tire[1] - 10)) + se(s["rollout"]) + wait(3)
    w += emit_at(MUDWAVE17, MUDSHEET if side == "player" else MUDDRIP17, 0, (TARGET_FROM_ATTACKER[side][0] + tire[0],
                 TARGET_FROM_ATTACKER[side][1] + tire[1] + 8)) + se(s["mudshot"])
    for k in range(8):                                                         # *splat splat splat*
        if k % 2 == 0:
            w += func(34, 8, 0, 1, rgb(120, 80, 40), 10 + k, 0) + func(36, 1, 0, 1, 1, 264)
        if k == 4:
            w += se(s["mudshot"]) + se(s["rollout"])
        w += wait(2)
    w += func(34, 8, 0, 2, rgb(110, 72, 34), 15, 0) + func(48) + wait(10)
    return w


def _hot_grill(side, s):
    """Fire Fang (Hot Grill): a contact grill opens up round the foe like a mouth, sizzling - CHOMP - CHOMP -
    and they come out with grill marks on them, smoking."""
    at = (0, 12)
    w = se(s["bonk"])
    for k in range(5):                                                         # *tssss*
        w += emit_at(FOREMAN17, GRILLOPEN, 1, at)
        if k == 1:
            w += emit_at(FOREMAN17, GREASE, 1, (0, 0)) + se(s["burn2"])
        w += wait(1)
    for n in range(2):                                                         # CHOMP... CHOMP
        w += se(s["bite"]) + emit_at(SIZZLE17, SIZZLEFX, 1, (0, 4)) + shake_defender(2 + n * 2, 2)
        if n == 1:
            w += flash_screen(4) + se(s["flame"]) + func(34, 8, 0, 2, rgb(255, 120, 30), 14, 0) + func(48)
        w += _hold(FOREMAN17, GRILLSHUT, 1, (at[0], at[1] - 2), 4 + n * 2)
        if n == 0:
            w += _hold(FOREMAN17, GRILLOPEN, 1, at, 3)
    w += emit_at(MARKS17, MARKS, 1, (0, 14)) + emit_at(SIZZLE17, SIZZSTEAM, 1, (0, 22)) + se(s["burn2"])
    w += wait(18)
    return w


def _taser_grill(side, s):
    """Thunder Fang (Taser Grill): a car battery behind them, jumper cables in hand - the clamps touch: SPARKS -
    again: SPARKS - then the clamps go for the foe like a jaw and CHOMP. Lit up, then smoking."""
    sx = 1 if side == "player" else -1
    batt = (-46, 64) if side == "player" else (34, 8)                       # (yours: up behind them, clear of the boxes)
    at = CLAMPS_AT[side]
    (ko, ro), (ks, rs_) = (((CABLES17, CLAMPO_R), (CABLES17, CLAMPS_R)) if side == "player"
                           else ((CABLESL17, CLAMPO_L), (CABLESL17, CLAMPS_L)))
    bat = lambda: emit_at(CABLES17, BATT17, 0, batt)
    w = se(s["bonk"])
    for k in range(3):
        w += bat() + emit_at(ko, ro, 0, at) + wait(1)
    for k in range(2):                                                         # *KZZT* ... *KZZT*
        w += bat() + emit_at(ks, rs_, 0, at) + emit_at(CABLES17, JSPARK17, 0, (at[0] + sx * 22, at[1])) + se(s["spark"])
        w += func(68, 1, 1, 1, 2, 0) + wait(1)
        for j in range(2 + k):
            w += bat() + emit_at(ko, ro, 0, at) + wait(1)
    dx, dy = TARGET_FROM_ATTACKER[side]
    for at2 in _arc(at, (dx - sx * 6, dy + 18), 4, 12, ease=1.5)[1:]:           # *lunge*
        w += bat() + emit_at(ko, ro, 0, at2) + wait(1)
    bite = (-sx * 6, 18)
    w += emit_at(JOLT17, JBOLT17, 1, (0, 16)) + emit_at(CABLES17, JSPARK17, 1, (0, 18)) + se(s["bite"]) + se(s["tbolt"])
    w += flash_screen(4) + func(48)
    for k in range(7):                                                         # CHOMP - BZZZZT
        w += bat() + emit_at(ks, rs_, 1, (bite[0] + (k % 2), bite[1]))
        w += func(34, 8, 0, 1, rgb(255, 245, 60) if k % 2 else rgb(40, 40, 70), 14, 0) + func(36, 2, 0, 1, 1, 264)
        if k == 3:
            w += se(s["spark2"])
        w += wait(1)
    w += func(34, 8, 0, 1, rgb(255, 250, 140), 14, 0) + emit_at(JOLT17, JSMOKE17, 1, (0, 24))
    for k in range(3):
        w += bat() + emit_at(ko, ro, 1, (bite[0] - sx * k * 8, bite[1] + k * 4)) + wait(1)
    return w + wait(12)


def _rizz(side, s):
    """Charm (Rizz): a slow wink - *ting* - and a bouquet of gas-station roses slides on over to the foe, the $4.99
    sticker still on. The foe melts anyway: blushing, hearts, can't even look at them."""
    sx = 1 if side == "player" else -1
    face = (sx * 6, 36) if side == "player" else (-6, 30)
    w = emit_at(ROSES17, WINK17, 0, face) + se(s["captivate"]) + wait(8)
    dx, dy = TARGET_FROM_ATTACKER[side]
    end = (dx - sx * 34, dy + 8)
    for at in _arc((sx * 26, 22), end, 8, 6, ease=.7):                         # *slides them over*
        w += emit_at(ROSES17, ROSES1, 0, at) + wait(1)
    w += emit_at(LOVE17, HEARTPOP17, 1, (0, 26)) + emit_at(LOVE17, HEARTSUP17, 1, (0, 20)) + se(s["attract"])
    for k in range(12):                                                        # *blushing*
        w += emit_at(ROSES17, ROSES1, 0, end)
        if k % 3 == 0:
            w += func(34, 8, 0, 1, rgb(255, 90, 150), 14, 0)
        if k == 4:
            w += bmove(side, 264, 4, -sx * 6, 0)                               # *looks away*
        if k == 8:
            w += bmove(side, 264, 4, sx * 6, -6) + se(s["loyal"])              # *melts*
        w += wait(1)
    return w + bmove(side, 264, 4, 0, 6) + wait(6)


def _bulk_up(side, s):
    """Growth (Bulk Up): the GAINZ tub - two scoops into the shaker, poof, poof - shake, shake, SHAKE - chug it,
    glug glug glug - and they PUMP up: red glow, arrows going up."""
    sx = 1 if side == "player" else -1
    tub = (-28, 58) if side == "player" else (40, 12)
    sh = (sx * 32, 18)
    T = lambda: emit_at(GAINZ17, TUB17, 0, tub)
    w = se(s["bonk"])
    for k in range(2):                                                         # scoop... scoop
        w += T() + emit_at(GAINZ17, SHAKER17, 0, sh) + wait(1)
        w += T() + emit_at(GAINZ17, SHAKER17, 0, sh) + emit_at(GAINZ17, POWDER17, 0, (sh[0], sh[1] + 22)) + se(s["sand"])
        w += wait(1)
    for n, (reps, amp) in enumerate(((2, 4), (3, 6), (4, 8))):                 # shake, shake, SHAKE
        for k in range(reps):
            for y in (amp, -amp // 2):
                w += T() + emit_at(GAINZ17, SHAKER17, 0, (sh[0], sh[1] + y))
                if y > 0:
                    w += se(s["rollout2"])
                w += wait(1)
        w += T() + emit_at(GAINZ17, SHAKER17, 0, sh) + wait(1)
    chug = (sx * 16, 46) if side == "player" else (-sx * -16, 40)
    for k in range(6):                                                         # glug glug glug
        w += T() + emit_at(GAINZ17, CHUG17, 0, (chug[0], chug[1] + (k % 2)))
        if k % 2 == 0:
            w += se(s["absorb"])
        w += wait(1)
    w += emit_at(PUMP17, CHEVRONS17, 0, (0, 6)) + se(s["focus"])
    w += flash_screen(2)
    for k in range(3):                                                         # *PUMP*
        w += bmove(side, 258, 2, 0, 5) + func(34, 2, 0, 1, rgb(255, 70, 40), 14, 0) + wait(2)
        w += bmove(side, 258, 2, 0, -5) + wait(3)
    return w + wait(6)


def _curb_stomp(side, s):
    """Stomp (Curb Stomp): the foe's fresh all-white kicks, sparkling - *ting* - and a GIANT lime-green Croc comes
    down on them. STOMP. Grinds it in. Lifts off: creased, scuffed, a tread print. The foe is LIVID."""
    sx = 1 if side == "player" else -1
    kicks = (-sx * 42, 2) if side == "player" else (42, 14)
    K = lambda res=KICKS1: emit_at(KICKS17, res, 1, kicks)
    w = K() + emit_at(KICKS17, KSPARK17, 1, (kicks[0], kicks[1] + 8)) + se(s["bling"]) + wait(1)
    for k in range(5):
        w += K() + (emit_at(KICKS17, KSPARK17, 1, (kicks[0] + 10, kicks[1] + 4)) if k == 2 else []) + wait(1)
    w += se(s["whoosh"])
    for k, y in enumerate((96, 64, 36)):                                       # here it comes
        w += K() + emit_at(KICKS17, CROC1, 1, (kicks[0], kicks[1] + y)) + wait(1)
    w += se(s["bslam"]) + se(s["bonk"]) + flash_screen(3) + func(68, 4, 4, 1, 3, 0)   # STOMP
    w += emit_at(VEIN17, STOMPDUST17, 1, (kicks[0], kicks[1] - 4))
    for k in range(6):                                                         # *grinds it in*
        w += emit_at(KICKS17, CROC1, 1, (kicks[0] + (3 if k % 2 else -3), kicks[1] + 14)) + K()
        if k == 3:
            w += se(s["sand"])
        w += wait(1)
    for k, y in enumerate((30, 60, 96)):                                       # ...lifts off
        w += K(KICKSWRECKED) + emit_at(KICKS17, CROC1, 1, (kicks[0], kicks[1] + y)) + wait(1)
    w += emit_at(VEIN17, VEINS17, 1, (0, 30)) + se(s["rage"])
    for k in range(10):                                                        # LIVID
        w += K(KICKSWRECKED)
        if k % 2 == 0:
            w += func(34, 8, 0, 1, rgb(255, 40, 30), 14, 0) + shake_defender(2, 1)
        w += wait(1)
    return w + func(48) + wait(4)


def _get_back(side, s):
    """Payback (Get Back): throwing the ex's stuff out on the lawn - the hoodie, the controller, the heart
    boxers, the torn photo rain down on the foe - and then the whole UR STUFF box. BONK."""
    up = 120
    w = []
    for k, (ps, res, x) in enumerate(((STUFF17, HOODIE17, -14), (JUNK17, BOXERS17, 16), (STUFF17, PAD17, -4),
                                      (JUNK17, PHOTO17, 12))):
        w += emit_at(ps, res, 1, (x, up)) + se(s["whoosh"]) + wait(3)
        if k >= 2:
            w += se(s["bonk"]) + shake_defender(2, 1)
    w += wait(4) + se(s["bonk"]) + shake_defender(2, 2) + wait(3)
    box = (0, 8)
    w += se(s["whoosh"]) + stop_motion(STUFF17, STUFFBOX17, 1, (0, up), box, 5, ease=2.0)
    w += emit_at(STUFF17, JUNKDUST17, 1, (0, -6)) + se(s["bslam"]) + flash_screen(4) + func(68, 4, 3, 1, 3, 0)
    w += shake_defender(4, 3) + func(48)
    w += _hold(STUFF17, STUFFBOX17, 1, box, 10)
    return w + wait(4)


def _gun_twirl(side, s):
    """Swords Dance (Gun Twirl): the revolver spins round the finger like a movie - faster, FASTER - tossed up
    flipping - caught - *click* - and they're glowing red, power flaring off them."""
    at = (26, 66) if side == "player" else (-26, 40)
    held = (TWIRL17, GUN_HELD) if side == "player" else (AURA17, GUNHELD_L)
    hat = (at[0], at[1] + round(RES3_DROP * 1.4)) if side == "player" else at   # (GUN_HELD is res 3)
    w = se(s["bling"]) + _hold(*held, 0, hat, 3)
    w += emit_at(TWIRL17, GUN_SLOW, 0, at) + se(s["whoosh"]) + wait_frames(TWIRL_SLOW / 2) + se(s["whoosh"])
    w += wait_frames(TWIRL_SLOW / 2)
    w += emit_at(TWIRL17, GUN_FAST, 0, at)                                     # *spinning* FASTER
    for k in range(3):
        w += se(s["whoosh"]) + wait_frames(TWIRL_FAST / 3)
    w += emit_at(TWIRL17, GUN_TOSS, 0, at) + se(s["whoosh"]) + wait_frames(TOSS_FRAMES)   # tossed up... flipping...
    w += se(s["disable"]) + flash_screen(1) + _hold(*held, 0, hat, 2)         # *click*
    w += emit_at(AURA17, FLARES17, 0, (0, 6)) + se(s["focus"])
    for k in range(8):                                                         # POWER
        w += emit_at(*held, 0, hat)
        if k % 3 == 0:
            w += func(34, 2, 0, 1, rgb(255, 50, 40), 14, 0) + shake_attacker(1, 2)
        w += wait(1)
    return w + wait(4)


def _ace_shot(side, s):
    """Aerial Ace (Ace Shot): the deck fans out - riffle, riffle - the ace of spades flicked out - it curves way out
    past the foe and comes swooping back round (never misses) - SLICE - and sticks in them."""
    sx = 1 if side == "player" else -1
    deck = DECK_AT[side]
    w = se(s["bonk"])
    for k in range(4):                                                         # *riffle*
        w += emit_at(CARDS17, DECK17, 0, (deck[0] + (k % 2), deck[1] + (k % 2)))
        if k % 2 == 0:
            w += se(s["sand"])
        w += wait(1)
    ace = (deck[0], deck[1] + 26)
    w += _hold(CARDS17, DECK17, 0, deck, 3, lambda k: emit_at(CARDS17, ACE17, 0, (ace[0], ace[1] - 6 + k * 3)))
    w += se(s["whoosh"])
    dx, dy = TARGET_FROM_ATTACKER[side]
    p0, p1, p2 = ace, (dx + sx * 70, dy + 80), (dx, dy + 20)                    # out wide... and back round
    n = 9
    for k in range(1, n + 1):
        t = k / n
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
        w += emit_at(CARDS17, ACE17, 0, (round(x), round(y))) + emit_at(CARDS17, CARDTRAIL, 0, (round(x) - sx * 6, round(y)))
        if k == 5:
            w += se(s["whoosh"])
        w += wait(1)
    w += emit_at(SLICE17, SLICE1, 1, (0, 16)) + se(s["slash"]) + se(s["aslash"]) + flash_screen(4)   # SLICE
    w += shake_defender(3, 3) + func(48)
    stuck = (sx * 4, 22)
    w += _hold(CARDS17, ACE17, 1, stuck, 10)                                   # *thunk*
    return w + wait(4)


def _jack_em(side, s):
    """Thief (Jack Em): the foe's designer bag sitting right next to them - an arcade claw drops down from the top
    of the screen - wobbles - CLAMP - and up it goes with the bag. Got it."""
    sx = 1 if side == "player" else -1
    bag = (-sx * 36, 0) if side == "player" else (36, 14)
    B = lambda: emit_at(BAG17, BAG1, 1, bag)

    def claw(res, y, wob=0):
        x = bag[0] + wob
        return (emit_at(CLAW17, res, 1, (x, y)) + emit_at(CLAW17, CABLE17, 1, (x, y + 60)) +
                emit_at(CLAW17, CABLE17, 1, (x, y + 120)))
    w = B() + emit_at(CLAW17, CLAWSPARK, 1, (bag[0] + 8, bag[1] + 10)) + se(s["bling"]) + wait(1)
    w += _hold(BAG17, BAG1, 1, bag, 3)
    top, low = 150, bag[1] + 26
    w += se(s["disable"])
    for k in range(7):                                                         # here comes the claw
        w += B() + claw(CLAWOPEN, round(top + (low - top) * (k / 6) ** .8)) + wait(1)
    for wob in (3, -3, 2, -1):                                                 # *wobble*
        w += B() + claw(CLAWOPEN, low, wob) + wait(1)
    w += se(s["bonk"]) + claw(CLAWBAG, low - 4) + wait(1)                      # CLAMP
    w += claw(CLAWBAG, low - 4) + shake_defender(2, 2) + se(s["swipe"]) + wait(1)   # hey!!
    for k in range(8):                                                         # ...and up it goes
        w += claw(CLAWBAG, round(low - 4 + (top - low) * (k / 7) ** 1.4)) + wait(1)
    w += se(s["chaching"]) + func(34, 2, 0, 1, rgb(255, 220, 60), 12, 0) + wait(10)
    return w


def _drop_a_track(side, s):
    """Sing (Drop a Track): lights down, purple - a 50s mic stand - a slow jam drifting over - lighters up,
    swaying - the foe sways along... a sleep mask drops over their eyes. Zzz."""
    sx = 1 if side == "player" else -1
    mic = MIC_AT[side]
    lighters = [(sx * x, y) for x, y in ((64, 54), (88, 62), (112, 50))] if side == "player" else \
               [(sx * x, y) for x, y in ((60, 2), (84, 10), (108, 0))]
    M = lambda: emit_at(MICS17, MICSTAND, 0, mic)
    w = func(33, 0, 1, 0, 10, rgb(80, 40, 120)) + M() + se(s["bonk"]) + wait(1)
    w += emit_at(SLEEPZ17, NOTES_E17 if side == "player" else NOTES_P17, 0, (mic[0], mic[1] + 26)) + se(s["sleep"])
    sway = 0
    for k in range(18):                                                        # lighters up... swaying
        lean = 3 if (k // 3) % 2 else -3
        w += M()
        for i, (x, y) in enumerate(lighters[:1 + k // 3]):
            w += emit_at(MICS17, LIGHTER17, 0, (x + lean, y + (i % 2)))
        if k % 3 == 0 and k:
            w += bmove(side, 264, 5, lean * 2 - sway, 0)                      # the foe sways along
            sway = lean * 2
        w += wait(1)
    w += bmove(side, 264, 4, -sway, 0)
    w += se(s["yawn"])
    for k, y in enumerate((84, 64, 46, 36)):                                   # *mask drops*
        w += M() + emit_at(MICS17, MASK17, 1, (0, y)) + wait(1)
    w += emit_at(MICS17, ZZ17, 1, (sx * -14, 46)) + se(s["sleep"])
    for k in range(10):                                                        # Zzz
        w += M() + emit_at(MICS17, MASK17, 1, (0, 36))
        if k % 4 == 0:
            w += func(34, 8, 0, 1, rgb(120, 100, 220), 10, 0)
        w += wait(1)
    w += func(33, 0, 1, 10, 0, rgb(80, 40, 120)) + wait(4)
    return w


def _dust_up(side, s):
    """Sandstorm (Dust Up): a gas leaf blower - pull, pull - VRRRRM - and it kicks up a dust storm that sweeps the
    whole block: plastic bags, cans, all of it blowing through. Everybody's eating dirt."""
    sx = 1 if side == "player" else -1
    at = BLOWER_AT[side]
    blower = BLOWER_R if side == "player" else BLOWER_L
    Bl = lambda j=0: emit_at(BLOWER17, blower, 0, (at[0] + (j % 2), at[1]))
    w = se(s["bonk"]) + Bl() + wait(1)
    for k in range(2):                                                         # *pull* ... *pull*
        w += se(s["swipe"]) + Bl() + wait(1) + Bl() + wait(1)
    w += se(s["gust"]) + func(33, 0, 1, 0, 9, rgb(200, 160, 100))             # VRRRRM
    w += emit_at(BLOWER17, SPECKS_R, 0, BLOWER_TIP[side]) if side == "player" else emit_at(TRASH17, SPECKS_L, 0, BLOWER_TIP[side])
    dx, dy = TARGET_FROM_ATTACKER[side]
    mid = (dx // 2, dy // 2 + 10)
    w += emit_at(DUSTSTORM17, DUST_R if side == "player" else DUST_L, 0, (mid[0] - sx * 90, mid[1]))
    lane = (-sx * 150 + mid[0], mid[1] + 4)
    trash = ([(BLOWER17, PBAG_R), (TRASH17, SODA_R)] if side == "player" else [(TRASH17, PBAG_L), (TRASH17, SODA_L)])
    for k in range(20):                                                        # the whole block
        w += Bl(k)
        if k == 2:
            w += emit_at(*trash[0], 0, lane)
        if k == 6:
            w += emit_at(*trash[1], 0, (lane[0], lane[1] - 26)) + se(s["sand"])
        if k == 10:
            w += emit_at(*trash[0], 0, (lane[0], lane[1] + 30))
        if k >= 6 and k % 3 == 0:
            w += func(34, 8, 0, 1, rgb(200, 160, 100), 12, 0) + func(36, 1, 0, 1, 1, 264)
        if k == 12:
            w += se(s["gust"]) + func(34, 2, 0, 1, rgb(200, 160, 100), 10, 0)
        w += wait(1)
    w += func(33, 0, 1, 9, 0, rgb(200, 160, 100)) + wait(6)
    return w


# ------------------------------------------------------------------ set 18: thirty more

def _l3(scl):
    """Lift for a prop on file 82's res 3 (it draws that far below its emitter)."""
    return round(RES3_DROP * scl)


def _mid(side, f=.5, up=0):
    """A point between the two, f of the way from the attacker (attacker-relative)."""
    dx, dy = TARGET_FROM_ATTACKER[side]
    return round(dx * f), round(dy * f) + up


def _run_it_back(side, s):
    """Encore (Run It Back): DJ decks - the record spins up - wikka-wikka - REWIND - the foe gets yanked back and
    has to run the whole thing back. Twice."""
    sx = 1 if side == "player" else -1
    deck = (sx * 36, 32) if side == "player" else (-40, 12)
    rec = (deck[0] - 7, deck[1] + 9)
    D = lambda k=0: emit_at(DJ18, 1, 0, deck)
    w = se(s["bonk"]) + _hold(DJ18, 1, 0, deck, 2)
    w += emit_at(DJ18, 2, 0, rec) + se(s["disable"])
    for k in range(8):                                                         # wikka-wikka
        w += D()
        if k in (2, 4, 5, 7):
            w += se(s["swipe"]) + emit_at(DJ18, 0, 0, (rec[0] - sx * 10, rec[1] + 6))
        w += wait(1)
    w += emit_at(DJFX18, 0, 1, (0, 20)) + se(s["confuse2"])                    # REWIND
    for n in range(2):
        w += D() + bmove(side, 264, 4, sx * 18, 0) + func(34, 8, 0, 1, rgb(80, 220, 255), 12, 0) + wait(1)
        w += D() + se(s["swipe"]) + wait(1)
        w += D() + bmove(side, 264, 3, -sx * 18, 0) + emit_at(DJFX18, 1, 1, (0, 20)) + flash_screen(1) + wait(1)
        w += D() + shake_defender(2, 2) + wait(1)
    w += _hold(DJ18, 1, 0, deck, 3)
    return w + wait(4)


def _pass_it_off(side, s):
    """Baton Pass (Pass It Off): a duffel bag stuffed with cash - look left, look right - and YEET, it's off the
    screen to the next homie. Act natural."""
    sx = 1 if side == "player" else -1
    bag = (sx * 30, 18) if side == "player" else (-30, 16)
    w = se(s["chaching"]) + _hold(DUFFEL18, 1, 0, bag, 3)
    for d in (-1, 1, -1, 1):                                                   # *looks around*
        w += bmove(side, 258, 2, d * 6, 0) + _hold(DUFFEL18, 1, 0, bag, 1)
    w += se(s["whoosh"])
    if side == "player":                                                       # off behind them
        w += emit_at(DUFFEL18, 3, 0, (bag[0], bag[1] + _l3(1.1)))
    else:
        w += emit_at(DUFFEL18, 2, 0, bag)
    w += emit_at(DUFFEL18, 0, 0, (bag[0] - sx * 20, bag[1])) + wait(8)
    for k in range(2):                                                         # *whistles*
        w += func(34, 2, 0, 1, rgb(255, 255, 255), 14, 0) + se(s["pop"]) + wait(4)
    return w + wait(4)


def _brass_knucks(side, s):
    """Metal Claw (Brass Knucks): gold knucks slide on - *shine* - jab - jab - POW. Seeing stars."""
    sx = 1 if side == "player" else -1
    res = 1 if side == "player" else 2
    at = (sx * 30, 22) if side == "player" else (-30, 18)
    w = se(s["swipe"]) + stop_motion(KNUX18, res, 0, (at[0] - sx * 30, at[1]), at, 4, ease=.6)
    w += emit_at(KNUX18, 0, 0, (at[0] + sx * 8, at[1] + 10)) + se(s["bling"]) + _hold(KNUX18, res, 0, at, 3)
    w += emit_at(KNUX18, 0, 0, (at[0] - sx * 6, at[1] + 4)) + _hold(KNUX18, res, 0, at, 2)
    dx, dy = TARGET_FROM_ATTACKER[side]
    for n in range(3):                                                         # jab... jab... POW
        for p in _arc(at, (dx - sx * 14, dy + 14), 3, 4, ease=1.5)[1:]:
            w += emit_at(KNUX18, res, 0, p) + wait(1)
        w += emit_at(POW18, 1 if n == 2 else 0, 1, (0, 16)) + se(s["bslam"] if n == 2 else s["bonk"])
        w += shake_defender(2 + n, 2)
        if n == 2:
            w += flash_screen(4) + func(48) + func(68, 3, 3, 1, 3, 0)
        for p in _arc((dx - sx * 14, dy + 14), at, 3, 4)[1:]:
            w += emit_at(KNUX18, res, 0, p) + wait(1)
    w += emit_at(KNUX18, 0, 0, (at[0] + sx * 8, at[1] + 10)) + _hold(KNUX18, res, 0, at, 3)
    return w + wait(4)


def _doughnuts(side, s):
    """Fire Spin (Doughnuts): a muscle car whips doughnuts round the foe - SKRRRT - tire smoke everywhere - and
    the burnt rubber goes up in a ring of fire. They're boxed in."""
    c = (0, 10) if side == "player" else (0, 16)
    w = []
    for k in range(24):                                                        # two laps
        a = math.pi + k * math.tau / 12
        p = (round(c[0] + 56 * math.cos(a)), round(c[1] + 18 * math.sin(a)))
        w += emit_at(CAR18, 1 if math.sin(a) < 0 else 2, 1, p)
        if k % 2 == 0:
            w += emit_at(CAR18, 0, 1, (p[0], p[1] - 8))
        if k % 6 == 0:
            w += se(s["skrrt"])
        w += wait(1)
    w += emit_at(RINGFIRE18, 0, 1, (0, 4)) + emit_at(RINGFIRE18, 1, 1, (0, 6)) + se(s["flame"]) + flash_screen(3)
    for k in range(4):                                                         # boxed in
        w += func(34, 8, 0, 1, rgb(255, 110, 20), 13, 0) + shake_defender(2, 2) + wait(4)
    return w + wait(4)


def _diss_track(side, s):
    """Taunt (Diss Track): the diss track drops - EXPLICIT - every note aimed straight at the foe. They get
    TIGHT."""
    cd = _mid(side, .4, 30)
    w = se(s["whoosh"]) + stop_motion(CD18, 1, 0, (cd[0], cd[1] + 50), cd, 3, ease=.7)
    w += se(s["bonk"]) + emit_at(CD18, 0, 0, (cd[0] + 18, cd[1] + 18)) + _hold(CD18, 1, 0, cd, 2)
    w += se(s["disable"]) + emit_at(NOTES18, 0 if side == "player" else 1, 0, cd) + se(s["captivate"])
    for k in range(14):                                                        # the bars
        w += emit_at(CD18, 1, 0, cd)
        if k % 3 == 1:
            w += func(34, 8, 0, 1, rgb(255, 50, 40), 12 + k // 3, 0) + shake_defender(1 + k // 5, 2)
        if k == 9:
            w += se(s["rage"]) + bmove(side, 264, 2, 0, 6)
        if k == 10:
            w += bmove(side, 264, 2, 0, -6)
        w += wait(1)
    return w + wait(4)


def _bootleg(side, s):
    """Knock Off (Bootleg): a shady trench coat sidles up to the foe - psst - flashes open: a wall of ROLEKS -
    they bite... and the watch falls apart in their hands. Gears everywhere. The coat dips."""
    sx = 1 if side == "player" else -1
    coat = (-sx * 44, 22) if side == "player" else (44, 20)
    w = se(s["swipe"]) + stop_motion(COAT18, 1, 1, (coat[0] - sx * 60, coat[1]), coat, 4, ease=.6)
    w += se(s["sucker"]) + _hold(COAT18, 1, 1, coat, 4)                        # psst
    w += se(s["bling"]) + flash_screen(2) + emit_at(COAT18, 0, 1, coat)        # *flash*
    w += bmove(side, 264, 4, -sx * 8, 0)
    w += _hold(COAT18, 2, 1, coat, 10, lambda k: emit_at(COAT18, 0, 1, (coat[0], coat[1] + 6)) if k == 5 else [])
    w += bmove(side, 264, 4, sx * 8, 0)
    w += emit_at(GEARS18, 0, 1, (0, 18)) + se(s["smash"]) + se(s["bonk"]) + shake_defender(3, 3) + func(48)
    w += stop_motion(COAT18, 1, 1, coat, (coat[0] - sx * 70, coat[1]), 4, ease=1.6)   # *dips*
    return w + wait(8)


def _run_em_off(side, s):
    """Whirlwind (Run Em Off): grandma's broom comes out - sweep, sweep, sweep - GET OFF MY PORCH - swept right
    off the block."""
    sx = 1 if side == "player" else -1
    res = 1 if side == "player" else 2
    feet = (-sx * 24, 6) if side == "player" else (24, 14)
    w = []
    for n in range(3):                                                         # sweep, sweep, sweep
        for p in ((feet[0] - sx * 18, feet[1] + 12), (feet[0] + sx * 6, feet[1] + 2)):
            w += emit_at(BROOM18, res, 1, p) + wait(1)
        w += emit_at(BROOM18, 0, 1, feet) + se(s["swipe"]) + bmove(side, 264, 2, sx * 4, 0) + wait(1)
    w += se(s["gust"])                                                         # GET OFF MY PORCH
    for p in ((feet[0] - sx * 24, feet[1] + 16), (feet[0] - sx * 4, feet[1] + 8), (feet[0] + sx * 20, feet[1])):
        w += emit_at(BROOM18, res, 1, p) + wait(1)
    w += emit_at(BROOM18, 0, 1, (feet[0] + sx * 20, feet[1])) + bmove(side, 264, 6, sx * 80, 4) + wait(8)
    w += bmove(side, 264, 12, -sx * 92, -4) + wait(8)
    return w


def _suplex(side, s):
    """Seismic Toss (Suplex): the ring drops in round the foe - DING DING - up... up... SUPLEX - one, two,
    three - and the title belt goes up over the attacker."""
    ring = (0, 4) if side == "player" else (0, 12)
    R = lambda: emit_at(RING18, 1, 1, ring)
    w = se(s["whoosh"]) + stop_motion(RING18, 1, 1, (ring[0], ring[1] + 80), ring, 3, ease=1.6) + se(s["bslam"])
    w += func(68, 2, 2, 1, 2, 0)
    for k in range(2):                                                         # DING DING
        w += R() + se(s["bling"]) + wait(1) + R() + wait(1)
    w += bmove(side, 264, 8, 0, 46)                                            # up... up...
    for k in range(5):
        w += R() + (bmove(side, 264, 2, 3 if k % 2 else -3, 0) if k < 4 else []) + wait(1)
    w += bmove(side, 264, 2, 0, -46) + wait(1)                                 # SUPLEX
    w += R() + se(s["kaboom"]) + flash_screen(5) + func(68, 6, 4, 1, 4, 0) + shake_defender(4, 3) + func(48)
    for k in range(3):                                                         # 1... 2... 3
        w += R() + se(s["bonk"]) + wait(1) + R() + wait(1) + R() + wait(1)
    head = (0, 56) if side == "player" else (0, 44)
    w += se(s["chaching"]) + emit_at(RING18, 0, 0, head)
    w += _hold(RING18, 2, 0, head, 8, lambda k: func(34, 2, 0, 1, rgb(255, 220, 60), 12, 0) if k % 4 == 0 else [])
    return w + wait(2)


def _leg_sweep(side, s):
    """Low Kick (Leg Sweep): a puddle and a WET FLOOR sign right there - the foe walks into it anyway - SLIP -
    flat on their back, seeing stars."""
    sx = 1 if side == "player" else -1
    pud = (-sx * 30, 2) if side == "player" else (30, 10)
    sign = (pud[0] - sx * 36, pud[1] + 16)
    P = lambda: emit_at(WET18, 1, 1, sign) + emit_at(WET18, 2, 1, pud)
    w = se(s["bonk"])
    for k in range(5):
        w += P() + wait(1)
    w += bmove(side, 264, 6, -sx * 20, 0)                                      # *walks right into it*
    for k in range(2):
        w += P() + wait(1)
    w += P() + emit_at(WET18, 0, 1, pud) + se(s["splash"]) + bmove(side, 264, 2, 0, 16) + wait(1)   # SLIP
    w += P() + bmove(side, 264, 3, 0, -28) + wait(1)
    w += P() + se(s["bonk"]) + flash_screen(2) + func(68, 3, 3, 1, 3, 0) + shake_defender(3, 2) + wait(1)
    for k in range(10):                                                        # stars
        a = k * math.pi / 3
        w += P() + emit_at(STARS18, 0, 1, (round(-sx * 20 + 14 * math.cos(a)), round(18 + 5 * math.sin(a)))) + wait(1)
    w += bmove(side, 264, 6, sx * 20, 12) + wait(4)
    return w


def _dark_vibes(side, s):
    """Dark Pulse (Dark Vibes): lights out - a black candle lights itself - skulls drift up - and pulses of pure
    bad vibes roll over the foe."""
    sx = 1 if side == "player" else -1
    cand = (-sx * 30, 24) if side == "player" else (34, 14)
    C = lambda: emit_at(CANDLE18, 1, 0, cand)
    w = func(33, 0, 1, 0, 11, rgb(40, 10, 60)) + C() + se(s["nshade"]) + wait(1)
    w += emit_at(CANDLE18, 0, 0, (cand[0], cand[1] + 20))
    for k in range(5):
        w += C() + wait(1)
    w += emit_at(WAVES18, 0 if side == "player" else 1, 0, (0, 24)) + se(s["nshade"])
    for k in range(14):                                                        # the vibes
        w += C()
        if k % 4 == 3:
            w += func(34, 8, 0, 1, rgb(120, 40, 200), 13, 0) + shake_defender(2, 2)
        w += wait(1)
    w += func(48) + func(33, 0, 1, 11, 0, rgb(40, 10, 60)) + wait(6)
    return w


def _premonition(side, s):
    """Future Sight (Premonition): a fortune cookie floats down, glowing - wobble - CRACK - the fortune:
    UR TAKIN AN L. The foe's whole face drops."""
    at = _mid(side, .55, 46)
    w = se(s["psych"]) + stop_motion(COOKIE18, 1, 0, (at[0], at[1] + 40), at, 4, ease=.6)
    for k in range(6):                                                         # *wobble*
        w += emit_at(COOKIE18, 1, 0, (at[0] + (2 if k % 2 else -2), at[1])) + wait(1)
    w += emit_at(COOKIE18, 0, 0, at) + se(s["crack"]) + flash_screen(1)        # CRACK
    slip = (at[0], at[1] + 28)
    for k in range(16):
        w += emit_at(COOKIE18, 2, 0, at) + emit_at(SLIP18, 0, 0, slip)
        if k == 3:
            w += se(s["tdown"])
        if k in (5, 9, 13):
            w += func(34, 8, 0, 1, rgb(60, 110, 255), 12, 0)
        w += wait(1)
    return w + bmove(side, 264, 4, 0, -6) + wait(4) + bmove(side, 264, 4, 0, 6) + wait(2)


def _ankle_break(side, s):
    """Fake Out (Ankle Break): dribble dribble - crossover - crossover back - the foe's ankles GIVE OUT and they
    hit the floor. Then the ball goes right past them."""
    sx = 1 if side == "player" else -1
    base = (-sx * 36, 6) if side == "player" else (36, 16)
    w = []
    for k in range(6):                                                         # dribble
        w += emit_at(BALL18, 1, 1, (base[0], base[1] + (14 if k % 2 else 0)))
        if k % 2 == 0:
            w += se(s["bonk"])
        w += wait(1)
    for d in (1, -1):                                                          # crossover... and back
        w += emit_at(BALL18, 1, 1, (base[0] + sx * 9 * d, base[1] + 8)) + wait(1)
        w += emit_at(BALL18, 1, 1, (base[0] + sx * 18 * d, base[1])) + se(s["bonk"])
        w += emit_at(BALL18, 0, 1, (base[0] + sx * 10 * d, base[1] + 6)) + bmove(side, 264, 3, sx * 12 * d, 0) + wait(1)
    w += se(s["crack"]) + bmove(side, 264, 3, 0, -16) + shake_defender(2, 2) + func(68, 2, 2, 1, 2, 0)   # ANKLES
    for k in range(6):                                                         # ...and past them
        w += emit_at(BALL18, 1, 1, (base[0] - sx * 18 + sx * k * 16, base[1] + (10 if k % 2 else 0))) + wait(1)
    w += bmove(side, 264, 6, 0, 16) + wait(4)
    return w


def _scheme(side, s):
    """Nasty Plot (Scheme): the conspiracy board goes up - red string, pin, pin, pin - they lean in... it's all
    connected - and the evil glow comes on."""
    sx = 1 if side == "player" else -1
    board = (-sx * 30, 42) if side == "player" else (34, 34)
    B = lambda: emit_at(CORK18, 1, 0, board)
    w = se(s["bonk"]) + _hold(CORK18, 1, 0, board, 2)
    for k in range(4):                                                         # pin... pin... string...
        w += B() + emit_at(CORK18, 0, 0, (board[0] + (-12, 10, -4, 12)[k], board[1] + (8, 10, -2, -6)[k])) + se(s["disable"])
        w += wait(1) + B() + wait(1)
    w += bmove(side, 258, 3, -sx * 6, 2) + _hold(CORK18, 1, 0, board, 2)       # *leans in*
    w += emit_at(AURA18, 0, 0, (0, 6)) + se(s["curse"]) + bmove(side, 258, 3, sx * 6, -2)
    for k in range(8):                                                         # it's ALL connected
        w += B()
        if k % 3 == 0:
            w += func(34, 2, 0, 1, rgb(150, 30, 220), 13, 0) + shake_attacker(1, 2)
        w += wait(1)
    return w + wait(4)


def _steel_plate(side, s):
    """Iron Defense (Steel Plate): kitchen armor - a pot CLANGS down on their head, a baking sheet goes up - and
    everything pings right off it."""
    sx = 1 if side == "player" else -1
    head = (0, 56) if side == "player" else (0, 42)
    sheet = (sx * 30, 18) if side == "player" else (-30, 14)
    w = se(s["whoosh"]) + stop_motion(ARMOR18, 1, 0, (head[0], head[1] + 60), head, 4, ease=1.8)
    w += emit_at(ARMOR18, 0, 0, head) + se(s["harden"]) + se(s["bonk"]) + shake_attacker(2, 2)   # CLANG
    for k, x in enumerate((60, 46, 36)):
        w += emit_at(ARMOR18, 1, 0, head) + emit_at(ARMOR18, 2, 0, (sx * x, sheet[1])) + wait(1)
    for k in range(9):                                                         # ping, ping, ping
        w += emit_at(ARMOR18, 1, 0, head) + emit_at(ARMOR18, 2, 0, sheet)
        if k % 3 == 0:
            w += emit_at(ARMOR18, 0, 0, (sheet[0] + sx * 6, sheet[1] + 6)) + se(s["bonk"]) + flash_screen(1)
        if k == 7:
            w += func(34, 2, 0, 1, rgb(180, 190, 210), 13, 0)
        w += wait(1)
    return w + wait(4)


def _turn_up(side, s):
    """Uproar (Turn Up): lights down, the disco ball drops - everybody bouncing on the beat, the whole screen
    shaking - until the neighbors slap a NOISE COMPLAINT on it. Record scratch."""
    mid = _mid(side, .5, 70)
    w = func(33, 0, 1, 0, 10, rgb(60, 20, 90)) + emit_at(PARTY18, 1, 0, mid) + se(s["bling"])
    w += emit_at(LIGHTS18, 0, 0, _mid(side, .5, 10)) + emit_at(LIGHTS18, 1, 0, _mid(side, .5, 20))
    for k in range(6):                                                         # untz untz untz
        w += se(s["bass"]) + func(68, 1, 2, 1, 2, 0) + bmove(side, 258, 2, 0, 5) + bmove(side, 264, 2, 0, 5) + wait(2)
        w += bmove(side, 258, 2, 0, -5) + bmove(side, 264, 2, 0, -5) + wait(2)
    paper = _mid(side, .5, 14)
    w += se(s["swipe"]) + stop_motion(PARTY18, 2, 0, (paper[0], paper[1] + 90), paper, 3, ease=1.6)   # *scrrratch*
    w += se(s["bonk"]) + flash_screen(2) + func(33, 0, 1, 10, 0, rgb(60, 20, 90))
    w += _hold(PARTY18, 2, 0, paper, 10, lambda k: shake_defender(1, 2) if k == 3 else [])
    return w + wait(2)


def _tough_it_out(side, s):
    """Endure (Tough It Out): band-aid - band-aid - band-aid - an ice pack on the head - held together by nothing
    but spite."""
    spots = [(1, (-10, 30)), (3, (12, 22 + _l3(.5))), (1, (2, 40)), (3, (-14, 16 + _l3(.5)))] if side == "player" else \
            [(1, (-10, 22)), (3, (12, 14 + _l3(.5))), (1, (2, 32)), (3, (-14, 8 + _l3(.5)))]
    head = (0, 58) if side == "player" else (0, 44)
    w = []
    for n in range(len(spots)):                                                # slap... slap... slap...
        for k in range(3):
            for res, p in spots[:n + 1]:
                w += emit_at(AID18, res, 0, p)
            if k == 0:
                w += se(s["dslap"]) + shake_attacker(1, 2)
            w += wait(1)
    w += se(s["whoosh"])
    for k in range(7):                                                         # ...ice pack
        y = head[1] + max(0, 30 - k * 10)
        for res, p in spots:
            w += emit_at(AID18, res, 0, p)
        w += emit_at(AID18, 2, 0, (head[0], y))
        if k == 3:
            w += se(s["bonk"]) + emit_at(AID18, 0, 0, head)
        if k in (4, 6):
            w += func(34, 2, 0, 1, rgb(255, 60, 40), 13, 0)
        w += wait(1)
    w += se(s["focus"]) + func(34, 2, 0, 1, rgb(255, 220, 60), 13, 0)
    for k in range(4):
        for res, p in spots:
            w += emit_at(AID18, res, 0, p)
        w += emit_at(AID18, 2, 0, head) + wait(1)
    return w + wait(2)


def _plan_z(side, s):
    """Last Resort (Plan Z): out of options. So they throw the KITCHEN SINK."""
    sx = 1 if side == "player" else -1
    up = (0, 72) if side == "player" else (0, 56)
    w = se(s["harden"])
    for k in range(4):                                                         # it's comin' up
        w += emit_at(SINK18, 1, 0, (-sx * 10 + sx * k * 3, 12 + k * (up[1] - 12) // 3)) + wait(1)
    w += se(s["focus"])
    for k in range(5):                                                         # *strains*
        w += emit_at(SINK18, 1, 0, (up[0] + (2 if k % 2 else -2), up[1] - (k % 2))) + shake_attacker(1, 1) + wait(1)
    dx, dy = TARGET_FROM_ATTACKER[side]
    w += se(s["whoosh"])
    for p in _arc(up, (dx, dy + 14), 7, 40, ease=1.3)[1:]:                     # HEAVE
        w += emit_at(SINK18, 1, 0, p) + wait(1)
    w += emit_at(BOOM18, 0, 1, (0, 6)) + emit_at(BOOM18, 1, 1, (0, 10)) + se(s["kaboom"]) + se(s["smash"])
    w += flash_screen(5) + func(68, 6, 4, 1, 4, 0) + shake_defender(4, 3) + func(48)
    w += emit_at(SINK18, 0, 1, (6, 30))
    w += _hold(SINK18, 1, 1, (0, 14), 8, lambda k: se(s["splash"]) if k == 3 else [])
    return w + wait(2)


def _throwdown(side, s):
    """Close Combat (Throwdown): they dive in - the cartoon fight cloud - BAP BOP POW - stars - a shoe flies out
    - then a TOOTH - and they walk out dusting themselves off."""
    sx = 1 if side == "player" else -1
    dx, dy = TARGET_FROM_ATTACKER[side]
    cloud = (-sx * 22, 12) if side == "player" else (22, 20)
    w = bmove(side, 258, 4, round(dx * .45), round(dy * .2)) + se(s["whoosh"]) + wait(2)
    w += emit_at(BRAWLFX18, 0, 1, cloud)
    sounds = ("bonk", "dslap", "chop", "bonk", "swipe", "dslap")
    for k in range(14):                                                        # BAP BOP POW
        w += emit_at(BRAWL18, 1, 1, (cloud[0] + (3 if k % 2 else -3), cloud[1] + (2 if k % 3 == 0 else 0)))
        w += se(s[sounds[k % len(sounds)]])
        if k % 3 == 1:
            w += emit_at(BRAWL18, 0, 1, (cloud[0] + (8 if k % 2 else -10), cloud[1] + 16)) + func(68, 1, 2, 1, 2, 0)
        if k == 5:
            w += emit_at(BRAWL18, 2, 1, (cloud[0], cloud[1] + 16))             # a shoe
        if k == 10:
            w += emit_at(BRAWL18, 3, 1, (cloud[0], cloud[1] + 16 + _l3(.45)))  # ...a TOOTH
        w += wait(1)
    w += bmove(side, 258, 6, -round(dx * .45), -round(dy * .2)) + flash_screen(3) + shake_defender(4, 3) + func(48)
    return w + wait(8)


def _stay_calm(side, s):
    """Calm Mind (Stay Calm): lights soft - a scented candle, chamomile tea - cucumber slices on - breathe in...
    breathe out... At peace. Dangerously at peace."""
    sx = 1 if side == "player" else -1
    tea = (sx * 32, 12) if side == "player" else (-32, 8)
    cand = (-sx * 32, 16) if side == "player" else (32, 12)
    eyes = [(-7, 52 + _l3(.4)), (7, 52 + _l3(.4))] if side == "player" else [(-7, 36 + _l3(.4)), (7, 36 + _l3(.4))]
    base = lambda: emit_at(CALM18, 1, 0, tea) + emit_at(CALM18, 2, 0, cand)
    w = func(33, 0, 1, 0, 8, rgb(170, 140, 220)) + se(s["amnesia"])
    for k in range(3):
        w += base() + wait(1)
    for n, e in enumerate(eyes):                                               # cucumbers on
        for k in range(2):
            w += base()
            for e2 in eyes[:n + 1]:
                w += emit_at(CALM18, 3, 0, e2)
            if k == 0:
                w += se(s["pop"])
            w += wait(1)
    w += emit_at(CALM18, 0, 0, (tea[0], tea[1] + 18))
    for k in range(16):                                                        # in... out...
        w += base()
        for e in eyes:
            w += emit_at(CALM18, 3, 0, e)
        if k in (0, 8):
            w += bmove(side, 258, 12, 0, 4) + func(34, 2, 0, 1, rgb(140, 230, 200), 10, 0)
        if k in (4, 12):
            w += bmove(side, 258, 12, 0, -4)
        w += wait(1)
    return w + func(33, 0, 1, 8, 0, rgb(170, 140, 220)) + wait(4)


def _snow_cone(side, s):
    """Powder Snow (Snow Cone): a rainbow snow cone - wind up - SPLAT, right in the face. Instant brain freeze."""
    sx = 1 if side == "player" else -1
    hand = (sx * 26, 24) if side == "player" else (-26, 20)
    w = se(s["bling"]) + _hold(SNOWCONE18, 1, 0, hand, 3)
    w += _hold(SNOWCONE18, 1, 0, (hand[0] - sx * 12, hand[1] + 6), 2)          # wind up
    dx, dy = TARGET_FROM_ATTACKER[side]
    w += se(s["whoosh"])
    for p in _arc((hand[0] - sx * 12, hand[1] + 6), (dx, dy + 28), 5, 18, ease=1.2)[1:]:
        w += emit_at(SNOWCONE18, 1, 0, p) + wait(1)
    w += emit_at(SNOWCONE18, 0, 1, (0, 28)) + se(s["splat"]) + flash_screen(2)   # SPLAT
    for k in range(10):                                                        # brain freeze
        w += emit_at(SNOWCONE18, 2, 1, (0, 28))
        if k % 3 == 0:
            w += func(34, 8, 0, 1, rgb(150, 210, 255), 13, 0) + shake_defender(1, 3)
        w += wait(1)
    return w + wait(4)


def _crash_out(side, s):
    """Thrash (Crash Out): a whole cookout table - they stare at it - shaking - shaking - and FLIP IT. Plates,
    ribs, the red cup, all of it, onto the foe."""
    t = _mid(side, .45, 4)
    T = lambda: emit_at(TABLE18, 1, 0, t)
    w = se(s["bonk"]) + _hold(TABLE18, 1, 0, t, 3)
    for n in range(3):                                                         # *shaking*
        w += T() + func(34, 2, 0, 1, rgb(255, 40, 30), 10 + n * 2, 0) + shake_attacker(1 + n, 2) + wait(1)
        w += T() + wait(1) + T() + wait(1)
    w += se(s["rage"]) + se(s["whoosh"]) + emit_at(PLATES18, 1, 0, (t[0], t[1] + 20)) + emit_at(PLATES18, 2, 0, (t[0], t[1] + 20))
    w += emit_at(TABLE18, 0, 0, (t[0], t[1] + 18))
    dx, dy = TARGET_FROM_ATTACKER[side]
    for p in _arc((t[0], t[1] + 8), (dx, dy + 10), 4, 24, ease=1.2)[1:]:       # FLIP
        w += emit_at(TABLE18, 2, 0, p) + wait(1)
    w += emit_at(PLATES18, 0, 1, (0, 4)) + se(s["kaboom"]) + flash_screen(4) + func(68, 5, 4, 1, 4, 0)
    w += shake_defender(4, 3) + func(48)
    w += _hold(TABLE18, 2, 1, (0, 10), 6)
    return w + wait(2)


def _pogo_stick(side, s):
    """Bounce (Pogo Stick), two turns. Turn 1: boing... boing... BOING - clean off the top of the screen. Turn 2:
    they come down out of the sky pogo-first on the foe's head."""
    pg = (0, 2) if side == "player" else (0, -8)
    one = []
    for n, h in enumerate((10, 16, 24)):                                       # boing... boing... BOING
        one += se(s["rollout2"]) + emit_at(POGO18, 0, 0, (pg[0], pg[1] - 16))
        one += bmove(side, 258, 4, 0, h)
        for k in range(2):
            one += emit_at(POGO18, 1, 0, (pg[0], pg[1] + h * (k + 1) // 2)) + wait(1)
        one += bmove(side, 258, 4, 0, -h)
        for k in range(2):
            one += emit_at(POGO18, 1, 0, (pg[0], pg[1] + h * (1 - k) // 2)) + wait(1)
    one += se(s["whoosh"]) + bmove(side, 258, 6, 0, 150) + wait(4) + func(40, 2, 1)   # gone
    one += bmove(side, 258, 1, 0, -150) + wait(2)
    dx, dy = TARGET_FROM_ATTACKER[side]
    two = bmove(side, 258, 1, dx, dy + 150) + wait(1) + func(40, 2, 0) + se(s["whoosh"])
    two += bmove(side, 258, 5, 0, -150 + 34) + wait(3)                         # ...incoming
    two += emit_at(POGO18, 0, 1, (0, -6)) + emit_at(POGO18, 1, 1, (0, 30)) + se(s["bslam"]) + flash_screen(4)
    two += func(68, 4, 4, 1, 3, 0) + shake_defender(4, 3) + func(48)
    for k in range(3):
        two += emit_at(POGO18, 1, 1, (0, 30 + k * 6)) + wait(1)
    two += bmove(side, 258, 8, -dx, -dy - 34) + wait(8)
    return one, two


def _pogo_turn2_first(side, s):
    """Test only: Pogo Stick with the turns swapped."""
    one, two = _pogo_stick(side, s)
    return two, one


def _shear_pain(side, s):
    """X-Scissor (Shear Pain): salon shears - snip snip snip snip - hair flying everywhere - a big X - and the
    reveal: a fresh bald spot, gleaming."""
    sx = 1 if side == "player" else -1
    head = (0, 36) if side == "player" else (0, 46)
    at = (head[0] - sx * 18, head[1] + 6)
    w = se(s["swipe"]) + stop_motion(SCISS18, 1, 1, (at[0] - sx * 60, at[1] + 10), at, 3, ease=.7)
    for k in range(8):                                                         # snip snip snip
        shut = k % 2 == 1
        w += emit_at(SCISS18, 2 if shut else 1, 1, (at[0] + sx * (k % 4) * 4, at[1] - (k % 3) * 3))
        if shut:
            w += se(s["slash"]) + emit_at(SCISS18, 0, 1, (head[0], head[1] + 4)) + shake_defender(1, 1)
        w += wait(1)
    for frm, to in (((-20, 20), (20, -14)), ((20, 20), (-20, -14))):           # a big X
        for t in (0, .5, 1):
            w += emit_at(SCISS18, 2, 1, (head[0] + sx * round(frm[0] + (to[0] - frm[0]) * t), head[1] + round(frm[1] + (to[1] - frm[1]) * t))) + wait(1)
        w += se(s["slash"]) + emit_at(SCISS18, 0, 1, head)
    w += wait(3) + emit_at(SHINE18, 0, 1, (head[0] + sx * 4, head[1] + 10)) + se(s["bling"])   # *ting*
    for k in range(2):
        w += func(34, 8, 0, 1, rgb(255, 90, 120), 13, 0) + wait(4)
    return w + wait(4)


def _lava_lamp(side, s):
    """Lava Plume (Lava Lamp): the lava lamp heats up... bubbling... rattling... and ERUPTS - wax everywhere."""
    sx = 1 if side == "player" else -1
    top = (-30, 60) if side == "player" else (30, 60)                         # (the BLOBS18 spray starts here)
    lamp = (top[0], top[1] - 28)
    L = lambda j=0: emit_at(LAMP18, 1, 0, (lamp[0] + j, lamp[1]))
    w = se(s["bonk"]) + L() + wait(1) + emit_at(LAMP18, 0, 0, (lamp[0], lamp[1] + 6)) + se(s["burn2"])
    for k in range(6):
        w += L() + wait(1)
    for k in range(6):                                                         # *rattling*
        w += L(2 if k % 2 else -2) + func(68, 1, 1, 1, 1, 0) + wait(1)
    w += emit_at(BLOBS18, 0 if side == "player" else 1, 0, top) + se(s["sbomb"]) + se(s["flame"]) + flash_screen(2)
    for k in range(12):                                                        # ERUPTS
        w += L(1 if k % 2 else -1)
        if k % 3 == 2:
            w += func(34, 8, 0, 1, rgb(255, 110, 30), 13, 0) + shake_defender(2, 2)
        w += wait(1)
    return w + func(48) + wait(4)


def _stack_up(side, s):
    """Stockpile (Stack Up): pancakes drop one at a time onto the stack - higher - higher - then butter and
    SYRUP. Stocked up."""
    sx = 1 if side == "player" else -1
    base = (sx * 34, 6) if side == "player" else (-34, 2)
    STEP = 7
    stack = lambda n: [w for i in reversed(range(n)) for w in emit_at(PANCAKE18, 1, 0, (base[0], base[1] + i * STEP))]
    w = []
    for n in range(5):                                                         # plop... plop...
        for y in (70, 34, 10):
            w += stack(n) + emit_at(PANCAKE18, 1, 0, (base[0], base[1] + n * STEP + y)) + wait(1)
        w += stack(n + 1) + se(s["pop"]) + wait(1)
    top = (base[0], base[1] + 5 * STEP)
    w += se(s["bling"]) + emit_at(PANCAKE18, 0, 0, (top[0], top[1] + 6))
    for k in range(10):                                                        # butter, SYRUP
        w += emit_at(PANCAKE18, 2, 0, (top[0], top[1] - 2)) + stack(5)
        if k in (2, 6):
            w += func(34, 2, 0, 1, rgb(255, 200, 80), 12, 0) + bmove(side, 258, 3, 0, 4)
        if k in (4, 8):
            w += bmove(side, 258, 3, 0, -4)
        w += wait(1)
    return w + wait(2)


def _clap_back(side, s):
    """Counter (Clap Back): a clapperboard pops up in their face - TAKE 2 - SNAP - and SNAP again, harder."""
    sx = 1 if side == "player" else -1
    at = (-sx * 40, 28) if side == "player" else (40, 36)
    w = se(s["disable"]) + _hold(CLAP18, 1, 1, at, 4)
    for n in range(2):                                                         # SNAP... SNAP
        w += emit_at(CLAP18, 2, 1, at) + emit_at(CLAP18, 0, 1, (at[0] + sx * 20, at[1] + 10))
        w += se(s["dslap"]) + flash_screen(2 + n * 2) + shake_defender(2 + n * 2, 2) + func(48)
        if n:
            w += se(s["bonk"]) + func(68, 4, 3, 1, 3, 0)
        w += wait(1) + _hold(CLAP18, 2, 1, at, 3)
        if not n:
            w += _hold(CLAP18, 1, 1, at, 3)
    return w + wait(4)


def _hammer_time(side, s):
    """Crabhammer (Hammer Time): the carnival high striker next to the foe - the mallet winds up - WHAM - the
    puck rockets up - DING DING DING - and then the mallet comes down on the foe too."""
    sx = 1 if side == "player" else -1
    tower = (-sx * 46, 24) if side == "player" else (46, 30)
    pad = (tower[0], tower[1] - 34)
    mres, lift = (2, 0) if side == "player" else (3, _l3(1.2))
    T = lambda: emit_at(STRIKER18, 1, 1, tower)
    M = lambda p: emit_at(STRIKER18, mres, 1, (p[0], p[1] + lift))
    w = se(s["bonk"]) + _hold(STRIKER18, 1, 1, tower, 2)
    for k in range(4):                                                         # winding up
        w += T() + M((pad[0] - sx * 34, pad[1] + 40 + k * 3)) + wait(1)
    for p in ((pad[0] - sx * 24, pad[1] + 26), (pad[0] - sx * 10, pad[1] + 10)):
        w += T() + M(p) + wait(1)
    w += emit_at(STRIKER18, 0, 1, pad) + se(s["bslam"]) + func(68, 3, 3, 1, 3, 0)   # WHAM
    for k in range(7):                                                         # the puck
        w += T() + M((pad[0] - sx * 10, pad[1] + 10)) + emit_at(PUCK18, 0, 1, (tower[0], pad[1] + 4 + k * 10)) + wait(1)
    w += emit_at(STRIKER18, 0, 1, (tower[0], tower[1] + 32)) + flash_screen(3)
    for k in range(3):                                                         # DING DING DING
        w += T() + emit_at(PUCK18, 0, 1, (tower[0], tower[1] + 28)) + se(s["bling"]) + wait(1)
    for p in ((-sx * 30, 60), (-sx * 14, 46), (-sx * 2, 36)):                  # ...and on the foe
        w += T() + M(p) + wait(1)
    w += se(s["bslam"]) + se(s["bonk"]) + flash_screen(4) + shake_defender(4, 3) + func(48)
    w += emit_at(STRIKER18, 0, 1, (0, 34)) + _hold(STRIKER18, 1, 1, tower, 4)
    return w + wait(2)


def _chalkboard(side, s):
    """Metal Sound (Chalkboard): a chalkboard - a fork - and the slowest, longest SCREEEECH. The foe's soul leaves
    their body. (So does the attacker's, a little.)"""
    board = _mid(side, .44, 44)
    B = lambda: emit_at(CHALK18, 1, 0, board)
    w = se(s["bonk"]) + _hold(CHALK18, 1, 0, board, 3)
    for k in range(14):                                                        # SCREEEEEECH
        t = k / 13
        w += emit_at(CHALK18, 2, 0, (board[0] - 10 + round(26 * t), board[1] + 20 - round(32 * t))) + B()   # (fork first:
#                                                                                   the older emitter draws on top)
        if k % 2 == 0:
            w += se(s["leer"]) + emit_at(CHALK18, 0, 0, (board[0] - 6 + round(26 * t), board[1] + 6 - round(32 * t)))
        if k % 3 == 1:
            w += func(34, 8, 0, 1, rgb(200, 230, 255), 13, 0) + shake_defender(2, 2)
        if k == 9:
            w += shake_attacker(1, 2)
        w += wait(1)
    w += func(34, 8, 0, 1, rgb(80, 120, 255), 14, 0) + flash_screen(2) + func(48)
    return w + _hold(CHALK18, 1, 0, board, 3)


def _mosquito(side, s):
    """Bug Buzz (Mosquito): one mosquito. bzzzz. Round and round their head. They swing at it - and SLAP
    THEMSELVES. It flies off. Bites everywhere."""
    sx = 1 if side == "player" else -1
    head = (0, 34) if side == "player" else (0, 44)
    w = []
    for k in range(16):                                                        # bzzzzz
        a = k * math.tau / 8
        p = (round(head[0] + 26 * math.cos(a)), round(head[1] + 10 * math.sin(a) + 4 * math.sin(a * 3)))
        w += emit_at(MOSQ18, 1 if math.sin(a) < 0 else 2, 1, p)
        if k % 4 == 0:
            w += se(s["psting"])
        if k in (5, 11):
            w += bmove(side, 264, 2, -sx * 4, 0)
        if k in (7, 13):
            w += bmove(side, 264, 2, sx * 4, 0)
        w += wait(1)
    w += _hold(MOSQ18, 1, 1, (head[0] - 4, head[1] - 4), 2)                    # *lands*
    w += se(s["dslap"]) + se(s["bonk"]) + flash_screen(3) + func(68, 3, 3, 1, 3, 0) + shake_defender(3, 3) + func(48)
    for k in range(4):                                                         # *buzzes off*
        w += emit_at(MOSQ18, 1, 1, (head[0] + 10 + k * 20, head[1] + 10 + k * 14)) + wait(1)
    w += emit_at(WELT18, 0, 1, (0, 20)) + se(s["psting"])
    for k in range(2):
        w += func(34, 8, 0, 1, rgb(255, 80, 80), 13, 0) + wait(4)
    return w + wait(4)


def _flush_it(side, s):
    """Whirlpool (Flush It): the foe hops over into the open - a giant toilet rises round them - the handle -
    FLUSHHHH - spinning, sinking, the TP roll whipping round - then they pop back up, soaked."""
    sx = 1 if side == "player" else -1
    on = (-sx * 44, 16) if side == "player" else (10, 24)                      # (clear of your HP box / the text)
    seat = (on[0], on[1] - 2)
    T = lambda: emit_at(TOILET18, 1, 1, seat)
    w = bmove(side, 264, 6, *on) + wait(3)
    w += se(s["bonk"]) + stop_motion(TOILET18, 1, 1, (seat[0], seat[1] - 40), seat, 3, ease=.7)
    w += _hold(TOILET18, 1, 1, seat, 3)
    w += se(s["surf"]) + se(s["whoosh"]) + emit_at(FLUSH18, 0, 1, (seat[0], seat[1] + 14))   # FLUSH
    w += emit_at(FLUSH18, 1, 1, (seat[0], seat[1] + 12))
    w += bmove(side, 264, 12, 0, -20) + func(34, 8, 0, 1, rgb(90, 170, 255), 12, 0)
    for k in range(12):                                                        # round and round
        a = k * math.tau / 6
        w += T() + emit_at(TOILET18, 2, 1, (seat[0] + round(30 * math.cos(a)), seat[1] + round(16 + 10 * math.sin(a))))
        if k % 3 == 0:
            w += bmove(side, 264, 2, 4 if k % 2 else -4, 0)
        if k == 6:
            w += se(s["surf"])
        w += wait(1)
    w += bmove(side, 264, 3, 0, 20) + emit_at(TOILET18, 0, 1, (seat[0], seat[1] + 16)) + se(s["splash"]) + flash_screen(2)
    w += _hold(TOILET18, 1, 1, seat, 5)                                        # *bloop*
    w += bmove(side, 264, 6, -on[0], -on[1]) + wait(4)
    return w


# ------------------------------------------------------------------ set 19: the TMs

def _lob(ps, res, side, frm, to, steps, height, extra=lambda k: []):
    """A prop lobbed from frm (attacker-relative) to to (attacker-relative) over steps ticks."""
    w = []
    for k, p in enumerate(_arc(frm, to, steps, height, ease=1.2)[1:]):
        w += emit_at(ps, res, 0, p) + extra(k) + wait(1)
    return w


def _foe_at(side, off=(0, 0)):
    """The foe's spot + off, attacker-relative (for lobbing things onto them)."""
    dx, dy = TARGET_FROM_ATTACKER[side]
    return dx + off[0], dy + off[1]


def _fruit_throw(side, s):
    """Natural Gift (Fruit Throw): a pineapple lobbed - BONK - then a whole watermelon, slow and heavy - SPLAT."""
    sx = 1 if side == "player" else -1
    hand = (sx * 24, 26)
    w = se(s["whoosh"]) + _lob(FRUIT19, 1, side, hand, _foe_at(side, (0, 30)), 5, 24)
    w += se(s["bonk"]) + shake_defender(2, 2) + wait(3)
    w += se(s["whoosh"]) + _lob(FRUIT19, 2, side, hand, _foe_at(side, (0, 26)), 7, 40)
    w += emit_at(FRUIT19, 0, 1, (0, 20)) + se(s["splat"]) + se(s["bslam"]) + flash_screen(3) + shake_defender(4, 3) + func(48)
    w += _hold(FRUIT19, 3, 1, (0, 20 + _l3(1.2)), 10, lambda k: func(34, 8, 0, 1, rgb(240, 70, 90), 12, 0) if k == 2 else [])
    return w + wait(2)


def _crash_pad(side, s):
    """Roost (Crash Pad): a flat air mattress - pump, pump, pump - it puffs up - they flop on it - healing."""
    sx = 1 if side == "player" else -1
    bed = (sx * 30, 24) if side == "player" else (-36, 2)
    w = se(s["bonk"]) + _hold(MATTRESS19, 1, 0, bed, 3)
    for k in range(3):                                                         # pump, pump, pump
        w += emit_at(MATTRESS19, 1, 0, bed) + se(s["whoosh"]) + wait(1)
        w += emit_at(MATTRESS19, 2, 0, bed) + emit_at(MATTRESS19, 0, 0, (bed[0] - sx * 30, bed[1])) + wait(1)
    w += se(s["pop"]) + _hold(MATTRESS19, 2, 0, bed, 2)
    w += bmove(side, 258, 4, sx * 10, 6) + _hold(MATTRESS19, 2, 0, bed, 1)     # *flop*
    w += bmove(side, 258, 3, 0, -10) + se(s["bonk"]) + _hold(MATTRESS19, 2, 0, bed, 1)
    w += emit_at(HEAL19, 0, 0, (0, 10)) + se(s["absorb"])
    for k in range(8):
        w += emit_at(MATTRESS19, 2, 0, bed)
        if k % 3 == 0:
            w += func(34, 2, 0, 1, rgb(120, 255, 140), 12, 0)
        w += wait(1)
    w += bmove(side, 258, 6, -sx * 10, 4) + _hold(MATTRESS19, 2, 0, bed, 3)
    return w


def _toss_it(side, s):
    """Fling (Toss It): the whole old box TV - heave - CRASH. Static everywhere."""
    sx = 1 if side == "player" else -1
    up = (sx * 10, 60) if side == "player" else (-10, 48)
    w = se(s["harden"])
    for k in range(4):                                                         # *lifts it*
        w += emit_at(TV19, 1, 0, (up[0] + (2 if k % 2 else -2), up[1] - 24 + k * 8)) + wait(1)
    w += se(s["whoosh"]) + _lob(TV19, 1, side, up, _foe_at(side, (0, 18)), 6, 30)
    w += emit_at(TV19, 0, 1, (0, 20)) + se(s["smash"]) + se(s["kaboom"]) + flash_screen(4) + func(68, 4, 4, 1, 3, 0)
    w += shake_defender(4, 3) + func(48) + _hold(TV19, 1, 1, (0, 14), 6)
    return w + wait(2)


def _dream_killer(side, s):
    """Dream Eater (Dream Killer): the foe's dream bubble - a mansion, a stack of cash, a chain - a pin floats
    over... POP. Back to reality. The attacker eats the leftovers."""
    sx = 1 if side == "player" else -1
    bub = (sx * -6, 58) if side == "player" else (6, 60)
    w = se(s["sleep"])
    for k in range(6):                                                         # *dreaming*
        w += emit_at(DREAM19, 1, 1, (bub[0], bub[1] + (k % 2))) + wait(1)
    dx, dy = TARGET_FROM_ATTACKER[side]
    for t in (0, .35, .65, .85, 1):                                            # here comes the pin
        p = (round(sx * 20 + (dx + bub[0] - sx * 22 - sx * 20) * t), round(30 + (dy + bub[1] - 30) * t))
        w += emit_at(DREAM19, 1, 1, bub) + emit_at(DREAM19, 2, 0, p) + wait(1)
    w += emit_at(DREAM19, 0, 1, bub) + se(s["pop"]) + flash_screen(2)        # POP
    w += func(34, 8, 0, 1, rgb(120, 120, 140), 14, 0) + shake_defender(2, 3) + wait(4)
    w += se(s["absorb"]) + func(34, 2, 0, 1, rgb(200, 120, 255), 12, 0) + wait(6)
    return w


def _claw_clap(side, s):
    """Dragon Claw (Claw Clap): a giant boiled lobster claw - snap... snap... - CLAMPS on - Old Bay everywhere."""
    sx = 1 if side == "player" else -1
    op, sh = ((LOBSTER19, 1), (LOBSTER19, 2)) if side == "player" else ((LOBL19, 0), (LOBL19, 1))
    at = (sx * 30, 24) if side == "player" else (-30, 20)
    w = se(s["bonk"])
    for k in range(2):                                                         # snap... snap...
        w += emit_at(*op, 0, at) + wait(1) + emit_at(*sh, 0, at) + se(s["bite"]) + wait(1)
    dx, dy = TARGET_FROM_ATTACKER[side]
    for p in _arc(at, (dx - sx * 22, dy + 18), 4, 8, ease=1.4)[1:]:
        w += emit_at(*op, 0, p) + wait(1)
    w += emit_at(LOBSTER19, 0, 1, (0, 22)) + se(s["bite"]) + se(s["bslam"]) + flash_screen(3)   # CLAMP
    for k in range(7):
        w += emit_at(*sh, 1, (-sx * 22 + (k % 2), 18)) + shake_defender(1, 1) + wait(1)
    w += func(48) + _hold(*op, 1, (-sx * 30, 22), 2)
    return w + wait(2)


def _u_turn(side, s):
    """U-turn: a rental e-scooter zips in from behind the attacker - BONK - pulls a U-turn and zips back out."""
    sx = 1 if side == "player" else -1
    go, back = (1, 2) if side == "player" else (2, 1)
    dx, dy = TARGET_FROM_ATTACKER[side]
    w = se(s["whoosh"])
    for k in range(7):                                                         # zip in
        t = k / 6
        w += emit_at(SCOOT19, go, 0, (round(-sx * 60 + (dx - sx * 20 + sx * 60) * t), round(10 + (dy + 4 - 10) * t)))
        w += emit_at(SCOOT19, 0, 0, (round(-sx * 76 + (dx + sx * 40) * t), round(14 + (dy - 10) * t))) + wait(1)
    w += se(s["bonk"]) + flash_screen(2) + shake_defender(3, 2) + func(48)
    for k in range(2):
        w += emit_at(SCOOT19, back, 1, (-sx * 20, 4)) + wait(1)                # *U-turn*
    w += se(s["whoosh"])
    for k in range(6):                                                         # ...and dips
        w += emit_at(SCOOT19, back, 1, (-sx * (20 + k * 40), 4 - k * 4)) + wait(1)
    w += func(34, 2, 0, 1, rgb(255, 255, 255), 13, 0) + se(s["pop"]) + wait(4)
    return w


def _dragon_beam(side, s):
    """Dragon Pulse (Dragon Beam): the parade dragon dances its way over - and a string of firecrackers goes off
    all round the foe. POP POP POP POP."""
    sx = 1 if side == "player" else -1
    res = 1 if side == "player" else 2
    w = se(s["bass"])
    for k in range(8):                                                         # *dancing over*
        t = k / 7
        p = _mid(side, .2 + t * .4, 20 + (8 if k % 2 else 0))
        w += emit_at(DRAGON19, res, 0, p) + (se(s["bonk"]) if k % 2 == 0 else []) + wait(1)
    end = _mid(side, .6, 20)
    for k in range(12):                                                        # POP POP POP
        w += emit_at(DRAGON19, res, 0, end)
        w += emit_at(DRAGON19, 0, 1, (((k * 23) % 50) - 25, ((k * 17) % 40)))
        w += se(s["pop"] if k % 2 else s["bonk"])
        if k % 3 == 2:
            w += shake_defender(2, 1) + func(34, 8, 0, 1, rgb(255, 120, 40), 12, 0)
        w += wait(1)
    w += flash_screen(3) + func(48)
    return w + wait(4)


def _silver_dust(side, s):
    """Silver Wind (Silver Dust): a glitter-bomb envelope slides over - the foe opens it - and silver glitter
    explodes ALL over them. It's never coming out."""
    sx = 1 if side == "player" else -1
    env = (-sx * 30, 14) if side == "player" else (30, 24)
    w = se(s["swipe"]) + stop_motion(GLITTER19, 1, 1, (env[0] - sx * 60, env[1]), env, 4, ease=.6)
    w += _hold(GLITTER19, 1, 1, env, 4)
    w += emit_at(GLITTER19, 0, 1, (env[0], env[1] + 16)) + se(s["bling"]) + flash_screen(3)   # *FWOOMP*
    for k in range(12):
        w += emit_at(GLITTER19, 2, 1, env)
        if k % 2 == 0:
            w += func(34, 8, 0, 1, rgb(220, 225, 245), 13, 0)
        if k in (3, 7):
            w += se(s["bling"])
        w += wait(1)
    return w + shake_defender(2, 3) + wait(6)


def _ice_storm(side, s):
    """Hail (Ice Storm): a giant bag of party ICE falls out the sky - SPLITS - and cubes hail down on everybody."""
    mid = _mid(side, .5, 30)
    w = se(s["whoosh"]) + stop_motion(ICEBAG19, 1, 0, (mid[0], mid[1] + 90), mid, 4, ease=1.8)
    w += emit_at(ICEBAG19, 0, 0, mid) + se(s["ishard"]) + se(s["smash"]) + flash_screen(2)
    w += func(33, 0, 1, 0, 7, rgb(170, 210, 255)) + emit_at(CUBES19, 0, 0, (mid[0], mid[1] + 70))
    for k in range(16):                                                        # *clatter clatter*
        if k % 3 == 0:
            w += se(s["bonk"]) + shake_defender(1, 1)
        if k % 5 == 2:
            w += shake_attacker(1, 1)
        w += wait(1)
    w += func(34, 8, 0, 1, rgb(170, 220, 255), 12, 0) + func(33, 0, 1, 7, 0, rgb(170, 210, 255)) + wait(4)
    return w


def _confiscate(side, s):
    """Embargo (Confiscate): CAUTION tape whips across the foe - the siren - their stuff goes in an EVIDENCE bag."""
    sx = 1 if side == "player" else -1
    tape = (0, 22) if side == "player" else (0, 30)
    bag = (-sx * 44, 22) if side == "player" else (44, 30)
    w = se(s["alarm"])
    for k in range(5):                                                         # the tape stretches across
        w += emit_at(EVID19, 1, 1, (tape[0] - sx * (60 - k * 15), tape[1])) + emit_at(EVID19, 0, 1, (0, 30)) + wait(1)
    w += se(s["swipe"]) + stop_motion(EVID19, 2, 1, (bag[0], bag[1] + 60), bag, 3, ease=1.6)
    for k in range(10):                                                        # *bagged and tagged*
        w += emit_at(EVID19, 1, 1, tape) + emit_at(EVID19, 2, 1, bag)
        if k % 2 == 0:
            w += emit_at(EVID19, 0, 1, (0, 30))
        if k == 3:
            w += se(s["disable"]) + func(34, 8, 0, 1, rgb(140, 140, 160), 13, 0)
        w += wait(1)
    return w + wait(2)


def _flick_a_bic(side, s):
    """Will-O-Wisp (Flick a Bic): strike... strike... FSST - the match catches - ghostly blue flames drift across
    and cling to the foe."""
    sx = 1 if side == "player" else -1
    box = (sx * 30, 28) if side == "player" else (-34, 12)
    w = []
    for k in range(2):                                                         # strike... strike...
        w += emit_at(MATCH19, 1, 0, box) + se(s["swipe"]) + wait(1) + emit_at(MATCH19, 1, 0, box) + wait(1)
    w += emit_at(MATCH19, 0, 0, (box[0] + sx * 20, box[1] + 28)) + se(s["ember"])   # FSST
    w += emit_at(WISP19, 0 if side == "player" else 1, 0, (40 * sx, 30 if side == "player" else 26))
    for k in range(18):
        w += emit_at(MATCH19, 2, 0, box)
        if k >= 10 and k % 3 == 1:
            w += func(34, 8, 0, 1, rgb(110, 120, 255), 13, 0) + shake_defender(1, 2)
        w += wait(1)
    return w + se(s["burn2"]) + wait(4)


def _static_shock(side, s):
    """Shock Wave (Static Shock): a balloon rubbed on their head - squeak squeak squeak - sparks crackling - and
    ZAP, it jumps straight to the foe."""
    head = (0, 56) if side == "player" else (0, 46)
    w = []
    for k in range(8):                                                         # *rub rub rub*
        w += emit_at(BALLOON19, 1, 0, (head[0] + (6 if k % 2 else -6), head[1] + 6))
        if k % 2 == 0:
            w += se(s["swipe"])
        if k >= 4:
            w += emit_at(BALLOON19, 0, 0, head)
        w += wait(1)
    w += emit_at(ZAP19, 0 if side == "player" else 1, 0, (10 if side == "player" else -10, head[1])) + se(s["zap"])
    w += _hold(BALLOON19, 1, 0, (head[0], head[1] + 6), 2)
    w += se(s["tbolt"]) + flash_screen(3) + func(48)
    for k in range(4):
        w += func(34, 8, 0, 1, rgb(255, 245, 60) if k % 2 == 0 else rgb(40, 40, 70), 13, 0) + shake_defender(2, 1) + wait(1)
    return w + func(34, 8, 0, 1, rgb(255, 250, 140), 13, 0) + wait(4)


def _graze(side, s):
    """False Swipe (Graze): a frisbee screams in - right past their head, by a hair - gone. One single feather
    drifts down. They're shaking."""
    sx = 1 if side == "player" else -1
    dx, dy = TARGET_FROM_ATTACKER[side]
    w = se(s["whoosh"])
    for k in range(8):
        t = k / 7
        p = (round(sx * 20 + (dx + sx * 70 - sx * 20) * t), round(30 + (dy + 44 - 30) * t + 10 * math.sin(math.pi * t)))
        w += emit_at(FRISBEE19, 1, 0, p) + wait(1)
    w += emit_at(FRISBEE19, 0, 1, (sx * 4, 44)) + se(s["swipe"])
    w += shake_defender(1, 6) + wait(10)
    w += func(34, 8, 0, 1, rgb(160, 160, 200), 12, 0) + wait(10)
    return w


def _fall_guy(side, s):
    """Substitute (Fall Guy): POOF - and a crash-test dummy is sitting where they were. Ready to take the hit."""
    at = (0, 14) if side == "player" else (0, 8)
    w = emit_at(DUMMY19, 0, 0, at) + se(s["pop"]) + flash_screen(1)
    for k in range(12):
        w += emit_at(DUMMY19, 1, 0, (at[0] + ((1, -1, 0)[k % 3] if k < 4 else 0), at[1]))
        if k == 5:
            w += se(s["bonk"])
        w += wait(1)
    return w + wait(2)


def _shady_claw(side, s):
    """Shadow Claw (Shady Claw): the lights dip - and claws rip up out of the foe's own shadow, one, two, THREE."""
    sx = 1 if side == "player" else -1
    w = func(33, 0, 1, 0, 9, rgb(40, 10, 60))
    for n, dx in enumerate((-sx * 16, sx * 14, 0)):
        for k, y in enumerate((-30, -10, 8)):
            w += emit_at(CLAWS19, n % 2, 1, (dx, y + n * 4)) + wait(1)
        w += se(s["slash"]) + shake_defender(2 + n, 2)
        if n == 2:
            w += flash_screen(3) + func(48)
        w += wait(2)
    return w + func(33, 0, 1, 9, 0, rgb(40, 10, 60)) + wait(4)


def _steel_toe(side, s):
    """Iron Tail (Steel Toe): a wrecking ball swings in off the top of the screen - WHAM - and swings back out."""
    sx = 1 if side == "player" else -1
    pivot = (-sx * 50, 120)
    path = []
    for a in (-60, -40, -20, -6, 0):
        r = math.radians(a)
        path.append((round(pivot[0] - sx * 100 * math.sin(r)), round(pivot[1] - 100 * math.cos(r))))
    w = se(s["whoosh"])
    for p in path:                                                             # *swiiing*
        w += emit_at(WRECK19, 1, 1, (p[0] + sx * 50, p[1])) + wait(1)
    w += emit_at(WRECK19, 0, 1, (0, 8)) + se(s["kaboom"]) + se(s["bslam"]) + flash_screen(5)    # WHAM
    w += func(68, 6, 4, 1, 4, 0) + shake_defender(4, 3) + func(48)
    for p in reversed(path[:-1]):
        w += emit_at(WRECK19, 1, 1, (p[0] + sx * 50, p[1])) + wait(1)
    return w + wait(4)


def _hidden_strap(side, s):
    """Hidden Power (Hidden Strap): a teddy bear sits there... innocent... wobble... RIIIP - and a STRAP rises out
    of the stuffing. BLAP. BLAP. BLAP."""
    sx = 1 if side == "player" else -1
    bear = (sx * 30, 26) if side == "player" else (-34, 10)
    gun = (bear[0] + sx * 4, bear[1] + 26)
    tip = (gun[0] + sx * 20, gun[1] + 6)
    G = (PISTOL19, 1 if side == "player" else 2)
    B = lambda: emit_at(TEDDY19, 2, 0, bear)
    w = se(s["bonk"]) + _hold(TEDDY19, 1, 0, bear, 4)
    for k in range(4):                                                         # *wobble*
        w += emit_at(TEDDY19, 1, 0, (bear[0] + (2 if k % 2 else -2), bear[1])) + wait(1)
    w += emit_at(TEDDY19, 0, 0, (bear[0], bear[1] + 6)) + se(s["slash"]) + flash_screen(2)    # RIIIP
    for k, y in enumerate((-8, 4, 14, 20)):                                    # the strap comes out
        w += emit_at(*G, 0, (gun[0], gun[1] + y - 20)) + B() + wait(1)
    w += se(s["disable"]) + _hold(*G, 0, gun, 3, lambda k: B())                # *chk-chk*
    for n, sound in enumerate(("boom", "sshot", "boom")):                      # BLAP. BLAP. BLAP.
        w += emit_at(*G, 0, (gun[0] - sx * 3, gun[1] + 2)) + B()
        w += emit_at(PISTOL19, 0, 0, tip) + emit_at(ORBS19, 0 if side == "player" else 1, 0, tip)
        w += se(s[sound]) + flash_screen(2 if n < 2 else 5) + wait(1)
        w += emit_at(*G, 0, gun) + B() + shake_defender(2 + n, 2)
        if n == 2:
            w += func(48) + func(68, 3, 3, 1, 3, 0)
        w += wait(1) + _hold(*G, 0, gun, 3, lambda k: B())
    return w + _hold(*G, 0, gun, 3, lambda k: B())


def _bullet_spray(side, s):
    """Bullet Seed (Bullet Spray): a bag of sunflower seeds - and they spit 'em like a machine gun."""
    sx = 1 if side == "player" else -1
    bag = (sx * 28, 26) if side == "player" else (-30, 8)
    w = se(s["bonk"]) + _hold(SEEDS19, 1, 0, bag, 3)
    w += emit_at(SEEDFX19, 0 if side == "player" else 1, 0, (6 * sx, 40 if side == "player" else 32))
    for k in range(18):                                                        # ptu-ptu-ptu-ptu
        w += emit_at(SEEDS19, 1, 0, bag) + se(s["peck"] if k % 2 else s["bonk"])
        if k >= 4 and k % 2 == 0:
            w += shake_defender(1, 1)
        w += wait(1)
    return w + func(48) + wait(4)


def _rock_pile(side, s):
    """Rock Tomb (Rock Pile): beep... beep... beep... a dump truck backs right up to the foe - tips - and
    BURIES them in gravel."""
    sx = 1 if side == "player" else -1
    lvl, tip = ((TRUCKL19, 0), (TRUCKL19, 1)) if side == "player" else ((TRUCK19, 1), (TRUCK19, 2))
    spot = (-sx * 46, 30) if side == "player" else (48, 34)
    w = []
    for k in range(6):                                                         # beep... beep...
        w += emit_at(*lvl, 1, (spot[0] - sx * (50 - k * 10), spot[1]))
        if k % 2 == 0:
            w += se(s["alarm"])
        w += wait(1)
    w += _hold(*lvl, 1, spot, 2) + se(s["harden"])
    w += emit_at(GRAVEL19, 0, 1, (0, 30)) + se(s["rollout"])
    for k in range(10):                                                        # *buried*
        w += emit_at(*tip, 1, spot)
        if k % 3 == 0:
            w += func(68, 1, 2, 1, 2, 0) + shake_defender(2, 1) + func(34, 8, 0, 1, rgb(150, 140, 130), 12 + k // 3, 0)
        w += wait(1)
    w += emit_at(TRUCK19, 0, 1, (0, 0)) + se(s["bslam"]) + func(48) + _hold(*lvl, 1, spot, 3)
    return w + wait(2)


def _overcook(side, s):
    """Overheat (Overcook): the toaster's glowing - ding - two charcoal slices fly out - black smoke - the smoke
    alarm going OFF - and the whole cloud rolls over the foe."""
    sx = 1 if side == "player" else -1
    t = (sx * 30, 28) if side == "player" else (-34, 10)
    alarm = _mid(side, .5, 80)
    w = se(s["burn2"])
    for k in range(6):
        w += emit_at(TOAST19, 1, 0, t) + (emit_at(TOAST19, 0, 0, (t[0], t[1] + 14)) if k % 2 else []) + wait(1)
    w += emit_at(SMOKE19, 1, 0, (t[0], t[1] + 18)) + emit_at(SMOKE19, 0, 0, (t[0], t[1] + 16)) + se(s["pop"]) + flash_screen(2)
    for k in range(14):                                                        # BEEP BEEP BEEP
        w += emit_at(TOAST19, 2, 0, t) + emit_at(TOAST19, 3, 0, (alarm[0], alarm[1] + _l3(.7)))
        if k % 3 == 0:
            w += se(s["alarm"])
        if k >= 6 and k % 2 == 0:
            w += func(34, 8, 0, 1, rgb(60, 50, 50), 13, 0) + shake_defender(1, 2)
        w += wait(1)
    return w + func(48) + wait(4)


def _energy_drink(side, s):
    """Energy Ball (Energy Drink): crack - glug glug glug - the eye twitch - and they fire a ball of pure caffeine
    at the foe."""
    sx = 1 if side == "player" else -1
    can = (sx * 30, 26) if side == "player" else (-30, 22)
    w = se(s["pop"]) + emit_at(CAN19, 0, 0, (can[0], can[1] + 30)) + _hold(CAN19, 1, 0, can, 2)
    for k in range(6):                                                         # glug glug glug
        w += emit_at(CAN19, 1, 0, (can[0] - sx * 8, can[1] + 8 + (k % 2) * 2))
        if k % 2 == 0:
            w += se(s["absorb"])
        w += wait(1)
    for k in range(6):                                                         # *twitch*
        w += shake_attacker(2, 1) + func(34, 2, 0, 1, rgb(120, 255, 60), 12, 0) + wait(1)
    w += emit_at(GREEN19, 0 if side == "player" else 1, 0, (sx * 24, 28 if side == "player" else 24)) + se(s["zen"])
    w += wait_frames(14) + flash_screen(3) + se(s["bslam"]) + func(34, 8, 0, 1, rgb(120, 255, 60), 13, 0)
    return w + shake_defender(3, 3) + func(48) + wait(6)


def _dream_talk(side, s):
    """Sleep Talk (Dream Talk): nightcap on, out cold - mumbling nonsense - and they swing at the foe IN THEIR
    SLEEP."""
    sx = 1 if side == "player" else -1
    head = (0, 54) if side == "player" else (0, 42)
    bub = (sx * 26, head[1] + 20)
    cap = lambda: emit_at(SLEEP19, 1, 0, head)
    w = emit_at(SLEEP19, 0, 0, (sx * 10, head[1] + 10)) + se(s["sleep"])
    for k in range(10):                                                        # mumble mumble
        w += cap() + (emit_at(SLEEP19, 2, 0, bub) if k >= 3 else [])
        if k == 4:
            w += se(s["confuse"])
        w += wait(1)
    dx, dy = TARGET_FROM_ATTACKER[side]
    w += bmove(side, 258, 4, round(dx * .45), round(dy * .3)) + cap() + wait(1) + cap() + wait(1)   # *sleep-swings*
    w += se(s["bonk"]) + flash_screen(2) + shake_defender(3, 2) + func(48) + cap() + wait(1)
    w += bmove(side, 258, 6, -round(dx * .45), -round(dy * .3))
    for k in range(5):
        w += cap() + wait(1)
    return w + wait(2)


def _trade_spots(side, s):
    """Skill Swap (Trade Spots): they hold up their cards - the cards fly across and swap - then the two of them
    literally TRADE SPOTS. ...And back."""
    dx, dy = TARGET_FROM_ATTACKER[side]
    a, f = (16, 40), (dx - 16, dy + 40)
    w = se(s["bling"])
    for k in range(3):
        w += emit_at(CARDS19, 1, 0, a) + emit_at(CARDS19, 2, 0, f) + wait(1)
    for t in (.25, .5, .75, 1):                                                # the cards trade
        w += emit_at(CARDS19, 1, 0, (round(a[0] + (f[0] - a[0]) * t), round(a[1] + (f[1] - a[1]) * t + 14 * math.sin(math.pi * t))))
        w += emit_at(CARDS19, 2, 0, (round(f[0] + (a[0] - f[0]) * t), round(f[1] + (a[1] - f[1]) * t - 14 * math.sin(math.pi * t))))
        w += wait(1)
    w += emit_at(CARDS19, 0, 0, a) + emit_at(CARDS19, 0, 0, f) + se(s["swipe"])
    w += bmove(side, 258, 10, dx, dy) + bmove(side, 264, 10, -dx, -dy) + wait(7)   # TRADE SPOTS
    w += se(s["bonk"]) + flash_screen(2) + wait(6)
    w += bmove(side, 258, 10, -dx, -dy) + bmove(side, 264, 10, dx, dy) + wait(7)   # ...nah
    return w + wait(2)


def _big_blast(side, s):
    """Focus Blast (Big Blast): a firework mortar - the fuse sizzling... sizzling... - THOOMP - and a whole Fourth
    of July goes off on the foe."""
    sx = 1 if side == "player" else -1
    m = (sx * 30, 26) if side == "player" else (-34, 8)
    w = se(s["bonk"]) + _hold(MORTAR19, 1, 0, m, 2) + se(s["ember"])
    for k in range(8):                                                         # sizzle...
        w += emit_at(MORTAR19, 1, 0, m) + (emit_at(MORTAR19, 0, 0, (m[0] + sx * 18, m[1] - 2)) if k % 2 else []) + wait(1)
    w += se(s["kaboom"]) + func(68, 2, 2, 1, 2, 0)                             # THOOMP
    for p in _arc((m[0], m[1] + 20), _foe_at(side, (0, 30)), 5, 40)[1:]:
        w += emit_at(MORTAR19, 1, 0, m) + emit_at(MORTAR19, 0, 0, p) + wait(1)
    w += emit_at(FIREWORK19, 0, 1, (0, 30)) + emit_at(FIREWORK19, 1, 1, (0, 30)) + se(s["explo"]) + flash_screen(6)
    for k in range(4):
        w += func(34, 8, 0, 1, (rgb(255, 60, 120), rgb(120, 255, 255), rgb(255, 220, 40), rgb(255, 255, 255))[k], 13, 0)
        w += shake_defender(2, 1) + wait(2)
    return w + func(48) + wait(4)


def _dumpster_dive(side, s):
    """Recycle (Dumpster): the blue recycling bin - rummage, rummage - a banana flies out - junk everywhere -
    FOUND IT. Good as new."""
    sx = 1 if side == "player" else -1
    bin_ = (sx * 30, 26) if side == "player" else (-34, 12)
    w = se(s["bonk"]) + _hold(BIN19, 1, 0, bin_, 2)
    for k in range(10):                                                        # *rummage*
        w += emit_at(BIN19, 1, 0, (bin_[0] + (2 if k % 2 else -2), bin_[1]))
        if k % 2 == 0:
            w += se(s["sand"])
        if k == 3:
            w += emit_at(BIN19, 2, 0, (bin_[0], bin_[1] + 20))
        if k == 6:
            w += emit_at(BIN19, 3, 0, (bin_[0], bin_[1] + 20 + _l3(.5)))
        w += wait(1)
    w += emit_at(BIN19, 0, 0, (bin_[0], bin_[1] + 34)) + se(s["chaching"]) + func(34, 2, 0, 1, rgb(255, 220, 60), 13, 0)
    return w + _hold(BIN19, 1, 0, bin_, 4)


def _snack_grab(side, s):
    """Pluck (Snack Grab): the foe's berry, just sitting there - a reacher-grabber stretches all the way over -
    snap - and it's gone. Munch."""
    sx = 1 if side == "player" else -1
    op, sh = ((GRAB19, 1), (GRAB19, 2)) if side == "player" else ((GRABL19, 0), (GRABL19, 1))
    berry = (-sx * 30, 8 + _l3(.5)) if side == "player" else (30, 18 + _l3(.5))
    w = emit_at(GRAB19, 0, 1, (berry[0], berry[1] - _l3(.5) + 6)) + _hold(GRAB19, 3, 1, berry, 3)
    dx, dy = TARGET_FROM_ATTACKER[side]
    tip = (dx + berry[0] - sx * 36, dy + berry[1] - _l3(.5))
    for t in (0, .3, .6, .85, 1):                                              # *streeetch*
        p = (round(sx * 20 + (tip[0] - sx * 20) * t), round(20 + (tip[1] - 20) * t))
        w += emit_at(*op, 0, p) + emit_at(GRAB19, 3, 1, berry) + wait(1)
    w += se(s["disable"]) + emit_at(*sh, 0, tip) + wait(1)                     # snap
    for t in (.7, .4, .1):
        w += emit_at(*sh, 0, (round(sx * 20 + (tip[0] - sx * 20) * t), round(20 + (tip[1] - 20) * t))) + wait(1)
    w += se(s["absorb"]) + func(34, 2, 0, 1, rgb(140, 120, 255), 12, 0) + shake_defender(1, 2) + wait(6)
    return w


def _snow_plow(side, s):
    """Avalanche (Snow Plow): the city plow comes through, light bar flashing - pushing a WALL of snow - and dumps
    the whole thing on the foe."""
    sx = 1 if side == "player" else -1
    res = 1 if side == "player" else 2
    dx, dy = TARGET_FROM_ATTACKER[side]
    w = se(s["rollout"])
    for k in range(8):
        t = k / 7
        p = (round(-sx * 50 + (dx - sx * 44 + sx * 50) * t), round(10 + (dy + 4 - 10) * t))
        w += emit_at(PLOW19, res, 0, p) + emit_at(PLOW19, 0, 0, (p[0] + sx * 30, p[1] - 6))
        if k % 3 == 0:
            w += se(s["alarm"])
        w += wait(1)
    w += emit_at(SNOWWALL19, 0, 1, (0, 10)) + se(s["blizzard"]) + flash_screen(3) + func(68, 4, 3, 1, 3, 0)
    w += func(34, 8, 0, 1, rgb(240, 245, 255), 15, 0) + shake_defender(3, 3) + func(48)
    w += _hold(PLOW19, res, 1, (-sx * 44, 4), 6)
    return w + wait(2)


def _slow_mo(side, s):
    """Trick Room (Slow Mo): the remote - SLOW - *click* - the whole screen goes sepia and ripples, everybody
    moving like they're underwater... then back."""
    sx = 1 if side == "player" else -1
    r = (sx * 32, 34) if side == "player" else (-32, 26)
    w = se(s["bonk"]) + _hold(REMOTE19, 1, 0, r, 3) + se(s["disable"])
    w += func(33, 0, 1, 0, 9, rgb(190, 150, 90)) + emit_at(REMOTE19, 0, 0, _mid(side, .5, 20)) + emit_at(SEPIA19, 0, 1, (0, 20))
    w += se(s["psych"])
    w += bmove(side, 258, 24, 0, 6) + bmove(side, 264, 24, 0, 6)              # *slooooow*
    for k in range(12):
        w += emit_at(REMOTE19, 1, 0, r) + wait(1)
    w += bmove(side, 258, 24, 0, -6) + bmove(side, 264, 24, 0, -6)
    for k in range(12):
        w += emit_at(REMOTE19, 1, 0, r) + wait(1)
    w += func(33, 0, 1, 9, 0, rgb(190, 150, 90)) + wait(4)
    return w


def _flash_bang(side, s):
    """Flash Cannon (Flash Bang): a disposable camera - click... click... - FLASH - the foe sees spots for the
    rest of the week."""
    sx = 1 if side == "player" else -1
    cam = (sx * 30, 30) if side == "player" else (-30, 26)
    w = se(s["bonk"]) + _hold(CAMERA19, 1, 0, cam, 2)
    for k in range(2):                                                         # click... click...
        w += emit_at(CAMERA19, 1, 0, cam) + emit_at(CAMERA19, 0, 0, (cam[0] - sx * 8, cam[1] + 6)) + se(s["disable"]) + flash_screen(1)
        w += wait(1) + _hold(CAMERA19, 1, 0, cam, 3)
    w += emit_at(FLASH19, 1, 1, (0, 20)) + se(s["bling"]) + flash_screen(8) + func(48)   # FLASH
    w += emit_at(FLASH19, 0, 1, (0, 24))
    for k in range(10):                                                        # seeing spots
        w += emit_at(CAMERA19, 1, 0, cam)
        if k % 3 == 0:
            w += shake_defender(1, 2) + func(34, 8, 0, 1, rgb(255, 255, 255), 12, 0)
        w += wait(1)
    return w + wait(4)


def _hit_the_gym(side, s):
    """Bulk Up (Hit the Gym): kettlebell swings - one - two - THREE - sweat flying - towel over the shoulder -
    flex."""
    sx = 1 if side == "player" else -1
    base = (sx * 26, 10) if side == "player" else (-26, 6)
    w = []
    for n in range(3):                                                         # swing, swing, SWING
        for y in (0, 16, 30, 16):
            w += emit_at(GYM19, 1, 0, (base[0] + sx * (y // 3), base[1] + y))
            if y == 30:
                w += se(s["whoosh"]) + emit_at(GYM19, 0, 0, (0, 40))
            w += wait(1)
    w += se(s["bonk"]) + _hold(GYM19, 1, 0, base, 1)
    tow = (-sx * 14, 44) if side == "player" else (14, 34)
    w += se(s["focus"])
    for k in range(8):                                                         # *flex*
        w += emit_at(GYM19, 2, 0, tow) + emit_at(GYM19, 1, 0, base)
        if k in (0, 4):
            w += bmove(side, 258, 2, 0, 5) + func(34, 2, 0, 1, rgb(255, 60, 40), 13, 0)
        if k in (2, 6):
            w += bmove(side, 258, 2, 0, -5)
        w += wait(1)
    return w + wait(2)


# ------------------------------------------------------------------ set 20: last TMs + level-up

def _sx(side):
    return 1 if side == "player" else -1


def _clown_on(side, s):
    """Torment (Clown On): a red clown nose lobbed onto the foe's face - BOINK - then two bike horns honk at
    them from both sides. HONK HONK. Confetti."""
    sx = _sx(side)
    w = se(s["whoosh"]) + _lob(CLOWN20, 1, side, (sx * 22, 30), _foe_at(side, (-sx * 4, 14)), 5, 22)
    w += se(s["bonk"]) + shake_defender(1, 2)
    for k in range(10):
        w += emit_at(CLOWN20, 1, 1, (-sx * 4, 14))
        if k in (2, 6):                                                        # HONK
            w += emit_at(CLOWN20, 2, 1, (-34, 26 + _l3(0))) + se(s["alarm"]) + shake_defender(2, 1)
        if k in (4, 8):                                                        # HONK
            w += emit_at(CLOWN20, 3, 1, (34, 26 + _l3(.9))) + se(s["alarm"]) + shake_defender(2, 1)
        w += wait(1)
    w += emit_at(CLOWN20, 0, 1, (0, 30)) + se(s["pop"]) + func(34, 8, 0, 1, rgb(255, 80, 160), 12, 0)
    return w + _hold(CLOWN20, 1, 1, (-sx * 4, 14), 4)


def _swipe(side, s):
    """Snatch (Swipe): a card reader pops up by the foe - the attacker's card slides through - beep... beep...
    APPROVED. Their stuff is the attacker's now."""
    sx = _sx(side)
    rd = (-sx * 30, 30) if side == "player" else (30, 34)
    w = se(s["bonk"]) + _hold(SWIPE20, 1, 1, rd, 2)
    for k in range(6):                                                         # *swiiipe*
        w += emit_at(SWIPE20, 3, 1, (rd[0] + sx * (-20 + k * 8), rd[1] + 14 + _l3(.5) - k * 2))
        w += emit_at(SWIPE20, 1, 1, rd) + (se(s["swipe"]) if k == 0 else []) + wait(1)
    for k in range(2):                                                         # beep... beep...
        w += se(s["lockon"]) + _hold(SWIPE20, 1, 1, rd, 2)
    w += emit_at(SWIPE20, 0, 1, (rd[0], rd[1] + 20)) + se(s["chaching"]) + flash_screen(2)
    w += _hold(SWIPE20, 2, 1, rd, 8, lambda k: func(34, 2, 0, 1, rgb(80, 255, 120), 12, 0) if k == 3 else [])
    return w + wait(2)


def _one_punch(side, s):
    """Focus Punch (One Punch): an arcade punch machine - wind up - wind up - POW - the score rolls to 999 and
    the foe takes the whole punch."""
    sx = _sx(side)
    m = (sx * 40, 20) if side == "player" else (-40, 18)
    w = se(s["focus"]) + _hold(PUNCHM20, 1, 0, m, 3)
    for k in range(2):                                                         # wind up...
        w += bmove(side, 258, 3, -sx * 8, 0) + _hold(PUNCHM20, 1, 0, m, 1)
        w += bmove(side, 258, 3, sx * 8, 0) + _hold(PUNCHM20, 1, 0, m, 1)
    w += bmove(side, 258, 2, sx * 16, 0) + se(s["bslam"]) + flash_screen(3)   # POW
    w += emit_at(PUNCHM20, 0, 0, (m[0], m[1] + 30)) + bmove(side, 258, 3, -sx * 16, 0)
    for k in range(5):
        w += emit_at(PUNCHM20, 1 if k % 2 else 2, 0, m) + se(s["clock"]) + wait(1)
    w += se(s["chaching"]) + emit_at(PUNCHM20, 2, 0, m) + emit_at(PUNCHM20, 0, 1, (0, 20)) + se(s["kaboom"])
    w += shake_defender(4, 3) + func(68, 4, 4, 1, 3, 0) + func(48)
    return w + _hold(PUNCHM20, 2, 0, m, 6)


def _tax_punch(side, s):
    """Drain Punch (Tax Punch): a piggy bank shows up - the punch lands - coins fly out the foe and back into
    the pig. Taxes, playa."""
    sx = _sx(side)
    pig = (-sx * 6, 50) if side == "player" else (4, 46)
    w = se(s["bonk"]) + _hold(PIGGY20, 1, 0, pig, 2)
    w += bmove(side, 258, 2, sx * 14, 4) + emit_at(PIGGY20, 1, 0, pig) + se(s["bslam"]) + flash_screen(2)
    w += shake_defender(3, 2) + bmove(side, 258, 3, -sx * 14, -4)
    w += emit_at(COINS20, 0 if side == "player" else 1, 1, (0, 14))
    for k in range(14):
        w += emit_at(PIGGY20, 1, 0, pig)
        if k % 3 == 0:
            w += se(s["chaching"] if k % 2 else s["bling"])
        if k % 4 == 1:
            w += func(34, 8, 0, 1, rgb(255, 210, 60), 12, 0)
        w += wait(1)
    w += emit_at(PIGGY20, 0, 0, (pig[0], pig[1] + 12)) + se(s["absorb"]) + func(34, 2, 0, 1, rgb(255, 230, 90), 12, 0)
    return w + _hold(PIGGY20, 1, 0, pig, 4)


def _iron_wing(side, s):
    """Steel Wing (Iron Wing): a giant clothes iron flies in - PSSSHHT - presses the foe flat. Crease-free."""
    sx = _sx(side)
    res = 1 if side == "player" else 2
    w = se(s["whoosh"]) + stop_motion(IRON20, res, 1, (-sx * 80, 60), (0, 34), 5, ease=1.4)
    for k in range(3):                                                         # press... press... press
        w += emit_at(IRON20, res, 1, (0, 26)) + se(s["bslam"]) + shake_defender(2, 1) + bmove(side, 264, 2, 0, -4)
        w += emit_at(IRON20, 0, 1, (0, 12)) + se(s["smoke"]) + wait(1)
        w += emit_at(IRON20, res, 1, (0, 36)) + bmove(side, 264, 2, 0, 4) + wait(1)
    w += func(34, 8, 0, 1, rgb(230, 230, 240), 13, 0) + func(48)
    return w + _hold(IRON20, res, 1, (0, 38), 3) + wait(2)


def _flashbang_switch(side, s):
    """Flash (Flashbang): a light switch on the wall - click - a giant bulb over the foe - the whole screen goes
    WHITE."""
    sx = _sx(side)
    sw = (sx * 28, 44) if side == "player" else (-28, 38)
    w = _hold(LIGHT20, 1, 0, sw, 4) + se(s["disable"]) + _hold(LIGHT20, 2, 0, sw, 2)
    w += emit_at(LIGHT20, 3, 1, (0, 66 + _l3(1.2))) + wait(2)
    w += emit_at(LIGHT20, 0, 1, (0, 50)) + se(s["zap"]) + flash_screen(10) + func(33, 0, 1, 0, 12, rgb(255, 255, 240))
    for k in range(6):
        w += emit_at(LIGHT20, 2, 0, sw) + emit_at(LIGHT20, 3, 1, (0, 66 + _l3(1.2))) + wait(1)
    w += func(34, 8, 0, 1, rgb(255, 255, 230), 14, 0) + shake_defender(1, 3)
    return w + func(33, 0, 1, 12, 0, rgb(255, 255, 240)) + wait(6)


def _rock_trap(side, s):
    """Stealth Rock (Rock Trap): LEGO bricks scattered all over the foe's side - they step on one - OWWW -
    hop - another one."""
    sx = _sx(side)
    spots = [(-30, -4), (-10, -10), (12, -6), (32, -10), (-20, -18), (24, -18)]
    w = se(s["sand"])
    for k, p in enumerate(spots):                                              # *clatter*
        w += _lob(LEGO20, 1, side, (sx * 18, 26), _foe_at(side, p), 3, 14)
        w += se(s["bonk"])
    lay = lambda: sum((emit_at(LEGO20, 1, 1, p) for p in spots), [])
    for k in range(10):
        w += lay()
        if k in (2, 6):                                                        # OWWW
            w += emit_at(LEGO20, 0, 1, (0, 0)) + se(s["crack"]) + bmove(side, 264, 2, 0, 10) + shake_defender(2, 1)
        if k in (4, 8):
            w += bmove(side, 264, 2, 0, -10)
        w += wait(1)
    return w + func(34, 8, 0, 1, rgb(255, 80, 60), 12, 0) + wait(2)


def _trip_wire(side, s):
    """Grass Knot (Trip Wire): the foe's shoelaces tie themselves together - they take a step - faceplant."""
    sx = _sx(side)
    w = se(s["vwhip"]) + _hold(LACES20, 1, 1, (0, -4), 4) + se(s["vwhip2"]) + _hold(LACES20, 1, 1, (0, -4), 4)
    w += bmove(side, 264, 3, -sx * 6, 6) + _hold(LACES20, 1, 1, (-sx * 6, 0), 1)             # *step*...
    w += bmove(side, 264, 2, -sx * 14, -18) + se(s["bslam"]) + emit_at(LACES20, 0, 1, (-sx * 20, -16))
    w += flash_screen(2) + shake_defender(3, 3) + func(68, 3, 3, 1, 2, 0) + _hold(LACES20, 1, 1, (-sx * 14, -10), 8)
    return w + bmove(side, 264, 5, sx * 20, 12) + wait(2)


def _grudge(side, s):
    """Frustration (Grudge): a pressure gauge on the attacker - needle creeping - into the RED - steam blows
    out the top - then they let it ALL out."""
    sx = _sx(side)
    g = (-sx * 6, 54) if side == "player" else (6, 50)
    w = se(s["rage"])
    for k in range(8):                                                         # *creeping*
        w += emit_at(GAUGE20, 1 if k < 5 else 2, 0, g) + (shake_attacker(1, 1) if k > 4 else []) + wait(1)
    w += emit_at(STEAM20, 0, 0, (g[0], g[1] + 18)) + se(s["fwoosh"]) + func(34, 2, 0, 1, rgb(255, 40, 30), 14, 0)
    for k in range(8):
        w += emit_at(GAUGE20, 2, 0, g) + (se(s["smoke"]) if k == 3 else []) + wait(1)
    w += bmove(side, 258, 2, sx * 14, 4) + emit_at(GAUGE20, 0, 1, (0, 20)) + se(s["kaboom"]) + flash_screen(3)
    return w + shake_defender(4, 3) + func(48) + bmove(side, 258, 3, -sx * 14, -4) + wait(4)


def _front(side, s):
    """Facade (Front): a big Lambo rolls up next to the attacker - stuntin' - then the wind blows it over.
    It's cardboard. It was always cardboard. They hit anyway."""
    sx = _sx(side)
    car = (-sx * 26, 24) if side == "player" else (26, 16)
    w = se(s["bass"]) + stop_motion(FRONT20, 1, 0, (car[0] - sx * 70, car[1]), car, 5, ease=.8)
    w += se(s["bling"]) + _hold(FRONT20, 1, 0, car, 6, lambda k: bmove(side, 258, 2, 0, 4 if k % 2 == 0 else -4) if k < 4 else [])
    w += se(s["gust"]) + _hold(FRONT20, 1, 0, (car[0] + sx * 2, car[1]), 2)
    w += emit_at(FRONT20, 2, 0, car) + emit_at(FRONT20, 0, 0, car) + se(s["flop"]) + _hold(FRONT20, 2, 0, car, 6)
    w += bmove(side, 258, 2, sx * 14, 4) + emit_at(FRONT20, 0, 1, (0, 10)) + se(s["bslam"]) + shake_defender(3, 2)
    return w + func(48) + bmove(side, 258, 3, -sx * 14, -4) + _hold(FRONT20, 2, 0, car, 3)


def _inside_job(side, s):
    """Secret Power (Inside Job): a wall safe by the foe - dial spinning - click - it swings open and a spring
    boxing glove BOINGS out. Inside job."""
    sx = _sx(side)
    sf = (-sx * 36, 30) if side == "player" else (36, 34)
    w = _hold(SAFE20, 1, 1, sf, 2)
    for k in range(3):
        w += se(s["clock"]) + _hold(SAFE20, 1, 1, sf, 1)
    w += se(s["disable"]) + emit_at(SAFE20, 2, 1, sf) + emit_at(SAFE20, 0, 1, (sf[0], sf[1] + 10)) + wait(1)
    w += se(s["bslam"]) + flash_screen(2) + shake_defender(4, 2) + func(48)
    w += _hold(SAFE20, 2, 1, sf, 8, lambda k: func(34, 8, 0, 1, rgb(255, 60, 60), 12, 0) if k == 1 else [])
    return w + wait(2)


def _wall_climb(side, s):
    """Rock Climb (Wall Climb): a climbing wall shows up - the attacker climbs it - hand, hand, hand - and
    DROPS off the top onto the foe."""
    sx = _sx(side)
    wall = (-sx * 30, 26) if side == "player" else (30, 22)
    w = se(s["bonk"]) + _hold(CLIMB20, 1, 0, wall, 2)
    for k in range(4):                                                         # climb
        w += bmove(side, 258, 2, 0, 8) + emit_at(CLIMB20, 1, 0, wall) + se(s["bonk"]) + wait(1)
        w += emit_at(CLIMB20, 1, 0, wall) + wait(1)
    w += se(s["whoosh"]) + bmove(side, 258, 4, sx * 40, 0) + _hold(CLIMB20, 1, 0, wall, 2)
    w += bmove(side, 258, 2, 0, -32) + emit_at(CLIMB20, 0, 1, (0, 30)) + se(s["kaboom"]) + flash_screen(3)
    w += shake_defender(4, 3) + func(68, 4, 4, 1, 2, 0) + func(48)
    return w + bmove(side, 258, 5, -sx * 40, 0) + wait(4)


def _fake_pass(side, s):
    """Feint (Fake Pass): the attacker cocks back - pump fake - pump fake - the foe looks the wrong way - BONK,
    the football hits them in the head."""
    sx = _sx(side)
    hand = (-sx * 6, 40) if side == "player" else (6, 36)
    w = []
    for k in range(2):                                                         # pump fake
        w += emit_at(FOOTB20, 1, 0, hand) + bmove(side, 258, 2, -sx * 6, 0) + wait(1)
        w += emit_at(FOOTB20, 1, 0, (hand[0] + sx * 8, hand[1] + 4)) + bmove(side, 258, 2, sx * 6, 0)
        w += se(s["whoosh"]) + shake_defender(2, 1) + wait(1)
    w += _hold(FOOTB20, 1, 0, hand, 3)
    w += se(s["whoosh"]) + _lob(FOOTB20, 1, side, hand, _foe_at(side, (0, 34)), 5, 20,
                                lambda k: emit_at(FOOTB20, 0, 0, hand) if k == 0 else [])
    w += se(s["bonk"]) + flash_screen(2) + shake_defender(3, 2) + func(48)
    return w + _lob(FOOTB20, 1, side, _foe_at(side, (0, 34)), _foe_at(side, (sx * 30, 60)), 4, 10) + wait(2)


def _smoke_screen(side, s):
    """Mist (Smoke Screen): fog machines on both sides of the attacker - club lights - and the stage fills with
    fog until you can't see a thing."""
    sx = _sx(side)
    l, r = (-36, 26), (40, 26)
    w = se(s["bass"]) + emit_at(FOG20, 0, 0, (0, 20))
    for k in range(4):
        w += emit_at(FOG20, 1, 0, l) + emit_at(FOG20, 2, 0, r) + wait(1)
    w += emit_at(FOGFX20, 0, 0, (l[0] + 14, l[1] + 6)) + emit_at(FOGFX20, 1, 0, (r[0] - 14, r[1] + 6)) + se(s["haze"])
    for k in range(18):
        w += emit_at(FOG20, 1, 0, l) + emit_at(FOG20, 2, 0, r)
        if k % 6 == 0:
            w += se(s["bass"]) + func(34, 2, 0, 1, rgb(200, 120, 255), 10, 0)
        w += wait(1)
    return w + func(33, 0, 1, 0, 8, rgb(220, 220, 235)) + wait(4) + func(33, 0, 1, 8, 0, rgb(220, 220, 235))


def _plug_in(side, s):
    """Charge (Plug In): a guitar amp - they plug in - and hit ONE power chord. The amp shakes the screen and
    they're charged."""
    sx = _sx(side)
    amp = (-sx * 36, 28) if side == "player" else (36, 14)
    w = se(s["bonk"]) + _hold(AMP20, 1, 0, amp, 3) + se(s["zap"]) + _hold(AMP20, 1, 0, amp, 2)
    w += emit_at(AMPFX20, 0, 0, (amp[0], amp[1] + 14)) + emit_at(AMPFX20, 1, 0, (0, 10)) + se(s["thunder"])
    w += se(s["bass"]) + flash_screen(4) + func(68, 3, 3, 1, 4, 0)
    for k in range(12):
        w += emit_at(AMP20, 1, 0, (amp[0] + (1 if k % 2 else -1), amp[1]))
        if k % 3 == 0:
            w += emit_at(AMP20, 0, 0, (amp[0], amp[1] + 20)) + func(34, 2, 0, 1, rgb(255, 240, 80), 12, 0)
        w += wait(1)
    return w + _hold(AMP20, 1, 0, amp, 2)


def _bed_bugs(side, s):
    """Bug Bite (Bed Bugs): a cheap motel pillow - the attacker fluffs it - a swarm of bed bugs pours out and
    swarms the foe. Itchy."""
    sx = _sx(side)
    pil = (sx * 20, 30) if side == "player" else (-20, 26)
    w = se(s["bonk"])
    for k in range(4):                                                         # *fluff fluff*
        w += emit_at(BUGS20, 1, 0, (pil[0], pil[1] + (3 if k % 2 else 0))) + (se(s["flop"]) if k % 2 else []) + wait(1)
    w += emit_at(BUGFX20, 0 if side == "player" else 1, 0, (pil[0], pil[1] + 6)) + se(s["psting"])
    for k in range(14):
        w += emit_at(BUGS20, 1, 0, pil)
        if k > 7 and k % 2 == 0:
            w += shake_defender(1, 1) + se(s["bite"])
        w += wait(1)
    return w + func(34, 8, 0, 1, rgb(200, 60, 60), 12, 0) + wait(4)


def _squeeze_out(side, s):
    """Wring Out (Squeeze Out): the foe gets wrung like a mop over a mop bucket - squeeeeze - dirty water."""
    w = se(s["splash"]) + _hold(MOP20, 1, 1, (0, -16), 3)
    for k in range(4):                                                         # squeeeeze
        w += emit_at(MOP20, 1, 1, (0, -16)) + shake_defender(2, 1)
        w += emit_at(MOP20, 0, 1, (0, 6)) + se(s["constrict"] if k % 2 == 0 else s["splat"]) + wait(1)
        w += emit_at(MOP20, 1, 1, (0, -16)) + wait(1)
    w += func(34, 8, 0, 1, rgb(150, 140, 90), 13, 0) + func(48)
    return w + _hold(MOP20, 1, 1, (0, -16), 4)


def _loud_pack(side, s):
    """Magical Leaf (Loud Pack): a neon fanny pack unzips - and bills fly out, homing straight in on the foe."""
    sx = _sx(side)
    fp = (sx * 14, 40) if side == "player" else (-14, 36)
    w = se(s["bling"]) + _hold(FANNY20, 1, 0, fp, 3) + se(s["swipe"])
    w += emit_at(FANNY20, 2, 0, fp) + emit_at(FANNY20, 0, 0, (fp[0], fp[1] + 12))
    w += emit_at(MONEY20, 0 if side == "player" else 1, 0, (fp[0], fp[1] + 4))
    for k in range(14):
        w += emit_at(FANNY20, 2, 0, fp)
        if k % 4 == 3:
            w += se(s["chaching"]) + shake_defender(1, 1)
        w += wait(1)
    return w + func(34, 8, 0, 1, rgb(100, 220, 90), 12, 0) + _hold(FANNY20, 2, 0, fp, 3)


def _grind(side, s):
    """Endeavor (Grind): a treadmill - the attacker runs, and runs, and runs, sweat flying - then grinds the
    foe down to their level."""
    sx = _sx(side)
    tm = (sx * 6, 14) if side == "player" else (-6, 4)
    w = se(s["bonk"]) + _hold(TREAD20, 1, 0, tm, 2) + emit_at(TREAD20, 0, 0, (0, 40))
    for k in range(14):                                                        # *run run run*
        w += emit_at(TREAD20, 1, 0, tm) + bmove(side, 258, 1, 0, 3 if k % 2 else -3)
        if k % 2 == 0:
            w += se(s["rollout"] if k % 4 == 0 else s["bonk"])
        w += wait(1)
    w += se(s["focus"]) + func(34, 2, 0, 1, rgb(255, 80, 60), 13, 0) + _hold(TREAD20, 1, 0, tm, 2)
    w += bmove(side, 258, 2, sx * 16, 4) + se(s["bslam"]) + flash_screen(2) + shake_defender(3, 3)
    return w + func(48) + bmove(side, 258, 3, -sx * 16, -4) + wait(4)


def _sniff_out(side, s):
    """Odor Sleuth (Sniff Out): a deerstalker drops onto the attacker - a magnifying glass sweeps over the foe
    - green stink lines - FOUND YOU."""
    sx = _sx(side)
    w = se(s["whoosh"]) + stop_motion(SLEUTH20, 2, 0, (0, 90), (0, 44), 4, ease=1.6)
    w += se(s["bonk"]) + _hold(SLEUTH20, 2, 0, (0, 44), 2)
    w += emit_at(SLEUTH20, 0, 1, (0, 10)) + se(s["sscent"])
    for k in range(12):                                                        # *sweep*
        x = (-24, -8, 8, 24, 8, -8)[k % 6]
        w += emit_at(SLEUTH20, 2, 0, (0, 44)) + emit_at(SLEUTH20, 1, 1, (x, 18 + (k % 3) * 2))
        if k % 4 == 0:
            w += se(s["leer"])
        w += wait(1)
    w += se(s["lockon"]) + flash_screen(2) + func(34, 8, 0, 1, rgb(160, 220, 60), 13, 0)
    return w + _hold(SLEUTH20, 1, 1, (0, 18), 4, lambda k: emit_at(SLEUTH20, 2, 0, (0, 44)))


def _hide_out(side, s):
    """Withdraw (Hide Out): the attacker ducks behind a potted ficus - leaves rustle - two eyes peek out. Hidin'."""
    sx = _sx(side)
    pl = (sx * 4, 6)
    w = se(s["leaf"]) + bmove(side, 258, 3, -sx * 6, -6) + emit_at(FICUS20, 0, 0, (pl[0], pl[1] + 30))
    for k in range(14):
        w += emit_at(FICUS20, 1, 0, (pl[0] + (1 if k in (2, 3, 9) else 0), pl[1]))
        if k in (5, 6, 7, 11, 12):                                             # *peek*
            w += emit_at(FICUS20, 2, 0, (pl[0] + sx * (8 if k < 9 else -8), pl[1] + 30))
        if k == 5:
            w += se(s["leer"])
        w += wait(1)
    w += func(34, 2, 0, 1, rgb(120, 220, 120), 12, 0) + _hold(FICUS20, 1, 0, pl, 3)
    return w + bmove(side, 258, 3, sx * 6, 6)


def _rock_candy(side, s):
    """Power Gem (Rock Candy): a giant rock candy stick - it sparkles - and fires a pink sugar beam at the foe."""
    sx = _sx(side)
    rc = (sx * 18, 36) if side == "player" else (-18, 32)
    w = se(s["bling"]) + _hold(CANDY20, 1, 0, rc, 3)
    w += emit_at(CANDY20, 0, 0, (rc[0], rc[1] + 16)) + se(s["bling"]) + _hold(CANDY20, 1, 0, rc, 2)
    w += emit_at(GEMBEAM20, 0 if side == "player" else 1, 0, (rc[0], rc[1] + 8)) + se(s["sbeam"])
    for k in range(12):
        w += emit_at(CANDY20, 1, 0, rc)
        if k > 5 and k % 2 == 0:
            w += shake_defender(1, 1) + emit_at(CANDY20, 0, 1, (0, 20))
        w += wait(1)
    return w + func(34, 8, 0, 1, rgb(255, 120, 230), 13, 0) + se(s["bling"]) + wait(4)


def _mooch(side, s):
    """Leech Life (Mooch): a giant milkshake with a straw stuck in the foe - sluuurp - the attacker drinks it."""
    sx = _sx(side)
    ms = (-sx * 30, 34) if side == "player" else (30, 30)
    w = se(s["bonk"]) + _hold(SHAKE20, 1, 1, ms, 3) + se(s["absorb"])
    for k in range(16):                                                        # sluuurp
        w += emit_at(SHAKE20, 1, 1, ms)
        if k % 4 == 0:
            w += emit_at(SHAKE20, 0, 1, (ms[0], ms[1] + 20)) + shake_defender(1, 1) + se(s["mdrain"])
        if k == 8:
            w += func(34, 8, 0, 1, rgb(255, 170, 200), 12, 0)
        w += wait(1)
    return w + func(34, 2, 0, 1, rgb(255, 180, 210), 12, 0) + se(s["absorb"]) + wait(4)


def _peep_game(side, s):
    """Detect (Peep Game): a periscope pops up - looks left - looks right - sees it all coming. Peeped."""
    sx = _sx(side)
    ps = (sx * 16, 30) if side == "player" else (-16, 26)
    w = se(s["whoosh"]) + stop_motion(SCOPE20, 1, 0, (ps[0], ps[1] - 30), ps, 3, ease=.8)
    for res in (1, 2, 1):                                                      # look... look... look
        w += _hold(SCOPE20, res, 0, ps, 3) + se(s["leer"])
    w += emit_at(SCOPE20, 0, 0, (ps[0], ps[1] + 30)) + se(s["xsense"]) + flash_screen(2)
    w += func(34, 2, 0, 1, rgb(255, 255, 200), 12, 0) + _hold(SCOPE20, 1, 0, ps, 4)
    return w + stop_motion(SCOPE20, 1, 0, ps, (ps[0], ps[1] - 30), 3, ease=1.4)


def _zaza_storm(side, s):
    """Leaf Storm (Zaza Storm): a whirlwind of green leaves kicks up off the attacker and buries the foe."""
    r = 0 if side == "player" else 1
    w = se(s["twister"]) + func(33, 0, 1, 0, 6, rgb(90, 180, 60))
    for k in range(3):                                                         # wave, wave, wave
        w += emit_at(LEAVES20, r, 0, (0, 10 + k * 8)) + se(s["leaf"]) + bmove(side, 258, 2, 0, 3) + wait(2)
        w += bmove(side, 258, 2, 0, -3) + se(s["gust"]) + wait(2)
    for k in range(12):
        if k % 3 == 0:
            w += shake_defender(2, 1) + se(s["leaf"])
        w += wait(1)
    return w + func(34, 8, 0, 1, rgb(90, 200, 70), 13, 0) + func(48) + func(33, 0, 1, 6, 0, rgb(90, 180, 60)) + wait(4)


def _dip_out(side, s):
    """Teleport (Dip Out): an EXIT door shows up - it swings open - light pours out - they're gone."""
    sx = _sx(side)
    dr = (sx * 30, 26) if side == "player" else (-30, 22)
    w = se(s["bonk"]) + _hold(EXIT20, 1, 0, dr, 4) + se(s["disable"])
    w += emit_at(EXIT20, 2, 0, dr) + emit_at(EXIT20, 0, 0, dr) + _hold(EXIT20, 2, 0, dr, 2)
    w += se(s["whoosh"]) + bmove(side, 258, 3, sx * 26, 0) + func(40, 2, 1) + _hold(EXIT20, 2, 0, dr, 3)
    w += se(s["bonk"]) + _hold(EXIT20, 1, 0, dr, 4) + bmove(side, 258, 1, -sx * 26, 0)
    return w + func(40, 2, 0) + wait(2)


def _mouthwash_spit(side, s):
    """Spit Up (Spit Bars): the attacker swigs mouthwash - gargles - and SPITS a blue stream at the foe."""
    sx = _sx(side)
    mw = (sx * 10, 46) if side == "player" else (-10, 40)
    w = se(s["bonk"]) + _hold(MOUTH20, 1, 0, mw, 3)
    for k in range(6):                                                         # *gargle*
        w += emit_at(MOUTH20, 1, 0, mw) + shake_attacker(1, 1) + (emit_at(MOUTH20, 0, 0, (0, 46)) if k % 2 else [])
        w += (se(s["bubble"]) if k % 2 == 0 else []) + wait(1)
    w += emit_at(SPITFX20, 0 if side == "player" else 1, 0, (sx * 8, 34)) + se(s["hpump"])
    for k in range(10):
        if k > 3 and k % 2 == 0:
            w += shake_defender(2, 1) + se(s["splash"])
        w += wait(1)
    return w + func(34, 8, 0, 1, rgb(80, 170, 255), 13, 0) + func(48) + wait(3)


def _post_up(side, s):
    """Ingrain (Post Up): a lawn chair with an umbrella unfolds - they sit - they're not moving. Ever."""
    sx = _sx(side)
    ch = (sx * 12, 14) if side == "player" else (-12, 4)
    w = se(s["bonk"]) + _hold(CHAIR20, 1, 0, ch, 2) + bmove(side, 258, 3, 0, -6) + se(s["flop"])
    for k in range(14):
        w += emit_at(CHAIR20, 1, 0, ch)
        if k % 5 == 0:
            w += emit_at(CHAIR20, 0, 0, (0, 30)) + func(34, 2, 0, 1, rgb(120, 255, 140), 12, 0) + se(s["absorb"])
        w += wait(1)
    return w + bmove(side, 258, 3, 0, 6) + _hold(CHAIR20, 1, 0, ch, 2)


def _stab_combo(side, s):
    """Fury Cutter (Stab Combo): slash - "2 HIT!" - slash slash - "3 HIT!" - slash slash slash - "5 HIT COMBO!"."""
    sx = _sx(side)
    sign = (-sx * 30, 52) if side == "player" else (30, 50)
    w = []
    for n, (cnt, sres, sps) in enumerate(((2, 2, SLASH20), (1, 0, COMBO20), (2, 1, COMBO20))):
        for c in range(cnt):
            w += bmove(side, 258, 1, sx * 10, 3) + emit_at(SLASH20, 1, 1, (0, 20)) + emit_at(SLASH20, 0, 1, (0, 20))
            w += se(s["slash"]) + shake_defender(2, 1) + bmove(side, 258, 1, -sx * 10, -3) + wait(1)
        w += emit_at(sps, sres, 1, sign) + se(s["bling"] if n < 2 else s["chaching"]) + wait(3)
    return w + flash_screen(3) + func(48) + wait(4)


def _blood_pact(side, s):
    """Destiny Bond (Blood Pact): two halves of a BFF necklace - one on each - they snap together - and a purple
    line ties their fates."""
    sx = _sx(side)
    lh, rh = ((1, 2) if side == "player" else (2, 1))
    a, d = (sx * 6, 50), (0, 46)
    w = se(s["curse"]) + _hold(BFF20, lh, 0, a, 2, lambda k: emit_at(BFF20, rh, 1, d))
    w += emit_at(LINK20, 0 if side == "player" else 1, 0, (0, 30)) + se(s["dteam"])
    for k in range(10):
        w += emit_at(BFF20, lh, 0, a) + emit_at(BFF20, rh, 1, d)
        if k == 2:
            w += emit_at(BFF20, 0, 0, (0, 30)) + emit_at(BFF20, 0, 1, (0, 30))
        w += wait(1)
    w += se(s["bling"]) + flash_screen(2) + func(34, 2, 0, 1, rgb(160, 40, 220), 13, 0)
    return w + func(34, 8, 0, 1, rgb(160, 40, 220), 13, 0) + wait(6)

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
            150: _air_force, 151: _sixth_sense,
            152: _gold_grill, 153: _air_it_out, 154: _barricade, 155: _zen_dome, 156: _freeloader,
            157: _drip_check, 158: _yell_woop, 159: _security, 160: _wax_on, 161: _beef,
            162: _big_bass, 163: _ice_chip, 164: _get_even, 165: _car_magnet, 166: _one_two, 167: _power_bank,
            168: _duck_down, 169: _brain_freeze, 170: _lock_on, 171: _night_shank,
            172: _got_ya_back, 173: _ice_out, 174: _stone_cold, 175: _rizz_up, 176: _pickup_line, 177: _ice_cold,
            178: _ground_game, 179: _tailgate, 180: _iced_out, 181: _photo_op,
            182: _box_cutter, 183: _muscle, 184: _smash_n_grab, 185: _lay_low, 186: _hot_hands,
            187: _taser_punch, 188: _og_power, 189: _laser_sight, 190: _mudslinging, 191: _hot_grill,
            192: _taser_grill, 193: _rizz, 194: _bulk_up, 195: _curb_stomp, 196: _get_back,
            197: _gun_twirl, 198: _ace_shot, 199: _jack_em, 200: _drop_a_track, 201: _dust_up,
            202: _lay_low_turn2_first,
            203: _run_it_back,
            204: _pass_it_off,
            205: _brass_knucks,
            206: _doughnuts,
            207: _diss_track,
            208: _bootleg,
            209: _run_em_off,
            210: _suplex,
            211: _leg_sweep,
            212: _dark_vibes,
            213: _premonition,
            214: _ankle_break,
            215: _scheme,
            216: _steel_plate,
            217: _turn_up,
            218: _tough_it_out,
            219: _plan_z,
            220: _throwdown,
            221: _stay_calm,
            222: _snow_cone,
            223: _crash_out,
            224: _pogo_stick,
            225: _shear_pain,
            226: _lava_lamp,
            227: _stack_up,
            228: _clap_back,
            229: _hammer_time,
            230: _chalkboard,
            231: _mosquito,
            232: _flush_it,
            233: _pogo_turn2_first,
            234: _fruit_throw,
            235: _crash_pad,
            236: _toss_it,
            237: _dream_killer,
            238: _claw_clap,
            239: _u_turn,
            240: _dragon_beam,
            241: _silver_dust,
            242: _ice_storm,
            243: _confiscate,
            244: _flick_a_bic,
            245: _static_shock,
            246: _graze,
            247: _fall_guy,
            248: _shady_claw,
            249: _steel_toe,
            250: _hidden_strap,
            251: _bullet_spray,
            252: _rock_pile,
            253: _overcook,
            254: _energy_drink,
            255: _dream_talk,
            256: _trade_spots,
            257: _big_blast,
            258: _dumpster_dive,
            259: _snack_grab,
            260: _snow_plow,
            261: _slow_mo,
            262: _flash_bang,
            263: _hit_the_gym,
            264: _clown_on,
            265: _swipe,
            266: _one_punch,
            267: _tax_punch,
            268: _iron_wing,
            269: _flashbang_switch,
            270: _rock_trap,
            271: _trip_wire,
            272: _grudge,
            273: _front,
            274: _inside_job,
            275: _wall_climb,
            276: _fake_pass,
            277: _smoke_screen,
            278: _plug_in,
            279: _bed_bugs,
            280: _squeeze_out,
            281: _loud_pack,
            282: _grind,
            283: _sniff_out,
            284: _hide_out,
            285: _rock_candy,
            286: _mooch,
            287: _peep_game,
            288: _zaza_storm,
            289: _dip_out,
            290: _mouthwash_spit,
            291: _post_up,
            292: _stab_combo,
            293: _blood_pact,
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
        150: (JETS, KICK, STOMPFX), 151: (SKYEYE, CRYSTAL, COSMOS),
        152: (TEETHR, TEETHL), 153: (HAZEFOG, TOWELS), 154: (FURNITURE,), 155: (ZEN, ZENFX), 156: (COUSIN, LEECHFX),
        157: (MIRROR, DRIPFX), 158: (SIREN, WOOP), 159: (SECURITY1, BUBBLES14), 160: (BUFFER, SHINE14),
        161: (STEAK, STEAMFX),
        162: (BASSFISH, BASSFX), 163: (ICECUP, ICEHIT), 164: (LISTBOOK, LISTFX), 165: (MAGNET14,),
        166: (BELL14, GLOVES), 167: (BANK16, PHONE16, BEAM16), 168: (RACK,), 169: (SLUSH, JAWS16), 170: (BINOC,),
        171: (NIGHT16,),
        172: (SHAKE, SHAKEFX), 173: (DIAMONDS, ICEBLOCK), 174: (COLDSHADES, SPIKES), 175: (DATE, HEARTS16),
        176: (PICKUP, BLUSH), 177: (ACUNIT, FLAKES), 178: (POTHOLE1, CONES), 179: (TAILGATE, GRILLSMOKE),
        180: (SNOWMACH, SNOWSTORM), 181: (RINGLIGHT, FLASHES),
        182: (BOX17, CUTTER17, CUTL17), 183: (BAR17, PLATE17), 184: (CASE17, CROW17, LOOT17), 185: (SHOVEL17, DIRT17),
        186: (STOVE17, GLOVEL17, FLAMES17), 202: (SHOVEL17, DIRT17),
        187: (TGLOVE17, ZAPB17, ZAPS17), 188: (RELICS17, OGAURA17), 189: (POINTER17, PSYRING17, DIZZY17),
        190: (TIRE17, MUDWAVE17), 191: (FOREMAN17, MARKS17, SIZZLE17),
        192: (CABLES17, CABLESL17, JOLT17), 193: (ROSES17, LOVE17), 194: (GAINZ17, PUMP17), 195: (KICKS17, VEIN17),
        196: (STUFF17, JUNK17),
        197: (TWIRL17, AURA17), 198: (CARDS17, SLICE17), 199: (BAG17, CLAW17), 200: (MICS17, SLEEPZ17),
        201: (BLOWER17, TRASH17, DUSTSTORM17),
        203: (DJ18, DJFX18),
        204: (DUFFEL18,),
        205: (KNUX18, POW18),
        206: (CAR18, RINGFIRE18),
        207: (CD18, NOTES18),
        208: (COAT18, GEARS18),
        209: (BROOM18,),
        210: (RING18,),
        211: (WET18, STARS18),
        212: (CANDLE18, WAVES18),
        213: (COOKIE18, SLIP18),
        214: (BALL18,),
        215: (CORK18, AURA18),
        216: (ARMOR18,),
        217: (PARTY18, LIGHTS18),
        218: (AID18,),
        219: (SINK18, BOOM18),
        220: (BRAWL18, BRAWLFX18),
        221: (CALM18,),
        222: (SNOWCONE18,),
        223: (TABLE18, PLATES18),
        224: (POGO18,),
        225: (SCISS18, SHINE18),
        226: (LAMP18, BLOBS18),
        227: (PANCAKE18,),
        228: (CLAP18,),
        229: (STRIKER18, PUCK18),
        230: (CHALK18,),
        231: (MOSQ18, WELT18),
        232: (TOILET18, FLUSH18),
        233: (POGO18,),
        234: (FRUIT19,),
        235: (MATTRESS19, HEAL19),
        236: (TV19,),
        237: (DREAM19,),
        238: (LOBSTER19, LOBL19),
        239: (SCOOT19,),
        240: (DRAGON19,),
        241: (GLITTER19,),
        242: (ICEBAG19, CUBES19),
        243: (EVID19,),
        244: (MATCH19, WISP19),
        245: (BALLOON19, ZAP19),
        246: (FRISBEE19,),
        247: (DUMMY19,),
        248: (CLAWS19,),
        249: (WRECK19,),
        250: (TEDDY19, ORBS19, PISTOL19),
        251: (SEEDS19, SEEDFX19),
        252: (TRUCK19, TRUCKL19, GRAVEL19),
        253: (TOAST19, SMOKE19),
        254: (CAN19, GREEN19),
        255: (SLEEP19,),
        256: (CARDS19,),
        257: (MORTAR19, FIREWORK19),
        258: (BIN19,),
        259: (GRAB19, GRABL19),
        260: (PLOW19, SNOWWALL19),
        261: (REMOTE19, SEPIA19),
        262: (CAMERA19, FLASH19),
        263: (GYM19,),
        264: (CLOWN20,),
        265: (SWIPE20,),
        266: (PUNCHM20,),
        267: (PIGGY20, COINS20,),
        268: (IRON20,),
        269: (LIGHT20,),
        270: (LEGO20,),
        271: (LACES20,),
        272: (GAUGE20, STEAM20,),
        273: (FRONT20,),
        274: (SAFE20,),
        275: (CLIMB20,),
        276: (FOOTB20,),
        277: (FOG20, FOGFX20,),
        278: (AMP20, AMPFX20,),
        279: (BUGS20, BUGFX20,),
        280: (MOP20,),
        281: (FANNY20, MONEY20,),
        282: (TREAD20,),
        283: (SLEUTH20,),
        284: (FICUS20,),
        285: (CANDY20, GEMBEAM20,),
        286: (SHAKE20,),
        287: (SCOPE20,),
        288: (LEAVES20,),
        289: (EXIT20,),
        290: (MOUTH20, SPITFX20,),
        291: (CHAIR20,),
        292: (SLASH20, COMBO20,),
        293: (BFF20, LINK20,),
        101: (SNORE, SNOREZ), 102: (BADBATCH, TOXB), 103: (BURNS, BURNF), 104: (ICED, ICEG),
        105: (TASED, JAGS), 106: (WHERE, QMARKS), 107: (CRUSH, HEARTS2), 108: (CLOUT, CLOUTUPS),
        109: (STOREBAG, LOOKS), 110: (STASH, STASHG), 112: (GAINS, UPS), 113: (DOWNBAD, DOWNS), 114: (HENNY, DRIPS, AHHH)}


LOOPING_SE = {1914, 1915, 1938, 1946, 1972, 1982, 2010, 2041, 2065, 2121}   # SEs the game's own scripts stop with 44


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

        def stops(part):                                           # StopSE (44) for every looping SE it started:
            ids = {part[i + 1] for i in range(len(part) - 1)       #  those never end on their own (the originals
                   if part[i] == 5 and part[i + 1] in LOOPING_SE}  #  stop them too) - else they play forever
            return [w for i in sorted(ids) for w in (44, i)]
        if isinstance(got, tuple):                                 # a two-turn move (Fly): turn 1, turn 2
            one, two = got[0] + stops(got[0]) + tail, got[1] + stops(got[1]) + tail
            w = [13, 2, 1 + len(one)] + one + two                  # JumpByVariantBit0: bit 0 set = the hit
        else:
            w = got + stops(got) + tail
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
