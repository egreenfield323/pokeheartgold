"""Set 29 batch 3: Power Trade, Guard Trade, Shove Off, Dirty Cross, Open Window (variants 494-498).
Run once from the repo root: python -X utf8 hood/test/reel/set29_b3.py  (art: set29_b3_art.py, already in fxart)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import set23_lib  # noqa: E402

NAMES = "TRADE29 UMB29 BROOM29 SPRAY29 WIN29 WINB29".split()

KITS = '''
    # ---- set 29, batch 3 ----------------------------------------------------------------------------------
    # Power Trade (Power Swap): their pre-workout, the foe's chamomile - swapped
    b, rs = pk(TRADE29, {1: (fxart.preworkout_tub(), .6, 4, {}), 2: (fxart.chamomile_box(), .6, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 230, 120), rgb(255, 255, 255), .4, 10, .2, life=14)
    fin(TRADE29, b, rs, (0, 1, 2))

    # Guard Trade (Guard Swap): the foe's sturdy umbrella, their busted one - swapped - and then it rains
    b, rs = pk(UMB29, {1: (fxart.big_umbrella(), .8, 4, {}), 2: (fxart.big_umbrella(busted=True), .8, 4, {})}, alpha=fxart.fizz_drop())
    burst(b, rs, 0, rgb(120, 170, 255), rgb(220, 235, 255), .22, 3, .02, gravity=.03, life=14, radius=.5)
    fin(UMB29, b, rs, (0, 1, 2))

    # Shove Off (Arm Thrust): a push broom - shove (replays per hit: short)
    b, rs = pk(BROOM29, {1: (fxart.push_broom(), .8, 4, {}), 2: (flipx(fxart.push_broom()), .8, 4, {})}, alpha=fxart.soft_puff())
    puffs(b, rs, 0, rgb(190, 170, 130), n=4, life=14, scl=.26, up=.04)
    fin(BROOM29, b, rs, (0, 1, 2))

    # Dirty Cross (Cross Poison): rattle rattle - PSST - PSST - a toxic green X tagged on the foe
    b, rs = pk(SPRAY29, {1: (fxart.spray_can(), .6, 4, {}), 2: (fxart.paint_x(), .8, 4, {})}, alpha=fxart.soft_puff())
    puffs(b, rs, 0, rgb(110, 230, 60), n=4, life=16, scl=.24, up=.03)
    fin(SPRAY29, b, rs, (0, 1, 2))

    # Open Window (Defog): fog everywhere - the window slides up - a pizza box fans it all out
    b, rs = pk(WIN29, {1: (fxart.sash_window(), 1.0, 4, {}), 2: (fxart.sash_window(opened=True), 1.0, 4, {})}, alpha=fxart.soft_puff())
    puffs(b, rs, 0, rgb(200, 200, 210), n=3, life=22, scl=.42, up=.02)
    fin(WIN29, b, rs, (0, 1, 2))
    b, rs = pk(WINB29, {1: (fxart.pizza_box_fan(), .7, 4, {}), 2: (flipx(fxart.pizza_box_fan()), .7, 4, {})})
    fin(WINB29, b, rs, (1, 2))
'''

SCRIPTS = '''
def _power_trade(side, s):
    """Power Swap (Power Trade): a tub of pre-workout over them, a box of chamomile tea over the foe. Swapped. Now
    the foe's hyped up and they're... calm. On purpose."""
    dx, dy = TARGET_FROM_ATTACKER[side]
    a, b = (0, _p(side, 62, 54)), (dx, dy + 46)
    both = lambda pa, pb, r=(1, 2): emit_at(TRADE29, r[0], 0, pa) + emit_at(TRADE29, r[1], 0, pb)
    w = se(s["pop"])
    for k in range(8):
        w += both(a, b) + wait(1)
    w += se(s["whoosh"])
    for k in range(6):                                                         # swap
        t = (k + 1) / 6
        h = round(24 * 4 * t * (1 - t))
        pa, pb = _lerp(a, b, t), _lerp(b, a, t)
        w += both((pa[0], pa[1] + h), (pb[0], pb[1] - h)) + wait(1)
    w += se(s["bling"]) + emit_at(TRADE29, 0, 0, a) + emit_at(TRADE29, 0, 1, (0, 46))
    w += func(34, 2, 0, 1, rgb(250, 230, 150), 11, 0) + func(34, 8, 0, 1, rgb(255, 90, 90), 11, 0)
    for k in range(10):
        w += both(b, a) + wait(1)
    return w


def _guard_trade(side, s):
    """Guard Swap (Guard Trade): they're under a busted bodega umbrella, the foe's under a big sturdy golf umbrella.
    Swapped. Then it starts pouring - right on the foe."""
    dx, dy = TARGET_FROM_ATTACKER[side]
    a, b = (0, _p(side, 58, 52)), (dx, dy + 44)
    both = lambda pa, pb: emit_at(UMB29, 2, 0, pa) + emit_at(UMB29, 1, 0, pb)
    w = se(s["pop"])
    for k in range(8):
        w += both(a, b) + wait(1)
    w += se(s["whoosh"])
    for k in range(6):                                                         # swap
        t = (k + 1) / 6
        h = round(24 * 4 * t * (1 - t))
        pa, pb = _lerp(a, b, t), _lerp(b, a, t)
        w += both((pa[0], pa[1] + h), (pb[0], pb[1] - h)) + wait(1)
    w += se(s["raindance"] if "raindance" in s else s["splash"])
    for k in range(14):                                                        # ...and it pours on the foe
        w += both(b, a)
        if k % 2 == 0:
            w += emit_at(UMB29, 0, 0, (dx + (k % 4 - 2) * 6, dy + 60))
        if k == 6:
            w += func(34, 8, 0, 1, rgb(120, 170, 255), 12, 0) + shake_defender(1, 2)
        w += wait(1)
    return w


def _shove_off(side, s):
    """Arm Thrust (Shove Off): a push broom sweeps the foe right off their spot - shove. (Replays per hit: short.)"""
    sx = _sx(side)
    res = _p(side, 1, 2)
    w = se(s["swipe"])
    for k in range(3):
        w += emit_at(BROOM29, res, 1, (-sx * (50 - k * 10), 6)) + wait(1)
    w += se(s["bonk"]) + func(48) + bmove(side, 264, 2, sx * 10, 0) + emit_at(BROOM29, 0, 1, (-sx * 10, -2))
    w += emit_at(BROOM29, res, 1, (-sx * 16, 6)) + wait(1) + emit_at(BROOM29, res, 1, (-sx * 14, 6)) + wait(2)
    w += bmove(side, 264, 3, -sx * 10, 0) + wait(3)
    return w + wait(8)


def _dirty_cross(side, s):
    """Cross Poison (Dirty Cross): a spray can by the foe - rattle rattle. PSST - one stroke. PSST - the other. A dirty
    green X tagged right on them. Toxic."""
    sx = _sx(side)
    can = (-sx * 28, 34)
    w = se(s["pop"])
    for k in range(6):                                                         # rattle rattle
        w += emit_at(SPRAY29, 1, 1, (can[0], can[1] + (3 if k % 2 else -3))) + (se(s["peck"]) if k % 2 == 0 else []) + wait(1)
    for n in range(2):                                                         # PSST... PSST
        w += se(s["spray"])
        for k in range(4):
            y = 40 - k * 10
            x = (-12 + k * 8) * (1 if n == 0 else -1)
            w += emit_at(SPRAY29, 1, 1, can) + emit_at(SPRAY29, 0, 1, (x, y)) + wait(1)
    w += se(s["slash"]) + se(s["toxic"]) + flash_screen(2) + func(48) + shake_defender(3, 2)   # TAGGED
    w += func(34, 8, 0, 1, rgb(110, 230, 60), 12, 0)
    for k in range(10):
        w += emit_at(SPRAY29, 2, 1, (0, 22)) + (emit_at(SPRAY29, 1, 1, can) if k < 5 else []) + wait(1)
    return w + wait(3) + wait(8)


def _open_window(side, s):
    """Defog (Open Window): fog everywhere. A window - they shove it open. Then a greasy pizza box, fanning like
    crazy - the fog rolls out the window till it's clear."""
    win = _s23(side, 0, (124, 70))
    fan = (win[0] + 30, win[1] - 20)
    w = func(33, 0, 1, 0, 8, 0) + se(s["haze"] if "haze" in s else s["smoke"])
    for k in range(8):                                                         # fog everywhere
        w += emit_at(WIN29, 0, 0, (win[0] + (k * 37 % 120) - 60, win[1] + (k * 23 % 60) - 40)) + emit_at(WIN29, 1, 0, win) + wait(1)
    w += se(s["swipe"]) + _hold(WIN29, 2, 0, win, 3)                          # shoved open
    for k in range(14):                                                        # fan it out
        w += emit_at(WIN29, 2, 0, win) + emit_at(WINB29, 1 + k % 2, 0, (fan[0] + (k % 2) * 6, fan[1] + (k % 2) * 4))
        if k % 2 == 0:
            p = (win[0] + 60 - k * 4, win[1] - 30 + (k * 5) % 30)
            w += emit_at(WIN29, 0, 0, p) + se(s["gust"] if k % 4 == 0 else s["whoosh"])
        w += wait(1)
    w += func(33, 0, 1, 8, 0, 0) + se(s["bling"]) + func(34, 8, 0, 1, rgb(220, 220, 230), 10, 0)
    return w + _hold(WIN29, 2, 0, win, 6)
'''

TABLE = {494: ("_power_trade", ("TRADE29",), "Power Swap"),
         495: ("_guard_trade", ("UMB29",), "Guard Swap"),
         496: ("_shove_off", ("BROOM29",), "Arm Thrust"),
         497: ("_dirty_cross", ("SPRAY29",), "Cross Poison"),
         498: ("_open_window", ("WIN29", "WINB29"), "Defog")}

if __name__ == "__main__":
    set23_lib.apply(NAMES, KITS, SCRIPTS, TABLE)
