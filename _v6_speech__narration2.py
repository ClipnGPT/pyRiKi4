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
    print('narration2:init')
    print('narration2:start')
    print('narration2:proc')
    print('')



    files = glob.glob('narration/mp3/*.mp3')
    files.sort()

    for file in files:
        file = file.replace('\\', '/')
        fileId = file.replace('narration/mp3/', '')
        fileId = fileId.replace('.tts', '')

        if (True):
            print(fileId)

            f1 = file
            f2 = 'narration/wav/' + fileId[:-4] + '.wav'
            try:
                sox = subprocess.Popen(['sox', '-q', f1, '-r', '16000', '-b', '16', '-c', '1', f2, ], \
                      shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                sox.wait()
                sox.terminate()
                sox = None
            except Exception as e:
                pass

            txt = ''
            file2 = 'narration/tts/' + fileId[:-4] + '.txt'

            if (os.path.exists(file2)):
                try:
                    rt = codecs.open(file2, 'r', 'utf-8')
                    for t in rt:
                        txt = (txt + ' ' + str(t)).strip()
                    rt.close
                    rt = None
                except Exception as e:
                    rt = None

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

                f1 = 'narration/tts/' + fileId[:-4] + '.txt'
                f2 = 'narration/tts/' + fileId[:-4] + '.[' + f + '].txt'
                try:
                    os.rename(f1, f2)
                except Exception as e:
                    pass

                #f1 = 'narration/mp3/' + fileId[:-4] + '.tts.mp3'
                f1 = file
                f2 = 'narration/mp3/' + fileId[:-4] + '.[' + f + '].mp3'
                try:
                    os.rename(f1, f2)
                except Exception as e:
                    pass

                f1 = 'narration/wav/' + fileId[:-4] + '.wav'
                f2 = 'narration/wav/' + fileId[:-4] + '.[' + f + '].wav'
                try:
                    os.rename(f1, f2)
                except Exception as e:
                    pass



    print('')
    print('narration2:terminate')
    print('narration2:bye!')



