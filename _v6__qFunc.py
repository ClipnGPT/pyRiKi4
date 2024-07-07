#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# COPYRIGHT (C) 2014-2024 Mitsuo KONDOU.
# This software is released under the MIT License.
# https://github.com/konsan1101
# Thank you for keeping the rules.
# ------------------------------------------------



import sys
import os
import time
import datetime
import codecs
import glob

import json

import subprocess

import psutil
import shutil

import unicodedata

import socket
qHOSTNAME = socket.gethostname().lower()



qPath_sounds    = '_sounds/'
qPath_icons     = '_icons/'
qPath_fonts     = '_fonts/'



class qFunc_class:

    def __init__(self, ):
        self.kans  = '〇一二三四五六七八九'
        self.tais1 = '千百十'
        self.tais2 = '京兆億万'
        self.suuji = {'〇', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十', \
                      '百', '千', '万', '億', '兆', \
                      '０', '１', '２', '３', '４', '５', '６', '７', '８', '９', \
                      '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
    
    def __del__(self, ):
        pass
                
    def init(self, ):
        return True

    def setNice(self, nice, ):
        try:
            p = psutil.Process()
            if   (nice == 'high'): # 優先度: 高
                p.nice(psutil.HIGH_PRIORITY_CLASS)
            elif (nice == 'above'): # 優先度: 通常以上
                p.nice(psutil.ABOVE_NORMAL_PRIORITY_CLASS)
            elif (nice == 'normal'): # 優先度: 通常
                p.nice(psutil.NORMAL_PRIORITY_CLASS)
            elif (nice == 'below'): # 優先度: 通常以下
                p.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
            elif (nice == 'idol'): # 優先度: 低
                p.nice(psutil.IDLE_PRIORITY_CLASS)
            else: # 優先度: 通常
                p.nice(psutil.NORMAL_PRIORITY_CLASS)
        except:
            pass

    def getNice(self, ):
        try:
            p = psutil.Process()
            nice = p.nice()
            if   (nice == psutil.HIGH_PRIORITY_CLASS): # 優先度: 高
                return 'high'
            elif (nice == psutil.ABOVE_NORMAL_PRIORITY_CLASS): # 優先度: 通常以上
                return 'above'
            elif (nice == psutil.NORMAL_PRIORITY_CLASS): # 優先度: 通常
                return 'normal'
            elif (nice == psutil.BELOW_NORMAL_PRIORITY_CLASS): # 優先度: 通常以下
                return 'below'
            elif (nice == psutil.IDLE_PRIORITY_CLASS): # 優先度: 低
                return 'idol'
            else: # 優先度: 通常
                pass
        except:
            pass
        return 'normal'

    def getJson(self, json_path='_config/', json_file='test_key.json', ):
        json_dic = {}
        try:
            with codecs.open(json_path + json_file, 'r', 'utf-8') as r:
                json_dic = json.load(r)
            if (json_dic != {}):
                return True, json_dic
        except Exception as e:
            print('getJson error! ' + json_path + json_file)
        return False, {}

    def putJson(self, json_path='_config/', json_file='test_key.json', json_dic={}, ):
        try:
            w = codecs.open(json_path + json_file, 'w', 'utf-8')
            w.write(json.dumps(json_dic, indent=4, ensure_ascii=False, ))
            w.close()
            return True
        except Exception as e:
            print('putJson error! ' + json_path + json_file) 
        return False

    def makeDirs(self, ppath, remove=False, ):
        try:
            if (len(ppath) > 0):
                path=ppath.replace('\\', '/')
                if (path[-1:] != '/'):
                    path += '/'
                if (not os.path.isdir(path[:-1])):
                    os.makedirs(path[:-1])
                else:
                    if (remove == True):
                        try:
                            shutil.rmtree(path, ignore_errors=True, )
                        except Exception as e:
                            pass
                    elif (str(remove).isdigit()):
                        files = glob.glob(path + '*')
                        for f in files:
                            try:
                                nowTime   = datetime.datetime.now()
                                fileStamp = os.path.getmtime(f)
                                fileTime  = datetime.datetime.fromtimestamp(fileStamp)
                                td = nowTime - fileTime
                                if (td.days >= int(remove)):
                                    self.remove(f)
                            except Exception as e:
                                pass

        except Exception as e:
            pass
        return True

    def kill(self, name, ):
        if (os.name == 'nt'):
            try:
                kill = subprocess.Popen(['taskkill', '/im', name + '.exe', '/f', ], \
                       shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                kill.wait()
                kill.terminate()
                kill = None
                return True
            except Exception as e:
                pass
        else:
            try:
                kill = subprocess.Popen(['pkill', '-9', '-f', name, ], \
                       shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                kill.wait()
                kill.terminate()
                kill = None
                return True
            except Exception as e:
                pass
        return False

    def kill_pid(self, pid, ):
        if (os.name == 'nt'):
            try:
                kill = subprocess.Popen(['taskkill', '/pid', str(pid), '/f', ], \
                       shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                kill.wait()
                kill.terminate()
                kill = None
                return True
            except Exception as e:
                pass
        else:
            try:
                kill = subprocess.Popen(['pkill', '-9', '-P', str(pid), ], \
                       shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                kill.wait()
                kill.terminate()
                kill = None
                return True
            except Exception as e:
                pass
        return False

    def remove(self, filename, maxWait=1, ):
        if (not os.path.exists(filename)):
            return True

        if (maxWait == 0):
            try:
                os.remove(filename) 
                return True
            except Exception as e:
                return False
        else:
            chktime = time.time()
            while (os.path.exists(filename)) and ((time.time() - chktime) <= maxWait):
                try:
                    os.remove(filename)
                    return True
                except Exception as e:
                    pass
                time.sleep(0.10)

            if (not os.path.exists(filename)):
                return True
            else:
                return False

    def copy(self, fromFile, toFile, ):
        try:
            shutil.copy2(fromFile, toFile)
            return True
        except Exception as e:
            return False

    def txtsWrite(self, filename, txts=[''], encoding='utf-8', exclusive=False, mode='w', ):
        if (exclusive == False):
            try:
                w = codecs.open(filename, mode, encoding)
                for txt in txts:
                    if (encoding != 'shift_jis'):
                        w.write(txt + '\n')
                    else:
                        w.write(txt + '\r\n')
                w.close()
                w = None
                return True
            except Exception as e:
                w = None
                return False
        else:
            res = self.remove(filename, )
            if (res == False):
                return False
            else:
                f2 = filename[:-4] + '.txtsWrite.tmp'
                res = self.remove(f2, )
                if (res == False):
                    return False
                else:
                    try:
                        w = codecs.open(f2, mode, encoding)
                        for txt in txts:
                            if (encoding != 'shift_jis'):
                                w.write(txt + '\n')
                            else:
                                w.write(txt + '\r\n')
                        w.close()
                        w = None
                        os.rename(f2, filename)
                        return True
                    except Exception as e:
                        w = None
                        return False

    def txtsRead(self, filename, encoding='utf-8', exclusive=False, ):
        if (not os.path.exists(filename)):
            return False, ''

        encoding2 = encoding
        if (encoding2 == 'utf-8'):
            encoding2 =  'utf-8-sig'

        if (exclusive == False):
            try:
                txts = []
                txt  = ''
                r = codecs.open(filename, 'r', encoding2)
                for t in r:
                    t = t.replace('\n', '')
                    t = t.replace('\r', '')
                    txt  = (txt + ' ' + str(t)).strip()
                    txts.append(t)
                r.close
                r = None
                return txts, txt
            except Exception as e:
                r = None
                return False, ''
        else:
            f2 = filename[:-4] + '.txtsRead.tmp'
            res = self.remove(f2, )
            if (res == False):
                return False, ''
            else:
                try:
                    os.rename(filename, f2)
                    txts = []
                    txt  = ''
                    r = codecs.open(f2, 'r', encoding2)
                    for t in r:
                        t = t.replace('\n', '')
                        t = t.replace('\r', '')
                        txt = (txt + ' ' + str(t)).strip()
                        txts.append(t)
                    r.close
                    r = None
                    self.remove(f2, )
                    return txts, txt
                except Exception as e:
                    r = None
                    return False, ''

    def statusSet(self, filename='', Flag=True, txt='_on_'):
        if (Flag == True):
            chktime = time.time()
            while (not os.path.exists(filename)) and ((time.time() - chktime) < 1):
                try:
                    w = open(filename, 'w')
                    w.write(txt)
                    w.close()
                    w = None
                    return True
                except Exception as e:
                    w = None
                time.sleep(0.10)
        else:
            chktime = time.time()
            while (os.path.exists(filename)) and ((time.time() - chktime) < 1):
                try:
                    os.remove(filename, )
                    return True
                except Exception as e:
                    pass
                time.sleep(0.10)
        return False

    def statusCheck(self, filename='', ):
        if (os.path.exists(filename)):
            return True
        else:
            return False

    def statusWait_false(self, filename, falseWait=1, ):
        if (falseWait != 0):
            chktime = time.time()
            while (os.path.exists(filename)) and ((time.time() - chktime) < falseWait):
                time.sleep(0.10)
        return self.statusCheck(filename)

    def txtFilePath(self, txt='',):
        if (txt == ''):
            return False
        chk = txt.replace('\\','/')
        if (os.path.isfile(chk)) \
        or (os.path.isdir(chk)):
            return chk
        return False

    def txt2filetxt(self, txt='', ):
        ftxt = txt.replace(' ','_')
        ftxt = ftxt.replace('　','_')
        ftxt = ftxt.replace('、','_')
        ftxt = ftxt.replace('。','_')
        ftxt = ftxt.replace('"','_')
        ftxt = ftxt.replace('$','_')
        ftxt = ftxt.replace('%','_')
        ftxt = ftxt.replace('&','_')
        ftxt = ftxt.replace("'",'_')
        ftxt = ftxt.replace('\\','_')
        ftxt = ftxt.replace('|','_')
        ftxt = ftxt.replace('*','_')
        ftxt = ftxt.replace('/','_')
        ftxt = ftxt.replace('?','_')
        ftxt = ftxt.replace(':',',')
        ftxt = ftxt.replace('<','_')
        ftxt = ftxt.replace('>','_')
        return ftxt

    def url2filepath(self, txt='', ):
        # EDGE
        s = txt.find('プロファイル 1 - Microsoft')
        if (s >= 0):
            txt = txt[:s] + 'MicrosoftEdge'

        # 前後逆転
        s = txt.find(' - ')
        if (s < 0):
            ftxt = txt
        else:
            ftxt = txt[s+2:] + '/' + txt[:s]

        # HTTP
        ftxt = ftxt.replace('https://','')
        ftxt = ftxt.replace('http://','')
        ftxt = ftxt.replace('//','/')
        ftxt = ftxt.replace('/#','/')
        s = ftxt.find('?')
        if (s >= 0):
            ftxt = ftxt[:s]
        s = ftxt.find('#')
        if (s >= 0):
            ftxt = ftxt[:s]

        ftxt = ftxt.replace(' ','')
        ftxt = ftxt.replace('　','_')
        ftxt = ftxt.replace('、','.')
        ftxt = ftxt.replace('。','.')
        ftxt = ftxt.replace('"','')
        ftxt = ftxt.replace('$','_')
        ftxt = ftxt.replace('%','_')
        ftxt = ftxt.replace('&','_')
        ftxt = ftxt.replace("'",'')
        ftxt = ftxt.replace('\\','_')
        ftxt = ftxt.replace('|','_')
        ftxt = ftxt.replace('*','_')
        ftxt = ftxt.replace('?','_')
        ftxt = ftxt.replace(':',',')
        ftxt = ftxt.replace('<','_')
        ftxt = ftxt.replace('>','_')
        ftxt = ftxt.replace('(','')
        ftxt = ftxt.replace(')','')
        ftxt = ftxt.replace('.','_')
        return ftxt



    def in_japanese(self, txt=''):
        t = txt.replace('\r', '')
        t = t.replace('\n', '')
        try:
            for s in t:
                name = unicodedata.name(s) 
                if ('CJK UNIFIED' in name) \
                or ('HIRAGANA' in name) \
                or ('KATAKANA' in name):
                    return True
        except Exception as e:
            pass
        return False



    # 関数(1)_漢数字（例：二三五六〇一）を単純変換する関数
    def kan2num(self, text):
        for i, tmp in enumerate(self.kans):
            text = text.replace(tmp, str(i)) # replaceメソッドで置換
        return text

    # 関数(2)_4桁までの漢数字（例：六千五百八）を数値変換する関数
    def kans2numf(self, text):
        ans = 0 # 初期値（計算結果を加算していく）
        poss = 0 # スタート位置
        for i, tmp in enumerate(self.tais1):
            pos = text.find(tmp) # 大数（千百十）の位置を順次特定
            if pos == -1: # 対象となる大数（千百十）が無い場合
                block = 0
                pos = poss - 1
            elif  pos == poss: # '二千百'のように'千'と'百'の間に数字がない場合
                block = 1
            else:
                block = int(self.kan2num(text[poss:pos])) # 'possとposの間の漢数字を数値に変換
            ans += block * (10 ** (len(self.tais1) - i))
            poss = pos + 1 # possをposの次の位置に設定
        if poss != len(text): # 一の位の数字がある場合
            ans += int(self.kan2num(text[poss:len(text)]))
        return ans

    # 関数(3)_20桁までの漢数字（例：六兆五千百億十五万八千三十二）を数値変換する関数
    def kans2num(self, text):
        ans = 0
        poss = 0
        for i, tmp in enumerate(self.tais2):
            pos = text.find(tmp)
            if pos == -1:
                block = 0
                pos = poss - 1
            elif  pos == poss:
                block = 1
            else:
                block = self.kans2numf(text[poss:pos])
            ans += block * (10 ** (4 * (len(self.tais2) - i)))
            poss = pos + 1
        if poss != len(text):
            ans += self.kans2numf(text[poss:len(text)])
        return ans

    # 関数(4)_文字列中の漢数字を算用数字に変換する関数（カンマ表示に簡易対応）
    def strkan2num(self, text):
        ans = ''
        tmp = ''
        for chr in text:
            if chr in self.suuji or (tmp != '' and chr == ','): # 文字が数字又はカンマの場合
                tmp += chr # 数字が続く限りtmpに格納
            else: # 文字が数字でない場合
                if tmp != '': # tmpに数字が格納されている場合
                    ans += str(self.kans2num(tmp.replace(',', ''))) #算用数字に変換して連結
                    tmp = ''
                ans += chr
        if tmp != '': # 文字列の最後が数字で終わる場合の処理
            ans += str(self.kans2num(tmp.replace(',', '')))
        return ans



    def waitSec(self, sec=0, ):
        xSec = sec
        while (int(xSec) > 0):
            print('wait … ' + str(int(xSec)))
            time.sleep(1)
            xSec -= 1
        if (xSec > 0):
            time.sleep(xSec)
        return True

    def guideSound(self, filename=None, sync=True):
        playfile = filename
        if (filename == '_up'):
            playfile = qPath_sounds + '_sound_up.mp3'
        if (filename == '_ready'):
            playfile = qPath_sounds + '_sound_ready.mp3'
        if (filename == '_accept'):
            playfile = qPath_sounds + '_sound_accept.mp3'
        if (filename == '_ok'):
            playfile = qPath_sounds + '_sound_ok.mp3'
        if (filename == '_ng'):
            playfile = qPath_sounds + '_sound_ng.mp3'
        if (filename == '_down'):
            playfile = qPath_sounds + '_sound_down.mp3'
        if (filename == '_shutter'):
            playfile = qPath_sounds + '_sound_shutter.mp3'
        if (filename == '_pingpong'):
            playfile = qPath_sounds + '_sound_pingpong.mp3'

        if (os.path.exists(playfile)):

            sox = subprocess.Popen(['sox', '-q', playfile, '-d', ], \
                  shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
            if (sync == True):
                sox.wait()
                sox.terminate()
                sox = None

            return True

        return False

    def chkSelfDev(self, dev=None, ):
        if (dev is None):
            return False
        elif (dev.isdigit()):
            return True
        elif (str(dev).lower().find('localhost')  >= 0):
            return True
        elif (str(dev).lower().find(qHOSTNAME) >= 0):
            return True
        else:
            return False



if (__name__ == '__main__'):

    qFunc = qFunc_class()
    qFunc.init()

    qFunc.kill('sox')

    print(qFunc.chkSelfDev('http://localhost:...'))


    txt = '十八才'
    print(txt, qFunc.strkan2num(txt))
    txt = '二十五才'
    print(txt, qFunc.strkan2num(txt))
    txt = 'F二'
    print(txt, qFunc.strkan2num(txt))

    txt = '平成二十三年十一月二十三日に5,000円使った'
    print(txt, qFunc.strkan2num(txt))
    txt = '２０１８年１０-１２月期における日本の名目ＧＤＰは五百四十八兆七千七百二十億円、実質ＧＤＰは５３４兆３,３７０億円です'
    print(txt, qFunc.strkan2num(txt))



