try:
    import win32gui, win32con
    win32gui.ShowWindow(win32gui.GetForegroundWindow() , win32con.SW_HIDE)
    import yt_dlp
    from pydub import AudioSegment

    def getUrl():
        f = open('urlForDownload.txt', 'r')
        videoUrl = f.readline()
        f.close()
        return videoUrl

    def downloadMusic():
        ydlOpts = {
        'format' : 'bestaudio/best',
        # For download forbidden music. Need Tor browser
        #'proxy' : 'socks5://127.0.0.1:9150/',
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

        isDownloadComplete = False
        pathToTheSong = ''
        with yt_dlp.YoutubeDL(ydlOpts) as ydl:
            videoUrl = getUrl()
            info = ydl.extract_info(videoUrl)
            pathToTheSong = ydl.prepare_filename(info)
            pathToTheSong = pathToTheSong.replace('.webm', '.mp3')
            isDownloadComplete = True
        return isDownloadComplete, pathToTheSong

    def computeDbToReduce(song):
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
            song = AudioSegment.from_mp3(pathToTheSong)
            dbRoReduce = computeDbToReduce(song)
            if dbRoReduce > 0:
                song -= dbRoReduce
                song.export(pathToTheSong, 'mp3')

    main()
except Exception as ex:
    win32gui.ShowWindow(win32gui.GetForegroundWindow() , win32con.SW_SHOW)
    print("Error: ", ex)
    input("Press enter to exit...")