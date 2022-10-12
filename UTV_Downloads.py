# Used pyQt5 packages ......................
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap

# Used video downloder package  ............
import yt_dlp
import json
import requests
import time
import concurrent.futures
import winsound
from YT_Check import *

Formats = ['bestvideo*+bestaudio/best', 'bestaudio/best',
           'bestvideo[height<=1080]+bestaudio/best[height<=1080]', 'bestvideo[height<=720]+bestaudio/best[height<=720]',
           'bestvideo[height<=480]+bestaudio/best[height<=480]', 'bestvideo[height<=360]+bestaudio/best[height<=360]',
           'bestvideo[height<=240]+bestaudio/best[height<=240]', 'bestvideo[height<=144]+bestaudio/best[height<=144]']


class Thread_DownloadUV(QtCore.QThread):
    ProgressCount = QtCore.pyqtSignal(int)
    DownloadSpeed = QtCore.pyqtSignal(str)
    TimeRemains = QtCore.pyqtSignal(str)
    Downloaded_So_Far = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        QThread.__init__(self, parent)
        self.MainCode = parent
        self.VideoFormat = None
        self.Format_Requested = None
        self.Video_folder = None
        self.The_link = None

        self.Requested_Sub_lang = ''

        self.is_running = True

        self.YTV_Checks = Thread_ChecksUV(self)
        # print('processing..... Downloader Thread......')

        langss = self.YTV_Checks.Commands_for_subs
        print(f"Sub Coms : {langss}")

        x = self.MainCode.comboBox_Quality_Sub_YV.currentIndex()
        print(x)

    def run(self):

        cnt = 0
        link = self.MainCode.lineEdit_YTV_link.text()
        if link != '':
            self.The_link = link.replace('&', '"&"')
            #print(self.The_link)
            self.MainCode.label_Pcomplete_UTV.setText("................... Downloading Started ...................")
        else:
            print("Enter a Link to download..........")

        self.Video_folder = self.MainCode.lineEdit_YTV_F.text()
        #print(f'Downloading Location : "{self.Video_folder}"')

        if self.MainCode.radioButton_UTV_AudioOnly.isChecked():
            if self.Video_folder != '':
                #print("Audio Only")
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

            else:
                self.MainCode.label_Pcomplete_UTV.setText("............. Add Location to Download Video .............")
                """while True:
                    cnt += 1
                    if cnt < 100:
                        time.sleep(0.01)
                        self.ProgressCount.emit(cnt)
                        print(cnt)
                    elif cnt == 100:
                        self.ProgressCount.emit(cnt)
                        cnt = 0"""

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


        if self.VideoFormat != 'bestaudio/best':
            ydl_opts = {

                'noplaylist': True, 'no_warnings': True,
                #'ignoreerrors': True, 'quiet': True,
                'outtmpl': {'default': f'{self.Video_folder}/%(title)s.%(ext)s'},
                'format': self.VideoFormat, 'ext': 'mp4/webm',
                'progress_hooks': [self.My_Progress_hook],
                'writesubtitles': True,
                'writeautomaticsub': True, 'subtitleslangs': {self.Requested_Sub_lang},
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download(self.The_link)

        elif self.VideoFormat == 'bestaudio/best':
            ydl_opts = {'format': 'bestaudio/best',
                        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', }],
                        'outtmpl': {'default': f'{self.Video_folder}/%(title)s.%(ext)s'},
                        'progress_hooks': [self.My_Progress_hook],
                        'postprocessor_hooks': [self.My_Progress_hook_Audios],

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

            #print(f"downloaded so far :- {d['_downloaded_bytes_str']}")
            #print(f"status :- {d['status']}")

            Speed = d['_speed_str']
            self.DownloadSpeed.emit(Speed)

            per_ct = d['_percent_str']
            split = per_ct.split('%')
            pct = split[0]
            percentage = float(pct)

            cnt = round(percentage)
            self.ProgressCount.emit(cnt)

            TimeRemaining = d['_eta_str']
            self.TimeRemains.emit(TimeRemaining)

            Data_Downloaded = d['_downloaded_bytes_str']
            self.Downloaded_So_Far.emit(Data_Downloaded)

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
