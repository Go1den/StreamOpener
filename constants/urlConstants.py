from collections import OrderedDict

from constants.labelConstants import LabelConstants

class URLConstants:
    DISCORD = "https://discord.gg/T4nykvK"
    GITHUB = "https://github.com/Go1den/StreamOpener/issues"
    TWITCH_VALIDATE = "https://id.twitch.tv/oauth2/validate"
    TWITCH_OAUTH = "https://id.twitch.tv/oauth2/authorize"
    TWITCH_USER_FOLLOWS = "https://api.twitch.tv/helix/users/follows"
    TWITCH_LIVE_FOLLOWED = "https://api.twitch.tv/helix/streams"
    TWITCH_GAME_INFO = "https://api.twitch.tv/helix/games"
    TWITCH = "https://twitch.tv/"
    TWITCH_GO1DEN_SUBSCRIBE = 'https://www.twitch.tv/products/go1den'
    TWITCH_MY_WEBSITE = 'https://www.go1den.com'
    REDIRECT_URI = "http://www.go1den.com/streamopener-oauth/"
    KADGAR = "https://kadgar.net/live/"
    MULTISTREAM = "https://multistre.am/"
    MULTITWITCH = "https://multitwitch.tv/"
    TWITCHTHEATER = "https://twitchtheater.tv/"

    ORDERED_STREAMING_SITES = OrderedDict()
    ORDERED_STREAMING_SITES[LabelConstants.URL_TWITCH] = TWITCH
    ORDERED_STREAMING_SITES[LabelConstants.URL_KADGAR] = KADGAR
    ORDERED_STREAMING_SITES[LabelConstants.URL_MULTISTREAM] = MULTISTREAM
    ORDERED_STREAMING_SITES[LabelConstants.URL_MULTITWITCH] = MULTITWITCH
    ORDERED_STREAMING_SITES[LabelConstants.URL_TWITCHTHEATER] = TWITCHTHEATER