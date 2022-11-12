

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


lang = []
Auto_langs = []
# Subtitles that need to download......
Alw_Sub_Languages = ['en', 'si', 'ta']
Auto_Sub_Langs = []
Not_In_Direct_Sub = []
Not_In_Auto_Sub = []

