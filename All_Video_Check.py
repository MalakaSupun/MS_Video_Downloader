# Importing PyQt5........................
from PyQt5.QtCore import QThread, pyqtSignal   # For QThread and QtSignal.......
from PyQt5.QtGui import QPixmap                # For QPixmp ....................
# Video downloading package .............
import yt_dlp                                    # this is the most important module for app
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

# All direct sub languages available for video.....
lang = []
# All auto sub languages available for video.....
Auto_langs = []
# Subtitles that need to download......
Alw_Sub_Languages = ['en', 'si', 'ta']
# Available auto sub languages..........
Auto_Sub_Langs = []
# Not available direct subs ..............
Not_In_Direct_Sub = []
# Not available auto subs ................
Not_In_Auto_Sub = []

class Thread_ChecksUP(QThread):
    # Signal for playlist ..................
    Playlist_details = QtCore.pyqtSignal(int)

    def __init__(self, parent):
        QThread.__init__(self, parent)
        self.MainCode = parent

        # Main video parameters ....................
        self.Thumbnail_To_Download = ''
        self.Formats = ''
        self.The_link = ''
        self.channelName = ''
        self.YTP_VideoCount = ''
        self.YTP_ViewCount = ''
        self.YTP_title = ''
        self.isPlayList = ''
        self.Audio_Size = ''
        self.Audio_Format = ''
        self.Uploaded_Date = ''
        
        # Thumbnail list ............................
        self.thumbnails = []
        
        # Setting status of the application .........
        self.Video_checked = 0

