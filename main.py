try:
    import win32gui, win32con
    win32gui.ShowWindow(win32gui.GetForegroundWindow() , win32con.SW_HIDE)
    import musicDownloading
    import volumeReducing

    pathToTheSong = musicDownloading.downloadMusic()
    volumeReducing.reduceVolume(pathToTheSong)

except Exception as ex:
    win32gui.ShowWindow(win32gui.GetForegroundWindow() , win32con.SW_SHOW)
    print("Error: ", ex)
    input("Press enter to exit...")
