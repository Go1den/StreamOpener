import json
import sys
import webbrowser
from typing import List

import easygui
import requests

from constants import TWITCH_OAUTH_LINK, CLIENT_ID, SCOPES, REDIRECT_URI, RESPONSE_TYPE, TWITCH_VALIDATE_LINK, TWITCH_LIVE_FOLLOWED_LINK, V5_JSON, MSG_ACCESS_TOKEN, \
    TITLE_ACCESS_TOKEN

def authorize() -> str:
    oauthURL = TWITCH_OAUTH_LINK + "?&scope=" + SCOPES + "&response_type=" + RESPONSE_TYPE + "&client_id=" + CLIENT_ID + "&redirect_uri=" + REDIRECT_URI
    webbrowser.open(oauthURL, new=2)
    while 1:
        value = easygui.enterbox(msg=MSG_ACCESS_TOKEN, title=TITLE_ACCESS_TOKEN, strip=True)
        if value is None:
            sys.exit(1)
        with open("oauth.txt", "w") as f:
            f.write(value)
        if validateOAuth():
            return value

def validateOAuth() -> bool:
    with open("oauth.txt", "r") as f:
        currentOAuth = f.read().rstrip()
    if not currentOAuth:
        return False
    parameters = {
        "Authorization": "OAuth " + currentOAuth
    }
    response = requests.get(TWITCH_VALIDATE_LINK, headers=parameters)
    return "client_id" in response.text

def getLiveFollowedStreams(oAuth: str) -> List[str]:
    parameters = {
        "Authorization": "OAuth " + oAuth,
        "Client-ID": CLIENT_ID,
        "Accept": V5_JSON,
        "limit": "100"
    }
    response = requests.get(TWITCH_LIVE_FOLLOWED_LINK, headers=parameters)
    jsonStreams = json.loads(response.text)
    liveStreams = []
    if jsonStreams["streams"] is not None:
        for stream in jsonStreams["streams"]:
            liveStreams.append(
                stream['channel']["display_name"] + " playing " + stream['game'] + " for " + str(stream['viewers']) + " viewers (" + stream['channel']['status'] + ")")
    return liveStreams
