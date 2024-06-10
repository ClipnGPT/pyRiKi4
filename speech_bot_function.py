#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# COPYRIGHT (C) 2014-2024 Mitsuo KONDOU.
# This software is released under the not MIT License.
# Permission from the right holder is required for use.
# https://github.com/konsan1101
# Thank you for keeping the rules.
# ------------------------------------------------

import sys
import os
import time
import datetime
import codecs
import shutil

import glob
import importlib



import _v6__qRiKi_key
qRiKi_key = _v6__qRiKi_key.qRiKi_key_class()



class botFunction:

    def __init__(self, ):
        self.function_modules = []

    def init(self, ):
        return True

    def functions_load(self, functions_path='_extensions/function/', secure_level='medium', ):
        res_load_all = True
        res_load_msg = ''
        self.functions_unload()
        #print('Load functions ... ')

        path = functions_path
        path_files = glob.glob(path + '*.py')
        path_files.sort()
        if (len(path_files) > 0):
            for f in path_files:
                base_name = os.path.basename(f)
                if (base_name[:4] != '_v6_') and (base_name[:4] != '_v7_'):

                    try:
                        file_name   = os.path.splitext(base_name)[0]
                        print('Functions Loading ... "' + file_name + '" ...')
                        loader = importlib.machinery.SourceFileLoader(file_name, f)
                        ext_script = file_name
                        ext_module = loader.load_module()
                        ext_onoff  = 'off'
                        ext_class  = ext_module._class()
                        print('Functions Loading ... "' + ext_script + '" (' + ext_class.func_name + ') _class.func_proc')
                        ext_version     = ext_class.version
                        ext_func_name   = ext_class.func_name
                        ext_func_ver    = ext_class.func_ver
                        ext_func_auth   = ext_class.func_auth
                        ext_function    = ext_class.function
                        ext_func_reset  = ext_class.func_reset
                        ext_func_proc   = ext_class.func_proc
                        #print(ext_version, ext_func_auth, )

                        # コード認証
                        auth = False
                        if   (secure_level == 'low') or (secure_level == 'medium'):
                            if (ext_func_auth == ''):
                                auth = '1' #注意
                                if (secure_level != 'low'):
                                    res_load_msg += '"' + ext_script + '"が認証されていません。(Warning!)' + '\n'
                            else:
                                auth = qRiKi_key.decryptText(text=ext_func_auth)
                                if  (auth != ext_func_name + '-' + ext_func_ver):
                                    #print(ext_func_auth, auth)
                                    if (secure_level == 'low'):
                                        auth = '1' #注意
                                        res_load_msg += '"' + ext_script + '"は改ざんされたコードです。(Warning!)' + '\n'
                                    else:
                                        res_load_msg += '"' + ext_script + '"は改ざんされたコードです。Loadingはキャンセルされます。' + '\n'
                                        res_load_all = False
                                else:
                                    auth = '2' #認証
                                    ext_onoff  = 'on'
                        else:
                            if (ext_func_auth == ''):
                                res_load_msg += '"' + ext_script + '"が認証されていません。Loadingはキャンセルされます。' + '\n'
                                res_load_all = False
                            else:
                                auth = qRiKi_key.decryptText(text=ext_func_auth)
                                if  (auth != ext_func_name + '-' + ext_func_ver):
                                    #print(ext_func_auth, auth)
                                    res_load_msg += '"' + ext_script + '"は改ざんされたコードです。Loadingはキャンセルされます。' + '\n'
                                    res_load_all = False
                                else:
                                    auth = '2' #認証
                                    ext_onoff  = 'on'

                        if (auth != False):
                            module_dic = {}
                            module_dic['script']     = ext_script
                            module_dic['module']     = ext_module
                            module_dic['onoff']      = ext_onoff
                            module_dic['class']      = ext_class
                            module_dic['func_name']  = ext_func_name
                            module_dic['func_ver']   = ext_func_ver
                            module_dic['func_auth']  = ext_func_auth
                            module_dic['function']   = ext_function
                            module_dic['func_reset'] = ext_func_reset
                            module_dic['func_proc']  = ext_func_proc
                            self.function_modules.append(module_dic)

                    except Exception as e:
                        print(e)

        return res_load_all, res_load_msg

    def functions_reset(self, ):
        res_reset_all = True
        res_reset_msg = ''
        #print('Reset functions ... ')

        for module_dic in self.function_modules:
            ext_script     = module_dic['script']
            ext_func_name  = module_dic['func_name']
            ext_func_reset = module_dic['func_reset']
            print('Functions Reset   ... "' + ext_script + '" (' + ext_func_name + ') _class.func_reset')
            try:
                res = False
                res = ext_func_reset()
            except:
                pass
            if (res == False):
                module_dic['onoff'] = 'off'
                res_reset_all = False
                res_reset_msg += ext_func_name + 'のリセット中にエラーがありました。' + '\n'

        return res_reset_all, res_reset_msg

    def functions_unload(self, ):
        res_unload_all = True
        res_unload_msg = ''
        #print('Unload functions ... ')

        for module_dic in self.function_modules:
            ext_script    = module_dic['script']
            ext_func_name = module_dic['func_name']
            ext_module    = module_dic['module']
            ext_class     = module_dic['class']
            ext_func_proc = module_dic['func_proc']
            print('Functions Unload  ... "' + ext_script + '" (' + ext_func_name + ') _class.func_proc')

            try:
                #del ext_func_proc
                del ext_class
                del ext_module
            except:
                res_unload_all = False
                res_unload_msg += ext_func_name + 'の開放中にエラーがありました。' + '\n'

        self.function_modules = []

        return res_unload_all, res_unload_msg



if __name__ == '__main__':

        #botFunc = speech_bot_function.botFunction()
        botFunc = botFunction()

        if (True):
            
            if True:
                #res, msg = openaiAPI.functions_load(functions_path='_extensions/function/', secure_level='medium', )
                res, msg = botFunc.functions_load(
                    functions_path='_extensions/function/', secure_level='low', )
                if (res != True) or (msg != ''):
                    print(msg)
                    print()
 
            if True:
                res, msg = botFunc.functions_reset()
                if (res != True) or (msg != ''):
                    print(msg)
                    print()

            if True:
                res, msg = botFunc.functions_unload()
                if (res != True) or (msg != ''):
                    print(msg)
                    print()


