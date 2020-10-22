import sys
import webbrowser
from tkinter import Tk, NSEW, Frame, Menu, BooleanVar

from constants.fileConstants import FileConstants
from constants.labelConstants import LabelConstants
from constants.miscConstants import MiscConstants
from constants.urlConstants import URLConstants
from fileHandler import writeSettings, readSettings, readTeams
from frames.scrollableFrame import ScrollableFrame
from frames.searchFrame import SearchFrame
from twitchapi import getAllStreamsUserFollows, getLiveFollowedStreams, getAllTwitchTags
from windows.aboutWindow import AboutWindow
from windows.filterWindow import FilterWindow
from windows.teamWindow import TeamWindow

class MainWindow2:
    def __init__(self, credentials):
        self.window = Tk()
        self.window.withdraw()
        self.credentials = credentials
        self.settings = readSettings()
        self.followedStreams = getAllStreamsUserFollows(self.credentials.oauth, self.credentials.user_id)
        self.teams = readTeams(self.followedStreams)
        self.tags = getAllTwitchTags(self.credentials.oauth)

        self.windowFrame = Frame(self.window)
        self.scrollableFrame = ScrollableFrame(1010, 680, self.windowFrame)
        self.liveStreams = getLiveFollowedStreams(credentials.oauth, [self.followedStreams[i:i + 100] for i in range(0, len(self.followedStreams), 100)])

        self.singleSelectMode = BooleanVar()
        self.multipleSelectMode = BooleanVar()
        self.hideThumbnail = BooleanVar()
        self.hideBoxArt = BooleanVar()
        self.enableFilters = BooleanVar()

        self.searchFrame = SearchFrame(self)

        self.initializeWindow()
        self.gridFrames()
        self.addMenu()
        self.applySettings()
        self.window.deiconify()

    def gridFrames(self):
        for stream in self.liveStreams:
            self.scrollableFrame.addStreamFrame(stream)
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
        manageMenu.add_command(label=LabelConstants.SETTINGS_TAG_WINDOW)
        menu.add_cascade(label=LabelConstants.EDIT, menu=manageMenu)

        settingsMenu = Menu(menu, tearoff=0)
        settingsMenu.add_checkbutton(label=LabelConstants.HIDE_THUMBNAIL, variable=self.hideThumbnail, command=lambda: self.toggleThumbnail())
        settingsMenu.add_checkbutton(label=LabelConstants.HIDE_BOXART, variable=self.hideBoxArt, command=lambda: self.toggleBoxArt())
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

    def toggleThumbnail(self):
        if self.hideThumbnail.get():
            self.scrollableFrame.showThumbnails(False)
        else:
            self.scrollableFrame.showThumbnails(True)
        self.settings[LabelConstants.SETTINGS_JSON][MiscConstants.KEY_HIDE_THUMBNAIL] = self.hideThumbnail.get()
        writeSettings(self.settings)

    def toggleBoxArt(self):
        if self.hideBoxArt.get():
            self.scrollableFrame.showBoxArt(False)
        else:
            self.scrollableFrame.showBoxArt(True)
        self.settings[LabelConstants.SETTINGS_JSON][MiscConstants.KEY_HIDE_BOXART] = self.hideBoxArt.get()
        writeSettings(self.settings)


    def applySettings(self):
        # refresh = False
        # if MiscConstants.KEY_FILTERS in self.settings[LabelConstants.SETTINGS_JSON]:
        #     self.enableFilters.set(self.settings[LabelConstants.SETTINGS_JSON][MiscConstants.KEY_FILTERS])
        #     refresh = True
        # if MiscConstants.KEY_SELECTION_MODE in self.settings[LabelConstants.SETTINGS_JSON]:
        #     selectionMode = self.settings[LabelConstants.SETTINGS_JSON][MiscConstants.KEY_SELECTION_MODE]
        #     self.setSelectionModes(selectionMode == MULTIPLE, self.settings[LabelConstants.SETTINGS_JSON][MiscConstants.KEY_SELECTION_MODE])
        # else:
        #     self.setSelectionModes(False, SINGLE)
        if MiscConstants.KEY_HIDE_THUMBNAIL in self.settings[LabelConstants.SETTINGS_JSON]:
            self.hideThumbnail.set(self.settings[LabelConstants.SETTINGS_JSON][MiscConstants.KEY_HIDE_THUMBNAIL])
            # self.toggleThumbnail()
        else:
            self.hideThumbnail.set(False)
        self.scrollableFrame.showThumbnails(not self.hideThumbnail.get())

        if MiscConstants.KEY_HIDE_BOXART in self.settings[LabelConstants.SETTINGS_JSON]:
            self.hideBoxArt.set(self.settings[LabelConstants.SETTINGS_JSON][MiscConstants.KEY_HIDE_BOXART])
        else:
            self.hideBoxArt.set(False)
        self.scrollableFrame.showBoxArt(not self.hideBoxArt.get())
        # if MiscConstants.KEY_OPEN_STREAMS_ON in self.settings[LabelConstants.SETTINGS_JSON]:
        #     self.site.set(self.settings[LabelConstants.SETTINGS_JSON][MiscConstants.KEY_OPEN_STREAMS_ON])
        # else:
        #     self.site.set(URLConstants.ORDERED_STREAMING_SITES[LabelConstants.URL_TWITCH])
        # if MiscConstants.KEY_TEAM in self.settings[LabelConstants.SETTINGS_JSON] and self.settings[LabelConstants.SETTINGS_JSON][MiscConstants.KEY_TEAM] in self.teams.keys():
        #     self.teamDropdown.set(self.settings[LabelConstants.SETTINGS_JSON][MiscConstants.KEY_TEAM])
        #     refresh = True
        # if refresh:
        #     self.refresh()
