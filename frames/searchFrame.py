from tkinter import Frame, Label, Button, messagebox, W, Listbox, Scrollbar, MULTIPLE, NONE, NSEW, StringVar, CENTER, RAISED
from tkinter.ttk import Combobox

from constants.labelConstants import LabelConstants
from constants.urlConstants import URLConstants

class SearchFrame:
    def __init__(self, window):
        self.frame = Frame(window)
        self.parent = window

        self.site = StringVar()

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
        self.comboboxTeam = Combobox(self.filterFrame, values=[1, 2, 3, 4], state="readonly")
        self.comboboxTeam.grid(row=2, column=0, padx=4, pady=4)
        self.buttonTeam = Button(self.filterFrame, text=LabelConstants.ADD, width=8, command=lambda: self.addFilter())
        self.buttonTeam.grid(row=2, column=1, padx=4, pady=4)

        labelTag = Label(self.filterFrame, text=LabelConstants.SEARCH_TAG)
        labelTag.grid(row=3, column=0, sticky=W, columnspan=2, padx=4, pady=4)
        self.comboboxTag = Combobox(self.filterFrame, values=[1, 2, 3, 4], state="readonly")
        self.comboboxTag.grid(row=4, column=0, padx=4, pady=4)
        self.buttonTag = Button(self.filterFrame, text=LabelConstants.ADD, width=8, command=lambda: self.addFilter())
        self.buttonTag.grid(row=4, column=1, padx=4, pady=4)

    def populateAppliedFilterFrame(self):
        labelAppliedFilters = Label(self.appliedFilterFrame, text=LabelConstants.APPLIED_FILTERS)
        labelAppliedFilters.grid(row=0, column=0, sticky=W, columnspan=2, padx=4, pady=4)
        scrollbarAppliedFilters = Scrollbar(self.appliedFilterFrame)
        scrollbarAppliedFilters.grid(row=1, column=1, sticky="NWS")
        self.appliedFiltersListbox = Listbox(self.appliedFilterFrame, selectmode=MULTIPLE, yscrollcommand=scrollbarAppliedFilters.set, activestyle=NONE, width=33)
        scrollbarAppliedFilters.config(command=self.appliedFiltersListbox.yview)
        self.appliedFiltersListbox.grid(row=1, column=0, sticky=NSEW, padx=(4, 0))
        self.appliedFiltersListbox.configure(exportselection=False)

    def populateButtonFrame(self):
        self.buttonRemove = Button(self.appliedFilterButtonFrame, text=LabelConstants.REMOVE, width=18, command=lambda: self.removeSelected())
        self.buttonRemove.grid(row=0, column=0, sticky=NSEW, padx=4, pady=4)
        self.buttonReset = Button(self.appliedFilterButtonFrame, text=LabelConstants.RESET, width=8, command=lambda: self.reset())
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
        self.siteDropdown = Combobox(self.urlFrame, textvariable=self.site, state="readonly", values=list(URLConstants.ORDERED_STREAMING_SITES.keys()))
        self.siteDropdown.bind("<<ComboboxSelected>>", self.updateURLSetting)
        self.siteDropdown.grid(row=1, column=0, sticky=NSEW, padx=4, pady=4)

    def populateStreamButtonFrame(self):
        self.buttonOk = Button(self.streamButtonFrame, text=LabelConstants.OPEN_STREAMS, width=28, command=lambda: self.openURL())
        self.buttonOk.grid(row=0, column=0, sticky=NSEW, padx=4, pady=4)

    def addFilter(self):
        messagebox.showinfo("Ok", "Filter added.")

    def removeSelected(self):
        messagebox.showinfo("Ok", "Filters removed.")

    def reset(self):
        messagebox.showinfo("Ok", "Reset")

    def updateURLSetting(self):
        messagebox.showinfo("Ok", "URL updated.")

    def openURL(self):
        messagebox.showinfo("Ok", "URL opened.")

