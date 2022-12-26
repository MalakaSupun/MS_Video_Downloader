# For system operations ................
import sys

# Required PyQt5 classes
# loading Ui...............
from PyQt5.uic import loadUi
# Importing QtGui .........
from PyQt5.QtGui import *
# Importing QtCore .........
from PyQt5.QtCore import *
# Importing QtWidgets .......
from PyQt5.QtWidgets import *

# Classes that created by me.......
from YT_Check import *                 # For checking YouTube videos 
from UTV_Downloads import *            # For Downloading YouTube videos 
from YP_Check import *                 # For checking YouTube Playlists 
from UTP_Downloads import *            # For Downloading YouTube Playlists 


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('UI_Designs/UI_one.ui', self)

        # Youtube Video Downloading........................................
        self.YTV_Checks = Thread_ChecksUV(self)
        self.UTV_Downloads = Thread_ChecksUV(self)

        # Youtube Playlist Downloading....................................
        self.YTP_Checks = Thread_ChecksUP(self)
        self.UTP_Downloads = Thread_DownloadUP(self)
        
        # Setting window titles and icon .............
        self.setWindowTitle('MS Downloader')
        icon = QIcon()
        icon.addPixmap(QPixmap("Icons/Window_icon.png"))  # Main icon.......
        self.setWindowIcon(icon)
        
        # Setting current tab to welcome screen...........................
        self.tabWidget.setCurrentIndex(6)
       
        # Handling radio buttons ....................
        self.HandleRadio()
        
        # Setting default layers ......................
        self.setDefault()
        
        # Handling buttons .............................
        self.HandleButtons()
        
        # Setting threads for Qt Classes  ................
        self.thread = {}

    # Handle all the redio buttons..........................
    def HandleRadio(self):

        # Setting audio only redio buttons..................
        self.radioButton_UTV_AudioOnly.toggled.connect(self.RedioBTN_UTV_AudioOnly)
        self.radioButton_UTP_AudioOnly.toggled.connect(self.RedioBTN_UTP_AudioOnly)
        self.radioButton_FBV_AudioOnly.toggled.connect(self.RedioBTN_FBV_AudioOnly)
        self.radioButton_OV_AudioOnly.toggled.connect(self.RedioBTN_OV_AudioOnly)

        # Setting Sub redio buttons.........................
        self.radioButton_UTV_subs.toggled.connect(self.RedioBTN_UTV_Subs)
        self.radioButton_UTP_subs.toggled.connect(self.RedioBTN_UTP_Subs)
        self.radioButton_FBV_subs.toggled.connect(self.RedioBTN_FBV_Subs)
        self.radioButton_UDV_subs.toggled.connect(self.RedioBTN_UDV_Subs)
        self.radioButton_OV_subs.toggled.connect(self.RedioBTN_OV_Subs)

        # Setting mp3 redio buttons.........................
        self.radioButton_UTV_AudioOnly_MP3.toggled.connect(self.RedioBTN_UTV_AudioOnly_mp3)

    def HandleButtons(self):
        
        # Switching between Tabs......................
        self.pushButton_Welcome.clicked.connect(self.Welcome)
        self.pushButton_About.clicked.connect(self.openAbout)
        self.pushButton_Yt_Video.clicked.connect(self.openYT_V_download)
        self.pushButton_Yt_playlist.clicked.connect(self.openYT_P_download)
        self.pushButton_Facebook.clicked.connect(self.openFB_V_download)
        self.pushButton_Udemy.clicked.connect(self.openUdemy_V_download)
        self.pushButton_OtherD.clicked.connect(self.openOther_V_download)
        
        # Browse buttons for file locations............
        self.pushButton_YT_BR.clicked.connect(self.Browse_YTV)
        self.pushButton_YT_PR.clicked.connect(self.Browse_YTP)
        self.pushButton_FB_Br.clicked.connect(self.Browse_FB)
        self.pushButton_UD_Br.clicked.connect(self.Browse_UD)
        self.pushButton_O_Br.clicked.connect(self.Browse_OV)

        # Check button for videos .....................
        self.pushButton_Go_1.clicked.connect(self.GO_YTV)
        self.pushButton_Go_2.clicked.connect(self.GO_YTP)
        self.pushButton_YTV_Download_BTN.clicked.connect(self.Download_Yt_Video)
        self.pushButton_YTP_Downloads.clicked.connect(self.Download_Yt_PlayList)        

    # Handle all the normal operations ....................
    def setDefault(self):
        # set visibility off of the tab icons..............
        self.tabWidget.tabBar().setVisible(False)

        # Differences type additions for application................
        Q1 = [' Best Audio & Video', ' 1080p', ' 720p', ' 480p', ' 360p', ' 240p', ' 144p']
        Q2 = [' English', ' Sinhala', 'Tamil']
        Q3 = [' Edge', ' Chrome', ' FireFox']
        Q4 = [' Best Audio & Video', ' SD', ' HD', ' 1080p', ' 720p', ' 480p', ' 360p', ' 240p', ' 144p']
        # Video Quality addition.....................................
        self.comboBox_Quality_YV.addItems(Q1)
        self.comboBox_Quality_VP.addItems(Q1)
        self.comboBox_Quality_UD.addItems(Q1)
        self.comboBox_Quality_OV.addItems(Q1)
        # Sub language Addition......................................
        self.comboBox_Quality_Sub_YP.addItems(Q2)
        self.comboBox_Quality_Sub_YV.addItems(Q2)
        self.comboBox_Quality_Sub_FB.addItems(Q2)
        self.comboBox_Quality_Sub_UDV.addItems(Q2)
        self.comboBox_Quality_Sub_OV.addItems(Q2)
        # Browser Additions..........................................
        self.comboBox_Quality_OV_Bz.addItems(Q3)
        self.comboBox_Quality_OVP_Bz.addItems(Q3)
        self.comboBox_Quality_FB_Bz.addItems(Q3)
        # Video quality for sd & HD additions........................
        self.comboBox_Quality_FB.addItems(Q4)

        # Set starting progress Bar values.............
        self.progressBar_YT_V.setValue(0)
        self.progressBar_VT_Pt.setValue(0)
        self.progressBar_YT_Pv.setValue(0)
        self.progressBar_FB.setValue(0)
        self.progressBar_UD_V.setValue(0)
        self.progressBar_UD_VT.setValue(0)
        self.progressBar_O_V.setValue(0)

        # Set Strings to labels..............
        self.label_Pcomplete_UTV.setText(" Add a YouTube video URL to Download............... ")
        self.label_Pcomplete_YT_P.setText(" Add a YouTube PlayList URL to Download................ ")
        self.label_Pcomplete_FB.setText(" Add a FaceBook video URL to Download............... ")
        self.label_Vcomplete_UD.setText(" Add a Udemy course URL to Download...............")
        self.label_Vcomplete_OV.setText(" Add a video URL to Download....................")
        

    # Browse all the dialogs for file saving place ........
    def Browse_YTV(self):
        try:
            # Browse folder for video to download
            file_YTV = str(QFileDialog.getExistingDirectory(self, " Select Directory to Save Video "))
            self.lineEdit_YTV_F.setText(str(file_YTV))
        except:
            self.label_Pcomplete_UTV.setText("An Error is Occurred")

    def Browse_YTP(self):
        try:
            file_YTP = str(QFileDialog.getExistingDirectory(self, " Select Directory to Save Videos "))
            self.lineEdit_VT_P.setText(str(file_YTP))
        except:
            self.label_Pcomplete_YT_P.setText("An Error is Occurred")

    def Browse_FB(self):
        try:
            file_FB = str(QFileDialog.getExistingDirectory(self, " Select Directory to Save Videos "))
            self.lineEdit_FB_F.setText(str(file_FB))
        except:
            self.label_Pcomplete_FB.setText("An Error is Occurred")

    def Browse_UD(self):
        try:
            file_UD = str(QFileDialog.getExistingDirectory(self, " Select Directory to Save Videos "))
            self.lineEdit_UD_F.setText(str(file_UD))
        except:
            self.label_Vcomplete_UD.setText("An Error is Occurred")

    def Browse_OV(self):
        try:
            file_OV = str(QFileDialog.getExistingDirectory(self, " Select Directory to Save Videos "))
            self.lineEdit_O_F.setText(str(file_OV))
        except:
            self.label_Vcomplete_OV.setText("An Error is Occurred")

    # Adding all the pictures for the App window ..........
    def Set_Thumbs_forTerminates(self):
        pic = 'Icons\Tumbs\LightingMQ.png'
        pix = QPixmap(pic)
       
        if self.tabWidget.currentIndex() == 0:
            self.Youtube_Vthumbnail.setPixmap(pix)
        elif self.tabWidget.currentIndex() == 1:
            self.Youtube_Pthumbnail.setPixmap(pix)

    # Redio buttons for new name...........................
    def RedioBTN_UTV_AudioOnly_mp3(self):
        Bs_1 = self.sender()
        if Bs_1.isChecked():
            print('Checked - YouTube - get Mp3 from video')
        else:
            print('Un-Checked - YouTube -  Get best audio from video')

    def RedioBTN_FBV_AudioOnly_mp3(self):
        Bs_2 = self.sender()
        if Bs_2.isChecked():
            self.lineEdit_FB_Nname.setDisabled(False)
            self.label_47.setDisabled(False)
            print('Checked - redioBTN_FB_AudioOnly')
        else:
            self.lineEdit_FB_Nname.setDisabled(True)
            self.label_47.setDisabled(True)
            print('Un-Checked - redioBTN_FB_AudioOnly')

    def RedioBTN_OV_AudioOnly_mp3(self):
        Bs_3 = self.sender()
        if Bs_3.isChecked():
            self.lineEdit_OV_Nname.setDisabled(False)
            self.label_15.setDisabled(False)
            print('Checked - redioBTN_OV_AudioOnly')
        else:
            self.lineEdit_OV_Nname.setDisabled(True)
            self.label_15.setDisabled(True)
            print('Un-Checked - redioBTN_OV_AudioOnly')

    # Redio buttons for Audio only.........................
    def RedioBTN_UTV_AudioOnly(self):
        Bs_4 = self.sender()
        if Bs_4.isChecked():
            self.comboBox_Quality_YV.setDisabled(True)
            self.label_2.setDisabled(True)
            print('Checked - redioBTN_OV_Audio only')
            self.radioButton_UTV_AudioOnly_MP3.setDisabled(False)
        else:
            self.comboBox_Quality_YV.setDisabled(False)
            self.label_2.setDisabled(False)
            self.radioButton_UTV_AudioOnly_MP3.setDisabled(True)
            print('Un-Checked - redioBTN_OV_Audio only')

    def RedioBTN_UTP_AudioOnly(self):
        Bs_5 = self.sender()
        if Bs_5.isChecked():
            self.comboBox_Quality_VP.setDisabled(True)
            self.label_24.setDisabled(True)
            print('Checked - redioBTN_OV_Audio only')
        else:
            self.comboBox_Quality_VP.setDisabled(False)
            self.label_24.setDisabled(False)
            print('Un-Checked - redioBTN_OV_Audio only')

    def RedioBTN_FBV_AudioOnly(self):
        Bs_6 = self.sender()
        if Bs_6.isChecked():
            self.comboBox_Quality_FB.setDisabled(True)
            self.label_25.setDisabled(True)
            print('Checked - redioBTN_OV_Nname')
        else:
            self.comboBox_Quality_FB.setDisabled(False)
            self.label_25.setDisabled(False)
            print('Un-Checked - redioBTN_OV_Nname')

    def RedioBTN_OV_AudioOnly(self):
        Bs_6 = self.sender()
        if Bs_6.isChecked():
            self.comboBox_Quality_OV.setDisabled(True)
            self.label_14.setDisabled(True)
            print('Checked - redioBTN_OV_Nname')
        else:
            self.comboBox_Quality_OV.setDisabled(False)
            self.label_14.setDisabled(False)
            print('Un-Checked - redioBTN_OV_Nname')

    # Redio buttons for enable Subs........................
    def RedioBTN_UTV_Subs(self):
        Bs_7 = self.sender()
        if Bs_7.isChecked():
            self.comboBox_Quality_Sub_YV.setDisabled(False)
            self.radioButton_YTV_subM.setDisabled(False)
            print('Checked - redioBTN_UTV_subs')
        else:
            self.comboBox_Quality_Sub_YV.setDisabled(True)
            self.radioButton_YTV_subM.setDisabled(True)
            print('Un-Checked - redioBTN_UTV_subs')

    def RedioBTN_UTP_Subs(self):
        Bs_8 = self.sender()
        if Bs_8.isChecked():
            self.radioButton_YTP_subM.setDisabled(False)
            self.comboBox_Quality_Sub_YP.setDisabled(False)
            print('Checked - redioBTN_UTP_subs')
        else:
            self.comboBox_Quality_Sub_YP.setDisabled(True)
            self.radioButton_YTP_subM.setDisabled(True)
            print('Un-Checked - redioBTP_UTV_subs')

    def RedioBTN_FBV_Subs(self):
        Bs_9 = self.sender()
        if Bs_9.isChecked():
            self.comboBox_Quality_Sub_FB.setDisabled(False)
            self.radioButton_FB_subM.setDisabled(False)
            print('Checked - redioBTN_FBV_subs')
        else:
            self.comboBox_Quality_Sub_FB.setDisabled(True)
            self.radioButton_FB_subM.setDisabled(True)
            print('Un-Checked - redioBTN_FBV_subs')

    def RedioBTN_UDV_Subs(self):
        Bs_10 = self.sender()
        if Bs_10.isChecked():
            self.comboBox_Quality_Sub_UDV.setDisabled(False)
            self.radioButton_UD_subM.setDisabled(False)
            print('Checked - redioBTN_UDV_subs')
        else:
            self.comboBox_Quality_Sub_UDV.setDisabled(True)
            self.radioButton_UD_subM.setDisabled(True)
            print('Un-Checked - redioBTN_UDV_subs')

    def RedioBTN_OV_Subs(self):
        Bs_11 = self.sender()
        if Bs_11.isChecked():
            self.comboBox_Quality_Sub_OV.setDisabled(False)
            self.radioButton_Ov_subM.setDisabled(False)
            self.label_18.setDisabled(False)
            print('Checked - redioBTN_OV_subs')
        else:
            self.comboBox_Quality_Sub_OV.setDisabled(True)
            self.radioButton_Ov_subM.setDisabled(True)
            self.label_18.setDisabled(True)
            print('Un-Checked - redioBTN_OV_subs')

    # Switching between Tabs ..............................
    def openYT_V_download(self):
        self.tabWidget.setCurrentIndex(0)
        self.Other_Main_Icon.setPixmap(QPixmap('Icons/Youtube.png'))
        self.Other_Main_Icon_2.setPixmap(QPixmap(''))

    def openYT_P_download(self):
        self.tabWidget.setCurrentIndex(1)
        self.Other_Main_Icon.setPixmap(QPixmap('Icons/Youtube.png'))
        self.Other_Main_Icon_2.setPixmap(QPixmap('Icons/Playlist.png'))

    def openFB_V_download(self):
        self.tabWidget.setCurrentIndex(2)
        self.Other_Main_Icon.setPixmap(QPixmap('Icons/Facebook.png'))
        self.Other_Main_Icon_2.setPixmap(QPixmap(''))

    def openUdemy_V_download(self):
        self.tabWidget.setCurrentIndex(3)
        self.Other_Main_Icon.setPixmap(QPixmap('Icons/Multimedia.png'))
        self.Other_Main_Icon_2.setPixmap(QPixmap('Icons/Playlist.png'))

    def openOther_V_download(self):
        self.tabWidget.setCurrentIndex(4)
        self.Other_Main_Icon.setPixmap(QPixmap('Icons/Multimedia.png'))
        self.Other_Main_Icon_2.setPixmap(QPixmap(''))

    def openAbout(self):
        self.tabWidget.setCurrentIndex(5)
        self.Other_Main_Icon.setPixmap(QPixmap('Icons/Window_icon_1.png'))
        #self.Other_Main_Icon_About.setPixmap(QPixmap('Icons/Thumbnail_1.png'))
        self.Other_Main_Icon_2.setPixmap(QPixmap(''))

    def Welcome(self):
        self.tabWidget.setCurrentIndex(6)
 # ______________________________________________YouTube Video________________________________________________
 # Start downloading YouTube videos .....................       
    def Download_Yt_Video(self):
        self.thread[1] = Thread_DownloadUV(self)
        self.thread[1].start()
        # Three signals for the application interface ......................
        self.thread[1].ProgressCount.connect(self.YTV_ProgressBar)
        self.thread[1].DownloadSpeed.connect(self.YTV_Downloading_Speed)
        self.thread[1].TimeRemains.connect(self.YTV_Downloading_Time_Remains)
        
 # Getting all the necessary information for app interface ..................     
    def GO_YTV(self):
        self.thread[2] = Thread_ChecksUV(self)
        self.thread[2].start()
        link = self.lineEdit_YTV_link.text()
        if link != '':
            self.Checking_GIF()
            
    # Checking for video information .........................    
    def Checking_GIF(self):
        Loading_GIf = QMovie("GIFs/Magnify_no_Background.gif")
        self.Youtube_Vthumbnail.setMovie(Loading_GIf)
        Loading_GIf.start()

    def YTV_ProgressBar(self, The_percentage):
        cnt = The_percentage
        self.progressBar_YT_V.setValue(cnt)

    def YTV_Downloading_Speed(self, The_Speed):
        Speed = The_Speed
        self.label_DSpeed_YTV_2.setText(str(Speed))

    def YTV_Downloading_Time_Remains(self, The_Time):
        TimeRemaining = The_Time
        self.label_RTime_YTV_2.setText(TimeRemaining)
        
# ______________________________________________YouTube Playlist _______________________________________________
    
    def Download_Yt_PlayList(self):
        self.thread[4] = Thread_DownloadUP(self)
        self.thread[4].start() 
    
    def GO_YTP(self):
        self.thread[3] = Thread_ChecksUP(self)
        self.thread[3].start()
        PlayListURL = self.lineEdit_YTP_link.text()
        if PlayListURL != '':
            Loading_GIf = QMovie("GIFs/Magnify_no_Background.gif")  // Loading Gif
            self.Youtube_Pthumbnail.setMovie(Loading_GIf)           // set off Gif
            Loading_GIf.start()                                     // start gif..................
              

def main():
    App = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    App.exec_()


if __name__ == '__main__':
    main()
