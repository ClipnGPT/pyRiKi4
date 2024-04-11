@ECHO OFF
REM ------------------------------------------------
REM COPYRIGHT (C) 2014-2024 Mitsuo KONDOU.
REM This software is released under the MIT License.
REM https://github.com/konsan1101
REM Thank you for keeping the rules.
REM ------------------------------------------------

cd "C:\Users\kondou\Documents\GitHub\pyRiKi2"

IF NOT EXIST temp            MKDIR temp
IF NOT EXIST temp\s5_1voice  MKDIR temp\s5_1voice

start adintool -in adinnet -out file -filename temp/s5_1voice/julius -startid 5001

start adintool-gui -in mic -rewind 555 -headmargin 333 -tailmargin 444 -lv 777

rem   adintool     -in mic -rewind 555 -headmargin 333 -tailmargin 444 -lv 777 -out file -filename temp/s5_1voice/julius -startid 1
start adintool     -in mic -rewind 555 -headmargin 333 -tailmargin 444 -lv 777 -out adinnet -server localhost -port 5530

rem   PAUSE
exit
