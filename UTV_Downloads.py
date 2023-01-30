# PyQt module for application...........
from PyQt5.QtCore import QThread, pyqtSignal             # Threading and signals.....
from PyQt5.QtGui import QPixmap                          # Import for showing thumbnail image.....
# The main module for the application............
import yt_dlp
# Importing json for extracting information......
import json
# Request module for getting thumbnails..........
import requests
# Time module for application...................
import time
# For python normal theadings.....
import concurrent.futures
# For notificaton sounds......
import winsound
# Importing video checking class...
from YT_Check import *
# plyer module for notifications
from plyer import notification

#All Downloading formats.............
Formats = ['bestvideo*+bestaudio/best', 'bestaudio/best',
           'bestvideo[height<=1080]+bestaudio/best[height<=1080]', 'bestvideo[height<=720]+bestaudio/best[height<=720]',
           'bestvideo[height<=480]+bestaudio/best[height<=480]', 'bestvideo[height<=360]+bestaudio/best[height<=360]',
           'bestvideo[height<=240]+bestaudio/best[height<=240]', 'bestvideo[height<=144]+bestaudio/best[height<=144]']


class Thread_DownloadUV(QtCore.QThread):
           
    # Signals for Ui updates.....       
    ProgressCount = QtCore.pyqtSignal(int)      # Progress Count.........
    DownloadSpeed = QtCore.pyqtSignal(str)      # Downloading speed......
    TimeRemains = QtCore.pyqtSignal(str)        # Remaining time ........
    Downloaded_So_Far = QtCore.pyqtSignal(str)  # Size of file that downloaded so far .......

    def __init__(self, parent):
        QThread.__init__(self, parent)
        self.MainCode = parent
           
        # method for class. ............
        self.YTV_Checks = Thread_ChecksUV(self)

        # Variables for app ...................
        self.Link = ''
        self.VideoFormat = ''
        self.Format_Requested = ''
        self.Video_folder = ''
        self.The_link = ''
        self.Requested_Sub_lang = ''
        self.is_running = True

    def run(self):
        self.VideoDownloaded = 0
        link = self.MainCode.lineEdit_YTV_link.text()    # Video Link .................................
        self.Link = link

        if link != '':
            self.The_link = link.replace('&', '"&"')
            self.MainCode.label_Pcomplete_UTV.setText("................... Downloading Started ...................")
        else:
            print("Enter a Link to download..........")

        self.Video_folder = self.MainCode.lineEdit_YTV_F.text()

        if self.MainCode.radioButton_UTV_AudioOnly.isChecked():
            if self.Video_folder != '':
                
                self.Format_Selection()
                self.Downloader()
                self.MainCode.label_Pcomplete_UTV.setText("................... Format Downloaded ...................")
                self.MainCode.progressBar_YT_V.setValue(0)
            else:
                self.MainCode.label_Pcomplete_UTV.setText("............. Add Location to Download  .............")

        else:
            if self.Video_folder != '':
                self.Format_Requested = self.MainCode.comboBox_Quality_YV.currentIndex()
                print(f'Requested Format :{self.Format_Requested}')
                self.Format_Selection()
                self.Downloader()
                self.MainCode.label_Pcomplete_UTV.setText("................... Video Downloaded ...................")
                self.MainCode.progressBar_YT_V.setValue(0)
                self.VideoDownloaded = 1
                self.Notifications()          # Make a notification.......   

            else:
                self.MainCode.label_Pcomplete_UTV.setText("............. Add Location to Download Video .............")
                self.Notifications()          # Make a notification.......   

    def SelectSubtitles(self):
        Lang_Text = self.MainCode.comboBox_Quality_Sub_YV.currentText()
        if Lang_Text == "Tamil":
            self.Requested_Sub_lang = 'ta'
        elif Lang_Text == "Sinhala":
            self.Requested_Sub_lang = 'si'
        elif Lang_Text == "English":
            self.Requested_Sub_lang = 'en'
        elif Lang_Text == "English-Auto-Gen":
            self.Requested_Sub_lang = 'en'
        elif Lang_Text == "Sinhala-Auto-Gen":
            self.Requested_Sub_lang = 'si'
        elif Lang_Text == "Tamil-Auto-Gen":
            self.Requested_Sub_lang = 'ta'

    def Format_Selection(self):
        if self.MainCode.radioButton_UTV_AudioOnly.isChecked():
            self.VideoFormat = 'bestaudio/best'
        else:
            if self.Format_Requested == 0:
                self.VideoFormat = 'bestvideo*+bestaudio/best'
            if self.Format_Requested == 1:
                self.VideoFormat = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'
            if self.Format_Requested == 2:
                self.VideoFormat = 'bestvideo[height<=720]+bestaudio/best[height<=720]'
            if self.Format_Requested == 3:
                self.VideoFormat = 'bestvideo[height<=480]+bestaudio/best[height<=480]'
            if self.Format_Requested == 4:
                self.VideoFormat = 'bestvideo[height<=360]+bestaudio/best[height<=360]'
            if self.Format_Requested == 5:
                self.VideoFormat = 'bestvideo[height<=240]+bestaudio/best[height<=240]'
            if self.Format_Requested == 6:
                self.VideoFormat = 'bestvideo[height<=144]+bestaudio/best[height<=144]'

    def Downloader(self):

        print(self.VideoFormat)
        if self.MainCode.radioButton_UTV_subs.isChecked():
            self.SelectSubtitles()
            print(f"Selected Sub Language : {self.Requested_Sub_lang}")

        if not self.MainCode.radioButton_YTV_subM.isChecked(): # 
            print("Download sub + video")
            if self.VideoFormat != 'bestaudio/best': # best video download .....

                ydl_opts = {
                    'noplaylist': True,  
                    'format_sort': {'ext': True},
                    'ignoreerrors': True,  'no_warnings': True,
                    'outtmpl': {'default': f'{self.Video_folder}/%(title)s.%(ext)s'},
                    'writesubtitles': True,
                    'writeautomaticsub': True, 'subtitleslangs': {self.Requested_Sub_lang},
                    'format': self.VideoFormat, 'ext': 'mp4',
                    'progress_hooks': [self.My_Progress_hook],
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download(self.The_link)

            elif self.VideoFormat == 'bestaudio/best':

                ydl_opts = {
                    'noplaylist': True,
                    'ignoreerrors': True,  'no_warnings': True,
                    'format_sort': {'ext': True},
                    'format': 'bestaudio/best',
                    'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', }],
                    'outtmpl': {'default': f'{self.Video_folder}/%(title)s.%(ext)s'},
                    'progress_hooks': [self.My_Progress_hook],
                    'postprocessor_hooks': [self.My_Progress_hook_Audios],
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download(self.The_link)

        elif self.MainCode.radioButton_YTV_subM.isChecked():
            print("Download sub + video")
            if self.VideoFormat != 'bestaudio/best':

                ydl_opts = {
                    'skip_download': True,
                    'noplaylist': True,
                    'format_sort': {'ext': True},
                    #'quiet': True,
                    'ignoreerrors': True,  'no_warnings': True,
                    'outtmpl': {'default': f'{self.Video_folder}/%(title)s.%(ext)s'},
                    'writesubtitles': True,
                    'writeautomaticsub': True, 'subtitleslangs': {self.Requested_Sub_lang},
                    'format': self.VideoFormat,
                    'ext': 'mp4',
                    'progress_hooks': [self.My_Progress_hook],
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download(self.The_link)

            elif self.VideoFormat == 'bestaudio/best':

                ydl_opts = {
                    'skip_download': True,
                    'noplaylist': True,
                    'format_sort': {'ext': True},
                    'writesubtitles': True,
                    'writeautomaticsub': True, 'subtitleslangs': {self.Requested_Sub_lang},
                    'ignoreerrors': True,  'no_warnings': True,
                    #'quiet': True,
                    'outtmpl': {'default': f'{self.Video_folder}/%(title)s.%(ext)s'},
                    'progress_hooks': [self.My_Progress_hook],

                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download(self.The_link)

    def My_Progress_hook_Audios(self, d):

        if d['status'] == 'finished':
            print('\n................. Making MP3 Finished..................')
        elif d['status'] == "processing":
            print('.........Audio Processing..........Making MP3...........')
        elif d['status'] == "started":
            print('.......... Audio string to process_Making MP3 ..........')

    def My_Progress_hook(self, d):

        if d['status'] == 'finished':
            print('\n.......................................Finished.................................................')
            self.MainCode.label_DSpeed_YTV_2.setText('0')
            self.MainCode.label_DBytes_YTV.setText("0")
        elif d['status'] == "downloading":

            Speed = d['_speed_str']
            self.DownloadSpeed.emit(Speed)                   # Send through signal......

            per_ct = d['_percent_str']
            split = per_ct.split('%')
            pct = split[0]
            percentage = float(pct)

            cnt = round(percentage)
            self.ProgressCount.emit(cnt)                     # Send through signal......

            TimeRemaining = d['_eta_str']
            self.TimeRemains.emit(TimeRemaining)

            Data_Downloaded = d['_downloaded_bytes_str']
            self.Downloaded_So_Far.emit(Data_Downloaded)     # Send through signal......

        if d['status'] == "Error":
           
            print("\n..........Error..........Error..........Error..........\n")
            winsound.PlaySound("Sounds/Error.mp3", winsound.SND_FILENAME)

    def set_current_Size(self):
        if Thread_ChecksUV.Video_checked == 1:
            Index = self.MainCode.comboBox_Quality_YV.currentIndex()
            if Index == 0:
                self.MainCode.label_Views_Selected_YTV_Size.setText(
                    f'Size of video selected : {Thread_ChecksUV.BestV_Size}  MB')
            if Index == 1:
                self.MainCode.label_Views_Selected_YTV_Size.setText(
                    f'Size of video selected : {Thread_ChecksUV.V1080p_Size}  MB')
            if Index == 2:
                self.MainCode.label_Views_Selected_YTV_Size.setText(
                    f'Size of video selected : {Thread_ChecksUV.V720p_Size}  MB')
            if Index == 3:
                self.MainCode.label_Views_Selected_YTV_Size.setText(
                    f'Size of video selected : {Thread_ChecksUV.V480p_Size}  MB')
            if Index == 4:
                self.MainCode.label_Views_Selected_YTV_Size.setText(
                    f'Size of video selected : {Thread_ChecksUV.V360p_Size}  MB')
            if Index == 5:
                self.MainCode.label_Views_Selected_YTV_Size.setText(
                    f'Size of video selected : {Thread_ChecksUV.V240p_Size}  MB')
            if Index == 6:
                self.MainCode.label_Views_Selected_YTV_Size.setText(
                    f'Size of video selected : {Thread_ChecksUV.V144p_Size}  MB')

           
    #  Set up notifications for downloader...........      
    def Notifications(self):
        if self.VideoDownloaded == 1:
                notification.notify(            
                title="YouTube Video Download",                                                           # Title of the notification.......
                message=" Video Downloaded !!! ",                                                         # Message.............
                app_icon="E:\other\Python\Projects\Youtube_Downloader_Yt_dlp\Icons\Tumbs\Main_icon.ico",  # Icon path ..........
                timeout=10,
                app_name="Ms Video Download",                                                             # App name........               
                ticker="Video Download",                                                                  # Tikker ..............
                toast=True
            )
        elif self.VideoDownloaded == 0:
            if self.Video_folder or self.Link == '':
                    notification.notify(
                    title="YouTube Not Video Download",                                                       # Title of the notification.......                                                                                     
                    message=" Add Location and Link to Download Video !!! ",                                  # Message.............
                    app_icon="E:\other\Python\Projects\Youtube_Downloader_Yt_dlp\Icons\Tumbs\Main_icon.ico",  # Icon Path........
                    app_name="Ms Video Download",                                                             
                    timeout=10,                                                                               # Tikker ..............
                    ticker="Video Download",
                    toast=True
                )

