from tkinter import Toplevel, Frame, NSEW, E, Label, Entry, StringVar, Button, W, messagebox
from tkinter.ttk import Combobox

from constants.fileConstants import FILE_STREAMOPENER_ICON
from constants.messageConstants import MSG_FILTER_ALREADY_EXISTS, MSG_NO_FILTER_INFO_PROVIDED, MSG_INVALID_GAME
from constants.labelConstants import LABEL_CANCEL, LABEL_OK, LABEL_GAME, LABEL_STREAMER, LABEL_ERROR, LABEL_ALL_TEAM, LABEL_FILTER_KEY_GAME, LABEL_FILTER_KEY_STREAMER, \
    LABEL_FILTER_KEY_COMBINED, LABEL_NEW_FILTER_WINDOW, LABEL_NEW_FILTER_INSTRUCTIONS
from twitchapi import isRecognizedTwitchGame

class NewFilterWindow:
    def __init__(self, parent):
        self.window = Toplevel(parent.window)
        self.window.withdraw()
        self.parent = parent

        self.entryFrame = Frame(self.window)
        self.buttonFrame = Frame(self.window)

        self.comboboxStream = None
        self.game = StringVar()

        self.initializeWindow()
        self.gridFrames()
        self.addEntryFrame()
        self.addButtonFrame()
        self.finalizeWindow()

    def initializeWindow(self):
        self.parent.window.attributes('-disabled', 1)
        self.window.iconbitmap(FILE_STREAMOPENER_ICON)
        self.window.geometry('324x140+{x}+{y}'.format(x=self.parent.window.winfo_x() + 30, y=self.parent.window.winfo_y() + 50))
        self.window.title(LABEL_NEW_FILTER_WINDOW)
        self.window.resizable(False, False)
        self.window.transient(self.parent.window)
        self.window.grab_set()

    def gridFrames(self):
        self.entryFrame.grid(row=0, sticky=NSEW, padx=4, pady=4)
        self.buttonFrame.grid(row=1, sticky=E, padx=4, pady=4)

    def addEntryFrame(self):
        labelInstructions = Label(self.entryFrame, text=LABEL_NEW_FILTER_INSTRUCTIONS)
        labelInstructions.grid(row=0, column=0, columnspan=2, sticky=W, padx=4, pady=4)
        labelStream = Label(self.entryFrame, text=LABEL_STREAMER)
        labelStream.grid(row=1, column=0, sticky=E, padx=4, pady=4)
        self.comboboxStream = Combobox(self.entryFrame, values=self.parent.parent.teams[LABEL_ALL_TEAM], state="readonly")
        self.comboboxStream.grid(row=1, column=1, sticky=W, padx=(0, 4), pady=4)
        labelGame = Label(self.entryFrame, text=LABEL_GAME)
        labelGame.grid(row=2, column=0, sticky=E, padx=4, pady=4)
        entryGame = Entry(self.entryFrame, textvariable=self.game, width=40)
        entryGame.grid(row=2, column=1, sticky=W, padx=(0, 4), pady=4)

    def addButtonFrame(self):
        buttonOk = Button(self.buttonFrame, text=LABEL_OK, width=8, command=lambda: self.ok())
        buttonOk.grid(row=0, column=0, sticky=NSEW, padx=4, pady=4)
        buttonCancel = Button(self.buttonFrame, text=LABEL_CANCEL, width=8, command=lambda: self.window.destroy())
        buttonCancel.grid(row=0, column=1, sticky=NSEW, padx=4, pady=4)

    def ok(self):
        game = self.game.get().strip()
        streamer = self.comboboxStream.get()
        if not game and not streamer:
            messagebox.showerror(LABEL_ERROR, MSG_NO_FILTER_INFO_PROVIDED)
        if game and not isRecognizedTwitchGame(self.parent.parent.credentials.oauth, game):
            messagebox.showerror(LABEL_ERROR, MSG_INVALID_GAME)
        else:
            newFilter = {}
            if streamer:
                newFilter["streamer"] = streamer
            if game:
                newFilter["game"] = game
            if streamer and game:
                newFilter["description"] = streamer + " streaming " + game
                key = LABEL_FILTER_KEY_COMBINED
            elif streamer:
                newFilter["description"] = streamer
                key = LABEL_FILTER_KEY_STREAMER
            else:
                newFilter["description"] = game
                key = LABEL_FILTER_KEY_GAME
            if newFilter in self.parent.filters["filters"][key]:
                messagebox.showerror(LABEL_ERROR, MSG_FILTER_ALREADY_EXISTS)
            else:
                self.parent.addFilter(key, newFilter)
                self.window.destroy()

    def finalizeWindow(self):
        self.window.deiconify()
        self.parent.window.wait_window(self.window)
        self.parent.window.attributes('-disabled', 0)
        self.parent.window.deiconify()
