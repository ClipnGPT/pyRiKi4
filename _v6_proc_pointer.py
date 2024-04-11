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

import random



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



import _v6__qRiKi_key

config_file = '_v6_proc_pointer_key.json'

qRiKi_key = _v6__qRiKi_key.qRiKi_key_class()
res, dic = qRiKi_key.getCryptJson(config_file=config_file, auto_crypt=False, )
if (res == False):
    dic['_crypt_']      = 'none'
    dic['mouseEnable']  = 'yes'
    dic['mousePointer'] = 'yes'
    dic['changeScreen'] = 'no'
    dic['beatSec']      = 10
    dic['waitSec']      = 60
    dic['dayStart']     = '06:55:00'
    dic['dayEnd']       = '16:05:00'
    dic['lunchStart']   = '12:05:00'
    dic['lunchEnd']     = '12:55:00'
    res = qRiKi_key.putCryptJson(config_file=config_file, put_dic=dic, )



class proc_pointer:

    def __init__(self, name='thread', id='0', runMode='debug', ):

        self.path      = qPath_d_ctrl

        self.runMode   = runMode

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
        self.lastSign  = '00:00'

        json_file = '_v6_proc_pointer_key.json'
        self.mouseEnable  = 'yes'
        self.mousePointer = 'yes'
        self.changeScreen = 'no'
        self.beatSec      = 10
        self.waitSec      = 60
        self.dayStart     = '06:55:00'
        self.dayEnd       = '16:05:00'
        self.lunchStart   = '12:05:00'
        self.lunchEnd     = '12:55:00'
        res, json_dic = qRiKi_key.getCryptJson(config_file=json_file, auto_crypt=False, )
        if (res == True):
            self.mouseEnable  = dic['mouseEnable']
            self.mousePointer = dic['mousePointer']
            self.screenChange = dic['changeScreen']
            self.beatSec      = dic['beatSec']
            self.waitSec      = dic['waitSec']
            self.dayStart     = dic['dayStart']
            self.dayEnd       = dic['dayEnd']
            self.lunchStart   = dic['lunchStart']
            self.lunchEnd     = dic['lunchEnd']
        qLog.log('info', self.proc_id, 'mouseEnable  = ' + str(self.mouseEnable ), display=self.logDisp, )
        qLog.log('info', self.proc_id, 'mousePointer = ' + str(self.mousePointer), display=self.logDisp, )
        qLog.log('info', self.proc_id, 'changeScreen = ' + str(self.changeScreen), display=self.logDisp, )
        qLog.log('info', self.proc_id, 'beatSec      = ' + str(self.beatSec     ), display=self.logDisp, )
        qLog.log('info', self.proc_id, 'waitSec      = ' + str(self.waitSec     ), display=self.logDisp, )
        qLog.log('info', self.proc_id, 'dayStart     = ' + str(self.dayStart    ), display=self.logDisp, )
        qLog.log('info', self.proc_id, 'dayEnd       = ' + str(self.dayEnd      ), display=self.logDisp, )
        qLog.log('info', self.proc_id, 'lunchStart   = ' + str(self.lunchStart  ), display=self.logDisp, )
        qLog.log('info', self.proc_id, 'lunchEnd     = ' + str(self.lunchEnd    ), display=self.logDisp, )

        try:
            (w, h) = qGUI.size()
        except Exception as e:
            w = 640
            h = 480
        self.sc_width  = w
        self.sc_height = h
        qLog.log('info', self.proc_id, 'Screen = (' + str(self.sc_width) + ', ' + str(self.sc_height) + ')', display=self.logDisp, )

        if (self.changeScreen.lower()  == 'yes'):
            qLog.log('info', self.proc_id, 'Change Sub Screen ...', display=self.logDisp, )
            try:
                qGUI.keyDown('ctrlleft')
                qGUI.keyDown('winleft')
                qGUI.press('right')
                qGUI.keyUp('winleft')
                qGUI.keyUp('ctrlleft')
            except Exception as e:
                pass

        self.last_x = self.sc_width / 2
        self.last_y = self.sc_height / 2
        self.last_t = time.time()
        self.moveTo(self.last_x, self.last_y)

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

            # ビジー設定
            #if (qFunc.statusCheck(self.fileBsy) == False):
            #    qFunc.statusSet(self.fileBsy, True)

            if int(time.time() - self.proc_last) >= self.beatSec:

                # 実行カウンタ
                self.proc_last = time.time()
                self.proc_seq += 1
                if (self.proc_seq > 9999):
                    self.proc_seq = 1
                seq4 = '{:04}'.format(self.proc_seq)
                seq2 = '{:02}'.format(self.proc_seq)

                # 処理                
                self.sub_proc(seq4, )

            # ビジー解除
            #qFunc.statusSet(self.fileBsy, False)

            # アイドリング
            slow = False
            if  (qFunc.statusCheck(qBusy_dev_cpu) == True):
                slow = True
            if  (qFunc.statusCheck(qBusy_dev_scn) == True):
                slow = True

            if (slow == True):
                time.sleep(1.00)
            else:
                if (cn_r.qsize() == 0):
                    time.sleep(0.25)
                else:
                    time.sleep(0.50)

        # 終了処理
        if (True):

            # レディ解除
            qFunc.statusSet(self.fileRdy, False)

            # ビジー解除
            qFunc.statusSet(self.fileBsy, False)

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



    def sub_proc(self, seq4, ):
        #print(seq4)
        self.check()

    def moveTo(self, x, y):
        if (self.mouseEnable.lower() == 'yes'):
            try:
                qGUI.moveTo(int(x), int(y))
            except Exception as e:
                pass
        if (self.mousePointer.lower() == 'yes'):
            try:
                qGUI.press("ctrl")
            except Exception as e:
                pass
        try:
            (x, y) = qGUI.position()
            self.last_x = x
            self.last_y = y
            qLog.log('info', self.proc_id, 'Position = (' + str(self.last_x) + ', ' + str(self.last_y) + ')', display=self.logDisp, )
        except Exception as e:
            pass

    def check(self, ):
        nowTime = datetime.datetime.now()
        nowHHMMSS = nowTime.strftime('%H:%M:%S')
        nowHHMM   = nowTime.strftime('%H:%M')
        nowYOUBI  = nowTime.strftime('%a')
        if (nowHHMMSS < self.dayStart) \
        or (nowHHMMSS > self.dayEnd):
            # ビジー解除
            if (qFunc.statusCheck(self.fileBsy) == True):
                qFunc.statusSet(self.fileBsy, False)
                qLog.log('info', self.proc_id, 'mouse pointer stop (day time)', display=self.logDisp, )
            return
        if  (nowHHMMSS > self.lunchStart) \
        and (nowHHMMSS < self.lunchEnd):
            # ビジー解除
            if (qFunc.statusCheck(self.fileBsy) == True):
                qFunc.statusSet(self.fileBsy, False)
                qLog.log('info', self.proc_id, 'mouse pointer stop (lunch time)', display=self.logDisp, )
            return
        if  (nowYOUBI == 'Sat') \
        or  (nowYOUBI == 'Sun') \
        or  (nowYOUBI == '土') \
        or  (nowYOUBI == '日'):
            # ビジー解除
            if (qFunc.statusCheck(self.fileBsy) == True):
                qFunc.statusSet(self.fileBsy, False)
                qLog.log('info', self.proc_id, 'mouse pointer stop (YOUBI=' & nowYOUBI & ')', display=self.logDisp, )
            return

        (x, y) = qGUI.position()
        if (x != self.last_x) or (y != self.last_y):
            # ビジー解除
            if (qFunc.statusCheck(self.fileBsy) == True):
                qFunc.statusSet(self.fileBsy, False)
                qLog.log('info', self.proc_id, 'mouse pointer stop', display=self.logDisp, )

            self.last_x = x
            self.last_y = y
            self.last_t = time.time()

        if ((time.time() - self.last_t) > self.waitSec):

            # ビジー設定
            if (qFunc.statusCheck(self.fileBsy) == False):
                qFunc.statusSet(self.fileBsy, True)
                qLog.log('info', self.proc_id, 'mouse pointer start', display=self.logDisp, )

            # マウス移動
            x += int(random.random() * 10) - 5
            if (x < 100):
                x = 100
            if (x > (self.sc_width-100)):
                x = (self.sc_width-100)
            y += int(random.random() * 10) - 5
            if (y < 100):
                y = 100
            if (y > (self.sc_height-100)):
                y = (self.sc_height-100)

            self.moveTo(x, y)



if __name__ == '__main__':

    # 共通クラス
    qRiKi.init()
    qFunc.init()

    # ログ
    nowTime  = datetime.datetime.now()
    filename = qPath_log + nowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
    qLog.init(mode='logger', filename=filename, )

    # 設定
    pointer_thread = proc_pointer('pointer', '0', )
    pointer_thread.begin()



    # ループ（スクリプト実行）
    if (qRUNATTR == 'python'):
        chktime = time.time()
        while ((time.time() - chktime) < 120):

            res_data  = pointer_thread.get()
            res_name  = res_data[0]
            res_value = res_data[1]
            if (res_name != ''):
                print(res_name, res_value, )

            if (pointer_thread.proc_s.qsize() == 0):
                pointer_thread.put(['_status_', ''])

            time.sleep(1.00)



    # 無限ループ（ｅｘｅ実行）
    if (qRUNATTR != 'python'):

        while True:
            res_data  = pointer_thread.get()
            res_name  = res_data[0]
            res_value = res_data[1]
            if (res_name != ''):
                print(res_name, res_value, )

            time.sleep(1.00)



    time.sleep(1.00)
    pointer_thread.abort()
    del pointer_thread



