#!/bin/bash
# enemy.sh NAME V1 V2 ...: like reel.sh, but Cyndaquil uses move 2 (Leer, a stub in the showcase) so Pidgey's FMJ
# plays the reel FROM THE ENEMY SIDE. One long capture (900 shots, every 8 frames); the last shot should be back at
# "What will CYNDAQUIL do?" (no freeze). Output: hood/test/reels_out/NAME.png + NAME_frames/.
cd "$(dirname "$0")/../../.."
OUT=hood/test/reels_out
N=$1; shift
ORD=$(echo "$@" | tr ' ' ',')
python -I hood/test/fast_patch.py >/dev/null || { echo "fast_patch failed"; exit 1; }
python -I -c "import sys; sys.path.insert(0,'hood'); import battlefx; battlefx.showcase('hood-soulsilver.nds','hood-showcase.nds', order=[$ORD])" >/dev/null || exit 1
printf 'touch 128 90\nwait 40\ntouch 192 51\nwait 60\n' > hood/test/reel/_leer.txt
python -c "
import ctypes,subprocess,sys,time; sys.path.insert(0,'hood/test'); import winmenu
r=subprocess.run(['tasklist','/FI','IMAGENAME eq DeSmuME_0.9.13_x64.exe','/FO','CSV','/NH'],capture_output=True,text=True).stdout
pid=int(r.split(',')[1].strip('\"'))
for h in winmenu.dialogs_of(pid): ctypes.windll.user32.PostMessageW(h,0x10,0,0)
time.sleep(2)"
timeout 900 python -I hood/test/capture.py --rom hood-showcase.nds --slot 6 --frames 900 --step 8 --lead 100 --cmds hood/test/reel/_leer.txt >/dev/null 2>&1
for i in $(seq 1 90); do grep -q DONE hood/test/out/log.txt && break; sleep 5; done
python -I -c "
import sys; sys.path.insert(0,'hood/test'); from run import gd_to_png; from pathlib import Path
for g in sorted(Path('hood/test/out').glob('*.gd')): gd_to_png(g, g.with_suffix('.png')); g.unlink()"
python -I hood/test/reel/sheet.py "$OUT/$N.png" 0 900 9 .5
rm -rf "$OUT/${N}_frames"; mkdir -p "$OUT/${N}_frames"; cp hood/test/out/f_*.png "$OUT/${N}_frames/"
