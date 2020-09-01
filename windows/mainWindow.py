import io
import sys
import webbrowser
from tkinter import StringVar, Tk, Frame, Label, NSEW, Listbox, MULTIPLE, END, Scrollbar, Menu, W, Button, NONE, messagebox, CENTER, RAISED, BooleanVar, SINGLE, DISABLED, NORMAL
from tkinter.ttk import Combobox
from urllib.request import urlopen

from PIL import ImageTk, Image

from constants import FILE_STREAMOPENER_ICON, ORDERED_STREAMING_SITES, LABEL_STREAM_DROPDOWN, LABEL_STREAMOPENER, LABEL_GAME, LABEL_STREAMER, LABEL_VIEWERS, TWITCH_LINK, \
    MSG_WATCH_ON_TWITCH, LABEL_TWITCH, LABEL_ERROR, MSG_NO_SITE_SELECTED, MSG_NO_STREAMS_SELECTED, LABEL_NO_TITLE, FILE_PREVIEW_BOX_ART, FILE_STREAM_PREVIEW, DISCORD_LINK, \
    GITHUB_LINK, LABEL_SELECTED_STREAMS, LABEL_RIGHT, LABEL_REFRESH, LABEL_RESET, LABEL_LEFT, LABEL_LIVE_STREAMS, LABEL_OPEN_STREAMS, LABEL_PREVIEW, LABEL_VIA_DISCORD, \
    LABEL_VIA_GITHUB, LABEL_REPORT_ISSUE, LABEL_QUIT, LABEL_FILE, LABEL_SINGLE, LABEL_MULTIPLE, LABEL_SELECTION_MODE, LABEL_HIDE_THUMBNAIL, LABEL_SETTINGS_MENU, LABEL_ABOUT, \
    LABEL_HELP, LABEL_TEAMS_DROPDOWN, LABEL_SETTINGS_TEAM_WINDOW, KEY_SELECTION_MODE, KEY_HIDE_THUMBNAIL, KEY_OPEN_STREAMS_ON, KEY_TEAM, LABEL_SETTINGS_JSON, LABEL_URL_TWITCH, \
    LABEL_FILTER, LABEL_FILTER_STREAMER, LABEL_FILTER_GAME, LABEL_FILTER_COMBO, LABEL_SETTINGS_FILTER_WINDOW, MSG_FILTER_ADDED, LABEL_INFO, MSG_FILTER_ALREADY_EXISTS, LABEL_EDIT, \
    LABEL_ENABLE_FILTERS, KEY_FILTERS, LABEL_FILTER_KEY_STREAMER, LABEL_FILTER_KEY_GAME, LABEL_FILTER_KEY_COMBINED, LABEL_UNFOLLOW_WINDOW
from fileHandler import readTeams, readSettings, writeSettings, writeTeams, readFilters, writeFilters
from twitchapi import getLiveFollowedStreams, getAllStreamsUserFollows
from windows.aboutWindow import AboutWindow
from windows.filterWindow import FilterWindow
from windows.teamWindow import TeamWindow
from windows.unfollowWindow import UnfollowWindow

class MainWindow:
    def __init__(self, credentials):
        self.window = Tk()
        self.window.withdraw()
        self.site = StringVar()
        self.credentials = credentials
        self.settings = readSettings()
        self.followedStreams = getAllStreamsUserFollows(self.credentials.oauth, self.credentials.user_id)
        self.teams = readTeams(self.followedStreams)
        self.currentTeam = StringVar()
        self.filters = readFilters()
        self.liveStreams = getLiveFollowedStreams(self.credentials.oauth, [self.followedStreams[i:i + 100] for i in range(0, len(self.followedStreams), 100)])
        self.selectedStreams = None
        self.unselectedStreams = None
        self.previewStreamObject = None
        self.previewImage = ImageTk.PhotoImage(Image.open(FILE_STREAM_PREVIEW))
        self.boxArtImage = ImageTk.PhotoImage(Image.open(FILE_PREVIEW_BOX_ART))
        self.previewTitle = StringVar()
        self.previewName = StringVar()
        self.previewGame = StringVar()
        self.previewViewers = StringVar()
        self.singleSelectMode = BooleanVar()
        self.multipleSelectMode = BooleanVar()
        self.hideThumbnail = BooleanVar()
        self.enableFilters = BooleanVar()

        self.labelImage = None
        self.labelBoxArt = None
        self.liveListBox = None
        self.selectedListBox = None
        self.siteDropdown = None
        self.teamDropdown = None

        self.buttonFilterGame = None
        self.buttonFilterStreamer = None
        self.buttonFilterCombined = None

        self.teamsFrame = Frame(self.window)
        self.streamFrame = Frame(self.window)
        self.urlFrame = Frame(self.window)
        self.previewLabelFrame = Frame(self.window)
        self.previewFrame = Frame(self.window)
        self.filterFrame = Frame(self.window)
        self.okFrame = Frame(self.window)

        self.initializeWindow()
        self.gridFrames()
        self.addMenu()
        self.addTeamsDropdown()
        self.addLiveListbox()
        self.addListBoxButtons()
        self.addSelectedListbox()
        self.addURLDropdown()
        self.addPreviewLabel()
        self.addPreview()
        self.addFilterFrame()
        self.addOkButton()
        self.applySettings()
        self.window.deiconify()

    def initializeWindow(self):
        self.window.iconbitmap(FILE_STREAMOPENER_ICON)
        self.window.geometry('380x674')
        self.window.title(LABEL_STREAMOPENER)
        self.window.resizable(width=False, height=False)

    def gridFrames(self):
        self.previewFrame.grid_columnconfigure(1, weight=1)
        self.teamsFrame.grid(row=0, sticky=NSEW, padx=8, pady=(4, 0))
        self.streamFrame.grid(row=1, sticky=NSEW, padx=4, pady=4)
        self.urlFrame.grid(row=2, sticky=NSEW, padx=8, pady=4)
        self.previewLabelFrame.grid(row=3, sticky=NSEW, padx=12)
        self.previewFrame.grid(row=4, sticky=NSEW, padx=(12, 6), pady=(2, 4))
        self.filterFrame.grid(row=5, sticky=NSEW, padx=(8, 4), pady=4)
        self.okFrame.grid(row=6, sticky=NSEW, padx=(8, 4), pady=4)

    def addMenu(self):
        menu = Menu(self.window)

        fileMenu = Menu(menu, tearoff=0)
        fileMenu.add_command(label=LABEL_QUIT, command=lambda: self.closeWindow())
        menu.add_cascade(label=LABEL_FILE, menu=fileMenu)

        manageMenu = Menu(menu, tearoff=0)
        manageMenu.add_command(label=LABEL_SETTINGS_TEAM_WINDOW, command=lambda: TeamWindow(self, self.teams))
        manageMenu.add_command(label=LABEL_SETTINGS_FILTER_WINDOW, command=lambda: FilterWindow(self))
        manageMenu.add_command(label=LABEL_UNFOLLOW_WINDOW, command=lambda: UnfollowWindow(self))
        menu.add_cascade(label=LABEL_EDIT, menu=manageMenu)

        selectModeMenu = Menu(menu, tearoff=0)
        selectModeMenu.add_checkbutton(label=LABEL_SINGLE, variable=self.singleSelectMode, command=lambda: self.setSelectionModes(False, SINGLE))
        selectModeMenu.add_checkbutton(label=LABEL_MULTIPLE, variable=self.multipleSelectMode, command=lambda: self.setSelectionModes(True, MULTIPLE))

        settingsMenu = Menu(menu, tearoff=0)
        settingsMenu.add_cascade(label=LABEL_SELECTION_MODE, menu=selectModeMenu)
        settingsMenu.add_checkbutton(label=LABEL_HIDE_THUMBNAIL, variable=self.hideThumbnail, command=lambda: self.toggleThumbnail(False))
        settingsMenu.add_checkbutton(label=LABEL_ENABLE_FILTERS, variable=self.enableFilters, command=lambda: self.toggleFilters())
        menu.add_cascade(label=LABEL_SETTINGS_MENU, menu=settingsMenu)

        issueMenu = Menu(menu, tearoff=0)
        issueMenu.add_command(label=LABEL_VIA_DISCORD, command=lambda: webbrowser.open(DISCORD_LINK, new=2))
        issueMenu.add_command(label=LABEL_VIA_GITHUB, command=lambda: webbrowser.open(GITHUB_LINK, new=2))

        helpMenu = Menu(menu, tearoff=0)
        helpMenu.add_cascade(label=LABEL_REPORT_ISSUE, menu=issueMenu)
        helpMenu.add_command(label=LABEL_ABOUT, command=lambda: AboutWindow(self))
        menu.add_cascade(label=LABEL_HELP, menu=helpMenu)

        self.window.config(menu=menu)

    def addTeamsDropdown(self):
        labelTeamsDropdown = Label(self.teamsFrame, text=LABEL_TEAMS_DROPDOWN)
        labelTeamsDropdown.grid(row=0, column=0, sticky=NSEW, padx=4, pady=4)
        self.teamDropdown = Combobox(self.teamsFrame, textvariable=self.currentTeam, state="readonly", values=list(self.teams.keys()))
        self.teamDropdown.current(0)
        self.teamDropdown.bind("<<ComboboxSelected>>", self.refresh)
        self.teamDropdown.grid(row=0, column=1, sticky=NSEW, padx=4, pady=4)

    def addLiveListbox(self):
        frameLiveListBox = Frame(self.streamFrame)
        frameLiveListBox.grid(row=0, column=0, sticky=NSEW, padx=4, pady=(0, 4))
        labelLiveListBox = Label(frameLiveListBox, text=LABEL_LIVE_STREAMS)
        labelLiveListBox.grid(row=0, column=0, padx=4, sticky=W)
        scrollbar = Scrollbar(frameLiveListBox)
        scrollbar.grid(row=1, column=1, sticky="NWS")
        self.liveListBox = Listbox(frameLiveListBox, selectmode=SINGLE, yscrollcommand=scrollbar.set, activestyle=NONE)
        scrollbar.config(command=self.liveListBox.yview)
        self.populateLiveListBox()
        self.liveListBox.bind('<<ListboxSelect>>', self.onSelectLiveListbox)
        self.liveListBox.grid(row=1, column=0, sticky=NSEW, padx=(4, 0))

    def addListBoxButtons(self):
        frameListBoxButtons = Frame(self.streamFrame)
        frameListBoxButtons.grid(row=0, column=1, sticky=NSEW, pady=(0, 4))
        buttonLeftArrow = Button(frameListBoxButtons, text=LABEL_LEFT, width=7, command=lambda: self.unselectStreams())
        buttonLeftArrow.grid(row=0, sticky=NSEW, padx=4, pady=(38, 4))
        buttonReset = Button(frameListBoxButtons, text=LABEL_RESET, width=7, command=lambda: self.reset())
        buttonReset.grid(row=1, sticky=NSEW, padx=4, pady=4)
        buttonRefresh = Button(frameListBoxButtons, text=LABEL_REFRESH, width=7, command=lambda: self.refresh())
        buttonRefresh.grid(row=2, sticky=NSEW, padx=4, pady=4)
        buttonRightArrow = Button(frameListBoxButtons, text=LABEL_RIGHT, width=7, command=lambda: self.selectStreams())
        buttonRightArrow.grid(row=3, sticky=NSEW, padx=4, pady=4)

    def addSelectedListbox(self):
        frameSelectedListBox = Frame(self.streamFrame)
        frameSelectedListBox.grid(row=0, column=2, sticky=NSEW, pady=(0, 4))
        labelLiveListBox = Label(frameSelectedListBox, text=LABEL_SELECTED_STREAMS)
        labelLiveListBox.grid(row=0, column=0, padx=4, sticky=W)
        scrollbar = Scrollbar(frameSelectedListBox)
        scrollbar.grid(row=1, column=1, sticky="NWS")
        self.selectedListBox = Listbox(frameSelectedListBox, selectmode=SINGLE, yscrollcommand=scrollbar.set, activestyle=NONE)
        scrollbar.config(command=self.selectedListBox.yview)
        self.selectedListBox.bind('<<ListboxSelect>>', self.onSelectSelectedListBox)
        self.selectedListBox.grid(row=1, column=0, sticky=NSEW, padx=(4, 0))

    def addURLDropdown(self):
        labelSiteDropdown = Label(self.urlFrame, text=LABEL_STREAM_DROPDOWN)
        labelSiteDropdown.grid(row=1, column=0, sticky=NSEW, padx=4, pady=4)
        self.siteDropdown = Combobox(self.urlFrame, textvariable=self.site, state="readonly", values=list(ORDERED_STREAMING_SITES.keys()))
        self.siteDropdown.bind("<<ComboboxSelected>>", self.updateURLSetting)
        self.siteDropdown.grid(row=1, column=1, sticky=NSEW, padx=4, pady=4)

    def addPreviewLabel(self):
        labelPreview = Label(self.previewLabelFrame, text=LABEL_PREVIEW)
        labelPreview.grid(sticky=NSEW)

    def addPreview(self):
        self.setDefaultPreviewLabels()
        self.labelImage = Label(self.previewFrame, image=self.previewImage, bd=1)
        self.labelImage.grid(row=0, sticky=W, columnspan=2)
        labelTitle = Label(self.previewFrame, textvariable=self.previewTitle)
        labelTitle.grid(row=1, sticky=W, columnspan=2)
        boxArtFrame = Frame(self.previewFrame)
        boxArtFrame.grid(row=2, column=0, sticky=NSEW)
        self.labelBoxArt = Label(boxArtFrame, image=self.boxArtImage, bd=1)
        self.labelBoxArt.grid(row=0, column=0, sticky=W)
        boxArtLabelFrame = Frame(self.previewFrame)
        boxArtLabelFrame.grid(row=2, column=1, sticky=NSEW)
        labelName = Label(boxArtLabelFrame, textvariable=self.previewName, anchor=W)
        labelName.grid(row=0, sticky=W)
        labelGame = Label(boxArtLabelFrame, textvariable=self.previewGame)
        labelGame.grid(row=1, sticky=W)
        labelViewers = Label(boxArtLabelFrame, textvariable=self.previewViewers)
        labelViewers.grid(row=2, sticky=W)

    def addFilterFrame(self):
        labelFilter = Label(self.filterFrame, text=LABEL_FILTER)
        labelFilter.grid(row=0, column=0, sticky=NSEW, padx=(4, 2), pady=4)
        self.buttonFilterStreamer = Button(self.filterFrame, text=LABEL_FILTER_STREAMER, width=13,
                                           command=lambda: self.addFilter(self.previewStreamObject.stylizedStreamName, None))
        self.buttonFilterStreamer.grid(row=0, column=1, sticky=NSEW, padx=4, pady=4)
        self.buttonFilterGame = Button(self.filterFrame, text=LABEL_FILTER_GAME, width=13, command=lambda: self.addFilter(None, self.previewStreamObject.gameTitle))
        self.buttonFilterGame.grid(row=0, column=2, sticky=NSEW, padx=4, pady=4)
        self.buttonFilterCombined = Button(self.filterFrame, text=LABEL_FILTER_COMBO, width=13,
                                           command=lambda: self.addFilter(self.previewStreamObject.stylizedStreamName, self.previewStreamObject.gameTitle))
        self.buttonFilterCombined.grid(row=0, column=3, sticky=NSEW, padx=4, pady=4)

    def addOkButton(self):
        buttonOk = Button(self.okFrame, text=LABEL_OPEN_STREAMS, width=50, command=lambda: self.openURL(), anchor=CENTER, relief=RAISED)
        buttonOk.grid(sticky=NSEW, padx=4, pady=4)

    def applySettings(self):
        refresh = False
        if KEY_FILTERS in self.settings[LABEL_SETTINGS_JSON]:
            self.enableFilters.set(self.settings[LABEL_SETTINGS_JSON][KEY_FILTERS])
            refresh = True
        if KEY_SELECTION_MODE in self.settings[LABEL_SETTINGS_JSON]:
            selectionMode = self.settings[LABEL_SETTINGS_JSON][KEY_SELECTION_MODE]
            self.setSelectionModes(selectionMode == MULTIPLE, self.settings[LABEL_SETTINGS_JSON][KEY_SELECTION_MODE])
        else:
            self.setSelectionModes(False, SINGLE)
        if KEY_HIDE_THUMBNAIL in self.settings[LABEL_SETTINGS_JSON]:
            self.hideThumbnail.set(self.settings[LABEL_SETTINGS_JSON][KEY_HIDE_THUMBNAIL])
            self.toggleThumbnail(True)
        else:
            self.hideThumbnail.set(False)
        if KEY_OPEN_STREAMS_ON in self.settings[LABEL_SETTINGS_JSON]:
            self.site.set(self.settings[LABEL_SETTINGS_JSON][KEY_OPEN_STREAMS_ON])
        else:
            self.site.set(ORDERED_STREAMING_SITES[LABEL_URL_TWITCH])
        if KEY_TEAM in self.settings[LABEL_SETTINGS_JSON] and self.settings[LABEL_SETTINGS_JSON][KEY_TEAM] in self.teams.keys():
            self.teamDropdown.set(self.settings[LABEL_SETTINGS_JSON][KEY_TEAM])
            refresh = True
        if refresh:
            self.refresh()

    def addFilter(self, name=None, game=None):
        if name or game:  # one must have a value or else filtering is pointless
            newFilter = {}
            if name:
                newFilter["streamer"] = name
            if game:
                newFilter["game"] = game
            if "streamer" in newFilter.keys():
                if "game" in newFilter.keys():
                    newFilter["description"] = newFilter["streamer"] + " streaming " + newFilter["game"]
                    filterCategory = "combined"
                else:
                    newFilter["description"] = newFilter["streamer"]
                    filterCategory = "streamer"
            else:
                newFilter["description"] = newFilter["game"]
                filterCategory = "game"
            if newFilter not in self.filters["filters"][filterCategory]:
                self.filters["filters"][filterCategory].append(newFilter)
                writeFilters(self.filters)
                messagebox.showinfo(LABEL_INFO, MSG_FILTER_ADDED.format(newFilter["description"]))
            else:
                messagebox.showerror(LABEL_ERROR, MSG_FILTER_ALREADY_EXISTS)

    def setFilters(self, newFilters):
        self.filters = newFilters
        writeFilters(self.filters)
        if self.enableFilters.get():
            self.refresh()

    def toggleThumbnail(self, isProgramJustStarting):
        if not self.hideThumbnail.get():
            if not isProgramJustStarting:
                self.window.geometry('380x654')  # I do not know why this works, but for some reason the window adds 20px to the 614 here
                self.labelImage.grid()
            self.hideThumbnail.set(False)
        else:
            self.labelImage.grid_remove()
            if isProgramJustStarting:
                self.window.geometry('380x494')
            else:
                self.window.geometry('380x474')
            self.hideThumbnail.set(True)
        self.settings[LABEL_SETTINGS_JSON][KEY_HIDE_THUMBNAIL] = self.hideThumbnail.get()
        writeSettings(self.settings)

    def setSelectionModes(self, isMultipleMode: bool, selectionMode: str):
        if isMultipleMode:
            self.singleSelectMode.set(False)
            self.multipleSelectMode.set(True)
        else:
            self.multipleSelectMode.set(False)
            self.singleSelectMode.set(True)
        self.settings[LABEL_SETTINGS_JSON][KEY_SELECTION_MODE] = selectionMode
        writeSettings(self.settings)
        self.liveListBox.configure(selectmode=selectionMode)
        self.selectedListBox.configure(selectmode=selectionMode)
        self.liveListBox.selection_clear(0, END)
        self.selectedListBox.selection_clear(0, END)
        self.resetPreview()

    def updateURLSetting(self, event=None):
        self.settings[LABEL_SETTINGS_JSON][KEY_OPEN_STREAMS_ON] = self.siteDropdown.get()
        writeSettings(self.settings)

    def populateLiveListBox(self):
        tmpLiveList = [stream for stream in self.teams[self.currentTeam.get()] if stream in [x.stylizedStreamName for x in self.liveStreams if not self.isFiltered(x)]]
        for stream in tmpLiveList:
            self.liveListBox.insert(END, stream)

    # TODO: condense these methods into one common method
    def onSelectLiveListbox(self, event):
        w = event.widget
        if self.multipleSelectMode.get():
            if self.selectedStreams:
                changedSelection = set(self.selectedStreams).symmetric_difference(set(w.curselection()))
                self.selectedStreams = w.curselection()
            else:
                self.selectedStreams = w.curselection()
                changedSelection = w.curselection()
            selectedStreamName = w.get(int(list(changedSelection)[0]))
            self.updatePreviewFrame(selectedStreamName)
        else:
            self.selectedStreams = w.curselection()
            selectedStreamName = w.get(w.curselection())
            self.updatePreviewFrame(selectedStreamName)

    # TODO: condense these methods into one common method
    def onSelectSelectedListBox(self, event):
        w = event.widget
        if self.multipleSelectMode.get():
            if self.unselectedStreams:
                changedSelection = set(self.unselectedStreams).symmetric_difference(set(w.curselection()))
                self.unselectedStreams = w.curselection()
            else:
                self.unselectedStreams = w.curselection()
                changedSelection = w.curselection()
            unselectedStreamName = w.get(int(list(changedSelection)[0]))
            self.updatePreviewFrame(unselectedStreamName)
        else:
            self.unselectedStreams = w.curselection()
            unselectedStreamName = w.get(w.curselection())
            self.updatePreviewFrame(unselectedStreamName)

    # Todo: combine these methods
    def selectStreams(self):
        if self.selectedStreams:
            for stream in self.selectedStreams:
                self.selectedListBox.insert(END, self.liveListBox.get(stream))
            for stream in reversed(self.selectedStreams):
                self.liveListBox.delete(stream)
            self.liveListBox.selection_clear(0, END)
            self.selectedStreams = None
            self.resetPreview()

    # Todo: combine these methods
    def unselectStreams(self):
        if self.unselectedStreams:
            for stream in self.unselectedStreams:
                if stream in self.teams[self.currentTeam.get()]:
                    self.liveListBox.insert(END, self.selectedListBox.get(stream))
            for stream in reversed(self.unselectedStreams):
                self.selectedListBox.delete(stream)
            self.selectedListBox.selection_clear(0, END)
            self.unselectedStreams = None
            self.resetPreview()

    def setTeams(self, teams):
        self.teams = teams
        writeTeams(self.teams)
        self.updateTeamDropdown()

    def updateTeamDropdown(self):
        self.teamDropdown.configure(values=list(self.teams.keys()))
        self.teamDropdown.current(0)
        self.refresh()

    def reset(self):
        self.liveListBox.selection_clear(0, END)
        self.liveListBox.delete(0, END)
        self.selectedListBox.selection_clear(0, END)
        self.selectedListBox.delete(0, END)
        self.populateLiveListBox()
        self.selectedStreams = None
        self.unselectedStreams = None
        self.resetPreview()

    def setDefaultPreviewLabels(self):
        self.previewTitle.set(LABEL_NO_TITLE)
        self.previewGame.set(LABEL_GAME)
        self.previewName.set(LABEL_STREAMER)
        self.previewViewers.set(LABEL_VIEWERS)

    def resetPreview(self):
        self.previewStreamObject = None
        self.previewImage = ImageTk.PhotoImage(Image.open(FILE_STREAM_PREVIEW))
        self.labelImage.configure(image=self.previewImage)
        self.boxArtImage = ImageTk.PhotoImage(Image.open(FILE_PREVIEW_BOX_ART))
        self.labelBoxArt.configure(image=self.boxArtImage)
        self.setFilterButtonsState(DISABLED)
        self.setDefaultPreviewLabels()

    def setFilterButtonsState(self, state):
        self.buttonFilterGame.configure(state=state)
        self.buttonFilterStreamer.configure(state=state)
        self.buttonFilterCombined.configure(state=state)

    def updatePreviewFrame(self, selectedStreamName):
        thisStream = [stream for stream in self.liveStreams if stream.stylizedStreamName == selectedStreamName][0]
        self.previewStreamObject = thisStream
        if len(thisStream.streamTitle) > 50:
            self.previewTitle.set(thisStream.streamTitle[:50] + "...")
        else:
            self.previewTitle.set(thisStream.streamTitle)
        if len(thisStream.gameTitle) > 45:
            self.previewGame.set(LABEL_GAME + thisStream.streamTitle[:45] + "...")
        else:
            self.previewGame.set(LABEL_GAME + thisStream.gameTitle)
        self.previewName.set(LABEL_STREAMER + thisStream.streamName)
        self.previewViewers.set(LABEL_VIEWERS + thisStream.viewerCount)
        self.previewImage = self.getImageFromURL(thisStream.previewImage, ImageTk.PhotoImage(Image.open(FILE_STREAM_PREVIEW)))
        self.labelImage.configure(image=self.previewImage)
        self.boxArtImage = self.getImageFromURL(thisStream.boxArtURL, ImageTk.PhotoImage(Image.open(FILE_PREVIEW_BOX_ART)))
        self.labelBoxArt.configure(image=self.boxArtImage)
        self.setFilterButtonsState(NORMAL)

    def getImageFromURL(self, url, defaultImage) -> ImageTk.PhotoImage:
        try:
            rawData = urlopen(url).read()
            im = Image.open(io.BytesIO(rawData))
            return ImageTk.PhotoImage(im)
        except ValueError:
            return defaultImage

    def refresh(self, event=None):
        if self.selectedListBox:  # Don't refresh if the window hasn't been fully created yet
            self.followedStreams = getAllStreamsUserFollows(self.credentials.oauth, self.credentials.user_id)
            self.teams = readTeams(self.followedStreams)
            refreshStreams = getLiveFollowedStreams(self.credentials.oauth, [self.followedStreams[i:i + 100] for i in range(0, len(self.followedStreams), 100)])
            tmpLiveList = refreshStreams
            tmpSelectedList = []
            for stylizedStreamName in self.selectedListBox.get(0, END):
                stream = [stream for stream in self.liveStreams if stream.stylizedStreamName == stylizedStreamName][0]
                if stream.isLive(refreshStreams):
                    tmpSelectedList.append(stream.stylizedStreamName)
                else:
                    self.selectedListBox.delete(self.selectedListBox.get(0, END).index(stylizedStreamName))
            self.liveListBox.delete(0, END)
            tmpLiveList = [stream for stream in tmpLiveList if not self.isFiltered(stream)]
            # TODO: The below line might be able to combine with populateListbox
            tmpLiveList = [stream for stream in self.teams[self.currentTeam.get()] if
                           self.isNotSelected(stream, tmpSelectedList) and stream in [x.stylizedStreamName for x in tmpLiveList]]
            for stream in tmpLiveList:
                self.liveListBox.insert(END, stream)
            self.liveStreams = refreshStreams
            self.settings[LABEL_SETTINGS_JSON][KEY_TEAM] = self.teamDropdown.get()
            writeSettings(self.settings)
            self.resetPreview()

    def isNotSelected(self, stream, tmpSelectedList) -> bool:
        return stream not in tmpSelectedList

    def toggleFilters(self):
        self.settings[LABEL_SETTINGS_JSON][KEY_FILTERS] = self.enableFilters.get()
        writeSettings(self.settings)
        self.refresh()

    def openURL(self):
        finalURL = ORDERED_STREAMING_SITES.get(self.siteDropdown.get())
        watchingSingleStreamOnTwitch = False
        if len(self.selectedListBox.get(0, END)) == 1 and finalURL != TWITCH_LINK and messagebox.askyesno(LABEL_TWITCH, MSG_WATCH_ON_TWITCH):
            finalURL = TWITCH_LINK
            watchingSingleStreamOnTwitch = True
        if not watchingSingleStreamOnTwitch and not self.siteDropdown.get():
            messagebox.showerror(LABEL_ERROR, MSG_NO_SITE_SELECTED)
        elif len(self.selectedListBox.get(0, END)) > 0:
            if finalURL == TWITCH_LINK:
                for selectedStream in self.selectedListBox.get(0, END):
                    for stream in self.liveStreams:
                        if stream.stylizedStreamName == selectedStream:
                            webbrowser.open(finalURL + stream.streamName, new=2)
            else:
                for selectedStream in self.selectedListBox.get(0, END):
                    for stream in self.liveStreams:
                        if stream.stylizedStreamName == selectedStream:
                            finalURL += stream.streamName + "/"
                webbrowser.open(finalURL, new=2)
        else:
            messagebox.showerror(LABEL_ERROR, MSG_NO_STREAMS_SELECTED)

    def isFiltered(self, stream):
        if self.enableFilters.get():
            isGameFiltered = stream.gameTitle in [x["description"] for x in self.filters["filters"][LABEL_FILTER_KEY_GAME]]
            isStreamFiltered = stream.stylizedStreamName in [x["description"] for x in self.filters["filters"][LABEL_FILTER_KEY_STREAMER]]
            isComboFiltered = stream.stylizedStreamName + " streaming " + stream.gameTitle in [x["description"] for x in self.filters["filters"][LABEL_FILTER_KEY_COMBINED]]
            return isGameFiltered or isStreamFiltered or isComboFiltered
        return False

    def closeWindow(self):
        sys.exit(0)
