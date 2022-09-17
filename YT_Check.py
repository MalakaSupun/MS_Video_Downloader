from PyQt5 import QtCore
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
import yt_dlp
import json
import requests
import time
import concurrent.futures

'''Formats = ['bestvideo*+bestaudio/best', 'bestaudio/best',
           'bestvideo[height<=1080]+bestaudio/best[height<=1080]', 'bestvideo[height<=720]+bestaudio/best[height<=720]',
           'bestvideo[height<=480]+bestaudio/best[height<=480]', 'bestvideo[height<=360]+bestaudio/best[height<=360]',
           'bestvideo[height<=244]+bestaudio/best[height<=244]', 'bestvideo[height<=144]+bestaudio/best[height<=144]']'''

Alw_Sub_Languages = ['en', 'si', 'ta']
lang = []
Auto_langs = []
Not_In_Direct_Sub = []
Not_In_Auto_Sub = []


class Thread_ChecksUV(QThread):
    countChanged = QtCore.pyqtSignal(int)

    def __init__(self, parent):
        QThread.__init__(self, parent)
        self.MainCode = parent

        self.Video_checked = 0
        self.V240p_Size = " "
        self.V360p_Size = " "
        self.V480p_Size = " "
        self.V720p_Size = " "
        self.V1080p_Size = " "
        self.Direct_Sub_Avalability = " "
        self.Video_Duration = " "
        self.YTV_ViewCount = 000000
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

    def run(self):
        self.MainCode.progressBar_YT_V.setValue(0)
        self.MainCode.label_Pcomplete_UTV.setText("................... Video Checking ...................")
        print("................... Video Checking ...................")

        S_Time = time.perf_counter()

        self.F_Requested = self.MainCode.comboBox_Quality_YV.currentIndex()
        link = self.MainCode.lineEdit_YTV_link.text()
        if link != '':
            self.The_link = link.replace('&', '"&"')
            print(self.The_link)
            if self.MainCode.radioButton_UTV_AudioOnly.isChecked():
                Formats = ['bestvideo*+bestaudio/best', 'bestaudio/best']
            else:
                Formats = ['bestvideo*+bestaudio/best',
                           'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
                           'bestvideo[height<=720]+bestaudio/best[height<=720]',
                           'bestvideo[height<=480]+bestaudio/best[height<=480]',
                           'bestvideo[height<=360]+bestaudio/best[height<=360]',
                           'bestvideo[height<=244]+bestaudio/best[height<=244]',
                           'bestvideo[height<=144]+bestaudio/best[height<=144]']

            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(self.get_Video_info, Formats)

            F_Time = time.perf_counter()
            self.Set_Lables()
            self.set_Selected_Video_Size()
            print(f'Execution Time : {round(F_Time - S_Time, 3)} s')

        else:
            print("Add Link to Download / Check")
            self.MainCode.label_Pcomplete_UTV.setText(
                "................... Add Link to Download / Check ...................")

    def Sub_langs(self, item):
        if item == 'en':
            ls = "English"
            return ls
        elif item == 'si':
            ld = "Sinhala"
            return ld
        elif item == 'ta':
            lz = "Tamil"
            return lz

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

    def Set_Lables(self):

        Video_title = self.YT_title
        Youtube_Channel = self.Yt_Channle
        View_Count = self.YTV_ViewCount
        Uploaded_Date = self.Uploded_Date
        Thumbnail_URL = self.Thumbnail_URL
        Video_Duration = self.Video_Duration

        # Sub titles of the videos.......................................
        # Direct_Sub_Availability = self.Direct_Sub_Avalability
        # Auto_Sub_Availability = self.Auto_Sub_Avalability

        Video_Best_Format = self.BestV_Format
        V_Size_Best = self.BestV_Size
        V_Size_1008p = self.V1080p_Size
        V_Size_720p = self.V720p_Size
        V_Size_480p = self.V480p_Size
        V_Size_360p = self.V360p_Size
        V_Size_240p = self.V240p_Size
        V_Size_144p = self.V144p_Size

        self.MainCode.label_Title_YTV.setText(f'Video Title : {Video_title}')
        self.MainCode.label_Views_YTV.setText(f'Video Views : {View_Count:,}')
        self.MainCode.label_Channel_YTV.setText(f'Channel : {Youtube_Channel}')
        self.MainCode.label_Duration_YTV.setText(f'Video Duration(H:M:S) : {Video_Duration} ')
        self.MainCode.label_Date_YTV.setText(f'Uploaded Date : {Uploaded_Date}')
        self.MainCode.label_Channel_YTV_BTV.setText(f'Best format available:  {Video_Best_Format} ')

        try:
            Direct_Sub_Availability = self.Direct_Sub_Avalability
            for a in Direct_Sub_Availability:
                if a != 'live_chat':
                    lang.append(a)
                elif a == 'live_chat':
                    raise KeyError

            # self.MainCode.label_Channel_YTV_BTV_Subs.setText(f'Subtitles : Not-Available')
            self.MainCode.radioButton_UTV_subs.setDisabled(False)
            print('\nDirect sub available..... ')
            print(f"Direct sub langs: {lang}")

            Available_Direct_Subs = [a for a in lang if self.Sub_langs(a)]
            print(f"Available direct sub langs: {Available_Direct_Subs}")
            if Available_Direct_Subs.__len__() == 0:
                print("No Direct Subtitles Available \n................... Key Error! ...................")
                raise KeyError
            if Available_Direct_Subs.__len__() != 0:
                en_c = Available_Direct_Subs.count('en')
                si_c = Available_Direct_Subs.count('si')
                ta_c = Available_Direct_Subs.count('ta')
                if en_c == 0:
                    Not_In_Direct_Sub.append("English")
                if si_c == 0:
                    Not_In_Direct_Sub.append("Sinhala")
                if ta_c == 0:
                    Not_In_Direct_Sub.append("Tamil")
                '''if en_c or si_c or ta_c == 0:
                    raise KeyError'''
                print(f"Sub Titles not in the direct subs : {Not_In_Direct_Sub}")

            Auto_Sub_Availability = self.Auto_Sub_Avalability
            for y in Auto_Sub_Availability:
                Auto_langs.append(y)
            print(f"Auto Sub Titles :{Auto_langs}")
            Available_Auto_Subs = [b for b in Auto_langs if self.Sub_langs(b)]
            print(f"Available direct sub langs: {Available_Auto_Subs}")
            self.MainCode.label_Channel_YTV_BTV_Subs.setText(f'Subtitles : Available')


        except KeyError:
            try:
                Auto_Sub_Availability = self.Auto_Sub_Avalability
                for y in Auto_Sub_Availability:
                    Auto_langs.append(y)
                print(f"All Available Auto Sub Titles :{Auto_langs}")

                Available_Auto_Subs = [b for b in Auto_langs if self.Sub_langs(b)]
                print(f"Available Auto sub langs: {Available_Auto_Subs}")

                if Available_Auto_Subs.__len__() == 0:
                    self.MainCode.label_Channel_YTV_BTV_Subs.setText(f'Subtitles : Not Available')
                    self.MainCode.radioButton_UTV_subs.setDisabled(True)
                else:
                    self.MainCode.label_Channel_YTV_BTV_Subs.setText(f'Subtitles : Available')
                    self.MainCode.radioButton_UTV_subs.setDisabled(False)
                    en_ca = Available_Auto_Subs.count('en')
                    si_ca = Available_Auto_Subs.count('si')
                    ta_ca = Available_Auto_Subs.count('ta')
                    if en_ca == 0:
                        Not_In_Auto_Sub.append("English")
                    if si_ca == 0:
                        Not_In_Auto_Sub.append("Sinhala")
                    if ta_ca == 0:
                        Not_In_Auto_Sub.append("Tamil")
                    print(f"Sub Titles not in the auto subs : {Not_In_Auto_Sub}")
            except:
                print("........No subtitles available for this video...........")
                self.MainCode.radioButton_UTV_subs.setDisabled(True)
                self.MainCode.label_Channel_YTV_BTV_Subs.setText(f'Subtitles : Not Available')

        except:
            print("........No subtitles available for this video...........")
            self.MainCode.radioButton_UTV_subs.setDisabled(True)
            self.MainCode.label_Channel_YTV_BTV_Subs.setText(f'Subtitles : Not Available')

        self.MainCode.comboBox_Quality_YV.clear()
        Q1s = [f' Best Audio & Video  < {V_Size_Best} MB >',
               f' 1080p                       < {V_Size_1008p} MB >',
               f' 720p                         < {V_Size_720p} MB >',
               f' 480p                         < {V_Size_480p} MB >',
               f' 360p                         < {V_Size_360p} MB >',
               f' 240p                         < {V_Size_240p} MB >',
               f' 144p                         < {V_Size_144p} MB >']

        self.MainCode.comboBox_Quality_YV.addItems(Q1s)
        self.MainCode.comboBox_Quality_YV.setCurrentIndex(self.F_Requested)

        try:
            # Thumbnail_Link = B["thumbnail"]
            response = requests.get(Thumbnail_URL)
            # name = "YTV_Thumbnail.jpg"
            with open("YTV_Thumbnail.jpg", "wb") as thumbnail:
                thumbnail.write(response.content)

            self.MainCode.Youtube_Vthumbnail.setPixmap(QPixmap('YTV_Thumbnail.jpg'))
        except:
            self.MainCode.Youtube_Vthumbnail.setPixmap(QPixmap('Icons/Thumbnail.png'))
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
