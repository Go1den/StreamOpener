from tkinter import Tk, NSEW

from constants.fileConstants import FileConstants
from constants.labelConstants import LabelConstants
from frames.streamFrame import StreamFrame
from twitchapi import getAllStreamsUserFollows, getLiveFollowedStreams

class MainWindow2:
    def __init__(self, credentials):
        self.window = Tk()
        self.window.withdraw()
        self.credentials = credentials
        self.followedStreams = getAllStreamsUserFollows(credentials.oauth, credentials.user_id)
        self.liveStreams = getLiveFollowedStreams(credentials.oauth, [self.followedStreams[i:i + 100] for i in range(0, len(self.followedStreams), 100)])

        self.gridFrames()
        self.initializeWindow()
        self.window.deiconify()

    def gridFrames(self):
        i = 0
        j = 0
        for stream in self.liveStreams:
            streamFrame = StreamFrame(stream, self.window)
            streamFrame.frame.grid(row=i, column=j, sticky=NSEW, padx=4, pady=4)
            j += 1
            if j == 3:
                i += 1
                j = 0

    def initializeWindow(self):
        self.window.iconbitmap(FileConstants.STREAMOPENER_ICON)
        self.window.geometry('1280x720')
        self.window.title(LabelConstants.STREAMOPENER)
        self.window.resizable(width=False, height=False)





