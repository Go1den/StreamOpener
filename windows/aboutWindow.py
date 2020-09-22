import webbrowser
from tkinter import Button, W, Toplevel, Label, LEFT, PhotoImage, Frame, SE

from constants.fileConstants import FileConstants
from constants.labelConstants import LabelConstants
from constants.urlConstants import URLConstants
from windows.windowHelper import WindowHelper

class AboutWindow:
    def __init__(self, parent):
        self.window = Toplevel(parent.window)
        self.window.withdraw()
        self.parent = parent

        self.frameTop = Frame(self.window)
        self.aboutImage = PhotoImage(file=FileConstants.STREAMOPENER_ICON_64)

        WindowHelper.initializeWindow(self.window, self.parent, 0, 0, 60, 100, LabelConstants.ABOUT)
        self.addAboutFrame()
        WindowHelper.finalizeWindow(self.window, self.parent)

    def addAboutFrame(self):
        aboutImageLabel = Label(self.frameTop, image=self.aboutImage)
        aboutImageLabel.grid(row=0, column=0, padx=4, pady=4)

        aboutLabel = Label(self.frameTop, text=LabelConstants.ABOUT_WINDOW_INFO, justify=LEFT)
        aboutLabel.grid(row=0, column=1, sticky=W, pady=4)

        self.frameTop.grid(row=0, column=0, sticky=W)

        aboutSupportLabel = Label(self.window, text=LabelConstants.ABOUT_ME, justify=LEFT)
        aboutSupportLabel.grid(row=1, column=0, sticky=W, padx=4, columnspan=2)

        mySubscribeButton = Button(self.window, text=LabelConstants.SUBSCRIBE_TWITCH, width=25,
                                   command=lambda: webbrowser.open(URLConstants.TWITCH_GO1DEN_SUBSCRIBE, new=2))
        mySubscribeButton.grid(row=2, column=0, columnspan=2, pady=4, padx=4)

        myWebsiteButton = Button(self.window, text=LabelConstants.VISIT_MY_WEBSITE, width=25, command=lambda: webbrowser.open(URLConstants.TWITCH_MY_WEBSITE, new=2))
        myWebsiteButton.grid(row=3, column=0, columnspan=2, pady=4, padx=4)

        aboutThanksLabel = Label(self.window, text=LabelConstants.THANKS, justify=LEFT)
        aboutThanksLabel.grid(row=4, column=0, sticky=W, pady=4, padx=4)

        okButton = Button(self.window, text=LabelConstants.OK, width=8, command=lambda: self.window.destroy())
        okButton.grid(row=5, column=0, sticky=SE, pady=4, padx=4)
