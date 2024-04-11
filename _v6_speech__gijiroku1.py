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

import shutil



if __name__ == '__main__':
    print('gijiroku1:init')

    print('')
    print('gijiroku1:start')

    print('')
    print('gijiroku1:check filecount')

    files = {}

    fn = '0n'
    files[fn] = glob.glob('gijiroku/temp/wav_' + fn + '/*')
    fn = '1eq3'
    files[fn] = glob.glob('gijiroku/temp/wav_' + fn + '/*')
    fn = '1eq6'
    files[fn] = glob.glob('gijiroku/temp/wav_' + fn + '/*')
    fn = '1eq9'
    files[fn] = glob.glob('gijiroku/temp/wav_' + fn + '/*')
    fn = '2nv'
    files[fn] = glob.glob('gijiroku/temp/wav_' + fn + '/*')
    fn = '3eq3v'
    files[fn] = glob.glob('gijiroku/temp/wav_' + fn + '/*')
    fn = '3eq6v'
    files[fn] = glob.glob('gijiroku/temp/wav_' + fn + '/*')
    fn = '3eq9v'
    files[fn] = glob.glob('gijiroku/temp/wav_' + fn + '/*')

    maxfn  = ''
    maxlen = 0
    for fn in files:
        if len(files[fn]) != 0:
            print('filecount gijiwave_' + fn, '=', len(files[fn]))
            if (len(files[fn]) > maxlen and len(files[fn]) >1):
                maxfn  = fn
                maxlen = len(files[fn])

    fn = '0n'
    if (maxfn != ''):
        fn = maxfn

    if maxfn != '':
        #if maxfn == '0n':
        #    fn='1eq3'
        #if maxfn == '2nv':
        #    fn='3eq3v'
        fn='0n'

        print('')
        print('gijiroku1:proc ' + fn + ' (pass = ' + maxfn + ')')
        print('')

    #a=input('pause (press enter) > ')

    if fn != '':

        #XCOPY gijiroku\temp\wav_%fn%\*.* gijiroku\wav\*.* /Q/R/Y

        print('XCOPY',      'gijiroku/temp/wav_'+fn+'/', 'gijiroku/wav/')
        for f1 in files[fn]:
            f1 = f1.replace('\\', '/')
            f2 = f1
            f2 = f2.replace('gijiroku/temp/wav_'+fn+'/', 'gijiroku/wav/')
            #qFunc.copy(f1, f2)
            shutil.copy2(f1, f2)

        f1 = 'gijiroku/temp/temp__gijiroku16_' + fn + '.wav'
        f2 = 'gijiroku/temp/temp__gijiroku16.wav'
        print('COPY', f1, f2)
        #qFunc.copy(f1, f2)
        shutil.copy2(f1, f2)

        #sox "gijiroku/temp/temp__gijiroku16.wav"      "gijiroku/temp/temp__gijiroku16.mp3"

        #f1 = 'gijiroku/temp/temp__gijiroku16.wav'
        #f2 = 'gijiroku/temp/temp__gijiroku16.mp3'
        #print('sox', '-q', f1, f2)
        #sox = subprocess.Popen(['sox', '-q', f1, f2, ])
        #sox.wait()
        #sox.terminate()
        #sox = None

        #COPY gijiroku\temp\temp__gijilist16_%fn%.txt   gijiroku\temp\temp__gijilist16.txt

        f1 = 'gijiroku/temp/temp__gijilist16_' + fn + '.txt'
        f2 = 'gijiroku/temp/temp__gijilist16.txt'
        print('COPY', f1, f2)
        #qFunc.copy(f1, f2)
        shutil.copy2(f1, f2)



    print('')
    print('gijiroku1:terminate')

    print('gijiroku1:bye!')



