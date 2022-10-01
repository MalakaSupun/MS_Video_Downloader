from PyQt5 import QtCore
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
import yt_dlp
import subprocess
import requests
import time
import json
import concurrent.futures


class Thread_ChecksUP(QThread):
    Playlist_details = QtCore.pyqtSignal(int)

    def __init__(self, parent):
        QThread.__init__(self, parent)
        self.MainCode = parent

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
        self.thumbnails = []
        self.Video_checked = 0

    def run(self):
        self.MainCode.progressBar_YT_V.setValue(0)
        self.MainCode.label_Pcomplete_YT_P.setText("................... Playlist Checking ...................")
        print("................... Playlist Checking ...................")
        self.The_link = self.MainCode.lineEdit_YTP_link.text()

        if self.The_link != '':
            print(f"Playlist URL : {self.The_link}")

            if self.MainCode.radioButton_UTV_AudioOnly.isChecked():
                self.Formats = 'bestaudio/best'
            else:
                self.Formats = 'bestvideo*+bestaudio/best'

            self.get_Video_info()
            self.Video_checked = 1

        else:
            print("Add Link to Download / Check")
            self.MainCode.label_Pcomplete_YT_P.setText(
                "................... Add Link to Download / Check ...................")
            self.MainCode.Youtube_Pthumbnail.setPixmap(QPixmap(r'Icons\Tumbs\LightingMQ.png'))

    def get_Video_info(self):
        # ,'quiet': True

        ydl_opts = {'format': self.Formats, 'no_warnings': True, 'ignoreerrors': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(self.The_link, download=False)
            A = json.dumps(ydl.sanitize_info(info), indent=2)
            B = json.loads(A)

            self.isPlayList = B["_type"]
            print(f"Your link is representing a : {self.isPlayList}")

            
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
                    
                    for thumbs in B["thumbnails"]:
                        self.thumbnails.append(thumbs["url"])
                    self.Thumbnail_To_Download = self.thumbnails[-1]
                    
                    try:
                        response = requests.get(self.Thumbnail_To_Download)
                        with open("Thumbnail\Youtube_PlayList\YTP_Thumbnail.jpg", "wb") as thumbnail:
                            thumbnail.write(response.content)

                        self.MainCode.Youtube_Pthumbnail.setPixmap(QPixmap('Thumbnail\Youtube_PlayList\YTP_Thumbnail.jpg'))

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
            else:
                print("Link is not of the Play List .........")
                self.MainCode.Youtube_Pthumbnail.setPixmap(QPixmap(r'Icons\Tumbs\LightingMQ.png'))
                self.MainCode.label_Pcomplete_YT_P.setText(
                    ".............. Added link is not valid .... Add valid Link to search ...................")
