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

import subprocess

import json



# aws
import boto3

# aws 音声認識、翻訳機能、音声合成
import speech_api_aws_key as aws_key

# aws ストレージ
import storage_api_aws
s3_api = storage_api_aws.StorageAPI()
import storage_api_aws_key as s3_key



class SpeechAPI:

    def __init__(self, ):
        self.timeOut        = 120
        self.stt_key_id     = None
        self.stt_secret_key = None
        self.stt_client     = None
        self.tra_key_id     = None
        self.tra_secret_key = None
        self.tra_client     = None
        self.tts_key_id     = None
        self.tts_secret_key = None
        self.tts_client     = None
        self.region_name    = 'ap-northeast-1'
        self.bucketid       = 'kondou-pycv-'

    def setTimeOut(self, timeOut=120, ):
        self.timeOut = timeOut

    def authenticate(self, api, key_id, secret_key, ):
        # aws 音声認識
        if (api == 'stt'):
            try:
                # Service connect
                self.stt_client = boto3.client('transcribe',
                        aws_access_key_id     = key_id, 
                        aws_secret_access_key = secret_key,
                        region_name           = self.region_name,
                        )
                self.stt_key_id     = key_id
                self.stt_secret_key = secret_key
                return True
            except Exception as e:
                return False

        # aws 翻訳機能
        if (api == 'tra'):
            try:
                # Service connect
                self.tra_client = boto3.client('translate',
                        aws_access_key_id     = key_id, 
                        aws_secret_access_key = secret_key,
                        region_name           = self.region_name,
                        )
                self.tra_key_id     = key_id
                self.tra_secret_key = secret_key
                return True
            except Exception as e:
                return False

        # aws 音声合成
        if (api == 'tts'):
            try:
                # Service connect
                self.tts_client = boto3.client('polly',
                        aws_access_key_id     = key_id, 
                        aws_secret_access_key = secret_key,
                        region_name           = self.region_name,
                        )
                self.tts_key_id     = key_id
                self.tts_secret_key = secret_key
                return True
            except Exception as e:
                return False

        return False



    def recognize(self, inpWave, inpLang='ja-JP', bucket='default', ):
        res_text = ''
        res_api  = ''
        s3bucket = self.bucketid + bucket

        if (self.stt_client is None):
            print('aws: Not Authenticate Error !')

        else:
            lang  = ''

            if (inpLang == 'auto'):
                lang  = 'ja-JP'
            elif (inpLang == 'ja' or inpLang == 'ja-JP'):
                lang  = 'ja-JP'
            elif (inpLang == 'en' or inpLang == 'en-US'):
                lang  = 'en-US'
            elif (inpLang == 'ar'):
                lang  = 'ar-AR'
            elif (inpLang == 'es'):
                lang  = 'es-ES'
            elif (inpLang == 'de'):
                lang  = 'de-DE'
            elif (inpLang == 'fr'):
                lang  = 'fr-FR'
            elif (inpLang == 'it'):
                lang  = 'it-IT'
            elif (inpLang == 'pt'):
                lang  = 'pt-BR'
            elif (inpLang == 'zh' or inpLang == 'zh-CN'):
                lang  = 'zh-CN'

            if (lang != ''):
                #try:

                    # mp3 変換
                    inpFile = inpWave
                    if (inpWave[-4:].lower() == '.wav'):
                        inpFile = inpWave[:-4] + '.mp3'
                        if (os.path.exists(inpFile)):
                            os.remove(inpFile)
                        sox = subprocess.Popen(['sox', '-q', inpWave, '-r', '16000', '-b', '16', '-c', '1', inpFile, ], \
                              shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                        sox.wait()
                        sox.terminate()
                        sox = None
                        time.sleep(1)

                    # s3 認証
                    if (os.path.exists(inpFile)):
                        res = s3_api.authenticate('s3', 
                                    s3_key.getkey('s3', 'key_id',     ),
                                    s3_key.getkey('s3', 'secret_key', ),
                                    )
                        if (res == True):

                            # ファイル名決定
                            inpPath  = os.path.dirname(inpFile)
                            if (inpPath != ''):
                                inpPath += '/'
                            inpFname = os.path.basename(inpFile)
                            job_name = inpFname[:-4]
                            resFname = job_name + '.json'

                            # 音声認識ＪＯＢ削除
                            try:
                                self.stt_client.delete_transcription_job(TranscriptionJobName=job_name,)
                            except Exception as e:
                                pass

                            # ファイル削除
                            res = s3_api.s3_remove(bucket=bucket, s3File=inpFname, )
                            res = s3_api.s3_remove(bucket=bucket, s3File=resFname, )

                            # mp3 送信
                            res = s3_api.s3_put(bucket=bucket, inpPath=inpPath, inpFile=inpFname, s3File='', )
                            if (res == True):

                                file_uri = 's3://' + s3bucket + '/' + inpFname

                                # 音声認識ＪＯＢ開始
                                self.stt_client.start_transcription_job(TranscriptionJobName=job_name,
                                                                Media={'MediaFileUri': file_uri},
                                                                MediaFormat=inpFname[-3:],
                                                                MediaSampleRateHertz=16000,
                                                                LanguageCode=lang,
                                                                Settings={'ShowSpeakerLabels' : True,
                                                                            'MaxSpeakerLabels' : 5, },
                                                                OutputBucketName=s3bucket,
                                                                )

                                # ファイル待機
                                res = s3_api.s3_wait_get(bucket=bucket, s3File=resFname, 
                                                        outPath=inpPath, outFile='', maxWait=self.timeOut, )
                                if (res == True):

                                    # 戻り値取得
                                    res_dic = {}
                                    try:
                                        res_file = inpPath + resFname
                                        with codecs.open(res_file, 'r', 'utf-8') as r:
                                            res_dic = json.load(r)
                                    except Exception as e:
                                        #print(e.args)
                                        res_dic = {}

                                    #print(json.dumps(res_dic, indent=4, ensure_ascii=False, ))

                                    res_text = ''
                                    for transcript in res_dic['results']['transcripts']:
                                        t = str(transcript['transcript'])
                                        res_text = (res_text + ' ' + str(t)).strip()
                                    res_api = 'aws'

                            # 処理後の整理
                            time.sleep(7.00)

                            # 音声認識ＪＯＢ削除
                            try:
                                self.stt_client.delete_transcription_job(TranscriptionJobName=job_name,)
                            except Exception as e:
                                pass

                            # ファイル削除
                            res = s3_api.s3_remove(bucket=bucket, s3File=inpFname, )
                            res = s3_api.s3_remove(bucket=bucket, s3File=resFname, )

                #except Exception as e:
                #    pass

            if (res_text != ''):
                res_text = str(res_text).strip()
                while (res_text[-1:] == '。') \
                   or (res_text[-1:] == '、') \
                   or (res_text[-1:] == '.'):
                    res_text = res_text[:-1]

                if (inpLang == 'ja' or inpLang == 'ja-JP'):
                    chk_text = str(res_text).replace(' ', '')
                    chk_text = str(chk_text).replace('.', '')
                    chk_text = str(chk_text).replace('_', '')
                    if (not chk_text.encode('utf-8').isalnum()):
                        res_text = str(res_text).replace(' ', '')

                # aws fault!
                if (res_text.lower() == 'x'):
                    res_text = ''

                return res_text, res_api

        return res_text, res_api



    def translate(self, inpText='こんにちは', inpLang='ja-JP', outLang='en-US', ):
        res_text = ''
        res_api  = ''
        if (self.tra_client is None):
            print('aws: Not Authenticate Error !')

        else:
            inp = ''
            out = ''

            if (inpLang == 'auto'):
                inp = 'ja-JP'
            elif (inpLang == 'ja' or inpLang == 'ja-JP'):
                inp = 'ja-JP'
            elif (inpLang == 'en' or inpLang == 'en-US'):
                inp = 'en-US'
            elif (inpLang == 'ar'):
                inp = 'ar-AR'
            elif (inpLang == 'es'):
                inp = 'es-ES'
            elif (inpLang == 'de'):
                inp = 'de-DE'
            elif (inpLang == 'fr'):
                inp = 'fr-FR'
            elif (inpLang == 'it'):
                inp = 'it-IT'
            elif (inpLang == 'pt'):
                inp = 'pt-BR'
            elif (inpLang == 'zh' or inpLang == 'zh-CN'):
                inp = 'zh-CN'

            if   (outLang == 'ar'):
                out = 'ar-AR'
            elif (outLang == 'en' or outLang == 'en-US'):
                out = 'en-US'
            elif (outLang == 'es'):
                out = 'es-US'
            elif (outLang == 'de'):
                out = 'de-DE'
            elif (outLang == 'fr'):
                out = 'fr-FR'
            elif (outLang == 'it'):
                out = 'it-IT'
            elif (outLang == 'ja' or outLang == 'ja-JP'):
                out = 'ja-JP'
            elif (outLang == 'pt'):
                out = 'pt-BR'
            elif (outLang == 'zh' or outLang == 'zh-CN'):
                out = 'zh-CN'

            if (inp != '') and (out != '') and (inpText != '') and (inpText != '!'):
                try:

                    # 機械翻訳
                    response = self.tra_client.translate_text(
                        Text=inpText,
                        SourceLanguageCode=inpLang, #inp,
                        TargetLanguageCode=outLang, #out,
                    )

                    res_text = response['TranslatedText']
                    res_api = 'aws'

                except Exception as e:
                    pass

            if (res_text != ''):
                res_text = str(res_text).strip()
                while (res_text[-1:] == '。') \
                   or (res_text[-1:] == '、') \
                   or (res_text[-1:] == '.'):
                    res_text = res_text[:-1]

                if (outLang == 'ja' or outLang == 'ja-JP'):
                    chk_text = str(res_text).replace(' ', '')
                    chk_text = str(chk_text).replace('.', '')
                    chk_text = str(chk_text).replace('_', '')
                    if (not chk_text.encode('utf-8').isalnum()):
                        res_text = str(res_text).replace(' ', '')

                # aws fault!
                if (res_text.lower() == 'x'):
                    res_text = ''

                return res_text, res_api

        return res_text, res_api



    def vocalize(self, outText='hallo', outLang='en-US', outGender='Female', outFile='temp_voice.mp3', ):
        if (self.tts_client is None):
            print('aws: Not Authenticate Error !')

        else:
            if (os.path.exists(outFile)):
                try:
                    os.remove(outFile)
                except Exception as e:
                    pass

            lang  = ''
            voice = ''
            gend  = outGender

            if   (outLang == 'ja' or outLang=='ja-JP'):
                lang  = 'ja-JP'
                voice = 'Mizuki'
                gend  = 'Female'
            elif (outLang == 'en' or outLang == 'en-US'):
                lang  = 'en-US'
                voice = 'Joanna'
                gend  = 'Female'
            elif (outLang == 'ar'):
                lang  = 'ar-eg'
                voice = 'Zeina'
                gend  = 'Female'
            elif (outLang == 'es'):
                lang  = 'es-US'
                voice = 'Lupe'
                gend  = 'Female'
            elif (outLang == 'de'):
                lang  = 'de-DE'
                voice = 'Naja'
                gend  = 'Female'
            elif (outLang == 'fr'):
                lang  = 'fr-FR'
                voice = 'Céline'
                gend  = 'Female'
            elif (outLang == 'it'):
                lang  = 'it-IT'
                voice = 'Bianca'
                gend  = 'Male'
            elif (outLang == 'pt'):
                lang  = 'pt-BR'
                voice = 'Camila'
                gend  = 'Male'
            elif (outLang == 'zh' or outLang == 'zh-CN'):
                lang  = 'zh-CN'
                voice = 'Zhiy'
                gend  = 'Female'

            if (voice != '') and (outText != '') and (outText != '!'):
                try:

                    # 音声合成
                    response = self.tts_client.synthesize_speech(
                            Text = outText,
                            OutputFormat = outFile[-3:],
                            VoiceId = voice, )

                    file = open(outFile, 'wb')
                    file.write(response['AudioStream'].read())
                    file.close()

                    return outText, 'aws'

                except Exception as e:
                    pass
        return '', ''



if __name__ == '__main__':

        #awsAPI = aws_api.SpeechAPI()
        awsAPI = SpeechAPI()

        key_id     = aws_key.getkey('stt', 'key_id',     )
        secret_key = aws_key.getkey('stt', 'secret_key', )
        res1  = awsAPI.authenticate('stt', key_id, secret_key, )
        key_id     = aws_key.getkey('tra', 'key_id',     )
        secret_key = aws_key.getkey('tra', 'secret_key', )
        res2  = awsAPI.authenticate('tra', key_id, secret_key, )
        key_id     = aws_key.getkey('tts', 'key_id',     )
        secret_key = aws_key.getkey('tts', 'secret_key', )
        res3  = awsAPI.authenticate('tts', key_id, secret_key, )
        print('authenticate:', res1, res2, res3)

        if (res1 == True) and (res2 == True) and (res3 == True):

            text = '今日は久しぶりにゆっくり休めます。'
            file = 'temp_voice.mp3'

            res, api = awsAPI.vocalize(outText=text, outLang='ja', outFile=file)
            print('vocalize:', res, '(' + api + ')' )

            sox = subprocess.Popen(['sox', file, '-d', '-q'], )
            sox.wait()
            sox.terminate()
            sox = None

            file2 = 'temp_voice.wav'
            sox = subprocess.Popen(['sox', '-q', file, '-r', '16000', '-b', '16', '-c', '1', file2, ], )
            sox.wait()
            sox.terminate()
            sox = None

            res, api = awsAPI.recognize(inpWave=file2, inpLang='ja', )
            print('recognize:', res, '(' + api + ')' )

            res, api = awsAPI.translate(inpText=text, inpLang='ja', outLang='en', )
            print('translate:', res, '(' + api + ')' )



