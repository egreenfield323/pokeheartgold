"""Batch D1 of the set 20 redo (282-286). Run once from the repo root: python -X utf8 hood/test/reel/batch_d1.py"""
import re
from pathlib import Path
HERE = Path(__file__).resolve().parent
p = 'hood/gunfx.py'
s = open(p, encoding='utf-8').read()
assert 'def _same_smoke(' not in s, "batch D1 already applied"


def swap_kit(s, name, new):
    a = s.index(f'    b, rs = pk({name},')
    b = s.index('    b, rs = pk(', a + 10)
    return s[:a] + new + s[b:]


def swap_fn(s, old, new):
    a = s.index(f'def {old}(side, s):')
    b = re.search(r'^def ', s[a + 10:], re.M).start() + a + 10
    return s[:a] + new + s[b:]


new_names = "SMOKEB22 K9B22 HIDEB22 MOOCHB22".split()
for n in new_names:
    assert not re.search(r'\b' + n + r'\b', s), n
a = 'BUGB22, LOUDB22) = range(554, 557)\nLAST_KIT = LOUDB22\n'
assert s.count(a) == 1
s = s.replace(a, 'BUGB22, LOUDB22) = range(554, 557)\n(' + ', '.join(new_names) + f') = range(557, {557 + len(new_names)})\nLAST_KIT = {new_names[-1]}\n')
a = 'BUGB22: 82, LOUDB22: 82})\n'
assert s.count(a) == 1
s = s.replace(a, a + 'DONOR.update({' + ', '.join(f'{n}: 82' for n in new_names) + '})\n')

s = swap_kit(s, 'TREAD20', '''    b, rs = pk(TREAD20, {1: (fxart.hoop_earrings(), .8, 4, {}), 2: (fxart.rope_chain(), .9, 4, {})}, alpha=fxart.wink_twinkle())
    burst(b, rs, 0, rgb(255, 255, 220), rgb(255, 255, 255), .6, 6, .1, life=14)
    fin(TREAD20, b, rs, (0, 1, 2))
    b, rs = pk(SMOKEB22, {1: (fxart.jelly_jar(), ONE_TO_ONE, 4, {}), 2: (fxart.line_bubble(["WE CAN GET", "THE SAME", "SMOKE"]), ONE_TO_ONE, 4, {})})
    fin(SMOKEB22, b, rs, (1, 2))

''')
s = swap_kit(s, 'SLEUTH20', '''    b, rs = pk(SLEUTH20, {1: (fxart.k9_dog(), ONE_TO_ONE, 4, {}), 2: (fxart.k9_dog(barking=True), ONE_TO_ONE, 4, {})},
               alpha=fxart.soft_puff())
    burst(b, rs, 0, rgb(230, 230, 240), rgb(255, 255, 255), .5, 4, .06, up=.04, life=14)
    fin(SLEUTH20, b, rs, (0, 1, 2))
    b, rs = pk(K9B22, {1: (fxart.sandwich(), .8, 4, {})})
    fin(K9B22, b, rs, (1,))

''')
s = swap_kit(s, 'FICUS20', '''    b, rs = pk(FICUS20, {1: (fxart.tiny_cactus(), .55, 4, {}), 2: (fxart.tiny_cactus(fallen=True), .55, 4, {})},
               alpha=fxart.fizz_drop())
    burst(b, rs, 0, rgb(200, 230, 255), rgb(255, 255, 255), .35, 10, .2, up=.06, gravity=.012, life=16)
    fin(FICUS20, b, rs, (0, 1, 2))
    b, rs = pk(HIDEB22, {1: (fxart.line_bubble(["ACHOO!"]), ONE_TO_ONE, 4, {})})
    fin(HIDEB22, b, rs, (1,))

''')
s = swap_kit(s, 'CANDY20', '''    b, rs = pk(CANDY20, {1: (fxart.big_chain(), 1.0, 4, {})}, alpha=fxart.wink_twinkle())
    burst(b, rs, 0, rgb(210, 245, 255), rgb(255, 255, 255), .7, 8, .16, life=16)
    fin(CANDY20, b, rs, (0, 1))
''')
s = swap_kit(s, 'GEMBEAM20', '''    b, rs = pk(GEMBEAM20, {}, alpha=fxart.wink_twinkle())
    spray2(b, rs, {"player": (30, 46), "enemy": (-30, 40)}, (0, 22), 12, clr=rgb(255, 220, 60),
           clr_anm=(rgb(255, 255, 255), rgb(255, 180, 20)), scl=.6, gen=3, gen_intvl=1, emtr_life=20, radius=.2,
           spread=.02, alpha=(31, 31, 0), flags_on=(1 << 14) | (1 << 12))
    for r in (0, 1):
        rot(b, rs, r, spin=0x0C00)
    fin(GEMBEAM20, b, rs, (0, 1))

''')
s = swap_kit(s, 'SHAKE20', '''    b, rs = pk(SHAKE20, {1: (fxart.food_tray(), 1.0, 4, {}), 2: (fxart.food_tray(burger=False), 1.0, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 220, 120), rgb(255, 255, 220), .4, 6, .12, life=12)
    fin(SHAKE20, b, rs, (0, 1, 2))
    b, rs = pk(MOOCHB22, {1: (fxart.french_fry(), .5, 4, {}), 2: (fxart.burger(), .8, 4, {})})
    fin(MOOCHB22, b, rs, (1, 2))

''')
s = s.replace(', PLUGB22, BUGB22, LOUDB22]', ', PLUGB22, BUGB22, LOUDB22, ' + ', '.join(new_names) + ']')

scripts = (HERE / 'batch_d1_scripts.py').read_text(encoding='utf-8').split('\n# ====\n')
olds = ("_grind", "_sniff_out", "_hide_out", "_rock_candy", "_mooch")
news = ("_same_smoke", "_k9_unit", "_hide_out", "_bling_beam", "_mooch")
for old, new in zip(olds, scripts):
    s = swap_fn(s, old, new.strip('\n') + '\n\n\n')
for old, new in zip(olds, news):
    k = f' {old},\n'
    assert s.count(k) == 1, old
    s = s.replace(k, f' {new},\n')
for a, b in (('        282: (TREAD20,),\n', '        282: (TREAD20, SMOKEB22),\n'),
             ('        283: (SLEUTH20,),\n', '        283: (SLEUTH20, K9B22),\n'),
             ('        284: (FICUS20,),\n', '        284: (FICUS20, HIDEB22),\n'),
             ('        286: (SHAKE20,),\n', '        286: (SHAKE20, MOOCHB22),\n')):
    assert s.count(a) == 1, a
    s = s.replace(a, b)
open(p, 'w', encoding='utf-8', newline='').write(s)
print('batch D1 applied')
