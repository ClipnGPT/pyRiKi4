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
import base64
import subprocess



# ollama チャットボット
import ollama

import speech_bot_ollama_key  as ollama_key



# base64 encode
def base64_encode(file_path):
    with open(file_path, "rb") as input_file:
        return base64.b64encode(input_file.read()).decode('utf-8')



class _ollamaAPI:

    def __init__(self, ):
        self.log_queue              = None
        self.bot_auth               = None

        self.temperature            = 0.8
        self.timeOut                = 120

        self.ollama_api_type        = 'ollama'
        self.ollama_default_gpt     = 'auto'
        self.ollama_default_class   = 'auto'
        self.ollama_auto_continue   = 3
        self.ollama_max_step        = 10
        self.ollama_max_assistant   = 5
       
        self.ollama_server          = 'localhost'
        self.ollama_port            = '11434'

        self.ollama_a_enable        = False
        self.ollama_a_nick_name     = ''
        self.ollama_a_model         = None
        self.ollama_a_token         = 0

        self.ollama_b_enable        = False
        self.ollama_b_nick_name     = ''
        self.ollama_b_model         = None
        self.ollama_b_token         = 0

        self.ollama_v_enable        = False
        self.ollama_v_nick_name     = ''
        self.ollama_v_model         = None
        self.ollama_v_token         = 0

        self.ollama_x_enable        = False
        self.ollama_x_nick_name     = ''
        self.ollama_x_model         = None
        self.ollama_x_token         = 0

        self.history                = []

        self.seq                    = 0
        self.reset()

    def init(self, log_queue=None, ):
        self.log_queue = log_queue
        return True

    def reset(self, ):
        self.history                = []
        return True

    def print(self, session_id='admin', text='', ):
        print(text, flush=True)
        if (session_id == 'admin') and (self.log_queue is not None):
            try:
                self.log_queue.put(['chatBot', text + '\n'])
            except:
                pass

    def stream(self, session_id='admin', text='', ):
        print(text, end='', flush=True)
        if (session_id == 'admin') and (self.log_queue is not None):
            try:
                self.log_queue.put(['chatBot', text])
            except:
                pass

    def authenticate(self, api,
                     ollama_api_type,
                     ollama_default_gpt, ollama_default_class,
                     ollama_auto_continue,
                     ollama_max_step, ollama_max_assistant,

                     ollama_server, ollama_port,

                     ollama_a_nick_name, ollama_a_model, ollama_a_token, 
                     ollama_b_nick_name, ollama_b_model, ollama_b_token, 
                     ollama_v_nick_name, ollama_v_model, ollama_v_token, 
                     ollama_x_nick_name, ollama_x_model, ollama_x_token, 
                    ):

        # 設定
        self.bot_auth                 = None

        self.ollama_default_gpt       = ollama_default_gpt
        self.ollama_default_class     = ollama_default_class
        if (str(ollama_auto_continue) != 'auto'):
            self.ollama_auto_continue = int(ollama_auto_continue)
        if (str(ollama_max_step)      != 'auto'):
            self.ollama_max_step      = int(ollama_max_step)
        if (str(ollama_max_assistant) != 'auto'):
            self.ollama_max_assistant = int(ollama_max_assistant)

        # ollama サーバー
        if (str(ollama_server) != 'auto'):
            self.ollama_server       = ollama_server
        if (str(ollama_port) != 'auto'):
            self.ollama_port         = ollama_port

        # 認証
        self.ollama_client = None
        self.ollama_models = []
        try:
            self.ollama_client = ollama.Client(host=f"http://{ self.ollama_server }:{ self.ollama_port }", )
            get_models  = self.ollama_client.list().get('models')
            for model in get_models:
                self.ollama_models.append(model.get('name'))
        except:
            print(' ollama  : server (' + self.ollama_server + ') not enabled! ')
            if (self.ollama_server == 'localhost'):
                self.ollama_client = None
            else:
                print(' ollama  : localhost try ... ')
                try:
                    del self.ollama_client
                    self.ollama_client = ollama.Client(host="http://localhost:11434", )
                    get_models  = self.ollama_client.list().get('models')
                    for model in get_models:
                        self.ollama_models.append(model.get('name'))
                    self.ollama_server = 'localhost'
                    self.ollama_port   = '11434'
                except:
                    self.ollama_client = None

        if (self.ollama_client is not None):

            # ollama チャットボット
            if (ollama_a_nick_name != ''):
                self.ollama_a_enable     = False
                self.ollama_a_nick_name  = ollama_a_nick_name
                self.ollama_a_model      = ollama_a_model
                self.ollama_a_token      = int(ollama_a_token)
                if (self.ollama_a_model in self.ollama_models):
                    self.ollama_a_enable = True
                    self.bot_auth        = True
                else:
                    try:
                        print(' ollama  : model download ... (' + self.ollama_a_model + ') ')
                        if (os.name == 'nt'):
                            try:
                                subprocess.Popen(['cmd.exe', '/c', 'ollama', 'pull', self.ollama_a_model, ])
                            except:
                                pass
                        self.ollama_client.pull(self.ollama_a_model, )
                        self.ollama_a_enable = True
                        self.bot_auth        = True
                        self.ollama_models.append(self.ollama_a_model)
                        print(' ollama  : model download complete.')
                    except:
                        print(' ollama  : model download error!')

            if (ollama_b_nick_name != ''):
                self.ollama_b_enable     = False
                self.ollama_b_nick_name  = ollama_b_nick_name
                self.ollama_b_model      = ollama_b_model
                self.ollama_b_token      = int(ollama_b_token)
                if (self.ollama_b_model in self.ollama_models):
                    self.ollama_b_enable = True
                    self.bot_auth        = True
                else:
                    try:
                        print(' ollama  : model download ... (' + self.ollama_b_model + ') ')
                        if (os.name == 'nt'):
                            try:
                                subprocess.Popen(['cmd.exe', '/c', 'ollama', 'pull', self.ollama_b_model, ])
                            except:
                                pass
                        self.ollama_client.pull(self.ollama_b_model, )
                        self.ollama_b_enable = True
                        self.bot_auth        = True
                        self.ollama_models.append(self.ollama_b_model)
                        print(' ollama  : model download complete.')
                    except:
                        print(' ollama  : model download error!')

            if (ollama_v_nick_name != ''):
                self.ollama_v_enable     = False
                self.ollama_v_nick_name  = ollama_v_nick_name
                self.ollama_v_model      = ollama_v_model
                self.ollama_v_token      = int(ollama_v_token)
                if (self.ollama_v_model in self.ollama_models):
                    self.ollama_v_enable = True
                    self.bot_auth        = True
                else:
                    try:
                        print(' ollama  : model download ... (' + self.ollama_v_model + ') ')
                        if (os.name == 'nt'):
                            try:
                                subprocess.Popen(['cmd.exe', '/c', 'ollama', 'pull', self.ollama_v_model, ])
                            except:
                                pass
                        self.ollama_client.pull(self.ollama_v_model, )
                        self.ollama_v_enable = True
                        self.bot_auth        = True
                        self.ollama_models.append(self.ollama_v_model)
                        print(' ollama  : model download complete.')
                    except:
                        print(' ollama  : model download error!')

            if (ollama_x_nick_name != ''):
                self.ollama_x_enable     = False
                self.ollama_x_nick_name  = ollama_x_nick_name
                self.ollama_x_model      = ollama_x_model
                self.ollama_x_token      = int(ollama_x_token)
                if (self.ollama_x_model in self.ollama_models):
                    self.ollama_x_enable = True
                    self.bot_auth        = True
                else:
                    try:
                        print(' ollama  : model download ... (' + self.ollama_x_model + ') ')
                        if (os.name == 'nt'):
                            try:
                                subprocess.Popen(['cmd.exe', '/c', 'ollama', 'pull', self.ollama_x_model, ])
                            except:
                                pass
                        self.ollama_client.pull(self.ollama_x_model, )
                        self.ollama_x_enable = True
                        self.bot_auth        = True
                        self.ollama_models.append(self.ollama_x_model)
                        print(' ollama  : model download complete.')
                    except:
                        print(' ollama  : model download error!')

        # 戻り値
        if (self.bot_auth == True):
            return True
        else:
            return False

    def setTimeOut(self, timeOut=60, ):
        self.timeOut = timeOut

    def text_replace(self, text='', ):
        if (text.strip() == ''):
            return ''

        text = text.replace('\r', '')

        text = text.replace('。', '。\n')
        text = text.replace('?', '?\n')
        text = text.replace('？', '?\n')
        text = text.replace('!', '!\n')
        text = text.replace('！', '!\n')
        text = text.replace('。\n」','。」')
        text = text.replace('。\n"' ,'。"')
        text = text.replace("。\n'" ,"。'")
        text = text.replace('?\n」','?」')
        text = text.replace('?\n"' ,'?"')
        text = text.replace("?\n'" ,"?'")
        text = text.replace('!\n」','!」')
        text = text.replace('!\n"' ,'!"')
        text = text.replace("!\n'" ,"!'")

        text = text.replace('\n \n ' ,'\n')
        text = text.replace('\n \n' ,'\n')

        hit = True
        while (hit == True):
            if (text.find('\n\n')>0):
                hit = True
                text = text.replace('\n\n', '\n')
            else:
                hit = False

        return text.strip()

    def history_add(self, history=[], sysText=None, reqText=None, inpText='こんにちは', ):
        res_history = history

        # sysText, reqText, inpText -> history
        if (sysText is not None) and (sysText.strip() != ''):
            if (len(res_history) > 0):
                if (sysText.strip() != res_history[0]['content'].strip()):
                    res_history = []
            if (len(res_history) == 0):
                self.seq += 1
                dic = {'seq': self.seq, 'time': time.time(), 'role': 'system', 'name': '', 'content': sysText.strip() }
                res_history.append(dic)
        if (reqText is not None) and (reqText.strip() != ''):
            self.seq += 1
            dic = {'seq': self.seq, 'time': time.time(), 'role': 'user', 'name': '', 'content': reqText.strip() }
            res_history.append(dic)
        if (inpText.strip() != ''):
            self.seq += 1
            dic = {'seq': self.seq, 'time': time.time(), 'role': 'user', 'name': '', 'content': inpText.rstrip() }
            res_history.append(dic)

        return res_history

    def history_zip1(self, history=[]):
        res_history = history

        if (len(res_history) > 0):
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

    def history2msg_text(self, history=[], ):
        # 過去メッセージ追加
        msg_text = ''
        if (len(history) > 2):
            msg_text += "''' これは過去の会話履歴です。\n"
            for m in range(len(history) - 2):
                role    = history[m+1].get('role','')
                content = history[m+1].get('content','')
                name    = history[m+1].get('name','')
                if (role != 'system'):
                    # 全てユーザーメッセージにて処理
                    if (name is None) or (name == ''):
                        msg_text += '(' + role + ')' + '\n' + content + '\n'
                    else:
                        if (role == 'function_call'):
                            msg_text += '(function ' + name + ' call)'  + '\n' + content + '\n'
                        else:
                            msg_text += '(function ' + name + ' result) ' + '\n' + content + '\n'
            msg_text += "''' 会話履歴はここまでです。\n"
            msg_text += "\n"
        m = len(history) - 1
        msg_text += history[m].get('content', '')
        #print(msg_text)

        return msg_text



    def files_check(self, filePath=[], ):
        upload_files = []
        image_urls   = []

        # filePath確認
        if (len(filePath) > 0):
            try:

                for file_name in filePath:
                    if (os.path.isfile(file_name)):
                        if (os.path.getsize(file_name) <= 20000000):

                            upload_files.append(file_name)
                            file_ext = os.path.splitext(file_name)[1][1:].lower()
                            if (file_ext in ('jpg', 'jpeg', 'png')):
                                base64_text = base64_encode(file_name)
                                if (file_ext in ('jpg', 'jpeg')):
                                    url = {"url": f"data:image/jpeg;base64,{base64_text}"}
                                    image_url = {'type':'image_url', 'image_url': url}
                                    image_urls.append(image_url)
                                if (file_ext == 'png'):
                                    url = {"url": f"data:image/png;base64,{base64_text}"}
                                    image_url = {'type':'image_url', 'image_url': url}
                                    image_urls.append(image_url)

            except Exception as e:
                print(e)

        return upload_files, image_urls



    def run_gpt(self, chat_class='chat', model_select='auto',
                nick_name=None, model_name=None,
                session_id='admin', history=[], function_modules=[],
                sysText=None, reqText=None, inpText='こんにちは',
                upload_files=[], image_urls=[], 
                temperature=0.8, max_step=10, jsonMode=False, ):

        # 戻り値
        res_text        = ''
        res_path        = ''
        res_files       = []
        res_name        = None
        res_api         = None
        res_history     = history

        if (self.bot_auth is None):
            self.print(session_id, ' ollama  : Not Authenticate Error !')
            return res_text, res_path, res_name, res_api, res_history

        # モデル 設定
        res_name = self.ollama_a_nick_name
        res_api  = self.ollama_a_model
        if  (chat_class == 'ollama'):
            if (self.ollama_b_enable == True):
                res_name = self.ollama_b_nick_name
                res_api  = self.ollama_b_model

        # モデル 補正 (assistant)
        if ((chat_class == 'assistant') \
        or  (chat_class == 'コード生成') \
        or  (chat_class == 'コード実行') \
        or  (chat_class == '文書検索') \
        or  (chat_class == '複雑な会話') \
        or  (chat_class == 'アシスタント') \
        or  (model_select == 'x')):
            if (self.ollama_x_enable == True):
                res_name = self.ollama_x_nick_name
                res_api  = self.ollama_x_model

        # model 指定
        if (self.ollama_a_nick_name != ''):
            if (inpText.strip()[:len(self.ollama_a_nick_name)+1].lower() == (self.ollama_a_nick_name.lower() + ',')):
                inpText = inpText.strip()[len(self.ollama_a_nick_name)+1:]
        if (self.ollama_b_nick_name != ''):
            if (inpText.strip()[:len(self.ollama_b_nick_name)+1].lower() == (self.ollama_b_nick_name.lower() + ',')):
                inpText = inpText.strip()[len(self.ollama_b_nick_name)+1:]
                if (self.ollama_b_enable == True):
                        res_name = self.ollama_b_nick_name
                        res_api  = self.ollama_b_model
        if (self.ollama_v_nick_name != ''):
            if (inpText.strip()[:len(self.ollama_v_nick_name)+1].lower() == (self.ollama_v_nick_name.lower() + ',')):
                inpText = inpText.strip()[len(self.ollama_v_nick_name)+1:]
                if   (self.ollama_v_enable == True):
                    if  (len(image_urls) > 0) \
                    and (len(image_urls) == len(upload_files)):
                        res_name = self.ollama_v_nick_name
                        res_api  = self.ollama_v_model
                elif (self.ollama_x_enable == True):
                        res_name = self.ollama_x_nick_name
                        res_api  = self.ollama_x_model
        if (self.ollama_x_nick_name != ''):
            if (inpText.strip()[:len(self.ollama_x_nick_name)+1].lower() == (self.ollama_x_nick_name.lower() + ',')):
                inpText = inpText.strip()[len(self.ollama_x_nick_name)+1:]
                if   (self.ollama_x_enable == True):
                        res_name = self.ollama_x_nick_name
                        res_api  = self.ollama_x_model
                elif (self.ollama_b_enable == True):
                        res_name = self.ollama_b_nick_name
                        res_api  = self.ollama_b_model
        if   (inpText.strip()[:5].lower() == ('riki,')):
            inpText = inpText.strip()[5:]
            if   (self.ollama_x_enable == True):
                        res_name = self.ollama_x_nick_name
                        res_api  = self.ollama_x_model
            elif (self.ollama_b_enable == True):
                        res_name = self.ollama_b_nick_name
                        res_api  = self.ollama_b_model
        elif (inpText.strip()[:7].lower() == ('vision,')):
            inpText = inpText.strip()[7:]
            if   (self.ollama_v_enable == True):
                if  (len(image_urls) > 0) \
                and (len(image_urls) == len(upload_files)):
                        res_name = self.ollama_v_nick_name
                        res_api  = self.ollama_v_model
            elif (self.ollama_x_enable == True):
                        res_name = self.ollama_x_nick_name
                        res_api  = self.ollama_x_model
        elif (inpText.strip()[:10].lower() == ('assistant,')):
            inpText = inpText.strip()[10:]
            if   (self.ollama_x_enable == True):
                        res_name = self.ollama_x_nick_name
                        res_api  = self.ollama_x_model
            elif (self.ollama_b_enable == True):
                        res_name = self.ollama_b_nick_name
                        res_api  = self.ollama_b_model
        elif (inpText.strip()[:7].lower() == ('openai,')):
            inpText = inpText.strip()[7:]
        elif (inpText.strip()[:7].lower() == ('claude,')):
            inpText = inpText.strip()[7:]
        elif (inpText.strip()[:7].lower() == ('gemini,')):
            inpText = inpText.strip()[7:]
        elif (inpText.strip()[:11].lower() == ('perplexity,')):
            inpText = inpText.strip()[11:]
        elif (inpText.strip()[:5].lower() == ('pplx,')):
            inpText = inpText.strip()[5:]
        elif (inpText.strip()[:6].lower() == ('local,')):
            inpText = inpText.strip()[6:]

        # モデル 未設定時
        if (res_api is None):
            res_name = self.ollama_a_nick_name
            res_api  = self.ollama_a_model
            if (self.ollama_b_enable == True):
                if (len(upload_files) > 0) \
                or (len(inpText) > 1000):
                    res_name = self.ollama_b_nick_name
                    res_api  = self.ollama_b_model

        # モデル 補正 (vision)
        if  (len(image_urls) > 0) \
        and (len(image_urls) == len(upload_files)):
            if   (self.ollama_v_enable == True):
                res_name = self.ollama_v_nick_name
                res_api  = self.ollama_v_model
            elif (self.ollama_x_enable == True):
                res_name = self.ollama_x_nick_name
                res_api  = self.ollama_x_model

        # history 追加・圧縮 (古いメッセージ)
        res_history = self.history_add(history=res_history, sysText=sysText, reqText=reqText, inpText=inpText, )
        res_history = self.history_zip1(history=res_history, )

        # メッセージ作成
        #msg_text = self.history2msg_text(history=res_history, )

        print(' history = "", ')
        msg_text = ''
        if (sysText is not None) and (sysText != ''):
            msg_text += sysText + '\n'
        if (reqText is not None) and (reqText != ''):
            msg_text += reqText + '\n'
        msg_text += inpText
        messages = []

        # 画像無し
        if (len(image_urls) == 0) \
        or (len(image_urls) != len(upload_files)):
            msg = {"role": "user", "content": msg_text }
            messages.append(msg)

        # 画像あり
        else:
            images = []
            for file_name in upload_files:
                if (os.path.isfile(file_name)):
                    if (os.path.getsize(file_name) <= 20000000):
                        file_ext = os.path.splitext(file_name)[1][1:].lower()
                        if (file_ext in ('jpg', 'jpeg', 'png')):
                            images.append(file_name)
            msg = {"role": "user", "content": msg_text, "images":images }
            messages.append(msg)

        # ストリーム実行?
        if (session_id == 'admin'):
            stream = True
        else:
            stream = False
        print(' stream = False, ')
        stream = False

        # 実行ループ
        #try:
        if True:

            n = 0
            function_name = ''
            while (function_name != 'exit') and (n < int(max_step)):

                # 結果
                res_role      = None
                res_content   = None

                # GPT
                n += 1
                self.print(session_id, f" ollama  : { res_api }, pass={ n }, ")

                # 結果
                content_text = None
                response = self.ollama_client.chat(model=res_api, 
                                            messages=messages, 
                                            options={"temperature": 0 },
                                            stream=stream, )

                # Stream 表示
                if (stream == True):
                    try:
                        chkTime     = time.time()
                        for chunk in response:
                            if ((time.time() - chkTime) > self.timeOut):
                                break
                            #print(chunk)

                            content_text = response['message']['content']
                            if (content_text is not None) and (content_text != ''):
                                self.stream(session_id, content_text)
                                if (res_content is None):
                                    res_role    = 'assistant'
                                    res_content = ''
                                res_content += content_text

                        # 改行
                        if (res_content is not None):
                            self.print(session_id, )

                    except Exception as e:
                        print(e)

                # response 結果
                if (stream == False):
                    content_text = response['message']['content']
                    if (content_text is not None) and (content_text != ''):
                        res_role    = 'assistant'
                        res_content = content_text

                # GPT 会話終了
                #if (res_role == 'assistant') and (res_content is not None):
                function_name   = 'exit'
                self.print(session_id, f" ollama  : { res_name.lower() } complite.")

            # 正常回答
            if (res_content is not None):
                #self.print(session_id, res_content.rstrip())
                res_text += res_content.rstrip()

            # 異常回答
            else:
                self.print(session_id, ' ollama  : Error !')

            # History 追加格納
            if (res_text.strip() != ''):
                self.seq += 1
                dic = {'seq': self.seq, 'time': time.time(), 'role': 'assistant', 'name': '', 'content': res_text }
                res_history.append(dic)

        #except Exception as e:
        #    print(e)
        #    res_text = ''

        return res_text, res_path, res_files, res_name, res_api, res_history



    def chatBot(self, chat_class='auto', model_select='auto',
                session_id='admin', history=[], function_modules=[],
                sysText=None, reqText=None, inpText='こんにちは', 
                filePath=[],
                temperature=0.8, max_step=10, inpLang='ja-JP', outLang='ja-JP', ):

        # 戻り値
        res_text    = ''
        res_path    = ''
        res_files   = []
        nick_name   = None
        model_name  = None
        res_history = history

        if (sysText is None):
            sysText = 'あなたは美しい日本語を話す賢いアシスタントです。'

        if (self.bot_auth is None):
            self.print(session_id, ' ollama : Not Authenticate Error !')
            return res_text, res_path, nick_name, model_name, res_history

        # ファイル分離
        upload_files    = []
        image_urls      = []
        try:
            upload_files, image_urls = self.files_check(filePath=filePath, )
        except Exception as e:
            print(e)

        # 実行モデル判定
        #nick_name  = 'auto'
        #model_name = 'auto'

        # ollama
        res_text, res_path, res_files, nick_name, model_name, res_history = \
        self.run_gpt(   chat_class=chat_class, model_select=model_select,
                        nick_name=nick_name, model_name=model_name,
                        session_id=session_id, history=res_history, function_modules=function_modules,
                        sysText=sysText, reqText=reqText, inpText=inpText,
                        upload_files=upload_files, image_urls=image_urls,
                        temperature=temperature, max_step=max_step, )

        # 文書成形
        text = self.text_replace(text=res_text, )
        if (text.strip() != ''):
            res_text = text
        else:
            res_text = '!'

        return res_text, res_path, res_files, nick_name, model_name, res_history



if __name__ == '__main__':

        #ollamaAPI = speech_bot_ollama.ChatBotAPI()
        ollamaAPI = _ollamaAPI()

        api_type = ollama_key.getkey('ollama','ollama_api_type')
        print(api_type)

        log_queue = queue.Queue()
        res = ollamaAPI.init(log_queue=log_queue, )

        res = ollamaAPI.authenticate('ollama',
                            api_type,
                            ollama_key.getkey('ollama','ollama_default_gpt'), ollama_key.getkey('ollama','ollama_default_class'),
                            ollama_key.getkey('ollama','ollama_auto_continue'),
                            ollama_key.getkey('ollama','ollama_max_step'), ollama_key.getkey('ollama','ollama_max_assistant'),
                            ollama_key.getkey('ollama','ollama_server'), ollama_key.getkey('ollama','ollama_port'),
                            ollama_key.getkey('ollama','ollama_a_nick_name'), ollama_key.getkey('ollama','ollama_a_model'), ollama_key.getkey('ollama','ollama_a_token'),
                            ollama_key.getkey('ollama','ollama_b_nick_name'), ollama_key.getkey('ollama','ollama_b_model'), ollama_key.getkey('ollama','ollama_b_token'),
                            ollama_key.getkey('ollama','ollama_v_nick_name'), ollama_key.getkey('ollama','ollama_v_model'), ollama_key.getkey('ollama','ollama_v_token'),
                            ollama_key.getkey('ollama','ollama_x_nick_name'), ollama_key.getkey('ollama','ollama_x_model'), ollama_key.getkey('ollama','ollama_x_token'),
                            )
        print('authenticate:', res, )
        if (res == True):
            
            function_modules = []
            filePath         = []

            #if True:
            #    import    speech_bot_function
            #    botFunc = speech_bot_function.botFunction()

            #    res, msg = botFunc.functions_load(
            #        functions_path='_extensions/function/', secure_level='low', )
            #    if (res != True) or (msg != ''):
            #        print(msg)
            #        print()

            #    for module_dic in botFunc.function_modules:
            #        if (module_dic['onoff'] == 'on'):
            #            function_modules.append(module_dic)

            if True:
                sysText = None
                reqText = ''
                inpText = 'mini,おはようございます。'
                #inpText = 'phi3,おはようございます。'
                print()
                print('[Request]')
                print(reqText, inpText )
                print()
                res_text, res_path, res_files, res_name, res_api, ollamaAPI.history = \
                    ollamaAPI.chatBot(  chat_class='auto', model_select='auto', 
                                        session_id='admin', history=ollamaAPI.history, function_modules=function_modules,
                                        sysText=sysText, reqText=reqText, inpText=inpText, filePath=filePath,
                                        inpLang='ja', outLang='ja', )
                print()
                print(f"[{ res_name }] ({ res_api })")
                print(str(res_text))
                print()

            if True:
                sysText = None
                reqText = ''
                inpText = '画像検索に利用できるように、この画像の内容を箇条書きで教えてください。'
                filePath = ['_icons/dog.jpg']
                #filePath = ['_icons/dog.jpg', '_icons/kyoto.png']
                print()
                print('[Request]')
                print(reqText, inpText )
                print()
                res_text, res_path, res_files, res_name, res_api, ollamaAPI.history = \
                    ollamaAPI.chatBot(  chat_class='auto', model_select='auto', 
                                        session_id='admin', history=ollamaAPI.history, function_modules=function_modules,
                                        sysText=sysText, reqText=reqText, inpText=inpText, filePath=filePath,
                                        inpLang='ja', outLang='ja', )
                print()
                print(f"[{ res_name }] ({ res_api })")
                print(str(res_text))
                print()

            if False:
                print('[History]')
                for h in range(len(ollamaAPI.history)):
                    print(ollamaAPI.history[h])
                ollamaAPI.history = []



