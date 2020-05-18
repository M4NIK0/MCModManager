@echo off
echo ATTENTION, L'OPERATION SUPPRIMERA TOUT LE CONTENU DE LA VERSION INSTALLEE
pause
cls
:start
echo Quel pack ?
echo ------------
set "file=packs/profiles.txt"
set /A i=0
for /F "usebackq delims=" %%a in ("%file%") do (
set /A i+=1
::call echo %%i%%
call set array[%%i%%]=%%a
call set n=%%i%%
)
for /L %%i in (1,1,%n%) do call echo %%array[%%i]%%
echo ------------
set /p pack=""
set /p Ver=<packs\%pack%\version.txt
If exist packs/%pack% (
 rd "%appdata%\.minecraft\mods\%Ver%" /S /Q
 mkdir "%appdata%\.minecraft\mods\%Ver%"
 robocopy "packs\%pack%\modpack" "%appdata%\.minecraft\mods\%Ver%"
 del "%appdata%\.minecraft\options.txt"
 del "%appdata%\.minecraft\optionsof.txt"
 del "%appdata%\.minecraft\optionsshaders.txt"
 copy "packs\%pack%\options\options.txt" "%appdata%\.minecraft\"
 copy "packs\%pack%\options\optionsof.txt" "%appdata%\.minecraft\"
 copy "packs\%pack%\options\optionsshaders.txt" "%appdata%\.minecraft\"
 echo "%Ver%"
 cls
 echo Config chargee !
 pause
 exit
) Else (
 cls
 echo Cette config n'existe pas !
 pause
 cls
 goto start
)