from collections import OrderedDict

CLIENT_ID = "dzdcecm2nwr4j6ywb349cyvv81i9sv"

STREAMOPENER_ICON = 'streamopenericon.ico'

BEARER = "Bearer "

TWITCH_VALIDATE_LINK = "https://id.twitch.tv/oauth2/validate"
TWITCH_OAUTH_LINK = "https://id.twitch.tv/oauth2/authorize"
TWITCH_USER_FOLLOWS_LINK = "https://api.twitch.tv/helix/users/follows"
TWITCH_LIVE_FOLLOWED_LINK = "https://api.twitch.tv/helix/streams"
TWITCH_GAME_INFO_LINK = "https://api.twitch.tv/helix/games"
TWITCH_LINK = "https://twitch.tv/"
SCOPES = "user_read"
RESPONSE_TYPE = "token"
REDIRECT_URI = "http://www.go1den.com/streamopener-oauth/"
V5_JSON = "application/vnd.twitchtv.v5+json"

ORDERED_STREAMING_SITES = OrderedDict()
ORDERED_STREAMING_SITES['Kadgar'] = "https://kadgar.net/live/"
ORDERED_STREAMING_SITES['MultiStream'] = "https://multistre.am/"
ORDERED_STREAMING_SITES['MultiTwitch'] = "https://multitwitch.tv/"
ORDERED_STREAMING_SITES['TwitchTheater'] = "https://twitchtheater.tv/"

MSG_ACCESS_TOKEN = "Please enter the access_token from the URL you were redirected to."
TITLE_ACCESS_TOKEN = "Enter Access Token"

MSG_SELECT_STREAMS = "Choose the streams you want to watch:"
TITLE_SELECT_STREAMS = "Select Streams"

MSG_SELECT_SITE = "Choose the website you want to watch these streams on:"
TITLE_SELECT_SITE = "Select Website"

MSG_WATCH_ON_TWITCH = "Only one stream was selected. Would you like to watch on Twitch instead of your selected site?"
MSG_NO_SITE_SELECTED = "No website selected."
MSG_NO_STREAMS_SELECTED = "No streams selected."

LABEL_NO_TITLE = "Title will appear here."
LABEL_STREAM_DROPDOWN = "Open streams on:"
LABEL_STREAMOPENER = "StreamOpener"
LABEL_GAME = "Game: "
LABEL_STREAMER = "Streamer: "
LABEL_VIEWERS = "Viewers: "
LABEL_TWITCH = "Twitch"
LABEL_ERROR = "Error"

FILE_PREVIEW_BOX_ART = "previewboxart.png"
FILE_STREAM_PREVIEW = "streampreview.png"