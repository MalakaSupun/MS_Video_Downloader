# PyQt5 libraries used ........
from PyQt5 import QtCore
from PyQt5.QtCore import QThread, pyqtSignal     # Signals and threads for UI .......................
from PyQt5.QtGui import QPixmap
# Downloading module ..................
import yt_dlp                                    # this is the most important module for app .......
# Json for information gathering.......
import json
# For Thumbnail downloading ...........
import requests
# Importanting time package ..........
import time
# For file managements ...............
import os
# For executive threads ..............
import concurrent.futures

# Lists for operations................
lang = []
Auto_langs = []
# Subtitles that need to download......
Alw_Sub_Languages = ['en', 'si', 'ta']
# Available auto subs .................
Auto_Sub_Langs = []
# Not Available direct subs ...........
Not_In_Direct_Sub = []
# Not Available auto subs ........... 
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

    def run(self):
        self.ClearLists()
        self.MainCode.progressBar_YT_V.setValue(0)
        self.MainCode.label_Pcomplete_UTV.setText("................... Video Checking ...................")
        print("................... Video Checking ...................")

        S_Time = time.perf_counter()         # Starting time...........
        self.Set_Default_Labels()            # Update all labels........

        self.F_Requested = self.MainCode.comboBox_Quality_YV.currentIndex()  # extracting qulity from UI...................
        link = self.MainCode.lineEdit_YTV_link.text()                        # extracting link from UI...................
        
        if link != '':
            self.The_link = link.replace('&', '"&"')
            print(self.The_link)
            if self.MainCode.radioButton_UTV_AudioOnly.isChecked():
                Formats = ['bestvideo*+bestaudio/best', 'bestaudio/best']
            else:
                Formats = ['bestvideo*+bestaudio/best',
                           'bestvideo[height<=1080]+bestaudio/best[height<=1080]',     # 1080p
                           'bestvideo[height<=720]+bestaudio/best[height<=720]',       # 720p
                           'bestvideo[height<=480]+bestaudio/best[height<=480]',       # 480p
                           'bestvideo[height<=360]+bestaudio/best[height<=360]',       # 360p
                           'bestvideo[height<=244]+bestaudio/best[height<=244]',       # 244p
                           'bestvideo[height<=144]+bestaudio/best[height<=144]']       # 144p

            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(self.get_Video_info, Formats)

            F_Time = time.perf_counter()
            self.Set_Lables()                                                          # Setup labs....
            self.set_Selected_Video_Size()                                             # Set selected video size.....
            print(f'Execution Time : {round(F_Time - S_Time, 3)} s')
            self.Video_checked = 1
            self.ClearLists()                                                          # Clear all lists.........

        else:
            print("Add Link to Download / Check")
            self.MainCode.label_Pcomplete_UTV.setText(
                "................... Add Link to Download / Check ...................")

    # Separate subtitle languages......        
    def Sub_langs(self, item):
        if item == 'en':                 # Englis subs......
            return 'en'
        elif item == 'si':               # Sinhala subs ....
            return 'en'
        elif item == 'ta':               # Tamil subs.......
            return 'en'

    def get_Video_info(self, VideoFormat):
        # 'quiet': True,
        ydl_opts = {'format': VideoFormat, 'noplaylist': True, 'ignoreerrors': True, 'no_warnings': True, }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(self.The_link, download=False)

            A = json.dumps(ydl.sanitize_info(info), indent=2)
            B = json.loads(A)

            if VideoFormat == 'bestaudio/best':
                self.Audio_Format = B["format_note"]
                self.Audio_Size = round(int(B["filesize"]) / 1048576, 2)

            if VideoFormat == 'bestvideo*+bestaudio/best':
                try:
                    self.BestV_Format = B["format_note"]
                    self.BestV_Size = round(int(B["filesize_approx"]) / (1024 * 1024), 2)

                    self.YT_title = B["title"]
                    self.Yt_Channle = B["channel"]
                    self.YTV_ViewCount = B["view_count"]
                    Date = B["upload_date"]
                    self.Uploded_Date = f'{Date[0]}{Date[1]}{Date[2]}{Date[3]}/{Date[4]}{Date[5]}/{Date[6]}{Date[7]}'
                    self.Thumbnail_URL = B["thumbnail"]
                    self.Video_Duration = B["duration_string"]
                    self.Thumbnail_Link = B["thumbnail"]
                    self.Direct_Sub_Avalability = B["subtitles"]
                    self.Auto_Sub_Avalability = B["automatic_captions"]
                except KeyError:
                    try:
                        self.Auto_Sub_Avalability = B["automatic_captions"]
                    except KeyError:
                        print("No Any Subs")

            if VideoFormat == 'bestvideo[height<=1080]+bestaudio/best[height<=1080]':
                self.V1080p_Size = round(int(B["filesize_approx"]) / (1024 * 1024), 2)
            if VideoFormat == 'bestvideo[height<=720]+bestaudio/best[height<=720]':
                self.V720p_Size = round(int(B["filesize_approx"]) / (1024 * 1024), 2)
            if VideoFormat == 'bestvideo[height<=480]+bestaudio/best[height<=480]':
                self.V480p_Size = round(int(B["filesize_approx"]) / (1024 * 1024), 2)
            if VideoFormat == 'bestvideo[height<=360]+bestaudio/best[height<=360]':
                self.V360p_Size = round(int(B["filesize_approx"]) / (1024 * 1024), 2)
            if VideoFormat == 'bestvideo[height<=244]+bestaudio/best[height<=244]':
                self.V240p_Size = round(int(B["filesize_approx"]) / (1024 * 1024), 2)
            if VideoFormat == 'bestvideo[height<=144]+bestaudio/best[height<=144]':
                self.V144p_Size = round(int(B["filesize_approx"]) / (1024 * 1024), 2)
                
    # Clear all the lists for re-checking ..............
    def ClearLists(self):
        lang.clear()
        Auto_langs.clear()
        Auto_Sub_Langs.clear()
        self.Filtered_Direct_Subs.clear()
        self.Filtered_Auto_Subs.clear()
        self.Available_Subs.clear()
        self.Commands_for_subs.clear()

    def Set_Lables(self):
        self.ClearLists()                    # Clear list for new labels .......................
        Video_title = self.YT_title
        Youtube_Channel = self.Yt_Channle
        View_Count = self.YTV_ViewCount
        Uploaded_Date = self.Uploded_Date
        Thumbnail_URL = self.Thumbnail_URL
        Video_Duration = self.Video_Duration

        Video_Best_Format = self.BestV_Format
        V_Size_Best = self.BestV_Size
        V_Size_1008p = self.V1080p_Size
        V_Size_720p = self.V720p_Size
        V_Size_480p = self.V480p_Size
        V_Size_360p = self.V360p_Size
        V_Size_240p = self.V240p_Size
        V_Size_144p = self.V144p_Size

        # Try to download thumbnail by Request module ...............
        try:
            thumbstT = time.perf_counter()
            # Thumbnail_Link = B["thumbnail"]
            response = requests.get(Thumbnail_URL)
            # name = "YTV_Thumbnail.jpg"
            with open("YTV_Thumbnail.jpg", "wb") as thumbnail:
                thumbnail.write(response.content)

            self.MainCode.Youtube_Vthumbnail.setPixmap(QPixmap('YTV_Thumbnail.jpg'))
            thumbEdT = time.perf_counter()
            print(round(thumbEdT - thumbstT, 3))  # 0.443s
          
        # Downloading thumbnail using yt-dlp ..............................
        except:
           
            try:
                # Remove all previous thumbnails......
                try:
                    os.remove(
                        r'E:\other\Python\Projects\Youtube_Downloader_Yt_dlp\Thumbnail\Youtube_Video\YoutubeVideoThumb.jpg')
                    os.remove(
                        r'E:\other\Python\Projects\Youtube_Downloader_Yt_dlp\Thumbnail\Youtube_Video\YoutubeVideoThumb.webp')
                except:
                    os.remove(
                        r'E:\other\Python\Projects\Youtube_Downloader_Yt_dlp\Thumbnail\Youtube_Video\YoutubeVideoThumb.webp')
            except:
                print("........ No previous thumbnail images ........")

            # 17.122s
            Video_folder = r'Thumbnail\Youtube_Video'
            ydl_opts = {'writethumbnail': True,
                        'noplaylist': True,
                        'outtmpl': {'default': f'{Video_folder}/YoutubeVideoThumb.%(ext)s'},
                        'skip_download': True, 'ignoreerrors': True, 'no_warnings': True
                        }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download(self.The_link)
            try:
                self.MainCode.Youtube_Vthumbnail.setPixmap(QPixmap(r'Thumbnail\Youtube_Video\YoutubeVideoThumb'))
            except:
                self.MainCode.Youtube_Vthumbnail.setPixmap(QPixmap(r'Icons\Tumbs\minis.png'))

        self.MainCode.label_Title_YTV.setText(f'{Video_title}')
        self.MainCode.label_Views_YTV.setText(f'{View_Count:,}')
        self.MainCode.label_Channel_YTV.setText(f'{Youtube_Channel}')
        self.MainCode.label_Duration_YTV.setText(f'{Video_Duration}')
        self.MainCode.label_Date_YTV.setText(f'{Uploaded_Date}')
        self.MainCode.label_Channel_YTV_BTV.setText(f'{Video_Best_Format}')

        try:
            Direct_Sub_Availability = self.Direct_Sub_Avalability
            for a in Direct_Sub_Availability:
                if a != 'live_chat':
                    lang.append(a)
                elif a == 'live_chat':
                    raise KeyError

            self.MainCode.radioButton_UTV_subs.setDisabled(False)
            print(f"Direct sub langs: {lang}")

            self.Filtered_Direct_Subs = [a for a in lang if self.Sub_langs(a)]

            print(f"Available direct sub langs: {self.Filtered_Direct_Subs}")
            if self.Filtered_Direct_Subs.__len__() == 0:
                print("No Direct Subtitles Available \n................... Key Error! ...................")
                raise KeyError
            if self.Filtered_Direct_Subs.__len__() != 0:

                for i in self.Filtered_Direct_Subs:
                    if i == 'en':
                        self.Available_Subs.append("English")
                    elif i == 'si':
                        self.Available_Subs.append("Sinhala")
                    elif i == 'ta':
                        self.Available_Subs.append("Tamil")
            self.Commands_for_subs = self.Filtered_Direct_Subs.copy()

            if len(self.Filtered_Direct_Subs) != 3:
                Auto_Sub_Availability = self.Auto_Sub_Avalability
                for y in Auto_Sub_Availability:
                    Auto_Sub_Langs.append(y)

                self.Filtered_Auto_Subs = [a for a in Auto_Sub_Langs if self.Sub_langs(a)]
                print(f"Filtered Auto Subs : {self.Filtered_Auto_Subs}")
                self.Commands_for_subs.extend(self.Filtered_Auto_Subs.copy())
                for i in self.Filtered_Auto_Subs:
                    if i == 'en':
                        self.Available_Subs.append("English-Auto-Gen")
                    elif i == 'si':
                        self.Available_Subs.append("Sinhala-Auto-Gen")
                    elif i == 'ta':
                        self.Available_Subs.append("Tamil-Auto-Gen")

            self.MainCode.label_Channel_YTV_BTV_Subs.setText(f'Available')
            print(f'Available Subs : {self.Available_Subs}')
            print(f"Commands For Available Subs : {self.Commands_for_subs}")

        except KeyError:
            try:
                Auto_Sub_Availability = self.Auto_Sub_Avalability
                for y in Auto_Sub_Availability:
                    Auto_langs.append(y)

                print(f"All Available Auto Sub Titles :{Auto_langs}")

                self.Filtered_Auto_Subs = [b for b in Auto_langs if self.Sub_langs(b)]
                print(f"Available Auto sub langs: {self.Filtered_Auto_Subs}")

                self.Commands_for_subs.extend(self.Filtered_Auto_Subs.copy())

                if self.Filtered_Auto_Subs.__len__() == 0:
                    self.MainCode.label_Channel_YTV_BTV_Subs.setText(f' Not Available')
                    self.MainCode.radioButton_UTV_subs.setDisabled(True)
                else:
                    for i in self.Filtered_Auto_Subs:
                        if i == 'en':
                            self.Available_Subs.append("English-Auto-Gen")
                        elif i == 'si':
                            self.Available_Subs.append("Sinhala-Auto-Gen")
                        elif i == 'ta':
                            self.Available_Subs.append("Tamil-Auto-Gen")

                    self.MainCode.label_Channel_YTV_BTV_Subs.setText(f' Available')
                    self.MainCode.radioButton_UTV_subs.setDisabled(False)
                    print(f'Available Subs : {self.Available_Subs}')
                    print(f"Commands For Available Subs : {self.Commands_for_subs}")
            except:
                print("........No subtitles available for this video...........")
                self.MainCode.radioButton_UTV_subs.setDisabled(True)
                self.MainCode.label_Channel_YTV_BTV_Subs.setText(f' Not Available')

        except:
            print("........No subtitles available for this video...........")
            self.MainCode.radioButton_UTV_subs.setDisabled(True)
            self.MainCode.label_Channel_YTV_BTV_Subs.setText(f' Not Available')

        self.MainCode.comboBox_Quality_YV.clear()
        Q1s = [f' Best Audio & Video  < {V_Size_Best} MB >',
               f' 1080p                       < {V_Size_1008p} MB >',
               f' 720p                         < {V_Size_720p} MB >',
               f' 480p                         < {V_Size_480p} MB >',
               f' 360p                         < {V_Size_360p} MB >',
               f' 240p                         < {V_Size_240p} MB >',
               f' 144p                         < {V_Size_144p} MB >']

        self.MainCode.comboBox_Quality_YV.addItems(Q1s)

        self.MainCode.comboBox_Quality_Sub_YV.clear()
        self.MainCode.comboBox_Quality_Sub_YV.addItems(self.Available_Subs)

        self.MainCode.comboBox_Quality_YV.setCurrentIndex(self.F_Requested)

        # print(B["requested_subtitles"])

        self.MainCode.label_Pcomplete_UTV.setText("................... Video Checked ...................")
        # F_Time = time.perf_counter()
        self.Video_checked = 1

    def set_Selected_Video_Size(self):
        # Thread_DownloadUV.F_Requested = self.MainCode.comboBox_Quality_YV.currentIndex()
        if self.MainCode.radioButton_UTV_AudioOnly.isChecked():
            self.MainCode.label_Views_Selected_YTV_Size.setText(f'Size of Audio : {self.Audio_Size}  MB')
        else:
            if self.F_Requested == 0:
                self.MainCode.label_Views_Selected_YTV_Size.setText(
                    f'Size of video selected : {self.BestV_Size}  MB')
            if self.F_Requested == 1:
                self.MainCode.label_Views_Selected_YTV_Size.setText(
                    f'Size of video selected : {self.V1080p_Size}  MB')
            if self.F_Requested == 2:
                self.MainCode.label_Views_Selected_YTV_Size.setText(
                    f'Size of video selected : {self.V720p_Size}  MB')
            if self.F_Requested == 3:
                self.MainCode.label_Views_Selected_YTV_Size.setText(
                    f'Size of video selected : {self.V480p_Size}  MB')
            if self.F_Requested == 4:
                self.MainCode.label_Views_Selected_YTV_Size.setText(
                    f'Size of video selected : {self.V360p_Size}  MB')
            if self.F_Requested == 5:
                self.MainCode.label_Views_Selected_YTV_Size.setText(
                    f'Size of video selected : {self.V240p_Size}  MB')
            if self.F_Requested == 6:
                self.MainCode.label_Views_Selected_YTV_Size.setText(
                    f'Size of video selected : {self.V144p_Size}  MB')
    # Default labels for application .................................
    def Set_Default_Labels(self):
        self.MainCode.label_Title_YTV.setText('')
        self.MainCode.label_Views_YTV.setText('')
        self.MainCode.label_Channel_YTV.setText('')
        self.MainCode.label_Duration_YTV.setText('')
        self.MainCode.label_Date_YTV.setText('')
        self.MainCode.label_Channel_YTV_BTV_Subs.setText('')
        self.MainCode.label_Channel_YTV_BTV.setText('')
        self.MainCode.label_DBytes_YTV.setText("0 KB")
        self.MainCode.label_DSpeed_YTV_2.setText('0 MiB/s')
        self.MainCode.label_RTime_YTV_2.setText('00:00:00')

