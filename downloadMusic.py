import yt_dlp
import os
import time
from contextlib import redirect_stdout 
from pydub import AudioSegment

class bcolors:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
os.system('color')

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

def main():
    with open('outputInfo.txt', 'w', encoding='utf-8') as f: 
        with redirect_stdout(f): 
            isDownloadComplete = downloadMusic()

    if isDownloadComplete:
        print(f"{bcolors.OKGREEN}Your song was downloaded successfuly")
        file_name = 'outputInfo.txt'
        f = open(file_name, 'r', encoding='utf-8')
        while True:
            pathToTheSong = f.readline()
            if "[download]" in pathToTheSong:
                break
        pathToTheSong = pathToTheSong[24:]
        pathToTheSong = pathToTheSong[:-5] + "mp3"
        f.close()

        try:
            song = AudioSegment.from_mp3(pathToTheSong)
            dbRoReduce = normaliseLoudness(song)
            if dbRoReduce > 0:
                song -= dbRoReduce
                song.export(pathToTheSong, "mp3")
            print(f"{bcolors.OKGREEN}Loudness is normal now")
            time.sleep(1)
        except Exception as ex:
            print(f"{bcolors.FAIL}Error: Problem with loudness")
            time.sleep(3)
    else:
        print(f"{bcolors.FAIL}Error: Your song was not downloaded")
        time.sleep(3)

main()
