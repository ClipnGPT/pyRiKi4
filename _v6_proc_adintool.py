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
qCtrl_control_speech     = 'temp/control_speech.txt'



# 共通ルーチン
import  _v6__qRiKi
qRiKi = _v6__qRiKi.qRiKi_class()
import  _v6__qFunc
qFunc = _v6__qFunc.qFunc_class()
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



class proc_adintool:

    def __init__(self, name='thread', id='0', runMode='debug', 
        micDev='0', micType='bluetooth', micGuide='sound', micLevel='777', ):

        self.path      = qPath_s_inp

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

        adin_rewind   = '555'
        adin_headmg   = '333'
        adin_tailmg   = '444'
        vadLevel      = '1'
        if (self.micLevel == '1'):
            vadLevel  = '3'

        adintool_exe = None
        adintool_gui = None

        # ガイド音
        if (self.micGuide != 'off'):
            qFunc.guideSound('_up')

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
                out_value = '!ready'
                if (adintool_exe is not None):
                    files = glob.glob(self.path + '*')
                    if (len(files) == 0):
                        out_value = '_ready_'
                    else:
                        out_value = '_busy_'

                cn_s.put([out_name, out_value])



            # 処理

            # on ?
            sw = 'off'
            if  (qFunc.statusCheck(qBusy_dev_mic) == False):
                if (self.micDev.isdigit()):
                    if (self.micType == 'usb'):
                            sw = 'on'
                    else:
                        if  (qFunc.statusWait_false(qBusy_s_ctrl,  1) == False) \
                        and (qFunc.statusWait_false(qBusy_s_wav,   1) == False) \
                        and (qFunc.statusWait_false(qBusy_s_STT,   1) == False) \
                        and (qFunc.statusWait_false(qBusy_s_TTS,   1) == False) \
                        and (qFunc.statusWait_false(qBusy_s_TRA,   1) == False) \
                        and (qFunc.statusWait_false(qBusy_s_play,  1) == False) \
                        and (qFunc.statusWait_false(qBusy_s_chat,  1) == False):
                            sw = 'on'

            # off -> on
            if (sw == 'on'):
                if (adintool_exe is None):

                    # 実行カウンタ
                    self.proc_last = time.time()
                    self.proc_seq += 1
                    if (self.proc_seq > 9999):
                        self.proc_seq = 1

                    # ビジー設定 (ready)
                    if (qFunc.statusCheck(self.fileBsy) == False):
                        qFunc.statusSet(self.fileBsy, True)
                    if (str(self.id) == '0'):
                        qFunc.statusSet(qBusy_s_inp, True)

                    # ガイド音
                    if (self.micGuide == 'on' or self.micGuide == 'sound') \
                    or (qFunc.statusCheck(qRdy__s_force)  == True) \
                    or (qFunc.statusCheck(qBusy_v_recept) == True):
                        qFunc.guideSound('_ready')

                    if (True):
                        nowTime = datetime.datetime.now()
                        filename = self.path + nowTime.strftime('%Y%m%d.%H%M%S') +'.adintool'
                        adintool_exe = subprocess.Popen(['adintool', '-in', 'mic', \
                                        '-rewind', adin_rewind, '-headmargin', adin_headmg, '-tailmargin', adin_tailmg, \
                                        '-fvad', vadLevel, '-lv', self.micLevel, \
                                        '-out', 'file', '-filename', filename, '-startid', '5001', ] , \
                                        shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

                if (adintool_gui is None) and (os.name == 'nt'):
                    if (self.micGuide == 'on') or (self.micGuide == 'display') \
                    or (qFunc.statusCheck(qRdy__s_force)  == True) \
                    or (qFunc.statusCheck(qBusy_v_recept) == True):
                        adintool_gui = subprocess.Popen(['adintool-gui', '-in', 'mic', \
                                        '-rewind', adin_rewind, '-headmargin', adin_headmg, '-tailmargin', adin_tailmg, \
                                        '-lv', self.micLevel,] , \
                                        shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

            # フォース 終了
            if (adintool_gui is not None):
                if (self.micGuide != 'on') and (self.micGuide != 'display') \
                and (qFunc.statusCheck(qRdy__s_force)  != True) \
                and (qFunc.statusCheck(qBusy_v_recept) != True):
                    adintool_gui.terminate()
                    adintool_gui = None

            # off, accept ?
            sw = 'on'
            if (qFunc.statusCheck(qBusy_dev_mic) == True):
                    sw = 'off'
            if (self.micType == 'bluetooth'):
                if  (qFunc.statusCheck(qBusy_s_play) == True):
                    sw = 'off'
            if (adintool_exe is not None):
                files = glob.glob(self.path + '*')
                if (len(files) > 0):
                    chktime = time.time()
                    while (len(files) > 0) and ((time.time() - chktime) < 2):
                        time.sleep(0.20)
                        files = glob.glob(self.path + '*')
                    if (len(files) == 0):
                        sw = 'accept'

            # on -> off, accept
            if (sw == 'off') or (sw == 'accept'):

                # adintool 終了
                if (adintool_gui is not None):
                    adintool_gui.terminate()
                    adintool_gui = None

                if (self.micType == 'bluetooth'):

                    # adintool 終了
                    if (adintool_exe is not None):
                        adintool_exe.terminate()
                        adintool_exe = None

                    # ビジー解除 (!ready)
                    qFunc.statusSet(self.fileBsy, False)
                    if (str(self.id) == '0'):
                        qFunc.statusSet(qBusy_s_inp, False)

                # ガイド音
                time.sleep(0.50)
                if (sw == 'accept'):
                    if (self.micGuide == 'on') or (self.micGuide == 'sound') \
                    or (qFunc.statusCheck(qRdy__s_force)  == True) \
                    or (qFunc.statusCheck(qBusy_v_recept) == True):
                        qFunc.guideSound('_accept')

                # フォース 終了
                if (qFunc.statusCheck(qRdy__s_force) == True):
                    qFunc.statusSet(qRdy__s_force, False)

                time.sleep(0.50)



            # アイドリング
            slow = False
            if  (qFunc.statusCheck(qBusy_dev_cpu) == True):
                slow = True
            if  (qFunc.statusCheck(qBusy_dev_mic) == True):
                slow = True

            if (slow == True):
                time.sleep(0.50)
            else:
                if (cn_r.qsize() == 0):
                    time.sleep(0.25)
                else:
                    time.sleep(0.05)

        # 終了処理
        if (True):

            # レディ解除
            qFunc.statusSet(self.fileRdy, False)

            # adintool 終了
            if (adintool_gui is not None):
                adintool_gui.terminate()
                adintool_gui = None

            if (adintool_exe is not None):
                adintool_exe.terminate()
                adintool_exe = None

            # ビジー解除 (!ready)
            qFunc.statusSet(self.fileBsy, False)
            if (str(self.id) == '0'):
                qFunc.statusSet(qBusy_s_inp, False)

            # ガイド音
            if (self.micGuide != 'off'):
                qFunc.guideSound('_down')

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



if __name__ == '__main__':

    # 共通クラス
    qRiKi.init()
    qFunc.init()

    # ログ
    nowTime  = datetime.datetime.now()
    filename = qPath_log + nowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
    qLog.init(mode='logger', filename=filename, )

    # 初期設定
    qFunc.remove(qCtrl_control_speech)
    qRiKi.statusReset_speech(False)

    qFunc.kill('adintool')
    qFunc.kill('adintool-gui')

    # パラメータ
    runMode = 'debug'
    if (len(sys.argv) >= 2):
        runMode  = str(sys.argv[1]).lower()

    # 開始
    adintool_thread = proc_adintool('adintool', '0', runMode, )
    adintool_thread.begin()



    # テスト実行
    if (len(sys.argv) < 2):

        chktime = time.time()
        while ((time.time() - chktime) < 15):

            res_data  = adintool_thread.get()
            res_name  = res_data[0]
            res_value = res_data[1]
            if (res_name != ''):
                print(res_name, res_value, )

            if (adintool_thread.proc_s.qsize() == 0):
                adintool_thread.put(['_status_', ''])

            time.sleep(0.05)



    # 単体実行
    if (len(sys.argv) >= 2):

        # 待機ループ
        while (True):

            # 終了確認
            control = ''
            txts, txt = qFunc.txtsRead(qCtrl_control_speech)
            if (txts != False):
                qLog.log('info', str(txt))
                if (txt == '_end_'):
                    break
                else:
                    qFunc.remove(qCtrl_control_speech)
                    control = txt

            # メッセージ
            res_data  = adintool_thread.get()
            res_name  = res_data[0]
            res_value = res_data[1]
            #if (res_name != ''):
            #    print(res_name, res_value, )

            time.sleep(0.50)



    # 終了
    adintool_thread.abort()
    del adintool_thread

    qFunc.kill('adintool')
    qFunc.kill('adintool-gui')


