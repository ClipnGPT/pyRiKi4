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



import platform
qPLATFORM = platform.system().lower() #windows,darwin,linux

qRUNATTR  = 'python'
if getattr(sys, 'frozen', False):
    qRUNATTR = 'exe'

import socket
qHOSTNAME = socket.gethostname().lower()



def setFolder(name='temp'):
    if (name[-1:] == '/'):
        name = name[:-1]
    if (not os.path.isdir(name)):
        os.makedirs(name)
    return name + '/'



qPath_pictures   = ''
qPath_videos     = ''
if (os.name == 'nt'):
    qUSERNAME = os.environ["USERNAME"]
    qPath_pictures  = setFolder('C:/Users/' + qUSERNAME + '/Pictures/RiKi/')
    qPath_videos    = setFolder('C:/Users/' + qUSERNAME + '/Videos/RiKi/'  )
else:
    qUSERNAME = os.environ["USER"]



qPath_sounds    = '_sounds/'
qPath_icons     = '_icons/'
qPath_fonts     = '_fonts/'

qPath_cache      = setFolder('_cache/' )
qPath_config     = setFolder('_config/')
qPath_controls   = setFolder('_controls/')
qPath_temp       = setFolder('temp/'   )

qPath_log        = setFolder(qPath_temp + '_log/'          )
qPath_work       = setFolder(qPath_temp + '_work/'         )
qPath_rec        = setFolder(qPath_temp + '_recorder/'     )
qPath_recept     = setFolder(qPath_temp + '_recept/'       )
qPath_s_ctrl     = setFolder(qPath_temp + 's6_0control/'   )
qPath_s_inp      = setFolder(qPath_temp + 's6_1voice/'     )
qPath_s_wav      = setFolder(qPath_temp + 's6_2wav/'       )
qPath_s_jul      = setFolder(qPath_temp + 's6_3stt_julius/')
qPath_s_STT      = setFolder(qPath_temp + 's6_4stt_txt/'   )
qPath_s_TTS      = setFolder(qPath_temp + 's6_5tts_txt/'   )
qPath_s_TRA      = setFolder(qPath_temp + 's6_6tra_txt/'   )
qPath_s_play     = setFolder(qPath_temp + 's6_7play/'      )
qPath_s_chat     = setFolder(qPath_temp + 's6_8chat/'      )
qPath_v_ctrl     = setFolder(qPath_temp + 'v6_0control/'   )
qPath_v_inp      = setFolder(qPath_temp + 'v6_1vision/'    )
qPath_v_jpg      = setFolder(qPath_temp + 'v6_2jpg/'       )
qPath_v_detect   = setFolder(qPath_temp + 'v6_3detect/'    )
qPath_v_cv       = setFolder(qPath_temp + 'v6_5cv_txt/'    )
qPath_v_photo    = setFolder(qPath_temp + 'v6_7photo/'     )
qPath_v_msg      = setFolder(qPath_temp + 'v6_7photo_msg/' )
qPath_v_recept   = setFolder(qPath_temp + 'v6_9recept/'    )
qPath_d_ctrl     = setFolder(qPath_temp + 'd6_0control/'   )
qPath_d_play     = setFolder(qPath_temp + 'd6_1play/'      )
qPath_d_prtscn   = setFolder(qPath_temp + 'd6_2screen/'    )
qPath_d_movie    = setFolder(qPath_temp + 'd6_5movie/'     )
qPath_d_telop    = setFolder(qPath_temp + 'd6_7telop_txt/' )
qPath_d_upload   = setFolder(qPath_temp + 'd6_9upload/'    )

qBusy_dev_cpu    = qPath_work + 'busy_dev_cpu.txt'
qBusy_dev_com    = qPath_work + 'busy_dev_commnication.txt'
qBusy_dev_mic    = qPath_work + 'busy_dev_microphone.txt'
qBusy_dev_spk    = qPath_work + 'busy_dev_speaker.txt'
qBusy_dev_cam    = qPath_work + 'busy_dev_camera.txt'
qBusy_dev_dsp    = qPath_work + 'busy_dev_display.txt'
qBusy_dev_scn    = qPath_work + 'busy_dev_screen.txt'
qBusy_s_ctrl     = qPath_work + 'busy_s_0control.txt'
qBusy_s_inp      = qPath_work + 'busy_s_1audio.txt'
qBusy_s_wav      = qPath_work + 'busy_s_2wav.txt'
qBusy_s_STT      = qPath_work + 'busy_s_4stt_txt.txt'
qBusy_s_TTS      = qPath_work + 'busy_s_5tts_txt.txt'
qBusy_s_TRA      = qPath_work + 'busy_s_6tra_txt.txt'
qBusy_s_play     = qPath_work + 'busy_s_7play.txt'
qBusy_s_chat     = qPath_work + 'busy_s_8chat.txt'
qBusy_v_ctrl     = qPath_work + 'busy_v_0control.txt'
qBusy_v_inp      = qPath_work + 'busy_v_1video.txt'
qBusy_v_QR       = qPath_work + 'busy_v_2QR.txt'
qBusy_v_jpg      = qPath_work + 'busy_v_3jpg.txt'
qBusy_v_CV       = qPath_work + 'busy_v_5cv.txt'
qBusy_v_recept   = qPath_work + 'busy_v_9recept.txt'
qBusy_d_ctrl     = qPath_work + 'busy_d_0control.txt'
qBusy_d_inp      = qPath_work + 'busy_d_1screen.txt'
qBusy_d_QR       = qPath_work + 'busy_d_2QR.txt'
qBusy_d_rec      = qPath_work + 'busy_d_5rec.txt'
qBusy_d_telework = qPath_work + 'busy_d_6telework.txt'
qBusy_d_play     = qPath_work + 'busy_d_7play.txt'
qBusy_d_browser  = qPath_work + 'busy_d_8web.txt'
qBusy_d_telop    = qPath_work + 'busy_d_9telop.txt'
qBusy_d_upload   = qPath_work + 'busy_d_9blob.txt'
qRdy__s_force    = qPath_work + 'ready_s_force.txt'
qRdy__s_fproc    = qPath_work + 'ready_s_fproc.txt'
qRdy__s_sendkey  = qPath_work + 'ready_s_sendkey.txt'
qRdy__v_mirror   = qPath_work + 'ready_v_mirror.txt'
qRdy__v_reader   = qPath_work + 'ready_v_reder.txt'
qRdy__v_sendkey  = qPath_work + 'ready_v_sendkey.txt'
qRdy__d_reader   = qPath_work + 'ready_d_reder.txt'
qRdy__d_sendkey  = qPath_work + 'ready_d_sendkey.txt'



class qRiKi_class:

    def __init__(self, ):
        pass

    def __del__(self, ):
        pass
                
    def init(self, ):
        self.makeDirs('temp/_log/',   False)
        self.makeDirs(qPath_cache,    False)

        self.makeDirs(qPath_log,      False)
        self.makeDirs(qPath_work,     False)
        self.makeDirs(qPath_rec,      False)
        self.makeDirs(qPath_recept,   False)

        self.makeDirs(qPath_s_ctrl,   False)
        self.makeDirs(qPath_s_inp,    False)
        self.makeDirs(qPath_s_wav,    False)
        self.makeDirs(qPath_s_jul,    False)
        self.makeDirs(qPath_s_STT,    False)
        self.makeDirs(qPath_s_TTS,    False)
        self.makeDirs(qPath_s_TRA,    False)
        self.makeDirs(qPath_s_play,   False)
        self.makeDirs(qPath_s_chat,   False)
        self.makeDirs(qPath_v_ctrl,   False)
        self.makeDirs(qPath_v_inp,    False)
        self.makeDirs(qPath_v_jpg,    False)
        self.makeDirs(qPath_v_detect, False)
        self.makeDirs(qPath_v_cv,     False)
        self.makeDirs(qPath_v_photo,  False)
        self.makeDirs(qPath_v_msg,    False)
        self.makeDirs(qPath_v_recept, False)
        self.makeDirs(qPath_d_ctrl,   False)
        self.makeDirs(qPath_d_play,   False)
        self.makeDirs(qPath_d_prtscn, False)
        self.makeDirs(qPath_d_movie,  False)
        self.makeDirs(qPath_d_telop,  False)
        self.makeDirs(qPath_d_upload, False)

        if (qPath_pictures != ''):
            self.makeDirs(qPath_pictures, False)
        if (qPath_videos != ''):
            self.makeDirs(qPath_videos,   False)

        return True

    def makeDirs(self, ppath, remove=False, ):
        try:
            if (len(ppath) > 0):
                path=ppath.replace('\\', '/')
                if (path[-1:] != '/'):
                    path += '/'
                if (not os.path.isdir(path[:-1])):
                    os.makedirs(path[:-1])
                else:
                    if (remove != False):
                        files = glob.glob(path + '*')
                        for f in files:
                            if (remove == True):
                                try:
                                    self.remove(f)
                                except Exception as e:
                                    pass
                            if (str(remove).isdigit()):
                                try:
                                    nowTime   = datetime.datetime.now()
                                    fileStamp = os.path.getmtime(f)
                                    fileTime  = datetime.datetime.fromtimestamp(fileStamp)
                                    td = nowTime - fileTime
                                    if (td.days >= int(remove)):
                                        self.remove(f)
                                except Exception as e:
                                    pass

        except Exception as e:
            pass
        return True

    def getValue(self, field):
        if (field == 'qPLATFORM'       ): return qPLATFORM
        if (field == 'qRUNATTR'        ): return qRUNATTR
        if (field == 'qHOSTNAME'       ): return qHOSTNAME
        if (field == 'qUSERNAME'       ): return qUSERNAME
        if (field == 'qPath_controls'  ): return qPath_controls
        if (field == 'qPath_pictures'  ): return qPath_pictures
        if (field == 'qPath_videos'    ): return qPath_videos
        if (field == 'qPath_cache'     ): return qPath_cache
        if (field == 'qPath_sounds'    ): return qPath_sounds
        if (field == 'qPath_icons'     ): return qPath_icons
        if (field == 'qPath_fonts'     ): return qPath_fonts

        if (field == 'qPath_log'       ): return qPath_log
        if (field == 'qPath_work'      ): return qPath_work
        if (field == 'qPath_rec'       ): return qPath_rec
        if (field == 'qPath_recept'    ): return qPath_recept

        if (field == 'qPath_s_ctrl'    ): return qPath_s_ctrl
        if (field == 'qPath_s_inp'     ): return qPath_s_inp
        if (field == 'qPath_s_wav'     ): return qPath_s_wav
        if (field == 'qPath_s_jul'     ): return qPath_s_jul
        if (field == 'qPath_s_STT'     ): return qPath_s_STT
        if (field == 'qPath_s_TTS'     ): return qPath_s_TTS
        if (field == 'qPath_s_TRA'     ): return qPath_s_TRA
        if (field == 'qPath_s_play'    ): return qPath_s_play
        if (field == 'qPath_s_chat'    ): return qPath_s_chat
        if (field == 'qPath_v_ctrl'    ): return qPath_v_ctrl
        if (field == 'qPath_v_inp'     ): return qPath_v_inp
        if (field == 'qPath_v_jpg'     ): return qPath_v_jpg
        if (field == 'qPath_v_detect'  ): return qPath_v_detect
        if (field == 'qPath_v_cv'      ): return qPath_v_cv
        if (field == 'qPath_v_photo'   ): return qPath_v_photo
        if (field == 'qPath_v_msg'     ): return qPath_v_msg
        if (field == 'qPath_v_recept'  ): return qPath_v_recept
        if (field == 'qPath_d_ctrl'    ): return qPath_d_ctrl
        if (field == 'qPath_d_play'    ): return qPath_d_play
        if (field == 'qPath_d_prtscn'  ): return qPath_d_prtscn
        if (field == 'qPath_d_movie'   ): return qPath_d_movie
        if (field == 'qPath_d_telop'   ): return qPath_d_telop
        if (field == 'qPath_d_upload'  ): return qPath_d_upload

        if (field == 'qBusy_dev_cp'   ): return qBusy_dev_cpu
        if (field == 'qBusy_dev_com'   ): return qBusy_dev_com
        if (field == 'qBusy_dev_mic'   ): return qBusy_dev_mic
        if (field == 'qBusy_dev_spk'   ): return qBusy_dev_spk
        if (field == 'qBusy_dev_cam'   ): return qBusy_dev_cam
        if (field == 'qBusy_dev_dsp'   ): return qBusy_dev_dsp
        if (field == 'qBusy_dev_scn'   ): return qBusy_dev_scn
        if (field == 'qBusy_s_ctrl'    ): return qBusy_s_ctrl
        if (field == 'qBusy_s_inp'     ): return qBusy_s_inp
        if (field == 'qBusy_s_wav'     ): return qBusy_s_wav
        if (field == 'qBusy_s_STT'     ): return qBusy_s_STT
        if (field == 'qBusy_s_TTS'     ): return qBusy_s_TTS
        if (field == 'qBusy_s_TRA'     ): return qBusy_s_TRA
        if (field == 'qBusy_s_play'    ): return qBusy_s_play
        if (field == 'qBusy_s_chat'    ): return qBusy_s_chat
        if (field == 'qBusy_v_ctrl'    ): return qBusy_v_ctrl
        if (field == 'qBusy_v_inp'     ): return qBusy_v_inp
        if (field == 'qBusy_v_QR'      ): return qBusy_v_QR
        if (field == 'qBusy_v_jpg'     ): return qBusy_v_jpg
        if (field == 'qBusy_v_CV'      ): return qBusy_v_CV
        if (field == 'qBusy_v_recept'  ): return qBusy_v_recept
        if (field == 'qBusy_d_ctrl'    ): return qBusy_d_ctrl
        if (field == 'qBusy_d_inp'     ): return qBusy_d_inp
        if (field == 'qBusy_d_QR'      ): return qBusy_d_QR
        if (field == 'qBusy_d_rec'     ): return qBusy_d_rec
        if (field == 'qBusy_d_telework'): return qBusy_d_telework
        if (field == 'qBusy_d_play'    ): return qBusy_d_play
        if (field == 'qBusy_d_browser' ): return qBusy_d_browser
        if (field == 'qBusy_d_telop'   ): return qBusy_d_telop
        if (field == 'qBusy_d_upload'  ): return qBusy_d_upload
        if (field == 'qRdy__s_force'   ): return qRdy__s_force
        if (field == 'qRdy__s_fproc'   ): return qRdy__s_fproc
        if (field == 'qRdy__s_sendkey' ): return qRdy__s_sendkey
        if (field == 'qRdy__v_mirror'  ): return qRdy__v_mirror
        if (field == 'qRdy__v_reader'  ): return qRdy__v_reader
        if (field == 'qRdy__v_sendkey' ): return qRdy__v_sendkey
        if (field == 'qRdy__d_reader'  ): return qRdy__d_reader
        if (field == 'qRdy__d_sendkey' ): return qRdy__d_sendkey

        print('check program !' + field)
        return None

    def checkWakeUpWord(self, txt='', ):
        proc_text = txt.lower()
        if (proc_text == '力') or (proc_text == 'りき') \
        or (proc_text == 'リキ') or (proc_text == 'リッキー') \
        or (proc_text == '三木') or (proc_text == 'みき') \
        or (proc_text == 'ミキ') or (proc_text == 'ミッキー') \
        or (proc_text == '理系') \
        or (proc_text == 'ウィキ') \
        or (proc_text == 'riki') \
        or (proc_text == 'miki') or (proc_text == 'mickey') \
        or (proc_text == 'wiki') \
        or (proc_text == 'フォース') or (proc_text == 'force') \
        or (proc_text[:6] == 'コンピュータ') or (proc_text == 'computer') \
        or (proc_text.find('riki,') >= 0):
            return True
        else:
            return False

    def statusSet(self, filename, Flag=True, txt='_on_'):
        if (Flag == True):
            chktime = time.time()
            while (not os.path.exists(filename)) and ((time.time() - chktime) < 1):
                try:
                    w = open(filename, 'w')
                    w.write(txt)
                    w.close()
                    w = None
                    return True
                except Exception as e:
                    w = None
                time.sleep(0.10)
        else:
            chktime = time.time()
            while (os.path.exists(filename)) and ((time.time() - chktime) < 1):
                try:
                    os.remove(filename, )
                    return True
                except Exception as e:
                    pass
                time.sleep(0.10)
        return False

    def statusCheck(self, filename, ):
        if (os.path.exists(filename)):
            return True
        else:
            return False

    def statusWait_false(self, filename, falseWait=1, ):
        if (falseWait != 0):
            chktime = time.time()
            while (os.path.exists(filename)) and ((time.time() - chktime) < falseWait):
                time.sleep(0.10)
        return self.statusCheck(filename)

    def statusWait_true(self, filename, trueWait=1, ):
        if (trueWait != 0):
            chktime = time.time()
            while (not os.path.exists(filename)) and ((time.time() - chktime) < trueWait):
                time.sleep(0.10)
        return self.statusCheck(filename)

    def statusWait_speech(self, idolSec=2, maxWait=15, ):
        busy_flag = True
        chktime1 = time.time()
        while (busy_flag == True) and ((time.time() - chktime1) < maxWait):
            busy_flag = False
            chktime2 = time.time()
            while ((time.time() - chktime2) < idolSec):
                if (self.statusCheck(qBusy_s_wav ) == True) \
                or (self.statusCheck(qBusy_s_STT ) == True) \
                or (self.statusCheck(qBusy_s_TTS ) == True) \
                or (self.statusCheck(qBusy_s_TRA ) == True) \
                or (self.statusCheck(qBusy_s_play) == True) \
                or (self.statusCheck(qBusy_s_chat) == True):
                    busy_flag = True
                    time.sleep(0.10)
                    break
        return busy_flag

    def statusReset_speech(self, Flag=False):
        self.statusSet(qBusy_dev_cpu,   Flag)
        self.statusSet(qBusy_dev_com,   Flag)
        self.statusSet(qBusy_dev_mic,   Flag)
        self.statusSet(qBusy_dev_spk,   Flag)
        self.statusSet(qBusy_s_ctrl,    Flag)
        self.statusSet(qBusy_s_inp,     Flag)
        self.statusSet(qBusy_s_wav,     Flag)
        self.statusSet(qBusy_s_STT,     Flag)
        self.statusSet(qBusy_s_TTS,     Flag)
        self.statusSet(qBusy_s_TRA,     Flag)
        self.statusSet(qBusy_s_play,    Flag)
        self.statusSet(qBusy_s_chat,    Flag)
        self.statusSet(qRdy__s_force,   Flag)
        self.statusSet(qRdy__s_fproc,   Flag)
        self.statusSet(qRdy__s_sendkey, Flag)
        return True

    def statusReset_vision(self, Flag=False):
        self.statusSet(qBusy_dev_cpu,   Flag)
        self.statusSet(qBusy_dev_com,   Flag)
        self.statusSet(qBusy_dev_cam,   Flag)
        self.statusSet(qBusy_dev_dsp,   Flag)
        self.statusSet(qBusy_v_ctrl,    Flag)
        self.statusSet(qBusy_v_inp,     Flag)
        self.statusSet(qBusy_v_QR,      Flag)
        self.statusSet(qBusy_v_jpg,     Flag)
        self.statusSet(qBusy_v_CV,      Flag)
        self.statusSet(qBusy_v_recept,  Flag)
        self.statusSet(qRdy__v_mirror,  Flag)
        self.statusSet(qRdy__v_reader,  Flag)
        self.statusSet(qRdy__v_sendkey, Flag)
        return True

    def statusReset_desktop(self, Flag=False):
        self.statusSet(qBusy_dev_cpu,   Flag)
        self.statusSet(qBusy_dev_com,   Flag)
        self.statusSet(qBusy_dev_scn,   Flag)
        self.statusSet(qBusy_d_ctrl,    Flag)
        self.statusSet(qBusy_d_inp,     Flag)
        self.statusSet(qBusy_d_QR,      Flag)
        self.statusSet(qBusy_d_rec,     Flag)
        self.statusSet(qBusy_d_telework,Flag)
        self.statusSet(qBusy_d_play,    Flag)
        self.statusSet(qBusy_d_browser, Flag)
        self.statusSet(qBusy_d_telop,   Flag)
        self.statusSet(qBusy_d_upload,  Flag)
        self.statusSet(qRdy__d_reader,  Flag)
        self.statusSet(qRdy__d_sendkey, Flag)
        return True

    def tts(self, id, text, idolSec=2, maxWait=15, ):
        self.statusWait_speech(idolSec, maxWait, )

        if (text != ''):
            nowTime = datetime.datetime.now()
            stamp   = nowTime.strftime('%Y%m%d.%H%M%S')
            filename = qPath_s_TTS + stamp + '.' + str(id) + '.txt'
            try:
                w = codecs.open(filename, 'w', 'utf-8')
                w.write(text)
                w.close()
                w = None
                return True
            except Exception as e:
                w = None
                return False

        return False

    def chat(self, id, text, ):

        if (text != ''):
            nowTime = datetime.datetime.now()
            stamp   = nowTime.strftime('%Y%m%d.%H%M%S')
            filename = qPath_s_chat + stamp + '.' + str(id) + '.txt'
            try:
                w = codecs.open(filename, 'w', 'utf-8')
                w.write(text)
                w.close()
                w = None
                return True
            except Exception as e:
                w = None
                return False

        return False

    def speech(self, id='speech', speechs=[], lang='auto', idolSec=2, maxWait=15, ):
        self.statusWait_speech(idolSec, maxWait, )

        outLang = lang
        if (outLang == 'auto'):
            if   (qPLATFORM == 'windows'):
                #outLang = 'ja,winos,'
                outLang = 'ja,hoya,'
            elif (qPLATFORM == 'darwin'):
                outLang = 'ja,macos,'
            else:
                outLang = 'ja,free,'

        seq = 0
        for speech in speechs:
            text = outLang + str(speech['text'])
            seq+= 1
            id2  = id + '.' + '{:02}'.format(seq)
            self.tts(id2, text, 0, 0, )
            try:
                time.sleep(speech['wait'])
            except Exception as e:
                pass

        return True

class qBusy_status_txts_class(object):
    def __init__(self):
        self.check     = ''

        self.dev_cpu   = False
        self.dev_com   = False
        self.dev_mic   = False
        self.dev_spk   = False
        self.dev_cam   = False
        self.dev_dsp   = False
        self.dev_scn   = False
        self.s_ctrl    = False
        self.s_inp     = False
        self.s_wav     = False
        self.s_STT     = False
        self.s_TTS     = False
        self.s_TRA     = False
        self.s_play    = False
        self.s_chat    = False
        self.s_force   = False
        self.s_sendkey = False
        self.v_ctrl    = False
        self.v_inp     = False
        self.v_QR      = False
        self.v_jpg     = False
        self.v_CV      = False
        self.v_recept  = False
        self.v_mirror  = False
        self.v_reader  = False
        self.v_sendkey = False
        self.d_ctrl    = False
        self.d_inp     = False
        self.d_QR      = False
        self.d_rec     = False
        self.d_telework= False
        self.d_play    = False
        self.d_browser = False
        self.d_telop   = False
        self.d_upload  = False
        self.d_reader  = False
        self.d_sendkey = False

    def statusCheck(self, filename, ):
        if (os.path.exists(filename)):
            return True
        else:
            return False

    def getAll(self):
        change = False

        if (self.check !='all'):
            change = True
        self.check = 'all'

        # ステータス取得
        check = self.statusCheck(qBusy_dev_cpu)
        if (check != self.dev_cpu):
            change = True
        self.dev_cpu = check
        check = self.statusCheck(qBusy_dev_com)
        if (check != self.dev_com):
            change = True
        self.dev_com = check
        check = self.statusCheck(qBusy_dev_mic)
        if (check != self.dev_mic):
            change = True
        self.dev_mic = check
        check = self.statusCheck(qBusy_dev_spk)
        if (check != self.dev_spk):
            change = True
        self.dev_spk = check
        check = self.statusCheck(qBusy_dev_cam)
        if (check != self.dev_cam):
            change = True
        self.dev_cam = check
        check = self.statusCheck(qBusy_dev_dsp)
        if (check != self.dev_dsp):
            change = True
        self.dev_dsp = check
        check = self.statusCheck(qBusy_dev_scn)
        if (check != self.dev_scn):
            change = True
        self.dev_scn = check

        check = self.statusCheck(qBusy_s_ctrl)
        if (check != self.s_ctrl):
            change = True
        self.s_ctrl = check
        check = self.statusCheck(qBusy_s_inp )
        if (check != self.s_inp):
            change = True
        self.s_inp = check
        check = self.statusCheck(qBusy_s_wav )
        if (check != self.s_wav):
            change = True
        self.s_wav = check
        check = self.statusCheck(qBusy_s_STT )
        if (check != self.s_STT):
            change = True
        self.s_STT = check
        check = self.statusCheck(qBusy_s_TTS )
        if (check != self.s_TTS):
            change = True
        self.s_TTS = check
        check = self.statusCheck(qBusy_s_TRA )
        if (check != self.s_TRA):
            change = True
        self.s_TRA = check
        check = self.statusCheck(qBusy_s_play)
        if (check != self.s_play):
            change = True
        self.s_play = check
        check = self.statusCheck(qBusy_s_chat)
        if (check != self.s_chat):
            change = True
        self.s_chat = check
        check = self.statusCheck(qRdy__s_force)
        if (check != self.s_force):
            change = True
        self.s_force = check
        check = self.statusCheck(qRdy__s_sendkey)
        if (check != self.s_sendkey):
            change = True
        self.s_sendkey = check

        check = self.statusCheck(qBusy_v_ctrl)
        if (check != self.v_ctrl):
            change = True
        self.v_ctrl = check
        check = self.statusCheck(qBusy_v_inp )
        if (check != self.v_inp):
            change = True
        self.v_inp = check
        check = self.statusCheck(qBusy_v_QR  )
        if (check != self.v_QR):
            change = True
        self.v_QR = check
        check = self.statusCheck(qBusy_v_jpg )
        if (check != self.v_jpg):
            change = True
        self.v_jpg = check
        check = self.statusCheck(qBusy_v_CV  )
        if (check != self.v_CV):
            change = True
        self.v_CV = check
        check = self.statusCheck(qBusy_v_recept)
        if (check != self.v_recept):
            change = True
        self.v_recept = check
        check = self.statusCheck(qRdy__v_mirror)
        if (check != self.v_mirror):
            change = True
        self.v_mirror = check
        check = self.statusCheck(qRdy__v_reader)
        if (check != self.v_reader):
            change = True
        self.v_reader = check
        check = self.statusCheck(qRdy__v_sendkey)
        if (check != self.v_sendkey):
            change = True
        self.v_sendkey = check

        check = self.statusCheck(qBusy_d_ctrl)
        if (check != self.d_ctrl):
            change = True
        self.d_ctrl = check
        check = self.statusCheck(qBusy_d_inp )
        if (check != self.d_inp):
            change = True
        self.d_inp = check
        check = self.statusCheck(qBusy_d_QR  )
        if (check != self.d_QR):
            change = True
        self.d_QR = check
        check = self.statusCheck(qBusy_d_rec )
        if (check != self.d_rec):
            change = True
        self.d_rec = check
        check = self.statusCheck(qBusy_d_telework)
        if (check != self.d_telework):
            change = True
        self.d_telework = check
        check = self.statusCheck(qBusy_d_play)
        if (check != self.d_play):
            change = True
        self.d_play = check
        check = self.statusCheck(qBusy_d_browser)
        if (check != self.d_browser):
            change = True
        self.d_browser = check
        check = self.statusCheck(qBusy_d_telop)
        if (check != self.d_telop):
            change = True
        self.d_telop = check
        check = self.statusCheck(qBusy_d_upload)
        if (check != self.d_upload):
            change = True
        self.d_upload = check
        check = self.statusCheck(qRdy__d_reader)
        if (check != self.d_reader):
            change = True
        self.d_reader = check
        check = self.statusCheck(qRdy__d_sendkey)
        if (check != self.d_sendkey):
            change = True
        self.d_sendkey = check

        if (change != True):
            return False

        # 文字列生成
        txts=[]
        txts.append('[Device control]')
        if (self.dev_cpu == True):
            txts.append(' CPU    : slow!___')
        else:
            txts.append(' CPU    : ________')
        if (self.dev_com == True):
            txts.append(' Comm   : disable!')
        else:
            txts.append(' Comm   : ________')
        if (self.dev_mic == True):
            txts.append(' Mic    : disable!')
        else:
            txts.append(' Mic    : ________')
        if (self.dev_spk == True):
            txts.append(' Speaker: disable!')
        else:
            txts.append(' Speaker: ________')
        if (self.dev_cam == True):
            txts.append(' camera : disable!')
        else:
            txts.append(' camera : ________')
        if (self.dev_dsp == True):
            txts.append(' Display: disable!')
        else:
            txts.append(' Display: ________')
        if (self.dev_scn == True):
            txts.append(' Screen : disable!')
        else:
            txts.append(' Screen : ________')

        txts.append('')
        txts.append('[Speech status]')
        if (self.s_ctrl == True):
            txts.append(' Ctrl   : active__')
        else:
            txts.append(' Ctrl   : ________')
        if (self.s_inp == True):
            txts.append(' Input  : ready___')
        else:
            txts.append(' Input  : ________')
        if (self.s_wav == True):
            txts.append(' Wave   : busy!___')
        else:
            txts.append(' Wave   : ________')
        if (self.s_STT == True):
            txts.append(' STT    : busy!___')
        else:
            txts.append(' STT    : ________')
        if (self.s_TTS == True):
            txts.append(' TTS    : busy!___')
        else:
            txts.append(' TTS    : ________')
        if (self.s_TRA == True):
            txts.append(' TRA    : busy!___')
        else:
            txts.append(' TRA    : ________')
        if (self.s_play == True):
            txts.append(' Play   : busy!___')
        else:
            txts.append(' Play   : ________')
        if (self.s_chat == True):
            txts.append(' Chat   : busy!___')
        else:
            txts.append(' Chat   : ________')
        if (self.s_force == True):
            txts.append(' RIKI   : active__')
        else:
            txts.append(' RIKI   : ________')
        if (self.s_sendkey == True):
            txts.append(' SendKey: active__')
        else:
            txts.append(' SendKey: ________')

        txts.append('')
        txts.append('[Vision status]')
        if (self.v_ctrl == True):
            txts.append(' Ctrl   : active__')
        else:
            txts.append(' Ctrl   : ________')
        if (self.v_inp == True):
            txts.append(' Input  : active__')
        else:
            txts.append(' Input  : ________')
        if (self.v_QR == True):
            txts.append(' QR scan: active__')
        else:
            txts.append(' QR scan: ________')
        if (self.v_jpg == True):
            txts.append(' jpeg   : busy!___')
        else:
            txts.append(' jpeg   : ________')
        if (self.v_CV == True):
            txts.append(' CV     : busy!___')
        else:
            txts.append(' CV     : ________')
        if (self.v_recept == True):
            txts.append(' recept : busy!___')
        else:
            txts.append(' recept : ________')
        if (self.v_reader == True):
            txts.append(' Reader : active__')
        else:
            txts.append(' Reader : ________')
        if (self.v_sendkey == True):
            txts.append(' SendKey: active__')
        else:
            txts.append(' SendKey: ________')

        txts.append('')
        txts.append('[Desktop status]')
        if (self.d_ctrl == True):
            txts.append(' Ctrl   : active__')
        else:
            txts.append(' Ctrl   : ________')
        if (self.d_inp == True):
            txts.append(' Capture: active__')
        else:
            txts.append(' Capture: ________')
        if (self.d_QR == True):
            txts.append(' QR scan: active__')
        else:
            txts.append(' QR scan: ________')
        if (self.d_rec == True):
            txts.append(' Rec    : rec!____')
        else:
            txts.append(' Rec    : ________')
        if (self.d_play == True):
            txts.append(' Play   : play!___')
        else:
            txts.append(' Play   : ________')
        if (self.d_browser == True):
            txts.append(' Browser: play!___')
        else:
            txts.append(' Browser: ________')
        if (self.d_telop == True):
            txts.append(' Telop  : active__')
        else:
            txts.append(' Telop  : ________')
        if (self.d_upload == True):
            txts.append(' Upload : active__')
        else:
            txts.append(' Upload : ________')
        if (self.d_reader == True):
            txts.append(' Reader : active__')
        else:
            txts.append(' Reader : ________')
        if (self.d_sendkey == True):
            txts.append(' SendKey: active__')
        else:
            txts.append(' SendKey: ________')

        txts.append('')
        return txts

    def getRecorder(self):
        change = False

        if (self.check !='recorder'):
            change = True
        self.check = 'recorder'

        # ステータス取得
        check = self.statusCheck(qBusy_s_inp )
        if (check != self.s_inp):
            change = True
        self.s_inp = check
        check = self.statusCheck(qBusy_d_rec )
        if (check != self.d_rec):
            change = True
        self.d_rec = check
 
        if (change != True):
            return False

        # 文字列生成
        txts=[]
        if (self.s_inp == True):
            txts.append(' Speech   : ready__')
        else:
            txts.append(' Speech   : _______')
        if (self.d_rec == True):
            txts.append(' Recorder : rec!___')
        else:
            txts.append(' Recorder : _______')

        return txts



if (__name__ == '__main__'):

    qRiKi = qRiKi_class()
    qRiKi.init()

    # テスト
    qBusy_status_txts = qBusy_status_txts_class()

    qRiKi.statusReset_speech(True)
    qRiKi.statusReset_vision(True)
    qRiKi.statusReset_desktop(True)

    qRiKi.statusReset_speech(False)
    qRiKi.statusReset_vision(False)
    qRiKi.statusReset_desktop(False)

    txts = qBusy_status_txts.getAll()
    for txt in txts:
        print(txt)

    txts = qBusy_status_txts.getRecorder()
    for txt in txts:
        print(txt)


