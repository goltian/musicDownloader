import win32gui, win32con
win32gui.ShowWindow(win32gui.GetForegroundWindow() , win32con.SW_HIDE)

import yt_dlp
import os
from pydub import AudioSegment

import matplotlib.pyplot as plt
def printError(errorMessage):
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.axis([0, 10, 0, 10])
    ax.axis('off')
    ax.text(0, 5, errorMessage, fontsize=24, color="red")
    plt.show()

def getUrl():
    f = open('urlForDownload.txt', 'r')
    videoUrl = f.readline()
    f.close()
    return videoUrl

def downloadMusic():
    isDownloadComplete = False

    ydlOpts = {
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

    videoUrl = getUrl()
    pathToTheSong = ""
    with yt_dlp.YoutubeDL(ydlOpts) as ydl:
        try:
            info = ydl.extract_info(videoUrl)
            pathToTheSong = ydl.prepare_filename(info)
            pathToTheSong = pathToTheSong.replace(".webm", ".mp3")
            isDownloadComplete = True
        except Exception:
            printError("Error: Problem with download")

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
            printError("Error: Problem with loudness")

main()
