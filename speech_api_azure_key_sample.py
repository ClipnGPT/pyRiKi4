#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# COPYRIGHT (C) 2014-2024 Mitsuo KONDOU.
# This software is released under the MIT License.
# https://github.com/konsan1101
# Thank you for keeping the rules.
# ------------------------------------------------



def getkey(api, key, ):

    # azure 音声認識
    if (api == 'stt'):
        print('speech_api_azure_key.py')
        print('set your key!')
        if (key == 'key'):
            return 'your key'
            #return 'your key'
        if (key == 'authurl'):
            return 'your auth url'
            #return 'https://eastasia.api.cognitive.microsoft.com/sts/v1.0/issueToken'
        if (key == 'procurl'):
            return 'your proc url'
            #return 'https://eastasia.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1'


    # azure 音声合成
    if (api == 'tts'):
        print('speech_api_azure_key.py')
        print('set your key!')
        if (key == 'key'):
            return 'your key'
            #return 'your key'
        if (key == 'authurl'):
            return 'your auth url'
            #return 'https://eastasia.api.cognitive.microsoft.com/sts/v1.0/issueToken'
        if (key == 'procurl'):
            return 'your proc url'
            #return 'https://eastasia.tts.speech.microsoft.com/cognitiveservices/v1'
 
    # azure 翻訳機能
    if (api == 'tra'):
        #print('speech_api_azure_key.py')
        #print('set your key!')
        if (key == 'key'):
            return 'your key'
            #return 'your key'
        if (key == 'authurl'):
            return 'your auth url'
            #return 'https://api.cognitive.microsoft.com/sts/v1.0/issueToken'
        if (key == 'procurl'):
            return 'your proc url'
            #return 'https://api.microsofttranslator.com/v2/http.svc/Translate'

    return False


