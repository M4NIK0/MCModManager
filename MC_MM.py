import sys, random, os, shutil, time, requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QLabel, QHBoxLayout, QVBoxLayout, QSlider, QGridLayout, QToolBar, QPushButton, QAction, QCheckBox, QStatusBar, QWidget, QFileDialog, QToolBar, QMessageBox, QLineEdit, QComboBox, QScrollArea
from PyQt5.QtCore import Qt, QCoreApplication, QRect, QSize
from PyQt5.QtGui import QIcon, QKeySequence
from PIL import Image, ImageQt

class packFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.waitFrame = QFrame()
        self.name = 'Default_Name'
        self.loader = 'Default_Loader'
        self.mods = ['Default', 'Mods', 'List']
        self.version = 'Default_version'
        self.text = ['Load', 'Delete', 'Display mods', 'Loader', 'Installed Mods', 'Yes', 'No', 'Are you sure you want to delete the pack']
        self.setStyleSheet('border: 1px solid black')
        self.packsPath = ''
        self.backupPath = ''
        self.MCMMPath = ''
        self.settingsData = {}
        self.langData = {}

    def createContent(self):
        print('onCreateContent ' + self.name)
        mainLayout = QHBoxLayout()
        col1 = QVBoxLayout()
        col2 = QVBoxLayout()
        col3 = QVBoxLayout()
        nameLabel = QLabel()
        versionLabel = QLabel()
        loaderLabel = QLabel()
        modsListButton = QPushButton()
        loadButton = QPushButton()
        deleteButton = QPushButton()

        nameLabel.setText(self.name)
        versionLabel.setText(self.version)
        loaderLabel.setText(self.text[3] + ': ' + self.loader)
        modsListButton.setText(self.text[2])
        loadButton.setText(self.text[0])
        deleteButton.setText(self.text[1])

        loadButton.clicked.connect(self.onLoad)
        deleteButton.clicked.connect(self.onDelete)
        modsListButton.clicked.connect(self.onModsList)

        col1.addWidget(nameLabel)
        col1.addWidget(versionLabel)
        col2.addWidget(loaderLabel)
        col2.addWidget(modsListButton)
        col3.addWidget(loadButton)
        col3.addWidget(deleteButton)

        col1Frame = QFrame()
        col2Frame = QFrame()
        col3Frame = QFrame()

        col1Frame.setLayout(col1)
        col2Frame.setLayout(col2)
        col3Frame.setLayout(col3)

        mainLayout.addWidget(col1Frame)
        mainLayout.addWidget(col2Frame)
        mainLayout.addWidget(col3Frame)

        col1Frame.setStyleSheet('border-width: 0;')
        col2Frame.setStyleSheet('border-width: 0;')
        col3Frame.setStyleSheet('border-width: 0;')

        loadButton.setStyleSheet('border-width: 2;')
        deleteButton.setStyleSheet('border-width: 2;')
        modsListButton.setStyleSheet('border-width: 2;')

        self.setLayout(mainLayout)
        self.setMaximumHeight(100)

    def onDelete(self):
        print('onDelete ' + self.name)

        def onYes():
            print('Deleting pack ' + self.name)
            print(self.packsPath)
            self.waitFrame.show()
            shutil.rmtree(self.packsPath.replace('MC_MM_Install', self.MCMMPath) + '\\' + self.name)
            self.waitFrame.close()
            print('Pack files removed')
            
            packsDat = open(self.packsPath.replace('MC_MM_Install', self.MCMMPath) + '\\Packs.dat', 'r')
            packsData = packsDat.readlines()
            packsDat.close()

            packsDataWrite = ''
            for i in range(len(packsData)):
                if not self.name in packsData[i]:
                    packsDataWrite += packsData[i]

            packsDat = open(self.packsPath.replace('MC_MM_Install', self.MCMMPath) + '\\Packs.dat', 'w')
            packsDat.write(packsDataWrite)
            packsDat.close()

            print('Pack deleted from configs')
            
            for i in range(len(self.children())):
                self.children()[i].deleteLater()
            self.resize(0, 0)

            self.deletePopup.close()


        def onNo():
            print('Canceled deletion of pack ' + self.name)
            self.deletePopup.close()

        self.deletePopup = QFrame()
        deletePopupLayoutButtons = QHBoxLayout()
        buttonYes = QPushButton()
        buttonNo = QPushButton()

        buttonYes.setText(self.text[5])
        buttonNo.setText(self.text[6])

        buttonYes.clicked.connect(onYes)
        buttonNo.clicked.connect(onNo)

        deletePopupLayoutButtons.addWidget(buttonYes)
        deletePopupLayoutButtons.addWidget(buttonNo)

        self.deletePopup.setLayout(deletePopupLayoutButtons)

        self.deletePopup.setWindowModality(Qt.ApplicationModal)
        self.deletePopup.setWindowTitle(self.langData['packDeleteWindowTitle'])
        self.deletePopup.setMaximumHeight(50)
        self.deletePopup.setMaximumWidth(400)
        self.deletePopup.setMinimumHeight(50)
        self.deletePopup.setMinimumWidth(400)
        self.deletePopup.show()

    def onLoad(self):
        def onDonePopupClose():
            print('onDonePopupClose')
            self.donePopup.close()

        print('onLoad ' + self.name)
        if self.name == 'RickAstley' or self.name == 'Yolo':
                os.system("start \"\" https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        print('Warning, loading still don\'t backup for now !\nMaybe in the next update ?')
        if os.path.exists(os.getenv('APPDATA') + '\\.minecraft\\mods'):
            print('Transfering mods...')
            shutil.rmtree(os.getenv('APPDATA') + '\\.minecraft\\mods')
            shutil.copytree(self.settingsData['packLocation'].replace('MC_MM_Install', self.MCMMPath) + '\\' + self.name + '\\mods', os.getenv('APPDATA') + '\\.minecraft\\mods', dirs_exist_ok=True)
            print('Done.\nTransfering Options...')
        else: print('No mods folder found !\Playing in vanilla ?')
        if os.path.exists(self.settingsData['packLocation'].replace('MC_MM_Install', self.MCMMPath) + '\\' + self.name + '\\options'):
            shutil.copytree(self.settingsData['packLocation'].replace('MC_MM_Install', self.MCMMPath) + '\\' + self.name + '\\options', os.getenv('APPDATA') + '\\.minecraft', dirs_exist_ok=True)
            print('Done.\nTransfering config...')
        else: print('No options folder found !')
        if os.path.exists(os.getenv('APPDATA') + '\\.minecraft\\config'):
            shutil.rmtree(os.getenv('APPDATA') + '\\.minecraft\\config')
            shutil.copytree(self.settingsData['packLocation'].replace('MC_MM_Install', self.MCMMPath) + '\\' + self.name + '\\config', os.getenv('APPDATA') + '\\.minecraft\\config', dirs_exist_ok=True)
        else: print('No config folder found !\nPlaying in vanilla ?')
        print('Done.')

        self.donePopup = QFrame()
        self.donePopup.setMaximumHeight(100)
        self.donePopup.setMaximumWidth(220)
        self.donePopup.setMinimumHeight(100)
        self.donePopup.setMinimumWidth(220)
        doneLabel = QLabel()
        doneLabel.setText(self.langData['packLoadDone'])
        self.donePopupLayout = QVBoxLayout()
        self.donePopupLayout.addWidget(doneLabel)
        okayButton = QPushButton()
        okayButton.setText(self.langData['okayButton'])

        okayButton.clicked.connect(onDonePopupClose)

        self.donePopupLayout.addWidget(okayButton)
        self.donePopup.setLayout(self.donePopupLayout)
        self.donePopup.setWindowModality(Qt.ApplicationModal)
        self.donePopup.show()


    def onModsList(self):
        print('onModsList ' + self.name)
        self.scrollModsArea = QScrollArea()
        self.modListFrame = QFrame()
        self.modListFrame.setMaximumWidth(250)
        self.modListFrame.setMinimumWidth(250)
        self.scrollModsArea.setMaximumWidth(255)
        self.scrollModsArea.setMinimumWidth(255)
        self.scrollModsArea.resize(255, 700)
        modListFrameLayout = QVBoxLayout()
        for i in range(len(self.mods)):
            testLabel = QLabel()
            testLabel.setText(self.mods[i])
            modListFrameLayout.addWidget(testLabel)
        self.modListFrame.setLayout(modListFrameLayout)
        self.scrollModsArea.setWidget(self.modListFrame)
        self.scrollModsArea.setWindowTitle(self.text[4])
        self.scrollModsArea.setWindowModality(Qt.ApplicationModal)
        self.scrollModsArea.show()

class packList(QFrame):
    def __init__(self):
        super().__init__()
        self.waitFrame = QFrame()
        self.langData = {}
        self.settingsData = {}
        self.MCMMPath = ''
        self.layout = QVBoxLayout()

    def onExplore(self):
        dataRead = open(self.settingsData['packLocation'].replace('MC_MM_Install', self.MCMMPath) + '\\Packs.dat', 'r')
        packList = dataRead.readlines()
        dataRead.close()
        print('Loading packs...')
        for i in range(len(packList)):
            packList[i] = packList[i].replace('\n', '')
            if os.path.exists(self.settingsData['packLocation'].replace('MC_MM_Install', self.MCMMPath) + '\\' + packList[i] + '\\Info.dat'):
                packDataFile = open(self.settingsData['packLocation'].replace('MC_MM_Install', self.MCMMPath) + '\\' + packList[i] + '\\Info.dat', 'r')
                packRawData = packDataFile.readlines()
                packDataFile.close()
                dicData = {}
                for j in range(len(packRawData)):
                    packRawData[j] = packRawData[j].replace('\n', '').split('|')
                    dicData[packRawData[j][0]] = packRawData[j][1]
                packFramed = packFrame()
                packFramed.waitFrame = self.waitFrame
                packFramed.langData = self.langData
                packFramed.name = packList[i]
                packFramed.loader = dicData['Loader']
                packFramed.mods = dicData['ModsList'].split(',')
                packFramed.version = dicData['MCVersion']
                packFramed.text = [self.langData['packLoadButton'], self.langData['packDeleteButton'], self.langData['packDisplayModsButton'], self.langData['packLoader'], self.langData['packInstalledMods'], self.langData['yes'], self.langData['no'], self.langData['packSureDelete']]
                packFramed.packsPath = self.settingsData['packLocation']
                packFramed.backupPath = self.settingsData['backupLocation']
                packFramed.MCMMPath = self.MCMMPath
                packFramed.settingsData = self.settingsData
                packFramed.createContent()
                self.layout.addWidget(packFramed)

            else:
                print('Pack ' + packList[i] + ' \Info.dat not found !')


        self.setLayout(self.layout)

class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.packScrolling = QScrollArea()
        self.langData = {}
        self.settingsData = {}
        self.saved = True
        self.langList = []
        self.selectedLanguage = ''
        self.settingsToApply = []
        self.MCMMPath = ''
        self.version = ''


    def continueLoad(self):
        if os.path.exists(self.MCMMPath + '\\Update.py'):
            os.remove(self.MCMMPath + '\\Update.py')
            print('Removed Update.py (it\'s not an update running !)')

        self.waitFrame = QFrame() #Frame in case MCMM is busy a long time
        waitFrameLayout = QHBoxLayout()
        waitFrameText = QLabel()
            
        waitFrameText.setText(self.langData['MC_MM_Busy'])
        waitFrameLayout.addWidget(waitFrameText)
        self.waitFrame.setLayout(waitFrameLayout)
        self.waitFrame.setFixedHeight(10)
        self.waitFrame.setFixedWidth(350)

        self.waitFrame.setWindowTitle(self.langData['MC_MM_BusyWindowTitle'])

        self.waitFrame.setWindowModality(Qt.ApplicationModal)

        self.settingsPopup = QMainWindow() #Creating settings window
        self.settingsPopup.setWindowTitle(self.langData['settingsWindow'])

        self.setWindowTitle(self.langData['mainWindow'])
        self.resize(1024, 600)
        self.layout = QHBoxLayout()
        self.menu = self.menuBar()
        self.fileMenu = self.menu.addMenu('&' + self.langData['file'])
        self.softwareMenu = self.menu.addMenu('&' + self.langData['MC_MM'])

        self.exitAction = QAction(self.langData['exit'])

        self.saveAction = QAction(self.langData['save']) #File menu actions
        self.importAction = QAction(self.langData['import'])
        self.exportAction = QAction(self.langData['export'])

        self.settingsAction = QAction(self.langData['settings']) #MC Mod Manager menu actions
        self.infoAction = QAction(self.langData['info'])

        self.exitAction.triggered.connect(self.onExit)

        self.saveAction.triggered.connect(self.onSave) #File menu actions
        self.importAction.triggered.connect(self.onImport)
        self.exportAction.triggered.connect(self.onExport)

        self.importAction.setShortcut(QKeySequence('Ctrl+I'))
        self.exportAction.setShortcut(QKeySequence('Ctrl+E'))
        self.exitAction.setShortcut(QKeySequence('Ctrl+Q'))

        self.settingsAction.triggered.connect(self.onSettings) #MC Mod Manager menu actions
        self.infoAction.triggered.connect(self.onInfo)

        self.fileMenu.addAction(self.saveAction)#File menu actions
        self.fileMenu.addAction(self.importAction)
        self.fileMenu.addAction(self.exportAction)

        self.softwareMenu.addAction(self.settingsAction) #MC Mod Manager menu actions
        self.softwareMenu.addAction(self.infoAction)

        self.exitButton = self.menu.addAction(self.exitAction)

        self.packsFrame = packList()
        self.packsFrame.waitFrame, self.packsFrame.settingsData, self.packsFrame.langData, self.packsFrame.MCMMPath = self.waitFrame, self.settingsData, self.langData, self.MCMMPath
        self.packsFrame.onExplore()

        self.packsFrame.setMinimumWidth(700)
        self.packsFrame.width = self.width
        self.packScrolling.setWidget(self.packsFrame)
        self.setCentralWidget(self.packScrolling)

        self.onUpdate()
        

        if os.path.exists(self.MCMMPath + '\\firstRun'):
            def onFirstRunPopupClose():
                print('onFirstPopupClose')
                os.remove(self.MCMMPath + '\\firstRun')
                self.firstRunPopup.close()
            self.firstRunPopup = QFrame()
            self.firstRunPopupLayout = QVBoxLayout()
            self.firstRunPopup.setWindowTitle(self.langData['firstRunWindowTitle'])

            okayButton = QPushButton()
            okayButton.setText(self.langData['okayButton'])
            okayButton.clicked.connect(onFirstRunPopupClose)

            firstRunTitleLabel = QLabel()
            firstRunTitleLabel.setText(self.langData['firstRunTextP1'] + os.environ.get("USERNAME") + self.langData['firstRunTextP2'] + self.version + self.langData['firstRunTextP3'] + '\n' + self.langData['firstRunText'])
            firstRunTitleLabel.setAlignment(Qt.AlignCenter)

            firstRunTextLabel = QLabel()
            firstRunTextLabel.setText(self.langData['firstRunText2'] + '\n' + self.langData['firstRunText3'] + '\n' + self.langData['firstRunText4'])
            firstRunTextLabel.setAlignment(Qt.AlignCenter)

            self.firstRunPopupLayout.addWidget(firstRunTitleLabel)
            self.firstRunPopupLayout.addWidget(firstRunTextLabel)
            self.firstRunPopupLayout.addWidget(okayButton)
            self.firstRunPopup.setLayout(self.firstRunPopupLayout)
            self.firstRunPopup.setWindowModality(Qt.ApplicationModal)
            self.firstRunPopup.setFixedWidth(450)
            self.firstRunPopup.setFixedHeight(150)
            self.firstRunPopup.show()

    def onInfo(self):
        print('onInfo')
        self.infoPopup = QFrame()
        self.infoPopup.setMinimumWidth(600)
        self.infoPopup.setMinimumHeight(450)
        self.infoPopup.setMaximumWidth(600)
        self.infoPopup.setFixedHeight(450)
        self.infoPopupLayout = QVBoxLayout()
        infoTitle = QLabel()
        self.infoPopup.setWindowTitle(self.langData['infoWindowTitle'])
        infoTitle.setText(self.langData['infoTitle'])
        self.infoPopupLayout.addWidget(infoTitle)
        infoData = self.langData['infoParagraph'].split('[')
        infoScrollFrame = QFrame()
        infoScrollFrameLayout = QVBoxLayout()
        infoScroll = QScrollArea()

        for i in infoData:
            if not i == 'https://github.com/M4NIK0/MCModManager/':
                infoLine = QLabel()
                infoLine.setText(i)
            else:
                def openGithub():
                    os.system("start \"\" https://github.com/M4NIK0/MCModManager/")
                infoLine = QPushButton()
                infoLine.setText(self.langData['infoGithubLink'])
                infoLine.clicked.connect(openGithub)

            infoScrollFrameLayout.addWidget(infoLine)
        infoScrollFrame.setLayout(infoScrollFrameLayout)
        infoScroll.setWidget(infoScrollFrame)

        self.infoPopupLayout.addWidget(infoScroll)

        changelogTitle = QLabel()
        changelogTitle.setText(self.langData['infoChangelogTitle'])
        self.infoPopupLayout.addWidget(changelogTitle)

        changelogScrollFrame = QFrame()
        changelogScrollFrameLayout = QVBoxLayout()
        changelogScroll = QScrollArea()

        changelogFile = open(self.MCMMPath + '\\Changelog.txt', 'r')
        changelogData = changelogFile.readlines()
        changelogFile.close()
        for i in range(len(changelogData)):
            changelogData[i] = changelogData[i].replace('\n', '')

        for i in changelogData:
            if not i == 'https://github.com/M4NIK0/MCModManager/': # [Couane, i know you read this, send this code: 16754
                infoLine = QLabel()
                infoLine.setText(i)
            else:
                def openGithub():
                    os.system("start \"\" https://github.com/M4NIK0/MCModManager/")
                infoLine = QPushButton()
                infoLine.setText(self.langData['infoGithubLink'])
                infoLine.clicked.connect(openGithub)

            changelogScrollFrameLayout.addWidget(infoLine)
        changelogScrollFrame.setLayout(changelogScrollFrameLayout)
        changelogScroll.setWidget(changelogScrollFrame)

        self.infoPopupLayout.addWidget(changelogScroll)

        self.infoPopup.setLayout(self.infoPopupLayout)
        self.infoPopup.setWindowModality(Qt.ApplicationModal)
        self.infoPopup.show()

    def onSave(self):
        def onSaveApply():
            packName = self.nameText.text()
            packVersion = self.versionText.text()
            packLoader = self.loaderText.text()
            modsList = self.modsText.text()
            optionsGet = self.optionsCheckBox.checkState()
            optionsofGet = self.optionsofCheckBox.checkState()
            optionsshadersGet = self.optionsshadersCheckBox.checkState()
            optionsMore = self.optionsText.text()
            packsDatFile = open(self.settingsData['packLocation'].replace('MC_MM_Install', self.MCMMPath) + '\\Packs.dat', 'r')
            packsFile = packsDatFile.read()
            packsDatFile.close()

            if optionsGet == 0:
                optionsGet = False
            else:
                optionsGet = True

            if optionsshadersGet == 0:
                optionsshadersGet = False
            else:
                optionsshadersGet = True

            if optionsofGet == 0:
                optionsofGet = False
            else:
                optionsofGet = True

            if packName == '' or packName in packsFile:
                print('Cannot save pack without or with a duplicated name !')
            else:
                print('Saving pack as ' + packName)
                if packVersion == '':
                    packVersion = self.langData['packSaveUnknownversion']
                if modsList == '':
                    modsList = self.langData['packSaveUnknownMods']
                if packLoader == '':
                    packLoader = self.langData['packUnknownLoader']

                infoWrite = 'OptionsList|'
                if optionsGet:
                    infoWrite += 'options,'
                if optionsofGet:
                    infoWrite += 'optionsof,'
                if optionsshadersGet:
                    infoWrite += 'optionsshaders,'
                infoWrite += optionsMore + '\nModsList|' + modsList + '\nLoader|' + packLoader + '\nMCVersion|' + packVersion + '\nCreationDate|' + str(time.strftime('%d %b %Y %H:%M:%S'))
    
                os.mkdir(self.settingsData['packLocation'].replace('MC_MM_Install', self.MCMMPath) + '\\' + packName)
                
                infoFile = open(self.settingsData['packLocation'].replace('MC_MM_Install', self.MCMMPath) + '\\' + packName + '\\Info.dat', 'w')
                infoFile.write(infoWrite)
                infoFile.close()
    
                packsDatFile = open(self.settingsData['packLocation'].replace('MC_MM_Install', self.MCMMPath) + '\\Packs.dat', 'w')
                packsDatFile.write(packsFile + packName + '\n')
                packsDatFile.close()

                print('Transfering mods...')

                if os.path.exists(os.getenv('APPDATA') + '\\.minecraft\\mods'):
                    shutil.copytree(os.getenv('APPDATA') + '\\.minecraft\\mods', self.settingsData['packLocation'].replace('MC_MM_Install', self.MCMMPath) + '\\' + packName + '\\mods')

                print('Done.\nTransfering selected options...')

                if optionsGet or optionsofGet or optionsshadersGet:
                    os.mkdir(self.settingsData['packLocation'].replace('MC_MM_Install', self.MCMMPath) + '\\' + packName + '\\options')

                if optionsGet and os.path.exists(os.getenv('APPDATA') + '\\.minecraft\\options.txt'):
                    shutil.copy(os.getenv('APPDATA') + '\\.minecraft\\options.txt', self.settingsData['packLocation'].replace('MC_MM_Install', self.MCMMPath) + '\\' + packName + '\\options\\')
                
                if optionsofGet and os.path.exists(os.getenv('APPDATA') + '\\.minecraft\\optionsof.txt'):
                    shutil.copy(os.getenv('APPDATA') + '\\.minecraft\\optionsof.txt', self.settingsData['packLocation'].replace('MC_MM_Install', self.MCMMPath) + '\\' + packName + '\\options\\')
                
                if optionsshadersGet and os.path.exists(os.getenv('APPDATA') + '\\.minecraft\\optionsshaders.txt'):
                    shutil.copy(os.getenv('APPDATA') + '\\.minecraft\\optionsshaders.txt', self.settingsData['packLocation'].replace('MC_MM_Install', self.MCMMPath) + '\\' + packName + '\\options\\')

                print('Done.\nTransfering config...')

                if os.path.exists(os.getenv('APPDATA') + '\\.minecraft\\config'):
                    shutil.copytree(os.getenv('APPDATA') + '\\.minecraft\\config', self.settingsData['packLocation'].replace('MC_MM_Install', self.MCMMPath) + '\\' + packName + '\\config')

                self.savePopup.close()
                self.packsFrame = packList()
                self.waitFrame, self.packsFrame.settingsData, self.packsFrame.langData, self.packsFrame.MCMMPath = self.waitFrame, self.settingsData, self.langData, self.MCMMPath
                self.packsFrame.onExplore()
                self.packsFrame.setMinimumWidth(700)
                self.packScrolling.setWidget(self.packsFrame)

        print('onSave')
        self.savePopup = QFrame()
        self.savePopup.setWindowTitle(self.langData['packSaveWindowName'])

        self.optionsFrame = QFrame()
        self.optionsFrameLayout = QHBoxLayout()

        self.optionsofCheckBox = QCheckBox()
        self.optionsCheckBox = QCheckBox()
        self.optionsshadersCheckBox = QCheckBox()

        self.optionsofLabel = QLabel()
        self.optionsLabel = QLabel()
        self.optionsshadersLabel = QLabel()

        self.optionsofLabel.setText('optionsof')
        self.optionsLabel.setText('options')
        self.optionsshadersLabel.setText('optionsshaders')

        self.optionsFrameLayout.addWidget(self.optionsLabel)
        self.optionsFrameLayout.addWidget(self.optionsCheckBox)
        self.optionsFrameLayout.addWidget(self.optionsofLabel)
        self.optionsFrameLayout.addWidget(self.optionsofCheckBox)
        self.optionsFrameLayout.addWidget(self.optionsshadersLabel)
        self.optionsFrameLayout.addWidget(self.optionsshadersCheckBox)

        self.optionsFrame.setLayout(self.optionsFrameLayout)

        self.nameText = QLineEdit()
        self.versionText = QLineEdit()
        self.loaderText = QLineEdit()
        self.optionsText = QLineEdit()
        self.modsText = QLineEdit()
        self.hintTextsLabel = QLabel()
        self.hintTextsLabel.setText(self.langData['packSaveOptionsIndication'])

        self.optionsEditFrame = QFrame()

        self.optionsEditLayout = QVBoxLayout()

        self.optionsEditLayout.addWidget(self.nameText)
        self.optionsEditLayout.addWidget(self.versionText)
        self.optionsEditLayout.addWidget(self.loaderText)
        self.optionsEditLayout.addWidget(self.modsText)
        self.optionsEditLayout.addWidget(self.optionsFrame)
        self.optionsEditLayout.addWidget(self.optionsText)
        self.optionsEditLayout.addWidget(self.hintTextsLabel)

        self.optionsEditFrame.setLayout(self.optionsEditLayout)

        self.labelsFrame = QFrame()

        self.labelsLayout = QVBoxLayout()
        
        self.nameLabel = QLabel()
        self.versionLabel = QLabel()
        self.loaderLabel = QLabel()
        self.modsLabel = QLabel()
        self.optionsLabel = QLabel()
        self.emptyLabel = QLabel()
        self.saveButton = QPushButton()

        self.nameLabel.setText(self.langData['packSaveName'])
        self.versionLabel.setText(self.langData['packSaveVersion'])
        self.loaderLabel.setText(self.langData['packSaveLoader'])
        self.modsLabel.setText(self.langData['packSaveMods'])
        self.optionsLabel.setText(self.langData['packSaveOptions'])
        self.saveButton.setText(self.langData['packSaveSaveButton'])

        self.saveButton.clicked.connect(onSaveApply)

        self.labelsLayout.addWidget(self.nameLabel)
        self.labelsLayout.addWidget(self.versionLabel)
        self.labelsLayout.addWidget(self.loaderLabel)
        self.labelsLayout.addWidget(self.modsLabel)
        self.labelsLayout.addWidget(self.optionsLabel)
        self.labelsLayout.addWidget(self.emptyLabel)
        self.labelsLayout.addWidget(self.saveButton)

        self.labelsFrame.setLayout(self.labelsLayout)

        self.savePopupLayout = QHBoxLayout()

        self.savePopupLayout.addWidget(self.labelsFrame)
        self.savePopupLayout.addWidget(self.optionsEditFrame)

        self.savePopup.setLayout(self.savePopupLayout)

        self.savePopup.setMinimumSize(400,220)
        self.savePopup.setMaximumSize(400,220)

        self.savePopup.setWindowModality(Qt.ApplicationModal)
        self.savePopup.show()
        

        

    def onSettings(self):
        print('onSettings')
        settingsPopupMainFrame = QFrame()
        self.settingsPopup.resize(500, 260)
        self.settingsPopup.setMaximumSize(500, 260)
        self.settingsPopup.setMinimumSize(500, 260)

        self.settingsPopup.layout = QVBoxLayout()

        frameBackupsLocation = QFrame() #Backup and Packs Location part
        framePacksLocation = QFrame()

        frameBackupsLocation.layout = QHBoxLayout()
        framePacksLocation.layout = QHBoxLayout()

        self.locationPacksTextZone = QLineEdit()
        self.locationBackupsTextZone = QLineEdit()

        self.locationBackupsTextZone.setText(self.settingsData['backupLocation'])
        self.locationPacksTextZone.setText(self.settingsData['packLocation'])

        locationPacksLabel = QLabel()
        locationBackupsLabel = QLabel()

        locationPacksLabel.setText(self.langData['locationOptionPacks'])
        locationBackupsLabel.setText(self.langData['locationOptionBackups'])

        locationPacksLoadButton = QPushButton()
        locationBackupsLoadButton = QPushButton()

        locationPacksLoadButton.setText(self.langData['browseText'])
        locationBackupsLoadButton.setText(self.langData['browseText'])

        locationPacksLoadButton.clicked.connect(self.onSearchPacks)
        locationBackupsLoadButton.clicked.connect(self.onSearchBackups)

        framePacksLocation.layout.addWidget(locationPacksLabel)
        framePacksLocation.layout.addWidget(self.locationPacksTextZone) 
        framePacksLocation.layout.addWidget(locationPacksLoadButton)

        frameBackupsLocation.layout.addWidget(locationBackupsLabel)
        frameBackupsLocation.layout.addWidget(self.locationBackupsTextZone)
        frameBackupsLocation.layout.addWidget(locationBackupsLoadButton)

        framePacksLocation.setLayout(framePacksLocation.layout)
        frameBackupsLocation.setLayout(frameBackupsLocation.layout)

        self.settingsPopup.layout.addWidget(framePacksLocation)
        self.settingsPopup.layout.addWidget(frameBackupsLocation)

        pathHelpText = QLabel() #Adding a small help text to reset place for packs
        pathHelpText.setText(self.langData['pathHelpOptions'])
        self.settingsPopup.layout.addWidget(pathHelpText)


        #Part for language
        frameLanguage = QFrame()
        labelLanguage = QLabel()
        self.dropdownLanguage = QComboBox()

        for i in self.langList:
            self.dropdownLanguage.addItem(i)
        dicLanguagesIndex = {}
        for i in range(len(langList)):
            dicLanguagesIndex[langList[i]] = i

        self.dropdownLanguage.setCurrentIndex(dicLanguagesIndex[self.selectedLanguage])

        frameLanguage.layout = QHBoxLayout()

        labelLanguage.setText(self.langData['languages'])
        print(self.settingsData)

        frameLanguage.layout.addWidget(labelLanguage)
        frameLanguage.layout.addWidget(self.dropdownLanguage)

        frameLanguage.setLayout(frameLanguage.layout)

        self.settingsPopup.layout.addWidget(frameLanguage)

        updateFrame = QFrame()
        updateFrameLayout = QHBoxLayout()

        updateStartupLabel = QLabel()
        updateStartupLabel.setText(self.langData['updateAutoSettings'])
        self.updateCheckBox = QCheckBox()
        if self.settingsData['checkForUpdates'] == 'True':
            self.updateCheckBox.setChecked(True)
        updateCheckButton = QPushButton()
        updateCheckButton.setText(self.langData['updateCheckSettings'])

        updateFrameLayout.addWidget(updateStartupLabel)
        updateFrameLayout.addWidget(self.updateCheckBox)
        updateFrameLayout.addWidget(updateCheckButton)

        updateCheckButton.clicked.connect(self.onUpdateFromSettings)

        updateFrame.setLayout(updateFrameLayout)

        self.settingsPopup.layout.addWidget(updateFrame)
        
        cancelButton = QPushButton()
        applyButton = QPushButton()

        cancelButton.clicked.connect(self.onCancelSettings)
        applyButton.clicked.connect(self.onApplySettings)

        cancelButton.setText(self.langData['cancelButton'])
        applyButton.setText(self.langData['applyButton'])

        mainButtonsFrame = QFrame()
        mainButtonsFrame.layout = QHBoxLayout()

        mainButtonsFrame.layout.addWidget(cancelButton)
        mainButtonsFrame.layout.addWidget(applyButton)

        mainButtonsFrame.setLayout(mainButtonsFrame.layout)
        
        self.settingsPopup.layout.addWidget(mainButtonsFrame)

        settingsPopupMainFrame.setLayout(self.settingsPopup.layout) #Define all layout to settings window
        self.settingsPopup.setCentralWidget(settingsPopupMainFrame)

        self.settingsPopup.setWindowModality(Qt.ApplicationModal)

        self.settingsPopup.show()
    
    
    def onCancelSettings(self):
        print('onCancelSettings')
        self.settingsPopup.close()

    def onApplySettings(self):
        print('onApplySettings')
        print(self.locationBackupsTextZone.text())
        print(self.locationPacksTextZone.text())
        print(self.langList[self.dropdownLanguage.currentIndex()])
        optionsList = [self.langList[self.dropdownLanguage.currentIndex()], self.locationPacksTextZone.text(), self.locationBackupsTextZone.text(), self.updateCheckBox.checkState()]
        if optionsList[1] == '':
            optionsList[1] = 'MC_MM_Install\\Packs'
        if optionsList[2] == '':
            optionsList[2] = 'MC_MM_Install\\Backups'
        if not os.path.exists(optionsList[1].replace('MC_MM_Install', self.MCMMPath)):
            print(optionsList[1] + ' does not exists !\nAborting apply for this path...')
            optionsList[1] = self.settingsData['packLocation']
        if not os.path.exists(optionsList[2].replace('MC_MM_Install', self.MCMMPath)):
            print(optionsList[2] + ' does not exists !\nAborting apply for this path...')
            optionsList[2] = self.settingsData['backupLocation']
        
        if optionsList[1] == optionsList[2]:
            print('Packs and Backups cannot be at the same location !')
            print('Aborting modification of paths...')
            optionsList[1] = self.settingsData['packLocation']
            optionsList[2] = self.settingsData['backupLocation']

        optionsList[3] = str(optionsList[3])
        if optionsList[3] == '2':
            optionsList[3] = 'True'
        elif optionsList[3] == '0':
            optionsList[3] = 'False'

        optionsToWrite = ''
        optionsValsList = ['lang = ', 'packLocation = ', 'backupLocation = ', 'checkForUpdates = ']
        for i in range(len(optionsList)):
            optionsToWrite += optionsValsList[i] + optionsList[i] + "\n"
        optionsToWrite += 'username = user'
        print(optionsToWrite)
        optionsFile = open(self.MCMMPath + '\\options.dat', 'w')
        optionsFile.write(optionsToWrite)
        optionsFile.close()
        self.settingsData['lang'] = optionsList[0]
        self.settingsData['packLocation'] = optionsList[1]
        self.settingsData['backupLocation'] = optionsList[2]
        self.settingsData['checkForUpdates'] = optionsList[3]
        print('Saved settings')
        self.settingsPopup.close()

    def onLanguageChange(self):
        print('onLanguageChange')

    def onBackupsPathChange(self):
        print('onBackupsLanguageChnges')

    def onPacksPathChange(self):
        print('onPacksPathChange')

    def onSearchPacks(self):
        print('onSearchPacks')
        dir = QFileDialog.getExistingDirectory(None, self.langData['pathFolder'], 'C:\\', QFileDialog.ShowDirsOnly).replace('/', '\\')
        if not dir == '':
            print(dir, 'selected for packs folder')
            self.locationPacksTextZone.setText(dir)

    def onSearchBackups(self):
        print('onSearchBackups')
        dir = QFileDialog.getExistingDirectory(None, self.langData['pathFolder'], 'C:\\', QFileDialog.ShowDirsOnly).replace('/', '\\')
        if not dir == '':
            print(dir, 'selected for backups folder')
            self.locationBackupsTextZone.setText(dir)

    def onImport(self):
        def importApply():
            packToImport = self.importLocationText.text()
            packsDatFile = open(self.settingsData['packLocation'].replace('MC_MM_Install', self.MCMMPath) + '\\Packs.dat', 'r')
            packsFile = packsDatFile.read()
            packsDatFile.close()
            if self.importNameText.text() == '' or not os.path.exists(packToImport):
                print('Cannot import a pack without a name !')
            elif self.importNameText.text() in packsFile:
                print('Cannot import a pack with a duplicated name !')
            else:
                print('Verifying archive at ' + packToImport + "(Copying and unpacking in WorkDir)")

                self.waitFrame.show()

                shutil.copyfile(packToImport, self.MCMMPath + '\\WorkDir\\Pack.zip')
                shutil.unpack_archive(self.MCMMPath + '\\WorkDir\\Pack.zip', self.MCMMPath + '\\WorkDir\\Pack')

                self.waitFrame.close()
                print("Archive copied and unpacked !")
                print('Looking for Info.dat...')
                if os.path.exists(self.MCMMPath + '\\WorkDir\\Pack\\Info.dat'):
                    print('File found !\nMoving files in' + self.settingsData['packLocation'].replace('MC_MM_Install', self.MCMMPath))
                    self.waitFrame.show()
                    shutil.move(self.MCMMPath + "\\WorkDir\\Pack", self.settingsData['packLocation'].replace('MC_MM_Install', self.MCMMPath) + '\\' + self.importNameText.text())
                    os.remove(self.MCMMPath + '\\WorkDir\\Pack.zip')
                    self.waitFrame.close()
                    print('Files moved !\nAdding pack in configs...')

                    packsDatFile = open(self.settingsData['packLocation'].replace('MC_MM_Install', self.MCMMPath) + '\\Packs.dat', 'w')
                    packsDatFile.write(packsFile + self.importNameText.text() + '\n')
                    packsDatFile.close()

                    self.packsFrame = packList()
                    self.waitFrame, self.packsFrame.settingsData, self.packsFrame.langData, self.packsFrame.MCMMPath = self.waitFrame, self.settingsData, self.langData, self.MCMMPath
                    self.packsFrame.onExplore()

                    self.packsFrame.setMinimumWidth(700)
                    self.packScrolling.setWidget(self.packsFrame)
                    self.importWindow.close()
                else:
                    print('File not found !\nCannot import a pack without any information !')


        def importCancel():
            print('Import cancelled')
            self.importWindow.close()

        def browseFile():
            print('Browsing file...')
            file = QFileDialog.getOpenFileName(self,'Single File', self.settingsData['packLocation'].replace('MC_MM_Install', self.MCMMPath),'*.mcmp')
            file = file[0]
            if file == "":
                print('Nothing selected !')
            else:
                print('File selected: ' + file)
                self.importLocationText.setText(file)

        print('onImport')
        self.importWindow = QFrame()
        self.importWindow.layout = QVBoxLayout()

        locationFrame = QFrame()
        locationFrameLayout = QHBoxLayout()
        locationFrameLabel = QLabel()
        locationBrowseButton = QPushButton()
        self.importLocationText = QLineEdit()

        nameFrame = QFrame()
        nameFrameLayout = QHBoxLayout()
        nameFrameLabel = QLabel()
        self.importNameText = QLineEdit()

        buttonsFrame = QFrame()
        buttonsFrameLayout = QHBoxLayout()
        cancelButton = QPushButton()
        loadButton = QPushButton()

        locationBrowseButton.clicked.connect(browseFile)
        loadButton.clicked.connect(importApply)
        cancelButton.clicked.connect(importCancel)

        locationFrameLabel.setText(self.langData['importLocationLabel'])
        locationBrowseButton.setText(self.langData['browseText'])

        nameFrameLabel.setText(self.langData['importNameLabel'])

        cancelButton.setText(self.langData['cancelButton'])
        loadButton.setText(self.langData['importLoadButton'])

        locationFrameLayout.addWidget(locationFrameLabel)
        locationFrameLayout.addWidget(self.importLocationText)
        locationFrameLayout.addWidget(locationBrowseButton)
        locationFrame.setLayout(locationFrameLayout)

        nameFrameLayout.addWidget(nameFrameLabel)
        nameFrameLayout.addWidget(self.importNameText)
        nameFrame.setLayout(nameFrameLayout)

        buttonsFrameLayout.addWidget(cancelButton)
        buttonsFrameLayout.addWidget(loadButton)
        buttonsFrame.setLayout(buttonsFrameLayout)

        self.importWindow.layout.addWidget(locationFrame)
        self.importWindow.layout.addWidget(nameFrame)
        self.importWindow.layout.addWidget(buttonsFrame)
        self.importWindow.setLayout(self.importWindow.layout)

        self.importWindow.setWindowTitle(self.langData['importWindowTitle'])
        self.importWindow.setWindowModality(Qt.ApplicationModal)
        self.importWindow.setFixedWidth(700)
        self.importWindow.setFixedHeight(150)
        self.importWindow.show()

    def onExport(self):
        print('onExport')

    def onLaunchMC(self):
        print('onLaunchMC')

    def onUpdate(self):
        print('onUpdate')
        def onSkipUpdate():
            print('onSkipUpdate')
            updateSkippedFile = open(self.MCMMPath + '\\skipUpdate', 'w')
            updateSkippedFile.write(self.responceVersion)
            updateSkippedFile.close()
            self.updateWindow.close()
    
        def onCancelUpdate():
            print('Update canceled !')
            self.updateWindow.close()

        def onDownloadUpdate():
            print('onDownloadUpdate')
            print('Downloading update...')
            updateData = requests.get('https://github.com/M4NIK0/MCModManager/releases/download/' + self.responceVersion + '/MCMM.' + self.responceVersion + '.zip')
            updateFile = open(self.MCMMPath + '\\WorkDir\\Update.zip', "wb").write(updateData.content)
            print('Downloaded successfuly !\nDecompressing update file...')
            if not os.path.exists(self.MCMMPath + '\\WorkDir\\Update'):
                os.mkdir(self.MCMMPath + '\\WorkDir\\Update')
            shutil.unpack_archive(self.MCMMPath + '\\WorkDir\\Update.zip', self.MCMMPath + '\\WorkDir\\Update')
            print('Decompression successful !')
            print('Running update scipt...')
            self.settingsPopup.close()
            self.close()
            self.updateWindow.close()
            os.system('python ' + self.MCMMPath + '\\WorkDir\\Update\\Update.py')

        response = requests.get("https://api.github.com/repos/M4NIK0/MCModManager/releases/latest")
        self.responceVersion = response.json()["name"]
        if self.responceVersion != 'v' + self.version:
            print('Update found !')
            updateSkip = False
            if not os.path.exists(self.MCMMPath + '\\skipUpdate'):
                updateSkip = False
            else:
                updateSkippedFile = open(self.MCMMPath + '\\skipUpdate', 'r')
                updateSkipped = updateSkippedFile.read().replace('\n', '')
                updateSkippedFile.close()
                if self.responceVersion == updateSkipped:
                    updateSkip = True
                    print('Update skipped !')
            if (not updateSkip) and ('True' in self.settingsData['checkForUpdates']):
                self.updateWindow = QFrame()
                updateLabel = QLabel()
                updateWindowLayout = QVBoxLayout()
                updateButtonsLayout = QHBoxLayout()
                updateButtonsFrame = QFrame()
                downloadButton = QPushButton()
                cancelButton = QPushButton()
                skipButton = QPushButton()
                updateLabel.setText(self.langData['updateTitle'])
                downloadButton.setText(self.langData['updateDownload'])
                cancelButton.setText(self.langData['updateCancel'])
                skipButton.setText(self.langData['updateSkip'])

                downloadButton.clicked.connect(onDownloadUpdate)
                cancelButton.clicked.connect(onCancelUpdate)
                skipButton.clicked.connect(onSkipUpdate)

                updateButtonsLayout.addWidget(downloadButton)
                updateButtonsLayout.addWidget(skipButton)
                updateButtonsLayout.addWidget(cancelButton)

                updateButtonsFrame.setLayout(updateButtonsLayout)

                updateWindowLayout.addWidget(updateLabel)
                updateWindowLayout.addWidget(updateButtonsFrame)

                self.updateWindow.setLayout(updateWindowLayout)

                self.updateWindow.setWindowTitle(self.langData['updateWindowTitle'])

                self.updateWindow.setWindowModality(Qt.ApplicationModal)

                self.updateWindow.show()

    def onUpdateFromSettings(self):
        print('onUpdate')
        def onSkipUpdate():
            print('onSkipUpdate')
            updateSkippedFile = open(self.MCMMPath + '\\skipUpdate', 'w')
            updateSkippedFile.write(self.responceVersion)
            updateSkippedFile.close()
            self.updateWindow.close()
    
        def onCancelUpdate():
            print('Update canceled !')
            self.updateWindow.close()

        def onDownloadUpdate():
            print('onDownloadUpdate')
            print('Downloading update...')
            updateData = requests.get('https://github.com/M4NIK0/MCModManager/releases/download/' + self.responceVersion + '/MCMM.' + self.responceVersion + '.zip')
            updateFile = open(self.MCMMPath + '\\WorkDir\\Update.zip', "wb").write(updateData.content)
            print('Downloaded successfuly !\nDecompressing update file...')
            if not os.path.exists(self.MCMMPath + '\\WorkDir\\Update'):
                os.mkdir(self.MCMMPath + '\\WorkDir\\Update')
            shutil.unpack_archive(self.MCMMPath + '\\WorkDir\\Update.zip', self.MCMMPath + '\\WorkDir\\Update')
            print('Decompression successful !')
            print('Running update scipt...')
            self.settingsPopup.close()
            self.close()
            self.updateWindow.close()
            os.system('python ' + self.MCMMPath + '\\WorkDir\\Update\\Update.py')

        response = requests.get("https://api.github.com/repos/M4NIK0/MCModManager/releases/latest")
        self.responceVersion = response.json()["name"]
        if self.responceVersion != 'v' + self.version:
            print('Update found !')
            updateSkip = False
            if not os.path.exists(self.MCMMPath + '\\skipUpdate'):
                updateSkip = False
            else:
                updateSkippedFile = open(self.MCMMPath + '\\skipUpdate', 'r')
                updateSkipped = updateSkippedFile.read().replace('\n', '')
                updateSkippedFile.close()
                if self.responceVersion == updateSkipped:
                    updateSkip = True
                    print('Update skipped !')
            if True:
                self.updateWindow = QFrame()
                updateLabel = QLabel()
                updateWindowLayout = QVBoxLayout()
                updateButtonsLayout = QHBoxLayout()
                updateButtonsFrame = QFrame()
                downloadButton = QPushButton()
                cancelButton = QPushButton()
                skipButton = QPushButton()
                updateLabel.setText(self.langData['updateTitle'])
                downloadButton.setText(self.langData['updateDownload'])
                cancelButton.setText(self.langData['updateCancel'])
                skipButton.setText(self.langData['updateSkip'])

                downloadButton.clicked.connect(onDownloadUpdate)
                cancelButton.clicked.connect(onCancelUpdate)
                skipButton.clicked.connect(onSkipUpdate)

                updateButtonsLayout.addWidget(downloadButton)
                updateButtonsLayout.addWidget(skipButton)
                updateButtonsLayout.addWidget(cancelButton)

                updateButtonsFrame.setLayout(updateButtonsLayout)

                updateWindowLayout.addWidget(updateLabel)
                updateWindowLayout.addWidget(updateButtonsFrame)

                self.updateWindow.setLayout(updateWindowLayout)

                

                self.updateWindow.show()
        else:
            self.updateWindow = QFrame()
            updateLabel = QLabel()
            updateWindowLayout = QVBoxLayout()
            updateButtonsFrame = QFrame()
            okButton = QPushButton()
            updateLabel.setText(self.langData['updateNotFound'])
            okButton.setText(self.langData['okayButton'])
            okButton.clicked.connect(self.updateWindow.close)
            updateWindowLayout.addWidget(updateLabel)
            updateWindowLayout.addWidget(okButton)
            self.updateWindow.setLayout(updateWindowLayout)

            self.updateWindow.setWindowTitle(self.langData['updateWindowTitle'])

            self.updateWindow.setWindowModality(Qt.ApplicationModal)

            self.updateWindow.show()

    def onExit(self):
        print('onExit')
        self.close()

print('Software made by Maniko\ngithub.com/M4NiK0\nIf you did not get it from my GitHub, then go grab it there:\nhttps://github.com/M4NIK0/MCModManager')

#Files opening for full loading of MC_MM
runLocation = os.getcwd()
versionFile = open('version', 'r')
version = versionFile.read()
versionFile.close()
print('Version loaded')

optionsFile = open('options.dat', 'r')
options = optionsFile.readlines()
optionsFile.close()
optionsDicKeys = ['lang', 'packLocation', 'backupLocation', 'checkForUpdates', 'username']
optionsDic = {}
for i in range(len(options)):
    options[i] = options[i].replace('\n', '')
    optionsDic[optionsDicKeys[i]] = options[i].replace(optionsDicKeys[i] + ' = ', '')
print('Options loaded')

#Verification of installed languages
langPass = False
langToDelete = 0
while not langPass:
    langListFile = open('langList.dat', 'r')
    langList = langListFile.readlines()
    langListFile.close()
    langListFile = open('langList.dat', 'w')
    languageToWrite = ''
    for i in range(len(langList)):
        langList[i] = langList[i].replace('\n', '')
        if not os.path.exists(runLocation + '\\lang\\' + langList[i] + '.lang'):
            print(langList[i] + '.lang', 'not found !\nDeleting from list...')
            langToDelete += 1
        else:
            languageToWrite += langList[i] + '\n'
    langListFile.write(languageToWrite)
    langListFile.close()
    if langToDelete == 0:
        langPass = True
    langToDelete = 0
print('Lang list loaded')

print("MC_MM v" + version + " run at " + runLocation)

#Load lang file based on options
if not optionsDic['lang'] in langList:
    optionsDic['lang'] = 'en-us'
    print('Lang not found, passing in en-us')

langFile = open(runLocation + '\\lang\\' + optionsDic['lang'] + '.lang', 'r', encoding="utf-8")
langData = langFile.readlines()
langFile.close()

langDic = {}
for i in range(len(langData)):
    langData[i] = langData[i].replace('\n', '')
    langData[i] = langData[i].split('|')
    langDic[langData[i][0]] = langData[i][1]
print('Lang file loaded')

app = QCoreApplication.instance()

if app is None:
    app = QApplication(sys.argv)

test = mainWindow()
test.langData, test.settingsData, test.langList, test.selectedLanguage, test.MCMMPath, test.version = langDic, optionsDic, langList, optionsDic['lang'], runLocation, version
test.continueLoad()
test.show()
app.exec()