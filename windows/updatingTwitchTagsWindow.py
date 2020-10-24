from copy import deepcopy
from tkinter import Tk, Frame, NSEW, Label, Toplevel, messagebox

from constants.labelConstants import LabelConstants
from constants.messageConstants import MessageConstants
from twitchapi import updateTwitchTags
from windows.windowHelper import WindowHelper

class UpdatingTwitchTagsWindow:
    def __init__(self, parent):
        self.window = Toplevel(parent.window)
        self.window.withdraw()
        self.window.protocol("WM_DELETE_WINDOW", self.noClose)
        self.parent = parent
        self.tags = deepcopy(parent.tags)

        self.frame = Frame(self.window)
        self.frame.grid(row=0, sticky=NSEW, padx=4, pady=4)

        labelPleaseWait = Label(self.frame, text=MessageConstants.UPDATING_TWITCH_TAGS)
        labelPleaseWait.grid(row=0, sticky=NSEW, padx=4, pady=4)

        WindowHelper.initializeWindow(self.window, self.parent, 300, 100, 30, 50, LabelConstants.UPDATE_IN_PROGRESS)

        self.window.deiconify()
        self.parent.window.attributes('-disabled', 0)
        self.parent.window.deiconify()
        self.window.update()

        beforeLen = len(self.tags)
        self.tags = updateTwitchTags(self.parent.parent.credentials.oauth, self.tags, True)
        afterLen = len(self.tags)
        messagebox.showinfo(LabelConstants.UPDATE_COMPLETE, MessageConstants.TAGS_ADDED.format(afterLen - beforeLen))
        self.parent.tags = self.tags
        self.window.destroy()

    def noClose(self):
        # Prevents closing the window while updating
        pass
