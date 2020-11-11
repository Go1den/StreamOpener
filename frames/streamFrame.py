from tkinter import Frame, Label, W, NSEW, Button, StringVar, SE, SW, S, GROOVE, NW, END

from constants.labelConstants import LabelConstants
from constants.miscConstants import MiscConstants
from stream import Stream

class StreamFrame:
    def __init__(self, stream: Stream, parent, scrollWindow, searchFrame, color):
        self.frame = Frame(scrollWindow, relief=GROOVE, highlightbackground=color, highlightcolor=color, highlightthickness=3)
        self.stream = stream
        self.parent = parent
        self.searchFrame = searchFrame

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
        if len(self.stream.streamTitle) > 45:
            self.previewTitle.set(self.stream.streamTitle[:45].encode("ascii", "ignore").decode() + "...")
        else:
            self.previewTitle.set(self.stream.streamTitle.encode("ascii", "ignore").decode())
        self.boxArtImage = self.stream.DEFAULT_BOX_ART
        self.previewImage = self.stream.DEFAULT_STREAM_PREVIEW
        self.previewName.set(self.stream.stylizedStreamName)
        self.previewViewers.set(self.stream.viewerCount + LabelConstants.VIEWERS)

    def addPreview(self):
        self.labelImage = Label(self.previewFrame, image=self.previewImage, bd=1)
        self.labelImage.bind(MiscConstants.BIND_LEFT_MOUSE, lambda x: self.onClick(None))
        self.labelImage.grid(row=1, sticky=W)
        labelTitle = Label(self.previewFrame, textvariable=self.previewTitle, fg="white", bg="black")
        labelTitle.bind(MiscConstants.BIND_LEFT_MOUSE, lambda x: self.onClick(None))
        labelTitle.grid(row=1, sticky=NW, padx=4, pady=4)
        self.labelBoxArt = Label(self.previewFrame, image=self.boxArtImage, bd=1)
        self.labelBoxArt.bind(MiscConstants.BIND_LEFT_MOUSE, lambda x: self.onClick(None))
        self.labelBoxArt.grid(row=1, column=0, sticky=SW, padx=4, pady=4)
        labelName = Label(self.previewFrame, textvariable=self.previewName, fg="white", bg="#b71ef7")
        labelName.bind(MiscConstants.BIND_LEFT_MOUSE, lambda x: self.onClick(None))
        labelName.grid(row=1, sticky=S, padx=4, pady=4)
        labelViewers = Label(self.previewFrame, textvariable=self.previewViewers, fg="white", bg="black")
        labelViewers.bind(MiscConstants.BIND_LEFT_MOUSE, lambda x: self.onClick(None))
        labelViewers.grid(row=1, sticky=SE, padx=4, pady=4)

    def addFilterFrame(self):
        labelFilter = Label(self.filterFrame, text=LabelConstants.FILTER, anchor=W)
        labelFilter.grid(row=0, column=0, sticky=NSEW, padx=(4, 2))
        self.buttonFilterStreamer = Button(self.filterFrame, text=LabelConstants.FILTER_STREAMER, width=10,
                                           command=lambda: self.parent.addFilter(self.stream.stylizedStreamName, None))
        self.buttonFilterStreamer.grid(row=0, column=1, sticky=NSEW, padx=(2, 4), pady=(0, 4))
        self.buttonFilterGame = Button(self.filterFrame, text=LabelConstants.FILTER_GAME, width=10, command=lambda: self.parent.addFilter(None, self.stream.gameTitle))
        self.buttonFilterGame.grid(row=0, column=2, sticky=NSEW, padx=4, pady=(0, 4))
        self.buttonFilterCombined = Button(self.filterFrame, text=LabelConstants.FILTER_COMBO, width=13,
                                           command=lambda: self.parent.addFilter(self.stream.stylizedStreamName, self.stream.gameTitle))
        self.buttonFilterCombined.grid(row=0, column=3, sticky=NSEW, padx=(4, 0), pady=(0, 4))

    def onClick(self, event):
        if self.frame.cget("highlightbackground") == "red":
            self.frame.config(highlightbackground="grey", highlightcolor="grey")
            idx = self.searchFrame.selectedStreamsListbox.get(0, END).index(self.stream.streamName)
            self.searchFrame.selectedStreamsListbox.delete(idx)
        else:
            self.frame.config(highlightbackground="red", highlightcolor="red")
            self.searchFrame.selectedStreamsListbox.insert(END, self.stream.streamName)
