"""Pistol Whip (Scratch) redo, variant 500 (Scratch remapped off 294). PARKED 2026-11-03: the user had it undone
and will ask for it back. To put it back, from the repo root:
    cat hood/test/reel/set30_pw_art.py >> hood/fxart.py
    python -X utf8 hood/test/reel/set30_pw.py
then rebuild with hood/patch_rom.py. Verified both sides in DeSmuME before it was parked."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import set23_lib  # noqa: E402

NAMES = "PW30 PWB30 PWC30".split()

KITS = '''
    # ---- Pistol Whip redo -------------------------------------------------------------------------------------------
    # aimed - *click* - *click* - empty. Flipped round, grip first - WHAP. Seeing stars.
    b, rs = pk(PW30, {1: (fxart.whip_pistol(), .9, 4, {}), 2: (flipx(fxart.whip_pistol()), .9, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 250, 200), rgb(255, 255, 255), .6, 14, .32, life=14)
    fin(PW30, b, rs, (0, 1, 2))
    b, rs = pk(PWB30, {1: (fxart.whip_pistol(pose="whip"), .9, 4, {}), 2: (flipx(fxart.whip_pistol(pose="whip")), .9, 4, {})})
    fin(PWB30, b, rs, (1, 2))
    b, rs = pk(PWC30, {1: (fxart.click_bubble(), ONE_TO_ONE / 2, 4, {})}, alpha=fxart.tiny_spark())
    prop(b, rs, 0, tex=0, clr=rgb(255, 230, 60), clr_anm=(rgb(255, 230, 60), rgb(255, 230, 60)), scl=.45, life=4)   # dizzy stars
    fin(PWC30, b, rs, (0, 1))
'''

SCRIPTS = '''
def _pistol_whip2(side, s):
    """Scratch (Pistol Whip): the pistol comes up, aimed at the foe. *click*. ...*click*. Empty. They stare at it. So
    they flip it round, grab the barrel, lunge in and WHAP the foe with the grip. The foe's seeing stars."""
    sx = _sx(side)
    dx, dy = TARGET_FROM_ATTACKER[side]
    res = _p(side, 1, 2)
    gun = (sx * 32, 30)
    bub = (gun[0] + sx * 14, gun[1] + 24)
    g = lambda o=(0, 0), j=0: emit_at(PW30, res, 0, (gun[0] + o[0] + j, gun[1] + o[1]))
    w = se(s["pop"])
    for k in range(3):                                                         # it comes up
        w += g((0, -12 + k * 4)) + wait(1)
    w += se(s["lockon"]) + _hold(PW30, res, 0, gun, 4)                        # aimed
    for n in range(2):                                                         # *click* ... *click*
        w += se(s["disable"])
        for k in range(6):
            w += g(j=(1 if k < 2 and k % 2 == 0 else 0)) + emit_at(PWC30, 1, 0, bub) + wait(1)
        w += _hold(PW30, res, 0, gun, 3)
    for k in range(8):                                                         # ...they stare at it
        w += g((0, 4 if 2 <= k < 6 else 0), j=(1 if k % 4 == 0 else 0)) + wait(1)
    lunge = (round(dx * .45), round(dy * .45))
    w += se(s["whoosh"]) + bmove(side, 258, 3, lunge[0], lunge[1])            # flip it - lunge in
    for k in range(3):
        o = _lerp((0, 0), lunge, (k + 1) / 3)
        w += emit_at(PWB30, res, 0, (gun[0] + o[0], gun[1] + o[1] + 10)) + wait(1)
    hit = (dx - sx * 16, dy + 34)
    w += emit_at(PWB30, res, 0, (hit[0] - sx * 6, hit[1] + 18)) + wait(1)
    w += se(s["bslam"]) + se(s["bonk"]) + flash_screen(4) + emit_at(PWB30, res, 0, hit)   # WHAP
    w += emit_at(PW30, 0, 1, (0, 34)) + func(48) + shake_defender(4, 3) + wait(1)
    w += emit_at(PWB30, res, 0, hit) + wait(1)
    w += bmove(side, 258, 4, -lunge[0], -lunge[1])
    import math
    for k in range(16):                                                        # seeing stars
        for j in range(3):
            a = k * .55 + j * math.tau / 3
            w += emit_at(PWC30, 0, 1, (round(math.cos(a) * 16), round(44 + math.sin(a) * 5)))
        if k == 3:
            w += se(s["bonk"])
        if k < 4:
            w += emit_at(PWB30, res, 0, (gun[0], gun[1] + 10))
        w += wait(1)
    return w + wait(4)
'''

TABLE = {500: ("_pistol_whip2", ("PW30", "PWB30", "PWC30"), "Scratch")}

if __name__ == "__main__":
    set23_lib.apply(NAMES, KITS, SCRIPTS, TABLE, remap=("Scratch",))
