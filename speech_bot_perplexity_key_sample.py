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

    # perplexity チャットボット
    if (api == 'perplexity'):
        print('speech_bot_perplexity_key.py')
        print('set your key!')
        if (key == 'perplexity_api_type'):
            return 'use perplexity api type'
        if (key == 'perplexity_default_gpt'):
            return 'use perplexity default gpt'
        if (key == 'perplexity_default_class'):
            return 'use chat default class'
        if (key == 'perplexity_auto_continue'):
            return 'use chat auto continue'
        if (key == 'perplexity_max_step'):
            return 'chat max step'
        if (key == 'perplexity_max_assistant'):
            return 'use max assistant'

        if (key == 'perplexity_key_id'):
            return 'your perplexity key'

        if (key == 'perplexity_a_nick_name'):
            return 'your perplexity (a) nick name'
        if (key == 'perplexity_a_model'):
            return 'your perplexity (a) model'
        if (key == 'perplexity_a_token'):
            return 'your perplexity (a) token'

        if (key == 'perplexity_b_nick_name'):
            return 'your perplexity (b) nick name'
        if (key == 'perplexity_b_model'):
            return 'your perplexity (b) model'
        if (key == 'perplexity_b_token'):
            return 'your perplexity (b) token'

        if (key == 'perplexity_v_nick_name'):
            return 'your perplexity (v) nick name'
        if (key == 'perplexity_v_model'):
            return 'your perplexity (v) model'
        if (key == 'perplexity_v_token'):
            return 'your perplexity (v) token'

        if (key == 'perplexity_x_nick_name'):
            return 'your perplexity (x) nick name'
        if (key == 'perplexity_x_model'):
            return 'your perplexity (x) model'
        if (key == 'perplexity_x_token'):
            return 'your perplexity (x) token'

    return False


