#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# COPYRIGHT (C) 2014-2024 Mitsuo KONDOU.
# This software is released under the MIT License.
# https://github.com/konsan1101
# Thank you for keeping the rules.
# ------------------------------------------------



def getkey(api, key):

    # google 画像認識
    if (api == 'cv'):
        print('vision_api_google_key.py')
        print('set your key!')
        if (key == 'url'):
            #return 'your url'
            return 'https://vision.googleapis.com/v1/images:annotate'
        if (key == 'key'):
            #return 'your key'
            return 'your key'

    # google OCR認識
    if (api == 'ocr'):
        print('vision_api_google_key.py')
        print('set your key!')
        if (key == 'url'):
            #return 'your url'
            return 'https://vision.googleapis.com/v1/images:annotate'
        if (key == 'key'):
            #return 'your key'
            return 'your key'

    return False


