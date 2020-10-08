from tkinter import Frame, Label, W, NSEW, Button, StringVar

from PIL import ImageTk, Image

from constants.fileConstants import FileConstants
from constants.labelConstants import LabelConstants

class StreamFrame:
    def __init__(self, stream, window):
        self.frame = Frame(window)
        self.stream = stream
        self.parent = window

        self.previewFrame = Frame(self.frame)
        self.boxArtFrame = Frame(self.previewFrame)
        self.filterFrame = Frame(self.previewFrame)

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

    def setStream(self, stream):
        self.stream = stream
        self.setStringVars()

    def setStringVars(self):
        if len(self.stream.streamTitle) > 50:
            self.previewTitle.set(self.stream.streamTitle[:50] + "...")
        else:
            self.previewTitle.set(self.stream.streamTitle)
        if self.stream.boxArtURL:
            self.boxArtImage = self.stream.boxArtURL
        else:
            self.boxArtImage = ImageTk.PhotoImage(Image.open(FileConstants.PREVIEW_BOX_ART))
        if self.stream.previewImage:
            self.previewImage = self.stream.previewImage
        else:
            self.previewImage = ImageTk.PhotoImage(Image.open(FileConstants.STREAM_PREVIEW))
        self.previewName.set(LabelConstants.STREAMER + self.stream.streamName)
        if len(self.stream.gameTitle) > 45:
            self.previewGame.set(LabelConstants.GAME + self.stream.gameTitle[:45] + "...")
        else:
            self.previewGame.set(LabelConstants.GAME + self.stream.gameTitle)
        self.previewViewers.set(LabelConstants.VIEWERS + self.stream.viewerCount)

    def addPreview(self):
        self.labelImage = Label(self.previewFrame, image=self.previewImage, bd=1)
        self.labelImage.grid(row=0, sticky=W, columnspan=2)
        labelTitle = Label(self.previewFrame, textvariable=self.previewTitle)
        labelTitle.grid(row=1, sticky=W, columnspan=2)
        self.boxArtFrame.grid(row=2, column=0, sticky=NSEW)
        self.labelBoxArt = Label(self.boxArtFrame, image=self.boxArtImage, bd=1)
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
        labelFilter = Label(self.filterFrame, text=LabelConstants.FILTER)
        labelFilter.grid(row=0, column=0, sticky=NSEW, padx=(4, 2), pady=4)
        self.buttonFilterStreamer = Button(self.filterFrame, text=LabelConstants.FILTER_STREAMER, width=13,
                                           command=lambda: self.parent.addFilter(self.stream.stylizedStreamName, None))
        self.buttonFilterStreamer.grid(row=0, column=1, sticky=NSEW, padx=4, pady=4)
        self.buttonFilterGame = Button(self.filterFrame, text=LabelConstants.FILTER_GAME, width=13, command=lambda: self.parent.addFilter(None, self.stream.gameTitle))
        self.buttonFilterGame.grid(row=0, column=2, sticky=NSEW, padx=4, pady=4)
        self.buttonFilterCombined = Button(self.filterFrame, text=LabelConstants.FILTER_COMBO, width=13,
                                           command=lambda: self.parent.addFilter(self.stream.stylizedStreamName, self.stream.gameTitle))
        self.buttonFilterCombined.grid(row=0, column=3, sticky=NSEW, padx=4, pady=4)



