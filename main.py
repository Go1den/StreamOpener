from PIL import ImageTk, Image

from constants.fileConstants import FileConstants
from credentials import Credentials
from stream import Stream
from twitchapi import authorize, validateOAuth
from windows.mainWindow import MainWindow

if not validateOAuth():
    oAuth = authorize()
else:
    with open("oauth.txt", "r") as f:
        oAuth = f.read().rstrip()

credentials = Credentials(oAuth)
mainWindow = MainWindow(credentials)
Stream.DEFAULT_BOX_ART = ImageTk.PhotoImage(Image.open(FileConstants.PREVIEW_BOX_ART))
Stream.DEFAULT_STREAM_PREVIEW = ImageTk.PhotoImage(Image.open(FileConstants.STREAM_PREVIEW))
mainWindow.window.mainloop()
