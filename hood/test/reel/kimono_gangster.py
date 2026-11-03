"""The Kimono Girls ("Dancers") rewritten as a hardcore gangster family: Zuki is the boss, the Dance Theater is
the front. Writes the rows into hood/data/dialogue/*.json and the named trainer lose-lines into
hood/data/trainer_dialogue.json. Then apply with:
  python hood/apply_dialogue.py msg_0618_T27R0501 msg_0058_D17R0110 msg_0125_D40R0107 msg_0115_D36R0101 msg_0122_D39R0101 msg_0377
Re-runnable. Row endings / tokens must match the original rows (apply_dialogue checks)."""
import json
from pathlib import Path
D = Path(__file__).resolve().parents[2] / "data"

ROWS = {
 "msg_0618_T27R0501": {
  "_comment": "Ecruteak Dance Theater = the front for the Dancers, a hardcore gangster family (Zuki = the boss). A Fed heckles a Dancer and has no idea who he's messing with; the five Dancers' test; the useless men with sudden aches.",
  "1": r"Quit doin' that serious dance!\nGimme somethin' upbeat! I paid\fadmission! Well, the GOVERNMENT did!\r",
  "2": r"...You know who you talkin' to?\nThis theater is FAMILY property.\rSit down. Before the family sit\nyou down. Permanently.\r",
  "3": r"Huh? Was that a THREAT?\nI'm a FEDERAL agent! I'll write\fyou up! I got a CLIPBOARD!\r",
  "7": r"Oops! I got a important mission!\rAlso that Dancer looked at me like\nshe know where I live.\fShe DO know where I live. She\fknow my MOM.\rI'm OUT!\r",
  "9": r"You must be {STRVAR_1 3, 0, 0}, correct?\nThat was EXCELLENT.\fCold. Calm. Didn't even flinch...\rThe family could use somebody\nlike that...\rOhoho! I was talkin' to myself.\fI do that. Witnesses don't.",
  "10": r"For Dancers like me, the dance is\nEVERYTHING. Also it's a front.\rTwelve years we been runnin' this\ntheater. Not ONE cop came inside.\rHomies the same way. Loyal. Quiet.\nThey grow a lil every day.",
  "11": r"Welcome.\nMy name is Zuki. I run this family.\fWe met before in Violet City.\rTo bring back HO-OH, we needed\nsomebody solid with homies.\fSomebody who don't snitch.\rWe had Mr. Pokémon pass that\nMystery Egg along. He owed us.\fEverybody owe us.\rThe Egg went from Mr. Pokémon\nto Professor Elm, and then\fto you. We watched the whole time.\rBut bein' solid ain't enough\nto sit at the family table.\fI gotta test you.\rYou ready? {YESNO 0}",
  "12": r"Welcome.\nMy name is Zuki. I run this family.\fWe met before in Violet City.\rTo bring back LUGIA, we needed\nsomebody solid with homies.\fSomebody who don't snitch.\rWe had Mr. Pokémon pass that\nMystery Egg along. He owed us.\fEverybody owe us.\rThe Egg went from Mr. Pokémon\nto Professor Elm, and then\fto you. We watched the whole time.\rBut bein' solid ain't enough\nto sit at the family table.\fI gotta test you.\rYou ready? {YESNO 0}",
  "13": r"I'ma test you. If you fold,\nwe never met.\rYou ready? {YESNO 0}",
  "14": r"That's fine...\nThe family is patient.\fWe wait. We ALWAYS wait.",
  "15": r"You real strong.\rYou found me in Ilex Forest.\rMy name is Naoko. I'm the family's\ngetaway driver.\fI can't read a map. I got us lost\fon EVERY job.\rWe still never got caught. Cops can't\nfind us 'cause WE can't find us.\rLet me challenge you and your\nhomies!\r",
  "16": r"...\rYou ran that Fed off our stage.\rThe family noticed.\r...\rThe one who know the most\ntalk the least.\fI'm Miki. I break legs.\rLet me challenge you and your\nhomies!\r",
  "17": r"Hard fightin' spirit!\rYou pushed me off the ice in the\nIce Path. I don't forget a favor.\rI'm the one who skate in sandals.\fBoots leave footprints. I'm Sayo.\rI was listenin' in the Dragon's Den\nwhen you passed the Elder's test.\fI'm ALWAYS listenin'.\rLet me challenge you and your\nhomies!\r",
  "18": r"I'm the last one.\rYou was solid in the Goldenrod\nTunnel. That's MY tunnel.\fEverything underground go through me.\rI'm Kuni. I spin even underground.\fESPECIALLY underground.\rI watched you shut down The Feds\nat the Radio Tower.\fThey was on our turf anyway.\rLet me challenge you and your\nhomies!\r",
  "19": r"Talk to Zuki in the middle\nwhen you ready. Nobody skip the boss.",
  "20": r"We was right about you.\nYou family now...\rTake it. Don't ask where it\ncame from.\r",
  "21": r"Boss! Big sisters!\rLookout just called it in. Giant\nhomie shadow over the Bell Tower!\rIt could be...\r",
  "22": r"Boss! Big sisters!\rLookout just called it in. Giant\nhomie shadow in the Whirl Islands!\rIt could be...\r",
  "23": r"Zuki: {STRVAR_1 3, 0, 0}!\nThe family's movin' to the Bell Tower.\fBe there. Nobody's late twice.\r",
  "24": r"Zuki: {STRVAR_1 3, 0, 0}!\nThe family's movin' to the Whirl Islands.\fBe there. Nobody's late twice.\r",
  "25": r"WASSUP with that Fed, messin' with a\nDancer?! Do he KNOW who they are?\rYou a Hustler, ain't you?\fGo help HIM! Before she do\fsomethin' to him!",
  "26": r"WONDERFUL! You so brave for your age!\rYou saved that Fed's LIFE.\nHe don't even know it.\fI want you to have this.\fDon't be shy--take it!\r",
  "29": r"The Dancers ain't just great dancers,\nthey run EVERYTHING in Ecruteak.\rThe lights, the tea shop, the parking.\nLord help you if you double-park.",
  "36": r"The Dancers is SO beautiful...\rBut nobody ask 'em out. Last guy who\ntried? Nobody seen him since.\rIf you love somethin', anything is\npossible. Except me gettin' a date.",
  "37": r"Doin' somethin' that foul to a Dancer!\rThat Fed is DONE. They gon' find him\nin a teacup.\fBack in my day we RESPECTED\fthe family!",
  "40": r"Good looks for your help the\nother day. The family remember.",
  "41": r"We rehearsin' a dance.\nAnd countin' money. Mostly money.",
  "42": r"Good looks for helpin' the other day.\rYou proved the bond between\npeople and homies is like the\fbond of the family. Unbreakable.\rWe all appreciate you, {STRVAR_1 3, 0, 0}!\rYou need anything--ANYTHING--\nyou call us.\fAnd thank Mr. Pokémon and\fProfessor Elm. They on the payroll.",
  "43": r"We rehearsin' a dance.\nAnd countin' money. Mostly money.",
  "44": r"Good looks for your help the\nother day. The family remember.",
  "45": r"I'ma test how tight you\nare with your homies. Family rules!\r",
 },
 "msg_0058_D17R0110": {
  "_comment": "Bell Tower roof. Zuki and the Dancers (a gangster family) summon HO-OH.",
  "0": r"Zuki: Yes. This where the family\nwelcome HO-OH.\rWhen the dance we practiced for\ndays becomes one with the sound of\fthe Clear Bell we gave you,\rHO-OH gon' come down from the\ngreat arch of the sky again!\fIt owe us a visit.\r",
  "1": r"That's all we can do for you...\nWhat you do now is on you.\fNo witnesses.",
  "2": r"That IS HO-OH...\nThe guardian of the sky round here\fsince forever...\rSo many tried and tried, and\ncame up short...\r{STRVAR_1 3, 0, 0}, your heart and the Clear\nBell in sync finally made\fit show up... The family been waitin'.\r",
  "3": r"{STRVAR_1 3, 0, 0}, you see it?\rHO-OH been waitin' for somebody\nlike you this whole time.\fRight...? Right. Nobody tell us no.\r",
  "5": r"You did amazing.\nTell Professor Elm the family said\fwassup. He'll know what it mean.",
  "6": r"You ain't just got HO-OH to show,\nyou caught it too...\rYou made now. You family.\nWe got nothin' else to say.\rStay outta trouble. Or call us first.",
  "7": r"If that's what you believe, we\nain't gon' change your mind.\fWe COULD. We won't.\rStill, if you wanna see HO-OH again,\nmaybe come back here\fafter everything settle down...",
  "8": r"I think when you turn your back\non it, HO-OH won't come back for\fa while... Like everybody who\fcrossed the family.\rIf you wanna see HO-OH, maybe\ncome back here after everything\fsettle down...",
 },
 "msg_0125_D40R0107": {
  "_comment": "Whirl Islands basin. Zuki and the Dancers (a gangster family) summon LUGIA.",
  "0": r"Zuki: That's right.\nThis where the family welcome LUGIA.\rWhen the dance we practiced for days\nbecomes one with the sound of the\fTidal Bell we gave you, then\fLUGIA gon' rise up from the\fwaterfall basin again!\fIt owe us a visit.\r",
  "1": r"That's all we can do for you...\nWhat you do now is on you.\fNo witnesses.",
  "2": r"That IS LUGIA...\nThe guardian of these islands\fsince forever...\rSo many tried over and over,\nand came up short...\r{STRVAR_1 3, 0, 0}, your heart in total\nsync with the Tidal Bell finally\fmade it show up... The family been waitin'.\r",
  "3": r"{STRVAR_1 3, 0, 0}, you see it?\rLUGIA... It been waitin' for\nsomebody like you this whole time.\fRight...? Right. Nobody tell us no.",
  "5": r"You did amazing. Tell\nProfessor Elm the family said\fwassup. He'll know what it mean.",
  "6": r"You ain't just got LUGIA to show,\nyou caught it too...\rYou made now. You family.\nWe got nothin' else to say.\rStay outta trouble. Or call us first.",
  "7": r"If that's what you believe, we\nain't gon' change your mind.\fWe COULD. We won't.\rStill, if you wanna see LUGIA again,\nmaybe come back here\fafter everything settle down...",
  "8": r"I think once you turn your back\non it, LUGIA won't come back for\fa while... Like everybody who\fcrossed the family.\rIf you wanna see LUGIA, maybe\ncome back here after everything\fsettle down...",
 },
 "msg_0115_D36R0101": {
  "30": r"What? You remember me from Violet City?\fNever happened. We never met.\rI'm the family's getaway driver.\nI got lost. In a forest.\fDURING the getaway.\rYou gon' show me the way out? {YESNO 0}",
 },
 "msg_0377": {
  "7": r"Kimono Girls? Never heard of 'em.\nI don't owe 'em NOTHIN'.\fWhy you lookin' at me like that?\r",
 },
}

LOSE = {
 "Zuki": "...Fine. You family now. Don't make me regret it.",
 "Naoko": "I lost. Like I lose on every map.",
 "Miki": "...Respect.",
 "Sayo": "My sandals slipped. That's the story we tellin'.",
 "Kuni": "Down here nobody lose. ...Keep this quiet.",
}


def main():
    for bank, rows in ROWS.items():
        p = D / "dialogue" / f"{bank}.json"
        d = json.loads(p.read_text(encoding="utf-8"))
        for k, v in rows.items():
            assert k == "_comment" or k in d, (bank, k)
            d[k] = v
        p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    p = D / "trainer_dialogue.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    for name, line in LOSE.items():
        d["named"].setdefault(name, {})["TRMSG_LOSE"] = line
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("written")


if __name__ == "__main__":
    main()
