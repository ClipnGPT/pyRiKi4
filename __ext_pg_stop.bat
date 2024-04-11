@ECHO OFF
REM ------------------------------------------------
REM COPYRIGHT (C) 2014-2024 Mitsuo KONDOU.
REM This software is released under the MIT License.
REM https://github.com/konsan1101
REM Thank you for keeping the rules.
REM ------------------------------------------------

ECHO ...‚T...
ping localhost -w 1000 -n 2 >nul
ECHO ...‚S...
ping localhost -w 1000 -n 2 >nul
ECHO ...‚R...
ping localhost -w 1000 -n 2 >nul
ECHO ...‚Q...
ping localhost -w 1000 -n 2 >nul
ECHO ...‚P...
ping localhost -w 1000 -n 2 >nul

ECHO;
rem ECHO taskkill /im msaccess.exe /f >nul
rem      taskkill /im msaccess.exe /f >nul

ping localhost -w 1000 -n 3 >nul
EXIT


