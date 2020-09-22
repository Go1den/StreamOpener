from tkinter import Toplevel, Frame, NSEW, StringVar, Label, Entry, Button, messagebox, E

from constants.fileConstants import FileConstants
from constants.labelConstants import LabelConstants
from constants.messageConstants import MessageConstants
from windows.windowHelper import WindowHelper

class TeamNameWindow:
    def __init__(self, parent):
        self.window = Toplevel(parent.window)
        self.window.withdraw()
        self.parent = parent
        self.teamName = StringVar()

        self.entryFrame = Frame(self.window)
        self.buttonFrame = Frame(self.window)

        WindowHelper.initializeWindow(self.window, self.parent, 260, 106, 30, 50, LabelConstants.TEAM_NAME_WINDOW)
        self.gridFrames()
        self.addEntryFrame()
        self.addButtonFrame()
        WindowHelper.finalizeWindow(self.window, self.parent)

    def gridFrames(self):
        self.entryFrame.grid(row=0, padx=4, pady=4, sticky=NSEW)
        self.buttonFrame.grid(row=1, padx=4, pady=4, sticky=E)

    def addEntryFrame(self):
        labelTeamName = Label(self.entryFrame, text=LabelConstants.TEAM_NAME)
        labelTeamName.grid(row=0, sticky="NSW", padx=2, pady=4)
        entryTeamName = Entry(self.entryFrame, textvariable=self.teamName, width=40)
        entryTeamName.focus()
        entryTeamName.grid(row=1, sticky=NSEW, padx=4, pady=4)

    def addButtonFrame(self):
        buttonOk = Button(self.buttonFrame, text=LabelConstants.OK, width=8, command=lambda: self.ok())
        buttonOk.grid(row=0, column=0, sticky=NSEW, padx=4, pady=4)
        buttonCancel = Button(self.buttonFrame, text=LabelConstants.CANCEL, width=8, command=lambda: self.window.destroy())
        buttonCancel.grid(row=0, column=1, sticky=NSEW, padx=4, pady=4)

    def ok(self):
        self.teamName.set(self.teamName.get().strip())
        if self.isValidTeamName(self.teamName.get()):
            if self.parent.isRename:
                self.rename()
            else:
                self.createNewTeam()
            self.cancel()
        else:
            self.window.grab_set()

    def cancel(self):
        self.parent.window.grab_set()
        self.window.destroy()

    def isValidTeamName(self, name):
        if name == LabelConstants.ALL_TEAM:
            messagebox.showerror(LabelConstants.ERROR, MessageConstants.RESERVED_NAME)
            return False
        elif name in self.parent.teams.keys():
            messagebox.showerror(LabelConstants.ERROR, MessageConstants.DUPLICATE_TEAM)
            return False
        elif not all(letter.isalnum() or letter.isspace() for letter in name):
            messagebox.showerror(LabelConstants.ERROR, MessageConstants.ALNUM_ONLY)
            return False
        elif len(name) < 1 or len(name) > 20:
            messagebox.showerror(LabelConstants.ERROR, MessageConstants.TEAM_NAME_LENGTH)
            return False
        elif name.isspace():
            messagebox.showerror(LabelConstants.ERROR, MessageConstants.ALL_SPACES)
            return False
        else:
            return True

    def rename(self):
        self.parent.teams[self.teamName.get()] = self.parent.teams.pop(self.parent.comboboxTeam.get())
        self.parent.comboboxTeam.current()
        self.parent.comboboxTeam.configure(values=self.parent.getListOfTeams())
        self.parent.comboboxTeam.set(self.teamName.get())
        self.parent.currentTeam = self.teamName.get()

    def createNewTeam(self):
        self.parent.teams[self.teamName.get()] = []
        self.parent.comboboxTeam.configure(values=self.parent.getListOfTeams())
        self.parent.comboboxTeam.set(self.teamName.get())
        self.parent.switchActiveTeam()
