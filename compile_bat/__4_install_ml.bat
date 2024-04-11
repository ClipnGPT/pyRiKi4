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
ECHO etc
ECHO -------

ECHO;
ECHO -------------
ECHO deep learning
ECHO -------------
    python -m pip  install --upgrade gym
    python -m pip  install --upgrade atari-py
    python -m pip  install --upgrade scikit-image
    python -m pip  install --upgrade scikit-learn

rem ECHO;
rem ECHO -----------
rem ECHO yolo3 keras
rem ECHO -----------
rem    python -m pip  install --upgrade tensorflow
rem    python -m pip  install --upgrade keras

rem ECHO;
rem ECHO -------------
rem ECHO yolo3 pytorch
rem ECHO -------------
rem python -m pip  install --upgrade torch==1.2.0+cpu torchvision==0.4.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
rem python -m pip  install --upgrade torchvision

ECHO;
ECHO ----------------------
ECHO azureml,version update
ECHO ----------------------
    python -m pip  uninstall -y  numpy
    python -m pip  uninstall -y  pandas
    python -m pip  uninstall -y  matplotlib
    python -m pip  uninstall -y  scipy
    python -m pip  uninstall -y  scikit-learn
    python -m pip  install       numpy==1.16.2
    python -m pip  install       pandas==0.23.4
    python -m pip  install       matplotlib==3.0.3
    python -m pip  install       scipy==1.1.0
    python -m pip  install       scikit-learn==0.20.3

ECHO;
ECHO ---------------
ECHO azureml
ECHO ---------------
    python -m pip  install --upgrade azureml-sdk
    python -m pip  install --upgrade azureml-dataprep
    python -m pip  install --upgrade azureml-train-automl
    python -m pip  install --upgrade azureml.widgets
    python -m pip  install --ignore-installed azureml-train-automl-client



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
