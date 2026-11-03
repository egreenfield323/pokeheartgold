"""Batch D3 of the set 20 redo (292-293). Run once from the repo root: python -X utf8 hood/test/reel/batch_d3.py"""
import re
from pathlib import Path
HERE = Path(__file__).resolve().parent
p = 'hood/gunfx.py'
s = open(p, encoding='utf-8').read()
assert 'def _ride_or_die(' not in s, "batch D3 already applied"


def swap_kit(s, name, new):
    a = s.index(f'    b, rs = pk({name},')
    b = s.index('    b, rs = pk(', a + 10)
    return s[:a] + new + s[b:]


def swap_fn(s, old, new):
    a = s.index(f'def {old}(side, s):')
    b = re.search(r'^def ', s[a + 10:], re.M).start() + a + 10
    return s[:a] + new + s[b:]


new_names = ["COMBOB22"]
for n in new_names:
    assert not re.search(r'\b' + n + r'\b', s), n
a = 'SPITB22, POSTB22) = range(561, 566)\nLAST_KIT = POSTB22\n'
assert s.count(a) == 1
s = s.replace(a, 'SPITB22, POSTB22) = range(561, 566)\nCOMBOB22 = 566\nLAST_KIT = COMBOB22\n')
a = 'SPITB22: 82, POSTB22: 82})\n'
assert s.count(a) == 1
s = s.replace(a, a + 'DONOR.update({COMBOB22: 82})\n')

s = swap_kit(s, 'BFF20', '''    b, rs = pk(BFF20, {1: (fxart.handcuff(), .8, 4, {}), 2: (fxart.cuff_key(), .7, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(230, 235, 245), rgb(255, 255, 255), .5, 6, .14, life=12)
    fin(BFF20, b, rs, (0, 1, 2))
    b, rs = pk(COMBOB22, {1: (fxart.burst_sign(["COMBO", "BREAKER!"], fill=(220, 40, 40, 255), text=(255, 255, 255, 255)), SIGN_SCALE, 4, {"colors": 30})})
    fin(COMBOB22, b, rs, (1,))
''')
old = """    spray2(b, rs, {"player": (0, 30), "enemy": (0, 26)}, (0, 30), 20, clr=rgb(170, 60, 255),
           clr_anm=(rgb(240, 200, 255), rgb(100, 0, 160)),"""
assert s.count(old) == 1                     # (LINK20 is the last kit of its group: recolour it in place)
s = s.replace(old, """    spray2(b, rs, {"player": (0, 30), "enemy": (0, 26)}, (0, 30), 20, clr=rgb(200, 205, 220),
           clr_anm=(rgb(255, 255, 255), rgb(140, 145, 160)),""")
s = s.replace(', SPITB22, POSTB22]', ', SPITB22, POSTB22, COMBOB22]')
assert ', POSTB22, COMBOB22]' in s

scripts = (HERE / 'batch_d3_scripts.py').read_text(encoding='utf-8').split('\n# ====\n')
for old, new in zip(("_stab_combo", "_blood_pact"), scripts):
    s = swap_fn(s, old, new.strip('\n') + '\n\n\n')
k = ' _blood_pact,\n'
assert s.count(k) == 1
s = s.replace(k, ' _ride_or_die,\n')
for a, b in (('        292: (SLASH20, COMBO20,),\n', '        292: (SLASH20, COMBO20, COMBOB22),\n'),):
    assert s.count(a) == 1, a
    s = s.replace(a, b)
open(p, 'w', encoding='utf-8', newline='').write(s)
print('batch D3 applied')
