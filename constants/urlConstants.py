from collections import OrderedDict

from constants.labelConstants import LabelConstants

class URLConstants:
    DISCORD_LINK = "https://discord.gg/nqWxgHm"
    GITHUB_LINK = "https://github.com/Go1den/StreamOpener/issues"
    TWITCH_VALIDATE_LINK = "https://id.twitch.tv/oauth2/validate"
    TWITCH_OAUTH_LINK = "https://id.twitch.tv/oauth2/authorize"
    TWITCH_USER_FOLLOWS_LINK = "https://api.twitch.tv/helix/users/follows"
    TWITCH_LIVE_FOLLOWED_LINK = "https://api.twitch.tv/helix/streams"
    TWITCH_GAME_INFO_LINK = "https://api.twitch.tv/helix/games"
    TWITCH_LINK = "https://twitch.tv/"
    TWITCH_GO1DEN_SUBSCRIBE_LINK = 'https://www.twitch.tv/products/go1den'
    TWITCH_MY_WEBSITE = 'https://www.go1den.com'
    REDIRECT_URI = "http://www.go1den.com/streamopener-oauth/"
    URL_KADGAR = "https://kadgar.net/live/"
    URL_MULTISTREAM = "https://multistre.am/"
    URL_MULTITWITCH = "https://multitwitch.tv/"
    URL_TWITCHTHEATER = "https://twitchtheater.tv/"

    ORDERED_STREAMING_SITES = OrderedDict()
    ORDERED_STREAMING_SITES[LabelConstants.LABEL_URL_TWITCH] = TWITCH_LINK
    ORDERED_STREAMING_SITES[LabelConstants.LABEL_URL_KADGAR] = URL_KADGAR
    ORDERED_STREAMING_SITES[LabelConstants.LABEL_URL_MULTISTREAM] = URL_MULTISTREAM
    ORDERED_STREAMING_SITES[LabelConstants.LABEL_URL_MULTITWITCH] = URL_MULTITWITCH
    ORDERED_STREAMING_SITES[LabelConstants.LABEL_URL_TWITCHTHEATER] = URL_TWITCHTHEATER