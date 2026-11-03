"""Batch C of the set 20 redo (277-281). Run once from the repo root: python -X utf8 hood/test/reel/batch_c.py"""
import re
from pathlib import Path
HERE = Path(__file__).resolve().parent
p = 'hood/gunfx.py'
s = open(p, encoding='utf-8').read()
assert 'def _vape_cloud(' not in s, "batch C already applied"


def swap_kit(s, name, new):
    a = s.index(f'    b, rs = pk({name},')
    b = s.index('    b, rs = pk(', a + 10)
    return s[:a] + new + s[b:]


def swap_fn(s, old, new):
    a = s.index(f'def {old}(side, s):')
    b = re.search(r'^def ', s[a + 10:], re.M).start() + a + 10
    return s[:a] + new + s[b:]


new_names = "PLUGB22 BUGB22 LOUDB22".split()
for n in new_names:
    assert not re.search(r'\b' + n + r'\b', s), n
a = 'SAFEB22, PARKB22) = range(549, 554)\nLAST_KIT = PARKB22\n'
assert s.count(a) == 1
s = s.replace(a, 'SAFEB22, PARKB22) = range(549, 554)\n(' + ', '.join(new_names) + f') = range(554, {554 + len(new_names)})\nLAST_KIT = {new_names[-1]}\n')
a = 'SAFEB22: 82, PARKB22: 82})\n'
assert s.count(a) == 1
s = s.replace(a, a + 'DONOR.update({' + ', '.join(f'{n}: 82' for n in new_names) + '})\n')
SGN = lambda t: f'(fxart.burst_sign({t}, fill=(220, 40, 40, 255), text=(255, 255, 255, 255)), SIGN_SCALE, 4, {{"colors": 30}})'

s = swap_kit(s, 'FOG20', '''    b, rs = pk(FOG20, {1: (fxart.vape_mod(), .9, 4, {}), 2: (fxart.cool_shades(), .8, 4, {})}, alpha=fxart.ring())
    prop(b, rs, 0, tex=0, clr=rgb(225, 225, 235), clr_anm=(rgb(255, 255, 255), rgb(190, 190, 205)), scl=.6, life=18,
         alpha=(26, 20, 0), scl_anm=(.4, 1.2, 1.8, 40, 200), vel=(0, .25), axis=(0, 1, 0))
    fin(FOG20, b, rs, (0, 1, 2))

''')
s = swap_kit(s, 'AMP20', '''    b, rs = pk(AMP20, {1: (fxart.phone_charge(), ONE_TO_ONE, 4, {}), 2: (fxart.phone_charge(level="3%"), ONE_TO_ONE, 4, {})},
               alpha=fxart.zig_spark())
    burst(b, rs, 0, rgb(255, 240, 90), rgb(255, 255, 255), .5, 10, .2, up=.1, life=14)
    fin(AMP20, b, rs, (0, 1, 2))
    b, rs = pk(PLUGB22, {1: (fxart.phone_charge(level="100%"), ONE_TO_ONE, 4, {}), 2: (fxart.fast_charger(), 1.1, 4, {})})
    fin(PLUGB22, b, rs, (1, 2))

''')
s = swap_kit(s, 'BUGS20', f'''    b, rs = pk(BUGS20, {{1: (fxart.motel_bed(), 1.6, 4, {{}})}}, alpha=fxart.bed_bug())
    burst(b, rs, 0, rgb(120, 60, 30), rgb(190, 120, 70), .4, 14, .24, up=.1, gravity=.01, life=24)
    fin(BUGS20, b, rs, (0, 1))
    b, rs = pk(BUGB22, {{1: {SGN('["1 STAR."]')}}})
    fin(BUGB22, b, rs, (1,))

''')
s = swap_kit(s, 'MOP20', '''    b, rs = pk(MOP20, {1: (fxart.key_ring(), .9, 4, {}), 2: (fxart.rubber_chicken(), .9, 4, {})}, alpha=fxart.gold_coin())
    burst(b, rs, 0, rgb(255, 210, 60), rgb(255, 250, 200), .45, 12, .14, up=.12, gravity=.02, life=26)
    fin(MOP20, b, rs, (0, 1, 2))

''')
s = swap_kit(s, 'FANNY20', '''    b, rs = pk(FANNY20, {1: (fxart.neon_fanny_pack(), 1.0, 4, {}), 2: (fxart.boombox_pack(), 1.0, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 240, 80), rgb(255, 255, 220), .55, 10, .2, life=14)
    fin(FANNY20, b, rs, (0, 1, 2))
''')
s = swap_kit(s, 'MONEY20', '''    b, rs = pk(MONEY20, {}, alpha=fxart.music_note())
    spray2(b, rs, {"player": (32, 34), "enemy": (-32, 30)}, (0, 20), 20, clr=rgb(255, 80, 220),
           clr_anm=(rgb(120, 255, 255), rgb(255, 240, 60)), scl=.6, gen=2, gen_intvl=2, emtr_life=12, radius=.3,
           spread=.05, alpha=(31, 31, 0))
    fin(MONEY20, b, rs, (0, 1))
    b, rs = pk(LOUDB22, {1: (fxart.line_bubble(["TURN IT", "DOWN!"]), ONE_TO_ONE, 4, {}), 2: (fxart.house_slipper(), .9, 4, {})})
    fin(LOUDB22, b, rs, (1, 2))

''')
s = s.replace(', SAFEB22, PARKB22]', ', SAFEB22, PARKB22, ' + ', '.join(new_names) + ']')

scripts = (HERE / 'batch_c_scripts.py').read_text(encoding='utf-8').split('\n# ====\n')
olds = ("_smoke_screen", "_plug_in", "_bed_bugs", "_squeeze_out", "_loud_pack")
news = ("_vape_cloud", "_plug_in", "_bed_bugs", "_shakedown", "_loud_pack")
for old, new in zip(olds, scripts):
    s = swap_fn(s, old, new.strip('\n') + '\n\n\n')
for old, new in zip(olds, news):
    k = f' {old},\n'
    assert s.count(k) == 1, old
    s = s.replace(k, f' {new},\n')
for a, b in (('        278: (AMP20, AMPFX20,),\n', '        278: (AMP20, AMPFX20, PLUGB22),\n'),
             ('        279: (BUGS20, BUGFX20,),\n', '        279: (BUGS20, BUGB22),\n'),
             ('        281: (FANNY20, MONEY20,),\n', '        281: (FANNY20, MONEY20, LOUDB22),\n')):
    assert s.count(a) == 1, a
    s = s.replace(a, b)
open(p, 'w', encoding='utf-8', newline='').write(s)
print('batch C applied')
