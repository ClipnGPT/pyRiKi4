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

from requests_toolbelt import SSLAdapter
import requests
import ssl



# hoya 音声合成
import speech_api_hoya_key as hoya_key



class SpeechAPI:

    def __init__(self, ):
        self.timeOut = 10
        self.authkey = None

    def setTimeOut(self, timeOut=10, ):
        self.timeOut = timeOut

    def authenticate(self, key):
        self.authkey = key
        if (self.authkey is not None):
            return True
        return False

    def vocalize(self, outText='hallo', outLang='en-US', outGender='female', outFile='temp_voice.wav'):
        if (self.authkey is None):
            print('HOYA: Not Authenticate Error !')

        else:
            if (os.path.exists(outFile)):
                try:
                    os.remove(outFile)
                except Exception as e:
                    pass

            lang = ''
            if   (outLang == 'ja') or (outLang == 'ja-JP'):
                lang = 'ja-JP'

            # HOYA
            url  = 'https://api.voicetext.jp/v1/tts'
            params = {
                'text': outText,
                'speaker': 'hikari',     # free! haruka,hikari,show,takeru,santa,bear
                'emotion': 'happiness',  # happiness,anger,sadness
                'emotion_level': 1,      # 1,2,3,4
                'pitch': 100,            # 50-200
                'speed': 150,            # 50-400
                'volume': 100,           # 50-200
                'format': 'wav'          # wav,ogg,aac
                }
            
            if (lang != '') and (outText != '') and (outText != '!'):

                #try:
                    ssn = requests.Session()
                    #ssn.mount(     url, SSLAdapter(ssl.PROTOCOL_TLSv1))
                    ssn.mount(     url, SSLAdapter(ssl.PROTOCOL_SSLv23))
                    res = ssn.post(url, params=params, auth=(self.authkey, ''), timeout=self.timeOut, )
                    #print(res.status_code)
                    if (res.status_code == 200):
                        wb = open(outFile, 'wb')
                        wb.write(res.content)
                        wb.close()
                        wb = None
                        return outText, 'hoya'
                #except Exception as e:
                #    pass

        return '', ''



if __name__ == '__main__':

        #hoyaAPI = hoya_api.SpeechAPI()
        hoyaAPI = SpeechAPI()

        res = hoyaAPI.authenticate(hoya_key.getkey(), )
        if (res == True):

            text = 'こんにちは'
            file = 'temp_voice.wav'

            res, api = hoyaAPI.vocalize(outText=text, outLang='ja-JP', outFile=file)
            print('vocalize:', res, '(' + api + ')' )

            sox = subprocess.Popen(['sox', file, '-d', '-q'], )
            sox.wait()
            sox.terminate()
            sox = None



