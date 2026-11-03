def _same_smoke(side, s):
    """Endeavor (Same Smoke): fight prep - the earrings come off - the chain comes off - jelly on the face,
    *shine* - "WE CAN GET THE SAME SMOKE" - and they swing."""
    sx = _sx(side)
    bub = (sx * 50, 58) if side == "player" else (-40, 30)
    jar = (sx * 42, 40) if side == "player" else (-40, 26)
    w = []
    for res, frm, n in ((1, (sx * 6, 34), "earrings"), (2, (sx * 4, 16), "chain")):      # off... off
        w += se(s["swipe"]) + _hold(TREAD20, res, 0, frm, 3)
        for k in range(5):
            t = (k + 1) / 5
            w += emit_at(TREAD20, res, 0, (round(frm[0] - sx * 70 * t), round(frm[1] + 30 * t - 20 * t * t))) + wait(1)
        w += se(s["bonk"]) + wait(2)
    w += se(s["splat"]) + _hold(SMOKEB22, 1, 0, jar, 4, lambda k: shake_attacker(1, 1) if k == 1 else [])   # *jelly*
    w += se(s["bling"]) + emit_at(TREAD20, 0, 0, (sx * 10, 30)) + _hold(SMOKEB22, 1, 0, jar, 2)
    for k in range(12):                                                        # "WE CAN GET THE SAME SMOKE"
        w += emit_at(SMOKEB22, 2, 0, bub)
        if k == 6:
            w += bmove(side, 264, 3, 0, 4) + shake_defender(1, 2)              # (the foe gulps)
        w += wait(1)
    w += bmove(side, 264, 2, 0, -4) + bmove(side, 258, 2, sx * 20, 6) + se(s["bslam"]) + se(s["kaboom"]) + flash_screen(3)
    w += shake_defender(4, 3) + func(48) + func(68, 3, 3, 1, 2, 0) + bmove(side, 258, 4, -sx * 20, -6)
    return w + wait(3)
# ====
def _k9_unit(side, s):
    """Odor Sleuth (K9 Unit): a police K9 trots in and sniffs round the foe - sniff... sniff... - sits - BARKS -
    and pulls a sandwich off them. Eats it. Trots off."""
    dog = (36, 10) if side == "player" else (-40, 40)
    run = 70 if side == "player" else -70
    w = []
    for k in range(5):                                                         # *trot trot*
        w += emit_at(SLEUTH20, 1, 1, (dog[0] + round(run * (1 - (k + 1) / 5)), dog[1] + (2 if k % 2 else 0))) + wait(1)
    for n in range(2):                                                         # sniff... sniff...
        w += se(s["sscent"])
        for k in range(4):
            w += emit_at(SLEUTH20, 1, 1, (dog[0] - (4 if k % 2 else 0), dog[1]))
            if k == 1:
                w += emit_at(SLEUTH20, 0, 1, (dog[0] - 26, dog[1] + 4))
            w += wait(1)
        w += _hold(SLEUTH20, 1, 1, dog, 2)
    for k in range(8):                                                         # *sits* - BARK BARK
        w += emit_at(SLEUTH20, 2, 1, dog)
        if k in (1, 4):
            w += se(s["rage"]) + shake_defender(2, 2) + func(34, 8, 0, 1, rgb(255, 255, 160), 10, 0)
        w += wait(1)
    for k in range(5):                                                         # *yoink*
        t = (k + 1) / 5
        w += emit_at(SLEUTH20, 2, 1, dog) + emit_at(K9B22, 1, 1, (round(dog[0] * t - 4), round(20 + 14 * (1 - (2 * t - 1) ** 2)))) + wait(1)
    w += se(s["crunch"]) + _hold(SLEUTH20, 2, 1, dog, 3, lambda k: emit_at(K9B22, 1, 1, (dog[0] - 8, dog[1] + 16)) if k < 1 else [])
    w += se(s["bite"]) + _hold(SLEUTH20, 2, 1, dog, 4)
    for k in range(5):                                                         # ...and off
        w += emit_at(SLEUTH20, 1, 1, (dog[0] + round(run * (k + 1) / 5), dog[1] + (2 if k % 2 else 0))) + wait(1)
    return w + wait(2)
# ====
def _hide_out(side, s):
    """Withdraw (Hide Out): they hide behind a tiny potted cactus. Way too small. The foe looks left... looks
    right... - "ACHOO!" - the cactus tips over."""
    sx = _sx(side)
    pot = (sx * 2, 4) if side == "player" else (0, 0)
    bub = (sx * 50, 58) if side == "player" else (-40, 30)
    w = se(s["whoosh"]) + bmove(side, 258, 3, 0, -6) + _hold(FICUS20, 1, 0, pot, 4)       # *crouches*
    for d_ in (-12, 24, -12):                                                  # the foe looks left... right...
        w += bmove(side, 264, 3, d_, 0) + _hold(FICUS20, 1, 0, pot, 4)
        if d_ != -12 or len(w) > 50:
            w += se(s["leer"])
    w += _hold(FICUS20, 1, 0, pot, 3)                                          # *...*
    for k in range(10):                                                        # ACHOO!
        w += emit_at(HIDEB22, 1, 0, bub) + emit_at(FICUS20, 2 if k > 0 else 1, 0, (pot[0] + sx * 4, pot[1] - 2))
        if k == 0:
            w += se(s["cough"]) + shake_attacker(3, 2) + emit_at(FICUS20, 0, 0, (pot[0], pot[1] + 10))
        if k == 3:
            w += bmove(side, 264, 2, 0, 6) + func(34, 8, 0, 1, rgb(255, 255, 200), 10, 0)   # *the foe sees them*
        w += wait(1)
    w += bmove(side, 264, 2, 0, -6) + bmove(side, 258, 3, 0, 6) + func(34, 2, 0, 1, rgb(120, 200, 255), 12, 0)
    return w + wait(3)
# ====
def _bling_beam(side, s):
    """Power Gem (Bling Beam): the iced-out chain - tink - tink - then the medallion fires a gold beam and
    crusts the foe in diamonds."""
    sx = _sx(side)
    med = (sx * 8, 22) if side == "player" else (-8, 16)
    w = se(s["bling"]) + _hold(CANDY20, 1, 0, med, 3)
    for n in range(2):                                                         # tink... tink
        w += se(s["bling"]) + emit_at(CANDY20, 0, 0, (med[0], med[1] - 6)) + _hold(CANDY20, 1, 0, med, 5)
    w += _hold(CANDY20, 1, 0, med, 2) + se(s["sbeam"]) + flash_screen(2)       # BLING
    w += emit_at(GEMBEAM20, 0 if side == "player" else 1, 0, (med[0], med[1] - 6))
    for k in range(14):
        w += emit_at(CANDY20, 1, 0, med)
        if k > 4 and k % 2 == 0:
            w += emit_at(CANDY20, 0, 1, ((k * 13) % 30 - 15, 10 + (k * 7) % 30)) + shake_defender(1, 1)
        if k == 8:
            w += se(s["bling"]) + func(34, 8, 0, 1, rgb(210, 245, 255), 14, 0)    # *iced out*
        w += wait(1)
    return w + func(48) + wait(4)
# ====
def _mooch(side, s):
    """Leech Life (Mooch): the foe's got a tray of food - the attacker takes a fry - another fry - then the
    WHOLE burger. Munch. The foe just stares."""
    sx = _sx(side)
    dx, dy = TARGET_FROM_ATTACKER[side]
    tray = (34, 8) if side == "player" else (-36, 40)
    tray_a = (dx + tray[0], dy + tray[1])
    mouth = (sx * 10, 30) if side == "player" else (-10, 24)
    have = {"burger": True}
    t_ = lambda: emit_at(SHAKE20, 1 if have["burger"] else 2, 1, tray)
    w = se(s["bling"]) + _hold(SHAKE20, 1, 1, tray, 4)
    for n, (res, kit) in enumerate(((1, MOOCHB22), (1, MOOCHB22), (2, MOOCHB22))):   # fry... fry... BURGER
        if n == 2:
            have["burger"] = False
            w += t_() + wait(1) + t_() + wait(1)
        w += se(s["whoosh"])
        w += _lob(kit, res, side, (tray_a[0] - 8, tray_a[1] + 10), mouth, 5, 24, lambda k: t_())
        w += se(s["crunch"]) + shake_attacker(1, 2) + emit_at(SHAKE20, 0, 0, mouth) + t_() + wait(1)
        w += func(34, 2, 0, 1, rgb(120, 255, 140), 10 + n, 0) + se(s["absorb"]) + t_() + wait(2) + t_() + wait(2)
    for k in range(8):                                                         # *stares*
        w += t_()
        if k == 2:
            w += func(34, 8, 0, 1, rgb(255, 80, 80), 12, 0) + shake_defender(2, 2)
        w += wait(1)
    return w
