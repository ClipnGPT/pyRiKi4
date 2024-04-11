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

import platform    # platform.system().lower() #windows,darwin,linux



# gtts 音声合成
from gtts import gTTS



class SpeechAPI:

    def __init__(self, ):
        self.system = None
        self.timeOut = 10
    
    def setTimeOut(self, timeOut=10, ):
        self.timeOut = timeOut

    def authenticate(self, ):
        self.system = platform.system().lower() #windows,darwin,linux
        return True

    def vocalize(self, outText='hallo', outLang='en-US', outGender='female', outFile='temp_voice.mp3', api='free', ):
        if (self.system is None):
            print('GTTS: Not Authenticate Error !')

        else:
            if (os.path.exists(outFile)):
                try:
                    os.remove(outFile)
                except Exception as e:
                    pass

            if (outText != '') and (outText != '!'):

                try:

                    # Google
                    tts = gTTS(text=outText, lang=outLang, slow=False)
                    tts.save(outFile)
                    return outText, 'free'

                except Exception as e:
                    pass

        return '', ''



if __name__ == '__main__':

        #gttsAPI = gtts_api.SpeechAPI()
        gttsAPI = SpeechAPI()

        res = gttsAPI.authenticate()
        if (res == True):

            text = 'Hallo'
            file = 'temp_voice.mp3'

            res, api = gttsAPI.vocalize(outText=text, outLang='en', outFile=file)
            print('vocalize:', res, '(' + api + ')' )

            sox = subprocess.Popen(['sox', file, '-d', '-q'], )
            sox.wait()
            sox.terminate()
            sox = None

            text = 'こんにちは'
            file = 'temp_voice.mp3'

            res, api = gttsAPI.vocalize(outText=text, outLang='ja', outFile=file)
            print('vocalize:', res, '(' + api + ')' )

            sox = subprocess.Popen(['sox', file, '-d', '-q'], )
            sox.wait()
            sox.terminate()
            sox = None


