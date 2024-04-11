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
ECHO Waiting...5s
ping localhost -w 1000 -n 5 >nul

rem  --------
     PAUSE
rem  --------



ECHO;
ECHO -------
ECHO jupyter
ECHO -------
    python -m pip  install --upgrade jupyter
rem python -m jupyter notebook --generate-config
rem c.NotebookApp.notebook_dir = 'C:/Users/kondou/notebook'
rem c.NotebookApp.open_browser = True

rem python -m jupyter notebook



ECHO;
ECHO ----------------------
ECHO bluetooth, nfc(felica)
ECHO ----------------------
    python -m pip  install --upgrade pybluez
    python -m pip  install --upgrade nfcpy



rem  --------
     PAUSE
rem  --------

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
