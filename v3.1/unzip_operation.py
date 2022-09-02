import zipfile
import time
import os 
import concurrent.futures
import glob
from PyQt5.QtCore import QThread, pyqtSignal,QRect

class Unzip(QThread):

    countChanged = pyqtSignal(int)
    messageChanged = pyqtSignal(str)
    zipListChanged = pyqtSignal(str)

    def run(self):
        #初期条件
        self.all_files = self.zip_list
        self.unzip_counter = 0
        self.contents_num = 1
        self.zip_files_message = ""
        self.message = ""
        self.download_message = ""

        n = 0
        while True:
            self.countChanged.emit((self.unzip_counter/self.contents_num) * 100)
            self.contents_num = self.contents_in_zipfile(self.all_files)
            self.message_display()
            if(self.check_ren_flag == 0):
                print("here")
                with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count(), thread_name_prefix="thread") as executor:
                    executor.submit(self.job, self.all_files[0])
                    break
                break
            else:
                with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count(), thread_name_prefix="thread") as executor:
                    while (n != len(self.all_files)):
                        executor.submit(self.job, self.all_files[n])
                        n = n + 1
                        self.check_downloading()

                self.check_downloading()

        self.messageChanged.emit(self.message + "解凍完了!")
    
    def check_downloading(self):
        
        string = self.all_files[0][:self.all_files[0].rfind('-')]
        files = glob.glob(self.folder_path + '/*.zip')
        self.download_message = ""

        for f in files:
            #ダウンロード途中のファイルは除外する
            if('.part' in f):
                pass
            elif(os.path.getsize(f)==0):
                self.download_message = self.download_message + "[Waiting…]"+ os.path.basename(f) + "\n"
            
            f = f.replace('\\','/')
            if(string in f) and (f not in self.all_files):
                self.all_files.append(f)
        for i in range(len(self.all_files)):
            self.all_files[i] = self.all_files[i].replace('\\','/')

    def job(self,zip_file):
        print(zip_file)
        if(os.path.getsize(zip_file)==0):
            if(self.zip_files_message==""):
                self.download_message = "[Waiting…]"+ os.path.basename(zip_file)
            else:
                self.download_message = self.download_message + "\n[Waiting…]"+ os.path.basename(zip_file)
            
            self.zipListChanged.emit(self.zip_files_message + self.download_message)
            
        else:
            if(self.zip_files_message==""):
                self.zip_files_message = "【start】"+ os.path.basename(zip_file)
            else:
                self.zip_files_message = self.zip_files_message + "\n【start】"+ os.path.basename(zip_file)

            self.zipListChanged.emit(self.zip_files_message+ self.download_message)
            
            counter = (self.unzip_counter/self.contents_num) * 100

            with zipfile.ZipFile(zip_file) as zip_f:
                zip_f.extractall(self.output_path)

                self.unzip_counter = self.unzip_counter + len(zip_f.namelist())

                counter = (self.unzip_counter/self.contents_num) * 100
                self.countChanged.emit(counter)

            self.zip_files_message = self.zip_files_message.replace("【start】"+ os.path.basename(zip_file),"【OK】"+ os.path.basename(zip_file))
            self.zipListChanged.emit(self.zip_files_message + self.download_message)
            
            self.message_display()

    def contents_in_zipfile(self,zip_list):
        counter = 0
        if(len(zip_list)!=0):
            for zip_file in zip_list:
                try:
                    with zipfile.ZipFile(zip_file) as zip_f:
                        lst = zip_f.namelist()
                        counter = counter + len(lst)
                except:
                    pass
        return counter

    def message_display(self):
        self.message = "解凍済み："+str(self.unzip_counter)+"/"+str(self.contents_num)+"件\n"
        self.messageChanged.emit(self.message)

        if(self.contents_num == 0):
            pass
        else:
            self.countChanged.emit((self.unzip_counter/self.contents_num) * 100)
