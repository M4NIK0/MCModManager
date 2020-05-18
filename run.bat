@echo off
set /p PgVer=< "version.txt"
echo Minecraft Mod Manager v%PgVer%

If exist C:/Program Files/7-zip/7z.exe
    echo 7zip found successfuly
    pause
    cscript "msgs.vbs"
    exit
) Else (
    echo 7zip not found in C:/Program Files/7-zip/7z.exe !
    echo 7zip not installed/wrong directory
    echo Please install 7z !
    set /p yn= "Install ? (y/n) "
    If %yn% == y (
        start "lib/7z_lib.exe"
    )
)