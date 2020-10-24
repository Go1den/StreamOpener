from tkinter import ttk, NSEW, Canvas, SW

from PIL import ImageTk, Image

from constants.fileConstants import FileConstants
from frames.streamFrame import StreamFrame

class ScrollableFrame(ttk.Frame):
    def __init__(self, width, height, searchFrame, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.streamFrames = []
        self.searchFrame = searchFrame
        self.windowFrame = container
        self.currentRow = 0
        self.currentColumn = 0

        self.DEFAULT_STREAM_PREVIEW = ImageTk.PhotoImage(Image.open(FileConstants.STREAM_PREVIEW))

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set, width=width, height=height)
        self.canvas.grid(row=0, column=0, sticky=NSEW, padx=(4, 0), pady=4)
        self.scrollbar.grid(row=0, column=1, sticky=NSEW, padx=(0, 4), pady=4)
        self.scrollable_frame.bind('<Enter>', self.bindMouseWheel)
        self.scrollable_frame.bind('<Leave>', self.unbindMouseWheel)

    def bindMouseWheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self.onMouseWheel)

    def unbindMouseWheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def onMouseWheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def addStreamFrame(self, stream):
        streamFrame = StreamFrame(stream, self.windowFrame.master, self.scrollable_frame, self.searchFrame)
        streamFrame.frame.grid(row=self.currentRow, column=self.currentColumn, sticky=NSEW, padx=4, pady=4)
        self.streamFrames.append(streamFrame)
        self.currentColumn += 1
        if self.currentColumn == 3:
            self.currentRow += 1
            self.currentColumn = 0

    def showThumbnails(self, showThumbnails):
        for streamFrame in self.streamFrames:
            if showThumbnails:
                streamFrame.labelImage.configure(image=streamFrame.previewImage)
            else:
                streamFrame.labelImage.configure(image=self.DEFAULT_STREAM_PREVIEW)

    def showBoxArt(self, showBoxArt):
        for streamFrame in self.streamFrames:
            if showBoxArt:
                streamFrame.labelBoxArt.grid(row=1, column=0, sticky=SW, padx=4, pady=4)
            else:
                streamFrame.labelBoxArt.grid_forget()

    def updateStreamFrameBorders(self, selectedStreams):
        for streamFrame in self.streamFrames:
            if streamFrame.stream.streamName not in selectedStreams:
                streamFrame.frame.config(highlightbackground="grey", highlightcolor="grey")

