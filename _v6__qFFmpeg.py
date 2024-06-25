#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# COPYRIGHT (C) 2014-2024 Mitsuo KONDOU.
# This software is released under the MIT License.
# https://github.com/konsan1101
# Thank you for keeping the rules.
# ------------------------------------------------



import os
import time

import queue
import threading
import subprocess

import numpy as np
import cv2
#try:
#    from ultralytics import YOLO
#except Exception as e:
#    print(e)

import platform
qPLATFORM = platform.system().lower() #windows,darwin,linux



# 共通ルーチン
import  _v6__qFunc
qFunc = _v6__qFunc.qFunc_class()
import  _v6__qGUI
qGUI  = _v6__qGUI.qGUI_class()



# フォント
qPath_fonts   = '_fonts/'
qFONT_default = {'file':qPath_fonts + '_vision_font_ipaexg.ttf','offset':8}
qFONT_DSEG7   = {'file':qPath_fonts + 'DSEG7Classic-Bold.ttf','offset':8}



class qCV2_class:

    def __init__(self, ): 
        # カメラ
        self.cv2video               = None
        self.cv2device              = None

        # 差分処理
        self.cv2sabun_model         = None
        self.cv2sabun_width         = 480 #処理サイズ
        self.cv2sabun_height        = 270 #処理サイズ
        self.cv2sabun_minDots       = int((self.cv2sabun_width * self.cv2sabun_height) * 0.001) # 480*270画像で129dot

        # cascade
        self.cascade_procSize       = 640
        self.cascade_xml_face       = '_cv2data/xml/_vision_opencv_face.xml'
        self.cascade_xml_cars       = '_cv2data/xml/_vision_opencv_cars.xml'
        self.cascade_xml_fullbody   = '_cv2data/xml/_vision_opencv_fullbody.xml'
        self.cascade_casName        = self.cascade_xml_face
        #self.cascade_cascade       = cv2.CascadeClassifier(self.cascade_casName)
        self.cascade_cascade        = None

        # ssd
        self.ssd_procSize           = 512
        self.ssd_config             = '_cv2data/dnn/ssd/frozen_inference_graph.pb'
        self.ssd_weights            = '_cv2data/dnn/ssd/ssd_mobilenet_v2_coco_2018_03_29.pbtxt'
        self.ssd_threshold_score    = 0.8
        self.ssd_threshold_nms      = 0.45
        #self.ssd_model             = cv2.dnn.readNetFromTensorflow(self.ssd_config, self.ssd_weights)
        self.ssd_model              = None
        self.ssd_labels             = []
        self.ssd_colors             = []
        res, _                      = qFunc.txtsRead('_cv2data/dnn/ssd/labels.txt', )
        if (res != False):
            self.ssd_labels         = res
        for n in range(len(self.ssd_labels)):
            self.ssd_colors.append(np.random.randint(low=0, high=255, size=3, dtype=np.uint8))

        # yolov8 -> onnx
        self.yolov8_procSize        = 640
        #self.yolov8_model = YOLO('_cv2data/yolov8/yolov8n.pt')
        #self.yolov8_model.export(format='onnx', imgsz=self.yolov8_procSize, opset=12, )

        # yolov8
        self.yolov8_weights         = '_cv2data/yolov8/yolov8n.onnx'
        self.yolov8_model           = None
        self.yolov8_threshold_score = 0.8
        self.yolov8_threshold_nms   = 0.45
        self.yolov8_labels          = []
        self.yolov8_colors          = []
        res, _                      = qFunc.txtsRead('_cv2data/yolov8/yolov8_labels.txt', )
        if (res != False):
            self.yolov8_labels      = res
        for n in range(len(self.yolov8_labels)):
            self.yolov8_colors.append(np.random.randint(low=0, high=255, size=3, dtype=np.uint8))

        # yolov4
        # normal
        #self.yolov4_procSize       = 512
        #self.yolov4_config         = '_cv2data/yolov4/yolov4_512x512.cfg'
        #self.yolov4_weights        = '_cv2data/yolov4/yolov4_512x512.weights'
        # tiny
        self.yolov4_procSize        = 416
        self.yolov4_config          = '_cv2data/yolov4/yolov4-tiny_416x416.cfg'
        self.yolov4_weights         = '_cv2data/yolov4/yolov4-tiny_416x416.weights'
        #self.yolov4_net            = cv2.dnn.readNet(self.yolov4_config, self.yolov4_weights)
        #self.yolov4_model          = cv2.dnn_DetectionModel(self.yolov4_net, )
        #self.yolov4_model.setInputParams(scale=1 / 255, size=(self.yolov4_procSize, self.yolov4_procSize), swapRB=True, )
        self.yolov4_net             = None
        self.yolov4_model           = None
        self.yolov4_confThreshold   = 0.8
        self.yolov4_nmsThreshold    = 0.45
        self.yolov4_labels          = []
        self.yolov4_colors          = []
        res, _                      = qFunc.txtsRead('_cv2data/yolov4/yolov4_labels.txt', )
        if (res != False):
            self.yolov4_labels      = res
        for n in range(len(self.yolov4_labels)):
            self.yolov4_colors.append(np.random.randint(low=0, high=255, size=3, dtype=np.uint8))



    def cv2imread(self, filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
        try:
            n = np.fromfile(filename, dtype)
            img = cv2.imdecode(n, flags)
            return img
        except Exception as e:
            print(e)
            return None

    def cv2imwrite(self, filename, img, params=None):
        try:
            ext = os.path.splitext(filename)[1]
            result, n = cv2.imencode(ext, img, params)

            if result:
                with open(filename, mode='w+b') as f:
                    n.tofile(f)
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

    def cv2capture(self, dev='0', retry_max=2, retry_wait=1.00, ):

        retry_max   = retry_max
        retry_count = 0
        check       = False
        while (check == False) and (retry_count <= retry_max):
            # キャプチャー
            image = self.cv2capture_sub(dev, )
            if (image is not None):
                check = True
            # リトライ
            if (check == False):
                time.sleep(retry_wait)
                retry_count += 1

        if (check == True):
            return image
        else:
            return None

    def cv2capture_sub(self, dev='0', ):
        image   = None

        # オープン
        res = self.cv2open(dev=dev, )

        # 取り込み
        if  (res == True):
            image = self.cv2read()

        # クローズ
        self.cv2close()

        return image

    def cv2open(self, dev='0', ):

        # クローズ
        self.cv2close()

        # オープン
        try:
            if (not str(dev).isdigit()):
                self.cv2video = cv2.VideoCapture(dev)
            else:
                if (os.name != 'nt'):
                    self.cv2video = cv2.VideoCapture(int(dev))
                else:
                    self.cv2video = cv2.VideoCapture(int(dev), cv2.CAP_DSHOW)
        except Exception as e:
            self.cv2video  = None
            self.cv2device = None
            return False

        self.cv2device = dev
        return True

    def cv2read(self, ):
        frame = None

        # 取り込み
        if (self.cv2video is not None):
            try:
                ret, frame = self.cv2video.read()
            except Exception as e:
                ret = False
                frame = None

        return frame

    def cv2close(self, ):

        # クローズ
        try:
            self.cv2video.release()
        except Exception as e:
            pass

        self.cv2video  = None
        self.cv2device = None
        return True



    # 差分処理
    def cv2sabun(self, inp_image=None, base_image=None, ):
        if (inp_image is None):
            return None, None, None, 0

        # 入力画像
        inp_height, inp_width = inp_image.shape[:2]

        # 最初の画像
        if (self.cv2sabun_model is None):
            self.cv2sabun_model = cv2.bgsegm.createBackgroundSubtractorMOG()
            #self.cv2sabun_height, self.cv2sabun_width = inp_height, inp_width
            #self.cv2sabun_minDots = int((self.cv2sabun_width * self.cv2sabun_height) * 0.002) # 640x360画像で460dot

        # 入出力画像
        proc_height, proc_width = self.cv2sabun_height, self.cv2sabun_width
        proc_image = cv2.resize(inp_image, (proc_width, proc_height))
        if (base_image is not None):
            out_image  = base_image.copy()
        else:
            # 彩度、明度変換
            hsv_image = cv2.cvtColor(inp_image, cv2.COLOR_BGR2HSV)  # 色空間をBGRからHSVに変換
            s_magnification = 0.7  # 彩度(Saturation)の倍率
            v_magnification = 0.7  # 明度(Value)の倍率
            hsv_image[:,:,(1)] = hsv_image[:,:,(1)]*s_magnification  # 彩度の計算
            hsv_image[:,:,(2)] = hsv_image[:,:,(2)]*v_magnification  # 明度の計算
            out_image = cv2.cvtColor(hsv_image,cv2.COLOR_HSV2BGR)  # 色空間をHSVからBGRに変換
        base_image = out_image.copy()

        # 差分画像
        min_left   = -1
        min_top    = -1
        max_right  = -1
        max_bottom = -1
        sabun_image  = np.zeros((inp_height, inp_width, 3), np.uint8)
        sabun_ritu = 0
        #sabun_dots = 0
        #sabun_imgs = []

        # 差分演算する
        sabun_mask = self.cv2sabun_model.apply(proc_image)
        # 輪郭抽出する
        sabun_contours = cv2.findContours(sabun_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        # 小さい輪郭は除く
        sabun_contours = list(filter(lambda x: cv2.contourArea(x) > self.cv2sabun_minDots, sabun_contours))
        if (len(sabun_contours) != 0):

            # 輪郭を囲む外接矩形を取得する
            sabun_boxs = list(map(lambda x: cv2.boundingRect(x), sabun_contours))

            # 矩形を描画する
            for l, t, w, h in sabun_boxs:

                # 座標計算
                left   = int(l * inp_width  / proc_width )
                top    = int(t * inp_height / proc_height)
                width  = int(w * inp_width  / proc_width )
                height = int(h * inp_height / proc_height)

                out_image[  top:top+height, left:left+width ] = inp_image[ top:top+height, left:left+width ]
                cv2.rectangle(out_image, (left, top), (left + width, top + height), (255,255,0), 2)
                base_image[ top:top+height, left:left+width ] = inp_image[ top:top+height, left:left+width ]

                if (min_left   == -1) or (left <  min_left):
                    min_left   = left
                if (min_top    == -1) or (top  <  min_top ):
                    min_top    = top
                if (max_right  == -1) or ((left+width) > max_right ):
                    max_right  = (left+width)
                if (max_bottom == -1) or ((top+height) > max_bottom):
                    max_bottom = (top+height)

                #img = inp_image[top:top+height, left:left+width ]
                #sabun_dots += w * h
                #sabun_imgs.append(img.copy())

            ## 輪郭を取得する
            #sabun_contours2,hierarchy = cv2.findContours(sabun_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            ## 輪郭を描写する
            #output_img=cv2.drawContours(output_img, sabun_contours2, -1, (255,255,0), 3)

        # 差分領域
        if  (min_left   == -1) \
        and (min_top    == -1) \
        and (max_right  == -1) \
        and (max_bottom == -1):
            out_image  = inp_image.copy()
            base_image = inp_image.copy()

        else:
            base_image[  min_top:max_bottom, min_left:max_right ] = inp_image[ min_top:max_bottom, min_left:max_right ]
            sabun_image[ min_top:max_bottom, min_left:max_right ] = inp_image[ min_top:max_bottom, min_left:max_right ]
            # 率計算
            sabun_dots = (max_right - min_left) * (max_bottom - min_top)
            sabun_ritu = sabun_dots / (inp_width * inp_height) * 100

        return out_image, base_image, sabun_image, sabun_ritu, #sabun_imgs



    def cv2detect_cascade(self, inp_image=None, base_image=None, search='face', ):
        out_image  = None
        hit_images = []

        # 検索条件
        xml = self.cascade_casName
        if   (search == 'face'):
            xml = self.cascade_xml_face
            self.cascade_haar_scale     = 1.1
            self.cascade_min_neighbors  = 10
            self.cascade_min_size       = (15, 15)
        elif (search == 'cars'):
            xml = self.cascade_xml_cars
            self.cascade_haar_scale     = 1.1
            self.cascade_min_neighbors  = 3
            self.cascade_min_size       = (15, 15)
        elif (search == 'fullbody'):
            xml = self.cascade_xml_fullbody
            self.cascade_haar_scale     = 1.1
            self.cascade_min_neighbors  = 10
            self.cascade_min_size       = (15, 15)
        if (search == 'face') or (search == 'cars') or (search == 'fullbody'):
            if (xml != self.cascade_casName):
                self.cascade_casName = xml
                self.cascade_cascade = None

        # 初回モデル構築
        if (self.cascade_cascade is None):
            try:
                self.cascade_cascade = cv2.CascadeClassifier(self.cascade_casName)
                print('cv2detect_cascade : "' + self.cascade_casName + '" loading complite!')
            except Exception as e:
                print(e)
                self.cascade_cascade = None

        # エラー？
        if (self.cascade_cascade is None):
            return None, hit_images

        # 入出力画像
        inp_height, inp_width = inp_image.shape[:2]
        if (base_image is not None):
            out_image  = base_image.copy()
        else:
            # 彩度、明度変換
            hsv_image = cv2.cvtColor(inp_image, cv2.COLOR_BGR2HSV)  # 色空間をBGRからHSVに変換
            s_magnification = 1  # 彩度(Saturation)の倍率
            v_magnification = 0.5  # 明度(Value)の倍率
            hsv_image[:,:,(1)] = hsv_image[:,:,(1)]*s_magnification  # 彩度の計算
            hsv_image[:,:,(2)] = hsv_image[:,:,(2)]*v_magnification  # 明度の計算
            out_image = cv2.cvtColor(hsv_image,cv2.COLOR_HSV2BGR)  # 色空間をHSVからBGRに変換

        # 入力画像成形
        if (inp_width > self.cascade_procSize):
            proc_width  = self.cascade_procSize
            proc_height = int(inp_height * self.cascade_procSize / inp_width)
            proc_img = cv2.resize(inp_image, (proc_width, proc_height))
        else:
            proc_img = inp_image.copy()
            proc_width, proc_height = inp_width, inp_height

        gray1 = cv2.cvtColor(proc_img, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.equalizeHist(gray1)

        # 物体検出
        try:
            rects = self.cascade_cascade.detectMultiScale(gray2, 
                    scaleFactor=self.cascade_haar_scale,
                    minNeighbors=self.cascade_min_neighbors,
                    minSize=self.cascade_min_size, )
        except Exception as e:
            print(e)
            return None, hit_images

        if (rects is not None):
            for rect in rects:
                l, t, w, h = rect

                # 座標計算
                left   = int(l * inp_width  / proc_width )
                top    = int(t * inp_height / proc_height)
                width  = int(w * inp_width  / proc_width )
                height = int(h * inp_height / proc_height)
                if (search == 'face'):
                    left   -= 10
                    width  += 20
                    top    -= 10
                    height += 20
                if (left < 0):
                    left = 0
                if (top < 0):
                    top = 0
                if ((left + width) > inp_width):
                    width = inp_width - left
                if ((top + height) > inp_height):
                    height = inp_height - top

                # マーキングと戻り値
                img = inp_image[top:top+height, left:left+width ]
                cv2.rectangle(out_image, (left,top), (left+width,top+height), (0,0,255), 5)
                hit_images.append(img.copy())

        return out_image, hit_images

    def cv2detect_ssd(self, inp_image=None, base_image=None, search='person', ):
        out_image  = None
        hit_images = []
        all_labels = []
        all_images = []
        all_scores = []

        # 初回モデル構築
        if (self.ssd_model is None):
            try:
                self.ssd_model = cv2.dnn.readNetFromTensorflow(self.ssd_config, self.ssd_weights)
                print('cv2detect_ssd : "' + self.ssd_weights + '" loading complite!')
            except Exception as e:
                print(e)
                self.ssd_model = None

        # エラー？
        if (self.ssd_model is None):
            return None, hit_images, all_images, all_labels, all_scores

        # 入出力画像
        inp_height, inp_width = inp_image.shape[:2]
        if (base_image is not None):
            out_image  = base_image.copy()
        else:
            # 彩度、明度変換
            hsv_image = cv2.cvtColor(inp_image, cv2.COLOR_BGR2HSV)  # 色空間をBGRからHSVに変換
            s_magnification = 1  # 彩度(Saturation)の倍率
            v_magnification = 0.5  # 明度(Value)の倍率
            hsv_image[:,:,(1)] = hsv_image[:,:,(1)]*s_magnification  # 彩度の計算
            hsv_image[:,:,(2)] = hsv_image[:,:,(2)]*v_magnification  # 明度の計算
            out_image = cv2.cvtColor(hsv_image,cv2.COLOR_HSV2BGR)  # 色空間をHSVからBGRに変換

        # 入力画像成形　四角形へ
        if (inp_width > inp_height):
            proc_size = inp_width
            proc_img  = np.zeros((proc_size,proc_size,3), np.uint8)
            offset    = int((inp_width-inp_height)/2)
            proc_img[offset:offset+inp_height, 0:inp_width] = inp_image.copy()
        elif (inp_height > inp_width):
            proc_size = inp_height
            proc_img  = np.zeros((proc_size,proc_size,3), np.uint8)
            offset    = int((inp_height-inp_width)/2)
            proc_img[0:inp_height, offset:offset+inp_width] = inp_image.copy()
        else:
            proc_size = inp_width
            proc_img  = inp_image.copy()
            offset    = 0
        proc_img = cv2.resize(proc_img, (self.ssd_procSize, self.ssd_procSize), )

        # 物体検出
        try:
            blob = cv2.dnn.blobFromImage(proc_img, size=(self.ssd_procSize, self.ssd_procSize), swapRB=True)
            self.ssd_model.setInput(blob)
            output = self.ssd_model.forward()
        except Exception as e:
            print(e)
            return None, hit_images, all_images, all_labels, all_scores

        # outputは[1:1:100:7]のリストになっているため、後半の2つを取り出す
        detections = output[0, 0, :, :]

        classids = []
        scores   = []
        boxes    = []

        # detectionには[?,id番号、予測確率、Xの開始点、Yの開始点、Xの終了点、Yの終了点]が入っている。
        for detection in detections:

            # 予測確率がthreshold_score以上を取り出す。
            score = detection[2]
            if (score >= float(self.ssd_threshold_score)/2):

                # 元の画像サイズを掛けて、四角で囲むための4点の座標情報を得る
                axis = detection[3:7] * (self.ssd_procSize, self.ssd_procSize, self.ssd_procSize, self.ssd_procSize)

                # floatからintに変換して、変数に取り出す。
                (l, t, r, b) = axis.astype(np.int64)[:4]
                left   = int(l)
                top    = int(t)
                width  = int(r - l)
                height = int(b - t)

                # ある程度の大きさのものを取り出す。
                #if  (width  >= inp_width /20) and (width  <= inp_width /2  ) \
                #and (height >= inp_height/10) and (height <= inp_height/1.5):

                classids.append(int(detection[1]))
                scores.append(float(score))
                boxes.append([int(left), int(top), int(width), int(height)])

        # 重複した領域を排除した内容を利用する。
        indices = cv2.dnn.NMSBoxes(boxes, scores, float(self.ssd_threshold_score), float(self.ssd_threshold_nms), 0.5, )
        if (len(indices)<3):
            indices = cv2.dnn.NMSBoxes(boxes, scores, float(self.ssd_threshold_score/2), float(self.ssd_threshold_nms), 0.5, )
        #if (len(indices)<3):
        #    indices = cv2.dnn.NMSBoxes(boxes, scores, float(0.0), float(self.ssd_threshold_nms), 0.5, )

        # ループ
        for i in indices:
            id    = classids[i]
            score = scores[i]
            box   = boxes[i][0:4]
            try:
                label  = self.ssd_labels[id]
                label2 = label + '({:4.1f}%)'.format(score*100)
                color  = [ int(c) for c in self.ssd_colors[id] ]
            except:
                label  = str(id)
                label2 = label + '({:4.1f}%)'.format(score*100)
                color  = (int(255),int(255),int(255))
            #print(label2, box)

            # 座標計算
            l, t, w, h = box
            if   (inp_width > inp_height):
                left   = int(l * (proc_size / self.ssd_procSize))
                top    = int(t * (proc_size / self.ssd_procSize)) - offset
                width  = int(w * (proc_size / self.ssd_procSize))
                height = int(h * (proc_size / self.ssd_procSize))
            elif (inp_height > inp_width):
                left   = int(l * (proc_size / self.ssd_procSize)) - offset
                top    = int(t * (proc_size / self.ssd_procSize))
                width  = int(w * (proc_size / self.ssd_procSize))
                height = int(h * (proc_size / self.ssd_procSize))
            else:
                left   = int(l * (proc_size / self.ssd_procSize))
                top    = int(t * (proc_size / self.ssd_procSize))
                width  = int(w * (proc_size / self.ssd_procSize))
                height = int(h * (proc_size / self.ssd_procSize))
            if (left < 0):
                left = 0
            if (top < 0):
                top = 0
            if ((left + width) > inp_width):
                width = inp_width - left
            if ((top + height) > inp_height):
                height = inp_height - top

            try:

                # 枠とラベル
                cv2.rectangle(out_image, (left, top), (left+width, top+height), color, 5)
                t_size = cv2.getTextSize(label2, cv2.FONT_HERSHEY_COMPLEX_SMALL, 1 , 1)[0]
                x = left + t_size[0] + 3
                y = top  + t_size[1] + 4
                cv2.rectangle(out_image, (left, top), (x, y), color, -1)
                cv2.putText(out_image, label2, (left, top + t_size[1] + 1), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0), 1)

                # 結果
                img = inp_image[top:top+height, left:left+width ]
                if (label == search):
                    hit_images.append(img.copy())
                all_images.append(img.copy())
                all_labels.append(label)
                all_scores.append(score)

            except Exception as e:
                print(e)

        return out_image, hit_images, all_images, all_labels, all_scores

    def cv2detect_yolov8(self, inp_image=None, base_image=None, search='person', ):
        out_image  = None
        hit_images = []
        all_labels = []
        all_images = []
        all_scores = []

        # 初回モデル構築
        if (self.yolov8_model is None):
            try:
                self.yolov8_model : cv2.dnn.Net = cv2.dnn.readNetFromONNX(self.yolov8_weights)
                print('cv2detect_yolov8 : "' + self.yolov8_weights + '" loading complite!')
            except Exception as e:
                print(e)
                self.yolov8_model = None

        # エラー？
        if (self.yolov8_model is None):
            return None, hit_images, all_images, all_labels, all_scores

        # 入出力画像
        inp_height, inp_width = inp_image.shape[:2]
        if (base_image is not None):
            out_image  = base_image.copy()
        else:
            # 彩度、明度変換
            hsv_image = cv2.cvtColor(inp_image, cv2.COLOR_BGR2HSV)  # 色空間をBGRからHSVに変換
            s_magnification = 1  # 彩度(Saturation)の倍率
            v_magnification = 0.5  # 明度(Value)の倍率
            hsv_image[:,:,(1)] = hsv_image[:,:,(1)]*s_magnification  # 彩度の計算
            hsv_image[:,:,(2)] = hsv_image[:,:,(2)]*v_magnification  # 明度の計算
            out_image = cv2.cvtColor(hsv_image,cv2.COLOR_HSV2BGR)  # 色空間をHSVからBGRに変換

        # 入力画像成形　四角形へ
        if (inp_width > inp_height):
            proc_size = inp_width
            proc_img  = np.zeros((proc_size,proc_size,3), np.uint8)
            offset    = int((inp_width-inp_height)/2)
            proc_img[offset:offset+inp_height, 0:inp_width] = inp_image.copy()
        elif (inp_height > inp_width):
            proc_size = inp_height
            proc_img  = np.zeros((proc_size,proc_size,3), np.uint8)
            offset    = int((inp_height-inp_width)/2)
            proc_img[0:inp_height, offset:offset+inp_width] = inp_image.copy()
        else:
            proc_size = inp_width
            proc_img  = inp_image.copy()
            offset    = 0
        proc_img = cv2.resize(proc_img, (self.yolov8_procSize, self.yolov8_procSize), )

        # 物体検出
        try:
            blob = cv2.dnn.blobFromImage(proc_img, scalefactor=1/255, size=(self.yolov8_procSize, self.yolov8_procSize), swapRB=True)
            self.yolov8_model.setInput(blob)
            output = self.yolov8_model.forward()
            output = np.array([cv2.transpose(output[0])])
        except Exception as e:
            print(e)
            return None, hit_images, all_images, all_labels, all_scores

        detections = output[0]

        classids = []
        scores   = []
        boxes    = []

        for detection in detections:
            classes_scores = detection[4:]
            (minScore, score, minClassLoc, (x, classid)) = cv2.minMaxLoc(classes_scores)
            if (score >= float(self.yolov8_threshold_score)):
                width  = detection[2]
                height = detection[3]
                left   = detection[0] - (width  / 2)
                top    = detection[1] - (height / 2)
                classids.append(int(classid))
                scores.append(float(score))
                boxes.append([int(left), int(top), int(width), int(height)])
                #print('rows', classid, score, [left, top, width, height], )

        # 重複した領域を排除した内容を利用する。
        indices = cv2.dnn.NMSBoxes(boxes, scores, float(self.yolov8_threshold_score), float(self.yolov8_threshold_nms), 0.5, )
        if (len(indices)<3):
            indices = cv2.dnn.NMSBoxes(boxes, scores, float(self.yolov8_threshold_score/2), float(self.yolov8_threshold_nms), 0.5, )
        #if (len(indices)<3):
        #    indices = cv2.dnn.NMSBoxes(boxes, scores, float(0.0), float(self.yolov8_threshold_nms), 0.5, )

        # ループ
        for i in indices:
            id    = classids[i]
            score = scores[i]
            box   = boxes[i][0:4]
            try:
                label  = self.yolov8_labels[id]
                label2 = label + '({:4.1f}%)'.format(score*100)
                color  = [ int(c) for c in self.yolov8_colors[id] ]
            except:
                label  = str(id)
                label2 = label + '({:4.1f}%)'.format(score*100)
                color  = (int(255),int(255),int(255))
            #print(label2, box)

            # 座標計算
            l, t, w, h = box
            if   (inp_width > inp_height):
                left   = int(l * (proc_size / self.yolov8_procSize))
                top    = int(t * (proc_size / self.yolov8_procSize)) - offset
                width  = int(w * (proc_size / self.yolov8_procSize))
                height = int(h * (proc_size / self.yolov8_procSize))
            elif (inp_height > inp_width):
                left   = int(l * (proc_size / self.yolov8_procSize)) - offset
                top    = int(t * (proc_size / self.yolov8_procSize))
                width  = int(w * (proc_size / self.yolov8_procSize))
                height = int(h * (proc_size / self.yolov8_procSize))
            else:
                left   = int(l * (proc_size / self.yolov8_procSize))
                top    = int(t * (proc_size / self.yolov8_procSize))
                width  = int(w * (proc_size / self.yolov8_procSize))
                height = int(h * (proc_size / self.yolov8_procSize))
            if (left < 0):
                left = 0
            if (top < 0):
                top = 0
            if ((left + width) > inp_width):
                width = inp_width - left
            if ((top + height) > inp_height):
                height = inp_height - top

            try:

                # 枠とラベル
                cv2.rectangle(out_image, (left, top), (left+width, top+height), color, 5)
                t_size = cv2.getTextSize(label2, cv2.FONT_HERSHEY_COMPLEX_SMALL, 1 , 1)[0]
                x = left + t_size[0] + 3
                y = top  + t_size[1] + 4
                cv2.rectangle(out_image, (left, top), (x, y), color, -1)
                cv2.putText(out_image, label2, (left, top + t_size[1] + 1), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0), 1)

                # 結果
                img = inp_image[top:top+height, left:left+width ]
                if (label == search):
                    hit_images.append(img.copy())
                all_images.append(img.copy())
                all_labels.append(label)
                all_scores.append(score)

            except Exception as e:
                print(e)

        return out_image, hit_images, all_images, all_labels, all_scores

    def cv2detect_yolov4(self, inp_image=None, base_image=None, search='person', ):
        out_image  = None
        hit_images = []
        all_labels = []
        all_images = []
        all_scores = []

        # 初回モデル構築
        if (self.yolov4_model is None):
            try:
                self.yolov4_net   = cv2.dnn.readNet(self.yolov4_config, self.yolov4_weights)
                self.yolov4_model = cv2.dnn_DetectionModel(self.yolov4_net, )
                self.yolov4_model.setInputParams(scale=1 / 255, size=(self.yolov4_procSize, self.yolov4_procSize), swapRB=True, )
                print('cv2detect_yolov4 : "' + self.yolov4_weights + '" loading complite!')
            except Exception as e:
                print(e)
                self.yolov4_net   = None
                self.yolov4_model = None

        # エラー？
        if (self.yolov4_model is None):
            return out_image, hit_images, all_images, all_labels, all_scores

        # 入出力画像
        inp_height, inp_width = inp_image.shape[:2]
        if (base_image is not None):
            out_image  = base_image.copy()
        else:
            # 彩度、明度変換
            hsv_image = cv2.cvtColor(inp_image, cv2.COLOR_BGR2HSV)  # 色空間をBGRからHSVに変換
            s_magnification = 1  # 彩度(Saturation)の倍率
            v_magnification = 0.5  # 明度(Value)の倍率
            hsv_image[:,:,(1)] = hsv_image[:,:,(1)]*s_magnification  # 彩度の計算
            hsv_image[:,:,(2)] = hsv_image[:,:,(2)]*v_magnification  # 明度の計算
            out_image = cv2.cvtColor(hsv_image,cv2.COLOR_HSV2BGR)  # 色空間をHSVからBGRに変換

        # 入力画像成形　四角形へ
        if (inp_width > inp_height):
            proc_size = inp_width
            proc_img  = np.zeros((proc_size,proc_size,3), np.uint8)
            offset    = int((inp_width-inp_height)/2)
            proc_img[offset:offset+inp_height, 0:inp_width] = inp_image.copy()
        elif (inp_height > inp_width):
            proc_size = inp_height
            proc_img  = np.zeros((proc_size,proc_size,3), np.uint8)
            offset    = int((inp_height-inp_width)/2)
            proc_img[0:inp_height, offset:offset+inp_width] = inp_image.copy()
        else:
            proc_size = inp_width
            proc_img  = inp_image.copy()
            offset    = 0
        proc_img = cv2.resize(proc_img, (self.yolov4_procSize, self.yolov4_procSize), )

        # 物体検出
        try:
            detect_result = self.yolov4_model.detect(proc_img, confThreshold=float(self.yolov4_threshold_score/2), nmsThreshold=self.yolov4_nmsThreshold , )
        except Exception as e:
            print(e)
            return None, hit_images, all_images, all_labels, all_scores

        if (detect_result is not None):
            classids = detect_result[0]
            scores   = detect_result[1]
            boxs     = detect_result[2]
            for i in range(len(classids)):
                id    = classids[i]
                score = scores[i]
                try:
                    label  = self.yolov4_labels[id]
                    label2 = label + '({:4.1f}%)'.format(score*100)
                    color  = [ int(c) for c in self.yolov4_colors[id] ]
                except:
                    label  = str(id)
                    label2 = label + '({:4.1f}%)'.format(score*100)
                    color  = (int(255),int(255),int(255))
                #print(label2)

                # 座標計算
                l, t, w, h = boxs[i][0:4]
                if   (inp_width > inp_height):
                    left   = int(l * (proc_size / self.yolov4_procSize))
                    top    = int(t * (proc_size / self.yolov4_procSize)) - offset
                    width  = int(w * (proc_size / self.yolov4_procSize))
                    height = int(h * (proc_size / self.yolov4_procSize))
                elif (inp_height > inp_width):
                    left   = int(l * (proc_size / self.yolov4_procSize)) - offset
                    top    = int(t * (proc_size / self.yolov4_procSize))
                    width  = int(w * (proc_size / self.yolov4_procSize))
                    height = int(h * (proc_size / self.yolov4_procSize))
                else:
                    left   = int(l * (proc_size / self.yolov4_procSize))
                    top    = int(t * (proc_size / self.yolov4_procSize))
                    width  = int(w * (proc_size / self.yolov4_procSize))
                    height = int(h * (proc_size / self.yolov4_procSize))
                if (left < 0):
                    left = 0
                if (top < 0):
                    top = 0
                if ((left + width) > inp_width):
                    width = inp_width - left
                if ((top + height) > inp_height):
                    height = inp_height - top

                try:

                    # 枠とラベル
                    cv2.rectangle(out_image, (left, top), (left+width, top+height), color, 5)
                    t_size = cv2.getTextSize(label2, cv2.FONT_HERSHEY_COMPLEX_SMALL, 1 , 1)[0]
                    x = left + t_size[0] + 3
                    y = top  + t_size[1] + 4
                    cv2.rectangle(out_image, (left, top), (x, y), color, -1)
                    cv2.putText(out_image, label2, (left, top + t_size[1] + 1), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0), 1)

                    # 結果
                    img = inp_image[top:top+height, left:left+width ]
                    if (label == search):
                        hit_images.append(img.copy())
                    all_images.append(img.copy())
                    all_labels.append(label)
                    all_scores.append(score)

                except Exception as e:
                    print(e)

        return out_image, hit_images, all_images, all_labels, all_scores



    def cv2img2mov(self, inp_file='temp/_work/image.jpg', out_file='temp/_work/movie.mp4', \
                sec=60, fps=10, zoom=True, ):

        if (os.name == 'nt'):
            inp_file = inp_file.replace('/', '\\')
            out_file = out_file.replace('/', '\\')

        # 確認
        if (not os.path.isfile(inp_file)):
            return False

        # 削除
        if (os.path.isfile(out_file)):
            os.remove(out_file)

        # 読取
        image = None
        height, width = 0, 0
        img   = None
        h, w  = 0, 0
        try:
            #image = cv2.imread(inp_file)
            image = self.cv2imread(inp_file)
            height, width = image.shape[:2]
            if (width > 1920):
                height = int(height * (1920/width))
                width  = 1920
                img_wk = cv2.resize(image, (width, height))
                image  = img_wk.copy()
            if (height > 1080):
                width  = int(width * (1080/height))
                height = 1080
                img_wk = cv2.resize(image, (width, height))
                image  = img_wk.copy()
            img = image.copy()
            h, w = 0, 0
        except Exception as e:
            print(e)
            return False

        # 書込
        fourcc = cv2.VideoWriter_fourcc('m','p','4', 'v')
        video  = cv2.VideoWriter(out_file, fourcc, fps, (width, height))
        for f in range(int(sec * fps)+1):
            if (zoom != True):
                video.write(image)
            else:
                wk_h = int((height*0.15) * f / (sec * fps))
                wk_w = int((width*0.15) * f / (sec * fps))
                if (wk_h != h) and (wk_w != w):
                    h, w = wk_h, wk_w
                    img = cv2.resize(image[h:height-h, w:width-w], (width, height))
                video.write(img)
        video.release()

        # 戻り値
        if (os.path.isfile(out_file)):
            if (os.path.getsize(out_file) > 0):
                return out_file
        return False



class qFFmpeg_class:

    def __init__(self, ): 
        self.dev_cam = []
        self.dev_mic = []
        self.checkUpdateDevInfo(update=True, )

    def ffmpeg_list_dev(self, ):
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
            while ((time.time() - checkTime) < 5):
                # バッファから1行読み込む.
                line = ffmpeg.stderr.readline()
                # バッファが空 + プロセス終了.
                if (not line) and (ffmpeg.poll() is not None):
                    break
                # テキスト
                txt = line.decode('utf-8')
                #print(txt)

                # ffmpeg 5
                if  (txt.find('dshow @') >=0) \
                and (txt.find('(video)') >=0):
                    st = txt.find('"') + 1
                    en = txt[st:].find('"')
                    t  = txt[st:st+en]
                    if  (t.find('OBS ')  < 0)\
                    and (t.find('OMEN ') < 0):
                        cam.append(t)
                        #print('cam:', t)
                elif (txt.find('dshow @') >=0) \
                and  (txt.find('(audio)') >=0):
                    st = txt.find('"') + 1
                    en = txt[st:].find('"')
                    t  = txt[st:st+en]
                    mic.append(t)
                    #print('mic:', t)

                # ffmpeg 4
                elif (txt.find('DirectShow video devices') >=0):
                    flag = 'cam'
                elif (txt.find('DirectShow audio devices') >=0):
                    flag = 'mic'
                elif (flag == 'cam') and (txt.find('"') >=0):
                    st = txt.find('"') + 1
                    en = txt[st:].find('"')
                    t  = txt[st:st+en]
                    if  (t.find('OBS ')  < 0)\
                    and (t.find('OMEN ') < 0):
                        cam.append(t)
                        #print('cam:', t)
                elif (flag == 'mic') and (txt.find('"') >=0):
                    st = txt.find('"') + 1
                    en = txt[st:].find('"')
                    t  = txt[st:st+en]
                    mic.append(t)
                    #print('mic:', t)
                else:
                    flag = ''

            # 時限待機
            if (ffmpeg is not None):
                checkTime = time.time()
                while ((time.time() - checkTime) < 2):
                    line = ffmpeg.stderr.readline()
                    #print(line)
                    if (not line) and (ffmpeg.poll() is not None):
                        break
                ffmpeg.terminate()
                ffmpeg = None

        elif (qPLATFORM == 'darwin'):

            ffmpeg = subprocess.Popen(['ffmpeg', '-y',
	            '-threads', '2',
	            '-f', 'avfoundation',
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
                if   (txt.find('AVFoundation video devices') >=0):
                    flag = 'cam'
                elif (txt.find('AVFoundation audio devices') >=0):
                    flag = 'mic'
                elif (flag == 'cam') and (txt.find('] [') >=0):
                    st = txt.find('] [') + 3
                    en = txt[st:].find('] ') + 2
                    t  = txt[st+en:]
                    t  = t.replace('\n', '')
                    if (t != 'Capture screen 0'):
                        cam.append(t)
                        #print('cam:', t)
                elif (flag == 'mic') and (txt.find('] [') >=0):
                    st = txt.find('] [') + 3
                    en = txt[st:].find('] ') + 2
                    t  = txt[st+en:]
                    t  = t.replace('\n', '')
                    mic.append(t)
                    #print('mic:', t)

            ffmpeg.terminate()
            ffmpeg = None

        return cam, mic

    def checkUpdateDevInfo(self, update=True):
        change = False

        cam, mic = self.ffmpeg_list_dev()
        if (cam != self.dev_cam) \
        or (mic != self.dev_mic):
            change = True
            if (update == True):
                self.dev_cam = cam
                self.dev_mic = mic

        return change

    def capture(self, dev='desktop', full=True, 
                work_path='temp/_work/desktop', retry_max=2, retry_wait=1.00, ):

        retry_max   = retry_max
        retry_count = 0
        check       = False
        while (check == False) and (retry_count <= retry_max):
            # キャプチャー
            image = self.capture_sub(dev, full, work_path)
            if (image is not None):
                check = True
            # リトライ
            if (check == False):
                time.sleep(retry_wait)
                retry_count += 1

        if (check == True):
            return image
        else:
            return None

    def capture_sub(self, dev='desktop', full=True, 
                    work_path='temp/_work/desktop', ):
        image = None

        # ファイル削除
        for i in range(1, 9999):
            fn = work_path + '.' + '{:04}'.format(i) + '.jpg'
            if os.path.isfile(fn):
                os.remove(fn)
            else:
                break

        # qGUI キャプチャ
        if (image is None):
            if  ( (os.name == 'nt') \
                   and (dev == 'desktop') and (full == False) ) \
            or  ( (os.name != 'nt') ):

                pil_image = qGUI.screenshot()
                image = np.array(pil_image, dtype=np.uint8)
                if (image.ndim == 2):  # モノクロ
                    pass
                elif (image.shape[2] == 3):  # カラー
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                elif (image.shape[2] == 4):  # 透過
                    image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGRA)

                # イメージ保存
                #try:
                #    cv2.imwrite(workpath + '.0001.jpg', capture)
                #except:
                #    capture = None

        # ffmpag キャプチャ
        if (image is None):

            ffmpeg = None

            # デスクトップ
            if (os.name == 'nt'):
                if (dev == 'desktop'):

                    # ffmpeg -y -f gdigrab -i desktop -ss 0 -t 0.2 -r 10 -q 1 temp.%04d.jpg
                    ffmpeg = subprocess.Popen(['ffmpeg', '-y',
                        '-threads', '2',
                        '-f', 'gdigrab', '-i', 'desktop',
                        '-ss','0','-t','0.2','-r','10',
                        '-q','1', 
                        work_path + '.' + '%04d.jpg',
                        '-loglevel', 'warning',
                        ], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

                #else:
                #
                #    # ffmpeg -y -f avfoundation -i 1:0 -ss 0 -t 0.2 -r 10 -q 1 temp.%04d.jpg
                #    ffmpeg = subprocess.Popen(['ffmpeg', '-y',
                #        '-threads', '2',
                #        '-f', 'avfoundation', '-i', '1:0',
                #        '-ss','0','-t','0.2','-r','10',
                #        '-q','1', 
                #        work_path + '.' + '%04d.jpg',
                #        '-loglevel', 'warning',
                #        ], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

            # カメラ
            if (os.name == 'nt'):
                if (dev != 'desktop'):

                    ffmpeg = subprocess.Popen(['ffmpeg', '-y',
                        '-threads', '2',
                        '-rtbufsize', '1024M',
                        '-f', 'dshow', '-i', 'video=' + dev,
                        '-ss','0','-t','0.5','-r','10',
                        '-q','1', 
                        work_path + '.' + '%04d.jpg',
                        '-loglevel', 'warning',
                        ], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

            # 時限待機・画像取得
            if (ffmpeg is not None):
                checkTime = time.time()
                while ((time.time() - checkTime) < 2):
                    line = ffmpeg.stderr.readline()
                    #print(line)
                    if (not line) and (ffmpeg.poll() is not None):
                        break
                ffmpeg.terminate()
                ffmpeg = None

                # イメージ取得
                try:
                    image = cv2.imread(work_path + '.0001.jpg')
                except:
                    image = None

        return image

    def rec_start(self, dev='desktop', rate='10', 
                    out_filev='temp/_work/recorder.mp4', out_filea='temp/_work/recorder.wav',
                    retry_max=3, retry_wait=5.00, ):

        #retry_max   = 3
        retry_count = 0
        check       = False
        while (check == False) and (retry_count <= retry_max):
            # 録画
            res_ffmpeg, res_sox, res_filev, res_filea = self.rec_start_sub(
                dev=dev, rate=rate, out_filev=out_filev, out_filea=out_filea, try_count=retry_count, )
            # チェック
            if (res_ffmpeg is not None) or (res_sox is not None):
                check = True
            # リトライ
            if (check == False) and (retry_count <= retry_max):
                time.sleep(retry_wait)
                retry_count += 1
                #print('retry', retry_count)

        if (check == True):
            #print('return', res_ffmpeg, res_sox, res_filev, res_filea)
            return res_ffmpeg, res_sox, res_filev, res_filea
        else:
            #print('return', None, None, '', '')
            return None, None, '', ''

    def rec_start_sub(self, dev='desktop', rate='10',
                        out_filev='temp/_work/recorder.mp4', out_filea='temp/_work/recorder.wav',
                        try_count=0, ):
        res_ffmpeg = None
        res_sox    = None
        res_filev  = out_filev
        res_filea  = out_filea

        # 録画　開始
        if (res_filev != ''):

            # デスクトップ Linux
            if (os.name != 'nt'):
                if (res_ffmpeg is None) and (dev == 'desktop'):

                        if (res_filev[-4:] != '.flv'):
                            res_filev = res_filev[:-4] + '.flv'

                        if (os.path.isfile(res_filev)):
                            os.remove(res_filev)

                        # ffmpeg -f avfoundation -i 1:0 -vcodec flv1 -q:v 0 -r 10 desktop.flv
                        res_ffmpeg = subprocess.Popen(['ffmpeg', '-y',
                            '-threads', '2',
                            '-f', 'avfoundation',
                            '-i', '1:0',
                            '-vf', 'scale=1920:-2',
                            '-vcodec', 'flv1',
                            '-q:v', '0',
                            '-r', str(rate),
                            res_filev,
                            '-loglevel', 'warning',
                            ], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                        time.sleep(0.50)
                        if (res_ffmpeg.poll() is not None):
                            res_ffmpeg.terminate()
                            res_ffmpeg = None

            # デスクトップ Windows
            if (os.name == 'nt'):

                # 初回
                if (res_ffmpeg is None) and (dev == 'desktop'):
                    if (try_count == 0) and (res_filev[-4:] == '.mp4'):

                        if (os.path.isfile(res_filev)):
                            os.remove(res_filev)

                        # GPU encoder, intel GPU 6th enable !
                        # ffmpeg -init_hw_device qsv:hw -f gdigrab -i desktop -vcodec hevc_qsv -r 10 desktop.mp4
                        res_ffmpeg = subprocess.Popen(['ffmpeg', '-y',
                            '-threads', '2',
                            '-init_hw_device', 'qsv:hw',
                            '-f', 'gdigrab', '-i', 'desktop',
                            '-vf', 'scale=1920:-2',
                            '-vcodec', 'hevc_qsv',
                            '-r', str(rate),
                            res_filev,
                            '-loglevel', 'warning',
                            ], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

                # ２回目
                if (res_ffmpeg is None) and (dev == 'desktop'):
                    if (try_count == 1) and (res_filev[-4:] == '.mp4'):

                        if (os.path.isfile(res_filev)):
                            os.remove(res_filev)

                        # GPU encoder, intel GPU enable !
                        # ffmpeg -init_hw_device qsv:hw -f gdigrab -i desktop -vcodec h264_qsv -r 10 desktop.mp4
                        res_ffmpeg = subprocess.Popen(['ffmpeg', '-y',
                            '-threads', '2',
                            '-init_hw_device', 'qsv:hw',
                            '-f', 'gdigrab', '-i', 'desktop',
                            '-vf', 'scale=1920:-2',
                            '-vcodec', 'h264_qsv',
                            '-r', str(rate),
                            res_filev,
                            '-loglevel', 'warning',
                            ], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

                # ３回目以降
                if (res_ffmpeg is None) and (dev == 'desktop'):
                    if (try_count >= 2):

                        if (res_filev[-4:] != '.flv'):
                            res_filev = res_filev[:-4] + '.flv'

                        if (os.path.isfile(res_filev)):
                            os.remove(res_filev)

                        # ffmpeg -f gdigrab -i desktop -vcodec flv1 -q:v 0 -r 10 desktop.flv
                        res_ffmpeg = subprocess.Popen(['ffmpeg', '-y',
                            '-threads', '2',
                            '-f', 'gdigrab', '-i', 'desktop',
                            '-vf', 'scale=1920:-2',
                            '-vcodec', 'flv1',
                            '-q:v', '0',
                            '-r', str(rate),
                            res_filev,
                            '-loglevel', 'warning',
                            ], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

            # カメラ Windows
            if (os.name == 'nt'):

                # 初回
                if (res_ffmpeg is None) and (dev != 'desktop'):
                    if (try_count == 0) and (res_filev[-4:] == '.mp4'):

                        if (os.path.isfile(res_filev)):
                            os.remove(res_filev)

                        # GPU encoder, intel 6th GPU enable !
                        # ffmpeg -init_hw_device qsv:hw -rtbufsize 1024M -f dshow -i "video=Microsoft Camera Front" -vcodec hevc_qsv -r 10 camera.mp4
                        res_ffmpeg = subprocess.Popen(['ffmpeg', '-y',
                            '-threads', '2',
                            '-init_hw_device', 'qsv:hw',
                            '-rtbufsize', '1024M',
                            '-f', 'dshow', '-i', 'video=' + dev,
                            '-vf', 'scale=1920:-2',
                            '-vcodec', 'hevc_qsv',
                            '-r', str(rate),
                            res_filev,
                            '-loglevel', 'warning',
                            ], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

                # ２回目
                if (res_ffmpeg is None) and (dev != 'desktop'):
                    if (try_count == 1) and (res_filev[-4:] == '.mp4'):

                        if (os.path.isfile(res_filev)):
                            os.remove(res_filev)

                        # GPU encoder, intel GPU enable !
                        # ffmpeg -init_hw_device qsv:hw -rtbufsize 1024M -f dshow -i "video=Microsoft Camera Front" -vcodec h264_qsv -r 10 camera.mp4
                        res_ffmpeg = subprocess.Popen(['ffmpeg', '-y',
                            '-threads', '2',
                            '-init_hw_device', 'qsv:hw',
                            '-rtbufsize', '1024M',
                            '-f', 'dshow', '-i', 'video=' + dev,
                            '-vf', 'scale=1920:-2',
                            '-vcodec', 'h264_qsv',
                            '-r', str(rate),
                            res_filev,
                            '-loglevel', 'warning',
                            ], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

                # ３回目以降
                if (res_ffmpeg is None) and (dev != 'desktop'):
                    if (try_count >= 2):

                        if (res_filev[-4:] != '.flv'):
                            res_filev = res_filev[:-4] + '.flv'

                        if (os.path.isfile(res_filev)):
                            os.remove(res_filev)

                        # ffmpeg -rtbufsize 1024M -f dshow -i "video=Microsoft Camera Front" -vcodec flv1 -q:v 0 -r 10 camera.flv
                        res_ffmpeg = subprocess.Popen(['ffmpeg', '-y',
                            '-threads', '2',
                            '-rtbufsize', '1024M',
                            '-f', 'dshow', '-i', 'video=' + dev,
                            '-vf', 'scale=1920:-2',
                            '-vcodec', 'flv1',
                            '-q:v', '0',
                            '-r', str(rate),
                            res_filev,
                            '-loglevel', 'warning',
                            ], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

        # 録音　開始
        if (res_filea != ''):

            if (os.path.isfile(res_filea)):
                os.remove(res_filea)

            res_sox = subprocess.Popen(['sox',
                '-q', '-d', '-r', '16000', '-b', '16', '-c', '1',
                res_filea,
                ], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

        # 起動確認
        time.sleep(5.00)

        check = True
        if (res_filev != ''):
            if (not os.path.isfile(res_filev)):
                check = False
            else:
                if (os.path.getsize(res_filev) == 0):
                    check = False
        #if (res_filea != ''):
        #    if (not os.path.isfile(res_filea)):
        #        check = False
        #    else:
        #        if (os.path.getsize(res_filea) == 0):
        #            check = False

        # 起動エラー
        if (check == False):
            if (res_filev != ''):
                if (res_ffmpeg is not None):
                    res_ffmpeg.terminate()
                    res_ffmpeg = None
                    res_filev  = ''
            if (res_filea != ''):
                if (res_sox is not None):
                    res_sox.terminate()
                    res_sox    = None
                    res_filea  = ''

        return res_ffmpeg, res_sox, res_filev, res_filea

    def rec_stop(self, ffmpeg, sox, ):

        # 録画　停止
        if (ffmpeg is not None):
            ffmpeg.stdin.write(b'q\n')
            try:
                ffmpeg.stdin.flush()
            except Exception as e:
                pass

        # 録音　停止・終了
        if (sox is not None):
            #if (os.name != 'nt'):
            #    sox.send_signal(signal.SIGINT)
            #else:
            #    sox.send_signal(signal.CTRL_C_EVENT)
            #time.sleep(2.00)
            sox.terminate()
            sox = None

        # 録画　時限待機・終了
        if (ffmpeg is not None):
            checkTime = time.time()
            while ((time.time() - checkTime) < 5):
                line = ffmpeg.stderr.readline()
                if (not line) and (ffmpeg.poll() is not None):
                    break

            #logb, errb = ffmpeg.communicate()
            ffmpeg.wait()
            ffmpeg.terminate()
            ffmpeg = None

        return True

    def encodemp4mp3(self, inp_filev='temp/_work/recorder.mp4', inp_filea='temp/_work/recorder.wav', rate='10',
                    out_filev='temp/_work/recorder_h265.mp4', out_filea='temp/_work/recorder_mp3.mp3', ):

        mp4ok = False
        mp3ok = False

        # 音声確認
        if (inp_filea != ''):
            if (not os.path.isfile(inp_filea)):
                inp_filea = ''
                out_filea = ''
            else:
                if (os.path.getsize(inp_filea) <= 44):
                    inp_filea = ''
                    out_filea = ''

        # 動画＋音声変換

        # GPU encoder 変換
        if (mp4ok == False) and (os.name == 'nt'):
            if (inp_filev != '') and (inp_filea != '') and (out_filev != ''):

                if (os.path.isfile(out_filev)):
                    os.remove(out_filev)

                # GPU encoder, intel 6th GPU enable !
                ffmpeg = subprocess.Popen(['ffmpeg', '-y',
                    '-threads', '2',
                    '-init_hw_device', 'qsv:hw',
                    '-i', inp_filev, '-i', inp_filea,
                    '-vf', 'scale=1920:-1',
                    '-vcodec', 'hevc_qsv', '-r', str(rate),
                    '-acodec', 'libmp3lame', '-strict', 'unofficial', '-ab', '96k', '-ac', '1', '-ar', '16000',
                    #'-acodec', 'aac', '-ab', '96k', '-ac', '1', '-ar', '16000',
                    out_filev,
                    '-loglevel', 'warning',
                    ], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

                #logb, errb = ffmpeg.communicate()
                ffmpeg.wait()
                ffmpeg.terminate()
                ffmpeg = None
                if (os.path.isfile(out_filev)):
                    if (os.path.getsize(out_filev) > 0):
                        mp4ok = True

        # GPU encoder 変換
        if (mp4ok == False) and (os.name == 'nt'):
            if (inp_filev != '') and (inp_filea != '') and (out_filev != ''):

                if (os.path.isfile(out_filev)):
                    os.remove(out_filev)

                # GPU encoder, intel GPU enable !
                ffmpeg = subprocess.Popen(['ffmpeg', '-y',
                    '-threads', '2',
                    '-init_hw_device', 'qsv:hw',
                    '-i', inp_filev, '-i', inp_filea,
                    '-vf', 'scale=1920:-1',
                    '-vcodec', 'h264_qsv', '-r', str(rate),
                    '-acodec', 'libmp3lame', '-strict', 'unofficial', '-ab', '96k', '-ac', '1', '-ar', '16000',
                    #'-acodec', 'aac', '-ab', '96k', '-ac', '1', '-ar', '16000',
                    out_filev,
                    '-loglevel', 'warning',
                    ], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

                #logb, errb = ffmpeg.communicate()
                ffmpeg.wait()
                ffmpeg.terminate()
                ffmpeg = None
                if (os.path.isfile(out_filev)):
                    if (os.path.getsize(out_filev) > 0):
                        mp4ok = True

        # software encoder 変換
        if (mp4ok == False):
            if (inp_filev != '') and (inp_filea != '') and (out_filev != ''):

                if (os.path.isfile(out_filev)):
                    os.remove(out_filev)

                # software encoder,
                ffmpeg = subprocess.Popen(['ffmpeg', '-y',
                    '-threads', '2',
                    '-i', inp_filev, '-i', inp_filea,
                    '-vcodec', 'libx265', '-r', str(rate),
                    '-acodec', 'libmp3lame', '-strict', 'unofficial', '-ab', '96k', '-ac', '1', '-ar', '16000',
                    #'-acodec', 'aac', '-ab', '96k', '-ac', '1', '-ar', '16000',
                    out_filev,
                    '-loglevel', 'warning',
                    ], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

                #logb, errb = ffmpeg.communicate()
                ffmpeg.wait()
                ffmpeg.terminate()
                ffmpeg = None
                if (os.path.isfile(out_filev)):
                    if (os.path.getsize(out_filev) > 0):
                        mp4ok = True

        # 動画変換

        # GPU encoder 変換
        if (mp4ok == False) and (os.name == 'nt'):
            if (inp_filev != '') and (out_filev != ''):

                if (os.path.isfile(out_filev)):
                    os.remove(out_filev)

                # GPU encoder, intel 6th GPU enable !
                ffmpeg = subprocess.Popen(['ffmpeg', '-y',
                    '-threads', '2',
                    '-init_hw_device', 'qsv:hw',
                    '-i', inp_filev,
                    '-vf', 'scale=1920:-1',
                    '-vcodec', 'hevc_qsv', '-r', str(rate),
                    out_filev,
                    '-loglevel', 'warning',
                    ], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

                #logb, errb = ffmpeg.communicate()
                ffmpeg.wait()
                ffmpeg.terminate()
                ffmpeg = None
                if (os.path.isfile(out_filev)):
                    if (os.path.getsize(out_filev) > 0):
                        mp4ok = True

        # GPU encoder 変換
        if (mp4ok == False) and (os.name == 'nt'):
            if (inp_filev != '') and (out_filev != ''):

                if (os.path.isfile(out_filev)):
                    os.remove(out_filev)

                # GPU encoder, intel GPU enable !
                ffmpeg = subprocess.Popen(['ffmpeg', '-y',
                    '-threads', '2',
                    '-init_hw_device', 'qsv:hw',
                    '-i', inp_filev,
                    '-vf', 'scale=1920:-1',
                    '-vcodec', 'h264_qsv', '-r', str(rate),
                    out_filev,
                    '-loglevel', 'warning',
                    ], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

                #logb, errb = ffmpeg.communicate()
                ffmpeg.wait()
                ffmpeg.terminate()
                ffmpeg = None
                if (os.path.isfile(out_filev)):
                    if (os.path.getsize(out_filev) > 0):
                        mp4ok = True

        # software encoder 変換
        if (mp4ok == False):
            if (inp_filev != '') and (out_filev != ''):

                if (os.path.isfile(out_filev)):
                    os.remove(out_filev)

                # software encoder,
                ffmpeg = subprocess.Popen(['ffmpeg', '-y',
                    '-threads', '2',
                    '-i', inp_filev,
                    '-vcodec', 'libx265', '-r', str(rate),
                    out_filev,
                    '-loglevel', 'warning',
                    ], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

                #logb, errb = ffmpeg.communicate()
                ffmpeg.wait()
                ffmpeg.terminate()
                ffmpeg = None
                if (os.path.isfile(out_filev)):
                    if (os.path.getsize(out_filev) > 0):
                        mp4ok = True

        # 音声処理
        mp3ok = False
        if (inp_filea != '') and (out_filea != ''):
            sox = subprocess.Popen(['sox', '-q', inp_filea, out_filea,
                ], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
            sox.wait()
            sox.terminate()
            sox = None
            if (os.path.isfile(out_filea)):
                if (os.path.getsize(out_filea) > 0):
                    mp3ok = True

        # 戻り値
        if   (mp4ok == True) and (mp3ok == True):
            return [out_filev, out_filea]
        elif (mp4ok == True) and (mp3ok == False):
            return [out_filev]
        elif (mp4ok == False) and (mp3ok == True):
            return [out_filea]
        else:
            return False



    def img2mov(self, inp_file='temp/_work/image.jpg', out_file='temp/_work/movie.mp4', \
                sec=300, rate=1, ):
        print('Warning... You used qFFmpeg.img2mov, Please using qCV.cv2img2mov, ')

        if (os.name == 'nt'):
            inp_file = inp_file.replace('/', '\\')
            out_file = out_file.replace('/', '\\')

        # 確認
        if (not os.path.isfile(inp_file)):
            return False

        # 削除
        if (os.path.isfile(out_file)):
            os.remove(out_file)

        # 変換
        ffmpeg = subprocess.Popen(['ffmpeg', '-y',
            '-loop', '1',
            #'-r', str(rate),
            '-r', '1',
            '-i', inp_file, 
            #'-vcodec', 'libx264',
            #'-vf', 'scale=1920:-1',
            #'-pix_fmt', 'yuv420p',
            '-t', str(sec),
            #'-r', str(rate),
            '-r', '1',
            out_file,
            '-loglevel', 'warning',
            ])
            #], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
        #logb, errb = ffmpeg.communicate()
        ffmpeg.wait()
        ffmpeg.terminate()
        ffmpeg = None

        # 戻り値
        if (os.path.isfile(out_file)):
            if (os.path.getsize(out_file) > 0):
                return out_file
        return False



class qFFplay_class:

    #波形表示メモ
    #オクターブ表示
    # ffmpeg -i "desktop/temp4.m4v" -filter_complex showcqt=size=640x360 -pix_fmt yuv420p -acodec copy -loglevel error -f matroska - | ffplay -i - -loglevel error
    # ffplay -f lavfi -i "amovie=desktop/temp4.m4v,asplit[out1],showcqt[out0]"
    #スペクトル表示
    # ffmpeg -i "desktop/temp4.m4v" -filter_complex showspectrum=size=640x360:slide=scroll:mode=separate -pix_fmt yuv420p -acodec copy -loglevel error -f matroska - | ffplay -i - -loglevel error
    #波形表示
    # ffmpeg -i "desktop/temp4.m4v" -filter_complex showwaves=size=640x360:mode=cline:split_channels=1 -pix_fmt yuv420p -acodec copy -loglevel error -f matroska - | ffplay -i - -loglevel error
    #スコープ表示
    # ffmpeg -i "desktop/temp4.m4v" -filter_complex avectorscope=size=640x360 -pix_fmt yuv420p -acodec copy -loglevel error -f matroska - | ffplay -i - -loglevel error

    #静止画再生
    #ffmpeg -loop 1 -r 1 -i "desktop/image.jpg" -t 10 -r 1 -f matroska - | ffplay -i - -autoexit

    def __init__(self, ):
        self.breakFlag  = threading.Event()
        self.breakDelay = 0
        self.breakFlag.clear()
        self.proc_beat  = None

        self.ffplay     = None
        self.ffpid      = None

    def __del__(self):
        self.breakDelay = 0
        self.breakFlag.clear()
        self.proc_beat  = None

        self.reset_ffplay()

    def reset_ffplay(self,):

        if (self.ffplay is not None):
            try:
                time.sleep(0.25)
                self.ffplay.terminate()
                self.ffplay = None
            except:
                self.ffplay = None

        if (self.ffpid is not None):
            time.sleep(0.25)
            qFunc.kill_pid(self.ffpid)
            self.ffpid = None

        try:
            del self.proc_main
            self.proc_main = None
        except:
            self.proc_main = None

        self.breakFlag.clear()

    def begin(self,
              delaySec=0, fadeSec=0, screen=0, panel='5+',
              title='qFFplay', play_file='', vol=100, fps=10, order='normal',
              overlayTime='', overlayDate='', startSec=0, limitSec=0, ):

        self.reset_ffplay()

        self.proc_main = threading.Thread(target=self.main_proc, args=(
                delaySec, fadeSec, screen, panel,
                title, play_file, vol, fps, order,
                overlayTime, overlayDate, startSec, limitSec,
        ), daemon=True, )

        self.breakDelay = 0
        self.breakFlag.clear()
        self.proc_beat  = None
        self.proc_main.start()

    def abort(self, waitMax=5, ):
        try:
            self.ffplay.stdin.write(b'q\n')
            self.ffplay.stdin.flush()
        except Exception as e:
            pass

        self.breakDelay = 0
        self.breakFlag.set()

        chktime = time.time()
        while (self.proc_beat is not None) and ((time.time() - chktime) <= waitMax):
            self.breakDelay = 0
            self.breakFlag.set()
            time.sleep(0.25)
        if (self.proc_beat is not None):
            print('qFFplay_class : abort -> break !')

        time.sleep(1.00)
        self.reset_ffplay()

    def delayAbort(self, delaySec=3, ):
        self.breakDelay = delaySec
        self.breakFlag.set()

    def is_alive(self, ):
        if (self.proc_beat is None):
            return False
        else:
            return True

    def main_proc(self, 
                  delaySec=0, fadeSec=0, screen=0, panel='5+',
                  title='qFFplay', play_file='', vol=100, fps=10, order='normal',
                  overlayTime='', overlayDate='', startSec=0, limitSec=0, ):

        startSec = round(startSec, 2)
        limitSec = round(limitSec, 2)
        input_file1 = play_file.replace('\\', '/')
        #if (os.name == 'nt'):
        #    input_file1 = play_file.replace('/', '\\')
        input_file2 = input_file1

        # 開始(待機)
        # time.sleep(delaySec)
        checkTime = time.time()
        while ((time.time() - checkTime) <= delaySec):
            time.sleep(0.10)
            # 停止要求確認
            if (self.breakFlag.is_set()):
                self.breakFlag.clear()
                print('ffplay delay break! (play cancel)')
                #break
                return

        # 表示位置
        qGUI.checkUpdateScreenInfo(update=True, )
        play_left, play_top, play_width, play_height = qGUI.getScreenPanelPosSize(screen=screen, panel=panel)

        # 開始自動フェード
        st_fadeStart = startSec
        st_fadeSec   = fadeSec + 4

        # 終了自動フェード
        ed_fadeStart = None
        ed_fadeSec   = fadeSec + 8
        if (limitSec > ed_fadeSec):
            ed_fadeStart = startSec + limitSec - ed_fadeSec

        # vf
        vf  = 'fps=' + str(fps)
        if (startSec != 0):
            vf += f",fade=t=in:st={ st_fadeStart :.2f}:d={ st_fadeSec - 2 :.2f}"
        if (ed_fadeStart is not None):
            vf += f",fade=t=out:st={ ed_fadeStart :.2f}:d={ ed_fadeSec - 2 :.2f}"
        if (overlayTime == 'yes'):
            vf += ",drawtext=fontfile=" + qFONT_DSEG7['file'] + ":fontsize=64:fontcolor=magenta:x=80:y=h-180:text='%{localtime\\:%H %M}'"
        if (overlayDate == 'yes'):
            vf += ",drawtext=fontfile=" + qFONT_default['file'] + ":fontsize=38:fontcolor=cyan:x=80:y=h-100:text='%{localtime\\:%Y-%m-%d}'"

        # af
        af = ''
        #if (startSec != 0):
        af = 'afade=t=in:st=' + str(st_fadeStart) + ':d=' + str(st_fadeSec - 1 )
        if (ed_fadeStart is not None):
            af += ',afade=t=out:st=' + str(ed_fadeStart) + ':d=' + str(ed_fadeSec - 1)

        # 再生コマンド
        Pcmd = []

        # 静止画対応
        if  (play_file[-4:].lower() == '.jpg') \
        or  (play_file[-4:].lower() == '.png'):
            if (limitSec == 0):
                limitSec = 60
            startSec    = 0
            input_file2 = '-'

            Pcmd.append('ffmpeg')
            Pcmd.append('-loop')
            Pcmd.append('1')
            Pcmd.append('-i')
            Pcmd.append(input_file1)
            Pcmd.append('-vcodec')
            Pcmd.append('libx264')
            Pcmd.append('-vf')
            Pcmd.append('scale=1920:-1')
            Pcmd.append('-pix_fmt')
            Pcmd.append('yuv420p')
            Pcmd.append('-r')
            Pcmd.append('1')
            Pcmd.append('-t')
            Pcmd.append(str(limitSec))
            Pcmd.append('-f')
            Pcmd.append('matroska')
            Pcmd.append(input_file2)
            Pcmd.append('-loglevel')
            Pcmd.append('error')
            Pcmd.append('|')

        Pcmd.append('ffplay')
        Pcmd.append('-i')
        Pcmd.append(input_file2)
        if (startSec != 0):
            Pcmd.append('-ss')
            Pcmd.append(str(startSec))
        if (limitSec != 0):
            Pcmd.append('-t')
            Pcmd.append(str(limitSec))
        if (float(vol) <= 0):
            Pcmd.append('-an')
        else:
            Pcmd.append('-volume')
            Pcmd.append(str(vol))
        if  (play_file[-4:].lower() == '.wav') \
        or  (play_file[-4:].lower() == '.mp3') \
        or  (play_file[-4:].lower() == '.m4a'):
            Pcmd.append('-showmode')
            Pcmd.append('1')
        Pcmd.append('-vf')
        Pcmd.append(vf)
        if (float(vol) > 0):
            Pcmd.append('-af')
            Pcmd.append(af)
        Pcmd.append('-noborder')
        Pcmd.append('-autoexit')
        Pcmd.append('-window_title')
        Pcmd.append(str(title))
        Pcmd.append('-left')
        Pcmd.append(str(play_left))
        Pcmd.append('-top')
        Pcmd.append(str(play_top))
        Pcmd.append('-x')
        Pcmd.append(str(play_width))
        Pcmd.append('-y')
        Pcmd.append(str(play_height))
        if (order == 'top'):
            Pcmd.append('-alwaysontop')
        Pcmd.append('-loglevel')
        Pcmd.append('error')

        #print(Pcmd)
        if (play_file[-4:].lower() == '.jpg') \
        or (play_file[-4:].lower() == '.png'):      # shell=True
            #self.ffplay = subprocess.Popen(Pcmd)
            self.ffplay = subprocess.Popen(Pcmd, \
            shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
            self.ffpid  = self.ffplay.pid
        else:
            #self.ffplay = subprocess.Popen(Pcmd)
            self.ffplay = subprocess.Popen(Pcmd, \
            shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
            self.ffpid  = self.ffplay.pid

        # １回だけ最前面実行
        run2top = False

        # 再生終了待機
        if (limitSec == 0):
            limitSec = 3600 * 4 #最大4時間

        try:
            checkTime = time.time()
            while (self.ffplay.poll() is None) and ((time.time() - checkTime) <= (limitSec + 5)):
                self.proc_beat = time.time()

                # 停止要求確認
                if (self.breakFlag.is_set()):
                    time.sleep(self.breakDelay)
                    self.breakFlag.clear()
                    break

                # １回だけ最前面実行
                if (order == 'top') and (run2top == False):
                    if ((time.time() - checkTime) > 1):
                        run2top = True
                        qGUI.setForegroundWindow(winTitle=title, )

                time.sleep(0.25)
        except:
            pass

        try:
            self.ffplay.stdin.write(b'q\n')
            self.ffplay.stdin.flush()
        except Exception as e:
            pass

        try:
            time.sleep(0.25)
            self.ffplay.terminate()
            self.ffplay = None
        except:
            self.ffplay = None

        time.sleep(0.25)
        qFunc.kill_pid(self.ffpid)
        self.ffpid = None

        # 終了
        self.proc_beat = None
        self.breakFlag.clear()



if __name__ == '__main__':

    qPath_work = 'temp/_work/'
    qFunc.makeDirs(qPath_work, remove=False, )

    # ffmpeg 操作
    qFFmpeg = qFFmpeg_class()
    qFFplay = qFFplay_class()
    qCV2    = qCV2_class()



    #inp_file = "_photos/_photo_cv.jpg"
    #out_file = "temp/temp1.mp4"
    #res = qFFmpeg.img2mov(inp_file, out_file, sec=10, rate=0.2, )
    #print(res)

    #inp_file = "_photos/_photo_cv.jpg"
    #out_file = "temp/temp2.mp4"
    #res = qCV2.cv2img2mov(inp_file, out_file, sec=10, rate=0.2, )
    #print(res)



#    qCV2.cv2open(dev='0', )
#    img = qCV2.cv2read()
#    # yolov8
#    out_image, _, _, _, _ = qCV2.cv2detect_yolov8(inp_image=img, search='person', )
#    if (out_image is not None):
#        proc_img = cv2.resize(out_image, (640, 360))
#        cv2.imshow('cv2 yolov8', proc_img)
#        cv2.waitKey(1)
#    time.sleep(10)
#    qCV2.cv2close()
#    cv2.destroyAllWindows()


    if (True):
        img=cv2.imread('_icons/dog.jpg')

        n = 100

        # ssd
        chkTime = time.time()
        for i in range(n):
            out_image, _, _, _, _ = qCV2.cv2detect_ssd(inp_image=img, search='person', )
        if (out_image is not None):
            proc_img = cv2.resize(out_image, (640, 360))
            cv2.imshow('cv2 ssd', proc_img)
            cv2.waitKey(1)
        print('cv2 ssd', float((time.time() - chkTime)/100*1000), 'ms', )

        # yolov4
        chkTime = time.time()
        for i in range(n):
            out_image, _, _, _, _ = qCV2.cv2detect_yolov4(inp_image=img, search='person', )
        if (out_image is not None):
            proc_img = cv2.resize(out_image, (640, 360))
            cv2.imshow('cv2 yolov4', proc_img)
            cv2.waitKey(1)
        print('cv2 yolov4', float((time.time() - chkTime)/100*1000), 'ms', )

        # yolov8
        chkTime = time.time()
        for i in range(n):
            out_image, _, _, _, _ = qCV2.cv2detect_yolov8(inp_image=img, search='person', )
        if (out_image is not None):
            proc_img = cv2.resize(out_image, (640, 360))
            cv2.imshow('cv2 yolov8', proc_img)
            cv2.waitKey(1)
        print('cv2 yolov8', float((time.time() - chkTime)/100*1000), 'ms', )

        time.sleep(10)
        cv2.destroyAllWindows()

        #cv2 ssd    137.03853607177734 ms
        #cv2 yolov4 89.66382503509521 ms
        #cv2 yolov8 190.63435316085815 ms



    if (True):

        print('')
        print('【デバイス名取得】')

        # デバイス名取得
        cam, mic = qFFmpeg.ffmpeg_list_dev()
        print('cam')
        print(cam)
        print('mic')
        print(mic)



    if (True):

        print('')
        print('【スクリーンショット】')

        # デスクトップ
        work_path = qPath_work + 'capture'
        img       = qFFmpeg.capture(dev='desktop', full=True, work_path=work_path, )
        if (img is not None):
            proc_img = cv2.resize(img, (640, 360))
            cv2.imshow('desktop', proc_img)
            cv2.waitKey(1)
            time.sleep(5.00)



    if (os.name == 'nt'):

        print('')
        print('【カメラ１ショット】')

        # カメラ
        count = 0
        for cam_dev in cam:
            work_path = qPath_work + 'capture_' + str(count)
            img       = qFFmpeg.capture(dev=cam_dev, full=True, work_path=work_path, )
            if (img is not None):
                proc_img = cv2.resize(img, (640, 360))
                cv2.imshow('capture_' + str(count), proc_img)
                cv2.waitKey(1)

            count += 1

        time.sleep(5.00)
        cv2.destroyAllWindows()



    if (True):

        print('')
        print('【ＣＶ２画像認識】（６０秒）')

        if (len(cam) > 0):
            qCV2.cv2open(dev='0', )

            checkTime = time.time()
            while ((time.time() - checkTime) < 60):

                img = qCV2.cv2read()
                if (img is not None):

                    # cascade
                    out_image, _ = qCV2.cv2detect_cascade(inp_image=img, search='face', )
                    if (out_image is not None):
                        proc_img = cv2.resize(out_image, (640, 360))
                        cv2.imshow('cv2 cascade', proc_img)
                        cv2.waitKey(1)

                    # ssd
                    out_image, _, _, _, _ = qCV2.cv2detect_ssd(inp_image=img, search='person', )
                    if (out_image is not None):
                        proc_img = cv2.resize(out_image, (640, 360))
                        cv2.imshow('cv2 ssd', proc_img)
                        cv2.waitKey(1)

                    # yolov4
                    out_image, _, _, _, _ = qCV2.cv2detect_yolov4(inp_image=img, search='person', )
                    if (out_image is not None):
                        proc_img = cv2.resize(out_image, (640, 360))
                        cv2.imshow('cv2 yolov4', proc_img)
                        cv2.waitKey(1)

                    # yolov8
                    out_image, _, _, _, _ = qCV2.cv2detect_yolov8(inp_image=img, search='person', )
                    if (out_image is not None):
                        proc_img = cv2.resize(out_image, (640, 360))
                        cv2.imshow('cv2 yolov8', proc_img)
                        cv2.waitKey(1)

                time.sleep(0.10)

            qCV2.cv2close()

        time.sleep(5.00)
        cv2.destroyAllWindows()



    if (os.name == 'nt'):

        print('')
        print('【レコーダー】（10秒）')

        # デスクトップレコーダー
        print('start')

        rec_filev = 'temp/_work/recorder.mp4'
        rec_filea = 'temp/_work/recorder.wav'
        ffmpeg, sox, rec_filev, rec_filea = qFFmpeg.rec_start(dev='desktop', rate=10, 
                                                                out_filev=rec_filev, out_filea=rec_filea,
                                                                retry_max=3, retry_wait=5.00,)
        time.sleep(10.00)

        print('stop')

        qFFmpeg.rec_stop(ffmpeg, sox,)
        ffmpeg = None
        sox    = None

        print(rec_filev, rec_filea, )



        print('')
        print('【動画変換】')

        # 動画変換

        mp4_filev = 'temp/_work/recorder_mp4.mp4'
        mp3_filea = 'temp/_work/recorder_mp3.mp3'
        res = qFFmpeg.encodemp4mp3(inp_filev=rec_filev, inp_filea=rec_filea, rate=10, 
                                   out_filev=mp4_filev, out_filea=mp3_filea,)

        print(mp4_filev)



        mp4_filev = 'temp/_work/recorder_mp4.mp4'

        print('')
        print('【動画再生】')

        # 動画再生

        delaySec = 0
        limitSec = 18
        qFFplay.begin(delaySec=0, fadeSec=0, screen=0, panel='5+',
              title='qFFplay', play_file=mp4_filev, vol=100, fps=30, order='top',
              overlayTime='', overlayDate='', limitSec=limitSec,)
        time.sleep(delaySec)

        print('')
        print('５秒後停止指示')
        qFFplay.delayAbort(5)

        print('')
        print('ステータス変化(is_alive)')
        checkTime = time.time()
        while ((time.time() - checkTime) <= 10):
            print('is_alive', qFFplay.is_alive())
            time.sleep(1.00)



    print('')
    print('おしまい')



