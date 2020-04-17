#!/usr/bin/python3
# -*- coding:utf-8 -*-
# For Python 3.6+

from TaikoTools.consts import *
from TaikoTools import checker, packer
import fire

ERROR = "[Error]: ERROR COMMAND!"

class CLI(object):
    def check(self, type = "all"):
        types = [SysType, StoryType, CharaType]
        if type == "all":
            for t in types:
                checker.dat_header_checker(t)
        elif type in types: checker.dat_header_checker(type)
        else: print(ERROR)
        
    def text(self, action, type = "all"):
        types = [SysType, StoryType, CharaType]
        actions = ["export", "import"]
        if action not in actions: print(ERROR)
        elif action == "export":
            if type == "all":
                for t in types:
                    packer.unpack_dat(t)
            elif type in types: packer.unpack_dat(type)
            else: print(ERROR)
        else:
            if type == "all":
                for t in types:
                    packer.pack_dat(t)
            elif type in types: packer.pack_dat(type)
            else: print(ERROR)
    
    def img(self, action, type = "all"):
        types = [SysType, StoryType]
        actions = ["export", "import"]
        if action not in actions: print(ERROR)
        elif action == "export":
            if type == "all":
                for t in types:
                    packer.unpack_txp(t)
            elif type in types: packer.unpack_txp(type)
            else: print(ERROR)
        else:
            if type == "all":
                for t in types:
                    packer.pack_txp(t)
            elif type in types: packer.pack_txp(type)
            else: print(ERROR)
            
    def packall(self):
        packer.packall()
        
    def unpackall(self):
        packer.unpackall()
        
if __name__ == "__main__":
    fire.Fire(CLI)