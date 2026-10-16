"""Synthesized gunshot sound effects for Hood HeartGold (generated from scratch, so no licensing issues).

shots() -> {name: float32 array in [-1, 1] at RATE}; adpcm(samples) -> DS IMA-ADPCM bytes (4-byte header).
"""
import numpy as np

RATE = 22050
_rng = np.random.default_rng(7)


def _t(sec, rate):
    return np.arange(int(sec * rate)) / rate


def _lowpass(x, cutoff, rate):
    a = np.exp(-2 * np.pi * cutoff / rate)
    y = np.empty_like(x)
    acc = 0.0
    for i, v in enumerate(x):
        acc = (1 - a) * v + a * acc
        y[i] = acc
    return y


def _highpass(x, cutoff, rate):
    return x - _lowpass(x, cutoff, rate)


def _shot(rate, crack=1.0, body_hz=110, body=1.0, tail=0.25, tail_lp=2500, length=0.45, snap=0.0):
    t = _t(length, rate)
    n = _rng.uniform(-1, 1, len(t))
    out = np.zeros(len(t))
    out += crack * _highpass(n, 1800, rate) * np.exp(-t / 0.004)                 # the crack
    if snap:                                                                       # supersonic snap (rifles)
        out += snap * np.sign(np.sin(2 * np.pi * 2900 * t)) * np.exp(-t / 0.0025)
    sweep = body_hz * (1 + 1.5 * np.exp(-t / 0.01))                               # chest-thump that drops in pitch
    out += body * np.sin(2 * np.pi * np.cumsum(sweep) / rate) * np.exp(-t / 0.05)
    out += _lowpass(n, tail_lp, rate) * 1.6 * np.exp(-t / tail) * (1 - np.exp(-t / 0.003))   # gas blast / room tail
    return out


def _place(dst, src, at, rate, gain=1.0):
    i = int(at * rate)
    j = min(len(dst), i + len(src))
    dst[i:j] += gain * src[:j - i]


def _finish(x, drive=2.2):
    x = np.tanh(drive * x / (np.max(np.abs(x)) + 1e-9))      # soft clip for punch
    x /= np.max(np.abs(x))
    fade = np.minimum(1, (len(x) - np.arange(len(x))) / (0.02 * RATE))
    return (x * fade * 0.98).astype(np.float32)


def shots(rate=RATE):
    out = {}
    out["9mm"] = _finish(_shot(rate, crack=1.0, body_hz=120, body=1.2, tail=0.09, tail_lp=3000, length=0.45))
    out["deagle"] = _finish(_shot(rate, crack=0.8, body_hz=70, body=2.0, tail=0.18, tail_lp=1400, length=0.6), 3.0)
    out["rifle"] = _finish(_shot(rate, crack=1.3, body_hz=140, body=0.8, tail=0.12, tail_lp=4000, length=0.5, snap=0.7))
    street = _shot(rate, crack=1.0, body_hz=105, body=1.3, tail=0.07, tail_lp=2600, length=0.6)
    echo = _lowpass(street, 1200, rate)
    _place(street, echo, 0.13, rate, 0.45)                    # bounces off the buildings
    _place(street, echo, 0.29, rate, 0.2)
    out["street_echo"] = _finish(street)
    tap = np.zeros(int(0.55 * rate))
    one = _shot(rate, crack=1.1, body_hz=125, body=1.1, tail=0.06, tail_lp=3200, length=0.3)
    _place(tap, one, 0.0, rate)
    _place(tap, one, 0.16, rate, 0.9)
    out["double_tap"] = _finish(tap)
    # low caliber: one tap of the double tap, cut short and a touch brighter (fires fast in sprays)
    out["pop"] = _finish(_shot(rate, crack=1.2, body_hz=150, body=.9, tail=.035, tail_lp=3600, length=.22))
    out["skrrt"] = skrrt(rate)
    out["bling"] = bling(rate)
    out["chaching"] = chaching(rate)
    out["fwoosh"] = fwoosh(rate)
    out["whoosh"] = whoosh(rate)
    out["smash"] = smash(rate)
    out["bonk"] = bonk(rate)
    out["splat"] = splat(rate)
    return out


def whoosh(rate=RATE, length=.35):
    """Something thrown past: a band of noise sweeping up then fading."""
    t = _t(length, rate)
    n = _rng.uniform(-1, 1, len(t))
    env = np.sin(np.pi * np.clip(t / length, 0, 1)) ** 2
    f = t / length                                              # sweep: crossfade a dull and a bright band
    lo = _lowpass(n, 900, rate) * (1 - f) + _lowpass(n, 3400, rate) * f
    return _finish(_highpass(lo, 300, rate) * env, 1.6)


def smash(rate=RATE, length=.55):
    """Glass bottle breaking: a crack, then tinkling shards."""
    t = _t(length, rate)
    n = _rng.uniform(-1, 1, len(t))
    out = _highpass(n, 2500, rate) * np.exp(-t / .03) * 1.5
    out += np.sin(2 * np.pi * 120 * t) * np.exp(-t / .03)
    for k in range(14):                                        # shards
        at = .02 + _rng.uniform(0, .4)
        f = _rng.uniform(3500, 7500)
        tt = np.clip(t - at, 0, None)
        out += .35 * np.sin(2 * np.pi * f * tt) * np.exp(-tt / .025) * (t >= at)
    return _finish(out, 1.5)


def bonk(rate=RATE, length=.35):
    """Brick hitting a head: a dull thud with a woody knock on top."""
    t = _t(length, rate)
    n = _rng.uniform(-1, 1, len(t))
    thud = np.sin(2 * np.pi * np.cumsum(140 * (1 + .8 * np.exp(-t / .015))) / rate) * np.exp(-t / .07)
    knock = np.sin(2 * np.pi * 620 * t) * np.exp(-t / .03) * .7 + _lowpass(n, 2000, rate) * np.exp(-t / .01)
    return _finish(thud * 1.4 + knock, 2.0)


def splat(rate=RATE, length=.4):
    """Egg breaking on someone: a wet slap that smears out."""
    t = _t(length, rate)
    n = _rng.uniform(-1, 1, len(t))
    slap = _lowpass(n, 1600, rate) * np.exp(-t / .05)
    goo = _lowpass(n, 600, rate) * (1 + .4 * np.sin(2 * np.pi * 9 * t)) * np.exp(-t / .15) * .8
    return _finish(slap * 1.5 + goo, 1.8)


def fwoosh(rate=RATE, length=.6):
    """Rocket launch: a thump, then a roaring hiss that sweeps away."""
    t = _t(length, rate)
    n = _rng.uniform(-1, 1, len(t))
    thump = np.sin(2 * np.pi * np.cumsum(90 * (1 + 2 * np.exp(-t / .02))) / rate) * np.exp(-t / .06)
    roar = _lowpass(n, 1800, rate) * np.minimum(1, t / .03) * np.exp(-t / .35)
    hiss = _highpass(n, 3000, rate) * np.exp(-((t - .12) / .12) ** 2) * .5
    return _finish(thump * 1.2 + roar * 1.4 + hiss, 2.0)


def chaching(rate=RATE, length=.7):
    """Cash register: the drawer's 'cha' (a ratchety slide) then the bell 'ching'."""
    t = _t(length, rate)
    n = _rng.uniform(-1, 1, len(t))
    cha = np.zeros(len(t))
    for k in range(7):                                         # ratchet clicks of the drawer
        i = int((.01 + k * .018) * rate)
        m = int(.012 * rate)
        cha[i:i + m] += _highpass(n[i:i + m], 1500, rate) * np.exp(-np.arange(m) / rate / .003) * (1 - k * .08)
    slide = _lowpass(n, 2500, rate) * np.exp(-((t - .1) / .05) ** 2) * .5
    ring = np.zeros(len(t))
    at = .16
    tt = np.clip(t - at, 0, None)
    for f, a, d in ((2093, 1.0, .25), (2637, .8, .22), (4186, .4, .12), (5274, .25, .08)):
        ring += a * np.sin(2 * np.pi * f * tt) * np.exp(-tt / d) * (t >= at)
    return _finish(cha + slide + ring * .9, 1.4)


def bling(rate=RATE, length=.5):
    """Ice catching the light: a bright metallic 'tiiing' with a little chain jingle under it."""
    t = _t(length, rate)
    tone = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t / d)
               for f, a, d in ((3520, 1.0, .18), (5274, .6, .12), (7040, .45, .08), (8870, .3, .05)))
    n = _rng.uniform(-1, 1, len(t))
    jingle = np.zeros(len(t))
    for k, at in enumerate((.0, .035, .06, .11)):              # a few clinks of the links
        i = int(at * rate)
        m = min(len(t) - i, int(.03 * rate))
        jingle[i:i + m] += _highpass(n[:m], 4000, rate) * np.exp(-np.arange(m) / rate / .006) * (1 - k * .15)
    return _finish(tone + .5 * jingle, 1.3)


def skrrt(rate=RATE, length=.8):
    """Tyre screech over an engine revving up - the drive-by arriving."""
    t = _t(length, rate)
    n = _rng.uniform(-1, 1, len(t))
    # screech: noise squeezed through a wobbling narrow band around 2.5 kHz
    f = 2500 + 300 * np.sin(2 * np.pi * 7 * t)
    car = np.sin(2 * np.pi * np.cumsum(f) / rate)
    screech = car * (0.6 + 0.4 * _lowpass(n, 800, rate) / .3) * np.exp(-((t - .25) / .22) ** 2)
    # engine: sawtooth that revs from 70 to 140 Hz, a bit of grit
    ef = 70 + 70 * np.clip(t / length, 0, 1) ** .7
    ph = np.cumsum(ef) / rate
    engine = (2 * (ph % 1) - 1) * .8 + _lowpass(n, 300, rate) * .6
    engine = _lowpass(engine, 900, rate) * np.minimum(1, t / .05)
    return _finish(screech * .9 + engine * .8, 1.6)


_STEP = [7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 19, 21, 23, 25, 28, 31, 34, 37, 41, 45, 50, 55, 60, 66, 73, 80, 88, 97,
         107, 118, 130, 143, 157, 173, 190, 209, 230, 253, 279, 307, 337, 371, 408, 449, 494, 544, 598, 658, 724, 796,
         876, 963, 1060, 1166, 1282, 1411, 1552, 1707, 1878, 2066, 2272, 2499, 2749, 3024, 3327, 3660, 4026, 4428,
         4871, 5358, 5894, 6484, 7132, 7845, 8630, 9493, 10442, 11487, 12635, 13899, 15289, 16818, 18500, 20350,
         22385, 24623, 27086, 29794, 32767]
_IDX = [-1, -1, -1, -1, 2, 4, 6, 8]


def adpcm(x):
    """float samples -> DS IMA-ADPCM (header: s16 first sample, u8 step index, u8 0; low nibble first)."""
    pcm = np.clip(np.round(x * 32767), -32768, 32767).astype(int)
    pred, idx = int(pcm[0]), 0
    nib = []
    for s in pcm[1:]:
        step = _STEP[idx]
        diff = int(s) - pred
        code = 0
        if diff < 0:
            code, diff = 8, -diff
        d = step >> 3
        if diff >= step:
            code |= 4; diff -= step; d += step
        if diff >= step >> 1:
            code |= 2; diff -= step >> 1; d += step >> 1
        if diff >= step >> 2:
            code |= 1; d += step >> 2
        pred = max(-32768, min(32767, pred - d if code & 8 else pred + d))
        idx = max(0, min(88, idx + _IDX[code & 7]))
        nib.append(code)
    if len(nib) % 2:
        nib.append(0)
    body = bytes(nib[i] | nib[i + 1] << 4 for i in range(0, len(nib), 2))
    return int(pcm[0]).to_bytes(2, "little", signed=True) + bytes([0, 0]) + body


def write_wav(path, x, rate=RATE):
    import wave
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())
