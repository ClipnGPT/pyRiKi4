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

import json

import queue
from PIL import ImageGrab, Image

import google.generativeai as genai
#import google.ai.generativelanguage as glm



# gemini チャットボット
import speech_bot_gemini_key  as gemini_key



class _geminiAPI:

    def __init__(self, ):
        self.log_queue              = None
        self.bot_auth               = None

        self.temperature            = 0.8
        self.timeOut                = 60

        self.gemini_api_type        = 'gemini'
        self.gemini_default_gpt     = 'auto'
        self.gemini_default_class   = 'auto'
        self.gemini_auto_continue   = 3
        self.gemini_max_step        = 10
        self.gemini_max_assistant   = 5
       
        self.gemini_key_id          = None

        self.gemini_a_enable        = False
        self.gemini_a_nick_name     = ''
        self.gemini_a_model         = None
        self.gemini_a_token         = 0

        self.gemini_b_enable        = False
        self.gemini_b_nick_name     = ''
        self.gemini_b_model         = None
        self.gemini_b_token         = 0

        self.history                = []

        self.seq                    = 0
        self.reset()

    def init(self, log_queue=None, ):
        self.log_queue = log_queue
        return True

    def reset(self, ):
        self.history                = []
        return True

    def print(self, session_id='0', text='', ):
        print(text, flush=True)
        if (session_id == '0') and (self.log_queue is not None):
            try:
                self.log_queue.put(['chatBot', text + '\n'])
            except:
                pass

    def stream(self, session_id='0', text='', ):
        print(text, end='', flush=True)
        if (session_id == '0') and (self.log_queue is not None):
            try:
                self.log_queue.put(['chatBot', text])
            except:
                pass

    def authenticate(self, api,
                     gemini_api_type,
                     gemini_default_gpt, gemini_default_class,
                     gemini_auto_continue,
                     gemini_max_step, gemini_max_assistant,

                     gemini_key_id,

                     gemini_a_nick_name, gemini_a_model, gemini_a_token, 
                     gemini_b_nick_name, gemini_b_model, gemini_b_token, 
                    ):

        # 設定

        # 認証
        self.bot_auth                 = None

        self.gemini_default_gpt       = gemini_default_gpt
        self.gemini_default_class     = gemini_default_class
        if (str(gemini_auto_continue) != 'auto'):
            self.gemini_auto_continue = int(gemini_auto_continue)
        if (str(gemini_max_step)      != 'auto'):
            self.gemini_max_step      = int(gemini_max_step)
        if (str(gemini_max_assistant) != 'auto'):
            self.gemini_max_assistant = int(gemini_max_assistant)

        # gemini チャットボット
        if (gemini_a_nick_name != ''):
            self.gemini_a_enable     = False
            self.gemini_a_nick_name  = gemini_a_nick_name
            self.gemini_a_model      = gemini_a_model
            self.gemini_a_token      = int(gemini_a_token)

        if (gemini_b_nick_name != ''):
            self.gemini_b_enable     = False
            self.gemini_b_nick_name  = gemini_b_nick_name
            self.gemini_b_model      = gemini_b_model
            self.gemini_b_token      = int(gemini_b_token)

        # API-KEYの設定
        genai.configure(api_key=gemini_key_id, ) 

        # モデル一覧
        hit = False
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                model = m.name.replace('models/', '')
                if (model == self.gemini_a_model):
                    print(model)
                    self.gemini_a_enable = True
                    hit = True
                if (model == self.gemini_b_model):
                    print(model)
                    self.gemini_b_enable = True
                    hit = True

        if (hit == True):
            self.bot_auth = True
            return True
        else:
            return False

    def setTimeOut(self, timeOut=60, ):
        self.timeOut = timeOut

    def history_add(self, history=[], sysText=None, reqText=None, inpText='こんにちは', ):
        res_history = history

        # sysText, reqText, inpText -> history
        if (sysText is None):
            sysText = 'あなたは教師のように話す賢いアシスタントです。'
        if (sysText.strip() != ''):
            if (len(res_history) > 0):
                if (sysText.strip() != res_history[0]['content'].strip()):
                    res_history = []
            if (len(res_history) == 0):
                self.seq += 1
                dic = {'seq': self.seq, 'time': time.time(), 'role': 'system', 'name': '', 'content': sysText.strip() }
                res_history.append(dic)
        if (reqText is not None):
            if (reqText.strip() != ''):
                self.seq += 1
                dic = {'seq': self.seq, 'time': time.time(), 'role': 'user', 'name': '', 'content': reqText.strip() }
                res_history.append(dic)
        if (inpText.strip() != ''):
            if (inpText.rstrip() != ''):
                self.seq += 1
                dic = {'seq': self.seq, 'time': time.time(), 'role': 'user', 'name': '', 'content': inpText.rstrip() }
                res_history.append(dic)

        return res_history

    def history_zip1(self, history=[]):
        res_history = history

        for h in reversed(range(len(res_history))):
            tm = res_history[h]['time']
            if ((time.time() - tm) > 900): #15分で忘れてもらう
                if (h != 0):
                    del res_history[h]
                else:
                    if (res_history[0]['role'] != 'system'):
                        del res_history[0]

        return res_history

    def history_zip2(self, history=[], leave_count=4, ):
        res_history = history

        if (len(res_history) > 6):
            for h in reversed(range(2, len(res_history) - leave_count)):
                del res_history[h]

        return res_history

    def chatBot(self, chat_class='auto', model_select='auto',
                session_id='0', history=[], function_modules=[],
                sysText=None, reqText=None, inpText='こんにちは', 
                filePath=[],
                temperature=0.8, maxStep=10, inpLang='ja-JP', outLang='ja-JP', ):

        # 戻り値
        res_text        = ''
        res_path        = ''
        res_files       = []
        res_name        = None
        res_api         = None
        res_history     = history

        if (self.bot_auth is None):
            self.print(session_id, ' Gemini : Not Authenticate Error !')
            return res_text, res_path, res_name, res_api, res_history

        # tools
        tools = []
        for module_dic in function_modules:
            func_dic = module_dic['function']
            func_str = json.dumps(func_dic, ensure_ascii=False, )
            func_str = func_str.replace('"type"', '"type_"')
            func_str = func_str.replace('"object"', '"OBJECT"')
            func_str = func_str.replace('"string"', '"STRING"')
            func     = json.loads(func_str)
            tools.append(func)

        # history 追加・圧縮 (古いメッセージ)
        res_history = self.history_add(history=res_history, sysText=sysText, reqText=reqText, inpText=inpText, )
        res_history = self.history_zip1(history=res_history, )

        # 送信データ
        msg_text = ''
        if (len(res_history) <= 1):
            if (reqText is not None) and (reqText != ''):
                msg_text += reqText + '\n'
        msg_text += inpText

        request = []
        request.append(msg_text)

        # 過去メッセージ追加
        if (len(res_history) > 1):
            msg_text += '\n'
            msg_text += "''' ここから過去の会話履歴です。\n"
            for m in range(len(res_history) - 1):
                role    = res_history[m].get('role','')
                content = res_history[m].get('content','')
                name    = res_history[m].get('name','')
                if (role != 'system'):
                    # 全てユーザーメッセージにて処理
                    if (name is None) or (name == ''):
                        msg_text += '(' + role + ')' + '\n' + content + '\n'
                    else:
                        if (role == 'function_call'):
                            msg_text += '(function ' + name + ' call)'  + '\n' + content + '\n'
                        else:
                            msg_text += '(function ' + name + ' result) ' + '\n' + content + '\n'
            msg_text += "''' ここまで過去の会話履歴です。\n"

        # モデル
        if (model_select == 'auto'):
            if (res_api is None):
                if (self.gemini_a_nick_name != ''):
                    if (inpText.strip()[:len(self.gemini_a_nick_name)+1].lower() == (self.gemini_a_nick_name.lower() + ',')):
                        inpText = inpText.strip()[len(self.gemini_a_nick_name)+1:]
                        res_name = self.gemini_a_nick_name
                        res_api  = self.gemini_a_model
                if (self.gemini_b_nick_name != ''):
                    if (inpText.strip()[:len(self.gemini_b_nick_name)+1].lower() == (self.gemini_b_nick_name.lower() + ',')):
                        inpText = inpText.strip()[len(self.gemini_b_nick_name)+1:]
                        res_name = self.gemini_b_nick_name
                        res_api  = self.gemini_b_model
        if (res_api is None):
            if (len(filePath) == 0):
                        res_name = self.gemini_a_nick_name
                        res_api  = self.gemini_a_model
            else:
                if (self.gemini_b_nick_name != ''):
                        res_name = self.gemini_b_nick_name
                        res_api  = self.gemini_b_model
                else:
                        res_name = self.gemini_a_nick_name
                        res_api  = self.gemini_a_model

        # gemini 1.5 強制！
        res_name = self.gemini_b_nick_name
        res_api  = self.gemini_b_model

        # gemini
        gemini = genai.GenerativeModel( model_name=res_api,
                                        system_instruction=sysText, tools=tools, )

        # # ファイル削除
        # files = genai.list_files()
        # for f in files:
        #    self.print(session_id, f"Gemini :'Delete file { f.name }.")
        #    genai.delete_file(f.name)

        # ファイル添付
        for file_name in filePath:
            if (os.path.isfile(file_name)):
                #if (file_name[-4:].lower() in ['.jpg', '.png']):
                #    img = Image.open(file_name)
                #    request.append(img)
                #else:

                    # 確認
                    hit = False
                    up_files = genai.list_files()
                    for upf in up_files:
                        if (upf.display_name == os.path.basename(file_name)):
                            hit = True
                            upload_obj = genai.get_file(upf.name)
                            request.append(upload_obj)
                            break

                    if (hit == False):

                        # 送信
                        self.print(session_id, f" Gemini : Upload file '{ file_name }'.")
                        upload_file = genai.upload_file(file_name, display_name=os.path.basename(file_name), )
                        upload_obj  = genai.get_file(upload_file.name)

                        # 待機
                        self.print(session_id, f" Gemini : Upload processing ... '{ upload_file.name }'")
                        chkTime = time.time()
                        while ((time.time() - chkTime) < 120) and (upload_file.state.name == "PROCESSING"):
                            time.sleep(5.00)
                        if (upload_file.state.name == "PROCESSING"):
                            self.print(session_id, ' Gemini : Upload timeout. (120s)')
                            return res_text, res_path, res_name, res_api, res_history

                        # 完了
                        self.print(session_id, ' Gemini : Upload complete.')
                        request.append(upload_obj)

        # gemini
        #chat = gemini.start_chat(history=history, )
        chat = gemini.start_chat(history=[], )
        if (session_id == '0'):
            stream = True
        else:
            stream = False

        # 実行ループ
        n = 0
        function_name = ''
        while (function_name != 'exit') and (n < int(maxStep)):

            # 結果
            res_role      = None
            res_content   = None
            tool_calls    = []

            # GPT
            n += 1
            self.print(session_id, f" Gemini : { res_api }, pass={ n }, ")

            # 結果
            content       = {"role": "user", "parts": request }
            response      = chat.send_message(content=content, stream=stream, )
            content_text  = None
            content_parts = None

            # Stream 表示
            if (stream == True):
                chkTime     = time.time()
                for chunk in response:
                    if ((time.time() - chkTime) > self.timeOut):
                        break

                    content_text = chunk.candidates[0].content.parts[0].text
                    if (content_text is not None) and (content_text != ''):
                        self.stream(session_id, content_text)
                        if (res_content is None):
                            res_role    = 'assistant'
                            res_content = ''
                        res_content += content_text

                    else:
                        content_parts = chunk.candidates[0].content.parts
                        if (content_parts is not None):
                            try:
                                for parts in content_parts:
                                    f_name   = parts.function_call.name
                                    f_args   = parts.function_call.args
                                    f_kwargs = None
                                    if (f_args is not None):
                                        json_dic = {}
                                        for key,value in f_args.items():
                                            json_dic[key] = value
                                        f_kwargs = json.dumps(json_dic, ensure_ascii=False, )
                                    tool_calls.append({"id": parts, "type": "function", "function": { "name": f_name, "arguments": f_kwargs } })
                            except Exception as e:
                                print(e)

                # 改行
                if (res_content is not None):
                    self.print(session_id, )

            # response 結果
            if (stream == False):
                    content_text = response.candidates[0].content.parts[0].text
                    if (content_text is not None) and (content_text != ''):
                        res_role    = 'assistant'
                        res_content = content_text

                    else:
                        content_parts = response.candidates[0].content.parts
                        if (content_parts is not None):
                            try:
                                for parts in content_parts:
                                    f_name   = parts.function_call.name
                                    f_args   = parts.function_call.args
                                    f_kwargs = None
                                    if (f_args is not None):
                                        json_dic = {}
                                        for key,value in f_args.items():
                                            json_dic[key] = value
                                        f_kwargs = json.dumps(json_dic, ensure_ascii=False, )
                                    tool_calls.append({"id": parts, "type": "function", "function": { "name": f_name, "arguments": f_kwargs } })
                            except Exception as e:
                                print(e)

            # function 指示?
            if (len(tool_calls) > 0):
                self.print(session_id, )

                # メッセージ格納
                request = []
                #request.append(inpText)
                #if (content_parts is not None):
                #    for parts in content_parts:
                #        request.append(parts)

                for tc in tool_calls:
                    f_id     = tc.get('id')
                    f_name   = tc['function'].get('name')
                    f_kwargs = tc['function'].get('arguments')

                    hit = False

                    for module_dic in function_modules:
                        if (f_name == module_dic['func_name']):
                            hit = True
                            self.print(session_id, f" Gemini :   function_call '{ module_dic['script'] }' ({ f_name })")
                            self.print(session_id, f" Gemini :   → { f_kwargs }")

                            # メッセージ追加格納
                            self.seq += 1
                            dic = {'seq': self.seq, 'time': time.time(), 'role': 'function_call', 'name': f_name, 'content': f_kwargs }
                            res_history.append(dic)

                            # function 実行
                            try:
                                ext_func_proc  = module_dic['func_proc']
                                res_json = ext_func_proc( f_kwargs )
                            except Exception as e:
                                print(e)
                                # エラーメッセージ
                                dic = {}
                                dic['error'] = e 
                                res_json = json.dumps(dic, ensure_ascii=False, )

                            # tool_result
                            self.print(session_id, f" Gemini :   → { res_json }")
                            self.print(session_id, )

                            # メッセージ追加格納
                            res_dic  = json.loads(res_json)
                            res_list = []
                            for key,value in res_dic.items():
                                res_list.append({ "key": key, "value": { "string_value": value } })
                            parts = {
                                        "function_response": {
                                            "name": f_name, 
                                            "response": {
                                                "fields": res_list
                                            }
                                        }
                                    }
                            request.append(parts)
  
                            self.seq += 1
                            dic = {'seq': self.seq, 'time': time.time(), 'role': 'function', 'name': f_name, 'content': res_json }
                            res_history.append(dic)

                            # パス情報確認
                            try:
                                dic  = json.loads(res_json)
                                path = dic['image_path']
                                if (path is None):
                                    path = dic.get('excel_path')
                                if (path is not None):
                                    res_path = path
                                    res_files.append(path)
                                    res_files = list(set(res_files))
                            except:
                                pass

                            break

                    if (hit == False):
                        self.print(session_id, f" Gemini :   function_call Error ! ({ f_name })")
                        print(res_role, res_content, f_name, f_kwargs, )
                        break

            # GPT 会話終了
            elif (res_role == 'assistant') and (res_content is not None):
                function_name   = 'exit'
                self.print(session_id, f" Gemini : { res_name.lower() } complite.")

        if (res_content is not None):
            #self.print(session_id, res_content.rstrip())
            res_text += res_content.rstrip() + '\n'

        #res_history = chat.history

        # History 追加格納
        self.seq += 1
        dic = {'seq': self.seq, 'time': time.time(), 'role': 'assistant', 'name': '', 'content': res_text }
        res_history.append(dic)

        # # ファイル削除
        # files = genai.list_files()
        # for f in files:
        #    self.print(session_id, f"Gemini :'Delete file { f.name }.")
        #    genai.delete_file(f.name)

        # 文書成形
        if (res_text != ''):
            text = res_text
            text = text.replace('\r', '')

            text = text.replace('。', '。\n')
            text = text.replace('？', '？\n')
            text = text.replace('！', '！\n')
            text = text.replace('。\n」','。」')
            text = text.replace('。\n"' ,'。"')
            text = text.replace("。\n'" ,"。'")
            text = text.replace('？\n」','？」')
            text = text.replace('？\n"' ,'？"')
            text = text.replace("？\n'" ,"？'")
            text = text.replace('！\n」','！」')
            text = text.replace('！\n"' ,'！"')
            text = text.replace("！\n'" ,"！'")

            text = text.replace('\n \n ' ,'\n')
            text = text.replace('\n \n' ,'\n')

            hit = True
            while (hit == True):
                if (text.find('\n\n')>0):
                    hit = True
                    text = text.replace('\n\n', '\n')
                else:
                    hit = False
            text = text.strip()

            res_text    = text
        else:
            res_text = '!'

        return res_text, res_path, res_files, res_name, res_api, res_history



if __name__ == '__main__':

        #geminiAPI = speech_bot_gemini.ChatBotAPI()
        geminiAPI = _geminiAPI()

        api_type = gemini_key.getkey('gemini','gemini_api_type')
        print(api_type)

        log_queue = queue.Queue()
        res = geminiAPI.init(log_queue=log_queue, )

        res = geminiAPI.authenticate('google',
                            api_type,
                            gemini_key.getkey('gemini','gemini_default_gpt'), gemini_key.getkey('gemini','gemini_default_class'),
                            gemini_key.getkey('gemini','gemini_auto_continue'),
                            gemini_key.getkey('gemini','gemini_max_step'), gemini_key.getkey('gemini','gemini_max_assistant'),
                            gemini_key.getkey('gemini','gemini_key_id'),
                            gemini_key.getkey('gemini','gemini_a_nick_name'), gemini_key.getkey('gemini','gemini_a_model'), gemini_key.getkey('gemini','gemini_a_token'),
                            gemini_key.getkey('gemini','gemini_b_nick_name'), gemini_key.getkey('gemini','gemini_b_model'), gemini_key.getkey('gemini','gemini_b_token'),
                            )
        print('authenticate:', res, )
        if (res == True):
            
            function_modules = []
            filePath         = []

            if True:
                import    speech_bot_function
                botFunc = speech_bot_function.botFunction()

                #res, msg = openaiAPI.functions_load(functions_path='_extensions/openai_gpt/', secure_level='medium', )
                res, msg = botFunc.functions_load(
                    functions_path='_extensions/openai_gpt/', secure_level='low', )
                if (res != True) or (msg != ''):
                    print(msg)
                    print()

                for module_dic in botFunc.function_modules:
                    if (module_dic['onoff'] == 'on'):
                        function_modules.append(module_dic)

            if True:
                sysText = None
                reqText = ''
                #inpText = 'わたしの名前は「こんさん」です'
                inpText = '兵庫県三木市の天気？'
                print()
                print('[Request]')
                print(reqText, inpText )
                print()
                res_text, res_path, res_files, res_name, res_api, geminiAPI.history = \
                    geminiAPI.chatBot(  chat_class='chat', model_select='auto', 
                                        session_id='0', history=geminiAPI.history, function_modules=function_modules,
                                        sysText=sysText, reqText=reqText, inpText=inpText, filePath=filePath,
                                        inpLang='ja', outLang='ja', )
                print()
                print(f"[{ res_name }] ({ res_api })")
                print(str(res_text))
                print()

            if False:
                sysText = None
                reqText = ''
                inpText = 'わたしの名前はわかりますか？'
                print()
                print('[Request]')
                print(reqText, inpText )
                print()
                res_text, res_path, res_files, res_name, res_api, geminiAPI.history = \
                    geminiAPI.chatBot(  chat_class='chat', model_select='auto', 
                                        session_id='0', history=geminiAPI.history, function_modules=function_modules,
                                        sysText=sysText, reqText=reqText, inpText=inpText, filePath=filePath,
                                        inpLang='ja', outLang='ja', )
                print()
                print(f"[{ res_name }] ({ res_api })")
                print(str(res_text))
                print()

            if False:
                sysText = None
                reqText = ''
                #inpText = 'おはようございます。'
                inpText = 'この画像はなんだと思いますか？'
                filePath = ['_icons/dog.jpg', '_icons/kyoto.png']
                #inpText = '議事録作成してください。'
                #filePath = ["C:/Users/admin/Desktop/output-1a.mp3"]
                print()
                print('[Request]')
                print(reqText, inpText )
                print()
                res_text, res_path, res_files, res_name, res_api, geminiAPI.history = \
                    geminiAPI.chatBot(  chat_class='chat', model_select='auto', 
                                        session_id='0', history=geminiAPI.history, function_modules=function_modules,
                                        sysText=sysText, reqText=reqText, inpText=inpText, filePath=filePath,
                                        inpLang='ja', outLang='ja', )
                print()
                print(f"[{ res_name }] ({ res_api })")
                print(str(res_text))
                print()

            if True:
                print('[History]')
                for h in range(len(geminiAPI.history)):
                    print(geminiAPI.history[h])
                geminiAPI.history = []



