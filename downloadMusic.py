import yt_dlp
import os
import time
from contextlib import redirect_stdout 
from pydub import AudioSegment

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

    # The url needed to be youtube url
    if 'https://www.youtube.com/watch' in video_url:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([video_url])
                isDownloadComplete = True
            except Exception as ex:
                file_name = 'forbiddenUrls.txt'
                f = open(file_name, 'a')
                f.write(str(video_url))
                f.write('\n')
                f.close()
                time.sleep(3)

    return isDownloadComplete

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

with open('outputInfo.txt', 'w') as f: 
    with redirect_stdout(f): 
        isDownloadComplete = downloadMusic()

if isDownloadComplete:
    file_name = 'outputInfo.txt'
    f = open(file_name, 'r')
    while True:
        pathToTheSong = f.readline()
        if "[download]" in pathToTheSong:
            break
    pathToTheSong = pathToTheSong[24:]
    pathToTheSong = pathToTheSong[:-5] + "mp3"
    f.close()

    song = AudioSegment.from_mp3(pathToTheSong)
    dbRoReduce = normaliseLoudness(song)
    song -= dbRoReduce
    song.export(pathToTheSong, "mp3")

    print("Your song was downloaded successfuly")
    time.sleep(1)
else:
    print("Error. Your song was not downloaded")
    time.sleep(3)