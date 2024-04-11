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



import logging
from rainbow_logging_handler import RainbowLoggingHandler



class qLog_class:

    def __init__(self, ):
        global qLog_mode
        global qLog_file
        qLog_mode     = 'logger'
        qLog_file     = ''

        self.display  = True
        self.outfile  = False

    def init(self, mode='logger', filename='', display=True, outfile=True, ):
        global qLog_mode
        global qLog_file
        global qLog_logger_disp
        global qLog_logger_file

        qLog_mode     = mode
        if (filename == ''):
            if (not os.path.isdir('temp')):
                os.makedirs('temp')
            if (not os.path.isdir('temp/_log')):
                os.makedirs('temp/_log')
            nowTime = datetime.datetime.now()
            qLog_file = 'temp/_log/' + nowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
        else:
            qLog_file = filename
        self.display  = display
        self.outfile  = outfile

        # ロガー定義
        if (qLog_mode == 'logger'):
            qLog_logger_disp = logging.getLogger('RiKiDisp')
            qLog_logger_disp.setLevel(logging.DEBUG)
            for h in qLog_logger_disp.handlers:
                qLog_logger_disp.removeHandler(h)
            qLog_logger_file = logging.getLogger('RiKiFile')
            qLog_logger_file.setLevel(logging.DEBUG)
            for h in qLog_logger_file.handlers:
                qLog_logger_file.removeHandler(h)

        # コンソールハンドラー
        if (qLog_mode == 'logger'):
            console_format  = logging.Formatter('%(asctime)s %(message)s')
            console_handler = RainbowLoggingHandler(sys.stderr, color_funcName=('black', 'yellow', True))
            console_handler.setFormatter(console_format)
            qLog_logger_disp.addHandler(console_handler)

        # ファイルハンドラー
        if (qLog_mode == 'logger'):
            file_format  = logging.Formatter('%(asctime)s, %(lineno)d, %(levelname)s, %(message)s')
            file_handler = logging.FileHandler(qLog_file, 'a', 'utf-8', )
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(file_format)
            qLog_logger_file.addHandler(file_handler)

    def log(self, level='info', proc='', msg='info', mode=None, display=None, outfile=None,):
        global qLog_mode
        global qLog_file
        global qLog_logger_disp
        global qLog_logger_file

        if (proc == ''):
            procname = ''
        else:
            procname = proc + ' : '

        if (mode is None):
            try:
                mode = qLog_mode
            except:
                mode = 'logger'

        if (display is None):
            try:
                display = self.display
            except:
                display=True
        if (outfile is None):
            try:
                outfile = self.outfile
            except:
                outfile = True

        # ログ出力（logger）
        txt = str(procname + msg)
        if (mode == 'logger'):
            try:
                if   (level=='info') or (level==logging.INFO):
                    if (display == True):
                        qLog_logger_disp.info(txt)
                    if (outfile == True):
                        qLog_logger_file.info(txt)
                elif (level=='debug') or (level==logging.DEBUG):
                    if (display == True):
                        qLog_logger_disp.debug(txt)
                    if (outfile == True):
                        qLog_logger_file.debug(txt)
                elif (level=='warning') or (level==logging.WARNING):
                    if (display == True):
                        qLog_logger_disp.warning(txt)
                    if (outfile == True):
                        qLog_logger_file.warning(txt)
                elif (level=='error') or (level==logging.ERROR):
                    if (display == True):
                        qLog_logger_disp.error(txt)
                    if (outfile == True):
                        qLog_logger_file.error(txt)
                elif (level=='critical') or (level==logging.CRITICAL):
                    if (display == True):
                        qLog_logger_disp.critical(txt)
                    if (outfile == True):
                        qLog_logger_file.critical(txt)
                else:
                    qLog_logger_disp.critical(txt)
                    qLog_logger_file.critical(txt)
            except:
                mode = 'nologger'

        # ログ出力（local）
        if (mode != 'logger'):
            nowTime = datetime.datetime.now()
            txt = str(procname + msg)
            if (display == True):
                s  = nowTime.strftime('%H:%M:%S') + ' ' + txt
                if   (level=='info') or (level==logging.INFO):
                    print( s )
                elif (level=='debug') or (level==logging.DEBUG):
                    print( self.colorTxt(txt=s, fgColor='cyan', fgLine='', bgColor='', ) )
                elif (level=='warning') or (level==logging.WARNING):
                    print( self.colorTxt(txt=s, fgColor='yellow', fgLine='', bgColor='', ) )
                elif (level=='error') or (level==logging.ERROR):
                    print( self.colorTxt(txt=s, fgColor='red', fgLine='', bgColor='', ) )
                elif (level=='critical') or (level==logging.CRITICAL):
                    print( self.colorTxt(txt=s, fgColor='white', fgLine='', bgColor='red', ) )
                else:
                    print( self.colorTxt(txt=s, fgColor='white', fgLine='', bgColor='red', ) )
            if (outfile == True):
                try:
                    s  = nowTime.strftime('%Y-%m-%d %H:%M:%S') + ', '
                    s += str(level) + ', '
                    s += str(txt)
                    w = codecs.open(qLog_file, 'a', 'utf-8')
                    w.write(s + '\n')
                    w.close()
                    w = None
                except:
                    pass
            
    def exception(self, e):
        global qLog_mode
        global qLog_logger_disp
        global qLog_logger_file

        try:
            mode = qLog_mode
        except:
            mode = 'logger'

        # ログ出力（logger）
        txt = str(e.args)
        if (mode == 'logger'):
            try:
                qLog_logger_disp.exception(txt)
                qLog_logger_file.exception(txt)
            except:
                mode = 'nologger'

        # ログ出力（local）
        if (mode != 'logger'):
            self.log(level='error', proc='', msg=txt, mode=mode, display=True, outfile=True, )

    def colorTxt(self, txt='', fgColor='', fgLine='', bgColor='', ):
        txtColor = ''
        if   (fgLine != ''):
            txtColor += '\033[4m'
        if   (fgColor == 'black'):
            txtColor += '\033[30m'
        elif (fgColor == 'red'):
            txtColor += '\033[31m'
        elif (fgColor == 'green'):
            txtColor += '\033[32m'
        elif (fgColor == 'yellow'):
            txtColor += '\033[33m'
        elif (fgColor == 'blue'):
            txtColor += '\033[34m'
        elif (fgColor == 'magenta'):
            txtColor += '\033[35m'
        elif (fgColor == 'cyan'):
            txtColor += '\033[36m'
        elif (fgColor == 'white'):
            txtColor += '\033[37m'
        if   (bgColor == 'black'):
            txtColor += '\033[40m'
        elif (bgColor == 'red'):
            txtColor += '\033[41m'
        elif (bgColor == 'green'):
            txtColor += '\033[42m'
        elif (bgColor == 'yellow'):
            txtColor += '\033[43m'
        elif (bgColor == 'blue'):
            txtColor += '\033[44m'
        elif (bgColor == 'magenta'):
            txtColor += '\033[45m'
        elif (bgColor == 'cyan'):
            txtColor += '\033[46m'
        elif (bgColor == 'white'):
            txtColor += '\033[47m'
        resetColor = ''
        if (txtColor != ''):
            resetColor = '\033[0m'
        return txtColor + str(txt) + resetColor



def sub():
    proc_name = 'sub'
    proc_id   = '{0:10s}'.format(proc_name).replace(' ', '_')

    qLog.log('info', proc_id, 'start')
    qLog.log('info', proc_id, 'error test ↓')
    try:
        a=100/0
    except Exception as e:
        qLog.exception(e)        
    qLog.log('info', proc_id, 'end')
    
    return True



if __name__ == '__main__':
    main_name = 'main'
    main_id   = '{0:10s}'.format(main_name).replace(' ', '_')

    qLog     = qLog_class()
    nowTime  = datetime.datetime.now()
    filename = ''
    qLog.init(mode='logger', filename=filename, )
    #qLog.init(mode='nologger', filename=filename, )

    qLog.log('info', main_id, 'run')

    qLog.log('info'    , main_id, '')
    qLog.log('debug'   , main_id, 'debug')
    qLog.log('warning' , main_id, 'warning')
    qLog.log('error'   , main_id, 'error')
    qLog.log('critical', main_id, 'critical')
    qLog.log('info'    , main_id, '')

    x = sub()


