from copy import copy
from tkinter import Frame, NSEW, Label, Scrollbar, Listbox, W, SINGLE, NONE, Button, Toplevel, END, MULTIPLE, DISABLED, NORMAL
from tkinter.ttk import Combobox
from typing import List

from constants import FILE_STREAMOPENER_ICON, LABEL_TEAM_WINDOW, LABEL_FREE_AGENTS, LABEL_LEFT, LABEL_UP, LABEL_DOWN, LABEL_RIGHT, LABEL_TEAM_MEMBERS, LABEL_TEAMS_DROPDOWN, \
    LABEL_CREATE_NEW_TEAM, LABEL_RENAME, LABEL_DELETE, LABEL_OK, LABEL_CANCEL, LABEL_ALL_TEAM
from teamNameWindow import TeamNameWindow

class TeamWindow:
    def __init__(self, parent, teams):
        self.window = Toplevel(parent.window)
        self.window.withdraw()
        self.parent = parent
        self.teams = copy(teams)
        self.teamFrame = Frame(self.window)
        self.streamFrame = Frame(self.window)
        self.buttonFrame = Frame(self.window)

        self.isRename = False
        self.tempName = None
        self.currentTeam = None
        self.teamsExist = False
        self.pageLoaded = False

        self.comboboxTeam = None
        self.freeAgentListbox = None
        self.teamMemberListbox = None

        self.selectedFreeAgents = None
        self.selectedTeamMembers = None

        self.buttonLeftArrow = None
        self.buttonUpArrow = None
        self.buttonDownArrow = None
        self.buttonRightArrow = None
        self.buttonRename = None

        self.initializeWindow()
        self.gridFrames()
        self.addDropdown()
        self.addFreeAgentListbox()
        self.addListboxButtons()
        self.addTeamMemberListbox()
        self.addButtons()
        if self.teamsExist:
            self.switchActiveTeam()
        self.pageLoaded = True
        self.window.deiconify()
        self.parent.window.wait_window(self.window)
        self.parent.window.attributes('-disabled', 0)
        self.parent.window.deiconify()

    def initializeWindow(self):
        self.parent.window.attributes('-disabled', 1)
        self.window.iconbitmap(FILE_STREAMOPENER_ICON)
        self.window.geometry('380x282+{x}+{y}'.format(x=self.parent.window.winfo_x() + 30, y=self.parent.window.winfo_y() + 50))
        self.window.title(LABEL_TEAM_WINDOW)
        self.window.resizable(width=False, height=False)
        self.window.transient(self.parent.window)
        self.window.grab_set()

    def gridFrames(self):
        self.buttonFrame.grid_columnconfigure(0, weight=1)
        self.buttonFrame.grid_columnconfigure(1, weight=1)
        self.buttonFrame.grid_columnconfigure(2, weight=1)
        self.buttonFrame.grid_columnconfigure(3, weight=1)
        self.teamFrame.grid(row=0, sticky=NSEW, padx=4, pady=4)
        self.streamFrame.grid(row=1, sticky=NSEW, padx=4, pady=4)
        self.buttonFrame.grid(row=2, sticky=NSEW, padx=4, pady=4)

    def addDropdown(self):
        teams = self.getListOfTeams()
        labelTeam = Label(self.teamFrame, text=LABEL_TEAMS_DROPDOWN)
        labelTeam.grid(row=0, column=0, sticky=NSEW, padx=4, pady=4)
        self.comboboxTeam = Combobox(self.teamFrame, values=teams, state="readonly")
        self.comboboxTeam.bind("<<ComboboxSelected>>", self.switchActiveTeam)
        if teams:
            self.teamsExist = True
            self.comboboxTeam.current(0)
            self.currentTeam = self.comboboxTeam.get()
        self.comboboxTeam.grid(row=0, column=1, padx=4, pady=4)
        buttonNewTeam = Button(self.teamFrame, text=LABEL_CREATE_NEW_TEAM, width=16, command=self.createNewTeam)
        buttonNewTeam.grid(row=0, column=2, sticky=NSEW, padx=(40, 4), pady=4)

    def addFreeAgentListbox(self):
        frameFreeAgentListBox = Frame(self.streamFrame)
        frameFreeAgentListBox.grid(row=0, column=0, sticky=NSEW, padx=4, pady=(0, 4))
        labelFreeAgentListBox = Label(frameFreeAgentListBox, text=LABEL_FREE_AGENTS)
        labelFreeAgentListBox.grid(row=0, column=0, padx=4, sticky=W)
        scrollbar = Scrollbar(frameFreeAgentListBox)
        scrollbar.grid(row=1, column=1, sticky="NWS")
        self.freeAgentListbox = Listbox(frameFreeAgentListBox, selectmode=MULTIPLE, yscrollcommand=scrollbar.set, activestyle=NONE)
        scrollbar.config(command=self.freeAgentListbox.yview)
        self.freeAgentListbox.bind('<<ListboxSelect>>', self.onSelectFreeAgentListbox)
        self.freeAgentListbox.grid(row=1, column=0, sticky=NSEW, padx=(4, 0))

    def addListboxButtons(self):
        frameListBoxButtons = Frame(self.streamFrame)
        frameListBoxButtons.grid(row=0, column=1, sticky=NSEW, pady=(0, 4))
        self.buttonLeftArrow = Button(frameListBoxButtons, text=LABEL_LEFT, width=7, command=lambda: self.moveLeft(), state=DISABLED)
        self.buttonLeftArrow.grid(row=0, sticky=NSEW, padx=4, pady=(38, 4))
        self.buttonUpArrow = Button(frameListBoxButtons, text=LABEL_UP, width=7, command=lambda: self.moveUp(), state=DISABLED)
        self.buttonUpArrow.grid(row=1, sticky=NSEW, padx=4, pady=4)
        self.buttonDownArrow = Button(frameListBoxButtons, text=LABEL_DOWN, width=7, command=lambda: self.moveDown(), state=DISABLED)
        self.buttonDownArrow.grid(row=2, sticky=NSEW, padx=4, pady=4)
        self.buttonRightArrow = Button(frameListBoxButtons, text=LABEL_RIGHT, width=7, command=lambda: self.moveRight(), state=DISABLED)
        self.buttonRightArrow.grid(row=3, sticky=NSEW, padx=4, pady=4)

    def addTeamMemberListbox(self):
        frameTeamMemberListbox = Frame(self.streamFrame)
        frameTeamMemberListbox.grid(row=0, column=2, sticky=NSEW, pady=(0, 4))
        labelLiveListBox = Label(frameTeamMemberListbox, text=LABEL_TEAM_MEMBERS)
        labelLiveListBox.grid(row=0, column=0, padx=4, sticky=W)
        scrollbar = Scrollbar(frameTeamMemberListbox)
        scrollbar.grid(row=1, column=1, sticky="NWS")
        self.teamMemberListbox = Listbox(frameTeamMemberListbox, selectmode=SINGLE, yscrollcommand=scrollbar.set, activestyle=NONE)
        scrollbar.config(command=self.teamMemberListbox.yview)
        self.teamMemberListbox.bind('<<ListboxSelect>>', self.onSelectTeamMemberListbox)
        self.teamMemberListbox.grid(row=1, column=0, sticky=NSEW, padx=(4, 0))

    def addButtons(self):
        self.buttonRename = Button(self.buttonFrame, text=LABEL_RENAME, width=8, command=lambda: self.rename())
        self.buttonRename.grid(row=0, column=0, sticky=NSEW, padx=(8, 4), pady=4)
        buttonDelete = Button(self.buttonFrame, text=LABEL_DELETE, width=8, command=lambda: self.delete())
        buttonDelete.grid(row=0, column=1, sticky=NSEW, padx=4, pady=4)
        buttonSave = Button(self.buttonFrame, text=LABEL_OK, width=8, command=lambda: self.ok())
        buttonSave.grid(row=0, column=2, sticky=NSEW, padx=4, pady=4)
        buttonCancel = Button(self.buttonFrame, text=LABEL_CANCEL, width=8, command=lambda: self.window.destroy())
        buttonCancel.grid(row=0, column=3, sticky=NSEW, padx=4, pady=4)

    def moveLeft(self):
        if self.selectedTeamMembers:
            for stream in self.selectedTeamMembers:
                self.freeAgentListbox.insert(END, self.teamMemberListbox.get(stream))
            for stream in reversed(self.selectedTeamMembers):
                self.teamMemberListbox.delete(stream)
            self.teamMemberListbox.selection_clear(0, END)
            self.selectedTeamMembers = None
            self.buttonLeftArrow.configure(state=DISABLED)

    def moveUp(self):
        index = self.teamMemberListbox.curselection()
        if self.selectedTeamMembers and len(self.selectedTeamMembers) == 1 and index is not None and index[0] != 0:
            stream = self.teamMemberListbox.get(index[0])
            self.teamMemberListbox.delete(index[0])
            self.teamMemberListbox.insert(index[0] - 1, stream)
            self.teamMemberListbox.selection_set(index[0] - 1)

    def moveDown(self):
        index = self.teamMemberListbox.curselection()
        if self.selectedTeamMembers and len(self.selectedTeamMembers) == 1 and index is not None and index[0] != self.teamMemberListbox.size() - 1:
            stream = self.teamMemberListbox.get(index[0])
            self.teamMemberListbox.delete(index[0])
            self.teamMemberListbox.insert(index[0] + 1, stream)
            self.teamMemberListbox.selection_set(index[0] + 1)

    def moveRight(self):
        if self.selectedFreeAgents:
            for stream in self.selectedFreeAgents:
                self.teamMemberListbox.insert(END, self.freeAgentListbox.get(stream))
            for stream in reversed(self.selectedFreeAgents):
                self.freeAgentListbox.delete(stream)
            self.freeAgentListbox.selection_clear(0, END)
            self.selectedFreeAgents = None
            self.buttonRightArrow.configure(state=DISABLED)

    def switchActiveTeam(self, event=None):
        if self.pageLoaded and self.currentTeam is not None and len(self.currentTeam) > 0:
            self.storeCurrentTeamChanges(self.currentTeam)
        teamMembers = self.teams[self.comboboxTeam.get()]
        freeAgents = [x for x in self.teams[LABEL_ALL_TEAM] if x not in teamMembers]
        self.clearListboxes()
        for streamer in freeAgents:
            self.freeAgentListbox.insert(END, streamer)
        for streamer in teamMembers:
            self.teamMemberListbox.insert(END, streamer)
        self.currentTeam = self.comboboxTeam.get()

    def clearListboxes(self):
        self.freeAgentListbox.selection_clear(0, END)
        self.teamMemberListbox.selection_clear(0, END)
        self.freeAgentListbox.delete(0, END)
        self.teamMemberListbox.delete(0, END)

    def onSelectFreeAgentListbox(self, event):
        w = event.widget
        self.selectedFreeAgents = w.curselection()
        self.buttonRightArrow.configure(state=NORMAL)
        self.buttonLeftArrow.configure(state=DISABLED)
        self.buttonUpArrow.configure(state=DISABLED)
        self.buttonDownArrow.configure(state=DISABLED)

    def onSelectTeamMemberListbox(self, event):
        w = event.widget
        self.selectedTeamMembers = w.curselection()
        self.buttonRightArrow.configure(state=DISABLED)
        self.buttonLeftArrow.configure(state=NORMAL)
        if len(self.selectedTeamMembers) > 1:
            self.buttonUpArrow.configure(state=DISABLED)
            self.buttonDownArrow.configure(state=DISABLED)
        else:
            self.buttonUpArrow.configure(state=NORMAL)
            self.buttonDownArrow.configure(state=NORMAL)

    def getListOfTeams(self) -> List[str]:
        return list(key for key in self.teams.keys() if key != LABEL_ALL_TEAM)

    def rename(self):
        if self.comboboxTeam.current() >= 0:
            self.isRename = True
            TeamNameWindow(self)

    def storeCurrentTeamChanges(self, key):
        self.teams[key] = list(self.teamMemberListbox.get(0, END))

    def ok(self):
        if self.comboboxTeam.get() != "":
            self.storeCurrentTeamChanges(self.comboboxTeam.get())
        self.parent.setTeams(self.teams)
        self.window.destroy()

    def delete(self):
        self.teams.pop(self.comboboxTeam.get())
        self.comboboxTeam.set("")
        self.comboboxTeam.selection_clear()
        self.clearListboxes()
        self.comboboxTeam.configure(values=self.getListOfTeams())
        self.currentTeam = None

    def createNewTeam(self):
        self.isRename = False
        TeamNameWindow(self)
