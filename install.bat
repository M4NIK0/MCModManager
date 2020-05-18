@echo off
set /p Name= "Quel est le nom du modpack ? "
cls
set /p Version= "Quelle est la version du modpack ? "
rmdir "%appdata%\.minecraft\mods\%Version%" -Force
mkdir "%appdata%\.minecraft\mods\%Version%"
cd
cls
:wah
@echo Quel est le nom du fichier contenant le modpack ?
set /p NameP= "(ex: Nom Mod Pack Precis) "
cls
@echo Et son extension ?
set /p Ext= "(ex: zip, rar, 7z) "
if exist "install/%NameP%.%Ext%" (
 copy "install\%NameP%.%Ext%" "%appdata%/.minecraft/mods/%Version%/Pack.%Ext%" -Force
 "C:/Program Files/7-zip/7z" e "%appdata%/.minecraft/mods/%Version%/Pack.%Ext%" -Force
 del "Pack.%Ext%"

 mkdir packs
 cls
 mkdir packs/%Name%
 cls
 mkdir "packs/%Name%/options"
 cls
 robocopy "%appdata%\.minecraft\mods\%Version%" "packs\%Name%\modpack"
 cls
 copy "%appdata%\.minecraft\options.txt" "packs\%Name%\options\options.txt"
 copy "%appdata%\.minecraft\optionsof.txt" "packs\%Name%\options\optionsof.txt"
 copy "%appdata%\.minecraft\optionsshaders.txt" "packs\%Name%\options\optionsshaders.txt"
 copy version.txt "packs\%Name%\version.txt"
 echo %Version% > "packs\%Name%\version.txt"
 echo %Name% (%version%) >> "packs\profiles.txt"
 cls
 echo Modpack mis en place !
 pause
 exit
) Else (
    echo Le fichier %Name%.%Ext% n'existe pas !
    pause
    cls
    goto wah
)