import os, shutil, time

MCMMPath = os.getcwd()

versionFile = open(MCMMPath + '\\Version', 'r')
updateFromVersion = versionFile.read().replace('\n', '')
versionFile.close()

versionFile = open(MCMMPath + '\\WorkDir\\Update\\Version', 'r')
updateToVersion = versionFile.read().replace('\n', '')
versionFile.close()

print('Updating from ' + updateFromVersion)
print('install update at', MCMMPath)
shutil.copyfile(MCMMPath + '\\WorkDir\\Update\\MC_MM.py', MCMMPath + '\\MC_MM.py', follow_symlinks=True)
print('MC_MM.py updated')
shutil.copyfile(MCMMPath + '\\WorkDir\\Update\\Version', MCMMPath + '\\Version', follow_symlinks=True)
print('Version file updated')

oldOptionsFile = open(MCMMPath + '\\options.dat', 'r')
oldOptions = oldOptionsFile.readlines()
oldOptionsFile.close()
for i in range(len(oldOptions)):
    oldOptions[i] = oldOptions[i].replace('\n', '')
    if i == 3:
        oldOptions[i] = 'checkForUpdates = True'
oldOptions.append('username = user')
toWrite = ''
for i in oldOptions:
    toWrite += i + '\n'
newOptionsFile = open(MCMMPath + '\\options.dat', 'w')
newOptionsFile.write(toWrite)
newOptionsFile.close()
print('Added new option')

packsLocation = ''
for i in oldOptions:
    if 'packLocation = ' in i:
        packsLocation = i.replace('packLocation = ', '').replace('MC_MM_Install', MCMMPath)
shutil.copytree(MCMMPath + '\\WorkDir\\Update\\Packs\\Demo MCMM v0.9.5\\', packsLocation + '\\Demo MCMM v0.9.5')
packsDatFile = open(packsLocation + '\\Packs.dat', 'a')
packsDatFile.write('Demo MCMM v0.9.5\n')
packsDatFile.close()
print("Added new example config")

firstRunFile = open(MCMMPath + '\\firstRun', 'w')
firstRunFile.write('Install success !')
firstRunFile.close()
shutil.copyfile(MCMMPath + '\\WorkDir\\Update\\Changelog.txt', MCMMPath + '\\Changelog.txt', follow_symlinks=True)
print('Added firstRun and Changelog.txt')

shutil.copyfile(MCMMPath + '\\WorkDir\\Update\\lang\\en-us.lang', MCMMPath + '\\lang\\en-us.lang', follow_symlinks=True)
print('en-us lang file updated\nDeleting update files...')
shutil.rmtree(MCMMPath + '\\WorkDir\\Update')
if os.path.exists(MCMMPath + '\\WorkDir\\Update.zip'):
    os.remove(MCMMPath + '\\WorkDir\\Update.zip')
print('Update finished !\nStarting MCMM...')

os.system('Run.bat')