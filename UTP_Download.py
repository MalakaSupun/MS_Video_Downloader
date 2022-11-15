# This is for download youtube playlists .....................
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
Formats = ['bestvideo*+bestaudio/best', 'bestaudio/best',
           'bestvideo[height<=1080]+bestaudio/best[height<=1080]', 'bestvideo[height<=720]+bestaudio/best[height<=720]',
           'bestvideo[height<=480]+bestaudio/best[height<=480]', 'bestvideo[height<=360]+bestaudio/best[height<=360]',
           'bestvideo[height<=240]+bestaudio/best[height<=240]', 'bestvideo[height<=144]+bestaudio/best[height<=144]']

class Thread_DownloadUP(QtCore.QThread):
    # Signals for application ....................       
    ProgressCount = QtCore.pyqtSignal(int)      # Progress count...........
    DownloadSpeed = QtCore.pyqtSignal(str)      # Downloading speed .......
    TimeRemains = QtCore.pyqtSignal(str)        # Time remaining ..........
    Downloaded_So_Far = QtCore.pyqtSignal(str)  # Downloaded Data amount...

    def __init__(self, parent):
        QThread.__init__(self, parent)
        self.MainCode = parent
