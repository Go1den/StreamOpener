from tkinter import Frame, NSEW, Label, Scrollbar, Listbox, W, SINGLE, NONE, Button, Toplevel
from tkinter.ttk import Combobox

from constants import FILE_STREAMOPENER_ICON, LABEL_TEAM_WINDOW, LABEL_FREE_AGENTS, LABEL_LEFT, LABEL_UP, LABEL_DOWN, LABEL_RIGHT, LABEL_TEAM_MEMBERS

class TeamWindow:
    def __init__(self, parentWindow, teams):
        self.window = Toplevel(parentWindow)
        self.window.withdraw()
        self.teams = teams
        self.teamFrame = Frame(self.window)
        self.streamFrame = Frame(self.window)
        self.buttonFrame = Frame(self.window)

        self.freeAgentListbox = None
        self.teamMemberListbox = None

        self.initializeWindow()
        self.gridFrames()
        self.addDropdown()
        self.addFreeAgentListbox()
        self.addListboxButtons()
        self.addTeamMemberListbox()
        self.addButtons()
        self.window.deiconify()
        self.window.mainloop()

    def initializeWindow(self):
        self.window.iconbitmap(FILE_STREAMOPENER_ICON)
        self.window.geometry('380x282')
        self.window.title(LABEL_TEAM_WINDOW)
        self.window.resizable(width=False, height=False)
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
        labelTeam = Label(self.teamFrame, text="Team:")
        labelTeam.grid(row=0, column=0, sticky=NSEW, padx=4, pady=4)
        comboboxTeam = Combobox(self.teamFrame, values=list(self.teams.keys()), state="readonly")
        comboboxTeam.current(0)
        comboboxTeam.grid(row=0, column=1, padx=4, pady=4)
        buttonNewTeam = Button(self.teamFrame, text="Create New Team", width=16)
        buttonNewTeam.grid(row=0, column=2, sticky=NSEW, padx=(40, 4), pady=4)

    def addFreeAgentListbox(self):
        frameFreeAgentListBox = Frame(self.streamFrame)
        frameFreeAgentListBox.grid(row=0, column=0, sticky=NSEW, padx=4, pady=(0, 4))
        labelFreeAgentListBox = Label(frameFreeAgentListBox, text=LABEL_FREE_AGENTS)
        labelFreeAgentListBox.grid(row=0, column=0, padx=4, sticky=W)
        scrollbar = Scrollbar(frameFreeAgentListBox)
        scrollbar.grid(row=1, column=1, sticky="NWS")
        self.freeAgentListbox = Listbox(frameFreeAgentListBox, selectmode=SINGLE, yscrollcommand=scrollbar.set, activestyle=NONE)
        scrollbar.config(command=self.freeAgentListbox.yview)
        # self.populateFreeAgentListBox()
        # self.freeAgentListbox.bind('<<ListboxSelect>>', self.onSelectFreeAgentListbox)
        self.freeAgentListbox.grid(row=1, column=0, sticky=NSEW, padx=(4, 0))

    def addListboxButtons(self):
        frameListBoxButtons = Frame(self.streamFrame)
        frameListBoxButtons.grid(row=0, column=1, sticky=NSEW, pady=(0, 4))
        buttonLeftArrow = Button(frameListBoxButtons, text=LABEL_LEFT, width=7, command=lambda: self.unselectStreams())
        buttonLeftArrow.grid(row=0, sticky=NSEW, padx=4, pady=(38, 4))
        buttonReset = Button(frameListBoxButtons, text=LABEL_UP, width=7, command=lambda: self.increasePriority())
        buttonReset.grid(row=1, sticky=NSEW, padx=4, pady=4)
        buttonRefresh = Button(frameListBoxButtons, text=LABEL_DOWN, width=7, command=lambda: self.decreasePriority())
        buttonRefresh.grid(row=2, sticky=NSEW, padx=4, pady=4)
        buttonRightArrow = Button(frameListBoxButtons, text=LABEL_RIGHT, width=7, command=lambda: self.selectStreams())
        buttonRightArrow.grid(row=3, sticky=NSEW, padx=4, pady=4)

    def addTeamMemberListbox(self):
        frameTeamMemberListbox = Frame(self.streamFrame)
        frameTeamMemberListbox.grid(row=0, column=2, sticky=NSEW, pady=(0, 4))
        labelLiveListBox = Label(frameTeamMemberListbox, text=LABEL_TEAM_MEMBERS)
        labelLiveListBox.grid(row=0, column=0, padx=4, sticky=W)
        scrollbar = Scrollbar(frameTeamMemberListbox)
        scrollbar.grid(row=1, column=1, sticky="NWS")
        self.teamMemberListbox = Listbox(frameTeamMemberListbox, selectmode=SINGLE, yscrollcommand=scrollbar.set, activestyle=NONE)
        scrollbar.config(command=self.teamMemberListbox.yview)
        # self.teamMemberListbox.bind('<<ListboxSelect>>', self.onSelectTeamMemberListbox)
        self.teamMemberListbox.grid(row=1, column=0, sticky=NSEW, padx=(4, 0))

    def addButtons(self):
        buttonDelete = Button(self.buttonFrame, text="Rename", width=8)
        buttonDelete.grid(row=0, column=0, sticky=NSEW, padx=(8, 4), pady=4)
        buttonDelete = Button(self.buttonFrame, text="Delete", width=8)
        buttonDelete.grid(row=0, column=1, sticky=NSEW, padx=4, pady=4)
        buttonSave = Button(self.buttonFrame, text="Save", width=8)
        buttonSave.grid(row=0, column=2, sticky=NSEW, padx=4, pady=4)
        buttonSave = Button(self.buttonFrame, text="Cancel", width=8)
        buttonSave.grid(row=0, column=3, sticky=NSEW, padx=4, pady=4)

    def unselectStreams(self):
        pass

    def increasePriority(self):
        pass

    def decreasePriority(self):
        pass

    def selectStreams(self):
        pass
