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



# google 機械翻訳
import speech_api_google     as google_api
import speech_api_google_key as google_key



if __name__ == '__main__':

    inpLang = 'ja'
    outLang = 'en'
    inpFile = 'temp/temp_inpText.txt'
    outFile = 'temp/temp_speech.txt'

    if (len(sys.argv) >= 2):
        inpLang = sys.argv[1]
    if (len(sys.argv) >= 3):
        outLang = sys.argv[2]
    if (len(sys.argv) >= 4):
        inpFile = sys.argv[3]
    if (len(sys.argv) >= 5):
        outFile = sys.argv[4]



    print('')
    print('speech_translate_google.py')
    print(' 1)inpLang = ' + str(inpLang))
    print(' 2)outLang = ' + str(outLang))
    print(' 3)inpFile = ' + str(inpFile))
    print(' 4)outFile = ' + str(outFile))



    if (os.path.exists(outFile)):
        os.remove(outFile)



    inpText = ''
    if (os.path.exists(inpFile)):
        rt = codecs.open(inpFile, 'r', 'shift_jis')
        for t in rt:
            inpText = (inpText + ' ' + str(t)).strip()
        rt.close
        rt = None

    outText = ''
    if (inpText != ''):

        #try:
        print(' ' + inpText)

        googleAPI = google_api.SpeechAPI()
        res = googleAPI.authenticate('tra', google_key.getkey('tra'), )
        if (res == True):

            outText, api = googleAPI.translate(inpText=inpText, inpLang=inpLang, outLang=outLang, )

        #except Exception as e:
        #print(' Error!', sys.exc_info()[0])
        #sys.exit()



    print(' ' + outText)
    if (outText != ''):
        w = codecs.open(outFile, 'w', 'shift_jis')
        w.write(outText)
        w.close()
        w = None



