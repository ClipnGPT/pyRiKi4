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

import queue
import threading
import subprocess



if __name__ == '__main__':
    print('gijiroku2:init')
    print('gijiroku2:start')
    print('gijiroku2:proc')
    print('')



    outFile = 'gijiroku/9.結果テキスト_sjis.txt'
    if (os.path.exists(outFile)):
        os.remove(outFile)



    files = glob.glob('gijiroku/stt/*.txt')
    files.sort()

    for file in files:
        file = file.replace('\\', '/')
        fileId = file.replace('gijiroku/stt/', '')
        if (fileId[0:1] != '_'):
            print(fileId)

            txt = ''
            try:
                rt = codecs.open(file, 'r', 'utf-8')
                for t in rt:
                    txt = (txt + ' ' + str(t)).strip()
                rt.close
                rt = None
            except Exception as e:
                rt = None

            try:
                a = codecs.open(outFile, 'a', 'shift_jis')
                a.write(fileId[:-4].replace('julius.','') + ', [' + txt + ']\r\n')
                a.close()
                a = None
            except Exception as e:
                a = None

            if (txt != ''):

                f = txt.replace(' ','_')
                f = f.replace('　','_')
                f = f.replace('"','_')
                f = f.replace('$','_')
                f = f.replace('%','_')
                f = f.replace('&','_')
                f = f.replace("'",'_')
                f = f.replace('\\','_')
                f = f.replace('|','_')
                f = f.replace('*','_')
                f = f.replace('/','_')
                f = f.replace('?','_')
                f = f.replace(':',',')
                f = f.replace('<','_')
                f = f.replace('>','_')
                if (len(f)>100):
                    f = f[:100] + '…'

                f1 = 'gijiroku/mp3/' + fileId[:-4]                                   + '.mp3'
                f2 = 'gijiroku/mp3/' + fileId[:-4].replace('julius.','') + '.[' + f + '].mp3'
                try:
                    os.rename(f1, f2)
                except Exception as e:
                    pass



    print('')
    print('gijiroku2:terminate')
    print('gijiroku2:bye!')



