from twitchapi import authorize, validateOAuth
from window import Window

oAuth = None

if not validateOAuth():
    oAuth = authorize()
else:
    with open("oauth.txt", "r") as f:
        oAuth = f.read().rstrip()

w = Window(oAuth)
w.window.mainloop()
