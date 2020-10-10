import io
from tkinter import Frame, Label, W, NSEW, Button, StringVar, SE, SW, S, GROOVE, NW
from urllib.request import urlopen

from PIL import ImageTk, Image

from constants.fileConstants import FileConstants
from constants.labelConstants import LabelConstants

class StreamFrame:
    def __init__(self, stream, window):
        self.frame = Frame(window, relief=GROOVE, bd=2)
        self.stream = stream
        self.parent = window

        self.previewFrame = Frame(self.frame)
        self.boxFrame = Frame(self.frame)
        self.boxArtFrame = Frame(self.boxFrame)
        self.boxArtLabelFrame = Frame(self.boxFrame)
        self.filterFrame = Frame(self.frame)

        self.labelImage = None
        self.labelBoxArt = None
        self.buttonFilterGame = None
        self.buttonFilterStreamer = None
        self.buttonFilterCombined = None

        self.previewTitle = StringVar()
        self.previewImage = None
        self.boxArtImage = None
        self.previewName = StringVar()
        self.previewGame = StringVar()
        self.previewViewers = StringVar()

        self.setStringVars()
        self.addPreview()
        self.addFilterFrame()
        self.gridFrames()

    def gridFrames(self):
        self.previewFrame.grid(row=0, sticky=NSEW)
        self.boxFrame.grid(row=1, sticky=NSEW)
        self.boxArtFrame.grid(row=0, column=0, sticky=NSEW)
        self.boxArtLabelFrame.grid(row=0, column=1, sticky=W)
        self.filterFrame.grid(row=2, sticky=NSEW)

    def setStream(self, stream):
        self.stream = stream
        self.setStringVars()

    def setStringVars(self):
        if len(self.stream.streamTitle) > 50:
            self.previewTitle.set(self.stream.streamTitle[:50] + "...")
        else:
            self.previewTitle.set(self.stream.streamTitle)
        if self.stream.boxArtURL:
            self.boxArtImage = self.getImageFromURL(self.stream.boxArtURL, ImageTk.PhotoImage(Image.open(FileConstants.PREVIEW_BOX_ART)))
        else:
            self.boxArtImage = ImageTk.PhotoImage(Image.open(FileConstants.PREVIEW_BOX_ART))
        if self.stream.previewImage:
            self.previewImage = self.getImageFromURL(self.stream.previewImage, ImageTk.PhotoImage(Image.open(FileConstants.STREAM_PREVIEW)))
        else:
            self.previewImage = ImageTk.PhotoImage(Image.open(FileConstants.STREAM_PREVIEW))
        self.previewName.set(self.stream.streamName)
        if len(self.stream.gameTitle) > 45:
            self.previewGame.set(LabelConstants.GAME + self.stream.gameTitle[:45] + "...")
        else:
            self.previewGame.set(LabelConstants.GAME + self.stream.gameTitle)
        self.previewViewers.set(self.stream.viewerCount + LabelConstants.VIEWERS)

    def addPreview(self):
        self.labelImage = Label(self.previewFrame, image=self.previewImage, bd=1)
        self.labelImage.grid(row=1, sticky=W)
        labelTitle = Label(self.previewFrame, textvariable=self.previewTitle)
        labelTitle.grid(row=1, sticky=NW, padx=4, pady=4)
        self.labelBoxArt = Label(self.previewFrame, image=self.boxArtImage, bd=1)
        self.labelBoxArt.grid(row=1, column=0, sticky=SW, padx=4, pady=4)
        labelName = Label(self.previewFrame, textvariable=self.previewName)
        labelName.grid(row=1, sticky=S, padx=4, pady=4)
        labelViewers = Label(self.previewFrame, textvariable=self.previewViewers)
        labelViewers.grid(row=1, sticky=SE, padx=4, pady=4)

    def addFilterFrame(self):
        labelFilter = Label(self.filterFrame, text=LabelConstants.FILTER, anchor=W)
        labelFilter.grid(row=0, column=0, sticky=NSEW, padx=(4, 2), pady=(4, 0))
        self.buttonFilterStreamer = Button(self.filterFrame, text=LabelConstants.FILTER_STREAMER, width=10,
                                           command=lambda: self.parent.addFilter(self.stream.stylizedStreamName, None))
        self.buttonFilterStreamer.grid(row=0, column=1, sticky=NSEW, padx=(2, 4), pady=4)
        self.buttonFilterGame = Button(self.filterFrame, text=LabelConstants.FILTER_GAME, width=10, command=lambda: self.parent.addFilter(None, self.stream.gameTitle))
        self.buttonFilterGame.grid(row=0, column=2, sticky=NSEW, padx=4, pady=4)
        self.buttonFilterCombined = Button(self.filterFrame, text=LabelConstants.FILTER_COMBO, width=13,
                                           command=lambda: self.parent.addFilter(self.stream.stylizedStreamName, self.stream.gameTitle))
        self.buttonFilterCombined.grid(row=0, column=3, sticky=NSEW, padx=4, pady=4)

    def getImageFromURL(self, url, defaultImage) -> ImageTk.PhotoImage:
        try:
            rawData = urlopen(url).read()
            im = Image.open(io.BytesIO(rawData))
            return ImageTk.PhotoImage(im)
        except ValueError:
            return defaultImage
