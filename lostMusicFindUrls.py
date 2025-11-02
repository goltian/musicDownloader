import os
import regex

codec = 'utf-8'
channelNamesFile = open('channelNames.txt', 'r', encoding=codec)
songNamesAndLinksFile = open('songNamesAndLinks.txt', 'r', encoding=codec)

songTitles = []
fullTitles = []
links = []

for _ in range(2583):
    channelNameStr = channelNamesFile.readline()[:-1]
    songNameStr = songNamesAndLinksFile.readline()[:-1]
    titleStr = channelNameStr + ' - ' + songNameStr
    linkNameStr = songNamesAndLinksFile.readline()[:-1]

    songTitles.append(songNameStr)
    fullTitles.append(titleStr)
    links.append(linkNameStr)

channelNamesFile.close()
songNamesAndLinksFile.close()

# assign directory
directory = 'D:\music'
textOfAllSongs = ''
for root, dirs, files in os.walk(directory):
    for file in files:
        textOfAllSongs = textOfAllSongs + file + '\n'

urlsForLostSongsToDownloadFile = open('urlsForLostSongsToDownload.txt', 'w', encoding=codec)

# iterate over files in
# that directory
curId = 0
for songTitlePattern, fullTitlePattern in zip(songTitles, fullTitles):
    if 'Видео удалено' in fullTitlePattern:
        print(curId, ' ERROR ', fullTitlePattern)
        urlsForLostSongsToDownloadFile.write(fullTitlePattern)
        urlsForLostSongsToDownloadFile.write(links[curId])
        urlsForLostSongsToDownloadFile.write('\n')
    elif fullTitlePattern in textOfAllSongs:
        ...
    elif songTitlePattern in textOfAllSongs:
        ...
    else:
        try:
            errorCountInPattern = min(6, int(len(songTitlePattern) / 10))
            re_pat = regex.compile(rf'({songTitlePattern})' + f'{{e<={errorCountInPattern}}}', regex.BESTMATCH)
            patternWasFound = re_pat.search(textOfAllSongs)
            if patternWasFound:
                ...
            else:
                print(curId, ' ERROR ', fullTitlePattern)
                urlsForLostSongsToDownloadFile.write(fullTitlePattern)
                urlsForLostSongsToDownloadFile.write(links[curId])
                urlsForLostSongsToDownloadFile.write('\n')
        except:
            print(curId, ' ERROR ', fullTitlePattern)
            urlsForLostSongsToDownloadFile.write(fullTitlePattern)
            urlsForLostSongsToDownloadFile.write(links[curId])
            urlsForLostSongsToDownloadFile.write('\n')

    curId += 1
    print(curId)

urlsForLostSongsToDownloadFile.close()