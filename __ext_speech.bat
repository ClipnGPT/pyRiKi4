@ECHO OFF
REM ------------------------------------------------
REM COPYRIGHT (C) 2014-2024 Mitsuo KONDOU.
REM This software is released under the MIT License.
REM https://github.com/konsan1101
REM Thank you for keeping the rules.
REM ------------------------------------------------

IF EXIST "C:\Python3"   GOTO PY
IF EXIST "C:\Python4"   GOTO PY

:DOS
ECHO;@%1@%2@%3
GOTO ABORT

:PY
start /b python __ext_speech.py %1 %2 %3

:ABORT
rem ping localhost -w 1000 -n 3 >nul
EXIT
