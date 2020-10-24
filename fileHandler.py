import json
from collections import OrderedDict
from json import JSONDecodeError
from typing import List

from constants.fileConstants import FileConstants
from constants.labelConstants import LabelConstants
from constants.miscConstants import MiscConstants

def readTeams(followedStreams: List[dict]) -> OrderedDict:
    allTeam = [stream["to_name"] for stream in followedStreams]
    result = OrderedDict()
    result["All"] = sorted(allTeam, key=str.casefold)
    try:
        with open(FileConstants.TEAMS, "r") as f:
            teamsJson = f.read()
        teams = json.loads(teamsJson)
        for team in sorted(teams['teams'], key=str.casefold):
            result[team] = teams['teams'][team]
    except JSONDecodeError:
        pass
    except FileNotFoundError:
        pass
    return result

def writeTeams(teams: OrderedDict):
    teamsDict = {"teams": {}}
    for item in teams.items():
        if item[0] != LabelConstants.ALL_TEAM:
            teamsDict["teams"][item[0]] = item[1]
    jsonTeams = json.dumps(teamsDict, indent=2)
    with open(FileConstants.TEAMS, "w") as f:
        f.write(jsonTeams)

def readSettings():
    try:
        with open(FileConstants.SETTINGS, "r") as f:
            settingsJson = f.read()
        settings = json.loads(settingsJson)
        return populateMissingSettings(settings)
    except JSONDecodeError:
        return populateMissingSettings({"settings": {}})
    except FileNotFoundError:
        return populateMissingSettings({"settings": {}})

# TODO add remove unused settings method

def populateMissingSettings(settings) -> dict:
    if MiscConstants.KEY_OPEN_STREAMS_ON not in settings["settings"]:
        settings["settings"][MiscConstants.KEY_OPEN_STREAMS_ON] = LabelConstants.URL_TWITCH
    if MiscConstants.KEY_HIDE_THUMBNAIL not in settings["settings"]:
        settings["settings"][MiscConstants.KEY_HIDE_THUMBNAIL] = False
    if MiscConstants.KEY_SELECTION_MODE not in settings["settings"]:
        settings["settings"][MiscConstants.KEY_SELECTION_MODE] = "single"
    if MiscConstants.KEY_TEAM not in settings["settings"]:
        settings["settings"][MiscConstants.KEY_TEAM] = LabelConstants.ALL_TEAM
    if MiscConstants.KEY_FILTERS not in settings["settings"]:
        settings["settings"][MiscConstants.KEY_FILTERS] = False
    return settings

def writeSettings(settings: dict):
    jsonSettings = json.dumps(settings, indent=2)
    with open(FileConstants.SETTINGS, "w") as f:
        f.write(jsonSettings)

def readFilters() -> dict:
    try:
        with open(FileConstants.FILTERS, "r") as f:
            filtersJson = f.read()
        filters = json.loads(filtersJson)
        return filters
    except JSONDecodeError:
        return {"filters": {"streamer": [], "combined": [], "game": []}}
    except FileNotFoundError:
        return {"filters": {"streamer": [], "combined": [], "game": []}}

def writeFilters(settings: dict):
    filtersJson = json.dumps(settings, indent=2)
    with open(FileConstants.FILTERS, "w") as f:
        f.write(filtersJson)
