"""Set 27 batch 1 (INSANE): Send It, Allergy Szn, Blackout, Aura Farm, Rush Hour (variants 424-428).
Run once from the repo root: python -X utf8 hood/test/reel/set27_b1.py  (art: set27_b1_art.py, already in fxart)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import set23_lib  # noqa: E402

NAMES = "SEND27 SENDB27 POLL27 POLLB27 POLLC27 DARK27 DARKB27 AURA27 AURAB27 RUSH27 RUSHB27 RUSHC27".split()

KITS = '''
    # ---- set 27, batch 1 (INSANE) -------------------------------------------------------------------------
    # Send It (Brave Bird): the projects roof, a bedsheet cape - hop, nothing - hop, nothing - SEND IT: a flaming dive
    b, rs = pk(SEND27, {1: (fxart.hero_cape(), .9, 4, {}), 2: (flipx(fxart.hero_cape()), .9, 4, {})}, alpha=fxart.soft_puff())
    burst(b, rs, 0, rgb(255, 120, 20), rgb(255, 240, 120), .35, 6, .1, up=.04, life=14, radius=.3)
    fin(SEND27, b, rs, (0, 1, 2))
    b, rs = pk(SENDB27, {1: (fxart.roof_ledge(), 1.5, 4, {}), 2: (fxart.dive_crater(), 1.5, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 240, 120), rgb(255, 255, 255), .4, 6, .06, up=.05, life=24, radius=.3)
    burst(b, rs, 3, rgb(150, 120, 90), rgb(220, 200, 170), .5, 18, .34, up=.24, gravity=.02, life=26)
    fin(SENDB27, b, rs, (0, 1, 2, 3))

    # Allergy Szn (Seed Flare): POLLEN HIGH - VERY HIGH - EXTREME - a giant flower blows - ACHOO!
    b, rs = pk(POLL27, {1: (fxart.pollen_board(), ONE_TO_ONE, 4, {"colors": 30}), 2: (fxart.pollen_board(level="VERY HIGH"), ONE_TO_ONE, 4, {"colors": 30})},
               alpha=fxart.pollen_dot())
    burst(b, rs, 0, rgb(250, 220, 60), rgb(255, 250, 180), .3, 6, .12, up=.04, life=30, radius=.6)
    fin(POLL27, b, rs, (0, 1, 2))
    b, rs = pk(POLLB27, {1: (fxart.pollen_board(level="EXTREME"), ONE_TO_ONE, 4, {"colors": 30}), 2: (fxart.monster_flower(), 1.9, 4, {})},
               alpha=fxart.pollen_dot())
    burst(b, rs, 0, rgb(250, 220, 60), rgb(255, 250, 180), .5, 26, .4, up=.12, life=40, radius=.8)
    fin(POLLB27, b, rs, (0, 1, 2))
    b, rs = pk(POLLC27, {1: (fxart.monster_flower(open_=0), 1.9, 4, {}),
                         2: (fxart.burst_sign(["ACHOO!"], fill=(255, 230, 60, 255), text=(200, 40, 30, 255)), SIGN_SCALE, 4, {"colors": 30})})
    fin(POLLC27, b, rs, (1, 2))

    # Blackout (Dark Void): the skyline's windows go out block by block - pitch black - two eyes - Zs
    b, rs = pk(DARK27, {1: (fxart.city_skyline(), 2.0, 4, {}), 2: (fxart.city_skyline(lit=1), 2.0, 4, {})})
    fin(DARK27, b, rs, (1, 2))
    b, rs = pk(DARKB27, {1: (fxart.city_skyline(lit=0), 2.0, 4, {}), 2: (fxart.dark_eyes(), .7, 4, {})}, alpha=fxart.snore_z())
    burst(b, rs, 0, rgb(200, 210, 255), rgb(255, 255, 255), .32, 1, .03, up=.07, life=30, radius=.1)
    fin(DARKB27, b, rs, (0, 1, 2))

    # Aura Farm (Aura Sphere): pose +100 AURA - pose +500 - the giant aura ball - +10000
    b, rs = pk(AURA27, {1: (fxart.aura_tag(), ONE_TO_ONE, 4, {"colors": 30}), 2: (fxart.aura_tag(n="+500"), ONE_TO_ONE, 4, {"colors": 30})},
               alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(170, 120, 255), rgb(255, 240, 255), .45, 12, .2, up=.06, life=18)
    burst(b, rs, 3, rgb(150, 110, 255), rgb(255, 255, 255), .6, 28, .42, life=24, radius=.6)
    fin(AURA27, b, rs, (0, 1, 2, 3))
    b, rs = pk(AURAB27, {1: (fxart.aura_tag(n="+10000"), ONE_TO_ONE, 4, {"colors": 30}), 2: (fxart.aura_orb(), 1.4, 4, {})})
    fin(AURAB27, b, rs, (1, 2))

    # Rush Hour (Dragon Rush): the subway pulls in - doors open - the whole rush hour stampedes over the foe
    b, rs = pk(RUSH27, {1: (fxart.subway_car(), 1.8, 4, {}), 2: (fxart.subway_car(doors_open=True), 1.8, 4, {})}, alpha=fxart.soft_puff())
    puffs(b, rs, 0, rgb(200, 200, 190), n=4, life=16, scl=.3, up=.05)
    fin(RUSH27, b, rs, (0, 1, 2))
    b, rs = pk(RUSHB27, {1: (flipx(fxart.subway_car()), 1.8, 4, {}), 2: (flipx(fxart.subway_car(doors_open=True)), 1.8, 4, {})})
    fin(RUSHB27, b, rs, (1, 2))
    b, rs = pk(RUSHC27, {1: (fxart.commuter(), .7, 4, {}), 2: (fxart.commuter(tint=1), .7, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 250, 200), rgb(255, 255, 255), .5, 10, .28, life=10)
    fin(RUSHC27, b, rs, (0, 1, 2))
'''

SCRIPTS = '''
def _send_it(side, s):
    """Brave Bird (Send It): up on the projects roof in a bedsheet cape. Hop - nothing. Hop - nothing. Then they SEND
    IT: up off the top of the screen and back down on the foe in a ball of fire. Crater. They're seeing stars."""
    sx = _sx(side)
    dx, dy = TARGET_FROM_ATTACKER[side]
    cres = _p(side, 1, 2)
    roof = (0, 8)
    cape = lambda j=0: emit_at(SEND27, cres, 0, (-sx * (14 + j), 18))
    scene = lambda j=0: emit_at(SENDB27, 1, 0, roof) + cape(j)
    w = se(s["pop"]) + bmove(side, 258, 2, 0, 8)
    for k in range(5):
        w += scene() + wait(1)
    for n in range(2):                                                         # hop... nothing. hop... nothing.
        w += se(s["whoosh"]) + bmove(side, 258, 2, 0, 10)
        for k in range(3):
            w += emit_at(SENDB27, 1, 0, roof) + cape(k % 2 * 3) + wait(1)
        w += bmove(side, 258, 2, 0, -10) + _hold(SENDB27, 1, 0, roof, 4, lambda k: cape())
    w += se(s["gust"]) + func(33, 0, 1, 0, 14, 0) + bmove(side, 258, 3, 0, 130)   # SEND IT
    for k in range(5):
        w += emit_at(SENDB27, 1, 0, roof) + wait(1)
    w += se(s["flame"]) + bmove(side, 258, 4, dx, dy - 138)
    for k in range(5):                                                         # the fireball comes down
        t = (k + 1) / 5
        x, y = round(dx * t), round(138 + (dy - 138) * t)
        w += emit_at(SEND27, 0, 0, (x, y + 20)) + emit_at(SEND27, 0, 0, (x - sx * 8, y + 34)) + wait(1)
    w += se(s["kaboom"]) + se(s["explo"]) + flash_screen(6) + func(68, 6, 6, 1, 12, 0)
    w += emit_at(SENDB27, 3, 1, (0, 10)) + emit_at(SENDB27, 2, 1, (0, -10)) + shake_defender(5, 4) + func(48)
    for k in range(8):
        w += emit_at(SENDB27, 2, 1, (0, -10)) + (emit_at(SEND27, 0, 1, (sx * (k - 4) * 4, 6)) if k % 2 == 0 else []) + wait(1)
    w += bmove(side, 258, 4, -dx, -dy) + func(33, 0, 1, 14, 0, 0) + wait(2)   # *recoil*
    for k in range(10):
        w += (emit_at(SENDB27, 0, 0, (0, 40)) if k % 4 == 0 else []) + wait(1)
    return w + func(34, 2, 0, 1, rgb(255, 120, 120), 11, 0) + shake_attacker(2, 3)


def _allergy_szn(side, s):
    """Seed Flare (Allergy Szn): the TV pollen count - HIGH. The foe sniffles. VERY HIGH - pollen everywhere. EXTREME
    - a giant flower bursts open beside the foe and the whole screen goes yellow. ACHOO! - blown clean back."""
    sx = _sx(side)
    dx, dy = TARGET_FROM_ATTACKER[side]
    brd = _s23(side, 0, (104, 86))
    flw = (-sx * 40, 12)
    w = []
    for n, (kit, res) in enumerate(((POLL27, 1), (POLL27, 2), (POLLB27, 1))):  # HIGH... VERY HIGH... EXTREME
        w += se(s["alarm"] if n == 2 else s["pop"])
        for k in range(8 + n * 2):
            w += emit_at(kit, res, 0, brd)
            if k % (4 - n) == 0:
                w += emit_at(POLL27, 0, 1, (sx * (k * 9 % 40 - 20), 20 + k * 3 % 20))
            if k == 4:
                w += shake_defender(1 + n, 2) + (se(s["sscent"]) if n else [])
            w += wait(1)
    w += func(33, 0, 1, 0, 12, 0) + se(s["lseed"]) + _hold(POLLC27, 1, 1, flw, 5)   # the bud
    w += se(s["kaboom"]) + se(s["sbomb"]) + flash_screen(5) + func(68, 5, 5, 1, 10, 0)   # *FWOOMP*
    for k in range(12):                                                        # pollen EVERYWHERE
        w += emit_at(POLLB27, 2, 1, flw)
        if k % 2 == 0:
            w += emit_at(POLLB27, 0, 1, (flw[0] + sx * (k * 7 % 30), 20 + k * 2)) + func(34, 8, 0, 1, rgb(250, 220, 60), 13, 0)
        w += wait(1)
    w += _hold(POLLB27, 2, 1, flw, 3) + se(s["bslam"]) + se(s["boom"]) + flash_screen(4)   # ACHOO!
    w += emit_at(POLLC27, 2, 1, (sx * 6, 52)) + emit_at(POLL27, 0, 1, (0, 30)) + bmove(side, 264, 2, sx * 24, 0)
    for k in range(8):
        w += emit_at(POLLC27, 2, 1, (sx * 6, 52)) + emit_at(POLLB27, 2, 1, flw) + wait(1)
    w += bmove(side, 264, 4, -sx * 24, 0) + wait(3) + func(48) + func(33, 0, 1, 12, 0, 0)   # func 48 restores the spot it saw: after the return
    return w + wait(4)


def _blackout(side, s):
    """Dark Void (Blackout): the city skyline at night. The lights flicker - a block goes dark. Another. Then the whole
    city: pitch black. Just a pair of eyes in the dark... and the foe's out cold."""
    sx = _sx(side)
    sky = _s23(side, 0, _p(side, (92, 80), (128, 62)))
    eyes = (0, 34)
    w = se(s["pop"]) + _hold(DARK27, 1, 0, sky, 6)
    w += func(33, 0, 1, 0, 8, 0)
    for n, (kit, res) in enumerate(((DARK27, 1), (DARK27, 2), (DARK27, 1), (DARK27, 2))):   # *flicker*
        w += emit_at(kit, res, 0, sky) + (se(s["zap"]) if n == 1 else []) + wait(1)
    w += se(s["disable"]) + _hold(DARK27, 2, 0, sky, 7)                      # a block goes dark
    w += se(s["zap"]) + func(33, 0, 1, 8, 16, 0) + _hold(DARKB27, 1, 0, sky, 6)   # the whole city
    w += se(s["shadow"]) + func(34, 8, 0, 1, rgb(10, 10, 20), 15, 0) + func(34, 2, 0, 1, rgb(10, 10, 20), 15, 0)
    w += _hold(DARKB27, 1, 0, sky, 6)
    for k in range(12):                                                        # just eyes. blink.
        if k not in (5, 6):
            w += emit_at(DARKB27, 2, 0, eyes)
        if k == 2:
            w += se(s["mlook"])
        w += wait(1)
    w += se(s["sleep"]) + shake_defender(2, 2)
    for k in range(12):
        w += (emit_at(DARKB27, 0, 1, (sx * 14, 36)) if k % 3 == 0 else []) + (emit_at(DARKB27, 2, 0, eyes) if k < 6 else []) + wait(1)
    w += func(33, 0, 1, 16, 0, 0) + func(34, 8, 0, 1, rgb(80, 80, 160), 10, 0)
    return w + wait(4)


def _aura_farm(side, s):
    """Aura Sphere (Aura Farm): a pose - "+100 AURA". A cooler pose - "+500 AURA". Then they cash ALL of it in: the
    screen goes dark, a giant aura ball - thrown - and "+10000 AURA"."""
    sx = _sx(side)
    dx, dy = TARGET_FROM_ATTACKER[side]
    tag = _p(side, (sx * 34, 58), (-34, 30))
    w = []
    for n in range(2):                                                         # pose... +100. pose... +500.
        w += se(s["swipe"]) + bmove(side, 258, 2, sx * (4 if n else -4), 6) + emit_at(AURA27, 0, 0, (0, 26))
        w += se(s["bling"]) + _hold(AURA27, 1 + n, 0, tag, 9) + bmove(side, 258, 2, -sx * (4 if n else -4), -6) + wait(2)
    w += func(33, 0, 1, 0, 14, 0) + se(s["focus"])                           # cash it ALL in
    orb = (sx * 18, 34)
    for k in range(10):
        w += emit_at(AURAB27, 2, 0, (orb[0], orb[1] + (k % 2)))
        if k % 3 == 0:
            w += emit_at(AURA27, 0, 0, orb) + func(34, 2, 0, 1, rgb(170, 120, 255), 12, 0)
        w += wait(1)
    w += se(s["sbeam"]) + _lob(AURAB27, 2, side, orb, (dx, dy + 24), 4, 4)
    w += se(s["kaboom"]) + se(s["explo"]) + flash_screen(6) + func(68, 6, 6, 1, 12, 0)
    w += emit_at(AURA27, 3, 1, (0, 24)) + shake_defender(5, 4) + func(34, 8, 0, 1, rgb(170, 120, 255), 14, 0) + func(48)
    w += func(33, 0, 1, 14, 0, 0) + se(s["bling"])
    for k in range(12):                                                        # +10000 AURA
        w += emit_at(AURAB27, 1, 0, tag) + (emit_at(AURA27, 0, 0, (0, 30)) if k % 4 == 0 else []) + wait(1)
    return w


def _rush_hour(side, s):
    """Dragon Rush (Rush Hour): the subway pulls in - screech - doors open - and the entire rush hour pours out and
    stampedes right over the foe. Coffee, briefcases, nobody stops."""
    sx = _sx(side)
    dx, dy = TARGET_FROM_ATTACKER[side]
    kit = _p(side, RUSH27, RUSHB27)
    y = _p(side, 96, 80)
    xs = _p(side, (-60, 104), (320, 150))
    door = _s23(side, 0, (xs[1] + sx * 12, y + 2))
    at = lambda x: _s23(side, 0, (x, y))
    w = se(s["whoosh"]) + func(33, 0, 1, 0, 10, 0)
    for k in range(6):                                                         # it pulls in
        t = 1 - (1 - (k + 1) / 6) ** 2
        w += emit_at(kit, 1, 0, at(round(xs[0] + (xs[1] - xs[0]) * t))) + (se(s["rollout"]) if k % 2 == 0 else []) + wait(1)
    w += se(s["sface"]) + emit_at(RUSH27, 0, 0, at(xs[1] - sx * 30)) + _hold(kit, 1, 0, at(xs[1]), 5)   # *screech*
    w += se(s["alarm"]) + _hold(kit, 2, 0, at(xs[1]), 3)                     # ding - doors open
    goal = (dx + sx * 40, dy + 4)
    for k in range(16):                                                        # THE STAMPEDE
        w += emit_at(kit, 2, 0, at(xs[1]))
        for j in range(2):
            t = ((k * 2 + j) % 6 + 1) / 6
            p = _lerp(door, goal, t)
            w += emit_at(RUSHC27, 1 + (k + j) % 2, 0, (p[0], p[1] + (j * 6 - 3)))
        if k % 3 == 0:
            w += se(s["flop"] if k % 6 else s["bslam"]) + shake_defender(2, 1) + emit_at(RUSHC27, 0, 1, (0, 14))
        if k == 6:
            w += func(68, 4, 4, 1, 10, 0)
        w += wait(1)
    w += se(s["kaboom"]) + flash_screen(4) + _hold(kit, 1, 0, at(xs[1]), 3)
    w += wait(2) + func(48) + func(33, 0, 1, 10, 0, 0)
    for k in range(5):                                                         # it pulls out
        w += emit_at(kit, 1, 0, at(xs[1] + sx * 40 * (k + 1))) + wait(1)
    return w + wait(2)
'''

TABLE = {424: ("_send_it", ("SEND27", "SENDB27"), "Brave Bird"),
         425: ("_allergy_szn", ("POLL27", "POLLB27", "POLLC27"), "Seed Flare"),
         426: ("_blackout", ("DARK27", "DARKB27"), "Dark Void"),
         427: ("_aura_farm", ("AURA27", "AURAB27"), "Aura Sphere"),
         428: ("_rush_hour", ("RUSH27", "RUSHB27", "RUSHC27"), "Dragon Rush")}

if __name__ == "__main__":
    set23_lib.apply(NAMES, KITS, SCRIPTS, TABLE)
