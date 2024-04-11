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



# インターフェース
qCtrl_control_kernel     = 'temp/control_kernel.txt'
qCtrl_control_speech     = 'temp/control_speech.txt'
qCtrl_control_vision     = 'temp/control_vision.txt'
qCtrl_control_desktop    = 'temp/control_desktop.txt'
qCtrl_control_bgm        = 'temp/control_bgm.txt'
qCtrl_control_browser    = 'temp/control_browser.txt'
qCtrl_control_player     = 'temp/control_player.txt'
qCtrl_control_telop      = 'temp/control_telop.txt'

# 外部プログラム
qExt_pg_start            = '__ext_pg_start.bat'
qExt_pg_stop             = '__ext_pg_stop.bat'



# 共通ルーチン
import  _v6__qRiKi
qRiKi = _v6__qRiKi.qRiKi_class()
import  _v6__qFunc
qFunc = _v6__qFunc.qFunc_class()
import  _v6__qGUI
qGUI  = _v6__qGUI.qGUI_class()
import  _v6__qLog
qLog  = _v6__qLog.qLog_class()

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



class proc_controls:

    def __init__(self, name='thread', id='0', runMode='debug', 
        micDev='0', micType='bluetooth', micGuide='on', micLevel='777',  ):

        self.path      = qPath_s_ctrl

        self.runMode   = runMode
        self.micDev    = micDev
        self.micType   = micType
        self.micGuide  = micGuide
        self.micLevel  = micLevel

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

        # 変数
        self.last_text     = ''
        self.last_time     = time.time()

        # 起動条件（kernel.pyと合わせる）
        self.run_vision    = False
        self.run_desktop   = False
        self.run_bgm       = False
        self.run_browser   = False
        self.run_player    = False
        self.run_telop     = False

        if   (self.runMode == 'debug'):
            self.run_vision    = True
            self.run_desktop   = True
            self.run_bgm       = True
            self.run_browser   = True
            self.run_player    = True
            self.run_telop     = True
        elif (self.runMode == 'hud'):
            self.run_vision    = True
            self.run_desktop   = True
            self.run_bgm       = True
            self.run_browser   = True
            self.run_player    = True
        elif (self.runMode == 'live'):
            self.run_vision    = True
            self.run_desktop   = True
            self.run_bgm       = True
            self.run_browser   = True
            self.run_player    = True
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
            self.run_vision    = True
            self.run_desktop   = True
        elif (self.runMode == 'assistant'):
            self.run_vision    = True
            self.run_desktop   = True
            self.run_telop     = True
        elif (self.runMode == 'reception'):
            self.run_vision    = True
            self.run_telop     = True

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

    def abort(self, waitMax=5, ):
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

        # フォース リセット
        qFunc.statusSet(qRdy__s_force, False)
        qFunc.statusSet(qRdy__s_fproc, False)
        self.force_last = time.time()

        # 待機ループ
        self.proc_step = '5'

        while (self.proc_step == '5'):
            self.proc_beat = time.time()

            # 停止要求確認
            if (self.breakFlag.is_set()):
                self.breakFlag.clear()
                self.proc_step = '9'
                break

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

            # レディ設定
            if (qFunc.statusCheck(self.fileRdy) == False):
                qFunc.statusSet(self.fileRdy, True)

            # ステータス応答
            if (inp_name.lower() == '_status_'):
                out_name  = inp_name
                out_value = '_ready_'
                cn_s.put([out_name, out_value])

            # フォース 自動終了（有効１０秒）
            if (qFunc.statusCheck(qRdy__s_force) == True) \
            or (qFunc.statusCheck(qRdy__s_fproc) == True):
                if ((time.time() - self.force_last) > 10):
                    qFunc.statusSet(qRdy__s_force, False)
                    qFunc.statusSet(qRdy__s_fproc, False)
                    self.force_last  = time.time()

            # 処理
            path = self.path
            path_files = glob.glob(path + '*.txt')
            path_files.sort()
            if (len(path_files) > 0):

                #try:
                if (True):

                    for f in path_files:

                        # 停止要求確認
                        if (self.breakFlag.is_set()):
                            self.breakFlag.clear()
                            self.proc_step = '9'
                            break

                        proc_file = f.replace('\\', '/')

                        if (proc_file[-4:].lower() == '.txt' and proc_file[-8:].lower() != '.wrk.txt'):
                            f1 = proc_file
                            f2 = proc_file[:-4] + '.wrk.txt'
                            try:
                                os.rename(f1, f2)
                                proc_file = f2
                            except Exception as e:
                                pass

                        if (proc_file[-8:].lower() == '.wrk.txt'):
                            f1 = proc_file
                            f2 = proc_file[:-8] + proc_file[-4:]
                            try:
                                os.rename(f1, f2)
                                proc_file = f2
                            except Exception as e:
                                pass

                            # 実行カウンタ
                            self.proc_last = time.time()
                            self.proc_seq += 1
                            if (self.proc_seq > 9999):
                                self.proc_seq = 1
                            seq4 = '{:04}'.format(self.proc_seq)
                            seq2 = '{:02}'.format(self.proc_seq)

                            proc_name = proc_file.replace(path, '')
                            proc_name = proc_name[:-4]

                            work_name = self.proc_id + '.' + seq2
                            work_file = qPath_work + work_name + '.txt'
                            if (os.path.exists(work_file)):
                                os.remove(work_file)

                            if (proc_file[-9:].lower() != '_sjis.txt'):
                                proc_txts, proc_text = qFunc.txtsRead(proc_file, encoding='utf-8', exclusive=False, )
                            else:
                                proc_txts, proc_text = qFunc.txtsRead(proc_file, encoding='shift_jis', exclusive=False, )

                            if (proc_txts != False):
                                if (proc_text != '') and (proc_text != '!'):
                                    qFunc.txtsWrite(work_file, txts=[proc_text], encoding='utf-8', exclusive=False, mode='w', )

                                if (os.path.exists(work_file)):

                                    qFunc.remove(proc_file)

                                    # ログ
                                    #if (self.runMode == 'debug') or (not self.micDev.isdigit()):
                                    #    qLog.log('info', self.proc_id, '' + proc_name + ' → ' + work_name, display=self.logDisp,)

                                    # 結果出力
                                    if (cn_s.qsize() < 99):
                                        out_name  = '[txts]'
                                        out_value = proc_txts
                                        cn_s.put([out_name, out_value])

                                    # ビジー設定
                                    if (qFunc.statusCheck(self.fileBsy) == False):
                                        qFunc.statusSet(self.fileBsy, True)
                                        if (str(self.id) == '0'):
                                            qFunc.statusSet(qBusy_s_ctrl, True)

                                        if (self.micType == 'bluetooth') or (self.micGuide == 'on' or self.micGuide == 'sound'):
                                            qFunc.statusWait_false(qBusy_s_inp , 3)

                                    # フォース 覚醒
                                    qFunc.statusSet(qRdy__s_force, False)
                                    if (qRiKi.checkWakeUpWord(proc_text) == True):
                                        qFunc.statusSet(qRdy__s_force, True)
                                        qFunc.statusSet(qRdy__s_fproc, True)
                                        self.force_last  = time.time()

                                    # 処理
                                    self.proc_last = time.time()
                                    self.sub_proc(seq4, proc_file, work_file, proc_name, proc_text, cn_s, )

                                    # フォース 終了
                                    if  (qFunc.statusCheck(qRdy__s_force) == False):
                                        time.sleep(2.00)
                                        qFunc.statusSet(qRdy__s_fproc, False)

                #except Exception as e:
                #    pass



            # ビジー解除
            qFunc.statusSet(self.fileBsy, False)
            if (str(self.id) == '0'):
                qFunc.statusSet(qBusy_s_ctrl, False)

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
                    time.sleep(0.25)
                else:
                    time.sleep(0.10)

        # 終了処理
        if (True):

            # レディ解除
            qFunc.statusSet(self.fileRdy, False)

            # ビジー解除
            qFunc.statusSet(self.fileBsy, False)
            if (str(self.id) == '0'):
                qFunc.statusSet(qBusy_s_ctrl, False)

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



    def sub_proc(self, seq4, proc_file, work_file, proc_name, proc_text, cn_s, ):

        # 有効コマンド？
        if (proc_text == ''):
            return

        jp_true = qFunc.in_japanese(proc_text)
        if (proc_text == self.last_text) and ((time.time() - self.last_time) < 15):
            word_true = False
        else:
            word_true = True
            self.last_text = proc_text
            self.last_time = time.time()

        # フォース 状態
        fproc = qRiKi.checkWakeUpWord(proc_text)
        if (fproc == False):
            fproc = qFunc.statusCheck(qRdy__s_fproc)
        if (fproc == True) or (proc_text[:1] == '_'):

            qLog.log('warning', self.proc_id, 'Fource Cmd  【' + proc_text + '】', )
            fource_run = False

            # システム制御
            if   (proc_text.find('リセット') >= 0):
                qFunc.statusSet(qRdy__s_force, False)
                fource_run = True
                out_name  = 'control'
                out_value = '_reset_'
                cn_s.put([out_name, out_value])
                qFunc.txtsWrite(qCtrl_control_kernel , txts=[out_value], encoding='utf-8', exclusive=True, mode='w', )
                qFunc.txtsWrite(qCtrl_control_vision , txts=[out_value], encoding='utf-8', exclusive=True, mode='w', )
                qFunc.txtsWrite(qCtrl_control_desktop, txts=[out_value], encoding='utf-8', exclusive=True, mode='w', )

            if  ((proc_text.find('システム') >= 0) and (proc_text.find('終了') >= 0)) \
            or  (proc_text == 'バルス'):
                qFunc.statusSet(qRdy__s_force, False)
                fource_run = True
                out_name  = 'control'
                out_value = '_end_'
                cn_s.put([out_name, out_value])
                qFunc.txtsWrite(qCtrl_control_kernel , txts=[out_value], encoding='utf-8', exclusive=True, mode='w', )

            if   (proc_text.find('リブート') >= 0) \
            or   (proc_text.find('再起動') >= 0):
                qFunc.statusSet(qRdy__s_force, False)
                fource_run = True
                out_name  = 'control'
                out_value = '_reboot_'
                cn_s.put([out_name, out_value])
                qFunc.txtsWrite(qCtrl_control_kernel , txts=[out_value], encoding='utf-8', exclusive=True, mode='w', )
                self.run_bgm = False
                self.run_browser = False
                self.run_player  = False
                self.run_telop   = False

            if   (proc_text.find('操作') >= 0) \
            and ((proc_text.find('画面') >= 0) or (proc_text.find('パネル') >= 0)):
                qFunc.statusSet(qRdy__s_force, False)
                fource_run = True
                out_name  = 'control'
                out_value = '_gui_'
                cn_s.put([out_name, out_value])
                qFunc.txtsWrite(qCtrl_control_kernel , txts=[out_value], encoding='utf-8', exclusive=True, mode='w', )

            # 機能制御
            if   (proc_text.find('画面') >= 0) \
            and ((proc_text.find('開始') >= 0) or (proc_text.find('起動') >= 0)):
                qFunc.statusSet(qRdy__s_force, False)
                fource_run = True
                qFunc.txtsWrite(qCtrl_control_kernel ,txts=['_desktop_begin_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_desktop = True
                qFunc.statusWait_false(qCtrl_control_kernel, 5)
                qFunc.txtsWrite(qCtrl_control_kernel ,txts=['_vision_begin_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_vision  = True

            if   (proc_text.find('画面') >= 0) and (proc_text.find('終了') >= 0):
                qFunc.txtsWrite(qCtrl_control_kernel ,txts=['_desktop_end_'], encoding='utf-8', exclusive=True, mode='w', )
                qFunc.statusSet(qRdy__s_force, False)
                fource_run = True
                self.run_desktop = False
                qFunc.statusWait_false(qCtrl_control_kernel, 5)
                qFunc.txtsWrite(qCtrl_control_kernel ,txts=['_vision_end_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_vision  = False

            if   (proc_text.find('ビジョン') >= 0) \
            and ((proc_text.find('開始') >= 0) or (proc_text.find('起動') >= 0)):
                qFunc.statusSet(qRdy__s_force, False)
                fource_run = True
                qFunc.txtsWrite(qCtrl_control_kernel ,txts=['_vision_begin_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_vision = True

            if   (proc_text.find('ビジョン') >= 0) and (proc_text.find('終了') >= 0):
                qFunc.statusSet(qRdy__s_force, False)
                fource_run = True
                qFunc.txtsWrite(qCtrl_control_kernel ,txts=['_vision_end_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_vision = False

            if   (proc_text.find('デスクトップ') >= 0) \
            and ((proc_text.find('開始') >= 0) or (proc_text.find('起動') >= 0)):
                qFunc.statusSet(qRdy__s_force, False)
                fource_run = True
                qFunc.txtsWrite(qCtrl_control_kernel ,txts=['_desktop_begin_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_desktop = True

            if   (proc_text.find('デスクトップ') >= 0) and (proc_text.find('終了') >= 0):
                qFunc.statusSet(qRdy__s_force, False)
                fource_run = True
                qFunc.txtsWrite(qCtrl_control_kernel ,txts=['_desktop_end_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_desktop = False

            if  ((proc_text.find('ＢＧＭ') >= 0) or (proc_text.find('BGM') >= 0)) \
            and ((proc_text.find('開始') >= 0) or (proc_text.find('起動') >= 0)):
                qFunc.statusSet(qRdy__s_force, False)
                fource_run = True
                # BGM 起動
                qFunc.txtsWrite(qCtrl_control_kernel ,txts=['_bgm_begin_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_bgm = True
                # BGM 開始
                qFunc.statusWait_false(qCtrl_control_bgm, 5)
                qFunc.txtsWrite(qCtrl_control_bgm ,txts=['_start_'], encoding='utf-8', exclusive=True, mode='w', )

            if  ((proc_text.find('ＢＧＭ') >= 0) or (proc_text.find('BGM') >= 0)) \
            and  (proc_text.find('終了') >= 0):
                qFunc.statusSet(qRdy__s_force, False)
                fource_run = True
                # BGM 停止
                qFunc.statusWait_false(qCtrl_control_bgm, 5)
                qFunc.txtsWrite(qCtrl_control_bgm ,txts=['_stop_'], encoding='utf-8', exclusive=True, mode='w', )
                # BGM 終了
                qFunc.statusWait_false(qCtrl_control_bgm, 5)
                qFunc.txtsWrite(qCtrl_control_kernel ,txts=['_bgm_end_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_bgm = False

            if  ((proc_text.find('ＢＧＭ') >= 0) or (proc_text.find('BGM') >= 0)) \
            and ((proc_text.find('停止') >= 0) or (proc_text.find('ストップ') >= 0)):
                qFunc.statusSet(qRdy__s_force, False)
                fource_run = True
                # BGM 停止
                qFunc.statusWait_false(qCtrl_control_bgm, 5)
                qFunc.txtsWrite(qCtrl_control_bgm ,txts=['_stop_'], encoding='utf-8', exclusive=True, mode='w', )

            if   (proc_text.find('動画') >= 0) \
            and ((proc_text.find('開始') >= 0) or (proc_text.find('起動') >= 0)):
                qFunc.statusSet(qRdy__s_force, False)
                fource_run = True
                # 動画 起動
                qFunc.txtsWrite(qCtrl_control_kernel ,txts=['_player_begin_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_player = True
                # 動画 メニュー
                #qFunc.statusWait_false(qCtrl_control_player, 5)
                #qFunc.txtsWrite(qCtrl_control_player ,txts=['_stop_'], encoding='utf-8', exclusive=True, mode='w', )
                qFunc.statusWait_false(qCtrl_control_player, 5)
                qFunc.txtsWrite(qCtrl_control_player ,txts=['動画メニュー'], encoding='utf-8', exclusive=True, mode='w', )

            if   (proc_text.find('動画') >= 0) and (proc_text.find('終了') >= 0):
                qFunc.statusSet(qRdy__s_force, False)
                fource_run = True
                # 動画 停止
                qFunc.statusWait_false(qCtrl_control_player, 5)
                qFunc.txtsWrite(qCtrl_control_player ,txts=['_stop_'], encoding='utf-8', exclusive=True, mode='w', )
                # 動画 終了
                qFunc.statusWait_false(qCtrl_control_player, 5)
                qFunc.txtsWrite(qCtrl_control_kernel ,txts=['_player_end_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_player = False

            if   (proc_text.find('動画') >= 0) \
            and ((proc_text.find('停止') >= 0) or (proc_text.find('ストップ') >= 0)):
                qFunc.statusSet(qRdy__s_force, False)
                fource_run = True
                # 動画 停止
                qFunc.statusWait_false(qCtrl_control_player, 5)
                qFunc.txtsWrite(qCtrl_control_player ,txts=['_stop_'], encoding='utf-8', exclusive=True, mode='w', )

            if  ((proc_text.find('ブラウザ') >= 0) or (proc_text.find('ウェブ') >= 0)) \
            and ((proc_text.find('開始') >= 0) or (proc_text.find('起動') >= 0)):
                qFunc.statusSet(qRdy__s_force, False)
                fource_run = True
                # ブラウザ 起動
                qFunc.txtsWrite(qCtrl_control_kernel ,txts=['_browser_begin_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_browser = True
                # ブラウザ 開く
                qFunc.statusWait_false(qCtrl_control_browser, 5)
                qFunc.txtsWrite(qCtrl_control_browser ,txts=['_start_'], encoding='utf-8', exclusive=True, mode='w', )

            if  ((proc_text.find('ブラウザ') >= 0) or (proc_text.find('ウェブ') >= 0)) \
            and  (proc_text.find('終了') >= 0):
                qFunc.statusSet(qRdy__s_force, False)
                fource_run = True
                # ブラウザ 閉じる
                qFunc.statusWait_false(qCtrl_control_browser, 5)
                qFunc.txtsWrite(qCtrl_control_browser ,txts=['_stop_'], encoding='utf-8', exclusive=True, mode='w', )
                # ブラウザ 終了
                qFunc.statusWait_false(qCtrl_control_browser, 5)
                qFunc.txtsWrite(qCtrl_control_kernel ,txts=['_browser_end_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_browser = False

            if  ((proc_text.find('ブラウザ') >= 0) or (proc_text.find('ウェブ') >= 0)) \
            and ((proc_text.find('停止') >= 0) or (proc_text.find('ストップ') >= 0)):
                qFunc.statusSet(qRdy__s_force, False)
                fource_run = True
                # ブラウザ 閉じる
                qFunc.statusWait_false(qCtrl_control_browser, 5)
                qFunc.txtsWrite(qCtrl_control_browser ,txts=['_stop_'], encoding='utf-8', exclusive=True, mode='w', )

            if   (proc_text.find('テロップ') >= 0) \
            and ((proc_text.find('開始') >= 0) or (proc_text.find('起動') >= 0)):
                qFunc.statusSet(qRdy__s_force, False)
                fource_run = True
                # テロップ 起動
                qFunc.txtsWrite(qCtrl_control_kernel ,txts=['_telop_begin_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_telop = True

            if   (proc_text.find('テロップ') >= 0) and (proc_text.find('終了') >= 0):
                qFunc.statusSet(qRdy__s_force, False)
                fource_run = True
                # テロップ 終了
                qFunc.statusWait_false(qCtrl_control_telop, 5)
                qFunc.txtsWrite(qCtrl_control_kernel ,txts=['_telop_end_'], encoding='utf-8', exclusive=True, mode='w', )
                self.run_telop = False

            # 外部プログラム開始 qExt_pg_start
            if  ((proc_text.find('プログラム') >= 0) \
            and  ((proc_text.find('開始') >= 0) or (proc_text.find('起動') >= 0))):
                qFunc.statusSet(qRdy__s_force, False)
                fource_run = True
                if (os.name == 'nt'):
                    if (os.path.exists(qExt_pg_start)):
                        ext_program = subprocess.Popen([qExt_pg_start, proc_text, ], )
                                      #shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

            # 外部プログラム終了 qExt_pg_stop
            if   (proc_text.find('プログラム') >= 0) and (proc_text.find('終了') >= 0):
                qFunc.statusSet(qRdy__s_force, False)
                fource_run = True
                if (os.name == 'nt'):
                    if (os.path.exists(qExt_pg_stop)):
                        ext_program = subprocess.Popen([qExt_pg_stop, proc_text, ], )
                                      #shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

            # ガイド表示
            if (fource_run == True):
                cn_s.put(['_guide_', proc_text])
                self.last_text = proc_text
                self.last_time = time.time()
                return

        # 動画向け特別コマンド
        if (self.run_player == True) \
        and  (proc_text.find('動画') >=0) and (proc_text.find('メニュー') >=0):
            qFunc.statusSet(qRdy__s_force, False)
            # 動画 メニュー
            qFunc.statusWait_false(qCtrl_control_player, 5)
            qFunc.txtsWrite(qCtrl_control_player ,txts=['_stop_'], encoding='utf-8', exclusive=True, mode='w', )
            qFunc.statusWait_false(qCtrl_control_player, 5)
            qFunc.txtsWrite(qCtrl_control_player ,txts=['動画メニュー'], encoding='utf-8', exclusive=True, mode='w', )
            
            cn_s.put(['_guide_', proc_text])
            self.last_text = proc_text
            self.last_time = time.time()
            return

        if (self.run_player == True) \
        and  (word_true == True) \
        and  (proc_text.lower() >= '01') and (proc_text.lower() <= '09'):
            qFunc.statusSet(qRdy__s_force, False)
            # 動画 番号で開く
            qFunc.statusWait_false(qCtrl_control_player, 5)
            qFunc.txtsWrite(qCtrl_control_player ,txts=['_stop_'], encoding='utf-8', exclusive=True, mode='w', )
            qFunc.statusWait_false(qCtrl_control_player, 5)
            qFunc.txtsWrite(qCtrl_control_player ,txts=[proc_text.lower()], encoding='utf-8', exclusive=True, mode='w', )

            cn_s.put(['_guide_', proc_text])
            self.last_text = proc_text
            self.last_time = time.time()
            return

        # インターフェース
        #if (self.run_vision    == True):
        #    qFunc.txtsWrite(qCtrl_control_vision   ,txts=[proc_text], encoding='utf-8', exclusive=True, mode='w', )
        #if (self.run_desktop   == True):
        #    qFunc.txtsWrite(qCtrl_control_desktop  ,txts=[proc_text], encoding='utf-8', exclusive=True, mode='w', )
        if (self.run_bgm       == True):
            qFunc.txtsWrite(qCtrl_control_bgm      ,txts=[proc_text], encoding='utf-8', exclusive=True, mode='w', )
        if (self.run_browser   == True):
            qFunc.txtsWrite(qCtrl_control_browser  ,txts=[proc_text], encoding='utf-8', exclusive=True, mode='w', )
        #if (self.run_player    == True):
        #    qFunc.txtsWrite(qCtrl_control_player   ,txts=[proc_text], encoding='utf-8', exclusive=True, mode='w', )
        #if (self.run_telop     == True):
        #    qFunc.txtsWrite(qCtrl_control_telop    ,txts=[proc_text], encoding='utf-8', exclusive=True, mode='w', )

        # 動画　特別コマンド
        if  (self.run_player == True) \
        and (proc_text.find('動画') >=0) and (proc_text.find('メニュー') >=0):
            # 動画 メニュー
            qFunc.statusWait_false(qCtrl_control_player, 5)
            qFunc.txtsWrite(qCtrl_control_player ,txts=['_stop_'], encoding='utf-8', exclusive=True, mode='w', )
            qFunc.statusWait_false(qCtrl_control_player, 5)
            qFunc.txtsWrite(qCtrl_control_player ,txts=['動画メニュー'], encoding='utf-8', exclusive=True, mode='w', )
            
            cn_s.put(['_guide_', proc_text])
            self.last_text = proc_text
            self.last_time = time.time()
            return

        # 動画　特別コマンド
        if  (self.run_player == True) \
        and (word_true == True) \
        and (proc_text.lower() >= '01') and (proc_text.lower() <= '09'):
            # 動画 番号で開く
            qFunc.statusWait_false(qCtrl_control_player, 5)
            qFunc.txtsWrite(qCtrl_control_player ,txts=['_stop_'], encoding='utf-8', exclusive=True, mode='w', )
            qFunc.statusWait_false(qCtrl_control_player, 5)
            qFunc.txtsWrite(qCtrl_control_player ,txts=[proc_text.lower()], encoding='utf-8', exclusive=True, mode='w', )

            cn_s.put(['_guide_', proc_text])
            self.last_text = proc_text
            self.last_time = time.time()
            return

        # 画面操作
        if (proc_text.find('メイン') >= 0) and (proc_text.find('スクリーン') >= 0):
            qGUI.keyDown('ctrlleft')
            qGUI.keyDown('winleft')
            qGUI.press('left')
            qGUI.press('left')
            qGUI.press('left')
            qGUI.press('left')
            qGUI.press('left')
            qGUI.keyUp('winleft')
            qGUI.keyUp('ctrlleft')

        if (proc_text.find('サブ') >= 0) and (proc_text.find('スクリーン') >= 0):
            qGUI.keyDown('ctrlleft')
            qGUI.keyDown('winleft')
            qGUI.press('right')
            qGUI.keyUp('winleft')
            qGUI.keyUp('ctrlleft')

        if (proc_text.find('スクリーン') >= 0) and (proc_text.find('キーボード') >= 0):
            qGUI.keyDown('ctrlleft')
            qGUI.keyDown('winleft')
            qGUI.press('o')
            qGUI.keyUp('winleft')
            qGUI.keyUp('ctrlleft')

        # キーボード操作
        if (proc_text[-3:] == 'を入力'):
            qGUI.sendKey(proc_text[:-3],cr=True, lf=False)
        elif (proc_text[-2:] == '入力'):
            qGUI.sendKey(proc_text[:-2],cr=True, lf=False)

        if (proc_text == '改行') or (proc_text.lower() == 'enter'):
            qGUI.press('enter')

        if (proc_text.lower() == 'f1') or (proc_text.lower() == 'f 1'):
            qGUI.press('f1')
        if (proc_text.lower() == 'f2') or (proc_text.lower() == 'f 2'):
            qGUI.press('f2')
        if (proc_text.lower() == 'f3') or (proc_text.lower() == 'f 3'):
            qGUI.press('f3')
        if (proc_text.lower() == 'f4') or (proc_text.lower() == 'f 4'):
            qGUI.press('f4')
        if (proc_text.lower() == 'f5') or (proc_text.lower() == 'f 5'):
            qGUI.press('f5')
        if (proc_text.lower() == 'f6') or (proc_text.lower() == 'f 6'):
            qGUI.press('f6')
        if (proc_text.lower() == 'f7') or (proc_text.lower() == 'f 7'):
            qGUI.press('f7')
        if (proc_text.lower() == 'f8') or (proc_text.lower() == 'f 8'):
            qGUI.press('f8')
        if (proc_text.lower() == 'f9') or (proc_text.lower() == 'f 9'):
            qGUI.press('f9')
        if (proc_text.lower() == 'f10') or (proc_text.lower() == 'f 10'):
            qGUI.press('f10')
        if (proc_text.lower() == 'f11') or (proc_text.lower() == 'f 11'):
            qGUI.press('f11')
        if (proc_text.lower() == 'f12') or (proc_text.lower() == 'f 12'):
            qGUI.press('f12')

        if (proc_text == 'ポーズ') \
        or (proc_text == '閉じる'):
            qGUI.press('pause')
        if (proc_text[-3:] == 'を検索'):
            qGUI.sendKey(proc_text[:-3],cr=False, lf=False)
            qGUI.press('f9')

        self.last_text = proc_text
        self.last_time = time.time()



if __name__ == '__main__':

    # 共通クラス
    qRiKi.init()
    qFunc.init()

    # ログ
    nowTime  = datetime.datetime.now()
    filename = qPath_log + nowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
    qLog.init(mode='logger', filename=filename, )

    # 設定
    controls_thread = proc_controls('controls', '0', )
    controls_thread.begin()



    # ループ
    chktime = time.time()
    while ((time.time() - chktime) < 15):

        res_data  = controls_thread.get()
        res_name  = res_data[0]
        res_value = res_data[1]
        if (res_name != ''):
            print(res_name, res_value, )

        if (controls_thread.proc_s.qsize() == 0):
            controls_thread.put(['_status_', ''])

        time.sleep(0.05)



    time.sleep(1.00)
    controls_thread.abort()
    del controls_thread


