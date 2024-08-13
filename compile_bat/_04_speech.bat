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

set pyname=_v6__main_speech
    echo;
    echo %pyname%.py
    pyinstaller %pyname%.py  -F --log-level ERROR  --hidden-import=tiktoken_ext.openai_public --hidden-import=tiktoken_ext --icon="_icons/speech_start.ico"
IF EXIST "dist\%pyname%.exe"  ECHO "%pyname%.exe"
    copy "dist\%pyname%.exe"       "%pyname%.exe"
    del  "%pyname%.spec"
    copy "%pyname%.exe"        "C:\RiKi_assistant\%pyname%.exe"
    copy "%pyname%.exe"        "C:\RiKi_speech\%pyname%.exe"
    copy "%pyname%.exe"        "C:\_共有\Worker\%pyname%.exe"
    ping  localhost -w 1000 -n 1 >nul
    del  "%pyname%.exe"

set pyname=_v6_speech__gijiroku1
    echo;
    echo %pyname%.py
    pyinstaller %pyname%.py  -F --log-level ERROR  --icon="_icons/speech_start.ico"
IF EXIST "dist\%pyname%.exe"  ECHO "%pyname%.exe"
    copy "dist\%pyname%.exe"       "%pyname%.exe"
    del  "%pyname%.spec"
    copy "%pyname%.exe"        "C:\RiKi_speech\%pyname%.exe"
    ping  localhost -w 1000 -n 1 >nul
    del  "%pyname%.exe"

set pyname=_v6_speech__gijiroku2
    echo;
    echo %pyname%.py
    pyinstaller %pyname%.py  -F --log-level ERROR  --icon="_icons/speech_start.ico"
IF EXIST "dist\%pyname%.exe"  ECHO "%pyname%.exe"
    copy "dist\%pyname%.exe"       "%pyname%.exe"
    del  "%pyname%.spec"
    copy "%pyname%.exe"        "C:\RiKi_speech\%pyname%.exe"
    ping  localhost -w 1000 -n 1 >nul
    del  "%pyname%.exe"

set pyname=_v6_speech__narration1
    echo;
    echo %pyname%.py
    pyinstaller %pyname%.py  -F --log-level ERROR  --icon="_icons/speech_start.ico"
IF EXIST "dist\%pyname%.exe"  ECHO "%pyname%.exe"
    copy "dist\%pyname%.exe"       "%pyname%.exe"
    del  "%pyname%.spec"
    copy "%pyname%.exe"        "C:\RiKi_speech\%pyname%.exe"
    ping  localhost -w 1000 -n 1 >nul
    del  "%pyname%.exe"

set pyname=_v6_speech__narration2
    echo;
    echo %pyname%.py
    pyinstaller %pyname%.py  -F --log-level ERROR  --icon="_icons/speech_start.ico"
IF EXIST "dist\%pyname%.exe"  ECHO "%pyname%.exe"
    copy "dist\%pyname%.exe"       "%pyname%.exe"
    del  "%pyname%.spec"
    copy "%pyname%.exe"        "C:\RiKi_speech\%pyname%.exe"
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
IF EXIST "C:\_共有\Worker\temp"           RD "C:\_共有\Worker\temp"           /s /q
IF EXIST "C:\_共有\Worker\_cache"         RD "C:\_共有\Worker\_cache"         /s /q
PAUSE



