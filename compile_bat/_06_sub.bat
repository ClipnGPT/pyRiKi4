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
ECHO etc 1/2
ECHO -------
    python -m pip  install --upgrade screeninfo
    python -m pip  install --upgrade pyautogui
    python -m pip  install --upgrade pywin32
    python -m pip  install --upgrade psutil
    python -m pip  install --upgrade rainbow-logging-handler
    python -m pip  install --upgrade pycryptodome

    python -m pip  install --upgrade numpy
rem python -m pip  install --upgrade opencv-python
rem python -m pip  install --upgrade opencv-contrib-python
    python -m pip  install --upgrade opencv-python==4.9.0.80
    python -m pip  install --upgrade opencv-contrib-python==4.9.0.80

    python -m pip  install --upgrade pysimplegui==4.60.5
    python -m pip  install --upgrade pillow

ECHO;
ECHO -------
ECHO compile 1/2
ECHO -------

set pyname=_v6__sub_bgm
    echo;
    echo %pyname%.py
    pyinstaller %pyname%.py  -F --log-level ERROR  --icon="_icons/bgm.ico"
IF EXIST "dist\%pyname%.exe"  ECHO "%pyname%.exe"
    copy "dist\%pyname%.exe"       "%pyname%.exe"
    del  "%pyname%.spec"
    copy "%pyname%.exe"        "C:\RiKi_assistant\%pyname%.exe"
    ping  localhost -w 1000 -n 1 >nul
    del  "%pyname%.exe"

set pyname=_v6__sub_player
    echo;
    echo %pyname%.py
    pyinstaller %pyname%.py  -F --log-level ERROR  --icon="_icons/RiKi_showMeVideo.ico"
IF EXIST "dist\%pyname%.exe"  ECHO "%pyname%.exe"
    copy "dist\%pyname%.exe"       "%pyname%.exe"
    del  "%pyname%.spec"
    copy "%pyname%.exe"        "C:\RiKi_assistant\%pyname%.exe"
    ping  localhost -w 1000 -n 1 >nul
    del  "%pyname%.exe"

set pyname=_v6_proc_capture
    echo;
    echo %pyname%.py
    pyinstaller %pyname%.py  -F --log-level ERROR  --icon="_icons/capture.ico"
IF EXIST "dist\%pyname%.exe"  ECHO "%pyname%.exe"
    copy "dist\%pyname%.exe"       "%pyname%.exe"
    del  "%pyname%.spec"
    copy "%pyname%.exe"        "C:\RiKi_assistant\%pyname%.exe"
    copy "%pyname%.exe"        "C:\_共有\RPA\%pyname%.exe"
    ping  localhost -w 1000 -n 1 >nul
    del  "%pyname%.exe"

ECHO;
IF EXIST "build"        RD "build"        /s /q
IF EXIST "dist"         RD "dist"         /s /q
IF EXIST "__pycache__"  RD "__pycache__"  /s /q

rem  --------
rem  PAUSE
rem  --------

ECHO;
ECHO -------
ECHO etc 2/2
ECHO -------
    python -m pip  install --upgrade selenium
    python -m pip  install --upgrade bs4

ECHO;
ECHO -------
ECHO compile 2/2
ECHO -------

set pyname=_v6__sub_browser
    echo;
    echo %pyname%.py
    pyinstaller %pyname%.py  -F --log-level ERROR  --icon="_icons/browser.ico"
IF EXIST "dist\%pyname%.exe"  ECHO "%pyname%.exe"
    copy "dist\%pyname%.exe"       "%pyname%.exe"
    del  "%pyname%.spec"
    copy "%pyname%.exe"        "C:\RiKi_assistant\%pyname%.exe"
    copy "%pyname%.exe"        "C:\_共有\RPA\%pyname%.exe"
    ping  localhost -w 1000 -n 1 >nul
    del  "%pyname%.exe"

ECHO;
IF EXIST "build"        RD "build"        /s /q
IF EXIST "dist"         RD "dist"         /s /q
IF EXIST "__pycache__"  RD "__pycache__"  /s /q
IF EXIST "C:\RiKi_assistant\temp"         RD "C:\RiKi_assistant\temp"         /s /q
IF EXIST "C:\RiKi_assistant\_cache"       RD "C:\RiKi_assistant\_cache"       /s /q
IF EXIST "C:\_共有\RPA\temp"              RD "C:\_共有\RPA\temp"           /s /q
IF EXIST "C:\_共有\RPA\_cache"            RD "C:\_共有\RPA\_cache"         /s /q
PAUSE



