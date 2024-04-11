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

import cv2



# 共通ルーチン
import  _v6__qGuide
qGuide= _v6__qGuide.qGuide_class()



if __name__ == '__main__':

    # パラメータ
    imgPath = '_icons/'
    imgFile = 'detect_speech.png'
    inpText = ''

    if (len(sys.argv) >= 2):
        wavPath = str(sys.argv[1])
        if (wavPath[:-1] != '/'):
            wavPath += '/'
    if (len(sys.argv) >= 3):
        wavFile  = str(sys.argv[2])
    if (len(sys.argv) >= 4):
        inpText  = str(sys.argv[3])

    # 画像表示
    imgFile = imgPath + imgFile
    img = cv2.imread(imgFile)
    qGuide.init(screen=0, panel='auto', title='detect_speech', image=img,)
    qGuide.open()

    # メッセージ
    time.sleep(0.25)
    if (inpText == ''):
        inpText = '!'
    qGuide.setMessage(txt=inpText, )

    # 待機
    chkTime = time.time()
    while ((time.time() - chkTime) < 3):
        event, values = qGuide.read()
        if event in (None, 'Exit'):
            break

    # 画像消去
    qGuide.close()
    qGuide.terminate()


