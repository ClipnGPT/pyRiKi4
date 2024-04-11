#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# COPYRIGHT (C) 2014-2024 Mitsuo KONDOU.
# This software is released under the MIT License.
# https://github.com/konsan1101
# Thank you for keeping the rules.
# ------------------------------------------------



def getkey(api, key, ):

    # aws s3
    if (api == 's3'):
        #print('storage_api_aws_key.py')
        #print('set your key!')
        if (key == 'key_id'):
            return 'your access key id'
        if (key == 'secret_key'):
            return 'your secret access key'

    return False


