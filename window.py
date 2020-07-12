import io
import sys
import webbrowser
from tkinter import StringVar, Tk, Frame, Label, NSEW, Listbox, MULTIPLE, END, Scrollbar, Menu, W, Button, NONE, GROOVE, messagebox
from tkinter.messagebox import ERROR
from tkinter.ttk import Combobox
from urllib.request import urlopen

from PIL import ImageTk, Image

from aboutWindow import AboutWindow
from constants import STREAMOPENER_ICON, ORDERED_STREAMING_SITES, LABEL_STREAM_DROPDOWN, LABEL_STREAMOPENER
from twitchapi import getLiveFollowedStreams

class Window:
    def __init__(self, oauth=None):
        self.window = Tk()
        self.site = StringVar()
        self.oauth = oauth
        self.streams = getLiveFollowedStreams(self.oauth)
        self.selectedStreams = None
        self.unselectedStreams = None
        self.previewImage = ImageTk.PhotoImage(Image.open("streampreview.png"))
        self.previewTitle = StringVar()
        self.previewName = StringVar()
        self.previewGame = StringVar()
        self.previewViewers = StringVar()

        self.labelImage = None
        self.liveListBox = None
        self.selectedListBox = None
        self.siteDropdown = None

        self.streamFrame = Frame(self.window)
        self.urlFrame = Frame(self.window)
        self.previewFrame = Frame(self.window, bd=2, relief=GROOVE, width=352, height=274)
        self.okFrame = Frame(self.window)

        self.initializeWindow()
        self.gridFrames()
        self.addMenu()
        self.addLiveListbox()
        self.addListBoxButtons()
        self.addSelectedListbox()
        self.addDropdown()
        self.addPreview()
        self.addOkButton()

    def addOkButton(self):
        buttonOk = Button(self.okFrame, text="Take me to the streams!", width=50, command=lambda: self.openURL())
        buttonOk.grid(sticky=NSEW, padx=4, pady=4)

    def initializeWindow(self):
        self.window.iconbitmap(STREAMOPENER_ICON)
        self.window.geometry('376x580')
        self.window.title(LABEL_STREAMOPENER)

    def gridFrames(self):
        self.streamFrame.grid(row=0, sticky=NSEW, padx=4, pady=4)
        self.urlFrame.grid(row=1, sticky=NSEW, padx=4, pady=4)
        self.previewFrame.grid(row=2, sticky=NSEW, padx=(12,4), pady=4)
        self.previewFrame.grid_propagate(False)
        self.okFrame.grid(row=3, sticky=NSEW, padx=(8, 4), pady=4)
        # TODO: Padding is all fricked up

    def addMenu(self):
        menu = Menu(self.window)
        fileMenu = Menu(menu, tearoff=0)

        issueMenu = Menu(menu, tearoff=0)
        issueMenu.add_command(label="via Discord", command=lambda: webbrowser.open('https://discord.gg/nqWxgHm', new=2))
        issueMenu.add_command(label="via Github", command=lambda: webbrowser.open('https://github.com/Go1den/StreamOpener/issues', new=2))

        fileMenu.add_cascade(label="Report Issue", menu=issueMenu)
        fileMenu.add_command(label="Quit", command=lambda: self.closeWindow())
        menu.add_cascade(label="File", menu=fileMenu)

        helpMenu = Menu(menu, tearoff=0)
        helpMenu.add_command(label="About", command=lambda: AboutWindow(self.window))
        menu.add_cascade(label="Help", menu=helpMenu)

        self.window.config(menu=menu)

    def addLiveListbox(self):
        frameLiveListBox = Frame(self.streamFrame)
        frameLiveListBox.grid(row=0, column=0, sticky=NSEW, padx=4, pady=(0, 4))
        labelLiveListBox = Label(frameLiveListBox, text="Live Streams:")
        labelLiveListBox.grid(row=0, column=0, padx=4, sticky=W)
        scrollbar = Scrollbar(frameLiveListBox)
        scrollbar.grid(row=1, column=1, sticky="NWS")
        self.liveListBox = Listbox(frameLiveListBox, selectmode=MULTIPLE, yscrollcommand=scrollbar.set, activestyle=NONE)
        scrollbar.config(command=self.liveListBox.yview)
        self.populateLiveListBox()
        self.liveListBox.bind('<<ListboxSelect>>', self.onSelectLiveListbox)
        self.liveListBox.grid(row=1, column=0, sticky=NSEW, padx=(4, 0))

    def populateLiveListBox(self):
        for stream in self.streams:
            self.liveListBox.insert(END, stream.stylizedStreamName)

    def addListBoxButtons(self):
        frameListBoxButtons = Frame(self.streamFrame)
        frameListBoxButtons.grid(row=0, column=1, sticky=NSEW, pady=(0, 4))
        buttonLeftArrow = Button(frameListBoxButtons, text="<--", width=7, command=lambda: self.unselectStreams())
        buttonLeftArrow.grid(row=0, sticky=NSEW, padx=4, pady=(38, 4))
        buttonReset = Button(frameListBoxButtons, text="Reset", width=7, command=lambda: self.reset())
        buttonReset.grid(row=1, sticky=NSEW, padx=4, pady=4)
        buttonRefresh = Button(frameListBoxButtons, text="Refresh", width=7, command=lambda: self.refresh())
        buttonRefresh.grid(row=2, sticky=NSEW, padx=4, pady=4)
        buttonRightArrow = Button(frameListBoxButtons, text="-->", width=7, command=lambda: self.selectStreams())
        buttonRightArrow.grid(row=3, sticky=NSEW, padx=4, pady=4)

    def addSelectedListbox(self):
        frameSelectedListBox = Frame(self.streamFrame)
        frameSelectedListBox.grid(row=0, column=2, sticky=NSEW, pady=(0, 4))
        labelLiveListBox = Label(frameSelectedListBox, text="Selected Streams:")
        labelLiveListBox.grid(row=0, column=0, padx=4, sticky=W)
        scrollbar = Scrollbar(frameSelectedListBox)
        scrollbar.grid(row=1, column=1, sticky="NWS")
        self.selectedListBox = Listbox(frameSelectedListBox, selectmode=MULTIPLE, yscrollcommand=scrollbar.set, activestyle=NONE)
        scrollbar.config(command=self.selectedListBox.yview)
        self.selectedListBox.bind('<<ListboxSelect>>', self.onSelectSelectedListBox)
        self.selectedListBox.grid(row=1, column=0, sticky=NSEW, padx=(4, 0))

    def addPreview(self):
        self.previewTitle.set("Title will appear here.")
        self.previewGame.set("Game: ")
        self.previewName.set("Streamer: ")
        self.previewViewers.set("Viewers: ")
        self.labelImage = Label(self.previewFrame, image=self.previewImage)
        self.labelImage.grid(row=0)
        labelTitle = Label(self.previewFrame, textvariable=self.previewTitle)
        labelTitle.grid(row=1, sticky=W)
        labelName = Label(self.previewFrame, textvariable=self.previewName)
        labelName.grid(row=2, sticky=W)
        labelGame = Label(self.previewFrame, textvariable=self.previewGame)
        labelGame.grid(row=3, sticky=W)
        labelViewers = Label(self.previewFrame, textvariable=self.previewViewers)
        labelViewers.grid(row=4, sticky=W)

    def onSelectLiveListbox(self, event):
        w = event.widget
        if self.selectedStreams:
            changedSelection = set(self.selectedStreams).symmetric_difference(set(w.curselection()))
            self.selectedStreams = w.curselection()
        else:
            self.selectedStreams = w.curselection()
            changedSelection = w.curselection()
        selectedStreamName = w.get(int(list(changedSelection)[0]))
        self.updatePreviewFrame(selectedStreamName)
        print(self.selectedStreams)

    def onSelectSelectedListBox(self, event):
        w = event.widget
        if self.unselectedStreams:
            changedSelection = set(self.unselectedStreams).symmetric_difference(set(w.curselection()))
            self.unselectedStreams = w.curselection()
        else:
            self.unselectedStreams = w.curselection()
            changedSelection = w.curselection()
        unselectedStreamName = w.get(int(list(changedSelection)[0]))
        self.updatePreviewFrame(unselectedStreamName)
        print(self.unselectedStreams)

    def selectStreams(self):
        if self.selectedStreams:
            for stream in self.selectedStreams:
                self.selectedListBox.insert(END, self.liveListBox.get(stream))
            for stream in reversed(self.selectedStreams):
                self.liveListBox.delete(stream)
            self.liveListBox.selection_clear(0, END)
            self.selectedStreams = None

    def unselectStreams(self):
        if self.unselectedStreams:
            for stream in self.unselectedStreams:
                self.liveListBox.insert(END, self.selectedListBox.get(stream))
            for stream in reversed(self.unselectedStreams):
                self.selectedListBox.delete(stream)
            self.selectedListBox.selection_clear(0, END)
            self.unselectedStreams = None

    def reset(self):
        self.liveListBox.selection_clear(0, END)
        self.liveListBox.delete(0, END)
        self.selectedListBox.selection_clear(0, END)
        self.selectedListBox.delete(0, END)
        self.populateLiveListBox()
        self.selectedStreams = None
        self.unselectedStreams = None
        self.previewImage = ImageTk.PhotoImage(Image.open("streampreview.png"))
        self.labelImage.configure(image=self.previewImage)

    def addDropdown(self):
        labelSiteDropdown = Label(self.urlFrame, text=LABEL_STREAM_DROPDOWN)
        labelSiteDropdown.grid(row=1, column=0, sticky=NSEW, padx=4, pady=4)
        self.siteDropdown = Combobox(self.urlFrame, textvariable=self.site, state="readonly", values=list(ORDERED_STREAMING_SITES.keys()))
        self.siteDropdown.grid(row=1, column=1, sticky=NSEW, padx=4, pady=4)

    def updatePreviewFrame(self, selectedStreamName):
        thisStream = [stream for stream in self.streams if stream.stylizedStreamName == selectedStreamName][0]
        if len(thisStream.streamTitle) > 50:
            self.previewTitle.set(thisStream.streamTitle[:50] + "...")
        else:
            self.previewTitle.set(thisStream.streamTitle)
        self.previewGame.set("Game: " + thisStream.gameTitle)
        self.previewName.set("Streamer: " + thisStream.streamName)
        self.previewViewers.set("Viewers: " + thisStream.viewerCount)
        self.getImageFromURL(thisStream.previewImage)

    def getImageFromURL(self, url):
        rawData = urlopen(url).read()
        im = Image.open(io.BytesIO(rawData))
        self.previewImage = ImageTk.PhotoImage(im)
        self.labelImage.configure(image=self.previewImage)

    def refresh(self):
        getLiveFollowedStreams(self.oauth)
        # TODO: refresh lists

    def openURL(self):
        watchingOnTwitch = False
        if len(self.selectedListBox.get(0, END)) == 1 and messagebox.askyesno("Twitch", "Only one stream was selected. Would you like to watch on Twitch instead of your selected site?"):
            finalURL = "https://twitch.tv/"
            watchingOnTwitch = True
        if not watchingOnTwitch and not self.siteDropdown.get():
            messagebox.showerror("Error", "No website selected.")
        elif len(self.selectedListBox.get(0, END)) > 0:
            if not watchingOnTwitch:
                finalURL = ORDERED_STREAMING_SITES.get(self.siteDropdown.get())
            for selectedStream in self.selectedListBox.get(0, END):
                for stream in self.streams:
                    if stream.stylizedStreamName == selectedStream:
                        finalURL += stream.streamName + "/"
            webbrowser.open(finalURL, new=2)
        else:
            messagebox.showerror("Error", "No streams selected.")

    def closeWindow(self):
        sys.exit(0)
