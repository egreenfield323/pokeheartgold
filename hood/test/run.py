#!/usr/bin/env python3
"""Run a DeSmuME test session headlessly-ish (DeSmuME window opens, but input comes from Lua, not
the keyboard, so it never touches other apps).

    python hood/test/run.py ROM CMDFILE [--desmume DIR]

DIR holds DeSmuME_0.9.13_x64.exe + lua51.dll (a private copy; your own install is never touched).
Screenshots land in hood/test/out/*.png (top screen above bottom screen).
"""
import struct
import subprocess
import sys
import time
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent


def gd_to_png(src, dst):
    b = src.read_bytes()
    sig, w, h = struct.unpack_from(">HHH", b, 0)
    if sig == 0xFFFE:                     # truecolor gd: header 11 bytes, ARGB pixels
        off = 11
        im = Image.frombytes("RGBA", (w, h), b[off:off + w * h * 4], "raw", "ARGB")
    else:
        raise ValueError("unexpected gd header")
    im.convert("RGB").save(dst)


def main():
    rom, cmds = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    dsm = Path(sys.argv[sys.argv.index("--desmume") + 1]) if "--desmume" in sys.argv else HERE / "desmume"
    out = HERE / "out"
    out.mkdir(exist_ok=True)
    for f in out.glob("*"):
        f.unlink()
    (HERE / "cmds.txt").write_text(cmds.read_text())
    # start from the user's own DeSmuME config (savestates only load with matching emulator settings),
    # but point the paths at the private copy and mute the sound
    import configparser
    user_ini = Path(r"C:/Users/Evan/Documents/dsume/desmume.ini")
    cfg = configparser.RawConfigParser()
    cfg.optionxform = str
    if user_ini.exists():
        cfg.read(user_ini, encoding="utf-8")
    for sec in ("PathSettings", "Sound", "Scripting"):
        if not cfg.has_section(sec):
            cfg.add_section(sec)
    cfg.set("PathSettings", "StateSlots", str(dsm / "StateSlots"))
    cfg.set("PathSettings", "States", str(dsm / "StateSlots"))
    cfg.set("PathSettings", "Battery", str(dsm / "battery"))
    cfg.set("Sound", "Volume", "0")
    with open(dsm / "desmume.ini", "w", encoding="utf-8") as f:
        cfg.write(f, space_around_delimiters=False)
    (dsm / "states").mkdir(exist_ok=True)
    (dsm / "battery").mkdir(exist_ok=True)
    # DeSmuME's "auto-load Lua with ROM" looks for <rom>.lua beside the ROM: run a private copy
    import shutil
    trom = dsm / "hood-soulsilver.nds"
    if not trom.exists() or trom.stat().st_mtime < rom.stat().st_mtime:
        shutil.copy2(rom, trom)
    (dsm / "hood-soulsilver.lua").write_text('dofile([[' + str(HERE / "runner.lua") + ']])' + chr(10))
    p = subprocess.Popen([str(dsm / "DeSmuME_0.9.13_x64.exe"), str(trom)], cwd=dsm)
    log = out / "log.txt"
    sys.path.insert(0, str(HERE))
    import winmenu
    time.sleep(6)
    if "--state" in sys.argv:          # DeSmuME's own File > Load State > N (message, not keyboard)
        slot = sys.argv[sys.argv.index("--state") + 1]
        print("state:", winmenu.fire_path(p.pid, ("File", "Load State", slot)))
        time.sleep(3)
    print("lua:", winmenu.run_lua(p.pid, str(HERE / "runner.lua")))
    t0 = time.time()
    limit = float(sys.argv[sys.argv.index('--timeout') + 1]) if '--timeout' in sys.argv else 60
    while p.poll() is None and time.time() - t0 < limit:
        if time.time() - t0 > 20 and not log.exists():
            print("script did not start within 20s; giving up")
            break
        if log.exists() and "DONE" in log.read_text(errors="ignore"):
            time.sleep(1)
            break
        time.sleep(0.5)
    if p.poll() is None:
        p.kill()
    for g in sorted(out.glob("*.gd")):
        gd_to_png(g, g.with_suffix(".png"))
        g.unlink()
    print(log.read_text(errors="ignore") if log.exists() else "no log (script didn't start?)")
    print("pngs:", len(list(out.glob("*.png"))))


if __name__ == "__main__":
    main()
