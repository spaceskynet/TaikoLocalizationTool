#!/usr/bin/python3
# -*- coding:utf-8 -*-
# For Python 3.6+

REPLACE_STRING = (("『","【"), ("』","】"), ("!", "！"), ("?", "？"), ("ーー", "——"))
COLOR_BLUE = (b'\x1b\x01\x04', b'\x1b\x01\x07')
COLOR_UNKNOWN = (b'\x1b\x01\x01', b'\x1b\x01\x02')
COLOR_NULL = (b'', b'')
COLOR_BLUE_TAG = ("<color-blue>", "</color-blue>")
COLOR_UNKNOWN_TAG = ("<color-unknown>", "</color-unknown>")
COLOR_NULL_TAG =('', '')
COLOR_MAP = {
                COLOR_BLUE: COLOR_BLUE_TAG, 
                COLOR_UNKNOWN: COLOR_UNKNOWN_TAG,
                COLOR_NULL: COLOR_NULL_TAG,
                COLOR_BLUE_TAG: COLOR_BLUE, 
                COLOR_UNKNOWN_TAG: COLOR_UNKNOWN,
                COLOR_NULL_TAG: COLOR_NULL,
            }
SysType = "sys"
StoryType = "story"
CharaType = "chara"
TYPE_MAP = {
                SysType: "SysDatExcel",
                StoryType: "StoryDatExcel",
                CharaType: "CharaDatExcel",
           }
IS_REPLACE_STRING = False
IS_REPLACE_ROW_FLAG = False
MAX_ROW_CHAR = 19
TRY_RANGE = 0x10 * 20

lzx_path = "Tools\\lzx.exe"
ctpktool_path = "Tools\\ctpktool.exe"

sys_dat_file_dir = "_data\\system\\text"
story_dat_file_dir = "_data\\system\\storytext"
chara_dat_file_dir = "_data\\system"

sys_dat_xlsx = "sys_text.xlsx"
story_dat_xlsx = "story_text.xlsx"
chara_dat_xlsx = "chara_text.xlsx"

sys_img_file_dir = "_data"
story_img_file_dir = "_data"

sys_dat_output_dir = "sys_dat_output"
story_dat_output_dir = "story_dat_output"
chara_dat_output_dir = "chara_dat_output"

sys_img_output_dir = "sys_img_output"
story_img_output_dir = "story_img_output"
data_dir = "_data"
all_output_dir = "output"

sys_dat_files = ['AreaPointText_00.dat', 'BattleText_00.dat', 'BossText_00.dat', 'CecText_00.dat', 'CharaText_00.dat', 'CommonUIText_00.dat', 'CostumeText_00.dat', 'DegreeText_00.dat', 'DialogText_00.dat', 'DiaryText_00.dat', 'DonCardText_00.dat', 'EncountText_00.dat', 'ErrorText_00.dat', 'HelpText_00.dat', 'HintText_00.dat', 'InfomationText_00.dat', 'InfoText_00.dat', 'InitAppText_00.dat', 'ItemText_00.dat', 'LevelText_00.dat', 'MagicText_00.dat', 'NaviMapText_00.dat', 'NetText_00.dat', 'QrText_00.dat', 'QuestText_00.dat', 'SkillText_00.dat', 'StampText_00.dat', 'StoreText_00.dat', 'StorySystemText_00.dat', 'SystemText_00.dat', 'WorldText_00.dat'] #Ignore 'QuestText_01.dat'

story_dat_files = ['000_GIMMICK_SET_A.dat', '000_LOCK_SET_A.dat', '000_LOSE_SET_A.dat', '000_NPC_SET_A.dat', '000_NPC_SET_B.dat', '000_NPC_SET_C.dat', '000_NPC_SET_D.dat', '000_NPC_SET_E.dat', '000_NPC_SET_F.dat', '000_NPC_SET_G.dat', '000_NPC_SET_H.dat', '000_NPC_SET_I.dat', '000_SEKIBAN_SET_A.dat', '000_SEKI_R_SET_A.dat', '000_TAIKOMAHOU_SET_A.dat', '001_GIMMICK_SET_A.dat', '001_GIMMICK_SET_B.dat', '001_NPC_SET_A.dat', '001_NPC_SET_B.dat', '002_LOCK_SET_A.dat', '002_NPC_SET_A.dat', '003_GIMMICK_SET_A.dat', '003_LOCK_SET_A.dat', '003_NPC_SET_A.dat', '004_GIMMICK_SET_A.dat', '004_LOCK_SET_A.dat', '004_NPC_SET_A.dat', '004_NPC_SET_B.dat', '005_GIMMICK_SET_A.dat', '005_GIMMICK_SET_B.dat', '005_LOCK_SET_A.dat', '005_NPC_SET_A.dat', '006_GIMMICK_SET_A.dat', '006_LOCK_SET_A.dat', '006_MIMIKKU.dat', '006_NPC_SET_A.dat', '006_NPC_SET_B.dat', '007_GIMMICK_SET_A.dat', '007_NPC_SET_A.dat', 'MAIN_STORY_000_A.dat', 'MAIN_STORY_000_B.dat', 'MAIN_STORY_000_C.dat', 'MAIN_STORY_000_D.dat', 'MAIN_STORY_000_E.dat', 'MAIN_STORY_001_A.dat', 'MAIN_STORY_001_B.dat', 'MAIN_STORY_001_C.dat', 'MAIN_STORY_001_D.dat', 'MAIN_STORY_001_E.dat', 'MAIN_STORY_001_F.dat', 'MAIN_STORY_001_G.dat', 'MAIN_STORY_002_A.dat', 'MAIN_STORY_002_B.dat', 'MAIN_STORY_002_C.dat', 'MAIN_STORY_002_D.dat', 'MAIN_STORY_002_E.dat', 'MAIN_STORY_002_F.dat', 'MAIN_STORY_002_G.dat', 'MAIN_STORY_002_H.dat', 'MAIN_STORY_002_I.dat', 'MAIN_STORY_002_J.dat', 'MAIN_STORY_003_A.dat', 'MAIN_STORY_003_B.dat', 'MAIN_STORY_003_C.dat', 'MAIN_STORY_003_D.dat', 'MAIN_STORY_003_E.dat', 'MAIN_STORY_003_F.dat', 'MAIN_STORY_003_G.dat', 'MAIN_STORY_003_H.dat', 'MAIN_STORY_003_I.dat', 'MAIN_STORY_003_J.dat', 'MAIN_STORY_003_K.dat', 'MAIN_STORY_003_L.dat', 'MAIN_STORY_004_A.dat', 'MAIN_STORY_004_B.dat', 'MAIN_STORY_004_C.dat', 'MAIN_STORY_004_D.dat', 'MAIN_STORY_004_E.dat', 'MAIN_STORY_004_F.dat', 'MAIN_STORY_004_G.dat', 'MAIN_STORY_004_H.dat', 'MAIN_STORY_004_I.dat', 'MAIN_STORY_004_J.dat', 'MAIN_STORY_004_K.dat', 'MAIN_STORY_004_L.dat', 'MAIN_STORY_004_M.dat', 'MAIN_STORY_004_N.dat', 'MAIN_STORY_004_O.dat', 'MAIN_STORY_004_P.dat', 'MAIN_STORY_004_Q.dat', 'MAIN_STORY_004_R.dat', 'MAIN_STORY_004_S.dat', 'MAIN_STORY_004_T.dat', 'MAIN_STORY_005_A.dat', 'MAIN_STORY_005_B.dat', 'MAIN_STORY_005_C.dat', 'MAIN_STORY_005_D.dat', 'MAIN_STORY_005_E.dat', 'MAIN_STORY_005_F.dat', 'MAIN_STORY_005_G.dat', 'MAIN_STORY_005_H.dat', 'MAIN_STORY_005_I.dat', 'MAIN_STORY_005_J.dat', 'MAIN_STORY_006_A.dat', 'MAIN_STORY_006_B.dat', 'MAIN_STORY_006_C.dat', 'MAIN_STORY_006_D.dat', 'MAIN_STORY_006_E.dat', 'MAIN_STORY_006_F.dat', 'MAIN_STORY_006_G.dat', 'MAIN_STORY_006_H.dat', 'MAIN_STORY_006_I.dat', 'MAIN_STORY_006_J.dat', 'MAIN_STORY_006_K.dat', 'MAIN_STORY_007_A.dat', 'MAIN_STORY_007_B.dat', 'MAIN_STORY_007_C.dat', 'MAIN_STORY_007_D.dat', 'MAIN_STORY_007_E.dat', 'MAIN_STORY_007_F.dat', 'MAIN_STORY_007_G.dat', 'MAIN_STORY_007_H.dat', 'MAIN_STORY_007_I.dat', 'MAIN_STORY_007_J.dat', 'STORY_001.dat', 'STORY_002.dat', 'SUB_001_000.dat', 'SUB_001_001.dat', 'SUB_001_002.dat', 'SUB_001_003.dat', 'SUB_001_100.dat', 'SUB_001_101.dat', 'SUB_001_102.dat', 'SUB_002_000.dat', 'SUB_002_001.dat', 'SUB_002_002.dat', 'SUB_002_100.dat', 'Sub_002_101.dat', 'SUB_002_102.dat', 'SUB_002_103.dat', 'SUB_003_000.dat', 'SUB_003_001.dat', 'SUB_003_002.dat', 'SUB_003_100.dat', 'SUB_003_101.dat', 'SUB_003_102.dat', 'Sub_003_103.dat', 'SUB_003_104.dat', 'SUB_004_000.dat', 'SUB_004_001.dat', 'SUB_004_002.dat', 'SUB_005_000.dat', 'SUB_005_001.dat', 'SUB_005_002.dat', 'SUB_005_100.dat', 'SUB_005_101.dat', 'SUB_005_300.dat', 'SUB_006_000.dat', 'SUB_006_001.dat', 'SUB_006_002.dat', 'SUB_007_000.dat', 'SUB_007_001.dat', 'SUB_007_002.dat', 'SUB_007_003.dat', 'SUB_007_004.dat', 'SUB_007_005.dat', 'SUB_007_006.dat', 'SUB_007_007.dat', 'SUB_007_008.dat', 'SUB_007_009.dat', 'SUB_007_010.dat', 'SUB_200_000.dat', 'SUB_202_000.dat', 'SUB_202_002.dat', 'SUB_203_000.dat', 'SUB_204_000.dat', 'SUB_205_000.dat', 'SUB_206_000.dat', 'SUB_207_000.dat', 'SUB_208_000.dat', 'SUB_300_000.dat', 'SUB_409_000.dat', 'SUB_500_100.dat', 'SUB_500_101.dat', 'SUB_500_102.dat']    

chara_dat_files = ['CharaName.dat']

story_img_files = ["story\\adv\\sprite\\0100.txp", "story\\adv\\sprite\\0101.txp", "story\\adv\\sprite\\0102.txp", "story\\adv\\sprite\\0103.txp", "story\\adv\\sprite\\0104.txp", "story\\adv\\sprite\\0105.txp", "story\\adv\\sprite\\0106.txp", "story\\adv\\sprite\\0300.txp", "story\\adv\\sprite\\0301.txp", "story\\adv\\sprite\\0302.txp", "story\\adv\\sprite\\0303.txp", "story\\adv\\sprite\\0304.txp", "story\\adv\\sprite\\0305.txp", "story\\adv\\sprite\\0306.txp", "story\\adv\\sprite\\0307.txp", "story\\adv\\sprite\\0308.txp", "story\\adv\\sprite\\0309.txp", "story\\adv\\sprite\\0310.txp", "story\\adv\\sprite\\0311.txp", "story\\adv\\sprite\\0312.txp", "story\\adv\\sprite\\0313.txp", "story\\adv\\sprite\\0314.txp", "story\\adv\\sprite\\0315.txp", "story\\adv\\sprite\\0316.txp", "story\\adv\\sprite\\0317.txp", "story\\adv\\sprite\\0318.txp", "story\\adv\\sprite\\0319.txp", "story\\adv\\sprite\\0320.txp", "story\\adv\\sprite\\0321.txp", "story\\adv\\sprite\\0322.txp", "story\\adv\\sprite\\0323.txp", "story\\adv\\sprite\\0324.txp", "story\\adv\\sprite\\0325.txp", "story\\adv\\sprite\\0326.txp", "story\\adv\\sprite\\0327.txp", "story\\adv\\sprite\\0328.txp", "story\\adv\\sprite\\0329.txp", "story\\adv\\sprite\\0330.txp", "story\\adv\\sprite\\0331.txp", "story\\adv\\sprite\\0332.txp", "story\\adv\\sprite\\0333.txp", "story\\adv\\sprite\\0334.txp", "story\\adv\\sprite\\0335.txp", "story\\adv\\sprite\\0336.txp", "story\\adv\\sprite\\0337.txp", "story\\adv\\sprite\\0338.txp", "story\\adv\\sprite\\0339.txp", "story\\adv\\sprite\\0340.txp", "story\\adv\\sprite\\0341.txp", "story\\adv\\sprite\\0342.txp", "story\\gasya\\gasya_tail.txp", "story\\gasyaeffect\\gasyaeffect.txp", "story\\level\\Level_Tail.txp", "story\\map_menu\\map_menu.txp", "story\\map_select_tail\\map_select_tail.txp", "story\\memberlist\\memberlist_Head.txp", "story\\memberlist\\memberlist_Tail.txp", "story\\membertop\\membertop_Tail.txp", "story\\menudifficulty\\menudifficulty_tail.txp", "story\\menuhelp\\menuhelp_tail.txp", "story\\menuitem\\menuitem_head.txp", "story\\menuitem\\menuitem_tail.txp", "story\\menumix\\menumix_tail.txp", "story\\menutop\\menutop_tail.txp", "story\\mixdialog\\mixdialog_tail.txp", "story\\mixeffect\\mixeffect.txp", "story\\naviicon\\naviicon.txp", "story\\shop\\Shop_Tail.txp", "story\\titlecall\\titlecall.txp"]

sys_img_files = ["common\\dialog\\dialog.txp", "common\\dialog\\main_daialog.txp", "common\\dialog\\story_daialog.txp", "common\\keyassign\\main_keyassign.txp", "common\\keyassign\\story_keyassign.txp", "common\\loading\\loading.txp", "common\\loading\\loading_story.txp", "common\\save\\save.txp", "costume\\CostumeMaine_Head.txp", "costume\\CostumeMaine_Tail.txp", "crosscommunication\\crosscommunication_head.txp", "crosscommunication\\crosscommunication_tail.txp", "datadelete\\DataDelete_Tail.txp", "enso\\combo.txp", "enso\\kusudama.txp", "enso\\number.txp", "enso\\battle\\battle.txp", "enso\\gage\\gage_easy.txp", "enso\\gage\\gage_hard.txp", "enso\\gage\\gage_normal.txp", "enso\\lane\\end_action.txp", "enso\\onpu\\onpu.txp", "enso\\pause\\pause_enso.txp", "enso\\pause\\pause_story.txp", "gamesetting\\GameInstitute_Tail.txp", "infomation\\Information_Head.txp", "infomation\\Information_Tail.txp", "logo\\logo.txp", "modeselect\\ModeSelect_Tail.txp", "nameentry\\NameEntry_Tail.txp", "playing\\Guide_Head.txp", "playing\\Guide_Tail.txp", "playsetting\\PlaySettintg_Head.txp", "playsetting\\PlaySettintg_Tail.txp", "result\\result_head.txp", "result\\result_tail.txp", "songselect\\SongSelect_Head.txp", "songselect\\SongSelect_Tail.txp", "store\\Store_Head.txp", "store\\Store_Tail.txp", "store\\Store_Top.txp", "title\\title_tail.txp", "title\\title_head.txp", "wireless\\quest.txp", "wireless\\wireless.txp", "stampbook\\StampBook_Head.txp", "system\\songtitle\\song_title_tate.txp", "system\\songtitle\\song_title_tate_sub.txp", "system\\songtitle\\song_title_yoko.txp", "system\\songtitle\\song_title_yoko_sub.txp"]
