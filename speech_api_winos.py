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

import pythoncom
import platform    # platform.system().lower() #windows,darwin,linux
if (platform.system().lower() == 'windows'):
    import win32com.client



# winos 音声合成



class SpeechAPI:

    def __init__(self, ):
        self.system = None

    def authenticate(self, ):
        self.system = platform.system().lower() #windows,darwin,linux
        if (self.system == 'windows'):
            return True
        return False

    def vocalize(self, outText='hallo', outLang='en-US', outGender='female', outFile='temp_voice.wav'):
        if (self.system is None):
            print('WINOS: Not Authenticate Error !')

        else:
            if (os.path.exists(outFile)):
                try:
                    os.remove(outFile)
                except Exception as e:
                    pass

            #ja-JP:日本語〇,    en-US:英語〇,
            #ar-AR:アラビア語x, es-ES:スペイン語×, de-DE:ドイツ語×
            #fr-FR:フランス語〇,it-IT:イタリア語×, pt-BR:ポルトガル語×
            #ru-RU:ロシア語×,  tr-TR:トルコ語×,   uk-UK:ウクライナ語×
            #zh-CN:中国語×,    kr-KR:韓国語×

            lang = ''
            if   (outLang == 'ja') or (outLang == 'ja-JP'):
                lang = 'ja-JP'
            elif (outLang == 'en') or (outLang == 'en-US'):
                lang = 'en-US'
            elif (outLang == 'ar'):
                lang = 'ar-AR'
            elif (outLang == 'es'):
                lang = 'es-ES'
            elif (outLang == 'de'):
                lang = 'de-DE'
            elif (outLang == 'fr'):
                lang = 'fr-FR'
            elif (outLang == 'it'):
                lang = 'it-IT'
            elif (outLang == 'pt'):
                lang = 'pt-BR'
            elif (outLang == 'r'):
                lang = 'ru-RU'
            elif (outLang == 'tr'):
                lang = 'tr-TR'
            elif (outLang == 'uk'):
                lang = 'uk-UK'
            elif (outLang == 'zh') or (outLang == 'zh-CN'):
                lang = 'zh-CN'
            elif (outLang == 'kr'):
                lang = 'kr-KR'

            if (lang != '') and (outText != '') and (outText != '!'):

                try:

                    # MS Windows
                    stml  = '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">'
                    if (lang == 'ja-JP'):
                        stml += '<prosody rate="1.0">'
                    stml += '<voice xml:lang="' + lang + '" gender="' + outGender.lower() + '">'
                    stml += outText
                    stml += '</voice>'
                    if (lang == 'ja-JP'):
                        stml += '</prosody>'
                    stml += '</speak>'

                    pythoncom.CoInitialize()

                    engine = None
                    if (True):
                        try:
                            engine = win32com.client.Dispatch('SAPI.SpVoice')
                            #engine.Speak(stml)
                        except Exception as e:
                            print('win32com.client.Dispatch(SAPI.SpVoice) is error !', lang, outGender.lower(), )

                    stream = None
                    if (engine is not None):
                        try:
                            stream = win32com.client.Dispatch('SAPI.SpFileStream')

                            stream.open(outFile, 3, False)
                            #for speaker in engine.GetAudioOutputs():
                            #    print(speaker.GetDescription())
                            engine.AudioOutputStream = stream
                            engine.Speak(stml)
                            stream.close()

                        except Exception as e:
                            print('win32com.client.Dispatch(SAPI.SpFileStream) is error !')

                    pythoncom.CoUninitialize()

                    engine = None
                    stream = None

                    if (os.path.exists(outFile)):
                        rb = open(outFile, 'rb')
                        size = sys.getsizeof(rb.read())
                        if (size <= 44):
                            os.remove(outFile)
                        else:
                            return outText, 'winos'
                except Exception as e:
                    pass

        return '', ''



if __name__ == '__main__':

        #winosAPI = winos_api.SpeechAPI()
        winosAPI = SpeechAPI()

        res = winosAPI.authenticate()
        if (res == True):

            text = 'Hallo!'
            file = 'temp_voice.wav'

            res, api = winosAPI.vocalize(outText=text, outLang='en', outFile=file)
            print('vocalize:', res, '(' + api + ')' )

            sox = subprocess.Popen(['sox', file, '-d', '-q'], )
            sox.wait()
            sox.terminate()
            sox = None

            text = 'こんにちは'
            file = 'temp_voice.wav'

            res, api = winosAPI.vocalize(outText=text, outLang='ja', outFile=file)
            print('vocalize:', res, '(' + api + ')' )

            sox = subprocess.Popen(['sox', file, '-d', '-q'], )
            sox.wait()
            sox.terminate()
            sox = None


