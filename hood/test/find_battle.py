"""Walk back and forth in the grass (running DeSmuME, save already loaded) until the FIGHT menu shows up,
then save DeSmuME state slot N.   python find_battle.py [slot=3] [tries=25]"""
import subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image
here = Path(__file__).parent
slot = sys.argv[1] if len(sys.argv) > 1 else "3"
tries = int(sys.argv[2]) if len(sys.argv) > 2 else 25


def go(cmds):
    subprocess.run([sys.executable, '-I', str(here / 'lua_go.py'), cmds, '60'], check=True, capture_output=True)


def fight_menu(p):
    a = np.asarray(Image.open(p).convert('RGB')).astype(int)[192:]
    red = (a[..., 0] > 180) & (a[..., 1] < 90) & (a[..., 2] < 90)
    return red[40:120, 30:230].mean() > .4


go("press B;wait 20")
for i in range(tries):
    go("hold left 16;hold right 16;wait 4;shot w")
    if fight_menu(here / 'out' / 'w.png'):
        go("wait 30;shot w")                          # let the intro finish, check again
    if fight_menu(here / 'out' / 'w.png'):
        go(f"save {slot};shot w")
        print("battle! saved slot", slot, "after", i + 1, "passes")
        break
else:
    print("no battle yet")
