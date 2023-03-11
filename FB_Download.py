
# Importing PyQt5........................
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
# Video downloading package .............
import yt_dlp
# Importing json ........................
import json
# Requests module for thumbnail ........
import requests
# Time module for calculating time .....
import time
# For Threading ..........................
import concurrent.futures
# For Sound notification .................
import winsound
# Class imports ..........................
from YT_Check import *
# For notification ........................
from plyer import 


# All the formats ..........................
Formats = ['bestvideo*+bestaudio/best', 'bestaudio/best',                                         # Best video and audios
           'bestvideo[height<=1080]+bestaudio/best[height<=1080]',                                # 1080p                                               
           'bestvideo[height<=720]+bestaudio/best[height<=720]',                                  # 720p
           'bestvideo[height<=480]+bestaudio/best[height<=480]',                                  # 480p
           'bestvideo[height<=360]+bestaudio/best[height<=360]',                                  # 360p
           'bestvideo[height<=240]+bestaudio/best[height<=240]',                                  # 240p
           'bestvideo[height<=144]+bestaudio/best[height<=144]']                                  # 144p



def run(self):
        self.VideoDownloaded = 0
        link = self.MainCode.lineEdit_YTV_link.text()    # Link of the video.....
        self.Link = link
        if link != '':
            self.The_link = link.replace('&', '"&"')      # Replace link with & marks
            # print(self.The_link)
            self.MainCode.label_Pcomplete_UTV.setText("................... Downloading Started ...................")
        else:
            print("Enter a Link to download..........")                 

        self.Video_folder = self.MainCode.lineEdit_YTV_F.text()
        # print(f'Downloading Location : "{self.Video_folder}"')

        if self.MainCode.radioButton_UTV_AudioOnly.isChecked():
            if self.Video_folder != '':
                # print("Audio Only")
                self.Format_Selection()   # Selecting formats to downloading ......
                self.Downloader()         # Execute Downloading function ..........
                self.MainCode.label_Pcomplete_UTV.setText("................... Format Downloaded ...................")
                self.MainCode.progressBar_YT_V.setValue(0)
            else:
                self.MainCode.label_Pcomplete_UTV.setText("............. Add Location to Download  .............")

        else:
            if self.Video_folder != '':
                self.Format_Requested = self.MainCode.comboBox_Quality_YV.currentIndex()
                print(f'Requested Format :{self.Format_Requested}')
                self.Format_Selection() 
                self.Downloader()         
                self.MainCode.label_Pcomplete_UTV.setText("................... Video Downloaded ...................")
                self.MainCode.progressBar_YT_V.setValue(0)                                                                 # Zeroing progress bar.......
                self.VideoDownloaded = 1                                                                                                                             
                self.Notifications()                                                                                       # Sendin out notifications....


            else:
                self.MainCode.label_Pcomplete_UTV.setText("............. Add Location to Download Video .............")
                self.Notifications()                                                                                        # Sendin out notifications...
                      
                




