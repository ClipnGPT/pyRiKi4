@ECHO OFF
REM ------------------------------------------------
REM COPYRIGHT (C) 2014-2024 Mitsuo KONDOU.
REM This software is released under the MIT License.
REM https://github.com/konsan1101
REM Thank you for keeping the rules.
REM ------------------------------------------------

REM CALL __setpath.bat

rem     brew install lame
rem     brew install sox
rem rem brew install libsox-fmt-all
rem     brew install ffmpeg
rem     brew install zbar
rem     brew install julius

rem rem brew install libopencv-dev
rem rem brew install python-opencv

rem rem brew cask install chromedriver
rem     brew install geckodriver

rem ECHO;
rem ECHO ----------------
rem ECHO anaconda check !
rem ECHO ----------------
rem start conda info -e
rem source activate base
rem call   activate base

rem  --------
     PAUSE
rem  --------



rem ECHO;
rem ECHO ---------
rem ECHO uninstall
rem ECHO ---------
    python -m pip freeze     > requirements.txt
    python -m pip uninstall -r requirements.txt -y

ECHO;
ECHO Waiting...5s
ping localhost -w 1000 -n 5 >nul



ECHO;
ECHO --------
ECHO pip list
ECHO --------
    python -m pip  list

rem  --------
     PAUSE
rem  --------
