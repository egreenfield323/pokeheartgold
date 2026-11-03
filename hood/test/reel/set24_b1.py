"""Set 24 batch 1 (INSANE): Full Auto, 18 Wheeler, Holy Fire, Sentencing, Clock Out (variants 330-334).
Hyper Beam / Giga Impact / Sacred Fire / Judgment / Roar of Time move off their shared variants (10 and 11).
Run once from the repo root: python -X utf8 hood/test/reel/set24_b1.py  (art: set24_b1_art.py, already in fxart)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import set23_lib  # noqa: E402

NAMES = "FA24 FAB24 FAC24 TRUCK24 TRUCKB24 HOLY24 HOLYB24 HOLYC24 GAVEL24 GAVELB24 CLOCK24 CLOCKB24 CLOCKC24".split()

KITS = '''
    # ---- set 24: thirty more (batch 1, the INSANE ones) -------------------------------------------------------
    # Full Auto (Hyper Beam): the pistol jams - *CLICK* - jams again - so out comes a MINIGUN on a tripod, spins up,
    # and the whole screen goes BRRRRRRT. Smoke clears. RELOADING...
    b, rs = pk(FA24, {1: (fxart.jam_pistol(), .7, 4, {}), 2: (flipx(fxart.jam_pistol()), .7, 4, {})}, alpha=fxart.brass_shell())
    burst(b, rs, 0, rgb(240, 190, 60), rgb(255, 240, 160), .3, 4, .14, up=.16, gravity=.02, life=20, spin=0x1000)
    burst(b, rs, 3, rgb(255, 200, 60), rgb(255, 255, 220), .35, 6, .22, life=8)
    fin(FA24, b, rs, (0, 1, 2, 3))
    b, rs = pk(FAB24, {1: (fxart.minigun(), 1.5, 4, {}), 2: (flipx(fxart.minigun()), 1.5, 4, {})}, alpha=fxart.tracer_streak())
    for res, sd in ((0, "player"), (3, "enemy")):
        spray(b, rs, res, sd, FA_TIP24[sd], (0, 24), 8, tex=0, clr=rgb(255, 230, 90), clr_anm=(rgb(255, 255, 220), rgb(255, 150, 30)),
              scl=.9, gen=2, gen_intvl=1, emtr_life=96, radius=.08, spread=.03, alpha=(31, 31, 0))
    fin(FAB24, b, rs, (0, 1, 2, 3))
    b, rs = pk(FAC24, {1: (fxart.line_bubble(["CLICK."]), ONE_TO_ONE, 4, {}), 2: (fxart.line_bubble(["RELOADING..."]), ONE_TO_ONE, 4, {}),
                       3: (fxart.muzzle_star(), 1.1, 2, {})}, alpha=fxart.soft_puff())
    puffs(b, rs, 0, rgb(150, 150, 155), n=8, life=30, scl=.45, up=.05)
    fin(FAC24, b, rs, (0, 1, 2, 3))

    # 18 Wheeler (Giga Impact): HONK - HONK - HOOOOONK - an 18-wheeler barrels across the whole screen through the foe
    b, rs = pk(TRUCK24, {1: (fxart.semi_truck(), 3.0, 4, {}), 2: (flipx(fxart.semi_truck()), 3.0, 4, {})}, alpha=fxart.glow_dot())
    burst(b, rs, 0, rgb(255, 250, 200), rgb(255, 255, 255), 1.4, 3, .02, life=10, alpha=(28, 24, 0))
    fin(TRUCK24, b, rs, (0, 1, 2))
    b, rs = pk(TRUCKB24, {}, alpha=fxart.soft_puff(), alpha1=fxart.speck(64))
    puffs(b, rs, 0, rgb(150, 150, 155), n=5, life=24, scl=.28, up=.04)
    burst(b, rs, 1, rgb(200, 200, 210), rgb(255, 255, 255), .5, 18, .4, up=.2, gravity=.02, life=26, tex=1, spin=0x0C00)
    burst(b, rs, 2, rgb(255, 230, 60), rgb(255, 255, 220), .4, 7, .08, up=.02, life=26, radius=.5, tex=1)
    fin(TRUCKB24, b, rs, (0, 1, 2))

    # Holy Fire (Sacred Fire): church. "CAN I GET AN AMEN?" ... "...amen." ... the stained glass blazes, a shaft of
    # light, and a pillar of holy fire on the foe. They come out of it with a halo.
    b, rs = pk(HOLY24, {1: (fxart.stained_glass(), 1.4, 4, {}), 2: (fxart.stained_glass(lit=True), 1.4, 4, {})}, alpha=fxart.holy_ray())
    prop(b, rs, 0, tex=0, clr=rgb(255, 240, 160), clr_anm=(rgb(255, 255, 255), rgb(255, 210, 80)), scl=1.1, life=22,
         gen=3, gen_intvl=1, emtr_life=40, init_pos=1, radius=.5, axis=(0, -1, 0), vel=(.01, .9), alpha=(26, 20, 0))
    fin(HOLY24, b, rs, (0, 1, 2))
    b, rs = pk(HOLYB24, {1: (fxart.line_bubble(["CAN I GET", "AN AMEN?"]), ONE_TO_ONE, 4, {}),
                         2: (fxart.line_bubble(["I SAID", "CAN I GET", "AN AMEN?!"]), ONE_TO_ONE, 4, {})}, alpha=fxart.soft_puff())
    puffs(b, rs, 0, rgb(250, 245, 230), n=10, life=40, scl=.5, up=.01)
    fin(HOLYB24, b, rs, (0, 1, 2))
    b, rs = pk(HOLYC24, {1: (fxart.line_bubble(["...amen."]), ONE_TO_ONE, 4, {}), 2: (fxart.gold_halo(), .5, 4, {})}, alpha=fxart.holy_flame())
    prop(b, rs, 0, tex=0, clr=rgb(255, 150, 30), clr_anm=(rgb(255, 250, 200), rgb(240, 60, 10)), scl=.42, life=18,
         gen=6, gen_intvl=1, emtr_life=6, init_pos=1, radius=.9, axis=(0, 1, 0), vel=(.04, .5), alpha=(31, 31, 0),
         scl_anm=(.5, 1.3, .6, 50, 160))
    fin(HOLYC24, b, rs, (0, 1, 2))

    # Sentencing (Judgment): court's in session - BANG - BANG - GUILTY! - and a GIANT gavel comes down from the sky
    b, rs = pk(GAVEL24, {1: (fxart.judge_gavel(), .9, 4, {}), 2: (fxart.judge_gavel(), 3.6, 4, {})}, alpha=fxart.speck())
    burst(b, rs, 0, rgb(200, 160, 110), rgb(255, 240, 200), .35, 8, .18, up=.1, gravity=.014, life=16)
    fin(GAVEL24, b, rs, (0, 1, 2))
    b, rs = pk(GAVELB24, {1: (fxart.burst_sign(["GUILTY!"], fill=(40, 30, 20, 255), text=(255, 220, 60, 255)), SIGN_SCALE, 4, {"colors": 30})},
               alpha=fxart.soft_puff())
    burst(b, rs, 0, rgb(190, 170, 140), rgb(250, 240, 220), .55, 18, .45, up=.04, life=30, alpha=(28, 22, 0), scl_anm=(.5, 1.3, 1.8, 60, 200))
    fin(GAVELB24, b, rs, (0, 1))

    # Clock Out (Roar of Time): the time clock: 4:58... 4:59... 5:00 - KA-CHUNK - time itself stops, clocks
    # everywhere, a shockwave, then it all snaps back on the foe
    b, rs = pk(CLOCK24, {1: (fxart.time_clock(), ONE_TO_ONE, 4, {"colors": 30}), 2: (fxart.time_clock(t="4:59"), ONE_TO_ONE, 4, {"colors": 30})},
               alpha=fxart.ring())
    prop(b, rs, 0, tex=0, clr=rgb(255, 220, 140), clr_anm=(rgb(255, 255, 230), rgb(200, 140, 60)), scl=1.0, life=22,
         alpha=(28, 20, 0), scl_anm=(.2, 3.4, 4.2, 70, 200))
    fin(CLOCK24, b, rs, (0, 1, 2))
    b, rs = pk(CLOCKB24, {1: (fxart.time_clock(t="5:00"), ONE_TO_ONE, 4, {"colors": 30}), 2: (fxart.punch_card(), .45, 4, {})})
    fin(CLOCKB24, b, rs, (1, 2))
    b, rs = pk(CLOCKC24, {})
    b, wc = added(b, fxart.wall_clock(), 24)
    burst(b, rs, 0, rgb(255, 255, 255), rgb(255, 255, 255), .45, 10, .3, up=.12, gravity=.006, life=40, radius=.6, spin=0x0900, tex=wc,
          clr_anm=(rgb(255, 255, 255), rgb(255, 255, 255)), alpha=(31, 31, 0))
    fin(CLOCKC24, b, rs, (0,))
'''

SCRIPTS = '''
FA_GUN24 = {"player": (96, 88), "enemy": (152, 66)}                      # minigun spot (screen)
FA_TIP24 = {"player": (68, 50), "enemy": (-67, 11)}                     # its barrel tip, attacker-relative


def _full_auto_insane(side, s):
    """Hyper Beam (Full Auto): the pistol - *CLICK*, jammed. *CLICK*, smack it, nothing. Fine: a MINIGUN drops from
    the sky on its tripod, spins up... and the whole screen goes BRRRRRRRRT. When the smoke clears: RELOADING..."""
    sx = _sx(side)
    gun = _p(side, (sx * 30, 26), (-30, 16))
    pres = _p(side, 1, 2)
    bub = _p(side, (sx * 50, 58), (-40, 30))
    mg = _s23(side, 0, FA_GUN24[side])
    tip = FA_TIP24[side]
    mres = _p(side, 1, 2)
    toss = _p(side, (-60, 70), (70, 60))
    dx, dy = TARGET_FROM_ATTACKER[side]
    w = se(s["pop"]) + _hold(FA24, pres, 0, gun, 3)
    for n in range(2):                                                         # *CLICK*... *CLICK*
        w += se(s["disable"]) + emit_at(FA24, pres, 0, (gun[0] + sx * 2, gun[1]))
        w += _hold(FAC24, 1, 0, bub, 7, lambda k: emit_at(FA24, pres, 0, gun) + (shake_attacker(2, 2) if n == 1 and k == 3 else []) +
                   (se(s["bonk"]) if n == 1 and k == 3 else []))
        w += _hold(FA24, pres, 0, gun, 3)
    w += se(s["whoosh"]) + _lob(FA24, pres, side, gun, toss, 5, 20)        # *yeets the pistol*
    w += wait(3) + func(33, 0, 1, 0, 10, rgb(50, 0, 0)) + wait(2)
    for k in range(4):                                                         # *the minigun drops in*
        w += emit_at(FAB24, mres, 0, (mg[0], mg[1] + round(110 * (1 - (k + 1) / 4) ** 1.5))) + wait(1)
    w += se(s["bslam"]) + func(68, 3, 3, 1, 3, 0) + emit_at(FAC24, 0, 0, (mg[0], mg[1] - 24)) + _hold(FAB24, mres, 0, mg, 3)
    for k in range(9):                                                         # whirrrRRRR
        w += emit_at(FAB24, mres, 0, (mg[0] + (k % 2), mg[1]))
        if k % (3 if k < 5 else 1) == 0:
            w += se(s["rollout"])
        w += wait(1)
    w += se(s["boom"]) + flash_screen(3) + emit_at(FAB24, _p(side, 0, 3), 0, tip) + func(68, 2, 2, 1, 30, 0) + shake_attacker(1, 30)
    for k in range(28):                                                        # BRRRRRRRRRRRRT
        w += emit_at(FAB24, mres, 0, (mg[0] + (k % 2) * 2 * sx, mg[1] + (k % 3) - 1))
        w += emit_at(FAC24, 3, 0, (tip[0], tip[1] + _l3(1.1)))
        w += se(s["pop"] if k % 2 else s["boom"])
        if k % 2 == 0:
            w += emit_at(FA24, 0, 0, (mg[0] - sx * 6, mg[1] + 6))
            w += emit_at(FA24, 3, 1, (((k * 13) % 36) - 18, 12 + (k * 7) % 34 + _l3(.35)))
        if k % 4 == 0:
            w += shake_defender(2, 1)
        if k % 7 == 6:
            w += flash_screen(2)
        w += wait(1)
    w += se(s["kaboom"]) + func(48) + func(34, 8, 0, 1, rgb(40, 30, 30), 13, 0)
    for k in range(3):
        w += emit_at(FAC24, 0, 1, ((k - 1) * 16, 20 + k * 6))
    w += _hold(FAB24, mres, 0, mg, 6) + func(33, 0, 1, 10, 0, rgb(50, 0, 0))
    for k in range(12):                                                        # RELOADING...
        w += emit_at(FAB24, mres, 0, mg) + emit_at(FAC24, 2, 0, bub)
        if k % 4 == 0:
            w += emit_at(FAC24, 0, 0, tip)
        w += wait(1)
    return w


def _eighteen_wheeler(side, s):
    """Giga Impact (18 Wheeler): they hop in the cab. HONK - headlights off-screen. HONK - the nose of an 18-wheeler,
    the foe turns. HOOOOOOONK - it barrels across the whole screen straight through them."""
    sx = _sx(side)
    y = _p(side, 72, 108)
    fx = _S23_AT["enemy" if side == "player" else "player"][0]
    tr = _p(side, 1, 2)
    start = -150 if side == "player" else 410
    pos = lambda x: _s23(side, 0, (x, y))
    w = se(s["whoosh"]) + bmove(side, 258, 3, 0, 10) + func(40, 2, 1) + wait(2)   # *hops in*
    w += func(33, 0, 1, 0, 6, rgb(20, 20, 40)) + wait(2)
    for n, (x, ticks) in enumerate(((start - sx * 40, 6), (start + sx * 130, 8))):   # HONK... HONK...
        w += se(s["horn"]) + emit_at(TRUCK24, 0, 0, _s23(side, 0, (_p(side, 10, 246), y + 8)))
        w += _hold(TRUCK24, tr, 0, pos(x), ticks, lambda k: (bmove(side, 264, 2, -sx * 6, 0) if n == 1 and k == 2 else []))
        if n == 1:
            w += bmove(side, 264, 2, sx * 6, 0)
    for k in range(3):                                                         # HOOOOOOONK
        w += se(s["horn"]) + emit_at(TRUCK24, tr, 0, pos(start + sx * 130)) + emit_at(TRUCK24, 0, 0, _s23(side, 0, (_p(side, 30, 226), y + 8))) + wait(1)
    w += flash_screen(3) + func(34, 8, 0, 1, rgb(255, 255, 255), 12, 0) + shake_defender(1, 2) + wait(2)
    hit = False
    xs = [start + sx * (130 + 90 * (k + 1)) for k in range(7)]
    for x in xs:                                                               # VRRRRRRRMMMMM
        w += emit_at(TRUCK24, tr, 0, pos(x)) + emit_at(TRUCKB24, 0, 0, _s23(side, 0, (x - sx * 120, y + 30)))
        if not hit and (x - fx) * sx > 30:
            hit = True
            w += se(s["kaboom"]) + se(s["bslam"]) + se(s["smash"]) + flash_screen(6) + func(68, 8, 6, 1, 6, 0)
            w += emit_at(TRUCKB24, 1, 1, (0, 20)) + bmove(side, 264, 3, sx * 40, 34) + func(34, 8, 0, 1, rgb(255, 80, 40), 14, 0)
        w += wait(1)
    w += func(33, 0, 1, 6, 0, rgb(20, 20, 40)) + emit_at(TRUCKB24, 0, 1, (0, 10)) + wait(3)
    w += bmove(side, 264, 4, -sx * 40, -34) + se(s["bslam"]) + shake_defender(3, 2) + emit_at(TRUCKB24, 2, 1, (0, 40))
    w += wait(6) + func(40, 2, 0) + bmove(side, 258, 3, 0, -10) + shake_attacker(2, 3) + wait(4)   # (the driver's dizzy too)
    return w


def _holy_fire(side, s):
    """Sacred Fire (Holy Fire): the lights go down, stained glass. "CAN I GET AN AMEN?" ... nothing. "I SAID CAN I
    GET AN AMEN?!" ... "...amen." Then the window blazes, the sky opens, and a pillar of holy fire comes down on
    the foe. They walk out of it with a halo."""
    sx = _sx(side)
    win = _s23(side, 0, (214, 34))
    bub = _p(side, (sx * 50, 58), (-40, 30))
    fbub = _p(side, (-30, 36), (50, 58))
    window = lambda lit=False: emit_at(HOLY24, 2 if lit else 1, 0, win)
    w = func(33, 0, 1, 0, 10, rgb(50, 30, 80)) + se(s["safeguard"]) + _hold(HOLY24, 1, 0, win, 4)
    w += _hold(HOLYB24, 1, 0, bub, 10, lambda k: window())
    w += _hold(HOLY24, 1, 0, win, 6)                                           # *...crickets*
    w += bmove(side, 258, 2, 0, 6) + se(s["rage"])
    w += _hold(HOLYB24, 2, 0, bub, 11, lambda k: window() + (bmove(side, 258, 2, 0, -6) if k == 2 else []))
    w += _hold(HOLYC24, 1, 1, fbub, 8, lambda k: window())                     # "...amen."
    w += se(s["sbeam"]) + flash_screen(4) + func(33, 0, 1, 10, 0, rgb(50, 30, 80))   # *the window blazes*
    for k in range(4):
        w += window(True) + emit_at(HOLYB24, 0, 1, ((k - 2) * 30, 96)) + wait(1)
    w += emit_at(HOLY24, 0, 1, (0, 110))
    w += _hold(HOLY24, 2, 0, win, 8, lambda k: emit_at(HOLYB24, 0, 1, ((k % 3 - 1) * 40, 100)) if k % 3 == 0 else [])
    w += se(s["flame"]) + se(s["kaboom"]) + flash_screen(5) + func(68, 4, 6, 1, 6, 0)   # FWOOOOOM
    for k in range(16):
        w += emit_at(HOLYC24, 0, 1, ((k % 3 - 1) * 6, 4 + (k % 3) * 24)) + window(True)
        if k % 3 == 0:
            w += shake_defender(2, 1) + se(s["ember"])
        if k == 4:
            w += func(34, 8, 0, 1, rgb(255, 140, 30), 14, 0)
        w += wait(1)
    for k in range(12):                                                        # *halo*
        w += emit_at(HOLYC24, 2, 1, (0, 46 + (k % 2))) + window(True) + wait(1)
    return w + func(48) + wait(2)


def _sentencing(side, s):
    """Judgment (Sentencing): court is in session. BANG. BANG. GUILTY! The courtroom goes dark - and a GIANT gavel
    comes down out of the sky on the foe."""
    g = _s23(side, 0, (104, 86))
    sign = _p(side, (0, 58), (0, 50))
    bang = lambda: se(s["bonk"]) + emit_at(GAVEL24, 0, 0, (g[0], g[1] - 10)) + func(68, 1, 1, 1, 1, 0)
    w = func(33, 0, 1, 0, 8, rgb(70, 40, 20)) + se(s["pop"]) + _hold(GAVEL24, 1, 0, (g[0], g[1] + 10), 3)
    for n in range(2):                                                         # BANG... BANG...
        w += emit_at(GAVEL24, 1, 0, (g[0], g[1] + 14)) + wait(1) + emit_at(GAVEL24, 1, 0, g) + bang() + wait(1)
        w += _hold(GAVEL24, 1, 0, g, 4 + n)
    w += se(s["chaching"])
    for k in range(12):                                                        # GUILTY! bang bang bang
        w += emit_at(GAVELB24, 1, 0, sign) + emit_at(GAVEL24, 1, 0, (g[0], g[1] + (8 if k % 2 else 0)))
        if k % 2 == 1:
            w += bang()
        if k == 6:
            w += shake_defender(2, 2)
        w += wait(1)
    w += _hold(GAVEL24, 1, 0, g, 3) + wait(3)   # *...the room goes dark*
    for k in range(5):                                                         # *the sky*
        t = ((k + 1) / 5) ** 1.8
        w += emit_at(GAVEL24, 2, 1, (-33, round(160 - 161 * t))) + wait(1)
    w += se(s["kaboom"]) + se(s["bslam"]) + se(s["explo"]) + flash_screen(6) + func(68, 8, 8, 1, 6, 0)   # SLAMMED
    w += emit_at(GAVELB24, 0, 1, (0, 0)) + bmove(side, 264, 2, 0, -12) + shake_defender(4, 3)
    w += _hold(GAVEL24, 2, 1, (-33, -1), 6)
    for k in range(4):
        w += emit_at(GAVEL24, 2, 1, (-33, -1 + (k + 1) * 34)) + wait(1)
    w += bmove(side, 264, 4, 0, 12) + func(33, 0, 1, 8, 0, rgb(70, 40, 20)) + func(48)
    return w + wait(4)


def _clock_out(side, s):
    """Roar of Time (Clock Out): the time clock reads 4:58. Tick. Tick. 4:59 - the longest minute in history. 5:00 -
    the card goes in, KA-CHUNK - and they clock out so hard time itself stops: sepia, clocks everywhere, a roar
    that rings out over the foe. Then time snaps back - all at once."""
    sx = _sx(side)
    c = _s23(side, 0, (104, 84))
    slot = (c[0] - 4, c[1] - 6)
    w = se(s["pop"]) + _hold(CLOCK24, 1, 0, c, 3)
    for kit, res, ticks, gap in ((CLOCK24, 1, 6, 3), (CLOCK24, 2, 12, 4)):    # tick... tick...  (4:58, 4:59)
        for k in range(ticks):
            w += emit_at(kit, res, 0, c)
            if k % gap == 0:
                w += se(s["clock"])
            if res == 2 and k in (3, 7):
                w += bmove(side, 258, 1, 0, 4) + wait(1) + bmove(side, 258, 1, 0, -4)   # *taps foot*
            w += wait(1)
    w += se(s["bling"]) + _hold(CLOCKB24, 1, 0, c, 3)                          # 5:00
    w += se(s["whoosh"]) + _lob(CLOCKB24, 2, side, (sx * 24, 26), slot, 4, 12, lambda k: emit_at(CLOCKB24, 1, 0, c))
    w += se(s["bslam"]) + _hold(CLOCKB24, 1, 0, c, 2)                          # KA-CHUNK
    w += se(s["rage"]) + se(s["kaboom"]) + flash_screen(5) + func(33, 0, 1, 0, 13, rgb(150, 110, 60))   # CLOCK. OUT.
    w += func(34, 8, 0, 1, rgb(150, 150, 150), 15, 0) + func(68, 3, 3, 1, 14, 0)
    for k in range(16):
        w += emit_at(CLOCKB24, 1, 0, c)
        if k % 3 == 0:
            w += emit_at(CLOCK24, 0, 0, (0, 30)) + se(s["bdrum"] if k % 2 == 0 else s["clock"])
        if k in (1, 6, 11):
            w += emit_at(CLOCKC24, 0, 1, (0, 30)) + emit_at(CLOCKC24, 0, 0, (sx * 60, 50))
        w += wait(1)
    w += se(s["kaboom"]) + flash_screen(6) + func(33, 0, 1, 13, 0, rgb(150, 110, 60))   # *snap*
    w += shake_defender(5, 4) + func(48) + func(34, 8, 0, 1, rgb(255, 230, 120), 12, 0)
    return w + _hold(CLOCKB24, 1, 0, c, 6)
'''

TABLE = {330: ("_full_auto_insane", ("FA24", "FAB24", "FAC24"), "Hyper Beam"),
         331: ("_eighteen_wheeler", ("TRUCK24", "TRUCKB24"), "Giga Impact"),
         332: ("_holy_fire", ("HOLY24", "HOLYB24", "HOLYC24"), "Sacred Fire"),
         333: ("_sentencing", ("GAVEL24", "GAVELB24"), "Judgment"),
         334: ("_clock_out", ("CLOCK24", "CLOCKB24", "CLOCKC24"), "Roar of Time")}

if __name__ == "__main__":
    # FA_TIP24 is used by the kit code too: define it before build_files (module level, near TARGET_FROM_ATTACKER)
    p = set23_lib.ROOT / "hood/gunfx.py"
    s = p.read_text(encoding="utf-8")
    a = 'TARGET_FROM_ATTACKER = {"player": (121, 59), "enemy": (-121, -59)}'
    assert s.count(a) == 1 and "FA_TIP24" not in s
    i = s.index("\n", s.index(a)) + 1
    s = s[:i] + 'FA_TIP24 = {"player": (68, 50), "enemy": (-67, 11)}                     # Full Auto minigun barrel tip, attacker-relative\n' + s[i:]
    p.write_text(s, encoding="utf-8", newline="")
    set23_lib.apply(NAMES, KITS, SCRIPTS.replace('FA_TIP24 = {"player": (68, 50), "enemy": (-67, 11)}                     # its barrel tip, attacker-relative\n', ''),
                    TABLE, remap=("Hyper Beam", "Giga Impact", "Sacred Fire", "Judgment", "Roar of Time"))
