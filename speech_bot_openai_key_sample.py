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

    # openai チャットボット
    if (api == 'chatgpt'):
        print('speech_bot_openai_key.py')
        print('set your key!')
        if (key == 'openai_api_type'):
            return 'use openai api type'
        if (key == 'openai_default_gpt'):
            return 'use openai default gpt'
        if (key == 'openai_default_class'):
            return 'use chat default class'
        if (key == 'openai_auto_continue'):
            return 'use chat auto continue'
        if (key == 'openai_max_step'):
            return 'chat max step'
        if (key == 'openai_max_assistant'):
            return 'use max assistant'

        if (key == 'openai_organization'):
            return 'your openai organization'
        if (key == 'openai_key_id'):
            return 'your openai key'

        if (key == 'gpt_a_nick_name'):
            return 'your gpt (a) nick name'
        if (key == 'gpt_a_model1'):
            return 'your gpt (a) model1'
        if (key == 'gpt_a_token1'):
            return 'your gpt (a) token1'
        if (key == 'gpt_a_model2'):
            return 'your gpt (a) model2'
        if (key == 'gpt_a_token2'):
            return 'your gpt (a) token2'
        if (key == 'gpt_a_model3'):
            return 'your gpt (a) model3'
        if (key == 'gpt_a_token3'):
            return 'your gpt (a) token3'

        if (key == 'gpt_b_nick_name'):
            return 'your gpt (b) nick name'
        if (key == 'gpt_b_model1'):
            return 'your gpt (b) model1'
        if (key == 'gpt_b_token1'):
            return 'your gpt (b) token1'
        if (key == 'gpt_b_model2'):
            return 'your gpt (b) model2'
        if (key == 'gpt_b_token2'):
            return 'your gpt (b) token2'
        if (key == 'gpt_b_model3'):
            return 'your gpt (b) model3'
        if (key == 'gpt_b_token3'):
            return 'your gpt (b) token3'
        
        if (key == 'gpt_b_length'):
            return 'your gpt (b) length'

        if (key == 'gpt_v_nick_name'):
            return 'your gpt (v) nick name'
        if (key == 'gpt_v_model'):
            return 'your gpt (v) model'
        if (key == 'gpt_v_token'):
            return 'your gpt (v) token'

        if (key == 'gpt_x_nick_name'):
            return 'your gpt (x) nick name'
        if (key == 'gpt_x_model1'):
            return 'your gpt (x) model1'
        if (key == 'gpt_x_token1'):
            return 'your gpt (x) token1'
        if (key == 'gpt_x_model2'):
            return 'your gpt (x) model2'
        if (key == 'gpt_x_token2'):
            return 'your gpt (x) token2'

        if (key == 'azure_endpoint'):
            return 'your azure endpoint'
        if (key == 'azure_version'):
            return 'your azure version'
        if (key == 'azure_key_id'):
            return 'your azure key'

        if (key == 'azure_a_nick_name'):
            return 'your azure (a) nick name'
        if (key == 'azure_a_model1'):
            return 'your azure (a) model1'
        if (key == 'azure_a_token1'):
            return 'your azure (a) token1'
        if (key == 'azure_a_model2'):
            return 'your azure (a) model2'
        if (key == 'azure_a_token2'):
            return 'your azure (a) token2'
        if (key == 'azure_a_model3'):
            return 'your azure (a) model3'
        if (key == 'azure_a_token3'):
            return 'your azure (a) token3'

        if (key == 'azure_b_nick_name'):
            return 'your azure (b) nick name'
        if (key == 'azure_b_model1'):
            return 'your azure (b) model1'
        if (key == 'azure_b_token1'):
            return 'your azure (b) token1'
        if (key == 'azure_b_model2'):
            return 'your azure (b) model2'
        if (key == 'azure_b_token2'):
            return 'your azure (b) token2'
        if (key == 'azure_b_model3'):
            return 'your azure (b) model3'
        if (key == 'azure_b_token3'):
            return 'your azure (b) token3'

        if (key == 'azure_b_length'):
            return 'your azure (b) length'

        if (key == 'azure_v_nick_name'):
            return 'your azure (v) nick name'
        if (key == 'azure_v_model'):
            return 'your azure (v) model'
        if (key == 'azure_v_token'):
            return 'your azure (v) token'

        if (key == 'azure_x_nick_name'):
            return 'your azure (x) nick name'
        if (key == 'azure_x_model1'):
            return 'your azure (x) model1'
        if (key == 'azure_x_token1'):
            return 'your azure (x) token1'
        if (key == 'azure_x_model2'):
            return 'your azure (x) model2'
        if (key == 'azure_x_token2'):
            return 'your azure (x) token2'

    return False


