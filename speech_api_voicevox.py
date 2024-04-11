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
import json
import requests
import wave



# voicevox 音声合成



class SpeechAPI:

    def __init__(self, ):
        self.system = None
        self.timeOut = 30

    def setTimeOut(self, timeOut=30, ):
        self.timeOut = timeOut

    def authenticate(self, ):
        self.system = platform.system().lower() #windows,darwin,linux
        return True

    def vocalize(self, outText='hallo', outLang='ja-JP', outGender='female', outFile='temp_voice.wav'):
        if (self.system is None):
            print('VOICEVOX: Not Authenticate Error !')

        else:
            if (os.path.exists(outFile)):
                try:
                    os.remove(outFile)
                except Exception as e:
                    pass

            #ja-JP:日本語〇

            lang = ''
            if   (outLang == 'ja') or (outLang == 'ja-JP'):
                lang = 'ja-JP'

            speaker = 20 #女性
            if (outGender == 'male'):
                speaker = 21 #男性

            if (lang != '') and (outText != '') and (outText != '!'):

                try:

                    host = 'localhost'
                    port = 50021
                    params = (
                        ('text', outText),
                        ('speaker', speaker),
                    )
                    response1 = requests.post(
                        url=f'http://{host}:{port}/audio_query',
                        params=params,
                        timeout=self.timeOut,
                    )
 
                    headers = {'Content-Type': 'application/json',}
                    response2 = requests.post(
                        url=f'http://{host}:{port}/synthesis',
                        headers=headers,
                        params=params,
                        data=json.dumps(response1.json()),
                        timeout=self.timeOut,
                    )

                    wf = wave.open(outFile, 'wb')
                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(24000)
                    wf.writeframes(response2.content)
                    wf.close()

                    if (os.path.exists(outFile)):
                        rb = open(outFile, 'rb')
                        size = sys.getsizeof(rb.read())
                        if (size <= 44):
                            os.remove(outFile)
                        else:
                            return outText, 'voicevox'
                except Exception as e:
                    pass

        return '', ''



if __name__ == '__main__':

        #voicevoxAPI = voicevox_api.SpeechAPI()
        voicevoxAPI = SpeechAPI()

        res = voicevoxAPI.authenticate()
        if (res == True):

            text = 'こんにちは'
            file = 'temp_voice.wav'

            res, api = voicevoxAPI.vocalize(outText=text, outLang='ja', outFile=file)
            print('vocalize:', res, '(' + api + ')' )

            sox = subprocess.Popen(['sox', file, '-d', '-q'], )
            sox.wait()
            sox.terminate()
            sox = None


