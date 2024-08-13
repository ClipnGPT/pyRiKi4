#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# COPYRIGHT (C) 2014-2024 Mitsuo KONDOU.
# This software is released under the MIT License.
# https://github.com/konsan1101
# Thank you for keeping the rules.
# ------------------------------------------------



import sys
import os
import time
import datetime
import codecs
import glob

import queue
import threading
import subprocess

# dummy import
if (os.name == 'nt'):
    import comtypes.client
    import comtypes.stream

#print(os.path.dirname(__file__))
#print(os.path.basename(__file__))
#print(sys.version_info)



# インターフェース
qCtrl_control_kernel     = 'temp/control_kernel.txt'
qCtrl_control_speech     = 'temp/control_speech.txt'
qCtrl_control_vision     = 'temp/control_vision.txt'
qCtrl_control_desktop    = 'temp/control_desktop.txt'
qCtrl_control_self       = qCtrl_control_speech

# 出力インターフェース
qCtrl_result_audio       = 'temp/result_audio.txt'
qCtrl_result_speech      = 'temp/result_speech.txt'
qCtrl_recognize          = 'temp/result_recognize.txt'
qCtrl_recognize_sjis     = 'temp/result_recognize_sjis.txt'
qCtrl_translate          = 'temp/result_translate.txt'
qCtrl_translate_sjis     = 'temp/result_translate_sjis.txt'



# 共通ルーチン
import  _v6__qRiKi
qRiKi = _v6__qRiKi.qRiKi_class()
import  _v6__qFunc
qFunc = _v6__qFunc.qFunc_class()
import  _v6__qGUI
qGUI  = _v6__qGUI.qGUI_class()
import  _v6__qLog
qLog  = _v6__qLog.qLog_class()
import  _v6__qGuide
qGuide= _v6__qGuide.qGuide_class()

qPLATFORM        = qRiKi.getValue('qPLATFORM'        )
qRUNATTR         = qRiKi.getValue('qRUNATTR'         )
qHOSTNAME        = qRiKi.getValue('qHOSTNAME'        )
qUSERNAME        = qRiKi.getValue('qUSERNAME'        )
qPath_controls   = qRiKi.getValue('qPath_controls'   )
qPath_pictures   = qRiKi.getValue('qPath_pictures'   )
qPath_videos     = qRiKi.getValue('qPath_videos'     )
qPath_cache      = qRiKi.getValue('qPath_cache'      )
qPath_sounds     = qRiKi.getValue('qPath_sounds'     )
qPath_icons      = qRiKi.getValue('qPath_icons'      )
qPath_fonts      = qRiKi.getValue('qPath_fonts'      )
qPath_log        = qRiKi.getValue('qPath_log'        )
qPath_work       = qRiKi.getValue('qPath_work'       )
qPath_rec        = qRiKi.getValue('qPath_rec'        )
qPath_recept     = qRiKi.getValue('qPath_recept'     )

qPath_s_ctrl     = qRiKi.getValue('qPath_s_ctrl'     )
qPath_s_inp      = qRiKi.getValue('qPath_s_inp'      )
qPath_s_wav      = qRiKi.getValue('qPath_s_wav'      )
qPath_s_jul      = qRiKi.getValue('qPath_s_jul'      )
qPath_s_STT      = qRiKi.getValue('qPath_s_STT'      )
qPath_s_TTS      = qRiKi.getValue('qPath_s_TTS'      )
qPath_s_TRA      = qRiKi.getValue('qPath_s_TRA'      )
qPath_s_play     = qRiKi.getValue('qPath_s_play'     )
qPath_s_chat     = qRiKi.getValue('qPath_s_chat'     )
qPath_v_ctrl     = qRiKi.getValue('qPath_v_ctrl'     )
qPath_v_inp      = qRiKi.getValue('qPath_v_inp'      )
qPath_v_jpg      = qRiKi.getValue('qPath_v_jpg'      )
qPath_v_detect   = qRiKi.getValue('qPath_v_detect'   )
qPath_v_cv       = qRiKi.getValue('qPath_v_cv'       )
qPath_v_photo    = qRiKi.getValue('qPath_v_photo'    )
qPath_v_msg      = qRiKi.getValue('qPath_v_msg'      )
qPath_v_recept   = qRiKi.getValue('qPath_v_recept'   )
qPath_d_ctrl     = qRiKi.getValue('qPath_d_ctrl'     )
qPath_d_play     = qRiKi.getValue('qPath_d_play'     )
qPath_d_prtscn   = qRiKi.getValue('qPath_d_prtscn'   )
qPath_d_movie    = qRiKi.getValue('qPath_d_movie'    )
qPath_d_telop    = qRiKi.getValue('qPath_d_telop'    )
qPath_d_upload   = qRiKi.getValue('qPath_d_upload'   )

qBusy_dev_cpu    = qRiKi.getValue('qBusy_dev_cp'    )
qBusy_dev_com    = qRiKi.getValue('qBusy_dev_com'    )
qBusy_dev_mic    = qRiKi.getValue('qBusy_dev_mic'    )
qBusy_dev_spk    = qRiKi.getValue('qBusy_dev_spk'    )
qBusy_dev_cam    = qRiKi.getValue('qBusy_dev_cam'    )
qBusy_dev_dsp    = qRiKi.getValue('qBusy_dev_dsp'    )
qBusy_dev_scn    = qRiKi.getValue('qBusy_dev_scn'    )
qBusy_s_ctrl     = qRiKi.getValue('qBusy_s_ctrl'     )
qBusy_s_inp      = qRiKi.getValue('qBusy_s_inp'      )
qBusy_s_wav      = qRiKi.getValue('qBusy_s_wav'      )
qBusy_s_STT      = qRiKi.getValue('qBusy_s_STT'      )
qBusy_s_TTS      = qRiKi.getValue('qBusy_s_TTS'      )
qBusy_s_TRA      = qRiKi.getValue('qBusy_s_TRA'      )
qBusy_s_play     = qRiKi.getValue('qBusy_s_play'     )
qBusy_s_chat     = qRiKi.getValue('qBusy_s_chat'     )
qBusy_v_ctrl     = qRiKi.getValue('qBusy_v_ctrl'     )
qBusy_v_inp      = qRiKi.getValue('qBusy_v_inp'      )
qBusy_v_QR       = qRiKi.getValue('qBusy_v_QR'       )
qBusy_v_jpg      = qRiKi.getValue('qBusy_v_jpg'      )
qBusy_v_CV       = qRiKi.getValue('qBusy_v_CV'       )
qBusy_v_recept   = qRiKi.getValue('qBusy_v_recept'   )
qBusy_d_ctrl     = qRiKi.getValue('qBusy_d_ctrl'     )
qBusy_d_inp      = qRiKi.getValue('qBusy_d_inp'      )
qBusy_d_QR       = qRiKi.getValue('qBusy_d_QR'       )
qBusy_d_rec      = qRiKi.getValue('qBusy_d_rec'      )
qBusy_d_telework = qRiKi.getValue('qBusy_d_telework' )
qBusy_d_play     = qRiKi.getValue('qBusy_d_play'     )
qBusy_d_browser  = qRiKi.getValue('qBusy_d_browser'  )
qBusy_d_telop    = qRiKi.getValue('qBusy_d_telop'    )
qBusy_d_upload   = qRiKi.getValue('qBusy_d_upload'   )
qRdy__s_force    = qRiKi.getValue('qRdy__s_force'    )
qRdy__s_fproc    = qRiKi.getValue('qRdy__s_fproc'    )
qRdy__s_sendkey  = qRiKi.getValue('qRdy__s_sendkey'  )
qRdy__v_mirror   = qRiKi.getValue('qRdy__v_mirror'   )
qRdy__v_reader   = qRiKi.getValue('qRdy__v_reader'   )
qRdy__v_sendkey  = qRiKi.getValue('qRdy__v_sendkey'  )
qRdy__d_reader   = qRiKi.getValue('qRdy__d_reader'   )
qRdy__d_sendkey  = qRiKi.getValue('qRdy__d_sendkey'  )

# thread ルーチン群
import _v6_proc_controls
import _v6_proc_adintool
import _v6_proc_voice2wav
import _v6_proc_coreSTT
import _v6_proc_coreTTS
import _v6_proc_playvoice
import _v6_proc_txtreader
import _v6_proc_chatbot

# julius 音声認識
import speech_api_julius



# debug
runMode     = 'chatbot'

qApiInp     = 'free'
qApiTrn     = 'free'
qApiOut     = qApiTrn
#if (qPLATFORM == 'windows'):
#    qApiOut = 'winos'
if (qPLATFORM == 'darwin'):
    qApiOut = 'macos'
qLangInp    = 'ja'
#qLangTrn    = 'en,fr,'
qLangTrn    = 'en'
qLangTxt    = qLangInp
qLangOut    = qLangTrn[:2]



class main_speech:

    def __init__(self, name='thread', id='0', runMode='debug',
                    micDev='0', micType='bluetooth', micGuide='on', micLevel='888',
                    qApiInp='free', qApiTrn='free', qApiOut='free',
                    qLangInp='ja', qLangTrn='en,fr,', qLangTxt='ja', qLangOut='en',
                    ):
        self.runMode   = runMode
        self.micDev    = micDev
        self.micType   = micType
        self.micGuide  = micGuide
        self.micLevel  = micLevel

        self.qApiInp   = qApiInp
        self.qApiTrn   = qApiTrn
        self.qApiOut   = qApiOut
        self.qLangInp  = qLangInp
        self.qLangTrn  = qLangTrn
        self.qLangTxt  = qLangTxt
        self.qLangOut  = qLangOut

        self.breakFlag = threading.Event()
        self.breakFlag.clear()
        self.name      = name
        self.id        = id
        self.proc_id   = '{0:10s}'.format(name).replace(' ', '_')
        self.proc_id   = self.proc_id[:-2] + '_' + str(id)
        if (runMode == 'debug'):
            self.logDisp = True
        else:
            self.logDisp = False
        qLog.log('info', self.proc_id, 'init', display=self.logDisp, )

        self.proc_s    = None
        self.proc_r    = None
        self.proc_main = None
        self.proc_beat = None
        self.proc_last = None
        self.proc_step = '0'
        self.proc_seq  = 0

    def __del__(self, ):
        qLog.log('info', self.proc_id, 'bye!', display=self.logDisp, )

    def begin(self, ):
        #qLog.log('info', self.proc_id, 'start')

        self.fileRun = qPath_work + self.proc_id + '.run'
        self.fileRdy = qPath_work + self.proc_id + '.rdy'
        self.fileBsy = qPath_work + self.proc_id + '.bsy'
        qFunc.statusSet(self.fileRun, False)
        qFunc.statusSet(self.fileRdy, False)
        qFunc.statusSet(self.fileBsy, False)

        self.proc_s = queue.Queue()
        self.proc_r = queue.Queue()
        self.proc_main = threading.Thread(target=self.main_proc, args=(self.proc_s, self.proc_r, ), daemon=True, )
        self.proc_beat = time.time()
        self.proc_last = time.time()
        self.proc_step = '0'
        self.proc_seq  = 0
        self.proc_main.start()

    def abort(self, waitMax=20, ):
        qLog.log('info', self.proc_id, 'stop', display=self.logDisp, )

        self.breakFlag.set()
        chktime = time.time()
        while (self.proc_beat is not None) and ((time.time() - chktime) < waitMax):
            time.sleep(0.25)
        chktime = time.time()
        while (os.path.exists(self.fileRun)) and ((time.time() - chktime) < waitMax):
            time.sleep(0.25)

    def put(self, data, ):
        self.proc_s.put(data)
        return True

    def checkGet(self, waitMax=5, ):
        chktime = time.time()
        while (self.proc_r.qsize() == 0) and ((time.time() - chktime) < waitMax):
            time.sleep(0.10)
        data = self.get()
        return data

    def get(self, ):
        if (self.proc_r.qsize() == 0):
            return ['', '']
        data = self.proc_r.get()
        self.proc_r.task_done()
        return data

    def main_proc(self, cn_r, cn_s, ):
        # ログ
        qLog.log('info', self.proc_id, 'start', display=self.logDisp, )
        qFunc.statusSet(self.fileRun, True)
        self.proc_beat = time.time()

        # 初期設定
        self.proc_step = '1'

        txts, txt = qFunc.txtsRead(qCtrl_control_self)
        if (txts != False):
            if (txt == '_end_'):
                qFunc.remove(qCtrl_control_self)

        # 外部ＰＧリセット
        qFunc.kill('adintool-gui')
        qFunc.kill('adintool')
        qFunc.kill('julius')

        # 起動条件
        run_priority         = 'normal'
        controls_thread      = None
        controls_switch      = 'on'
        adintool_thread      = None
        adintool_switch      = 'on'
        voice2wav_thread     = None
        voice2wav_switch     = 'on'
        coreSTT_thread       = None
        coreSTT_switch       = 'on'
        coreTTS_thread       = None
        coreTTS_switch       = 'on'
        playvoice_thread     = None
        playvoice_switch     = 'on'
        julius_thread        = None
        julius_switch        = 'off'
        sttreader_thread     = None
        sttreader_switch     = 'off'
        trareader_thread     = None
        trareader_switch     = 'off'
        chatbot_thread       = None
        chatbot_switch       = 'off'

        if   (self.runMode == 'debug'):
            julius_switch    = 'on'
            sttreader_switch = 'on'
            trareader_switch = 'on'
        elif (self.runMode == 'hud'):
            pass
        elif (self.runMode == 'live'):
            pass
        elif (self.runMode == 'translator'):
            trareader_switch = 'on'
        elif (self.runMode == 'speech'):
            sttreader_switch = 'on'
        elif (self.runMode == 'number'):
            julius_switch    = 'on'
            sttreader_switch = 'on'
        elif (self.runMode == 'chat'):
            pass
        elif (self.runMode == 'chatbot'):
            sttreader_switch = 'on'
            chatbot_switch   = 'on'
        elif (self.runMode == 'camera'):
            julius_switch    = 'on'
        elif (self.runMode == 'assistant'):
            run_priority     = 'below' # 通常以下
            julius_switch    = 'on'
            sttreader_switch = 'on'
        elif (self.runMode == 'reception'):
            pass
        elif (self.runMode == 'tts'):
            controls_switch  = 'off'
            adintool_switch  = 'off'
            voice2wav_switch = 'off'
            coreSTT_switch   = 'off'

        if (not self.micDev.isdigit()):
            julius_switch    = 'off'
            sttreader_switch = 'off'
            trareader_switch = 'off'
            chatbot_switch   = 'off'

        # 実行優先順位設定
        qFunc.setNice(run_priority)

        # 待機ループ
        self.proc_step = '5'

        onece = True
        last_alive = time.time()

        while (self.proc_step == '5'):
            self.proc_beat = time.time()

            # 終了確認
            txts, txt = qFunc.txtsRead(qCtrl_control_self)
            if (txts != False):
                qLog.log('info', self.proc_id, '' + str(txt))
                if (txt == '_end_'):
                    break

            # 停止要求確認
            if (self.breakFlag.is_set()):
                self.breakFlag.clear()
                self.proc_step = '9'
                break

            # 活動メッセージ
            if  ((time.time() - last_alive) > 30):
                qLog.log('debug', self.proc_id, 'alive', display=True, )
                last_alive = time.time()

            # キュー取得
            if (cn_r.qsize() > 0):
                cn_r_get  = cn_r.get()
                inp_name  = cn_r_get[0]
                inp_value = cn_r_get[1]
                cn_r.task_done()
            else:
                inp_name  = ''
                inp_value = ''

            if (cn_r.qsize() > 1) or (cn_s.qsize() > 20):
                qLog.log('warning', self.proc_id, 'queue overflow warning!, ' + str(cn_r.qsize()) + ', ' + str(cn_s.qsize()))

            # スレッド設定

            speechs = []

            if (controls_thread is None) and (controls_switch == 'on'):
                cn_s.put(['_guide_', 'controls start!'])

                controls_thread = _v6_proc_controls.proc_controls(
                                    name='controls', id='0',
                                    runMode=self.runMode,
                                    micDev=self.micDev, micType=self.micType, micGuide=self.micGuide, micLevel=self.micLevel,
                                    )
                controls_thread.begin()
                time.sleep(1.00)

                if (self.runMode == 'debug') \
                or (self.runMode == 'live'):
                    speechs.append({ 'text':'「音声制御」の機能が有効になりました。', 'wait':0, })

            if (controls_thread is not None) and (controls_switch != 'on'):
                controls_thread.abort()
                del controls_thread
                controls_thread = None

            if (adintool_thread is None) and (adintool_switch == 'on'):
                cn_s.put(['_guide_', 'adintool start!'])

                adintool_thread  = _v6_proc_adintool.proc_adintool(
                                    name='adintool', id='0', 
                                    runMode=self.runMode,
                                    micDev=self.micDev, micType=self.micType, micGuide=self.micGuide, micLevel=self.micLevel,
                                    )
                adintool_thread.begin()
                time.sleep(1.00)

                if (self.runMode == 'debug') \
                or (self.runMode == 'live'):
                    speechs.append({ 'text':'「マイク入力」の機能が有効になりました。', 'wait':0, })

            if (adintool_thread is not None) and (adintool_switch != 'on'):
                adintool_thread.abort()
                del adintool_thread
                adintool_thread = None

            if (voice2wav_thread is None) and (voice2wav_switch == 'on'):
                cn_s.put(['_guide_', 'voice2wave start!'])

                voice2wav_thread = _v6_proc_voice2wav.proc_voice2wav(
                                    name='voice2wave', id='0',
                                    runMode=self.runMode,
                                    micDev=self.micDev, micType=self.micType, micGuide=self.micGuide, micLevel=self.micLevel,
                                    )
                voice2wav_thread.begin()
                time.sleep(1.00)

                if (self.runMode == 'debug') \
                or (self.runMode == 'live'):
                    speechs.append({ 'text':'「音響補正」の機能が有効になりました。', 'wait':0, })

            if (voice2wav_thread is not None) and (voice2wav_switch != 'on'):
                voice2wav_thread.abort()
                del voice2wav_thread
                voice2wav_thread = None

            if (coreSTT_thread is None) and (coreSTT_switch == 'on'):
                cn_s.put(['_guide_', 'coreSTT start!'])

                coreSTT_thread   = _v6_proc_coreSTT.proc_coreSTT(
                                    name='coreSTT', id='0', 
                                    runMode=self.runMode,
                                    micDev=self.micDev, micType=self.micType, micGuide=self.micGuide, micLevel=self.micLevel, 
                                    qApiInp=self.qApiInp, qApiTrn=self.qApiTrn, qApiOut=self.qApiOut,
                                    qLangInp=self.qLangInp, qLangTrn=self.qLangTrn, qLangTxt=self.qLangTxt, qLangOut=self.qLangOut,
                                    )
                coreSTT_thread.begin()
                time.sleep(1.00)

                speechs = []
                if (self.runMode == 'debug') \
                or (self.runMode == 'live'):
                    speechs.append({ 'text':'「ＡＩ音声認識」の機能が有効になりました。', 'wait':0, })
                    speechs.append({ 'text':'「ＡＩ機械翻訳」の機能が有効になりました。', 'wait':0, })

            if (coreSTT_thread is not None) and (coreSTT_switch != 'on'):
                coreSTT_thread.abort()
                del coreSTT_thread
                coreSTT_thread = None

            if (coreTTS_thread is None) and (coreTTS_switch == 'on'):
                cn_s.put(['_guide_', 'coreTTS start!'])

                coreTTS_thread   = _v6_proc_coreTTS.proc_coreTTS(
                                    name='coreTTS', id='0',
                                    runMode=self.runMode,
                                    micDev=self.micDev, micType=self.micType, micGuide=self.micGuide, micLevel=self.micLevel, 
                                    qApiInp=self.qApiInp, qApiTrn=self.qApiTrn, qApiOut=self.qApiOut,
                                    qLangInp=self.qLangInp, qLangTrn=self.qLangTrn, qLangTxt=self.qLangTxt, qLangOut=self.qLangOut,
                                    )
                coreTTS_thread.begin()
                time.sleep(1.00)

                if (self.runMode == 'debug') \
                or (self.runMode == 'live'):
                    speechs.append({ 'text':'「ＡＩ音声合成」の機能が有効になりました。', 'wait':0, })

            if (coreTTS_thread is not None) and (coreTTS_switch != 'on'):
                coreTTS_thread.abort()
                del coreTTS_thread
                coreTTS_thread = None

            if (playvoice_thread is None) and (playvoice_switch == 'on'):
                cn_s.put(['_guide_', 'playvoice start!'])

                playvoice_thread = _v6_proc_playvoice.proc_playvoice(
                                    name='playvoice', id='0',
                                    runMode=self.runMode,
                                    micDev=self.micDev, micType=self.micType, micGuide=self.micGuide, micLevel=self.micLevel,
                                    )
                playvoice_thread.begin()
                time.sleep(1.00)

                if (self.runMode == 'debug') \
                or (self.runMode == 'live'):
                    speechs.append({ 'text':'「スピーカー出力」の機能が有効になりました。', 'wait':0, })

            if (playvoice_thread is not None) and (playvoice_switch != 'on'):
                playvoice_thread.abort()
                del playvoice_thread
                playvoice_thread = None

            if (julius_thread is None) and (julius_switch == 'on'):
                cn_s.put(['_guide_', 'julius start!'])

                julius_thread    = speech_api_julius.proc_julius(
                                    name='julius', id='0', 
                                    runMode=self.runMode,
                                    )
                julius_thread.begin()
                time.sleep(1.00)

                if (self.runMode == 'debug') \
                or (self.runMode == 'live'):
                    speechs.append({ 'text':'「ＪＵＬＩＵＳローカル音声認識」の機能が有効になりました。', 'wait':0, })

            if (julius_thread is not None) and (julius_switch != 'on'):
                julius_thread.abort()
                del julius_thread
                julius_thread = None

            if (sttreader_thread is None) and (sttreader_switch == 'on'):
                cn_s.put(['_guide_', 'sttreader start!'])

                sttreader_thread = _v6_proc_txtreader.proc_txtreader(
                                    name='sttreader', id='0', 
                                    runMode=self.runMode,
                                    micDev=self.micDev, path='qPath_s_STT',
                                    )
                sttreader_thread.begin()
                time.sleep(1.00)

                if (self.runMode == 'debug') \
                or (self.runMode == 'live'):
                    speechs.append({ 'text':'「音声認識結果のテキスト連携」の機能が有効になりました。', 'wait':0, })

            if (sttreader_thread is not None) and (sttreader_switch != 'on'):
                sttreader_thread.abort()
                del sttreader_thread
                sttreader_thread = None

            if (trareader_thread is None) and (trareader_switch == 'on'):
                cn_s.put(['_guide_', 'trareader start!'])

                trareader_thread = _v6_proc_txtreader.proc_txtreader(
                                    name='trareader', id='0', 
                                    runMode=runMode,
                                    micDev=self.micDev, path='qPath_s_TRA',
                                    )
                trareader_thread.begin()
                time.sleep(1.00)

                if (self.runMode == 'debug') \
                or (self.runMode == 'live'):
                    speechs.append({ 'text':'「機械翻訳結果のテキスト連携」の機能が有効になりました。', 'wait':0, })

            if (chatbot_thread is not None) and (chatbot_switch != 'on'):
                chatbot_thread.abort()
                del chatbot_thread
                chatbot_thread = None

            if (chatbot_thread is None) and (chatbot_switch == 'on'):
                cn_s.put(['_guide_', 'chatbot start!'])

                chatbot_thread = _v6_proc_chatbot.proc_coreChat(
                                    name='chatbot', id='0', 
                                    runMode=runMode,
                                    )
                chatbot_thread.begin()
                time.sleep(1.00)

                if (self.runMode == 'debug') \
                or (self.runMode == 'live'):
                    speechs.append({ 'text':'「チャットＧＰＴとの会話」の機能が有効になりました。', 'wait':0, })

            if (chatbot_thread is not None) and (chatbot_switch != 'on'):
                chatbot_thread.abort()
                del chatbot_thread
                chatbot_thread = None

            if (len(speechs) != 0):
                qRiKi.speech(id=self.proc_id, speechs=speechs, lang='', )

            if (onece == True):
                onece = False

                if   (self.runMode == 'debug') \
                or   (self.runMode == 'live') \
                or   (self.runMode == 'hud') \
                or   (self.runMode == 'camera'):
                    speechs = []
                    speechs.append({ 'text':'「ハンズフリー機能」の準備が完了しました。', 'wait':0, })
                    qRiKi.speech(id=self.proc_id, speechs=speechs, lang='', )

            # レディー設定
            if (qFunc.statusCheck(self.fileRdy) == False):
                qFunc.statusSet(self.fileRdy, True)

            # ステータス応答
            if (inp_name.lower() == '_status_'):
                out_name  = inp_name
                out_value = '_ready_'
                cn_s.put([out_name, out_value])

            # 処理
            if (True):

                # 音声ファイル処理（バッチ）時の自動終了
                if (not self.micDev.isdigit()):
                    if (self.qApiInp != 'aws'):
                        if  ((time.time() - coreSTT_thread.proc_last) > 120) \
                        and ((time.time() - coreTTS_thread.proc_last) > 120):
                            qFunc.txtsWrite(qCtrl_control_self, txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
                            break
                    else:
                        if  ((time.time() - coreSTT_thread.proc_last) > 300) \
                        and ((time.time() - coreTTS_thread.proc_last) > 300):
                            qFunc.txtsWrite(qCtrl_control_self, txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
                            break

                # 制御処理
                control = ''

                if (controls_thread is not None):
                    while (controls_thread.proc_r.qsize() != 0):
                        res_data  = controls_thread.get()
                        res_name  = res_data[0]
                        res_value = res_data[1]

                        # 制御
                        if (res_name.lower() == 'control'):
                            control = res_value
                            # 結果出力
                            cn_s.put([res_name, res_value])
                            break

                        # ガイド表示
                        if (res_name.lower() == '_guide_'):
                            cn_s.put(['_guide_', res_value])

                # マイク切り替え時、自動復旧処理
                if (control == ''):
                    if (self.micDev.isdigit()):
                        if (voice2wav_switch == 'on'):
                            if  ((time.time() - voice2wav_thread.proc_last) > 30):
                                control = '_reset_mic_'

                if (control == '_reset_mic_'):
                    if (adintool_switch == 'on'):
                        adintool_thread.abort()
                    if (voice2wav_switch == 'on'):
                        voice2wav_thread.abort()
                    if (julius_switch == 'on'):
                        julius_thread.abort()
                    if (adintool_switch == 'on'):
                        adintool_thread.begin()
                    if (voice2wav_switch == 'on'):
                        voice2wav_thread.begin()
                    if (julius_switch == 'on'):
                        julius_thread.begin()

                # 音声入力（マイク入力）
                if (adintool_thread is not None):
                    res_data  = adintool_thread.get()

                # 音声処理（前処理）
                if (voice2wav_thread is not None):
                    res_data  = voice2wav_thread.get()
                    res_name  = res_data[0]
                    res_value = res_data[1]

                # julius 音声認識（ローカル処理）
                if (julius_thread is not None):
                    if (res_name == 'filename'):
                        julius_thread.put(['filename', res_value])

                # ＡＩ音声認識（クラウド処理）
                if (coreSTT_thread is not None):
                    res_data  = coreSTT_thread.get()

                # ＡＩ音声合成（クラウド処理）
                if (coreTTS_thread is not None):
                    res_data  = coreTTS_thread.get()

                # 音声出力（スピーカー出力）
                if (playvoice_thread is not None):
                    res_data  = playvoice_thread.get()

                # julius 音声認識 外部インターフェース用
                if (julius_thread is not None):
                    while (julius_thread.proc_r.qsize() != 0):
                        res_data  = julius_thread.get()
                        res_name  = res_data[0]
                        res_value = res_data[1]
                        if (res_name == '[txts]'):
                            for proc_text in res_value:
                                qLog.log('debug', '    julius', proc_text, )

                                # フォース 覚醒
                                if (qRiKi.checkWakeUpWord(proc_text) == True):
                                    if (qFunc.statusCheck(qRdy__s_force) == False):
                                        qFunc.statusSet(qRdy__s_force, True)
                                        qFunc.statusSet(qRdy__s_fproc, True)

                                # 終了操作
                                if ((proc_text.find('システム') >=0) and (proc_text.find('終了') >=0)) \
                                or  (proc_text == 'バルス'):
                                    qFunc.txtsWrite(qCtrl_control_kernel, txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
                                    qFunc.txtsWrite(qCtrl_control_self, txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
                                    break

                # 音声認識 外部インターフェース用
                if (sttreader_thread is not None):
                    while (sttreader_thread.proc_r.qsize() != 0):
                        res_data  = sttreader_thread.get()
                        res_name  = res_data[0]
                        res_value = res_data[1]
                        if (res_name == '[txts]'):
                            for proc_text in res_value:

                                # 文字送信
                                if (qRiKi.checkWakeUpWord(proc_text) == False):
                                    qGUI.notePad(proc_text)
                                    if (qFunc.statusCheck(qRdy__s_sendkey) == True):
                                        qGUI.sendKey(proc_text)

                # 機械翻訳 外部インターフェース用
                if (trareader_thread is not None):
                    while (trareader_thread.proc_r.qsize() != 0):
                        res_data  = trareader_thread.get()
                        res_name  = res_data[0]
                        res_value = res_data[1]
                        if (res_name == '[txts]'):
                            for proc_text in res_value:

                                # 文字送信
                                if (qRiKi.checkWakeUpWord(proc_text) == False):
                                    qGUI.notePad(proc_text)
                                    if (qFunc.statusCheck(qRdy__s_sendkey) == True):
                                        qGUI.sendKey(proc_text)

                # チャットボット 外部インターフェース用
                if (chatbot_thread is not None):
                    while (chatbot_thread.proc_r.qsize() != 0):
                        res_data  = chatbot_thread.get()
                        res_name  = res_data[0]
                        res_value = res_data[1]
                        if (res_name == '[txts]'):
                            for proc_text in res_value:

                                # 文字送信
                                if (qRiKi.checkWakeUpWord(proc_text) == False):
                                    qGUI.notePad(proc_text)
                                    if (qFunc.statusCheck(qRdy__s_sendkey) == True):
                                        qGUI.sendKey(proc_text)

            # アイドリング
            slow = False
            if  (qFunc.statusCheck(qBusy_dev_cpu) == True):
                slow = True
            if  (qFunc.statusCheck(qBusy_dev_mic) == True) \
            and (qFunc.statusCheck(qBusy_dev_spk) == True):
                slow = True

            if (slow == True):
                time.sleep(1.00)
            else:
                if (cn_r.qsize() == 0):
                    time.sleep(0.50)
                else:
                    time.sleep(0.25)

        # 終了処理
        if (True):

            # レディー解除
            qFunc.statusSet(self.fileRdy, False)

            # ビジー解除
            qFunc.statusSet(self.fileBsy, False)

            # スレッド停止
            if (controls_thread is not None):
                controls_thread.abort()
                del controls_thread
                controls_thread = None

            if (adintool_thread is not None):
                adintool_thread.abort()
                del adintool_thread
                adintool_thread = None

            if (voice2wav_thread is not None):
                voice2wav_thread.abort()
                del voice2wav_thread
                voice2wav_thread = None

            if (coreSTT_thread is not None):
                coreSTT_thread.abort()
                del coreSTT_thread
                coreSTT_thread = None

            if (coreTTS_thread is not None):
                coreTTS_thread.abort()
                del coreTTS_thread
                coreTTS_thread = None

            if (playvoice_thread is not None):
                playvoice_thread.abort()
                del playvoice_thread
                playvoice_thread = None

            if (julius_thread is not None):
                julius_thread.abort()
                del julius_thread
                julius_thread = None

            if (sttreader_thread is not None):
                sttreader_thread.abort()
                del sttreader_thread
                sttreader_thread = None

            if (trareader_thread is not None):
                trareader_thread.abort()
                del trareader_thread
                trareader_thread = None

            if (chatbot_thread is not None):
                chatbot_thread.abort()
                del chatbot_thread
                chatbot_thread = None

            # 外部ＰＧリセット
            qFunc.kill('adintool-gui')
            qFunc.kill('adintool')
            qFunc.kill('julius')

            # キュー削除
            while (cn_r.qsize() > 0):
                cn_r_get = cn_r.get()
                cn_r.task_done()
            while (cn_s.qsize() > 0):
                cn_s_get = cn_s.get()
                cn_s.task_done()

            # ログ
            qLog.log('info', self.proc_id, 'end', display=self.logDisp, )
            qFunc.statusSet(self.fileRun, False)
            self.proc_beat = None



# シグナル処理
import signal
def signal_handler(signal_number, stack_frame):
    print(os.path.basename(__file__), 'accept signal =', signal_number)

#signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGINT,  signal.SIG_IGN)
signal.signal(signal.SIGTERM, signal.SIG_IGN)



if __name__ == '__main__':
    main_name = 'speech'
    main_id   = '{0:10s}'.format(main_name).replace(' ', '_')

    # 共通クラス

    qRiKi.init()
    qFunc.init()

    # ログ

    nowTime  = datetime.datetime.now()
    filename = qPath_log + nowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
    qLog.init(mode='logger', filename=filename, )

    qLog.log('info', main_id, 'init')
    qLog.log('info', main_id, 'exsample.py runMode, mic..., ')

    #runMode  debug, hud, live, translator, speech, number, chat, chatbot, camera, assistant, reception,
    #micDev   num or file
    #micType  usb or bluetooth
    #micGuide off, on, display, sound
    #api      free, google, watson, azure, aws, winos, macos,
    #lang     ja, en, fr, kr...

    # パラメータ

    if (True):

        #runMode     = 'live'
        micDev      = '0'
        micType     = 'bluetooth'
        micGuide    = 'on'
        micLevel    = '888'

        if (len(sys.argv) >= 2):
            runMode  = str(sys.argv[1]).lower()

        if   (runMode == 'debug'):
            micType   = 'bluetooth'
            micGuide  = 'on'
        elif (runMode == 'hud'):
            micType   = 'bluetooth'
            micGuide  = 'off'
        elif (runMode == 'live'):
            micType   = 'bluetooth'
            micGuide  = 'off'
        elif (runMode == 'translator'):
            micType   = 'bluetooth'
            micGuide  = 'display'
        elif (runMode == 'speech'):
            micType   = 'usb'
            micGuide  = 'display'
        elif (runMode == 'number'):
            micType   = 'usb'
            micGuide  = 'display'
        elif (runMode == 'chat'):
            micType   = 'bluetooth'
            micGuide  = 'off'
        elif (runMode == 'chatbot'):
            micType   = 'bluetooth'
            micGuide  = 'display'
        elif (runMode == 'camera'):
            micType   = 'bluetooth'
            micGuide  = 'off'
        elif (runMode == 'assistant'):
            micType   = 'usb'
            micGuide  = 'off'
        elif (runMode == 'reception'):
            micType   = 'usb'
            micGuide  = 'off'

        if (len(sys.argv) >= 3):
            micDev   = str(sys.argv[2]).lower()
            if (not micDev.isdigit()):
                micGuide = 'off' 
        if (len(sys.argv) >= 4):
            micType  = str(sys.argv[3]).lower()
        if (len(sys.argv) >= 5):
            micGuide = str(sys.argv[4]).lower()
        if (len(sys.argv) >= 6):
            p = str(sys.argv[5]).lower()
            if (p.isdigit() and p != '0'):
                micLevel = p

        if (len(sys.argv) >= 7):
            qApiInp  = str(sys.argv[6]).lower()
            if (qApiInp == 'google') or (qApiInp == 'watson') \
            or (qApiInp == 'azure')  or (qApiInp == 'aws'):
                qApiTrn  = qApiInp
                qApiOut  = qApiInp
            else:
                qApiTrn  = 'free'
                qApiOut  = 'free'
            #if (qApiInp == 'nict'):
            #    #qLangTrn = 'en,fr,es,id,my,th,vi,zh,ko,'
            #    qLangTrn = 'en,fr,es,id,zh,ko,'
            #    qLangOut = qLangTrn[:2]
        if (len(sys.argv) >= 8):
            qApiTrn  = str(sys.argv[7]).lower()
        if (len(sys.argv) >= 9):
            qApiOut  = str(sys.argv[8]).lower()
        if (len(sys.argv) >= 10):
            qLangInp = str(sys.argv[9]).lower()
            qLangTxt = qLangInp
        if (len(sys.argv) >= 11):
            qLangTrn = str(sys.argv[10]).lower()
            qLangOut = qLangTrn[:2]
        if (len(sys.argv) >= 12):
            qLangTxt = str(sys.argv[11]).lower()
        if (len(sys.argv) >= 13):
            qLangOut = str(sys.argv[12]).lower()

        qLog.log('info', main_id, 'runMode  =' + str(runMode  ))
        qLog.log('info', main_id, 'micDev   =' + str(micDev   ))
        qLog.log('info', main_id, 'micType  =' + str(micType  ))
        qLog.log('info', main_id, 'micGuide =' + str(micGuide ))
        qLog.log('info', main_id, 'micLevel =' + str(micLevel ))

        qLog.log('info', main_id, 'qApiInp  =' + str(qApiInp  ))
        qLog.log('info', main_id, 'qApiTrn  =' + str(qApiTrn  ))
        qLog.log('info', main_id, 'qApiOut  =' + str(qApiOut  ))
        qLog.log('info', main_id, 'qLangInp =' + str(qLangInp ))
        qLog.log('info', main_id, 'qLangTrn =' + str(qLangTrn ))
        qLog.log('info', main_id, 'qLangTxt =' + str(qLangTxt ))
        qLog.log('info', main_id, 'qLangOut =' + str(qLangOut ))

    # 初期設定

    if (True):

        qFunc.remove(qCtrl_control_speech     )

        qFunc.remove(qCtrl_result_audio       )
        qFunc.remove(qCtrl_result_speech      )
        qFunc.remove(qCtrl_recognize          )
        qFunc.remove(qCtrl_recognize_sjis     )
        qFunc.remove(qCtrl_translate          )
        qFunc.remove(qCtrl_translate_sjis     )

        qFunc.makeDirs(qPath_log,      15 )
        qFunc.makeDirs(qPath_work,     15 )
        qFunc.makeDirs(qPath_rec,      15 )

        qFunc.makeDirs(qPath_s_ctrl, True )
        if (micDev.isdigit()):
            qFunc.makeDirs(qPath_s_inp,  True )
        qFunc.makeDirs(qPath_s_wav,  True )
        qFunc.makeDirs(qPath_s_jul,  True )
        qFunc.makeDirs(qPath_s_STT,  True )
        qFunc.makeDirs(qPath_s_TRA,  True )
        if (micDev.isdigit()):
            qFunc.makeDirs(qPath_s_TTS,  True )
            qFunc.makeDirs(qPath_s_play, True )
            qFunc.makeDirs(qPath_s_chat, True )

        qRiKi.statusReset_speech(False)

        #if (runMode == 'assistant'):
        #    qFunc.statusSet(qBusy_dev_mic, True)
        #    qFunc.statusSet(qBusy_dev_spk, True)

    # 起動

    guide_disp = False
    guide_time = time.time()

    main_core = None
    if (True):

        qLog.log('info', main_id, 'start')

        # ガイド表示（開始）

        img = qGuide.getIconImage(filename='_speech_start_', )
        if (img is not None):
            qGuide.init(screen=0, panel='7', title='_speech_start_', image=img, alpha_channel=0.5, )
            qGuide.open()
            guide_disp = True
            guide_time = time.time()

        # コアスレッド起動

        main_core = main_speech(main_id, '0', 
                                runMode=runMode,
                                micDev=micDev, micType=micType, micGuide=micGuide, micLevel=micLevel,
                                qApiInp=qApiInp, qApiTrn=qApiTrn, qApiOut=qApiOut,
                                qLangInp=qLangInp, qLangTrn=qLangTrn, qLangTxt=qLangTxt, qLangOut=qLangOut, )
        main_core.begin()

    # 待機ループ

    while (main_core is not None):

        # 終了確認

        control = ''
        txts, txt = qFunc.txtsRead(qCtrl_control_self)
        if (txts != False):
            qLog.log('info', main_id, '' + str(txt))
            if (txt == '_end_'):
                break
            else:
                qFunc.remove(qCtrl_control_self)
                control = txt

        # スレッド応答

        while (main_core.proc_r.qsize() != 0) and (control == ''):
            res_data  = main_core.get()
            res_name  = res_data[0]
            res_value = res_data[1]
            if (res_name.lower() == 'control'):
                control  = res_value
                break

            # ガイド表示

            if (res_name.lower() == '_guide_'):
                if (guide_disp == True):
                    qGuide.setMessage(txt=res_value, )
                    guide_time = time.time()
                else:
                    img = qGuide.getIconImage(filename='_speech_guide_', )
                    if (img is not None):
                        qGuide.init(screen=0, panel='7', title='_speech_guide_', image=img, alpha_channel=0.5, )
                        qGuide.setMessage(txt=res_value, )
                        #qGuide.open()
                        guide_disp = True
                        guide_time = time.time()

        # ガイド表示（自動消去）

        if (guide_disp == True):
            event, values = qGuide.read()
            if (event in (None, '-exit-', '-cancel-')):
                qGuide.close()
                guide_disp = False
        if (guide_disp == True):
            if ((time.time() - guide_time) > 3):
                qGuide.close()
                guide_disp = False

        # アイドリング

        slow = False
        if   (qFunc.statusCheck(qBusy_dev_cpu) == True):
            slow = True
        elif (qFunc.statusCheck(qBusy_dev_mic) == True) \
         and (qFunc.statusCheck(qRdy__s_force)   == False) \
         and (qFunc.statusCheck(qRdy__s_sendkey) == False):
            slow = True

        if (slow == True):
            time.sleep(1.00)
        else:
            time.sleep(0.25)

    # 終了

    if (True):

        qLog.log('info', main_id, 'terminate')

        # ガイド表示（終了）

        img = qGuide.getIconImage(filename='_speech_stop_', )
        if (img is not None):
            qGuide.init(screen=0, panel='7', title='_speech_stop_', image=img, alpha_channel=0.5, )
            qGuide.open()
            guide_disp = True
            guide_time = time.time()

        # 外部ＰＧリセット

        qFunc.kill('adintool-gui')
        qFunc.kill('adintool')
        qFunc.kill('julius')

        # コアスレッド終了

        if (main_core is not None):
            main_core.abort()
            del main_core

        # ガイド表示終了

        qGuide.close()
        qGuide.terminate()
        guide_disp = False

        time.sleep(2.00)
        qLog.log('info', main_id, 'bye!')

        sys.exit(0)


