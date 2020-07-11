import sys
import webbrowser
from tkinter import StringVar, Tk, Frame, Label, NSEW, Listbox, MULTIPLE, END, Scrollbar, Menu, W
from tkinter.ttk import Combobox

from PIL import ImageTk, Image

from aboutWindow import AboutWindow
from constants import STREAMOPENER_ICON, ORDERED_STREAMING_SITES, LABEL_STREAM_DROPDOWN, LABEL_STREAMOPENER

class Window:
    def __init__(self, streams=None):
        if streams is None:
            streams = []
        self.window = Tk()
        self.site = StringVar()
        self.streams = streams
        self.selectedStreams = []
        self.previewImage = ImageTk.PhotoImage(Image.open("streampreview.png"))
        self.previewTitle = StringVar()
        self.previewName = StringVar()
        self.previewGame = StringVar()
        self.previewViewers = StringVar()

        self.initializeWindow()
        self.addMenu()
        self.addListbox()
        self.addDropdown()
        self.addPreview()

    def initializeWindow(self):
        self.window.iconbitmap(STREAMOPENER_ICON)
        self.window.geometry('400x600')
        self.window.title(LABEL_STREAMOPENER)

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

    def addListbox(self):
        frameListBox = Frame(self.window)
        frameListBox.grid(row=0, column=0, columnspan=2, sticky=NSEW)
        scrollbar = Scrollbar(frameListBox)
        scrollbar.grid(row=0, column=1, sticky="NWS")
        listbox = Listbox(frameListBox, selectmode=MULTIPLE, yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)
        for stream in self.streams:
            listbox.insert(END, stream.stylizedStreamName)
        listbox.bind('<<ListboxSelect>>', self.onSelect)
        listbox.grid(row=0, column=0, sticky=NSEW, padx=4, pady=4)

    def addPreview(self):
        framePreview = Frame(self.window)
        framePreview.grid(row=2, column=0, columnspan=2, sticky=NSEW)
        labelImage = Label(framePreview, image=self.previewImage)
        labelImage.grid(row=0, column=0, columnspan=2, sticky=NSEW)
        labelTitle = Label(framePreview, textvariable=self.previewTitle)
        labelTitle.grid(row=1, column=0, columnspan=2, sticky=W)
        labelName = Label(framePreview, textvariable=self.previewName)
        labelName.grid(row=2, column=0, sticky=W)
        labelViewers = Label(framePreview, textvariable=self.previewViewers)
        labelViewers.grid(row=2, column=1, sticky=W)
        labelGame = Label(framePreview, textvariable=self.previewGame)
        labelGame.grid(row=3, column=0, sticky=W)

    def onSelect(self, event):
        w = event.widget
        if self.selectedStreams:  # if not empty
            # compare last selectionlist with new list and extract the difference
            changedSelection = set(self.selectedStreams).symmetric_difference(set(w.curselection()))
            self.selectedStreams = w.curselection()
        else:
            # if empty, assign current selection
            self.selectedStreams = w.curselection()
            changedSelection = w.curselection()
        # changedSelection should always be a set with only one entry, therefore we can convert it to a lst and extract first entry
        selectedStreamName = w.get(int(list(changedSelection)[0]))
        self.updatePreviewFrame(selectedStreamName)

    def addDropdown(self):
        labelSiteDropdown = Label(self.window, text=LABEL_STREAM_DROPDOWN)
        labelSiteDropdown.grid(row=1, column=0, sticky=NSEW, padx=4, pady=4)
        siteDropdown = Combobox(self.window, textvariable=self.site, state="readonly", values=list(ORDERED_STREAMING_SITES.keys()))
        siteDropdown.grid(row=1, column=1, sticky=NSEW, padx=4, pady=4)

    def updatePreviewFrame(self, selectedStreamName):
        thisStream = [stream for stream in self.streams if stream.stylizedStreamName == selectedStreamName][0]
        self.previewTitle.set(thisStream.streamTitle)
        self.previewGame.set("Game: " + thisStream.gameTitle)
        self.previewName.set("Streamer: " + thisStream.streamName)
        self.previewViewers.set("Viewers: " + thisStream.viewerCount)

    def closeWindow(self):
        sys.exit(0)
