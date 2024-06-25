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

    # claude チャットボット
    if (api == 'claude'):
        print('speech_bot_claude_key.py')
        print('set your key!')
        if (key == 'claude_api_type'):
            return 'use claude api type'
        if (key == 'claude_default_gpt'):
            return 'use claude default gpt'
        if (key == 'claude_default_class'):
            return 'use chat default class'
        if (key == 'claude_auto_continue'):
            return 'use chat auto continue'
        if (key == 'claude_max_step'):
            return 'chat max step'
        if (key == 'claude_max_assistant'):
            return 'use max assistant'

        if (key == 'claude_key_id'):
            return 'your claude key'

        if (key == 'claude_a_nick_name'):
            return 'your claude (a) nick name'
        if (key == 'claude_a_model'):
            return 'your claude (a) model'
        if (key == 'claude_a_token'):
            return 'your claude (a) token'

        if (key == 'claude_b_nick_name'):
            return 'your claude (b) nick name'
        if (key == 'claude_b_model'):
            return 'your claude (b) model'
        if (key == 'claude_b_token'):
            return 'your claude (b) token'

        if (key == 'claude_v_nick_name'):
            return 'your claude (v) nick name'
        if (key == 'claude_v_model'):
            return 'your claude (v) model'
        if (key == 'claude_v_token'):
            return 'your claude (v) token'

        if (key == 'claude_x_nick_name'):
            return 'your claude (x) nick name'
        if (key == 'claude_x_model'):
            return 'your claude (x) model'
        if (key == 'claude_x_token'):
            return 'your claude (x) token'

    return False


