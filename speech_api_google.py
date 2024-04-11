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

import requests
import json
import base64
import io
import speech_recognition as sr
from gtts import gTTS

googletrans_ok = False
try:
    from googletrans import Translator
    googletrans_ok = True
except:
    pass


# google 音声認識、翻訳機能、音声合成
#pip install --upgrade google-cloud-speech
#pip install --upgrade google-cloud-translate
import google.cloud.speech
import google.cloud.translate_v2
import speech_api_google_key as google_key



class SpeechAPI:

    def __init__(self, ):
        self.timeOut = 10
        self.stt_key = None
        self.tra_key = None
        self.tts_key = None
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'speech_api_google_key.json'
    
    def setTimeOut(self, timeOut=10, ):
        self.timeOut = timeOut

    def authenticate(self, api, key, ):
        # google 音声認識
        if (api == 'stt'):
            if (self.stt_key is None):
                self.stt_key = key
            if (self.stt_key is not None):
                return True

        # google 翻訳機能
        if (api == 'tra'):
            if (self.tra_key is None):
                self.tra_key = key
            if (self.tra_key is not None):
                return True

        # google 音声合成
        if (api == 'tts'):
            if (self.tts_key is None):
                self.tts_key = key
            if (self.tts_key is not None):
                return True

        return False

    def recognize(self, inpWave, inpLang='ja-JP', api='auto', ):
        res_text = ''
        res_api  = ''
        if (self.stt_key is None):
            print('GOOGLE: Not Authenticate Error !')

        else:
            lang  = inpLang
            if (inpLang == 'auto'):
                lang  = 'ja-JP'
            elif (inpLang == 'ar'):
                lang  = 'ar-AR'
            elif (inpLang == 'en' or inpLang == 'en-US'):
                lang  = 'en-US'
            elif (inpLang == 'es'):
                lang  = 'es-ES'
            elif (inpLang == 'de'):
                lang  = 'de-DE'
            elif (inpLang == 'fr'):
                lang  = 'fr-FR'
            elif (inpLang == 'it'):
                lang  = 'it-IT'
            elif (inpLang == 'ja' or inpLang == 'ja-JP'):
                lang  = 'ja-JP'
            elif (inpLang == 'pt'):
                lang  = 'pt-BR'
            elif (inpLang == 'zh' or inpLang == 'zh-CN'):
                lang  = 'zh-CN'

            if (lang != ''):

                if (res_text == '') and (api == 'auto' or api == 'free'):
                    try:
                        srr  = sr.Recognizer()
                        with sr.AudioFile(inpWave) as source:
                            audio = srr.record(source)
                            res_text = srr.recognize_google(audio, language=inpLang)
                        if (res_text != ''):
                            res_api = 'free'
                            #print(res_text + '(' + res_api + ')')
                    except Exception as e:
                        pass

                if (res_text == '') and (api == 'auto' or api == 'google' or api == 'google8k'):

                        inpWave8k = inpWave[:-4] + '.8k.wav'
                        sox = subprocess.Popen(['sox', '-q', inpWave, '-r', '8000', '-b', '16', '-c', '1', inpWave8k, ], )
                        sox.wait()
                        sox.terminate()
                        sox = None

                        client = google.cloud.speech.SpeechClient()
                        config = google.cloud.speech.RecognitionConfig(
                            encoding=google.cloud.speech.RecognitionConfig.AudioEncoding.LINEAR16,
                            sample_rate_hertz=8000,
                            language_code=lang)
                        with io.open(inpWave8k, 'rb') as audio_file:
                            content = audio_file.read()
                            audio = google.cloud.speech.RecognitionAudio(content=content)
                        res = client.recognize(config=config, audio=audio)
                        #print(res)
                        res_text  = ''
                        for r in res.results:
                            #print('{}'.format(r.alternatives[0].transcript))
                            res_text += '{}'.format(r.alternatives[0].transcript)
                        if (res_text != ''):
                            res_api = 'google'
                            #print(res_text + '(' + res_api + ')')

                        try:
                            os.remove(inpWave8k)
                        except Exception as e:
                            pass

                if (res_text == '') and (api == 'auto' or api == 'google'):

                        client = google.cloud.speech.SpeechClient()
                        config = google.cloud.speech.RecognitionConfig(
                            encoding=google.cloud.speech.RecognitionConfig.AudioEncoding.LINEAR16,
                            sample_rate_hertz=16000,
                            language_code=lang)
                        with io.open(inpWave, 'rb') as audio_file:
                            content = audio_file.read()
                            audio = google.cloud.speech.RecognitionAudio(content=content)
                        res = client.recognize(config=config, audio=audio)
                        #print(res)
                        res_text  = ''
                        for r in res.results:
                            #print('{}'.format(r.alternatives[0].transcript))
                            res_text += '{}'.format(r.alternatives[0].transcript)
                        if (res_text != ''):
                            res_api = 'google'
                            #print(res_text + '(' + res_api + ')')

            if (res_text != ''):
                res_text = str(res_text).strip()
                while (res_text[-1:] == '。') \
                   or (res_text[-1:] == '、') \
                   or (res_text[-1:] == '.'):
                    res_text = res_text[:-1]

                if (inpLang == 'ja' or inpLang == 'ja-JP'):
                    chk_text = str(res_text).replace(' ', '')
                    chk_text = str(chk_text).replace('.', '')
                    chk_text = str(chk_text).replace('_', '')
                    if (not chk_text.encode('utf-8').isalnum()):
                        res_text = str(res_text).replace(' ', '')

                return res_text, res_api

        return res_text, res_api

    def translate(self, inpText='こんにちは', inpLang='ja', outLang='en', api='auto', ):
        res_text = ''
        res_api  = ''
        if (googletrans_ok == False):
            print('GOOGLE: googletrans not install !')

        elif (self.tra_key is None):
            print('GOOGLE: Not Authenticate Error !')

        else:
            inp = inpLang
            out = outLang
            if (inp != '') and (out != '') and (inpText != '') and (inpText != '!'):

                if (res_text == '') and (api == 'auto' or api == 'free'):
                    try:
                        ggtrans = Translator()
                        res = ggtrans.translate([inpText], src=inp, dest=out)
                        for t in res:
                             res_text += t.text
                        if (res_text != ''):
                            res_api = 'free'
                            #print(res_text + '(' + res_api + ')')
                    except Exception as e:
                        pass

                if (res_text == '') and (api == 'free' or api == 'free2'):
                    try:
                        url = 'https://translate.google.com/translate_a/single'
                        headers = {
                                  'User-Agent': 'GoogleTranslate/5.9.59004 (iPhone; iOS 10.2; ja; iPhone9,1)'
                                  }
                        params  = {
                                  'client': 'it',
                                  'dt': ['t', 'rmt', 'bd', 'rms', 'qca', 'ss', 'md', 'ld', 'ex'],
                                  'dj': '1',
                                  'sl': inp,
                                  'tl': out,
                                  'q': inpText,
                                  }
                        res = requests.get(url, headers=headers, params=params, timeout=self.timeOut, )
                        #print(res)
                        if (res.status_code == 200):
                            #print(res.text)
                            res_text = res.json()['sentences'][0]['trans']
                        if (res_text != ''):
                            res_api = 'free2'
                            #print(res_text + '(' + res_api + ')')
                    except Exception as e:
                        pass

                if (res_text == '') and (api == 'auto' or api == 'google'):
                    #try:
                        client = google.cloud.translate_v2.Client()
                        res = client.translate([inpText], 
                                               source_language=inp,
                                               target_language=out, )
                        #print(res)
                        for t in res:
                             res_text += t['translatedText']
                        if (res_text != ''):
                            res_api = 'google'
                            #print(res_text + '(' + res_api + ')')
                    #except Exception as e:
                    #    pass

            if (res_text != ''):
                res_text = str(res_text).strip()
                while (res_text[-1:] == '。') \
                   or (res_text[-1:] == '、') \
                   or (res_text[-1:] == '.'):
                    res_text = res_text[:-1]

                if (outLang == 'ja' or outLang == 'ja-JP'):
                    chk_text = str(res_text).replace(' ', '')
                    chk_text = str(chk_text).replace('.', '')
                    chk_text = str(chk_text).replace('_', '')
                    if (not chk_text.encode('utf-8').isalnum()):
                        res_text = str(res_text).replace(' ', '')

                return res_text, res_api

        return res_text, res_api

    def vocalize(self, outText='hallo', outLang='en-US', outGender='female', outFile='temp_voice.mp3', api='free', ):
        if (self.tts_key is None):
            print('GOOGLE: Not Authenticate Error !')

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

        #googleAPI = google_api.SpeechAPI()
        googleAPI = SpeechAPI()

        res1 = googleAPI.authenticate('stt', google_key.getkey('stt'), )
        res2 = googleAPI.authenticate('tra', google_key.getkey('tra'), )
        res3 = googleAPI.authenticate('tts', google_key.getkey('tts'), )
        print('authenticate:', res1, res2, res3)

        if (res1 == True) and (res2 == True) and (res3 == True):

            text = 'Hallo'
            file = 'temp_voice.mp3'

            res, api = googleAPI.vocalize(outText=text, outLang='en', outFile=file)
            print('vocalize:', res, '(' + api + ')' )

            sox = subprocess.Popen(['sox', file, '-d', '-q'], )
            sox.wait()
            sox.terminate()
            sox = None

            file2 = 'temp_voice.wav'
            sox = subprocess.Popen(['sox', '-q', file, '-r', '16000', '-b', '16', '-c', '1', file2, ], )
            sox.wait()
            sox.terminate()
            sox = None

            res, api = googleAPI.recognize(inpWave=file2, inpLang='en', api='auto', )
            print('recognize:', res, '(' + api + ')' )

            res, api = googleAPI.recognize(inpWave=file2, inpLang='en', api='google', )
            print('recognize:', res, '(' + api + ')' )

            file2 = '_sounds/_sound_hallo.wav'
            sox = subprocess.Popen(['sox', file2, '-d', '-q'], )
            sox.wait()
            sox.terminate()
            sox = None

            res, api = googleAPI.recognize(inpWave=file2, inpLang='ja', api='auto', )
            print('recognize:', res, '(' + api + ')' )

            res, api = googleAPI.recognize(inpWave=file2, inpLang='ja', api='google', )
            print('recognize:', res, '(' + api + ')' )

            res, api = googleAPI.translate(inpText=res, inpLang='ja', outLang='en', api='auto', )
            print('translate:', res, '(' + api + ')' )

            res, api = googleAPI.translate(inpText=res, inpLang='ja', outLang='en', api='google', )
            print('translate:', res, '(' + api + ')' )



