from credentials import Credentials
from twitchapi import authorize, validateOAuth
from windows.mainWindow import MainWindow

oAuth = None

if not validateOAuth():
    oAuth = authorize()
else:
    with open("oauth.txt", "r") as f:
        oAuth = f.read().rstrip()

credentials = Credentials(oAuth)
w = MainWindow(credentials)
w.window.mainloop()
