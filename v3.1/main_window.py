from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import (QMainWindow,QProgressBar,QPushButton,QTextEdit,QLabel,QFileDialog,QAction,qApp,QStyle,QStatusBar,QCheckBox)

import os
import zipfile
import glob
import time
import sys

import sub_window
from unzip_operation import Unzip

class Actions(QMainWindow):

    def __init__(self):
        self.select_zips_flag = False
        self.select_directory_flag = False

        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setting = QSettings("setting.ini", QSettings.IniFormat)

        self.setGeometry(700, 500, 520, 300)  
        self.setWindowTitle('UnZip For GD')

        ###↓メニューバー↓###
        exitAction = QAction(self.style().standardIcon(QStyle.SP_DialogCancelButton),'&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        settingDefaultPath = QAction('&ディレクトリ設定', self)        
        settingDefaultPath.setShortcut('Ctrl+D')
        settingDefaultPath.triggered.connect(self.makeDirectoryWindow)

        settingOption = QAction('&オプション機能', self)        
        settingOption.setShortcut('Ctrl+O')
        settingOption.triggered.connect(self.makeOptionWindow)

        self.statusBar = QStatusBar()

        menubar = self.menuBar()
        settings = menubar.addMenu('&設定')
        settings.addAction(settingDefaultPath)
        settings.addAction(settingOption)
        settings.addAction(exitAction)

        ###↑メニューバー↑###

        zip_label = QLabel('Zip File',self)
        zip_label.move(10, 35)
        output_label = QLabel('Output Folder',self)
        output_label.move(10, 130)

        self.zipText = QTextEdit(self)
        self.zipText.setGeometry(100, 35,300,80)
        self.zipText.setEnabled(True)
        self.zipText.setMouseTracking(False)
        self.zipText.setTabletTracking(True)
        self.zipText.setAcceptDrops(True)
        self.zipText.setReadOnly(True)

        self.zipSelectButton = QPushButton('Select', self)
        self.zipSelectButton.move(410, 85)       

        self.outputText = QTextEdit(self)
        self.outputText.setGeometry(100, 130,300,30)
        self.outputText.setEnabled(True)
        self.outputText.setMouseTracking(False)
        self.outputText.setTabletTracking(True)
        self.outputText.setAcceptDrops(True)
        self.outputText.setReadOnly(True)

        self.outputSelectButton = QPushButton('Select', self)
        self.outputSelectButton.move(410, 130)

        self.execText = QTextEdit(self)
        self.execText.setGeometry(100, 175,300,70)
        self.execText.setEnabled(True)
        self.execText.setMouseTracking(False)
        self.execText.setTabletTracking(True)
        self.execText.setAcceptDrops(True)
        self.execText.setReadOnly(True)

        self.execButton = QPushButton('Start', self)
        self.execButton.move(410, 215)

        self.progress = QProgressBar(self)
        self.progress.setGeometry(100, 255, 290, 25)
        self.progress.setMaximum(100)

        self.show()
       
        self.default_directory_onboot = self.setting.value("default_directory_onboot")
        self.check_on_flag = self.setting.value("check_on")

        if(int(self.check_on_flag) == 1):
            self.select_zips()

        self.zipSelectButton.clicked.connect(self.select_zips)

        self.execButton.clicked.connect(self.exec_button)
        self.outputSelectButton.clicked.connect(self.select_directory)

    def makeDirectoryWindow(self):
        subWindow = sub_window.DefaultPathWindow(self)
        subWindow.show()

    def makeOptionWindow(self):
        subWindow = sub_window.OptionWindow(self)
        subWindow.show()

    def select_zips(self):        
        self.default_directory = self.setting.value("default_directory")
        self.check_ren_flag = self.setting.value("check_ren")

        if(int(self.check_ren_flag) == 1):
            self.zip_list = self.select_ren_zips()

        else:
            # 第二引数はダイアログのタイトル、第三引数は表示するパス
            fnames = QFileDialog.getOpenFileNames(self, 'Open file',self.default_directory,"Zip files (*.zip)")
            self.zip_list = list(fnames[0])
            try:
                self.folder_path = self.zip_list[0][:self.zip_list[0].rfind('/')]
            except:
                pass
        zip_message = ""
        for zip_file_name in self.zip_list:
            message = os.path.basename(zip_file_name)
            if(zip_message==""):
                zip_message = message
            else:
                zip_message = zip_message + "\n" + message

        self.zipText.setText(zip_message)
        if (len(self.zip_list)!=0):
            self.select_zips_flag = True

    def select_ren_zips(self):
        fname = QFileDialog.getOpenFileName(self, '連番のZipファイルをすべて選択できます．', self.default_directory,"Zip files (*.zip)")
        self.folder_path = fname[0][:fname[0].rfind('/')]
        string = fname[0][:fname[0].rfind('-')]
        files = glob.glob(self.folder_path + '/*')
        
        
        if fname[0] == '':
            return []
        zip_list = []
        for f in files:
            if('.part' in f):
                pass
            else:
                f = f.replace('\\','/')
                if(string in f):
                    zip_list.append(f)

        return zip_list

    def select_directory(self):
        self.default_directory = self.setting.value("default_directory")
        self.output_dir = QFileDialog.getExistingDirectory(self, 'Select Directory',self.default_directory)

        self.outputText.setText(self.output_dir)
        if (self.output_dir!=""):
            self.select_directory_flag = True

    def onButtonClick(self):
        self.calc = External()
        self.calc.countChanged.connect(self.onCountChanged)
        self.calc.start()

    def exec_button(self):
        is_chacked = self.file_chacker()
        end_flag = False
        if is_chacked == True:
            self.zipSelectButton.setEnabled(False)
            self.outputSelectButton.setEnabled(False)
            self.execButton.setEnabled(False)
            
            self.execStart = Unzip()
            self.execStart.countChanged.connect(self.onCountChanged)
            self.execStart.messageChanged.connect(self.onMessage)
            self.execStart.zipListChanged.connect(self.onZipMessage)
            self.execStart.zip_list = self.zip_list
            self.execStart.output_path = self.output_dir
            self.execStart.folder_path = self.folder_path
            self.execStart.check_ren_flag = int(self.check_ren_flag)
            self.execStart.Text = self.execText
            self.execStart.start()
            
    def onCountChanged(self, value):
        self.progress.setValue(value)
    
    def onMessage(self, message):
        self.execText.setText(message)
    
    def onZipMessage(self, message):
        self.zipText.setText(message)

    def contents_in_zipfile(self):
        counter = 0
        for zip_file in self.zip_list:
            with zipfile.ZipFile(zip_file) as zip_f:
                lst = zip_f.namelist()
                counter = counter + len(lst)
        return counter          

    def file_chacker(self):
        if (self.select_directory_flag==True) and (self.select_zips_flag == True):
            return True
        else:
            self.execText.setText("出力先，zipファイルの設定を確認してください.")
            return False

