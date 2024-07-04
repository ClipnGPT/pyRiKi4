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



# anthropic(claude) チャットボット
import anthropic

import speech_bot_claude_key  as claude_key



# base64 encode
def base64_encode(file_path):
    with open(file_path, "rb") as input_file:
        return base64.b64encode(input_file.read()).decode('utf-8')



class _claudeAPI:

    def __init__(self, ):
        self.log_queue              = None
        self.bot_auth               = None

        self.temperature            = 0.8
        self.timeOut                = 60

        self.claude_api_type        = 'claude'
        self.claude_default_gpt     = 'auto'
        self.claude_default_class   = 'auto'
        self.claude_auto_continue   = 3
        self.claude_max_step        = 10
        self.claude_max_assistant   = 5
       
        self.claude_key_id          = None

        self.claude_a_enable        = False
        self.claude_a_nick_name     = ''
        self.claude_a_model         = None
        self.claude_a_token         = 0

        self.claude_b_enable        = False
        self.claude_b_nick_name     = ''
        self.claude_b_model         = None
        self.claude_b_token         = 0

        self.claude_v_enable        = False
        self.claude_v_nick_name     = ''
        self.claude_v_model         = None
        self.claude_v_token         = 0

        self.claude_x_enable        = False
        self.claude_x_nick_name     = ''
        self.claude_x_model         = None
        self.claude_x_token         = 0

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
                     claude_api_type,
                     claude_default_gpt, claude_default_class,
                     claude_auto_continue,
                     claude_max_step, claude_max_assistant,

                     claude_key_id,

                     claude_a_nick_name, claude_a_model, claude_a_token, 
                     claude_b_nick_name, claude_b_model, claude_b_token, 
                     claude_v_nick_name, claude_v_model, claude_v_token, 
                     claude_x_nick_name, claude_x_model, claude_x_token, 
                    ):

        # 設定

        # 認証
        self.bot_auth                 = None

        self.claude_default_gpt       = claude_default_gpt
        self.claude_default_class     = claude_default_class
        if (str(claude_auto_continue) != 'auto'):
            self.claude_auto_continue = int(claude_auto_continue)
        if (str(claude_max_step)      != 'auto'):
            self.claude_max_step      = int(claude_max_step)
        if (str(claude_max_assistant) != 'auto'):
            self.claude_max_assistant = int(claude_max_assistant)

        # claude チャットボット
        if (claude_a_nick_name != ''):
            self.claude_a_enable     = False
            self.claude_a_nick_name  = claude_a_nick_name
            self.claude_a_model      = claude_a_model
            self.claude_a_token      = int(claude_a_token)

        if (claude_b_nick_name != ''):
            self.claude_b_enable     = False
            self.claude_b_nick_name  = claude_b_nick_name
            self.claude_b_model      = claude_b_model
            self.claude_b_token      = int(claude_b_token)

        if (claude_v_nick_name != ''):
            self.claude_v_enable     = False
            self.claude_v_nick_name  = claude_v_nick_name
            self.claude_v_model      = claude_v_model
            self.claude_v_token      = int(claude_v_token)

        if (claude_x_nick_name != ''):
            self.claude_x_enable     = False
            self.claude_x_nick_name  = claude_x_nick_name
            self.claude_x_model      = claude_x_model
            self.claude_x_token      = int(claude_x_token)

        # API-KEYの設定
        self.client = None
        try:
            self.client = anthropic.Anthropic(
                # defaults to os.environ.get("ANTHROPIC_API_KEY")
                api_key=claude_key_id,
            )
        except Exception as e:
            print(e)
            return False

        # モデル
        hit = False
        if (self.claude_a_model != ''):
            self.claude_a_enable = True
            hit = True
        if (self.claude_b_model != ''):
            self.claude_b_enable = True
            hit = True
        if (self.claude_v_model != ''):
            self.claude_v_enable = True
            hit = True
        if (self.claude_x_model != ''):
            self.claude_x_enable = True
            hit = True

        if (hit == True):
            self.bot_auth = True
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



    def files_check(self, filePath=[], ):
        upload_files = []
        image_urls   = []

        # filePath確認
        if (len(filePath) > 0):
            try:

                for file_name in filePath:
                    if (os.path.isfile(file_name)):
                        # 2024/06/26 時点 max 10Mbyte 
                        if (os.path.getsize(file_name) <= 10000000):

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
            self.print(session_id, ' claude  : Not Authenticate Error !')
            return res_text, res_path, res_name, res_api, res_history

        # モデル 設定
        res_name = self.claude_a_nick_name
        res_api  = self.claude_a_model
        if  (chat_class == 'claude'):
            if (self.claude_b_enable == True):
                res_name = self.claude_b_nick_name
                res_api  = self.claude_b_model

        # モデル 補正 (assistant)
        if ((chat_class == 'assistant') \
        or  (chat_class == 'コード生成') \
        or  (chat_class == 'コード実行') \
        or  (chat_class == '文書検索') \
        or  (chat_class == '複雑な会話') \
        or  (chat_class == 'アシスタント') \
        or  (model_select == 'x')):
            if (self.claude_x_enable == True):
                res_name = self.claude_x_nick_name
                res_api  = self.claude_x_model

        # model 指定
        if (self.claude_a_nick_name != ''):
            if (inpText.strip()[:len(self.claude_a_nick_name)+1].lower() == (self.claude_a_nick_name.lower() + ',')):
                inpText = inpText.strip()[len(self.claude_a_nick_name)+1:]
        if (self.claude_b_nick_name != ''):
            if (inpText.strip()[:len(self.claude_b_nick_name)+1].lower() == (self.claude_b_nick_name.lower() + ',')):
                inpText = inpText.strip()[len(self.claude_b_nick_name)+1:]
                if   (self.claude_b_enable == True):
                        res_name = self.claude_b_nick_name
                        res_api  = self.claude_b_model
        if (self.claude_v_nick_name != ''):
            if (inpText.strip()[:len(self.claude_v_nick_name)+1].lower() == (self.claude_v_nick_name.lower() + ',')):
                inpText = inpText.strip()[len(self.claude_v_nick_name)+1:]
                if   (self.claude_v_enable == True):
                    if  (len(image_urls) > 0) \
                    and (len(image_urls) == len(upload_files)):
                        res_name = self.claude_v_nick_name
                        res_api  = self.claude_v_model
                elif (self.claude_x_enable == True):
                        res_name = self.claude_x_nick_name
                        res_api  = self.claude_x_model
        if (self.claude_x_nick_name != ''):
            if (inpText.strip()[:len(self.claude_x_nick_name)+1].lower() == (self.claude_x_nick_name.lower() + ',')):
                inpText = inpText.strip()[len(self.claude_x_nick_name)+1:]
                if   (self.claude_x_enable == True):
                        res_name = self.claude_x_nick_name
                        res_api  = self.claude_x_model
                elif (self.claude_b_enable == True):
                        res_name = self.claude_b_nick_name
                        res_api  = self.claude_b_model
        if   (inpText.strip()[:5].lower() == ('riki,')):
            inpText = inpText.strip()[5:]
            if   (self.claude_x_enable == True):
                        res_name = self.claude_x_nick_name
                        res_api  = self.claude_x_model
            elif (self.claude_b_enable == True):
                        res_name = self.claude_b_nick_name
                        res_api  = self.claude_b_model
        elif (inpText.strip()[:7].lower() == ('vision,')):
            inpText = inpText.strip()[7:]
            if   (self.claude_v_enable == True):
                if  (len(image_urls) > 0) \
                and (len(image_urls) == len(upload_files)):
                        res_name = self.claude_v_nick_name
                        res_api  = self.claude_v_model
            elif (self.claude_x_enable == True):
                        res_name = self.claude_x_nick_name
                        res_api  = self.claude_x_model
        elif (inpText.strip()[:10].lower() == ('assistant,')):
            inpText = inpText.strip()[10:]
            if (self.claude_b_enable == True):
                        res_name = self.claude_b_nick_name
                        res_api  = self.claude_b_model
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
            res_name = self.claude_a_nick_name
            res_api  = self.claude_a_model
            if (self.claude_b_enable == True):
                if (len(upload_files) > 0) \
                or (len(inpText) > 1000):
                    res_name = self.claude_b_nick_name
                    res_api  = self.claude_b_model

        # モデル 補正 (vision)
        if  (len(image_urls) > 0) \
        and (len(image_urls) == len(upload_files)):
            if   (self.claude_v_enable == True):
                res_name = self.claude_v_nick_name
                res_api  = self.claude_v_model
            elif (self.claude_x_enable == True):
                res_name = self.claude_x_nick_name
                res_api  = self.claude_x_model

        # history 追加・圧縮 (古いメッセージ)
        res_history = self.history_add(history=res_history, sysText=sysText, reqText=reqText, inpText=inpText, )
        res_history = self.history_zip1(history=res_history, )

        # 過去メッセージ追加
        msg_text = ''
        if (len(res_history) > 2):
            msg_text += "''' これは過去の会話履歴です。\n"
            for m in range(len(res_history) - 2):
                role    = res_history[m+1].get('role','')
                content = res_history[m+1].get('content','')
                name    = res_history[m+1].get('name','')
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

        # tools
        tools = []
        for module_dic in function_modules:
            func_dic = module_dic['function']
            func_str = json.dumps(func_dic, ensure_ascii=False, )
            func_str = func_str.replace('"parameters"', '"input_schema"')
            func     = json.loads(func_str)
            tools.append(func)

        # 送信データ
        if (len(res_history) <= 2):
            if (reqText is not None) and (reqText != ''):
                msg_text += reqText + '\n'
        msg_text += inpText

        # 送信データ 画像無し
        messages = []
        contents = []
        if (len(image_urls) == 0) \
        or (len(image_urls) != len(upload_files)):
            contents.append({"type":"text", "text": msg_text})
            messages.append({"role": "user", "content": contents })

        # 送信データ 画像あり
        else:
            for file_name in upload_files:
                if (os.path.isfile(file_name)):
                    if (os.path.getsize(file_name) <= 20000000):
                        file_ext = os.path.splitext(file_name)[1][1:].lower()
                        image_b64 = base64_encode(file_path=file_name)
                        if (file_ext in ('jpg', 'jpeg')):
                            contents.append({"type":"image", "source": {"type": "base64", "media_type": "image/jpeg", "data": image_b64 }})
                        if (file_ext in ('png')):
                            contents.append({"type":"image", "source": {"type": "base64", "media_type": "image/png", "data": image_b64 }})
            contents.append({"type":"text", "text": msg_text})
            messages.append({"role": "user", "content": contents })

        # ストリーム実行?
        if (session_id == 'admin'):
            stream = True
        else:
            stream = False
        #print(' stream = False, ')
        #stream = False

        # 実行ループ
        #try:
        if True:

            n = 0
            function_name = ''
            while (function_name != 'exit') and (n < int(max_step)):

                # 結果
                res_role      = None
                res_content   = ''
                tool_calls    = []

                # GPT
                n += 1
                self.print(session_id, f" claude  : { res_api }, pass={ n }, ")

                # Stream 表示
                if (stream == True):

                    chkTime = time.time()
                    with self.client.messages.stream(   model=res_api, 
                                                        max_tokens=1000,
                                                        temperature=0,
                                                        system=sysText,
                                                        messages=messages,
                                                        tools=tools, ) as streams:
                        # Stream 処理
                        hit_string = False
                        for chunk in streams:
                            if ((time.time() - chkTime) > self.timeOut):
                                break

                            try:
                                content_type = chunk.type
                                if   (content_type == 'content_block_delta'):
                                    try:
                                        # ストリーム
                                        delta_text = chunk.delta.text
                                        delta_text = delta_text.replace('\n\n', '\n')
                                        delta_text = delta_text.replace('\n\n', '\n')
                                        if (hit_string == False):
                                            if (delta_text[:1] == '\n'):
                                                delta_text = delta_text[1:]
                                        if (delta_text.strip() != ''):
                                            hit_string = True
                                            self.stream(session_id, delta_text)
                                    except:
                                        pass

                                elif (content_type == 'content_block_stop'):
                                    try:
                                        block_type = chunk.content_block.type
                                        if (block_type == 'text'):
                                            if (hit_string == True):
                                                # 改行
                                                self.print(session_id, )
                                                hit_string = False
                                    except:
                                        pass

                                elif (content_type == 'message_stop'):
                                    #self.print(session_id, )
                                    response = chunk.message

                            except Exception as e:
                                print(e)

                # 通常実行
                if (stream == False):
                    response = self.client.messages.create( model=res_api, 
                                                            max_tokens=1000,
                                                            temperature=0,
                                                            system=sysText,
                                                            messages=messages,
                                                            tools=tools, )

                # 共通 response 処理
                role        = response.role
                contents    = response.content

                # メッセージ保管
                msg = {"role": role, "content": contents }
                messages.append(msg)

                for c in range(len(contents)):
                    c_type     = response.content[c].type
                    if (c_type == 'text'):
                        c_text = response.content[c].text

                        # History 追加格納
                        if (c_text.strip() != ''):
                            if (stream == False):
                                self.print(session_id, c_text)
                            res_text += c_text + '\n'

                            self.seq += 1
                            dic = {'seq': self.seq, 'time': time.time(), 'role': 'assistant', 'name': '', 'content': c_text }
                            res_history.append(dic)

                    if (c_type == 'tool_use'):
                        f_id     = response.content[c].id
                        f_name   = response.content[c].name
                        f_kwargs = json.dumps(response.content[c].input, ensure_ascii=False, )
                        tool_calls.append({"id": f_id, "type": "function", "function": { "name": f_name, "arguments": f_kwargs } })

                # function 指示?
                contents = []
                if (len(tool_calls) > 0):
                    self.print(session_id, )

                    for tc in tool_calls:
                        f_id     = tc.get('id')
                        f_name   = tc['function'].get('name')
                        f_kwargs = tc['function'].get('arguments')

                        hit = False

                        for module_dic in function_modules:
                            if (f_name == module_dic['func_name']):
                                hit = True
                                self.print(session_id, f" claude  :   function_call '{ module_dic['script'] }' ({ f_name })")
                                self.print(session_id, f" claude  :   → { f_kwargs }")

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
                                self.print(session_id, f" claude  :   → { res_json }")
                                self.print(session_id, )

                                # メッセージ追加格納
                                contents.append({"type": "tool_result", "tool_use_id": f_id, "content": [{ "type": "text", "text": res_json }] })

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
                            self.print(session_id, f" claude  :   function_call Error ! ({ f_name })")
                            print(res_role, res_content, f_name, f_kwargs, )
                            break

                # tool 戻り値設定 → 再実行
                if (len(contents) > 0):
                    msg = {"role": "user", "content": contents }
                    messages.append(msg)

                # 実行終了
                else:
                    function_name = 'exit'

            # 正常回答
            if (res_text != ''):
                self.print(session_id, f" claude  : { res_name.lower() } complite.")
            else:
                self.print(session_id,  ' claude  : Error !')

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
            sysText = 'あなたは教師のように話す賢いアシスタントです。'

        if (self.bot_auth is None):
            self.print(session_id, ' claude : Not Authenticate Error !')
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

        # claude
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

        #claudeAPI = speech_bot_claude._claudeAPI()
        claudeAPI = _claudeAPI()

        api_type = claude_key.getkey('claude','claude_api_type')
        print(api_type)

        log_queue = queue.Queue()
        res = claudeAPI.init(log_queue=log_queue, )

        res = claudeAPI.authenticate('claude',
                            api_type,
                            claude_key.getkey('claude','claude_default_gpt'), claude_key.getkey('claude','claude_default_class'),
                            claude_key.getkey('claude','claude_auto_continue'),
                            claude_key.getkey('claude','claude_max_step'), claude_key.getkey('claude','claude_max_assistant'),
                            claude_key.getkey('claude','claude_key_id'),
                            claude_key.getkey('claude','claude_a_nick_name'), claude_key.getkey('claude','claude_a_model'), claude_key.getkey('claude','claude_a_token'),
                            claude_key.getkey('claude','claude_b_nick_name'), claude_key.getkey('claude','claude_b_model'), claude_key.getkey('claude','claude_b_token'),
                            claude_key.getkey('claude','claude_v_nick_name'), claude_key.getkey('claude','claude_v_model'), claude_key.getkey('claude','claude_v_token'),
                            claude_key.getkey('claude','claude_x_nick_name'), claude_key.getkey('claude','claude_x_model'), claude_key.getkey('claude','claude_x_token'),
                            )
        print('authenticate:', res, )
        if (res == True):
            
            function_modules = []
            filePath         = []

            if True:
                import    speech_bot_function
                botFunc = speech_bot_function.botFunction()

                res, msg = botFunc.functions_load(
                    functions_path='_extensions/function/', secure_level='low', )
                if (res != True) or (msg != ''):
                    print(msg)
                    print()

                for module_dic in botFunc.function_modules:
                    if (module_dic['onoff'] == 'on'):
                        function_modules.append(module_dic)

            if True:
                sysText = None
                reqText = ''
                #inpText = 'おはようございます。'
                inpText = '今日は、何月何日？'
                #inpText = '日本の３大都市の天気？'
                print()
                print('[Request]')
                print(reqText, inpText )
                print()
                res_text, res_path, res_files, res_name, res_api, claudeAPI.history = \
                    claudeAPI.chatBot(  chat_class='auto', model_select='auto', 
                                        session_id='admin', history=claudeAPI.history, function_modules=function_modules,
                                        sysText=sysText, reqText=reqText, inpText=inpText, filePath=filePath,
                                        inpLang='ja', outLang='ja', )
                print()
                print(f"[{ res_name }] ({ res_api })")
                print(str(res_text))
                print()

            if False:
                sysText = None
                reqText = ''
                inpText = '兵庫県三木市の天気？'
                print()
                print('[Request]')
                print(reqText, inpText )
                print()
                res_text, res_path, res_files, res_name, res_api, claudeAPI.history = \
                    claudeAPI.chatBot(  chat_class='auto', model_select='auto', 
                                        session_id='admin', history=claudeAPI.history, function_modules=function_modules,
                                        sysText=sysText, reqText=reqText, inpText=inpText, filePath=filePath,
                                        inpLang='ja', outLang='ja', )
                print()
                print(f"[{ res_name }] ({ res_api })")
                print(str(res_text))
                print()

            if True:
                sysText = None
                reqText = ''
                inpText = 'この画像はなんだと思いますか？'
                filePath = ['_icons/dog.jpg', '_icons/kyoto.png']
                print()
                print('[Request]')
                print(reqText, inpText )
                print()
                res_text, res_path, res_files, res_name, res_api, claudeAPI.history = \
                    claudeAPI.chatBot(  chat_class='auto', model_select='auto', 
                                        session_id='admin', history=claudeAPI.history, function_modules=function_modules,
                                        sysText=sysText, reqText=reqText, inpText=inpText, filePath=filePath,
                                        inpLang='ja', outLang='ja', )
                print()
                print(f"[{ res_name }] ({ res_api })")
                print(str(res_text))
                print()

            if False:
                sysText = None
                reqText = ''
                inpText = "genarate 'cute cat in room' image"
                print()
                print('[Request]')
                print(reqText, inpText )
                print()
                res_text, res_path, res_files, res_name, res_api, claudeAPI.history = \
                    claudeAPI.chatBot(  chat_class='flash', model_select='auto', 
                                        session_id='admin', history=claudeAPI.history, function_modules=[],
                                        sysText=sysText, reqText=reqText, inpText=inpText, filePath=filePath,
                                        inpLang='ja', outLang='ja', )
                print()
                print(f"[{ res_name }] ({ res_api })")
                print(str(res_text))
                print()

            if False:
                print('[History]')
                for h in range(len(claudeAPI.history)):
                    print(claudeAPI.history[h])
                claudeAPI.history = []



