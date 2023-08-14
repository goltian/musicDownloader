downloadBtn.addEventListener('click', () => {

    // Save url in file
    chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
        let url = tabs[0].url;

        var dataURI = "data:text/plain;charset=utf-8," + encodeURIComponent(url);
        chrome.downloads.download({
            url: dataURI,
            filename: "musicDownloader/urlForDownload.txt",
            saveAs: false,
            conflictAction: "overwrite",
        });
    });

    // Run our python code for downloading enternet content using its url
    var port = chrome.runtime.connectNative('com.music.musicdownloader');
})
