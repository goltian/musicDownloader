"""
Downloads a song by URL from youtube.
"""

import yt_dlp

def getUrl():
    f = open('urlForDownload.txt', 'r')
    videoUrl = f.readline()
    f.close()
    return videoUrl

def downloadMusic():
    """
    Downloads music on PC.
    Returns its path or None in case of error.
    """

    ydlOpts = {
    'format' : 'bestaudio/best',
    # For download forbidden music. Need Tor browser
    # 'proxy' : 'socks5://127.0.0.1:9150/',
    # Path and name for a song
    'outtmpl' : ('downloadedMusic\\' + '%(channel)s - %(title)s.%(ext)s'),
    # Webm to Mp3 convert
    'postprocessors' : [{
        'key' : 'FFmpegExtractAudio',
        'preferredcodec' : 'mp3',
        'preferredquality' : '192',
    }],
    'noplaylist' : True,
    }

    with yt_dlp.YoutubeDL(ydlOpts) as ydl:
        videoUrl = getUrl()
        info = ydl.extract_info(videoUrl)
        pathToTheSong = ydl.prepare_filename(info)
        pathToTheSong = pathToTheSong.replace('.webm', '.mp3')
        return pathToTheSong
