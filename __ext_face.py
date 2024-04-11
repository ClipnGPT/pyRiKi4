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
import subprocess


# 共通ルーチン
import  _v6__qGuide
qGuide= _v6__qGuide.qGuide_class()

qPath_sounds = '_sounds/'
def guideSound(filename=None, sync=True):
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



if __name__ == '__main__':

    # パラメータ
    imgPath = '_icons/'
    imgFile = 'detect_face.png'
    parm3   = 'null'

    if (len(sys.argv) >= 2):
        imgPath = str(sys.argv[1])
        if (imgPath[:-1] != '/'):
            imgPath += '/'
    if (len(sys.argv) >= 3):
        imgFile  = str(sys.argv[2])
    if (len(sys.argv) >= 4):
        parm3    = str(sys.argv[3])

    # 全画面表示中でなければ認識結果表示
    #if (True):
    if (os.path.exists('temp/_work/busy_dev_display.txt')):


        # 画像表示
        imgFile = imgPath + imgFile
        img = cv2.imread(imgFile)
        qGuide.init(screen=0, panel='auto', title='detect_face', image=img,)
        qGuide.open()

        # メッセージ
        time.sleep(0.25)
        qGuide.setMessage(txt='detect', )

        # 待機
        chkTime = time.time()
        while ((time.time() - chkTime) < 5):
            event, values = qGuide.read()
            if event in (None, 'Exit'):
                break

        # 画像消去
        qGuide.close()
        qGuide.terminate()

    # 以外は何もしない
    else:
        # 待機
        time.sleep(5.00)


