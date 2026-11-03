"""Batch D2 of the set 20 redo (287-291). Run once from the repo root: python -X utf8 hood/test/reel/batch_d2.py"""
import re
from pathlib import Path
HERE = Path(__file__).resolve().parent
p = 'hood/gunfx.py'
s = open(p, encoding='utf-8').read()
assert 'def _spit_bars(side, s):\n    """Spit Up (Spit Bars): they spit BARS' not in s, "batch D2 already applied"


def swap_kit(s, name, new):
    a = s.index(f'    b, rs = pk({name},')
    b = s.index('    b, rs = pk(', a + 10)
    return s[:a] + new + s[b:]


def swap_fn(s, old, new):
    a = s.index(f'def {old}(side, s):')
    b = re.search(r'^def ', s[a + 10:], re.M).start() + a + 10
    return s[:a] + new + s[b:]


new_names = "ZAZAB22 ZAZAC22 DIPB22 SPITB22 POSTB22".split()
for n in new_names:
    assert not re.search(r'\b' + n + r'\b', s), n
a = 'HIDEB22, MOOCHB22) = range(557, 561)\nLAST_KIT = MOOCHB22\n'
assert s.count(a) == 1
s = s.replace(a, 'HIDEB22, MOOCHB22) = range(557, 561)\n(' + ', '.join(new_names) + f') = range(561, {561 + len(new_names)})\nLAST_KIT = {new_names[-1]}\n')
a = 'HIDEB22: 82, MOOCHB22: 82})\n'
assert s.count(a) == 1
s = s.replace(a, a + 'DONOR.update({' + ', '.join(f'{n}: 82' for n in new_names) + '})\n')
SGN = lambda t: f'(fxart.burst_sign({t}, fill=(220, 40, 40, 255), text=(255, 255, 255, 255)), SIGN_SCALE, 4, {{"colors": 30}})'

s = swap_kit(s, 'SCOPE20', f'''    b, rs = pk(SCOPE20, {{1: (fxart.playbook_clipboard(), ONE_TO_ONE, 4, {{}}), 2: {SGN('["PEEPED."]')}}}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 255, 200), rgb(255, 255, 255), .55, 8, .18, life=14)
    fin(SCOPE20, b, rs, (0, 1, 2))
    b, rs = pk(ZAZAB22, {{1: (fxart.weather_map(), ONE_TO_ONE, 4, {{}}), 2: (fxart.weather_map(level="MODERATE"), ONE_TO_ONE, 4, {{}})}})
    fin(ZAZAB22, b, rs, (1, 2))
    b, rs = pk(ZAZAC22, {{1: (fxart.weather_map(level="SEVERE"), ONE_TO_ONE, 4, {{}})}})
    fin(ZAZAC22, b, rs, (1,))

''')
s = swap_kit(s, 'EXIT20', '''    b, rs = pk(EXIT20, {1: (fxart.exit_door(), ONE_TO_ONE, 4, {}), 2: (fxart.window_pane(), .9, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(170, 220, 250), rgb(255, 255, 255), .6, 16, .26, up=.06, gravity=.016, life=22)
    fin(EXIT20, b, rs, (0, 1, 2))
    b, rs = pk(DIPB22, {1: (fxart.window_pane(broken=True), .9, 4, {})})
    fin(DIPB22, b, rs, (1,))

''')
s = swap_kit(s, 'MOUTH20', f'''    b, rs = pk(MOUTH20, {{1: (fxart.jail_bar(), .8, 4, {{}})}}, alpha=fxart.fizz_drop())
    burst(b, rs, 0, rgb(200, 230, 255), rgb(255, 255, 255), .35, 6, .12, up=.06, gravity=.012, life=14)
    fin(MOUTH20, b, rs, (0, 1))
    b, rs = pk(SPITB22, {{1: (fxart.jail_cell(), 1.5, 4, {{}}), 2: {SGN('["LOCKED UP."]')}}})
    fin(SPITB22, b, rs, (1, 2))

''')
s = swap_kit(s, 'CHAIR20', '''    b, rs = pk(CHAIR20, {1: (fxart.lawn_chair(), 1.4, 4, {}), 2: (fxart.cooler_box(), .8, 4, {})}, alpha=fxart.wink_twinkle())
    sparkle(b, rs, c=rgb(150, 255, 150))
    fin(CHAIR20, b, rs, (0, 1, 2))
    b, rs = pk(POSTB22, {1: (fxart.bbq_grill(), .9, 4, {})}, alpha=fxart.soft_puff())
    puffs(b, rs, 0, rgb(225, 225, 230), n=6, up=.14)
    fin(POSTB22, b, rs, (0, 1))

''')
s = s.replace(', SMOKEB22, K9B22, HIDEB22, MOOCHB22]', ', SMOKEB22, K9B22, HIDEB22, MOOCHB22, ' + ', '.join(new_names) + ']')

scripts = (HERE / 'batch_d2_scripts.py').read_text(encoding='utf-8').split('\n# ====\n')
olds = ("_peep_game", "_zaza_storm", "_dip_out", "_mouthwash_spit", "_post_up")
news = ("_peep_game", "_zaza_storm", "_dip_out", "_spit_bars2", "_post_up")
for old, new in zip(olds, scripts):
    if old == "_mouthwash_spit":
        new = new.replace("def _spit_bars(side, s):", "def _spit_bars2(side, s):")     # (an older _spit_bars exists)
    s = swap_fn(s, old, new.strip('\n') + '\n\n\n')
for old, new in zip(olds, news):
    k = f' {old},\n'
    assert s.count(k) == 1, old
    s = s.replace(k, f' {new},\n')
for a, b in (('        288: (LEAVES20,),\n', '        288: (LEAVES20, ZAZAB22, ZAZAC22),\n'),
             ('        289: (EXIT20,),\n', '        289: (EXIT20, DIPB22),\n'),
             ('        290: (MOUTH20, SPITFX20,),\n', '        290: (MOUTH20, SPITB22),\n'),
             ('        291: (CHAIR20,),\n', '        291: (CHAIR20, POSTB22),\n')):
    assert s.count(a) == 1, a
    s = s.replace(a, b)
open(p, 'w', encoding='utf-8', newline='').write(s)
print('batch D2 applied')
