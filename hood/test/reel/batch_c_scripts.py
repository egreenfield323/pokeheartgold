def _vape_cloud(side, s):
    """Mist (Vape Cloud): a box-mod vape - puff, a smoke ring - puff, another - then one GIANT cloud swallows
    their whole side, and all you can see in it is a pair of shades."""
    sx = _sx(side)
    mod = (sx * 24, 34) if side == "player" else (-24, 26)
    shades = (sx * 10, 26) if side == "player" else (-6, 22)
    w = se(s["bonk"]) + _hold(FOG20, 1, 0, mod, 3)
    for n in range(2):                                                         # puff... a ring
        w += se(s["smoke"]) + _hold(FOG20, 1, 0, (mod[0], mod[1] + 2), 2)
        w += emit_at(FOG20, 0, 0, (mod[0] + sx * 6, mod[1] + 22)) + _hold(FOG20, 1, 0, mod, 5)
    w += se(s["haze"]) + _hold(FOG20, 1, 0, (mod[0], mod[1] + 3), 3)           # *the big one*
    w += emit_at(FOGFX20, 0, 0, (-20, 14)) + emit_at(FOGFX20, 1, 0, (24, 14)) + func(33, 0, 1, 0, 9, rgb(225, 225, 235))
    w += func(34, 2, 0, 1, rgb(235, 235, 245), 15, 0)
    for k in range(16):                                                        # ...just the shades
        w += emit_at(FOG20, 2, 0, shades)
        if k == 6:
            w += se(s["bling"]) + emit_at(FOGFX20, 0, 0, (shades[0] + 10, shades[1] + 4))
        w += wait(1)
    return w + func(33, 0, 1, 9, 0, rgb(225, 225, 235)) + _hold(FOG20, 2, 0, shades, 3)
# ====
def _plug_in(side, s):
    """Charge (Plug In): the phone's on 1% - plugged in... 1%... ...3%... - then they pull out a giant FAST
    charger: ZAP. 100%. Fully charged."""
    sx = _sx(side)
    ph = (sx * 40, 40) if side == "player" else (-40, 26)
    ch = (ph[0] - sx * 26, ph[1] - 6)
    w = se(s["disable"]) + _hold(AMP20, 1, 0, ph, 8)                           # *click* ... 1%
    w += _hold(AMP20, 1, 0, ph, 4, lambda k: shake_attacker(1, 1) if k == 1 else [])
    w += se(s["clock"]) + _hold(AMP20, 2, 0, ph, 8)                            # ...3%
    w += _hold(AMP20, 2, 0, ph, 4, lambda k: (func(34, 8, 0, 1, rgb(160, 170, 255), 9, 0) + shake_defender(1, 1)) if k == 1 else [])   # (the foe dozes)
    w += se(s["whoosh"])
    for k in range(4):                                                         # the FAST charger
        w += emit_at(AMP20, 2, 0, ph) + emit_at(PLUGB22, 2, 0, (ch[0] - sx * (3 - k) * 20, ch[1])) + wait(1)
    w += se(s["bonk"]) + _hold(AMP20, 2, 0, ph, 2, lambda k: emit_at(PLUGB22, 2, 0, ch))
    w += se(s["thunder"]) + se(s["zap"]) + flash_screen(4) + func(68, 3, 3, 1, 3, 0)          # ZAP
    w += emit_at(AMPFX20, 0, 0, (0, 20)) + emit_at(AMPFX20, 1, 0, (0, 10)) + emit_at(AMP20, 0, 0, ph)
    for k in range(12):                                                        # 100%
        w += emit_at(PLUGB22, 1, 0, ph) + emit_at(PLUGB22, 2, 0, ch)
        if k % 4 == 0:
            w += func(34, 2, 0, 1, rgb(255, 240, 80), 13, 0)
        w += wait(1)
    return w
# ====
def _bed_bugs(side, s):
    """Bug Bite (Bed Bugs): a sad motel bed - the foe lies down - itch... itch... - then the mattress ERUPTS
    with bugs and they launch off it. 1 STAR."""
    bed = (30, 6) if side == "player" else (-30, 40)
    hop = 24 if side == "player" else -24
    w = se(s["whoosh"])
    for k in range(4):                                                         # the bed slides in
        w += emit_at(BUGS20, 1, 1, (bed[0] + (3 - k) * 16, bed[1])) + wait(1)
    w += bmove(side, 264, 3, hop, 2) + _hold(BUGS20, 1, 1, (bed[0] - hop, bed[1]), 3)   # *lies down*
    for n in range(2):                                                         # itch... itch
        w += se(s["bite"]) + shake_defender(2, 2) + emit_at(BUGS20, 0, 1, (0, 6)) + _hold(BUGS20, 1, 1, (bed[0] - hop, bed[1]), 5)
    w += se(s["psting"]) + se(s["bslam"])                                      # ERUPT
    for k in range(3):
        w += emit_at(BUGS20, 0, 1, (k * 12 - 12, 4)) + emit_at(BUGS20, 1, 1, (bed[0] - hop, bed[1])) + wait(1)
    w += bmove(side, 264, 2, 0, 26) + func(34, 8, 0, 1, rgb(220, 60, 60), 13, 0)
    w += _hold(BUGS20, 1, 1, (bed[0] - hop, bed[1] - 26), 3) + bmove(side, 264, 4, -hop, -28) + func(48)
    for k in range(10):                                                        # 1 STAR.
        w += emit_at(BUGB22, 1, 1, (0, 62)) + emit_at(BUGS20, 1, 1, bed)
        if k == 0:
            w += se(s["bonk"])
        w += wait(1)
    return w
# ====
def _shakedown(side, s):
    """Wring Out (Shakedown): the foe gets shaken down - coins fall out - shake - their keys - shake HARDER -
    a rubber chicken. *squeak*. The attacker pockets the coins."""
    keys, chick = (-16, 0), (16, 2)
    have = []
    def floor():
        w = []
        if "keys" in have:
            w += emit_at(MOP20, 1, 1, keys)
        if "chick" in have:
            w += emit_at(MOP20, 2, 1, chick)
        return w
    w = []
    for n, what in enumerate(("coins", "keys", "chick")):
        w += se(s["rollout"]) + shake_defender(3 + n, 4) + floor() + wait(2) + floor() + wait(2)
        if what == "coins":
            w += emit_at(MOP20, 0, 1, (0, 22)) + se(s["chaching"])
        else:
            dest = keys if what == "keys" else chick
            res = 1 if what == "keys" else 2
            for k in range(3):
                w += floor() + emit_at(MOP20, res, 1, (dest[0], dest[1] + 24 - k * 8)) + wait(1)
            have.append(what)
            w += se(s["bonk"] if what == "keys" else s["astonish"])
        w += floor() + wait(2) + floor() + wait(2)
    w += func(48) + se(s["chaching"]) + func(34, 2, 0, 1, rgb(255, 220, 80), 12, 0)   # *pockets it*
    for k in range(6):
        w += floor() + wait(1)
    return w
# ====
def _loud_pack(side, s):
    """Magical Leaf (Loud Pack): the neon fanny pack unzips - a boombox inside - music notes home in on the foe,
    louder, LOUDER - "TURN IT DOWN!" from off-screen - and a slipper flies in and bonks the attacker."""
    sx = _sx(side)
    fp = (sx * 14, 40) if side == "player" else (-14, 36)
    bub = (-30, 64) if side == "player" else (40, -20)
    w = se(s["bling"]) + _hold(FANNY20, 1, 0, fp, 3) + se(s["swipe"]) + _hold(FANNY20, 2, 0, fp, 2)
    for n in range(3):                                                         # louder... LOUDER
        w += se(s["bass"]) + emit_at(MONEY20, 0 if side == "player" else 1, 0, (fp[0], fp[1] + 10))
        for k in range(5):
            w += emit_at(FANNY20, 2, 0, (fp[0] + (1 if k % 2 else -1) * (n + 1), fp[1]))
            if k == 4:
                w += shake_defender(n + 1, 1) + func(68, n + 1, n + 1, 1, 1, 0)
            w += wait(1)
    for k in range(8):                                                         # "TURN IT DOWN!"
        w += emit_at(LOUDB22, 1, 0, bub) + emit_at(FANNY20, 2, 0, fp) + wait(1)
    w += se(s["whoosh"])
    for t in (0, .25, .5, .75, 1):                                             # *slipper*
        p = (round(-sx * 100 + (sx * 4 + sx * 100) * t), round(70 + (40 - 70) * t))
        w += emit_at(LOUDB22, 2, 0, p) + emit_at(FANNY20, 2, 0, fp) + wait(1)
    w += se(s["bonk"]) + shake_attacker(3, 2) + emit_at(FANNY20, 0, 0, (sx * 4, 44))
    return w + _hold(FANNY20, 1, 0, fp, 5) + wait(2)
