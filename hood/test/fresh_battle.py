"""After any rebuild: reopen the ROM in DeSmuME, continue the in-game save (standing in Route 29 grass), walk
until a wild battle starts and save state slot 3 - so savestates always match the ROM being tested.
    python fresh_battle.py [rom=hood-showcase.nds]"""
import subprocess, sys, time
from pathlib import Path
here = Path(__file__).parent
sys.path.insert(0, str(here))
import winmenu
rom = str(here.parents[1] / (sys.argv[1] if len(sys.argv) > 1 else "hood-showcase.nds"))
res = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq DeSmuME_0.9.13_x64.exe', '/FO', 'CSV', '/NH'], capture_output=True, text=True).stdout
pid = int(res.split(',')[1].strip('"'))
assert winmenu.fire_path(pid, ('File', 'Recent ROM', rom)), "ROM not in DeSmuME's recent list"
time.sleep(3)
# title -> continue menu -> continue -> overworld (the save was made with the menu open: find_battle closes it)
subprocess.run([sys.executable, '-I', str(here / 'lua_go.py'), "wait 240;mash A 4;wait 120;press A;wait 300", '90'],
               check=True, capture_output=True)
r = subprocess.run([sys.executable, '-I', str(here / 'find_battle.py'), '3', '40'], capture_output=True, text=True)
print(r.stdout.strip() or r.stderr[-500:])
