#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# COPYRIGHT (C) 2014-2024 Mitsuo KONDOU.
# This software is released under the MIT License.
# https://github.com/konsan1101
# Thank you for keeping the rules.
# ------------------------------------------------



def getkey(api, key, ):

    # azure 画像認識
    if (api == 'cv'):
        print('vision_api_azure_key.py')
        print('set your key!')
        if (key == 'url'):
            #return 'your url'
            return 'https://japaneast.api.cognitive.microsoft.com/vision/v2.1/analyze'
        if (key == 'key'):
            #return 'your key'
            return 'your key'

    # azure OCR認識
    if (api == 'ocr'):
        print('vision_api_azure_key.py')
        print('set your key!')
        if (key == 'url'):
            #return 'your url'
            return 'https://japaneast.api.cognitive.microsoft.com/vision/v2.1/ocr'
        if (key == 'key'):
            #return 'your key'
            return 'your key'

    return False


