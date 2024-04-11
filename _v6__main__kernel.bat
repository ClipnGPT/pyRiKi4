@ECHO OFF

REM ------------------------------------------------
REM COPYRIGHT (C) 2014-2024 Mitsuo KONDOU.
REM This software is released under the MIT License.
REM https://github.com/konsan1101
REM Thank you for keeping the rules.
REM ------------------------------------------------

:API
ECHO;
ECHO API選択（入力無しはfree）
SET api=
SET /P api="f=free,g=google,w=watson,m=azure,a=aws,s=special,："
IF %api%@==@        SET api=free
IF %api%@==f@       SET api=free
IF %api%@==g@       SET api=google
IF %api%@==w@       SET api=watson
IF %api%@==m@       SET api=azure
IF %api%@==a@       SET api=aws
IF %api%@==s@       SET api=special
IF %api%@==free@    GOTO APIGO
IF %api%@==google@  GOTO APIGO
IF %api%@==watson@  GOTO APIGO
IF %api%@==azure@   GOTO APIGO
IF %api%@==aws@     GOTO APIGO
IF %api%@==special@ GOTO APIGO
GOTO API
:APIGO
ECHO %api%
                    SET apii=free
                    SET apit=free
                    SET apio=winos
IF %api%@==free@    SET apii=free
IF %api%@==free@    SET apit=free
IF %api%@==free@    SET apio=winos
IF %api%@==google@  SET apii=google
IF %api%@==google@  SET apit=google
IF %api%@==google@  SET apio=google
IF %api%@==watson@  SET apii=watson
IF %api%@==watson@  SET apit=watson
IF %api%@==watson@  SET apio=watson
IF %api%@==azure@   SET apii=azure
IF %api%@==azure@   SET apit=azure
IF %api%@==azure@   SET apio=azure
IF %api%@==aws@     SET apii=aws
IF %api%@==aws@     SET apit=aws
IF %api%@==aws@     SET apio=aws
IF %api%@==special@ SET apii=google
IF %api%@==special@ SET apit=azure
IF %api%@==special@ SET apio=watson

:MODE
ECHO;
ECHO MODE選択（入力無しはhud）
SET mode=
SET dev=bluetooth
SET guide=on
SET /P mode="1=hud,2=live,3=translator,4=speech,5=number,6=chat,7=chatbot,8=camera,9=assistant,10=reception,："
IF %mode%@==@            SET  mode=hud
IF %mode%@==1@           SET  mode=hud
IF %mode%@==2@           SET  mode=live
IF %mode%@==3@           SET  mode=translator
IF %mode%@==4@           SET  mode=speech
IF %mode%@==5@           SET  mode=number
IF %mode%@==6@           SET  mode=chat
IF %mode%@==7@           SET  mode=chatbot
IF %mode%@==8@           SET  mode=camera
IF %mode%@==9@           SET  mode=assistant
IF %mode%@==10@           SET  mode=reception
IF %mode%@==hud@         SET  dev=bluetooth
IF %mode%@==hud@         SET  guide=off
IF %mode%@==hud@         GOTO MODEGO
IF %mode%@==live@        SET  dev=bluetooth
IF %mode%@==live@        SET  guide=off
IF %mode%@==live@        GOTO MODEGO
IF %mode%@==translator@  SET  dev=bluetooth
IF %mode%@==translator@  SET  guide=on
IF %mode%@==translator@  GOTO MODEGO
IF %mode%@==speech@      SET  dev=usb
IF %mode%@==speech@      SET  guide=on
IF %mode%@==speech@      GOTO MODEGO
IF %mode%@==number@      SET  dev=usb
IF %mode%@==number@      SET  guide=on
IF %mode%@==number@      GOTO MODEGO
IF %mode%@==chat@        SET  dev=bluetooth
IF %mode%@==chat@        SET  guide=off
IF %mode%@==chat@        GOTO MODEGO
IF %mode%@==chatbot@     SET  dev=bluetooth
IF %mode%@==chatbot@     SET  guide=on
IF %mode%@==chatbot@     GOTO MODEGO
IF %mode%@==camera@      SET  dev=usb
IF %mode%@==camera@      SET  guide=off
IF %mode%@==camera@      GOTO MODEGO
IF %mode%@==assistant@   SET  dev=usb
IF %mode%@==assistant@   SET  guide=off
IF %mode%@==assistant@   GOTO MODEGO
IF %mode%@==reception@   SET  dev=usb
IF %mode%@==reception@   SET  guide=off
IF %mode%@==reception@   GOTO MODEGO
GOTO MODE
:MODEGO
ECHO %mode%
ECHO %dev%
ECHO guide %guide%

ECHO;
ECHO python _v6__destroy.py faster
     python _v6__destroy.py faster

ECHO;
rem      --------------------------------------------------------------------------------------------InpTrnTxtOutCam1..
rem ECHO start "RiKi" /min python _v6__main__kernel.py %mode% 0 %dev% %guide% 0 %apii% %apit% %apio% ja en ja en "http://repair-fujitsu:5555/MotionJpeg?w=640&h=480"
rem      start "RiKi" /min python _v6__main__kernel.py %mode% 0 %dev% %guide% 0 %apii% %apit% %apio% ja en ja en "http://repair-fujitsu:5555/MotionJpeg?w=640&h=480"
rem ECHO start "RiKi" /min python _v6__main__kernel.py %mode% 0 %dev% %guide% 0 %apii% %apit% %apio% ja en ja en "http://192.168.86.73:5555/MotionJpeg?w=640&h=480"
rem      start "RiKi" /min python _v6__main__kernel.py %mode% 0 %dev% %guide% 0 %apii% %apit% %apio% ja en ja en "http://192.168.86.73:5555/MotionJpeg?w=640&h=480"
    ECHO start "RiKi" /min python _v6__main__kernel.py %mode% 0 %dev% %guide% 0 %apii% %apit% %apio% ja en ja en
         start "RiKi" /min python _v6__main__kernel.py %mode% 0 %dev% %guide% 0 %apii% %apit% %apio% ja en ja en
rem      --------------------------------------------------------------------------------------------InpTrnTxtOutCam1..

IF %mode%@==reception@   GOTO RECEPTION
GOTO RECEPTIONPASS
:RECEPTION
    ECHO;Waiting 180s...
    ping localhost -w 1000 -n 180 >nul
    IF EXIST "temp\_work\busy_dev_display.txt"  DEL "temp\_work\busy_dev_display.txt"
:RECEPTIONPASS

rem ECHO;
rem ECHO python _v6__destroy.py faster
rem      python _v6__destroy.py faster

ECHO;
ECHO bye!
ping localhost -w 1000 -n 5 >nul

EXIT



