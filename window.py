from tkinter import StringVar, Tk, Frame, Label, EW, E, W, NSEW, RIGHT, CENTER, Listbox, MULTIPLE, END, Scrollbar, Y, NS
from tkinter.ttk import Combobox

from constants import STREAMOPENER_ICON, ORDERED_STREAMING_SITES, LABEL_STREAM_DROPDOWN, LABEL_STREAMOPENER

class Window:
    def __init__(self, streams=None):
        if streams is None:
            streams = []
        self.window = Tk()
        self.site = StringVar()
        self.streams = streams

        self.initializeWindow()
        self.addListbox()
        self.addFrame()

    def initializeWindow(self):
        self.window.iconbitmap(STREAMOPENER_ICON)
        self.window.geometry('300x600')
        self.window.title(LABEL_STREAMOPENER)

    def addListbox(self):
        frameListBox = Frame(self.window)
        frameListBox.grid(row=0, column=0, columnspan=2, sticky=NSEW)
        scrollbar = Scrollbar(frameListBox)
        scrollbar.grid(row=0, column=1, sticky="NWS")
        listbox = Listbox(frameListBox, selectmode=MULTIPLE, yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)
        for stream in self.streams:
            print(stream.stylizedStreamName)
            listbox.insert(END, stream.stylizedStreamName)
        listbox.grid(row=0, column=0, sticky=NSEW, padx=4, pady=4)

    def addFrame(self):
        labelSiteDropdown = Label(self.window, text=LABEL_STREAM_DROPDOWN)
        labelSiteDropdown.grid(row=1, column=0, sticky=NSEW, padx=4, pady=4)
        siteDropdown = Combobox(self.window, textvariable=self.site, state="readonly", values=list(ORDERED_STREAMING_SITES.keys()))
        siteDropdown.grid(row=1, column=1, sticky=NSEW, padx=4, pady=4)
