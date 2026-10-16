"""Run cmds (argv[1], ';'-separated) in the running DeSmuME via runner.lua; save shots to out/ as PNG."""
import subprocess, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import winmenu
from run import gd_to_png
here = Path(__file__).parent
out = here / 'out'
for f in out.glob('*'):
    f.unlink()
(here / 'cmds.txt').write_text('keepopen\n' + sys.argv[1].replace(';', '\n') + '\ndone\n')
res = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq DeSmuME_0.9.13_x64.exe', '/FO', 'CSV', '/NH'], capture_output=True, text=True).stdout
pid = int(res.split(',')[1].strip('"'))
print(winmenu.run_lua(pid, str(here / 'runner.lua')))
t0 = time.time()
while time.time() - t0 < float(sys.argv[2]) if len(sys.argv) > 2 else 90:
    l = out / 'log.txt'
    if l.exists() and 'DONE' in l.read_text(errors='ignore'):
        break
    time.sleep(1)
for g in out.glob('*.gd'):
    gd_to_png(g, g.with_suffix('.png'))
    g.unlink()
print(sorted(p.name for p in out.glob('*.png')))
