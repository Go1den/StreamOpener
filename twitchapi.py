import json
import sys
import webbrowser
from typing import List

import easygui
import requests

from constants import TWITCH_OAUTH_LINK, CLIENT_ID, SCOPES, REDIRECT_URI, RESPONSE_TYPE, TWITCH_VALIDATE_LINK, TWITCH_LIVE_FOLLOWED_LINK, V5_JSON, MSG_ACCESS_TOKEN, \
    TITLE_ACCESS_TOKEN, TWITCH_USER_FOLLOWS_LINK
from sanitize import sanitize
from stream import Stream

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
    headers = {
        "Authorization": "OAuth " + currentOAuth
    }
    response = requests.get(TWITCH_VALIDATE_LINK, headers=headers)
    print(response.text)
    return "client_id" in response.text

def getUserID(oAuth: str) -> str:
    headers = {
        "Authorization": "OAuth " + oAuth
    }
    response = requests.get(TWITCH_VALIDATE_LINK, headers=headers)
    return json.loads(response.text)["user_id"]

def getLiveFollowedStreams(oAuth: str) -> List[Stream]:
    user_id = getUserID(oAuth)
    usersFollowedStreams = getAllStreamsUserFollows(oAuth, user_id)
    return getLiveStreamsUserFollows(oAuth, usersFollowedStreams)

def getLiveStreamsUserFollows(oAuth: str, streams: List[List[str]]) -> List[Stream]:
    headers = {
        "Authorization": "Bearer " + oAuth,
        "Client-ID": CLIENT_ID,
    }
    for streamBatch in streams:
        params = {
            "user_id": streamBatch
        }
        response = requests.get(TWITCH_LIVE_FOLLOWED_LINK, headers=headers, params=params)
        jsonStreams = json.loads(response.text)
        # TODO: This shit whack yo, a million queries in one but we at least got it to return the live streams
        # for x in jsonStreams['data']:
        #     print(x)
        # if jsonStreams['data'] is not None:
        #     for stream in jsonStreams['data']:
        #         gameTitle = sanitize(stream['game'])
        #         previewImage = stream['preview']['medium']
        #         streamName = sanitize(stream['channel']["name"])
        #         streamTitle = sanitize(stream['channel']['status'])
        #         stylizedStreamName = stream['channel']['display_name']
        #         viewerCount = sanitize(str(stream['viewer_count']))
        #         liveStreams.append(Stream(gameTitle, previewImage, streamName, streamTitle, stylizedStreamName, viewerCount))
    # print(liveStreams)

def getAllStreamsUserFollows(oAuth, user_id) -> List[List[str]]:
    headers = {
        "Authorization": "Bearer " + oAuth,
        "Client-ID": CLIENT_ID,
    }
    params = {
        "from_id": user_id,
        "first": 100
    }
    moreStreams = True
    usersFollowedStreams = []
    while moreStreams:
        response = requests.get(TWITCH_USER_FOLLOWS_LINK, headers=headers, params=params)
        jsonStreams = json.loads(response.text)
        for stream in jsonStreams["data"]:
            usersFollowedStreams.append(stream['to_id'])
        try:
            params["after"] = jsonStreams["pagination"]["cursor"]
        except KeyError:
            moreStreams = False
    return [usersFollowedStreams[i:i+100] for i in range(0, len(usersFollowedStreams), 100)]
