"""Fire a menu item in another process's window by name (PostMessage WM_COMMAND). No keyboard, no focus."""
import ctypes
from ctypes import wintypes

u = ctypes.windll.user32
u.GetMenuStringW.argtypes = [wintypes.HMENU, wintypes.UINT, wintypes.LPWSTR, ctypes.c_int, wintypes.UINT]
u.GetSubMenu.restype = wintypes.HMENU
u.GetMenu.restype = wintypes.HMENU
WM_COMMAND, MF_BYPOSITION = 0x0111, 0x400


def windows_of(pid):
    found = []

    @ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    def cb(h, _):
        p = wintypes.DWORD()
        u.GetWindowThreadProcessId(h, ctypes.byref(p))
        if p.value == pid and u.IsWindowVisible(h) and u.GetMenu(h):
            found.append(h)
        return True
    u.EnumWindows(cb, 0)
    return found


def walk(menu, path=()):
    for i in range(u.GetMenuItemCount(menu)):
        buf = ctypes.create_unicode_buffer(256)
        u.GetMenuStringW(menu, i, buf, 256, MF_BYPOSITION)
        name = buf.value.replace("&", "").split("\t")[0]
        sub = u.GetSubMenu(menu, i)
        if sub:
            yield from walk(sub, path + (name,))
        else:
            yield path + (name,), u.GetMenuItemID(menu, i)


def fire(pid, text):
    for h in windows_of(pid):
        for path, mid in walk(u.GetMenu(h)):
            if path[-1].lower().startswith(text.lower()):
                u.PostMessageW(h, WM_COMMAND, mid, 0)
                return path
    return None


def items(pid):
    return [p for h in windows_of(pid) for p, _ in walk(u.GetMenu(h))]


def dialogs_of(pid):
    found = []

    @ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    def cb(h, _):
        p = wintypes.DWORD()
        u.GetWindowThreadProcessId(h, ctypes.byref(p))
        if p.value == pid and u.IsWindowVisible(h) and not u.GetMenu(h):
            found.append(h)
        return True
    u.EnumWindows(cb, 0)
    return found


def children(h):
    out = []

    @ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    def cb(c, _):
        cls = ctypes.create_unicode_buffer(64)
        u.GetClassNameW(c, cls, 64)
        txt = ctypes.create_unicode_buffer(256)
        u.GetWindowTextW(c, txt, 256)
        out.append((c, cls.value, txt.value))
        return True
    u.EnumChildWindows(h, cb, 0)
    return out


def lua_window(pid):
    """(edit, run button) of an open Lua script window, or None."""
    for d in dialogs_of(pid):
        kids = children(d)
        edits = [c for c, cls, _ in kids if cls.lower() == "edit"]
        runs = [c for c, cls, t in kids if cls.lower() == "button" and t.replace("&", "").lower() in ("run", "restart")]
        if edits and runs:
            return edits[0], runs[0]
    return None


def run_lua(pid, path, wait=3.0):
    """Put `path` in DeSmuME's Lua window and press Run - reusing an open window (only opening one if there
    is none), all via window messages."""
    import time
    win = lua_window(pid)
    if win:
        u.SendMessageW(win[0], 0x000C, 0, ctypes.c_wchar_p(path))     # WM_SETTEXT
        time.sleep(0.2)
        u.SendMessageW(win[1], 0x00F5, 0, 0)                           # BM_CLICK
        return "ok"
    if not fire(pid, "New Lua Script Window"):
        return "no menu"
    t0 = time.time()
    while time.time() - t0 < wait:
        for d in dialogs_of(pid):
            kids = children(d)
            edits = [c for c, cls, _ in kids if cls.lower() == "edit"]
            runs = [c for c, cls, t in kids if cls.lower() == "button" and t.replace("&", "").lower() in ("run", "restart")]
            if edits and runs:
                u.SendMessageW(edits[0], 0x000C, 0, ctypes.c_wchar_p(path))   # WM_SETTEXT
                time.sleep(0.2)
                u.SendMessageW(runs[0], 0x00F5, 0, 0)                          # BM_CLICK
                return "ok"
        time.sleep(0.2)
    return "no dialog"


def fire_path(pid, path):
    """Fire a menu item by its full path, e.g. ("File", "Load State", "2")."""
    want = tuple(p.lower() for p in path)
    for h in windows_of(pid):
        for p, mid in walk(u.GetMenu(h)):
            if tuple(x.lower() for x in p) == want:
                u.PostMessageW(h, WM_COMMAND, mid, 0)
                return True
    return False
