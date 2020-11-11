from tkinter import Frame, NSEW, Label, Toplevel

from constants.labelConstants import LabelConstants
from constants.messageConstants import MessageConstants
from windows.windowHelper import WindowHelper

class UpdatingStreamsWindow:
    def __init__(self, parent):
        self.window = Toplevel(parent.window)
        self.window.withdraw()
        self.window.protocol("WM_DELETE_WINDOW", self.noClose)
        self.parent = parent

        self.frame = Frame(self.window)
        self.frame.grid(row=0, sticky=NSEW, padx=4, pady=4)

        labelPleaseWait = Label(self.frame, text=MessageConstants.UPDATING_STREAMS)
        labelPleaseWait.grid(row=0, sticky=NSEW, padx=4, pady=4)

        WindowHelper.initializeWindow(self.window, self.parent, 300, 100, 30, 50, LabelConstants.UPDATE_IN_PROGRESS)

        self.window.deiconify()
        self.parent.window.attributes('-disabled', 0)
        self.parent.window.deiconify()
        self.window.update()

    def noClose(self):
        # Prevents closing the window while updating
        pass
