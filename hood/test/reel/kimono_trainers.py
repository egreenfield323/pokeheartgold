"""Write the Dancers' named TRMSG_LOSE lines (hood/data/trainer_dialogue.json "named") into trainers.json and the
msg_0728 bank for just those five trainers, the same way apply_hood.apply_trainers() does it."""
import json
import struct
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "hood"))
import apply_hood as ah  # noqa: E402

NAMES = ("Zuki", "Naoko", "Miki", "Sayo", "Kuni")
dlg = ah.load("trainer_dialogue.json")
path = ROOT / "files/poketool/trainer/trainers.json"
data = json.loads(path.read_text(encoding="utf-8"))
tbl = (ROOT / "files/poketool/trmsg/trtbl.narc").read_bytes()
off, size = ah.narc_files(tbl)[0]
row_of = {}
for r in range(size // 4):
    tr, ty = struct.unpack_from("<HH", tbl, off + 4 * r)
    row_of[(tr, ty)] = r
bank = ah.Bank.get("msg_0728")
for n, t in enumerate(data["trainers"]):
    name = t["name"].replace("{TRNAME}", "")
    if name not in NAMES:
        continue
    for msg in t["messages"]:
        if msg["type"] != "TRMSG_LOSE":
            continue
        end = "\\r" if msg["message"].endswith("\\r") else "\\n"
        msg["message"] = ah.wrap(dlg["named"][name]["TRMSG_LOSE"], end=end)
        ah.check_text(msg["message"], f"trainer {n} {name}", max_line=40)
        bank.set(row_of[(n, 1)], msg["message"])                 # type 1 = TRMSG_LOSE
        print(n, name, msg["message"])
if ah.ERRORS:
    sys.exit("\n".join(ah.ERRORS))
path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")
import text_edits  # noqa: E402
text_edits.apply(ah.Bank, only=["msg_0728"])
ah.Bank.save_all()
print("done")
