from mainwindow import MainWindow
from twitchapi import authorize, validateOAuth

oAuth = None

if not validateOAuth():
    oAuth = authorize()
else:
    with open("oauth.txt", "r") as f:
        oAuth = f.read().rstrip()

w = MainWindow(oAuth)
w.window.mainloop()
