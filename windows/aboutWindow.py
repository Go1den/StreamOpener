import webbrowser
from tkinter import Button, W, Toplevel, Label, LEFT, PhotoImage, Frame, SE

from constants.fileConstants import FileConstants
from constants.labelConstants import LabelConstants
from constants.urlConstants import URLConstants

class AboutWindow:
    def __init__(self, parent):
        self.window = Toplevel(parent.window)
        self.window.withdraw()
        self.parent = parent

        self.frameTop = Frame(self.window)
        self.aboutImage = PhotoImage(file=FileConstants.FILE_STREAMOPENER_ICON_64)

        self.initializeWindow()
        self.addAboutFrame()
        self.finalizeWindow()

    def initializeWindow(self):
        self.parent.window.attributes('-disabled', 1)
        self.window.iconbitmap(FileConstants.FILE_STREAMOPENER_ICON)
        self.window.geometry('+{x}+{y}'.format(x=self.parent.window.winfo_x() + 60, y=self.parent.window.winfo_y() + 100))
        self.window.title(LabelConstants.LABEL_ABOUT)
        self.window.resizable(False, False)
        self.window.transient(self.parent.window)
        self.window.grab_set()

    def addAboutFrame(self):
        aboutImageLabel = Label(self.frameTop, image=self.aboutImage)
        aboutImageLabel.grid(row=0, column=0, padx=4, pady=4)

        aboutLabel = Label(self.frameTop, text=LabelConstants.LABEL_ABOUT_WINDOW_INFO, justify=LEFT)
        aboutLabel.grid(row=0, column=1, sticky=W, pady=4)

        self.frameTop.grid(row=0, column=0, sticky=W)

        aboutSupportLabel = Label(self.window, text=LabelConstants.LABEL_ABOUT_ME, justify=LEFT)
        aboutSupportLabel.grid(row=1, column=0, sticky=W, padx=4, columnspan=2)

        mySubscribeButton = Button(self.window, text=LabelConstants.LABEL_SUBSCRIBE_TWITCH, width=25,
                                   command=lambda: webbrowser.open(URLConstants.TWITCH_GO1DEN_SUBSCRIBE_LINK, new=2))
        mySubscribeButton.grid(row=2, column=0, columnspan=2, pady=4, padx=4)

        myWebsiteButton = Button(self.window, text=LabelConstants.LABEL_VISIT_MY_WEBSITE, width=25, command=lambda: webbrowser.open(URLConstants.TWITCH_MY_WEBSITE, new=2))
        myWebsiteButton.grid(row=3, column=0, columnspan=2, pady=4, padx=4)

        aboutThanksLabel = Label(self.window, text=LabelConstants.LABEL_THANKS, justify=LEFT)
        aboutThanksLabel.grid(row=4, column=0, sticky=W, pady=4, padx=4)

        okButton = Button(self.window, text=LabelConstants.LABEL_OK, width=8, command=lambda: self.window.destroy())
        okButton.grid(row=5, column=0, sticky=SE, pady=4, padx=4)

    def finalizeWindow(self):
        self.window.deiconify()
        self.parent.window.wait_window(self.window)
        self.parent.window.attributes('-disabled', 0)
        self.parent.window.deiconify()
