"""Record what a move sounds like: reopen the ROM, load a savestate, start DeSmuME's File > Record WAV, pick move 1,
let it play, stop recording. Window messages only - no keyboard.

    python -I hood/test/record_audio.py OUT.wav [--rom hood-showcase.nds] [--slot 3] [--frames 900]
"""
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import winmenu  # noqa: E402

u = winmenu.u


def opt(name, default):
    return type(default)(sys.argv[sys.argv.index(name) + 1]) if name in sys.argv else default


def save_dialog(pid, path, timeout=5.0):
    """Fill the Save As dialog DeSmuME just opened with `path` and press Save."""
    t0 = time.time()
    while time.time() - t0 < timeout:
        for d in winmenu.dialogs_of(pid):
            title = winmenu.ctypes.create_unicode_buffer(200)
            u.GetWindowTextW(d, title, 200)
            if not title.value.lower().startswith("save"):
                continue
            kids = winmenu.children(d)
            edits = [c for c, cls, _ in kids if cls.lower() == "edit"][-1:]      # the file name (the first is search)
            saves = [c for c, cls, t in kids if cls.lower() == "button" and t.replace("&", "").lower() == "save"]
            if edits and saves:
                u.SendMessageW(edits[0], 0x000C, 0, winmenu.ctypes.c_wchar_p(str(path)))   # WM_SETTEXT
                time.sleep(0.2)
                u.SendMessageW(saves[0], 0x00F5, 0, 0)                                    # BM_CLICK
                return True
        time.sleep(0.2)
    return False


def main():
    out = Path(sys.argv[1]).resolve()
    rom = str(HERE.parents[1] / opt("--rom", "hood-showcase.nds"))
    slot, frames = opt("--slot", "3"), opt("--frames", 900)
    if out.exists():
        out.unlink()
    res = subprocess.run(["tasklist", "/FI", "IMAGENAME eq DeSmuME_0.9.13_x64.exe", "/FO", "CSV", "/NH"],
                         capture_output=True, text=True).stdout
    pid = int(res.split(",")[1].strip('"'))
    winmenu.fire_path(pid, ("File", "Recent ROM", rom))
    time.sleep(5)
    item = [p for p in winmenu.items(pid) if p[:2] == ("File", "Load State") and p[2].startswith(slot)][0]
    winmenu.fire_path(pid, item)
    time.sleep(2)
    assert winmenu.fire(pid, "Record WAV"), "no Record WAV menu item"
    assert save_dialog(pid, out), "no save dialog"
    time.sleep(1)
    log = HERE / "out" / "log.txt"
    if log.exists():
        log.unlink()
    (HERE / "cmds.txt").write_text(f"keepopen\nwait 20\npress A\nwait 30\npress A\nwait 90\npress A\nwait {frames}\ndone\n")
    print("lua:", winmenu.run_lua(pid, str(HERE / "runner.lua")))
    t0 = time.time()
    while time.time() - t0 < 60 + frames / 30:
        if log.exists() and "DONE" in log.read_text(errors="ignore"):
            break
        time.sleep(1)
    stop = [p for p in winmenu.items(pid) if p[0] == "File" and "wav" in p[-1].lower()]
    winmenu.fire_path(pid, stop[0])                       # the same item, now "Stop WAV"
    time.sleep(1)
    print(stop[0], "->", out, out.stat().st_size if out.exists() else "missing")


if __name__ == "__main__":
    main()
