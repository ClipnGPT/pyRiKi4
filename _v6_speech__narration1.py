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
    print('narration1:init')
    print('narration1:start')
    print('narration1:proc')
    print('')



    # 入力ファイル
    inpFile = 'narration/1.入力ファイル_sjis.txt'
    if (os.path.exists(inpFile)):

        nowTime=datetime.datetime.now()
        stamp=nowTime.strftime('%Y%m%d.%H%M%S')
        seq = 0

        rt = codecs.open(inpFile, 'r', 'shift_jis')
        for t in rt:
            txt = str(t).strip()
            if (txt != '' and txt != '!'):

                print(txt)



                seq += 1
                nnnn = '{:04}'.format(seq)

                file = 'narration/tts/' + stamp + '.narration.' + nnnn + '.txt'

                try:
                    w = codecs.open(file, 'w', 'utf-8')
                    w.write(txt + '\r')
                    w.close
                    w = None
                except Exception as e:
                    w = None



        rt.close
        rt = None



    print('')
    print('narration1:terminate')
    print('narration1:bye!')


