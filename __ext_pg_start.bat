@ECHO OFF
REM ------------------------------------------------
REM COPYRIGHT (C) 2014-2024 Mitsuo KONDOU.
REM This software is released under the MIT License.
REM https://github.com/konsan1101
REM Thank you for keeping the rules.
REM ------------------------------------------------

IF EXIST "C:\snkApps\SAAP_r545\RiKi˜AŒg”ÅSAAPŽÀØ‹L˜^—p2013R544_azipÚ‘±_PGWK.accdb"  GOTO BEGIN

ECHO;@@"C:\snkApps\SAAP_r545\RiKi˜AŒg”ÅSAAPŽÀØ‹L˜^—p2013R544_azipÚ‘±_PGWK.accdb"
ECHO;@@Not Found !
GOTO ABORT

:BEGIN
CD "C:\snkApps\SAAP_r545"

rem ----------------------------------------------------------------------------------------
ECHO start /b "" "C:\snkApps\SAAP_r545\RiKi˜AŒg”ÅSAAPŽÀØ‹L˜^—p2013R544_azipÚ‘±_PGWK.accdb"
     start /b "" "C:\snkApps\SAAP_r545\RiKi˜AŒg”ÅSAAPŽÀØ‹L˜^—p2013R544_azipÚ‘±_PGWK.accdb"
rem ----------------------------------------------------------------------------------------

:ABORT
ping localhost -w 1000 -n 3 >nul
EXIT


