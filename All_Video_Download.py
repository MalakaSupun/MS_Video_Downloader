# this is the script for downloading all video...............

# Importing PyQt5........................
from PyQt5.QtCore import QThread, pyqtSignal   # For QThreads and QtSignal ...
from PyQt5.QtGui import QPixmap                # For QPixmap .................
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


