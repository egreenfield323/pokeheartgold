"""Small code patches to the game's overlays.

follow_text: the walking-homie reactions (msg_0265) are read with MSGDATA_LOAD_DIRECT, which loads the WHOLE bank
into the field heap every time you talk to your homie. Vanilla's bank is ~69 KB; the hood rewrite ("CYNDAQUIL said:
"..." (...)") is ~85 KB, and past ~78 KB the allocation fails and the interaction hangs before the text box. So
FollowMon_ExpandInteractionMessage (overlay 2) is switched to MSGDATA_LOAD_LAZY (rows read from the file one at a
time, like most of the game's text), and the bank can be any size.
"""
import struct

import ndspy.code

OV_FIELD = 2
# FollowMon_ExpandInteractionMessage: movs r1,#0x1b / ... / movs r0,#0 (load type) / adds r2,#0xee (bank 265)
FOLLOW_TEXT_AT = 0xA11A
FOLLOW_TEXT_OLD = (0x2000, 0x32EE)                            # movs r0,#0 (DIRECT); adds r2,#0xee
FOLLOW_TEXT_NEW = 0x2001                                      # movs r0,#1 (LAZY)


def follow_text(rom):
    ovs = rom.loadArm9Overlays()
    ov = ovs[OV_FIELD]
    code = bytearray(ov.data)
    load, bank = struct.unpack_from("<HH", code, FOLLOW_TEXT_AT)
    if load == FOLLOW_TEXT_NEW:
        return
    assert (load, bank) == FOLLOW_TEXT_OLD, (hex(load), hex(bank))
    struct.pack_into("<H", code, FOLLOW_TEXT_AT, FOLLOW_TEXT_NEW)
    ov.data = bytes(code)
    old = len(rom.files[ov.fileID])
    packed = ov.save(compress=True)
    # same 0x200 slot in the ROM, so nothing after it moves (savestates)
    assert (len(packed) + 0x1FF) // 0x200 == (old + 0x1FF) // 0x200, (len(packed), old)
    rom.files[ov.fileID] = packed
    ov.compressedSize = len(packed)
    rom.arm9OverlayTable = ndspy.code.saveOverlayTable(ovs)


def patch(rom):
    follow_text(rom)
    print("code: walking-homie text read lazily")
