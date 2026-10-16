"""Battle animation scripts (files/a/0/1/0): a tiny assembler/disassembler for the u32 word format.

Only the commands Hood HeartGold uses are fully described; others are printed raw.
"""
import struct

NAMES = {0: "Wait", 1: "WaitForTasks", 2: "BeginLoop", 3: "EndLoop", 4: "End", 5: "PlaySE", 10: "Call",
         11: "Return", 15: "Jump", 22: "PlaySEWithPan", 26: "DelayedSE", 29: "WaitForSoundTasks", 45: "CallFunc",
         46: "CreateEmitter", 50: "WaitForParticles", 51: "LoadParticleSystem", 53: "FreeParticleSystem",
         64: "JumpBySide", 73: "InitSpriteManager", 74: "LoadCharResource", 75: "LoadPaletteResource",
         76: "LoadCellResource", 77: "LoadAnimResource", 78: "CreateSpriteWithFunc", 79: "CreateSprite",
         80: "FreeSpriteManager", 85: "BrightnessFlash", 56: "InitBattlerSpriteManager",
         57: "LoadBattlerSpriteResources", 58: "CreateBattlerSprite", 59: "FreeBattlerSpriteManager",
         60: "DeleteBattlerSprite", 25: "RepeatSE", 81: "SetBattlerSpriteVisible", 82: "StartBattlerSpriteDraw",
         83: "StopBattlerSpriteDraw", 6: "Nop6", 7: "Nop7", 55: "EmitterArgs",
         12: "SetArg", 13: "JumpByVariantBit0", 14: "JumpIfVariantEqual", 16: "SwitchBackground",
         17: "SetBgScroll", 18: "RestoreBackground", 20: "WaitForBackgroundSwitch", 23: "SetSEPan", 24: "PanSweepSE",
         30: "JumpIfArgEqual", 33: "JumpIfContextField01", 47: "CreateEmitterInSlot", 48: "CreateEmitterByPosition6",
         49: "CreateEmitterByPosition4", 62: "SetParticlePerspective", 63: "SetParticleFlipY", 65: "PlayCry",
         67: "ClearArgs", 70: "JumpByWeather", 71: "JumpIfField08Is1", 72: "JumpIfSameSide", 87: "JumpIfAttackerActive"}
FIXED = {  # argument words after the opcode, counted from each handler in battle_anim_system.c
    0: 1, 1: 0, 2: 1, 3: 0, 4: 0, 5: 1, 6: 0, 7: 0, 8: 2, 9: 0, 10: 1, 11: 0, 12: 2, 13: 2,
    14: 2, 15: 1, 16: 2, 17: 2, 18: 2, 19: 0, 20: 0, 21: 1, 22: 2, 23: 1, 24: 5, 25: 4, 26: 3, 27: 0,
    28: 0, 29: 0, 30: 3, 31: 2, 32: 1, 33: 1, 34: 3, 35: 5, 36: 5, 37: 0, 38: 0, 39: 0, 40: 0, 41: 0,
    42: 0, 43: 0, 44: 1, 46: 3, 47: 4, 48: 8, 49: 6, 50: 0, 51: 2, 52: 3, 53: 1, 54: 0, 55: 0, 56: 0,
    57: 1, 58: 4, 59: 0, 60: 1, 61: 1, 62: 2, 63: 2, 64: 3, 65: 3, 66: 1, 67: 0, 68: 1, 69: 1, 70: 5,
    71: 1, 72: 1, 74: 2, 75: 3, 76: 2, 77: 2, 79: 8, 80: 1, 81: 2, 82: 3, 83: 1, 84: 0, 85: 1, 86: 3,
    87: 1}


def disasm(words):
    out, i = [], 0
    while i < len(words):
        op = words[i]
        if op == 45:      # CallFunc id count args...
            n = 3 + words[i + 2]
        elif op == 55:    # inline emitter-callback data (BattleAnimSystem_ReadScriptArgs): 55 count values...
            n = 2 + words[i + 1]
        elif op == 73:    # InitSpriteManager index max caps[6]
            n = 9
        elif op == 78:    # CreateSpriteWithFunc mgr func res[6] count args...
            n = 10 + words[i + 9]
        elif op in FIXED:
            n = 1 + FIXED[op]
        else:
            out.append((i, f"?{op}", words[i + 1:i + 4]))
            i += 1
            continue
        out.append((i, NAMES.get(op, str(op)), list(words[i + 1:i + n])))
        i += n
    return out


def asm(cmds):
    """cmds: list of (opcode, [args]) -> bytes"""
    words = []
    for op, args in cmds:
        words.append(op)
        words.extend(a & 0xFFFFFFFF for a in args)
    return struct.pack(f"<{len(words)}I", *words)
