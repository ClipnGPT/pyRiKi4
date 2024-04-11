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



class proc_cv2dnn_yolo:

    def __init__(self, name='thread', id='0', runMode='debug',
                    procMode='640x480', ):
        self.runMode   = runMode
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

        # 定義ファイル
        file_config  = '_cv2data/dnn/yolov3/yolov3-tiny.cfg'
        file_weights = '_cv2data/dnn/yolov3/yolov3-tiny.weights'
        file_labels  = '_cv2data/dnn/yolov3/coco-labels.txt'
        #file_config  = '_cv2data/dnn/yolov3/yolov3.cfg'
        #file_weights = '_cv2data/dnn/yolov3/yolov3.weights'
        threshold_score = 0.25
        threshold_nms   = 0.4

        qLog.log('debug', self.proc_id, 'Loading Network.....', )
        model = cv2.dnn.readNetFromDarknet(file_config, file_weights)
        model.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        model.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
        layer_names = model.getLayerNames()
        #layer_names = [layer_names[i[0] - 1] for i in model.getUnconnectedOutLayers()]
        layer_names = [layer_names[i - 1] for i in model.getUnconnectedOutLayers()]
        qLog.log('debug', self.proc_id, 'Network successfully loaded', )

        # モデルの中の訓練されたクラス名
        classNames  = {}
        classColors = {}
        r = codecs.open(file_labels, 'r', 'utf-8')
        i = 0
        for t in r:
            t = t.replace('\n', '')
            t = t.replace('\r', '')
            classNames[i]  = str(t).strip()
            classColors[i] = np.random.randint(low=0, high=255, size=3, dtype='uint8')
            i += 1

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



                # 画像の読み込み
                image = inp_value.copy()
                image_height, image_width = image.shape[:2]

                # 入力画像成形
                if (image_width > image_height):
                    image_size = image_width
                    inp_image = np.zeros((image_width,image_width,3), np.uint8)
                    offset = int((image_width-image_height)/2)
                    inp_image[offset:offset+image_height, 0:image_width] = image.copy()

                    out_image = inp_image.copy()
                elif (image_height > image_width):
                    image_size = image_height
                    inp_image = np.zeros((image_height,image_height,3), np.uint8)
                    offset = int((image_height-image_width)/2)
                    inp_image[0:image_height, offset:offset+image_width] = image.copy()
                    out_image = inp_image.copy()
                else:
                    image_size = image_width
                    inp_image = image.copy()
                    out_image = inp_image.copy()

                # Imageをセットする
                blob = cv2.dnn.blobFromImage(inp_image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
                model.setInput(blob)

                # 画像から物体検出を行う
                output = model.forward(layer_names)

                pass_classids = []
                pass_scores   = []
                pass_boxes    = []

                # 人物検索
                nowTime = datetime.datetime.now()
                stamp = nowTime.strftime('%Y%m%d.%H%M%S')
                hit_count = 0
                hit_img   = None

                # ループ
                for detections in output:

                    # detectionには[Xの中心点、Yの中心点、Xの幅、Yの幅、クラス別予測確率…]が入っている。
                    for detection in detections:

                        # クラス別予測確率の最大を取り出す
                        scores = detection[5:]
                        classid = np.argmax(scores)

                        # 予測確率がthreshold_score以上を取り出す。
                        score = scores[classid]
                        if (score >= threshold_score):

                            # 元の画像サイズを掛けて、四角で囲むための4点の座標情報を得る
                            axis = detection[0:4] * (image_size, image_size, image_size, image_size)

                            # floatからintに変換して、変数に取り出す。
                            center_x, center_y, b_width, b_height = axis.astype(np.int64)[:4]
                            left   = int(center_x - b_width/2)
                            top    = int(center_y - b_height/2)
                            width  = int(b_width)
                            height = int(b_height)

                            # 変数に取り出す。
                            if  (width  >= image_size/20) and (width  <= image_size/2) \
                            and (height >= image_size/30) and (height <= image_size/1.5):
                                pass_classids.append(classid)
                                pass_scores.append(float(score))
                                pass_boxes.append([left, top, width, height])

                # 重複した領域を排除した内容を利用する。
                indices = cv2.dnn.NMSBoxes(pass_boxes, pass_scores, float(0.8), float(threshold_nms))
                if (len(indices)<3):
                    indices = cv2.dnn.NMSBoxes(pass_boxes, pass_scores, float(0.5), float(threshold_nms))
                if (len(indices)<3):
                    indices = cv2.dnn.NMSBoxes(pass_boxes, pass_scores, float(0.0), float(threshold_nms))
                for i in indices:
                    #i = i[0]
                    classid = pass_classids[i]
                    score   = pass_scores[i]
                    box     = pass_boxes[i]
                    left    = box[0]
                    if (left < 0):
                        left = 0
                    top     = box[1]
                    if (top < 0):
                        top = 0
                    width   = box[2]
                    if ((left + width) > image_size):
                        width = image_width - left
                    height  = box[3]
                    if ((top + height) > image_size):
                        height = image_size - top

                    # クラス名を取り出す。
                    class_name  = classNames[classid]
                    class_color = [ int(c) for c in classColors[classid] ]
                    label       = class_name + ' {0:.2f}'.format(score)

                    # (画像、開始座標、終了座標、色、線の太さ)を指定
                    cv2.rectangle(out_image, (left, top), (left+width, top+height), class_color, thickness=2)

                    # (画像、文字列、開始座標、フォント、文字サイズ、色)を指定
                    t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_COMPLEX_SMALL, 1 , 1)[0]
                    x = left + t_size[0] + 3
                    y = top + t_size[1] + 4
                    cv2.rectangle(out_image, (left, top), (x, y), class_color, -1)
                    cv2.putText(out_image, label, (left, top + t_size[1] + 1), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 1)

                    # 認識画像出力
                    if (score >= 0.5):
                        if (class_name == 'person') \
                        or (class_name == 'car'):

                            # 結果出力
                            out_name  = '[array]'
                            #out_value = inp_image[top:top+height, left:left+width].copy()
                            out_value = out_image[top:top+height, left:left+width].copy()
                            cn_s.put([out_name, out_value])

                        # 人物保管
                        if (class_name == 'person'):
                            hit_count += 1
                            if (hit_count == 1):
                                hit_img = inp_image[top:top+height, left:left+width].copy()

                                # ファイル出力
                                fn0 = stamp + '.' + class_name + '.jpg'
                                fn1 = qPath_rec      + fn0
                                fn2 = qPath_v_detect + fn0
                                fn3 = qPath_v_recept + fn0
                                if  (not os.path.exists(fn1)) \
                                and (not os.path.exists(fn2)) \
                                and (not os.path.exists(fn3)):
                                    try:

                                        cv2.imwrite(fn1, hit_img)
                                        cv2.imwrite(fn2, hit_img)
                                        cv2.imwrite(fn3, hit_img)

                                    except Exception as e:
                                        pass

                # 出力画像復元
                if (image_width > image_height):
                    offset = int((image_width-image_height)/2)
                    out_image = out_image[offset:offset+image_height, 0:image_width].copy()
                elif (image_height > image_width):
                    offset = int((image_height-image_width)/2)
                    out_image = out_image[0:image_height, offset:offset+image_width].copy()

                 # ＦＰＳ計測
                fps = fps_class.get()
                if ((time.time() - fps_last) > 5):
                    fps_last  = time.time()

                    # 結果出力(fps)
                    out_name  = '_fps_'
                    out_value = '{:.2f}'.format(fps)
                    cn_s.put([out_name, out_value])

                    # 結果出力(reso)
                    out_height, out_width = out_image.shape[:2]
                    out_name  = '_reso_'
                    out_value = str(out_width) + 'x' + str(out_height)
                    cn_s.put([out_name, out_value])

                # 結果出力
                out_name  = '[img]'
                out_value = out_image.copy()
                cn_s.put([out_name, out_value])

                #time.sleep(0.50)



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
                    time.sleep(0.25)
                else:
                    time.sleep(0.05)

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

    cv2dnn_yolo_thread = proc_cv2dnn_yolo('dnn_yolo', '0', )
    cv2dnn_yolo_thread.begin()

    #frame = cv2.imread('_photos/_photo_face.jpg')
    #cv2.imshow('Display', frame )
    #cv2.waitKey(1)
    #time.sleep(3.00)
    capture = cv2.VideoCapture('_photos/_drive.mp4')



    # ループ
    chktime = time.time()
    while ((time.time() - chktime) < 999):

        ret, frame = capture.read()
        if (frame is None):
            print('frame none')
            break

        while (cv2dnn_yolo_thread.proc_s.qsize() != 0):
            time.sleep(0.05)

        if (cv2dnn_yolo_thread.proc_s.qsize() == 0):
            frame2 = cv2.resize(frame, (480, 270))
            cv2dnn_yolo_thread.put(['[img]', frame2])

        while (cv2dnn_yolo_thread.proc_r.qsize() != 0):
            res_data  = cv2dnn_yolo_thread.get()
            res_name  = res_data[0]
            res_value = res_data[1]
            if (res_name != ''):
                cv2.namedWindow('Display', 1)
                if (res_name == '[img]'):
                    cv2.imshow('Display', res_value.copy() )
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                #if (res_name == '[array]'):
                #    cv2.imshow('Ary', res_value.copy() )
                #    if cv2.waitKey(1) & 0xFF == ord('q'):
                #        break
                if (res_name == '_fps_'):
                    print(res_name, res_value, )
                #else:
                #    print(res_name, res_value, )

        time.sleep(0.05)

    capture.release()



    #cv2.waitKey(0)
    time.sleep(1.00)
    cv2dnn_yolo_thread.abort()
    del cv2dnn_yolo_thread

    cv2.destroyAllWindows()



