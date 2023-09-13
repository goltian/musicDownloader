try:
    import win32gui, win32con
    win32gui.ShowWindow(win32gui.GetForegroundWindow() , win32con.SW_HIDE)
    from pydub import AudioSegment
    import download

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

    pathToTheSong = download.downloadMusic()
    song = AudioSegment.from_mp3(pathToTheSong)
    dbRoReduce = computeDbToReduce(song)
    if dbRoReduce > 0:
        song -= dbRoReduce
        song.export(pathToTheSong, 'mp3')

except Exception as ex:
    win32gui.ShowWindow(win32gui.GetForegroundWindow() , win32con.SW_SHOW)
    print("Error: ", ex)
    input("Press enter to exit...")
