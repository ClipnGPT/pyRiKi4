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



# google 音声認識
import speech_api_google     as google_api
import speech_api_google_key as google_key



if __name__ == '__main__':

    inpLang = 'ja'
    inpWave = 'temp/temp_inpWave.wav'
    inpText = 'temp/temp_inpText.txt'

    if (len(sys.argv) >= 2):
        inpLang = sys.argv[1]
    if (len(sys.argv) >= 3):
        inpWave = sys.argv[2]
    if (len(sys.argv) >= 4):
        inpText = sys.argv[3]



    print('')
    print('speech_input_google.py')
    print(' 1)inpLang = ' + str(inpLang))
    print(' 2)inpWave = ' + str(inpWave))
    print(' 3)inpText = ' + str(inpText))



    if os.path.exists(inpText):
        os.remove(inpText)



    resText = ''
    if (os.path.exists(inpWave)):

        #try:

        googleAPI = google_api.SpeechAPI()
        res = googleAPI.authenticate('stt', google_key.getkey('stt'), )
        if (res == True):

            resText, api = googleAPI.recognize(inpWave=inpWave, inpLang=inpLang)

        #except Exception as e:
        #    pass



    print(' ' + resText)
    if (resText != ''):
        w = codecs.open(inpText, 'w', 'shift_jis')
        w.write(resText)
        w.close()
        w = None



