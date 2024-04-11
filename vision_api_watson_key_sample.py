#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# COPYRIGHT (C) 2014-2024 Mitsuo KONDOU.
# This software is released under the MIT License.
# https://github.com/konsan1101
# Thank you for keeping the rules.
# ------------------------------------------------



def getkey(api, key, ):

    # watson 画像認識
    if (api == 'cv'):
        print('vision_api_watson_key.py')
        print('set your key!')
        if (key == 'url'):
            return 'your url'
        if (key == 'key'):
            return 'your key'

    # watson OCR認識
    if (api == 'ocr'):
        print('vision_api_watson_key.py')
        print('set your key!')
        if (key == 'url'):
            return 'your url'
        if (key == 'key'):
            return 'your key'

    return False


