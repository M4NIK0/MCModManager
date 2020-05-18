@echo off
:name
set /p Name= "Nom du pack ? "
If exist packs/%Name% (
 set /p Version= "Version du pack ? "
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
 set /p end= "Update des mods faite !"
exit
) Else (
 cls
 echo Ce pack n'existe pas !
 pause
 cls
 goto name
)