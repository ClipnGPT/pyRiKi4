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

    # gemini チャットボット
    if (api == 'gemini'):
        print('speech_bot_gemini_key.py')
        print('set your key!')
        if (key == 'gemini_api_type'):
            return 'use gemini api type'
        if (key == 'gemini_default_gpt'):
            return 'use gemini default gpt'
        if (key == 'gemini_default_class'):
            return 'use chat default class'
        if (key == 'gemini_auto_continue'):
            return 'use chat auto continue'
        if (key == 'gemini_max_step'):
            return 'chat max step'
        if (key == 'gemini_max_assistant'):
            return 'use max assistant'

        if (key == 'gemini_key_id'):
            return 'your gemini key'

        if (key == 'gemini_a_nick_name'):
            return 'your gemini (a) nick name'
        if (key == 'gemini_a_model'):
            return 'your gemini (a) model'
        if (key == 'gemini_a_token'):
            return 'your gemini (a) token'

        if (key == 'gemini_b_nick_name'):
            return 'your gemini (b) nick name'
        if (key == 'gemini_b_model'):
            return 'your gemini (b) model'
        if (key == 'gemini_b_token'):
            return 'your gemini (b) token'

        if (key == 'gemini_v_nick_name'):
            return 'your gemini (v) nick name'
        if (key == 'gemini_v_model'):
            return 'your gemini (v) model'
        if (key == 'gemini_v_token'):
            return 'your gemini (v) token'

        if (key == 'gemini_x_nick_name'):
            return 'your gemini (x) nick name'
        if (key == 'gemini_x_model'):
            return 'your gemini (x) model'
        if (key == 'gemini_x_token'):
            return 'your gemini (x) token'

    return False


