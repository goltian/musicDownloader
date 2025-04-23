import win32gui, win32con
win32gui.ShowWindow(win32gui.GetForegroundWindow() , win32con.SW_HIDE)
import musicDownloading
import volumeReducing
import random

random_index = str(random.randint(1, 1000))
tries = 3
for attempt in range(tries):
    try:
        print("Attemt № ", attempt, " starts")
        pathToTheSong = musicDownloading.downloadMusic(random_index)
        volumeReducing.reduceVolume(pathToTheSong)

    except Exception as ex:
        if attempt < tries - 1:
            print("Attemt № ", attempt, " failed")
            continue
        else:
            win32gui.ShowWindow(win32gui.GetForegroundWindow() , win32con.SW_SHOW)
            print("Error: ", ex)
            input("Press enter to exit...")
    break
