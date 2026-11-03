"""Set 25 batch 4: Moon Bath, Slime Down, Last Verse, Lip Gloss, Bottle Rain (variants 377-381).
Run once from the repo root: python -X utf8 hood/test/reel/set25_b4.py  (art: set25_b4_art.py, already in fxart)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import set23_lib  # noqa: E402

NAMES = "MOON25 MOONB25 SLIME25 SLIMEB25 VERSE25 VERSEB25 VERSEC25 GLOSS25 GLOSSB25 BOTTLE25".split()

KITS = '''
    # ---- set 25, batch 4 ----------------------------------------------------------------------------------
    # Moon Bath (Moonlight): night. The moon comes up, a beach lounger, the tanning reflector - tilt, tilt - then the
    # moonbeam hits and they glow, healed
    b, rs = pk(MOON25, {1: (fxart.big_moon(), 1.0, 4, {}), 2: (fxart.beach_lounger(), 1.3, 4, {})}, alpha=fxart.glow_dot())
    burst(b, rs, 0, rgb(200, 220, 255), rgb(255, 255, 255), .3, 10, .06, up=.12, life=24, radius=.6)
    fin(MOON25, b, rs, (0, 1, 2))
    b, rs = pk(MOONB25, {1: (fxart.sun_reflector(), .7, 4, {})}, alpha=fxart.holy_ray())
    prop(b, rs, 0, tex=0, clr=rgb(220, 230, 255), clr_anm=(rgb(255, 255, 255), rgb(170, 200, 255)), scl=1.0, life=20,
         gen=3, gen_intvl=1, emtr_life=24, init_pos=1, radius=.4, axis=(0, -1, 0), vel=(.01, .8), alpha=(24, 18, 0))
    fin(MOONB25, b, rs, (0, 1))

    # Slime Down (Acid Armor): a bucket of slime overhead - drip - drip - the whole bucket. Slimed. Hard to hit now.
    b, rs = pk(SLIME25, {1: (fxart.slime_bucket(), .9, 4, {}), 2: (fxart.slime_bucket(tipped=True), .9, 4, {})}, alpha=fxart.fizz_drop())
    burst(b, rs, 0, rgb(120, 230, 60), rgb(210, 255, 170), .35, 2, .02, gravity=.03, life=14)
    burst(b, rs, 3, rgb(120, 230, 60), rgb(210, 255, 170), .4, 14, .2, up=.14, gravity=.02, life=20)
    fin(SLIME25, b, rs, (0, 1, 2, 3))
    b, rs = pk(SLIMEB25, {1: (fxart.slime_goo(), 1.2, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(170, 220, 255), rgb(255, 255, 255), .45, 8, .12, life=14)
    fin(SLIMEB25, b, rs, (0, 1))

    # Last Verse (Perish Song): the spotlight, the last verse - 3 - 2 - 1 - MIC DROP
    b, rs = pk(VERSE25, {1: (fxart.stage_mic(), .9, 4, {}), 2: (fxart.burst_sign(["3"], fill=(30, 30, 40, 255), text=(255, 230, 80, 255)), SIGN_SCALE * 2, 4, {"colors": 30})},
               alpha=fxart.shout_arc())
    burst(b, rs, 0, rgb(255, 255, 255), rgb(255, 240, 160), .45, 4, .14, life=12)
    fin(VERSE25, b, rs, (0, 1, 2))
    b, rs = pk(VERSEB25, {1: (fxart.burst_sign(["2"], fill=(30, 30, 40, 255), text=(255, 230, 80, 255)), SIGN_SCALE * 2, 4, {"colors": 30}),
                          2: (fxart.burst_sign(["1"], fill=(30, 30, 40, 255), text=(255, 230, 80, 255)), SIGN_SCALE * 2, 4, {"colors": 30})})
    fin(VERSEB25, b, rs, (1, 2))
    b, rs = pk(VERSEC25, {1: (fxart.burst_sign(["MIC DROP."], fill=(200, 20, 30, 255), text=(255, 255, 255, 255)), SIGN_SCALE, 4, {"colors": 30})},
               alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 250, 200), rgb(255, 255, 255), .6, 16, .32, life=14)
    fin(VERSEC25, b, rs, (0, 1))

    # Lip Gloss (Lovely Kiss): swipe - swipe - the lips shine like a disco ball, the foe's hypnotized - and out cold
    b, rs = pk(GLOSS25, {1: (fxart.lip_gloss(), .7, 4, {}), 2: (fxart.glossy_lips(), .8, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 150, 220), rgb(255, 255, 255), .5, 12, .3, life=12)
    fin(GLOSS25, b, rs, (0, 1, 2))
    b, rs = pk(GLOSSB25, {}, alpha=fxart.sleep_z16())
    burst(b, rs, 0, rgb(120, 170, 255), rgb(230, 240, 255), .45, 3, .04, up=.1, life=30, radius=.2)
    fin(GLOSSB25, b, rs, (0,))

    # Bottle Rain (Barrage): a water bottle off the foe's head - bonk, splash (replays per hit: short)
    b, rs = pk(BOTTLE25, {1: (fxart.water_bottle(), .5, 4, {})}, alpha=fxart.fizz_drop())
    burst(b, rs, 0, rgb(120, 190, 255), rgb(230, 245, 255), .35, 10, .16, up=.18, gravity=.02, life=18)
    fin(BOTTLE25, b, rs, (0, 1))
'''

SCRIPTS = '''
def _moon_bath(side, s):
    """Moonlight (Moon Bath): night falls. The moon comes up, a beach lounger slides under them, out comes the tanning
    reflector - tilt... tilt... - then the moonbeam lands and they glow. Healed."""
    sx = _sx(side)
    moon = _s23(side, 0, _p(side, (222, 26), (40, 70)))
    chair = (sx * 8, -4)
    refl = (sx * 18, 26)
    scene = lambda: emit_at(MOON25, 1, 0, moon) + emit_at(MOON25, 2, 0, chair)
    w = func(33, 0, 1, 0, 12, rgb(10, 15, 60))
    for k in range(5):                                                         # *moonrise*
        w += emit_at(MOON25, 1, 0, (moon[0], moon[1] - 30 + k * 6)) + wait(1)
    w += se(s["whoosh"]) + _hold(MOON25, 2, 0, chair, 3, lambda k: emit_at(MOON25, 1, 0, moon))
    for n in range(2):                                                         # tilt... tilt...
        for k in range(4):
            w += scene() + emit_at(MOONB25, 1, 0, (refl[0] + (2 if k % 2 else -2) * (n + 1), refl[1])) + wait(1)
        w += se(s["bling"]) + emit_at(MOON25, 0, 0, (0, 16)) + _hold(MOONB25, 1, 0, refl, 3, lambda k: scene())
    w += se(s["sbeam"]) + flash_screen(3) + emit_at(MOONB25, 0, 0, (0, 90))     # *the moonbeam*
    for k in range(12):
        w += scene() + emit_at(MOONB25, 1, 0, refl)
        if k in (2, 8):
            w += se(s["absorb"]) + emit_at(MOON25, 0, 0, (0, 20)) + func(34, 2, 0, 1, rgb(200, 220, 255), 12, 0)
        w += wait(1)
    return w + func(33, 0, 1, 12, 0, rgb(10, 15, 60)) + wait(2)


def _slime_down(side, s):
    """Acid Armor (Slime Down): a bucket of green slime appears over their head. Drip. Drip. Then the whole bucket
    tips - SPLORCH - slimed head to toe. Good luck landing a hit now."""
    top = (0, 70)
    w = se(s["pop"]) + _hold(SLIME25, 1, 0, top, 4)
    for n in range(2):                                                         # drip... drip...
        w += se(s["bubble"]) + emit_at(SLIME25, 0, 0, (top[0] - 4 + 8 * n, top[1] - 12)) + _hold(SLIME25, 1, 0, top, 5)
        w += shake_attacker(1, 1)
    w += _hold(SLIME25, 2, 0, top, 3)                                          # *tips*
    w += se(s["splat"]) + se(s["sludge"]) + emit_at(SLIME25, 3, 0, (0, 30)) + shake_attacker(2, 2)
    for k in range(14):                                                        # SLIMED
        w += emit_at(SLIMEB25, 1, 0, (0, 26 - (k // 3)))
        if k < 4:
            w += emit_at(SLIME25, 2, 0, top)
        if k in (5, 10):
            w += se(s["harden"]) + emit_at(SLIMEB25, 0, 0, (0, 30)) + func(34, 2, 0, 1, rgb(140, 200, 255), 10, 0)
        w += wait(1)
    return w + wait(2)


def _last_verse(side, s):
    """Perish Song (Last Verse): lights down, spotlight - they spit the last verse - 3... 2... 1... MIC DROP. Everybody
    on the field feels that one."""
    sx = _sx(side)
    mic = (sx * 22, 34)
    sign = _p(side, (0, 58), (0, 50))
    w = func(33, 0, 1, 0, 12, rgb(20, 10, 30)) + se(s["pop"]) + _hold(VERSE25, 1, 0, mic, 3)
    for k in range(10):                                                        # *the verse*
        w += emit_at(VERSE25, 1, 0, (mic[0], mic[1] + (k % 2)))
        if k % 2 == 0:
            w += se(s["bass"]) + emit_at(VERSE25, 0, 0, (mic[0] + sx * 10, mic[1] + 6)) + bmove(side, 258, 1, 0, 3)
        else:
            w += bmove(side, 258, 1, 0, -3)
        w += wait(1)
    for kit, res in ((VERSE25, 2), (VERSEB25, 1), (VERSEB25, 2)):             # 3... 2... 1...
        w += se(s["clock"]) + _hold(kit, res, 0, sign, 6, lambda k: emit_at(VERSE25, 1, 0, mic))
    w += se(s["whoosh"])
    for k in range(5):                                                         # *drops it*
        w += emit_at(VERSE25, 1, 0, (mic[0] + sx * 4, mic[1] - k * 10)) + wait(1)
    w += se(s["kaboom"]) + se(s["bslam"]) + flash_screen(6) + func(68, 6, 6, 1, 6, 0) + emit_at(VERSEC25, 0, 0, (mic[0], mic[1] - 46))
    w += shake_defender(3, 3) + shake_attacker(3, 3) + func(34, 8, 0, 1, rgb(90, 90, 110), 12, 0) + func(34, 2, 0, 1, rgb(90, 90, 110), 12, 0)
    w += _hold(VERSEC25, 1, 0, sign, 12)
    return w + func(33, 0, 1, 12, 0, rgb(20, 10, 30)) + wait(2)


def _lip_gloss(side, s):
    """Lovely Kiss (Lip Gloss): swipe of lip gloss - shine. Another swipe - SHINE. Then the lips catch the light like
    a disco ball, the foe's hypnotized... sways... and drops off to sleep."""
    sx = _sx(side)
    mouth = (sx * 12, 34)
    w = []
    for n in range(2):                                                         # swipe... swipe...
        for k in range(4):
            w += emit_at(GLOSS25, 1, 0, (mouth[0] + (6 if k % 2 else -6), mouth[1])) + wait(1)
        w += se(s["bling"]) + emit_at(GLOSS25, 0, 0, mouth) + wait(3)
    w += se(s["bling"]) + se(s["sbeam"]) + flash_screen(3)                   # *SHINE*
    for k in range(10):
        w += emit_at(GLOSS25, 2, 0, mouth)
        if k % 3 == 0:
            w += emit_at(GLOSS25, 0, 0, mouth) + se(s["bling"])
        if k == 4:
            w += func(34, 8, 0, 1, rgb(255, 140, 210), 12, 0)
        w += wait(1)
    for k, d_ in enumerate((6, -12, 12, -6)):                                  # *sways...*
        w += bmove(side, 264, 3, d_, 0) + emit_at(GLOSS25, 2, 0, mouth) + wait(2)
    w += se(s["sleep"]) + bmove(side, 264, 4, 0, -6) + emit_at(GLOSSB25, 0, 1, (10, 40))
    w += wait(6) + emit_at(GLOSSB25, 0, 1, (14, 44)) + wait(6)
    return w + bmove(side, 264, 4, 0, 6) + wait(2)


def _bottle_rain(side, s):
    """Barrage (Bottle Rain): a water bottle off the foe's head - bonk - splash. (Replays per hit.)"""
    sx = _sx(side)
    dx, dy = TARGET_FROM_ATTACKER[side]
    w = se(s["whoosh"]) + _lob(BOTTLE25, 1, side, (sx * 20, 30), (dx, dy + 40), 5, 24)
    w += se(s["bonk"]) + se(s["splash"]) + emit_at(BOTTLE25, 0, 1, (0, 40)) + shake_defender(2, 2)
    return w + _lob(BOTTLE25, 1, side, (dx, dy + 40), (dx + sx * 30, dy + 70), 3, 10) + wait(1)
'''

TABLE = {377: ("_moon_bath", ("MOON25", "MOONB25"), "Moonlight"),
         378: ("_slime_down", ("SLIME25", "SLIMEB25"), "Acid Armor"),
         379: ("_last_verse", ("VERSE25", "VERSEB25", "VERSEC25"), "Perish Song"),
         380: ("_lip_gloss", ("GLOSS25", "GLOSSB25"), "Lovely Kiss"),
         381: ("_bottle_rain", ("BOTTLE25",), "Barrage")}

if __name__ == "__main__":
    set23_lib.apply(NAMES, KITS, SCRIPTS, TABLE)
