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
from PIL import Image, ImageDraw, ImageFont



# インターフェース
qCtrl_control_desktop    = 'temp/control_desktop.txt'



# 共通ルーチン
import  _v6__qRiKi
qRiKi = _v6__qRiKi.qRiKi_class()
import  _v6__qFunc
qFunc = _v6__qFunc.qFunc_class()
import  _v6__qLog
qLog  = _v6__qLog.qLog_class()
import  _v6__qFFmpeg
qFFmpeg=_v6__qFFmpeg.qFFmpeg_class()
qCV2   =_v6__qFFmpeg.qCV2_class()
import  _v6__qGuide
qGuide= _v6__qGuide.qGuide_class()

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



class proc_telework:

    def __init__(self, name='thread', id='0', runMode='debug', 
        sec=600, ):

        self.runMode   = runMode
        self.sec       = sec

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

        self.telework_run = False
        self.telework_end = False
        self.check_time   = 0
        self.check_step   = -1
        self.desktop_img  = None
        self.camera_img   = []
        self.face_img     = None
        self.display_img  = None

        # フォント
        self.font_default = {'file':qPath_fonts + '_vision_font_ipaexg.ttf','offset':8}
        self.font_status  = {'file':qPath_fonts + '_vision_font_ipag.ttf',  'offset':8}
        try:
            self.font192_default  = ImageFont.truetype(self.font_default['file'], 192, encoding='unic')
            self.font192_defaulty =                    self.font_default['offset']
        except:
            self.font192_default  = None
            self.font192_defaulty = 0

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
            telework_text = ''
            if (inp_name.lower() == '_status_'):
                out_name  = inp_name
                out_value = '_ready_'
                cn_s.put([out_name, out_value])

            # 処理
            elif (inp_name.lower() != ''):
                proc_text = inp_value

                qLog.log('info', self.proc_id, proc_text, display=True, )

                if (proc_text.find('リセット') >=0):
                    self.telework_run = False
                    self.telework_end = False
                    self.check_time   = 0
                    qFunc.statusSet(self.fileBsy, False)
                    if (str(self.id) == '0'):
                        qFunc.statusSet(qBusy_d_telework, False)

                elif (proc_text.lower() == '_telework_stop_') \
                  or (proc_text.find('テレワーク') >=0) and (proc_text.find('停止') >=0) \
                  or (proc_text.find('テレワーク') >=0) and (proc_text.find('終了') >=0):
                    if (self.telework_run == True):
                        self.telework_run = False
                        self.telework_end = True
                        self.check_time   = 0
                        telework_text = proc_text

                elif (proc_text.lower() == '_telework_start_') \
                  or (proc_text.lower() == '_telework_restart_') \
                  or (proc_text.find('テレワーク') >=0) and (proc_text.find('開始') >=0):
                    self.telework_run = True
                    self.telework_end = False
                    self.check_time   = 0
                    telework_text = proc_text

            # 在席チェック
            if (self.telework_run == True) or (self.telework_end == True):
                self.check_proc(telework_text, cn_s)

            if (str(self.id) == '0'):
                if  (self.telework_run == True) \
                or  (self.telework_end == True):
                    if (qFunc.statusCheck(qBusy_d_telework) == False):
                        qFunc.statusSet(qBusy_d_telework, True)
                else:
                    if (qFunc.statusCheck(qBusy_d_telework) == True):
                        qFunc.statusSet(qBusy_d_telework, False)

            # アイドリング
            slow = False
            if  (qFunc.statusCheck(qBusy_dev_cpu) == True):
                slow = True
            if  (self.telework_run == False) \
            and (self.telework_end == False):
                slow = True

            if (slow == True):
                time.sleep(1.00)
            else:
                if (cn_r.qsize() == 0):
                    time.sleep(0.50)
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

    def check_proc(self, telework_text, cn_s):

        alpha_channel = 0.2

        # 限界時間到達？
        start = False
        if (self.telework_run == True):
            if ((time.time() - self.check_time) > self.sec):
                start = True
                self.check_time  = time.time()
                if (telework_text == ''):
                    self.check_step  = 1
                else:
                    self.check_step  = 13
                self.desktop_img = None
                self.camera_img  = []
                self.face_img    = None
                self.display_img = None

        if (self.telework_end == True):
            if (self.check_step < 0):
                start = True
                self.check_time  = time.time()
                self.check_step  = 13
                self.desktop_img = None
                self.camera_img  = []
                self.face_img    = None
                self.display_img = None

        if (start == True):
            # ビジー設定
            if (qFunc.statusCheck(self.fileBsy) == False):
                qFunc.statusSet(self.fileBsy, True)

            # 実行カウンタ
            self.proc_last = time.time()
            self.proc_seq += 1
            if (self.proc_seq > 9999):
                self.proc_seq = 1
            seq4 = '{:04}'.format(self.proc_seq)
            seq2 = '{:02}'.format(self.proc_seq)

        # ３０秒前
        if   (self.check_step == 1) and ((time.time() - self.check_time) >= 0.00):
            self.check_time  = time.time()
            self.check_step  = 2

            img = cv2.imread(qPath_icons + 'number_30.png')
            cn_s.put(['_telework_guide_image_', img])

        if   (self.check_step == 2) and ((time.time() - self.check_time) >= 2.00):
            self.check_time  = time.time()
            self.check_step  = 3

            cn_s.put(['_telework_guide_close_', None])

        if   (self.check_step == 3) and ((time.time() - self.check_time) >= 20.00):
            self.check_time  = time.time()
            self.check_step  = 13

        # ５秒前
        if   (self.check_step == 11) and ((time.time() - self.check_time) >= 0.00):
            self.check_time  = time.time()
            self.check_step  = 12

            img = cv2.imread(qPath_icons + 'number_5.png')
            cn_s.put(['_telework_guide_image_', img])

        # ４秒前
        elif (self.check_step == 12) and ((time.time() - self.check_time) >= 2.00):
            self.check_time  = time.time()
            self.check_step  = 13

            img = cv2.imread(qPath_icons + 'number_4.png')
            cn_s.put(['_telework_guide_image_', img])

        # ３秒前
        elif (self.check_step == 13) and ((time.time() - self.check_time) >= 2.00):
            self.check_time  = time.time()
            self.check_step  = 14

            img = cv2.imread(qPath_icons + 'number_3.png')
            cn_s.put(['_telework_guide_image_', img])

        # ２秒前
        elif (self.check_step == 14) and ((time.time() - self.check_time) >= 2.00):
            self.check_time  = time.time()
            self.check_step  = 15

            img = cv2.imread(qPath_icons + 'number_2.png')
            cn_s.put(['_telework_guide_image_', img])

        # １秒前
        elif (self.check_step == 15) and ((time.time() - self.check_time) >= 2.00):
            self.check_time  = time.time()
            self.check_step  = 21

            img = cv2.imread(qPath_icons + 'number_1.png')
            cn_s.put(['_telework_guide_image_', img])

        # 環境取得
        elif (self.check_step == 21) and ((time.time() - self.check_time) >= 2.00):
            cn_s.put(['_telework_guide_close_', None])
            self.check_time  = time.time()
            self.check_step  = 22

            self.desktop_img = None
            self.camera_img  = []
            self.face_img    = None
            self.display_img = None

            # デバイス名取得
            cam, mic = qFFmpeg.ffmpeg_list_dev()

            # カメラ
            checkTime = time.time()
            while (self.face_img is None) and ((time.time() - checkTime) < 15.00):
                for cam_dev in cam:
                    work_path = qPath_work + qFunc.txt2filetxt(cam_dev)
                    img       = qFFmpeg.capture(dev=cam_dev, full=True, work_path=work_path, )
                    if (img is not None):
                        self.camera_img.append(img)
                        _, face_imgs = qCV2.cv2detect_cascade(inp_image=img, search='face', )
                        if (len(face_imgs) > 0):
                            self.face_img = face_imgs[0]
            if (len(cam) == 0):
                time.sleep(2.00)

            # デスクトップ
            work_path = qPath_work + 'desktop'
            self.desktop_img = qFFmpeg.capture(dev='desktop', full=True, work_path=work_path, )

            # 表示
            #if (self.desktop_img is not None):
            #    cn_s.put(['_telework_guide_', self.desktop_img])
            #if (self.face_img is not None):
            #    cn_s.put(['_telework_guide_', self.face_img])

            # 画像生成
            self.display_img = self.desktop_img.copy()
            display_height, display_width = self.display_img.shape[:2]

            # 顔合成
            if (self.face_img is not None):
                face_height, face_width = self.face_img.shape[:2]
                over_x = display_width  - face_width  - 10
                over_y = display_height - face_height - 10
                self.display_img[over_y:over_y+face_height, over_x:over_x+face_width] = self.face_img

            # 文字合成
            nowTime = datetime.datetime.now()
            txt     = nowTime.strftime('%m/%d %H:%M')

            textcolor = (0,255,0)
            if (len(self.camera_img) != 0):
                if (self.face_img is None):
                    txt += ' 離席中'
                    textcolor = (255,0,255)

            if (self.font192_default is None):
                cv2.putText(self.display_img, txt, (5,display_height-15), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, textcolor)
            else:
                pil_image = qGuide.cv2pil(self.display_img)
                text_draw = ImageDraw.Draw(pil_image)
                text_draw.text((10, 10), txt, font=self.font192_default, fill=textcolor)
                self.display_img = qGuide.pil2cv(pil_image)

            self.check_time  = time.time()

        # 表示と保存
        if   (self.check_step == 22) and ((time.time() - self.check_time) >= 0.00):
            self.check_time  = time.time()
            self.check_step = -1

            # 表示
            cn_s.put(['_telework_guide_image_', self.display_img])

            # 保存
            nowTime = datetime.datetime.now()
            stamp   = nowTime.strftime('%Y%m%d.%H%M%S')
            filename0 = qPath_rec      + stamp + '.telework.jpg'
            filename1 = qPath_d_upload + stamp + '.telework.jpg'
            filename2 = qPath_d_upload +         '_telework.jpg'
            cv2.imwrite(filename0, self.display_img)
            time.sleep(1.00)
            qFunc.copy(filename0, filename1)
            qFunc.copy(filename0, filename2)

            yyyymmdd = stamp[:8]
            if (qPath_pictures != ''):
                folder = qPath_pictures + yyyymmdd + '/'
                qFunc.makeDirs(folder)
                qFunc.copy(filename0, folder + stamp + '.telework.jpg')

            # 消去
            time.sleep(2.00)
            cn_s.put(['_telework_guide_close_', None])

            # ビジー解除
            qFunc.statusSet(self.fileBsy, False)

            self.telework_end = False



if __name__ == '__main__':

    # 共通クラス
    qRiKi.init()
    qFunc.init()

    # ログ
    nowTime  = datetime.datetime.now()
    filename = qPath_log + nowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
    qLog.init(mode='logger', filename=filename, )

    # 初期設定
    qFunc.remove(qCtrl_control_desktop)
    qRiKi.statusReset_desktop(False)

    # パラメータ
    runMode = 'debug'
    if (len(sys.argv) >= 2):
        runMode  = str(sys.argv[1]).lower()

    # 開始
    telework_thread = proc_telework('telework', '0', runMode, sec=60, )
    telework_thread.begin()



    # テスト実行
    if (len(sys.argv) < 2):

        telework_thread.put(['control', 'テレワーク開始'])

        chktime = time.time()
        while ((time.time() - chktime) < 150):

            res_data  = telework_thread.get()
            res_name  = res_data[0]
            res_value = res_data[1]
            if   (res_name == '_telework_guide_image_'):
                qGuide.init(screen=0, panel='0-', title='telework', image=res_value, alpha_channel=0.5, )
                qGuide.open()
            elif (res_name == '_telework_guide_close_'):
                qGuide.close()

            elif (res_name != ''):
                print(res_name, res_value, )

            #if (telework_thread.proc_s.qsize() == 0):
            #    telework_thread.put(['_status_', ''])

            time.sleep(1.00)

        telework_thread.put(['control', 'テレワーク終了'])

        chktime = time.time()
        while ((time.time() - chktime) < 30):

            res_data  = telework_thread.get()
            res_name  = res_data[0]
            res_value = res_data[1]
            if   (res_name == '_telework_guide_image_'):
                qGuide.init(screen=0, panel='0-', title='telework', image=res_value, alpha_channel=0.5, )
                qGuide.open()
            elif (res_name == '_telework_guide_close_'):
                qGuide.close()

            elif (res_name != ''):
                print(res_name, res_value, )

            #if (telework_thread.proc_s.qsize() == 0):
            #    telework_thread.put(['_status_', ''])

            time.sleep(1.00)



    # 単体実行
    if (len(sys.argv) >= 2):

        # 待機ループ
        while (True):

            # 終了確認
            control = ''
            txts, txt = qFunc.txtsRead(qCtrl_control_desktop)
            if (txts != False):
                qLog.log('info', str(txt))
                if (txt == '_end_'):
                    break
                else:
                    qFunc.remove(qCtrl_control_desktop)
                    control = txt

            # メッセージ
            res_data  = telework_thread.get()
            res_name  = res_data[0]
            res_value = res_data[1]
            if   (res_name == '_telework_guide_image_'):
                qGuide.init(screen=0, panel='0-', title='telework', image=res_value, alpha_channel=0.5, )
                qGuide.open()
            elif (res_name == '_telework_guide_close_'):
                qGuide.close()

            time.sleep(0.50)



    # 終了
    telework_thread.abort()
    del telework_thread



