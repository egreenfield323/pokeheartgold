"""Set 23 batch 6: Gas Up, Door Kick, Getaway, Bug Zapper, Split Bill (variants 324-328).
Run once from the repo root: python -X utf8 hood/test/reel/set23_b6.py  (art: set23_b6_art.py, already in fxart)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import set23_lib  # noqa: E402

NAMES = "GAS23 GASB23 GASC23 DOOR23 DOORB23 SCOOT23 SCOOTB23 SCOOTC23 ZAPR23 ZAPRB23 BILL23 BILLB23".split()

KITS = '''
    # ---- set 23, batch 6 ----------------------------------------------------------------------------------
    # Gas Up (Flatter): the pump nozzle goes in the foe - $5.00 - $20.00 - $99.99 - and they float up, all gassed
    b, rs = pk(GAS23, {1: (fxart.gas_pump(), ONE_TO_ONE, 4, {"colors": 30}), 2: (fxart.gas_pump(amount="$20.00"), ONE_TO_ONE, 4, {"colors": 30})},
               alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 220, 60), rgb(255, 255, 220), .45, 8, .12, up=.08, life=16)
    fin(GAS23, b, rs, (0, 1, 2))
    b, rs = pk(GASB23, {1: (fxart.gas_pump(amount="$99.99"), ONE_TO_ONE, 4, {"colors": 30}), 2: (flipx(fxart.gas_nozzle()), .55, 4, {})},
               alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 230, 60), rgb(255, 255, 220), .4, 7, .08, up=.02, life=24, radius=.5)
    fin(GASB23, b, rs, (0, 1, 2))
    b, rs = pk(GASC23, {1: (fxart.gas_nozzle(), .55, 4, {})})
    fin(GASC23, b, rs, (1,))

    # Door Kick (Mega Kick): knock knock - knock knock - "WHO IS IT?" - the door comes off its hinges into the foe
    b, rs = pk(DOOR23, {1: (fxart.front_door(), 1.15, 4, {}), 2: (fxart.front_door(flying=True), 1.0, 4, {})}, alpha=fxart.speck())
    burst(b, rs, 0, rgb(220, 200, 170), rgb(255, 255, 240), .4, 14, .24, up=.12, gravity=.016, life=20)
    fin(DOOR23, b, rs, (0, 1, 2))
    b, rs = pk(DOORB23, {1: (fxart.line_bubble(["WHO IS IT?"]), ONE_TO_ONE, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 255, 220), rgb(255, 255, 255), .35, 4, .12, life=8)
    fin(DOORB23, b, rs, (0, 1))

    # Getaway (ExtremeSpeed): the loot, a rental scooter - putt putt *beep* (battery low) - putt *beep* - TURBO
    b, rs = pk(SCOOT23, {1: (fxart.rental_scooter(), .8, 4, {}), 2: (flipx(fxart.rental_scooter()), .8, 4, {})}, alpha=fxart.speck())
    burst(b, rs, 0, rgb(255, 255, 255), rgb(255, 255, 255), .4, 8, .3, life=10)
    fin(SCOOT23, b, rs, (0, 1, 2))
    b, rs = pk(SCOOTB23, {1: (fxart.battery_low(), .45, 4, {}), 2: (fxart.battery_low(full=True), .45, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 240, 60), rgb(255, 255, 220), .45, 8, .2, life=12)
    fin(SCOOTB23, b, rs, (0, 1, 2))
    b, rs = pk(SCOOTC23, {1: (fxart.loot_sack(), .5, 4, {})}, alpha=fxart.speck())
    burst(b, rs, 0, rgb(80, 200, 90), rgb(200, 255, 200), .4, 12, .24, up=.14, gravity=.012, life=22, spin=0x0800)
    fin(SCOOTC23, b, rs, (0, 1))

    # Bug Zapper (Zap Cannon): the porch zapper hums - a moth, ZZT - another, ZZT - then the foe drifts toward the
    # light. BZZZZZT.
    b, rs = pk(ZAPR23, {1: (fxart.bug_zapper(), .9, 4, {}), 2: (fxart.bug_zapper(lit=False), .9, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(200, 220, 255), rgb(255, 255, 255), .4, 8, .2, life=10)
    burst(b, rs, 3, rgb(180, 200, 255), rgb(255, 255, 255), .55, 18, .34, life=14)
    fin(ZAPR23, b, rs, (0, 1, 2, 3))
    b, rs = pk(ZAPRB23, {1: (fxart.porch_moth(), .4, 4, {})}, alpha=fxart.soft_puff())
    puffs(b, rs, 0, rgb(90, 85, 85), n=4, life=18, scl=.3, up=.06)
    fin(ZAPRB23, b, rs, (0, 1))

    # Split Bill (Pain Split): the check lands - slide it over - it slides back - over - back - RIIIP, half each
    b, rs = pk(BILL23, {1: (fxart.check_folder(), ONE_TO_ONE, 4, {})}, alpha=fxart.glow_dot())
    burst(b, rs, 0, rgb(200, 150, 255), rgb(255, 240, 255), .3, 10, .06, up=.1, life=22, radius=.6)
    fin(BILL23, b, rs, (0, 1))
    b, rs = pk(BILLB23, {1: (fxart.receipt_half(), .55, 4, {}), 2: (fxart.receipt_half(right=True), .55, 4, {})}, alpha=fxart.speck())
    burst(b, rs, 0, rgb(250, 250, 245), rgb(255, 255, 255), .3, 10, .2, up=.1, gravity=.01, life=16)
    fin(BILLB23, b, rs, (0, 1, 2))
'''

SCRIPTS = '''
def _gas_up(side, s):
    """Flatter (Gas Up): a gas pump, the nozzle in the foe. $5.00 - they puff up a bit. $20.00 - they float.
    $99.99 - they're SO gassed they drift up off the ground, wobbling."""
    sx = _sx(side)
    pump = _s23(side, 0, (104, 84))
    noz = _p(side, (-26, 12), (26, 14))
    nkit, nres = (GASB23, 2) if side == "player" else (GASC23, 1)
    n_ = lambda: emit_at(nkit, nres, 1, noz)
    w = se(s["pop"]) + _hold(GAS23, 1, 0, pump, 3) + se(s["bonk"]) + _hold(GAS23, 1, 0, pump, 3, lambda k: n_())
    floats = 0
    for n, (kit, res, up) in enumerate(((GAS23, 1, 4), (GAS23, 2, 8), (GASB23, 1, 14))):   # glug glug
        w += se(s["bubble"])
        for k in range(6 + 2 * n):
            w += emit_at(kit, res, 0, pump) + n_()
            if k == 2:
                w += se(s["chaching"] if n == 2 else s["bubble"]) + emit_at(GAS23, 0, 1, (0, 20)) + bmove(side, 264, 4, 0, up)
                floats += up
            w += wait(1)
        w += _hold(kit, res, 0, pump, 3, lambda k: n_())
    w += se(s["confuse"]) + emit_at(GASB23, 0, 1, (0, 44)) + func(34, 8, 0, 1, rgb(255, 220, 80), 10, 0)
    for k in range(10):                                                        # *wobble wobble*
        w += emit_at(GASB23, 1, 0, pump)
        if k % 3 == 0:
            w += bmove(side, 264, 2, 6 if k % 2 == 0 else -6, 0)
        if k % 3 == 1:
            w += bmove(side, 264, 2, -6 if k % 2 == 1 else 6, 0)
        w += wait(1)
    return w + bmove(side, 264, 6, 0, -floats) + _hold(GASB23, 1, 0, pump, 4)


def _door_kick(side, s):
    """Mega Kick (Door Kick): a front door. Knock knock. Knock knock. "WHO IS IT?" - they kick it clean off its
    hinges and the whole door flies into the foe."""
    sx = _sx(side)
    door = _s23(side, 0, (106, 80))
    bub = _p(side, (-30, 36), (50, 58))
    dx, dy = TARGET_FROM_ATTACKER[side]
    dr = lambda dxy=(0, 0): emit_at(DOOR23, 1, 0, (door[0] + dxy[0], door[1] + dxy[1]))
    w = se(s["pop"]) + _hold(DOOR23, 1, 0, door, 4)
    for n in range(2):                                                         # knock knock
        for k in range(2):
            w += se(s["bonk"]) + emit_at(DOORB23, 0, 0, (door[0] - sx * 6, door[1] + 4)) + dr((sx, 0)) + wait(1) + dr() + wait(1)
        w += _hold(DOOR23, 1, 0, door, 5 + n)
    for k in range(10):                                                        # "WHO IS IT?"
        w += dr() + emit_at(DOORB23, 1, 1, bub) + wait(1)
    w += dr() + wait(1)
    w += bmove(side, 258, 2, sx * 16, 12) + se(s["bslam"]) + se(s["crack"]) + emit_at(DOOR23, 0, 0, door) + flash_screen(2)   # KICK
    pts = _arc(door, (dx - sx * 4, dy + 22), 5, 10)
    for k in range(1, 5):
        w += emit_at(DOOR23, 2, 0, pts[k]) + wait(1)
    w += se(s["kaboom"]) + emit_at(DOOR23, 0, 1, (0, 24)) + flash_screen(3) + shake_defender(4, 3) + func(48) + func(68, 4, 4, 1, 3, 0)
    w += _hold(DOOR23, 2, 0, (dx - sx * 4, dy + 16), 3) + bmove(side, 258, 4, -sx * 16, -12)
    pts = _arc((dx - sx * 4, dy + 16), (dx + sx * 30, dy - 10), 4, 8)
    for k in range(1, 4):
        w += emit_at(DOOR23, 2, 0, pts[k]) + wait(1)
    return w + wait(3)


def _getaway(side, s):
    """ExtremeSpeed (Getaway): the loot sack, a rental e-scooter. Putt putt... *beep* - battery low. Putt...
    *beep*. Then the battery goes full - TURBO - ZOOM straight through the foe."""
    sx = _sx(side)
    sc = _p(side, (sx * 26, 14), (-6, -16))
    res = _p(side, 1, 2)
    bag = (sc[0] + sx * 8, sc[1] + 14)
    batt = (0, _p(side, 58, 50))
    ride = lambda: emit_at(SCOOT23, res, 0, sc) + emit_at(SCOOTC23, 1, 0, bag)
    step = (sx * 10, sx * 4)
    zoom = (sx * 92, sx * 42)
    w = se(s["pop"]) + _hold(SCOOT23, res, 0, sc, 3, lambda k: emit_at(SCOOTC23, 1, 0, bag))
    for n in range(2):                                                         # putt putt... *beep*
        w += se(s["rollout"]) + bmove(side, 258, 8, *step)
        w += _hold(SCOOT23, res, 0, sc, 4, lambda k: emit_at(SCOOTC23, 1, 0, bag))
        for k in range(6):
            w += ride() + (emit_at(SCOOTB23, 1, 0, batt) if k % 2 == 0 else [])
            if k == 0:
                w += se(s["lockon"])
            w += wait(1)
        w += _hold(SCOOT23, res, 0, sc, 2, lambda k: emit_at(SCOOTC23, 1, 0, bag))
    w += se(s["dcharge"]) + emit_at(SCOOTB23, 0, 0, batt)                      # *TURBO*
    w += _hold(SCOOTB23, 2, 0, batt, 4, lambda k: ride())
    w += se(s["jet"]) + bmove(side, 258, 3, *zoom) + emit_at(SCOOT23, 0, 0, (-sx * 20, 0))   # ZOOM
    w += ride() + wait(1) + ride() + wait(1)
    w += se(s["kaboom"]) + se(s["bslam"]) + flash_screen(4) + emit_at(SCOOTC23, 0, 1, (0, 24))
    w += shake_defender(4, 3) + func(48) + func(68, 4, 4, 1, 3, 0) + ride() + wait(1)
    w += bmove(side, 258, 6, -zoom[0] - 2 * step[0], -zoom[1] - 2 * step[1])
    return w + _hold(SCOOT23, res, 0, sc, 5, lambda k: emit_at(SCOOTC23, 1, 0, bag))


def _bug_zapper(side, s):
    """Zap Cannon (Bug Zapper): a porch bug zapper humming purple. A moth flutters in - ZZT. Another - ZZT. Then the
    foe starts drifting toward the light, hypnotized... BZZZZZZT."""
    sx = _sx(side)
    zp = _s23(side, 0, _p(side, (150, 40), (110, 98)))
    drift = _p(side, (-16, 14), (18, 14))
    z = lambda k=0: emit_at(ZAPR23, 1 if k % 5 else 2, 0, zp)
    w = se(s["spark"]) + _hold(ZAPR23, 1, 0, zp, 4, z)
    for n in range(2):                                                         # flutter... ZZT
        start = (zp[0] + _p(side, 70, -70) * (1 if n == 0 else -1) * -1, zp[1] + (40 if n == 0 else -30))
        for k in range(6):
            t = (k + 1) / 6
            w += z(k + 1) + emit_at(ZAPRB23, 1, 0, (round(start[0] + (zp[0] - start[0]) * t), round(start[1] + (zp[1] - start[1]) * t + (6 if k % 2 else -6)))) + wait(1)
        w += se(s["spark"]) + emit_at(ZAPR23, 0, 0, zp) + emit_at(ZAPRB23, 0, 0, (zp[0], zp[1] - 6)) + flash_screen(1)
        w += _hold(ZAPR23, 1, 0, zp, 5, z)
    w += se(s["mlook"])                                                        # *...the light...*
    for k in range(4):
        w += bmove(side, 264, 4, drift[0] // 4, drift[1] // 4) + _hold(ZAPR23, 1, 0, zp, 2, z)
    w += se(s["tbolt"]) + se(s["spark"]) + flash_screen(5) + emit_at(ZAPR23, 3, 0, zp) + emit_at(ZAPR23, 3, 0, (zp[0] - drift[0], zp[1] - drift[1] + 20))   # BZZZZT
    for k in range(10):
        w += z(k)
        if k % 2 == 0:
            w += shake_defender(2, 1) + func(34, 8, 0, 1, rgb(255, 250, 80) if k % 4 == 0 else rgb(60, 60, 60), 14, 0)
        w += wait(1)
    w += func(34, 8, 0, 1, rgb(255, 250, 80), 12, 0) + emit_at(ZAPRB23, 0, 0, (zp[0] - drift[0], zp[1] - drift[1] + 30))
    return w + bmove(side, 264, 5, -(drift[0] // 4) * 4, -(drift[1] // 4) * 4) + _hold(ZAPR23, 1, 0, zp, 4, z)


def _split_bill(side, s):
    """Pain Split (Split Bill): the check lands between them. The attacker slides it over. The foe slides it back.
    Over. Back (faster). Then the attacker just rips the bill in half - half each."""
    sx = _sx(side)
    mid = _s23(side, 0, (124, 72))
    me, them = _s23(side, 0, _p(side, (100, 80), (150, 62))), _s23(side, 0, _p(side, (150, 62), (100, 80)))
    dx, dy = TARGET_FROM_ATTACKER[side]
    w = se(s["whoosh"])
    for k in range(3):                                                         # *lands*
        w += emit_at(BILL23, 1, 0, (mid[0], mid[1] + 30 - k * 10)) + wait(1)
    w += se(s["bonk"]) + _hold(BILL23, 1, 0, mid, 4)
    pos = mid
    for n, (to, who, steps) in enumerate(((them, 258, 4), (me, 264, 4), (them, 258, 3), (me, 264, 2))):
        d_ = (sx * 8, 3) if who == 258 else (-sx * 8, -3)
        w += bmove(side, who, 2, *d_) + se(s["swipe"])
        for k in range(steps):
            w += emit_at(BILL23, 1, 0, _lerp(pos, to, (k + 1) / steps)) + wait(1)
        pos = to
        w += bmove(side, who, 2, -d_[0], -d_[1]) + _hold(BILL23, 1, 0, pos, 3 if n < 3 else 4)
    for k in range(3):                                                         # *snatches it back to the middle*
        w += emit_at(BILL23, 1, 0, _lerp(pos, mid, (k + 1) / 3)) + wait(1)
    w += _hold(BILL23, 1, 0, mid, 3)
    w += se(s["slash"]) + se(s["crack"]) + emit_at(BILLB23, 0, 0, mid) + flash_screen(2)   # RIIIP
    a = _arc(mid, (sx * 10, 30), 5, 16)
    b_ = _arc(mid, (dx - sx * 10, dy + 30), 5, 16)
    left, right = _p(side, (1, 2), (2, 1))
    for k in range(1, 5):
        w += emit_at(BILLB23, left, 0, a[k]) + emit_at(BILLB23, right, 0, b_[k]) + wait(1)
    w += se(s["absorb"]) + emit_at(BILL23, 0, 0, (0, 20)) + emit_at(BILL23, 0, 1, (0, 20))
    w += func(34, 2, 0, 1, rgb(200, 150, 255), 12, 0) + func(34, 8, 0, 1, rgb(200, 150, 255), 12, 0) + shake_defender(1, 2)
    return w + _hold(BILLB23, left, 0, a[4], 6, lambda k: emit_at(BILLB23, right, 0, b_[4]))
'''

TABLE = {324: ("_gas_up", ("GAS23", "GASB23", "GASC23"), "Flatter"),
         325: ("_door_kick", ("DOOR23", "DOORB23"), "Mega Kick"),
         326: ("_getaway", ("SCOOT23", "SCOOTB23", "SCOOTC23"), "ExtremeSpeed"),
         327: ("_bug_zapper", ("ZAPR23", "ZAPRB23"), "Zap Cannon"),
         328: ("_split_bill", ("BILL23", "BILLB23"), "Pain Split")}

if __name__ == "__main__":
    set23_lib.apply(NAMES, KITS, SCRIPTS, TABLE)
