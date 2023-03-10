
# Importing PyQt5........................
from PyQt5.QtCore import QThread, pyqtSignal # QThread, pyqtSignal packages importings
from PyQt5.QtGui import QPixmap              # QPixmap package importing
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
Formats = ['bestvideo*+bestaudio/best', 'bestaudio/best',              # Best Video
           'bestvideo[height<=1080]+bestaudio/best[height<=1080]',     # 1080p
           'bestvideo[height<=720]+bestaudio/best[height<=720]',       # 720p
           'bestvideo[height<=480]+bestaudio/best[height<=480]',       # 480p 
           'bestvideo[height<=360]+bestaudio/best[height<=360]',       # 360p
           'bestvideo[height<=240]+bestaudio/best[height<=240]',       # 244p
           'bestvideo[height<=144]+bestaudio/best[height<=144]']       # 144p

class Thread_DownloadUP(QtCore.QThread):
    # Signals for application ....................       
    ProgressCount = QtCore.pyqtSignal(int)      # Progress count...........
    DownloadSpeed = QtCore.pyqtSignal(str)      # Downloading speed .......
    TimeRemains = QtCore.pyqtSignal(str)        # Time remaining ..........
    Downloaded_So_Far = QtCore.pyqtSignal(str)  # Downloaded Data amount...

    def __init__(self, parent):
        QThread.__init__(self, parent)
        self.MainCode = parent
           
           
    def get_Video_info(self):
       
        ydl_opts = {'format': self.Formats, 'no_warnings': True, 'ignoreerrors': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(self.The_link, download=False)
            A = json.dumps(ydl.sanitize_info(info), indent=2)
            B = json.loads(A)

            self.isPlayList = B["_type"]
            print(f"Your link is representing a : {self.isPlayList}")

