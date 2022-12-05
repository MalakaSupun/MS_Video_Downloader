# PyQt5 libraries ............................
from PyQt5 import QtCore                       # QtCore importing
from PyQt5.QtCore import QThread, pyqtSignal   # QThread and PyQt Signal import
from PyQt5.QtGui import QPixmap                # QPixmp import

# yt-dlp for download  videos..................
import yt_dlp

# for run external  commands ..................
import subprocess

# for get video thumbnails ....................
import requests

# time module for tasks  ......................
import time

# for handling json files .....................
import json

# for maintaining muilti-threading ...........
import concurrent.futures

# Subtitle languages .......
lang = []
# Auto su languages....... 
Auto_langs = []
# Subtitles that need to download......
Alw_Sub_Languages = ['en', 'si', 'ta']
# Auto available subtitles ............ 
Auto_Sub_Langs = []
# Not available direct subtitles ............ 
Not_In_Direct_Sub = []
# Auto available subtitles ............ 
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

    def run(self):
        self.MainCode.progressBar_YT_V.setValue(0)
        self.MainCode.label_Pcomplete_YT_P.setText("................... Playlist Checking ...................")
        print("................... Playlist Checking ...................")
        
        // Getting link from the UI ........
        self.The_link = self.MainCode.lineEdit_YTP_link.text()          

        // If the empty ........
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

    def get_Video_info(self):
       
        ydl_opts = {'format': self.Formats, 'no_warnings': True, 'ignoreerrors': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(self.The_link, download=False)
            A = json.dumps(ydl.sanitize_info(info), indent=2)
            B = json.loads(A)

            self.isPlayList = B["_type"]
            print(f"Your link is representing a : {self.isPlayList}")

            // Need to be a playlist to execute this code ........
            if self.isPlayList == "playlist":
                try:
                    self.YTP_title = B["title"]
                    self.YTP_VideoCount = B["playlist_count"]
                    self.YTP_ViewCount = B["view_count"]
                    Date = B["modified_date"]
                    self.Uploaded_Date = f'{Date[0]}{Date[1]}{Date[2]}{Date[3]}/{Date[4]}{Date[5]}/{Date[6]}{Date[7]}'
                    self.channelName = B["channel"]

                    self.MainCode.label_Title_YTP.setText(f'{self.YTP_title}')
                    self.MainCode.label_videoCount_YTP.setText(f'{self.YTP_VideoCount}')
                    self.MainCode.label_Channel_YTP.setText(f'{self.channelName}')
                    self.MainCode.label_PlayListViews_YTP.setText(f'{self.YTP_ViewCount:,}')
                    self.MainCode.label_Date_YTP.setText(f'{self.Uploaded_Date}')
                    
                    # Set list for thumbnail urls ...................................................................
                    for thumbs in B["thumbnails"]:
                        self.thumbnails.append(thumbs["url"])
                    # selecting right one out of all thumbnails ....................................................    
                    self.Thumbnail_To_Download = self.thumbnails[-1]
                    
                    # downloading video thumbnails .................
                    try:
                        response = requests.get(self.Thumbnail_To_Download)
                        with open("Thumbnail\Youtube_PlayList\YTP_Thumbnail.jpg", "wb") as thumbnail:
                            thumbnail.write(response.content)

                        self.MainCode.Youtube_Pthumbnail.setPixmap(QPixmap('Thumbnail\Youtube_PlayList\YTP_Thumbnail.jpg'))
                    # usef yt-dlp if 'request' not worked ...........
                    except:
                        Video_folder = r'Thumbnail\Youtube_PlayList'
                        ydl_opts = {'writethumbnail': True,
                                    'outtmpl': {'default': f'{Video_folder}/YoutubePlayListThumb.%(ext)s'},
                                    'skip_download': True, 'ignoreerrors': True, 'no_warnings': True
                                    }

                        with yt_dlp.YoutubeDL(ydl_opts) as ydl_YP:
                            ydl_YP.download(self.Thumbnail_To_Download)
                        try:
                            self.MainCode.Youtube_Pthumbnail.setPixmap(
                                QPixmap(r'Thumbnail\Youtube_Video\YoutubeVideoThumb'))
                        except:
                            self.MainCode.Youtube_Pthumbnail.setPixmap(QPixmap(r'Icons\Tumbs\minis.png'))

                except KeyError as key:
                    print(f"Error.......{key}...................")
                except:
                    print(f"Error..........................")
            // IF THE LINK IS NOT FROM A PLAYLIST ..........        
            else:
                print("Link is not of the Play List .........")
                self.MainCode.Youtube_Pthumbnail.setPixmap(QPixmap(r'Icons\Tumbs\LightingMQ.png'))
                self.MainCode.label_Pcomplete_YT_P.setText(
                    ".............. Added link is not valid .... Add valid Link to search ...................")
