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
import http.client
import xml.etree.ElementTree
import uuid



# azure 音声認識、翻訳機能、音声合成
import speech_api_azure_key as azure_key



class SpeechAPI:

    def __init__(self, ):
        self.timeOut   = 10
        self.stt_token = None
        self.stt_url   = None
        self.tra_token = None
        self.tra_url   = None
        self.tts_token = None
        self.tts_url   = None

    def setTimeOut(self, timeOut=10, ):
        self.timeOut = timeOut

    def authenticate(self, api, key, authurl, procurl, ):
        # azure 音声認識
        if (api == 'stt'):
            if (self.stt_token is None):
                self.stt_url = procurl
                #authurl  = 'https://eastasia.api.cognitive.microsoft.com/sts/v1.0/issueToken'
                headers = {
                            'Content-type': 'application/x-www-form-urlencoded',
                            'Content-Length': '0',
                            'Ocp-Apim-Subscription-Key': key,
                            }
                try:
                    res = requests.post(authurl, headers=headers, timeout=self.timeOut, )
                    #print(res)
                    if (res.status_code == 200):
                        #print(res.text)
                        self.stt_token = res.text
                except Exception as e:
                    self.stt_token = None
            if (self.stt_token is not None):
                return True

        # azure 翻訳機能
        if (api == 'tra'):
            if (self.tra_token is None):
                self.tra_url = procurl
                if (authurl != 'v3'):
                    # v1,v2
                    # #authurl  = 'https://api.cognitive.microsoft.com/sts/v1.0/issueToken'
                    # headers = {'Ocp-Apim-Subscription-Key': key}
                    # try:
                    #     res = requests.post(authurl, headers=headers, timeout=self.timeOut, )
                    #     #print(res)
                    #     if (res.status_code == 200):
                    #         #print(res.text)
                    #         self.tra_token = res.text
                    # except Exception as e:
                    #     self.tra_token = None
                    self.tra_token = None
                else:
                    # v3
                    self.tra_token = key
            if (self.tra_token is not None):
                return True

        # azure 音声合成
        if (api == 'tts'):
            if (self.tts_token is None):
                self.tts_url = procurl
                #authurl  = 'https://eastasia.api.cognitive.microsoft.com/sts/v1.0/issueToken'
                headers = {
                            'Content-type': 'application/x-www-form-urlencoded',
                            'Content-Length': '0',
                            'Ocp-Apim-Subscription-Key': key,
                            }
                try:
                    res = requests.post(authurl, headers=headers, timeout=self.timeOut, )
                    #print(res)
                    if (res.status_code == 200):
                        #print(res.text)
                        self.tts_token = res.text
                except Exception as e:
                    self.tts_token = None
            if (self.tts_token is not None):
                return True

        return False



    def recognize(self, inpWave, inpLang='ja-JP', ):
        res_text = ''
        res_api  = ''
        if (self.stt_token is None):
            print('AZURE: Not Authenticate Error !')

        else:
            lang  = ''

            if (inpLang == 'auto'):
                lang  = 'ja-JP'
            elif (inpLang == 'ja' or inpLang == 'ja-JP'):
                lang  = 'ja-JP'
            elif (inpLang == 'en' or inpLang == 'en-US'):
                lang  = 'en-US'
            elif (inpLang == 'ar'):
                lang  = 'ar-AR'
            elif (inpLang == 'es'):
                lang  = 'es-ES'
            elif (inpLang == 'de'):
                lang  = 'de-DE'
            elif (inpLang == 'fr'):
                lang  = 'fr-FR'
            elif (inpLang == 'it'):
                lang  = 'it-IT'
            elif (inpLang == 'pt'):
                lang  = 'pt-BR'
            elif (inpLang == 'zh' or inpLang == 'zh-CN'):
                lang  = 'zh-CN'

            if (lang != ''):
                try:
                    rb = open(inpWave, 'rb')
                    audio = rb.read()
                    rb.close
                    rb = None

                    #procurl  = 'https://eastasia.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1'
                    procurl  = self.stt_url
                    headers = {
                        'Content-Type': 'audio/wav; codec=audio/pcm; samplerate=16000',
                        'Authorization': 'Bearer ' + self.stt_token,
                        }
                    params = {
                        'language': lang,
                        'format': 'simple',
                        }

                    res = requests.post(procurl, headers=headers, params=params, data=audio, timeout=self.timeOut, )
                    #print(res)
                    if (res.status_code == 200):
                        #print(res.json())
                        res_text = res.json()['DisplayText']
                        if (res_text != ''):
                            res_api = 'azure'

                except Exception as e:
                    pass

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

                # azure fault!
                if (res_text.lower() == 'x'):
                    res_text = ''

                return res_text, res_api

        return res_text, res_api



    def translate(self, inpText='こんにちは', inpLang='ja-JP', outLang='en-US', ):
        res_text = ''
        res_api  = ''
        if (self.tra_token is None):
            print('AZURE: Not Authenticate Error !')

        else:
            inp = ''
            out = ''

            if (inpLang == 'auto'):
                inp = 'ja-JP'
            elif (inpLang == 'ja' or inpLang == 'ja-JP'):
                inp = 'ja-JP'
            elif (inpLang == 'en' or inpLang == 'en-US'):
                inp = 'en-US'
            elif (inpLang == 'ar'):
                inp = 'ar-AR'
            elif (inpLang == 'es'):
                inp = 'es-ES'
            elif (inpLang == 'de'):
                inp = 'de-DE'
            elif (inpLang == 'fr'):
                inp = 'fr-FR'
            elif (inpLang == 'it'):
                inp = 'it-IT'
            elif (inpLang == 'pt'):
                inp = 'pt-BR'
            elif (inpLang == 'zh' or inpLang == 'zh-CN'):
                inp = 'zh-CN'

            if   (outLang == 'ar'):
                out = 'ar-AR'
            elif (outLang == 'en' or outLang == 'en-US'):
                out = 'en-US'
            elif (outLang == 'es'):
                out = 'es-US'
            elif (outLang == 'de'):
                out = 'de-DE'
            elif (outLang == 'fr'):
                out = 'fr-FR'
            elif (outLang == 'it'):
                out = 'it-IT'
            elif (outLang == 'ja' or outLang == 'ja-JP'):
                out = 'ja-JP'
            elif (outLang == 'pt'):
                out = 'pt-BR'
            elif (outLang == 'zh' or outLang == 'zh-CN'):
                out = 'zh-CN'

            if (inp != '') and (out != '') and (inpText != '') and (inpText != '!'):
                try:

                    # v1,v2
                    # #procurl  = 'https://api.microsofttranslator.com/v2/http.svc/Translate'
                    # procurl  = self.tra_url
                    # headers = {'Content-Type': 'application/xml',}
                    # params  = {'appid': 'Bearer ' + self.tra_token,
                    #            'text': inpText,
                    #            'from': inp,
                    #            'to': out,
                    #            'category':'general',
                    #           }
                    #res = requests.get(procurl, headers=headers, params=params, timeout=self.timeOut, )

                    # v3
                    #procurl  = 'https://api.cognitive.microsofttranslator.com/translate?api-version=3.0'
                    procurl  = self.tra_url
                    procurl += '&from=' + inp + '&to=' + out
                    headers = {
                        'Ocp-Apim-Subscription-Key': self.tra_token,
                        'Content-type': 'application/json',
                        'X-ClientTraceId': str(uuid.uuid4())
                    }
                    body = [{
                        'text' : inpText,
                    }]
                    res = requests.post(procurl, headers=headers, json=body, timeout=self.timeOut, )

                    #print(res.status_code)
                    if (res.status_code == 200):
                        # v1,v2
                        #print(res.text)
                        #res_xml = res.text
                        #res_text = xml.etree.ElementTree.fromstring(res_xml).text
                        # v3
                        #print(res.json())
                        #print(res.json()[0]['translations'])
                        #print(res.json()[0]['translations'][0]['text'])
                        res_text = res.json()[0]['translations'][0]['text']
                        if (res_text != ''):
                            res_api = 'azure'

                except Exception as e:
                    pass

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

                # azure fault!
                if (res_text.lower() == 'x'):
                    res_text = ''

                return res_text, res_api

        return res_text, res_api



    def vocalize(self, outText='hallo', outLang='en-US', outGender='Female', outFile='temp_voice.mp3', ):
        if (self.tts_token is None):
            print('AZURE: Not Authenticate Error !')

        else:
            if (os.path.exists(outFile)):
                try:
                    os.remove(outFile)
                except Exception as e:
                    pass

            lang  = ''
            voice = ''
            gend  = outGender

            if   (outLang == 'ja' or outLang=='ja-JP'):
                lang  = 'ja-JP'
                voice = 'Microsoft Server Speech Text to Speech Voice (ja-JP, HarukaRUS)'
                gend  = 'Female'
            elif (outLang == 'en' or outLang == 'en-US'):
                lang  = 'en-US'
                voice = 'Microsoft Server Speech Text to Speech Voice (en-US, ZiraRUS)'
                gend  = 'Female'
            elif (outLang == 'ar'):
                lang  = 'ar-eg'
                voice = 'Microsoft Server Speech Text to Speech Voice (ar-EG, Hoda)'
                gend  = 'Female'
            elif (outLang == 'es'):
                lang  = 'es-US'
                voice = 'Microsoft Server Speech Text to Speech Voice (es-ES, Laura, Apollo)'
                gend  = 'Female'
            elif (outLang == 'de'):
                lang  = 'de-DE'
                voice = 'Microsoft Server Speech Text to Speech Voice (de-DE, Hedda)'
                gend  = 'Female'
            elif (outLang == 'fr'):
                lang  = 'fr-FR'
                voice = 'Microsoft Server Speech Text to Speech Voice (fr-FR, Julie, Apollo)'
                gend  = 'Female'
            elif (outLang == 'it'):
                lang  = 'it-IT'
                voice = 'Microsoft Server Speech Text to Speech Voice (it-IT, Cosimo, Apollo)'
                gend  = 'Male'
            elif (outLang == 'pt'):
                lang  = 'pt-BR'
                voice = 'Microsoft Server Speech Text to Speech Voice (pt-BR, Daniel, Apollo)'
                gend  = 'Male'
            elif (outLang == 'zh' or outLang == 'zh-CN'):
                lang  = 'zh-CN'
                voice = 'Microsoft Server Speech Text to Speech Voice (zh-CN, Yaoyao, Apollo)'
                gend  = 'Female'

            if (voice != '') and (outText != '') and (outText != '!'):
                try:

                    #host = 'eastasia.tts.speech.microsoft.com'
                    #path = '/cognitiveservices/v1'

                    procurl  = self.tts_url
                    procurl = procurl.replace('https://', '')
                    s = procurl.find('/')
                    host = procurl[:s]
                    path = procurl[s:]

                    headers = {'Content-type': 'application/ssml+xml', 
                                'X-Microsoft-OutputFormat': 'audio-16khz-32kbitrate-mono-mp3',
                                'Authorization': 'Bearer ' + self.tts_token, 
                                'User-Agent': 'TTSForPython'}

                    body = xml.etree.ElementTree.Element('speak', version='1.0')
                    body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
                    smtl = xml.etree.ElementTree.SubElement(body, 'voice')
                    smtl.set('{http://www.w3.org/XML/1998/namespace}lang', lang)
                    smtl.set('{http://www.w3.org/XML/1998/namespace}gender', gend)
                    smtl.set('name', voice)
                    smtl.text = outText

                    #print ('Connect to server')
                    conn = http.client.HTTPSConnection(host)
                    conn.request('POST', path, xml.etree.ElementTree.tostring(body), headers, )
                    res = conn.getresponse()
                    #print('Response', res.status, res.reason)
                    if (res.status == 200):
                        audio = res.read()
                        wb = open(outFile, 'wb')
                        wb.write(audio)
                        wb.close()
                        wb = None
                        return outText, 'azure'

                except Exception as e:
                    pass
        return '', ''



if __name__ == '__main__':

        #azureAPI = azure_api.SpeechAPI()
        azureAPI = SpeechAPI()

        key     = azure_key.getkey('stt', 'key', )
        authurl = azure_key.getkey('stt', 'authurl', )
        procurl = azure_key.getkey('stt', 'procurl', )
        res1 = azureAPI.authenticate('stt', key, authurl, procurl, )
        key     = azure_key.getkey('tra', 'key', )
        authurl = azure_key.getkey('tra', 'authurl', )
        procurl = azure_key.getkey('tra', 'procurl', )
        res2 = azureAPI.authenticate('tra', key, authurl, procurl, )
        key     = azure_key.getkey('tts', 'key', )
        authurl = azure_key.getkey('tts', 'authurl', )
        procurl = azure_key.getkey('tts', 'procurl', )
        res3 = azureAPI.authenticate('tts', key, authurl, procurl, )
        print('authenticate:', res1, res2, res3)

        if (res1 == True) and (res2 == True) and (res3 == True):

            text = 'hallo'
            file = 'temp_voice.mp3'

            res, api = azureAPI.vocalize(outText=text, outLang='en', outFile=file)
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

            res, api = azureAPI.recognize(inpWave=file2, inpLang='en', )
            print('recognize:', res, '(' + api + ')' )

            res, api = azureAPI.translate(inpText=res, inpLang='en', outLang='ja', )
            print('translate:', res, '(' + api + ')' )



