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

import io

import numpy as np
import cv2

import PySimpleGUI as sg

from PIL import Image, ImageDraw, ImageFont
if (os.name == 'nt'):
    import win32clipboard

import platform
qPLATFORM = platform.system().lower() #windows,darwin,linux



# 共通ルーチン
import  _v6__qGUI
qGUI  = _v6__qGUI.qGUI_class()



qPath_fonts     = '_fonts/'
qPath_icons     = '_icons/'



class qGuide_class:

    def __init__(self, ):

        # 初期化
        self.screen = 0
        self.panel  = '5'
        self.title  = 'Guide_5'
        self.image  = None

        self.window = None
        self.left   = 0
        self.top    = 0
        self.width  = 320
        self.height = 240

        # フォント
        self.font_default = {'file':qPath_fonts + '_vision_font_ipaexg.ttf','offset':8}
        self.font_status  = {'file':qPath_fonts + '_vision_font_ipag.ttf',  'offset':8}
        try:
            self.font32_default  = ImageFont.truetype(self.font_default['file'], 32, encoding='unic')
            self.font32_defaulty =                    self.font_default['offset']
        except:
            self.font32_default  = None
            self.font32_defaulty = 0

    def init(self, screen=0, panel='5', title='', image=None, alpha_channel=1,
        keep_on_top=True, no_titlebar=True, disable_close=False,
        resizable=False, icon=None, theme='Black', guideOffset='auto', ):

        # タイトル
        if (title ==''):
            title = 'Guide_' + panel
        self.title = title

        # 表示位置
        self.screen = screen
        self.panel  = panel
        #self.left, self.top, self.width, self.height = qGUI.getPanelPos(self.panel,)
        qGUI.checkUpdateScreenInfo(update=True, )
        self.left, self.top, self.width, self.height = qGUI.getScreenPanelPosSize(screen=screen, panel=panel, )
        image_height, image_width = self.width, self.height

        if (image is None):
            self.image = None
            image_width  = 320
            image_height = 160
            #self.image = np.zeros((image_height, image_width, 3), np.uint8)
        else:
            self.image = image.copy()
            image_height, image_width = image.shape[:2]

        # 表示位置 調整
        if  (self.title != 'detect_face') \
        and (self.title != 'detect_speech'):

            if (guideOffset=='auto'):
                if (self.panel == '7') \
                or (self.panel == '8') \
                or (self.panel == '9'):
                    self.top -= 50

        if (self.title.find('_guide_') >= 0):
            if (guideOffset=='auto'):
                self.height = int(self.height/4)    #DANGER !
                if (self.panel == '7') \
                or (self.panel == '8') \
                or (self.panel == '9'):
                    self.top += (self.height * 3)

        elif  (self.title == 'detect_face'):
            #w, h = qGUI.size()
            l, t, w, h = qGUI.getScreenPosSize(screen=self.screen)
            chksec9 = int(time.time()) % 10
            chksec2 = int(time.time()) % 2
            self.left   = int(w * (chksec9 * 0.1))
            self.top    = int(h * (chksec2 * 0.1))
            self.top   += int(h * 0.1)
            self.width  = int(w * 0.1)
            self.height = int(self.width * image_height / image_width)
            self.title  = 'Face_' + str(chksec9)
            self.image  = cv2.resize(image, (self.width, self.height))

        elif  (self.title == 'detect_speech'):
            #w, h = qGUI.size()
            l, t, w, h = qGUI.getScreenPosSize(screen=self.screen)
            chksec5 = int(time.time()) % 5
            chksec2 = int(time.time()) % 2
            self.left   = int(w * (chksec5 * 0.2))
            self.top    = int(h * (chksec2 * 0.1))
            self.top   += int(h * 0.7)
            self.width  = int(w * 0.2)
            self.height = int(self.width * image_height / image_width)
            self.title  = 'Speech_' + str(chksec5)
            self.image  = cv2.resize(image, (self.width, self.height))

        elif  (self.title == 'RiKi_cpuClock[analog]'):
            #w, h = qGUI.size()
            l, t, w, h = qGUI.getScreenPosSize(screen=self.screen)
            self.width  = int(h * 2 / 3) - 50
            self.height = int(h * 2 / 3) - 50
            self.left   = l + w - self.width
            self.top    = t

        elif  (self.title == 'RiKi_cpuClock[digital]'):
            #w, h = qGUI.size()
            l, t, w, h = qGUI.getScreenPosSize(screen=self.screen)
            self.width  = int(h * 2 / 3) - 50
            self.height = int(h * 2 / 3 / 2) - 50
            self.left   = l + w - self.width
            self.top    = t

        # PySimpleGUI
        sg.theme(theme)
        sg.set_options(element_padding=(0,0), margins=(1,1), border_width=0)

        # レイアウト
        red_x = "R0lGODlhEAAQAPeQAIsAAI0AAI4AAI8AAJIAAJUAAJQCApkAAJoAAJ4AAJkJCaAAAKYAAKcAAKcCAKcDA6cGAKgAAKsAAKsCAKwAAK0AAK8AAK4CAK8DAqUJAKULAKwLALAAALEAALIAALMAALMDALQAALUAALYAALcEALoAALsAALsCALwAAL8AALkJAL4NAL8NAKoTAKwbAbEQALMVAL0QAL0RAKsREaodHbkQELMsALg2ALk3ALs+ALE2FbgpKbA1Nbc1Nb44N8AAAMIWAMsvAMUgDMcxAKVABb9NBbVJErFYEq1iMrtoMr5kP8BKAMFLAMxKANBBANFCANJFANFEB9JKAMFcANFZANZcANpfAMJUEMZVEc5hAM5pAMluBdRsANR8AM9YOrdERMpIQs1UVMR5WNt8X8VgYMdlZcxtYtx4YNF/btp9eraNf9qXXNCCZsyLeNSLd8SSecySf82kd9qqc9uBgdyBgd+EhN6JgtSIiNuJieGHhOGLg+GKhOKamty1ste4sNO+ueenp+inp+HHrebGrefKuOPTzejWzera1O7b1vLb2/bl4vTu7fbw7ffx7vnz8f///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAJAALAAAAAAQABAAAAjUACEJHEiwYEEABniQKfNFgQCDkATQwAMokEU+PQgUFDAjjR09e/LUmUNnh8aBCcCgUeRmzBkzie6EeQBAoAAMXuA8ciRGCaJHfXzUMCAQgYooWN48anTokR8dQk4sELggBhQrU9Q8evSHiJQgLCIIfMDCSZUjhbYuQkLFCRAMAiOQGGLE0CNBcZYmaRIDLqQFGF60eTRoSxc5jwjhACFWIAgMLtgUocJFy5orL0IQRHAiQgsbRZYswbEhBIiCCH6EiJAhAwQMKU5DjHCi9gnZEHMTDAgAOw=="
        layout_no_titlebar = [[
                sg.Button('', image_data=red_x, button_color=('black', 'black'), key='-exit-', tooltip='Closes'),
                sg.Text(title, auto_size_text=True, ),
                ],[
                sg.Image(filename='', key='-image-', enable_events=True, ),
                ]]
        layout_with_title = [[
                sg.Image(filename='', key='-image-', enable_events=True, ),
                ]]

        # 定義
        self.close()
        try:
            #keep_on_top   = True
            #no_titlebar   = True
            #disable_close = False
            #resizable     = False
            #icon          = None
            if (qPLATFORM == 'darwin'):
                no_titlebar = False
            if (no_titlebar == True):
                self.window = sg.Window(self.title, layout_no_titlebar,
                            keep_on_top=keep_on_top,
                            auto_size_text=False,
                            auto_size_buttons=False,
                            grab_anywhere=True,
                            no_titlebar=True,
                            disable_close=disable_close,
                            default_element_size=(12, 1),
                            default_button_element_size=(12, 1),
                            return_keyboard_events=True,
                            alpha_channel=alpha_channel,
                            use_default_focus=False,
                            finalize=True,
                            location=(self.left, self.top),
                            size=(self.width + 4, self.height + 22),
                            resizable=resizable,
                            icon=icon, )
            else:
                self.window = sg.Window(self.title, layout_with_title,
                            keep_on_top=keep_on_top,
                            auto_size_text=False,
                            auto_size_buttons=False,
                            grab_anywhere=True,
                            no_titlebar=False,
                            disable_close=disable_close,
                            default_element_size=(12, 1),
                            default_button_element_size=(12, 1),
                            return_keyboard_events=True,
                            alpha_channel=alpha_channel,
                            use_default_focus=False,
                            finalize=True,
                            location=(self.left, self.top),
                            size=(self.width + 4, self.height + 22),
                            resizable=resizable,
                            icon=icon, )
            # イメージ更新
            if (self.image is not None):
                img = cv2.resize(self.image, (self.width, self.height))
            else:
                img = np.zeros((self.height, self.width, 3), np.uint8)
            png = cv2.imencode('.png', img)[1].tobytes()
            self.window['-image-'].update(data=png)

        except:
            self.window = None

        if (self.window is not None):
            return True
        else:
            return False

    def init_with_layout(self, screen=0, panel='5', title='', layout=None, alpha_channel=1,
        keep_on_top=True, no_titlebar=True, disable_close=False,
        resizable=False, icon=None, theme='Black', guideOffset='auto', ):

        # タイトル
        if (title ==''):
            title = 'Guide_' + panel
        self.title = title

        # 表示位置
        self.screen = screen
        self.panel  = panel
        #self.left, self.top, self.width, self.height = qGUI.getPanelPos(self.panel,)
        qGUI.checkUpdateScreenInfo(update=True, )
        self.left, self.top, self.width, self.height = qGUI.getScreenPanelPosSize(screen=screen, panel=panel, )

        # PySimpleGUI
        sg.theme(theme)
        #sg.set_options(element_padding=(0,0), margins=(1,1), border_width=0)

        # レイアウト
        if (layout is None):
            layout = [[
                    sg.Image(filename='', key='-image-', enable_events=True, ),
                    ]]

        # 定義
        self.close()
        try:
            #keep_on_top   = True
            #no_titlebar   = True
            #disable_close = False
            #resizable     = False
            #icon          = None
            if (qPLATFORM == 'darwin'):
                no_titlebar = False
            if (no_titlebar == True):
                self.window = sg.Window(self.title, layout,
                            keep_on_top=keep_on_top,
                            auto_size_text=False,
                            auto_size_buttons=False,
                            grab_anywhere=True,
                            no_titlebar=True,
                            disable_close=disable_close,
                            default_element_size=(12, 1),
                            default_button_element_size=(12, 1),
                            return_keyboard_events=False, #Danger!
                            alpha_channel=alpha_channel,
                            use_default_focus=False,
                            finalize=True,
                            location=(self.left, self.top),
                            size=(self.width + 4, self.height + 22),
                            resizable=resizable,
                            icon=icon, )
            else:
                self.window = sg.Window(self.title, layout,
                            keep_on_top=keep_on_top,
                            auto_size_text=False,
                            auto_size_buttons=False,
                            grab_anywhere=True,
                            no_titlebar=False,
                            disable_close=disable_close,
                            default_element_size=(12, 1),
                            default_button_element_size=(12, 1),
                            return_keyboard_events=False, #Danger!
                            alpha_channel=alpha_channel,
                            use_default_focus=False,
                            finalize=True,
                            location=(self.left, self.top),
                            size=(self.width + 4, self.height + 22),
                            resizable=resizable,
                            icon=icon, )

        except:
            self.window = None

        if (self.window is not None):
            return True
        else:
            return False

    def setImage(self, image=None, refresh=True, ):
        if (image is None):
            self.image = None
        else:
            self.image = image.copy()
        if (self.image is not None):
            img = cv2.resize(self.image, (self.width, self.height))
        else:
            img = np.zeros((self.height, self.width, 3), np.uint8)
        png = cv2.imencode('.png', img)[1].tobytes()
        self.window['-image-'].update(data=png)
        if (refresh == True):
            self.window.refresh()

    def setAlphaChannel(self, alpha_channel=1, ):
        try:
            self.window.alpha_channel=alpha_channel
        except:
            pass

    def setMessage(self, txt='', refresh=True, ):
        if (self.window is not None):
            if (self.image is not None):

                try:
                    img = cv2.resize(self.image, (self.width, self.height))

                    # 文字描写
                    if (txt != ''):
                        if (self.font32_default is None):
                            cv2.putText(img, txt, (5,self.height-15), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,0,255))
                        else:
                            pil_image = self.cv2pil(img)
                            text_draw = ImageDraw.Draw(pil_image)
                            text_draw.text((10, self.height-42), txt, font=self.font32_default, fill=(255,0,255))
                            img = self.pil2cv(pil_image)

                    # 更新
                    png = cv2.imencode('.png', img)[1].tobytes()
                    self.window['-image-'].update(data=png)
                    if (refresh == True):
                        self.window.refresh()
                    return True

                except:
                    pass

        return False

    def open(self, refresh=True, ):
        # 更新・表示
        #try:
        if True:
            if (self.window is not None):
                self.window.un_hide()
                if (refresh == True):
                    self.window.refresh()
                return True
        #except:
        #    pass
        return False

    def read(self, timeout=20, timeout_key='-timeout-', ):
        # 読取
        #try:
        if True:
            if (self.window is not None):
                event, values = self.window.read(timeout=timeout, timeout_key=timeout_key, )
                return event, values
        #except:
        #    pass
        return False, False

    def close(self, ):
        # 消去
        if (self.window is not None):
            #try:
            if True:
                self.read()
                self.window.hide()
                self.window.refresh()
            #except:
            #    pass
        return True

    def terminate(self, ):
        # 終了
        if (self.window is not None):
            #try:
            if True:
                self.read()
                self.window.close()
                del self.window
            #except:
            #    pass
        self.window = None
        return True



    def cv2pil(self, cv2_image=None):
        try:
            wrk_image = cv2_image.copy()
            if (wrk_image.ndim == 2):  # モノクロ
                pass
            elif (wrk_image.shape[2] == 3):  # カラー
                wrk_image = cv2.cvtColor(wrk_image, cv2.COLOR_BGR2RGB)
            elif (wrk_image.shape[2] == 4):  # 透過
                wrk_image = cv2.cvtColor(wrk_image, cv2.COLOR_BGRA2RGBA)
            pil_image = Image.fromarray(wrk_image)
            return pil_image
        except:
            pass
        return None

    def pil2cv(self, pil_image=None):
        try:
            cv2_image = np.array(pil_image, dtype=np.uint8)
            if (cv2_image.ndim == 2):  # モノクロ
                pass
            elif (cv2_image.shape[2] == 3):  # カラー
                cv2_image = cv2.cvtColor(cv2_image, cv2.COLOR_RGB2BGR)
            elif (cv2_image.shape[2] == 4):  # 透過
                cv2_image = cv2.cvtColor(cv2_image, cv2.COLOR_RGBA2BGRA)
            return cv2_image
        except:
            pass
        return None

    def img2clip(self, file):
        if (os.name == 'nt'):
            #try:
                img = Image.open(file)
                output = io.BytesIO()
                img.convert('RGB').save(output, 'BMP')
                data = output.getvalue()[14:]
                output.close()

                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
                win32clipboard.CloseClipboard()
                return True
            #except Exception as e:
            #    pass
        return False

    def getIconImage(self, filename='', ):
        if (filename != ''):
            imgfile = filename
            if (filename == '_kernel_start_'):
                imgfile = qPath_icons + 'RiKi_start.png'
            if (filename == '_kernel_stop_'):
                imgfile = qPath_icons + 'RiKi_stop.png'
            if (filename == '_kernel_guide_'):
                imgfile = qPath_icons + 'RiKi_guide.png'
            if (filename == '_speech_start_'):
                imgfile = qPath_icons + 'speech_start.png'
            if (filename == '_speech_stop_'):
                imgfile = qPath_icons + 'speech_stop.png'
            if (filename == '_speech_guide_'):
                imgfile = qPath_icons + 'speech_guide.png'
            if (filename == '_vision_start_'):
                imgfile = qPath_icons + 'cam_start.png'
            if (filename == '_vision_stop_'):
                imgfile = qPath_icons + 'cam_stop.png'
            if (filename == '_vision_guide_'):
                imgfile = qPath_icons + 'cam_guide.png'
            if (filename == '_desktop_start_'):
                imgfile = qPath_icons + 'rec_start.png'
            if (filename == '_desktop_stop_'):
                imgfile = qPath_icons + 'rec_stop.png'
            if (filename == '_desktop_guide_'):
                imgfile = qPath_icons + 'rec_guide.png'
            try:
                image = cv2.imread(imgfile)
                return image
            except Exception as e:
                pass
        return None

    # フェードアウト（フェード開始）
    def fadeOut(self, screen=0, panel='0', mask='black', outSec=2, ):
        if (mask != 'white'):
            img   = cv2.imread(qPath_icons + '__black.png')
            theme = 'Black'
        else:
            img   = cv2.imread(qPath_icons + '__white.png')
            theme = 'DefaultNoMoreNagging'
        self.init(screen=screen, panel=panel, title=mask, image=img, alpha_channel=0, theme=theme, guideOffset='off', )
        self.open()

        alpha = 0
        self.setAlphaChannel(alpha)

        chkTime = time.time()
        while ((time.time() - chkTime) < 5):
            event, values = self.read(timeout=int(outSec*1000/50), )
            if event in (None, '-exit-'):
                break
            alpha += 0.02
            if (alpha > 1):
                break
            self.setAlphaChannel(alpha)
            #time.sleep(0.01)
        alpha = 1
        self.setAlphaChannel(alpha)

        return True

    # フェードイン（フェード終了）
    def fadeIn(self, inSec=1, ):
        alpha = 1
        self.setAlphaChannel(alpha)

        chkTime = time.time()
        while ((time.time() - chkTime) < 5):
            event, values = self.read(timeout=int(inSec*1000/50), )
            if event in (None, '-exit-'):
                break
            alpha -= 0.02
            if (alpha < 0):
                break
            self.setAlphaChannel(alpha)
            #time.sleep(0.01)
        alpha = 0
        self.setAlphaChannel(alpha)

        self.close()
        self.terminate()

        return True



if __name__ == '__main__':

    qGuide = qGuide_class()

    if (True):
        res=qGuide.fadeOut(screen=0, panel='0', mask='black', outSec=2, )
        res=qGuide.fadeIn(inSec=1, )

    if (True):
        img = cv2.imread(qPath_icons + 'RiKi_start.png')
        qGuide.init(screen=0, panel='5', title='', image=img,)
        qGuide.open()
        time.sleep(1.00)
        qGuide.setMessage(txt='開始中．．．', )

        time.sleep(3.00)

        img = cv2.imread(qPath_icons + 'RiKi_stop.png')
        qGuide.setImage(image=img, )
        time.sleep(1.00)
        qGuide.setMessage(txt='終了中．．．', )

        time.sleep(5.00)


    if (True):
        img = cv2.imread(qPath_icons + 'RiKi_base.png')
        qGuide.init(screen=0, panel='5', title='_guide_', image=img,)
        qGuide.setMessage(txt='こんにちは', )
        #qGuide.open()

        chkTime = time.time()
        while ((time.time() - chkTime) < 5):
            event, values = qGuide.read()
            #print(event, values)
            if event in (None, '-exit-'):
                break
        qGuide.close()
        qGuide.terminate()
 


