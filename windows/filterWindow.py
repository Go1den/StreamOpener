from copy import deepcopy
from tkinter import Toplevel, Frame, NSEW, Label, Scrollbar, Listbox, MULTIPLE, NONE, END, Button, W

from constants.labelConstants import LabelConstants
from listboxHelper import alphabeticallyInsert
from windows.newFilterWindow import NewFilterWindow
from windows.windowHelper import WindowHelper

class FilterWindow:
    def __init__(self, parent):
        self.window = Toplevel(parent.window)
        self.window.withdraw()
        self.parent = parent
        self.filters = deepcopy(parent.filters)
        self.filterFrame = Frame(self.window)
        self.buttonFrame = Frame(self.window)

        self.filterGameListbox = None
        self.filterStreamListbox = None
        self.filterCombinedListbox = None

        WindowHelper.initializeWindow(self.window, self.parent, 460, 630, 30, 50, LabelConstants.FILTER_WINDOW)
        self.gridFrames()
        self.addFilterListbox()
        self.addButtons()
        WindowHelper.finalizeWindow(self.window, self.parent)

    def gridFrames(self):
        self.filterFrame.grid(row=0, sticky=NSEW, padx=4, pady=4)
        self.buttonFrame.grid(row=1, sticky=NSEW, padx=4, pady=4)

    def addFilterListbox(self):
        labelFilterGameListbox = Label(self.filterFrame, text=LabelConstants.FILTER_GAME_LISTBOX)
        labelFilterGameListbox.grid(row=0, column=0, sticky=W, padx=4, pady=4)
        scrollbarGame = Scrollbar(self.filterFrame)
        scrollbarGame.grid(row=1, column=1, sticky="NWS")
        self.filterGameListbox = Listbox(self.filterFrame, selectmode=MULTIPLE, yscrollcommand=scrollbarGame.set, activestyle=NONE, width=70)
        scrollbarGame.config(command=self.filterGameListbox.yview)
        self.filterGameListbox.grid(row=1, column=0, sticky=NSEW, padx=(4, 0))
        self.filterGameListbox.configure(exportselection=False)
        descriptions = []
        for f in self.filters["filters"]["game"]:
            descriptions.append(f["description"])
        for desc in sorted(descriptions, key=str.casefold):
            self.filterGameListbox.insert(END, desc)

        labelFilterStreamerListbox = Label(self.filterFrame, text=LabelConstants.FILTER_STREAMER_LISTBOX)
        labelFilterStreamerListbox.grid(row=2, column=0, sticky=W, padx=4, pady=4)
        scrollbarStreamer = Scrollbar(self.filterFrame)
        scrollbarStreamer.grid(row=3, column=1, sticky="NWS")
        self.filterStreamListbox = Listbox(self.filterFrame, selectmode=MULTIPLE, yscrollcommand=scrollbarStreamer.set, activestyle=NONE, width=70)
        scrollbarGame.config(command=self.filterStreamListbox.yview)
        self.filterStreamListbox.grid(row=3, column=0, sticky=NSEW, padx=(4, 0))
        self.filterStreamListbox.configure(exportselection=False)
        descriptions = []
        for f in self.filters["filters"]["streamer"]:
            descriptions.append(f["description"])
        for desc in sorted(descriptions, key=str.casefold):
            self.filterStreamListbox.insert(END, desc)

        labelFilterCombinedListbox = Label(self.filterFrame, text=LabelConstants.FILTER_COMBINED_LISTBOX)
        labelFilterCombinedListbox.grid(row=4, column=0, sticky=W, padx=4, pady=4)
        scrollbarCombined = Scrollbar(self.filterFrame)
        scrollbarCombined.grid(row=5, column=1, sticky="NWS")
        self.filterCombinedListbox = Listbox(self.filterFrame, selectmode=MULTIPLE, yscrollcommand=scrollbarCombined.set, activestyle=NONE, width=70)
        scrollbarCombined.config(command=self.filterGameListbox.yview)
        self.filterCombinedListbox.grid(row=5, column=0, sticky=NSEW, padx=(4, 0))
        self.filterCombinedListbox.configure(exportselection=False)
        descriptions = []
        for f in self.filters["filters"]["combined"]:
            descriptions.append(f["description"])
        for desc in sorted(descriptions, key=str.casefold):
            self.filterCombinedListbox.insert(END, desc)

    def addButtons(self):
        buttonNewFilter = Button(self.buttonFrame, text=LabelConstants.NEW_FILTER, width=13, command=lambda: NewFilterWindow(self))
        buttonNewFilter.grid(row=0, column=0, sticky=NSEW, padx=(8, 4), pady=4)
        buttonRemove = Button(self.buttonFrame, text=LabelConstants.DELETE, width=13, command=lambda: self.delete())
        buttonRemove.grid(row=0, column=1, sticky=NSEW, padx=4, pady=4)
        buttonOk = Button(self.buttonFrame, text=LabelConstants.OK, width=13, command=lambda: self.ok())
        buttonOk.grid(row=0, column=2, sticky=NSEW, padx=4, pady=4)
        buttonCancel = Button(self.buttonFrame, text=LabelConstants.CANCEL, width=13, command=lambda: self.window.destroy())
        buttonCancel.grid(row=0, column=3, sticky=NSEW, padx=4, pady=4)

    def delete(self):
        self.deleteByListbox(self.filterGameListbox, LabelConstants.FILTER_KEY_GAME)
        self.deleteByListbox(self.filterStreamListbox, LabelConstants.FILTER_KEY_STREAMER)
        self.deleteByListbox(self.filterCombinedListbox, LabelConstants.FILTER_KEY_COMBINED)

    def deleteByListbox(self, listbox: Listbox, key: str):
        descriptions = []
        for f in reversed(listbox.curselection()):
            descriptions.append(listbox.get(f))
            listbox.delete(f)
        self.filters["filters"][key] = [x for x in self.filters["filters"][key] if x["description"] not in descriptions]

    def ok(self):
        self.parent.setFilters(self.filters)
        self.window.destroy()

    def addFilter(self, key: str, newFilter: dict):
        self.filters["filters"][key].append(newFilter)
        description = newFilter["description"]
        if key == LabelConstants.FILTER_KEY_GAME:
            alphabeticallyInsert(self.filterGameListbox, description)
        elif key == LabelConstants.FILTER_KEY_STREAMER:
            alphabeticallyInsert(self.filterStreamListbox, description)
        elif key == LabelConstants.FILTER_KEY_COMBINED:
            alphabeticallyInsert(self.filterCombinedListbox, description)
