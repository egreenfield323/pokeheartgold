"""Set 25 batch 1 (INSANE): Burn It Down, Hydrant Bomb, Gun Garden, Meteor Drop, Blow Up (variants 362-366).
Run once from the repo root: python -X utf8 hood/test/reel/set25_b1.py  (art: set25_b1_art.py, already in fxart)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import set23_lib  # noqa: E402

NAMES = "BURN25 BURNB25 BURNC25 HYD25 HYDB25 GUN25 GUNB25 GUNC25 MET25 METB25 BLOW25 BLOWB25 BLOWC25".split()

KITS = '''
    # ---- set 25: thirty more (batch 1, INSANE) ----------------------------------------------------------------
    # Burn It Down (Blast Burn): a squirt of lighter fluid on the grill (whoomp), another (WHOOMP), then they toss
    # the whole bottle in - a mushroom fireball
    b, rs = pk(BURN25, {1: (fxart.barrel_grill(), 1.1, 4, {}), 2: (fxart.lighter_fluid(), .5, 4, {})}, alpha=fxart.holy_flame())
    burst(b, rs, 0, rgb(255, 120, 20), rgb(255, 240, 120), .4, 8, .12, up=.2, life=18)
    burst(b, rs, 3, rgb(255, 100, 20), rgb(255, 250, 160), .55, 14, .2, up=.3, life=22)
    fin(BURN25, b, rs, (0, 1, 2, 3))
    b, rs = pk(BURNB25, {1: (fxart.fireball_cloud(), 3.4, 16, {"scl_anm": (.2, 1.15, 1.0, 40, 255)})}, alpha=fxart.fizz_drop())
    burst(b, rs, 0, rgb(255, 230, 80), rgb(255, 255, 200), .3, 4, .08, gravity=.02, life=12)
    fin(BURNB25, b, rs, (0, 1))
    b, rs = pk(BURNC25, {}, alpha=fxart.holy_flame())
    spray2(b, rs, {"player": (40, 50), "enemy": (-40, 20)}, (0, 20), 12, clr=rgb(255, 110, 20),
           clr_anm=(rgb(255, 240, 140), rgb(220, 40, 10)), scl=.6, gen=2, gen_intvl=1, emtr_life=26, radius=.4,
           spread=.03, alpha=(31, 28, 0))
    fin(BURNC25, b, rs, (0, 1))

    # Hydrant Bomb (Hydro Cannon): the wrench on the hydrant - a trickle - a spurt - the cap blows off and the
    # whole hydrant becomes a water cannon
    b, rs = pk(HYD25, {1: (fxart.red_hydrant(), 1.0, 4, {}), 2: (fxart.red_hydrant(capless=True), 1.0, 4, {})}, alpha=fxart.water_jet())
    burst(b, rs, 0, rgb(120, 190, 255), rgb(230, 245, 255), .3, 4, .1, up=.04, gravity=.016, life=14)
    burst(b, rs, 3, rgb(120, 190, 255), rgb(230, 245, 255), .5, 16, .24, up=.34, gravity=.02, life=24)
    fin(HYD25, b, rs, (0, 1, 2, 3))
    b, rs = pk(HYDB25, {2: (fxart.pipe_wrench(), .55, 4, {})}, alpha=fxart.water_jet())
    spray2(b, rs, {"player": (42, 50), "enemy": (-42, 20)}, (0, 22), 10, clr=rgb(110, 180, 255),
           clr_anm=(rgb(230, 245, 255), rgb(60, 130, 240)), scl=.9, gen=3, gen_intvl=1, emtr_life=40, radius=.25,
           spread=.03, alpha=(31, 28, 0))
    fin(HYDB25, b, rs, (0, 1, 2))

    # Gun Garden (Frenzy Plant): bullets planted, watered - sprouts - stems - then a whole garden of pistol flowers
    # blooms and they all fire at once
    b, rs = pk(GUN25, {1: (fxart.flower_bed(), 1.2, 4, {}), 2: (fxart.flower_bed(stage=1), 1.2, 4, {})}, alpha=fxart.fizz_drop())
    burst(b, rs, 0, rgb(120, 190, 255), rgb(230, 245, 255), .3, 6, .06, gravity=.016, life=12)
    fin(GUN25, b, rs, (0, 1, 2))
    b, rs = pk(GUNB25, {1: (fxart.flower_bed(stage=2), 1.2, 4, {}), 2: (fxart.watering_can(), .5, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 230, 80), rgb(255, 255, 220), .5, 6, .16, life=8)
    fin(GUNB25, b, rs, (0, 1, 2))
    b, rs = pk(GUNC25, {1: (fxart.gun_flower(), .9, 4, {}), 2: (flipx(fxart.gun_flower()), .9, 4, {})}, alpha=fxart.tracer_streak())
    for res, sd in ((0, "player"), (3, "enemy")):
        spray(b, rs, res, sd, GG_TIP25[sd], (0, 24), 8, tex=0, clr=rgb(255, 230, 90), clr_anm=(rgb(255, 255, 220), rgb(255, 150, 30)),
              scl=.8, gen=3, gen_intvl=1, emtr_life=40, radius=.5, spread=.04, alpha=(31, 31, 0))
    fin(GUNC25, b, rs, (0, 1, 2, 3))

    # Meteor Drop (Draco Meteor): a pebble meteor - bonk. A bigger one - BONK. The sky goes dark... and the big one.
    b, rs = pk(MET25, {1: (fxart.meteor_rock(), .5, 4, {}), 2: (fxart.meteor_rock(), 1.0, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 160, 40), rgb(255, 250, 200), .5, 12, .26, up=.1, life=14)
    fin(MET25, b, rs, (0, 1, 2))
    b, rs = pk(METB25, {1: (fxart.meteor_rock(), 4.0, 4, {})}, alpha=fxart.soft_puff())
    puffs(b, rs, 0, rgb(255, 140, 40), n=12, life=30, scl=.5, up=.06)
    fin(METB25, b, rs, (0, 1))

    # Blow Up (Eruption): their phone: 1 notification, 12, 99+ - and it erupts like a volcano, notifications raining
    b, rs = pk(BLOW25, {1: (fxart.notif_phone(), ONE_TO_ONE, 4, {}), 2: (fxart.notif_phone(count="12"), ONE_TO_ONE, 4, {})}, alpha=fxart.holy_flame())
    burst(b, rs, 0, rgb(255, 100, 20), rgb(255, 240, 120), .5, 16, .14, up=.42, gravity=.02, life=26)
    fin(BLOW25, b, rs, (0, 1, 2))
    b, rs = pk(BLOWB25, {1: (fxart.notif_phone(count="99+"), ONE_TO_ONE, 4, {})})
    fin(BLOWB25, b, rs, (1,))
    b, rs = pk(BLOWC25, {})
    b, bell = added(b, fxart.notif_bell(), 24)
    spray2(b, rs, {"player": (36, 60), "enemy": (-36, 30)}, (0, 24), 14, art_tex=bell, clr=rgb(255, 255, 255),
           clr_anm=(rgb(255, 255, 255), rgb(255, 255, 255)), scl=.45, gen=1, gen_intvl=2, emtr_life=30, radius=.4,
           spread=.06, alpha=(31, 31, 31))
    fin(BLOWC25, b, rs, (0, 1))
'''

SCRIPTS = '''
GG_BED25 = {"player": (106, 92), "enemy": (106, 92)}


def _burn_it_down(side, s):
    """Blast Burn (Burn It Down): the cookout grill. A squirt of lighter fluid - whoomp. Another - WHOOMP (eyebrows
    gone). Then they toss the whole bottle in. *...* A mushroom fireball takes the screen and rolls over the foe."""
    sx = _sx(side)
    g = _s23(side, 0, (106, 88))
    over = (g[0] - sx * 4, g[1] + 26)
    w = se(s["pop"]) + _hold(BURN25, 1, 0, g, 3)
    for n in range(2):                                                         # squirt... whoomp
        w += _hold(BURN25, 2, 0, over, 2, lambda k: emit_at(BURN25, 1, 0, g))
        w += se(s["spray"]) + emit_at(BURNB25, 0, 0, (over[0], over[1] - 6)) + _hold(BURN25, 2, 0, over, 3, lambda k: emit_at(BURN25, 1, 0, g))
        w += se(s["ember"] if n == 0 else s["flame"]) + emit_at(BURN25, 0 if n == 0 else 3, 0, (g[0], g[1] + 8))
        if n == 1:
            w += shake_attacker(2, 2) + func(34, 2, 0, 1, rgb(60, 50, 50), 9, 0)    # *eyebrows*
        w += _hold(BURN25, 1, 0, g, 5 + n)
    w += se(s["whoosh"]) + _lob(BURN25, 2, side, (sx * 20, 30), (g[0], g[1] + 10), 5, 24, lambda k: emit_at(BURN25, 1, 0, g))
    w += se(s["ember"]) + _hold(BURN25, 1, 0, g, 6, lambda k: shake_attacker(1, 1) if k == 3 else [])   # *...tssss*
    w += func(33, 0, 1, 0, 12, rgb(160, 40, 0)) + se(s["kaboom"]) + se(s["explo"]) + flash_screen(8)   # KABOOOOM
    w += emit_at(BURNB25, 1, 0, (g[0], g[1] + 30)) + func(68, 6, 6, 1, 16, 0)
    w += emit_at(BURNC25, _p(side, 0, 1), 0, (g[0], g[1] + 20))
    for k in range(16):
        if k % 4 == 0:
            w += emit_at(BURN25, 3, 1, (((k * 13) % 30) - 15, 10 + (k * 7) % 20)) + shake_defender(2, 1)
        if k == 5:
            w += se(s["flame"]) + func(34, 8, 0, 1, rgb(255, 90, 20), 14, 0)
        w += wait(1)
    w += func(48) + func(33, 0, 1, 12, 0, rgb(160, 40, 0)) + func(34, 2, 0, 1, rgb(50, 40, 40), 12, 0)   # (they're sooty too)
    return w + _hold(BURN25, 1, 0, g, 4)


def _hydrant_bomb(side, s):
    """Hydro Cannon (Hydrant Bomb): a wrench on the fire hydrant - a trickle. Crank - a spurt. CRANK - the cap
    blows off and the hydrant turns into a water cannon aimed right at the foe."""
    h = _s23(side, 0, (106, 84))
    top = (h[0], h[1] + 22)
    nozzle = (h[0] + _sx(side) * 16, h[1] + 4)
    hy = lambda r=1: emit_at(HYD25, r, 0, h)
    w = se(s["pop"]) + _hold(HYD25, 1, 0, h, 3)
    for n in range(2):                                                         # crank... crank...
        for k in range(3):
            w += hy() + emit_at(HYDB25, 2, 0, (top[0] + (4 if k % 2 else -4), top[1] + 4)) + (se(s["harden"]) if k == 0 else []) + wait(1)
        for k in range(4 + 2 * n):
            w += hy() + (emit_at(HYD25, 0, 0, nozzle) if k % (3 - n) == 0 else []) + wait(1)
        if n == 1:
            w += shake_defender(1, 1)
    for k in range(4):                                                         # CRANK CRANK
        w += hy() + emit_at(HYDB25, 2, 0, (top[0] + (6 if k % 2 else -6), top[1] + 4)) + se(s["harden"]) + shake_attacker(1, 1) + wait(1)
    w += hy() + wait(1) + hy() + wait(1)                                       # *...*
    w += se(s["kaboom"]) + se(s["splash"]) + flash_screen(5) + emit_at(HYD25, 3, 0, top) + func(33, 0, 1, 0, 10, rgb(40, 90, 200))
    w += emit_at(HYDB25, _p(side, 0, 1), 0, top) + func(68, 4, 4, 1, 14, 0) + se(s["hpump"])
    for k in range(18):                                                        # FWOOOOOSH
        w += hy(2)
        if k % 4 == 0:
            w += shake_defender(2, 1) + se(s["surf"] if k == 0 else s["splash"])
        if k == 6:
            w += func(34, 8, 0, 1, rgb(80, 150, 255), 14, 0) + bmove(side, 264, 4, _sx(side) * 12, 4)
        w += wait(1)
    w += bmove(side, 264, 4, -_sx(side) * 12, -4) + func(48) + func(33, 0, 1, 10, 0, rgb(40, 90, 200))
    return w + _hold(HYD25, 2, 0, h, 5)


def _gun_garden(side, s):
    """Frenzy Plant (Gun Garden): they plant bullets in a flower bed. Water it - sprouts. Water it - stems. Then the
    whole bed blooms into pistol flowers... and every one of them opens fire."""
    sx = _sx(side)
    bed = _s23(side, 0, GG_BED25[side])
    can = (bed[0] - sx * 10, bed[1] + 34)
    flowers = [(bed[0] + dxx, bed[1] + 26) for dxx in (-26, 0, 26)]
    fres = _p(side, 1, 2)
    w = se(s["pop"]) + _hold(GUN25, 1, 0, bed, 4)
    for n, (kit, res) in enumerate(((GUN25, 2), (GUNB25, 1))):                # water... sprout... water... grow
        w += _hold(GUNB25, 2, 0, can, 3, lambda k: emit_at(GUN25, 1, 0, bed) if n == 0 else emit_at(GUN25, 2, 0, bed))
        w += se(s["bubble"]) + emit_at(GUN25, 0, 0, (bed[0], bed[1] + 18)) + _hold(GUNB25, 2, 0, can, 3, lambda k: emit_at(GUN25, 1 if n == 0 else 2, 0, bed))
        w += se(s["leaf"] if False else s["lseed"]) + _hold(kit, res, 0, bed, 5)
    w += _hold(GUNB25, 1, 0, bed, 3) + func(33, 0, 1, 0, 10, rgb(20, 40, 20))    # *...*
    for i, f in enumerate(flowers):                                            # bloom. bloom. BLOOM.
        w += se(s["pop"])
        for k in range(3):
            w += emit_at(GUNB25, 1, 0, bed) + [w_ for j in range(i) for w_ in emit_at(GUNC25, fres, 0, flowers[j])]
            w += emit_at(GUNC25, fres, 0, (f[0], f[1] - 16 + k * 8)) + wait(1)
    w += se(s["bling"]) + _hold(GUNB25, 1, 0, bed, 4, lambda k: [w_ for f in flowers for w_ in emit_at(GUNC25, fres, 0, f)])
    tip = GG_TIP25[side]
    w += se(s["boom"]) + flash_screen(3) + emit_at(GUNC25, _p(side, 0, 3), 0, tip) + func(68, 2, 2, 1, 20, 0)   # OPEN FIRE
    for k in range(18):
        w += emit_at(GUNB25, 1, 0, bed) + [w_ for f in flowers for w_ in emit_at(GUNC25, fres, 0, (f[0] - sx * (k % 2), f[1]))]
        w += se(s["pop"] if k % 2 else s["boom"])
        if k % 2 == 0:
            w += emit_at(GUNB25, 0, 0, flowers[(k // 2) % 3])
        if k % 4 == 0:
            w += shake_defender(2, 1)
        w += wait(1)
    w += func(48) + func(34, 8, 0, 1, rgb(60, 50, 50), 12, 0) + func(33, 0, 1, 10, 0, rgb(20, 40, 20))
    return w + _hold(GUNB25, 1, 0, bed, 4, lambda k: [w_ for f in flowers for w_ in emit_at(GUNC25, fres, 0, f)])


def _meteor_drop(side, s):
    """Draco Meteor (Meteor Drop): a pebble-sized meteor - bonk. A bigger one - BONK. The sky goes dark, a rumble...
    and the BIG one comes down and fills the whole sky."""
    w = []
    for n, (res, steps) in enumerate(((1, 5), (2, 6))):                         # bonk... BONK
        w += se(s["whoosh"])
        for k in range(steps):
            t = ((k + 1) / steps) ** 1.5
            w += emit_at(MET25, res, 1, (round(90 - 90 * t), round(130 - (100 - 10 * n) * t))) + wait(1)
        w += se(s["bonk"] if n == 0 else s["bslam"]) + emit_at(MET25, 0, 1, (0, 30)) + shake_defender(1 + 2 * n, 2) + wait(4)
    w += func(33, 0, 1, 0, 14, rgb(40, 10, 60)) + se(s["epower"]) + func(68, 1, 1, 1, 12, 0) + wait(6)   # *rumble*
    for k in range(10):                                                        # the BIG one
        t = ((k + 1) / 10) ** 1.7
        w += emit_at(METB25, 1, 1, (round(140 - 120 * t), round(200 - 150 * t))) + wait(1)
    w += se(s["kaboom"]) + se(s["explo"]) + flash_screen(8) + func(68, 8, 8, 1, 8, 0)   # IMPACT
    w += emit_at(METB25, 0, 1, (0, 20)) + emit_at(MET25, 0, 1, (0, 30)) + shake_defender(5, 4) + func(48)
    w += func(34, 8, 0, 1, rgb(255, 120, 40), 14, 0) + wait(4) + emit_at(METB25, 0, 1, (0, 40)) + wait(6)
    return w + func(33, 0, 1, 14, 0, rgb(40, 10, 60)) + wait(4)


def _blow_up(side, s):
    """Eruption (Blow Up): their phone buzzes: 1 notification. Buzz buzz: 12. BZZBZZBZZ: 99+. It's blowing up - then
    it literally erupts: lava out the top and notifications raining down on the foe."""
    sx = _sx(side)
    ph = _p(side, (sx * 40, 40), (-40, 26))
    w = []
    for n, (kit, res, ticks) in enumerate(((BLOW25, 1, 6), (BLOW25, 2, 7), (BLOWB25, 1, 10))):
        w += se(s["alarm"])
        for k in range(ticks):
            j = (1 + n) if k % 2 else -(1 + n)
            w += emit_at(kit, res, 0, (ph[0] + j, ph[1]))
            if k % (3 - min(n, 2)) == 0 and k:
                w += se(s["alarm"])
            w += wait(1)
        w += _hold(kit, res, 0, ph, 2 if n < 2 else 0)
    w += func(33, 0, 1, 0, 12, rgb(140, 30, 0)) + se(s["kaboom"]) + se(s["explo"]) + flash_screen(6)   # ERUPTION
    w += emit_at(BLOW25, 0, 0, (ph[0], ph[1] + 20)) + emit_at(BLOWC25, _p(side, 0, 1), 0, (ph[0], ph[1] + 20)) + func(68, 5, 5, 1, 14, 0)
    for k in range(18):
        w += emit_at(BLOWB25, 1, 0, (ph[0] + (2 if k % 2 else -2), ph[1]))
        if k % 6 == 0 and k:
            w += emit_at(BLOW25, 0, 0, (ph[0], ph[1] + 20)) + se(s["alarm"])
        if k % 4 == 1:
            w += shake_defender(2, 1)
        if k == 8:
            w += func(34, 8, 0, 1, rgb(255, 90, 30), 14, 0) + se(s["flame"])
        w += wait(1)
    return w + func(48) + func(33, 0, 1, 12, 0, rgb(140, 30, 0)) + _hold(BLOWB25, 1, 0, ph, 4)
'''

TABLE = {362: ("_burn_it_down", ("BURN25", "BURNB25", "BURNC25"), "Blast Burn"),
         363: ("_hydrant_bomb", ("HYD25", "HYDB25"), "Hydro Cannon"),
         364: ("_gun_garden", ("GUN25", "GUNB25", "GUNC25"), "Frenzy Plant"),
         365: ("_meteor_drop", ("MET25", "METB25"), "Draco Meteor"),
         366: ("_blow_up", ("BLOW25", "BLOWB25", "BLOWC25"), "Eruption")}

if __name__ == "__main__":
    p = set23_lib.ROOT / "hood/gunfx.py"
    s = p.read_text(encoding="utf-8")
    a = 'FA_TIP24 = {"player": (68, 50), "enemy": (-67, 11)}'
    assert s.count(a) == 1 and "GG_TIP25" not in s
    i = s.index("\n", s.index(a)) + 1
    s = s[:i] + 'GG_TIP25 = {"player": (57, 82), "enemy": (-94, 23)}                     # Gun Garden: middle flower muzzle, attacker-relative\n' + s[i:]
    p.write_text(s, encoding="utf-8", newline="")
    set23_lib.apply(NAMES, KITS, SCRIPTS, TABLE)
