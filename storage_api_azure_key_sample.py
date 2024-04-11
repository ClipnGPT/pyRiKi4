#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# COPYRIGHT (C) 2014-2024 Mitsuo KONDOU.
# This software is released under the MIT License.
# https://github.com/konsan1101
# Thank you for keeping the rules.
# ------------------------------------------------



def getkey(api, key, ):

    # azure blob
    if (api == 'blob'):
        print('storage_api_azure_key.py')
        print('set your key!')
        if (key == 'account'):
            return 'your account'
        if (key == 'key'):
            return 'your key'
        if (key == 'container'):
            return 'your container'

    return False


