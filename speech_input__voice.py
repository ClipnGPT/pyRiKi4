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

import subprocess

import speech_recognition as sr
import wave



if __name__ == '__main__':

    micDev  = 0
    inpWave = 'temp/temp_inpWave.wav'
    if (len(sys.argv) >= 2):
        micDev  = sys.argv[1]
    if (len(sys.argv) >= 3):
        inpWave = sys.argv[2]



    print('')
    print('speech_input__voice.py')
    print(' 1)micDev  = ' + str(micDev ))
    print(' 2)inpWave = ' + str(inpWave))



    if os.path.exists(inpWave):
        os.remove(inpWave)



    srr = sr.Recognizer()
    with sr.Microphone(int(micDev)) as source:
        srr.dynamic_energy_threshold = True
        srr.adjust_for_ambient_noise(source, duration=5)

        datasize=0
        while datasize<50000 or datasize>300000:
            print(' listning...')
            try:
                speech = srr.listen(source, timeout=15, phrase_time_limit=15)
                data    =speech.get_wav_data(16000,2)
                datasize=sys.getsizeof(data)
            except Exception as e:
                srr.dynamic_energy_threshold = True
                srr.adjust_for_ambient_noise(source, duration=5)
                datasize=0
            if datasize<50000 or datasize>300000:
                print(' ng! ')

        print(' accept', datasize, 'byte')



        wb = open(inpWave, 'wb')
        wb.write(data)
        wb.close
        wb = None



