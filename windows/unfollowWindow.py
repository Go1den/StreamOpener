from copy import deepcopy
from tkinter import Toplevel, Frame, NSEW, Label, Scrollbar, Listbox, MULTIPLE, NONE, W, END, Button, E, messagebox

from constants import FILE_STREAMOPENER_ICON, LABEL_UNFOLLOW_WINDOW, LABEL_ALL_TEAM, LABEL_SELECT_UNFOLLOW, LABEL_OK, LABEL_CANCEL, LABEL_INFO, MSG_STREAMS_UNFOLLOWED, \
    MSG_UNFOLLOW_FAILED, LABEL_ERROR, LABEL_CONFIRM, MSG_ABOUT_TO_UNFOLLOW
from twitchapi import unfollowStreams

class UnfollowWindow:
    def __init__(self, parent):
        self.window = Toplevel(parent.window)
        self.window.withdraw()
        self.parent = parent
        self.followedStreams = deepcopy(parent.teams[LABEL_ALL_TEAM])
        self.listboxFrame = Frame(self.window)
        self.buttonFrame = Frame(self.window)
        self.unfollowListbox = None

        self.initializeWindow()
        self.gridFrames()
        self.addListbox()
        self.addButtonFrame()
        self.finalizeWindow()

    def initializeWindow(self):
        self.parent.window.attributes('-disabled', 1)
        self.window.iconbitmap(FILE_STREAMOPENER_ICON)
        self.window.geometry('218x400+{x}+{y}'.format(x=self.parent.window.winfo_x() + 30, y=self.parent.window.winfo_y() + 50))
        self.window.title(LABEL_UNFOLLOW_WINDOW)
        self.window.resizable(width=False, height=False)
        self.window.transient(self.parent.window)
        self.window.grab_set()

    def gridFrames(self):
        self.listboxFrame.grid(row=0, sticky=NSEW, padx=4, pady=4)
        self.buttonFrame.grid(row=1, sticky=E, padx=4, pady=4)

    def addListbox(self):
        labelUnfollowListbox = Label(self.listboxFrame, text=LABEL_SELECT_UNFOLLOW)
        labelUnfollowListbox.grid(row=0, column=0, sticky=W, padx=4, pady=4)
        scrollbarGame = Scrollbar(self.listboxFrame)
        scrollbarGame.grid(row=1, column=1, sticky="NWS")
        self.unfollowListbox = Listbox(self.listboxFrame, selectmode=MULTIPLE, yscrollcommand=scrollbarGame.set, activestyle=NONE, width=30, height=20)
        scrollbarGame.config(command=self.unfollowListbox.yview)
        self.unfollowListbox.grid(row=1, column=0, sticky=NSEW, padx=(4, 0))
        self.unfollowListbox.configure(exportselection=False)
        for stream in self.followedStreams:
            print(stream)
            self.unfollowListbox.insert(END, stream)

    def addButtonFrame(self):
        buttonOk = Button(self.buttonFrame, text=LABEL_OK, width=8, command=lambda: self.ok())
        buttonOk.grid(row=0, column=0, sticky=E, padx=4, pady=4)
        buttonCancel = Button(self.buttonFrame, text=LABEL_CANCEL, width=8, command=lambda: self.cancel())
        buttonCancel.grid(row=0, column=1, sticky=E, padx=(4,0), pady=4)

    def ok(self):
        if messagebox.askyesno(LABEL_CONFIRM, MSG_ABOUT_TO_UNFOLLOW):
            if unfollowStreams(self.parent.credentials.oauth, self.parent.credentials.user_id, []):
                messagebox.showinfo(LABEL_INFO, MSG_STREAMS_UNFOLLOWED)
                # TODO: Remove unfollowed streams from any team or filter they were a part of and remove them from this list.
                # Or ask the user if they woud like to update their existing teams and filters I guess?
            else:
                messagebox.showerror(LABEL_ERROR, MSG_UNFOLLOW_FAILED)

    def cancel(self):
        # TODO: Refresh streams on the parent window
        self.window.destroy()

    def finalizeWindow(self):
        self.window.deiconify()
        self.parent.window.wait_window(self.window)
        self.parent.window.attributes('-disabled', 0)
        self.parent.window.deiconify()
