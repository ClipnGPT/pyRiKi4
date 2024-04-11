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

import psutil

import queue
import threading
import subprocess

import random

import numpy as np
import cv2

#print(os.path.dirname(__file__))
#print(os.path.basename(__file__))
#print(sys.version_info)



# インターフェース
qCtrl_control_player     = 'temp/control_player.txt'
qCtrl_control_self       = qCtrl_control_player



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

# フォント
qFONT_default = {'file':qPath_fonts + '_vision_font_ipaexg.ttf','offset':8}
qFONT_DSEG7   = {'file':qPath_fonts + 'DSEG7Classic-Bold.ttf','offset':8}



import _v6__qRiKi_key

config_file = '_v6__sub_player_key.json'

qRiKi_key = _v6__qRiKi_key.qRiKi_key_class()
res, dic = qRiKi_key.getCryptJson(config_file=config_file, auto_crypt=False, )
if (res == False):
    dic['_crypt_']             = 'none'
    dic['engine']              = 'ffplay'
    dic['path_winos']          = 'C:/Users/Public/'
    dic['path_macos']          = '/Users/Shared/'
    dic['path_linux']          = '/users/kondou/Documents/'
    dic['play_folder_00']      = 'BGV'
    dic['play_folder_01']      = '_m4v__Clip/Perfume'
    dic['play_folder_02']      = '_m4v__Clip/BABYMETAL'
    dic['play_folder_03']      = '_m4v__Clip/OneOkRock'
    dic['play_folder_04']      = '_m4v__Clip/きゃりーぱみゅぱみゅ'
    dic['play_folder_05']      = '_m4v__Clip/etc'
    dic['play_folder_06']      = '_m4v__Clip/SekaiNoOwari'
    dic['play_folder_07']      = 'BGM'
    dic['play_folder_08']      = '_m4v__Clip/Perfume'
    dic['play_folder_09']      = '_m4v__Clip/BABYMETAL'
    dic['play_volume']         = 100
    res = qRiKi_key.putCryptJson(config_file=config_file, put_dic=dic, )



def qFFplay(cn_s, runMode='debug', proc_id='player', screen=0, panel='0', file='', vol=100, order='normal', left=100, top=100, width=320, height=240, fps=5, overText1='', overText2='',
            limitSec=0, ):

    id = str(screen) + '-' + panel
    result = True

    #ffplay -i test_input.flv -volume 100 -window_title "test_input.flv" -noborder -autoexit -x 320 -y 240
    #ffplay -i test_input.flv -volume 100 -window_title "test_input.flv" -noborder -autoexit -fs
    #ffplay -f lavfi "amovie=test_sample.mp3,asplit[out0],showspectrum[out1]"
    #ffplay -f lavfi "amovie=test_sample.mp3,asplit[out0],showwaves[out1]"
    #ffplay -f lavfi "amovie=test_sample.mp3,asplit=3[out1][a][b]; [a]showwaves=s=320x100[waves]; [b]showspectrum=s=320x100[spectrum]; [waves][spectrum] vstack[out0]"

    #print(screen, panel, left, top, width, height, file, )

    # ファイル秒数取得
    if  (file[-4:].lower() != '.wav') \
    and (file[-4:].lower() != '.mp3') \
    and (file[-4:].lower() != '.m4a'):
        try:
            cap = cv2.VideoCapture(file)                            # 動画を読み込む
            video_frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)   # フレーム数を取得する
            video_fps = cap.get(cv2.CAP_PROP_FPS)                   # フレームレートを取得する
            video_len_sec = video_frame_count / video_fps
            #print(video_len_sec, file)
            if (video_len_sec > 0):
                if (limitSec == 0) or (video_len_sec < limitSec):
                    limitSec = video_len_sec
        except:
            pass

    vf = 'fps=' + str(fps)
    if (overText1 != '') or (overText2 != ''):
        #print(overText1,overText2)
        vf += ",drawtext=fontfile=" + qFONT_default['file'] + ":fontsize=256:fontcolor=white:x=0:y=0:text='" + overText1 + "'"

    qLog.log('info', proc_id, 'Play ' + file, )
    if (file[-4:].lower() == '.wav') \
    or (file[-4:].lower() == '.mp3') \
    or (file[-4:].lower() == '.m4a'):
            ffplay = subprocess.Popen(['ffplay', '-i', file, \
                                        '-volume', str(vol), \
                                        '-window_title', str(id), \
                                        '-noborder', '-autoexit', \
                                        '-left', str(left), '-top', str(top), \
                                        '-x', str(width), '-y', str(height), \
                                        '-loglevel', 'warning', \
                        ], )
                        #], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
    else:
        if (width != 0) or (height != 0):
            ffplay = subprocess.Popen(['ffplay', '-i', file, \
                                        '-vf', vf, \
                                        '-volume', str(vol), \
                                        '-window_title', str(id), \
                                        '-noborder', '-autoexit', \
                                        '-left', str(left), '-top', str(top), \
                                        '-x', str(width), '-y', str(height), \
                                        '-loglevel', 'warning', \
                        ], )
                        #], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
        else:
            #w, h = qGUI.size()
            l, t, w, h = qGUI.getScreenPosSize(screen=screen)
            ffplay = subprocess.Popen(['ffplay', '-i', file, \
                                        '-vf', vf, \
                                        '-volume', str(vol), \
                                        '-window_title', str(id), \
                                        '-noborder', '-autoexit', \
                                        #'-fs', \
                                        '-left', str(left), '-top', str(top), \
                                        '-x', str(w), '-y', str(h), \
                                        '-loglevel', 'warning', \
                        ], )
                        #], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

    time.sleep(1.00)

    # 最前面再生
    if (order == 'top'):
        res = qGUI.setForegroundWindow(winTitle=str(id), )

    if (file[-4:].lower() == '.wav') \
    or (file[-4:].lower() == '.mp3') \
    or (file[-4:].lower() == '.m4a') \
    or (file[-4:].lower() == '.mp4') \
    or (file[-4:].lower() == '.m4v') \
    or (file[-4:].lower() == '.mov'):
        if (int(limitSec) == 0):
            ffplay.wait()
        else:
            #ffplay.wait(timeout=int(limitSec))
            checkTime      = time.time()
            while (ffplay.poll() is None) and ((time.time() - checkTime) <= int(limitSec)):
                txts, txt = qFunc.txtsRead(qCtrl_control_self)
                if (txts != False):
                    if (txt == '_end_') or (txt == '_stop_'):
                        break
                time.sleep(0.50)

    else:
            time.sleep(1.00)
            #ffplay.wait()

    ffplay.terminate()
    ffplay = None

    return result



def panelPlay(cn_s, screen, panel, runMode, proc_id, path, vol, order, loop, overText1, overText2,
              limitSec, ):

    #print('★panelPlay', path)
    #qLog.log('info', proc_id, 'panelPlay ' + path, )

    #black_screen = 'off'
    #black_time   = None

    count = 0
    while (loop > 0):

        # --------------
        # ファイル指定実行
        # --------------
        if (os.path.isfile(path)):
            fn = path
            p  = panel

            fps = 15
            if (vol == 0):
                if (p=='0') or (p=='0-') or (p=='5'):
                    fps = 5
                else:
                    fps = 2

            if (fn[-4:].lower() == '.wav') \
            or (fn[-4:].lower() == '.mp3') \
            or (fn[-4:].lower() == '.m4a'):
                if (p=='0') or (p=='0-'):
                    p = '5+'

            # play
            #left, top, width, height = qGUI.getPanelPos(p, )
            left, top, width, height = qGUI.getScreenPanelPosSize(screen=screen, panel=p, )
            res = qFFplay(runMode, proc_id, screen, p, fn, vol, order, left, top, width, height, fps, overText1, overText2,
                         limitSec, )
            count += 1

            txts, txt = qFunc.txtsRead(qCtrl_control_self)
            if (txts != False):
                if (txt == '_end_') or (txt == '_stop_'):
                    loop = 0
                    break

            if (loop < 9):
                loop -= 1

        # --------------
        # フォルダ指定実行
        # --------------
        if (os.path.isdir(path)):
            files = glob.glob(path + '/*.*')
            random.shuffle(files)

            p = panel
            if (panel == '1397'):
                p = panel[(count % 4):(count % 4)+1] + '-'
            if (panel == '19'):
                p = panel[(count % 2):(count % 2)+1] + '-'
            if (panel == '28'):
                p = '82'[(count % 2):(count % 2)+1] + '-'
            if (panel == '37'):
                p = panel[(count % 2):(count % 2)+1] + '-'
            if (panel == '46'):
                p = '64'[(count % 2):(count % 2)+1] + '-'

            fps = 15
            if (vol == 0):
                if (p=='0') or (p=='0-') or (p=='5'):
                    fps = 5
                else:
                    fps = 2

            for fn in files:
                if (fn[-4:].lower() == '.wav') \
                or (fn[-4:].lower() == '.mp3') \
                or (fn[-4:].lower() == '.m4a'):
                    if (p=='0') or (p=='0-'):
                        p = '5+'

                # Wait! Pass!
                nowTime = datetime.datetime.now()
                nowYYMMDD = nowTime.strftime('%Y-%m-%d')
                nowHHMMSS = nowTime.strftime('%H:%M:%S')
                nowHHMM   = nowTime.strftime('%H:%M')
                nowYOUBI  = nowTime.strftime('%a')

                # 開始判断
                playFlag  = True
                limitSec2 = limitSec

                # play
                if (playFlag != True):
                    time.sleep(1.00)
                else:

                    # play
                    #left, top, width, height = qGUI.getPanelPos(p,)
                    left, top, width, height = qGUI.getScreenPanelPosSize(screen=screen, panel=p, )
                    res = qFFplay(cn_s, runMode, proc_id, screen, p, fn, vol, order, left, top, width, height, fps, overText1, overText2,
                                  limitSec2, )
                    count += 1

                txts, txt = qFunc.txtsRead(qCtrl_control_self)
                if (txts != False):
                    if (txt == '_end_') or (txt == '_stop_'):
                        loop = 0
                        break

        if (loop < 9):
            loop -= 1
            time.sleep(0.50)



class main_player:

    def __init__(self, name='thread', id='0', runMode='debug', waitSec=0, overPath='', overFolder='', overVolume='', screen=0, ):

        self.runMode   = runMode
        self.waitSec   = int(waitSec)
        self.overPath  = overPath
        self.overFolder= overFolder
        self.overVolume= overVolume
        self.screen    = int(screen)

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

        self.play_max  = 10
        self.play_proc = {}
        self.play_id   = {}
        self.play_path = {}
        for i in range(1, self.play_max+1):
            self.play_proc[i] = None
            self.play_id[i]   = None
            self.play_path[i] = None

        # 構成情報
        json_file = '_v6__sub_player_key.json'
        self.engine              = 'ffplay'
        self.path_winos          = 'C:/Users/Public/'
        self.path_macos          = '/Users/Shared/'
        self.path_linux          = '/users/kondou/Documents/'
        self.play_folder         = {}
        self.play_folder['00']   = 'BGV'
        self.play_folder['01']   = '_m4v__Clip/Perfume'
        self.play_folder['02']   = '_m4v__Clip/BABYMETAL'
        self.play_folder['03']   = '_m4v__Clip/OneOkRock'
        self.play_folder['04']   = '_m4v__Clip/きゃりーぱみゅぱみゅ'
        self.play_folder['05']   = '_m4v__Clip/etc'
        self.play_folder['06']   = '_m4v__Clip/SekaiNoOwari'
        self.play_folder['07']   = 'BGM'
        self.play_folder['08']   = '_m4v__Clip/Perfume'
        self.play_folder['09']   = '_m4v__Clip/BABYMETAL'
        self.play_volume         = 100
        res, json_dic = qRiKi_key.getCryptJson(config_file=json_file, auto_crypt=False, )
        if (res == True):
            self.engine              = json_dic['engine']
            self.path_winos          = json_dic['path_winos']
            self.path_macos          = json_dic['path_macos']
            self.path_linux          = json_dic['path_linux']
            self.play_folder['00']   = json_dic['play_folder_00']
            self.play_folder['01']   = json_dic['play_folder_01']
            self.play_folder['02']   = json_dic['play_folder_02']
            self.play_folder['03']   = json_dic['play_folder_03']
            self.play_folder['04']   = json_dic['play_folder_04']
            self.play_folder['05']   = json_dic['play_folder_05']
            self.play_folder['06']   = json_dic['play_folder_06']
            self.play_folder['07']   = json_dic['play_folder_07']
            self.play_folder['08']   = json_dic['play_folder_08']
            self.play_folder['09']   = json_dic['play_folder_09']
            self.play_volume         = json_dic['play_volume']

        if (self.overPath != ''):
            self.path_winos         = self.overPath
            self.path_macos         = self.overPath
            self.path_linux         = self.overPath

        if (self.overFolder != ''):
            self.play_folder['00']  = self.overFolder
            self.play_folder['01']  = self.overFolder
            self.play_folder['02']  = self.overFolder
            self.play_folder['03']  = self.overFolder
            self.play_folder['04']  = self.overFolder
            self.play_folder['05']  = self.overFolder
            self.play_folder['06']  = self.overFolder
            self.play_folder['07']  = self.overFolder
            self.play_folder['08']  = self.overFolder
            self.play_folder['09']  = self.overFolder

        if (self.overVolume != ''):
            self.play_volume        = self.overVolume

        self.path_play = {}
        for id in self.play_folder:
            if (os.name == 'nt'):
                self.path_play[id] = self.path_winos + self.play_folder[id]
            elif (qPLATFORM == 'darwin'):
                self.path_play[id] = self.path_macos + self.play_folder[id]
            else:
                self.path_play[id] = self.path_linux + self.play_folder[id]

        self.qCtrl_control_player = qCtrl_control_player
        self.qCtrl_control_self   = qCtrl_control_self

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

        txts, txt = qFunc.txtsRead(self.qCtrl_control_self)
        if (txts != False):
            if (txt == '_end_') or (txt == '_stop_'):
                qFunc.remove(self.qCtrl_control_self)

        if (self.waitSec > 0):
            qLog.log('info', self.proc_id, 'wait ' + str(self.waitSec) + 's (screen=' + str(self.screen) + ')', display=self.logDisp, )
            time.sleep(self.waitSec)

        # 待機ループ
        self.proc_step = '5'

        onece  = True

        last_alive = time.time()

        last_menu  = 0

        while (self.proc_step == '5'):
            self.proc_beat = time.time()

            # 終了確認
            control = ''
            txts, txt = qFunc.txtsRead(self.qCtrl_control_self)
            if (txts != False):
                qLog.log('info', self.proc_id, '' + str(txt))
                if (txt == '_end_'):
                    break

                if (txt == '_stop_'):
                    self.sub_proc(cn_s, '_stop_', )
                    time.sleep(5.00)

                qFunc.remove(self.qCtrl_control_self)
                control = txt

            # 停止要求確認
            if (self.breakFlag.is_set()):
                self.breakFlag.clear()
                self.proc_step = '9'
                break

            # 活動メッセージ
            if  ((time.time() - last_alive) > 30):
                qLog.log('debug', self.proc_id, 'alive', display=True, )
                last_alive = time.time()

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

            # レディー設定
            if (qFunc.statusCheck(self.fileRdy) == False):
                qFunc.statusSet(self.fileRdy, True)

            # ステータス応答
            if (inp_name.lower() == '_status_'):
                out_name  = inp_name
                out_value = '_ready_'
                cn_s.put([out_name, out_value])

            # 活動Ｑ検査
            if (os.path.exists(self.fileBsy)):
                self.sub_alive()

            # 選択アナウンス
            if (control.find('動画') >=0) and (control.find('メニュー') >=0):
                last_menu = time.time()
            if (control.lower() >= '01') and (control.lower() <= '09'):
                last_menu = 0

            if (last_menu != 0):
                if ((time.time() - last_menu) > 120):
                    if (onece == True):
                        onece = False

                        speechs = []
                        speechs.append({ 'text':'画面表示位置を指定して再生はいかがですか？', 'wait':0, })
                        qRiKi.speech(id='speech', speechs=speechs, lang='', )

            # 処理
            if (control != ''):
                self.sub_proc(cn_s, control, )

            # アイドリング
            slow = False
            if  (qFunc.statusCheck(qBusy_dev_cpu) == True):
                slow = True
            if  (qFunc.statusCheck(qBusy_dev_mic) == True):
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

            # レディー解除
            qFunc.statusSet(self.fileRdy, False)

            # 停止
            self.sub_proc(cn_s, '_stop_', )

            # ビジー解除
            qFunc.statusSet(self.fileBsy, False)
            if (str(self.id) == '0'):
                qFunc.statusSet(qBusy_d_play, False)

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



    # 処理
    def sub_proc(self, cn_s, proc_text, ):
        if (proc_text.find('リセット') >=0):
            #self.sub_stop(proc_text, )
            self.sub_stop('_stop_', )

        elif (proc_text.lower() == '_stop_'):
            #self.sub_stop(proc_text, )
            self.sub_stop('_stop_', )

        elif (proc_text.lower() == '_start_'):
            pass

        elif (proc_text.lower() == '_demo0-'):
            #self.sub_stop('_stop_', )
            self.sub_start(cn_s, proc_text, self.path_play['01'], panel='0' , vol=0  , order='normal', loop=1, )
            self.sub_start(cn_s, proc_text, self.path_play['01'], panel='0-', vol=int(self.play_volume), order='top', loop=1, )

        elif (proc_text.lower() == '_demo1397'):
            #self.sub_stop('_stop_', )
            self.sub_start(cn_s, proc_text, self.path_play['00'], panel='0'   , vol=0  , order='normal', loop=99, )
            self.sub_start(cn_s, proc_text, self.path_play['01'], panel='1397', vol=int(self.play_volume), order='top', loop=99, )

        elif (proc_text.lower() == '_demo1234'):
            #self.sub_stop('_stop_', )
            self.sub_start(cn_s, proc_text, self.path_play['05'], panel='0' , vol=int(self.play_volume), order='normal', loop=99, )
            self.sub_start(cn_s, proc_text, self.path_play['01'], panel='19', vol=0  , order='normal', loop=99, )
            self.sub_start(cn_s, proc_text, self.path_play['02'], panel='28', vol=0  , order='normal', loop=99, )
            self.sub_start(cn_s, proc_text, self.path_play['03'], panel='37', vol=0  , order='normal', loop=99, )
            self.sub_start(cn_s, proc_text, self.path_play['04'], panel='46', vol=0  , order='normal', loop=99, )

        elif ((proc_text.find('動画') >=0) and (proc_text.find('メニュー') >=0)) or (proc_text.lower() == '_test_'):
            #self.sub_stop('_stop_', )
            self.sub_start(cn_s, proc_text, self.path_play['00'], panel='0' , vol=0  , order='normal', loop=99, overText1='', )
            self.sub_start(cn_s, proc_text, self.path_play['01'], panel='1-', vol=0  , order='normal', loop=99, overText1='01', )
            self.sub_start(cn_s, proc_text, self.path_play['02'], panel='2-', vol=0  , order='normal', loop=99, overText1='02', )
            self.sub_start(cn_s, proc_text, self.path_play['03'], panel='3-', vol=0  , order='normal', loop=99, overText1='03', )
            self.sub_start(cn_s, proc_text, self.path_play['04'], panel='4-', vol=0  , order='normal', loop=99, overText1='04', )
            if (proc_text.find('動画') >=0) and (proc_text.find('メニュー') >=0):
                self.sub_start(cn_s, proc_text, self.path_play['05'], panel='5-', vol=0  , order='normal', loop=99, overText1='05', )
            if (proc_text.lower() == '_test_'):
                self.sub_start(cn_s, proc_text, self.path_play['05'], panel='5-', vol=int(self.play_volume), order='top', loop=99, overText1='05', )
            self.sub_start(cn_s, proc_text, self.path_play['06'], panel='6-', vol=0  , order='normal', loop=99, overText1='06', )
            self.sub_start(cn_s, proc_text, self.path_play['07'], panel='7-', vol=0  , order='normal', loop=99, overText1='07', )
            self.sub_start(cn_s, proc_text, self.path_play['08'], panel='8-', vol=0  , order='normal', loop=99, overText1='08', )
            self.sub_start(cn_s, proc_text, self.path_play['09'], panel='9-', vol=0  , order='normal', loop=99, overText1='09', )

        elif (proc_text.lower() >= '01') and (proc_text.lower() <= '09'):
            #self.sub_stop('_stop_', )
            self.sub_start(cn_s, proc_text, self.path_play[proc_text], panel='0-', vol=int(self.play_volume), order='top' , loop=99, )

        else:
            proc_path = qFunc.txtFilePath(proc_text)
            if (proc_path != False):
                #self.sub_stop('_stop_', )
                self.sub_start(cn_s, proc_text, proc_path, panel='0-', vol=int(self.play_volume), order='top', loop=1, )



    # 活動Ｑ検査
    def sub_alive(self, ):
        hit = -1
        for i in range(1, self.play_max+1):
            if (self.play_proc[i] is not None):
                #try:
                    if (not self.play_proc[i].is_alive()):
                        #self.play_proc[i].terminate()
                        del self.play_proc[i]
                        self.play_proc[i] = None
                        self.play_id[i]   = ''
                        self.play_path[i] = ''
                #except Exception as e:
                #        self.play_proc[i] = None
                #        self.play_id[i]   = ''
                #        self.play_path[i] = ''
            if (self.play_proc[i] is not None):
                hit = i
                break
        if (hit == -1):
            # ビジー解除
            qFunc.statusSet(self.fileBsy, False)
            if (str(self.id) == '0'):
                qFunc.statusSet(qBusy_d_play, False)
            return False
        else:
            # ビジー設定
            if (qFunc.statusCheck(self.fileBsy) == False):
                qFunc.statusSet(self.fileBsy, True)
                if (str(self.id) == '0'):
                    qFunc.statusSet(qBusy_d_play, True)
            return True



    # 開始
    def sub_start(self, cn_s, proc_text, proc_path, panel='0-', vol=100, order='normal', loop=1, overText1='', overText2='', ):

        # ログ
        qLog.log('info', self.proc_id, 'open ' + proc_path, display=True,)

        # 空きＱ検索
        hit = -1
        for i in range(1, self.play_max+1):
            if (self.play_proc[i] is not None):
                #try:
                    if (not self.play_proc[i].is_alive()):
                        #self.play_proc[i].terminate()
                        del self.play_proc[i]
                        self.play_proc[i] = None
                        self.play_id[i]   = ''
                        self.play_path[i] = ''
                #except Exception as e:
                #        self.play_proc[i] = None
                #        self.play_id[i]   = ''
                #        self.play_path[i] = ''
            if (self.play_proc[i] is None):
                hit = i
                break

        # オープン
        if (hit >= 0):

            # ビジー設定
            if (qFunc.statusCheck(self.fileBsy) == False):
                qFunc.statusSet(self.fileBsy, True)
                if (str(self.id) == '0'):
                    qFunc.statusSet(qBusy_d_play, True)

            limitSec        = 0

            i = hit
            self.play_id[i]     = panel
            self.play_path[i]   = proc_path
            self.play_proc[i]   = threading.Thread(target=panelPlay, args=(
                cn_s, self.screen, self.play_id[i], 
                self.runMode, self.proc_id, self.play_path[i], vol, order, loop, overText1, overText2,
                limitSec, 
                #), daemon=True, )
                ))
            self.play_proc[i].start()

            time.sleep(2.00)

    # 停止
    def sub_stop(self, proc_text, ):

        # リセット
        #qFunc.kill('ffplay', )
        qFunc.kill(self.engine, )

        # 全Ｑリセット
        for i in range(1, self.play_max+1):
            if (self.play_proc[i] is not None):
                try:
                    self.play_proc[i].terminate()
                    del self.play_proc[i]
                    self.play_proc[i] = None
                    self.play_id[i]   = ''
                    self.play_path[i] = ''
                except Exception as e:
                    self.play_proc[i] = None
                    self.play_id[i]   = ''
                    self.play_path[i] = ''

        # リセット
        #qFunc.kill('ffplay', )
        qFunc.kill(self.engine, )

        # ビジー解除
        self.sub_alive()



# シグナル処理
import signal
def signal_handler(signal_number, stack_frame):
    print(os.path.basename(__file__), 'accept signal =', signal_number)

#signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGINT,  signal.SIG_IGN)
signal.signal(signal.SIGTERM, signal.SIG_IGN)



runMode = 'debug'

overPath   = ''
#overPath   = 'C:/_共有/'
overFolder = ''
#overFolder = 'BGV/'
overVolume = ''



if __name__ == '__main__':
    main_name = 'player'
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

    # 初期設定
    if (len(sys.argv) >= 2):
        runMode    = str(sys.argv[1]).lower()

    if (True):

        txts, txt = qFunc.txtsRead(qCtrl_control_self)
        if (txts != False):
            if (txt == '_end_') or (txt == '_stop_'):
                qFunc.remove(qCtrl_control_self)

    # パラメータ

    if (True):

        if (len(sys.argv) >= 2):
            runMode    = str(sys.argv[1]).lower()
        if (len(sys.argv) >= 3):
            overPath   = str(sys.argv[2])
        if (len(sys.argv) >= 4):
            overFolder = str(sys.argv[3])
        if (len(sys.argv) >= 5):
            overVolume = str(sys.argv[4])

        qLog.log('info', main_id, 'runMode    = ' + str(runMode   ))
        qLog.log('info', main_id, 'overPath   = ' + str(overPath  ))
        qLog.log('info', main_id, 'overFolder = ' + str(overFolder))
        qLog.log('info', main_id, 'overVolume = ' + str(overVolume))

    # 起動

    if (True):

        qLog.log('info', main_id, 'start')

        main_core = {}

        main_start = time.time()
        onece      = True
        setting    = True
        last_check = time.time()

        cam_title = 'Check'
        cam_img   = None
        last_cam  = time.time()



    # 待機ループ

    while (True):

        # 終了確認
        txts, txt = qFunc.txtsRead(qCtrl_control_self)
        if (txts != False):
            if (txt == '_end_'):
                break

        # スクリーン設定
        if (setting == True) or ((time.time()-last_check)>5):
            last_check = time.time()
            change = qGUI.checkUpdateScreenInfo(update=True, )
            if (change == True) or (setting == True):
                setting = False
                qLog.log('info', main_id, 'Screen (re) Setting... ')

                # 停止
                qFunc.txtsWrite(qCtrl_control_self ,txts=['_stop_'], encoding='utf-8', exclusive=True, mode='w', )

                time.sleep(5.00)

                for m in range(len(main_core)):
                    try:
                        main_core[m].abort()
                        del main_core[m]
                    except:
                        pass
                main_core = {}

                qFunc.kill('ffplay', )

                # 起動
                s = 0
                id = '0'
                main_core[0] = main_player(main_name, id, runMode=runMode, waitSec=0, overPath=overPath, overFolder=overFolder, overVolume=overVolume, screen=s, )
                main_core[0].begin()
                
        # キュー取得
        for m in range(len(main_core)):
            main_core_get = main_core[m].get()
            inp_name  = main_core_get[0]
            inp_value = main_core_get[1]
            if (inp_name != ''):
                print(inp_name, inp_value,)

        # デバッグ
        if (runMode == 'debug'):

            # テスト開始
            if  ((time.time() - main_start) > 1):
                if (onece == True):
                    onece = False
                    #t = 'C:/Users/Public/_m4v__Clip/Perfume/Perfume_FLASH.m4v'
                    #t = 'C:/Users/Public/_m4v__Clip/Perfume'
                    #t = '_demo0-'   # base + center
                    #t = '_demo1397' # base + 1,3,9,7
                    #t = '_demo1234' # base + 1234,6789
                    t = '_test_'      # base + 1-9
                    qLog.log('debug', main_id, t, )
                    qFunc.txtsWrite(qCtrl_control_self ,txts=[t], encoding='utf-8', exclusive=True, mode='w', )

            # テスト終了
            if  ((time.time() - main_start) > 120):
                    qLog.log('debug', main_id, '_stop_', )
                    qFunc.txtsWrite(qCtrl_control_self ,txts=['_stop_'], encoding='utf-8', exclusive=True, mode='w', )
                    time.sleep(5.00)
                    qLog.log('debug', main_id, '_end_', )
                    qFunc.txtsWrite(qCtrl_control_self ,txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )

        # アイドリング
        slow = False
        if   (qFunc.statusCheck(qBusy_dev_cpu) == True):
            slow = True
        elif (qFunc.statusCheck(qBusy_dev_mic) == True):
            slow = True

        if (slow == True):
            time.sleep(1.00)
        else:
            time.sleep(0.50)

    # 終了

    if (True):

        qLog.log('info', main_id, 'terminate')

        for m in range(len(main_core)):
            main_core[m].abort()
            del main_core[m]
        main_core = {}

        qFunc.kill('ffplay', )

        qLog.log('info', main_id, 'bye!')

        sys.exit(0)


