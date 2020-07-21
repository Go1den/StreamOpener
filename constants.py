from collections import OrderedDict

BEARER = "Bearer "
CLIENT_ID = "dzdcecm2nwr4j6ywb349cyvv81i9sv"

DISCORD_LINK = "https://discord.gg/nqWxgHm"
GITHUB_LINK = "https://github.com/Go1den/StreamOpener/issues"
TWITCH_VALIDATE_LINK = "https://id.twitch.tv/oauth2/validate"
TWITCH_OAUTH_LINK = "https://id.twitch.tv/oauth2/authorize"
TWITCH_USER_FOLLOWS_LINK = "https://api.twitch.tv/helix/users/follows"
TWITCH_LIVE_FOLLOWED_LINK = "https://api.twitch.tv/helix/streams"
TWITCH_GAME_INFO_LINK = "https://api.twitch.tv/helix/games"
TWITCH_LINK = "https://twitch.tv/"

SCOPES = "user_read"
RESPONSE_TYPE = "token"
REDIRECT_URI = "http://www.go1den.com/streamopener-oauth/"

ORDERED_STREAMING_SITES = OrderedDict()
ORDERED_STREAMING_SITES['Kadgar'] = "https://kadgar.net/live/"
ORDERED_STREAMING_SITES['MultiStream'] = "https://multistre.am/"
ORDERED_STREAMING_SITES['MultiTwitch'] = "https://multitwitch.tv/"
ORDERED_STREAMING_SITES['TwitchTheater'] = "https://twitchtheater.tv/"

MSG_ACCESS_TOKEN = "Please enter the access_token from the URL you were redirected to."
TITLE_ACCESS_TOKEN = "Enter Access Token"

MSG_WATCH_ON_TWITCH = "Only one stream was selected. Would you like to watch on Twitch instead of your selected site?"
MSG_NO_SITE_SELECTED = "No website selected."
MSG_NO_STREAMS_SELECTED = "No streams selected."

LABEL_NO_TITLE = "Select a Live Stream to view details."
LABEL_STREAM_DROPDOWN = "Open streams on:"
LABEL_STREAMOPENER = "StreamOpener"
LABEL_GAME = "Game: "
LABEL_STREAMER = "Streamer: "
LABEL_VIEWERS = "Viewers: "
LABEL_TWITCH = "Twitch"
LABEL_ERROR = "Error"
LABEL_LIVE_STREAMS = "Live Streams"
LABEL_SELECTED_STREAMS = "Selected Streams"
LABEL_REFRESH = "Refresh"
LABEL_RESET = "Reset"
LABEL_LEFT = "<--"
LABEL_RIGHT = "-->"
LABEL_OPEN_STREAMS = "Take me to the streams!"
LABEL_PREVIEW = "Preview"

FILE_PREVIEW_BOX_ART = "previewboxart.png"
FILE_STREAM_PREVIEW = "streampreview.png"
STREAMOPENER_ICON = 'streamopenericon.ico'
