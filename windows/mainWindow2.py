import sys
import webbrowser
from tkinter import Tk, NSEW, Frame, Menu, SINGLE, MULTIPLE, BooleanVar

from constants.fileConstants import FileConstants
from constants.labelConstants import LabelConstants
from constants.urlConstants import URLConstants
from frames.scrollableFrame import ScrollableFrame
from frames.searchFrame import SearchFrame
from frames.streamFrame import StreamFrame
from twitchapi import getAllStreamsUserFollows, getLiveFollowedStreams
from windows.aboutWindow import AboutWindow
from windows.filterWindow import FilterWindow
from windows.teamWindow import TeamWindow

class MainWindow2:
    def __init__(self, credentials):
        self.window = Tk()
        self.window.withdraw()
        self.windowFrame = Frame(self.window)
        self.scrollableFrame = ScrollableFrame(1010, 680, self.windowFrame)
        self.credentials = credentials
        self.followedStreams = getAllStreamsUserFollows(credentials.oauth, credentials.user_id)
        self.liveStreams = getLiveFollowedStreams(credentials.oauth, [self.followedStreams[i:i + 100] for i in range(0, len(self.followedStreams), 100)])

        self.singleSelectMode = BooleanVar()
        self.multipleSelectMode = BooleanVar()
        self.hideThumbnail = BooleanVar()
        self.enableFilters = BooleanVar()

        self.searchFrame = SearchFrame(self.windowFrame)

        self.gridFrames()
        self.addMenu()
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

    def addMenu(self):
        menu = Menu(self.window)

        fileMenu = Menu(menu, tearoff=0)
        fileMenu.add_command(label=LabelConstants.QUIT, command=lambda: self.closeWindow())
        menu.add_cascade(label=LabelConstants.FILE, menu=fileMenu)

        manageMenu = Menu(menu, tearoff=0)
        manageMenu.add_command(label=LabelConstants.SETTINGS_TEAM_WINDOW, command=lambda: TeamWindow(self, self.teams))
        manageMenu.add_command(label=LabelConstants.SETTINGS_FILTER_WINDOW, command=lambda: FilterWindow(self))
        menu.add_cascade(label=LabelConstants.EDIT, menu=manageMenu)

        selectModeMenu = Menu(menu, tearoff=0)
        selectModeMenu.add_checkbutton(label=LabelConstants.SINGLE, variable=self.singleSelectMode, command=lambda: self.setSelectionModes(False, SINGLE))
        selectModeMenu.add_checkbutton(label=LabelConstants.MULTIPLE, variable=self.multipleSelectMode, command=lambda: self.setSelectionModes(True, MULTIPLE))

        settingsMenu = Menu(menu, tearoff=0)
        settingsMenu.add_cascade(label=LabelConstants.SELECTION_MODE, menu=selectModeMenu)
        settingsMenu.add_checkbutton(label=LabelConstants.HIDE_THUMBNAIL, variable=self.hideThumbnail, command=lambda: self.toggleThumbnail(False))
        settingsMenu.add_checkbutton(label=LabelConstants.ENABLE_FILTERS, variable=self.enableFilters, command=lambda: self.toggleFilters())
        menu.add_cascade(label=LabelConstants.SETTINGS_MENU, menu=settingsMenu)

        issueMenu = Menu(menu, tearoff=0)
        issueMenu.add_command(label=LabelConstants.VIA_DISCORD, command=lambda: webbrowser.open(URLConstants.DISCORD, new=2))
        issueMenu.add_command(label=LabelConstants.VIA_GITHUB, command=lambda: webbrowser.open(URLConstants.GITHUB, new=2))

        helpMenu = Menu(menu, tearoff=0)
        helpMenu.add_cascade(label=LabelConstants.REPORT_ISSUE, menu=issueMenu)
        helpMenu.add_command(label=LabelConstants.ABOUT, command=lambda: AboutWindow(self))
        menu.add_cascade(label=LabelConstants.HELP, menu=helpMenu)

        self.window.config(menu=menu)

    def initializeWindow(self):
        self.window.iconbitmap(FileConstants.STREAMOPENER_ICON)
        self.window.geometry('1280x720')
        self.window.title(LabelConstants.STREAMOPENER)
        self.window.resizable(width=False, height=False)

    def closeWindow(self):
        sys.exit(0)
