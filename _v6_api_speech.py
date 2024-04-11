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

#import pykakasi



# 出力インターフェース
qCtrl_result_speech      = 'temp/result_speech.txt'
qCtrl_recognize          = 'temp/result_recognize.txt'
qCtrl_recognize_sjis     = 'temp/result_recognize_sjis.txt'
qCtrl_translate          = 'temp/result_translate.txt'
qCtrl_translate_sjis     = 'temp/result_translate_sjis.txt'

# 外部プログラム
qExt_speech              = '__ext_speech.bat'



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



qApiInp    = 'free'
qApiTrn    = qApiInp
qApiOut    = qApiInp
if (qApiOut == 'free') and (qPLATFORM == 'windows'):
    qApiOut = 'winos'
if (qApiOut == 'free') and (qPLATFORM == 'darwin'):
    qApiOut = 'macos'
qLangInp   = 'ja'
qLangTrn   = 'en,fr,'
qLangTxt   = qLangInp
qLangOut   = qLangTrn[:2]


# google 音声認識、翻訳機能、音声合成
import speech_api_google     as google_api
import speech_api_google_key as google_key

# watson 音声認識、翻訳機能、音声合成
import speech_api_watson     as watson_api
import speech_api_watson_key as watson_key

# azure 音声認識、翻訳機能、音声合成
import speech_api_azure     as azure_api
import speech_api_azure_key as azure_key

# aws 音声認識、翻訳機能、音声合成
import speech_api_aws     as aws_api
import speech_api_aws_key as aws_key

# hoya 音声合成
import speech_api_hoya     as hoya_api
import speech_api_hoya_key as hoya_key

# winos 音声合成
if (qPLATFORM == 'windows'):
    import speech_api_winos as winos_api

# macos 音声合成
if (qPLATFORM == 'darwin'):
    import speech_api_macos as macos_api



def qVoiceInput(useApi='free', inpLang='auto', inpFile='_sounds/_sound_hallo.wav', apiRecovery=True, ):
    resText = ''
    resApi  = ''

    api   = useApi
    if  (api != 'free')   and (api != 'google') and (api != 'google8k') \
    and (api != 'watson') and (api != 'azure')  and (api != 'aws'):
        api = 'free'

    if (resText == '') and (api == 'watson'):
        watsonAPI = watson_api.SpeechAPI()
        res = watsonAPI.authenticate('stt',
                   watson_key.getkey('stt','url'),
                   watson_key.getkey('stt','key'), )
        if (res == True):
            resText, resApi = watsonAPI.recognize(inpWave=inpFile, inpLang=inpLang)
        if (resText == '') and (apiRecovery == True):
            api   = 'free'

    if (resText == '') and (api == 'azure'):
        azureAPI = azure_api.SpeechAPI()
        key     = azure_key.getkey('stt', 'key', )
        authurl = azure_key.getkey('stt', 'authurl', )
        procurl = azure_key.getkey('stt', 'procurl', )
        res = azureAPI.authenticate('stt', key, authurl, procurl, )
        if (res == True):
            resText, resApi = azureAPI.recognize(inpWave=inpFile, inpLang=inpLang)
        if (resText == '') and (apiRecovery == True):
            api   = 'free'

    if (resText == '') and (api == 'aws'):
        awsAPI = aws_api.SpeechAPI()
        key_id     = aws_key.getkey('stt', 'key_id',     )
        secret_key = aws_key.getkey('stt', 'secret_key', )
        res   = awsAPI.authenticate('stt', key_id, secret_key, )
        if (res == True):
            resText, resApi = awsAPI.recognize(inpWave=inpFile, inpLang=inpLang)
        if (resText == '') and (apiRecovery == True):
            api   = 'free'

    if (resText == '') and (api == 'google' or api == 'google8k' or api == 'free'):
        googleAPI = google_api.SpeechAPI()
        res = googleAPI.authenticate('stt', google_key.getkey('stt'), )
        if (res == True):
            if   (api == 'google'):
                resText, resApi = googleAPI.recognize(inpWave=inpFile, inpLang=inpLang, api=api)
            elif (api == 'google8k'):
                resText, resApi = googleAPI.recognize(inpWave=inpFile, inpLang=inpLang, api=api)
            else:
                resText, resApi = googleAPI.recognize(inpWave=inpFile, inpLang=inpLang, api=api)

    if (resText != ''):
        return resText, resApi

    return '', ''



def qTranslator_cacheFile(useApi='free', inpLang='ja', outLang='en', inpText='こんにちわ', ):
    if (inpText != '') and (inpText != '!'):
        f = qFunc.txt2filetxt(inpText)
        if (inpLang == 'ja'):
            f = f.replace('_','')
        while (f[:1] == '_'):
            f = f[1:]
        while (f[-1:] == '_'):
            f = f[:-1]

        cacheFile=qPath_cache + f + '_' + inpLang + '_' + outLang + '_' + useApi + '_utf8.txt'
        return cacheFile

    return ''

def qTranslator_fromCache(useApi='free', inpLang='ja', outLang='en', inpText='こんにちわ', ):
    cacheFile = qTranslator_cacheFile(useApi=useApi, inpLang=inpLang, outLang=outLang, inpText=inpText, )
    if (cacheFile != ''):
        if (os.path.exists(cacheFile)):
            res, txt = qFunc.txtsRead(cacheFile, encoding='utf-8', exclusive=False, )
            if (res != False):
                return True, txt
            else:
                return False, ''
    return False, ''

def qTranslator_toCache(useApi='free', inpLang='ja', outLang='en', inpText='こんにちわ', outText='Hello', ):
    cacheFile = qTranslator_cacheFile(useApi=useApi, inpLang=inpLang, outLang=outLang, inpText=inpText, )
    if (cacheFile == ''):
        return False
    if (os.path.exists(cacheFile)):
        return True
    if (len(cacheFile) > 128):
        return False
    if (inpLang != 'ja') and (inpLang != 'en'):
        return False
    #if (outLang != 'ja') and (outLang != 'en'):
    #    return False
    if (outText == '') or (outText == '!'):
        return False

    res = qFunc.txtsWrite(cacheFile, txts=[outText], encoding='utf-8', exclusive=False, mode='w', )
    return res



def qTranslator(useApi='free', inpLang='ja', outLang='en', inpText='こんにちわ', apiRecovery=True, ):
    resText = ''
    resApi  = ''

    api = useApi
    if  (api != 'free')  and (api != 'google') and (api != 'watson') \
    and (api != 'azure') and (api != 'aws'):
        api = 'free'
    if (inpText == '' or inpLang == outLang):
        api = 'none'

    apirun = True

    if (apirun == True):

        if (resText == ''):
            res, txt = qTranslator_fromCache(useApi=api, inpLang=inpLang, outLang=outLang, inpText=inpText, )
            if (res == True):
                resText = txt
                resApi  = api
                apirun  = False
            if (resText == '') and (useApi == 'google'):
                res, txt = qTranslator_fromCache(useApi='free', inpLang=inpLang, outLang=outLang, inpText=inpText, )
                if (res == True):
                    resText = txt
                    resApi  = 'free'
                    apirun  = False
            if (resText == '') and (useApi == 'free'):
                res, txt = qTranslator_fromCache(useApi='google', inpLang=inpLang, outLang=outLang, inpText=inpText, )
                if (res == True):
                    resText = txt
                    resApi  = 'google'
                    apirun  = False

        if (resText == '') and (api == 'none'):
            resText = inpText
            resApi  = api
            apirun  = False

        if (resText == '') and (api == 'watson'):
            watsonAPI = watson_api.SpeechAPI()
            res = watsonAPI.authenticate('tra',
                       watson_key.getkey('tra','url'),
                       watson_key.getkey('tra','key'), )
            if (res == True):
                if (inpLang == 'en' or outLang == 'en'):
                    resText , resApi = watsonAPI.translate(inpText=inpText, inpLang=inpLang, outLang=outLang, )
                else:
                    resTextx, resApi = watsonAPI.translate(inpText=inpText,  inpLang=inpLang, outLang='en', )
                    resText , resApi = watsonAPI.translate(inpText=resTextx, inpLang='en', outLang=outLang, )
            if (resText == '') and (apiRecovery == True):
                api = 'free'

        if (resText == '') and (api == 'azure'):
            azureAPI = azure_api.SpeechAPI()
            key     = azure_key.getkey('tra', 'key', )
            authurl = azure_key.getkey('tra', 'authurl', )
            procurl = azure_key.getkey('tra', 'procurl', )
            res = azureAPI.authenticate('tra', key, authurl, procurl, )
            if (res == True):
                resText, resApi = azureAPI.translate(inpText=inpText, inpLang=inpLang, outLang=outLang, )
            if (resText == '') and (apiRecovery == True):
                api = 'free'

        if (resText == '') and (api == 'aws'):
            awsAPI = aws_api.SpeechAPI()
            key_id     = aws_key.getkey('tra', 'key_id',     )
            secret_key = aws_key.getkey('tra', 'secret_key', )
            res   = awsAPI.authenticate('tra', key_id, secret_key, )
            if (res == True):
                resText, resApi = awsAPI.translate(inpText=inpText, inpLang=inpLang, outLang=outLang, )
            if (resText == '') and (apiRecovery == True):
                api = 'free'

        if (resText == '') and (api == 'free') and (useApi != 'free'):
            res, txt = qTranslator_fromCache(useApi=api, inpLang=inpLang, outLang=outLang, inpText=inpText, )
            if (res == True):
                resText = txt
                resApi  = api
                apirun  = False

        if (resText == '') and (api == 'google' or api == 'free'):
            googleAPI = google_api.SpeechAPI()
            res = googleAPI.authenticate('tra', google_key.getkey('tra'), )
            if (res == True):
                if   (api == 'google'):
                    resText, resApi = googleAPI.translate(inpText=inpText, inpLang=inpLang, outLang=outLang, api=api, )
                else:
                    resText, resApi = googleAPI.translate(inpText=inpText, inpLang=inpLang, outLang=outLang, api=api, )

    if (apirun == True):
        if (resText != ''):
            qTranslator_toCache(useApi=resApi, inpLang=inpLang, outLang=outLang, inpText=inpText, outText=resText, )

    if (resText != ''):
        return resText, resApi

    return '', ''



def qVoiceOutput_cacheFile(useApi='free', outLang='en', outText='Hallo', ):
    if (outText != '') and (outText != '!'):
        f = qFunc.txt2filetxt(outText)
        if (outLang == 'ja'):
            f = f.replace('_','')
        while (f[:1] == '_'):
            f = f[1:]
        while (f[-1:] == '_'):
            f = f[:-1]

        cacheFile=qPath_cache + f + '_' + outLang + '_' + useApi + '.mp3'
        return cacheFile

    return ''

def qVoiceOutput_fromCache(useApi='free', outLang='en', outText='Hallo', outFile='temp/temp_Hallo.mp3',):
    cacheFile = qVoiceOutput_cacheFile(useApi=useApi, outLang=outLang, outText=outText, )
    if (cacheFile != ''):
        if (os.path.exists(cacheFile)):
            try:
                if (cacheFile[-4:].lower() == outFile[-4:].lower()):
                    qFunc.copy(cacheFile, outFile)
                    return True
                else:
                    sox = subprocess.Popen(['sox', '-q', cacheFile, outFile, ], \
                          shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                    sox.wait()
                    sox.terminate()
                    sox = None
                    return True
            except Exception as e:
                pass
    return False

def qVoiceOutput_toCache(useApi='free', outLang='en', outText='Hallo', tempFile=''):
    cacheFile = qVoiceOutput_cacheFile(useApi=useApi, outLang=outLang, outText=outText, )
    if (cacheFile == ''):
        return False
    if (os.path.exists(cacheFile)):
        return True
    if (len(cacheFile) > 128):
        return False
    if (outLang != 'ja') and (outLang != 'en'):
        return False
    if (outText == '') or (outText == '!'):
        return False
    if (not os.path.exists(tempFile)):
        return False

    try:
        if (tempFile[-4:].lower() == cacheFile[-4:].lower()):
            qFunc.copy(tempFile, cacheFile)
            return True
        else:
            sox = subprocess.Popen(['sox', '-q', tempFile, cacheFile, ], \
                  shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
            sox.wait()
            sox.terminate()
            sox = None
            return True
    except Exception as e:
        pass

    return False

def qVoiceOutput(useApi='free', outLang='en', outText='Hallo', outFile='temp/temp_Hallo.mp3', tempFile='', apiRecovery=True, ):
    resText = ''
    resApi  = ''

    if (os.path.exists(outFile)):
        try:
            os.remove(outFile)
        except Exception as e:
            pass

    if (tempFile == ''):
        tempFileWav='temp/temp_qVoiceOutput.wav'
        tempFileMp3='temp/temp_qVoiceOutput.mp3'
    else:
        tempFileWav=tempFile[:-4] + '.wav'
        tempFileMp3=tempFile[:-4] + '.mp3'
    if (os.path.exists(tempFileWav)):
        try:
            os.remove(tempFileWav)
        except Exception as e:
            pass
    if (os.path.exists(tempFileMp3)):
        try:
            os.remove(tempFileMp3)
        except Exception as e:
            pass

    api   = useApi
    if  (api != 'free')  and (api != 'google') and (api != 'watson') \
    and (api != 'azure') and (api != 'aws') \
    and (api != 'winos') and (api != 'macos')  and (api != 'hoya'):
        api = 'free'
        if (qPLATFORM == 'windows'):
            api = 'winos'
        if (qPLATFORM == 'darwin'):
            api = 'macos'

    apirun = True
    #kakasi_api = True
    #if (kakasi_api == True):
    #    kakasi_ = pykakasi.kakasi()
    #    kakasi_.setMode('J', 'H') # J:漢字 H:ひらがな
    #    kakasi_cv = kakasi_.getConverter()

    if (apirun == True):

        if (resText == ''):
            res = qVoiceOutput_fromCache(useApi=api, outLang=outLang, outText=outText, outFile=outFile,)
            if (res == True):
                resText = outText
                resApi  = api
                apirun  = False
            if (resText == '') and (useApi == 'google'):
                res = qVoiceOutput_fromCache(useApi='free', outLang=outLang, outText=outText, outFile=outFile,)
                if (res == True):
                    resText = outText
                    resApi  = 'free'
                    apirun  = False
            if (resText == '') and (useApi == 'free'):
                res = qVoiceOutput_fromCache(useApi='google', outLang=outLang, outText=outText, outFile=outFile,)
                if (res == True):
                    resText = outText
                    resApi  = 'google'
                    apirun  = False

        if (resText == '') and (api == 'watson'):
            watsonAPI = watson_api.SpeechAPI()
            res = watsonAPI.authenticate('tts',
                       watson_key.getkey('tts','url'),
                       watson_key.getkey('tts','key'), )
            if (res == True):
                #if (outLang == 'ja') and (kakasi_api == True):
                #    outText_kana = kakasi_cv.do(outText)
                #    resText, resApi = watsonAPI.vocalize(outText=outText_kana, outLang=outLang, outFile=tempFileMp3, )
                #    if (resText != ''):
                #        resText = outText
                #else:
                #    resText, resApi = watsonAPI.vocalize(outText=outText, outLang=outLang, outFile=tempFileMp3, )
                resText, resApi = watsonAPI.vocalize(outText=outText, outLang=outLang, outFile=tempFileMp3, )
                if (resText != ''):
                    if (tempFileMp3[-4:].lower() == outFile[-4:].lower()):
                        qFunc.copy(tempFileMp3, outFile)
                    else:
                        sox = subprocess.Popen(['sox', '-q', tempFileMp3, outFile, ], \
                              shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                        sox.wait()
                        sox.terminate()
                        sox = None
            if (resText == '') and (apiRecovery == True):
                api  = 'free'

        if (resText == '') and (api == 'azure'):
            azureAPI = azure_api.SpeechAPI()
            key     = azure_key.getkey('tts', 'key', )
            authurl = azure_key.getkey('tts', 'authurl', )
            procurl = azure_key.getkey('tts', 'procurl', )
            res = azureAPI.authenticate('tts', key, authurl, procurl, )
            if (res == True):
                #if (outLang == 'ja') and (kakasi_api == True):
                #    outText_kana = kakasi_cv.do(outText)
                #    resText, resApi = azureAPI.vocalize(outText=outText_kana, outLang=outLang, outFile=tempFileMp3, )
                #    if (resText != ''):
                #        resText = outText
                #else:
                #    resText, resApi = azureAPI.vocalize(outText=outText, outLang=outLang, outFile=tempFileMp3, )
                resText, resApi = azureAPI.vocalize(outText=outText, outLang=outLang, outFile=tempFileMp3, )
                if (resText != ''):
                    if (tempFileMp3[-4:].lower() == outFile[-4:].lower()):
                        qFunc.copy(tempFileMp3, outFile)
                    else:
                        sox = subprocess.Popen(['sox', '-q', tempFileMp3, outFile, ], \
                              shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                        sox.wait()
                        sox.terminate()
                        sox = None
            if (resText == '') and (apiRecovery == True):
                api  = 'free'

        if (resText == '') and (api == 'aws'):
            awsAPI = aws_api.SpeechAPI()
            key_id     = aws_key.getkey('tts', 'key_id',     )
            secret_key = aws_key.getkey('tts', 'secret_key', )
            res   = awsAPI.authenticate('tts', key_id, secret_key, )
            if (res == True):
                #if (outLang == 'ja') and (kakasi_api == True):
                #    outText_kana = kakasi_cv.do(outText)
                #    resText, resApi = awsAPI.vocalize(outText=outText_kana, outLang=outLang, outFile=tempFileMp3, )
                #    if (resText != ''):
                #        resText = outText
                #else:
                #    resText, resApi = awsAPI.vocalize(outText=outText, outLang=outLang, outFile=tempFileMp3, )
                resText, resApi = awsAPI.vocalize(outText=outText, outLang=outLang, outFile=tempFileMp3, )
                if (resText != ''):
                    if (tempFileMp3[-4:].lower() == outFile[-4:].lower()):
                        qFunc.copy(tempFileMp3, outFile)
                    else:
                        sox = subprocess.Popen(['sox', '-q', tempFileMp3, outFile, ], \
                              shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                        sox.wait()
                        sox.terminate()
                        sox = None
            if (resText == '') and (apiRecovery == True):
                api  = 'free'

        if (resText == '') and (api == 'winos'):
            winosAPI = winos_api.SpeechAPI()
            res = winosAPI.authenticate()
            if (res == True):
                #if (outLang == 'ja') and (kakasi_api == True):
                #    outText_kana = kakasi_cv.do(outText)
                #    resText, resApi = winosAPI.vocalize(outText=outText_kana, outLang=outLang, outFile=tempFileWav, )
                #    if (resText != ''):
                #        resText = outText
                #else:
                #    resText, resApi = winosAPI.vocalize(outText=outText, outLang=outLang, outFile=tempFileWav, )
                resText, resApi = winosAPI.vocalize(outText=outText, outLang=outLang, outFile=tempFileWav, )
                if (resText != ''):
                    if (tempFileWav[-4:].lower() == outFile[-4:].lower()):
                        qFunc.copy(tempFileWav, outFile)
                    else:
                        sox = subprocess.Popen(['sox', '-q', tempFileWav, outFile, ], \
                              shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                        sox.wait()
                        sox.terminate()
                        sox = None
            if (resText == '') and (apiRecovery == True):
                api  = 'free'

        if (resText == '') and (api == 'macos'):
            macosAPI = macos_api.SpeechAPI()
            res = macosAPI.authenticate()
            if (res == True):
                #if (outLang == 'ja') and (kakasi_api == True):
                #    outText_kana = kakasi_cv.do(outText)
                #    resText, resApi = macosAPI.vocalize(outText=outText_kana, outLang=outLang, outFile=tempFileWav, )
                #    if (resText != ''):
                #        resText = outText
                #else:
                #    resText, resApi = macosAPI.vocalize(outText=outText, outLang=outLang, outFile=tempFileWav, )
                resText, resApi = macosAPI.vocalize(outText=outText, outLang=outLang, outFile=tempFileWav, )
                if (resText != ''):
                    if (tempFileWav[-4:].lower() == outFile[-4:].lower()):
                        qFunc.copy(tempFileWav, outFile)
                    else:
                        sox = subprocess.Popen(['sox', '-q', tempFileWav, outFile, ], \
                              shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                        sox.wait()
                        sox.terminate()
                        sox = None
            if (resText == '') and (apiRecovery == True):
                api  = 'free'

        if (resText == '') and (api == 'hoya'):
            hoyaAPI = hoya_api.SpeechAPI()
            res = hoyaAPI.authenticate(hoya_key.getkey(), )
            if (res == True):
                #if (outLang == 'ja') and (kakasi_api == True):
                #    outText_kana = kakasi_cv.do(outText)
                #    resText, resApi = hoyaAPI.vocalize(outText=outText_kana, outLang=outLang, outFile=tempFileWav, )
                #    if (resText != ''):
                #        resText = outText
                #else:
                #    resText, resApi = hoyaAPI.vocalize(outText=outText, outLang=outLang, outFile=tempFileWav, )
                resText, resApi = hoyaAPI.vocalize(outText=outText, outLang=outLang, outFile=tempFileWav, )
                if (resText != ''):
                    if (tempFileWav[-4:].lower() == outFile[-4:].lower()):
                        qFunc.copy(tempFileWav, outFile)
                    else:
                        sox = subprocess.Popen(['sox', '-q', tempFileWav, outFile, ], \
                              shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                        sox.wait()
                        sox.terminate()
                        sox = None
            if (resText == '') and (apiRecovery == True):
                api  = 'free'

        if (resText == '') and (api == 'free') and (useApi != 'free'):
                #if (outLang == 'ja') and (kakasi_api == True):
                #    outText_kana = kakasi_cv.do(outText)
                #    res = qVoiceOutput_fromCache(useApi=api, outLang=outLang, outText=outText_kana, outFile=outFile,)
                #else:
                #    res = qVoiceOutput_fromCache(useApi=api, outLang=outLang, outText=outText, outFile=outFile,)
                res = qVoiceOutput_fromCache(useApi=api, outLang=outLang, outText=outText, outFile=outFile,)
                if (res == True):
                    resText = outText
                    resApi  = api
                    apirun  = False

        if (resText == '') and (api == 'google' or api == 'free'):
            googleAPI = google_api.SpeechAPI()
            res = googleAPI.authenticate('tts', google_key.getkey('tts'), )
            if (res == True):
                if (api == 'google'):
                    #if (outLang == 'ja') and (kakasi_api == True):
                    #    outText_kana = kakasi_cv.do(outText)
                    #    resText, resApi = googleAPI.vocalize(outText=outText_kana, outLang=outLang, outFile=tempFileMp3, api='auto', )
                    #    if (resText != ''):
                    #        resText = outText
                    #else:
                    #    resText, resApi = googleAPI.vocalize(outText=outText, outLang=outLang, outFile=tempFileMp3, api='auto', )
                    resText, resApi = googleAPI.vocalize(outText=outText, outLang=outLang, outFile=tempFileMp3, api='auto', )
                else:
                    #if (outLang == 'ja') and (kakasi_api == True):
                    #    outText_kana = kakasi_cv.do(outText)
                    #    resText, resApi = googleAPI.vocalize(outText=outText_kana, outLang=outLang, outFile=tempFileMp3, api='free', )
                    #    if (resText != ''):
                    #        resText = outText
                    #else:
                    #    resText, resApi = googleAPI.vocalize(outText=outText, outLang=outLang, outFile=tempFileMp3, api='free', )
                    resText, resApi = googleAPI.vocalize(outText=outText, outLang=outLang, outFile=tempFileMp3, api='free', )
                if (resText != ''):
                    if (tempFileMp3[-4:].lower() == outFile[-4:].lower()):
                        qFunc.copy(tempFileMp3, outFile)
                    else:
                        sox = subprocess.Popen(['sox', '-q', tempFileMp3, outFile, ], \
                              shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                        sox.wait()
                        sox.terminate()
                        sox = None

    if (apirun == True):
        if (resText != ''):
            if (resApi == 'google' or resApi == 'free' or resApi == 'watson'):
                qVoiceOutput_toCache(useApi=resApi, outLang=outLang, outText=resText, tempFile=tempFileMp3,)
            else:
                qVoiceOutput_toCache(useApi=resApi, outLang=outLang, outText=resText, tempFile=tempFileWav,)

    try:
        if (os.path.exists(tempFileWav)):
            os.remove(tempFileWav)
        if (os.path.exists(tempFileMp3)):
            os.remove(tempFileMp3)
    except Exception as e:
        pass

    if (resText != ''):
        return resText, resApi

    return '', ''



def speech_batch(runMode, micDev,
                qApiInp, qApiTrn, qApiOut, qLangInp, qLangTrn, qLangTxt, qLangOut,
                procId, fileId,
                inpInput, inpOutput, trnInput, trnOutput, txtInput, txtOutput, outInput, outOutput,
                inpPlay, txtPlay, outPlay,  ):

    # 共通クラス
    qRiKi = _v6__qRiKi.qRiKi_class()
    qRiKi.init()
    qFunc = _v6__qFunc.qFunc_class()
    qFunc.init()

    # ログ
    nowTime  = datetime.datetime.now()
    filename = qPath_log + nowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
    qLog2  = _v6__qLog.qLog_class()
    qLog2.init(mode='logger', filename=filename, display=False, outfile=True, )

    # 設定

    qFunc.remove(qCtrl_result_speech      )
    qFunc.remove(qCtrl_recognize          )
    qFunc.remove(qCtrl_recognize_sjis     )
    qFunc.remove(qCtrl_translate          )
    qFunc.remove(qCtrl_translate_sjis     )

    inpRun  = False
    inpText = ''
    txtRun  = False
    txtText = ''
    txtWork = ''
    trnRun  = False
    trnIn   = ''
    trnText = ''
    outRun  = False

    # STT 処理

    if (inpInput != '' and os.path.exists(inpInput)):
        nowTime = datetime.datetime.now()
        stamp   = nowTime.strftime('%Y%m%d')
        recfile = qPath_rec + fileId + '.stt.mp3'

        inpRun   = True
        inpText  = ''



        if (qFunc.statusCheck(qBusy_dev_com) == True) \
        or (qApiInp == 'julius'):

            api = 'julius'
            waitfile = qPath_s_jul + fileId + '.txt'
            #print(waitfile)

            chktime = time.time()
            while ((time.time() - chktime) < 5):
                if (os.path.exists(waitfile)):

                    res_txts, res_text = qFunc.txtsRead(waitfile, encoding='utf-8', exclusive=False, )
                    if (res_txts != False):
                        inpText = res_text
                    break
                time.sleep(0.05)



        if  (qFunc.statusCheck(qBusy_dev_com) == False) \
        and (qApiInp != 'julius'):

            soxMsg1  = ''
            soxMsg2  = ''
            soxMsg3  = ''

            wrkApi   = 'free'
            if (qApiInp == 'google'):
                wrkApi = 'google8k'

            fseq = '00' + str(procId)

            wrkfile    = qPath_work + fseq[-2:]
            wrkfile_0  = wrkfile + '_input_0.wav'
            wrkfile_0s = wrkfile + '_input_0s.wav'
            wrkfile_1  = wrkfile + '_input_1.wav'
            wrkfile_1s = wrkfile + '_input_1s.wav'
            wrkfile_2  = wrkfile + '_input_2.wav'
            wrkfile_2s = wrkfile + '_input_2s.wav'
            wrkfile_x1 = wrkfile + '_input_x1.wav'
            wrkfile_x2 = wrkfile + '_input_x2.wav'
            wrkfile_y1 = wrkfile + '_input_y1.wav'
            wrkfile_y2 = wrkfile + '_input_y2.wav'
            wrkfile_y3 = wrkfile + '_input_y3.wav'
            wrkfile_y4 = wrkfile + '_input_y4.wav'
            wrkfile_y5 = wrkfile + '_input_y5.wav'
            wrkfile_y6 = wrkfile + '_input_y6.wav'
            wrkfile    = ''

            sox_0  = subprocess.Popen(['sox', '-q', inpInput, wrkfile_0, ], \
                     shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
            sox_0s = subprocess.Popen(['sox', '-q', inpInput, wrkfile_0s, \
                     'silence', '1', '0.5', '0.2%', '1', '0.5', '0%', ':restart', ], \
                     shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
            sox_1  = subprocess.Popen(['sox', '-q', inpInput, wrkfile_1,  '--norm', ], \
                     shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
            sox_1s = subprocess.Popen(['sox', '-q', inpInput, wrkfile_1s, '--norm', \
                     'silence', '1', '0.5', '0.2%', '1', '0.5', '0%', ':restart', ], \
                     shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
            sox_2  = subprocess.Popen(['sox', '-q', inpInput, wrkfile_2,  'gain', '+12', ], \
                     shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
            sox_2s = subprocess.Popen(['sox', '-q', inpInput, wrkfile_2s, 'gain', '+12', \
                     'silence', '1', '0.5', '0.2%', '1', '0.5', '0.1%', ':restart', ], \
                     shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

            sox_0.wait()
            sox_0.terminate()
            sox_0 = None
            if (os.path.exists(wrkfile_0)):
                inpTextX,api = qVoiceInput(wrkApi, qLangInp, wrkfile_0, False, )
                if (runMode == 'debug'):
                    qLog2.log('debug', '   ' + procId, '[' + inpText + '](' + wrkApi + ') step1 normal wav ', display=True)

                if (inpTextX != '' and inpTextX != '!') and (len(inpTextX) > len(inpText)):
                    inpText = inpTextX
                    soxMsg1 = ''
                    wrkfile  = wrkfile_0

            sox_0s.wait()
            sox_0s.terminate()
            sox_0s = None
            if (os.path.exists(wrkfile_0s)):
                #if (not micDev.isdigit()) or (runMode == 'debug') \
                #or (inpText == '') or (inpText == '!'):
                if (not micDev.isdigit()) or (runMode == 'debug'):
                    inpTextX,api = qVoiceInput(wrkApi, qLangInp, wrkfile_0s, False, )
                    if (runMode == 'debug'):
                        qLog2.log('debug', '   ' + procId, '[' + inpTextX + '](' + wrkApi + ') step1 sox silence 0.5s 0%', display=True)

                    if (inpTextX != '' and inpTextX != '!') and (len(inpTextX) > len(inpText)):
                        inpText = inpTextX
                        soxMsg1 = '< silence 0.5s 0% '
                        wrkfile  = wrkfile_0s

            sox_1.wait()
            sox_1.terminate()
            sox_1 = None
            if (os.path.exists(wrkfile_1)):
                #if (not micDev.isdigit()) or (runMode == 'debug') \
                #or (inpText == '') or (inpText == '!'):
                if (not micDev.isdigit()) or (runMode == 'debug'):
                    inpTextX,api = qVoiceInput(wrkApi, qLangInp, wrkfile_1, False, )
                    if (runMode == 'debug'):
                        qLog2.log('debug', '   ' + procId, '[' + inpTextX + '](' + wrkApi + ') step1 --norm', display=True)

                    if (inpTextX != '' and inpTextX != '!') and (len(inpTextX) > len(inpText)):
                        inpText = inpTextX
                        soxMsg1 = '< --norm '
                        wrkfile  = wrkfile_1

            sox_1s.wait()
            sox_1s.terminate()
            sox_1s = None
            if (os.path.exists(wrkfile_1s)):
                if (not micDev.isdigit()) or (runMode == 'debug') \
                or (inpText == '') or (inpText == '!'):
                    inpTextX,api = qVoiceInput(wrkApi, qLangInp, wrkfile_1s, False, )
                    if (runMode == 'debug'):
                        qLog2.log('debug', '   ' + procId, '[' + inpTextX + '](' + wrkApi + ') step1 --norm silence 0.5s 0%', display=True)

                    if (inpTextX != '' and inpTextX != '!') and (len(inpTextX) > len(inpText)):
                        inpText = inpTextX
                        soxMsg1 = '< --norm silence 0.5s 0% '
                        wrkfile  = wrkfile_1s

            sox_2.wait()
            sox_2.terminate()
            sox_2 = None
            if (os.path.exists(wrkfile_2)):
                #if (not micDev.isdigit()) or (runMode == 'debug') \
                #or (inpText == '') or (inpText == '!'):
                if (not micDev.isdigit()) or (runMode == 'debug'):
                    inpTextX,api = qVoiceInput(wrkApi, qLangInp, wrkfile_2, False, )
                    if (runMode == 'debug'):
                        qLog2.log('debug', '   ' + procId, '[' + inpTextX + '](' + wrkApi + ') step1 gain +12', display=True)

                    if (inpTextX != '' and inpTextX != '!') and (len(inpTextX) > len(inpText)):
                        inpText = inpTextX
                        soxMsg1 = '< gain +12 '
                        wrkfile  = wrkfile_2

            sox_2s.wait()
            sox_2s.terminate()
            sox_2s = None
            if (os.path.exists(wrkfile_2s)):
                #if (not micDev.isdigit()) or (runMode == 'debug') \
                #or (inpText == '') or (inpText == '!'):
                if (not micDev.isdigit()) or (runMode == 'debug'):
                    inpTextX,api = qVoiceInput(wrkApi, qLangInp, wrkfile_2s, False, )
                    if (runMode == 'debug'):
                        qLog2.log('debug', '   ' + procId, '[' + inpTextX + '](' + wrkApi + ') step1 gain +12 silence 0.5s 0.1%', display=True)

                    if (inpTextX != '' and inpTextX != '!') and (len(inpTextX) > len(inpText)):
                        inpText = inpTextX
                        soxMsg1 = '< gain +12 silence 0.5s 0.1% '
                        wrkfile  = wrkfile_2s

            if (wrkfile == ''):
                wrkfile  = wrkfile_0

            if (os.path.exists(wrkfile)):
                if (not micDev.isdigit()) or (runMode == 'debug'):

                    sox_x1 = subprocess.Popen(['sox', '-q', wrkfile, wrkfile_x1, \
                             'silence', '1', '0.3', '0.5%', '1', '0.3', '0.5%', ':restart', ], \
                             shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                    sox_x2 = subprocess.Popen(['sox', '-q', wrkfile, wrkfile_x2, \
                             'silence', '1', '0.3', '1%', '1', '0.3', '1%', ':restart', ], \
                             shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

                    sox_x1.wait()
                    sox_x1.terminate()
                    sox_x1 = None
                    if (os.path.exists(wrkfile_x1)):
                        inpTextX,api = qVoiceInput(wrkApi, qLangInp, wrkfile_x1, False, )
                        if (runMode == 'debug'):
                            qLog2.log('debug', '   ' + procId, '[' + inpTextX + '](' + wrkApi + ') step2 silence 0.3s 0.5%', display=True)

                        if (inpTextX != '' and inpTextX != '!') and (len(inpTextX) > len(inpText)):
                            inpText = inpTextX
                            soxMsg2 = '< silence 0.3s 0.5% '
                            wrkfile  = wrkfile_x1

                    sox_x2.wait()
                    sox_x2.terminate()
                    sox_x2 = None
                    if (os.path.exists(wrkfile_x2)):
                        inpTextX,api = qVoiceInput(wrkApi, qLangInp, wrkfile_x2, False, )
                        if (runMode == 'debug'):
                            qLog2.log('debug', '   ' + procId, '[' + inpTextX + '](' + wrkApi + ') step2 silence 0.3s 1.0%', display=True)

                        if (inpTextX != '' and inpTextX != '!') and (len(inpTextX) > len(inpText)):
                            inpText = inpTextX
                            soxMsg2 = '< silence 0.3s 1.0% '
                            wrkfile  = wrkfile_x2

            if (os.path.exists(wrkfile)):
                if (not micDev.isdigit()) or (runMode == 'debug'):

                    sox_y1 = subprocess.Popen(['sox', '-q', wrkfile, wrkfile_y1, \
                             'highpass', '50', ], \
                             shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                    sox_y2 = subprocess.Popen(['sox', '-q', wrkfile, wrkfile_y2, \
                             'equalizer', '500', '1.0q', '3', ], \
                             shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                    sox_y3 = subprocess.Popen(['sox', '-q', wrkfile, wrkfile_y3, \
                             'highpass', '50', 'equalizer', '500', '1.0q', '3', ], \
                             shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                    sox_y4 = subprocess.Popen(['sox', '-q', wrkfile, wrkfile_y4, \
                             'treble', '+2', ], \
                             shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                    sox_y5 = subprocess.Popen(['sox', '-q', wrkfile, wrkfile_y5, \
                             'highpass', '50', 'treble', '+2', ], \
                             shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                    sox_y6 = subprocess.Popen(['sox', '-q', wrkfile, wrkfile_y6, \
                             'highpass', '50', 'equalizer', '500', '1.0q', '3', 'treble', '+2', ], \
                             shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

                    sox_y1.wait()
                    sox_y1.terminate()
                    sox_y1 = None
                    if (os.path.exists(wrkfile_y1)):
                        inpTextX,api = qVoiceInput(wrkApi, qLangInp, wrkfile_y1, False, )
                        if (runMode == 'debug'):
                            qLog2.log('debug', '   ' + procId, '[' + inpTextX + '](' + wrkApi + ') step3 highpass 50', display=True)

                        if (inpTextX != '' and inpTextX != '!') and (len(inpTextX) > len(inpText)):
                            inpText = inpTextX
                            soxMsg3 = '< highpass 50 '
                            wrkfile  = wrkfile_y1

                    sox_y2.wait()
                    sox_y2.terminate()
                    sox_y2 = None
                    if (os.path.exists(wrkfile_y2)):
                        inpTextX,api = qVoiceInput(wrkApi, qLangInp, wrkfile_y2, False, )
                        if (runMode == 'debug'):
                            qLog2.log('debug', '   ' + procId, '[' + inpTextX + '](' + wrkApi + ') step3 equalizer 500 1.0q 3', display=True)

                        if (inpTextX != '' and inpTextX != '!') and (len(inpTextX) > len(inpText)):
                            inpText = inpTextX
                            soxMsg3 = '< equalizer 500 1.0q 3 '
                            wrkfile  = wrkfile_y2

                    sox_y3.wait()
                    sox_y3.terminate()
                    sox_y3 = None
                    if (os.path.exists(wrkfile_y3)):
                        inpTextX,api = qVoiceInput(wrkApi, qLangInp, wrkfile_y3, False, )
                        if (runMode == 'debug'):
                            qLog2.log('debug', '   ' + procId, '[' + inpTextX + '](' + wrkApi + ') step3 highpass + equalizer', display=True)

                        if (inpTextX != '' and inpTextX != '!') and (len(inpTextX) > len(inpText)):
                            inpText = inpTextX
                            soxMsg3 = '< highpass + equalizer '
                            wrkfile  = wrkfile_y3

                    sox_y4.wait()
                    sox_y4.terminate()
                    sox_y4 = None
                    if (os.path.exists(wrkfile_y4)):
                        inpTextX,api = qVoiceInput(wrkApi, qLangInp, wrkfile_y4, False, )
                        if (runMode == 'debug'):
                            qLog2.log('debug', '   ' + procId, '[' + inpTextX + '](' + wrkApi + ') step3 treble +2', display=True)

                        if (inpTextX != '' and inpTextX != '!') and (len(inpTextX) > len(inpText)):
                            inpText = inpTextX
                            soxMsg3 = '< treble +2 '
                            wrkfile  = wrkfile_y4

                    sox_y5.wait()
                    sox_y5.terminate()
                    sox_y5 = None
                    if (os.path.exists(wrkfile_y5)):
                        inpTextX,api = qVoiceInput(wrkApi, qLangInp, wrkfile_y5, False, )
                        if (runMode == 'debug'):
                            qLog2.log('debug', '   ' + procId, '[' + inpTextX + '](' + wrkApi + ') step3 highpass + treble', display=True)

                        if (inpTextX != '' and inpTextX != '!') and (len(inpTextX) > len(inpText)):
                            inpText = inpTextX
                            soxMsg3 = '< highpass + treble '
                            wrkfile  = wrkfile_y5

                    sox_y6.wait()
                    sox_y6.terminate()
                    sox_y6 = None
                    if (os.path.exists(wrkfile_y6)):
                        inpTextX,api = qVoiceInput(wrkApi, qLangInp, wrkfile_y6, False, )
                        if (runMode == 'debug'):
                            qLog2.log('debug', '   ' + procId, '[' + inpTextX + '](' + wrkApi + ') step3 highpass + equalizer + treble', display=True)

                        if (inpTextX != '' and inpTextX != '!') and (len(inpTextX) > len(inpText)):
                            inpText = inpTextX
                            soxMsg3 = '< highpass + equalizer + treble '
                            wrkfile  = wrkfile_y6

            if (wrkfile[-4:].lower() == recfile[-4:].lower()):
                qFunc.copy(wrkfile, recfile)
            else:
                sox = subprocess.Popen(['sox', '-q', wrkfile, recfile, ], \
                      shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                sox.wait()
                sox.terminate()
                sox = None

            if (inpPlay == 'on' or inpPlay == 'yes'):
                sox = subprocess.Popen(['sox', '-q', recfile, '-d', '--norm', ], \
                      shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                sox.wait()
                sox.terminate()
                sox = None

            if  ((wrkApi == 'free') or (wrkApi == 'google8k')) \
            and ((qApiInp != 'free') and (qApiInp != 'google')) \
            or  ((wrkApi != 'free') or (wrkApi != 'google8k')) and (qApiInp != wrkApi):
                if (os.path.exists(wrkfile)):

                    #inpTextX,api = qVoiceInput(qApiInp, qLangInp, wrkfile, False, )
                    inpTextX,api = qVoiceInput(qApiInp, qLangInp, wrkfile, )
                    if (inpTextX != '' and inpTextX != '!'):
                        inpText = inpTextX
                    else:
                        api = wrkApi

            if (os.path.exists(wrkfile_0)):
                os.remove(wrkfile_0)
            if (os.path.exists(wrkfile_0s)):
                os.remove(wrkfile_0s)
            if (os.path.exists(wrkfile_1)):
                os.remove(wrkfile_1)
            if (os.path.exists(wrkfile_1s)):
                os.remove(wrkfile_1s)
            if (os.path.exists(wrkfile_2)):
                os.remove(wrkfile_2)
            if (os.path.exists(wrkfile_2s)):
                os.remove(wrkfile_2s)
            if (os.path.exists(wrkfile_x1)):
                os.remove(wrkfile_x1)
            if (os.path.exists(wrkfile_x2)):
                os.remove(wrkfile_x2)
            if (os.path.exists(wrkfile_y1)):
                os.remove(wrkfile_y1)
            if (os.path.exists(wrkfile_y2)):
                os.remove(wrkfile_y2)
            if (os.path.exists(wrkfile_y3)):
                os.remove(wrkfile_y3)
            if (os.path.exists(wrkfile_y4)):
                os.remove(wrkfile_y4)
            if (os.path.exists(wrkfile_y5)):
                os.remove(wrkfile_y5)
            if (os.path.exists(wrkfile_y6)):
                os.remove(wrkfile_y6)

            if (inpText != '' and inpText != '!') and (soxMsg1 != '' or soxMsg2 != '' or soxMsg3 != ''):
                qLog2.log('debug', '   ' + procId, 'Recognition  <<<<' + soxMsg3 + soxMsg2 + soxMsg1 + '<<<<< wav', display=True)



        if (inpText != '') and (qLangInp == 'ja'):
            inpText = inpText.replace('　', '')
            inpText = inpText.replace( ' ', '')

        if (inpText == ''):
            inpText = '!'

        if (api == qApiInp) or (api == 'free' and qApiInp == 'google'):
                qLog2.log('info', '   ' + procId, 'Recognition  [' + inpText + '] ' + qLangInp + ' (' + api + ')', display=True)
        else:
            if (api != ''):
                qLog2.log('info', '   ' + procId, 'Recognition  [' + inpText + '] ' + qLangInp + ' (!' + api + ')', display=True)
            else:
                qLog2.log('info', '   ' + procId, 'Recognition  [' + inpText + '] ' + qLangInp + ' (!' + qApiInp + ')', display=True)

        if (inpText != '' and inpText != '!'):
            if (not inpText.isdigit()):
                numText = inpText
                if (len(inpText) <= 10):
                    try:
                        numText = qFunc.strkan2num(inpText)
                        numText.replace('零', '0')
                        if (not numText.isdigit()):
                            numText = inpText
                    except Exception as e:
                        pass
                if (numText != inpText):
                    qLog2.log('info', '   ' + procId, 'Recognition  [' + inpText + '] → [' + numText + ']', display=True)
                    inpText = str(numText)
                else:
                    if (runMode == 'number'):
                        numText = inpText
                        numText = numText.replace('ゼロ', '0')
                        numText = numText.replace('０',   '0')
                        numText = numText.replace('１',   '1')
                        numText = numText.replace('２',   '2')
                        numText = numText.replace('３',   '3')
                        numText = numText.replace('４',   '4')
                        numText = numText.replace('５',   '5')
                        numText = numText.replace('６',   '6')
                        numText = numText.replace('７',   '7')
                        numText = numText.replace('８',   '8')
                        numText = numText.replace('９',   '9')
                        numText = numText.replace('。', '')
                        numText = numText.replace('．', '.')
                        numText = numText.replace('　', '')
                        numText = numText.replace(' ', '')
                        numText = numText.replace(',', '')
                        if (numText[-1:] == '.'):
                            numText=numText[:-1]
                        if (numText != inpText and numText.isdigit()):
                            qLog2.log('info', '   ' + procId, 'Recognition  [' + inpText + '] → [' + numText + ']', display=True)
                            inpText = str(numText)



    # 外部プログラム
    if (inpText != '' and inpText != '!'):

        if (runMode == 'debug') \
        or (runMode == 'reception'):
            if (os.name == 'nt'):
                if (os.path.exists(qExt_speech)):
                    filePath = os.path.dirname(inpInput)
                    fileName = os.path.basename(inpInput)
                    ext_speech = subprocess.Popen([qExt_speech, filePath, fileName, inpText, ], )
                                 #shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

    # STT 結果出力

    if (inpOutput != '' and inpText != ''):

        if  (qFunc.statusCheck(qRdy__s_force) != True) \
        and (qFunc.statusCheck(qRdy__s_fproc) != True):
            qFunc.txtsWrite(inpOutput, txts=[inpText], encoding='utf-8', exclusive=False, mode='w', )

        if (inpText != '' and inpText != '!'):
            txt = qLangInp + ', [' + inpText + ']'
            qFunc.txtsWrite(qCtrl_recognize     , txts=[txt], encoding='utf-8', exclusive=True, mode='w', )
            qFunc.txtsWrite(qCtrl_recognize_sjis, txts=[txt], encoding='shift_jis', exclusive=True, mode='w', )

            filename = inpOutput.replace(qPath_s_STT, '')
            filename = filename.replace(qPath_s_TRA, '')
            filename = filename.replace(qPath_s_TTS, '')
            filename = filename.replace(qPath_work, '')

            filename1 = qPath_s_ctrl + filename
            qFunc.txtsWrite(filename1, txts=[inpText], encoding='utf-8', exclusive=False, mode='w', )
            filename2 = qPath_v_ctrl + filename
            qFunc.txtsWrite(filename2, txts=[inpText], encoding='utf-8', exclusive=False, mode='w', )
            filename3 = qPath_d_ctrl + filename
            qFunc.txtsWrite(filename3, txts=[inpText], encoding='utf-8', exclusive=False, mode='w', )
            if (runMode == 'chatbot'):
                filename4 = qPath_s_chat + filename
                qFunc.txtsWrite(filename4, txts=[inpText], encoding='utf-8', exclusive=False, mode='w', )

        nowTime = datetime.datetime.now()
        stamp   = nowTime.strftime('%Y%m%d')
        recfile = qPath_rec + fileId + '.stt.txt'
        recutf8 = qPath_rec + '_' + stamp + '_stt_utf8.txt'
        recsjis = qPath_rec + '_' + stamp + '_stt_sjis.txt'

        qFunc.txtsWrite(recfile, txts=[inpText], encoding='utf-8', exclusive=False, mode='w', )
        qFunc.txtsWrite(recutf8, txts=[inpText], encoding='utf-8', exclusive=False, mode='a', )
        qFunc.txtsWrite(recsjis, txts=[inpText], encoding='shift_jis', exclusive=False, mode='a', )



    # TRA 処理

    if (trnInput != ''):
        trnRun   = True
        trnIn    = ''
        trnText  = ''
        trnMulti = []

        if (trnInput == inpOutput ):
            trnIn = inpText
        else:
            res, trnIn = qFunc.txtsRead(trnInput, encoding='utf-8', exclusive=False, )

        while (trnIn[:3] == 'ja,' or trnIn[:3] == 'en,'):
            trnIn = trnIn[3:]

        if (trnIn == ''):
            trnIn = '!'

        if (trnIn != '!'):
            if (inpInput == ''):
                                    qLog2.log('info', '   ' + procId, 'Text Input   [' + trnIn + '] ' + qLangInp, display=True)
            langs = qLangTrn.split(',')
            for lang in langs:
                lang = str(lang).strip()
                if (lang != ''):
                    trnRes,api = qTranslator(qApiTrn, qLangInp, lang, trnIn, )
                    if (trnRes != '' and trnRes != '!'):
                        if (api == qApiTrn) or (api == 'free' and qApiTrn == 'google'):
                                if (inpInput != ''):
                                    qLog2.log('info', '   ' + procId, 'Translation  [' + trnRes + '] ' + lang + ' (' + api + ')', display=True)
                                else:
                                    qLog2.log('info', '   ' + procId, 'Text Trans   [' + trnRes + '] ' + lang + ' (' + api + ')', display=True)
                        else:
                            if (api != ''):
                                if (inpInput != ''):
                                    qLog2.log('info', '   ' + procId, 'Translation  [' + trnRes + '] ' + lang + ' (!' + api + ')', display=True)
                                else:
                                    qLog2.log('info', '   ' + procId, 'Text Trans   [' + trnRes + '] ' + lang + ' (!' + api + ')', display=True)
                            else:
                                if (inpInput != ''):
                                    qLog2.log('info', '   ' + procId, 'Translation  [' + trnRes + '] ' + lang + ' (!' + qApiTrn + ')', display=True)
                                else:
                                    qLog2.log('info', '   ' + procId, 'Text Trans   [' + trnRes + '] ' + lang + ' (!' + qApiTrn + ')', display=True)

                    if (trnRes == ''):
                        trnRes = '!'

                    if (trnRes != '' and trnRes != '!') and (runMode == 'number'):
                        numtxt = trnRes.lower()
                        numtxt = numtxt.replace('０', '0')
                        numtxt = numtxt.replace('zero', '0')
                        numtxt = numtxt.replace('one', '1')
                        numtxt = numtxt.replace('two', '2')
                        numtxt = numtxt.replace('three', '3')
                        numtxt = numtxt.replace('four', '4')
                        numtxt = numtxt.replace('five', '5')
                        numtxt = numtxt.replace('six', '6')
                        numtxt = numtxt.replace('seven', '7')
                        numtxt = numtxt.replace('eight', '8')
                        numtxt = numtxt.replace('nine', '9')
                        numtxt = numtxt.replace('。', '')
                        numtxt = numtxt.replace('．', '.')
                        numtxt = numtxt.replace('　', '')
                        numtxt = numtxt.replace(' ', '')
                        numtxt = numtxt.replace(',', '')
                        if (numtxt[-1:] == '.'):
                            numtxt=numtxt[:-1]
                        if (numtxt != trnRes and numtxt.isdigit()):
                            qLog2.log('info', '   ' + procId, 'Translation  [' + trnRes + '] → [' + numtxt + ']', display=True)
                            trnRes = str(numtxt)

                    trnMulti.append({'lang':lang, 'text':trnRes, 'api':api,})
                    if (lang == qLangTrn[:2]):
                        trnText = trnRes



    # TRA 結果出力

    if (trnOutput != '' and trnText != ''):
        qFunc.txtsWrite(trnOutput, txts=[trnText], encoding='utf-8', exclusive=False, mode='w', )

        if  (qFunc.statusCheck(qRdy__s_force) != True) \
        and (qFunc.statusCheck(qRdy__s_fproc) != True):
            for trnRes in trnMulti:
                filename = trnOutput
                filename = filename.replace('.'+qLangTrn[:2]+'.', '.'+trnRes['lang']+'.')
                if (filename != trnOutput):
                    txt = trnRes['text']
                    qFunc.txtsWrite(filename, txts=[txt], encoding='utf-8', exclusive=False, mode='w', )

        if (trnText != '' and trnText != '!'):
            #txt = qLangTrn[:2] + ', [' + trnText + ']'
            #qFunc.txtsWrite(qCtrl_translate,      txts=[txt], encoding='utf-8', exclusive=True, mode='w', )
            #qFunc.txtsWrite(qCtrl_translate_sjis, txts=[txt], encoding='shift_jis', exclusive=True, mode='w', )

            txts = []
            for trnRes in trnMulti:
                txts.append(trnRes['lang'] + ', [' + trnRes['text'] + ']')

            qFunc.txtsWrite(qCtrl_translate,      txts=txts, encoding='utf-8', exclusive=True, mode='w', )
            qFunc.txtsWrite(qCtrl_translate_sjis, txts=txts, encoding='shift_jis', exclusive=True, mode='w', )

            for trnRes in trnMulti:
                filename = trnOutput
                filename = filename.replace('.'+qLangTrn[:2]+'.', '.'+trnRes['lang']+'.')
                if (filename != trnOutput):
                    txt = trnRes['text']
                    qFunc.txtsWrite(filename, txts=[txt], encoding='utf-8', exclusive=False, mode='w', )

            #filename = trnOutput.replace(qPath_s_STT, '')
            #filename = filename.replace(qPath_s_TRA, '')
            #filename = filename.replace(qPath_s_TTS, '')
            #filename = filename.replace(qPath_work, '')

            #filename1 = qPath_s_ctrl + filename
            #qFunc.txtsWrite(filename1, txts=[trnText], encoding='utf-8', exclusive=False, mode='w', )
            #filename2 = qPath_v_ctrl + filename
            #qFunc.txtsWrite(filename2, txts=[trnText], encoding='utf-8', exclusive=False, mode='w', )
            #filename3 = qPath_d_ctrl + filename
            #qFunc.txtsWrite(filename3, txts=[trnText], encoding='utf-8', exclusive=False, mode='w', )

        if (inpInput != ''):
            nowTime = datetime.datetime.now()
            stamp   = nowTime.strftime('%Y%m%d')
            recfile = qPath_rec + fileId + '.translate.txt'
            recutf8 = qPath_rec + '_' + stamp + '_translate_utf8.txt'
            recsjis = qPath_rec + '_' + stamp + '_translate_sjis.txt'

            qFunc.txtsWrite(recfile, txts=[trnText], encoding='utf-8', exclusive=False, mode='w', )
            qFunc.txtsWrite(recutf8, txts=[trnText], encoding='utf-8', exclusive=False, mode='a', )
            qFunc.txtsWrite(recutf8, txts=[trnText], encoding='shift_jis', exclusive=False, mode='a', )



    # TTS 処理

    if (txtInput != ''):
        txtRun  = True
        txtText = ''
        txtInpLang = qLangTxt
        txtOutLang = qLangOut
        txtOutApi  = qApiOut

        if (txtInput == inpOutput ):
            txtText = inpText
            txtInpLang = qLangInp
            txtOutLang = qLangOut
            txtOutApi  = qApiOut
        else:
            res, txtText = qFunc.txtsRead(txtInput, encoding='utf-8', exclusive=False, )

        while (txtText[:3] == 'ja,' or txtText[:3] == 'en,'):
            txtInpLang = txtText[:2]
            txtOutLang = txtText[:2]
            txtText = txtText[3:]

        if (txtText[:7] == 'google,'):
            txtOutApi = txtText[:6]
            txtText = txtText[7:]
        if (txtText[:5] == 'free,'):
            txtOutApi = txtText[:4]
            txtText = txtText[5:]
        if (txtText[:7] == 'watson,'):
            txtOutApi = txtText[:6]
            txtText = txtText[7:]
        if (txtText[:6] == 'azure,'):
            txtOutApi = txtText[:5]
            txtText = txtText[6:]
        if (txtText[:4] == 'aws,'):
            txtOutApi = txtText[:3]
            txtText = txtText[4:]
        if (txtText[:6] == 'winos,'):
            txtOutApi = txtText[:5]
            txtText = txtText[6:]
        if (txtText[:6] == 'macos,'):
            txtOutApi = txtText[:5]
            txtText = txtText[6:]
        if (txtText[:5] == 'hoya,'):
            txtOutApi = txtText[:4]
            txtText = txtText[5:]

        #print(txtInpLang, txtOutApi, txtText)

        if (txtText == ''):
            txtText = '!'

        if (True):
            if (txtText != '' and txtText != '!'):
                if (txtInpLang != txtOutLang):
                    qLog2.log('info', '   ' + procId, 'Text Input   [' + txtText + '] ' + txtInpLang, display=True)

                #filename = txtInput.replace(qPath_s_STT, '')
                #filename = filename.replace(qPath_s_TRA, '')
                #filename = filename.replace(qPath_s_TTS, '')
                #filename = filename.replace(qPath_work, '')

                #filename1 = qPath_s_ctrl + filename
                #qFunc.txtsWrite(filename1, txts=[txtText], encoding='utf-8', exclusive=False, mode='w', )

    if (txtText != '' and txtInput != inpOutput):

        nowTime = datetime.datetime.now()
        stamp   = nowTime.strftime('%Y%m%d')
        recfile = qPath_rec + fileId + '.tts.txt'
        recutf8 = qPath_rec + '_' + stamp + '_tts_utf8.txt'
        recsjis = qPath_rec + '_' + stamp + '_tts_sjis.txt'

        qFunc.txtsWrite(recfile, txts=[txtText], encoding='utf-8', exclusive=False, mode='w', )
        qFunc.txtsWrite(recutf8, txts=[txtText], encoding='utf-8', exclusive=False, mode='a', )
        qFunc.txtsWrite(recutf8, txts=[txtText], encoding='shift_jis', exclusive=False, mode='a', )

    if (txtText != ''):
        txtWork = txtText

        if (txtInpLang != txtOutLang):
            txtWork,api = qTranslator(qApiTrn, txtInpLang, txtOutLang, txtText, )
            if (txtWork != '' and txtWork != '!'):
                if (api == qApiTrn) or (api == 'free' and qApiTrn == 'google'):
                        qLog2.log('info', '   ' + procId, 'Text Trans   [' + txtWork + '] ' + txtOutLang + ' (' + api + ')', display=True)
                else:
                    if (api != ''):
                        qLog2.log('info', '   ' + procId, 'Text Trans   [' + txtWork + '] ' + txtOutLang + ' (!' + api + ')', display=True)
                    else:
                        qLog2.log('info', '   ' + procId, 'Text Trans   [' + txtWork + '] ' + txtOutLang + ' (!' + qApiTrn + ')', display=True)

                txt = txtOutLang + ', [' + txtWork + ']'
                qFunc.txtsWrite(qCtrl_translate, txts=[txt], encoding='utf-8', exclusive=True, mode='w', )

        if (txtWork == ''):
            txtWork = '!'



    # TTS 結果出力

    if (txtOutput != '' and txtWork != '!'):

        nowTime = datetime.datetime.now()
        stamp   = nowTime.strftime('%Y%m%d')
        recfile = qPath_rec + fileId + '.tts.mp3'
        if (txtInput == inpOutput ):
            recfile = qPath_rec + fileId + '.feedback.mp3'

        #qLog2.log('info', '   ' + procId, 'Text Vocal   [' + txtWork + '] ' + txtOutLang + ' (' + qApiOut + ')', display=True)
        tmpfile = qPath_work + 'temp_qVoiceOutput.' + fileId + '.mp3'
        #res,api = qVoiceOutput(qApiOut, txtOutLang, txtWork, recfile, tmpfile)
        res,api = qVoiceOutput(txtOutApi, txtOutLang, txtWork, recfile, tmpfile)
        #if (api == qApiOut) or (api == 'free' and qApiOut == 'google'):
        if (api == txtOutApi) or (api == 'free' and txtOutApi == 'google'):
                qLog2.log('info', '   ' + procId, 'Text Vocal   [' + txtWork + '] ' + txtOutLang + ' (' + api + ')', display=True)
        else:
            if (api != ''):
                qLog2.log('info', '   ' + procId, 'Text Vocal   [' + txtWork + '] ' + txtOutLang + ' (!' + api + ')', display=True)
            else:
                qLog2.log('info', '   ' + procId, 'Text Vocal   [' + txtWork + '] ' + txtOutLang + ' (!' + txtOutApi + ')', display=True)

        if (os.path.exists(recfile)):

            if (recfile[-4:].lower() == txtOutput[-4:].lower()):
                qFunc.copy(recfile, txtOutput)
            else:
                sox = subprocess.Popen(['sox', '-q', recfile, txtOutput, ], \
                      shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                sox.wait()
                sox.terminate()
                sox = None

            if (txtPlay == 'on' or txtPlay == 'yes'):
                sox = subprocess.Popen(['sox', '-q', recfile, '-d', '--norm', ], \
                      shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                sox.wait()
                sox.terminate()
                sox = None



    if (outInput != ''):
        outRun  = True
        outText = ''

        if (outInput == inpOutput ):
            outText = inpText
        elif (outInput == trnOutput ):
            outText = trnText
        else:
            res, outText = qFunc.txtsRead(outInput, encoding='utf-8', exclusive=False, )

        if (outText == ''):
            outText = '!'



    if (outOutput != '' and outText != '!'):

        nowTime = datetime.datetime.now()
        stamp   = nowTime.strftime('%Y%m%d')
        if (inpInput != ''):
            recfile = qPath_rec + fileId + '.vocalize.mp3'
            if (outInput == inpOutput ):
                recfile = qPath_rec + fileId + '.feedback.mp3'
            elif (outInput == trnOutput ):
                recfile = qPath_rec + fileId + '.translate.mp3'
        else:
            recfile = qPath_rec + fileId + '.text2vocal.mp3'

        #qLog2.log('info', '   ' + procId, 'Vocalization [' + outText + '] ' + qLangOut + ' (' + qApiOut + ')', display=True)
        tmpfile = qPath_work + 'temp_qVoiceOutput.' + fileId + '.mp3'
        res,api = qVoiceOutput(qApiOut, qLangOut, outText, recfile, tmpfile)
        if (api == qApiOut) or (api == 'free' and qApiOut == 'google'):
                if (inpInput != ''):
                    qLog2.log('info', '   ' + procId, 'Vocalization [' + outText + '] ' + qLangOut + ' (' + api + ')', display=True)
                else:
                    qLog2.log('info', '   ' + procId, 'Text Vocal   [' + outText + '] ' + qLangOut + ' (' + api + ')', display=True)
        else:
            if (api != ''):
                if (inpInput != ''):
                    qLog2.log('info', '   ' + procId, 'Vocalization [' + outText + '] ' + qLangOut + ' (!' + api + ')', display=True)
                else:
                    qLog2.log('info', '   ' + procId, 'Text Vocal   [' + outText + '] ' + qLangOut + ' (!' + api + ')', display=True)
            else:
                if (inpInput != ''):
                    qLog2.log('info', '   ' + procId, 'Vocalization [' + outText + '] ' + qLangOut + ' (!' + qApiOut + ')', display=True)
                else:
                    qLog2.log('info', '   ' + procId, 'Text Vocal   [' + outText + '] ' + qLangOut + ' (!' + qApiOut + ')', display=True)

        if (os.path.exists(recfile)):

            if (recfile[-4:].lower() == outOutput[-4:].lower()):
                qFunc.copy(recfile, outOutput)
            else:
                sox = subprocess.Popen(['sox', '-q', recfile, outOutput, ], \
                      shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                sox.wait()
                sox.terminate()
                sox = None

            if (outPlay == 'on' or outPlay == 'yes'):
                sox = subprocess.Popen(['sox', '-q', recfile, '-d', '--norm', ], \
                      shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                sox.wait()
                sox.terminate()
                sox = None



    def loopback(text, lang='ja,hoya,', idolSec=2, maxWait=15, ):

        xrunMode = 'live'
        xmicDev  = '0'
        xApiInp  = 'free'
        xApiTrn  = 'free'
        xApiOut  = 'free'
        xLangInp = 'ja'
        xLangTrn = 'en'
        xLangTxt = xLangInp
        xLangOut = xLangTrn

        if (True):
            seq='00'
            fileId = 'CHK' + seq
            speechtext = lang + text

            nowTime = datetime.datetime.now()
            stamp   = nowTime.strftime('%Y%m%d.%H%M%S')
            wrkText = qPath_work + stamp + '.' + seq + '.selfcheck.txt'
            wrkOut  = qPath_work + stamp + '.' + seq + '.selfcheck.mp3'

            qFunc.txtsWrite(wrkText, txts=[speechtext], encoding='utf-8', exclusive=False, mode='w', )

            inpInput = ''
            inpOutput= ''
            trnInput = ''
            trnOutput= ''
            txtInput = wrkText
            txtOutput= wrkOut
            outInput = ''
            outOutput= ''
            inpPlay  = 'off'
            txtPlay  = 'off'
            outPlay  = 'off'

            res = speech_batch(
                xrunMode, xmicDev, 
                xApiInp, xApiTrn, xApiOut, xLangInp, xLangTrn, xLangTxt, xLangOut,
                str(seq), fileId,
                inpInput, inpOutput, trnInput, trnOutput, txtInput, txtOutput, outInput, outOutput,
                inpPlay, txtPlay, outPlay,
                )

            if (os.path.exists(wrkOut)):
                wrkPlay = qPath_s_play + stamp + '.' + fileId + '.mp3'
                qFunc.copy(wrkOut, wrkPlay)
                wrkInput = qPath_s_inp + stamp + '.' + fileId + '.mp3'
                qFunc.copy(wrkOut, wrkInput)

                time.sleep(3.00)
                self.wait(idolSec=3, maxWait=60)

                return wrkOut

        return False



class api_speech_class:

    def __init__(self, ):
        self.timeOut     = 15
        self.speech_proc = None
        self.speech_id   = None
        
    def __del__(self, ):
        self.speech_id   = None

    def setTimeOut(self, timeOut=5, ):
        self.timeOut = timeOut

    def execute(self, sync, 
            runMode, micDev,
            qApiInp, qApiTrn, qApiOut, qLangInp, qLangTrn, qLangTxt, qLangOut,
            procId, fileId,
            inpInput, inpOutput, trnInput, trnOutput, txtInput, txtOutput, outInput, outOutput,
            inpPlay, txtPlay, outPlay,
            ):

        if (sync == True):
            speech_batch(
                runMode, micDev,
                qApiInp, qApiTrn, qApiOut, qLangInp, qLangTrn, qLangTxt, qLangOut,
                procId, fileId,
                inpInput, inpOutput, trnInput, trnOutput, txtInput, txtOutput, outInput, outOutput,
                inpPlay, txtPlay, outPlay,
                )

        # threading
        if (sync != True):
            self.speech_proc = threading.Thread(target=speech_batch, args=(
                runMode, micDev,
                qApiInp, qApiTrn, qApiOut, qLangInp, qLangTrn, qLangTxt, qLangOut,
                procId, fileId,
                inpInput, inpOutput, trnInput, trnOutput, txtInput, txtOutput, outInput, outOutput,
                inpPlay, txtPlay, outPlay,
                ), daemon=True, )
            self.speech_proc.start()

        #if (sync == True):
        #    self.speech_proc.join()
        #    self.speech_id = None

        return True



if (__name__ == '__main__'):

    # 共通クラス
    qRiKi.init()
    qFunc.init()

    # ログ
    nowTime  = datetime.datetime.now()
    filename = qPath_log + nowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
    qLog.init(mode='logger', filename=filename, display=False, outfile=True, )

    qLog.log('info', '___main___:init')
    qLog.log('info', '___main___:exsample.py runMode, api..., lang..., ')
    #runMode  hud, live, translator, speech, number, chat, chatbot, camera, assistant, reception,
    #api      free, google, watson, azure, aws, winos, macos,
    #lang     ja, en, fr, kr...

    # 設定

    runMode  = 'debug'
    micDev   = '0'

    procId   = '00'
    fileId   = 'temp_sample'

    inpInput = '_sounds/_sound_hallo.wav'
    inpOutput= 'temp/temp_sample_ja.txt'
    trnInput = 'temp/temp_sample_ja.txt'
    trnOutput= 'temp/temp_sample_en.txt'
    txtInput = 'temp/temp_sample_ja.txt'
    txtOutput= 'temp/temp_sample_ja.mp3'
    outInput = 'temp/temp_sample_en.txt'
    outOutput= 'temp/temp_sample_en.mp3'

    inpPlay  = 'on'
    txtPlay  = 'off'
    outPlay  = 'on'

    if (len(sys.argv) >= 2):
        runMode  = str(sys.argv[1]).lower()
    if (len(sys.argv) >= 3):
        micDev   = str(sys.argv[2]).lower()
    if (len(sys.argv) >= 4):
        qApiInp  = str(sys.argv[3]).lower()
        if (qApiInp == 'free')  or (qApiInp == 'google') or (qApiInp == 'watson') \
        or (qApiInp == 'azure') or (qApiInp == 'aws'):
            qApiTrn  = qApiInp
            qApiOut  = qApiInp
        else:
            qApiTrn  = 'free'
            qApiOut  = 'free'
    if (len(sys.argv) >= 5):
        qApiTrn  = str(sys.argv[4]).lower()
    if (len(sys.argv) >= 6):
        qApiOut  = str(sys.argv[5]).lower()
    if (len(sys.argv) >= 7):
        qLangInp = str(sys.argv[6]).lower()
        qLangTxt = qLangInp
    if (len(sys.argv) >= 8):
        qLangTrn = str(sys.argv[7]).lower()
        qLangOut = qLangTrn[:2]
    if (len(sys.argv) >= 9):
        qLangTxt = str(sys.argv[8]).lower()
    if (len(sys.argv) >= 10):
        qLangOut = str(sys.argv[9]).lower()

    if (len(sys.argv) >= 11):
        procId   = sys.argv[10]
    if (len(sys.argv) >= 12):
        fileId   = sys.argv[11]

    if (len(sys.argv) >= 13):
        inpInput = sys.argv[12]
    if (len(sys.argv) >= 14):
        inpOutput= sys.argv[13]
    if (len(sys.argv) >= 15):
        trnInput = sys.argv[14]
    if (len(sys.argv) >= 16):
        trnOutput= sys.argv[15]
    if (len(sys.argv) >= 17):
        txtInput = sys.argv[16]
    if (len(sys.argv) >= 18):
        txtOutput= sys.argv[17]
    if (len(sys.argv) >= 19):
        outInput = sys.argv[18]
    if (len(sys.argv) >= 20):
        outOutput= sys.argv[19]

    if (len(sys.argv) >= 21):
        inpPlay  = str(sys.argv[20]).lower()
    if (len(sys.argv) >= 22):
        txtPlay  = str(sys.argv[21]).lower()
    if (len(sys.argv) >= 23):
        outPlay  = str(sys.argv[22]).lower()

    qLog.log('info', '')
    qLog.log('info', '___main___:runMode  =' + str(runMode  ))
    qLog.log('info', '___main___:micDev   =' + str(micDev   ))
    qLog.log('info', '___main___:qApiInp  =' + str(qApiInp  ))
    qLog.log('info', '___main___:qApiTrn  =' + str(qApiTrn  ))
    qLog.log('info', '___main___:qApiOut  =' + str(qApiOut  ))
    qLog.log('info', '___main___:qLangInp =' + str(qLangInp ))
    qLog.log('info', '___main___:qLangTrn =' + str(qLangTrn ))
    qLog.log('info', '___main___:qLangTxt =' + str(qLangTxt ))
    qLog.log('info', '___main___:qLangOut =' + str(qLangOut ))

    qLog.log('info', '___main___:procId   =' + str(procId   ))
    qLog.log('info', '___main___:fileId   =' + str(fileId   ))

    qLog.log('info', '___main___:inpInput =' + str(inpInput ))
    qLog.log('info', '___main___:inpOutput=' + str(inpOutput))
    qLog.log('info', '___main___:trnInput =' + str(trnInput ))
    qLog.log('info', '___main___:trnOutput=' + str(trnOutput))
    qLog.log('info', '___main___:txtInput =' + str(txtInput ))
    qLog.log('info', '___main___:txtOutput=' + str(txtOutput))
    qLog.log('info', '___main___:outInput =' + str(outInput ))
    qLog.log('info', '___main___:outOutput=' + str(outOutput))

    qLog.log('info', '___main___:inpPlay  =' + str(inpPlay  ))
    qLog.log('info', '___main___:txtPlay  =' + str(txtPlay  ))
    qLog.log('info', '___main___:outPlay  =' + str(outPlay  ))



    qLog.log('info', '')
    qLog.log('info', '___main___:start')



    # 音声処理 api
    #import       _v6_api_speech
    #api_speech = _v6_api_speech.api_speech_class()
    api_speech = api_speech_class()

    res = api_speech.execute(True,
            runMode, micDev,
            qApiInp, qApiTrn, qApiOut, qLangInp, qLangTrn, qLangTxt, qLangOut,
            procId, fileId,
            inpInput, inpOutput, trnInput, trnOutput, txtInput, txtOutput, outInput, outOutput,
            inpPlay, txtPlay, outPlay,  
            )



    qLog.log('info', '___main___:terminate')

    qLog.log('info', '___main___:bye!')


