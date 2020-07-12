import sys
import webbrowser

import easygui

from constants import MSG_SELECT_STREAMS, TITLE_SELECT_STREAMS, TITLE_SELECT_SITE, MSG_SELECT_SITE, ORDERED_STREAMING_SITES
from twitchapi import authorize, validateOAuth, getLiveFollowedStreams
from window import Window

oAuth = None

if not validateOAuth():
    oAuth = authorize()
else:
    with open("oauth.txt", "r") as f:
        oAuth = f.read().rstrip()

w = Window(oAuth)
w.window.mainloop()
