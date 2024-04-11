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



class proc_camera:

    def __init__(self, name='thread', id='0', runMode='debug', 
                    camDev='0', camMode='harf', camStretch='0', camRotate='0', camZoom='1.0', camFps='5', ):
        self.runMode    = runMode
        self.camDev     = camDev
        self.camDev_self= qFunc.chkSelfDev(camDev)
        self.camMode    = camMode
        self.camStretch = camStretch
        self.camRotate  = camRotate
        self.camZoom    = camZoom
        self.camSquare  = '0.05' #面積1/20以上
        self.camFps     = '5'
        if (camFps.isdigit()):
            self.camFps = str(camFps)

        self.camWidth   = 0
        self.camHeight  = 0
        if (camMode != 'default') and (camMode != 'auto'):
            camWidth, camHeight = qGUI.getResolution(camMode)
            self.camWidth   = camWidth
            self.camHeight  = camHeight

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

        # 変数設定
        self.riki_img = cv2.imread(qPath_icons + 'RiKi_base.png')
        self.blue_img = np.zeros((240,320,3), np.uint8)
        cv2.rectangle(self.blue_img,(0,0),(320,240),(255,0,0),-1)
        cv2.putText(self.blue_img, 'No Image ! (cam)', (40,80), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,255))

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

        # デバイス設定
        capture = None
        if (not self.camDev.isdigit()):
            try:
                capture = cv2.VideoCapture(self.camDev)
            except Exception as e:
                capture = None

        # 受付監視機能（差分検出）
        bgsegm_model = None
        if (self.runMode == 'reception'):
            bgsegm_model = cv2.bgsegm.createBackgroundSubtractorMOG()

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

            # デバイス設定
            if (self.camDev.isdigit()):
                if (capture is None):
                    if ((qFunc.statusCheck(qBusy_dev_cam) == False) \
                    or  (qFunc.statusCheck(qRdy__v_sendkey) == True)):

                        dev = self.camDev
                        #if (qFunc.statusCheck(qRdy__v_mirror) == True):
                        #    dev = '0'
                        #    if (qHOSTNAME == 'kondou-s10'):
                        #        dev = '1'

                        try:
                            if (os.name != 'nt'):
                                capture = cv2.VideoCapture(int(dev))
                            else:
                                capture = cv2.VideoCapture(int(dev), cv2.CAP_DSHOW)
                        except Exception as e:
                            capture = None

                        if (capture is not None):
                            try:
                                try:
                                    capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('H', '2', '6', '4'))
                                except Exception as e:
                                    pass
                                if (int(self.camWidth ) != 0):
                                    capture.set(cv2.CAP_PROP_FRAME_WIDTH,  int(self.camWidth ))
                                if (int(self.camHeight) != 0):
                                    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, int(self.camHeight))
                                if (int(self.camFps) != 0):
                                    capture.set(cv2.CAP_PROP_FPS,          int(self.camFps   ))
                            except Exception as e:
                                pass

                            # ビジー設定 (ready)
                            if (qFunc.statusCheck(self.fileBsy) == False):
                                qFunc.statusSet(self.fileBsy, True)
                                if (str(self.id) == '0'):
                                    qFunc.statusSet(qBusy_v_inp, True)

                if  (capture is not None):
                    if ((qFunc.statusCheck(qBusy_dev_cam) == True) \
                    and (qFunc.statusCheck(qRdy__v_sendkey) == False)):
                        try:
                            capture.release()
                        except Exception as e:
                            pass
                        capture = None

                        # ビジー解除 (!ready)
                        qFunc.statusSet(self.fileBsy, False)
                        if (str(self.id) == '0'):
                            qFunc.statusSet(qBusy_v_inp, False)

            # レディ設定
            if (capture is not None) and (not os.path.exists(self.fileRdy)):
                qFunc.statusSet(self.fileRdy, True)
            if (capture is None) and (os.path.exists(self.fileRdy)):
                qFunc.statusSet(self.fileRdy, False)

            # ステータス応答
            if (inp_name.lower() == '_status_'):
                out_name  = inp_name
                if (capture is not None):
                    out_value = '_ready_'
                else:
                    out_value = '!ready'
                cn_s.put([out_name, out_value])

            # 連携情報
            if (inp_name.lower() == '_camstretch_'):
                self.camStretch = inp_value
                fps_last = time.time() - 60
            if (inp_name.lower() == '_camrotate_'):
                self.camRotate = inp_value
                fps_last = time.time() - 60
            if (inp_name.lower() == '_camzoom_'):
                self.camZoom = inp_value
                fps_last = time.time() - 60



            # 画像処理
            if (cn_s.qsize() == 0):
            #if (True):

                # 画像取得
                ret = False
                frame = None
                if (capture is not None):
                    try:
                        ret, frame = capture.read()
                    except Exception as e:
                        ret = False
                        frame = None

                if  (qFunc.statusCheck(qBusy_dev_cam) == False) \
                and (ret == False):
                    frame = None

                    #qLog.log('info', self.proc_id, 'capture error!', display=self.logDisp,)
                    #time.sleep(5.00)
                    #self.proc_step = '9'
                    #break

                    qLog.log('warning', self.proc_id, 'capture error!', )
 
                    # デバイス開放
                    if (capture is not None): 
                        try:
                            capture.release()
                        except Exception as e:
                            pass
                        capture = None

                    time.sleep(1.00)

                    # デバイス設定
                    capture = None
                    if (not self.camDev.isdigit()):
                        try:
                            capture = cv2.VideoCapture(self.camDev)
                        except Exception as e:
                            capture = None

                if (frame is None):

                    if  (qFunc.statusCheck(qBusy_dev_cam)  == True) \
                    and (qFunc.statusCheck(qBusy_v_recept) == True):
                        input_img = self.riki_img.copy()
                    else:
                        input_img = self.blue_img.copy()

                    # 結果出力
                    out_name  = '[img]'
                    out_value = input_img.copy()
                    cn_s.put([out_name, out_value])

                    time.sleep(0.50)
                    frame = None



                if (frame is not None):

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
                    if (int(self.camStretch) != 0):
                        x = int((input_width/2) * abs(int(self.camStretch))/100)
                        if (int(self.camStretch) > 0):
                            perspective1 = np.float32([ [x, 0], [input_width-x, 0], [input_width, input_height], [0, input_height] ])
                        else:
                            perspective1 = np.float32([ [0, 0], [input_width, 0], [input_width-x, input_height], [x, input_height] ])
                        perspective2 = np.float32([ [0, 0], [input_width, 0], [input_width, input_height], [0, input_height] ])
                        transform_matrix = cv2.getPerspectiveTransform(perspective1, perspective2)
                        input_img = cv2.warpPerspective(input_img, transform_matrix, (input_width, input_height))

                    # ミラー有効
                    if (qFunc.statusCheck(qRdy__v_mirror) == True):
                        input_img = cv2.flip(input_img, 1) # 180 Rotation X

                    # 画像回転
                    if   (int(self.camRotate) == -180):
                        input_img = cv2.flip(input_img, 0) # 180 Rotation Y
                    elif (int(self.camRotate) == -360):
                        input_img = cv2.flip(input_img, 1) # 180 Rotation X
                    elif (abs(int(self.camRotate)) !=   0):
                        width2    = int((input_width - input_height)/2)
                        rect_img  = cv2.resize(input_img[0:input_height, width2:width2+input_height], (960,960))
                        rect_mat  = cv2.getRotationMatrix2D((480, 480), -int(self.camRotate), 1.0)
                        rect_r    = cv2.warpAffine(rect_img, rect_mat, (960, 960), flags=cv2.INTER_LINEAR)
                        input_img = cv2.resize(rect_r, (input_height, input_height))
                        input_height, input_width = input_img.shape[:2]

                    # ズーム
                    if (float(self.camZoom) != 1):
                        zm = float(self.camZoom)
                        x1 = int((input_width-(input_width/zm))/2)
                        x2 = input_width - x1
                        y1 = int((input_height-(input_height/zm))/2)
                        y2 = input_height - y1
                        zm_img = input_img[y1:y2, x1:x2]
                        input_img = zm_img.copy()
                        input_height, input_width = input_img.shape[:2]

                    # 4角形補足
                    if (float(self.camSquare) != 0):
                        if (self.runMode == 'debug') \
                        or (self.runMode == 'camera'):
                            if  (qFunc.statusCheck(qBusy_d_rec) == False):

                                square_contours = []
                                gray = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)

                                # 0:黒字に白、1:白地に黒
                                for bw in range(2):

                                    # 画像補正
                                    if (bw == 0):
                                        _, thresh = cv2.threshold(gray, 192, 255, cv2.THRESH_BINARY_INV)
                                    else:
                                        gray2 = cv2.bitwise_not(gray)
                                        _, thresh = cv2.threshold(gray2, 192, 255, cv2.THRESH_BINARY_INV)
                                    thresh_not = cv2.bitwise_not(thresh)

                                    # 輪郭抽出・幾何図形取得（黒字に白）
                                    contours, hierarchy = cv2.findContours(thresh_not, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                                    for i, cnt in enumerate(contours):

                                        # 面積で選別
                                        area = cv2.contourArea(cnt)
                                        if (area > ((input_height * input_width) * float(self.camSquare))):

                                            # 輪郭長さで輪郭を近似化する。
                                            arclen = cv2.arcLength(cnt, True)
                                            epsilon_len = arclen * 0.05
                                            approx_cnt = cv2.approxPolyDP(cnt, epsilon=epsilon_len, closed=True)

                                            # 画数で選別
                                            if (len(approx_cnt) == 4):

                                                # 座標ずらす
                                                x = np.array([])
                                                y = np.array([])
                                                for i in range(4):
                                                    x = np.append(x, approx_cnt[i][0][0])
                                                    y = np.append(y, approx_cnt[i][0][1])
                                                ave_x = np.mean(x)
                                                ave_y = np.mean(y)

                                                hit1 = False
                                                hit2 = False
                                                hit3 = False
                                                hit4 = False
                                                for i in range(4):
                                                    if (x[i] <= ave_x) and (y[i] <= ave_y):
                                                        hit1 = True
                                                        approx_cnt[0][0][0]=x[i]
                                                        approx_cnt[0][0][1]=y[i]
                                                    if (x[i] <= ave_x) and (y[i] > ave_y):
                                                        hit2 = True
                                                        approx_cnt[1][0][0]=x[i]
                                                        approx_cnt[1][0][1]=y[i]
                                                    if (x[i] > ave_x) and (y[i] > ave_y):
                                                        hit3 = True
                                                        approx_cnt[2][0][0]=x[i]
                                                        approx_cnt[2][0][1]=y[i]
                                                    if (x[i] > ave_x) and (y[i] <= ave_y):
                                                        hit4 = True
                                                        approx_cnt[3][0][0]=x[i]
                                                        approx_cnt[3][0][1]=y[i]

                                                if  (hit1 == True) and (hit2 == True) \
                                                and (hit3 == True) and (hit4 == True):
                                                    square_contours.append(approx_cnt)

                                # 4角形透過変換
                                for i, cnt in enumerate(square_contours):

                                    # 輪郭に外接する長方形を取得する。
                                    x, y, width, height = cv2.boundingRect(cnt)

                                    # 透過変換
                                    dst = []
                                    pts1 = np.float32(cnt)
                                    pts2 = np.float32([[0,0],[0,height],[width,height],[width,0]])

                                    M = cv2.getPerspectiveTransform(pts1,pts2)
                                    dst = cv2.warpPerspective(input_img,M,(width,height))

                                    #input_img = dst.copy()

                                    # オーバーレイ
                                    over_x = x
                                    over_y = y
                                    over_img = dst.copy()
                                    over_height, over_width = over_img.shape[:2]

                                    if  (over_x >=0) and (over_y >=0) \
                                    and ((over_x + over_width) < input_width) \
                                    and ((over_y + over_height) < input_height):
                                        input_img[over_y:over_y+over_height, over_x:over_x+over_width] = over_img
                                        cv2.rectangle(input_img,(over_x,over_y),(over_x+over_width,over_y+over_height),(0,0,0),1)

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
                        if (float(self.camZoom) != 1):
                            out_value += ' (Zoom=' + self.camZoom + ')'
                        cn_s.put([out_name, out_value])

                    # 受付監視機能（差分検出）
                    if (bgsegm_model is not None):
                        # 出力画像
                        bgsegm_img = input_img.copy()
                        # 差分演算する
                        bgsegm_mask = bgsegm_model.apply(input_img)
                        # 輪郭抽出する
                        bgsegm_contours = cv2.findContours(bgsegm_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
                        # 小さい輪郭は除く
                        dot0001 = int((input_width * input_height) * 0.001 + 500)
                        bgsegm_contours = list(filter(lambda x: cv2.contourArea(x) > dot0001, bgsegm_contours))
                        if (len(bgsegm_contours) != 0):
                            # 輪郭を囲む外接矩形を取得する
                            bgsegm_boxs = list(map(lambda x: cv2.boundingRect(x), bgsegm_contours))
                            # 矩形を描画する
                            for x, y, w, h in bgsegm_boxs:
                                cv2.rectangle(bgsegm_img, (x, y), (x + w, y + h), (255,255,0), 3)
                            ## 輪郭を取得する
                            #bgsegm_contours2,hierarchy = cv2.findContours(bgsegm_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                            ## 輪郭を描写する
                            #bgsegm_img=cv2.drawContours(bgsegm_img, bgsegm_contours2, -1, (255,255,0), 3)

                        # 監視中余計な画像出力抑止
                        if (len(bgsegm_contours) > 0):
                            if (self.camDev_self == False):
                                # 結果出力
                                out_name  = '[bgsegm_img]'
                                out_value = bgsegm_img.copy()
                                cn_s.put([out_name, out_value])
                            # 結果出力
                            out_name  = '[img]'
                            out_value = input_img.copy()
                            cn_s.put([out_name, out_value])
                            input_img = None
                        else:
                            # 結果出力
                            out_name  = '[bgsegm_img]'
                            out_value = input_img.copy()
                            cn_s.put([out_name, out_value])
                            input_img = None

                    # 結果出力
                    if (input_img is not None):
                        out_name  = '[img]'
                        out_value = input_img.copy()
                        cn_s.put([out_name, out_value])



            # アイドリング
            slow = False
            if  (qFunc.statusCheck(qBusy_dev_cpu) == True):
                slow = True
            if  (qFunc.statusCheck(qBusy_dev_cam  ) == True):
                slow = True
            if  (qFunc.statusCheck(qBusy_d_play   ) == True) \
            or  (qFunc.statusCheck(qBusy_d_browser) == True):
                slow = True

            if (slow == True):
                time.sleep(1.00)
            else:
                time.sleep((1/int(self.camFps))/2)

        # 終了処理
        if (True):

            # レディ解除
            qFunc.statusSet(self.fileRdy, False)

            # デバイス開放
            if (capture is not None): 
                try:
                    capture.release()
                except Exception as e:
                    pass
                capture = None

            # ビジー解除 (!ready)
            qFunc.statusSet(self.fileBsy, False)
            if (str(self.id) == '0'):
                qFunc.statusSet(qBusy_v_inp, False)

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

    # ビジー解除 (!ready)
    qFunc.statusSet(qBusy_dev_cam, False)

    # 設定
    cv2.namedWindow('Display', 1)
    cv2.moveWindow( 'Display', 0, 0)

    #runMode='debug'
    runMode='reception'
    camDev='0'
    #camDev='http://192.168.200.251/nphMotionJpeg?Resolution=640x480'
    #camDev='http://kondou-note:5555/MotionJpeg?w=640&h=480'
    #camDev='http://localhost:5555/MotionJpeg?w=640&h=480'
    camera_thread = proc_camera(name='camera', id='0', runMode=runMode, 
                    camDev=camDev, camMode='vga', camStretch='0', camRotate='0', camZoom='1.0', camFps='5',)
    camera_thread.begin()



    # ループ
    chktime = time.time()
    limit_sec = 15
    if (camDev != '0'):
        limit_sec = 600
    while ((time.time() - chktime) < limit_sec):

        res_data  = camera_thread.get()
        res_name  = res_data[0]
        res_value = res_data[1]
        if (res_name != ''):
            if (res_name == '[img]'):
                print(res_name, )
                cv2.imshow('Display', res_value.copy() )
                cv2.waitKey(1)
            elif (res_name == '[bgsegm_img]'):
                print(res_name, )
                cv2.imshow('Display', res_value.copy() )
                cv2.waitKey(1)
            else:
                print(res_name, res_value, )

        #if (camera_thread.proc_s.qsize() == 0):
        #    camera_thread.put(['_status_', ''])

        time.sleep(0.02)

    time.sleep(1.00)
    camera_thread.abort()
    del camera_thread



    cv2.destroyAllWindows()



