import sys
import os

from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

import main_window

def check_setting():#設定ファイルの有無，パスが通るか確認
    
    if(os.path.isfile("setting.ini") == True):
        setting = QSettings("setting.ini", QSettings.IniFormat)
        default_directory_onboot = setting.value("default_directory_onboot")

        if os.path.isdir(default_directory_onboot):
            pass
        else:
            setting.setValue("default_directory_onboot",os.path.expanduser('~') + '/Desktop')
        
        if os.path.isdir(setting.value("default_directory")):
            pass
        else:
            setting.setValue("default_directory",os.path.expanduser('~') + '/Desktop')

    else:
        setting = QSettings("setting.ini", QSettings.IniFormat)
        setting.setValue("default_directory_onboot",os.path.expanduser('~') + '/Desktop')
        setting.setValue("default_directory",os.path.expanduser('~') + '/Desktop')
        setting.setValue("check_on",0)
        setting.setValue("check_ren",0)

if __name__ == "__main__":
    check_setting()

    app = QApplication(sys.argv)
    #app.setWindowIcon(QIcon('icon.png'))
    window = main_window.Actions()
    sys.exit(app.exec_())

