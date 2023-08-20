import yt_dlp
import os
from contextlib import redirect_stdout 
from pydub import AudioSegment
import matplotlib.pyplot as plt


fig = plt.figure()
ax = fig.add_subplot()
fig.subplots_adjust(top=0.85)
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
        except Exception as ex:
            ax.text(0, 5, r'Error: Problem with loudness', fontsize=24, color="red")
            plt.show()
    else:
        ax.text(0, 5, r'Error: Your song was not downloaded', fontsize=18, color="red")
        plt.show()

main()
