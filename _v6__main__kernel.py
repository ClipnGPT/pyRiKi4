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

print(os.path.dirname(__file__))
print(os.path.basename(__file__))
print(sys.version_info)



# インターフェース
qCtrl_control_kernel     = 'temp/control_kernel.txt'
qCtrl_control_speech     = 'temp/control_speech.txt'
qCtrl_control_vision     = 'temp/control_vision.txt'
qCtrl_control_desktop    = 'temp/control_desktop.txt'
qCtrl_control_self       = qCtrl_control_kernel

qCtrl_control_bgm        = 'temp/control_bgm.txt'
qCtrl_control_browser    = 'temp/control_browser.txt'
qCtrl_control_player     = 'temp/control_player.txt'

# Python
qPython_main_speech      = '_v6__main_speech.py'
qPython_main_vision      = '_v6__main_vision.py'
qPython_main_desktop     = '_v6__main_desktop.py'
qPython_bgm              = '_v6__sub_bgm.py'
qPython_browser          = '_v6__sub_browser.py'
qPython_player           = '_v6__sub_player.py'



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



# debug
runMode     = 'hud'

qApiInp     = 'free'
qApiTrn     = 'free'
qApiOut     = qApiTrn
if (qPLATFORM == 'windows'):
    qApiOut = 'winos'
if (qPLATFORM == 'darwin'):
    qApiOut = 'macos'
qLangInp    = 'ja'
#qLangTrn    = 'en,fr,'
qLangTrn    = 'en'
qLangTxt    = qLangInp
qLangOut    = qLangTrn[:2]
cam1Dev     = 'auto'
cam2Dev     = 'auto'



# gui ルーチン
import _v6__main__gui
GUI  = _v6__main__gui.main_gui_class()



class main_kernel:

    def __init__(self, name='thread', id='0', runMode='debug',
                    micDev='0', micType='bluetooth', micGuide='on', micLevel='777',
                    qApiInp='free', qApiTrn='free', qApiOut='free',
                    qLangInp='ja', qLangTrn='en,fr,', qLangTxt='ja', qLangOut='en',
                    cam1Dev='auto', cam2Dev='auto',
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

        self.cam1Dev   = cam1Dev
        self.cam2Dev   = cam2Dev

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

        # 起動条件（controls.pyと合わせる）
        run_priority         = 'normal'
        main_speech_run      = None
        main_speech_switch   = 'on'
        main_vision_run      = None
        main_vision_switch   = 'off'
        main_desktop_run     = None
        main_desktop_switch  = 'off'
        bgm_run              = None
        bgm_switch           = 'off'
        browser_run          = None
        browser_switch       = 'off'
        player_run           = None
        player_switch        = 'off'

        if   (self.runMode == 'debug'):
            main_vision_switch   = 'on'
            main_desktop_switch  = 'on'
            bgm_switch           = 'on'
            browser_switch       = 'on'
            player_switch        = 'on'
        elif (self.runMode == 'hud'):
            main_vision_switch   = 'on'
            main_desktop_switch  = 'on'
            bgm_switch           = 'on'
            browser_switch       = 'on'
            player_switch        = 'on'
        elif (self.runMode == 'live'):
            main_vision_switch   = 'on'
            main_desktop_switch  = 'on'
            bgm_switch           = 'on'
            browser_switch       = 'on'
            player_switch        = 'on'
        elif (self.runMode == 'translator'):
            pass
        elif (self.runMode == 'speech'):
            pass
        elif (self.runMode == 'number'):
            pass
        elif (self.runMode == 'chat'):
            pass
        elif (self.runMode == 'chatbot'):
            pass
        elif (self.runMode == 'camera'):
            main_vision_switch   = 'on'
            main_desktop_switch  = 'on'
        elif (self.runMode == 'assistant'):
            run_priority         = 'below' # 通常以下
            main_vision_switch   = 'on'
            main_desktop_switch  = 'on'
        elif (self.runMode == 'reception'):
            main_vision_switch   = 'on'

        python_exe = 'python'
        if (qPLATFORM == 'darwin'):
            python_exe = 'python3'

        # 実行優先順位設定
        qFunc.setNice(run_priority)

        # 待機ループ
        self.proc_step = '5'

        onece = True
        last_alive = time.time()

        while (self.proc_step == '5'):
            self.proc_beat = time.time()

            # 終了確認
            control = ''
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

            if (main_speech_run is None) and (main_speech_switch == 'on'):
                cn_s.put(['_guide_', 'main_speech start!'])

                if (qRUNATTR == 'python'):
                    main_speech_run = subprocess.Popen([python_exe, qPython_main_speech, 
                                    self.runMode, 
                                    self.micDev, self.micType, self.micGuide, self.micLevel,
                                    self.qApiInp, self.qApiTrn, self.qApiOut,
                                    self.qLangInp, self.qLangTrn, self.qLangTxt, self.qLangOut, ], )
                                    #shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                else:
                    main_speech_run = subprocess.Popen([qPython_main_speech[:-3], 
                                    self.runMode, 
                                    self.micDev, self.micType, self.micGuide, self.micLevel,
                                    self.qApiInp, self.qApiTrn, self.qApiOut,
                                    self.qLangInp, self.qLangTrn, self.qLangTxt, self.qLangOut, ], )
                                    #shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                time.sleep(2.00)

                if   (self.runMode == 'debug'):
                    speechs.append({ 'text':'ハンズフリーコントロールシステムをデバッグモードで、起動しました。', 'wait':0, })
                elif (self.runMode == 'live'):
                    speechs.append({ 'text':'ハンズフリー翻訳機能を、起動しました。', 'wait':0, })
                elif (self.runMode == 'hud'):
                    speechs.append({ 'text':'ヘッドアップディスプレイ機能を、起動しました。', 'wait':0, })
                elif (self.runMode == 'camera'):
                    speechs.append({ 'text':'ハンズフリーカメラ機能を、起動しました。', 'wait':0, })
                elif (self.runMode == 'assistant'):
                    speechs.append({ 'text':'ＡＩアシスタント機能を、起動しました。', 'wait':0, })
                elif (self.runMode == 'reception'):
                    speechs.append({ 'text':'ＡＩ受付機能を、起動しました。', 'wait':0, })

            if (main_speech_run is not None) and (main_speech_switch != 'on'):
                time.sleep(10.00)
                #main_speech_run.wait()
                main_speech_run.terminate()
                main_speech_run = None

            if (main_vision_run is None) and (main_vision_switch == 'on'):
                cn_s.put(['_guide_', 'main_vision start!'])

                if (qRUNATTR == 'python'):
                    main_vision_run = subprocess.Popen([python_exe, qPython_main_vision, 
                                    self.runMode, self.cam1Dev, 'auto', '0', '0', '1.0', self.cam2Dev, ], )
                                    #shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                else:
                    main_vision_run = subprocess.Popen([qPython_main_vision[:-3],
                                    self.runMode, self.cam1Dev, 'auto', '0', '0', '1.0', self.cam2Dev, ], )
                                    #shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                time.sleep(2.00)

                if (self.runMode == 'debug') \
                or (self.runMode == 'live'):
                    speechs.append({ 'text':'カメラ機能を、起動しました。', 'wait':0, })

            if (main_vision_run is not None) and (main_vision_switch != 'on'):
                time.sleep(10.00)
                #main_vision_run.wait()
                main_vision_run.terminate()
                main_vision_run = None

                if (self.runMode == 'debug') \
                or (self.runMode == 'live'):
                    speechs.append({ 'text':'カメラ機能を、終了しました。', 'wait':0, })

            if (main_desktop_run is None) and (main_desktop_switch == 'on'):
                cn_s.put(['_guide_', 'main_desktop start!'])

                if (qRUNATTR == 'python'):
                    main_desktop_run = subprocess.Popen([python_exe, qPython_main_desktop, 
                                    self.runMode, ], )
                                    #shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                else:
                    main_desktop_run = subprocess.Popen([qPython_main_desktop[:-3], 
                                    self.runMode, ], )
                                    #shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                time.sleep(2.00)

                if (self.runMode == 'debug') \
                or (self.runMode == 'live'):
                    speechs.append({ 'text':'デスクトップ制御機能を、起動しました。', 'wait':0, })

            if (main_desktop_run is not None) and (main_desktop_switch != 'on'):
                time.sleep(10.00)
                #main_desktop_run.wait()
                main_desktop_run.terminate()
                main_desktop_run = None

                if (self.runMode == 'debug') \
                or (self.runMode == 'live'):
                    speechs.append({ 'text':'デスクトップ制御機能を、終了しました。', 'wait':0, })

            if (bgm_run is None) and (bgm_switch == 'on'):
                cn_s.put(['_guide_', 'bgm control start!'])

                if (qRUNATTR == 'python'):
                    bgm_run = subprocess.Popen([python_exe, qPython_bgm, self.runMode, ], )
                                #shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                else:
                    bgm_run = subprocess.Popen([qPython_bgm[:-3], self.runMode, ], )
                                #shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                time.sleep(2.00)

                if (self.runMode == 'debug') \
                or (self.runMode == 'live'):
                    speechs.append({ 'text':'ＢＧＭ再生機能を、起動しました。', 'wait':0, })

            if (bgm_run is not None) and (bgm_switch != 'on'):
                qFunc.txtsWrite(qCtrl_control_bgm, txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
                time.sleep(10.00)
                #bgm_run.wait()
                bgm_run.terminate()
                bgm_run = None

                if (self.runMode == 'debug') \
                or (self.runMode == 'live'):
                    speechs.append({ 'text':'ＢＧＭ再生機能を、終了しました。', 'wait':0, })

            if (browser_run is None) and (browser_switch == 'on'):
                cn_s.put(['_guide_', 'browser control start!'])

                if (qRUNATTR == 'python'):
                    browser_run = subprocess.Popen([python_exe, qPython_browser, self.runMode, ], )
                                #shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                else:
                    browser_run = subprocess.Popen([qPython_browser[:-3], self.runMode, ], )
                                #shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                time.sleep(2.00)

                if (self.runMode == 'debug') \
                or (self.runMode == 'live'):
                    speechs.append({ 'text':'ブラウザー連携機能を、起動しました。', 'wait':0, })

            if (browser_run is not None) and (browser_switch != 'on'):
                qFunc.txtsWrite(qCtrl_control_browser, txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
                time.sleep(10.00)
                #browser_run.wait()
                browser_run.terminate()
                browser_run = None

                if (self.runMode == 'debug') \
                or (self.runMode == 'live'):
                    speechs.append({ 'text':'ブラウザー連携機能を、終了しました。', 'wait':0, })

            if (player_run is None) and (player_switch == 'on'):
                cn_s.put(['_guide_', 'player control start!'])

                if (qRUNATTR == 'python'):
                    player_run = subprocess.Popen([python_exe, qPython_player, self.runMode, ], )
                                 #shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                else:
                    player_run = subprocess.Popen([qPython_player[:-3], self.runMode, ], )
                                 #shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                time.sleep(2.00)

                if (self.runMode == 'debug') \
                or (self.runMode == 'live'):
                    speechs.append({ 'text':'動画連携機能を、起動しました。', 'wait':0, })

            if (player_run is not None) and (player_switch != 'on'):
                qFunc.txtsWrite(qCtrl_control_player, txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
                time.sleep(10.00)
                #player_run.wait()
                player_run.terminate()
                player_run = None

                if (self.runMode == 'debug') \
                or (self.runMode == 'live'):
                    speechs.append({ 'text':'動画連携機能を、終了しました。', 'wait':0, })

            if (len(speechs) != 0):
                qRiKi.speech(id=main_id, speechs=speechs, lang='', )

            if (onece == True):
                onece = False

                if (self.runMode == 'debug') \
                or (self.runMode == 'live'):
                    time.sleep(40)
                    speechs = []
                    speechs.append({ 'text':'全ての準備が整いました。スタンバイしています。', 'wait':0, })
                    qRiKi.speech(id=main_id, speechs=speechs, lang='', )

            # レディー設定
            if (qFunc.statusCheck(self.fileRdy) == False):
                qFunc.statusSet(self.fileRdy, True)

            # ステータス応答
            if (inp_name.lower() == '_status_'):
                out_name  = inp_name
                out_value = '_ready_'
                cn_s.put([out_name, out_value])

            # リブート
            #if (control == '_reboot_'):
            #    out_name  = 'control'
            #    out_value = control
            #    cn_s.put([out_name, out_value])

            # コントロール
            control = ''
            if (inp_name.lower() == 'control'):
                control = inp_value
            if (control == '_speech_begin_'):
                main_speech_switch   = 'on'
            if (control == '_speech_end_'):
                main_speech_switch   = 'off'
            if (control == '_vision_begin_'):
                main_vision_switch   = 'on'
            if (control == '_vision_end_'):
                main_vision_switch   = 'off'
            if (control == '_desktop_begin_'):
                main_desktop_switch  = 'on'
            if (control == '_desktop_end_'):
                main_desktop_switch  = 'off'
            if (control == '_bgm_begin_'):
                bgm_switch           = 'on'
            if (control == '_bgm_end_') or (control == '_reboot_'):
                bgm_switch           = 'off'
            if (control == '_browser_begin_'):
                browser_switch       = 'on'
            if (control == '_browser_end_') or (control == '_reboot_'):
                browser_switch       = 'off'
            if (control == '_player_begin_'):
                player_switch        = 'on'
            if (control == '_player_end_') or (control == '_reboot_'):
                player_switch        = 'off'

            # アイドリング
            slow = False
            if (qFunc.statusCheck(qBusy_dev_cpu) == True):
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

            # プロセス終了
            qFunc.txtsWrite(qCtrl_control_kernel    ,txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
            qFunc.txtsWrite(qCtrl_control_speech    ,txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
            qFunc.txtsWrite(qCtrl_control_vision    ,txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
            qFunc.txtsWrite(qCtrl_control_desktop   ,txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
            qFunc.txtsWrite(qCtrl_control_bgm       ,txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
            qFunc.txtsWrite(qCtrl_control_browser   ,txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
            qFunc.txtsWrite(qCtrl_control_player    ,txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )

            # スレッド停止
            if (main_speech_run is not None):
                main_speech_run.wait()
                main_speech_run.terminate()
                main_speech_run = None

            if (main_vision_run is not None):
                main_vision_run.wait()
                main_vision_run.terminate()
                main_vision_run = None

            if (main_desktop_run is not None):
                main_desktop_run.wait()
                main_desktop_run.terminate()
                main_desktop_run = None

            if (bgm_run is not None):
                bgm_run.wait()
                bgm_run.terminate()
                bgm_run = None

            if (browser_run is not None):
                #browser_run.wait()
                browser_run.terminate()
                browser_run = None

            if (player_run is not None):
                #player_run.wait()
                player_run.terminate()
                player_run = None

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
    main_name = 'kernel'
    main_id   = '{0:10s}'.format(main_name).replace(' ', '_')

    # 共通クラス

    qRiKi.init()
    qFunc.init()

    # ログ

    nowTime  = datetime.datetime.now()
    filename = qPath_log + nowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
    qLog.init(mode='logger', filename=filename, )

    qLog.log('info', main_id, 'init')
    qLog.log('info', main_id, 'exsample.py runMode, ..., ')

    #runMode  debug, hud, live, translator, speech, number, chat, chatbot, camera, assistant, reception,

    # パラメータ

    if (True):

        #runMode     = 'live'
        micDev      = '0'
        micType     = 'bluetooth'
        micGuide    = 'on'
        micLevel    = '777'

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
            micGuide  = 'on'
        elif (runMode == 'speech'):
            micType   = 'usb'
            micGuide  = 'on'
        elif (runMode == 'number'):
            micType   = 'usb'
            micGuide  = 'on'
        elif (runMode == 'chat'):
            micType   = 'bluetooth'
            micGuide  = 'off'
        elif (runMode == 'chatbot'):
            micType   = 'bluetooth'
            micGuide  = 'on'
        elif (runMode == 'camera'):
            micType   = 'usb'
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
        if (len(sys.argv) >= 14):
            cam1Dev = str(sys.argv[13])
        if (len(sys.argv) >= 15):
            cam2Dev = str(sys.argv[14])

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

        qLog.log('info', main_id, 'cam1Dev  =' + str(cam1Dev  ))
        qLog.log('info', main_id, 'cam2Dev  =' + str(cam2Dev  ))

    # 初期設定

    if (qPLATFORM == 'darwin'):
        try:
            print('macOSでTKinterの利用設定　開始')
            subprocess.call(['/usr/bin/osascript', '-e',
            'tell app "Finder" to set frontmost of process "python" to true'])
            print('macOSでTKinterの利用設定　完了')
        except Exception as e:
            print('macOSでTKinterの利用設定　失敗')

    if (True):
        qFunc.remove(qCtrl_control_kernel    )
        qFunc.remove(qCtrl_control_speech    )
        qFunc.remove(qCtrl_control_vision    )
        qFunc.remove(qCtrl_control_desktop   )
        qFunc.remove(qCtrl_control_bgm       )
        qFunc.remove(qCtrl_control_browser   )
        qFunc.remove(qCtrl_control_player    )

        qRiKi.statusReset_speech(False)
        qRiKi.statusReset_vision(False)
        qRiKi.statusReset_desktop(False)


    # ＧＵＩ

    gui_disp   = False
    gui_time   = time.time()
    mouse_xy_zero = False
    mouse_xy_time = time.time()

    # 起動

    guide_disp = False
    guide_time = time.time()

    main_core = None
    if (True):

        qLog.log('info', main_id, 'start')

        # ガイド表示（開始）

        img = qGuide.getIconImage(filename='_kernel_start_', )
        if (img is not None):
            qGuide.init(screen=0, panel='1', title='_kernel_start_', image=img, alpha_channel=0.5, )
            qGuide.open()
            guide_disp = True
            guide_time = time.time()

        # コアスレッド起動

        main_core = main_kernel(main_id, '0', 
                                runMode=runMode,
                                micDev=micDev, micType=micType, micGuide=micGuide, micLevel=micLevel,
                                qApiInp=qApiInp, qApiTrn=qApiTrn, qApiOut=qApiOut,
                                qLangInp=qLangInp, qLangTrn=qLangTrn, qLangTxt=qLangTxt, qLangOut=qLangOut, 
                                cam1Dev=cam1Dev, cam2Dev=cam2Dev, )
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

        # 起動制御

        if (control.lower()[:8] == '_speech_') \
        or (control.lower()[:8] == '_vision_') \
        or (control.lower()[:9] == '_desktop_') \
        or (control.lower()[:5] == '_bgm_') \
        or (control.lower()[:9] == '_browser_') \
        or (control.lower()[:8] == '_player_'):
            main_core.put(['control', control])
            control = ''

        # リブート

        if (control == '_reboot_'):
            main_core.abort()
            del main_core
            qFunc.remove(qCtrl_control_kernel)
            main_core = None
            main_core = main_kernel(main_id, '0', 
                                    runMode=runMode,
                                    micDev=micDev, micType=micType, micGuide=micGuide, micLevel=micLevel,
                                    qApiInp=qApiInp, qApiTrn=qApiTrn, qApiOut=qApiOut,
                                    qLangInp=qLangInp, qLangTrn=qLangTrn, qLangTxt=qLangTxt, qLangOut=qLangOut, )
            main_core.begin()

        # ＧＵＩ表示

        if (control == '_gui_'):
            GUI.init(alpha_channel=0.7, )
            GUI.open()
            gui_disp = True
            gui_time = time.time()

        if (gui_disp == True):
            GUI.statusSet('_STS_SPEECH_', qFunc.statusCheck(qBusy_s_inp, ), )
            GUI.statusSet('_STS_RECORD_', qFunc.statusCheck(qBusy_d_rec, ), )
            GUI.statusSet('_STS_TELEWORK_', qFunc.statusCheck(qBusy_d_telework, ), )
        else:
            x, y = qGUI.position()
            if (x<100) and (y<100):
                if (mouse_xy_zero == True):
                    if ((time.time() - mouse_xy_time) > 3):
                        GUI.init(alpha_channel=0.7, )
                        GUI.open()
                        gui_disp = True
                        gui_time = time.time()
                        try:
                            qGUI.moveTo(0,101)
                        except:
                            pass
                else:
                    mouse_xy_zero = True
                    mouse_xy_time = time.time()
            else:
                    mouse_xy_zero = False

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
                    img = qGuide.getIconImage(filename='_kernel_guide_', )
                    if (img is not None):
                        qGuide.init(screen=0, panel='1', title='_kernel_guide_', image=img, alpha_channel=0.5, )
                        qGuide.setMessage(txt=res_value, )
                        #qGuide.open()
                        guide_disp = True
                        guide_time = time.time()

        # ＧＵＩ表示（自動消去）

        if (gui_disp == True):
            event, values = GUI.read()
            if (event in (None, '-exit-', '-cancel-')):
                #print(event, values)
                GUI.close()
                gui_disp = False
            if (event == '-ok-'):
                #print(event, values)
                GUI.close()
                gui_disp = False
            if (event[:5].lower() == 'riki,'):
                #print(event, values)
                GUI.close()
                gui_disp = False
                nowTime = datetime.datetime.now()
                stamp   = nowTime.strftime('%Y%m%d.%H%M%S')
                controld_file = qPath_s_ctrl + stamp + '.txt'
                qFunc.txtsWrite(controld_file, txts=[event], encoding='utf-8', exclusive=True, mode='w', )
                controld_file = qPath_v_ctrl + stamp + '.txt'
                qFunc.txtsWrite(controld_file, txts=[event], encoding='utf-8', exclusive=True, mode='w', )
                controld_file = qPath_d_ctrl + stamp + '.txt'
                qFunc.txtsWrite(controld_file, txts=[event], encoding='utf-8', exclusive=True, mode='w', )
            x, y = qGUI.position()
            if (x==0) and (y==0):
                gui_time = time.time()
            if ((time.time() - gui_time) > 15):
                GUI.close()
                gui_disp = False

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

        if (slow == True):
            time.sleep(1.00)
        else:
            time.sleep(0.25)

    # 終了

    if (True):

        qLog.log('info', main_id, 'terminate')

        # ＧＵＩ終了

        GUI.close()
        GUI.terminate()
        gui_disp = False

        # ガイド表示（終了）

        img = qGuide.getIconImage(filename='_kernel_stop_', )
        if (img is not None):
            qGuide.init(screen=0, panel='1', title='_kernel_stop_', image=img, alpha_channel=0.5, )
            qGuide.open()
            guide_disp = True
            guide_time = time.time()

        # コアスレッド終了

        if (main_core is not None):
            main_core.abort()
            del main_core

        # ガイド表示終了

        qGuide.close()
        qGuide.terminate()
        guide_disp = False

        time.sleep(5.00)
        qLog.log('info', main_id, 'bye!')

        sys.exit(0)


