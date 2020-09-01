from tkinter import Toplevel, Frame

from constants import FILE_STREAMOPENER_ICON, LABEL_UNFOLLOW_WINDOW

class UnfollowWindow:
    def __init__(self, parent):
        self.window = Toplevel(parent.window)
        self.window.withdraw()
        self.parent = parent
        self.filterFrame = Frame(self.window)
        self.buttonFrame = Frame(self.window)
        self.unfollowListbox = None

        self.initializeWindow()
        self.finalizeWindow()

    def initializeWindow(self):
        self.parent.window.attributes('-disabled', 1)
        self.window.iconbitmap(FILE_STREAMOPENER_ICON)
        self.window.geometry('460x630+{x}+{y}'.format(x=self.parent.window.winfo_x() + 30, y=self.parent.window.winfo_y() + 50))
        self.window.title(LABEL_UNFOLLOW_WINDOW)
        self.window.resizable(width=False, height=False)
        self.window.transient(self.parent.window)
        self.window.grab_set()

    def finalizeWindow(self):
        self.window.deiconify()
        self.parent.window.wait_window(self.window)
        self.parent.window.attributes('-disabled', 0)
        self.parent.window.deiconify()
