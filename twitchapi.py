import json
import sys
import webbrowser
from typing import List

import easygui
import requests

from constants.fileConstants import FILE_OAUTH
from constants.linkConstants import TWITCH_VALIDATE_LINK, TWITCH_OAUTH_LINK, TWITCH_USER_FOLLOWS_LINK, TWITCH_LIVE_FOLLOWED_LINK, TWITCH_GAME_INFO_LINK, REDIRECT_URI
from constants.messageConstants import MSG_ACCESS_TOKEN
from constants.miscConstants import BEARER, CLIENT_ID, OAUTH, SCOPES, RESPONSE_TYPE, TITLE_ACCESS_TOKEN
from sanitize import sanitize
from stream import Stream

def authorize() -> str:
    oauthURL = TWITCH_OAUTH_LINK + "?&scope=" + SCOPES + "&response_type=" + RESPONSE_TYPE + "&client_id=" + CLIENT_ID + "&redirect_uri=" + REDIRECT_URI
    webbrowser.open(oauthURL, new=2)
    while 1:
        value = easygui.enterbox(msg=MSG_ACCESS_TOKEN, title=TITLE_ACCESS_TOKEN, strip=True)
        if value is None:
            sys.exit(1)
        with open(FILE_OAUTH, "w") as f:
            f.write(value)
        if validateOAuth():
            return value

def validateOAuth() -> bool:
    with open(FILE_OAUTH, "r") as f:
        currentOAuth = f.read().rstrip()
    if not currentOAuth:
        return False
    headers = {
        "Authorization": OAUTH + currentOAuth
    }
    response = requests.get(TWITCH_VALIDATE_LINK, headers=headers)
    return "client_id" in response.text

def getUserID(oAuth: str) -> str:
    headers = {
        "Authorization": OAUTH + oAuth
    }
    response = requests.get(TWITCH_VALIDATE_LINK, headers=headers)
    return json.loads(response.text)["user_id"]

def getGameInformation(oAuth: str, games: List[str]) -> List:
    headers = {
        "Authorization": BEARER + oAuth,
        "Client-ID": CLIENT_ID,
    }
    params = {
        "id": games
    }
    response = requests.get(TWITCH_GAME_INFO_LINK, headers=headers, params=params)
    return json.loads(response.text)

def getLiveFollowedStreams(oAuth: str, streams: List[List[dict]]) -> List[Stream]:
    headers = {
        "Authorization": BEARER + oAuth,
        "Client-ID": CLIENT_ID,
    }
    liveStreams = []
    for streamBatch in streams:
        params = {
            "user_id": [stream['to_id'] for stream in streamBatch]
        }
        response = requests.get(TWITCH_LIVE_FOLLOWED_LINK, headers=headers, params=params)
        jsonStreams = json.loads(response.text)
        if jsonStreams['data'] is not None:
            gameIDs = []
            for stream in jsonStreams['data']:
                gameIDs.append(stream['game_id'])
            gameIDs = list(set(gameIDs))
            gameInformation = getGameInformation(oAuth, gameIDs)
            for stream in jsonStreams['data']:
                try:
                    game = [game for game in gameInformation['data'] if game['id'] == stream['game_id']][0]
                    gameTitle = game['name']
                    boxArtURL = game['box_art_url'].replace('{width}', '52').replace('{height}', '72')
                except IndexError:
                    gameTitle = "N/A"
                    boxArtURL = ""
                streamTitle = sanitize(stream['title'])
                previewImage = sanitize(stream['thumbnail_url'].replace('{width}', '320').replace('{height}', '180'))
                viewerCount = sanitize(str(stream['viewer_count']))
                gameTitle = sanitize(gameTitle)
                streamName = sanitize(stream['thumbnail_url'][52:].split('-')[0])
                stylizedStreamName = sanitize(stream['user_name'])
                liveStreams.append(Stream(gameTitle, previewImage, streamName, streamTitle, stylizedStreamName, viewerCount, boxArtURL))
    liveStreams.sort(key=lambda x: int(x.viewerCount), reverse=True)
    return liveStreams

def getAllStreamsUserFollows(oAuth, user_id) -> List[dict]:
    headers = {
        "Authorization": BEARER + oAuth,
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
            usersFollowedStreams.append(dict((x, stream[x]) for x in ("to_id", "to_name")))
        try:
            params["after"] = jsonStreams["pagination"]["cursor"]
        except KeyError:
            moreStreams = False
    return usersFollowedStreams

def isRecognizedTwitchGame(oAuth, game) -> bool:
    headers = {
        "Authorization": BEARER + oAuth,
        "Client-ID": CLIENT_ID,
    }
    params = {
        "name": game
    }
    response = requests.get(TWITCH_GAME_INFO_LINK, headers=headers, params=params)
    jsonResponse = json.loads(response.text)
    return jsonResponse["data"]
