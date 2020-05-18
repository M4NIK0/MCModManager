@echo off
:name
cls
echo Quel pack ?
echo ___________
set "file=packs/profiles.txt"
set /A i=0
for /F "usebackq delims=" %%a in ("%file%") do (
set /A i+=1
::call echo %%i%%
call set array[%%i%%]=%%a
call set n=%%i%%
)
for /L %%i in (1,1,%n%) do call echo %%array[%%i]%%
set /p Name= ""
If exist packs/%Name% (
 cls
 mkdir packs
 cls
 mkdir packs/%Name%
 cls
 mkdir "packs/%Name%/options"
 cls
 copy "%appdata%\.minecraft\options.txt" "packs\%Name%\options\options.txt"
 copy "%appdata%\.minecraft\optionsof.txt" "packs\%Name%\options\optionsof.txt"
 copy "%appdata%\.minecraft\optionsshaders.txt" "packs\%Name%\options\optionsshaders.txt"
 cls
 set /p end= "Options mises a jour !"
 exit
)
Else
 cls
 echo Ce pack n'existe pas !
 pause
 goto name
End If