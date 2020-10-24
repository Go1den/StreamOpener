import webbrowser
from tkinter import Frame, Label, Button, messagebox, W, Listbox, Scrollbar, MULTIPLE, NONE, NSEW, StringVar, GROOVE, END
from tkinter.ttk import Combobox

from constants.labelConstants import LabelConstants
from constants.messageConstants import MessageConstants
from constants.miscConstants import MiscConstants
from constants.urlConstants import URLConstants
from fileHandler import writeSettings

class SearchFrame:
    def __init__(self, parent):
        self.parent = parent
        self.frame = Frame(self.parent.windowFrame, relief=GROOVE, highlightbackground="grey", highlightcolor="grey", highlightthickness=1)

        self.site = StringVar()
        self.currentTeam = StringVar()

        self.filterFrame = Frame(self.frame)
        self.appliedFilterFrame = Frame(self.frame)
        self.appliedFilterButtonFrame = Frame(self.frame)
        self.selectedStreamsFrame = Frame(self.frame)
        self.urlFrame = Frame(self.frame)
        self.streamButtonFrame = Frame(self.frame)

        self.comboboxTeam = None
        self.buttonTeam = None
        self.comboboxTag = None
        self.buttonTag = None
        self.appliedFiltersListbox = None
        self.buttonRemove = None
        self.buttonReset = None
        self.selectedStreamsListbox = None
        self.siteDropdown = None
        self.buttonOk = None

        self.gridFrames()

        self.populateFilterFrame()
        self.populateAppliedFilterFrame()
        self.populateButtonFrame()
        self.populateSelectedStreamsFrame()
        self.populateUrlFrame()
        self.populateStreamButtonFrame()

    def gridFrames(self):
        self.filterFrame.grid(row=0, sticky=NSEW)
        self.appliedFilterFrame.grid(row=1, sticky=NSEW)
        self.appliedFilterButtonFrame.grid(row=2, sticky=NSEW)
        self.selectedStreamsFrame.grid(row=3, sticky=NSEW)
        self.urlFrame.grid(row=4, sticky=NSEW)
        self.streamButtonFrame.grid(row=5, sticky=NSEW)

    def populateFilterFrame(self):
        labelFilters = Label(self.filterFrame, text=LabelConstants.FILTERS)
        labelFilters.grid(row=0, column=0, sticky=W, columnspan=2, padx=4, pady=4)

        labelTeam = Label(self.filterFrame, text=LabelConstants.SEARCH_TEAMS)
        labelTeam.grid(row=1, column=0, sticky=W, columnspan=2, padx=4, pady=4)
        self.comboboxTeam = Combobox(self.filterFrame, textvariable=self.currentTeam, values=list(self.parent.teams.keys()), state="readonly", width=32)
        self.comboboxTeam.grid(row=2, column=0, columnspan=2, padx=4, pady=4)

    def populateAppliedFilterFrame(self):
        labelAppliedFilters = Label(self.appliedFilterFrame, text=LabelConstants.SEARCH_TAG)
        labelAppliedFilters.grid(row=0, column=0, sticky=W, columnspan=2, padx=4, pady=4)
        scrollbarAppliedFilters = Scrollbar(self.appliedFilterFrame)
        scrollbarAppliedFilters.grid(row=1, column=1, sticky="NWS")
        self.appliedFiltersListbox = Listbox(self.appliedFilterFrame, selectmode=MULTIPLE, yscrollcommand=scrollbarAppliedFilters.set, activestyle=NONE, width=33)
        scrollbarAppliedFilters.config(command=self.appliedFiltersListbox.yview)
        self.populateTwitchTagsListbox()
        self.appliedFiltersListbox.grid(row=1, column=0, sticky=NSEW, padx=(4, 0))
        self.appliedFiltersListbox.configure(exportselection=False)

    def populateTwitchTagsListbox(self):
        self.appliedFiltersListbox.delete(0, END)
        activeTags = [tag for tag in self.parent.tags if tag.isActive]
        for tag in list(map(lambda x: x.localizationNames['en-us'], activeTags)):
            self.appliedFiltersListbox.insert(END, tag)

    def populateButtonFrame(self):
        self.buttonRemove = Button(self.appliedFilterButtonFrame, text=LabelConstants.CLEAR_ALL, width=13, command=lambda: self.clearAll())
        self.buttonRemove.grid(row=0, column=0, sticky=NSEW, padx=4, pady=4)
        self.buttonReset = Button(self.appliedFilterButtonFrame, text=LabelConstants.APPLY_TAGS, width=13, command=lambda: self.applyTags())
        self.buttonReset.grid(row=0, column=1, sticky=NSEW, padx=4, pady=4)

    def populateSelectedStreamsFrame(self):
        labelSelectedStreamsFrame = Label(self.selectedStreamsFrame, text=LabelConstants.SELECTED_STREAMS)
        labelSelectedStreamsFrame.grid(row=0, column=0, sticky=W, columnspan=2, padx=4, pady=4)
        scrollbarSelectedStreams = Scrollbar(self.selectedStreamsFrame)
        scrollbarSelectedStreams.grid(row=1, column=1, sticky="NWS")
        self.selectedStreamsListbox = Listbox(self.selectedStreamsFrame, selectmode=MULTIPLE, yscrollcommand=scrollbarSelectedStreams.set, activestyle=NONE, width=33)
        scrollbarSelectedStreams.config(command=self.selectedStreamsListbox.yview)
        self.selectedStreamsListbox.grid(row=1, column=0, sticky=NSEW, padx=(4, 0))
        self.selectedStreamsListbox.configure(exportselection=False)

    def populateUrlFrame(self):
        labelSiteDropdown = Label(self.urlFrame, text=LabelConstants.STREAM_DROPDOWN)
        labelSiteDropdown.grid(row=0, column=0, sticky=W, padx=4, pady=4)
        self.siteDropdown = Combobox(self.urlFrame, textvariable=self.site, state="readonly", values=list(URLConstants.ORDERED_STREAMING_SITES.keys()), width=32)
        self.siteDropdown.bind("<<ComboboxSelected>>", self.updateURLSetting)
        self.siteDropdown.grid(row=1, column=0, sticky=NSEW, padx=4, pady=4)

    def populateStreamButtonFrame(self):
        self.buttonOk = Button(self.streamButtonFrame, text=LabelConstants.OPEN_STREAMS, width=30, command=lambda: self.openURL())
        self.buttonOk.grid(row=0, column=0, sticky=NSEW, padx=4, pady=25)

    def addFilter(self):
        messagebox.showinfo("Ok", "Filter added.")

    def clearAll(self):
        self.appliedFiltersListbox.selection_clear(0, END)

    def applyTags(self):
        messagebox.showinfo("Ok", "Reset")

    def updateURLSetting(self, event=None):
        self.parent.settings[LabelConstants.SETTINGS_JSON][MiscConstants.KEY_OPEN_STREAMS_ON] = self.siteDropdown.get()
        writeSettings(self.parent.settings)

    def openURL(self):
        finalURL = URLConstants.ORDERED_STREAMING_SITES.get(self.siteDropdown.get())
        isRareDrop = finalURL == URLConstants.RAREDROP
        watchingSingleStreamOnTwitch = False
        if len(self.selectedStreamsListbox.get(0, END)) == 1 and finalURL != URLConstants.TWITCH and messagebox.askyesno(LabelConstants.TWITCH, MessageConstants.WATCH_ON_TWITCH):
            finalURL = URLConstants.TWITCH
            watchingSingleStreamOnTwitch = True
        if not watchingSingleStreamOnTwitch and not self.siteDropdown.get():
            messagebox.showerror(LabelConstants.ERROR, MessageConstants.NO_SITE_SELECTED)
        elif len(self.selectedStreamsListbox.get(0, END)) > 0:
            if finalURL == URLConstants.TWITCH:
                for stream in self.selectedStreamsListbox.get(0, END):
                    webbrowser.open(finalURL + stream, new=2)
            else:
                for stream in self.selectedStreamsListbox.get(0, END):
                    if isRareDrop:
                        finalURL += "t" + stream + "/"
                    else:
                        finalURL += stream + "/"
                webbrowser.open(finalURL, new=2)
        else:
            messagebox.showerror(LabelConstants.ERROR, MessageConstants.NO_STREAMS_SELECTED)
