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
from pyzbar.pyzbar import decode



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



class proc_cvreader:

    def __init__(self, name='thread', id='0', runMode='debug', 
                    reader='all', procMode='1920x1080'):
        self.runMode   = runMode
        self.reader    = reader

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

        # ２重読取防止
        read_time = {}

        # リーダー
        qrdetector = cv2.QRCodeDetector()

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
                self.proc_last = time.time()
                self.proc_seq += 1
                if (self.proc_seq > 9999):
                    self.proc_seq = 1

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
                    if (str(self.id) == '0') or (str(self.id) == 'v'):
                        qFunc.statusSet(qBusy_v_QR, True)
                    if (str(self.id) == 'd'):
                        qFunc.statusSet(qBusy_d_QR, True)

                # 処理

                image_img   = inp_value.copy()
                image_height, image_width = image_img.shape[:2]

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
                
                gray_img = cv2.cvtColor(proc_img, cv2.COLOR_BGR2GRAY)
                #gray_img = cv2.equalizeHist(gray_img)

                nowTime = datetime.datetime.now()
                stamp = nowTime.strftime('%Y%m%d.%H%M%S')



                hit_count = 0
                res_count = 0

                codes = decode(gray_img)
                for code in codes:

                    code_text = code.data.decode("utf-8")
                    code_type = code.type
                    code_img  = None

                    # 読取状況確認 qr -> read
                    read_text = code_text
                    if (read_text == 'http://localhost/v5/sendkey_on.py'):
                        read_text = '_sendkey_on_'
                    if (read_text == 'http://localhost/v5/mic_off.py'):
                        read_text = '_mic_off_'
                    if (read_text == 'http://localhost/v5/mic_on.py'):
                        read_text = '_mic_on_'
                    if (read_text == 'http://localhost/v5/cpu_off.py'):
                        read_text = '_cpu_off_'
                    if (read_text == 'http://localhost/v5/cpu_on.py'):
                        read_text = '_cpu_on_'

                    read_text = read_text.replace('\r\n', '[cr]')
                    read_text = read_text.replace('\r', '[cr]')
                    read_text = read_text.replace('\n', '[cr]')

                    # 透過変換 -> code_img
                    hit = False

                    points = code.polygon
                    if (code_type == 'QRCODE') and (len(points) == 4):
                        hit = True
                        perspective1 = np.zeros((4,2), np.float32)

                        i = 0
                        for point in points:
                            proc_x = point[0]
                            proc_y = point[1]
                            img_x  = int(proc_x * image_width  / proc_width )
                            img_y  = int(proc_y * image_height / proc_height)
                            perspective1[i] = [img_x, img_y]
                            i += 1

                        sz  = int(image_width/4)
                        perspective2 = np.float32([[0, 0], [0, sz], [sz, sz], [sz, 0]])
                        transform_matrix = cv2.getPerspectiveTransform(perspective1, perspective2)
                        code_img = cv2.warpPerspective(image_img, transform_matrix, (sz,sz))

                    # 切り出し -> code_img
                    #if (hit == False):
                    #    hit = True

                    #    proc_left, proc_top, proc_w, proc_h = code.rect
                    #    img_left  = int(proc_left * image_width  / proc_width ) - 20
                    #    if (img_left < 0):
                    #        img_left = 0
                    #    img_top   = int(proc_top  * image_height / proc_height) - 20
                    #    if (img_top < 0):
                    #        img_top = 0
                    #    img_w     = int(proc_w    * image_width  / proc_width ) + 40
                    #    if (img_left + img_w > image_width):
                    #        img_w = image_width - img_left - 1
                    #    img_h     = int(proc_h    * image_height / proc_height) + 40
                    #    if (img_top + img_h > image_height):
                    #        img_h = image_height - img_top - 1

                    #    code_img = image_img[img_top:img_top + img_h, img_left:img_left+img_w]

                    # 経過時間計算
                    try:
                        sec = time.time() - read_time[read_text]
                    except Exception as e:
                        sec = 999

                    # 新規
                    if (sec == 999):
                        read_time[read_text] = time.time()
                    # on 指令は最初だけ、あとは継続
                    elif (read_text[-4:] == '_on_') or (read_text[-5:] == '_off_'):
                        read_time[read_text] = time.time()
                        read_text = ''
                        code_img  = None
                    # ３秒経過は新規とみなす
                    elif (sec > 3):
                        read_time[read_text] = time.time()
                    # ３秒以内は無視
                    else:
                        read_text = ''
                        code_img  = None

                    # 読取ＯＫ
                    if (code_text != '') and (read_text != ''):
                        hit_count += 1
                        qLog.log('info', self.proc_id, '' + code_type + ' [' + code_text + ']')

                        # 読取文字
                        if (read_text != ''):
                            qLog.log('info', self.proc_id, 'reader [' + read_text + ']')

                            # 結果出力
                            out_name  = '[txts]'
                            out_value = read_text.split('[cr]')
                            cn_s.put([out_name, out_value])
                            res_count += 1

                        # 読取画像
                        if (code_img is not None):

                            # 結果出力
                            out_name  = '[img]'
                            out_value = code_img.copy()
                            cn_s.put([out_name, out_value])
                            res_count += 1

                            # ファイル出力
                            fn1 = qPath_rec      + stamp + '.' + code_type + '.jpg'
                            fn2 = qPath_v_detect + stamp + '.' + code_type + '.jpg'
                            if (not os.path.exists(fn1)) and (not os.path.exists(fn2)):
                                try:
                                    cv2.imwrite(fn1, code_img)
                                    cv2.imwrite(fn2, code_img)
                                except Exception as e:
                                    pass

                # 読取記録
                if (hit_count > 0):

                    fn3 = qPath_rec     + stamp + '.reader.jpg'
                    fn4 = qPath_v_photo + stamp + '.reader.jpg'
                    if (not os.path.exists(fn3)) and (not os.path.exists(fn4)):
                        try:
                            cv2.imwrite(fn3, image_img)
                            cv2.imwrite(fn4, image_img)
                        except Exception as e:
                            pass

                    # ガイド音
                    if (str(self.id) == '0') or (str(self.id) == 'v'):
                        qFunc.guideSound('_ok')

                # on 指令の自動解除
                for key in list(read_time):
                    if ((time.time() - read_time[key]) > 3):
                        read_time.pop(key)
                        read_text2 = ''

                        # 自動解除 on -> off
                        if (key[-4:] == '_on_'):
                            read_text2 = key[:-4] + '_off_'
                            qLog.log('info', self.proc_id, 'reader [' + read_text2 + ']')

                        # 自動解除 off -> on
                        if (key[-5:] == '_off_'):
                            read_text2 = key[:-5] + '_on_'
                            qLog.log('info', self.proc_id, 'reader [' + read_text2 + ']')

                        # 結果出力
                        if (read_text2 != ''):
                            out_name  = '[txts]'
                            out_value = [read_text2]
                            cn_s.put([out_name, out_value])
                            res_count += 1

                # 無応答防止
                if (res_count == 0):

                    # 結果出力
                    out_name  = ''
                    out_value = ''
                    cn_s.put([out_name, out_value])

                time.sleep(0.50)



            # ビジー解除
            qFunc.statusSet(self.fileBsy, False)
            if (str(self.id) == '0') or (str(self.id) == 'v'):
                qFunc.statusSet(qBusy_v_QR, False)
            if (str(self.id) == 'd'):
                qFunc.statusSet(qBusy_d_QR, False)

            # アイドリング
            slow = False
            if  (qFunc.statusCheck(qBusy_dev_cpu  ) == True):
                slow = True
            if  (qFunc.statusCheck(qBusy_d_play   ) == True) \
            or  (qFunc.statusCheck(qBusy_d_browser) == True):
                slow = True
            if (str(self.id) == '0') or (str(self.id) == 'v'):
                if (qFunc.statusCheck(qBusy_dev_cam) == True):
                    slow = True
            if (str(self.id) == 'd'):
                if  (qFunc.statusCheck(qBusy_dev_scn) == True):
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
            if (str(self.id) == '0') or (str(self.id) == 'v'):
                qFunc.statusSet(qBusy_v_QR, False)
            if (str(self.id) == 'd'):
                qFunc.statusSet(qBusy_d_QR, False)

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

    cvreader_thread = proc_cvreader('reader', '0', )
    cvreader_thread.begin()

    inp = cv2.imread('_photos/_photo_qrcode.jpg')
    cv2.imshow('Display', cv2.resize(inp, (640,480)))
    cv2.waitKey(1)
    time.sleep(3.00)

    cvreader_thread.put(['[img]', inp.copy()])



    # ループ
    chktime = time.time()
    while ((time.time() - chktime) < 15):
        res_data  = cvreader_thread.get()
        res_name  = res_data[0]
        res_value = res_data[1]
        if (res_name != ''):
            if (res_name == '[img]'):
                cv2.imshow('Display', res_value.copy() )
                cv2.waitKey(1)
                time.sleep(2.00)
            elif (res_name == '[txts]'):
                print(res_name, res_value[0], )

        time.sleep(0.05)



    time.sleep(1.00)
    cvreader_thread.abort()
    del cvreader_thread

    cv2.destroyAllWindows()



