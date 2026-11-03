"""Batch B of the set 20 redo."""
import re, sys
p = 'hood/gunfx.py'
s = open(p, encoding='utf-8').read()

def swap_kit(s, name, new):
    a = s.index(f'    b, rs = pk({name},')
    b = s.index('    b, rs = pk(', a + 10)
    return s[:a] + new + s[b:]

def swap_fn(s, old, new):
    a = s.index(f'def {old}(side, s):')
    b = re.search(r'^def ', s[a + 10:], re.M).start() + a + 10
    return s[:a] + new + s[b:]

new_names = "CLOWNB22 SPIKEB22 LACEB22 SAFEB22 PARKB22".split()
for n in new_names:
    assert not re.search(r'\b' + n + r'\b', s), n
a = 'MADB22, MADC22) = range(543, 549)\nLAST_KIT = MADC22\n'
assert s.count(a) == 1
s = s.replace(a, 'MADB22, MADC22) = range(543, 549)\n(' + ', '.join(new_names) + f') = range(549, {549 + len(new_names)})\nLAST_KIT = {new_names[-1]}\n')
a = 'MADB22: 82, MADC22: 82})\n'
assert s.count(a) == 1
s = s.replace(a, a + 'DONOR.update({' + ', '.join(f'{n}: 82' for n in new_names) + '})\n')
SGN = lambda t: f'(fxart.burst_sign({t}, fill=(220, 40, 40, 255), text=(255, 255, 255, 255)), SIGN_SCALE, 4, {{"colors": 30}})'

s = swap_kit(s, 'CLOWN20', f'''    b, rs = pk(CLOWN20, {{1: (fxart.clown_nose(), .45, 4, {{}}), 2: (fxart.rainbow_wig(), 1.0, 4, {{}})}}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 80, 160), rgb(120, 255, 255), .55, 14, .22, up=.16, gravity=.012, life=24)
    fin(CLOWN20, b, rs, (0, 1, 2))
    b, rs = pk(CLOWNB22, {{1: {SGN('["CLOWNED."]')}, 2: (fxart.clown_shoes(), 1.0, 4, {{}})}})
    fin(CLOWNB22, b, rs, (1, 2))

''')
s = swap_kit(s, 'LEGO20', '''    b, rs = pk(LEGO20, {1: (fxart.spike_strip(), 1.3, 4, {}), 2: (fxart.pizza_scooter(), ONE_TO_ONE, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 255, 220), rgb(255, 255, 255), .5, 8, .2, life=12)
    fin(LEGO20, b, rs, (0, 1, 2))
    b, rs = pk(SPIKEB22, {1: (fxart.pizza_scooter(flat=True), ONE_TO_ONE, 4, {}), 2: (fxart.pizza_hat(), 1.0, 4, {})},
               alpha=fxart.soft_puff())
    burst(b, rs, 0, rgb(200, 200, 205), rgb(255, 255, 255), .6, 8, .14, up=.06, life=18)
    fin(SPIKEB22, b, rs, (0, 1, 2))

''')
s = swap_kit(s, 'LACES20', '''    b, rs = pk(LACES20, {1: (fxart.tied_laces(), 2.0, 4, {}), 2: (fxart.flying_sneaker(), .9, 4, {})}, alpha=fxart.soft_puff())
    burst(b, rs, 0, rgb(210, 200, 180), rgb(255, 255, 255), .7, 8, .14, up=.03, life=22)
    fin(LACES20, b, rs, (0, 1, 2))
    b, rs = pk(LACEB22, {1: (fxart.line_bubble(["WHO TIED", "THESE?!"]), ONE_TO_ONE, 4, {})})
    fin(LACEB22, b, rs, (1,))

''')
s = swap_kit(s, 'SAFE20', '''    b, rs = pk(SAFE20, {1: (fxart.wall_safe(), 1.0, 4, {}), 2: (fxart.safe_inside_man(), 1.0, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 230, 80), rgb(255, 255, 220), .55, 10, .22, life=14)
    fin(SAFE20, b, rs, (0, 1, 2))
    b, rs = pk(SAFEB22, {1: (fxart.line_bubble(["IT WAS OPEN", "THE WHOLE", "TIME"]), ONE_TO_ONE, 4, {}),
                         2: (fxart.spring_glove(), 1.2, 4, {})})
    fin(SAFEB22, b, rs, (1, 2))

''')
s = swap_kit(s, 'CLIMB20', f'''    b, rs = pk(CLIMB20, {{1: (fxart.blue_mailbox(), .9, 4, {{}}), 2: (fxart.fire_hydrant(), .8, 4, {{}})}}, alpha=fxart.dirt_clod())
    burst(b, rs, 0, rgb(150, 145, 140), rgb(210, 205, 200), .45, 8, .12, up=.1, gravity=.022, life=24)
    fin(CLIMB20, b, rs, (0, 1, 2))
    b, rs = pk(PARKB22, {{1: {SGN('["PARKOUR!"]')}}})
    fin(PARKB22, b, rs, (1,))

''')
s = s.replace(', MADB22, MADC22]', ', MADB22, MADC22, ' + ', '.join(new_names) + ']')

scripts = open(sys.argv[1], encoding='utf-8').read().split('\n# ====\n')
olds = ("_clown_on", "_rock_trap", "_trip_wire", "_inside_job", "_wall_climb")
news = ("_clown_on", "_spike_strip", "_got_laced", "_inside_job", "_parkour")
for old, new in zip(olds, scripts):
    s = swap_fn(s, old, new.strip('\n') + '\n\n\n')
for old, new in zip(olds, news):
    k = f' {old},\n'
    assert s.count(k) == 1, old
    s = s.replace(k, f' {new},\n')
for a, b in (('        264: (CLOWN20,),\n', '        264: (CLOWN20, CLOWNB22),\n'),
             ('        270: (LEGO20,),\n', '        270: (LEGO20, SPIKEB22),\n'),
             ('        271: (LACES20,),\n', '        271: (LACES20, LACEB22),\n'),
             ('        274: (SAFE20,),\n', '        274: (SAFE20, SAFEB22),\n'),
             ('        275: (CLIMB20,),\n', '        275: (CLIMB20, PARKB22),\n')):
    assert s.count(a) == 1, a
    s = s.replace(a, b)
open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
