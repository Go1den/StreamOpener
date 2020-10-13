from tkinter import Frame, Label, Button, messagebox, W, Listbox, Scrollbar, MULTIPLE, NONE, NSEW
from tkinter.ttk import Combobox

from constants.labelConstants import LabelConstants

class SearchFrame:
    def __init__(self, window):
        self.frame = Frame(window)
        self.parent = window

        self.filterFrame = Frame(self.frame)
        self.appliedFilterFrame = Frame(self.frame)
        self.appliedFilterButtonFrame = Frame(self.frame)

        self.comboboxTeam = None
        self.buttonTeam = None
        self.comboboxTag = None
        self.buttonTag = None
        self.appliedFiltersListbox = None

        self.gridFrames()

        self.populateFilterFrame()
        self.populateAppliedFilterFrame()
        self.populateButtonFrame()

    def gridFrames(self):
        self.filterFrame.grid(row=0, sticky=NSEW)
        self.appliedFilterFrame.grid(row=1, sticky=NSEW)
        self.appliedFilterButtonFrame.grid(row=2, sticky=NSEW)

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
        self.buttonRemove = Button(self.appliedFilterButtonFrame, text=LabelConstants.RESET, width=8, command=lambda: self.reset())
        self.buttonRemove.grid(row=0, column=1, sticky=NSEW, padx=4, pady=4)

    def addFilter(self):
        messagebox.showinfo("Ok", "Filter added.")

    def removeSelected(self):
        messagebox.showinfo("Ok", "Filters removed.")

    def reset(self):
        messagebox.showinfo("Ok", "Reset")


