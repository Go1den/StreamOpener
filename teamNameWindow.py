from tkinter import Toplevel, Frame, NSEW, StringVar, Label, Entry, Button, messagebox

from constants import FILE_STREAMOPENER_ICON, LABEL_TEAM_NAME, LABEL_TEAM_NAME_WINDOW, MSG_INVALID_TEAM_NAME, LABEL_ERROR

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

    def initializeWindow(self):
        self.window.iconbitmap(FILE_STREAMOPENER_ICON)
        self.window.geometry('380x200')
        self.window.title(LABEL_TEAM_NAME_WINDOW)
        self.window.resizable(width=False, height=False)
        self.window.grab_set()

    def gridFrames(self):
        self.entryFrame.grid(row=0, padx=4, pady=4, sticky=NSEW)
        self.buttonFrame.grid(row=1, padx=4, pady=4, sticky=NSEW)

    def addEntryFrame(self):
        labelTeamName = Label(self.entryFrame, text=LABEL_TEAM_NAME)
        labelTeamName.grid(row=0, sticky="NSW", padx=2, pady=4)
        entryTeamName = Entry(self.entryFrame, textvariable=self.teamName, width=40)
        entryTeamName.grid(row=1, sticky=NSEW, padx=4, pady=4)

    def addButtonFrame(self):
        buttonOk = Button(self.buttonFrame, text="Ok", width=8, command=lambda: self.ok())
        buttonOk.grid(row=0, column=0, sticky=NSEW, padx=4, pady=4)
        buttonCancel = Button(self.buttonFrame, text="Cancel", width=8, command=lambda: self.window.destroy())
        buttonCancel.grid(row=0, column=1, sticky=NSEW, padx=4, pady=4)

    def ok(self):
        if self.isValidTeamName(self.teamName.get()):
            self.parent.tempName = self.teamName.get()
            print(self.parent.tempName)
            self.cancel()
        else:
            messagebox.showerror(LABEL_ERROR, MSG_INVALID_TEAM_NAME)

    def cancel(self):
        self.parent.window.grab_set()
        self.window.destroy()

    def isValidTeamName(self, name):
        return name != "All" and name not in self.parent.teams.keys() and all(letter.isalnum() or letter.isspace() for letter in name)




