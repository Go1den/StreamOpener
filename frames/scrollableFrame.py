from tkinter import ttk, NSEW, Canvas, SW, messagebox, BooleanVar, END
from typing import List

from PIL import ImageTk, Image

from constants.fileConstants import FileConstants
from constants.labelConstants import LabelConstants
from constants.messageConstants import MessageConstants
from constants.miscConstants import MiscConstants
from fileHandler import writeFilters, readFilters, writeSettings, readTeams
from frames.streamFrame import StreamFrame
from stream import Stream
from twitchapi import getAllStreamsUserFollows, getLiveFollowedStreams

class ScrollableFrame(ttk.Frame):
    def __init__(self, width, height, parent, *args, **kwargs):
        super().__init__(parent.windowFrame, *args, **kwargs)
        self.canvas = Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.streamFrames = []
        self.parent = parent
        self.searchFrame = self.parent.searchFrame
        self.windowFrame = self.parent.windowFrame
        self.currentRow = 0
        self.currentColumn = 0
        self.filters = readFilters()
        self.enableFilters = BooleanVar()

        self.applySettings()

        self.DEFAULT_STREAM_PREVIEW = ImageTk.PhotoImage(Image.open(FileConstants.STREAM_PREVIEW))

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set, width=width, height=height)
        self.canvas.grid(row=0, column=0, sticky=NSEW, padx=(4, 0), pady=4)
        self.scrollbar.grid(row=0, column=1, sticky=NSEW, padx=(0, 4), pady=4)
        self.scrollable_frame.bind('<Enter>', self.bindMouseWheel)
        self.scrollable_frame.bind('<Leave>', self.unbindMouseWheel)
        self.refresh()

    def applySettings(self):
        if MiscConstants.KEY_FILTERS in self.parent.settings[LabelConstants.SETTINGS_JSON]:
            self.enableFilters.set(self.parent.settings[LabelConstants.SETTINGS_JSON][MiscConstants.KEY_FILTERS])

    def bindMouseWheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self.onMouseWheel)

    def unbindMouseWheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def onMouseWheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def addStreamFrame(self, stream):
        color = "red" if stream.streamName in self.parent.searchFrame.selectedStreamsListbox.get(0, END) else "grey"
        streamFrame = StreamFrame(stream, self, self.scrollable_frame, self.searchFrame, color)
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
                messagebox.showinfo(LabelConstants.INFO, MessageConstants.FILTER_ADDED.format(newFilter["description"]))
                if self.enableFilters.get():
                    self.refresh()
            else:
                messagebox.showerror(LabelConstants.ERROR, MessageConstants.FILTER_ALREADY_EXISTS)

    def setFilters(self, newFilters):
        self.filters = newFilters
        writeFilters(self.filters)
        if self.enableFilters.get():
            self.refresh()

    def isFiltered(self, stream):
        if self.enableFilters.get():
            isGameFiltered = stream.gameTitle in [x["description"] for x in self.filters["filters"][LabelConstants.FILTER_KEY_GAME]]
            isStreamFiltered = stream.stylizedStreamName in [x["description"] for x in self.filters["filters"][LabelConstants.FILTER_KEY_STREAMER]]
            isComboFiltered = stream.stylizedStreamName + " streaming " + stream.gameTitle in [x["description"] for x in
                                                                                               self.filters["filters"][LabelConstants.FILTER_KEY_COMBINED]]
            return isGameFiltered or isStreamFiltered or isComboFiltered
        return False

    def toggleFilters(self):
        self.parent.settings[LabelConstants.SETTINGS_JSON][MiscConstants.KEY_FILTERS] = self.enableFilters.get()
        writeSettings(self.parent.settings)
        self.refresh()

    def refresh(self, event=None):
        self.parent.followedStreams = getAllStreamsUserFollows(self.parent.credentials.oauth, self.parent.credentials.user_id)
        self.parent.teams = readTeams(self.parent.followedStreams)
        refreshStreams = getLiveFollowedStreams(self.parent.credentials.oauth, [self.parent.followedStreams[i:i + 100] for i in range(0, len(self.parent.followedStreams), 100)])
        tmpLiveList = refreshStreams
        for streamName in self.parent.searchFrame.selectedStreamsListbox.get(0, END):
            stream = [stream for stream in self.parent.liveStreams if stream.streamName == streamName][0]
            if not stream.isLive(refreshStreams):
                self.parent.searchFrame.selectedStreamsListbox.delete(self.parent.searchFrame.selectedStreamsListbox.get(0, END).index(streamName))
        currentTeamMembers = [streamName for streamName in self.parent.teams[self.parent.searchFrame.currentTeam.get()]]
        tmpLiveList = [stream for stream in tmpLiveList if not self.isFiltered(stream) and stream.stylizedStreamName in currentTeamMembers]
        self.parent.liveStreams = refreshStreams
        self.parent.settings[LabelConstants.SETTINGS_JSON][MiscConstants.KEY_TEAM] = self.parent.searchFrame.comboboxTeam.get()
        writeSettings(self.parent.settings)
        self.addStreamFrames(tmpLiveList)

    def isNotSelected(self, stream, tmpSelectedList) -> bool:
        return stream not in tmpSelectedList

    def addStreamFrames(self, streams: List[Stream]):
        for streamFrame in self.streamFrames:
            streamFrame.frame.grid_forget()
            streamFrame.frame.destroy()
        self.streamFrames = []
        self.currentRow = 0
        self.currentColumn = 0
        for stream in streams:
            self.addStreamFrame(stream)
        self.enforceSettings()

    def enforceSettings(self):
        if self.parent.hideBoxArt.get():
            self.showBoxArt(False)
        else:
            self.showBoxArt(True)
        if self.parent.hideThumbnail.get():
            self.showThumbnails(False)
        else:
            self.showThumbnails(True)
