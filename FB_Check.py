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

  class Thread_ChecksUV(QThread):
    # Thread Signal for application....
    countChanged = QtCore.pyqtSignal(int)

    def __init__(self, parent):
        QThread.__init__(self, parent)
        self.MainCode = parent
        # Parameters for application.....
        self.Filtered_Auto_Subs = []
        self.Available_Subs = []
        self.Video_checked = 0
        self.V240p_Size = " "
        self.V360p_Size = " "
        self.V480p_Size = " "
        self.V720p_Size = " "
        self.V1080p_Size = " "
        self.Direct_Sub_Avalability = " "
        self.Video_Duration = " "
        self.YTV_ViewCount = 0000
        self.Uploded_Date = " "
        self.Yt_Channle = " "
        self.Auto_Sub_Avalability = " "
        self.Thumbnail_Link = " "
        self.Thumbnail_URL = " "
        self.YT_title = " "
        self.BestV_Size = " "
        self.BestV_Format = " "
        self.V144p_Size = " "
        self.Audio_Size = " "
        self.Audio_Format = " "
        self.The_link = " "
        self.F_Requested = " "
        # self.Formats = " "
        self.Commands_for_subs = []
        self.Filtered_Direct_Subs = []


