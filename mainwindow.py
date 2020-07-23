import io
import sys
import webbrowser
from tkinter import StringVar, Tk, Frame, Label, NSEW, Listbox, MULTIPLE, END, Scrollbar, Menu, W, Button, NONE, messagebox, CENTER, RAISED, BooleanVar, SINGLE
from tkinter.ttk import Combobox
from urllib.request import urlopen

from PIL import ImageTk, Image

from aboutWindow import AboutWindow
from constants import FILE_STREAMOPENER_ICON, ORDERED_STREAMING_SITES, LABEL_STREAM_DROPDOWN, LABEL_STREAMOPENER, LABEL_GAME, LABEL_STREAMER, LABEL_VIEWERS, TWITCH_LINK, \
    MSG_WATCH_ON_TWITCH, LABEL_TWITCH, LABEL_ERROR, MSG_NO_SITE_SELECTED, MSG_NO_STREAMS_SELECTED, LABEL_NO_TITLE, FILE_PREVIEW_BOX_ART, FILE_STREAM_PREVIEW, DISCORD_LINK, \
    GITHUB_LINK, LABEL_SELECTED_STREAMS, LABEL_RIGHT, LABEL_REFRESH, LABEL_RESET, LABEL_LEFT, LABEL_LIVE_STREAMS, LABEL_OPEN_STREAMS, LABEL_PREVIEW, LABEL_VIA_DISCORD, \
    LABEL_VIA_GITHUB, LABEL_REPORT_ISSUE, LABEL_QUIT, LABEL_FILE, LABEL_SINGLE, LABEL_MULTIPLE, LABEL_SELECTION_MODE, LABEL_HIDE_THUMBNAIL, LABEL_SETTINGS_MENU, LABEL_ABOUT, \
    LABEL_HELP, LABEL_TEAM_WINDOW
from teamwindow import TeamWindow
from twitchapi import getLiveFollowedStreams, getAllStreamsUserFollows

class MainWindow:
    def __init__(self, credentials):
        self.window = Tk()
        self.window.withdraw()
        self.site = StringVar()
        self.credentials = credentials
        self.followedStreams = getAllStreamsUserFollows(self.credentials.oauth, self.credentials.user_id)
        self.liveStreams = getLiveFollowedStreams(self.credentials.oauth, [self.followedStreams[i:i + 100] for i in range(0, len(self.followedStreams), 100)])
        self.selectedStreams = None
        self.unselectedStreams = None
        self.previewImage = ImageTk.PhotoImage(Image.open(FILE_STREAM_PREVIEW))
        self.boxArtImage = ImageTk.PhotoImage(Image.open(FILE_PREVIEW_BOX_ART))
        self.previewTitle = StringVar()
        self.previewName = StringVar()
        self.previewGame = StringVar()
        self.previewViewers = StringVar()
        self.singleSelectMode = BooleanVar()
        self.multipleSelectMode = BooleanVar()
        self.singleSelectMode.set(True)
        self.multipleSelectMode.set(False)
        self.hideThumbnail = False

        self.labelImage = None
        self.labelBoxArt = None
        self.liveListBox = None
        self.selectedListBox = None
        self.siteDropdown = None

        self.streamFrame = Frame(self.window)
        self.urlFrame = Frame(self.window)
        self.previewLabelFrame = Frame(self.window)
        self.previewFrame = Frame(self.window)
        self.okFrame = Frame(self.window)

        self.initializeWindow()
        self.gridFrames()
        self.addMenu()
        self.addLiveListbox()
        self.addListBoxButtons()
        self.addSelectedListbox()
        self.addDropdown()
        self.addPreviewLabel()
        self.addPreview()
        self.addOkButton()
        self.window.deiconify()

    def initializeWindow(self):
        self.window.iconbitmap(FILE_STREAMOPENER_ICON)
        self.window.geometry('380x600')
        self.window.title(LABEL_STREAMOPENER)
        self.window.resizable(width=False, height=False)

    def gridFrames(self):
        self.previewFrame.grid_columnconfigure(1, weight=1)
        self.streamFrame.grid(row=0, sticky=NSEW, padx=4, pady=4)
        self.urlFrame.grid(row=1, sticky=NSEW, padx=8, pady=4)
        self.previewLabelFrame.grid(row=2, sticky=NSEW, padx=12)
        self.previewFrame.grid(row=3, sticky=NSEW, padx=(12, 6), pady=(2, 4))
        self.okFrame.grid(row=4, sticky=NSEW, padx=(8, 4), pady=4)

    def addMenu(self):
        menu = Menu(self.window)

        fileMenu = Menu(menu, tearoff=0)
        fileMenu.add_command(label=LABEL_QUIT, command=lambda: self.closeWindow())
        menu.add_cascade(label=LABEL_FILE, menu=fileMenu)

        selectModeMenu = Menu(menu, tearoff=0)
        selectModeMenu.add_checkbutton(label=LABEL_SINGLE, variable=self.singleSelectMode, command=lambda: self.setSelectionModes(False, SINGLE))
        selectModeMenu.add_checkbutton(label=LABEL_MULTIPLE, variable=self.multipleSelectMode, command=lambda: self.setSelectionModes(True, MULTIPLE))

        settingsMenu = Menu(menu, tearoff=0)
        settingsMenu.add_command(label=LABEL_TEAM_WINDOW, command=lambda: TeamWindow(self.window, {}))
        settingsMenu.add_cascade(label=LABEL_SELECTION_MODE, menu=selectModeMenu)
        settingsMenu.add_checkbutton(label=LABEL_HIDE_THUMBNAIL, command=lambda: self.toggleThumbnail())
        menu.add_cascade(label=LABEL_SETTINGS_MENU, menu=settingsMenu)

        issueMenu = Menu(menu, tearoff=0)
        issueMenu.add_command(label=LABEL_VIA_DISCORD, command=lambda: webbrowser.open(DISCORD_LINK, new=2))
        issueMenu.add_command(label=LABEL_VIA_GITHUB, command=lambda: webbrowser.open(GITHUB_LINK, new=2))

        helpMenu = Menu(menu, tearoff=0)
        helpMenu.add_cascade(label=LABEL_REPORT_ISSUE, menu=issueMenu)
        helpMenu.add_command(label=LABEL_ABOUT, command=lambda: AboutWindow(self.window))
        menu.add_cascade(label=LABEL_HELP, menu=helpMenu)

        self.window.config(menu=menu)

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

    def addDropdown(self):
        labelSiteDropdown = Label(self.urlFrame, text=LABEL_STREAM_DROPDOWN)
        labelSiteDropdown.grid(row=1, column=0, sticky=NSEW, padx=4, pady=4)
        self.siteDropdown = Combobox(self.urlFrame, textvariable=self.site, state="readonly", values=list(ORDERED_STREAMING_SITES.keys()))
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

    def addOkButton(self):
        buttonOk = Button(self.okFrame, text=LABEL_OPEN_STREAMS, width=50, command=lambda: self.openURL(), anchor=CENTER, relief=RAISED)
        buttonOk.grid(sticky=NSEW, padx=4, pady=4)

    def toggleThumbnail(self):
        if self.hideThumbnail:
            self.window.geometry('380x580')  # I do not know why this works, but for some reason the window adds 20px to the 580 here
            self.labelImage.grid()
            self.hideThumbnail = False
        else:
            self.labelImage.grid_remove()
            self.window.geometry('380x400')
            self.hideThumbnail = True

    def setSelectionModes(self, isMultipleMode, selectionMode):
        if isMultipleMode:
            self.singleSelectMode.set(False)
        else:
            self.multipleSelectMode.set(False)
        self.liveListBox.configure(selectmode=selectionMode)
        self.selectedListBox.configure(selectmode=selectionMode)
        self.liveListBox.selection_clear(0, END)
        self.selectedListBox.selection_clear(0, END)
        self.resetPreview()

    def populateLiveListBox(self):
        for stream in self.liveStreams:
            self.liveListBox.insert(END, stream.stylizedStreamName)

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
                self.liveListBox.insert(END, self.selectedListBox.get(stream))
            for stream in reversed(self.unselectedStreams):
                self.selectedListBox.delete(stream)
            self.selectedListBox.selection_clear(0, END)
            self.unselectedStreams = None
            self.resetPreview()

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
        self.previewImage = ImageTk.PhotoImage(Image.open(FILE_STREAM_PREVIEW))
        self.labelImage.configure(image=self.previewImage)
        self.boxArtImage = ImageTk.PhotoImage(Image.open(FILE_PREVIEW_BOX_ART))
        self.labelBoxArt.configure(image=self.boxArtImage)
        self.setDefaultPreviewLabels()

    def updatePreviewFrame(self, selectedStreamName):
        thisStream = [stream for stream in self.liveStreams if stream.stylizedStreamName == selectedStreamName][0]
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

    def getImageFromURL(self, url, defaultImage) -> ImageTk.PhotoImage:
        try:
            rawData = urlopen(url).read()
            im = Image.open(io.BytesIO(rawData))
            return ImageTk.PhotoImage(im)
        except ValueError:
            return defaultImage

    def refresh(self):
        self.followedStreams = getAllStreamsUserFollows(self.credentials.oauth, self.credentials.user_id)
        refreshStreams = getLiveFollowedStreams(self.credentials.oauth, [self.followedStreams[i:i + 100] for i in range(0, len(self.followedStreams), 100)])
        tmpLiveList = refreshStreams
        tmpSelectedList = []
        for stylizedStreamName in self.selectedListBox.get(0, END):
            stream = [stream for stream in self.liveStreams if stream.stylizedStreamName == stylizedStreamName][0]
            if stream.isLive(refreshStreams):
                tmpSelectedList.append(stream)
            else:
                self.selectedListBox.delete(self.selectedListBox.get(0, END).index(stylizedStreamName))
        self.liveListBox.delete(0, END)
        tmpLiveList = [stream for stream in tmpLiveList if stream.stylizedStreamName not in [stream.stylizedStreamName for stream in tmpSelectedList]]
        for stream in tmpLiveList:
            self.liveListBox.insert(END, stream.stylizedStreamName)
        self.liveStreams = refreshStreams
        self.resetPreview()

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

    def closeWindow(self):
        sys.exit(0)
