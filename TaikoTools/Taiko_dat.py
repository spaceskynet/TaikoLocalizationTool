#!/usr/bin/python3
# -*- coding:utf-8 -*-
# For Python 3.6+
import math, struct
from TaikoTools.consts import *

def ceil_len(len):
    return math.ceil((len) / 16) * 16

class SysDatFile(object):
    def __init__(self, file_name = ""):
        self.bin_text = None
        self.contents = {}
        self.file_name = file_name
        pass
    def dat_read(self):
        f = open(self.file_name ,"rb")
        bin_text = f.read()
        f.close()
        bin_text_len = len(bin_text)
        self.text_count, self.file_header = struct.unpack("<I8s", bin_text[:0xC])
        if self.file_header != b'\x10\x00\x00\x00\x20\x00\x00\x00': raise TypeError
        title_len = bin_text[0x10:min(0x10 + TRY_RANGE, bin_text_len)].find(b'\x00')
        self.title = bin_text[0x10:0x10 + title_len]
        title_len = ceil_len(title_len + 1)
        for i in range(self.text_count):
            flag_pos, txt_pos = struct.unpack("<II",bin_text[0x10 + title_len + i * 8:0x18 + title_len + i * 8])
            #print("{}:".format(i),flag_pos, txt_pos)
            flag = bin_text[flag_pos:txt_pos].replace(b'\x00',b'')
            txt_len = bin_text[txt_pos:min(txt_pos + TRY_RANGE, bin_text_len)].find(b'\x00')
            txt = bin_text[txt_pos:txt_pos + txt_len]
            txt_len = ceil_len(txt_len + 1)
            #print(flag, txt)
            self.contents[flag] = txt
        if len(self.contents.values()) != self.text_count:
            self.text_count = len(self.contents.values())
            print("[Error]: Source file [ %s ] has the same flag! Please delete the other duplicate key! " % self.file_name)
        #print(self.text_count, self.title ,self.contents)
        pass
    
    def dat_write(self):
        f = open(self.file_name + "_tr","wb")
        bin_text = b''
        s = struct.Struct('<IIII')
        bin_text += s.pack(self.text_count, 0x10, 0x20, 0x00)
        title_len = ceil_len(len(self.title) + 1)
        s = struct.Struct('>{}s'.format(title_len))
        bin_text += s.pack(self.title)
        s = struct.Struct('<II')
        info_len = ceil_len(0x08 * self.text_count) #if dat file > 15 MB, need + 1
        bin_text_body = b''
        for (flag, content) in self.contents.items():
            flag_pos = 0x10 + title_len + info_len + len(bin_text_body)
            flag_len = ceil_len(len(flag) + 1)
            txt_pos = flag_pos + flag_len
            txt = content
            txt_len = ceil_len(len(txt) + 1)
            bin_text_body += flag + b'\x00' * (flag_len - len(flag)) # write flag
            bin_text_body += txt + b'\x00' * (txt_len - len(txt)) # write flag
            #print("{}:".format(i),flag_pos, txt_pos)
            bin_text += s.pack(flag_pos, txt_pos)           
        bin_text += b'\x00' * (info_len - 0x08 * self.text_count)
        bin_text += bin_text_body
        
        f.write(bin_text)
        #print(self.text_count, self.title ,self.contents)
        f.close()
        pass

class CharaDatFile(object):
    def __init__(self, file_name = ""):
        self.bin_text = None
        self.contents = {}
        self.file_name = file_name
        pass
    def dat_read(self):
        f = open(self.file_name ,"rb")
        bin_text = f.read()
        f.close()
        bin_text_len = len(bin_text)
        self.file_header, self.text_count = struct.unpack("<4sI", bin_text[:0x8])
        if self.file_header != b'\x10\x00\x00\x00': raise TypeError
        for i in range(self.text_count):
            flag_pos, txt_pos, feature_code = struct.unpack("<III",bin_text[0x10 + i * 12:0x1C + i * 12])
            #print("{}:".format(i),flag_pos, txt_pos)
            flag = bin_text[flag_pos:txt_pos].replace(b'\x00',b'')
            txt_len = bin_text[txt_pos:min(txt_pos + TRY_RANGE, bin_text_len)].find(b'\x00')
            txt = bin_text[txt_pos:txt_pos + txt_len]
            txt_len = ceil_len(txt_len + 1)
            #print(flag, txt)
            self.contents[flag]= {'txt':txt, 'feature_code':feature_code}
        if len(self.contents.values()) != self.text_count:
            self.text_count = len(self.contents.values())
            print("[Error]: Source file [ %s ] has the same flag! Please delete the other duplicate key! " % self.file_name)
        #print(self.text_count, self.title ,self.contents)
        pass
    
    def dat_write(self):
        f = open(self.file_name + "_tr","wb")
        bin_text = b'\x10\x00\x00\x00' # write file_header
        bin_text += struct.pack("<III", self.text_count, 0x00, 0x00) # write text_count
        info_len = ceil_len(self.text_count * 12) # tail has more 00, don't need to + 1
        bin_text_body = b''
        s = struct.Struct('<III')
        for (flag, content) in self.contents.items():
            flag_pos = 0x10 + info_len + len(bin_text_body)
            flag_len = ceil_len(len(flag) + 1)
            txt_pos = flag_pos + flag_len
            txt = content['txt']
            txt_len = ceil_len(len(txt) + 1)
            bin_text_body += flag + b'\x00' * (flag_len - len(flag)) # write flag
            bin_text_body += txt + b'\x00' * (txt_len - len(txt)) # write flag
            #print("{}:".format(i),flag_pos, txt_pos)
            bin_text += s.pack(flag_pos, txt_pos, content['feature_code'])           
        bin_text += b'\x00' * (info_len - 12 * self.text_count)
        bin_text += bin_text_body
        
        f.write(bin_text)
        #print(self.text_count, self.title ,self.contents)
        f.close()
        pass
        
class StoryDatFile(object):
    def __init__(self, file_name = ""):
        self.bin_text = None
        self.contents = {}
        self.file_name = file_name
        pass
        
    def txt_replace(self, txt):
        for STRING in REPLACE_STRING:
            txt = txt.replace(*STRING)
        return txt
    
    def txt_insert(self, txt, pos, target):
        return txt[:pos]+ target + txt[pos:]
    
    def dat_read(self):
        f = open(self.file_name ,"rb")
        bin_text = f.read()
        f.close()
        bin_text_len = len(bin_text)
        self.file_header, self.text_count = struct.unpack("<4sI", bin_text[:0x8])
        if self.file_header != b'\x10\x00\x00\x00': raise TypeError
        for i in range(self.text_count):
            flag_pos, txt_info_pos, name_cnt = struct.unpack("<III",bin_text[0x10 + i * 12:0x1C + i * 12])
            #print("{}:".format(i),flag_pos, txt_info_pos)
            flag = bin_text[flag_pos:txt_info_pos].replace(b'\x00',b'')
            txt_pos, name_pos, phonetic_cnt, phonetic_info_pos = struct.unpack("<IIII", bin_text[txt_info_pos:txt_info_pos + 0x10])
            txt = bin_text[txt_pos:name_pos].replace(b'\x00',b'')
            name = bin_text[name_pos:phonetic_info_pos].replace(b'\x00',b'')
            self.contents[flag] = {}
            self.contents[flag]['phonetic'] = []
            self.contents[flag]['name'] = (name, name_cnt)
            #print("Read:", txt)
            for j in range(phonetic_cnt):
                phonetic_single_pos, phonetic_Y_pos, phonetic_X_pos, phonetic_raw_txt_len, phonetic_row = struct.unpack("<IIIII", bin_text[phonetic_info_pos + j * 20: phonetic_info_pos + (j + 1) * 20])
                phonetic_raw_txt_pos = txt.find(b'\x1B\x02%b' % (struct.pack("<b",j + 1))) - phonetic_raw_txt_len
                phonetic_raw_txt = txt[phonetic_raw_txt_pos:phonetic_raw_txt_pos + phonetic_raw_txt_len]
                txt = txt.replace(b'\x1B\x02%b' % (struct.pack("<b",j + 1)),b'')
                phonetic_txt_len = bin_text[phonetic_single_pos:min(phonetic_single_pos + TRY_RANGE, bin_text_len)].find(b'\x00')
                phonetic_txt = bin_text[phonetic_single_pos:phonetic_single_pos + phonetic_txt_len]
                self.contents[flag]['phonetic'].append((
                                                        (phonetic_Y_pos, phonetic_X_pos, phonetic_row), 
                                                        phonetic_txt, 
                                                        phonetic_raw_txt,
                                                        phonetic_raw_txt_pos
                                                    ))

            txt = txt.decode(encoding = 'utf-8')
            txt_newlines_pos = []
            if IS_REPLACE_ROW_FLAG:
                txt_newline_pos = txt.find('\n') 
                while txt_newline_pos != -1:
                    txt = txt.replace('\n','')
                    txt_newlines_pos.append(txt_newline_pos)
                    txt_newline_pos = txt.find('\n')
            if IS_REPLACE_STRING: txt = self.txt_replace(txt) # to ensure the correct rate of translate engine
            txt_formated = txt.encode()
            
            txt = []
            txt_formated = txt_formated.split(b'\x1b\x01')
            for i in range(len(txt_formated)):
                if b'\x1b\x01' + txt_formated[i][:1] == COLOR_BLUE[0]: 
                    txt.append([txt_formated[i][1:], COLOR_BLUE])
                    txt_formated[i + 1] = txt_formated[i + 1][1:]
                elif b'\x1b\x01' + txt_formated[i][:1] == COLOR_UNKNOWN[0]: 
                    txt.append([txt_formated[i][1:], COLOR_UNKNOWN])
                    txt_formated[i + 1] = txt_formated[i + 1][1:]
                elif txt_formated[i] != b'': txt.append([txt_formated[i], COLOR_NULL])
            
            self.contents[flag]['txt'] = [txt, txt_newlines_pos]
            #print(self.contents[flag]['txt'])
        #print(self.text_count, self.contents)
        if len(self.contents.values()) != self.text_count:
            self.text_count = len(self.contents.values())
            print("Source file [ %s ] has the same flag! Please delete the other duplicate key! " % self.file_name)
        pass
    
    def dat_write(self):
        f = open(self.file_name + "_tr","wb")
        bin_text = b'\x10\x00\x00\x00' # write file_header
        bin_text += struct.pack("<III", self.text_count, 0x00, 0x00) # write text_count
        info_len = ceil_len(self.text_count * 12) # tail has more 00, don't need to + 1
        bin_text_body = b''
        for (flag, content) in self.contents.items():
            flag_pos, (name, name_cnt) = 0x10 + info_len + len(bin_text_body), content['name']
            flag_len = ceil_len(len(flag) + 1)
            txt_info_pos = flag_pos + flag_len
            txt_info_len = 0x10
            #print(flag_pos, flag_len, txt_info_pos)
            bin_text += struct.pack("<III", flag_pos, txt_info_pos, name_cnt) # write info
            bin_text_body += flag + b'\x00' * (flag_len - len(flag)) # write flag
            #print(content['txt'])
            
            txt, txt_newlines_pos = content['txt']
            txt_formated = b''
            #print(txt)
            for (txt_raw , txt_color) in txt:
                #print(txt_raw , txt_color)
                txt_formated += txt_color[0] + txt_raw + txt_color[1]
            
            txt = txt_formated.decode(encoding = 'utf-8')
            if IS_REPLACE_ROW_FLAG:
                for i in range(len(txt_newlines_pos)): txt_newlines_pos[i] = (i + 1) * MAX_ROW_CHAR #
                for i in range(len(txt_newlines_pos)):
                    if txt_newlines_pos[i] + i >= len(txt): break
                    is_located_in_color_flag = txt[txt_newlines_pos[i] + i - 3:txt_newlines_pos[i] + i + 2].find(b'\x1b\x01'.decode(encoding = 'utf-8'))
                    if is_located_in_color_flag != -1: txt_newlines_pos[i] += is_located_in_color_flag 
                    txt = self.txt_insert(txt, txt_newlines_pos[i] + i, '\n')
            txt = txt.encode()
            
            phonetic_cnt = len(content['phonetic'])
            name_len = ceil_len(len(name) + 1)
            phonetic_info_len = ceil_len(20 * phonetic_cnt) # Because number of rows 1 ~ 3, tail has more 00, don't need to + 1
            for j in range(phonetic_cnt):
                phonetic_raw_txt, phonetic_raw_txt_pos = content['phonetic'][j][2:]
                phonetic_raw_txt_pos += j * 3 # 
                phonetic_raw_txt_len = len(phonetic_raw_txt)
                txt = self.txt_insert(txt, phonetic_raw_txt_pos + phonetic_raw_txt_len, b'\x1B\x02%b' % (struct.pack("<b",j + 1)))
            #print("Write:", txt)
            txt_len = ceil_len(len(txt) + 1)
            txt_pos = txt_info_pos + txt_info_len
            name_pos = txt_pos + txt_len
            phonetic_info_pos = name_pos + name_len
            bin_text_body += struct.pack("<IIII", txt_pos, name_pos, phonetic_cnt, phonetic_info_pos) # write txt_info
            bin_text_body += txt + b'\x00' * (txt_len - len(txt)) # write txt
            bin_text_body += name + b'\x00' * (name_len - len(name)) # write name
            bin_text_body_phonetic = b''
            for j in range(phonetic_cnt):
                (phonetic_Y_pos, phonetic_X_pos, phonetic_row), phonetic_txt, phonetic_raw_txt = content['phonetic'][j][:3]
                phonetic_raw_txt_len = len(phonetic_raw_txt)
                phonetic_single_pos = phonetic_info_pos + phonetic_info_len + len(bin_text_body_phonetic)
                bin_text_body += struct.pack("<IIIII", phonetic_single_pos, phonetic_Y_pos, phonetic_X_pos, phonetic_raw_txt_len, phonetic_row) # write phonetic_info
                phonetic_txt_len = ceil_len(len(phonetic_txt) + 1)
                bin_text_body_phonetic += phonetic_txt + b'\x00' * (phonetic_txt_len - len(phonetic_txt)) # write phonetic_txt
            bin_text_body += b'\x00' * (phonetic_info_len - 20 * phonetic_cnt)
            bin_text_body += bin_text_body_phonetic
        bin_text += b'\x00' * (info_len - self.text_count * 12)
        bin_text += bin_text_body
        f.write(bin_text)
        f.close()
        #print(self.text_count, self.contents)
        pass

if __name__ == "__main__":
    CharaDat = CharaDatFile("CharaName.dat")
    CharaDat.dat_read()
    for (flag, content) in CharaDat.contents.items():
        print(flag.decode(), content['txt'].decode())
    CharaDat.dat_write()
    