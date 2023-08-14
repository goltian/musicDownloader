from __future__ import unicode_literals
import yt_dlp
import os
import time

ydl_opts = {
    'format': 'bestaudio/best',

    # For download forbidden music. Need Tor browser
    #'proxy': "socks5://127.0.0.1:9150/",

    # Path and name for a song
    'outtmpl': os.path.join("downloadedMusic", '%(channel)s - %(title)s.%(ext)s'),

    # Webm to Mp3 convert
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

# Open url file
f = open('urlForDownload.txt','r')
video_url = f.readline()
f.close()

# The url needed to be youtube url
if "https://www.youtube.com/watch" in video_url:

    # The url needed not to be playlist url
    startOfPlaylist = video_url.find("&list")
    if startOfPlaylist != -1:
        video_url = video_url[:startOfPlaylist]

    tryToDownload = True
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        while tryToDownload:
            try:
                ydl.download([video_url])
                break
            except Exception as ex:
                if not "Error 403" in ex.args[0]:
                    tryToDownload = False
                    file_name = "forbiddenUrls.txt"
                    f = open(file_name, 'a')
                    f.write(str(video_url))
                    f.write('\n')
                    f.close()
                    print("Error. Video was not downloaded")
                    time.sleep(3)
else:
    print("It's not a youtube video")
    time.sleep(3)
