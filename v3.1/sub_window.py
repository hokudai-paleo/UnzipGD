from PyQt5.QtCore import QSettings

from PyQt5.QtWidgets import (QDialog,QCheckBox,QProgressBar,QPushButton,QLabel,QFileDialog)
from unzip_operation import Unzip

class DefaultPathWindow:
    def __init__(self, parent=None):
        self.setting = QSettings("setting.ini", QSettings.IniFormat)
        self.default_directory_onboot = self.setting.value("default_directory_onboot")
        self.check_flag = int(self.setting.value("check_on"))
        self.default_directory = self.setting.value("default_directory")

        self.w = QDialog(parent)
        self.parent = parent
        self.w.setGeometry(750, 525, 400, 270)  
        self.w.setWindowTitle('UnZip For GD')

        ###起動時設定###
        self.check = QCheckBox(self.w)
        self.check.move(10, 20)
        self.check.clicked.connect(self.checkbox)
        self.check.setChecked(self.check_flag)

        labelCheck = QLabel(self.w)
        labelCheck.move(30, 20)
        labelCheck.setText('アプリ起動時に，ファイル選択ダイアログを表示する')
        
        labelButton = QLabel(self.w)
        labelButton.move(30, 50)
        labelButton.setText('起動ディレクトリ変更')

        self.selectButton = QPushButton('Select', self.w)
        self.selectButton.move(180, 45)
        self.selectButton.clicked.connect(self.select_default_directory_onboot)

        self.labelSetting = QLabel(self.w)
        self.labelSetting.move(30, 80)
        self.setting_message = "設定値："+self.setting.value("default_directory_onboot")
        self.labelSetting.setText(self.setting_message)

        ###デフォルト使用時設定###
        labelCheckDefa = QLabel(self.w)
        labelCheckDefa.move(30, 130)
        labelCheckDefa.setText('通常使用時のルートディレクトリ設定')
        
        labelButtonDefa = QLabel(self.w)
        labelButtonDefa.move(30, 160)
        labelButtonDefa.setText('起動ディレクトリ変更')

        self.selectButtonDefa = QPushButton('Select', self.w)
        self.selectButtonDefa.move(180, 155)
        self.selectButtonDefa.clicked.connect(self.select_default_directory)

        self.labelSettingDefa = QLabel(self.w)
        self.labelSettingDefa.move(30, 190)
        setting_message_defa = "設定値："+self.setting.value("default_directory")
        self.labelSettingDefa.setText(setting_message_defa)

        ##セーブ・キャンセル##
        self.saveButton = QPushButton('Save', self.w)
        self.saveButton.move(80, 230)
        self.saveButton.clicked.connect(self.save)
        self.saveButton.clicked.connect(self.w.close)

        self.cancelButton = QPushButton('Cancel', self.w)
        self.cancelButton.move(180, 230)
        self.cancelButton.clicked.connect(self.w.close)

    def save(self):
        self.setting.setValue("check_on",self.check_flag)
        self.setting.setValue("default_directory_onboot",self.default_directory_onboot)
        self.setting.setValue("default_directory",self.default_directory)
        
    def checkbox(self,state):
        if(state == False):
            self.check_flag = 0
        else:
            self.check_flag = 1

    def select_default_directory_onboot(self):
        select_directory = QFileDialog.getExistingDirectory(self.w, 'Select Directory',self.default_directory_onboot)
        if (select_directory!=""):
            self.default_directory_onboot = select_directory
        
            self.setting_message = "設定値："+self.default_directory_onboot
            self.labelSetting.setText(self.setting_message)

    def select_default_directory(self):
        select_directory = QFileDialog.getExistingDirectory(self.w, 'Select Directory',self.default_directory)
        if (select_directory!=""):
            self.default_directory = select_directory
        
            setting_message = "設定値："+self.default_directory
            self.labelSettingDefa.setText(setting_message)
        
    # ここで親ウィンドウに値を渡している
    def setParamOriginal(self):
        self.parent.setParam(self.edit.text())

    def show(self):
        self.w.exec_()



class OptionWindow:
    def __init__(self, parent=None):
        self.setting = QSettings("setting.ini", QSettings.IniFormat)
        self.check_flag = int(self.setting.value("check_ren"))

        self.w = QDialog(parent)
        self.parent = parent
        self.w.setGeometry(750, 525, 280, 270)  
        self.w.setWindowTitle('UnZip For GD')

        ###起動時設定###
        self.check = QCheckBox(self.w)
        self.check.move(10, 20)
        self.check.clicked.connect(self.checkbox)
        self.check.setChecked(self.check_flag)

        labelCheck = QLabel(self.w)
        labelCheck.move(30, 20)
        labelCheck.setText('連番ファイル選択機能を使用する')
        
        ##セーブ・キャンセル##
        self.saveButton = QPushButton('Save', self.w)
        self.saveButton.move(80, 230)
        self.saveButton.clicked.connect(self.save)
        self.saveButton.clicked.connect(self.w.close)

        self.cancelButton = QPushButton('Cancel', self.w)
        self.cancelButton.move(180, 230)
        self.cancelButton.clicked.connect(self.w.close)


    def save(self):
        self.setting.setValue("check_ren",self.check_flag)
        
    def checkbox(self,state):
        if(state == False):
            self.check_flag = 0
        else:
            self.check_flag = 1

    # ここで親ウィンドウに値を渡している
    def setParamOriginal(self):
        self.parent.setParam(self.edit.text())

    def show(self):
        self.w.exec_()
