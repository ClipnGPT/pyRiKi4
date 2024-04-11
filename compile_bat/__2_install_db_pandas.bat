@ECHO OFF
REM ------------------------------------------------
REM COPYRIGHT (C) 2014-2024 Mitsuo KONDOU.
REM This software is released under the MIT License.
REM https://github.com/konsan1101
REM Thank you for keeping the rules.
REM ------------------------------------------------

REM CALL __setpath.bat

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
ECHO Waiting...10s
ping localhost -w 1000 -n 10 >nul

rem  --------
rem  PAUSE
rem  --------



ECHO;
ECHO -------
ECHO etc
ECHO -------
rem python -m pip  install --upgrade pyaudio
rem python -m pip  install --upgrade grpcio
rem python -m pip  install --upgrade grpcio-tools
rem python -m pip  install --upgrade pygame
rem python -m pip  install --upgrade matplotlib
rem python -m pip  install --upgrade pyflakes
rem python -m pip  install --upgrade pep8

    python -m pip  install --upgrade matplotlib
    python -m pip  install --upgrade seaborn
    python -m pip  install --upgrade pandas
    python -m pip  install --upgrade mojimoji

ECHO;
ECHO -------------
ECHO Excel,access
ECHO -------------
    python -m pip  install --upgrade xlrd
    python -m pip  install --upgrade xlwt
    python -m pip  install --upgrade openpyxl

ECHO;
ECHO -------------
ECHO DB
ECHO -------------
    python -m pip  install --upgrade pyodbc
    python -m pip  install --upgrade jaconv
    python -m pip  install --upgrade sqlalchemy



rem  --------
     PAUSE
rem  --------

rem ECHO;
rem ECHO ---------------------------
rem ECHO pyinstaller compile setting
rem rem  setuptools==49.6.0, 44.0.0
rem ECHO ---------------------------
rem rem  python -m pip  install --upgrade setuptools
rem rem  python -m pip  uninstall -y      setuptools
rem rem  python -m pip  install           setuptools==49.6.0
rem rem  python -m pip  install --upgrade pyinstaller
rem rem  python -m pip  uninstall -y      pyinstaller
rem rem  python -m pip  install           pyinstaller==3.6
rem rem  python -m pip  install --upgrade numpy
rem      python -m pip  uninstall -y      numpy
rem      python -m pip  install           numpy==1.19
rem rem  python -m pip  install --upgrade matplotlib==3.2.2
rem      python -m pip  uninstall -y      matplotlib
rem      python -m pip  install           matplotlib==3.2.2



ECHO;
ECHO -------------------
ECHO pip list --outdated
ECHO -------------------
    python -m pip  list --outdated

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
