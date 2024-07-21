@ECHO OFF
REM ------------------------------------------------
REM COPYRIGHT (C) 2014-2024 Mitsuo KONDOU.
REM This software is released under the MIT License.
REM https://github.com/konsan1101
REM Thank you for keeping the rules.
REM ------------------------------------------------

cd ".."

ECHO;
IF EXIST "build"        RD "build"        /s /q
IF EXIST "dist"         RD "dist"         /s /q
IF EXIST "__pycache__"  RD "__pycache__"  /s /q
PAUSE



ECHO;
ECHO -----
ECHO tools
ECHO -----
rem           pip  install --upgrade pip
    python -m pip  install --upgrade pip
    python -m pip  install --upgrade wheel
    python -m pip  install --upgrade setuptools
    python -m pip  install --upgrade pyinstaller

ECHO;
ECHO -------
ECHO etc
ECHO -------
    python -m pip  install --upgrade screeninfo
    python -m pip  install --upgrade pyautogui
    python -m pip  install --upgrade pywin32
    python -m pip  install --upgrade comtypes==1.4.4
    python -m pip  install --upgrade psutil
    python -m pip  install --upgrade rainbow-logging-handler
    python -m pip  install --upgrade pycryptodome



ECHO;
ECHO -------
ECHO compile
ECHO -------

set pyname=_v6__destroy
    echo;
    echo %pyname%.py
    pyinstaller %pyname%.py  -F --log-level ERROR --icon="_icons/RiKi_stop.ico"
IF EXIST "dist\%pyname%.exe"  ECHO "%pyname%.exe"
    copy "dist\%pyname%.exe"       "%pyname%.exe"
    del  "%pyname%.spec"
    copy "%pyname%.exe"        "C:\RiKi_assistant\%pyname%.exe"
    copy "%pyname%.exe"        "C:\RiKi_speech\%pyname%.exe"
    copy "%pyname%.exe"        "C:\RiKi_camera\%pyname%.exe"
    copy "%pyname%.exe"        "C:\RiKi_recorder\%pyname%.exe"
    ping  localhost -w 1000 -n 1 >nul
    del  "%pyname%.exe"



ECHO;
IF EXIST "build"        RD "build"        /s /q
IF EXIST "dist"         RD "dist"         /s /q
IF EXIST "__pycache__"  RD "__pycache__"  /s /q
IF EXIST "C:\RiKi_assistant\temp"         RD "C:\RiKi_assistant\temp"         /s /q
IF EXIST "C:\RiKi_assistant\_cache"       RD "C:\RiKi_assistant\_cache"       /s /q
IF EXIST "C:\RiKi_speech\temp"            RD "C:\RiKi_speech\temp"            /s /q
IF EXIST "C:\RiKi_speech\_cache"          RD "C:\RiKi_speech\_cache"          /s /q
IF EXIST "C:\RiKi_camera\temp"            RD "C:\RiKi_camera\temp"            /s /q
IF EXIST "C:\RiKi_camera\_cache"          RD "C:\RiKi_camera\_cache"          /s /q
IF EXIST "C:\RiKi_recorder\temp"          RD "C:\RiKi_recorder\temp"          /s /q
IF EXIST "C:\RiKi_recorder\_cache"        RD "C:\RiKi_recorder\_cache"        /s /q
IF EXIST "C:\_共有\Player\temp"           RD "C:\_共有\Player\temp"           /s /q
IF EXIST "C:\_共有\Player\_cache"         RD "C:\_共有\Player\_cache"         /s /q
IF EXIST "C:\_共有\Worker\temp"           RD "C:\_共有\Worker\temp"           /s /q
IF EXIST "C:\_共有\Worker\_cache"         RD "C:\_共有\Worker\_cache"         /s /q
PAUSE



