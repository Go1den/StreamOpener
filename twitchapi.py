import json
import sys
import webbrowser
from json import JSONDecodeError
from typing import List

import easygui
import requests

from constants.fileConstants import FileConstants
from constants.messageConstants import MessageConstants
from constants.miscConstants import MiscConstants
from constants.urlConstants import URLConstants
from sanitize import sanitize
from stream import Stream
from tag import Tag

def authorize() -> str:
    oauthURL = URLConstants.TWITCH_OAUTH + "?&scope=" + MiscConstants.SCOPES + "&response_type=" + MiscConstants.RESPONSE_TYPE + "&client_id=" + MiscConstants.CLIENT_ID + "&redirect_uri=" + URLConstants.REDIRECT_URI
    webbrowser.open(oauthURL, new=2)
    while 1:
        value = easygui.enterbox(msg=MessageConstants.ACCESS_TOKEN, title=MiscConstants.TITLE_ACCESS_TOKEN, strip=True)
        if value is None:
            sys.exit(1)
        with open(FileConstants.OAUTH, "w") as f:
            f.write(value)
        if validateOAuth():
            return value

def validateOAuth() -> bool:
    with open(FileConstants.OAUTH, "r") as f:
        currentOAuth = f.read().rstrip()
    if not currentOAuth:
        return False
    headers = {
        "Authorization": MiscConstants.OAUTH + currentOAuth
    }
    response = requests.get(URLConstants.TWITCH_VALIDATE, headers=headers)
    return "client_id" in response.text

def getUserID(oAuth: str) -> str:
    headers = {
        "Authorization": MiscConstants.OAUTH + oAuth
    }
    response = requests.get(URLConstants.TWITCH_VALIDATE, headers=headers)
    return json.loads(response.text)["user_id"]

def getGameInformation(oAuth: str, games: List[str]) -> List:
    headers = getAuthorizedHeader(oAuth)
    params = {
        "id": games
    }
    response = requests.get(URLConstants.TWITCH_GAME_INFO, headers=headers, params=params)
    return json.loads(response.text)

def getLiveFollowedStreams(oAuth: str, streams: List[List[dict]]) -> List[Stream]:
    headers = getAuthorizedHeader(oAuth)
    liveStreams = []
    for streamBatch in streams:
        params = {
            "user_id": [stream['to_id'] for stream in streamBatch]
        }
        response = requests.get(URLConstants.TWITCH_LIVE_FOLLOWED, headers=headers, params=params)
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
                gameTitle = sanitize(gameTitle)
                liveStreams.append(Stream(stream, gameTitle, boxArtURL))
    liveStreams.sort(key=lambda x: int(x.viewerCount), reverse=True)
    return liveStreams

def getTopTwitchStreams(credentials) -> List[Stream]:
    headers = getAuthorizedHeader(credentials.oauth)
    params = {
        "first": 99
    }
    topTwitchStreams = []
    response = requests.get(URLConstants.TWITCH_LIVE_FOLLOWED, headers=headers, params=params)
    jsonStreams = json.loads(response.text)
    if jsonStreams['data'] is not None:
        gameIDs = []
        for stream in jsonStreams['data']:
            gameIDs.append(stream['game_id'])
        gameIDs = list(set(gameIDs))
        gameInformation = getGameInformation(credentials.oauth, gameIDs)
        for stream in jsonStreams['data']:
            try:
                game = [game for game in gameInformation['data'] if game['id'] == stream['game_id']][0]
                gameTitle = game['name']
                boxArtURL = game['box_art_url'].replace('{width}', '52').replace('{height}', '72')
            except IndexError:
                gameTitle = "N/A"
                boxArtURL = ""
            gameTitle = sanitize(gameTitle)
            topTwitchStreams.append(Stream(stream, gameTitle, boxArtURL))
    return topTwitchStreams

def getAllStreamsUserFollows(credentials) -> List[dict]:
    headers = getAuthorizedHeader(credentials.oauth)
    params = {
        "from_id": credentials.user_id,
        "first": 100
    }
    moreStreams = True
    usersFollowedStreams = []
    while moreStreams:
        response = requests.get(URLConstants.TWITCH_USER_FOLLOWS, headers=headers, params=params)
        jsonStreams = json.loads(response.text)
        for stream in jsonStreams["data"]:
            usersFollowedStreams.append(dict((x, stream[x]) for x in ("to_id", "to_name")))
        try:
            params["after"] = jsonStreams["pagination"]["cursor"]
        except KeyError:
            moreStreams = False
    return usersFollowedStreams

def updateTwitchTags(oAuth, existingTags: List[Tag], isWritingToFile: bool) -> List[Tag]:
    headers = getAuthorizedHeader(oAuth)
    params = {}
    moreTags = True
    tags = existingTags
    while moreTags:
        response = requests.get(URLConstants.TWITCH_ALL_TAGS, headers=headers, params=params)
        jsonTags = json.loads(response.text)
        for tag in jsonTags["data"]:
            if tag["tag_id"] not in [t.id for t in tags]:
                tags.append(Tag(tag))
        try:
            params["after"] = jsonTags["pagination"]["cursor"]
        except KeyError:
            moreTags = False
    if isWritingToFile:
        writeTags(tags)
    return sorted(tags, key=lambda x: x.localizationNames["en-us"].casefold())

def readTags(oAuth) -> List[Tag]:
    try:
        with open(FileConstants.TAGS, "r") as f:
            tagsJson = f.read()
        tags = json.loads(tagsJson)
        tagList = [Tag(None, t["id"], t["isAuto"], t["localizationNames"], t["isActive"]) for t in tags]
        return sorted(tagList, key=lambda x: x.localizationNames["en-us"].casefold())
    except JSONDecodeError:
        return updateTwitchTags(oAuth, [], True)
    except FileNotFoundError:
        return updateTwitchTags(oAuth, [], True)

def writeTags(tags: List[Tag]):
    j = json.dumps([tag.__dict__ for tag in tags], indent=2)
    with open(FileConstants.TAGS, "w") as f:
        f.write(j)

def isRecognizedTwitchGame(oAuth, game) -> bool:
    headers = getAuthorizedHeader(oAuth)
    params = {
        "name": game
    }
    response = requests.get(URLConstants.TWITCH_GAME_INFO, headers=headers, params=params)
    jsonResponse = json.loads(response.text)
    return jsonResponse["data"]

def getAuthorizedHeader(oAuth: str) -> dict:
    return {
        "Authorization": MiscConstants.BEARER + oAuth,
        "Client-ID": MiscConstants.CLIENT_ID,
    }
