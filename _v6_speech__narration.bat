@ECHO OFF
REM ------------------------------------------------
REM COPYRIGHT (C) 2014-2024 Mitsuo KONDOU.
REM This software is released under the MIT License.
REM https://github.com/konsan1101
REM Thank you for keeping the rules.
REM ------------------------------------------------

ECHO;
ECHO 入力ファイル存在確認
IF NOT EXIST "narration\1.入力ファイル_sjis.txt"  ECHO "Not Found Input File! narration\1.入力ファイル_sjis.txt"
IF NOT EXIST "narration\1.入力ファイル_sjis.txt"  GOTO BYE
ECHO OK

:API
ECHO;
ECHO API選択（入力無しはfree）
SET api=
SET /P api="f=free,g=google,w=watson,m=azure,a=aws,winos,macos,："
IF %api%@==@        SET api=free
IF %api%@==f@       SET api=free
IF %api%@==g@       SET api=google
IF %api%@==w@       SET api=watson
IF %api%@==m@       SET api=azure
IF %api%@==a@       SET api=aws
IF %api%@==free@    GOTO APIGO
IF %api%@==google@  GOTO APIGO
IF %api%@==watson@  GOTO APIGO
IF %api%@==azure@   GOTO APIGO
IF %api%@==aws@     GOTO APIGO
IF %api%@==winos@   GOTO APIGO
IF %api%@==macos@   GOTO APIGO
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
IF %api%@==winos@   SET apii=free
IF %api%@==winos@   SET apit=free
IF %api%@==winos@   SET apio=winos
IF %api%@==macos@   SET apii=free
IF %api%@==macos@   SET apit=free
IF %api%@==macos@   SET apio=macos

IF NOT EXIST "temp"           MKDIR "temp"
IF NOT EXIST "temp\_log"      MKDIR "temp\_log"
IF NOT EXIST "temp\_cache"    MKDIR "temp\_cache"
IF NOT EXIST "narration"      MKDIR "narration"
IF NOT EXIST "narration\tts"  MKDIR "narration\tts"
IF NOT EXIST "narration\mp3"  MKDIR "narration\mp3"
IF NOT EXIST "narration\wav"  MKDIR "narration\wav"

ECHO;
ECHO ファイル整理

IF EXIST "narration\tts\*.*"  DEL "narration\tts\*.*" /Q
IF EXIST "narration\mp3\*.*"  DEL "narration\mp3\*.*" /Q
IF EXIST "narration\wav\*.*"  DEL "narration\wav\*.*" /Q

ECHO;
ECHO 処理データ準備

ECHO;
ECHO --------------------------------
ECHO python _v6_speech__narration1.py
     python _v6_speech__narration1.py
ECHO --------------------------------

ECHO;
ECHO 処理はクラウドで一気に行います。
ECHO 処理を実行するまえにテキストは ☆ 必ず ☆ 確かめてください。（narration/ttsフォルダ）
PAUSE

ECHO;
ECHO テキストは確認しましたね？
ECHO 処理はクラウドで一気に行います。（ファイル数＊０．５円）
PAUSE

ECHO;
ECHO -----------------------------
ECHO python _v6__destroy.py faster
     python _v6__destroy.py faster
ECHO -----------------------------

IF EXIST "temp\*.*"                DEL "temp\*.*"                /Q
IF EXIST "temp\s5_0control\*.*"    DEL "temp\s5_0control\*.*"    /Q
IF EXIST "temp\s5_1voice\*.*"      DEL "temp\s5_1voice\*.*"      /Q
IF EXIST "temp\s5_2wav\*.*"        DEL "temp\s5_2wav\*.*"        /Q
IF EXIST "temp\s5_3stt_julius\*.*" DEL "temp\s5_3stt_julius\*.*" /Q
IF EXIST "temp\s5_4stt_txt\*.*"    DEL "temp\s5_4stt_txt\*.*"    /Q
IF EXIST "temp\s5_5tts_txt\*.*"    DEL "temp\s5_5tts_txt\*.*"    /Q
IF EXIST "temp\s5_6tra_txt\*.*"    DEL "temp\s5_6tra_txt\*.*"    /Q
IF EXIST "temp\s5_7play\*.*"       DEL "temp\s5_7play\*.*"       /Q
IF EXIST "temp\_recorder\*.*"      DEL "temp\_recorder\*.*"      /Q
IF EXIST "temp\_work\*.*"          DEL "temp\_work\*.*"          /Q

IF NOT EXIST "temp\s5_5tts_txt"  MKDIR "temp\s5_5tts_txt"
ECHO XCOPY narration\tts\*.* temp\s5_5tts_txt /Q/R/Y
     XCOPY narration\tts\*.* temp\s5_5tts_txt /Q/R/Y

ECHO;
ECHO ----------------------------------------------------------------------InpTrn___TxtOut
ECHO 日本語出力
rem  python _v6__main_speech.py speech file usb off 0 %apii% %apit% %apio% ja ja,en ja ja
rem  python _v6__main_speech.py speech file usb off 0 %apii% %apit% %apio% ja ja,en ja ja
ECHO python _v6__main_speech.py speech file usb off 0 %apii% %apit% %apio% ja ja ja ja
     python _v6__main_speech.py speech file usb off 0 %apii% %apit% %apio% ja ja ja ja
rem  英語出力
rem  python _v6__main_speech.py speech file usb off 0 %apii% %apit% %apio% ja en,ja ja en
rem  キャッシュ学習
rem  python _v6__main_speech.py speech file usb off 0 %apii% %apit% %apio% ja en,fr,es,id,zh,ko,ja ja en
ECHO ----------------------------------------------------------------------InpTrn___TxtOut

IF EXIST "narration\mp3\*.*"      DEL "narration\mp3\*.*" /Q
ECHO XCOPY "temp\_recorder\*.mp3" "narration\mp3" /Q/R/Y
     XCOPY "temp\_recorder\*.mp3" "narration\mp3" /Q/R/Y

ECHO;
ECHO --------------------------------
ECHO python _v6_speech__narration2.py
     python _v6_speech__narration2.py
ECHO --------------------------------

ECHO;
ECHO %api% の処理は終了。
ECHO 作業ファイルクリアします。
PAUSE

IF EXIST "temp\*.*"                DEL "temp\*.*"                /Q
IF EXIST "temp\s5_0control\*.*"    DEL "temp\s5_0control\*.*"    /Q
IF EXIST "temp\s5_1voice\*.*"      DEL "temp\s5_1voice\*.*"      /Q
IF EXIST "temp\s5_2wav\*.*"        DEL "temp\s5_2wav\*.*"        /Q
IF EXIST "temp\s5_3stt_julius\*.*" DEL "temp\s5_3stt_julius\*.*" /Q
IF EXIST "temp\s5_4stt_txt\*.*"    DEL "temp\s5_4stt_txt\*.*"    /Q
IF EXIST "temp\s5_5tts_txt\*.*"    DEL "temp\s5_5tts_txt\*.*"    /Q
IF EXIST "temp\s5_6tra_txt\*.*"    DEL "temp\s5_6tra_txt\*.*"    /Q
IF EXIST "temp\s5_7play\*.*"       DEL "temp\s5_7play\*.*"       /Q
IF EXIST "temp\_recorder\*.*"      DEL "temp\_recorder\*.*"      /Q
IF EXIST "temp\_work\*.*"          DEL "temp\_work\*.*"          /Q

RD "narration\tts"  /s /q

:BYE
PAUSE
