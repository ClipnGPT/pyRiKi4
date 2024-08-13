#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# COPYRIGHT (C) 2014-2024 Mitsuo KONDOU.
# This software is released under the not MIT License.
# Permission from the right holder is required for use.
# https://github.com/konsan1101
# Thank you for keeping the rules.
# ------------------------------------------------

def getkey(api, key):

    # freeai チャットボット
    if (api == 'freeai'):
        print('speech_bot_freeai_key.py')
        print('set your key!')
        if (key == 'freeai_api_type'):
            return 'use freeai api type'
        if (key == 'freeai_default_gpt'):
            return 'use freeai default gpt'
        if (key == 'freeai_default_class'):
            return 'use chat default class'
        if (key == 'freeai_auto_continue'):
            return 'use chat auto continue'
        if (key == 'freeai_max_step'):
            return 'chat max step'
        if (key == 'freeai_max_assistant'):
            return 'use max assistant'

        if (key == 'freeai_key_id'):
            return 'your freeai key'

        if (key == 'freeai_a_nick_name'):
            return 'your freeai (a) nick name'
        if (key == 'freeai_a_model'):
            return 'your freeai (a) model'
        if (key == 'freeai_a_token'):
            return 'your freeai (a) token'

        if (key == 'freeai_b_nick_name'):
            return 'your freeai (b) nick name'
        if (key == 'freeai_b_model'):
            return 'your freeai (b) model'
        if (key == 'freeai_b_token'):
            return 'your freeai (b) token'

        if (key == 'freeai_v_nick_name'):
            return 'your freeai (v) nick name'
        if (key == 'freeai_v_model'):
            return 'your freeai (v) model'
        if (key == 'freeai_v_token'):
            return 'your freeai (v) token'

        if (key == 'freeai_x_nick_name'):
            return 'your freeai (x) nick name'
        if (key == 'freeai_x_model'):
            return 'your freeai (x) model'
        if (key == 'freeai_x_token'):
            return 'your freeai (x) token'

    return False


