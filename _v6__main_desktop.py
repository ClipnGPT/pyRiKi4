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

import cv2

#print(os.path.dirname(__file__))
#print(os.path.basename(__file__))
#print(sys.version_info)



# インターフェース
qCtrl_control_kernel     = 'temp/control_kernel.txt'
qCtrl_control_speech     = 'temp/control_speech.txt'
qCtrl_control_vision     = 'temp/control_vision.txt'
qCtrl_control_desktop    = 'temp/control_desktop.txt'
qCtrl_control_self       = qCtrl_control_desktop

qCtrl_control_browser    = 'temp/control_browser.txt'
qCtrl_control_player     = 'temp/control_player.txt'
qCtrl_control_telop      = 'temp/control_telop.txt'

# 出力インターフェース
qCtrl_result_desktop      = 'temp/result_desktop.txt'
qCtrl_result_prtscn       = 'temp/result_prtscn.jpg'
qCtrl_result_capture      = 'temp/result_capture.txt'
qCtrl_result_movie        = 'temp/result_movie.mp4'
qCtrl_result_recorder     = 'temp/result_recorder.txt'
qCtrl_result_telework     = 'temp/result_telework.txt'



# 共通ルーチン
import  _v6__qRiKi
qRiKi = _v6__qRiKi.qRiKi_class()
import  _v6__qFunc
qFunc = _v6__qFunc.qFunc_class()
import  _v6__qLog
qLog  = _v6__qLog.qLog_class()
import  _v6__qGuide
qGuide= _v6__qGuide.qGuide_class()
qGuide2=_v6__qGuide.qGuide_class()

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
import _v6_proc_controld
import _v6_proc_capture
import _v6_proc_cvreader
import _v6_proc_recorder
import _v6_proc_telework
if (qPLATFORM == 'windows'):
    import _v6_proc_uploader
import _v6_proc_pointer



# debug
runMode     = 'assistant'
runMode     = 'telework'



class main_desktop:

    def __init__(self, name='thread', id='0', runMode='debug', ):
        self.runMode   = runMode

        self.capStretch = '0'
        self.capRotate  = '0'
        self.capZoom    = '1'
        self.codeRead   = 'qr'

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
        qFunc.kill('ffmpeg')
        qFunc.kill('ffplay')
        qFunc.kill('ffprobe')

        # 起動条件
        run_priority         = 'normal'
        controld_thread      = None
        controld_switch      = 'on'
        capture_thread       = None
        capture_switch       = 'on'
        cvreader_thread      = None
        cvreader_switch      = 'on'
        recorder_thread      = None
        recorder_switch      = 'on'
        telework_thread      = None
        telework_switch      = 'on'
        uploader_thread      = None
        uploader_switch      = 'off'
        pointer_thread       = None
        pointer_switch       = 'off'

        if (self.runMode == 'debug'):
            capture_switch   = 'on'
            cvreader_switch  = 'on'
            recorder_switch  = 'on'
            telework_switch  = 'on'
            uploader_switch  = 'on'
            pointer_switch   = 'on'
        elif (self.runMode == 'hud'):
            capture_switch   = 'off'
            cvreader_switch  = 'off'
            recorder_switch  = 'on'
            telework_switch  = 'off'
            uploader_switch  = 'off'
            pointer_switch   = 'off'
        elif (self.runMode == 'live'):
            capture_switch   = 'off'
            cvreader_switch  = 'on'
            recorder_switch  = 'on'
            telework_switch  = 'off'
            uploader_switch  = 'off'
            pointer_switch   = 'off'
        elif (self.runMode == 'camera'):
            capture_switch   = 'off'
            cvreader_switch  = 'off'
            recorder_switch  = 'on'
            telework_switch  = 'off'
            uploader_switch  = 'off'
            pointer_switch   = 'off'
        elif (self.runMode == 'assistant'):
            run_priority     = 'below' # 通常以下
            capture_switch   = 'on'
            cvreader_switch  = 'on'
            recorder_switch  = 'on'
            telework_switch  = 'on'
            uploader_switch  = 'on'
            pointer_switch   = 'on'
        elif (self.runMode == 'reception'):
            capture_switch   = 'off'
            cvreader_switch  = 'off'
            recorder_switch  = 'off'
            telework_switch  = 'off'
            uploader_switch  = 'off'
            pointer_switch   = 'off'
        elif (self.runMode == 'recorder'):
            run_priority     = 'below' # 通常以下
            capture_switch   = 'off'
            cvreader_switch  = 'off'
            recorder_switch  = 'on'
            telework_switch  = 'off'
            uploader_switch  = 'on'
            pointer_switch   = 'off'
        elif (self.runMode == 'telework'):
            run_priority     = 'below' # 通常以下
            capture_switch   = 'off'
            cvreader_switch  = 'off'
            recorder_switch  = 'off'
            telework_switch  = 'on'
            uploader_switch  = 'on'
            pointer_switch   = 'on'

        if (qPLATFORM != 'windows'):
            uploader_switch  = 'off'

        # 実行優先順位設定
        qFunc.setNice(run_priority)

        # 待機ループ
        self.proc_step = '5'

        main_img = None
        win_img  = None

        cvreader_last_put  = time.time()
        cvreader_last_code = ''

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

            if (controld_thread is None) and (controld_switch == 'on'):
                cn_s.put(['_guide_', 'controld start!'])

                controld_thread = _v6_proc_controld.proc_controld(
                                    name='controld', id='0',
                                    runMode=self.runMode,
                                    )
                controld_thread.begin()
                time.sleep(1.00)

                if (self.runMode == 'debug') \
                or (self.runMode == 'live'):
                    speechs.append({ 'text':'「デスクトップ制御」の機能が有効になりました。', 'wait':0, })

            if (controld_thread is not None) and (controld_switch != 'on'):
                controld_thread.abort()
                del controld_thread
                controld_thread = None

            if (capture_thread is None) and (capture_switch == 'on'):
                cn_s.put(['_guide_', 'capture start!'])

                capture_thread = _v6_proc_capture.proc_capture(
                                    name='capture', id='0',
                                    runMode=self.runMode,
                                    capStretch=self.capStretch, capRotate=self.capRotate, capZoom=self.capZoom, capFps='2',
                                    )
                capture_thread.begin()
                time.sleep(1.00)

                if (self.runMode == 'debug') \
                or (self.runMode == 'live'):
                    speechs.append({ 'text':'「デスクトップ入力」の機能が有効になりました。', 'wait':0, })

            if (capture_thread is not None) and (capture_switch != 'on'):
                capture_thread.abort()
                del capture_thread
                capture_thread = None

            if (cvreader_thread is None) and (cvreader_switch == 'on'):
                cn_s.put(['_guide_', 'cvreader start!'])

                cvreader_thread = _v6_proc_cvreader.proc_cvreader(
                                    name='reader', id='d',
                                    runMode=self.runMode, 
                                    reader=self.codeRead,
                                    )
                cvreader_thread.begin()
                time.sleep(1.00)

                if (self.runMode == 'debug') \
                or (self.runMode == 'live'):
                    speechs.append({ 'text':'「画面ＱＲコード認識」の機能が有効になりました。', 'wait':0, })

            if (cvreader_thread is not None) and (cvreader_switch != 'on'):
                cvreader_thread.abort()
                del cvreader_thread
                cvreader_thread = None

            if (recorder_thread is None) and (recorder_switch == 'on'):
                cn_s.put(['_guide_', 'recorder start!'])

                recorder_thread  = _v6_proc_recorder.proc_recorder(
                                    name='recorder', id='0',
                                    runMode=self.runMode,
                                    )
                recorder_thread.begin()
                time.sleep(1.00)

                if (self.runMode == 'debug') \
                or (self.runMode == 'live'):
                    speechs.append({ 'text':'「デスクトップ記録」の機能が有効になりました。', 'wait':0, })

                # 記録開始
                if (self.runMode == 'recorder'):
                    recorder_thread.put(['control', '_rec_start_'])

            if (recorder_thread is not None) and (recorder_switch != 'on'):
                recorder_thread.abort()
                del recorder_thread
                recorder_thread = None

            if (telework_thread is None) and (telework_switch == 'on'):
                cn_s.put(['_guide_', 'telework start!'])

                telework_thread  = _v6_proc_telework.proc_telework(
                                    name='telework', id='0',
                                    runMode=self.runMode,
                                    )
                telework_thread.begin()
                time.sleep(1.00)

                if (self.runMode == 'debug') \
                or (self.runMode == 'live'):
                    speechs.append({ 'text':'「テレワーク記録」の機能が有効になりました。', 'wait':0, })

                # 記録開始
                if (self.runMode == 'telework'):
                    telework_thread.put(['control', '_telework_start_'])

            if (telework_thread is not None) and (telework_switch != 'on'):
                telework_thread.abort()
                del telework_thread
                telework_thread = None

            if (uploader_thread is None) and (uploader_switch == 'on'):
                cn_s.put(['_guide_', 'uploader start!'])

                uploader_thread  = _v6_proc_uploader.proc_uploader(
                                    name='uploader', id='0',
                                    runMode=self.runMode,
                                    )
                uploader_thread.begin()
                time.sleep(1.00)

                if (self.runMode == 'debug') \
                or (self.runMode == 'live'):
                    speechs.append({ 'text':'「ブロブ連携」の機能が有効になりました。', 'wait':0, })

            if (pointer_thread is not None) and (pointer_switch != 'on'):
                pointer_thread.abort()
                del pointer_thread
                pointer_thread = None

            if (pointer_thread is None) and (pointer_switch == 'on'):
                cn_s.put(['_guide_', 'pointer start!'])

                pointer_thread  = _v6_proc_pointer.proc_pointer(
                                    name='pointer', id='0',
                                    runMode=self.runMode,
                                    )
                pointer_thread.begin()
                time.sleep(1.00)

                if (self.runMode == 'debug') \
                or (self.runMode == 'live'):
                    speechs.append({ 'text':'「マウスポインタ表示」の機能が有効になりました。', 'wait':0, })

            if (pointer_thread is not None) and (pointer_switch != 'on'):
                pointer_thread.abort()
                del pointer_thread
                pointer_thread = None

            if (len(speechs) != 0):
                qRiKi.speech(id=self.proc_id, speechs=speechs, lang='', )

            if (onece == True):
                onece = False

                if   (self.runMode == 'debug') \
                or   (self.runMode == 'live'):
                    speechs = []
                    speechs.append({ 'text':'「デスクトップ制御」の準備が完了しました。', 'wait':0, })
                    qRiKi.speech(id=self.proc_id, speechs=speechs, lang='', )

            # レディー設定
            if (qFunc.statusCheck(self.fileRdy) == False):
                qFunc.statusSet(self.fileRdy, True)

            # ステータス応答
            if (inp_name.lower() == '_status_'):
                out_name  = inp_name
                out_value = '_ready_'
                cn_s.put([out_name, out_value])

            # レコーダー制御
            if (inp_name.lower() == 'recorder'):
                if (recorder_thread is not None):
                    recorder_thread.put(['control', inp_value])

            # テレワーク制御
            if (inp_name.lower() == 'telework'):
                if (telework_thread is not None):
                    telework_thread.put(['control', inp_value])

            # 制御処理
            control = ''

            if (controld_thread is not None):
                while (controld_thread.proc_r.qsize() != 0):
                    res_data  = controld_thread.get()
                    res_name  = res_data[0]
                    res_value = res_data[1]

                    # 制御
                    if (res_name.lower() == 'control'):
                        control = res_value
                        # 結果出力
                        cn_s.put([res_name, res_value])
                        break

                    # レコーダー制御
                    if (res_name.lower() == 'recorder'):
                        if (recorder_thread is not None):
                            recorder_thread.put(['control', res_value])

                    # テレワーク制御
                    if (res_name.lower() == 'telework'):
                        if (telework_thread is not None):
                            telework_thread.put(['control', res_value])

                    # ガイド表示
                    if (res_name.lower() == '_guide_'):
                        cn_s.put(['_guide_', res_value])

            # 画像入力（デスクトップ）
            if (capture_thread is not None):
                while (capture_thread.proc_r.qsize() != 0):
                    res_data  = capture_thread.get()
                    res_name  = res_data[0]
                    res_value = res_data[1]
                    if (res_name == '_fps_'):
                        pass
                    if (res_name == '_reso_'):
                        pass
                    if (res_name == '[window]'):
                        if (res_value is None):
                            win_img = None
                        else:
                            win_img = res_value.copy()
                    if (res_name == '[img]'):
                        main_img = res_value.copy()

                        # 画像識別（ＱＲ）
                        if ((time.time() - cvreader_last_put) >= 1):
                            if (cvreader_thread is not None):
                                if (cvreader_thread.proc_s.qsize() == 0):
                                    cvreader_thread.put(['[img]', main_img ])
                                    cvreader_last_put = time.time()

                        break

            # 画像合成（ＱＲ　識別結果）
            if (cvreader_thread is not None):
                while (cvreader_thread.proc_r.qsize() != 0):
                    res_data  = cvreader_thread.get()
                    res_name  = res_data[0]
                    res_value = res_data[1]
                    if (res_name == '[img]'):
                        pass
                    if (res_name == '[txts]'):

                        # コントロール出力
                        if (res_value[0][:1] == '_'):
                            nowTime = datetime.datetime.now()
                            stamp   = nowTime.strftime('%Y%m%d.%H%M%S')
                            controld_file = qPath_d_ctrl + stamp + '.txt'
                            qFunc.txtsWrite(controld_file, txts=res_value, encoding='utf-8', exclusive=True, mode='w', )

                        # 画面表示
                        #qFunc.txtsWrite(qCtrl_control_browser, txts=res_value, encoding='utf-8', exclusive=True, mode='w', )
                        #qFunc.txtsWrite(qCtrl_control_player, txts=res_value, encoding='utf-8', exclusive=True, mode='w', )

            # 記録機能
            if (recorder_thread is not None):
                while (recorder_thread.proc_r.qsize() != 0):
                    res_data  = recorder_thread.get()
                    res_name  = res_data[0]
                    res_value = res_data[1]

                    # ガイド表示
                    if (res_name.lower() == '_guide_'):
                        cn_s.put(['_guide_', res_value])

            # 記録機能
            if (telework_thread is not None):
                while (telework_thread.proc_r.qsize() != 0):
                    res_data  = telework_thread.get()
                    res_name  = res_data[0]
                    res_value = res_data[1]

                    # ガイド表示
                    if   (res_name.lower() == '_guide_'):
                        cn_s.put(['_guide_', res_value])

                    # テレワークガイド表示
                    elif (res_name.lower() == '_telework_guide_image_'):
                        cn_s.put([res_name, res_value])
                    elif (res_name.lower() == '_telework_guide_close_'):
                        cn_s.put([res_name, res_value])

            # アップロード機能
            if (uploader_thread is not None):
                while (uploader_thread.proc_r.qsize() != 0):
                    res_data  = uploader_thread.get()

            # マウスポインタ機能
            if (pointer_thread is not None):
                while (pointer_thread.proc_r.qsize() != 0):
                    res_data  = pointer_thread.get()

            # キャプチャ
            if (control == '_capture_'):
                if (main_img is not None):

                    # シャッター音
                    qFunc.guideSound('_shutter', sync=False)

                    # キャプチャ保存
                    nowTime = datetime.datetime.now()
                    stamp   = nowTime.strftime('%Y%m%d.%H%M%S')
                    self.save_capture(stamp, 'capture', main_img)

                    # ウィンドウ保存
                    if (win_img is not None):
                        self.save_capture(stamp, 'window', win_img)

                    # ガイド表示
                    cn_s.put(['_guide_', 'capture !'])


            # アイドリング
            slow = False
            if (qFunc.statusCheck(qBusy_dev_cpu) == True):
                slow = True
            if (qFunc.statusCheck(qBusy_dev_scn) == True):
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
            if (controld_thread is not None):
                controld_thread.abort()
                del controld_thread
                controld_thread = None

            if (capture_thread is not None):
                capture_thread.abort()
                del capture_thread
                capture_thread = None

            if (cvreader_thread is not None):
                cvreader_thread.abort()
                del cvreader_thread
                cvreader_thread = None

            if (recorder_thread is not None):
                recorder_thread.abort()
                qFunc.statusWait_false(qBusy_d_rec, falseWait=30)
                del recorder_thread
                recorder_thread = None

            if (telework_thread is not None):
                telework_thread.abort()
                del telework_thread
                telework_thread = None

            if (uploader_thread is not None):
                uploader_thread.abort()
                del uploader_thread
                uploader_thread = None

            if (pointer_thread is not None):
                pointer_thread.abort()
                del pointer_thread
                pointer_thread = None

            # 外部ＰＧリセット
            qFunc.kill('ffmpeg')
            qFunc.kill('ffplay')
            qFunc.kill('ffprobe')

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



    def save_capture(self, stamp, filemark, save_img):

        yyyymmdd = stamp[:8]

        # イメージ保存
        save_file = ''
        save_file = qPath_rec + stamp + '.' + filemark + '.jpg'
        cv2.imwrite(save_file, save_img)

        # クリップボードへ
        if (filemark == 'capture'):
            qGuide.img2clip(save_file)

        # コピー保存
        filename_s1 = qPath_d_prtscn + stamp + '.' + filemark + '.jpg'
        filename_s2 = qPath_d_upload + stamp + '.' + filemark + '.jpg'
        filename_s3 = qCtrl_result_prtscn
        #filename_s4 = qPath_pictures + stamp + '.' + filemark + '.jpg'
        qFunc.copy(save_file, filename_s1)
        qFunc.copy(save_file, filename_s2)
        qFunc.copy(save_file, filename_s3)
        if (qPath_pictures != ''):
            #qFunc.copy(save_file, filename_s4)
            folder = qPath_pictures + yyyymmdd + '/'
            qFunc.makeDirs(folder)
            qFunc.copy(save_file, folder + stamp + '.' + filemark + '.jpg')

            qFunc.txtsWrite(qCtrl_result_capture, txts=[stamp + '.' + filemark + '.jpg'], encoding='utf-8', exclusive=True, mode='w', )



# シグナル処理
import signal
def signal_handler(signal_number, stack_frame):
    print(os.path.basename(__file__), 'accept signal =', signal_number)

#signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGINT,  signal.SIG_IGN)
signal.signal(signal.SIGTERM, signal.SIG_IGN)



if __name__ == '__main__':
    main_name = 'desktop'
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

    # パラメータ

    if (True):

        #runMode     = 'debug'

        if (len(sys.argv) >= 2):
            runMode  = str(sys.argv[1]).lower()

        qLog.log('info', main_id, 'runMode  =' + str(runMode  ))

    # 初期設定

    if (True):

        qFunc.remove(qCtrl_control_desktop  )

        qFunc.remove(qCtrl_result_desktop   )
        qFunc.remove(qCtrl_result_prtscn    )
        qFunc.remove(qCtrl_result_capture   )
        qFunc.remove(qCtrl_result_movie     )
        qFunc.remove(qCtrl_result_recorder  )
        qFunc.remove(qCtrl_result_telework  )

        qFunc.makeDirs(qPath_log,        15 )
        qFunc.makeDirs(qPath_work,       15 )
        qFunc.makeDirs(qPath_rec,        15 )

        qFunc.makeDirs(qPath_d_ctrl,   True )
        qFunc.makeDirs(qPath_d_play,   True )
        qFunc.makeDirs(qPath_d_prtscn, True )
        qFunc.makeDirs(qPath_d_movie,  True )
        qFunc.makeDirs(qPath_d_telop,  True )
        qFunc.makeDirs(qPath_d_upload, True )

        if (qPath_videos != ''):
            qFunc.makeDirs(qPath_videos, 15 )

        qRiKi.statusReset_desktop(False)

    # 起動

    guide_disp = False
    guide_time = time.time()
    guide2_disp = False
    guide2_time = time.time()

    main_core = None
    if (True):

        qLog.log('info', main_id, 'start')

        # ガイド表示（開始）

        img = qGuide.getIconImage(filename='_desktop_start_', )
        if (img is not None):
            qGuide.init(screen=0, panel='9', title='_desktop_start_', image=img, alpha_channel=0.5, )
            qGuide.open()
            guide_disp = True
            guide_time = time.time()

        # コアスレッド起動

        main_core = main_desktop(main_id, '0', runMode=runMode, )
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

        # レコーダー制御

        if (control.lower() == '_rec_start_') \
        or (control.lower() == '_rec_stop_') \
        or (control.lower() == '_rec_restart_') \
        or (control.find('記録') >= 0) \
        or (control.find('録画') >= 0):
            main_core.put(['recorder', control])
            control = ''

        # テレワーク制御

        if (control.lower() == '_telework_start_') \
        or (control.lower() == '_telework_stop_') \
        or (control.lower() == '_telework_restart_') \
        or (control.find('テレワーク') >= 0):
            main_core.put(['telework', control])
            control = ''

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
                    img = qGuide.getIconImage(filename='_desktop_guide_', )
                    if (img is not None):
                        qGuide.init(screen=0, panel='9', title='_desktop_guide_', image=img, alpha_channel=0.5, )
                        qGuide.setMessage(txt=res_value, )
                        #qGuide.open()
                        guide_disp = True
                        guide_time = time.time()

            # テレワークガイド表示

            if  (res_name.lower() == '_telework_guide_image_'):
                qGuide2.init(panel='0-', title='telework', image=res_value, alpha_channel=0.5, )
                qGuide2.open()
                guide2_disp = True
                guide2_time = time.time()
            elif (res_name.lower() == '_telework_guide_close_'):
                qGuide2.close()
                guide2_disp = True

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

        if (guide2_disp == True):
            event, values = qGuide2.read()
            if (event in (None, '-exit-', '-cancel-')):
                qGuide2.close()
                guide2_disp = False
        if (guide2_disp == True):
            if ((time.time() - guide2_time) > 3):
                qGuide2.close()
                guide2_disp = False

        # アイドリング

        slow = False
        if  (qFunc.statusCheck(qBusy_dev_cpu) == True):
            slow = True
        if  (qFunc.statusCheck(qBusy_dev_scn) == True):
            slow = True

        if (slow == True):
            time.sleep(1.00)
        else:
            time.sleep(0.25)

    # 終了

    if (True):

        qLog.log('info', main_id, 'terminate')

        # ガイド表示（終了）

        img = qGuide.getIconImage(filename='_desktop_stop_', )
        if (img is not None):
            qGuide.init(screen=0, panel='9', title='_desktop_stop_', image=img, alpha_channel=0.5, )
            qGuide.open()
            guide_disp = True
            guide_time = time.time()

        # 外部ＰＧリセット

        qFunc.kill('ffmpeg')
        qFunc.kill('ffplay')
        qFunc.kill('ffprobe')

        # コアスレッド終了

        if (main_core is not None):
            main_core.abort()
            del main_core

        # ガイド表示終了

        qGuide.close()
        qGuide.terminate()
        guide_disp = False

        qGuide2.close()
        qGuide2.terminate()
        guide2_disp = False

        time.sleep(2.00)
        qLog.log('info', main_id, 'bye!')

        sys.exit(0)


