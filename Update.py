import os, shutil, time

MCMMPath = os.getcwd()

versionFile = open(MCMMPath + '\\Version', 'r')
updateFromVersion = versionFile.read().replace('\n', '')
versionFile.close()

versionFile = open(MCMMPath + '\\WorkDir\\Update\\Version', 'r')
updateToVersion = versionFile.read().replace('\n', '')
versionFile.close()

print('Reading options.dat and Packs.dat for demo pack install...')
settingsFile = open(MCMMPath + '\\WorkDir\\Update\\options.dat', 'r')
settings = settingsFile.readlines()
settingsFile.close()
settingsDic = {}
for i in range(len(settings)):
    settings[i] = settings[i].replace('\n', '')
    settings[i] = settings[i].split(' = ')
    settingsDic[settings[i][0]] = settings[i][1]
packsDatFile = open(settingsDic['packLocation'].replace('MC_MM_Install', MCMMPath) + '\\Packs.dat', 'a')
print('Done !')

print('Updating from ' + updateFromVersion)
print('install update at', MCMMPath)
shutil.copyfile(MCMMPath + '\\WorkDir\\Update\\MC_MM.py', MCMMPath + '\\MC_MM.py', follow_symlinks=True)
print('MC_MM.py updated')
shutil.copyfile(MCMMPath + '\\WorkDir\\Update\\Version', MCMMPath + '\\Version', follow_symlinks=True)
print('Version file updated')
shutil.copytree(MCMMPath + '\\WorkDir\\Update\\Packs\\Demo MCMM v1.0\\', settingsDic['packLocation'].replace('MC_MM_Install', MCMMPath) + '\\Demo MCMM v1.0\\')
packsDatFile.write('Demo MCMM v1.0\n')
print('Demo pack added to library')

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