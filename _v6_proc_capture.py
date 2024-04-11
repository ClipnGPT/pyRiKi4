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

import numpy as np
import cv2
if (os.name == 'nt'):
    import win32gui



# インターフェース
qCtrl_control_capture    = 'temp/control_capture.txt'
qCtrl_control_self       = qCtrl_control_capture



# 共通ルーチン
import  _v6__qRiKi
qRiKi = _v6__qRiKi.qRiKi_class()
import  _v6__qFunc
qFunc = _v6__qFunc.qFunc_class()
import  _v6__qLog
qLog  = _v6__qLog.qLog_class()
import  _v6__qFFmpeg
qFFmpeg=_v6__qFFmpeg.qFFmpeg_class()

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

config_file = '_v6_proc_capture_key.json'

qRiKi_key = _v6__qRiKi_key.qRiKi_key_class()
res, dic = qRiKi_key.getCryptJson(config_file=config_file, auto_crypt=False, )
if (res == False):
    dic['_crypt_']      = 'none'
    dic['pyscript']     = 'yes'
    res = qRiKi_key.putCryptJson(config_file=config_file, put_dic=dic, )

userpass_file = '_userpass_key.json'

res, dic = qRiKi_key.getCryptJson(config_file=userpass_file, auto_crypt=True, )
if (res == False):
    dic['_crypt_']      = 'none'
    dic['username']     = ''
    dic['password']     = ''
    res = qRiKi_key.putCryptJson(config_file=userpass_file, put_dic=dic, )



# FPS計測共通クラス
class qFPS_class(object):
    def __init__(self):
        self.start     = cv2.getTickCount()
        self.count     = 0
        self.FPS       = 0
        self.lastcheck = time.time()
    def get(self):
        self.count += 1
        if (self.count >= 15) or ((time.time() - self.lastcheck) > 5):
            nowTick  = cv2.getTickCount()
            diffSec  = (nowTick - self.start) / cv2.getTickFrequency()
            self.FPS = 1 / (diffSec / self.count)
            self.start = cv2.getTickCount()
            self.count = 0
            self.lastcheck = time.time()
        return self.FPS



class proc_capture:

    def __init__(self, name='thread', id='0', runMode='debug', 
        capStretch='0', capRotate='0', capZoom='1.0', capFps='2',
        username='', password='', ):

        self.runMode    = runMode
        self.capStretch = capStretch
        self.capRotate  = capRotate
        self.capZoom    = capZoom
        self.capFps     = '5'
        if (capFps.isdigit()):
            self.capFps = str(capFps)
        self.username   = username
        self.password   = password

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

        self.winName       = None
        self.last_winName  = None
        self.last_time     = time.time()
        self.last_pathName = None

        # 変数設定
        self.blue_img = np.zeros((240,320,3), np.uint8)
        cv2.rectangle(self.blue_img,(0,0),(320,240),(255,0,0),-1)
        cv2.putText(self.blue_img, 'No Image !', (40,80), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,255))

        # 最終実行スクリプト
        self.last_script = None

        # セキュリティ情報
        userpass_file = '_userpass_key.json'
        if (self.username == ''):
            res, json_dic = qRiKi_key.getCryptJson(config_file=userpass_file, auto_crypt=True, )
            if (res == True):
                self.username = json_dic['username']
                self.password = json_dic['password']

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

        # ＦＰＳ計測
        fps_class = qFPS_class()
        fps_last  = time.time()

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

            # 連携情報
            if (inp_name.lower() == '_capstretch_'):
                self.capStretch = inp_value
                fps_last = time.time() - 60
            if (inp_name.lower() == '_caprotate_'):
                self.capRotate = inp_value
                fps_last = time.time() - 60
            if (inp_name.lower() == '_capzoom_'):
                self.capZoom = inp_value
                fps_last = time.time() - 60



            # 画像処理
            frame = None
            input_img = None
            if (cn_s.qsize() == 0):
            #if (True):

                # 画像取得
                work_path = qPath_work + 'capture_' + '{:01}'.format(self.proc_seq % 10)
                frame = qFFmpeg.capture(dev='desktop', full=False, work_path=work_path, )
                #frame = qFFmpeg.capture(dev='desktop', full=True, work_path=work_path, )

                if (frame is not None):

                    # ビジー設定 (ready)
                    if (qFunc.statusCheck(self.fileBsy) == False):
                        qFunc.statusSet(self.fileBsy, True)
                        if (str(self.id) == '0'):
                            qFunc.statusSet(qBusy_d_inp, True)

                    # 実行カウンタ
                    self.proc_last = time.time()
                    self.proc_seq += 1
                    if (self.proc_seq > 9999):
                        self.proc_seq = 1

                    # frame_img
                    frame_img = frame.copy()
                    frame_height, frame_width = frame_img.shape[:2]
                    input_img = frame.copy()
                    input_height, input_width = input_img.shape[:2]

                    # 台形補正
                    if (int(self.capStretch) != 0):
                        x = int((input_width/2) * abs(int(self.capStretch))/100)
                        if (int(self.capStretch) > 0):
                            perspective1 = np.float32([ [x, 0], [input_width-x, 0], [input_width, input_height], [0, input_height] ])
                        else:
                            perspective1 = np.float32([ [0, 0], [input_width, 0], [input_width-x, input_height], [x, input_height] ])
                        perspective2 = np.float32([ [0, 0], [input_width, 0], [input_width, input_height], [0, input_height] ])
                        transform_matrix = cv2.getPerspectiveTransform(perspective1, perspective2)
                        input_img = cv2.warpPerspective(input_img, transform_matrix, (input_width, input_height))

                    # 画像回転
                    if   (int(self.capRotate) == -180):
                        input_img = cv2.flip(input_img, 0) # 180 Rotation Y
                    elif (int(self.capRotate) == -360):
                        input_img = cv2.flip(input_img, 1) # 180 Rotation X
                    elif (abs(int(self.capRotate)) !=   0):
                        width2    = int((input_width - input_height)/2)
                        rect_img  = cv2.resize(input_img[0:input_height, width2:width2+input_height], (960,960))
                        rect_mat  = cv2.getRotationMatrix2D((480, 480), -int(self.capRotate), 1.0)
                        rect_r    = cv2.warpAffine(rect_img, rect_mat, (960, 960), flags=cv2.INTER_LINEAR)
                        input_img = cv2.resize(rect_r, (input_height, input_height))
                        input_height, input_width = input_img.shape[:2]

                    # ズーム
                    if (float(self.capZoom) != 1):
                        zm = float(self.capZoom)
                        x1 = int((input_width-(input_width/zm))/2)
                        x2 = input_width - x1
                        y1 = int((input_height-(input_height/zm))/2)
                        y2 = input_height - y1
                        zm_img = input_img[y1:y2, x1:x2]
                        input_img = zm_img.copy()
                        input_height, input_width = input_img.shape[:2]

                    # ＦＰＳ計測
                    fps = fps_class.get()
                    if ((time.time() - fps_last) > 5):
                        fps_last  = time.time()

                        # 結果出力(fps)
                        out_name  = '_fps_'
                        out_value = '{:.1f}'.format(fps)
                        cn_s.put([out_name, out_value])

                        # 結果出力(reso)
                        out_name  = '_reso_'
                        out_value = str(input_width) + 'x' + str(input_height)
                        if (float(self.capZoom) != 1):
                            out_value += ' (Zoom=' + self.capZoom + ')'
                        cn_s.put([out_name, out_value])

                    # 結果出力
                    if (cn_s.qsize() == 0):
                        out_name  = '[img]'
                        out_value = input_img.copy()
                        cn_s.put([out_name, out_value])

            # メインウィンド取得
            if (os.name == 'nt'):
                try:
                    hWnd = win32gui.GetForegroundWindow()
                    self.winName = win32gui.GetWindowText(hWnd)
                    #print(self.winName)
                except:
                    self.winName = 'none'
                    #print(self.winName)
                
                if (self.winName.find('MicrosoftTeams') >= 0):
                    self.winName = 'MicrosoftTeams'

                if (self.winName != self.last_winName):
                    if (self.last_pathName is not None):
                        #print(self.last_pathName + " " + str(int(time.time() - self.last_time)) + 's ')
                        pass

                    if (self.winName is not None):

                        # 情報表示
                        qLog.log('info', self.proc_id, self.winName)

                        # パス
                        path = qFunc.url2filepath(self.winName)
                        if (path.find('/') >= 0):
                            if (path[-1:] != '/'):
                                path += '/'
                            path_first = path[:path.find('/')+1]
                        else:
                            path_first = path
                        path2 = qPath_controls + '_desktop/' + path
                        #print(path)
                        #print(path_first)
                        #print(path2)

                        self.last_winName  = self.winName
                        self.last_time     = time.time()
                        self.last_pathName = path2

                        # 画像保管
                        if (self.runMode == 'debug'):
                            #print(path2)
                            qFunc.makeDirs(path2, remove=False, )
                            if (input_img is not None):
                                cv2.imwrite(path2 + '_image.png', input_img)

                        # python script execute
                        if True: #try:
                            filename = path2 + '_script.py'
                            username = self.username
                            password = self.password
                            #print('check ' + filename)
                            if (os.path.exists(filename)):

                                userpass_file = '_userpass_key.json'
                                if (os.path.exists(path2 + userpass_file)):
                                    res, dic = qRiKi_key.getCryptJson(config_path=path2, config_file=userpass_file, auto_crypt=True, )
                                    if (res == True):
                                        username = dic['username']
                                        password = dic['password']
                                    else:
                                        if (os.path.exists(qPath_controls + '_desktop/' + path_first + userpass_file)):
                                            res, dic = qRiKi_key.getCryptJson(config_path=qPath_controls + '_desktop/' + path_first, config_file=userpass_file, auto_crypt=True, )
                                            if (res == True):
                                                username = dic['username']
                                                password = dic['password']

                                #print('python ' + filename + ' ' + self.runMode)
                                qLog.log('info', self.proc_id, filename + ' ' + self.runMode)

                                try:
                                    if (self.last_script is not None):
                                        time.sleep(1.00)
                                        self.last_script.terminate()
                                        self.last_script = None
                                except:
                                    pass

                                self.last_script = subprocess.Popen(['python', filename, self.runMode, path2, username, password, ], )
                                #self.last_script.wait()
                                #self.last_script.terminate()
                                #self.last_script = None
                        #except Exception as e:
                        #    pass

            # アイドリング
            slow = False
            if  (qFunc.statusCheck(qBusy_dev_cpu) == True):
                slow = True
            if  (qFunc.statusCheck(qBusy_dev_scn) == True):
                slow = True
            if  (qFunc.statusCheck(qBusy_d_play   ) == True) \
            or  (qFunc.statusCheck(qBusy_d_browser) == True):
                slow = True

            if (slow == True):
                time.sleep(1.00)
            else:
                time.sleep((1/int(self.capFps))/2)

        # 終了処理
        if (True):

            # レディ解除
            qFunc.statusSet(self.fileRdy, False)

            # ビジー解除 (!ready)
            qFunc.statusSet(self.fileBsy, False)
            if (str(self.id) == '0'):
                qFunc.statusSet(qBusy_d_inp, False)

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



runMode = 'debug'
username = ''
password = ''



if __name__ == '__main__':
    main_name = 'capture'
    main_id   = '{0:10s}'.format(main_name).replace(' ', '_')

    # 共通クラス
    qRiKi.init()
    qFunc.init()

    # ログ
    nowTime  = datetime.datetime.now()
    filename = qPath_log + nowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
    qLog.init(mode='logger', filename=filename, )

    qLog.log('info', main_id, 'init')
    qLog.log('info', main_id, 'exsample.py runMode, ')

    # パラメータ

    if (True):

        if (len(sys.argv) >= 2):
            runMode  = str(sys.argv[1]).lower()
        if (len(sys.argv) >= 3):
            username = str(sys.argv[2])
        if (len(sys.argv) >= 4):
            password = str(sys.argv[3])

        qLog.log('info', main_id, 'runMode  = ' + str(runMode  ))
        if (username != ''):
            qLog.log('info', main_id, 'username = *')
        if (password != ''):
            qLog.log('info', main_id, 'password = *')

    # 初期設定

    if (True):

        txts, txt = qFunc.txtsRead(qCtrl_control_self)
        if (txts != False):
            if (txt == '_end_'):
                qFunc.remove(qCtrl_control_self)

        if (runMode == 'debug'):
            cv2.namedWindow('Display', 1)
            cv2.moveWindow( 'Display', 500, 500)

    # 起動

    if (True):

        qLog.log('info', main_id, 'start')

        main_core = proc_capture(name='capture', id='0', runMode=runMode, 
                                  capStretch='0', capRotate='0', capZoom='1.0', capFps='2',
                                  username=username, password=password, )
        main_core.begin()

        main_start = time.time()
        onece      = True

    # 待機ループ

    while (True):

        # 終了確認
        txts, txt = qFunc.txtsRead(qCtrl_control_self)
        if (txts != False):
            if (txt == '_end_'):
                break

        else:

            res_data  = main_core.get()
            res_name  = res_data[0]
            res_value = res_data[1]
            if (res_name != ''):
                if (res_name == '[window]'):
                    pass
                elif (res_name == '[img]'):
                    if (runMode == 'debug'):
                        cv2.imshow('Display', res_value.copy() )
                        pass
                else:
                    #print(res_name, res_value, )
                    pass

            # デバッグ
            if (runMode == 'debug'):
                cv2.waitKey(1)

                # テスト終了
                if  ((time.time() - main_start) > 180):
                        qFunc.txtsWrite(qCtrl_control_self ,txts=['_stop_'], encoding='utf-8', exclusive=True, mode='w', )
                        time.sleep(5.00)
                        qFunc.txtsWrite(qCtrl_control_self ,txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )

        # アイドリング
        slow = False
        if   (qFunc.statusCheck(qBusy_dev_cpu) == True):
            slow = True

        if (slow == True):
            time.sleep(1.00)
        else:
            time.sleep(0.50)

    # 終了

    if (True):

        if (runMode == 'debug'):
            cv2.destroyAllWindows()

        qLog.log('info', main_id, 'terminate')

        main_core.abort()
        del main_core

        qLog.log('info', main_id, 'bye!')

        sys.exit(0)


