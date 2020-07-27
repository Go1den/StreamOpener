from twitchapi import getUserID

class Credentials:
    def __init__(self, oAuth=None):
        self.oauth = oAuth
        self.user_id = getUserID(self.oauth)