#!/usr/bin/python3
# -*- coding:utf-8 -*-
# For Python 3.6+

from TaikoTools.consts import *
import struct, os

def dat_header_checker(file_type):
    files = eval("{}_dat_files".format(file_type))
    dat_file_dir = eval("{}_dat_file_dir".format(file_type))
    for file_name in files:
        try:
            f = open(os.path.join(dat_file_dir, file_name), "rb")
        except FileNotFoundError as e:
            print("[Error]: Unable to open file. %s" % (e))
            continue
        bin_text = f.read()
        f.close()
        if file_type == "sys":
            text_count, file_header = struct.unpack("<I8s", bin_text[:0xC])
            if file_header != b'\x10\x00\x00\x00\x20\x00\x00\x00': print("[Error]: %s is not a %s file!\n" % (file_name, file_type))
        else:
            file_header, text_count = struct.unpack("<4sI", bin_text[:0x8])
            if file_header != b'\x10\x00\x00\x00': print("[Error]: %s is not a %s file!\n" % (file_name, file_type))
    print("[Check]: All %s dat file format is right!" % file_type)
        
if __name__ == "__main__":
    dat_header_checker(SysType)    