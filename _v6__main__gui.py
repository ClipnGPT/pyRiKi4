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

import psutil

import PySimpleGUI as sg

import platform
qPLATFORM = platform.system().lower() #windows,darwin,linux



import _v6__qRiKi_key

config_file = '_v6__main__gui_key.json'

qRiKi_key = _v6__qRiKi_key.qRiKi_key_class()
res, dic = qRiKi_key.getCryptJson(config_file=config_file, auto_crypt=False, )
if (res == False):
    dic['_crypt_'] = 'none'
    dic['btn11'] = 'ＢＧＭ開始'
    dic['cmd11'] = 'RiKi,ＢＧＭ開始'
    dic['btn12'] = 'ブラウザ開始'
    dic['cmd12'] = 'RiKi,ブラウザ開始'
    dic['btn13'] = '動画開始'
    dic['cmd13'] = 'RiKi,動画開始'
    dic['btn14'] = ''
    dic['cmd14'] = '14'
    dic['btn15'] = 'プログラム開始'
    dic['cmd15'] = 'RiKi,プログラム開始'
    dic['btn16'] = '全て終了'
    dic['cmd16'] = 'RiKi,ＢＧＭ・ブラウザ・動画・プログラム終了'
    dic['btn21'] = 'カメラ開始'
    dic['cmd21'] = 'RiKi,カメラ開始'
    dic['btn22'] = 'ミラー開始'
    dic['cmd22'] = 'RiKi,ミラー開始'
    dic['btn23'] = ''
    dic['cmd23'] = '23'
    dic['btn24'] = ''
    dic['cmd24'] = '24'
    dic['btn25'] = ''
    dic['cmd25'] = '25'
    dic['btn26'] = '全て終了'
    dic['cmd26'] = 'RiKi,カメラ終了'
    dic['btn31'] = '１分記録'
    dic['cmd31'] = 'RiKi,１分記録'
    dic['btn32'] = '記録開始'
    dic['cmd32'] = 'RiKi,記録開始'
    dic['btn33'] = '録画開始'
    dic['cmd33'] = 'RiKi,録画開始'
    dic['btn34'] = 'テレワーク開始'
    dic['cmd34'] = 'RiKi,テレワーク開始'
    dic['btn35'] = ''
    dic['cmd35'] = '35'
    dic['btn36'] = '全て終了'
    dic['cmd36'] = 'RiKi,記録・録画・テレワーク終了'
    dic['btn41'] = 'リセット'
    dic['cmd41'] = 'RiKi,リセット'
    dic['btn42'] = 'リブート'
    dic['cmd42'] = 'RiKi,リブート'
    dic['btn43'] = ''
    dic['cmd43'] = '43'
    dic['btn44'] = ''
    dic['cmd44'] = '44'
    dic['btn45'] = ''
    dic['cmd45'] = '45'
    dic['btn46'] = 'システム終了'
    dic['cmd46'] = 'RiKi,システム終了'
    res = qRiKi_key.putCryptJson(config_file=config_file, put_dic=dic, )



class sgDashGraph(object):

    def __init__(self, graph_elem, starting_count, color):
        self.GRAPH_WIDTH = 120
        self.GRAPH_HEIGHT = 40

        self.graph_current_item = 0
        self.graph_elem = graph_elem
        self.prev_value = starting_count
        self.max_sent = 1
        self.color = color

    def graph_value(self, current_value):
        delta = current_value - self.prev_value
        self.prev_value = current_value
        self.max_sent = max(self.max_sent, delta)
        percent_sent = 100 * delta / self.max_sent
        self.graph_elem.draw_line((self.graph_current_item, 0),
                                  (self.graph_current_item, percent_sent),
                                  color=self.color)
        if self.graph_current_item >= self.GRAPH_WIDTH:
            self.graph_elem.move(-1, 0)
        else:
            self.graph_current_item += 1
        return delta

    def graph_percentage_abs(self, value):
        self.graph_elem.draw_line((self.graph_current_item, 0),
                                  (self.graph_current_item, value),
                                  color=self.color)
        if self.graph_current_item >= self.GRAPH_WIDTH:
            self.graph_elem.move(-1, 0)
        else:
            self.graph_current_item += 1

def bytes2str(bytes, units=['  Byte', ' KByte', ' MByte', ' GByte', ' TByte', ' PByte', ' EByte']):
    if (bytes < 1024):
        return '{:4d}'.format(bytes) + units[0]
    else:
        return bytes2str(int(bytes) >> 10, units[1:])

def sgGraphColumn(name, key):
    GRAPH_WIDTH = 120
    GRAPH_HEIGHT = 40

    layout = [
        [sg.Text(name, font=('Courier 8'), key=key+'TXT_')],
        [sg.Graph((GRAPH_WIDTH, GRAPH_HEIGHT),
                    (0, 0),
                    (GRAPH_WIDTH, 120),
                    background_color='Black',
                    key=key+'GRAPH_')]]
    return sg.Col(layout, pad=(2, 2))

def sgButton(name, key):
    btn = sg.Button(name, key=key, size=(15,2),
                          button_color=('White','Darkcyan'), pad=(1, 1))
    return btn

class main_gui_class:

    def __init__(self, ):

        # 初期化
        self.window = None


    def init(self, alpha_channel=1,):

        # メニュー
        json_file = '_v6__main__gui_key.json'
        dic_btn = {}
        dic_cmd = {}
        dic_btn['11'] = 'ブラウザ開始'
        dic_cmd['11'] = 'RiKi,ブラウザ開始'
        dic_btn['12'] = 'ブラウザ終了'
        dic_cmd['12'] = 'RiKi,ブラウザ終了'
        dic_btn['13'] = ''
        dic_cmd['13'] = '13'
        dic_btn['14'] = ''
        dic_cmd['14'] = '14'
        dic_btn['15'] = 'プログラム開始'
        dic_cmd['15'] = 'RiKi,プログラム開始'
        dic_btn['16'] = 'プログラム終了'
        dic_cmd['16'] = 'RiKi,プログラム終了'
        dic_btn['21'] = 'カメラ開始'
        dic_cmd['21'] = 'RiKi,カメラ開始'
        dic_btn['22'] = 'ミラー開始'
        dic_cmd['22'] = 'RiKi,ミラー開始'
        dic_btn['23'] = ''
        dic_cmd['23'] = '23'
        dic_btn['24'] = ''
        dic_cmd['24'] = '24'
        dic_btn['25'] = ''
        dic_cmd['25'] = '25'
        dic_btn['26'] = '全て終了'
        dic_cmd['26'] = 'RiKi,カメラ終了'
        dic_btn['31'] = '１分記録'
        dic_cmd['31'] = 'RiKi,１分記録'
        dic_btn['32'] = '記録開始'
        dic_cmd['32'] = 'RiKi,記録開始'
        dic_btn['33'] = '録画開始'
        dic_cmd['33'] = 'RiKi,録画開始'
        dic_btn['34'] = 'テレワーク開始'
        dic_cmd['34'] = 'RiKi,テレワーク開始'
        dic_btn['35'] = ''
        dic_cmd['35'] = '35'
        dic_btn['36'] = '全て終了'
        dic_cmd['36'] = 'RiKi,記録・録画・テレワーク終了'
        dic_btn['41'] = 'リセット'
        dic_cmd['41'] = 'RiKi,リセット'
        dic_btn['42'] = 'リブート'
        dic_cmd['42'] = 'RiKi,リブート'
        dic_btn['43'] = ''
        dic_cmd['43'] = '43'
        dic_btn['44'] = ''
        dic_cmd['44'] = '44'
        dic_btn['45'] = ''
        dic_cmd['45'] = '45'
        dic_btn['46'] = 'システム終了'
        dic_cmd['46'] = 'RiKi,システム終了'
        res, json_dic = qRiKi_key.getCryptJson(config_file=json_file, auto_crypt=False, )
        if (res == True):
            dic_btn['11'] = json_dic['btn11']
            dic_cmd['11'] = json_dic['cmd11']
            dic_btn['12'] = json_dic['btn12']
            dic_cmd['12'] = json_dic['cmd12']
            dic_btn['13'] = json_dic['btn13']
            dic_cmd['13'] = json_dic['cmd13']
            dic_btn['14'] = json_dic['btn14']
            dic_cmd['14'] = json_dic['cmd14']
            dic_btn['15'] = json_dic['btn15']
            dic_cmd['15'] = json_dic['cmd15']
            dic_btn['16'] = json_dic['btn16']
            dic_cmd['16'] = json_dic['cmd16']
            dic_btn['21'] = json_dic['btn21']
            dic_cmd['21'] = json_dic['cmd21']
            dic_btn['22'] = json_dic['btn22']
            dic_cmd['22'] = json_dic['cmd22']
            dic_btn['23'] = json_dic['btn23']
            dic_cmd['23'] = json_dic['cmd23']
            dic_btn['24'] = json_dic['btn24']
            dic_cmd['24'] = json_dic['cmd24']
            dic_btn['25'] = json_dic['btn25']
            dic_cmd['25'] = json_dic['cmd25']
            dic_btn['26'] = json_dic['btn26']
            dic_cmd['26'] = json_dic['cmd26']
            dic_btn['31'] = json_dic['btn31']
            dic_cmd['31'] = json_dic['cmd31']
            dic_btn['32'] = json_dic['btn32']
            dic_cmd['32'] = json_dic['cmd32']
            dic_btn['33'] = json_dic['btn33']
            dic_cmd['33'] = json_dic['cmd33']
            dic_btn['34'] = json_dic['btn34']
            dic_cmd['34'] = json_dic['cmd34']
            dic_btn['35'] = json_dic['btn35']
            dic_cmd['35'] = json_dic['cmd35']
            dic_btn['36'] = json_dic['btn36']
            dic_cmd['36'] = json_dic['cmd36']
            dic_btn['41'] = json_dic['btn41']
            dic_cmd['41'] = json_dic['cmd41']
            dic_btn['42'] = json_dic['btn42']
            dic_cmd['42'] = json_dic['cmd42']
            dic_btn['43'] = json_dic['btn43']
            dic_cmd['43'] = json_dic['cmd43']
            dic_btn['44'] = json_dic['btn44']
            dic_cmd['44'] = json_dic['cmd44']
            dic_btn['45'] = json_dic['btn45']
            dic_cmd['45'] = json_dic['cmd45']
            dic_btn['46'] = json_dic['btn46']
            dic_cmd['46'] = json_dic['cmd46']

        dic_color = {}
        for id in dic_btn:
            if (dic_btn[id] != ''):
                dic_color[id] = ('Black', 'White') #20210321
            else:
                dic_color[id] = ('White', 'Black') #20210321

        # PySimpleGUI
        sg.theme('Black')
        sg.set_options(element_padding=(0,0), margins=(1,1), border_width=0)

        # レイアウト
        red_x = "R0lGODlhEAAQAPeQAIsAAI0AAI4AAI8AAJIAAJUAAJQCApkAAJoAAJ4AAJkJCaAAAKYAAKcAAKcCAKcDA6cGAKgAAKsAAKsCAKwAAK0AAK8AAK4CAK8DAqUJAKULAKwLALAAALEAALIAALMAALMDALQAALUAALYAALcEALoAALsAALsCALwAAL8AALkJAL4NAL8NAKoTAKwbAbEQALMVAL0QAL0RAKsREaodHbkQELMsALg2ALk3ALs+ALE2FbgpKbA1Nbc1Nb44N8AAAMIWAMsvAMUgDMcxAKVABb9NBbVJErFYEq1iMrtoMr5kP8BKAMFLAMxKANBBANFCANJFANFEB9JKAMFcANFZANZcANpfAMJUEMZVEc5hAM5pAMluBdRsANR8AM9YOrdERMpIQs1UVMR5WNt8X8VgYMdlZcxtYtx4YNF/btp9eraNf9qXXNCCZsyLeNSLd8SSecySf82kd9qqc9uBgdyBgd+EhN6JgtSIiNuJieGHhOGLg+GKhOKamty1ste4sNO+ueenp+inp+HHrebGrefKuOPTzejWzera1O7b1vLb2/bl4vTu7fbw7ffx7vnz8f///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAJAALAAAAAAQABAAAAjUACEJHEiwYEEABniQKfNFgQCDkATQwAMokEU+PQgUFDAjjR09e/LUmUNnh8aBCcCgUeRmzBkzie6EeQBAoAAMXuA8ciRGCaJHfXzUMCAQgYooWN48anTokR8dQk4sELggBhQrU9Q8evSHiJQgLCIIfMDCSZUjhbYuQkLFCRAMAiOQGGLE0CNBcZYmaRIDLqQFGF60eTRoSxc5jwjhACFWIAgMLtgUocJFy5orL0IQRHAiQgsbRZYswbEhBIiCCH6EiJAhAwQMKU5DjHCi9gnZEHMTDAgAOw=="
        layout = [
                # タイトル
                [sg.Button('', image_data=red_x, key='-exit-',  button_color=('Black', 'Black'), tooltip='Closes'), sg.Text('Power of AI, RiKi,')],
                # 内容
                [
                    # Extention
                    sg.Frame(layout=[
                            [sg.Text('')],
                            [sg.Button(dic_btn['11'], key=dic_cmd['11'], size=(18,2), button_color=dic_color['11'])],
                            [sg.Text('')],
                            [sg.Button(dic_btn['12'], key=dic_cmd['12'], size=(18,2), button_color=dic_color['12'])],
                            [sg.Text('')],
                            [sg.Button(dic_btn['13'], key=dic_cmd['13'], size=(18,2), button_color=dic_color['13'])],
                            [sg.Text('')],
                            [sg.Button(dic_btn['14'], key=dic_cmd['14'], size=(18,2), button_color=dic_color['14'])],
                            [sg.Text('')],
                            [sg.Button(dic_btn['15'], key=dic_cmd['15'], size=(18,2), button_color=dic_color['15'])],
                            [sg.Text('')],
                            [sg.Button(dic_btn['16'], key=dic_cmd['16'], size=(18,2), button_color=dic_color['16'])],
                            [sg.Text('')],
                            [sg.Text('Now Telework !', key='_STS_TELEWORK_', size=(18,1), justification='center', background_color='Gray')],
                        ], title='Extention Command'),
                    # vision
                    sg.Frame(layout=[
                            [sg.Text('')],
                            [sg.Button(dic_btn['21'], key=dic_cmd['21'], size=(18,2), button_color=dic_color['21'])],
                            [sg.Text('')],
                            [sg.Button(dic_btn['22'], key=dic_cmd['22'], size=(18,2), button_color=dic_color['22'])],
                            [sg.Text('')],
                            [sg.Button(dic_btn['23'], key=dic_cmd['23'], size=(18,2), button_color=dic_color['23'])],
                            [sg.Text('')],
                            [sg.Button(dic_btn['24'], key=dic_cmd['24'], size=(18,2), button_color=dic_color['24'])],
                            [sg.Text('')],
                            [sg.Button(dic_btn['25'], key=dic_cmd['25'], size=(18,2), button_color=dic_color['25'])],
                            [sg.Text('')],
                            [sg.Button(dic_btn['26'], key=dic_cmd['26'], size=(18,2), button_color=dic_color['26'])],
                            [sg.Text('')],
                            [sg.Text('')],
                        ], title='Vision Command'),
                    # desktop
                    sg.Frame(layout=[
                            [sg.Text('')],
                            [sg.Button(dic_btn['31'], key=dic_cmd['31'], size=(18,2), button_color=dic_color['31'])],
                            [sg.Text('')],
                            [sg.Button(dic_btn['32'], key=dic_cmd['32'], size=(18,2), button_color=dic_color['32'])],
                            [sg.Text('')],
                            [sg.Button(dic_btn['33'], key=dic_cmd['33'], size=(18,2), button_color=dic_color['33'])],
                            [sg.Text('')],
                            [sg.Button(dic_btn['34'], key=dic_cmd['34'], size=(18,2), button_color=dic_color['34'])],
                            [sg.Text('')],
                            [sg.Button(dic_btn['35'], key=dic_cmd['35'], size=(18,2), button_color=dic_color['35'])],
                            [sg.Text('')],
                            [sg.Button(dic_btn['36'], key=dic_cmd['36'], size=(18,2), button_color=dic_color['36'])],
                            [sg.Text('')],
                            [sg.Text('Now Recording !', key='_STS_RECORD_', size=(18,1), justification='center', background_color='Gray')],
                        ], title='Desktop Command'),
                    # kernel
                    sg.Frame(layout=[
                            [sg.Text('')],
                            [sg.Button(dic_btn['41'], key=dic_cmd['41'], size=(18,2), button_color=dic_color['41'])],
                            [sg.Text('')],
                            [sg.Button(dic_btn['42'], key=dic_cmd['42'], size=(18,2), button_color=dic_color['42'])],
                            [sg.Text('')],
                            [sg.Button(dic_btn['43'], key=dic_cmd['43'], size=(18,2), button_color=dic_color['43'])],
                            [sg.Text('')],
                            [sg.Button(dic_btn['44'], key=dic_cmd['44'], size=(18,2), button_color=dic_color['44'])],
                            [sg.Text('')],
                            [sg.Button(dic_btn['45'], key=dic_cmd['45'], size=(18,2), button_color=dic_color['45'])],
                            [sg.Text('')],
                            [sg.Button(dic_btn['46'], key=dic_cmd['46'], size=(18,2), button_color=dic_color['46'])],
                            [sg.Text('')],
                            [sg.Text('Speech READY !', key='_STS_SPEECH_', size=(18,1), justification='center', background_color='Gray')],
                        ], title='Kernel Command'),
                    # status
                    sg.Frame(layout=[

                            # Graph
                            [sgGraphColumn('CPU Usage          ', '_CPU_')],
                            [sgGraphColumn('MEM Usage          ', '_MEM_')],
                            [sgGraphColumn('NET Out            ', '_NET_OUT_')],
                            [sgGraphColumn('NET In             ', '_NET_IN_')],
                            [sgGraphColumn('DISK Read          ', '_DISK_READ_')],
                            [sgGraphColumn('DISK Write         ', '_DISK_WRITE_')],
                            [sg.Text(' ', font=('Courier 6'))],

                        ], title='System Status'),
                ],
                #　ボタン
                [sg.Text('_' * 256, size=(120,1))],
                [sgButton('ＯＫ', key='-ok-'), sg.Text(' ', size=(5,2)), sgButton('キャンセル', key='-cancel-')],
        ]

        # 定義
        self.close()
        #try:
        if True:
            no_titlebar = True
            if (qPLATFORM == 'darwin'):
                no_titlebar = False
            self.window = sg.Window('Power of AI, RiKi, ', layout,
                            keep_on_top=True,
                            no_titlebar=no_titlebar,
                            alpha_channel=alpha_channel,
                            finalize=True,
                            size=(760, 480),
                            )

            # setup graphs & initial values
            self.cpu_usage_graph = sgDashGraph(self.window['_CPU_GRAPH_'], 0, '#d34545')
            self.mem_usage_graph = sgDashGraph(self.window['_MEM_GRAPH_'], 0, '#BE7C29')
            net_io = psutil.net_io_counters()
            net_in = self.window['_NET_IN_GRAPH_']
            self.net_graph_in = sgDashGraph(net_in, net_io.bytes_recv, '#23a0a0')
            net_out = self.window['_NET_OUT_GRAPH_']
            self.net_graph_out = sgDashGraph(net_out, net_io.bytes_sent, '#56d856')
            disk_io = psutil.disk_io_counters()
            self.disk_graph_write = sgDashGraph(self.window['_DISK_WRITE_GRAPH_'], disk_io.write_bytes, '#be45be')
            self.disk_graph_read = sgDashGraph(self.window['_DISK_READ_GRAPH_'], disk_io.read_bytes, '#5681d8')

            # status reset
            self.status_speech = False
            self.window['_STS_SPEECH_'].update('', background_color='Black', )
            self.status_record = False
            self.window['_STS_RECORD_'].update('', background_color='Black', )
            self.status_telework = False
            self.window['_STS_TELEWORK_'].update('', background_color='Black', )

        #except:
        #    self.window = None

        if (self.window is not None):
            return True
        else:
            return False

    def open(self, ):
        # 更新・表示
        #try:
        if True:
            if (self.window is not None):
                self.window.un_hide()
                self.window.refresh()
                return True
        #except:
        #    pass
        return False

    def read(self, ):
        # update graphs
        cpu = psutil.cpu_percent(0)
        self.cpu_usage_graph.graph_percentage_abs(cpu)
        self.window['_CPU_TXT_'].update('CPU    {:5.1f} %'.format(cpu))
        mem_used = psutil.virtual_memory().percent
        self.mem_usage_graph.graph_percentage_abs(mem_used)
        self.window['_MEM_TXT_'].update('MEM    {:5.1f} %'.format(mem_used))
        net_io = psutil.net_io_counters()
        write_bytes = self.net_graph_out.graph_value(net_io.bytes_sent)
        read_bytes = self.net_graph_in.graph_value(net_io.bytes_recv)
        self.window['_NET_OUT_TXT_'].update('NET  O:{}'.format(bytes2str(write_bytes)))
        self.window['_NET_IN_TXT_'].update('NET  I:{}'.format(bytes2str(read_bytes)))
        disk_io = psutil.disk_io_counters()
        write_bytes = self.disk_graph_write.graph_value(disk_io.write_bytes)
        read_bytes = self.disk_graph_read.graph_value(disk_io.read_bytes)
        self.window['_DISK_WRITE_TXT_'].update('DISK W:{}'.format(bytes2str(write_bytes)))
        self.window['_DISK_READ_TXT_'].update('DISK R:{}'.format(bytes2str(read_bytes)))

        # update status
        if (self.status_speech != True):
            self.window['_STS_SPEECH_'].update('', background_color='Black', )
        else:
            self.window['_STS_SPEECH_'].update('Speech READY !', background_color='Green')
        if (self.status_record != True):
            self.window['_STS_RECORD_'].update('', background_color='Black', )
        else:
            self.window['_STS_RECORD_'].update('Now Recording !', background_color='Magenta')
        if (self.status_telework != True):
            self.window['_STS_TELEWORK_'].update('', background_color='Black', )
        else:
            self.window['_STS_TELEWORK_'].update('Now Telework !', background_color='Magenta')

        # 読取
        #try:
        if True:
            if (self.window is not None):
                event, values = self.window.read(timeout=20, timeout_key='-timeout-')
                return event, values
        #except:
        #    pass
        return False, False

    def statusSet(self, key, value):
        if   (key == '_STS_SPEECH_'):
            self.status_speech = value
        elif (key == '_STS_RECORD_'):
            self.status_record = value
        elif (key == '_STS_TELEWORK_'):
            self.status_telework = value
        return True

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



if __name__ == '__main__':

    GUI = main_gui_class()

    GUI.init()
    GUI.open()

    chkTime = time.time()
    while ((time.time() - chkTime) < 30):
        event, values = GUI.read()
        #print(event)
        if (event in (None, '-exit-', '-cancel-')):
            break
        if (event == '-ok-'):
            print(event, values)
            break
        if (event[:5].lower() == 'riki,'):
            print(event, values)
            break

        if ((time.time() - chkTime) > 5):
            GUI.statusSet('_STS_SPEECH_',   True)
        if ((time.time() - chkTime) > 10):
            GUI.statusSet('_STS_RECORD_',   True)
        if ((time.time() - chkTime) > 15):
            GUI.statusSet('_STS_RECORD_',   False)
            GUI.statusSet('_STS_TELEWORK_', True)

        time.sleep(0.10)

    GUI.close()
    GUI.terminate()


