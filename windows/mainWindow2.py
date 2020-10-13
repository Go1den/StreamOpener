from tkinter import Tk, NSEW, Frame

from constants.fileConstants import FileConstants
from constants.labelConstants import LabelConstants
from frames.scrollableFrame import ScrollableFrame
from frames.searchFrame import SearchFrame
from frames.streamFrame import StreamFrame
from twitchapi import getAllStreamsUserFollows, getLiveFollowedStreams

class MainWindow2:
    def __init__(self, credentials):
        self.window = Tk()
        self.window.withdraw()
        self.windowFrame = Frame(self.window)
        self.scrollableFrame = ScrollableFrame(1010, 680, self.windowFrame)
        self.credentials = credentials
        self.followedStreams = getAllStreamsUserFollows(credentials.oauth, credentials.user_id)
        self.liveStreams = getLiveFollowedStreams(credentials.oauth, [self.followedStreams[i:i + 100] for i in range(0, len(self.followedStreams), 100)])

        self.searchFrame = SearchFrame(self.windowFrame)

        self.gridFrames()
        self.initializeWindow()
        self.window.deiconify()

    def gridFrames(self):
        i = 0
        j = 0
        for stream in self.liveStreams:
            streamFrame = StreamFrame(stream, self.window, self.scrollableFrame.scrollable_frame)
            streamFrame.frame.grid(row=i, column=j, sticky=NSEW, padx=4, pady=4)
            j += 1
            if j == 3:
                i += 1
                j = 0

        self.searchFrame.frame.grid(row=0, column=0, sticky=NSEW, padx=4, pady=4)
        self.scrollableFrame.grid(row=0, column=1, sticky=NSEW, padx=4, pady=4)

        self.windowFrame.grid()

    def initializeWindow(self):
        self.window.iconbitmap(FileConstants.STREAMOPENER_ICON)
        self.window.geometry('1280x720')
        self.window.title(LabelConstants.STREAMOPENER)
        self.window.resizable(width=False, height=False)
