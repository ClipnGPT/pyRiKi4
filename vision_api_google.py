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

import cv2
import requests
import json
import base64



# google 画像認識、OCR認識
import vision_api_google_key as google_key

# google 機械翻訳
#import speech_api_google     as a_google_api
#import speech_api_google_key as a_google_key



class VisionAPI:

    def __init__(self, ):
        self.timeOut = 10
        self.cv_url  = None
        self.cv_key  = None
        self.ocr_url = None
        self.ocr_key = None

    def setTimeOut(self, timeOut=10, ):
        self.timeOut = timeOut

    def authenticate(self, api, url, key, ):
        # google 画像認識
        if (api == 'cv'):
            self.cv_url = url
            self.cv_key = key
            if (self.cv_key is not None):
                return True

        # google OCR認識
        if (api == 'ocr'):
            self.ocr_url = url
            self.ocr_key = key
            if (self.ocr_key is not None):
                return True

        return False



    def convert(self, inpImage, outImage, bw=True, bitwise=False, maxWidth=640, maxHeight=480, ):
        try:
            if (os.path.exists(outImage)):
                os.remove(outImage)

            image_img = cv2.imread(inpImage, cv2.IMREAD_UNCHANGED)
            if len(image_img.shape) == 3:
                image_height, image_width, image_channels = image_img.shape[:3]
            else:
                image_height, image_width = image_img.shape[:2]
                image_channels = 1

            proc_img    = image_img.copy()
            proc_width  = image_width
            proc_height = image_height
            if (bw == True):
                if (image_channels != 1):
                    proc_img = cv2.cvtColor(image_img, cv2.COLOR_BGR2GRAY)

                #proc_img = cv2.equalizeHist(proc_img)
                #proc_img = cv2.blur(proc_img, (3,3), 0)
                #_, proc_img = cv2.threshold(proc_img, 140, 255, cv2.THRESH_BINARY)

                if (bitwise == True):
                    proc_img = cv2.bitwise_not(proc_img.copy())

            if (maxWidth != 0):
                if (proc_width > maxWidth):
                    proc_height = int(proc_height * (maxWidth / proc_width))
                    proc_width  = maxWidth
                    proc_img = cv2.resize(proc_img, (proc_width, proc_height))

            if (maxHeight != 0):
                if (proc_height > maxHeight):
                    proc_width  = int(proc_width * (maxHeight / proc_height))
                    proc_height = maxHeight
                    proc_img = cv2.resize(proc_img, (proc_width, proc_height))

            if (maxWidth != 0) and (maxWidth != 0):
                if (proc_width > maxWidth) or (proc_height > maxHeight):
                    proc_width  = maxWidth
                    proc_height = maxHeight
                    proc_img = cv2.resize(proc_img, (proc_width, proc_height))

            cv2.imwrite(outImage, proc_img)
            return True

        except Exception as e:
            pass

        return False



    def cv(self, inpImage, inpLang='ja', ):
        res_text = None
        res_api  = ''

        if (self.cv_key is None):
            print('GOOGLE: Not Authenticate Error !')

        else:
            lang = inpLang

            if (True):
                try:
                    rb = open(inpImage, 'rb')
                    photo = rb.read()
                    rb.close
                    rb = None
                    photo_b64 = base64.b64encode(photo).decode('utf-8')

                    url  = self.cv_url
                    headers = {
                        'Content-Type': 'application/json',
                        }
                    params = {
                        'key': self.cv_key,
                        }
                    json_data = {
                        'requests': [ {
                             'image': {
                                 'content': photo_b64,
                                 },
                             'imageContext': {
                                 'languageHints': lang,
                                 },
                             'features': [ {
                                 'type': 'LABEL_DETECTION',
                                 'maxResults': 10,
                                 },
                                 {
                                 'type': 'LANDMARK_DETECTION',
                                 'maxResults': 10,
                                 },
                                 {
                                 'type': 'TEXT_DETECTION',
                                 'maxResults': 10,
                                 }, ],
                             }, ],
                        }
                    res = requests.post(url, headers=headers, params=params, 
                          data=json.dumps(json_data), timeout=self.timeOut, )
                    #print(res)
                    if (res.status_code == 200):
                        res_json = json.loads(res.text)
                        #print(res_json)
                        detect_label    = ''
                        detect_landmark = ''
                        for response in res_json['responses']:
                            try:
                                for label in response['labelAnnotations']:
                                    text = label['description']
                                    #a_googleAPI = a_google_api.SpeechAPI()
                                    #a_res = a_googleAPI.authenticate('tra', a_google_key.getkey('tra'), )
                                    #if (a_res == True):
                                    #    outText, api = a_googleAPI.translate(inpText=text, inpLang='en', outLang=lang, )
                                    #    if (outText != ''):
                                    #        text = outText
                                    detect_label += str(text) + ','
                                    detect_label = detect_label.strip()
                            except Exception as e:
                                pass
                            try:
                                for landmark in response['landmarkAnnotations']:
                                    text = landmark['description']
                                    #a_googleAPI = a_google_api.SpeechAPI()
                                    #a_res = a_googleAPI.authenticate('tra', a_google_key.getkey('tra'), )
                                    #if (a_res == True):
                                    #    outText, api = a_googleAPI.translate(inpText=text, inpLang='en', outLang=lang, )
                                    #    if (outText != ''):
                                    #        text = outText
                                    detect_landmark += str(text) + ','
                                    detect_landmark = detect_landmark.strip()
                            except Exception as e:
                                pass

                        res_text = {}
                        res_text['label']    = detect_label
                        res_text['landmark'] = detect_landmark
                except Exception as e:
                    pass

            return res_text, 'google'

        return None, ''

    def ocr(self, inpImage, inpLang='ja', ):
        res_text = None
        res_api  = ''

        if (self.ocr_key is None):
            print('GOOGLE: Not Authenticate Error !')

        else:
            lang = inpLang

            if (True):
                try:
                    rb = open(inpImage, 'rb')
                    photo = rb.read()
                    rb.close
                    rb = None
                    photo_b64 = base64.b64encode(photo).decode('utf-8')

                    url  = self.ocr_url
                    headers = {
                        'Content-Type': 'application/json',
                        }
                    params = {
                        'key': self.ocr_key,
                        }
                    json_data = {
                        'requests': [ {
                             'image': {
                                 'content': photo_b64,
                                 },
                             'imageContext': {
                                 'languageHints': lang,
                                 },
                             'features': [ {
                                 'type': 'TEXT_DETECTION',
                                 'maxResults': 10,
                                 }, ],
                             }, ],
                        }
                    res = requests.post(url, headers=headers, params=params, 
                          data=json.dumps(json_data), timeout=self.timeOut, )
                    #print(res)
                    if (res.status_code == 200):
                        res_json = json.loads(res.text)
                        #print(res_json)
                        res_text = []
                        for response in res_json['responses']:
                            try:
                                text_n = response['fullTextAnnotation']['text']
                                text_s = text_n.split('\n')
                                for text in text_s:
                                    text = str(text).strip()
                                    if (text != ''):
                                        res_text.append(text)
                            except Exception as e:
                                res_text = None
                except Exception as e:
                    pass

            return res_text, 'google'

        return None, ''



if __name__ == '__main__':

        #googleAPI = google_api.VisionAPI()
        googleAPI = VisionAPI()

        res1 = googleAPI.authenticate('cv' ,
                    google_key.getkey('cv' ,'url'),
                    google_key.getkey('cv' ,'key'), )
        res2 = googleAPI.authenticate('ocr',
                    google_key.getkey('ocr','url'),
                    google_key.getkey('ocr','key'), )
        print('authenticate:', res1, res2)
        if (res1 == True) and (res2 == True):

            file = '_photos/_photo_cv.jpg'
            temp = 'temp_photo_cv.jpg'

            res = googleAPI.convert(inpImage=file, outImage=temp, bw=False, )
            if (res == True):
                res, api = googleAPI.cv(inpImage=temp, inpLang='ja', )
                if (res is not None):
                    print('cv')
                    print('label:',    res['label'],    '(' + api + ')' )
                    print('landmark:', res['landmark'], '(' + api + ')' )

            res = googleAPI.convert(inpImage=file, outImage=temp, bw=True, )
            if (res == True):
                res, api = googleAPI.ocr(inpImage=temp, inpLang='ja', )
                if (res is not None):
                    print('ocr1')
                    for text in res:
                        print('ocr:', text, '(' + api + ')' )

            file = '_photos/_photo_ocr_meter.jpg'
            temp = 'temp_photo_ocr_meter.jpg'

            res = googleAPI.convert(inpImage=file, outImage=temp, bw=True, )
            if (res == True):
                res, api = googleAPI.ocr(inpImage=temp, inpLang='ja', )
                if (res is not None):
                    print('ocr2')
                    for text in res:
                        print('ocr:', text, '(' + api + ')' )

            res = googleAPI.convert(inpImage=file, outImage=temp, bw=True, bitwise=True, )
            if (res == True):
                res, api = googleAPI.ocr(inpImage=temp, inpLang='ja', )
                if (res is not None):
                    print('ocr3')
                    for text in res:
                        print('ocr:', text, '(' + api + ')' )


