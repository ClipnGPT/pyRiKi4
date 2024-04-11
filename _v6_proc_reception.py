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

import shutil

import cv2

import queue
import threading
import subprocess



# 外部プログラム
qExt_face                = '__ext_face.bat'



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



# 顔認識
class qFace_class:

    def __init__(self, ): 
        self.face_procWidth  = 640
        self.face_procHeight = 480
        self.face_casName    = '_cv2data/xml/_vision_opencv_face.xml'
        self.face_cascade    = cv2.CascadeClassifier(self.face_casName)
        self.face_haar_scale    = 1.1
        self.face_min_neighbors = 10
        self.face_min_size      = ( 15, 15)

    def detect_face(self, inp_image=None, ):
        output_img  = inp_image.copy()
        output_face = []

        try:

                image_img   = inp_image.copy()
                image_height, image_width = image_img.shape[:2]

                output_img  = image_img.copy()

                proc_width  = image_width
                proc_height = image_height
                if (proc_width  > self.face_procWidth):
                    proc_width  = self.face_procWidth
                    proc_height = int(proc_width * image_height / image_width)
                if (proc_width  != image_width ) \
                or (proc_height != image_height):
                    proc_img = cv2.resize(image_img, (proc_width, proc_height))
                else:
                    proc_img = image_img.copy()
                    proc_height, proc_width = proc_img.shape[:2]

                gray1 = cv2.cvtColor(proc_img, cv2.COLOR_BGR2GRAY)
                gray2 = cv2.equalizeHist(gray1)

                hit_count = 0
                hit_img   = None

                rects = self.face_cascade.detectMultiScale(gray2, 
                        scaleFactor=self.face_haar_scale,
                        minNeighbors=self.face_min_neighbors,
                        minSize=self.face_min_size, )
                if (rects is not None):
                    for (hit_x, hit_y, hit_w, hit_h) in rects:
                        hit_count += 1
                        x  = int(hit_x * image_width  / proc_width )
                        y  = int(hit_y * image_height / proc_height)
                        w  = int(hit_w * image_width  / proc_width )
                        h  = int(hit_h * image_height / proc_height)
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

                        # 結果出力
                        output_face.append(hit_img)

        except:
            pass

        return output_img, output_face

# 顔認識
qFace = qFace_class()



class proc_reception:

    def __init__(self, name='thread', id='0', runMode='debug',
        camDev='0', ):

        self.path        = qPath_v_recept

        self.runMode     = runMode
        self.camDev      = camDev
        self.camDev_self = qFunc.chkSelfDev(camDev)

        self.breakFlag   = threading.Event()
        self.breakFlag.clear()
        self.name        = name
        self.id          = id
        self.proc_id     = '{0:10s}'.format(name).replace(' ', '_')
        self.proc_id     = self.proc_id[:-2] + '_' + str(id)
        if (runMode == 'debug'):
            self.logDisp = True
        else:
            self.logDisp = False
        qLog.log('info', self.proc_id, 'init', display=self.logDisp, )

        self.proc_s      = None
        self.proc_r      = None
        self.proc_main   = None
        self.proc_beat   = None
        self.proc_last   = None
        self.proc_step   = '0'
        self.proc_seq    = 0

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

        self.last_extface   = time.time() - 60
        self.last_pingpong  = time.time() - 60

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

            # 処理
            path = self.path
            path_files = glob.glob(path + '*.jpg')
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

                        if (proc_file[-4:].lower() == '.jpg' and proc_file[-8:].lower() != '.wrk.jpg'):
                            f1 = proc_file
                            f2 = proc_file[:-4] + '.wrk.jpg'
                            try:
                                os.rename(f1, f2)
                                proc_file = f2
                            except Exception as e:
                                pass

                        if (proc_file[-8:].lower() == '.wrk.jpg'):
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
                            work_file = qPath_work + work_name + '.jpg'
                            if (os.path.exists(work_file)):
                                os.remove(work_file)

                            #qFunc.copy(proc_file, work_file)
                            shutil.copy2(proc_file, work_file)

                            if (os.path.exists(work_file)):

                                qFunc.remove(proc_file)

                                # ログ
                                #if (self.runMode == 'debug') or (not self.camDev.isdigit()):
                                #    qLog.log('info', self.proc_id, '' + proc_name + ' → ' + work_name, display=self.logDisp,)

                                # ビジー設定
                                if (qFunc.statusCheck(self.fileBsy) == False):
                                    qFunc.statusSet(self.fileBsy, True)

                                # 処理
                                self.proc_last = time.time()
                                face_hit = self.sub_proc(seq4, proc_file, work_file, cn_s, )
                                if (face_hit == True):
                                    break

                #except Exception as e:
                #    pass

            # ビジー解除
            qFunc.statusSet(self.fileBsy, False)
            qFunc.statusSet(qBusy_v_recept, False)

            # アイドリング
            slow = False
            if  (qFunc.statusCheck(qBusy_dev_cpu) == True):
                slow = True
            if  (qFunc.statusCheck(qBusy_dev_cam) == True) \
            and (qFunc.statusCheck(qBusy_dev_mic) == True):
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
            qFunc.statusSet(qBusy_v_recept, False)

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



    def sub_proc(self, seq4, proc_file, work_file, cn_s, ):

        if (os.name == 'nt'):

            # ファイル名分解
            file_name = work_file.replace(qPath_work, '')

            # 外部プログラム
            if ((time.time() - self.last_extface) > 0):
                self.last_extface = time.time()
                if (os.path.exists(qExt_face)):
                    ext_face = subprocess.Popen([qExt_face, qPath_work, file_name, 'null', ], )
                               #shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

            # ピンポン音
            if ((time.time() - self.last_pingpong) > 60):
                self.last_pingpong = time.time()
                qFunc.guideSound(filename='_pingpong', sync=False)

        out_name  = '[img_file]'
        out_value = [proc_file]
        cn_s.put([out_name, out_value])

        # 遠隔カメラは、ここまで
        if (self.camDev_self == False):
            return False

        # 顔認証
        img = cv2.imread(work_file)
        out_img, out_face = qFace.detect_face(inp_image=img, )

        # 顔認識できなかった場合、ここまで
        if (len(out_face) == 0):
            return False

        # ここから受付動作

        # ビジー設定
        qLog.log('info', self.proc_id, '無人受付 START', display=True, )
        qFunc.statusSet(qBusy_v_recept, True)

        # カメラ・マイク停止
        qLog.log('info', self.proc_id, '無人受付 カメラ・マイク停止', display=True, )
        qFunc.statusSet(qBusy_dev_cam, True)
        qFunc.statusSet(qBusy_dev_mic, True)

        # 表示　開始
        qLog.log('info', self.proc_id, '無人受付 表示開始', display=True, )
        busy_dsp = qFunc.statusCheck(qBusy_dev_dsp, )
        qFunc.statusSet(qBusy_dev_dsp, False)

        # 案内１
        qRiKi.tts(self.proc_id, 'ja, 受付は無人となっております。')
        qRiKi.tts(self.proc_id, 'ja, ご用件を30秒以内で、おはなしください。')

        # 待機
        time.sleep(2)

        # マイク　開始
        qLog.log('info', self.proc_id, '無人受付 マイク開始', display=True, )
        qFunc.statusSet(qBusy_dev_mic, False)

        # 音声認識
        time.sleep(30)

        # マイク　停止
        qLog.log('info', self.proc_id, '無人受付 マイク停止', display=True, )
        qFunc.statusSet(qBusy_dev_mic, True)

        # 待機
        time.sleep(2)

        # 案内２
        qRiKi.tts(self.proc_id, 'ja, ありがとうございました。')

        # 待機
        time.sleep(5)

        # フォルダクリア
        qFunc.makeDirs(qPath_v_recept, True)
        
        # ビジー解除
        qFunc.statusSet(qBusy_v_recept, True)

        # カメラ・マイク　再開
        qLog.log('info', self.proc_id, '無人受付 カメラ・マイク再開', display=True, )
        qFunc.statusSet(qBusy_dev_cam, False)
        qFunc.statusSet(qBusy_dev_mic, False)

        # 表示　再設定
        qLog.log('info', self.proc_id, '無人受付 表示再設定', display=True, )
        qFunc.statusSet(qBusy_dev_dsp, busy_dsp)

        qLog.log('info', self.proc_id, '無人受付 END', display=True, )

        return True



if __name__ == '__main__':

    # 共通クラス
    qRiKi.init()
    qFunc.init()

    # ログ
    nowTime  = datetime.datetime.now()
    filename = qPath_log + nowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
    qLog.init(mode='logger', filename=filename, )

    # 設定
    reception_thread = proc_reception('reception', '0', )
    reception_thread.begin()



    # ループ
    chktime = time.time()
    while ((time.time() - chktime) < 120):

        res_data  = reception_thread.get()
        res_name  = res_data[0]
        res_value = res_data[1]
        if (res_name != ''):
            print(res_name, res_value, )

        if (reception_thread.proc_s.qsize() == 0):
            reception_thread.put(['_status_', ''])

        time.sleep(0.05)



    time.sleep(1.00)
    reception_thread.abort()
    del reception_thread



