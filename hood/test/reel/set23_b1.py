"""Set 23 batch 1: Got Milk, Half Off, Crop Duster, Death Stare, Catch a Fade (variants 299-303).
Run once from the repo root: python -X utf8 hood/test/reel/set23_b1.py  (art: set23_b1_art.py, already in fxart)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import set23_lib  # noqa: E402

NAMES = "MILK23 MILKB23 MILKC23 HALF23 HALFB23 HALFC23 DUST23 DUSTB23 STARE23 FADE23 FADEB23".split()

KITS = '''
    # ---- set 23: thirty new moves (batch 1) ------------------------------------------------------------------
    # Got Milk (Milk Drink): sip... sip... CHUG the whole gallon, toss the jug - GOT MILK?
    b, rs = pk(MILK23, {1: (fxart.milk_gallon(), ONE_TO_ONE, 4, {}), 2: (fxart.milk_gallon(level="half"), ONE_TO_ONE, 4, {})},
               alpha=fxart.glow_dot())
    burst(b, rs, 0, rgb(120, 255, 140), rgb(230, 255, 230), .3, 8, .05, up=.12, life=22)
    fin(MILK23, b, rs, (0, 1, 2))
    b, rs = pk(MILKB23, {1: (fxart.milk_chug(), 1.1, 4, {}), 2: (flipx(fxart.milk_chug()), 1.1, 4, {})}, alpha=fxart.fizz_drop())
    burst(b, rs, 0, rgb(250, 250, 255), rgb(255, 255, 255), .3, 4, .08, up=.04, gravity=.012, life=14)
    fin(MILKB23, b, rs, (0, 1, 2))
    b, rs = pk(MILKC23, {1: (fxart.milk_gallon(level="empty", label=False), .8, 4, {}),
                         2: (fxart.burst_sign(["GOT MILK?"], fill=(40, 60, 140, 255), text=(255, 255, 255, 255)), SIGN_SCALE, 4, {"colors": 30})})
    fin(MILKC23, b, rs, (1, 2))

    # Half Off (Super Fang): the price gun - $20 - SALE - a giant 50% OFF tag - chomp
    b, rs = pk(HALF23, {1: (fxart.price_gun(), .9, 4, {}), 2: (flipx(fxart.price_gun()), .9, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 240, 160), rgb(255, 255, 255), .4, 6, .14, life=10)
    fin(HALF23, b, rs, (0, 1, 2))
    b, rs = pk(HALFB23, {1: (fxart.price_sticker("$20"), ONE_TO_ONE / 2, 4, {}),
                         2: (fxart.price_sticker("SALE", fill=(255, 255, 255, 255)), ONE_TO_ONE / 2, 4, {})})
    fin(HALFB23, b, rs, (1, 2))
    b, rs = pk(HALFC23, {1: (fxart.half_off_tag(), ONE_TO_ONE, 4, {"colors": 30})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 255, 255), rgb(255, 255, 255), .6, 10, .26, life=12)
    fin(HALFC23, b, rs, (0, 1))

    # Crop Duster (Poison Gas): a stroll past the foe - pfft - another - then a real crop duster dumps a green cloud
    b, rs = pk(DUST23, {1: (fxart.crop_duster(), 1.2, 4, {}), 2: (flipx(fxart.crop_duster()), 1.2, 4, {})}, alpha=fxart.soft_puff())
    burst(b, rs, 0, rgb(150, 220, 60), rgb(220, 255, 160), .4, 3, .05, life=22, alpha=(26, 20, 0), gravity=.004)
    fin(DUST23, b, rs, (0, 1, 2))
    b, rs = pk(DUSTB23, {1: (fxart.house_fly(), .4, 4, {})}, alpha=fxart.soft_puff())
    burst(b, rs, 0, rgb(110, 200, 30), rgb(180, 245, 90), .45, 9, .12, up=.04, life=28, alpha=(29, 24, 0), scl_anm=(.4, 1.3, 1.8, 60, 200))
    puffs(b, rs, 2, rgb(140, 210, 60), n=14, life=34, scl=.5, up=.03)
    fin(DUSTB23, b, rs, (0, 1, 2))

    # Death Stare (Glare): lights down, two eyes in the dark - a sweat bead - another - the foe locks up
    b, rs = pk(STARE23, {1: (fxart.stare_eyes(), 2.0, 4, {})}, alpha=fxart.fizz_drop())
    burst(b, rs, 0, rgb(150, 210, 255), rgb(240, 250, 255), .35, 1, .02, up=.02, gravity=.01, life=18)
    burst(b, rs, 2, rgb(150, 210, 255), rgb(240, 250, 255), .35, 12, .16, up=.12, gravity=.014, life=20)
    fin(STARE23, b, rs, (0, 1, 2))

    # Catch a Fade (Mega Punch): the barber pole spins - bzzz, hair flies - bzzz - "U WANT A FADE?" - POW
    b, rs = pk(FADE23, {1: (fxart.barber_pole(), .9, 4, {}), 2: (fxart.barber_pole(phase=1), .9, 4, {})}, alpha=fxart.hair_snip())
    burst(b, rs, 0, rgb(50, 35, 25), rgb(90, 70, 50), .22, 8, .08, up=.02, gravity=.02, life=18, spin=0x0800)
    fin(FADE23, b, rs, (0, 1, 2))
    b, rs = pk(FADEB23, {1: (fxart.hair_clippers(), .6, 4, {}), 2: (fxart.line_bubble(["U WANT", "A FADE?"]), ONE_TO_ONE, 4, {})},
               alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 250, 200), rgb(255, 255, 255), .6, 10, .3, life=10)
    fin(FADEB23, b, rs, (0, 1, 2))
'''

SCRIPTS = '''
def _got_milk(side, s):
    """Milk Drink (Got Milk): a gallon jug. Sip (heal). Sip. Then they CHUG the whole thing, toss the empty jug
    over their shoulder - GOT MILK?"""
    jug = _s23(side, 0, _p(side, (102, 96), (150, 66)))
    mouth = _s23(side, 0, _p(side, (70, 108), (180, 60)))
    toss = _s23(side, 0, _p(side, (-30, 30), (290, 0)))
    sign = _p(side, (0, 58), (0, 50))
    w = se(s["pop"]) + _hold(MILK23, 1, 0, jug, 4)
    for n, (lv, after) in enumerate(((1, 1), (1, 2))):                        # sip... sip...
        for k in (1, 2):
            w += emit_at(MILK23, lv, 0, _lerp(jug, mouth, k / 2)) + wait(1)
        w += se(s["bubble"]) + _hold(MILK23, lv, 0, mouth, 4, lambda k: shake_attacker(1, 1) if k == 1 else [])
        w += se(s["absorb"]) + emit_at(MILK23, 0, 0, (0, 20)) + func(34, 2, 0, 1, rgb(240, 250, 255), 8, 0)
        for k in (1, 2):
            w += emit_at(MILK23, after, 0, _lerp(mouth, jug, k / 2)) + wait(1)
        w += _hold(MILK23, after, 0, jug, 3)
    w += _hold(MILK23, 2, 0, jug, 2)                                           # *...*
    for k in (1, 2):
        w += emit_at(MILK23, 2, 0, _lerp(jug, mouth, k / 2)) + wait(1)
    chug = _p(side, 1, 2)
    for k in range(14):                                                        # CHUG CHUG CHUG
        w += emit_at(MILKB23, chug, 0, (mouth[0], mouth[1] + (2 if k % 2 else 0)))
        if k % 3 == 0:
            w += se(s["bubble"]) + shake_attacker(1, 1) + emit_at(MILKB23, 0, 0, (mouth[0] - 8, mouth[1] - 14))
        if k in (5, 10):
            w += se(s["absorb"]) + emit_at(MILK23, 0, 0, (0, 20))
        w += wait(1)
    w += se(s["whoosh"]) + _lob(MILKC23, 1, side, mouth, toss, 6, 30)        # *tosses the jug*
    w += se(s["bling"]) + func(34, 2, 0, 1, rgb(120, 255, 140), 12, 0)
    w += _hold(MILKC23, 2, 0, sign, 12, lambda k: emit_at(MILK23, 0, 0, (0, 20)) if k == 3 else [])
    return w + wait(2)


def _half_off(side, s):
    """Super Fang (Half Off): a price gun - click, a $20 sticker on the foe - click, SALE - then a giant red
    50% OFF tag slaps on and they bite. The foe's worth half now."""
    sx = _sx(side)
    gun = _s23(side, 0, _p(side, (106, 98), (150, 64)))
    tip = (gun[0] + sx * 20, gun[1] + 4)
    stick = [_p(side, (-12, 10), (-14, 14)), _p(side, (14, -4), (12, 30))]
    tag = _p(side, (0, 46), (0, 54))
    dx, dy = TARGET_FROM_ATTACKER[side]
    on = []
    g = _p(side, 1, 2)

    def dress():
        return [w_ for i in on for w_ in emit_at(HALFB23, i + 1, 1, stick[i])]
    w = se(s["pop"]) + _hold(HALF23, g, 0, gun, 3)
    for n in range(2):                                                         # click... click...
        w += se(s["lockon"]) + emit_at(HALF23, 0, 0, tip)
        for k, p in enumerate(_arc(tip, (dx + stick[n][0], dy + stick[n][1]), 5, 14, ease=1.0)[1:]):
            w += emit_at(HALF23, g, 0, (gun[0] - sx * (2 if k == 0 else 0), gun[1])) + emit_at(HALFB23, n + 1, 0, p) + dress() + wait(1)
        on.append(n)
        w += se(s["disable"]) + shake_defender(1, 1)
        if n == 1:
            w += bmove(side, 264, 3, 0, -6)                                    # *looks down at it*
        w += _hold(HALF23, g, 0, gun, 4, lambda k: dress())
        if n == 1:
            w += bmove(side, 264, 3, 0, 6)
    w += _hold(HALF23, g, 0, gun, 3, lambda k: dress())                        # *...*
    for k in range(4):                                                         # 50% OFF
        w += emit_at(HALFC23, 1, 1, (tag[0], tag[1] + round(60 * (1 - (k + 1) / 4) ** 1.4))) + dress() + wait(1)
    w += se(s["bslam"]) + se(s["chaching"]) + emit_at(HALFC23, 0, 1, tag) + shake_defender(2, 2)
    w += _hold(HALFC23, 1, 1, tag, 8, lambda k: dress())
    w += bmove(side, 258, 2, sx * 22, 8) + se(s["bite"]) + se(s["crunch"]) + flash_screen(3)    # CHOMP
    w += shake_defender(4, 3) + func(48) + func(34, 8, 0, 1, rgb(255, 60, 60), 12, 0)
    w += _hold(HALFC23, 1, 1, tag, 3, lambda k: dress())
    return w + bmove(side, 258, 4, -sx * 22, -8) + _hold(HALFC23, 1, 1, tag, 3, lambda k: dress())


def _crop_duster(side, s):
    """Poison Gas (Crop Duster): they stroll past the foe real casual - pfft, a little green puff. Stroll back -
    pfft, the foe coughs. Then a real crop-duster plane buzzes the lane and dumps a whole green cloud on them."""
    sx = _sx(side)
    w = []
    for n in range(2):                                                         # *strolls by*... pfft
        w += se(s["whoosh"]) + bmove(side, 258, 4, sx * 30, 10) + wait(2)
        w += se(s["smog"]) + emit_at(DUSTB23, 0, 0, (-sx * 20, 16 + n * 4)) + wait(2)
        if n == 0:
            w += shake_defender(1, 1) + wait(2)
        else:
            w += se(s["cough"]) + shake_defender(2, 2) + func(34, 8, 0, 1, rgb(170, 230, 90), 8, 0) + wait(2)
        w += bmove(side, 258, 4, -sx * 30, -10) + wait(3)
    w += wait(2) + se(s["jet"])                                               # *bzzzzz*
    xs = list(range(-40, 301, 26)) if side == "player" else list(range(300, -41, -26))
    fx = _S23_AT["enemy" if side == "player" else "player"][0]
    dropped = False
    for x in xs:
        w += emit_at(DUST23, _p(side, 1, 2), 1, _s23(side, 1, (x, 64)))
        w += emit_at(DUST23, 0, 1, _s23(side, 1, (x - sx * 22, 74)))
        if not dropped and (x - fx) * sx > -10:
            dropped = True
            w += se(s["smog"]) + emit_at(DUSTB23, 2, 1, (0, 14)) + emit_at(DUSTB23, 2, 1, (0, 34))
        w += wait(1)
    w += se(s["cough"]) + shake_defender(2, 3) + func(34, 8, 0, 1, rgb(130, 220, 60), 13, 0)
    for k in range(14):                                                        # *the flies move in*
        for j in range(3):
            a = (k * .7 + j * 2.1)
            w += emit_at(DUSTB23, 1, 1, (round(26 * math.cos(a)), 30 + round(10 * math.sin(a * 1.3))))
        if k == 7:
            w += se(s["cough"]) + shake_defender(1, 2)
        w += wait(1)
    return w + wait(2)


def _death_stare(side, s):
    """Glare (Death Stare): the lights go down and there's just the eyes. The foe sweats a bead. Another. Then
    they lock up completely."""
    eyes = _s23(side, 0, _p(side, (118, 70), (185, 64)))
    w = func(33, 0, 1, 0, 15, 0) + wait(3)
    w += se(s["leer"]) + _hold(STARE23, 1, 0, eyes, 6)
    for n in range(2):                                                         # gulp... gulp...
        w += emit_at(STARE23, 0, 1, (_p(side, 14, 16) * (1 if n else -1), 30)) + shake_defender(1, 1)
        w += _hold(STARE23, 1, 0, eyes, 7)
    w += _hold(STARE23, 1, 0, eyes, 3)                                         # *...*
    w += se(s["twave"]) + emit_at(STARE23, 2, 1, (0, 30)) + shake_defender(3, 3)
    for k in range(12):                                                        # *locked up*
        w += emit_at(STARE23, 1, 0, eyes)
        if k in (0, 6):
            w += func(34, 8, 0, 1, rgb(255, 240, 60), 14, 0)
        if k == 6:
            w += se(s["twave"])
        w += wait(1)
    return w + func(33, 0, 1, 15, 0, 0) + wait(4)


def _catch_a_fade(side, s):
    """Mega Punch (Catch a Fade): the barber pole spins up. Clippers over the foe's head - bzzz, hair flies.
    Bzzz again. "U WANT A FADE?" - the foe gulps - POW."""
    sx = _sx(side)
    pole = _s23(side, 0, _p(side, (112, 94), (152, 64)))
    head = _p(side, (0, 30), (0, 30))
    bub = _p(side, (sx * 50, 58), (-40, 30))
    spin = lambda k: emit_at(FADE23, 1 + k % 2, 0, pole)
    w = se(s["pop"]) + _hold(FADE23, 1, 0, pole, 3, lambda k: spin(k))
    for n in range(2):                                                         # bzzz... bzzz...
        w += se(s["zap"])
        for k in range(6):
            w += spin(k) + emit_at(FADEB23, 1, 1, (head[0] + (k % 3 - 1) * 6, head[1] + (1 if k % 2 else 0)))
            if k % 2 == 0:
                w += emit_at(FADE23, 0, 1, (head[0] + (k % 3 - 1) * 6, head[1] - 4))
            w += wait(1)
        w += shake_defender(1, 1) + _hold(FADE23, 1, 0, pole, 3, lambda k: spin(k))
    for k in range(12):                                                        # "U WANT A FADE?"
        w += spin(k) + emit_at(FADEB23, 2, 0, bub)
        if k == 6:
            w += bmove(side, 264, 3, 0, -5) + shake_defender(1, 1)            # *gulp*
        w += wait(1)
    w += bmove(side, 264, 2, 0, 5) + bmove(side, 258, 2, sx * 22, 8) + se(s["kaboom"]) + se(s["bslam"]) + flash_screen(4)
    w += emit_at(FADEB23, 0, 1, (0, 26)) + shake_defender(4, 3) + func(68, 4, 4, 1, 3, 0) + func(48)
    w += bmove(side, 258, 4, -sx * 22, -8)
    return w + _hold(FADE23, 1, 0, pole, 4, lambda k: spin(k))
'''

TABLE = {299: ("_got_milk", ("MILK23", "MILKB23", "MILKC23"), "Milk Drink"),
         300: ("_half_off", ("HALF23", "HALFB23", "HALFC23"), "Super Fang"),
         301: ("_crop_duster", ("DUST23", "DUSTB23"), "Poison Gas"),
         302: ("_death_stare", ("STARE23",), "Glare"),
         303: ("_catch_a_fade", ("FADE23", "FADEB23"), "Mega Punch")}

if __name__ == "__main__":
    set23_lib.apply(NAMES, KITS, SCRIPTS, TABLE)
