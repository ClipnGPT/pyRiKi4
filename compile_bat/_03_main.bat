@ECHO OFF
REM ------------------------------------------------
REM COPYRIGHT (C) 2014-2024 Mitsuo KONDOU.
REM This software is released under the MIT License.
REM https://github.com/konsan1101
REM Thank you for keeping the rules.
REM ------------------------------------------------

cd ".."

ECHO; ワーク削除
IF EXIST "build"        RD "build"        /s /q
IF EXIST "dist"         RD "dist"         /s /q
IF EXIST "__pycache__"  RD "__pycache__"  /s /q
PAUSE

rem ECHO;
rem ECHO -------
rem ECHO install
rem ECHO -------
rem call bat\__install_1_pycv.bat

ECHO;
ECHO -------
ECHO compile
ECHO -------

set pyname=_v6__main__kernel
    echo;
    echo %pyname%.py
    pyinstaller %pyname%.py  -F --log-level ERROR  --icon="_icons/RiKi_start.ico"
IF EXIST "dist\%pyname%.exe"  ECHO "%pyname%.exe"
    copy "dist\%pyname%.exe"       "%pyname%.exe"
    del  "%pyname%.spec"
    copy "%pyname%.exe"        "C:\RiKi_assistant\%pyname%.exe"
    ping  localhost -w 1000 -n 1 >nul
    del  "%pyname%.exe"

ECHO;
ECHO 注意！　C:/Python3/Lib/site-packages/pyzbar/*.dll;pyzbar　利用
ECHO;

set pyname=_v6__main_vision
    echo;
    echo %pyname%.py
    pyinstaller %pyname%.py  -F --log-level ERROR  --icon="_icons/cam_start.ico" --add-binary "C:/Python3/Lib/site-packages/pyzbar/*.dll;pyzbar"
IF EXIST "dist\%pyname%.exe"  ECHO "%pyname%.exe"
    copy "dist\%pyname%.exe"       "%pyname%.exe"
    del  "%pyname%.spec"
    copy "%pyname%.exe"        "C:\RiKi_assistant\%pyname%.exe"
    copy "%pyname%.exe"        "C:\RiKi_camera\%pyname%.exe"
    ping  localhost -w 1000 -n 1 >nul
    del  "%pyname%.exe"

set pyname=_v6__main_desktop
    echo;
    echo %pyname%.py
    pyinstaller %pyname%.py  -F --log-level ERROR  --icon="_icons/rec_start.ico" --add-binary "C:/Python3/Lib/site-packages/pyzbar/*.dll;pyzbar"
IF EXIST "dist\%pyname%.exe"  ECHO "%pyname%.exe"
    copy "dist\%pyname%.exe"       "%pyname%.exe"
    del  "%pyname%.spec"
    copy "%pyname%.exe"        "C:\RiKi_assistant\%pyname%.exe"
    copy "%pyname%.exe"        "C:\RiKi_recorder\%pyname%.exe"
    ping  localhost -w 1000 -n 1 >nul
    del  "%pyname%.exe"

ECHO;
IF EXIST "build"        RD "build"        /s /q
IF EXIST "dist"         RD "dist"         /s /q
IF EXIST "__pycache__"  RD "__pycache__"  /s /q
IF EXIST "C:\RiKi_assistant\temp"         RD "C:\RiKi_assistant\temp"         /s /q
IF EXIST "C:\RiKi_assistant\_cache"       RD "C:\RiKi_assistant\_cache"       /s /q
IF EXIST "C:\RiKi_camera\temp"            RD "C:\RiKi_camera\temp"            /s /q
IF EXIST "C:\RiKi_camera\_cache"          RD "C:\RiKi_camera\_cache"          /s /q
IF EXIST "C:\RiKi_recorder\temp"          RD "C:\RiKi_recorder\temp"          /s /q
IF EXIST "C:\RiKi_recorder\_cache"        RD "C:\RiKi_recorder\_cache"        /s /q
PAUSE



