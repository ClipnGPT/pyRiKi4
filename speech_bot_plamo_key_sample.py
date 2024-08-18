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

    # plamo チャットボット
    if (api == 'plamo'):
        print('speech_bot_plamo_key.py')
        print('set your key!')
        if (key == 'plamo_api_type'):
            return 'use plamo api type'
        if (key == 'plamo_default_gpt'):
            return 'use plamo default gpt'
        if (key == 'plamo_default_class'):
            return 'use chat default class'
        if (key == 'plamo_auto_continue'):
            return 'use chat auto continue'
        if (key == 'plamo_max_step'):
            return 'chat max step'
        if (key == 'plamo_max_assistant'):
            return 'use max assistant'

        if (key == 'plamo_key_id'):
            return 'your plamo key'

        if (key == 'plamo_a_nick_name'):
            return 'your plamo (a) nick name'
        if (key == 'plamo_a_model'):
            return 'your plamo (a) model'
        if (key == 'plamo_a_token'):
            return 'your plamo (a) token'

        if (key == 'plamo_b_nick_name'):
            return 'your plamo (b) nick name'
        if (key == 'plamo_b_model'):
            return 'your plamo (b) model'
        if (key == 'plamo_b_token'):
            return 'your plamo (b) token'

        if (key == 'plamo_v_nick_name'):
            return 'your plamo (v) nick name'
        if (key == 'plamo_v_model'):
            return 'your plamo (v) model'
        if (key == 'plamo_v_token'):
            return 'your plamo (v) token'

        if (key == 'plamo_x_nick_name'):
            return 'your plamo (x) nick name'
        if (key == 'plamo_x_model'):
            return 'your plamo (x) model'
        if (key == 'plamo_x_token'):
            return 'your plamo (x) token'

    return False


