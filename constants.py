from collections import OrderedDict

CLIENT_ID = "dzdcecm2nwr4j6ywb349cyvv81i9sv"

TWITCH_VALIDATE_LINK = "https://id.twitch.tv/oauth2/validate"
TWITCH_OAUTH_LINK = "https://id.twitch.tv/oauth2/authorize"
TWITCH_LIVE_FOLLOWED_LINK = "https://api.twitch.tv/kraken/streams/followed"
SCOPES = "user_read"
RESPONSE_TYPE = "token"
REDIRECT_URI = "http://www.go1den.com/streamopener-oauth/"
V5_JSON = "application/vnd.twitchtv.v5+json"

ORDERED_STREAMING_SITES = OrderedDict()
ORDERED_STREAMING_SITES['Kadgar'] = "https://kadgar.net/live/"
ORDERED_STREAMING_SITES['MultiTwitch'] = "https://multitwitch.tv/"
ORDERED_STREAMING_SITES['TwitchTheater'] = "https://twitchtheater.tv/"

MSG_ACCESS_TOKEN = "Please enter the access_token from the URL you were redirected to."
TITLE_ACCESS_TOKEN = "Enter Access Token"

MSG_SELECT_STREAMS = "Choose the streams you want to watch:"
TITLE_SELECT_STREAMS = "Select Streams"

MSG_SELECT_SITE = "Choose the website you want to watch these streams on:"
TITLE_SELECT_SITE = "Select Website"
