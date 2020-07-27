import json
from collections import OrderedDict
from json import JSONDecodeError
from typing import List

from constants import FILE_TEAMS, LABEL_ALL_TEAM, FILE_SETTINGS

def readTeams(followedStreams: List[dict]) -> OrderedDict:
    allTeam = [stream["to_name"] for stream in followedStreams]
    result = OrderedDict()
    result["All"] = sorted(allTeam, key=str.casefold)
    try:
        with open(FILE_TEAMS, "r") as f:
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
        if item[0] != LABEL_ALL_TEAM:
            teamsDict["teams"][item[0]] = item[1]
    jsonTeams = json.dumps(teamsDict, indent=2)
    with open(FILE_TEAMS, "w") as f:
        f.write(jsonTeams)

def readSettings():
    try:
        with open(FILE_SETTINGS, "r") as f:
            settingsJson = f.read()
        settings = json.loads(settingsJson)
        return settings
    except JSONDecodeError:
        return {"settings": {}}
    except FileNotFoundError:
        return {"settings": {}}

def writeSettings(settings: dict):
    jsonSettings = json.dumps(settings, indent=2)
    with open(FILE_SETTINGS, "w") as f:
        f.write(jsonSettings)
