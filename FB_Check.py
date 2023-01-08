# For Facebook Video information checking .

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
from plyer import notification


# All the formats ..........................
Formats = ['bestvideo*+bestaudio/best', 'bestaudio/best',
           'bestvideo[height<=1080]+bestaudio/best[height<=1080]', 'bestvideo[height<=720]+bestaudio/best[height<=720]',
           'bestvideo[height<=480]+bestaudio/best[height<=480]', 'bestvideo[height<=360]+bestaudio/best[height<=360]',
           'bestvideo[height<=240]+bestaudio/best[height<=240]', 'bestvideo[height<=144]+bestaudio/best[height<=144]']

# all sub languages available for video.....
lang = []

# all Auto sub languages available for video.....
Auto_langs = []
# Subtitles that need to download......
Alw_Sub_Languages = ['en', 'si', 'ta']
# Available auto languages available for video.....
Auto_Sub_Langs = []
# Not Available direct languages available for video.....
Not_In_Direct_Sub = []
# Not Available auto languages available for video.....
Not_In_Auto_Sub = []

   def run(self):
        self.MainCode.progressBar_YT_V.setValue(0)
        self.MainCode.label_Pcomplete_YT_P.setText("................... Playlist Checking ...................")
        print("................... Playlist Checking ...................")
        
        # Getting link from the UI ........
        self.The_link = self.MainCode.lineEdit_YTP_link.text()          

        # If the empty ........
        if self.The_link != '':
            print(f"Playlist URL : {self.The_link}")

            if self.MainCode.radioButton_UTV_AudioOnly.isChecked():
                self.Formats = 'bestaudio/best'
            else:
                self.Formats = 'bestvideo*+bestaudio/best'

            self.get_Video_info()
            # Setting status of the application .........
            self.Video_checked = 1

        else:
            print("Add Link to Download / Check")
            self.MainCode.label_Pcomplete_YT_P.setText(
                "................... Add Link to Download / Check ...................")
            self.MainCode.Youtube_Pthumbnail.setPixmap(QPixmap(r'Icons\Tumbs\LightingMQ.png'))
