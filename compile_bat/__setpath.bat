@ECHO OFF
REM ------------------------------------------------
REM COPYRIGHT (C) 2014-2024 Mitsuo KONDOU.
REM This software is released under the MIT License.
REM https://github.com/konsan1101
REM Thank you for keeping the rules.
REM ------------------------------------------------

rem python
    SET PATH=%PATH%;C:\Python3;
rem SET PATH=%PATH%;C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python37_86;

rem sox
rem SET PATH=%PATH%;C:\Program Files\sox-14-4-0;
    SET PATH=%PATH%;C:\Program Files (x86)\sox-14-4-0;
    SET AUDIODRIVER=waveaudio

rem julius
    SET PATH=%PATH%;C:\julius\win;

rem ffmpeg
    SET PATH=%PATH%;C:\ffmpeg\win\bin;

rem vlan
rem SET PATH=%PATH%;C:\Program Files\VideoLAN\VLC;
    SET PATH=%PATH%;C:\Program Files (x86)\VideoLAN\VLC;

C:
rem CD C:\pyRiKi2
    CD C:\C:\Users\kondou\Documents\GitHub\pyRiKi2

IF NOT EXIST temp       MKDIR temp
IF NOT EXIST temp\_log  MKDIR temp\_log

