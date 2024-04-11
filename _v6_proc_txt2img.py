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



# フォント
qFont_default = {'file':qPath_fonts + '_vision_font_ipaexg.ttf','offset':8}
qFont_status  = {'file':qPath_fonts + '_vision_font_ipag.ttf','offset':8}
qFont_zh = {'file':'C:/Windows/Fonts/msyh.ttc', 'offset':5}
qFont_ko = {'file':'C:/Windows/Fonts/batang.ttc', 'offset':10}



class proc_txt2img:

    def __init__(self, name='thread', id='0', runMode='debug', drawWidth='0', ):
        self.runMode   = runMode
        self.drawWidth = drawWidth

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
        self.flag_background = 'on'
        self.flag_blackwhite = 'black'

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

        # フォント
        font16_default  = ImageFont.truetype(qFont_default['file'], 16, encoding='unic')
        font16_defaulty =                    qFont_default['offset']
        font16_status   = ImageFont.truetype(qFont_status[ 'file'], 16, encoding='unic')
        font16_statusy  =                    qFont_status[ 'offset']
        font32_default  = ImageFont.truetype(qFont_default['file'], 32, encoding='unic')
        font32_defaulty =                    qFont_default['offset']
        font48_default  = ImageFont.truetype(qFont_default['file'], 48, encoding='unic')
        font48_defaulty =                    qFont_default['offset']
        if (os.path.exists(qFont_zh['file'])):
            font32_zh  = ImageFont.truetype(qFont_zh['file']     , 32, encoding='unic')
            font32_zhy =                    qFont_zh['offset']
        else:
            font32_zh  = ImageFont.truetype(qFont_default['file'], 32, encoding='unic')
            font32_zhy =                    qFont_default['offset']
        if (os.path.exists(qFont_ko['file'])):
            font32_ko  = ImageFont.truetype(qFont_ko['file']     , 32, encoding='unic')
            font32_koy =                    qFont_ko['offset']
        else:
            font32_ko  = ImageFont.truetype(qFont_default['file'], 32, encoding='unic')
            font32_koy =                    qFont_default['offset']

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

            # 表示連携
            elif (inp_name.lower() == '_flag_background_'):
                self.flag_background = inp_value
            elif (inp_name.lower() == '_flag_blackwhite_'):
                self.flag_blackwhite = inp_value

            # 処理
            elif (inp_name.lower() == '[txts]') \
              or (inp_name.lower() == '[status]') \
              or (inp_name.lower() == '[message_txts]'):

                # 実行カウンタ
                self.proc_last = time.time()
                self.proc_seq += 1
                if (self.proc_seq > 9999):
                    self.proc_seq = 1

                # ビジー設定
                if (qFunc.statusCheck(self.fileBsy) == False):
                    qFunc.statusSet(self.fileBsy, True)

                # 文字列確認
                texts = inp_value

                maxlen = 0
                for i in range(0, len(texts)):
                    if (texts[i][2:3] != ','):
                            if (qFunc.in_japanese(texts[i]) == True):
                                lenstr = len(texts[i]) * 2
                            else:
                                lenstr = len(texts[i])
                    else:
                        if  (texts[i][:3] == 'ja,') \
                        or  (texts[i][:3] == 'zh,') \
                        or  (texts[i][:3] == 'ko,'):
                            lenstr = len(texts[i]) * 2
                        else:
                            lenstr = len(texts[i])
                    if (maxlen < lenstr):
                        maxlen = lenstr

                # 描写キャンバス作成
                if (inp_name.lower() == '[status]'):
                    draw_width  = int(self.drawWidth)
                    draw_height = int(10 + (16 + 10) * len(texts))
                    if (draw_width == 0):
                        draw_width = 180
                if (inp_name.lower() == '[txts]'):
                    draw_width  = int(self.drawWidth)
                    draw_height = int(10 + (32 + 10) * len(texts))
                    if (draw_width == 0):
                        draw_width = int(50 + 16 * maxlen)
                if (inp_name.lower() == '[message_txts]'):
                    draw_width  = int(self.drawWidth)
                    draw_height = int(10 + (48 + 10) * len(texts))
                    if (draw_width == 0):
                        draw_width = int(100 + 24 * maxlen)

                if (self.flag_blackwhite != 'white'):
                    text_img  = Image.new('RGB', (draw_width, draw_height), (255,255,255))
                else:
                    text_img  = Image.new('RGB', (draw_width, draw_height), (  0,  0,  0))
                text_draw = ImageDraw.Draw(text_img)

                # 文字描写
                for i in range(0, len(texts)):

                    if (self.flag_blackwhite != 'white'):
                        txt_color = (  0,  0,  0)
                    else:
                        txt_color = (255,255,255)

                    if (inp_name.lower() == '[status]'):

                        if (texts[i].find('busy!'   )>=0) \
                        or (texts[i].find('slow!'   )>=0) \
                        or (texts[i].find('disable!')>=0) \
                        or (texts[i].find('rec!'    )>=0):
                            text_draw.rectangle((0, 5 + (16 + 10)*i, draw_width, (16 + 10)*(i+1)-1), fill=(0xff, 0x00, 0xff))
                            txt_color = (  0,  0,  0)
                        if (texts[i].find('active'  )>=0):
                            text_draw.rectangle((0, 5 + (16 + 10)*i, draw_width, (16 + 10)*(i+1)-1), fill=(0xff, 0xff, 0x00))
                            txt_color = (  0,  0,  0)
                        if (texts[i].find('ready'   )>=0):
                            text_draw.rectangle((0, 5 + (16 + 10)*i, draw_width, (16 + 10)*(i+1)-1), fill=(0x00, 0xff, 0x00))
                            txt_color = (  0,  0,  0)

                        text_draw.text((5, (16 + 10)*i + font16_statusy), texts[i], font=font16_status, fill=txt_color)

                    if (inp_name.lower() == '[txts]'):

                        if (texts[i][2:3] != ','):
                                text_draw.text((16, (32 + 10)*i + font32_defaulty), texts[i], font=font32_default, fill=txt_color)
                        else:
                            if   (texts[i][:3] == 'zh,'):
                                text_draw.text((16, (32 + 10)*i + font32_zhy), texts[i], font=font32_zh, fill=txt_color)
                            elif (texts[i][:3] == 'ko,'):
                                text_draw.text((16, (32 + 10)*i + font32_koy), texts[i], font=font32_ko, fill=txt_color)
                            else:
                                text_draw.text((16, (32 + 10)*i + font32_defaulty), texts[i], font=font32_default, fill=txt_color)

                    if (inp_name.lower() == '[message_txts]'):
                        text_draw.text((24, (48 + 10)*i + font48_defaulty), texts[i], font=font48_default, fill=txt_color)

                # 結果出力
                if (inp_name.lower() == '[status]'):
                    out_name  = '[status_img]'
                    out_value = np.asarray(text_img)
                    cn_s.put([out_name, out_value])
                if (inp_name.lower() == '[txts]'):
                    out_name  = '[txts_img]'
                    out_value = np.asarray(text_img)
                    cn_s.put([out_name, out_value])
                if (inp_name.lower() == '[message_txts]'):
                    out_name  = '[message_img]'
                    out_value = np.asarray(text_img)
                    cn_s.put([out_name, out_value])



            # ビジー解除
            if (cn_r.qsize() == 0):
                qFunc.statusSet(self.fileBsy, False)

            # アイドリング
            slow = False
            if (qFunc.statusCheck(qBusy_dev_cpu) == True):
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



    # テスト
    txt2img_thread = proc_txt2img('txt2img', '0', )
    txt2img_thread.begin()

    txt2img_thread.put(['[txts]', ['おはようございます']])
    resdata = txt2img_thread.checkGet()
    if (resdata[0] == '[txts_img]'):
        img = resdata[1].copy()
        cv2.namedWindow('Display',  1)
        cv2.imshow('Display', img )
        cv2.waitKey(1)
        time.sleep(5)

    txt2img_thread.put(['flag_blackwhite', 'white'])

    txt2img_thread.put(['[txts]', ['こんにちは', 'はじめまして']])
    resdata = txt2img_thread.checkGet()
    if (resdata[0] == '[txts_img]'):
        img = resdata[1].copy()
        cv2.namedWindow('Display',  1)
        cv2.imshow('Display', img )
        cv2.waitKey(1)
        time.sleep(5)

    time.sleep(1)
    txt2img_thread.abort()
    del txt2img_thread

    cv2.destroyAllWindows()



