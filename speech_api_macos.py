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

import platform



# macos 音声合成



class SpeechAPI:

    def __init__(self, ):
        self.system = None

    def authenticate(self, ):
        self.system = platform.system().lower() #windows,darwin,linux
        if (self.system == 'darwin'):
            return True
        return False

    def vocalize(self, outText='hallo', outLang='en', outGender='female', outFile='temp_voice.wav'):
        if (self.system is None):
            print('MACOS: Not Authenticate Error !')

        else:
            if (os.path.exists(outFile)):
                try:
                    os.remove(outFile)
                except Exception as e:
                    pass

            file = outFile[:-4] + '.wave'
            if (os.path.exists(file)):
                try:
                    os.remove(file)
                except Exception as e:
                    pass

            #ja-JP:日本語,    en-US:英語,
            #ar-SA:アラビア語, es-ES:スペイン語, de-DE:ドイツ語
            #fr-FR:フランス語, it-IT:イタリア語, pt-PT:ポルトガル語
            #ru-RU:ロシア語,  tr-TR:トルコ語,   uk-UK:ウクライナ語×
            #zh-CN:中国語,    ko-KR:韓国語

            voice = ''
            rate  = ''
            if   (outLang == 'ja') or (outLang == 'ja-JP'):
                rate  = '260'
                if (outGender != 'male'):
                    voice = 'Kyoko'
                    #voice = ''
                else:
                    voice = 'Otoya'
            elif (outLang == 'en') or (outLang == 'en-US'):
                if (outGender != 'male'):
                    voice = 'Ava'
                else:
                    voice = 'Tom'
            elif (outLang == 'ar'):
                voice = 'Laila'
            elif (outLang == 'es'):
                voice = 'Monica'
            elif (outLang == 'de'):
                voice = 'Anna'
            elif (outLang == 'fr'):
                voice = 'Aurelie'
            elif (outLang == 'it'):
                voice = 'Federica'
            elif (outLang == 'pt'):
                voice = 'Joana'
            elif (outLang == 'r'):
                voice = 'Milena'
            elif (outLang == 'tr'):
                voice = 'Yelda'
            elif (outLang == 'uk'):
                voice = ''
            elif (outLang == 'zh') or (outLang == 'zh-CN'):
                voice = 'Ting-Ting'
            elif (outLang == 'ko'):
                voice = 'Yuna'

            if (outText != '') and (outText != '!'):

                try:
                    if (voice != ''):
                        if (rate != ''):
                            say = subprocess.Popen(['say', '-v', voice, '"' + outText + '"', '-r', str(rate), '-o', file, ], )
                        else:
                            say = subprocess.Popen(['say', '-v', voice, '"' + outText + '"', '-o', file, ], )
                    else:
                        if (rate != ''):
                            say = subprocess.Popen(['say', '"' + outText + '"', '-r', str(rate), '-o', file, ], )
                        else:
                            say = subprocess.Popen(['say', '"' + outText + '"', '-o', file, ], )
                    say.wait()
                    say.terminate()
                    say = None

                    if (os.path.isfile(file)):
                        if (os.path.getsize(file) <= 4096):
                            os.remove(file)

                    if (os.path.exists(file)):
                        os.rename(file, outFile)

                    if (os.path.exists(outFile)):
                        rb = open(outFile, 'rb')
                        size = sys.getsizeof(rb.read())
                        if (size <= 44):
                            os.remove(outFile)
                        else:
                            return outText, 'macos'
                except Exception as e:
                    pass

        return '', ''



if __name__ == '__main__':

        #macosAPI = macos_api.SpeechAPI()
        macosAPI = SpeechAPI()

        res = macosAPI.authenticate()
        if (res == True):

            text = 'Hallo!'
            file = 'temp_voice.wav'

            res, api = macosAPI.vocalize(outText=text, outLang='en', outFile=file)
            print('vocalize:', res, '(' + api + ')' )

            sox = subprocess.Popen(['sox', file, '-d', '-q'], )
            sox.wait()
            sox.terminate()
            sox = None



