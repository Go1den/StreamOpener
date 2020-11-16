from copy import deepcopy
from tkinter import Toplevel, Frame, NSEW, NONE, Listbox, Label, Scrollbar, W, Button, END, E, EXTENDED

from constants.labelConstants import LabelConstants
from listboxHelper import alphabeticallyInsert
from windows.updatingTwitchTagsWindow import UpdatingTwitchTagsWindow
from windows.windowHelper import WindowHelper

class TagWindow:
    def __init__(self, parent):
        self.window = Toplevel(parent.window)
        self.window.withdraw()
        self.parent = parent
        self.tags = deepcopy(parent.tags)
        self.activeFrame = Frame(self.window)
        self.upDownButtonFrame = Frame(self.window)
        self.inactiveFrame = Frame(self.window)
        self.okCancelFrame = Frame(self.window)

        self.selectedActive = None
        self.selectedInactive = None

        self.activeListbox = None
        self.inactiveListbox = None

        WindowHelper.initializeWindow(self.window, self.parent, 460, 514, 30, 50, LabelConstants.TAG_WINDOW)
        self.gridFrames()
        self.addActiveListbox()
        self.addMoveButtons()
        self.addInactiveListbox()
        self.addOkCancelButtons()
        self.populateListboxes()
        WindowHelper.finalizeWindow(self.window, self.parent)

    def gridFrames(self):
        self.activeFrame.grid(row=0, sticky=NSEW, padx=4, pady=4)
        self.upDownButtonFrame.grid(row=1, sticky=NSEW, padx=4, pady=4)
        self.inactiveFrame.grid(row=2, sticky=NSEW, padx=4, pady=4)
        self.okCancelFrame.grid(row=3, sticky=E, padx=4, pady=4)

    def addActiveListbox(self):
        labelExplain = Label(self.activeFrame, text=LabelConstants.EXTENDED_MODE)
        labelExplain.grid(row=0, column=0, sticky=W, padx=4, pady=(0,4))
        labelActiveListbox = Label(self.activeFrame, text=LabelConstants.ACTIVE_TAGS)
        labelActiveListbox.grid(row=1, column=0, sticky=W, padx=4, pady=4)
        scrollbarActive = Scrollbar(self.activeFrame)
        scrollbarActive.grid(row=2, column=1, sticky="NWS")
        self.activeListbox = Listbox(self.activeFrame, selectmode=EXTENDED, yscrollcommand=scrollbarActive.set, activestyle=NONE, width=70)
        scrollbarActive.config(command=self.activeListbox.yview)
        self.activeListbox.bind('<<ListboxSelect>>', self.onSelectActiveListbox)
        self.activeListbox.grid(row=2, column=0, sticky=NSEW, padx=(4, 0))

    def addMoveButtons(self):
        buttonUp = Button(self.upDownButtonFrame, text=LabelConstants.UP, width=13, command=lambda: self.moveUp())
        buttonUp.grid(row=0, column=0, sticky=NSEW, padx=(116, 4), pady=4)
        buttonDown = Button(self.upDownButtonFrame, text=LabelConstants.DOWN, width=13, command=lambda: self.moveDown())
        buttonDown.grid(row=0, column=1, sticky=NSEW, padx=(20, 4), pady=4)

    def addInactiveListbox(self):
        labelInactiveListbox = Label(self.inactiveFrame, text=LabelConstants.INACTIVE_TAGS)
        labelInactiveListbox.grid(row=0, column=0, sticky=W, padx=4, pady=4)
        scrollbarInactive = Scrollbar(self.inactiveFrame)
        scrollbarInactive.grid(row=1, column=1, sticky="NWS")
        self.inactiveListbox = Listbox(self.inactiveFrame, selectmode=EXTENDED, yscrollcommand=scrollbarInactive.set, activestyle=NONE, width=70)
        scrollbarInactive.config(command=self.inactiveListbox.yview)
        self.inactiveListbox.bind('<<ListboxSelect>>', self.onSelectInactiveListbox)
        self.inactiveListbox.grid(row=1, column=0, sticky=NSEW, padx=(4, 0))

    def addOkCancelButtons(self):
        buttonUpdateTags = Button(self.okCancelFrame, text=LabelConstants.UPDATE_TAGS, width=26, command=lambda: self.updateTagLibrary())
        buttonUpdateTags.grid(row=0, column=1, sticky=E, padx=4, pady=4)
        buttonOk = Button(self.okCancelFrame, text=LabelConstants.OK, width=13, command=lambda: self.ok())
        buttonOk.grid(row=0, column=2, sticky=E, padx=4, pady=4)
        buttonCancel = Button(self.okCancelFrame, text=LabelConstants.CANCEL, width=13, command=lambda: self.close())
        buttonCancel.grid(row=0, column=3, sticky=E, padx=(4, 0), pady=4)

    def populateListboxes(self):
        self.activeListbox.delete(0, END)
        self.inactiveListbox.delete(0, END)
        descriptions = []
        for tag in filter(lambda t: t.isActive, self.tags):
            descriptions.append(tag.localizationNames["en-us"])
        for desc in sorted(descriptions, key=str.casefold):
            self.activeListbox.insert(END, desc)
        descriptions = []
        for tag in filter(lambda t: not t.isActive, self.tags):
            descriptions.append(tag.localizationNames["en-us"])
        for desc in sorted(descriptions, key=str.casefold):
            self.inactiveListbox.insert(END, desc)

    def updateTagLibrary(self):
        UpdatingTwitchTagsWindow(self)
        self.populateListboxes()

    def ok(self):
        for tag in self.tags:
            if tag.localizationNames["en-us"] in self.inactiveListbox.get(0, END):
                tag.isActive = False
            else:
                tag.isActive = True
        self.close()

    def close(self):
        self.parent.setTags(self.tags)
        self.window.destroy()

    def moveUp(self):
        if self.selectedInactive:
            for tag in self.selectedInactive:
                alphabeticallyInsert(self.activeListbox, self.inactiveListbox.get(tag))
            for tag in reversed(self.selectedInactive):
                self.inactiveListbox.delete(tag)
            self.inactiveListbox.selection_clear(0, END)
            self.selectedInactive = None

    def moveDown(self):
        if self.selectedActive:
            for tag in self.selectedActive:
                alphabeticallyInsert(self.inactiveListbox, self.activeListbox.get(tag))
            for tag in reversed(self.selectedActive):
                self.activeListbox.delete(tag)
            self.activeListbox.selection_clear(0, END)
            self.selectedActive = None

    def onSelectActiveListbox(self, event):
        w = event.widget
        self.selectedActive = w.curselection()

    def onSelectInactiveListbox(self, event):
        w = event.widget
        self.selectedInactive = w.curselection()
