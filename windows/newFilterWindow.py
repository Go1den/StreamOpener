from tkinter import Toplevel, Frame, NSEW, E, Label, Entry, StringVar, Button, W, messagebox

from constants.labelConstants import LabelConstants
from constants.messageConstants import MessageConstants
from twitchapi import isRecognizedTwitchGame
from windows.windowHelper import WindowHelper

class NewFilterWindow:
    def __init__(self, parent):
        self.window = Toplevel(parent.window)
        self.window.withdraw()
        self.parent = parent

        self.entryFrame = Frame(self.window)
        self.buttonFrame = Frame(self.window)

        self.comboboxStream = None
        self.game = StringVar()
        self.streamer = StringVar()

        WindowHelper.initializeWindow(self.window, self.parent, 324, 140, 30, 50, LabelConstants.NEW_FILTER_WINDOW)
        self.gridFrames()
        self.addEntryFrame()
        self.addButtonFrame()
        WindowHelper.finalizeWindow(self.window, self.parent)

    def gridFrames(self):
        self.entryFrame.grid(row=0, sticky=NSEW, padx=4, pady=4)
        self.buttonFrame.grid(row=1, sticky=E, padx=4, pady=4)

    def addEntryFrame(self):
        labelInstructions = Label(self.entryFrame, text=LabelConstants.NEW_FILTER_INSTRUCTIONS)
        labelInstructions.grid(row=0, column=0, columnspan=2, sticky=W, padx=4, pady=4)
        labelStream = Label(self.entryFrame, text=LabelConstants.STREAMER)
        labelStream.grid(row=1, column=0, sticky=E, padx=4, pady=4)
        entryStream = Entry(self.entryFrame, textvariable=self.streamer, width=40)
        entryStream.grid(row=1, column=1, sticky=W, padx=(0, 4), pady=4)
        labelGame = Label(self.entryFrame, text=LabelConstants.GAME)
        labelGame.grid(row=2, column=0, sticky=E, padx=4, pady=4)
        entryGame = Entry(self.entryFrame, textvariable=self.game, width=40)
        entryGame.grid(row=2, column=1, sticky=W, padx=(0, 4), pady=4)

    def addButtonFrame(self):
        buttonOk = Button(self.buttonFrame, text=LabelConstants.OK, width=8, command=lambda: self.ok())
        buttonOk.grid(row=0, column=0, sticky=NSEW, padx=4, pady=4)
        buttonCancel = Button(self.buttonFrame, text=LabelConstants.CANCEL, width=8, command=lambda: self.window.destroy())
        buttonCancel.grid(row=0, column=1, sticky=NSEW, padx=4, pady=4)

    def ok(self):
        game = self.game.get().strip()
        streamer = self.streamer.get().strip()
        if not game and not streamer:
            messagebox.showerror(LabelConstants.ERROR, MessageConstants.NO_FILTER_INFO_PROVIDED)
        if game and not isRecognizedTwitchGame(self.parent.parent.credentials.oauth, game):
            messagebox.showerror(LabelConstants.ERROR, MessageConstants.INVALID_GAME)
        else:
            newFilter = {}
            if streamer:
                newFilter["streamer"] = streamer
            if game:
                newFilter["game"] = game
            if streamer and game:
                newFilter["description"] = streamer + " streaming " + game
                key = LabelConstants.FILTER_KEY_COMBINED
            elif streamer:
                newFilter["description"] = streamer
                key = LabelConstants.FILTER_KEY_STREAMER
            else:
                newFilter["description"] = game
                key = LabelConstants.FILTER_KEY_GAME
            if newFilter in self.parent.filters["filters"][key]:
                messagebox.showerror(LabelConstants.ERROR, MessageConstants.FILTER_ALREADY_EXISTS)
            else:
                self.parent.addFilter(key, newFilter)
                self.window.destroy()
