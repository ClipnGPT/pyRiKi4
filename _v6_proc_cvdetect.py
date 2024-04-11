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



class proc_cvdetect:

    def __init__(self, name='thread', id='0', runMode='debug', 
                    casName='face', procMode='640x480', ):
        self.runMode   = runMode

        self.casName   = casName
        if (casName == 'cars'):
            self.casName = '_cv2data/xml/_vision_opencv_cars.xml'
        if (casName == 'face'):
            self.casName = '_cv2data/xml/_vision_opencv_face.xml'
        if (casName == 'fullbody'):
            self.casName = '_cv2data/xml/_vision_opencv_fullbody.xml'
        if (self.casName != 'none'):
            self.cas_nm  = self.casName[:-4]
            self.cas_nm  = self.cas_nm.replace('_cv2data/xml/_vision_opencv_', '')
            self.cascade = cv2.CascadeClassifier(self.casName)
            self.haar_scale    = 1.1
            self.min_neighbors = 10
            self.min_size      = ( 15, 15)
            if (self.cas_nm == 'cars'):
                self.haar_scale    = 1.1
                self.min_neighbors = 3
                self.min_size      = ( 15, 15)

        self.procMode  = procMode
        procWidth, procHeight = qGUI.getResolution(procMode)
        self.procWidth = procWidth
        self.procHeight= procHeight

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



            # 画像受取
            if (inp_name.lower() == '[img]'):

                # 実行カウンタ
                self.proc_last = time.time()
                self.proc_seq += 1
                if (self.proc_seq > 9999):
                    self.proc_seq = 1

                # ビジー設定
                if (qFunc.statusCheck(self.fileBsy) == False):
                    qFunc.statusSet(self.fileBsy, True)

                # 処理

                image_img   = inp_value.copy()
                image_height, image_width = image_img.shape[:2]

                output_img  = image_img.copy()

                proc_width  = image_width
                proc_height = image_height
                if (proc_width  > self.procWidth):
                    proc_width  = self.procWidth
                    proc_height = int(proc_width * image_height / image_width)
                if (proc_width  != image_width ) \
                or (proc_height != image_height):
                    proc_img = cv2.resize(image_img, (proc_width, proc_height))
                else:
                    proc_img = image_img.copy()
                    proc_height, proc_width = proc_img.shape[:2]

                gray1 = cv2.cvtColor(proc_img, cv2.COLOR_BGR2GRAY)
                gray2 = cv2.equalizeHist(gray1)

                nowTime = datetime.datetime.now()
                stamp = nowTime.strftime('%Y%m%d.%H%M%S')

                hit_count = 0
                hit_img   = None

                if (self.casName != 'none'):

                    rects = self.cascade.detectMultiScale(gray2, scaleFactor=self.haar_scale, minNeighbors=self.min_neighbors, minSize=self.min_size)
                    if (rects is not None):
                        #qLog.log('debug', self.proc_id, 'detect count = ' + str(len(rects)), )
                        for (hit_x, hit_y, hit_w, hit_h) in rects:
                            hit_count += 1
                            x  = int(hit_x * image_width  / proc_width )
                            y  = int(hit_y * image_height / proc_height)
                            w  = int(hit_w * image_width  / proc_width )
                            h  = int(hit_h * image_height / proc_height)
                            if (self.cas_nm == 'face'):
                                if (x > 10):
                                    x -= 10
                                    w += 20
                                if (y > 10):
                                    y -= 10
                                    h += 20
                            if (x < 0):
                                x = 0
                            if (y < 0):
                                y = 0
                            if ((x + w) > image_width):
                                    w = image_width - x
                            if ((y + h) > image_height):
                                    h = image_height - y
                            cv2.rectangle(output_img, (x,y), (x+w,y+h), (0,0,255), 2)

                            hit_img = cv2.resize(image_img[y:y+h, x:x+w],(h,w))

                            if (hit_count == 1):

                                # 結果出力
                                out_name  = '[detect]'
                                out_value = hit_img.copy()
                                cn_s.put([out_name, out_value])

                                # ファイル出力
                                fn0 = stamp + '.' + self.cas_nm + '.jpg'
                                fn1 = qPath_rec      + fn0
                                fn2 = qPath_v_detect + fn0
                                fn3 = qPath_v_recept + fn0
                                if  (not os.path.exists(fn1)) \
                                and (not os.path.exists(fn2)) \
                                and (not os.path.exists(fn3)):
                                    try:

                                        cv2.imwrite(fn1, hit_img)
                                        cv2.imwrite(fn2, hit_img)
                                        if (self.cas_nm == 'face'):
                                            cv2.imwrite(fn3, hit_img)

                                    except Exception as e:
                                        pass

                            # 結果出力
                            out_name  = '[array]'
                            out_value = hit_img.copy()
                            cn_s.put([out_name, out_value])

                if (hit_count == 0):

                    # 結果出力
                    out_name  = ''
                    out_value = ''
                    cn_s.put([out_name, out_value])

                else:

                    # 結果出力
                    #out_name  = '[photo]'
                    #out_value = image_img.copy()
                    #cn_s.put([out_name, out_value])

                    # 結果出力
                    out_name  = '[img]'
                    out_value = output_img.copy()
                    cn_s.put([out_name, out_value])

                    # ファイル出力
                    fn3 = qPath_rec     + stamp + '.detect.jpg'
                    fn4 = qPath_v_photo + stamp + '.detect.jpg'
                    if (not os.path.exists(fn3)) and (not os.path.exists(fn4)):
                        try:
                            cv2.imwrite(fn3, image_img)
                            cv2.imwrite(fn4, image_img)
                        except Exception as e:
                            pass

                time.sleep(0.50)



            # ビジー解除
            qFunc.statusSet(self.fileBsy, False)

            # アイドリング
            slow = False
            if  (qFunc.statusCheck(qBusy_dev_cpu  ) == True):
                slow = True
            if  (qFunc.statusCheck(qBusy_dev_cam  ) == True):
                slow = True
            if  (qFunc.statusCheck(qBusy_d_play   ) == True) \
            or  (qFunc.statusCheck(qBusy_d_browser) == True):
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



if __name__ == '__main__':

    # 共通クラス
    qRiKi.init()
    qFunc.init()

    # ログ
    nowTime  = datetime.datetime.now()
    filename = qPath_log + nowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
    qLog.init(mode='logger', filename=filename, )

    # 設定
    cv2.namedWindow('Display', 1)
    cv2.moveWindow( 'Display', 0, 0)

    cvdetect_thread = proc_cvdetect('detect', '0', procMode='full',)
    cvdetect_thread.begin()

    inp = cv2.imread('_photos/_photo_face.jpg')
    cv2.imshow('Display', inp )
    cv2.waitKey(1)
    time.sleep(3.00)

    cvdetect_thread.put(['[img]', inp.copy()])



    # ループ
    chktime = time.time()
    while ((time.time() - chktime) < 15):
        res_data  = cvdetect_thread.get()
        res_name  = res_data[0]
        res_value = res_data[1]
        if (res_name != ''):
            if (res_name == '[img]'):
                print('img')
                img = cv2.resize(res_value, (320, 240), )
                cv2.imshow('Display', img )
                cv2.waitKey(1)
                time.sleep(1.00)
            if (res_name == '[array]'):
                print('array')
                img = cv2.resize(res_value, (320, 240), )
                cv2.imshow('Display', img )
                cv2.waitKey(1)
                time.sleep(1.00)
            if (res_name == '[photo]'):
                print('photo')
                img = cv2.resize(res_value, (320, 240), )
                cv2.imshow('Display', img )
                cv2.waitKey(1)
                time.sleep(1.00)
            if (res_name == '[detect]'):
                print('detect')
                img = cv2.resize(res_value, (320, 240), )
                cv2.imshow('Display', img )
                cv2.waitKey(1)
                time.sleep(1.00)
            #else:
            #    print(res_name, res_value, )

        time.sleep(0.05)



    time.sleep(1.00)
    cvdetect_thread.abort()
    del cvdetect_thread

    cv2.destroyAllWindows()



