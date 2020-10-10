from credentials import Credentials
from twitchapi import authorize, validateOAuth
from windows.mainWindow2 import MainWindow2

oAuth = None

if not validateOAuth():
    oAuth = authorize()
else:
    with open("oauth.txt", "r") as f:
        oAuth = f.read().rstrip()

credentials = Credentials(oAuth)

# Experimental
w = MainWindow2(credentials)

# w = MainWindow(credentials)
w.window.mainloop()
