from tkinter import Toplevel, Frame, NSEW, StringVar, Label, Entry, Button, messagebox, E

from constants import FILE_STREAMOPENER_ICON, LABEL_TEAM_NAME, LABEL_TEAM_NAME_WINDOW, LABEL_ERROR, LABEL_ALL_TEAM, MSG_RESERVED_NAME, MSG_DUPLICATE_TEAM, \
    MSG_ALNUM_ONLY, MSG_TEAM_NAME_LENGTH, MSG_ALL_SPACES, LABEL_OK, LABEL_CANCEL

class TeamNameWindow:
    def __init__(self, parent):
        self.window = Toplevel(parent.window)
        self.window.withdraw()
        self.parent = parent
        self.teamName = StringVar()

        self.entryFrame = Frame(self.window)
        self.buttonFrame = Frame(self.window)

        self.initializeWindow()
        self.gridFrames()
        self.addEntryFrame()
        self.addButtonFrame()
        self.window.deiconify()
        self.parent.window.wait_window(self.window)
        self.parent.window.attributes('-disabled', 0)
        self.parent.window.deiconify()

    def initializeWindow(self):
        self.parent.window.attributes('-disabled', 1)
        self.window.iconbitmap(FILE_STREAMOPENER_ICON)
        self.window.geometry('260x106+{x}+{y}'.format(x=self.parent.window.winfo_x() + 30, y=self.parent.window.winfo_y() + 50))
        self.window.title(LABEL_TEAM_NAME_WINDOW)
        self.window.resizable(width=False, height=False)
        self.window.transient(self.parent.window)
        self.window.grab_set()

    def gridFrames(self):
        self.entryFrame.grid(row=0, padx=4, pady=4, sticky=NSEW)
        self.buttonFrame.grid(row=1, padx=4, pady=4, sticky=E)

    def addEntryFrame(self):
        labelTeamName = Label(self.entryFrame, text=LABEL_TEAM_NAME)
        labelTeamName.grid(row=0, sticky="NSW", padx=2, pady=4)
        entryTeamName = Entry(self.entryFrame, textvariable=self.teamName, width=40)
        entryTeamName.focus()
        entryTeamName.grid(row=1, sticky=NSEW, padx=4, pady=4)

    def addButtonFrame(self):
        buttonOk = Button(self.buttonFrame, text=LABEL_OK, width=8, command=lambda: self.ok())
        buttonOk.grid(row=0, column=0, sticky=NSEW, padx=4, pady=4)
        buttonCancel = Button(self.buttonFrame, text=LABEL_CANCEL, width=8, command=lambda: self.window.destroy())
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
        if name == LABEL_ALL_TEAM:
            messagebox.showerror(LABEL_ERROR, MSG_RESERVED_NAME)
            return False
        elif name in self.parent.teams.keys():
            messagebox.showerror(LABEL_ERROR, MSG_DUPLICATE_TEAM)
            return False
        elif not all(letter.isalnum() or letter.isspace() for letter in name):
            messagebox.showerror(LABEL_ERROR, MSG_ALNUM_ONLY)
            return False
        elif len(name) < 1 or len(name) > 20:
            messagebox.showerror(LABEL_ERROR, MSG_TEAM_NAME_LENGTH)
            return False
        elif name.isspace():
            messagebox.showerror(LABEL_ERROR, MSG_ALL_SPACES)
            return False
        else:
            return True

    def rename(self):
        self.parent.teams[self.teamName.get()] = self.parent.teams.pop(self.parent.comboboxTeam.get())
        self.parent.comboboxTeam.current()
        self.parent.comboboxTeam.configure(values=self.parent.getListOfTeams())
        self.parent.comboboxTeam.set(self.teamName.get())
        self.parent.currentTeam = self.teamName.get()
        print(self.parent.teams)

    def createNewTeam(self):
        self.parent.teams[self.teamName.get()] = []
        self.parent.comboboxTeam.configure(values=self.parent.getListOfTeams())
        self.parent.comboboxTeam.set(self.teamName.get())
        self.parent.switchActiveTeam()
        print(self.parent.teams)
