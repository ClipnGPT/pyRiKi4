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



# インターフェース
qCtrl_control_desktop    = 'temp/control_desktop.txt'

# 出力インターフェース
qCtrl_result_movie        = 'temp/result_movie.mp4'
qCtrl_result_recorder     = 'temp/result_recorder.txt'



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

config_file = '_v6_proc_recorder_key.json'

qRiKi_key = _v6__qRiKi_key.qRiKi_key_class()
res, dic = qRiKi_key.getCryptJson(config_file=config_file, auto_crypt=False, )
if (res == False):
    dic['_crypt_'] = 'none'
    dic['dspInfo'] = 'yes'
    dic['inpFPS']  = '10'
    dic['outFPS']  = '10'
    dic['mov2jpg'] = 'yes'
    res = qRiKi_key.putCryptJson(config_file=config_file, put_dic=dic, )



#def check_sox():
#    result = True
#
#    try:
#        sox = subprocess.Popen(['sox', '-q', '-d', '-r', '16000', '-b', '16', '-c', '1',
#                qPath_work + 'check_sox.wav', 'trim', '0', '0.5',
#                ], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
#        sox.wait()
#        sox.terminate()
#        sox = None
#    except Exception as e:
#        return False
#    
#    return result

def dshow_dev():
    cam = []
    mic = []

    if (os.name == 'nt'):

        ffmpeg = subprocess.Popen(['ffmpeg', '-y',
	            '-threads', '2',
	            '-f', 'dshow',
	            '-list_devices', 'true',
	            '-i', 'nul',
	            ], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

        flag = ''
        checkTime = time.time()
        while ((time.time() - checkTime) < 2):
            # バッファから1行読み込む.
            line = ffmpeg.stderr.readline()
            # バッファが空 + プロセス終了.
            if (not line) and (ffmpeg.poll() is not None):
                break
            # テキスト
            txt = line.decode('utf-8')
            if   (txt.find('DirectShow video devices') >=0):
                flag = 'cam'
            elif (txt.find('DirectShow audio devices') >=0):
                flag = 'mic'
            elif (flag == 'cam') and (txt.find(']  "') >=0):
                st = txt.find(']  "') + 4
                en = txt[st:].find('"')
                cam.append(txt[st:st+en])
                #print('cam:', txt[st:st+en])
            elif (flag == 'mic') and (txt.find(']  "') >=0):
                st = txt.find(']  "') + 4
                en = txt[st:].find('"')
                mic.append(txt[st:st+en])
                #print('mic:', txt[st:st+en])

        ffmpeg.terminate()
        ffmpeg = None

    return cam, mic



def movie2jpg(proc_id, batch_index, index=0, dev='desktop', 
                inpPath='', inpNamev='',
                outPath='', wrkPath='', sfps=1, scene=0.1, ):

    # パラメータ
    inpFilev = inpPath + inpNamev
    if (outPath == ''):
        outPath = qPath_rec
    if (wrkPath == ''):
        wrkPath = qPath_work + 'movie2jpeg' + '{:02}'.format(index) + '/'
    inpTime = inpNamev[:15]
    inpText = inpNamev[15:-4]

    # ファイルに日時
    dt1 = None
    f = inpNamev
    yyyy = int(f[:4])
    mm   = int(f[4:6])
    dd   = int(f[6:8])
    h    = int(f[9:11])
    m    = int(f[11:13])
    s    = int(f[13:15])
    dt1=datetime.datetime(yyyy,mm,dd,h,m,s,0)

    result = False

    if (True):

        try:

            # 作業ディレクトリ
            qFunc.makeDirs(wrkPath, remove=True, )

            # 動画処理
            ffmpeg = subprocess.Popen(['ffmpeg', '-y',
                '-threads', '2',
                '-i', inpFilev,
                '-ss', '0', '-t', '0.2', '-r', '10',
                '-qmin', '1', '-q', '1',
                wrkPath + '%04d.jpg',
                '-loglevel', 'warning',
                #], )
                ], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

            #logb, errb = ffmpeg.communicate()
            ffmpeg.wait()
            ffmpeg.terminate()
            ffmpeg = None

            stamp = dt1.strftime('%Y%m%d.%H%M%S.000000')

            # コピー
            seq4 = '0001'
            f0 =  wrkPath + seq4 + '.jpg'
            if (os.path.exists(f0)):
                if (inpText == ''):
                    f1 =  wrkPath + stamp[:-3] + '.jpg'
                    f2 =  outPath + stamp[:-3] + '.jpg'
                else:
                    f1 =  wrkPath + '_' + stamp[:-3] + inpText + '.jpg'
                    f2 =  outPath + '_' + stamp[:-3] + inpText + '.jpg'
                os.rename(f0, f1)
                qFunc.copy(f1, f2)
                os.remove(f1)

                if (result == False):
                    result = []
                result.append(f2)

        except Exception as e:
            pass

    if (inpText.find('録画-') < 0):
    #if (True):

        jpgok = False

        # 動画処理
        if (scene is None):
                try:
                    qFunc.makeDirs(wrkPath, remove=True, )

                    ffmpeg = subprocess.Popen(['ffmpeg', '-y',
                        '-threads', '2',
                        '-i', inpFilev,
                        '-filter:v', 'fps=fps=' + str(sfps) + ':round=down,showinfo',
                        wrkPath + '%04d.jpg',
                        #'-loglevel', 'warning',
                        ], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                    logb, errb = ffmpeg.communicate()
                    ffmpeg.wait()
                    ffmpeg.terminate()
                    ffmpeg = None

                    if (os.path.getsize(wrkPath + '0001.jpg') > 0):
                        jpgok = True
                except Exception as e:
                    pass

        else:

            if (jpgok == False):

                try:
                    qFunc.makeDirs(wrkPath, remove=True, )

                    # software encoder,
                    ffmpeg = subprocess.Popen(['ffmpeg', '-y',
                        '-threads', '2',
                        '-i', inpFilev,
                        '-filter:v', 'select=gt(scene\,' + str(scene) + '),scale=0:0,showinfo',
                        '-vsync', 'vfr',
                        wrkPath + '%04d.jpg',
                        #'-loglevel', 'warning',
                        ], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                    logb, errb = ffmpeg.communicate()
                    ffmpeg.wait()
                    ffmpeg.terminate()
                    ffmpeg = None
                    if (os.path.getsize(wrkPath + '0001.jpg') > 0):
                        jpgok = True
                except Exception as e:
                    pass

        if (jpgok == True):

            #log = logb.decode()
            log = errb.decode()
            txts = log.split('\n')
            for txt in txts:
                #print(txt)

                if (txt.find('Parsed_showinfo')>0) and (txt.find('] n:')>0):
                    # n, pts_time
                    n = ''
                    pts_time = ''
                    x_n        = txt.find(' n:')
                    x_pts      = txt.find(' pts:')
                    x_pts_time = txt.find(' pts_time:')
                    x_pos      = txt.find(' pos:')
                    if (x_n != 0) and (x_pts != 0):
                        n = txt[x_n+3:x_pts].strip()
                    if (x_pts_time != 0) and (x_pos != 0):
                        pts_time = txt[x_pts_time+10:x_pos].strip()

                    if (n == '') or (pts_time == ''):
                        #print(txt)
                        pass
                    else:
                        #print(n,pts_time)

                        # s => hhmmss
                        dt2=datetime.timedelta(seconds=float(pts_time))
                        dtx=dt1+dt2
                        stamp = dtx.strftime('%Y%m%d.%H%M%S.%f')
                        #print(stamp[:-7])

                        # コピー
                        seq4 = '{:04}'.format(int(n) + 1)
                        f0 =  wrkPath + seq4 + '.jpg'
                        if (os.path.exists(f0)):
                            if (inpText == ''):
                                f1 =  wrkPath + stamp[:-3] + '.jpg'
                                f2 =  outPath + stamp[:-3] + '.jpg'
                            else:
                                f1 =  wrkPath + '_' + stamp[:-3] + inpText + '.jpg'
                                f2 =  outPath + '_' + stamp[:-3] + inpText + '.jpg'
                            os.rename(f0, f1)
                            qFunc.copy(f1, f2)
                            os.remove(f1)

                            if (result == False):
                                result = []
                            result.append(f2)

    return result

def movie2mp4(proc_id, batch_index, index=0, dev='desktop', 
                inpPath='', inpNamev='', inpNamea='', 
                outPath='', outFPS='10', ):

    # パラメータ
    inpFilev = inpPath + inpNamev
    inpFilea = inpPath + inpNamea
    if (inpNamea == ''):
        inpFilea = ''
    if (outPath == ''):
        outPath = qPath_rec
    inpTime = inpNamev[:15]
    inpText = inpNamev[15:-4]
    if (inpText == ''):
        outFilev = outPath + inpTime + '.___' + '.mp4'
        outFilea = outPath + inpTime + '.___' + '.mp3'
    else:
        outFilev = outPath + '_' + inpTime + '.___' + inpText + '.mp4'
        outFilea = outPath + '_' + inpTime + '.___' + inpText + '.mp3'
    if (inpNamea == ''):
        outFilea = ''

    mp4ok = False
    mp3ok = False

    # デスクトップ以外はコピー（音捨てる）
    if (mp4ok == False) and (dev != 'desktop'):
        if (inpFilev[-4:] == outFilev[-4:]):
            qLog.log('warning', proc_id, 'thread ' + str(batch_index) + ' : copy mp4 → mp4', )
            qFunc.copy(inpFilev, outFilev)
            mp4ok = True
            return [outFilev]

    # 変換処理
    qLog.log('warning', proc_id, 'thread ' + str(batch_index) + ' : encode mp4,wav → mp4', )
    return qFFmpeg.encodemp4mp3(inp_filev=inpFilev, inp_filea=inpFilea, rate=outFPS, 
                                out_filev=outFilev, out_filea=outFilea,)



def movie_proc(runMode, proc_id, batch_index, index, dev, 
                rec_filev, rec_namev, rec_filea, rec_namea, 
                outFPS, mov2jpg, dspInfo, thread_wait, cn_s, ):

    # ログ
    qLog.log('info', proc_id, 'thread ' + str(batch_index) + ' : begin, wait=' + str(thread_wait), )

    # 実行待機
    if (thread_wait != 0):
        time.sleep(thread_wait)

    nowTime  = datetime.datetime.now()
    yyyymmdd = nowTime.strftime('%Y%m%d')

    # ログ
    qLog.log('info', proc_id, 'thread ' + str(batch_index) + ' : start', )

    # 動画変換
    res = movie2mp4(proc_id, batch_index, index=index, dev=dev,
                inpPath=qPath_work, inpNamev=rec_namev, inpNamea=rec_namea, 
                outPath=qPath_rec, outFPS=outFPS, )
    if (res != False):
        mp4file = ''
        for f in res:
            outFile = f.replace(qPath_rec, '')
            qFunc.copy(f, qPath_d_movie  + outFile)
            if (runMode != 'assistant'):
                qFunc.copy(f, qPath_d_upload + outFile)
            qFunc.copy(f, qCtrl_result_movie)
            if (qPath_videos != ''):
                folder = qPath_videos + yyyymmdd + '/'
                qFunc.makeDirs(folder)
                qFunc.copy(f, folder + outFile)
            if (outFile[-4:] == '.mp4'):
                mp4file = outFile

            # ログ
            if (outFile[-4:] == '.mp4'):
                qLog.log('debug', proc_id, 'thread ' + str(batch_index) + ' : ' + rec_namev + ' → ' + outFile, )
            if (outFile[-4:] == '.mp3'):
                qLog.log('debug', proc_id, 'thread ' + str(batch_index) + ' : ' + rec_namea + ' → ' + outFile, )

        if (mp4file != ''):
            qFunc.txtsWrite(qCtrl_result_recorder, txts=[mp4file], encoding='utf-8', exclusive=True, mode='w', )
        else:
            qFunc.txtsWrite(qCtrl_result_recorder, txts=['_mp4?_'], encoding='utf-8', exclusive=True, mode='w', )

    # サムネイル抽出
    if (mov2jpg.lower() == 'yes'):
        wrkPath = qPath_work + 'movie2jpeg' + '{:02}'.format(index) + '/'
        res = movie2jpg(proc_id, batch_index, index=index, dev=dev,
                    inpPath=qPath_work, inpNamev=rec_namev, 
                    outPath=qPath_rec, wrkPath=wrkPath, sfps=1, scene=0.1, )
        if (res != False):
            for f in res:
                outFile = f.replace(qPath_rec, '')
                qFunc.copy(f, qPath_d_movie  + outFile)
                if (runMode != 'assistant'):
                    qFunc.copy(f, qPath_d_upload + outFile)
                if (qPath_videos != ''):
                    folder = qPath_videos + yyyymmdd + '/'
                    qFunc.makeDirs(folder)
                    qFunc.copy(f, folder + outFile)

                # ログ
                qLog.log('debug', proc_id, 'thread ' + str(batch_index) + ' : ' + rec_namev + ' → ' + outFile, )

    # ワーク削除
    if (rec_filev != ''):
        qFunc.remove(rec_filev)
    if (rec_filea != ''):
        qFunc.remove(rec_filea)

    # ログ
    qLog.log('info', proc_id, 'thread ' + str(batch_index) + ' : complete', )

    # ガイド表示
    if (dspInfo.lower() == 'yes'):
        cn_s.put(['_guide_', 'rec ok (ch=' + str(index) + ') ' + dev])



class proc_recorder:

    def __init__(self, name='thread', id='0', runMode='debug', ):
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

        # 変数設定
        self.rec_max    = 10
        self.rec_text   = {}
        self.rec_title  = {}
        self.rec_dev    = {}
        self.rec_ffmpeg = {}
        self.rec_sox    = {}
        self.rec_start  = {}
        self.rec_limit  = {}
        self.rec_filev  = {}
        self.rec_filea  = {}
        for i in range(1, self.rec_max+1):
            self.rec_text[i]   = ''
            self.rec_title[i]  = ''
            self.rec_dev[i]    = ''
            self.rec_ffmpeg[i] = None
            self.rec_sox[i]    = None
            self.rec_start[i]  = time.time()
            self.rec_limit[i]  = None
            self.rec_filev[i]  = ''
            self.rec_filea[i]  = ''
        self.batch_max    = self.rec_max
        self.batch_index  = 0
        self.batch_thread = {}
        for i in range(self.batch_max):
            self.batch_thread[i] = None

        json_file = '_v6_proc_recorder_key.json'
        self.dspInfo = 'yes'
        self.inpFPS  = '10'
        self.outFPS  = '10'
        self.mov2jpg = 'yes'
        res, json_dic = qRiKi_key.getCryptJson(config_file=json_file, auto_crypt=False, )
        if (res == True):
            self.dspInfo = json_dic['dspInfo']
            self.inpFPS  = json_dic['inpFPS']
            self.outFPS  = json_dic['outFPS']
            self.mov2jpg = json_dic['mov2jpg']
        qLog.log('info', self.proc_id, 'dspInfo = ' + str(self.dspInfo), display=self.logDisp, )
        qLog.log('info', self.proc_id, 'inpFPS  = ' + str(self.inpFPS ), display=self.logDisp, )
        qLog.log('info', self.proc_id, 'outFPS  = ' + str(self.outFPS ), display=self.logDisp, )
        qLog.log('info', self.proc_id, 'mov2jpg = ' + str(self.mov2jpg), display=self.logDisp, )

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

    def abort(self, waitMax=20, ):
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

            # 制限時間、自動停止
            for i in range(1, self.rec_max+1):
                if (self.rec_limit[i] is not None):
                    if (time.time() > self.rec_limit[i]):
                        self.rec_limit[i] = None
                        
                        # 記録ストップ
                        if (self.rec_ffmpeg[i] is not None):

                            # 停止
                            self.sub_stop(i, '_stop_', 0, cn_s, )

            # 一定時間（5分毎）、自動リスタート
            for i in range(1, self.rec_max+1):
                if (self.rec_ffmpeg[i] is not None):
                    if (self.rec_dev[i] == 'desktop'):
                        text  = self.rec_text[i]
                        title = self.rec_title[i]
                        dev   = self.rec_dev[i]

                        if (self.runMode != 'debug'):
                            if  (title.find('録画') < 0):
                                # 記録は5分間隔
                                limit_sec = 60 * 5
                            else:
                                # 録画は10分間隔
                                limit_sec = 60 * 10
                        else:
                            limit_sec = 60 * 1

                        if ((time.time() - self.rec_start[i]) > limit_sec):

                            if  (title.find('録画') < 0):

                                # 記録リスタート
                                self.sub_start(index=0, proc_text='_rec_restart_', proc_title=title, dev=dev, cn_s=cn_s, )

                                # 記録ストップ
                                self.sub_stop(i, '_rec_stop_', 30, cn_s=cn_s, )

                            else:
                                # 全録画ストップ・録画開始
                                qLog.log('critical', self.proc_id, '録画終了', display=True,)

                                # 記録ストップ
                                self.sub_stop(i, '_rec_stop_', 60, cn_s=cn_s, )

                                count = 0
                                for x in range(1, self.rec_max+1):
                                    if (x != i):
                                        if (self.rec_ffmpeg[x] is not None):
                                            if (self.runMode != 'debug'):
                                                self.sub_stop(x, '_rec_stop_', 30 + (count*10), cn_s=cn_s, )
                                            else:
                                                self.sub_stop(x, '_rec_stop_', 30 + (count*10), cn_s=cn_s, )
                                            count += 1
                                self.sub_proc(proc_text='録画開始', cn_s=cn_s, )
                                break

            # ステータス応答
            if (inp_name.lower() == '_status_'):
                out_name  = inp_name
                out_value = '_ready_'
                cn_s.put([out_name, out_value])

            # 処理
            elif (inp_name.lower() != ''):
                self.sub_proc(inp_value, cn_s, )

            # アイドリング
            slow = False
            if  (qFunc.statusCheck(qBusy_dev_cpu) == True):
                slow = True
            if  (qFunc.statusCheck(qBusy_dev_scn) == True) \
            and (qFunc.statusCheck(qBusy_dev_dsp) == True):
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

            # 記録終了
            self.sub_proc('記録終了', cn_s, )
            qFunc.statusWait_false(self.fileBsy, 15)

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



    # 処理
    def sub_proc(self, proc_text, cn_s, ):

        if (proc_text.find('リセット') >=0):

            # 全記録ストップ
            for i in range(1, self.rec_max+1):
                if (self.rec_ffmpeg[i] is not None):
                    # 停止
                    self.sub_stop(i, '_stop_', 0, cn_s=cn_s, )


        elif (proc_text.lower() == '_rec_stop_') \
          or (proc_text.find('記録') >=0) and (proc_text.find('停止') >=0) \
          or (proc_text.find('記録') >=0) and (proc_text.find('終了') >=0) \
          or (proc_text.find('録画') >=0) and (proc_text.find('停止') >=0) \
          or (proc_text.find('録画') >=0) and (proc_text.find('終了') >=0):

            # 全記録ストップ
            for i in range(1, self.rec_max+1):
                if (self.rec_ffmpeg[i] is not None):
                    # 停止
                    self.sub_stop(i, '_stop_', 0, cn_s=cn_s, )

        elif (proc_text.find('録画') >=0):
            # デバイス名取得
            cam, mic = dshow_dev()
            # デスクトップ録画スタート
            cam_dev = 'desktop'
            title = qFunc.txt2filetxt('録画-' + cam_dev)
            self.sub_start(index=0, proc_text=proc_text, proc_title=title, dev=cam_dev, cn_s=cn_s, )
            # カメラ録画スタート
            for cam_dev in cam:
                title = qFunc.txt2filetxt('録画-' + cam_dev)
                self.sub_start(index=0, proc_text=proc_text, proc_title=title, dev=cam_dev, cn_s=cn_s, )

        elif (proc_text.lower() == '_rec_start_') \
          or (proc_text.find('記録') >=0):
            # デスクトップ記録スタート
            self.sub_start(index=0, proc_text=proc_text, proc_title='', dev='desktop', cn_s=cn_s, )



    # 記録開始
    def sub_start(self, index=0, proc_text='', proc_title='', dev='desktop', cn_s=None, ):
        if (proc_title == ''):
            proc_title = proc_text

        # インターフェース
        qFunc.remove(qCtrl_result_movie     )
        qFunc.remove(qCtrl_result_recorder  )

        # いちばん古い録画 -> index
        if (index == 0):
            min_start = time.time()
            min_index = 0
            max_start = 0
            max_index = 0
            for i in range(1, self.rec_max+1):
                if (self.rec_ffmpeg[i] is None):
                    if (index == 0):
                        index = i
                    if (self.rec_start[i] < min_start):
                        min_start = self.rec_start[i]
                        min_index = i
                        index = i # SET
                    if (self.rec_start[i] > max_start):
                        max_start = self.rec_start[i]
                        max_index = i

        # 開始処理
        if (index != 0):

            # ビジー設定
            if (qFunc.statusCheck(self.fileBsy) == False):
                qFunc.statusSet(self.fileBsy, True)
                if (str(self.id) == '0'):
                    qFunc.statusSet(qBusy_d_rec, True)

            # メッセージ　記録＋開始　または　録画
            if ((proc_text.lower() == '_rec_start_') \
             or (proc_text.find('記録') >=0)) \
            and (proc_text.find('開始') >=0) \
            and (dev == 'desktop'):
                speechs = []
                speechs.append({ 'text':'記録を開始します。', 'wait':0, })
                qRiKi.speech(id=self.proc_id, speechs=speechs, lang='', )

            elif (proc_text.find('録画') >=0) \
            and  (proc_text.find('開始') >=0) \
            and  (dev == 'desktop'):
                speechs = []
                speechs.append({ 'text':'録画を開始します。', 'wait':0, })
                qRiKi.speech(id=self.proc_id, speechs=speechs, lang='', )

            elif (proc_text.lower() == '_rec_restart_') \
            and (dev == 'desktop'):
                speechs = []
                speechs.append({ 'text':'記録は継続しています。', 'wait':0, })
                qRiKi.speech(id=self.proc_id, speechs=speechs, lang='', )

            if  (proc_text.lower() == '_rec_start_') \
             or (proc_text.lower() == '_rec_restart_') \
             or (proc_text.find('記録') >=0) \
             or (proc_text.find('録画') >=0):

                # デバイス名取得
                cam, mic = dshow_dev()

                # soxのチェック
                #sox_enable = check_sox()

                nowTime    = datetime.datetime.now()
                stamp      = nowTime.strftime('%Y%m%d.%H%M%S')

                # 連続録画
                if (proc_text.lower() == '_rec_start_') \
                or (proc_text.lower() == '_rec_restart_') \
                or (proc_text.find('開始') >=0):
                    self.rec_text[index]  = proc_text
                    self.rec_dev[index]   = dev
                    self.rec_start[index] = time.time()
                    self.rec_limit[index] = None

                    if  (proc_title.find('録画') < 0):
                        self.rec_title[index] = ''
                        self.rec_filev[index] = qPath_work + stamp + '.mp4'
                        self.rec_filea[index] = ''
                        #if (len(mic) > 0) and (sox_enable == True):
                        self.rec_filea[index] = qPath_work + stamp + '.wav'
                    else:
                        title = qFunc.txt2filetxt(proc_title)
                        self.rec_title[index] = title
                        self.rec_filev[index] = qPath_work + stamp + '.' + proc_title + '.mp4'
                        self.rec_filea[index] = ''
                        #if (len(mic) > 0) and (sox_enable == True):
                        self.rec_filea[index] = qPath_work + stamp + '.' + proc_title + '.wav'

                # 一時録画
                else:
                    self.rec_text[index]  = proc_text
                    title = qFunc.txt2filetxt(proc_title)
                    self.rec_title[index] = title
                    self.rec_dev[index]   = dev
                    self.rec_start[index] = time.time()
                    if (self.runMode != 'debug'):
                        self.rec_limit[index] = time.time() + 60
                    else:
                        self.rec_limit[index] = time.time() + 15
                    self.rec_filev[index] = qPath_work + stamp + '.' + proc_title + '.mp4'
                    self.rec_filea[index] = ''
                    #if (len(mic) > 0) and (sox_enable == True):
                    self.rec_filea[index] = qPath_work + stamp + '.' + proc_title + '.wav'

                # ログ
                qLog.log('critical', self.proc_id, self.rec_text[index] + ', ' + self.rec_title[index], display=True,)

                # 記録開始
                rec_filev = self.rec_filev[index]
                rec_filea = self.rec_filea[index]
                ffmpeg, sox, rec_filev, rec_filea = qFFmpeg.rec_start(dev=dev, rate=self.inpFPS, 
                                                                        out_filev=rec_filev, out_filea=rec_filea,
                                                                        retry_max=3, retry_wait=5.00,)
                if (ffmpeg is not None):
                    self.rec_ffmpeg[index] = ffmpeg
                    self.rec_sox[index]    = sox
                    self.rec_filev[index]  = rec_filev 
                    self.rec_filea[index]  = rec_filea

                    rec_namev = self.rec_filev[index].replace(qPath_work, '')
                    rec_namea = self.rec_filea[index].replace(qPath_work, '')

                    # ログ
                    qLog.log('info', self.proc_id, '' + rec_namev + ' rec start (ch=' + str(index) + ') ' + dev, display=True,)
                    if (self.rec_filea[index] != ''):
                        qLog.log('info', self.proc_id, '' + rec_namea + ' rec start (ch=' + str(index) + ') ' + dev, display=True,)

                    # ガイド表示
                    if (self.dspInfo.lower() == 'yes'):
                        cn_s.put(['_guide_', 'rec start (ch=' + str(index) + ') ' + dev])



    # 記録停止
    def sub_stop(self, index, proc_text, thread_wait, cn_s, ):

        # index
        if (index == 0):
            min_start = time.time()
            min_index = 0
            max_start = 0
            max_index = 0
            for i in range(1, self.rec_max+1):
                if (self.rec_ffmpeg[i] is not None):
                    if (self.rec_start[i] < min_start):
                        min_start = self.rec_start[i]
                        min_index = i
                    if (self.rec_start[i] > max_start):
                        max_start = self.rec_start[i]
                        max_index = i
            if (min_index != 0):
                index = min_index

        # 停止処理
        rec_filev = ''
        rec_filea = ''
        rec_namev = ''
        rec_namea = ''
        if (index != 0):

            # ログ
            qLog.log('critical', self.proc_id, proc_text + ', ' + self.rec_title[index], display=True,)

            # 記録停止
            ffmpeg = self.rec_ffmpeg[index]
            sox    = self.rec_sox[index]
            qFFmpeg.rec_stop(ffmpeg, sox,)
            self.rec_ffmpeg[index] = None
            self.rec_sox[index]    = None

            # ログ
            dev = self.rec_dev[index]
            rec_filev = self.rec_filev[index]
            rec_filea = self.rec_filea[index]
            rec_namev = rec_filev.replace(qPath_work, '')
            rec_namea = rec_filea.replace(qPath_work, '')
            if (os.path.exists(rec_filev)):
                    qLog.log('info', self.proc_id, '' + rec_namev + ' rec stop  (ch=' + str(index) + ') ' + dev, display=True,)

                    # ガイド表示
                    #if (self.dspInfo.lower() == 'yes'):
                    #    cn_s.put(['_guide_', 'rec ok (ch=' + str(index) + ') !'])

            else:
                    qLog.log('error', self.proc_id, '' + rec_namev + ' rec err   (ch=' + str(index) + ') ' + dev, display=True,)
                    rec_filev = ''
                    rec_namev = ''
                    rec_filea = ''
                    rec_namea = ''

                    # ガイド表示
                    if (self.dspInfo.lower() == 'yes'):
                        cn_s.put(['_guide_', 'rec error (ch=' + str(index) + ') '])

            if (rec_namea != ''):
                if (os.path.exists(rec_filea)):
                    qLog.log('info', self.proc_id, '' + rec_namea + ' rec stop  (ch=' + str(index) + ') ' + dev, display=True,)
                else:
                    rec_filea = ''
                    rec_namea = ''

        # 後処理
        if (rec_filev != ''):
            self.batch_index = (self.batch_index + 1) % self.batch_max

            if (thread_wait != 0):

                # threading
                self.batch_thread[self.batch_index] = threading.Thread(target=movie_proc, args=(
                    self.runMode, self.proc_id, self.batch_index, index, dev,
                    rec_filev, rec_namev, rec_filea, rec_namea,
                    self.outFPS, self.mov2jpg, self.dspInfo, thread_wait, cn_s,
                    ), daemon=True, )
                self.batch_thread[self.batch_index].start()

            else:
                movie_proc(
                    self.runMode, self.proc_id, self.batch_index, index, dev,
                    rec_filev, rec_namev, rec_filea, rec_namea,
                    self.outFPS, self.mov2jpg, self.dspInfo, thread_wait, cn_s,
                    )

        # いちばん古い録画 -> index
        index = 0
        if (index == 0):
            min_start = time.time()
            min_index = 0
            max_start = 0
            max_index = 0
            for i in range(1, self.rec_max+1):
                if (self.rec_ffmpeg[i] is not None):
                    if (self.rec_start[i] < min_start):
                        min_start = self.rec_start[i]
                        min_index = i
                    if (self.rec_start[i] > max_start):
                        max_start = self.rec_start[i]
                        max_index = i
            if (min_index != 0):
                index = min_index

        # 録画中がなければリセット
        if (index == 0):
            #qFunc.kill('ffmpeg')

            # メッセージ
            speechs = []
            speechs.append({ 'text':'記録を終了しました。', 'wait':0, })
            qRiKi.speech(id=self.proc_id, speechs=speechs, lang='', )

            # ビジー解除
            qFunc.statusSet(self.fileBsy, False)
            if (str(self.id) == '0'):
                qFunc.statusSet(qBusy_d_rec, False)



# シグナル処理
import signal
def signal_handler(signal_number, stack_frame):
    print(os.path.basename(__file__), 'accept signal =', signal_number)

#signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGINT,  signal.SIG_IGN)
signal.signal(signal.SIGTERM, signal.SIG_IGN)



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

    # SOX 状況
    #res = check_sox()
    #print('sox =', res)

    # SOX 状況
    if (os.name == 'nt'):
        cam, mic = dshow_dev()
        print('cam =', cam)
        print('mic =', mic)

    # 開始
    recorder_thread = proc_recorder('recorder', '0', runMode, )
    recorder_thread.begin()



    # テスト実行
    if (len(sys.argv) < 2):

        recorder_thread.put(['control', '録画開始'])

        time.sleep(130)

        recorder_thread.put(['control', '録画終了'])

        time.sleep(60)

        recorder_thread.put(['control', '記録開始'])

        time.sleep(130)

        recorder_thread.put(['control', 'デスクトップの記録1'])

        time.sleep(10)

        recorder_thread.put(['control', 'デスクトップの記録2'])

        time.sleep(10)

        recorder_thread.put(['control', '記録終了'])

        time.sleep(10)

        recorder_thread.put(['control', '録画開始'])

        time.sleep(90)

        recorder_thread.put(['control', '録画終了'])

        qFunc.statusWait_false(qBusy_d_rec, falseWait=30)



    # 単体実行
    if (len(sys.argv) >= 2):

        # 記録開始
        recorder_thread.put(['control', '_rec_start_'])

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
            res_data  = recorder_thread.get()
            res_name  = res_data[0]
            res_value = res_data[1]
            #if (res_name != ''):
            #    print(res_name, res_value, )

            time.sleep(0.50)



    # 終了
    recorder_thread.abort()
    qFunc.statusWait_false(qBusy_d_rec, falseWait=30)
    del recorder_thread



