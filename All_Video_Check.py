# Importing PyQt5........................
from PyQt5.QtCore import QThread, pyqtSignal   # For QThread and QtSignal.......
from PyQt5.QtGui import QPixmap                # For QPixmp ....................
# Video downloading package .............
import yt_dlp                                    # This is the most important module for app .....
# Importing json ........................
import json                                      # Using json for extract data from videos .....
# Requests module for thumbnail ........
import requests
# Time module for calculating time .....
import time                                      # Time module for operation.........
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
        self.thumbnails = []   # this is for store thumbnail linkz
        
        # Setting status of the application .........
        self.Video_checked = 0

def get_Video_info(self):
       
        ydl_opts = {'format': self.Formats, 'no_warnings': True, 'ignoreerrors': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(self.The_link, download=False)
            A = json.dumps(ydl.sanitize_info(info), indent=2)
            B = json.loads(A)

            self.isPlayList = B["_type"]
            print(f"Your link is representing a : {self.isPlayList}")

            # Need to be a playlist to execute this code ........
            if self.isPlayList == "playlist":
                try:
                    self.YTP_title = B["title"]                                      # Video title ....
                    self.YTP_VideoCount = B["playlist_count"]                        # Video count.....
                    self.YTP_ViewCount = B["view_count"]                             # View count .....
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
                        with open("Thumbnail\Youtube_PlayList\YTP_Thumbnail.jpg", "wb") as thumbnail:         # Path for png................
                            thumbnail.write(response.content)

                        self.MainCode.Youtube_Pthumbnail.setPixmap(QPixmap('Thumbnail\Youtube_PlayList\YTP_Thumbnail.jpg'))   # Path for png................
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
                            self.MainCode.Youtube_Pthumbnail.setPixmap(QPixmap(r'Icons\Tumbs\minis.png'))  # Path for png................

                except KeyError as key:
                    print(f"Error.......{key}...................")
                except:
                    print(f"Error..........................")
                
                      
            else:
                print("Link is not of the Play List .........")
                self.MainCode.Youtube_Pthumbnail.setPixmap(QPixmap(r'Icons\Tumbs\LightingMQ.png'))          # Path for png................
                self.MainCode.label_Pcomplete_YT_P.setText(
                    ".............. Added link is not valid .... Add valid Link to search ...................")
