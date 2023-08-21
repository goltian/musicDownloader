import win32gui, win32con
win32gui.ShowWindow(win32gui.GetForegroundWindow() , win32con.SW_HIDE)

import yt_dlp
import os
from pydub import AudioSegment
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot()
ax.axis([0, 10, 0, 10])
ax.axis('off')

def getUrl():
    f = open('urlForDownload.txt', 'r')
    video_url = f.readline()
    f.close()
    return video_url

def downloadMusic():
    isDownloadComplete = False

    ydl_opts = {
    'format' : 'bestaudio/best',
    # For download forbidden music. Need Tor browser
    #'proxy' : 'socks5://127.0.0.1:9150/',
    # Path and name for a song
    'outtmpl' : os.path.join('downloadedMusic', '%(channel)s - %(title)s.%(ext)s'),
    # Webm to Mp3 convert
    'postprocessors' : [{
        'key' : 'FFmpegExtractAudio',
        'preferredcodec' : 'mp3',
        'preferredquality' : '192',
    }],
    'noplaylist' : True,
    }

    video_url = getUrl()
    pathToTheSong = ""
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(video_url)
            pathToTheSong = ydl.prepare_filename(info)
            pathToTheSong = pathToTheSong.replace(".webm", ".mp3")
            isDownloadComplete = True
        except Exception:
            ax.text(0.05, 5, r'Error: Problem with download', fontsize=24, color="red")
            plt.show()

    return isDownloadComplete, pathToTheSong

def normaliseLoudness(song):
    CONST_DB_REDUCE_MULTIPLIER = 0.891229
    rms = song.rms
    if rms <= 5000:
        return 0

    dbToReduce = 0
    while rms > 5000:
        rms *= CONST_DB_REDUCE_MULTIPLIER
        dbToReduce += 1
    return (dbToReduce - 1)

def main():
    isDownloadComplete, pathToTheSong = downloadMusic()

    if isDownloadComplete:
        try:
            song = AudioSegment.from_mp3(pathToTheSong)
            dbRoReduce = normaliseLoudness(song)
            if dbRoReduce > 0:
                song -= dbRoReduce
                song.export(pathToTheSong, "mp3")
        except Exception:
            ax.text(0.2, 5, r'Error: Problem with loudness', fontsize=24, color="red")
            plt.show()

main()
