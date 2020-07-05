import sys
import webbrowser

import easygui

from constants import MSG_SELECT_STREAMS, TITLE_SELECT_STREAMS, TITLE_SELECT_SITE, MSG_SELECT_SITE, ORDERED_STREAMING_SITES
from twitchapi import authorize, validateOAuth, getLiveFollowedStreams

oAuth = None

if not validateOAuth():
    oAuth = authorize()
else:
    with open("oauth.txt", "r") as f:
        oAuth = f.read().rstrip()

liveStreams = getLiveFollowedStreams(oAuth)

chosenStreams = easygui.multchoicebox(MSG_SELECT_STREAMS, TITLE_SELECT_STREAMS, liveStreams, None)
if chosenStreams is None:
    sys.exit(1)

streamingSite = easygui.choicebox(MSG_SELECT_SITE, TITLE_SELECT_SITE, ORDERED_STREAMING_SITES.keys())
if streamingSite is None:
    sys.exit(1)

finalURL = ORDERED_STREAMING_SITES.get(streamingSite)
for chosenStream in chosenStreams:
    finalURL += chosenStream.split(" ")[0] + "/"

webbrowser.open(finalURL, new=2)
sys.exit(0)
