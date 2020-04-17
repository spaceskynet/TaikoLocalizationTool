#!/usr/bin/python3
# -*- coding:utf-8 -*-
# For Python 3.6+

import struct, os, shutil, sys

from TaikoTools.TableIO import SysDatExcel, StoryDatExcel, CharaDatExcel
from TaikoTools.consts import *

def check_tools():
    if not os.path.exists(lzx_path): 
        print("[Error]: Unable to find %s." % (lzx_path))
        os._exit(-1)
    if not os.path.exists(ctpktool_path): 
        print("[Error]: Unable to find %s." % (ctpktool_path))
        os._exit(-1)

def pack_txp(file_type):
    img_files = eval("{}_img_files".format(file_type))
    img_file_dir = eval("{}_img_file_dir".format(file_type))
    img_output_dir = eval("{}_img_output_dir".format(file_type))
    check_tools()
    for file in img_files:
        file = os.path.join(img_file_dir, file)
        if not os.path.exists(file[:-4]): raise FileNotFoundError
        try:
            ret = os.popen('{} -d {}'.format(lzx_path, file)).read() #
        except:
            pass
        finally:
            str, inf= "file is not LZX encoded!", "{} has been decompressed (LZ11)!"
            if str in ret: print("[Warning]: " + inf.format(os.path.split(file)[1]))
        ret = os.popen('{} -ivfd {} {}'.format(ctpktool_path , file, file[:-4])).read()
        #print(ret)
        if "load" not in ret: raise TypeError
        ret = os.popen('{} -evb {}'.format(lzx_path, file)).read()
        #print(ret)
        if "Done" not in ret: raise TypeError
        try:
            if not os.path.exists(os.path.join(img_output_dir, os.path.split(file)[0])):
                os.makedirs(os.path.join(img_output_dir, os.path.split(file)[0]))
            shutil.copy(file, os.path.join(img_output_dir, os.path.split(file)[0]))
        except IOError as e:
            print("[Error]: Unable to copy file. %s" % (e))
        except:
            print("[Error]: Unexpected error:", sys.exc_info())
        print("[Img]: %s Done." % os.path.split(file)[1])
    
def unpack_txp(file_type):
    img_files = eval("{}_img_files".format(file_type))
    img_file_dir = eval("{}_img_file_dir".format(file_type))
    img_output_dir = eval("{}_img_output_dir".format(file_type))
    check_tools()
    for file in img_files:
        file = os.path.join(img_file_dir, file)
        ret = os.popen('{} -d {}'.format(lzx_path, file)).read()
        #print(file, ret)
        if "Done" not in ret: raise TypeError
        if not os.path.exists(file[:-4]):
            os.mkdir(file[:-4])
        ret = os.popen('{} -evfd {} {}'.format(ctpktool_path, file, file[:-4])).read()
        print("[Img]: %s Done." % os.path.split(file)[1])
        #print(ret)
        #file_with_png[os.path.split(file)[1]] = []
        #ret = ret.split('\n')
    
def extract_txp(file_type):
    img_files = eval("{}_img_files".format(file_type))
    img_file_dir = eval("{}_img_file_dir".format(file_type))
    img_output_dir = eval("{}_img_output_dir".format(file_type))
    for file in img_files:
        file = os.path.join(img_file_dir, file)
        if not os.path.exists(os.path.join(img_output_dir, os.path.split(file)[0])):
            os.makedirs(os.path.join(img_output_dir, os.path.split(file)[0]))
        try:
            shutil.copy(file, os.path.join(img_output_dir, os.path.split(file)[0]))
        except IOError as e:
            print("[Error]: Unable to copy file. %s" % e)
        except:
            print("[Error]: Unexpected error:", sys.exc_info())
        else:
            print("[Img]: %s Done." % os.path.split(file)[1])

def pack_dat(file_type):
    DatTable = eval("{}({}_dat_xlsx)".format(TYPE_MAP[file_type], file_type))
    DatTable.import_from_table()
    dat_files = eval("{}_dat_files".format(file_type))
    dat_file_dir = eval("{}_dat_file_dir".format(file_type))
    dat_output_dir = eval("{}_dat_output_dir".format(file_type))
    for file in dat_files:
        file = os.path.join(dat_file_dir, file)
        if not os.path.exists(file + "_tr"): raise FileNotFoundError
        try:
            if not os.path.exists(os.path.join(dat_output_dir, os.path.split(file)[0])):
                os.makedirs(os.path.join(dat_output_dir, os.path.split(file)[0]))
            shutil.copy(file + "_tr", os.path.join(dat_output_dir, file))
        except IOError as e:
            print("[Error]: Unable to copy file. %s" % (e))
        except:
            print("[Error]: Unexpected error:", sys.exc_info())
        print("[Text]: %s Done." % os.path.split(file)[1])
    
def unpack_dat(file_type):
    DatTable = eval("{}({}_dat_xlsx)".format(TYPE_MAP[file_type], file_type))
    DatTable.export_to_table()
    
def unpack_dat_trans(file_type):
    DatTable = eval("{}({}_dat_xlsx)".format(TYPE_MAP[file_type], file_type))
    DatTable.export_trans_to_table()

def copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                shutil.copy2(s, d)

def packall():
    text_types = [SysType, StoryType, CharaType]
    img_types = [SysType, StoryType]
    for t in text_types: 
        pack_dat(t)
        dat_output_dir = eval("{}_dat_output_dir".format(t))
        copytree(os.path.join(dat_output_dir, data_dir), os.path.join(all_output_dir, data_dir))
    for t in img_types:
        pack_txp(t)
        img_output_dir = eval("{}_img_output_dir".format(t))
        copytree(os.path.join(img_output_dir, data_dir), os.path.join(all_output_dir, data_dir))
    print("[Pack]: All is Done.")
    
def unpackall():
    text_types = [SysType, StoryType, CharaType]
    img_types = [SysType, StoryType]
    for t in text_types: unpack_dat(t)
    for t in img_types: unpack_txp(t)
    print("[Unpack]: All is Done.")
    
if __name__ == "__main__":
    pack_txp(SysType)