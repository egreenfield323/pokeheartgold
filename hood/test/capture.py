"""Capture a move animation from the user's running DeSmuME (window messages only - no keyboard).

    python -I hood/test/capture.py [--frames N] [--step S] [--lead L] [--slot 2] [--crop x0,y0,x1,y1]

Reopens hood-soulsilver.nds, loads the battle savestate (slot 2: at the FIGHT menu), picks move 1 and
screenshots every S frames after a lead-in of L frames; writes out/sheet.png (and the frames).
"""
import subprocess
import sys
import time
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import winmenu  # noqa: E402
from run import gd_to_png  # noqa: E402

ROM = str(HERE.parents[1] / (sys.argv[sys.argv.index("--rom") + 1] if "--rom" in sys.argv else "hood-soulsilver.nds"))


def opt(name, default):
    return type(default)(sys.argv[sys.argv.index(name) + 1]) if name in sys.argv else default


def main():
    frames, step, lead, slot = opt("--frames", 120), opt("--step", 4), opt("--lead", 140), opt("--slot", "2")
    crop = tuple(int(v) for v in opt("--crop", "0,0,256,192").split(","))
    out = HERE / "out"
    out.mkdir(exist_ok=True)
    for f in out.glob("*"):
        f.unlink()
    (HERE / "cmds.txt").write_text(
        f"keepopen\nwait 20\npress A\nwait 30\npress A\nwait 90\npress A\nwait {lead}\n"
        f"burst f {frames} {step}\ndone\n")
    res = subprocess.run(["tasklist", "/FI", "IMAGENAME eq DeSmuME_0.9.13_x64.exe", "/FO", "CSV", "/NH"],
                         capture_output=True, text=True).stdout
    pid = int(res.split(",")[1].strip('"'))
    if "--noreload" not in sys.argv:                 # reopen the ROM (skip if it's already the running one)
        winmenu.fire_path(pid, ("File", "Recent ROM", ROM))
        time.sleep(5)
    item = [p for p in winmenu.items(pid) if p[:2] == ("File", "Load State") and p[2].startswith(slot)][0]
    winmenu.fire_path(pid, item)
    time.sleep(2)
    print("lua:", winmenu.run_lua(pid, str(HERE / "runner.lua")))
    t0 = time.time()
    log = out / "log.txt"
    while time.time() - t0 < 60 + frames * step / 30:
        if log.exists() and "DONE" in log.read_text(errors="ignore"):
            break
        time.sleep(1)
    for g in sorted(out.glob("*.gd")):
        gd_to_png(g, g.with_suffix(".png"))
        g.unlink()
    ims = [Image.open(p).crop(crop) for p in sorted(out.glob("f_*.png"))]
    if not ims:
        print("no frames")
        return
    w, h = ims[0].size
    cols = max(1, min(10, 2000 // (w + 2)))
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (w + 2), rows * (h + 2)))
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % cols) * (w + 2), (i // cols) * (h + 2)))
    sheet.save(out / "sheet.png")
    print(len(ims), "frames ->", out / "sheet.png")


if __name__ == "__main__":
    main()
