#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# COPYRIGHT (C) 2014-2024 Mitsuo KONDOU.
# This software is released under the MIT License.
# https://github.com/konsan1101
# Thank you for keeping the rules.
# ------------------------------------------------



def getkey(api,):

    # google 音声認識
    if (api == 'stt'):
        print('speech_api_google_key.py')
        print('set your key!')
        #return 'your key'
        return 'your key'

    # google 翻訳機能
    if (api == 'tra'):
        print('speech_api_google_key.py')
        print('set your key!')
        #return 'your key'
        return 'your key'

    # google 音声合成
    if (api == 'tts'):
        return 'free'

    if (api == 'json'):
        return \
r"""
{
  your key
}
"""

    return False



