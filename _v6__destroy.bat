@ECHO OFF
REM ------------------------------------------------
REM COPYRIGHT (C) 2014-2024 Mitsuo KONDOU.
REM This software is released under the MIT License.
REM https://github.com/konsan1101
REM Thank you for keeping the rules.
REM ------------------------------------------------

ECHO;
ECHO python _v6__destroy.py
     python _v6__destroy.py

ECHO;
ECHO Waiting...5s
ping localhost -w 1000 -n 5 >nul

ECHO;
ECHO taskkill /im python.exe /f
     taskkill /im python.exe /f

ECHO;
ECHO Waiting...5s
ping localhost -w 1000 -n 5 >nul

EXIT


