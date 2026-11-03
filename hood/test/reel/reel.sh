#!/bin/bash
# reel.sh NAME V1 V2 ...: fast-patch the ROM, build hood-showcase.nds playing those variants back to back, and
# capture two 330-shot segments (a shot every 3 emulator frames; segment b starts where a ends) from savestate
# slot 6 in the running DeSmuME. Output: hood/test/reels_out/NAME_a.png / NAME_b.png (contact sheets, every 3rd
# shot) and NAME_a_frames/ NAME_b_frames/ (every shot, f_NNN.png).
# Needs DeSmuME_0.9.13_x64.exe running with the hood test setup (see .claude/skills/hood-battle-animations).
cd "$(dirname "$0")/../../.."
OUT=hood/test/reels_out
mkdir -p "$OUT"
N=$1; shift
ORD=$(echo "$@" | tr ' ' ',')
python -I hood/test/fast_patch.py >/dev/null || { echo "fast_patch failed"; exit 1; }
python -I -c "import sys; sys.path.insert(0,'hood'); import battlefx; battlefx.showcase('hood-soulsilver.nds','hood-showcase.nds', order=[$ORD])" >/dev/null || { echo "showcase failed"; exit 1; }
python -c "
import ctypes,subprocess,sys,time; sys.path.insert(0,'hood/test'); import winmenu
r=subprocess.run(['tasklist','/FI','IMAGENAME eq DeSmuME_0.9.13_x64.exe','/FO','CSV','/NH'],capture_output=True,text=True).stdout
pid=int(r.split(',')[1].strip('\"'))
for h in winmenu.dialogs_of(pid): ctypes.windll.user32.PostMessageW(h,0x10,0,0)
time.sleep(2)"
for seg in a b; do
  lead=$([ $seg = a ] && echo 100 || echo 1080)
  extra=$([ $seg = a ] && echo "" || echo "--noreload")
  timeout 600 python -I hood/test/capture.py --rom hood-showcase.nds --slot 6 --frames 330 --step 3 --lead $lead $extra >/dev/null
  python -I hood/test/reel/sheet.py "$OUT/${N}_$seg.png" 0 330 3 .5
  rm -rf "$OUT/${N}_${seg}_frames"; mkdir -p "$OUT/${N}_${seg}_frames"; cp hood/test/out/f_*.png "$OUT/${N}_${seg}_frames/"
  python -I hood/test/clipcheck.py "$OUT/${N}_${seg}_frames" --min 20 --sheet "$OUT/${N}_${seg}_clip.png" | sed "s/^/[clip $seg] /"
done
