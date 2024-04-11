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

import subprocess

import cv2
import requests
import json



# watson 画像認識、OCR認識
#import watson_developer_cloud as watson
import ibm_watson as watson
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import vision_api_watson_key as watson_key



class VisionAPI:

    def __init__(self, ):
        self.timeOut  = 10
        self.cv_url   = None
        self.cv_key   = None
        self.cv_auth  = None
        self.ocr_url  = None
        self.ocr_key  = None
        self.ocr_auth = None

    def setTimeOut(self, timeOut=10, ):
        self.timeOut = timeOut

    def authenticate(self, api, url, key, ):
        # watson 画像認識
        if (api == 'cv'):
            self.cv_url  = url
            self.cv_key  = key
            try:
                self.cv_auth = IAMAuthenticator(key)
                if (self.cv_auth is not None):
                    return True
            except Exception as e:
                pass

        # watson OCR認識
        if (api == 'ocr'):
            self.ocr_url  = url
            self.ocr_key  = key
            try:
                self.ocr_auth = IAMAuthenticator(key)
                if (self.ocr_auth is not None):
                    return True
            except Exception as e:
                pass

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
            print('WATSON: Not Authenticate Error !')

        else:
            lang = inpLang

            if (True):
                #try:
                    visual_recognition = watson.VisualRecognitionV3(
                        version = '2018-03-19',
                        authenticator = self.cv_auth,)
                    #visual_recognition.set_disable_ssl_verification(True)

                    with open(inpImage, 'rb') as images_file:
                        res = visual_recognition.classify(
                            images_file = images_file,
                            threshold = '0.6',
                            owners = ['IBM'],
                            classifier_ids = ['default'],
                            accept_language = lang,
                            ).get_result()

                    #print(json.dumps(res, indent=4, ensure_ascii=False, ))
                    #print(res['images'][0]['classifiers'][0]['classes'])

                    classes = ''
                    try:
                        for class_nm in res['images'][0]['classifiers'][0]['classes']:
                            nm = str(class_nm.get('class'))
                            #print(nm)
                            classes += nm.strip() + ','
                    except Exception as e:
                        pass

                    res_text = {}
                    res_text['classes'] = classes
                #except Exception as e:
                #    pass

            return res_text, 'watson'

        return None, ''

    def ocr(self, inpImage, inpLang='ja', ):
        res_text = None
        res_api  = ''

        if (self.ocr_key is None):
            print('WATSON: Not Authenticate Error !')

        else:
            lang = inpLang

            if (True):
                #try:
                    visual_recognition = watson.VisualRecognitionV3(
                        version = '2018-03-19', 
                        authenticator = self.ocr_auth,)
                    #visual_recognition.set_disable_ssl_verification(True)

                    with open(inpImage, 'rb') as images_file:
                        res = visual_recognition.recognize_text(
                            images_file = images_file,
                            accept_language = lang,
                            ).get_result()

                    #print(json.dumps(res, indent=4, ensure_ascii=False, ))
                    #print(res['images'][0]['classifiers'][0]['classes'])

                    res_text = {}
                    #try:
                    #    for class_nm in res['images'][0]['classifiers'][0]['classes']:
                    #        nm = str(class_nm.get('class'))
                    #        #print(nm)
                    #        res_text.append( nm.strip() )
                    #except Exception as e:
                    #    pass

                #except Exception as e:
                #    pass

            return res_text, 'watson'

        return None, ''



if __name__ == '__main__':

        #watsonAPI = watson_api.VisionAPI()
        watsonAPI = VisionAPI()

        res1 = watsonAPI.authenticate('cv' ,
                    watson_key.getkey('cv' ,'url'),
                    watson_key.getkey('cv' ,'key'), )
        res2 = watsonAPI.authenticate('ocr' ,
                    watson_key.getkey('ocr' ,'url'),
                    watson_key.getkey('ocr' ,'key'), )
        print('authenticate:', res1, res2)
        if (res1 == True) and (res2 == True):

            file = '_photos/_photo_cv.jpg'
            temp = 'temp_photo_cv.jpg'

            res = watsonAPI.convert(inpImage=file, outImage=temp, bw=False, )
            if (res == True):
                res, api = watsonAPI.cv(inpImage=temp, inpLang='ja', )
                if (res is not None):
                    print('cv')
                    print('classes:', res['classes'], '(' + api + ')' )

            #file = '_photos/_photo_ocr_meter.jpg'
            #temp = 'temp_photo_ocr_meter.jpg'

            #res = watsonAPI.convert(inpImage=file, outImage=temp, bw=True, )
            #if (res == True):
            #    res, api = watsonAPI.ocr(inpImage=temp, inpLang='ja', )
            #    if (res is not None):
            #        print('ocr')
            #        for text in res:
            #            print('ocr:', text, '(' + api + ')' )


